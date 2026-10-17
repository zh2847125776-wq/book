# -*- coding: utf-8 -*-
"""Antigravity 第二路分片连续抽取驱动（Pro2 专属通道）。

定位：
1. 消费《分片工作区/Pro2》，与主仓库物理隔离，绝不直接写主仓库。
2. 批次倒序相向包抄：从 批361 倒序往前抽（361 -> 360 -> 359 ... -> 200）。
3. 专属保留号段：
   - K: 50000 ~ 69999
   - S: 5000 ~ 9999
   - C: 5000 ~ 9999
   - E: 80000 ~ 119999
   绝对不与主仓（K-31xxx, E-66xxx）及 Claude/Codex 历史分片冲突。
4. 调用 agy 时隔离 USERPROFILE 至 C:\\Users\\赵豪\\.gemini_pro2，并支持 PRO2 API Key / 凭据。
5. 入库时第 6 参数指向 分片工作区/Pro2/out，通过逐字回源与卡片护栏后落入分片。
6. 任何时候均可运行 `python 工具/分片_合并.py Pro2` 一键幂等并入主库。

用法:
    python 工具/Antigravity分片驱动_Pro2.py [起始批号, 默认361] [每组份数, 默认2] [模型, 默认gemini-3.8-flash-high]
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
MAIN_REPO = BASE / '交易知识体系汇编'
SHARD_ROOT = MAIN_REPO / '分片工作区/Pro2'
SHARD_OUT = SHARD_ROOT / 'out'
STAGE = SHARD_ROOT / 'stage'
REPLY_FILE = SHARD_ROOT / 'reply/cur_reply.md'
LOG_FILE = SHARD_ROOT / 'pro2_driver.log'
AGY_EXE = pathlib.Path(r'C:\ProgramData\agy\bin\agy.exe')
if not AGY_EXE.is_file():
    AGY_EXE = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'agy/bin/agy.exe'
PRO2_HOME = pathlib.Path(r'C:\Users\赵豪\.gemini_pro2')


def log(msg):
    line = '[%s] %s' % (time.strftime('%H:%M:%S'), msg)
    print(line, flush=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def load_shard_cfg():
    cfg_p = SHARD_ROOT / '号段.json'
    if not cfg_p.is_file():
        raise SystemExit('未找到号段配置文件: %s' % cfg_p)
    return json.loads(cfg_p.read_text(encoding='utf-8'))


def maxids_shard(cfg):
    k_min, k_max = cfg['K']
    s_min, s_max = cfg['S']
    c_min, c_max = cfg['C']
    e_min, e_max = cfg['E']

    k_files = [int(p.stem.split('_')[0].split('-')[1]) for p in (SHARD_OUT / '02_知识点').glob('K-*.md')]
    s_files = [int(p.stem.split('_')[0].split('-')[1]) for p in (SHARD_OUT / '03_方法与策略').glob('S-*.md')]
    c_files = [int(p.stem.split('_')[0].split('-')[1]) for p in (SHARD_OUT / '04_案例').glob('C-*.md')]

    ev_path = SHARD_OUT / '01_资料与索引/证据索引.tsv'
    ev_list = []
    if ev_path.is_file():
        ev_list = [int(x) for x in re.findall(r'(?m)^E-(\d{4,6})\t', ev_path.read_text(encoding='utf-8'))]

    cur_k = max(k_files) if k_files else k_min - 1
    cur_s = max(s_files) if s_files else s_min - 1
    cur_c = max(c_files) if c_files else c_min - 1
    cur_e = max(ev_list) if ev_list else e_min - 1

    return cur_k, cur_s, cur_c, cur_e


def done_sources_shard():
    p = SHARD_OUT / '01_资料与索引/来源去向.tsv'
    if not p.is_file():
        return set()
    lines = p.read_text(encoding='utf-8').splitlines()
    if not lines:
        return set()
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
    for f in sorted(glob.glob(str(MAIN_REPO / '工作分片/批*_清单.tsv'))):
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
    spec = importlib.util.spec_from_file_location('gen', str(MAIN_REPO / '工具/Arena任务_生成提示.py'))
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

"""
    prompt = instr + base_text
    pf = SHARD_ROOT / 'reply/arena_prompt_cur.txt'
    pf.write_text(prompt, encoding='utf-8')
    return pf, len(prompt)


