# -*- coding: utf-8 -*-
"""建一个隔离的分片工作区：
  python -X utf8 工具/分片_准备.py <Codex|Claude> <K起> <K止> <S起> <S止> <C起> <C止> <E起> <E止> <批号起> <批号止> [批号起2 批号止2 ...]

在 交易知识体系汇编/分片工作区/<名>/ 下建 out/（02/03/04/01_资料与索引/07_审计与交付）、
stage/、reply/，并把主台账 来源去向.tsv 复制一份过去做分片台账。
号段与批次范围写进 号段.json；三路号段互不重叠，合并时无需重编号。
"""
import json
import pathlib
import shutil
import sys

OUT = pathlib.Path(r'C:\Users\赵豪\dsh\交易知识体系汇编')


def main():
    name = sys.argv[1]
    k0, k1, s0, s1, c0, c1, e0, e1 = map(int, sys.argv[2:10])
    assert len(sys.argv) >= 12 and len(sys.argv) % 2 == 0, '批次范围须成对给出'
    ranges = [(int(sys.argv[i]), int(sys.argv[i + 1])) for i in range(10, len(sys.argv), 2)]
    for a, b in ranges:
        assert 1 <= a <= b, '批次范围非法: %d-%d' % (a, b)
    root = OUT / '分片工作区' / name
    out = root / 'out'
    for d in ('02_知识点', '03_方法与策略', '04_案例', '01_资料与索引', '07_审计与交付'):
        (out / d).mkdir(parents=True, exist_ok=True)
    (root / 'stage').mkdir(parents=True, exist_ok=True)
    (root / 'reply').mkdir(parents=True, exist_ok=True)
    # 分片台账：从主台账复制，Codex/Claude 只在分片副本上标记，未经合并不动主台账
    shutil.copy2(OUT / '01_资料与索引/来源去向.tsv', out / '01_资料与索引/来源去向.tsv')
    (out / '01_资料与索引/证据索引.tsv').write_text('证据ID\tsource_id\t位置\t原文摘录\t用途\t登记时间\n', encoding='utf-8')
    meta = {
        'worker': name,
        'K': [k0, k1], 'S': [s0, s1], 'C': [c0, c1], 'E': [e0, e1],
        'batches': ranges,
    }
    (root / '号段.json').write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding='utf-8')
    print('分片就绪: %s' % root)
    print(json.dumps(meta, ensure_ascii=False))


if __name__ == '__main__':
    main()
