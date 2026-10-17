# -*- coding: utf-8 -*-
"""把两个分片（Claude / Codex）的已抽成果同步回主台账 处理状态。

只改一件事：分片号段内、分片已判为终态（已抽取 / 无可用交易内容 / 工具脚本·无可用内容）
的来源，在主台账里从 已排批/待处理 改成同样的终态，并在备注里标注来源片与产物位置。

不改：路径、版本标识、非号段来源、分片未处理的来源。
用法：
    python3 工具/分片回写主台账.py            # dry-run，只打印
    python3 工具/分片回写主台账.py --apply    # 落盘（先自动备份）
"""
import csv
import pathlib
import shutil
import sys
import time

BASE = pathlib.Path(__file__).resolve().parent.parent
MAIN = BASE / '01_资料与索引/来源去向.tsv'
TERMINAL = {'已抽取', '无可用交易内容', '工具脚本·无可用内容'}

SHARDS = {
    'Claude': {'dir': BASE / '分片工作区/Claude', 'batches': list(range(132, 185)) + list(range(303, 362))},
    'Codex': {'dir': BASE / '分片工作区/Codex', 'batches': list(range(78, 132)) + list(range(244, 303))},
}


def read_tsv(p):
    with open(p, encoding='utf-8', newline='') as f:
        return list(csv.reader(f, delimiter='\t'))


def shard_status(shard):
    """返回 {source_id: 状态} —— 该片 out 台账里为终态的来源。"""
    p = shard['dir'] / 'out/01_资料与索引/来源去向.tsv'
    out = {}
    for r in read_tsv(p)[1:]:
        if len(r) > 3 and r[3] in TERMINAL:
            out[r[0]] = r[3]
    return out


def shard_batch_sources(shard):
    """该片号段内、清单上出现过的全部 source_id。"""
    srcs = set()
    for n in shard['batches']:
        p = BASE / ('工作分片/批%03d_清单.tsv' % n)
        if not p.exists():
            continue
        for line in p.read_text(encoding='utf-8').splitlines()[1:]:
            if line.strip():
                srcs.add(line.split('\t')[0])
    return srcs


def main():
    apply = '--apply' in sys.argv
    rows = read_tsv(MAIN)
    hdr, body = rows[0], rows[1:]
    assert hdr[3] == '处理状态' and hdr[4] == '备注', hdr

    plan = {}  # source_id -> (新状态, 备注追加)
    for name, shard in SHARDS.items():
        st = shard_status(shard)
        inscope = shard_batch_sources(shard)
        for sid in sorted(inscope):
            if sid not in st:
                continue
            plan[sid] = (st[sid], '｜分片已抽取(%s)' % name)

    changed = 0
    detail = {}
    for r in body:
        sid = r[0]
        if sid not in plan:
            continue
        new_st, note = plan[sid]
        if r[3] in TERMINAL:
            continue
        r[3] = new_st
        r[4] = (r[4] + note) if r[4] else note.lstrip('｜')
        changed += 1
        detail[new_st] = detail.get(new_st, 0) + 1

    print('主台账总行数      :', len(body))
    print('号段内终态来源数  :', len(plan))
    print('本次将改动行数    :', changed)
    for k, v in detail.items():
        print('   %-18s %d' % (k, v))

    if not apply:
        print('\n[dry-run] 未落盘。加 --apply 生效。')
        return

    bak = MAIN.with_name(MAIN.name + '.bak-%s-before-shardsync' % time.strftime('%Y%m%d-%H%M%S'))
    shutil.copy2(MAIN, bak)
    tmp = MAIN.with_suffix('.tsv.tmp')
    with open(tmp, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(hdr)
        w.writerows(body)
    tmp.replace(MAIN)
    print('\n备份:', bak)
    print('已写入:', MAIN)


if __name__ == '__main__':
    main()
