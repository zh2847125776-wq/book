# -*- coding: utf-8 -*-
"""Antigravity (agy CLI) 连续抽取驱动。

由 Arena 迁移至 Antigravity 本机通道：
1. 沿用批清单与台账「已抽取」过滤。
2. 备料至 C:/tmp/arena_stage。
3. 动态计算 K/S/C/E 安全号段（避开分片保留区，且符合现有最大+60护栏）。
4. 生成任务提示词（inline=False，要求模型用 view_file 读取本地备料文件）。
5. 调用本地 agy.exe CLI（默认 gemini-3.8-flash-high）执行抽取。
6. 回复写入 C:/tmp/antigravity_reply_cur.md。
7. 调用原样 Arena入库.py 执行回源校验、落卡、落索引、翻台账。

用法:
    python Antigravity驱动_连续抽取.py [批号, 默认批078] [每组份数, 默认2] [本轮最多组数, 0=不限] [模型, 默认gemini-3.8-flash-high]
"""
import csv
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

BASE = pathlib.Path(r'C:\Users\赵豪\dsh')
OUT = BASE / '交易知识体系汇编'
STAGE = pathlib.Path('C:/tmp/arena_stage')
LOG = pathlib.Path('C:/tmp/antigravity_driver.log')
REPLY_FILE = pathlib.Path('C:/tmp/antigravity_reply_cur.md')
AGY_EXE = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'agy/bin/agy.exe'


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


def done_sources():
    p = OUT / '01_资料与索引/来源去向.tsv'
    lines = p.read_text(encoding='utf-8').splitlines()
    head = lines[0].split('\t')
    si, sti = head.index('source_id'), head.index('处理状态')
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
        rows += list(csv.DictReader(open(f, encoding='utf-8'), delimiter='\t'))
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
            if src.stat().st_size < 50:
                log('    跳过 %s：底本近乎空文件（%d 字节）%s' % (r['source_id'], src.stat().st_size, rel))
                continue
            if not complete:
                log('    受限底本 %s：仅使用精简稿，入库须标注「仅精简稿可核」' % r['source_id'])
            dst = STAGE / ('%s_%s' % (r['source_id'], src.name))
            shutil.copy2(src, dst)
            got.append((r, dst))
    return got