def call_antigravity(prompt_text, timeout_sec=900, model='gemini-3.8-flash-high'):
    if not AGY_EXE.is_file():
        return False, 'AGY_EXE 不存在: %s' % AGY_EXE

    env = os.environ.copy()
    current_user = os.environ.get('USERNAME', '').lower()
    if 'worker' not in current_user:
        env['USERPROFILE'] = str(PRO2_HOME)
        env['HOME'] = str(PRO2_HOME)
    env['HTTPS_PROXY'] = 'http://127.0.0.1:7897'
    env['HTTP_PROXY'] = 'http://127.0.0.1:7897'
    env['https_proxy'] = 'http://127.0.0.1:7897'
    env['http_proxy'] = 'http://127.0.0.1:7897'
    env['NO_PROXY'] = 'localhost,127.0.0.1,::1'
    env['no_proxy'] = 'localhost,127.0.0.1,::1'

    # 支持通过环境变量直接注入第二账号 API KEY
    pro2_api_key = os.environ.get('GEMINI_API_KEY_PRO2') or os.environ.get('GEMINI_API_KEY')
    if pro2_api_key:
        env['GEMINI_API_KEY'] = pro2_api_key

    cmd = [str(AGY_EXE), '--model', model, '--dangerously-skip-permissions', '--print', prompt_text]
    t0 = time.time()
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=timeout_sec, cwd=str(MAIN_REPO))
        elapsed = time.time() - t0
        if res.returncode != 0:
            err = (res.stderr or '').strip()
            out = (res.stdout or '').strip()
            return False, 'EXIT_%d (耗时 %.1fs): %s | %s' % (res.returncode, elapsed, out[:150], err[:150])
        body = res.stdout or ''
        if not body.strip():
            return False, 'EMPTY_OUTPUT (耗时 %.1fs)' % elapsed
        return True, body
    except subprocess.TimeoutExpired:
        return False, 'TIMEOUT (超过 %ds)' % timeout_sec
    except Exception as ex:
        return False, 'EXCEPTION: %s' % str(ex)


