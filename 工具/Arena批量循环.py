# -*- coding: utf-8 -*-
"""外层循环：自动一批接一批地跑，直到所有来源整理完或 Arena 额度耗尽。

用法: python Arena批量循环.py [每组份数, 默认4] [起始批号, 可选]

每轮：
  1. 调 阶段C_取批.py 取下一批 20 份
  2. 调 Arena驱动_连续抽取.py <批号> <每组份数>
  3. 统计该批完成情况；未完成的会在下一轮被驱动自动重试（驱动只看台账「已抽取」）
  4. 若额度耗尽 / 连续两批零进展 → 停止
日志: C:/tmp/arena_loop.log
"""
import json
import pathlib
import re
import subprocess
import sys
import time
import urllib.request

OUT = pathlib.Path(r'C:\Users\赵豪\dsh\交易知识体系汇编')
LOG = pathlib.Path('C:/tmp/arena_loop.log')

GROUP = sys.argv[1] if len(sys.argv) > 1 else '2'   # 2026-09-30 实测附件上限=2，4份会卡 Updating
START = sys.argv[2] if len(sys.argv) > 2 else None
# 2026-10-06 用户要求：每跑满 GROUPS_PER_DRAW 组对话，就抽 DRAW_ROUNDS 轮卡，反复交替。
# 目的：持续把「新鲜、轻量、已验证旗舰」的会话灌进池子。同一个会话涨到几十万字符后
# 会出现发送键卡死、回复被静默丢弃、单组要等十几分钟——定期换新的能把这类退化摊平。
# 两个都可从命令行覆盖：python Arena批量循环.py 2 <起始批> 5 10
#
# 2026-10-07 用户要求把间隔从 10 组缩到 5 组：实测会话跑到 245K~340K 字符时，
# 「发送键卡死（SENDFAIL）」和「页面报错（BUSY）」明显变密（01a111c6 到 250K 时
# 连续两轮失败），而池子里又只有 1 条可用备用会话——缩短间隔能更快把重会话换掉。
# 改默认值而不是改启动参数：看门狗拉起循环时用的是 `Arena批量循环.py 2`（不带第 3 参），
# 只改命令行的话，看门狗重启一次就退回旧值。
GROUPS_PER_DRAW = int(sys.argv[3]) if len(sys.argv) > 3 else 5
DRAW_ROUNDS = int(sys.argv[4]) if len(sys.argv) > 4 else 10
groups_since_draw = 0

def allowed_batches():
    """三路分工时约束本循环只跑自己的份额。
    C:/tmp/arena_batches_allow.txt 每行一个批号或范围（如 24-77），不存在则不限。"""
    p = pathlib.Path('C:/tmp/arena_batches_allow.txt')
    if not p.exists():
        return None
    nums = set()
    for ln in p.read_text(encoding='utf-8').splitlines():
        ln = ln.strip()
        if not ln or ln.startswith('#'):
            continue
        if '-' in ln:
            a, b = ln.split('-', 1)
            nums.update(range(int(a), int(b) + 1))
        else:
            nums.add(int(ln))
    return nums

ALLOW = allowed_batches()


