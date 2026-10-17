# -*- coding: utf-8 -*-
"""修悬空引用：补登漏解析的证据号 + 标注 C 组未建的案例卡。"""
import csv
import pathlib
import re

OUT = pathlib.Path(r'C:\Users\赵豪\dsh\交易知识体系汇编')
IDX = OUT / '01_资料与索引'
SHARD = OUT / '工作分片'

# ── 1) 从记录里补登漏解析的证据号（表格行可能跨行或格式微异）──
need = ['E-0040', 'E-0107', 'E-0121']
found = {}
for f in sorted(SHARD.glob('批*_抽取_*.md')):
    text = f.read_text(encoding='utf-8')
    for eid in need:
        if eid in found:
            continue
        m = re.search(r'\|\s*' + eid + r'\s*\|\s*(SRC-\d{6}[^|]*)\|\s*([^|]*)\|\s*([^|]*)\|\s*([^|]*)\|', text)
        if not m:
            m2 = re.search(r'^' + eid + r'\t([^\t]*)\t([^\t]*)\t([^\t]*)\t([^\t]*)', text, re.M)
            if m2:
                found[eid] = (m2.group(1), m2.group(2), m2.group(3), m2.group(4))
        else:
            found[eid] = (m.group(1), m.group(2), m.group(3), m.group(4))
print('从记录找回:', {k: v[0][:22] for k, v in found.items()})

evfile = IDX / '证据索引.tsv'
lines = evfile.read_text(encoding='utf-8').splitlines()
have = {l.split('\t')[0] for l in lines[1:]}
add = 0
with open(evfile, 'a', encoding='utf-8') as f:
    for eid in need:
        if eid in have:
            continue
        if eid in found:
            s, pos, quote, use = found[eid]
            f.write('\t'.join([eid, '、'.join(re.findall(r'SRC-\d{6}', s)[:2]), pos.strip()[:60],
                               quote.strip()[:120].replace('\t', ' '), use.strip()[:70], '2026-09-28']) + '\n')
        else:
            f.write('\t'.join([eid, '', '（记录中未定位到该行，待回查）', '', '待回查', '2026-09-28']) + '\n')
        add += 1
print('证据索引补登: %d 条' % add)

# ── 2) 标注 C 组未建的案例卡引用 ──
missing_cases = ['C-0021', 'C-0022', 'C-0023', 'C-0024']
touched = 0
for d in ('02_知识点', '03_方法与策略', '04_案例'):
    for p in sorted((OUT / d).glob('*.md')):
        t = p.read_text(encoding='utf-8')
        o = t
        for c in missing_cases:
            t = re.sub(r'\b' + c + r'\b(?!（未建)', c + '（未建·批003 C组中断）', t)
        if t != o:
            p.write_text(t, encoding='utf-8')
            touched += 1
print('标注未建案例卡引用的卡片: %d 张' % touched)

# ── 3) 登记缺口 ──
g = OUT / '07_审计与交付/规则冲突与缺口.tsv'
extra = """69\t缺口\t批003 C组四张案例卡未建\tC组子代理中途失败，K-0075~K-0088 与 S-0029~S-0035 引用的 C-0021~C-0024 未创建（C组只建成 C-0020）。引用已就地标注「未建·批003 C组中断」\tSRC-003577,SRC-003966,SRC-003968,SRC-004200,SRC-004212\t待补：来源为第07课、第1349/1350课、第155/156课
"""
g.write_text(g.read_text(encoding='utf-8') + extra, encoding='utf-8')
print('已登记缺口 69')