def gen_prompt(picks, ids, note, staged_files, run_token):
    import importlib.util
    spec = importlib.util.spec_from_file_location('gen', str(OUT / '工具/Arena任务_生成提示.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    cfg = dict(picks=picks, kmin=ids[0], kmax=ids[1], smin=ids[2], smax=ids[3],
               cmin=ids[4], cmax=ids[5], emin=ids[6], emax=ids[7], inline=False, extra_note=note)
    base_text = m.build(**cfg)
    base_text = (base_text
                 .replace('我在附件里放了', '已在本地备料目录放了')
                 .replace('从附件里', '从上述文件里')
                 .replace('拿回附件', '拿回上述文件')
                 .replace('在附件里找不到', '在上述文件里找不到'))

    # 针对 Antigravity CLI 的前置指令：明确引导使用自带 view_file 工具阅读本地文件
    flist = '\n'.join('- `%s` 本地绝对路径：`%s`' % (r['source_id'], str(p)) for r, p in staged_files)
    instr = f"""【本地文件阅读与抽取任务】
请使用你自带的 `view_file` 工具依次阅读以下 {len(staged_files)} 份待抽取资料的完整正文：
{flist}

【格式与硬约束】
1. 回复正文第一行必须原样输出运行标记：`{run_token}`（单占一行，不要加代码块或解释）。
2. 从第二行开始严格按照规范输出：
   ## 卡片 （每个卡片一个 markdown 代码块包裹，标题如 # K-XXXX 名称）
   ## 证据清单 （tsv 代码块，5列制表符分隔：证据ID<TAB>source_id<TAB>位置<TAB>原文摘录<TAB>用途）
   ## 底本层级与疑点
   ## 与已有卡的关系
3. 「原文摘录」必须从上述文件中逐字复制原句（至少连续8个字完全一致），绝对不许改写、概括、拼接。
4. ID 号段严格限制在：K-{ids[0]}~K-{ids[1]}，S-{ids[2]}~S-{ids[3]}，C-{ids[4]}~C-{ids[5]}，E-{ids[6]}~E-{ids[7]}，不得超界。
5. 【质量硬约束与防空心化】：
   - 规矩是约束不是素材：卡片字段（尤其是「它解决什么问题」「适用边界与失效」）严禁抄入抽取铁律字眼（如「仅记录≤300字」「不采信Vision推断」「禁截断铁律」等）；「它解决什么问题」必须写明解决什么具体交易问题。
   - 禁止占位符：严禁输出「关联Sx与Cx；不跨源混用」、「见Sx与Cx」等空占位。「与其他概念的关系」必须写出实质概念关系（对照/前提/互斥/补充）；「案例与证据」必须包含具体标的、时间、形态或数字。
   - 逐节取证：各小节必须挂各自支撑的对应证据号，严禁整张卡片所有小节机械挂完全相同的一组证据号。

"""
    prompt = instr + base_text
    pf = pathlib.Path('C:/tmp/arena_prompt_cur.txt')
    pf.write_text(prompt, encoding='utf-8')
    return pf, len(prompt)


def call_antigravity(prompt_text, timeout_sec=900, model='gemini-3.8-flash-high', max_retries=4):
    if not AGY_EXE.is_file():
        return False, 'AGY_EXE 不存在: %s' % AGY_EXE

    env = os.environ.copy()
    env['HTTPS_PROXY'] = 'http://127.0.0.1:7897'
    env['HTTP_PROXY'] = 'http://127.0.0.1:7897'
    env['https_proxy'] = 'http://127.0.0.1:7897'
    env['http_proxy'] = 'http://127.0.0.1:7897'
    env['NO_PROXY'] = 'localhost,127.0.0.1,::1'
    env['no_proxy'] = 'localhost,127.0.0.1,::1'

    cmd = [str(AGY_EXE), '--model', model, '--dangerously-skip-permissions', '--print', prompt_text]

    last_err = ''
    for attempt in range(1, max_retries + 1):
        t0 = time.time()
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=timeout_sec, cwd=str(OUT))
            elapsed = time.time() - t0
            if res.returncode != 0:
                err = (res.stderr or '').strip()
                out = (res.stdout or '').strip()
                last_err = 'EXIT_%d (耗时 %.1fs): %s | %s' % (res.returncode, elapsed, out[:150], err[:150])
                if attempt < max_retries:
                    log('    [网络抖动重试 %d/%d] CLI 调用异常 (%s)，等待 15 秒后重试...' % (attempt, max_retries, last_err[:80]))
                    time.sleep(15)
                    continue
                return False, last_err
            body = res.stdout or ''
            if not body.strip():
                last_err = 'EMPTY_OUTPUT (耗时 %.1fs)' % elapsed
                if attempt < max_retries:
                    log('    [网络重试 %d/%d] CLI 输出为空，等待 15 秒后重试...' % (attempt, max_retries))
                    time.sleep(15)
                    continue
                return False, last_err
            return True, body
        except subprocess.TimeoutExpired:
            return False, 'TIMEOUT (超过 %ds)' % timeout_sec
        except Exception as ex:
            return False, 'EXCEPTION: %s' % str(ex)
    return False, last_err