def log(m):
    line = '[%s] %s' % (time.strftime('%m-%d %H:%M:%S'), m)
    print(line, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def done_count():
    lines = (OUT / '01_资料与索引/来源去向.tsv').read_text(encoding='utf-8').splitlines()
    h = lines[0].split('\t')
    sti = h.index('处理状态')
    return sum(1 for l in lines[1:] if len(l.split('\t')) > sti and l.split('\t')[sti] == '已抽取')


def done_set():
    lines = (OUT / '01_资料与索引/来源去向.tsv').read_text(encoding='utf-8').splitlines()
    h = lines[0].split('\t')
    si = h.index('source_id')
    sti = h.index('处理状态')
    s = set()
    for l in lines[1:]:
        c = l.split('\t')
        if len(c) > sti and c[sti] in {'已抽取', '工具脚本·无可用内容', '无可用交易内容'}:
            s.add(c[si])
    return s


def cards():
    n = 0
    for d in ('02_知识点', '03_方法与策略', '04_案例'):
        n += len(list((OUT / d).glob('*.md')))
    return n


def next_batch_num():
    nums = []
    for p in (OUT / '工作分片').glob('批*_清单.tsv'):
        m = re.match(r'批(\d+)', p.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums) + 1 if nums else 1


ALL_MODELS = ['claude-opus-5-5', 'claude-fable-5-1', 'gpt-6-astra']   # 2026-09-30 用户指定 3 个旗舰（去掉 gpt-6.1-sol，太慢）
BUSY_FLAG = pathlib.Path('C:/tmp/arena_busy.flag')
ROTATE_FLAG = pathlib.Path('C:/tmp/arena_rotate.flag')
MODEL_FILE = pathlib.Path('C:/tmp/arena_model.txt')
SESSION_FILE = pathlib.Path('C:/tmp/arena_session.txt')
PIN_FILE = pathlib.Path('C:/tmp/arena_pin_session.txt')
SKILL = pathlib.Path(r'C:\Users\赵豪\.agents\skills\arena-flagship\scripts')


def apply_session_pin():
    if not PIN_FILE.exists():
        return ''
    sid = PIN_FILE.read_text(encoding='utf-8-sig').strip()
    bad = set(pathlib.Path('C:/tmp/arena_bad_sessions.txt').read_text(encoding='utf-8').split()) if pathlib.Path('C:/tmp/arena_bad_sessions.txt').exists() else set()
    if not sid or sid in bad:
        PIN_FILE.unlink(missing_ok=True)
        log('固定会话已报错，取消锁定: %s' % (sid or '(空)'))
        return ''
    if not re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}', sid):
        raise ValueError('Invalid pinned Arena session id')
    import json
    pool = json.loads(pathlib.Path('C:/tmp/flagship_pool.json').read_text(encoding='utf-8-sig'))
    match = next((item for item in pool if item.get('sid') == sid), None)
    if not match or match.get('model') not in ALL_MODELS:
        raise ValueError('Pinned session is not in the verified flagship pool')
    if not SESSION_FILE.exists() or SESSION_FILE.read_text(encoding='utf-8-sig').strip() != sid:
        SESSION_FILE.write_text(sid, encoding='utf-8')
    model = match['model']
    if not MODEL_FILE.exists() or MODEL_FILE.read_text(encoding='utf-8-sig').strip() != model:
        MODEL_FILE.write_text(model, encoding='utf-8')
    return sid


ATI_CDP = pathlib.Path('C:/arena-ext/ati-cdp.mjs')


def _hub_keepalive():
    """抽卡期间给 hub 喂一个请求，重置它的 5 分钟闲置时钟，防止 Edge 被回收。
    抽卡全靠扩展内部跑 + ati-cdp 直连 9223，**都不经过 hub**；hub 5 分钟没收到
    客户端请求就把 Edge 闲置回收，抽卡随之被杀、页面重载、抽卡状态清零
    （2026-10-05 实测：抽卡每次都在第 3 轮后死掉，就是这个原因）。
    arena-hub.js 在任何非 /__arena/* 路径的请求到达时即重置时钟，
    所以即使后端返回 405/错误也无所谓——请求到达就算活动。"""
    try:
        urllib.request.urlopen('http://localhost:8931/mcp', timeout=8).read()
    except Exception:
        pass


def _ati_cdp(args, timeout=200):
    """调 ATI 直连 CDP 驱动（绕开可能被堵死的 MCP 后端）。"""
    return subprocess.run(['node', str(ATI_CDP)] + [str(a) for a in args],
                          capture_output=True, text=True, timeout=timeout, cwd=str(ATI_CDP.parent))


