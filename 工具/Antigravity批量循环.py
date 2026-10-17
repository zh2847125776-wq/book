# -*- coding: utf-8 -*-
"""Antigravity 批量抽取循环。

自动按批号顺序推进全量剩余来源，无 Arena 网页会话/抽卡/指纹等历史包袱：
1. 扫描工作分片中所有尚未完全抽取的批次（当前最早为批078）。
2. 每轮调用 Antigravity驱动_连续抽取.py 处理指定组数（或整批）。
3. 统计增量（来源、卡片、证据索引），连续 2 轮零进展则安全停止并告警。
4. 支持按组数限制或按批次推进。

用法:
    python Antigravity批量循环.py [每组份数, 默认2] [每批最多组数, 默认0=跑完整批] [模型, 默认gemini-3.8-flash-high]
"""
import csv
import glob
import os
import pathlib
import re
import subprocess
import sys
import time

BASE = pathlib.Path(r'C:\Users\赵豪\dsh')
OUT = BASE / '交易知识体系汇编'
LOG = pathlib.Path('C:/tmp/antigravity_loop.log')

GROUP = int(sys.argv[1]) if len(sys.argv) > 1 else 2
MAX_GROUPS_PER_BATCH = int(sys.argv[2]) if len(sys.argv) > 2 else 0
MODEL = sys.argv[3] if len(sys.argv) > 3 else 'gemini-3.8-flash-high'
MAX_BATCH_NUM = int(sys.argv[4]) if len(sys.argv) > 4 else 243


def log(msg):
    line = '[%s] %s' % (time.strftime('%m-%d %H:%M:%S'), msg)
    print(line, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def done_count():
    p = OUT / '01_资料与索引/来源去向.tsv'
    lines = p.read_text(encoding='utf-8').splitlines()
    h = lines[0].split('\t')
    sti = h.index('处理状态')
    return sum(1 for l in lines[1:] if len(l.split('\t')) > sti and l.split('\t')[sti] == '已抽取')


def done_set():
    p = OUT / '01_资料与索引/来源去向.tsv'
    lines = p.read_text(encoding='utf-8').splitlines()
    h = lines[0].split('\t')
    si, sti = h.index('source_id'), h.index('处理状态')
    SKIP = {'已抽取', '工具脚本·无可用内容', '无可用交易内容'}
    return {l.split('\t')[si] for l in lines[1:]
            if len(l.split('\t')) > sti and l.split('\t')[sti] in SKIP}


def card_counts():
    k = len(list((OUT / '02_知识点').glob('K-*.md')))
    s = len(list((OUT / '03_方法与策略').glob('S-*.md')))
    c = len(list((OUT / '04_案例').glob('C-*.md')))
    ev = len(re.findall(r'(?m)^E-(\d{4,5})\t', (OUT / '01_资料与索引/证据索引.tsv').read_text(encoding='utf-8')))
    return k, s, c, k + s + c, ev


def get_outstanding_batches():
    dn = done_set()
    outstanding = []
    for f in sorted((OUT / '工作分片').glob('批*_清单.tsv')):
        m = re.match(r'批(\d+)_清单', f.name)
        if not m:
            continue
        rows = list(csv.DictReader(open(f, encoding='utf-8'), delimiter='\t'))
        left = [r for r in rows if r['source_id'] not in dn]
        if left:
            outstanding.append((int(m.group(1)), '批%s' % m.group(1), len(left), len(rows)))
    outstanding.sort()
    return outstanding


def run_driver(batch, max_groups=0):
    cmd = [
        'python', '-X', 'utf8',
        str(OUT / '工具/Antigravity驱动_连续抽取.py'),
        batch, str(GROUP), str(max_groups), MODEL
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=14400)
    return res.returncode, res.stdout, res.stderr


def main():
    log('=== Antigravity 批量抽取循环启动 ===')
    log('配置: 每组 %d 份 | 每批最多 %s 组 | 模型 %s'
        % (GROUP, str(MAX_GROUPS_PER_BATCH) if MAX_GROUPS_PER_BATCH else '不限', MODEL))

    zero_progress_count = 0
    round_no = 0

    while True:
        round_no += 1
        outstanding = get_outstanding_batches()
        if not outstanding:
            log('=== 全部批次与来源均已抽取完毕！===')
            break

        total_left = sum(item[2] for item in outstanding)
        log('--- 循环第 %d 轮 | 待处理批次: %d 个 | 待处理来源: %d 份 ---'
            % (round_no, len(outstanding), total_left))
        log('前序待跑批次: %s' % ' | '.join('%s(%d/%d)' % (b, l, t) for _, b, l, t in outstanding[:5]))

        batch_num = outstanding[0][0]
        if batch_num > MAX_BATCH_NUM:
            log('=== 达到上限批次（批%d > 批%d），循环安全停止，严防越界 ===' % (batch_num, MAX_BATCH_NUM))
            break

        target_batch = outstanding[0][1]
        log('本轮处理目标: %s' % target_batch)

        before_done = done_count()
        bk, bs, bc, b_tot, b_ev = card_counts()

        rc, stdout, stderr = run_driver(target_batch, MAX_GROUPS_PER_BATCH)

        for line in (stdout or '').strip().splitlines()[-10:]:
            log('  [驱动] ' + line)

        after_done = done_count()
        ak, as_, ac, a_tot, a_ev = card_counts()

        delta_src = after_done - before_done
        delta_cards = a_tot - b_tot
        delta_ev = a_ev - b_ev

        log('本轮完成: %s | 来源增量: +%d | 卡片增量: +%d (K+%d/S+%d/C+%d) | 证据增量: +%d'
            % (target_batch, delta_src, delta_cards, ak - bk, as_ - bs, ac - bc, delta_ev))

        if delta_src == 0 and delta_cards == 0:
            zero_progress_count += 1
            wait_sec = min(180, 30 * zero_progress_count)
            log('!! 连续零进展第 %d/6 次，等待 %d 秒后重试...' % (zero_progress_count, wait_sec))
            if zero_progress_count >= 6:
                log('=== 连续 6 轮无进展，停止循环以待人工检查 ===')
                break
            time.sleep(wait_sec)
        else:
            zero_progress_count = 0
            time.sleep(2)


if __name__ == '__main__':
    main()
