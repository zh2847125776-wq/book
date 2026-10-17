# -*- coding: utf-8 -*-
"""把一个分片工作区的产出合并进主仓库（幂等：已存在的文件/证据/台账行跳过）。
  python -X utf8 工具/分片_合并.py <Codex|Claude> [--dry]

合并内容：
 1. out/02_知识点、03_方法与策略、04_案例 下的卡片文件 → 主仓库同名目录（同名文件跳过）
 2. out/补充卡片/*.md 补丁 → 追加到主仓库对应卡片（目标不存在则挂起报告，不丢）
 3. out/01_资料与索引/证据索引.tsv → 追加到主证据索引（同 E-ID 跳过）
 4. out/07_审计与交付/分片产出_*.md → 主审计目录（同名跳过）
 5. 分片台账里状态为「已抽取」的来源 → 主台账对应行标已抽取
"""
import pathlib
import re
import sys

OUT = pathlib.Path(r'C:\Users\赵豪\dsh\交易知识体系汇编')


def tsv_rows(p):
    lines = p.read_text(encoding='utf-8').splitlines()
    return lines[0], lines[1:]


def main():
    name = sys.argv[1]
    dry = '--dry' in sys.argv
    root = OUT / '分片工作区' / name
    out = root / 'out'
    assert root.is_dir(), '分片不存在: %s' % root
    moves, adds, leds, proofs = [], [], [], []

    for d in ('02_知识点', '03_方法与策略', '04_案例'):
        for f in sorted((out / d).glob('*.md')):
            dst = OUT / d / f.name
            if dst.exists():
                continue
            moves.append((f, dst))

    mhead, mrows = tsv_rows(OUT / '01_资料与索引/证据索引.tsv')
    have_ev = {r.split('\t')[0] for r in mrows if r.strip()}
    shead, srows = tsv_rows(out / '01_资料与索引/证据索引.tsv')
    assert shead.split('\t')[0] == '证据ID', '分片证据索引表头不对'
    for r in srows:
        if r.strip() and r.split('\t')[0] not in have_ev:
            adds.append(r)

    patches, dangling = [], []
    if (out / '补充卡片').is_dir():
        for f in sorted((out / '补充卡片').glob('*.md')):
            target = f.stem.split('_')[0]
            hit = []
            for d in ('02_知识点', '03_方法与策略', '04_案例'):
                hit += list((OUT / d).glob('%s_*.md' % target))
            if not hit:
                dangling.append(f.name)
                continue
            try:
                title = f.read_text(encoding='utf-8').splitlines()[1]
                if title.startswith('补充标题：'):
                    title = title[len('补充标题：'):]
            except Exception:
                title = ''
            t = hit[0].read_text(encoding='utf-8')
            if title and title[:16] in t:
                continue
            patches.append((f, hit[0]))

    for f in sorted((out / '07_审计与交付').glob('*.md')):
        dst = OUT / '07_审计与交付' / f.name
        if dst.exists():
            continue
        proofs.append((f, dst))

    _, mled = tsv_rows(OUT / '01_资料与索引/来源去向.tsv')
    # 取分片台账里已抽取的 source_id
    s_done = set()
    for p, collect in ((OUT / '01_资料与索引/来源去向.tsv', None), (out / '01_资料与索引/来源去向.tsv', s_done)):
        head, rows = tsv_rows(p)
        h = head.split('\t')
        if collect is not None:
            si, sti = h.index('source_id'), h.index('处理状态')
            for r in rows:
                c = r.split('\t')
                if len(c) > sti and c[si] and c[sti] == '已抽取':
                    collect.add(c[si])
    mhead2, mrows2 = tsv_rows(OUT / '01_资料与索引/来源去向.tsv')
    h2 = mhead2.split('\t')
    si2, sti2 = h2.index('source_id'), h2.index('处理状态')
    for i, r in enumerate(mrows2):
        c = r.split('\t')
        if len(c) > sti2 and c[si2] in s_done and c[sti2] != '已抽取':
            c[sti2] = '已抽取'
            mrows2[i] = '\t'.join(c)
            leds.append(c[si2])

    print('卡片待合并: %d | 补充待追加: %d | 证据待追加: %d | 产出待归档: %d | 台账待标记: %d'
          % (len(moves), len(patches), len(adds), len(proofs), len(leds)))
    if dangling:
        print('!! 目标卡不存在的补丁（挂起，下次重跑合并）: %s' % ','.join(dangling[:12]))
    if dry:
        for f, _ in moves[:10]:
            print('  卡片', f.name)
        for f, _ in patches[:10]:
            print('  补充', f.name)
        return
    for f, dst in moves:
        dst.write_bytes(f.read_bytes())
    for f, dst in patches:
        body = f.read_text(encoding='utf-8')
        lines = body.splitlines()
        title = lines[1] if len(lines) > 1 else f.name
        if title.startswith('补充标题：'):
            title = title[len('补充标题：'):]
        content = '\n'.join(lines[2:]).strip()
        with open(dst, 'a', encoding='utf-8') as fh:
            fh.write('\n\n---\n\n## 补充：' + title + '\n' + content + '\n')
    with open(OUT / '01_资料与索引/证据索引.tsv', 'a', encoding='utf-8') as fh:
        for r in adds:
            fh.write(r + '\n')
    for f, dst in proofs:
        dst.write_bytes(f.read_bytes())
    (OUT / '01_资料与索引/来源去向.tsv').write_text(mhead2 + '\n' + '\n'.join(mrows2) + '\n', encoding='utf-8')
    print('合并完成: 卡片 %d, 补充 %d, 证据 %d, 产出 %d, 台账 %d' % (len(moves), len(patches), len(adds), len(proofs), len(leds)))


if __name__ == '__main__':
    main()
