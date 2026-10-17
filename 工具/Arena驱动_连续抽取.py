# -*- coding: utf-8 -*-
"""Arena 旗舰会话连续抽取驱动。

每组：备料 → 生成内联提示 → 发进旗舰会话 → 等完成并按锚点抓取
     → 逐条回源验证 → 写卡/追加补充 → 入证据索引 → 复验。
额度耗尽或连续失败即停。
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys
import time

BASE = pathlib.Path(r'C:\Users\赵豪\dsh')
OUT = BASE / '交易知识体系汇编'
SKILL = pathlib.Path(r'C:\Users\赵豪\.agents\skills\arena-flagship\scripts')
SESSION = '01a0ec65-818f-708c-b6f7-d7eaf5a4850b'  # 默认值；若 C:/tmp/arena_session.txt 存在则以该文件为准
_sf = pathlib.Path('C:/tmp/arena_session.txt')
if _sf.exists():
    # utf-8-sig：PowerShell 的 Set-Content -Encoding UTF8 会写 BOM，BOM 混进会话号后
    # URL 会变成 /agent/%EF%BB%BF01a1...，驱动报 SESSION_MISMATCH 且死循环。读时一律吃掉 BOM。
    _v = _sf.read_text(encoding='utf-8-sig').strip()
    if _v:
        SESSION = _v
PIN_FILE = pathlib.Path('C:/tmp/arena_pin_session.txt')
if PIN_FILE.exists():
    _pin = PIN_FILE.read_text(encoding='utf-8-sig').strip()
    if _pin:
        SESSION = _pin
# 调试留痕（2026-10-03）：把驱动实际读到的会话串写出来，便于确认 BOM 来源
try:
    pathlib.Path('C:/tmp/arena_session_debug.txt').write_text(
        'SESSION=%r\nlen=%d\nfile=%s exists=%s\n' % (SESSION, len(SESSION), _sf, _sf.exists()),
        encoding='utf-8')
except Exception:
    pass
STAGE = pathlib.Path('C:/tmp/arena_stage')
LOG = pathlib.Path('C:/tmp/arena_driver.log')
ROTATE_FLAG = pathlib.Path('C:/tmp/arena_rotate.flag')
ROTATE_LEN = 550000  # 页正文超此长度即轮换会话。
                      # 2026-10-02 实测：会话涨到 60 万字符后，Arena 发送键点不动
                      # （需重试 4 次）、单组回复要等 33 分钟；40 万左右仍正常。
                      # 用户要求「过重只要不影响使用就行」，故定在影响使用的临界点之前。
KEEP = re.compile(r'[\u4e00-\u9fffA-Za-z0-9]')


def log(msg):
    line = '[%s] %s' % (time.strftime('%H:%M:%S'), msg)
    print(line, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def maxids():
    k = [int(p.stem.split('_')[0].split('-')[1]) for p in (OUT / '02_知识点').glob('K-*.md')]
    s = [int(p.stem.split('_')[0].split('-')[1]) for p in (OUT / '03_方法与策略').glob('S-*.md')]
    c = [int(p.stem.split('_')[0].split('-')[1]) for p in (OUT / '04_案例').glob('C-*.md')]
    ev = [int(x) for x in re.findall(r'(?m)^E-(\d{4,5})\t', (OUT / '01_资料与索引/证据索引.tsv').read_text(encoding='utf-8'))]
    return max(k or [0]), max(s or [0]), max(c or [0]), max(ev or [0])


# 号段保留区：这些区间已分配给分片工作区（Claude / Codex），主仓不得进入，否则合并时撞号。
# 2026-10-02 只护了 E（当时发现主仓 E6873 正朝 Claude 的 E8034 增长）。
# 2026-10-04 复核发现 K/S/C 同样在逼近：主仓 K 已到 2177，而 Codex 的 K 从 3855 起，
# 主仓再做约 210 组就会撞进去。故四类全部纳入保留，并在分片扩号后同步更新。
RESERVED = {
    'K': [(3855, 29999)],
    'S': [(3556, 19999)],
    'C': [(3800, 19999)],
    'E': [(8034, 9999), (10001, 58999)],
}


def safe_start(letter, n, span):
    """把起始号推到不与本类型任何保留区重叠的位置，保证 [n, n+span-1] 整段可用。"""
    bands = RESERVED.get(letter, [])
    for _ in range(500):
        end = n + span - 1
        clash = [hi for lo, hi in bands if not (end < lo or n > hi)]
        if not clash:
            return n
        n = max(clash) + 1
    return n


# 连续 BUSY 计数（2026-10-04）：用于区分「瞬时页面报错」与「会话真坏」。
BUSY_COUNT = pathlib.Path('C:/tmp/arena_busy_count.json')


def busy_count(sid):
    try:
        d = json.loads(BUSY_COUNT.read_text(encoding='utf-8'))
        return int(d.get(sid, 0)) if isinstance(d, dict) else 0
    except Exception:
        return 0


def set_busy_count(sid, n):
    try:
        d = json.loads(BUSY_COUNT.read_text(encoding='utf-8'))
        if not isinstance(d, dict):
            d = {}
    except Exception:
        d = {}
    if n <= 0:
        d.pop(sid, None)
    else:
        d[sid] = n
    try:
        BUSY_COUNT.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
    except Exception:
        pass


def done_sources():
    p = OUT / '01_资料与索引/来源去向.tsv'
    lines = p.read_text(encoding='utf-8').splitlines()
    head = lines[0].split('\t')
    si, sti = head.index('source_id'), head.index('处理状态')
    # 「已抽取」= 做过；另外这几类本来就不该抽，也视为不用处理，避免反复入选
    SKIP = {'已抽取', '工具脚本·无可用内容', '无可用交易内容'}
    return {l.split('\t')[si] for l in lines[1:]
            if len(l.split('\t')) > sti and l.split('\t')[sti] in SKIP}


def stage_files(picks):
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    import glob
    rows = []
    for f in sorted(glob.glob(str(OUT / '工作分片/批*_清单.tsv'))):
        rows += list(__import__('csv').DictReader(open(f, encoding='utf-8'), delimiter='\t'))
    got = []
    for r in rows:
        if r['source_id'] in picks:
            complete = (r.get('完整稿(阅读对象)') or '').strip()
            trimmed = (r.get('精简稿(导航用)') or '').strip()
            rel = complete or trimmed
            if not rel:
                log('    跳过 %s：完整稿和精简稿都为空' % r['source_id'])
                continue
            src = BASE / rel
            if not src.is_file():
                log('    跳过 %s：找不到文件 %s' % (r['source_id'], rel))
                continue
            # 0 字节（或近乎空）的残档会被 Arena 上传静默丢弃，附件数对不上提示词
            # 声明的份数 → UPLOAD 死循环（2026-10-06 实测：SRC-004629 的截断路径
            # 「学习笔记\第195」恰对应一个 9/27 生成的 0 字节残留，批062 连挂两轮）。
            # 这类文件视同缺失，走「备料不全，跳过」，绝不带病上传。
            if src.stat().st_size < 50:
                log('    跳过 %s：底本近乎空文件（%d 字节）%s，疑似排批路径截断' % (r['source_id'], src.stat().st_size, rel))
                continue
            if not complete:
                log('    受限底本 %s：仅使用精简稿，入库须标注「仅精简稿可核」' % r['source_id'])
            dst = STAGE / ('%s_%s' % (r['source_id'], src.name))
            shutil.copy2(src, dst)
            got.append((r, dst))
    return got


def gen_prompt(picks, ids, note):
    import importlib.util
    spec = importlib.util.spec_from_file_location('gen', str(OUT / '工具/Arena任务_生成提示.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    cfg = dict(picks=picks, kmin=ids[0], kmax=ids[1], smin=ids[2], smax=ids[3],
               cmin=ids[4], cmax=ids[5], emin=ids[6], emax=ids[7], inline=False, extra_note=note)
    t = m.build(**cfg)
    p = pathlib.Path('C:/tmp/arena_prompt_cur.txt')
    p.write_text(t, encoding='utf-8')
    return p, len(t)



def wait_idle(max_min=40):
    """等页面停止生成（没有 Stop generating 按钮）。

    2026-10-04：原来是 240 轮固定次数 × 每轮最多 120 秒超时，页面卡住时最坏能拖 8 小时
    （实测 01:02 起卡了 4 小时 45 分）。改成按墙钟封顶，并且单次探测异常不再让整批崩掉。
    """
    deadline = time.time() + max_min * 60
    while time.time() < deadline:
        out = ''
        try:
            r = subprocess.run(['node', str(SKILL / '_idle.mjs')], capture_output=True, text=True,
                               timeout=90, cwd=str(SKILL))
            out = (r.stdout or '').strip()
        except Exception as e:
            log('  空闲探测异常：%s' % str(e)[:80])
        if 'idle' in out:
            return True
        time.sleep(8)
    log('  页面长时间不空闲，放弃等待')
    return False


def run_and_grab(prompt_file, reply_file, anchor, stage, picks):
    """切进旗舰会话 → 上传+发送 → 等完成并按锚点抓取。返回 (ok, reason)"""
    # 发送前清掉旧回复文件，避免把上一次失败抓到的旧内容误当成本次结果
    for _stale in (reply_file, pathlib.Path('C:/tmp/arena_last.md')):
        try:
            _stale.unlink(missing_ok=True)
        except Exception:
            pass
    g = subprocess.run(['node', str(SKILL / '_goto.mjs'),
                        'https://arena.ai/agent/' + SESSION],
                       capture_output=True, text=True, timeout=300, cwd=str(SKILL))
    log('  切会话: %s' % (g.stdout or '').strip().replace('\n', ' | ')[-120:])
    # 2026-10-09 YG 红线：验证页（Try again / Reset session and reload 等）= 立即停止，
    # 绝不自动重试——多次触发风控可能封号。_goto 以 exit 5 上报。
    if g.returncode == 5 or '验证页: true' in (g.stdout or ''):
        return False, 'VERIFY'
    # 导航未确认时不发送，也不反复刷新同一地址。
    if g.returncode != 0 or SESSION not in (g.stdout or ''):
        log('  !! 未确认目标会话，保留本组待重试')
        return False, 'SESSION'
    # 页面就绪与否交给 arena-task.mjs 判断（它看的是输入框与文件输入是否存在，
    # 比「页长」可靠得多：健康的新会话页长本来就只有几百）。这里只做过重检测。
    try:
        pc = subprocess.run(['node', str(SKILL / '_pagelen.mjs')],
                            capture_output=True, text=True, timeout=90, cwd=str(SKILL))
        _pm = re.search(r'Result\s*\n\s*(\d+)', pc.stdout or '') or re.search(r'(\d{3,})', pc.stdout or '')
        plen = int(_pm.group(1)) if _pm else 0
    except Exception as ex:
        log('  页长检查异常: %s' % str(ex)[:80])
        plen = 0
    log('  会话页长: %d' % plen)
    # 2026-10-08 加：骨架页判据。实测 ?fresh=1 抽卡会话（01a11c0b）导航后停在启动骨架，
    # bodyLen 8428（侧栏撑起）、无输入框（.ProseMirror 不存在）、无 Stop 按钮，
    # arena-task 却报「输入框已清空、发送已确认」——组发进虚空，干等 13 分钟。
    # 页长阈值拦不住这种页（8428 看着正常），必须直接查编辑器在不在。
    try:
        ed = subprocess.run(['node', 'C:/arena-ext/ati-cdp.mjs', 'eval',
                             '(() => String(!!document.querySelector(".ProseMirror[contenteditable]")))()'],
                            capture_output=True, text=True, timeout=45, cwd='C:/arena-ext')
        _out = (ed.stdout or '').strip()
        # 只有明确返回 false 才判骨架；探测失败/空输出（扩展没连、CDP 抖动）一律放行，
        # 避免把网络抖动误判成坏会话、错杀健康会话。
        has_editor = 'false' not in _out.lower()
    except Exception:
        has_editor = True   # 探测本身失败不误伤，宁照旧流程走
    if not has_editor:
        log('  !! 页面无输入框（疑似启动骨架页），本会话不可用，标记轮换，保留本组')
        try:
            bad = pathlib.Path('C:/tmp/arena_bad_sessions.txt')
            bl = bad.read_text(encoding='utf-8-sig').splitlines() if bad.exists() else []
            if SESSION not in bl:
                bl.append(SESSION)
                bad.write_text('\n'.join(bl) + '\n', encoding='utf-8')
                log('  已隔离骨架会话 %s' % SESSION[:12])
        except Exception:
            pass
        ROTATE_FLAG.write_text(SESSION, encoding='utf-8')
        return False, 'ROTATE'
    if plen > ROTATE_LEN:
        pinned = PIN_FILE.read_text(encoding='utf-8-sig').strip() if PIN_FILE.exists() else ''
        if pinned and pinned == SESSION:
            # 用户已明确固定当前 gpt-6-astra 会话：不因正文变长换会话，
            # 继续让等待器抓取并由外层重试具体失败组。
            log('  会话已固定（%s），跳过页长轮换（%d > %d）' % (SESSION[:13], plen, ROTATE_LEN))
        else:
            log('  会话过重（%d > %d），请求轮换' % (plen, ROTATE_LEN))
            ROTATE_FLAG.write_text(SESSION, encoding='utf-8')
            return False, 'ROTATE'
    try:
        r = subprocess.run(['node', 'C:/tmp/arena-task.mjs', '--dir', str(stage),
                            '--prompt', str(prompt_file), '--out', 'C:/tmp/arena_last.md',
                            '--session', SESSION, '--no-poll'],
                           capture_output=True, text=True, timeout=900, cwd='C:/tmp')
    except subprocess.TimeoutExpired:
        return False, 'SENDTIMEOUT'
    tail = (r.stdout or '') + (r.stderr or '')
    for step in tail.splitlines():
        if step.startswith(('确认条:', '页面就绪:', '等待中就绪阶段', '上传', '附件数:', '发送已确认')):
            log('  提交步骤: ' + step[:240])
    log('  发送: %s' % tail.strip().replace('\n', ' | ')[-260:])
    for kw in ('额度', 'credit', 'upgrade', 'limit reached', 'out of', 'quota', 'insufficient'):
        if kw.lower() in tail.lower():
            return False, 'QUOTA:' + kw
    import re as _re
    # 页面/浏览器后端的前置失败（确认条探测、会话校验等）不是「附件没传全」。
    # 2026-10-01 实测：重会话下 getByRole 超时 → 抛异常 → 被误判成 UPLOAD 并快速重试 3 轮，
    # 白烧一个会话。这类失败必须交给外层按固定会话退避，而不是原地猛打。
    if 'PREPFAIL' in tail:
        _pm = _re.search(r'PREPFAIL:([^\n|]*)', tail)
        return False, 'PREPFAIL(%s)' % ((_pm.group(1).strip()[:120] if _pm else ''))
    m = _re.search(r'附件数:\s*(\d+)\s*/\s*(\d+)', tail)
    if not m or m.group(1) != m.group(2) or int(m.group(2)) != len(picks):
        return False, 'UPLOAD(附件 %s, 需 %d)' % (m.group(0) if m else '未读到', len(picks))
    if r.returncode != 0 or '发送已确认' not in tail:
        return False, 'SENDFAIL'
    # 早期查错：发完约 30 秒立即查一次「Something went wrong / service busy / 页面重置」，
    # 避免干等 40 分钟才发现（2026-09-30 用户要求）
    try:
        e = subprocess.run(['node', str(SKILL / '_earlyErr.mjs'), '30'],
                           capture_output=True, text=True, timeout=120, cwd=str(SKILL))
        elog = (e.stdout or '').strip()
        log('  早期查错(30s): %s' % elog.replace('\n', ' | ')[:100])
        if elog.startswith('BUSY'):
            return False, 'BUSY'
        if elog.startswith('RESET'):
            # 页面被重置，发送打到空白页 → 立即重发本组一次
            log('  页面重置，重发本组')
            try:
                subprocess.run(['node', str(SKILL / '_goto.mjs'),
                                'https://arena.ai/agent/' + SESSION],
                               capture_output=True, text=True, timeout=300, cwd=str(SKILL))
                resend = subprocess.run(['node', 'C:/tmp/arena-task.mjs', '--dir', str(stage),
                                      '--prompt', str(prompt_file), '--out', 'C:/tmp/arena_last.md',
                                      '--session', SESSION, '--no-poll'],
                                    capture_output=True, text=True, timeout=900, cwd='C:/tmp')
                log('  重发: %s' % ((resend.stdout or '') + (resend.stderr or '')).strip().replace('\n', ' | ')[-140:])
                if resend.returncode != 0 or '发送已确认' not in ((resend.stdout or '') + (resend.stderr or '')):
                    return False, 'RESEND-FAIL'
                re2 = subprocess.run(['node', str(SKILL / '_earlyErr.mjs'), '30'],
                                     capture_output=True, text=True, timeout=120, cwd=str(SKILL))
                elog2 = (re2.stdout or '').strip()
                log('  重发后查错: %s' % elog2.replace('\n', ' | ')[:100])
                if elog2.startswith('BUSY'):
                    return False, 'BUSY'
                if elog2.startswith('RESET'):
                    return False, 'RESET'
            except Exception as ex2:
                log('  重发异常: %s' % str(ex2)[:100])
                return False, 'RESEND-ERR'
    except Exception as ex:
        log('  早期查错异常: %s' % str(ex)[:80])
    # 等待完成 + 按锚点抓
    try:
        # 2026-10-08 YG 批准：组总上限 28→30 分钟（当晚 astra 会话思考期常超 28 分钟，
        # 实测组 004927/29 全程 n=0 被 28 分钟误杀；附件大小与此无关，每组固定 2 份精简稿）
        w = subprocess.run(['node', str(SKILL / '_wait.mjs'), anchor, str(reply_file), '30', SESSION],
                            capture_output=True, text=True, timeout=2400, cwd=str(SKILL))
        log('  抓取: %s' % ((w.stdout or '') + (w.stderr or '')).strip().replace('\n', ' | ')[-320:])
        # 2026-10-09 YG 红线：等待中出现验证页 = 立即停止整条线，绝不自动重试。
        if w.returncode == 5 or 'VERIFY_PAGE' in ((w.stdout or '') + (w.stderr or '')):
            return False, 'VERIFY'
        if w.returncode == 4 or 'PAGE_ERROR' in ((w.stdout or '') + (w.stderr or '')):
            return False, 'BUSY'
        if w.returncode != 0:
            return False, 'WAITFAIL(%d)' % w.returncode
    except subprocess.TimeoutExpired:
        log('  抓取超时，保留本组待重试，不入库未完成内容')
        return False, 'WAITTIMEOUT'
    except Exception as e:
        log('  抓取异常: %s' % str(e)[:150])
    if not reply_file.exists() or reply_file.stat().st_size < 300:
        return False, 'EMPTY'
    body = reply_file.read_text(encoding='utf-8')
    if re.search(r'service is busy|Something went wrong|Please try again|try again in a moment|overloaded|rate limit|too many requests|An error occurred', body, re.I):
        return False, 'BUSY'
    hit = [s for s in picks if s in body]
    if not hit:
        # 一份都没提到 -> 几乎肯定抓错了块
        return False, 'WRONGREPLY(一个来源都没提到)'
    if len(hit) < len(picks):
        # 部分覆盖：仍然放行入库（入库只标被覆盖的来源），未覆盖的留给下一轮重跑
        log('  注意：本组只覆盖 %d/%d 份，未覆盖 %s' % (len(hit), len(picks), ','.join(s for s in picks if s not in hit)))
    return True, 'OK'


def parse_and_ingest(picks, reply_file):
    raw = reply_file.read_text(encoding='utf-8')
    cards = {}
    for m in re.finditer(r'#\s*((?:补充\s*)?[KSC]-\d{4,5})\s+([^\n]+)\n(.*?)(?=\n\s*#\s*(?:补充\s*)?[KSC]-\d{4,5}|\n\s*tsv|\n\s*底本层级|\Z)', raw, re.S):
        cid, name, body = m.group(1).strip(), m.group(2).strip(), m.group(3)
        if cid not in cards or len(body) > len(cards[cid][1]):
            cards[cid] = (name, body)
    tsv, seen = [], set()
    for line in raw.splitlines():
        m = re.match(r'^(E-\d{4,5})\s*(SRC-\d{6})\s*(.*)$', line.strip())
        if m and m.group(1) not in seen:
            seen.add(m.group(1))
            tsv.append('\t'.join([m.group(1), m.group(2), re.sub(r'\s+', ' ', m.group(3)).strip()]))
    log('  解析：卡片 %d（%s）｜证据 %d' % (len(cards), ','.join(sorted(cards)), len(tsv)))
    if not tsv and not cards:
        return 0, 0
    # 验证
    def sm(s):
        o, i = [], []
        for k, ch in enumerate(s):
            if KEEP.match(ch):
                o.append(ch); i.append(k)
        return ''.join(o), i
    SRC = {}
    for f in STAGE.glob('*.md'):
        rr = f.read_text(encoding='utf-8')
        SRC[f.name.split('_')[0]] = (rr, sm(rr))

    def verify(sid, text):
        if sid not in SRC:
            return '', 0
        rr, (flat, imap) = SRC[sid]
        tgt, _ = sm(text)
        best = (0, -1)
        for i in range(len(tgt)):
            j = i + best[0] + 1
            while j <= len(tgt):
                if flat.find(tgt[i:j]) < 0:
                    break
                j += 1
            seg = tgt[i:j-1]
            if len(seg) > best[0]:
                best = (len(seg), flat.find(seg))
        blen, fstart = best
        if blen < 8:
            return '', 0
        return re.sub(r'\s+', '', rr[imap[fstart]:imap[fstart + blen - 1] + 1]), blen

    rows, okc, bad = [], 0, []
    for line in tsv:
        c = line.split('\t')
        q, _ = verify(c[1], '\t'.join(c[2:]))
        if q:
            okc += 1
            rows.append([c[0], c[1], '', q, '', '2026-09-29'])
        else:
            bad.append((c[0], c[2][:60]))
    log('  验证：%d/%d 通过%s' % (okc, len(tsv), ('，未通过 ' + str([b[0] for b in bad])) if bad else ''))
    # 写卡
    n = 0
    for cid, (name, body) in sorted(cards.items()):
        if cid.startswith('补充'):
            target = cid.replace('补充', '').strip()
            f = []
            for d in ('02_知识点', '03_方法与策略', '04_案例'):
                f += list((OUT / d).glob('%s_*.md' % target))
            if f:
                t = f[0].read_text(encoding='utf-8')
                if name[:20] not in t:
                    f[0].write_text(t.rstrip() + '\n\n---\n\n## 补充：' + name + '\n' + body.rstrip() + '\n', encoding='utf-8')
                    n += 1
                    log('    追加 %s → %s' % (name[:30], f[0].name))
        else:
            d = {'K': '02_知识点', 'S': '03_方法与策略', 'C': '04_案例'}[cid[0]]
            safe = re.sub(r'[\\/:*?"<>|]', '', name)[:40]
            p = OUT / d / ('%s_%s.md' % (cid, safe))
            if not p.exists():
                p.write_text('# %s %s\n%s\n' % (cid, name, body.rstrip()), encoding='utf-8')
                n += 1
                log('    新建 %s %s' % (cid, name[:34]))
    evp = OUT / '01_资料与索引/证据索引.tsv'
    have = set(re.findall(r'(?m)^(E-\d{4,5})\t', evp.read_text(encoding='utf-8')))
    add = [r for r in rows if r[0] not in have]
    with open(evp, 'a', encoding='utf-8') as fh:
        for r in add:
            fh.write('\t'.join(r) + '\n')
    # 台账
    p = OUT / '01_资料与索引/来源去向.tsv'
    lines = p.read_text(encoding='utf-8').splitlines()
    head = lines[0].split('\t')
    si, sti = head.index('source_id'), head.index('处理状态')
    for i, l in enumerate(lines[1:], 1):
        c = l.split('\t')
        if len(c) > sti and c[si] in picks and c[sti] != '已抽取':
            c[sti] = '已抽取'
            lines[i] = '\t'.join(c)
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    shutil.copy2(reply_file, OUT / '07_审计与交付' / ('Arena产出_%s.md' % '_'.join(sorted(picks))))
    return n, len(add)


def main():
    batch = sys.argv[1] if len(sys.argv) > 1 else '批005'
    GROUP = int(sys.argv[2]) if len(sys.argv) > 2 else 2   # 2026-09-30 实测附件上限=2（4份卡 Updating 不生成）
    # 2026-10-06 用户要求：本轮最多跑多少组（0=不限）。外层循环用「10 组对话 + 10 轮抽卡」
    # 反复交替，跑满就交回循环去抽卡。剩下的来源靠台账「已抽取」判断，下一轮天然续跑，
    # 既不会漏也不会重；组号 gi 每次重新编号，因为 todo 已经剔除了做过的来源。
    MAX_GROUPS = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    import csv
    rows = list(csv.DictReader(open(str(OUT / '工作分片') + '/' + batch + '_清单.tsv', encoding='utf-8'), delimiter='\t'))
    dn = done_sources()
    todo = [r for r in rows if r['source_id'] not in dn]
    log('=== %s：共 %d，已完成 %d，待做 %d%s ==='
        % (batch, len(rows), len(rows) - len(todo), len(todo),
           '（本轮上限 %d 组）' % MAX_GROUPS if MAX_GROUPS else ''))
    fail = 0
    done_groups = 0
    # 按体量分箱：每组附件总量压在 BUDGET 以内。精简稿中位 2KB 可以两份一组，
    # 但第2阶段的增强稿中位 79KB、最大 440KB，两份就能把会话顶爆（2026-10-01 排批实测），
    # 所以这里按实际字节数装箱，大文件自动降为一份一组。
    BUDGET = 200000
    groups, _cur, _sz = [], [], 0
    for r in todo:
        rel = ((r.get('完整稿(阅读对象)') or '').strip() or (r.get('精简稿(导航用)') or '').strip())
        p = BASE / rel
        sz = p.stat().st_size if p.is_file() else 0
        if _cur and (len(_cur) >= GROUP or _sz + sz > BUDGET):
            groups.append(_cur); _cur, _sz = [], 0
        _cur.append(r); _sz += sz
    if _cur:
        groups.append(_cur)
    for gi, pair in enumerate(groups):
        picks = [r['source_id'] for r in pair]
        types = [r['课型'] for r in pair]
        log('--- 组 %d/%d: %s（%s）' % (gi + 1, len(groups), picks, '/'.join(types)))
        if not wait_idle(40):
            log('=== 未确认页面空闲，停止本轮，保留剩余来源 ===')
            return
        k, s, c, ev = maxids()
        unit = max(1, len(pair) // 2)
        # 四类都要跳过保留区（原来只跳 E）：主仓 K/S/C 也在朝分片区涨。
        # 2026-10-06 修 off-by-one：K/S/C 的号段实际用到 k0+8*unit（即 span+1 个号），
        # 但原来 safe_start 只校验 [n, n+span-1]，最后一个号没校验——实测把主仓 K-3855
        # 写进了 Codex 分片的保留区（3855 起），和分片的 K-3855 撞号。这里把校验窗口
        # 对齐到真实使用范围。（E 那边本来就是 e0..e0+20*unit-1，span 一致，不动。）
        k0 = safe_start('K', k + 1, 8 * unit + 1)
        s0 = safe_start('S', s + 1, 5 * unit + 1)
        c0 = safe_start('C', c + 1, 5 * unit + 1)
        e0 = safe_start('E', ev + 1, 20 * unit)
        ids = ('%04d' % k0, '%04d' % (k0 + 8 * unit), '%04d' % s0, '%04d' % (s0 + 5 * unit),
               '%04d' % c0, '%04d' % (c0 + 5 * unit), '%04d' % e0, '%04d' % (e0 + 20 * unit - 1))
        # 开跑前先自检号段是否落在入库允许范围内（判据与 Arena入库.py 的 card_limits 一致：
        # ≤现有最大+60，或落在保留区之后的首个空闲块里）。否则会白烧一轮 Arena 才发现号段非法
        # ——实测批063 末组就是这样丢掉 9 张 K 卡的。
        _bad = []
        for _lt, _a, _b, _mx in (('K', k0, k0 + 8 * unit, k), ('S', s0, s0 + 5 * unit, s),
                                 ('C', c0, c0 + 5 * unit, c)):
            _nf = safe_start(_lt, _mx + 1, 1)
            if not (_b <= _mx + 60 or _nf <= _a <= _b <= _nf + 60):
                _bad.append('%s-%04d..%04d（现有最大 %d，保留区后首个空闲块 %d）' % (_lt, _a, _b, _mx, _nf))
        if _bad:
            log('=== 号段超出入库允许范围，停批（不烧 Arena 额度）: %s ===' % '; '.join(_bad))
            return
        got = stage_files(picks)
        if len(got) < len(picks):
            log('  备料不全，跳过'); continue
        note = '本组资料：' + '；'.join('%s（第%s课 %s，课型%s）' % (r['source_id'], r['课号'], r['主题'], r['课型']) for r, _ in got)
        note += '。**若这些资料属于同一系列，注意不要跨系列串联策略；若与已有卡讲同一件事，写「补充 K-xxxx」不要新建。**'
        note += '**请先核对底本层级**：若给的是"(增强版)"笔记而非完整稿，务必在卡片里标「仅增强稿可见」，不要写成完整稿。'
        # 每组唯一运行标记：防止把上一次同号段的旧回复误当成本次结果
        run_token = 'RUN-%s-G%d-%d' % (batch, gi + 1, int(time.time()))
        note += '。**请在回复正文第一行原样输出运行标记 `%s`（只输出该标记，不要解释），随后再开始正式输出卡片。**' % run_token
        pf, ln = gen_prompt(picks, ids, note)
        log('  提示 %d 字符，号段 K%s-%s S%s-%s C%s-%s E%s-%s' % (ln, *ids))
        anchor = run_token
        ok, why = run_and_grab(pf, pathlib.Path('C:/tmp/arena_reply_cur.md'), anchor, STAGE, picks)
        if not ok:
            log('  ✗ %s' % why)
            if why == 'VERIFY':
                # 2026-10-09 YG 红线：需要人工验证的页面 → 立刻停整条线，绝不重试。
                log('=== 页面需要人工验证（Try again / Reset session and reload），停止，不重试，等人工处理 ===')
                pathlib.Path('C:/tmp/arena_verify_stop.flag').write_text(SESSION, encoding='utf-8')
                break
            if why.startswith('PREPFAIL'):
                # 页面准备失败只退避重试当前会话，不能触发换会话。
                pathlib.Path('C:/tmp/arena_retry_same.flag').write_text(SESSION, encoding='utf-8')
                log('=== 页面前置失败，停批后重试同会话，不切换 ===')
                return
            if why in ('BUSY', 'RESET'):
                # Something went wrong / busy / 页面重置：当前回复不入库。
                # 2026-10-04：实测这类报错多为**瞬时页面级**错误，会话本身没坏——日志里 6 次
                # 里至少 2 次会话随后照常工作（01a1014c 在 00:41 与 07:28 被判死，10:59 还在正常出卡）。
                # 原逻辑第一次就永久拉黑，白丢一条已验证旗舰、还要重新抽卡十几分钟且常不命中。
                # 现在：第一次只退避重试同一会话，连续第二次才拉黑换会话。
                n = busy_count(SESSION) + 1
                if n >= 2:
                    set_busy_count(SESSION, 0)
                    pathlib.Path('C:/tmp/arena_busy.flag').write_text(SESSION, encoding='utf-8')
                    badp = pathlib.Path('C:/tmp/arena_bad_sessions.txt')
                    known = set(badp.read_text(encoding='utf-8').split()) if badp.exists() else set()
                    known.add(SESSION)
                    badp.write_text('\n'.join(sorted(known)) + '\n', encoding='utf-8')
                    log('=== 页面报错连续第 %d 次，隔离该会话，交给外层切换 ===' % n)
                else:
                    set_busy_count(SESSION, n)
                    pathlib.Path('C:/tmp/arena_retry_same.flag').write_text(SESSION, encoding='utf-8')
                    log('=== 页面报错第 %d 次（疑似瞬时），停批后重试同一会话 ===' % n)
                return
            if why == 'SENDFAIL':
                # 2026-10-04：Send 键卡在 React 状态失同步——正文已写进输入框，但按钮一直
                # disabled、Ctrl+Enter 也不提交。页面 URL 没变，普通重试会一直撞同一个坏状态
                # （实测连续 3 次 SENDFAIL 后驱动停批）。实测强制刷新页面一次即恢复
                # （刷新前写入后 sendDisabled=true，刷新后 false）。所以刷新后重试同一会话。
                key = 'SENDFAIL:' + SESSION
                n = busy_count(key) + 1
                if n <= 2:
                    set_busy_count(key, n)
                    log('  发送键卡死（第 %d 次），强制刷新页面后重试同一会话' % n)
                    try:
                        subprocess.run(['node', str(SKILL / '_goto.mjs'),
                                        'https://arena.ai/agent/' + SESSION, '--force'],
                                       capture_output=True, text=True, timeout=300, cwd=str(SKILL))
                    except Exception as ex:
                        log('  强制刷新异常: %s' % str(ex)[:100])
                    pathlib.Path('C:/tmp/arena_retry_same.flag').write_text(SESSION, encoding='utf-8')
                    return
                set_busy_count(key, 0)
                log('  发送键连续卡死 %d 次，刷新无效，按普通失败计数' % n)
            if why == 'ROTATE':
                # 会话过重：旗标已写，停批交给外层轮换新会话
                log('=== 会话过重，停批交给外层轮换 ===')
                return
            # 失败后先停掉残留生成，否则下一组上传拿不到输入框
            try:
                subprocess.run(['node', str(SKILL / '_stop.mjs')], capture_output=True, text=True, timeout=200, cwd=str(SKILL))
                log('  已清残留生成')
            except Exception:
                pass
            fail += 1
            if why.startswith('QUOTA'):
                log('=== 额度耗尽，停止 ==='); break
            if fail >= 3:
                log('=== 连续失败 3 次，停止 ==='); break
            continue
        fail = 0
        ing = subprocess.run(['python', '-X', 'utf8', str(OUT / '工具/Arena入库.py'),
                              'C:/tmp/arena_reply_cur.md', ids[6], ids[7], str(STAGE), ','.join(picks)],
                             capture_output=True, text=True, timeout=600)
        for ln in (ing.stdout or '').strip().splitlines():
            log('    ' + ln)
        # 护栏：回复里明明有卡片标题，却一张都没写进库 —— 2026-10-01 因模型漏写井号
        # 触发过一次，20 条证据进了索引、卡片全丢且台账照样标「已抽取」。这里必须吵。
        try:
            _rep = pathlib.Path('C:/tmp/arena_reply_cur.md').read_text(encoding='utf-8')
            _heads = len(re.findall(r'(?m)^[ \t]*(?:#{1,6}[ \t]*)?\*{0,2}(?:补充[ \t]*)?[KSC]-\d{4,5}\b', _rep))
        except Exception:
            _heads = 0
        _mc = re.search(r'新卡 (\d+)', ing.stdout or '')
        if _heads and _mc and int(_mc.group(1)) == 0:
            log('  !! 回复里有 %d 个卡片标题，但新卡 0：解析可能失败，本组须人工复核后再往下跑' % _heads)
            fail += 1
        if re.search(r'(?m)^证据 0 \|', ing.stdout or ''):
            log('  ✗ 证据 0，视为失败')
            fail += 1
            continue
        if ing.returncode != 0:
            log('  ✗ 入库失败: %s' % (ing.stderr or '')[-200:])
            fail += 1
            continue
        shutil.copy2('C:/tmp/arena_reply_cur.md', OUT / '07_审计与交付' / ('Arena产出_%s.md' % '_'.join(sorted(picks))))
        log('  ✓ 入库完成')
        set_busy_count(SESSION, 0)   # 本会话证明可用，清掉连续 BUSY 计数
        done_groups += 1
        if MAX_GROUPS and done_groups >= MAX_GROUPS:
            log('=== 本轮已跑满 %d 组，交回循环（剩余来源下一轮继续）===' % MAX_GROUPS)
            break
    k, s, c, ev = maxids()
    log('=== 结束：K%d S%d C%d 共 %d 卡，证据 %d 条 ===' % (k, s, c, k + s + c, ev))


if __name__ == '__main__':
    main()
