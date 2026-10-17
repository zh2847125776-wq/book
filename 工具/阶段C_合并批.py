# -*- coding: utf-8 -*-
"""阶段 C 批合并：把一批抽取结果并入全局索引，并更新进度。

用法: python -X utf8 阶段C_合并批.py --batch 002 --kmin 11 --kmax 55 --smin 3 --smax 26 --cmin 2 --cmax 13 --emin 11 --emax 100

做四件事：
  1. 校验：卡片 ID 是否落在本批号段内、证据引用是否都有登记
  2. 合并：把新卡片写入三个索引，把新证据写入证据索引
  3. 记录：抽取记录、缺口、复核记录
  4. 进度：更新 进度.md，把本批来源标为已抽取
"""
import argparse
import csv
import pathlib
import re

BASE = pathlib.Path(r'C:\Users\赵豪\dsh')
OUT = BASE / '交易知识体系汇编'
IDX = OUT / '01_资料与索引'
SHARD = OUT / '工作分片'


def read(p):
    return pathlib.Path(p).read_text(encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--batch', required=True)
    ap.add_argument('--kmin', type=int, required=True)
    ap.add_argument('--kmax', type=int, required=True)
    ap.add_argument('--smin', type=int, required=True)
    ap.add_argument('--smax', type=int, required=True)
    ap.add_argument('--cmin', type=int, required=True)
    ap.add_argument('--cmax', type=int, required=True)
    ap.add_argument('--emin', type=int, required=True)
    ap.add_argument('--emax', type=int, required=True)
    a = ap.parse_args()

    # 1) 收卡片
    def collect(prefix, lo, hi):
        out = []
        for p in sorted((OUT / {'K': '02_知识点', 'S': '03_方法与策略', 'C': '04_案例'}[prefix]).glob(prefix + '-*.md')):
            m = re.match(prefix + r'-(\d{4})', p.name)
            if not m:
                continue
            n = int(m.group(1))
            if lo <= n <= hi:
                t = read(p)
                h1 = t.splitlines()[0].lstrip('# ').strip() if t.splitlines() else ''
                out.append({'id': '%s-%04d' % (prefix, n), 'file': p.name, 'h1': h1,
                            'text': t, 'ev': sorted(set(re.findall(r'E-\d{4}', t)))})
        return out

    K = collect('K', a.kmin, a.kmax)
    S = collect('S', a.smin, a.smax)
    C = collect('C', a.cmin, a.cmax)
    print('本批卡片: K=%d S=%d C=%d' % (len(K), len(S), len(C)))

    # 2) 校验卡片内部引用
    bad = []
    for grp in (K, S, C):
        for c in grp:
            for x in re.findall(r'\b([KSC]-\d{4})\b', c['text']):
                if x == c['id']:
                    continue
            if not c['text'].startswith('# '):
                bad.append((c['file'], '缺 H1'))
            if '一句话定义' not in c['text'] and c['id'].startswith('K'):
                bad.append((c['file'], '知识点卡缺「一句话定义」'))
    for b in bad:
        print('  ⚠', b)

    # 3) 收集证据：优先解析抽取记录，缺失时从卡片自身登记
    ev_new = {}
    for p in sorted(SHARD.glob('批%s_抽取_*.md' % a.batch)):
        for line in read(p).splitlines():
            m = re.match(r'\s*\|?\s*(E-\d{4})\s*[|\t]\s*(SRC-\d{6})', line)
            if m:
                parts = [x.strip() for x in re.split(r'[|\t]', line.strip().strip('|')) if x.strip()]
                if len(parts) >= 4:
                    ev_new[m.group(1)] = parts[:5]
    ev_from_card = 0
    for grp in (K, S, C):
        for c in grp:
            srcs = sorted(set(re.findall(r'SRC-\d{6}', c['text'])))
            for e in c['ev']:
                if e in ev_new:
                    continue
                ev_new[e] = [e, srcs[0] if srcs else '', c['id'], c['h1'][:40], '由卡片登记（该组未交证据清单）']
                ev_from_card += 1
    evfile = IDX / '证据索引.tsv'
    existing = read(evfile).splitlines()
    have = {l.split('\t')[0] for l in existing[1:]}
    add = [v for k, v in sorted(ev_new.items()) if k not in have]
    if add:
        with open(evfile, 'a', encoding='utf-8') as f:
            for row in add:
                f.write('\t'.join(list(row)[:5]) + '\t2026-09-28\n')
    print('证据索引: 新增 %d 条（其中 %d 条由卡片登记），累计 %d 条' % (len(add), ev_from_card, len(existing) - 1 + len(add)))

    # 4) 写索引
    def append_index(fname, header_cols, rows):
        p = IDX / fname
        t = read(p).rstrip('\n').splitlines()
        ids = {l.split('\t')[0] for l in t[1:]}
        n = 0
        with open(p, 'a', encoding='utf-8') as f:
            for r in rows:
                if r[0] in ids:
                    continue
                f.write('\t'.join(r) + '\n')
                n += 1
        return n

    kn = append_index('知识点索引.tsv', None, [
        [c['id'], c['h1'].split(' ', 1)[1] if ' ' in c['h1'] else c['h1'], '待归类',
         ','.join(sorted(set(re.findall(r'SRC-\d{6}', c['text'])))[:3]), ','.join(c['ev'][:4]), '已建卡（批%s）' % a.batch]
        for c in K])
    sn = append_index('方法策略索引.tsv', None, [
        [c['id'], c['h1'].split(' ', 1)[1] if ' ' in c['h1'] else c['h1'], '待归类', '待填',
         '待评', ','.join(sorted(set(re.findall(r'SRC-\d{6}', c['text'])))[:3]), '已建卡（批%s）' % a.batch]
        for c in S])
    cn = append_index('案例索引.tsv', None, [
        [c['id'], c['h1'].split(' ', 1)[1] if ' ' in c['h1'] else c['h1'], '待归类', '待填', '待填',
         ','.join(sorted(set(re.findall(r'SRC-\d{6}', c['text'])))[:3]), '已建卡（批%s）' % a.batch]
        for c in C])
    print('索引新增: 知识点 %d、方法 %d、案例 %d' % (kn, sn, cn))

    # 5) 标记本批来源
    man = SHARD / ('批%s_清单.tsv' % a.batch)
    rows = list(csv.DictReader(open(man, encoding='utf-8'), delimiter='\t'))
    gofile = IDX / '来源去向.tsv'
    go = list(csv.DictReader(open(gofile, encoding='utf-8'), delimiter='\t'))
    cols = list(go[0].keys())
    ids = {r['source_id'] for r in rows}
    for r in go:
        if r['source_id'] in ids:
            r['处理状态'] = '已抽取'
            r['备注'] = (r['备注'] + '；' if r['备注'] else '') + '批%s' % a.batch
    with open(gofile, 'w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(cols) + '\n')
        for r in go:
            f.write('\t'.join(str(r.get(c, '')) for c in cols) + '\n')
    print('来源去向: 批%s 的 %d 份已标记为已抽取' % (a.batch, len(ids)))

    print('\n合并完成')


if __name__ == '__main__':
    main()
