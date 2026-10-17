# -*- coding: utf-8 -*-
"""追回被旧正则丢弃的卡片（不改证据索引、不改台账）。

背景：2026-10-01 批022 第1164/1165课那组，模型漏写 markdown 井号，
旧入库正则只认 `# K-xxxx`，结果 20 条证据入索引、卡片全丢。
本脚本用修好的 parse_cards 重新解析已存档的 Arena 产出，只补写卡片。
"""
import importlib.util
import pathlib
import re
import sys

OUT = pathlib.Path(r'C:\Users\赵豪\dsh\交易知识体系汇编')
spec = importlib.util.spec_from_file_location('ing', str(OUT / '工具/Arena入库.py'))
ing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ing)

reply = pathlib.Path(sys.argv[1])
allowed = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else None   # 例如 K-0718..K-0725
raw = reply.read_text(encoding='utf-8')
cards = ing.parse_cards(raw)
print('解析卡片 %d 张' % len(cards))

n_new = n_sup = n_skip = 0
for cid, (name, body) in sorted(cards.items()):
    if cid.startswith('补充'):
        target = cid.replace('补充', '').strip()
        f = []
        for d in ('02_知识点', '03_方法与策略', '04_案例'):
            f += list((OUT / d).glob('%s_*.md' % target))
        if not f:
            print('  补充目标不存在，跳过 %s' % cid)
            n_skip += 1
            continue
        t = f[0].read_text(encoding='utf-8')
        if name[:16] in t:
            n_skip += 1
            continue
        f[0].write_text(t.rstrip() + '\n\n---\n\n## 补充：' + name + '\n' + body.rstrip() + '\n', encoding='utf-8')
        print('  追补 %s → %s' % (cid, f[0].name))
        n_sup += 1
        continue
    if allowed and cid not in allowed:
        print('  不在本组号段，跳过 %s' % cid)
        n_skip += 1
        continue
    d = {'K': '02_知识点', 'S': '03_方法与策略', 'C': '04_案例'}[cid[0]]
    safe = re.sub(r'[\\/:*?"<>|]', '', name)[:40]
    p = OUT / d / ('%s_%s.md' % (cid, safe))
    if p.exists():
        print('  已存在，跳过 %s' % cid)
        n_skip += 1
        continue
    p.write_text('# %s %s\n%s\n' % (cid, name, body.rstrip()), encoding='utf-8')
    print('  追建 %s %s' % (cid, name[:40]))
    n_new += 1

print('追建新卡 %d ｜ 追补补充 %d ｜ 跳过 %d' % (n_new, n_sup, n_skip))
