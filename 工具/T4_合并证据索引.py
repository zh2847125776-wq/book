# -*- coding: utf-8 -*-
"""T4：合并各分片证据索引 → 主库 05_证据索引/证据清单.tsv

规则：
- 以主库 01_资料与索引/证据索引.tsv 为基（操作主，卡与工具读它）
- 追加各分片 out/01_资料与索引/证据索引.tsv 中「主库没有的」行（同 E-ID 跳过，遵循 工具/分片_合并.py 既有规则）
- 冲突行（主库已有同号但内容不同）**不并入**，单独出报告待决
- 输出按 E 号数值升序
"""
import pathlib
import shutil
import csv
import io
import sys
from datetime import datetime

BASE = pathlib.Path(r'C:\Users\赵豪\dsh\交易知识体系汇编')
LIVE = BASE / '01_资料与索引/证据索引.tsv'
OUTDIR = BASE / '05_证据索引'
SHARDS = ['Claude', 'Codex', 'Pro2', 'Redo166', 'Shard3_b220_243', '_已退役_Shard3_v1']
HEADER = '证据ID\tsource_id\t位置\t原文摘录\t用途\t登记时间'


def detect_nl(p):
    """探测原文件行尾，避免合并时整文件改写行尾。"""
    raw = p.read_bytes()
    return '\r\n' if b'\r\n' in raw[:4096] else '\n'


def load(p):
    """返回 {eid: 行原文(不含换行)}"""
    out = {}
    lines = p.read_text(encoding='utf-8').splitlines()
    for r in lines[1:]:
        if not r.strip():
            continue
        eid = r.split('\t')[0]
        out[eid] = r
    return out


def ekey(eid):
    try:
        return int(eid[2:])
    except ValueError:
        return 10 ** 9


def main():
    if not LIVE.is_file():
        sys.exit('主库索引不存在: %s' % LIVE)

    main_rows = load(LIVE)
    print('主库现有 %d 条' % len(main_rows))

    merged = dict(main_rows)
    safe_total, conflict = 0, []
    per_shard = []

    for s in SHARDS:
        f = BASE / '分片工作区' / s / 'out/01_资料与索引/证据索引.tsv'
        if not f.is_file():
            continue
        rows = load(f)
        safe = {k: v for k, v in rows.items() if k not in main_rows}
        conf = {k: v for k, v in rows.items() if k in main_rows}
        # 冲突里若两侧内容完全一致，不算冲突（可直接跳过）
        real_conf = {k: v for k, v in conf.items() if v != main_rows[k]}
        same = len(conf) - len(real_conf)
        merged.update(safe)
        safe_total += len(safe)
        for k in sorted(real_conf, key=ekey):
            conflict.append((s, k, main_rows[k], real_conf[k]))
        per_shard.append((s, len(rows), len(safe), len(real_conf), same))
        print('  %-20s 共 %5d ｜ 并入 %5d ｜ 内容相同跳过 %4d ｜ **冲突 %4d**'
              % (s, len(rows), len(safe), same, len(real_conf)))

    print()
    print('可并入合计 %d ｜ 冲突合计 %d ｜ 合并后 %d 条' % (safe_total, len(conflict), len(merged)))

    # 备份操作主
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    bak = LIVE.with_name(LIVE.name + '.bak-%s-before-T4merge' % ts)
    shutil.copy2(LIVE, bak)
    print('备份: %s' % bak)

    # 写操作主（升序，保留原行尾）
    nl = detect_nl(LIVE)
    order = sorted(merged, key=ekey)
    body = nl.join(merged[k] for k in order)
    LIVE.write_bytes((HEADER + nl + body + nl).encode('utf-8'))
    print('已写 %s  (%d 行, 行尾 %s)' % (LIVE, len(merged), repr(nl)))

    # 交付副本
    OUTDIR.mkdir(exist_ok=True)
    deliver = OUTDIR / '证据清单.tsv'
    shutil.copy2(LIVE, deliver)
    print('已写 %s' % deliver)

    # 冲突报告
    if conflict:
        rep = OUTDIR / '冲突报告_合并前待决.tsv'
        with open(rep, 'w', encoding='utf-8', newline='') as fh:
            w = csv.writer(fh, delimiter='\t')
            w.writerow(['来源分片', '证据ID', '主库source_id', '主库原文摘录(前80)',
                        '分片source_id', '分片原文摘录(前80)', '主库位置', '分片位置'])
            for s, k, a, b in conflict:
                pa, pb = a.split('\t'), b.split('\t')
                pa += [''] * (6 - len(pa)); pb += [''] * (6 - len(pb))
                w.writerow([s, k, pa[1], pa[3][:80], pb[1], pb[3][:80], pa[2][:40], pb[2][:40]])
        print('已写冲突报告 %s (%d 条)' % (rep, len(conflict)))

    # 摘要
    summ = OUTDIR / '合并摘要.md'
    lines = ['# 证据索引合并摘要（T4）', '', '时间：%s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
             '', '## 结果', '',
             '| 项 | 值 |', '|---|---:|',
             '| 合并前主库 | %d |' % len(main_rows),
             '| 本次并入 | %d |' % safe_total,
             '| 冲突待决 | %d |' % len(conflict),
             '| 合并后 | %d |' % len(merged), '',
             '## 各分片', '', '| 分片 | 索引行数 | 并入 | 内容相同跳过 | 冲突 |', '|---|---:|---:|---:|---:|']
    for s, n, sf, cf, sm in per_shard:
        lines.append('| %s | %d | %d | %d | %d |' % (s, n, sf, sm, cf))
    lines += ['', '## 规则', '',
              '- 基：`01_资料与索引/证据索引.tsv`（操作主，卡片与工具读它）',
              '- 追加：各分片 `out/01_资料与索引/证据索引.tsv` 中主库没有的号（同 E-ID 跳过，遵循 `工具/分片_合并.py` 既有规则）',
              '- **冲突行（主库已有同号但内容不同）不并入**，见 `冲突报告_合并前待决.tsv`',
              '- 输出按 E 号数值升序',
              '- 交付副本：`05_证据索引/证据清单.tsv`（与操作主内容一致）', '']
    summ.write_text('\n'.join(lines), encoding='utf-8')
    print('已写摘要 %s' % summ)


if __name__ == '__main__':
    main()
