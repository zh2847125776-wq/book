# -*- coding: utf-8 -*-
"""通用来源回填：解析所有抽取记录的证据表 → 给仍缺来源行的卡片补绑。"""
import csv
import pathlib
import re

BASE = pathlib.Path(r'C:\Users\赵豪\dsh')
OUT = BASE / '交易知识体系汇编'
IDX = OUT / '01_资料与索引'
SHARD = OUT / '工作分片'

# 1) 汇总所有记录里的 E → SRC
ev = {}
for f in sorted(SHARD.glob('批*_抽取_*.md')):
    for line in f.read_text(encoding='utf-8').splitlines():
        s = line.strip()
        cells = None
        if s.startswith('|') and s.count('|') >= 5:
            cells = [c.strip() for c in s.strip('|').split('|')]
        elif '\t' in s and re.match(r'^E-\d{4}\t', s):
            cells = [c.strip() for c in s.split('\t')]
        if not cells or len(cells) < 5 or not re.fullmatch(r'E-\d{4}', cells[0]):
            continue
        srcs = re.findall(r'SRC-\d{6}', cells[1])
        if cells[0] not in ev and srcs:
            ev[cells[0]] = srcs
print('从记录解析出带来源的证据: %d 条' % len(ev))

# 2) 证据索引里的来源
evidx = {}
for r in csv.DictReader(open(IDX / '证据索引.tsv', encoding='utf-8'), delimiter='\t'):
    s = re.findall(r'SRC-\d{6}', r['source_id'] or '')
    if s:
        evidx[r['证据ID']] = s
print('证据索引里有来源的: %d 条' % len(evidx))
merged = dict(evidx)
for k, v in ev.items():
    merged.setdefault(k, v)

# 3) 来源清单（用于标签） 与 各批清单（用于内容匹配兜底）
src = {r['source_id']: r for r in csv.DictReader(open(IDX / '来源清单.tsv', encoding='utf-8'), delimiter='\t')}
man = {}
for m in sorted(SHARD.glob('批*_清单.tsv')):
    for r in csv.DictReader(open(m, encoding='utf-8'), delimiter='\t'):
        man[r['source_id']] = r


def label(sid):
    r = man.get(sid) or src.get(sid) or {}
    rel = r.get('相对路径', '')
    m = re.search(r'第\s*(\d+)\s*课', rel)
    return '%s（%s%s）' % (sid, '第%s课 ' % m.group(1) if m else '', (r.get('主题') or '')[:22])


def bind(p):
    t = p.read_text(encoding='utf-8')
    if re.search(r'^> 来源：SRC-', t, re.M):
        return None
    eids = sorted(set(re.findall(r'E-\d{4}', t)))
    srcs = []
    for e in eids:
        for s in merged.get(e, []):
            if s not in srcs:
                srcs.append(s)
    if not srcs:
        return None
    line = '> 来源：%s · 证据 %s\n' % ('、'.join(label(s) for s in srcs[:3]), '、'.join(eids) if eids else '—')
    lines = t.splitlines(True)
    pos = 1 if lines and lines[0].startswith('# ') else 0
    lines.insert(pos, line + ('\n' if pos + 1 < len(lines) and lines[pos + 1].strip() else ''))
    p.write_text(''.join(lines), encoding='utf-8')
    return p.stem


done = []
for d in ('02_知识点', '03_方法与策略', '04_案例'):
    for p in sorted((OUT / d).glob('*.md')):
        r = bind(p)
        if r:
            done.append(r)
print('本轮回填: %d 张' % len(done))

tot = [p for d in ('02_知识点', '03_方法与策略', '04_案例') for p in (OUT / d).glob('*.md')]
have = [p for p in tot if re.search(r'^> 来源：SRC-', p.read_text(encoding='utf-8'), re.M)]
print('来源行覆盖: %d/%d' % (len(have), len(tot)))
for p in tot:
    t = p.read_text(encoding='utf-8')
    if not re.search(r'^> 来源：SRC-', t, re.M):
        n = len(set(re.findall(r'E-\d{4}', t)))
        print('  仍缺来源:', p.stem[:44], '| E号', n, '| 有无SRC', bool(re.search(r'SRC-\d{6}', t)))
