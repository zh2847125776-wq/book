# -*- coding: utf-8 -*-
"""撞号重映射入库：某组回复里的卡号已被别的组占用时，改写到当前空闲号段。

背景：2026-10-01 批022，组1 因解析缺陷没写出卡，驱动接着给组2 分了同一号段；
组1 的卡事后追回，组2 再写就会撞号被跳过（数据丢失）。本脚本把撞号的卡
顺延到该字母的当前最大号之后，并同步改写正文里对同组卡号的引用。

用法:
  python 阶段C_重映射入库.py <回复文件> <来源ID逗号分隔>
"""
import importlib.util
import pathlib
import re
import sys

OUT = pathlib.Path(r'C:\Users\赵豪\dsh\交易知识体系汇编')
DIRS = {'K': '02_知识点', 'S': '03_方法与策略', 'C': '04_案例'}
spec = importlib.util.spec_from_file_location('ing', str(OUT / '工具/Arena入库.py'))
ing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ing)


def maxnum(letter):
    nums = [int(p.stem.split('_')[0].split('-')[1]) for p in (OUT / DIRS[letter]).glob('%s-*.md' % letter)]
    return max(nums or [0])


def find(cid):
    for d in DIRS.values():
        f = list((OUT / d).glob('%s_*.md' % cid))
        if f:
            return f[0]
    return None


def main():
    raw = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')
    srcs = sys.argv[2].split(',') if len(sys.argv) > 2 else []
    cards = ing.parse_cards(raw)
    print('解析卡片 %d 张' % len(cards))

    # 第一遍：定出撞号映射
    mapping, nxt = {}, {k: maxnum(k) for k in DIRS}
    for cid in sorted(cards):
        if cid.startswith('补充'):
            continue
        if find(cid) is None:
            continue                      # 号段空闲，照原号写
        nxt[cid[0]] += 1
        mapping[cid] = '%s-%04d' % (cid[0], nxt[cid[0]])
    if mapping:
        print('撞号顺延:', ', '.join('%s→%s' % kv for kv in sorted(mapping.items())))
    else:
        print('无撞号')

    def remap(text):
        out = text
        for old, new in mapping.items():
            out = re.sub(r'(?<![0-9A-Za-z-])%s(?![0-9])' % re.escape(old), new, out)
        return out

    n_new = n_sup = n_skip = 0
    for cid, (name, body) in sorted(cards.items()):
        newid = mapping.get(cid, cid)
        name = remap(name)
        body = remap(body)
        if cid.startswith('补充'):
            target = remap(cid.replace('补充', '').strip())
            f = find(target)
            if not f:
                print('  补充目标不存在，跳过 %s' % cid)
                n_skip += 1
                continue
            t = f.read_text(encoding='utf-8')
            if name[:16] in t:
                n_skip += 1
                continue
            f.write_text(t.rstrip() + '\n\n---\n\n## 补充：' + name + '\n' + body.rstrip() + '\n', encoding='utf-8')
            print('  追补 %s → %s' % (cid, f.name[:60]))
            n_sup += 1
            continue
        p = OUT / DIRS[newid[0]] / ('%s_%s.md' % (newid, re.sub(r'[\\/:*?"<>|]', '', name)[:40]))
        if p.exists():
            print('  已存在，跳过 %s' % newid)
            n_skip += 1
            continue
        p.write_text('# %s %s\n%s\n' % (newid, name, body.rstrip()), encoding='utf-8')
        print('  写卡 %s%s' % (newid, ('（原 %s）' % cid) if newid != cid else ''))
        n_new += 1

    # 台账：把本组来源标成已抽取
    if srcs:
        p = OUT / '01_资料与索引/来源去向.tsv'
        lines = p.read_text(encoding='utf-8').splitlines()
        head = lines[0].split('\t')
        si, sti = head.index('source_id'), head.index('处理状态')
        for i, l in enumerate(lines[1:], 1):
            c = l.split('\t')
            if len(c) > sti and c[si] in srcs and c[sti] != '已抽取':
                c[sti] = '已抽取'
                lines[i] = '\t'.join(c)
        p.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('写卡 %d ｜ 追补 %d ｜ 跳过 %d' % (n_new, n_sup, n_skip))


if __name__ == '__main__':
    main()