def _ati_iso(expr, timeout=120):
    """在扩展隔离世界求值，返回字符串结果（失败返回 ''）。"""
    try:
        r = _ati_cdp(['isolated', expr], timeout=timeout)
        return str(json.loads((r.stdout or '').strip()).get('value') or '').strip()
    except Exception:
        return ''


def _current_agent_sid():
    """从当前页面地址读会话号。
    比 ArenaAutoDraw.status().sessionId 可靠——那个值实测是截断过的（34 位 vs 真实 36 位），
    拿它当会话号会让 URL 拼错、驱动报 SESSION_MISMATCH。"""
    return _ati_iso(r"(() => { const m = location.pathname.match(/\/agent\/([0-9a-f-]{30,})/); return m ? m[1] : ''; })()")


def _draw_into_file(target_model, rounds=16):
    """抽一个目标模型的新会话写入 SESSION_FILE；成功返回 (sid, model)。

    2026-10-04 改用插件的自动抽卡（ArenaAutoDraw，经 ati-cdp.mjs 直连 CDP）。换掉自研
    _mydraw.mjs 的三个原因：
      1. 旧版用 ATI_ACQUIRE 读 view.models[0]，正是调研里判定不可靠的那条路径（单指标、
         还会被未校验的 profile_similarity 重排）；插件版已修成逐探针多数派 + 样本强校验。
      2. 旧版不归档未命中的会话，探针会话越堆越多（实测 8 分钟堆 3 条）。
      3. 旧版一次跑满 16 轮、每轮约 2.5 分钟，而这里 capture_output=True 把输出全缓冲，
         日志长时间空白，看起来像卡死。插件版可以用 poll 实时看到进度。
    """
    pinned = apply_session_pin()
    if pinned:
        return pinned, MODEL_FILE.read_text(encoding='utf-8').strip()
    # 2026-10-06：开抽前必须把页面收拾干净。实测被 Arena 静默丢弃的那一组会在输入框里
    # 留下未发送草稿，插件的自动抽卡检测到「输入框有未发送内容」会直接拒绝启动
    # （不覆盖草稿）；若页面还挂着 Stop generating 按钮，插件报「当前回复仍在生成，
    # 已停止试运行」。两种情况都会让抽卡在 5 秒内空跑完，白烧一轮。
    try:
        subprocess.run(['node', str(SKILL / '_stop.mjs')], capture_output=True, text=True, timeout=200, cwd=str(SKILL))
        subprocess.run(['node', str(SKILL / '清理_输入框.mjs')], capture_output=True, text=True, timeout=200, cwd=str(SKILL))
    except Exception as e:
        log('  抽卡前清理页面失败: %s' % str(e)[:100])
    pat = '/^(%s)$/' % target_model
    try:
        _ati_cdp(['start', rounds, 'probe', pat], timeout=120)
    except Exception as e:
        log('  插件抽卡启动失败: %s' % str(e)[:100])
        return '', ''
    deadline = time.time() + 3000
    hits, last = [], ''
    while time.time() < deadline:
        time.sleep(20)
        _hub_keepalive()   # 每 20 秒喂一次 hub，防止抽卡期间 Edge 被 5 分钟闲置回收
        try:
            r = _ati_cdp(['poll'], timeout=120)
            j = json.loads(json.loads((r.stdout or '').strip()).get('value') or '{}')
        except Exception:
            continue
        last = str(j.get('progress') or '')[:120]
        hits = j.get('hits') or []
        if last:
            log('    抽卡进度: %s' % last)
        if not j.get('running'):
            break
    if not hits:
        log('  插件抽卡未命中 %s（%s）' % (target_model, last))
        return '', ''
    sid = _current_agent_sid()
    if not sid:
        log('  抽卡命中但读不到会话号，放弃本次')
        return '', ''
    SESSION_FILE.write_text(sid, encoding='utf-8')
    log('  插件抽卡命中 %s：%s' % (hits[0], sid[:12]))
    # 2026-10-06：poll 里的 hits 元素**可能是字符串**（"claude-fable-5-1"），也可能是
    # {target, model} 对象，两种都要认。之前只按对象处理，字符串走 .get() 抛
    # AttributeError 被 except 吞掉、回退成传进来的正则模式，于是 arena_model.txt 被写成
    # "claude-opus-5-5|claude-fable-5-1|gpt-6-astra"（23:15 命中 claude-fable-5-1 后实测）。
    real = ''
    for h in hits:
        cand = str((h.get('model') if isinstance(h, dict) else h) or '').strip()
        if cand in ALL_MODELS:          # 白名单校验：模式串/脏值一律不认
            real = cand
            break
    if not real:
        log('  命中但认不出模型名（hits=%s），MODEL_FILE 保持原值' % str(hits)[:80])
    return sid, real


