# -*- coding: utf-8 -*-
"""批 003 合并：从 A/B 记录解析证据清单 → 给卡片补来源行 → C 组按内容匹配绑源 → 并入索引。"""
import csv
import pathlib
import re
import collections

BASE = pathlib.Path(r'C:\Users\赵豪\dsh')
OUT = BASE / '交易知识体系汇编'
IDX = OUT / '01_资料与索引'
SHARD = OUT / '工作分片'

# ── 1) 解析 A 组（markdown 表格）与 B 组（制表符代码块）证据清单 ──
ev = {}   # E-id -> dict(source, pos, quote, use)
for f, mode in (('批003_抽取_A组.md', 'md'), ('批003_抽取_B组.md', 'tsv')):
    for line in (SHARD / f).read_text(encoding='utf-8').splitlines():
        s = line.strip()
        if mode == 'md':
            if not s.startswith('|'):
                continue
            cells = [c.strip() for c in s.strip('|').split('|')]
            if len(cells) < 5 or not re.fullmatch(r'E-\d{4}', cells[0]):
                continue
            ev[cells[0]] = {'source': cells[1], 'pos': cells[2], 'quote': cells[3][:120], 'use': cells[4]}
        else:
            if '\t' not in s or not re.match(r'^E-\d{4}\t', s):
                continue
            cells = [c.strip() for c in s.split('\t')]
            if len(cells) < 5:
                continue
            ev[cells[0]] = {'source': cells[1], 'pos': cells[2], 'quote': cells[3][:120], 'use': cells[4]}
print('解析出证据: A/B 共 %d 条（E-%s ~ E-%s）' % (
    len(ev), min(ev).split('-')[1] if ev else '?', max(ev).split('-')[1] if ev else '?'))

# ── 2) C 组候选来源（按内容匹配绑定）──
C_CANDS = {
    'SRC-003576': ('第06课 0115午间直播：风险提示与调整期纪律', None),
    'SRC-004200': ('第155课 读书：股票作手回忆录', None),
    'SRC-003966': ('第1349课 本周主要期货品种跟踪', None),
    'SRC-003577': ('第07课 0129早盘：破位后的反弹与减仓纪律', None),
    'SRC-004212': ('第156课 读书：股票作手回忆录', None),
    'SRC-003968': ('第1350课 主要期货品种价格跟踪', None),
}
man = {r['source_id']: r for r in csv.DictReader(open(SHARD / '批003_清单.tsv', encoding='utf-8'), delimiter='\t')}
for sid in list(C_CANDS):
    r = man.get(sid)
    p = BASE / r['完整稿(阅读对象)'] if r and r['完整稿(阅读对象)'] else None
    C_CANDS[sid] = (C_CANDS[sid][0], p.read_text(encoding='utf-8') if p and p.exists() else '')

C_CARDS = re.compile(r'^(K-00(7[5-9]|8[0-8])|S-00(2[7-9]|3[0-5])|C-00(2[0-4]))')
c_bind = {}
for d in ('02_知识点', '03_方法与策略', '04_案例'):
    for p in sorted((OUT / d).glob('*.md')):
        if not C_CARDS.match(p.stem):
            continue
        t = p.read_text(encoding='utf-8')
        # 取卡片里的中文专名/短语做指纹（>=5 字的连续中文）
        cands = [x for x in re.findall(r'[\u4e00-\u9fff]{5,}', t) if not x.startswith('一句话定义')]
        best, score = None, 0
        for sid, (label, src) in C_CANDS.items():
            if not src:
                continue
            hits = sum(1 for c in set(cands[:60]) if c in src)
            if hits > score:
                best, score = (sid, label), hits
        c_bind[p.stem] = (best, score)
print('\nC 组卡片内容匹配结果:')
for k, v in sorted(c_bind.items()):
    print('  %-46s %s  命中%d' % (k[:46], v[0][1] if v[0] else '未命中', v[1]))

# ── 3) 给卡片补/修来源行 ──
added = 0
for d in ('02_知识点', '03_方法与策略', '04_案例'):
    for p in sorted((OUT / d).glob('*.md')):
        m = re.match(r'([KSC])-(\d{4})', p.stem)
        if not m:
            continue
        t = p.read_text(encoding='utf-8')
        eids = sorted(set(re.findall(r'E-\d{4}', t)))
        if re.search(r'^> 来源：SRC-', t, re.M):
            continue
        srcs, note = [], ''
        for e in eids:
            if e in ev:
                for s in re.findall(r'SRC-\d{6}', ev[e]['source']):
                    if s not in srcs:
                        srcs.append(s)
        if not srcs and c_bind.get(p.stem, (None, 0))[0]:
            srcs = [c_bind[p.stem][0][0]]
            note = '（来源由卡片内容匹配 %s 认定，命中%d 处特征短语）' % (c_bind[p.stem][0][1], c_bind[p.stem][1])
        if not srcs:
            continue
        label = '、'.join('%s（%s）' % (s, man[s]['主题'][:24] if s in man else '') for s in srcs[:3])
        lin = '> 来源：%s · 证据 %s%s\n' % (label, '、'.join(eids) if eids else '—', note)
        lines = t.splitlines(True)
        idx = 1 if lines and lines[0].startswith('# ') else 0
        lines.insert(idx, lin + ('\n' if idx + 1 < len(lines) and lines[idx + 1].strip() else ''))
        p.write_text(''.join(lines), encoding='utf-8')
        added += 1
print('\n补充来源行的卡片: %d 张' % added)

# ── 4) 证据并入索引 ──
evfile = IDX / '证据索引.tsv'
existing = evfile.read_text(encoding='utf-8').splitlines()
have = {l.split('\t')[0] for l in existing[1:]}
new = 0
with open(evfile, 'a', encoding='utf-8') as f:
    for eid in sorted(ev):
        if eid in have:
            continue
        d = ev[eid]
        row = [eid, '、'.join(re.findall(r'SRC-\d{6}', d['source'])[:2]), d['pos'], d['quote'].replace('\t', ' '), d['use'][:80], '2026-09-28']
        f.write('\t'.join(row) + '\n')
        new += 1
    for stem, (b, sc) in sorted(c_bind.items()):
        if not b:
            continue
        t = (OUT / ('02_知识点' if stem.startswith('K') else '03_方法与策略' if stem.startswith('S') else '04_案例') / (stem + '.md')).read_text(encoding='utf-8')
        for eid in sorted(set(re.findall(r'E-\d{4}', t))):
            if eid in have or eid in ev:
                continue
            f.write('\t'.join([eid, b[0], stem, '（C组未交证据清单，来源由卡片内容匹配认定，命中%d 处）' % sc, stem, '2026-09-28']) + '\n')
            new += 1
print('证据索引新增 %d 条，累计 %d 条' % (new, len(existing) - 1 + new))
