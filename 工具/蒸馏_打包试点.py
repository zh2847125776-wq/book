# -*- coding: utf-8 -*-
"""打包 10 张高 freq S 卡 + 逐字证据，供人工在 Arena 跑阶段2 规则蒸馏试点。"""
import pathlib, re, csv, json

OUT = pathlib.Path(r'C:/Users/赵豪/dsh/交易知识体系汇编')
DEST = pathlib.Path(r'C:/Users/赵豪/Desktop/蒸馏试点_10卡_20261012')
DEST.mkdir(parents=True, exist_ok=True)

led = {r['source_id']: r for r in csv.DictReader(open(OUT/'01_资料与索引/来源去向.tsv', encoding='utf-8'), delimiter='\t')}
ev = {}
for r in csv.DictReader(open(OUT/'01_资料与索引/证据索引.tsv', encoding='utf-8'), delimiter='\t'):
    eid = (r.get('证据ID') or '').strip()
    if re.fullmatch(r'E-\d{4,5}', eid):
        ev[eid] = r

# 1) 选卡：freq（卡面引用的已抽取来源数）优先，证据条数次之
rows = []
for f in (OUT/'03_方法与策略').glob('*.md'):
    t = f.read_text(encoding='utf-8')
    m = re.search(r'^> 来源：(.+)', t, re.M)
    if not m:
        continue
    srcs = {s for s in re.findall(r'SRC-\d+', m.group(1)) if led.get(s, {}).get('处理状态') == '已抽取'}
    evs = sorted(set(re.findall(r'E-\d{4,5}', t)))
    rows.append({'f': f, 'text': t, 'freq': len(srcs), 'srcs': sorted(srcs), 'evs': evs})
rows.sort(key=lambda r: (-r['freq'], -len(r['evs']), r['f'].name))
picks = rows[:10]

# 2) 生成资料包
parts = ['# 阶段2 规则蒸馏 · 试点资料包（10 张 S 卡 + 逐字证据）', '',
         '说明：每张卡是一个交易方法的**已结构化摘要**；卡片下方是该卡引用的逐字证据（E-xxxx，原文摘录）。',
         '请**只依据**卡片与证据原文抽取可执行规则，不得用自身交易知识补全参数。', '']
manifest = []
for i, r in enumerate(picks, 1):
    cid = r['f'].stem.split('_')[0]
    parts.append('=' * 72)
    parts.append('## 资料 %d ｜ %s' % (i, r['f'].name))
    parts.append('（卡面引用来源数 freq=%d：%s）' % (r['freq'], '、'.join(r['srcs'])))
    parts.append('=' * 72)
    parts.append(r['text'].strip())
    parts.append('')
    parts.append('### 本卡引用的逐字证据')
    for eid in r['evs']:
        e = ev.get(eid)
        if not e:
            parts.append('- %s ｜（证据索引无此条）' % eid)
            continue
        q = (e.get('原文摘录') or '').replace('\n', ' ').replace('\t', ' ').strip()
        parts.append('- **%s** ｜ 位置：%s ｜ 摘录：%s' % (eid, (e.get('位置') or '')[:60], q[:220]))
    parts.append('')
    manifest.append({'no': i, 'card': cid, 'file': r['f'].name, 'freq': r['freq'],
                     'n_ev': len(r['evs']), 'srcs': r['srcs']})

(DEST/'01_资料包.md').write_text('\n'.join(parts), encoding='utf-8')
(DEST/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding='utf-8')

print('资料包字符数', len('\n'.join(parts)))
for m in manifest:
    print(m['no'], m['card'], 'freq=%d' % m['freq'], '证据%d条' % m['n_ev'], m['file'][:46])