def run_driver(batch):
    """跑一轮驱动，返回驱动 stdout。

    2026-10-06：第三个参数是本轮最多跑几组。循环用「10 组对话 + 10 轮抽卡」交替，
    所以按「离满 10 组还差几组」下闸门，跑满就交回来抽卡；剩下的来源由台账决定，
    下一轮天然续跑（驱动的 todo 只包含台账里还没「已抽取」的来源，不会漏也不会重）。
    """
    global groups_since_draw
    allow = max(1, GROUPS_PER_DRAW - groups_since_draw) if GROUPS_PER_DRAW > 0 else 0
    r = subprocess.run(['python', '-X', 'utf8', str(OUT / '工具/Arena驱动_连续抽取.py'),
                        batch, GROUP, str(allow)],
                       capture_output=True, text=True, timeout=86400, cwd=str(OUT))
    out = r.stdout or ''
    # 驱动每组成功入库打一行「✓ 入库完成」——这就是「完成了几次对话」的准确计数。
    groups_since_draw += out.count('✓ 入库完成')
    return out


def _pool_add(sid, model):
    """把命中的旗舰会话记进「已验证旗舰池」，轮换时免抽卡直接复用（2026-10-06）。

    池格式 [{sid, model, bodyLen, ts}]，轮换按 bodyLen 升序挑最轻的，所以这里量一下
    当前页面正文长度（量不到就记 0，语义是「刚抽到、默认很轻」）。
    """
    import json as _json
    try:
        blen = int(float(_ati_iso('() => document.body.innerText.length') or 0))
    except Exception:
        blen = 0
    p = pathlib.Path('C:/tmp/flagship_pool.json')
    try:
        pool = _json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else []
        if isinstance(pool, dict):
            pool = [pool]
        pool = [x for x in pool if isinstance(x, dict) and x.get('sid') != sid]
        pool.append({'sid': sid, 'model': model, 'bodyLen': blen, 'ts': int(time.time())})
        p.write_text(_json.dumps(pool, ensure_ascii=False, indent=1), encoding='utf-8')
        log('  已记入旗舰池：%s = %s（页长 %d，池内 %d 个）' % (sid[:12], model, blen, len(pool)))
    except Exception as e:
        log('  记入旗舰池失败: %s' % str(e)[:80])


def maybe_periodic_draw():
    """跑满 GROUPS_PER_DRAW 组对话就抽 DRAW_ROUNDS 轮卡，反复交替。

    命中 → _draw_into_file 已把新会话写进 SESSION_FILE，下一轮驱动自动切过去
    （新鲜会话更轻、发送键更稳）；未命中 → 继续用当前会话，不打断流水线。
    """
    global groups_since_draw
    if GROUPS_PER_DRAW <= 0 or groups_since_draw < GROUPS_PER_DRAW:
        return
    log('=== 已完成 %d 组对话 → 开始 %d 轮抽卡（目标：三个旗舰任一个）==='
        % (groups_since_draw, DRAW_ROUNDS))
    groups_since_draw = 0
    sid, model = _draw_into_file('|'.join(ALL_MODELS), DRAW_ROUNDS)
    if sid and model:
        MODEL_FILE.write_text(model, encoding='utf-8')
        _pool_add(sid, model)
        log('抽卡命中 %s，已切到新会话（更轻、发送更稳），下一组就用它' % model)
    elif sid:
        # 命中了但模型名没认出来：会话已经切过去，MODEL_FILE 保持原值（宁可不动，
        # 也不要把正则模式串写进去污染后续轮换顺序）。
        log('抽卡命中但模型名未识别，会话已切到 %s，MODEL_FILE 保持原值' % sid[:12])
    else:
        cur = SESSION_FILE.read_text(encoding='utf-8-sig').strip() if SESSION_FILE.exists() else ''
        log('抽卡未命中，继续用当前会话 %s' % (cur[:12] or '(无)'))