def main():
    batch = sys.argv[1] if len(sys.argv) > 1 else '批078'
    GROUP = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    MAX_GROUPS = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    MODEL = sys.argv[4] if len(sys.argv) > 4 else 'gemini-3.8-flash-high'

    manifest = OUT / '工作分片' / (batch + '_清单.tsv')
    if not manifest.is_file():
        log('错误：清单文件不存在: %s' % manifest)
        return

    rows = list(csv.DictReader(open(str(manifest), encoding='utf-8'), delimiter='\t'))
    dn = done_sources()
    todo = [r for r in rows if r['source_id'] not in dn]
    log('=== Antigravity 抽取通道启动 ===')
    log('批次: %s | 总来源: %d | 已完成: %d | 待抽: %d%s | 模型: %s'
        % (batch, len(rows), len(rows) - len(todo), len(todo),
           (' | 上限 %d 组' % MAX_GROUPS) if MAX_GROUPS else '', MODEL))

    if not todo:
        log('本批全部来源已处理完毕，退出。')
        return

    # 动态分箱：单组体积控制在 70KB 以内；单个大文件（>50KB）独立成组，避免超时
    BUDGET = 70000
    groups, _cur, _sz = [], [], 0
    for r in todo:
        rel = ((r.get('完整稿(阅读对象)') or '').strip() or (r.get('精简稿(导航用)') or '').strip())
        p = BASE / rel
        sz = p.stat().st_size if p.is_file() else 0
        if _cur and (len(_cur) >= GROUP or _sz + sz > BUDGET or sz > 50000):
            groups.append(_cur); _cur, _sz = [], 0
        _cur.append(r); _sz += sz
    if _cur:
        groups.append(_cur)

    fail_consecutive = 0
    done_groups = 0

    for gi, pair in enumerate(groups):
        picks = [r['source_id'] for r in pair]
        types = [r['课型'] for r in pair]
        log('--- 组 %d/%d: %s（%s）---' % (gi + 1, len(groups), picks, '/'.join(types)))

        k, s, c, ev = maxids()
        unit = max(1, len(pair) // 2)

        k0 = safe_start('K', k + 1, 8 * unit + 1)
        k_end = k0 + 8 * unit

        s_span = min(5 * unit + 1, 3555 - s) if s < 3555 else 5 * unit + 1
        s0 = safe_start('S', s + 1, s_span)
        s_end = s0 + s_span - 1 if s < 3555 else s0 + 5 * unit

        c_span = min(5 * unit + 1, 3799 - c) if c < 3799 else 5 * unit + 1
        c0 = safe_start('C', c + 1, c_span)
        c_end = c0 + c_span - 1 if c < 3799 else c0 + 5 * unit

        e0 = safe_start('E', ev + 1, 20 * unit)
        e_end = e0 + 20 * unit - 1

        ids = ('%04d' % k0, '%04d' % k_end, '%04d' % s0, '%04d' % s_end,
               '%04d' % c0, '%04d' % c_end, '%04d' % e0, '%04d' % e_end)

        # 护栏自检：号段是否在入库允许范围（<= 现有最大 + 60，或空闲块起点）
        _bad = []
        for _lt, _a, _b, _mx in (('K', k0, k_end, k), ('S', s0, s_end, s),
                                 ('C', c0, c_end, c)):
            _nf = safe_start(_lt, _mx + 1, 1)
            if not (_b <= _mx + 60 or _nf <= _a <= _b <= _nf + 60):
                _bad.append('%s-%04d..%04d（现有最大 %d，空闲块 %d）' % (_lt, _a, _b, _mx, _nf))
        if _bad:
            log('=== 号段超出入库允许范围，终止批次以防越界: %s ===' % '; '.join(_bad))
            return

        got = stage_files(picks)
        if len(got) < len(picks):
            log('  备料不全（实际 %d / 需 %d），跳过本组' % (len(got), len(picks)))
            continue

        note = '本组资料：' + '；'.join('%s（第%s课 %s，课型%s）' % (r['source_id'], r['课号'], r['主题'], r['课型']) for r, _ in got)
        note += '。**若这些资料属于同一系列，注意不要跨系列串联策略；若与已有卡讲同一件事，写「补充 K-xxxx」不要新建。**'
        note += '**请先核对底本层级**：若给的是"(增强版)"笔记而非完整稿，务必在卡片里标「仅增强稿可见」，不要写成完整稿。'

        run_token = 'RUN-%s-G%d-%d' % (batch, gi + 1, int(time.time()))
        pf, ln = gen_prompt(picks, ids, note, got, run_token)
        log('  提示已就绪: %d 字符 | 号段 K%s-%s S%s-%s C%s-%s E%s-%s' % (ln, *ids))

        prompt_content = pf.read_text(encoding='utf-8')
        log('  派发 Antigravity 抽取任务 (模型 %s)...' % MODEL)
        t_call_start = time.time()
        ok, reply_body = call_antigravity(prompt_content, timeout_sec=900, model=MODEL)
        call_dur = time.time() - t_call_start

        if not ok:
            log('  ✗ 模型调用失败 (%.1fs): %s' % (call_dur, reply_body))
            fail_consecutive += 1
            if fail_consecutive >= 3:
                log('=== 连续失败 3 组，停止运行以待人工检查通道 ===')
                break
            log('  等待 30 秒让网络/代理抖动恢复后继续下一组...')
            time.sleep(30)
            continue

        log('  ✓ 模型回复接收成功 (%.1fs, %d 字符)' % (call_dur, len(reply_body)))

        # 清除旧回复，写入新回复
        try:
            REPLY_FILE.unlink(missing_ok=True)
        except Exception:
            pass
        REPLY_FILE.write_text(reply_body, encoding='utf-8')

        # 调用原版 Arena入库.py（原样护栏，不改动一行）
        ing = subprocess.run(['python', '-X', 'utf8', str(OUT / '工具/Arena入库.py'),
                              str(REPLY_FILE), ids[6], ids[7], str(STAGE), ','.join(picks)],
                             capture_output=True, text=True, timeout=600)
        for ln in (ing.stdout or '').strip().splitlines():
            log('    ' + ln)

        # 校验入库结果
        _heads = len(re.findall(r'(?m)^[ \t]*(?:#{1,6}[ \t]*)?\*{0,2}(?:补充[ \t]*)?[KSC]-\d{4,5}\b', reply_body))
        _mc = re.search(r'新卡 (\d+)', ing.stdout or '')
        if _heads and _mc and int(_mc.group(1)) == 0:
            log('  !! 回复里有 %d 个卡片标题，但新卡 0：解析可能失败' % _heads)
            fail_consecutive += 1
        elif ing.returncode != 0:
            log('  ✗ 入库脚本返回非零退出码 (%d): %s' % (ing.returncode, (ing.stderr or '')[-200:]))
            fail_consecutive += 1
        elif re.search(r'(?m)^证据 0 \|', ing.stdout or ''):
            log('  ✗ 证据解析为 0，视为失败')
            fail_consecutive += 1
        else:
            log('  ✓ 入库成功')
            fail_consecutive = 0
            archive_name = 'Antigravity产出_%s.md' % '_'.join(sorted(picks))
            archive_path = OUT / '07_审计与交付' / archive_name
            shutil.copy2(str(REPLY_FILE), archive_path)
            done_groups += 1

            # 质量闸门：卡片充实度质检
            qc = subprocess.run(['python', '-X', 'utf8', str(OUT / '工具/质检_卡片充实度.py'), str(archive_path)],
                                capture_output=True, text=True, timeout=60)
            for qcln in (qc.stdout or '').strip().splitlines():
                log('    ' + qcln)

        if fail_consecutive >= 3:
            log('=== 连续失败 3 组，触发通道熔断守卫，停止运行 ===')
            break

        if MAX_GROUPS and done_groups >= MAX_GROUPS:
            log('=== 本轮已跑满 %d 组，顺利完成 ===' % MAX_GROUPS)
            break

    k, s, c, ev = maxids()
    log('=== 当前状态汇总: K%d S%d C%d 共 %d 卡，证据索引 %d 条 ===' % (k, s, c, k + s + c, ev))


if __name__ == '__main__':
    main()