def run_one_batch(batch_num, group_size=2, model='gemini-3.8-flash-high'):
    cfg = load_shard_cfg()
    batch_str = '批%03d' % batch_num
    manifest = MAIN_REPO / '工作分片' / (batch_str + '_清单.tsv')
    if not manifest.is_file():
        log('清单文件不存在: %s，跳过该批。' % manifest)
        return True

    rows = list(csv.DictReader(open(str(manifest), encoding='utf-8'), delimiter='\t'))
    dn = done_sources_shard()
    todo = [r for r in rows if r['source_id'] not in dn]

    log('====================================================')
    log('【Pro2 第二通道】正在处理: %s | 总来源: %d | 待抽: %d' % (batch_str, len(rows), len(todo)))
    log('====================================================')

    if not todo:
        log('本批全部来源在分片中已完成，跳过。')
        return True

    BUDGET = 70000
    groups, _cur, _sz = [], [], 0
    for r in todo:
        rel = ((r.get('完整稿(阅读对象)') or '').strip() or (r.get('精简稿(导航用)') or '').strip())
        p = BASE / rel
        sz = p.stat().st_size if p.is_file() else 0
        if _cur and (len(_cur) >= group_size or _sz + sz > BUDGET or sz > 50000):
            groups.append(_cur); _cur, _sz = [], 0
        _cur.append(r); _sz += sz
    if _cur:
        groups.append(_cur)

    fail_consecutive = 0
    for gi, pair in enumerate(groups):
        picks = [r['source_id'] for r in pair]
        types = [r['课型'] for r in pair]
        log('--- 组 %d/%d: %s（%s）---' % (gi + 1, len(groups), picks, '/'.join(types)))

        cur_k, cur_s, cur_c, cur_e = maxids_shard(cfg)
        unit = max(1, len(pair) // 2)

        k0 = cur_k + 1
        s0 = cur_s + 1
        c0 = cur_c + 1
        e0 = cur_e + 1

        # 检查是否溢出分片号段上限
        if (k0 + 8 * unit > cfg['K'][1] or s0 + 5 * unit > cfg['S'][1] or
                c0 + 5 * unit > cfg['C'][1] or e0 + 20 * unit > cfg['E'][1]):
            log('=== 警告：分片号段已用尽，停止推进。请运行 分片_准备.py 扩充号段 ===')
            return False

        ids = ('%04d' % k0, '%04d' % (k0 + 8 * unit),
               '%04d' % s0, '%04d' % (s0 + 5 * unit),
               '%04d' % c0, '%04d' % (c0 + 5 * unit),
               '%04d' % e0, '%04d' % (e0 + 20 * unit - 1))

        got = stage_files(picks)
        if len(got) < len(picks):
            log('  备料不全（实际 %d / 需 %d），跳过本组' % (len(got), len(picks)))
            continue

        note = '本组资料：' + '；'.join('%s（第%s课 %s，课型%s）' % (r['source_id'], r['课号'], r['主题'], r['课型']) for r, _ in got)
        note += '。**若这些资料属于同一系列，注意不要跨系列串联策略；若与已有卡讲同一件事，写「补充 K-xxxx」不要新建。**'
        note += '**请先核对底本层级**：若给的是"(增强版)"笔记而非完整稿，务必在卡片里标「仅增强稿可见」，不要写成完整稿。'

        run_token = 'RUN-PRO2-%s-G%d-%d' % (batch_str, gi + 1, int(time.time()))
        pf, ln = gen_prompt(picks, ids, note, got, run_token)
        log('  提示已就绪: %d 字符 | 分片号段 K%s-%s S%s-%s C%s-%s E%s-%s' % (ln, *ids))

        prompt_content = pf.read_text(encoding='utf-8')
        log('  派发 Antigravity 抽取任务 (模型 %s)...' % model)
        t_start = time.time()
        ok, reply_body = call_antigravity(prompt_content, timeout_sec=900, model=model)
        call_dur = time.time() - t_start

        if not ok:
            log('  ✗ 模型调用失败 (%.1fs): %s' % (call_dur, reply_body))
            fail_consecutive += 1
            if fail_consecutive >= 2:
                log('=== 连续失败 2 组，停止当前批次以防额度浪费 ===')
                return False
            continue

        log('  ✓ 模型回复接收成功 (%.1fs, %d 字符)' % (call_dur, len(reply_body)))

        REPLY_FILE.unlink(missing_ok=True)
        REPLY_FILE.write_text(reply_body, encoding='utf-8')

        # 调用原版 Arena入库.py，指定第 6 参数为 SHARD_OUT
        cmd_ing = ['python', '-X', 'utf8', str(MAIN_REPO / '工具/Arena入库.py'),
                   str(REPLY_FILE), ids[6], ids[7], str(STAGE), ','.join(picks), str(SHARD_OUT)]
        ing = subprocess.run(cmd_ing, capture_output=True, text=True, timeout=600)
        for ln in (ing.stdout or '').strip().splitlines():
            log('    ' + ln)

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
            log('  ✓ 分片入库成功')
            fail_consecutive = 0
            archive_name = '分片产出_Pro2_%s.md' % '_'.join(sorted(picks))
            shutil.copy2(str(REPLY_FILE), SHARD_OUT / '07_审计与交付' / archive_name)

        if fail_consecutive >= 2:
            log('=== 连续失败 2 组，停止当前批次 ===')
            return False

    return True


def main():
    cfg = load_shard_cfg()
    ranges = cfg.get('batches', [[200, 361]])
    
    # 收集全部待跑批次，按倒序排列（361 -> 360 -> ... -> 200）
    all_batches = []
    for lo, hi in ranges:
        all_batches.extend(range(lo, hi + 1))
    all_batches = sorted(all_batches, reverse=True)

    start_batch = int(sys.argv[1]) if len(sys.argv) > 1 else all_batches[0]
    group_size = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    model = sys.argv[3] if len(sys.argv) > 3 else 'gemini-3.8-flash-high'

    # 定位起始批号
    if start_batch in all_batches:
        idx = all_batches.index(start_batch)
        all_batches = all_batches[idx:]

    log('========================================================')
    log('=== Antigravity 第二路分片循环启动（Pro2 专属通道） ===')
    log('批次总数: %d | 扫描方向: 倒序（%d -> %d）' % (len(all_batches), all_batches[0], all_batches[-1]))
    log('隔离主目录: %s' % PRO2_HOME)
    log('分片工作区: %s' % SHARD_ROOT)
    log('模型: %s' % model)
    log('========================================================')

    for b in all_batches:
        ok = run_one_batch(b, group_size=group_size, model=model)
        if not ok:
            log('批次 %03d 遭遇阻滞，暂停 30 秒后重试...' % b)
            time.sleep(30)
        else:
            log('批次 %03d 完成或跳过，继续推进下一批。' % b)
            time.sleep(3)


if __name__ == '__main__':
    main()