def rotate_session():
    """会话过重时调用：优先复用侧栏现成的轻量旗舰会话，没有再现场抽卡。成功返回 True。"""
    pinned = apply_session_pin()
    if pinned:
        log('固定会话 %s：忽略轮换请求，不导航、不抽卡' % pinned)
        return True
    cur_session = SESSION_FILE.read_text(encoding='utf-8').strip() if SESSION_FILE.exists() else ''
    # 1) 先尝试复用侧栏里现成的全新/轻量旗舰会话（2026-09-30 用户要求）
    fresh = None          # 侧栏挑到的最轻候选，留给第 3 步兜底复用
    try:
        r = subprocess.run(['node', str(SKILL / '_pickFresh.mjs'), cur_session],
                           capture_output=True, text=True, timeout=400, cwd=str(SKILL))
        out = (r.stdout or '').strip()
        log('  现有旗舰会话挑选: %s' % out[:130])
        m = re.match(r'PICK:([a-zA-Z0-9-]+):([^:]+):(\d+)', out)
        if m:
            sid, newmodel, plen = m.group(1), m.group(2), int(m.group(3))
            fresh = (sid, newmodel, plen)
            if plen < 200000:   # 足够轻量才复用，否则仍去抽卡
                SESSION_FILE.write_text(sid, encoding='utf-8')
                MODEL_FILE.write_text(newmodel, encoding='utf-8')
                log('轮换完成（复用现有）: %s = %s（页长 %d）' % (sid[:12], newmodel, plen))
                return True
            log('  现有旗舰会话都偏重（最小 %d），改为现场抽卡' % plen)
        else:
            log('  无可用现有旗舰会话，现场抽卡')
    except Exception as e:
        log('  现有会话挑选失败: %s，改为现场抽卡' % str(e)[:120])
    # 1.5) 用「已验证旗舰池」兜底（2026-10-01 加）：侧栏扫描常常返回 NONE，
    #      现场抽卡要十几分钟且不一定命中白名单。池子是探活过的，直接拿来用最省。
    #      坏会话名单（渲染坏死的）一律跳过。
    try:
        import json as _json
        _poolp = pathlib.Path('C:/tmp/flagship_pool.json')
        _badp = pathlib.Path('C:/tmp/arena_bad_sessions.txt')
        _bad = set(_badp.read_text(encoding='utf-8').split()) if _badp.exists() else set()
        if _poolp.exists():
            # 用 utf-8-sig 读：这个文件可能被 PowerShell 的 Out-File -Encoding utf8
            # 写入而带 BOM（2026-10-05 实测），用纯 utf-8 会直接抛
            # "Unexpected UTF-8 BOM"，把整条池兜底路径打成现场抽卡。
            _pool = _json.loads(_poolp.read_text(encoding='utf-8-sig'))
            if isinstance(_pool, dict):
                _pool = [_pool]   # 容忍写成单个对象的旧格式
            _cand = [p for p in _pool
                     if p.get('sid') and p['sid'] != cur_session and p['sid'] not in _bad
                     and p.get('model') in ALL_MODELS]
            # 2026-10-08 修：bodyLen 快照不可全信——命中时量不到记 0、之后一直不回填，
            # 实测 01a11437 池记录 0、被当最轻选中，接手时真实页长 377K（骨架事故同源问题）。
            # 排序改为：新鲜且有实据的（ts 90 分钟内、bodyLen>0）按页长优先；
            # 陈旧/无据的垫底。驱动侧还有重会话守卫+骨架判据兜底，这里只求少踩雷。
            import time as _t
            def _rank(p):
                fresh = (_t.time() - p.get('ts', 0) < 5400) and p.get('bodyLen', 0) > 0
                return (0 if fresh else 1, p.get('bodyLen', 0))
            _cand.sort(key=_rank)
            if _cand:
                _pick = _cand[0]
                SESSION_FILE.write_text(_pick['sid'], encoding='utf-8')
                MODEL_FILE.write_text(_pick.get('model', ''), encoding='utf-8')
                log('轮换完成（用已验证旗舰池）: %s = %s（池记录页长 %d）'
                    % (_pick['sid'][:12], _pick.get('model'), _pick.get('bodyLen', 0)))
                return True
            log('  池里没有可用候选（%d 个，跳过坏会话 %d 个）' % (len(_pool), len(_bad)))
    except Exception as e:
        log('  池兜底失败: %s，改为现场抽卡' % str(e)[:120])
    # 2) 现场抽卡兜底
    cur = MODEL_FILE.read_text(encoding='utf-8').strip() if MODEL_FILE.exists() else ''
    order = ([cur] + [m for m in ALL_MODELS if m != cur]) if cur in ALL_MODELS else list(ALL_MODELS)
    for m in order:
        log('轮换：抽新会话（目标 %s）' % m)
        try:
            sid, newmodel = _draw_into_file(m)
            if sid and newmodel:
                MODEL_FILE.write_text(newmodel, encoding='utf-8')
                log('轮换完成：%s = %s' % (sid[:12], newmodel))
                return True
            log('轮换抽卡未命中 %s' % m)
        except Exception as e:
            log('轮换抽卡失败(%s): %s' % (m, str(e)[:150]))
    # 3) 最后兜底（2026-10-07 加）：抽卡也拿不到会话时，宁可复用一个偏重的旗舰会话，
    #    也不要让流水线空转。实测 07:19-08:14 连续四次抽卡全部「发送后未确认新会话」
    #    （疑似 Arena 对新建会话限流），而侧栏里 01a111c6(339K)/01a10588(347K) 明明可用，
    #    却因上面那条 >200000 被排除 → 会话指针留在被隔离的坏会话上，空转整整一小时。
    #    上限取驱动的过重阈值 400000：超过它驱动自己也会拒绝切进去。
    if fresh and fresh[2] < 400000:
        sid, newmodel, plen = fresh
        SESSION_FILE.write_text(sid, encoding='utf-8')
        MODEL_FILE.write_text(newmodel, encoding='utf-8')
        log('轮换完成（兜底复用偏重会话）: %s = %s（页长 %d）' % (sid[:12], newmodel, plen))
        return True
    if fresh:
        log('  兜底也放弃：侧栏最轻的会话页长 %d 已超过驱动的过重阈值 400000' % fresh[2])
    return False


def handle_busy():
    """页面明确报错时调用：换一个已验证旗舰会话，不把失败内容入库。"""
    cur = MODEL_FILE.read_text(encoding='utf-8').strip() if MODEL_FILE.exists() else ''
    pinned = PIN_FILE.read_text(encoding='utf-8-sig').strip() if PIN_FILE.exists() else ''
    if pinned:
        # 2026-10-01：Something went wrong 不再死守固定会话。
        # 只解除当前锁并换已验证会话；失败回复仍由驱动拒绝入库。
        PIN_FILE.unlink(missing_ok=True)
        log('固定会话 %s 已报错，解除锁定并切换已验证会话' % pinned)
    log('检测到 busy，当前模型 %s，先从已验证旗舰池切换' % (cur or '(未知)'))
    if rotate_session():
        return True
    cands = [m for m in ALL_MODELS if m != cur]
    if not cands:
        cands = list(ALL_MODELS)
    # 池中没有可用会话时，才现场抽一个新的已验证旗舰会话。
    import random
    random.shuffle(cands)
    pat = '/^(%s)$/' % '|'.join(cands)
    log('旗舰池无可用会话，改为现场抽卡（候选: %s）' % ','.join(cands))
    try:
        # 2026-10-04：改用插件自动抽卡（同 _draw_into_file），不再走自研 _mydraw.mjs。
        sid, newmodel = _draw_into_file('|'.join(cands), rounds=14)
        if sid and newmodel:
            MODEL_FILE.write_text(newmodel, encoding='utf-8')
            log('新会话 %s = %s' % (sid[:12], newmodel))
            return True
    except Exception as e:
        log('抽新会话失败: %s' % str(e)[:200])
    return False


log('=== 批量循环启动 | 每组 %s 份 ===' % GROUP)
_pinned = apply_session_pin()
if _pinned:
    log('固定会话生效: %s = %s' % (_pinned, MODEL_FILE.read_text(encoding='utf-8').strip()))
zero_rounds = 0
rounds = 0
while True:
    rounds += 1
    before = done_count()
    before_cards = cards()
    log('--- 第 %d 轮 | 已抽取 %d | 卡片 %d ---' % (rounds, before, before_cards))

    # 先补跑：任何已建清单但还有未抽取来源的批次（从中最早的一批开始）
    dn = done_set()
    outstanding = []
    import csv as _csv
    for f in sorted((OUT / '工作分片').glob('批*_清单.tsv')):
        m0 = re.match(r'批(\d+)_清单', f.name)
        if not m0:
            continue
        if ALLOW is not None and int(m0.group(1)) not in ALLOW:
            continue
        rows0 = list(_csv.DictReader(open(f, encoding='utf-8'), delimiter='\t'))
        deferred = set()
        deferred_file = pathlib.Path('C:/tmp/arena_deferred_sources.txt')
        if deferred_file.exists():
            deferred = set(x.strip() for x in deferred_file.read_text(encoding='utf-8').split() if x.strip())
        left = [r for r in rows0 if r['source_id'] not in dn and r['source_id'] not in deferred]
        if left:
            outstanding.append((int(m0.group(1)), '批%s' % m0.group(1), len(left)))
    if outstanding:
        outstanding.sort()
        log('待补跑 %d 批；最早: %s' % (len(outstanding), ' | '.join('%s(%d 份)' % (b, n) for _, b, n in outstanding[:5])))
        batch = outstanding[0][1]
        log('本轮补跑 %s' % batch)
        _out = run_driver(batch)
        tail = _out[-1500:]
        for ln in tail.strip().splitlines()[-8:]:
            log('  ' + ln)
        if '额度耗尽' in tail or 'QUOTA' in tail:
            log('=== 额度耗尽，循环结束 ===')
            break
        # 2026-10-09 YG 红线：驱动发现需要人工验证的页面（Try again / Reset session and
        # reload）→ 整条线立即结束。绝不自动重试/换会话——多次触发风控可能封号，
        # 看门狗看到 arena_verify_stop.flag 也不会拉起，直到人工删掉该旗标。
        if '✗ VERIFY' in tail or '需要人工验证' in tail or pathlib.Path('C:/tmp/arena_verify_stop.flag').exists():
            log('=== 页面需要人工验证，循环结束（不重试）。人工处理后删除 C:/tmp/arena_verify_stop.flag 再拉起 ===')
            break
        if ROTATE_FLAG.exists():
            ROTATE_FLAG.unlink(missing_ok=True)
            log('=== 会话过重，轮换新会话 ===')
            if rotate_session():
                log('已轮换，重跑本批 %s' % batch)
                zero_rounds = 0
                continue
            else:
                log('轮换失败，停一轮再看')
        if pathlib.Path('C:/tmp/arena_retry_same.flag').exists():
            pathlib.Path('C:/tmp/arena_retry_same.flag').unlink(missing_ok=True)
            log('页面前置失败，120 秒后重试同一会话')
            time.sleep(120)
            continue
        if BUSY_FLAG.exists():
            BUSY_FLAG.unlink(missing_ok=True)
            if handle_busy():
                log('已换会话，重跑本批 %s' % batch)
                continue
            else:
                log('换会话失败，停一轮再看')
        after = done_count()
        after_cards = cards()
        log('%s 补跑：已抽取 %d → %d（+%d）| 卡片 %d → %d（+%d）'
            % (batch, before, after, after - before, before_cards, after_cards, after_cards - before_cards))
        if after == before and after_cards == before_cards:
            zero_rounds += 1
            log('本轮零进展（第 %d 次）' % zero_rounds)
            if zero_rounds >= 2:
                log('=== 连续两轮零进展，停止 ===')
                break
        else:
            zero_rounds = 0
        # 每跑满 GROUPS_PER_DRAW 组对话 → 抽 DRAW_ROUNDS 轮卡，如此反复
        maybe_periodic_draw()
        time.sleep(15)
        continue

    # 没有欠账了，取新的一批（分工模式下份额外没有新批，直接结束）
    if ALLOW is not None:
        log('=== 本路份额内无欠账，循环结束 ===')
        break
    r = subprocess.run(['python', '-X', 'utf8', str(OUT / '工具/阶段C_取批.py'), '--size', '20'],
                       capture_output=True, text=True, timeout=900, cwd=str(OUT.parent))
    out = (r.stdout or '') + (r.stderr or '')
    if r.returncode != 0:
        log('取批失败: %s' % out[-300:])
        break
    if '没有可取的来源' in out or '无可取来源' in out or '剩余 0' in out:
        log('=== 没有可取的来源了，循环结束 ===')
        break
    m = re.search(r'批(\d+)_清单\.tsv', out)
    if not m:
        log('取批输出里找不到批号，停止。输出尾部: %s' % out[-300:])
        break
    batch = '批%s' % m.group(1)
    log('取到 %s' % batch)

    # 跑这一批
    _out = run_driver(batch)
    tail = _out[-1500:]
    for ln in tail.strip().splitlines()[-8:]:
        log('  ' + ln)
    if '额度耗尽' in tail or 'QUOTA' in tail:
        log('=== 额度耗尽，循环结束 ===')
        break
    if ROTATE_FLAG.exists():
        ROTATE_FLAG.unlink(missing_ok=True)
        log('=== 会话过重，轮换新会话 ===')
        if rotate_session():
            log('已轮换，重跑本批 %s' % batch)
            continue
        else:
            log('轮换失败，停一轮再看')
    if BUSY_FLAG.exists():
        BUSY_FLAG.unlink(missing_ok=True)
        if handle_busy():
            log('已换会话，重跑本批 %s' % batch)
            continue
        else:
            log('换会话失败，停一轮再看')

    after = done_count()
    after_cards = cards()
    log('%s 完成：已抽取 %d → %d（+%d）| 卡片 %d → %d（+%d）'
        % (batch, before, after, after - before, before_cards, after_cards, after_cards - before_cards))
    if after == before and after_cards == before_cards:
        zero_rounds += 1
        log('本轮零进展（第 %d 次）' % zero_rounds)
        if zero_rounds >= 2:
            log('=== 连续两轮零进展，停止（需人工检查会话/额度）===')
            break
    else:
        zero_rounds = 0
    # 每跑满 GROUPS_PER_DRAW 组对话 → 抽 DRAW_ROUNDS 轮卡，如此反复
    maybe_periodic_draw()
    time.sleep(30)

log('=== 批量循环结束 | 共 %d 轮 | 已抽取 %d | 卡片 %d ===' % (rounds, done_count(), cards()))
