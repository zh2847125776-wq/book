# -*- coding: utf-8 -*-
"""全量排批：把剩余所有原始资料一次性排进批次清单，交给 Arena批量循环.py 顺序跑完。

用法: python 阶段C_排批_全量.py [--size 20] [--dry]

池子分两阶段（顺序执行，便于分批验收）：
  阶段1 精简稿：与批001–023 同一口径（每课一份，完整稿作阅读对象）。
  阶段2 增强稿：主题汇编的 (增强版) 文档，去重后每份一份，证据限制标「仅增强稿可见」。

只创建清单与更新台账状态，不触发任何抽取；已进过批次的来源一律跳过。
"""
import argparse
import collections
import csv
import os
import pathlib
import re
import sys

OUT = pathlib.Path(r'C:\Users\赵豪\dsh\交易知识体系汇编')
IDX = OUT / '01_资料与索引'
SHARD = OUT / '工作分片'
PICKABLE = ('已配对完整稿', '仅精简稿可核', '待处理')
DONE_ST = {'已抽取', '工具脚本·无可用内容', '无可用交易内容', '无交易内容'}


def load(name):
    return list(csv.DictReader((IDX / name).open(encoding='utf-8'), delimiter='\t'))


def save(name, rows, cols):
    p = IDX / name
    with open(p, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter='\t', lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, '') for c in cols})


def kind_of(path):
    n = path
    if '读书' in n or '作手回忆录' in n or '股票大作手' in n:
        return '读书'
    if '期货' in n:
        return '期货'
    if '日评' in n or '解盘' in n or '股票' in n:
        return '日评'
    if '妖股' in n:
        return '妖股'
    if '专题' in n or '中级' in n or '交易思变' in n or '缺口技术' in n:
        return '专题'
    return '其他'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--size', type=int, default=20)
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()

    src = load('来源清单.tsv')
    go = load('来源去向.tsv')
    goby = {r['source_id']: r for r in go}
    rel = load('来源关系.tsv')
    only_note = {r['source_id'] for r in go if r['处理状态'] == '仅精简稿可核'}

    batched = set()
    for b in sorted(SHARD.glob('批*_清单.tsv')):
        for x in csv.DictReader(open(b, encoding='utf-8'), delimiter='\t'):
            batched.add(x['source_id'])
    nums = [int(m.group(1)) for m in (re.match(r'批(\d+)_清单', x.name) for x in SHARD.glob('批*_清单.tsv')) if m]
    nxt = (max(nums) + 1) if nums else 1

    # 阶段1：精简稿（含仅精简稿可核）
    stage1 = [r for r in src
              if r['版本标识'] == '精简稿'
              and goby.get(r['source_id'], {}).get('处理状态') in PICKABLE
              and goby.get(r['source_id'], {}).get('处理状态') not in DONE_ST
              and r['source_id'] not in batched]

    # 阶段2：增强稿，按文件名去重（同一文件在多个目录各有一份），优先取「学习笔记\」那份
    byname = collections.defaultdict(list)
    for r in src:
        if r['版本标识'] != '增强稿' or r['source_id'] in batched:
            continue
        if goby.get(r['source_id'], {}).get('处理状态') in DONE_ST:
            continue
        byname[os.path.basename(r['相对路径'].replace('/', '\\'))].append(r)
    trim_names = {os.path.basename(r['相对路径'].replace('/', '\\'))
                  for r in src if r['版本标识'] == '精简稿'}
    stage2 = []
    for name, rs in sorted(byname.items()):
        if name in trim_names:       # 与精简稿同名，已有同内容来源，不重复抽
            continue
        prim = [r for r in rs if r['相对路径'].startswith('学习笔记\\')]
        stage2.append(prim[0] if prim else rs[0])

    print('阶段1 精简稿待排: %d' % len(stage1))
    print('阶段2 增强稿待排: %d（去重后；原始条目 %d）' % (len(stage2), len(src) - len(stage1) - len(batched)))

    plan = []
    for tag, pool, limit in (('精简稿', stage1, ''), ('增强稿', stage2, '仅增强稿可见')):
        buckets = collections.defaultdict(list)
        for r in pool:
            buckets[kind_of(r['相对路径'])].append(r)
        order = ['专题', '其他', '日评', '期货', '读书', '妖股']
        picked = []
        i = 0
        while any(buckets[k] for k in order):
            k = order[i % len(order)]
            if buckets[k]:
                picked.append(buckets[k].pop(0))
            i += 1
        plan.append((tag, picked, limit))

    made, total_units = [], 0
    for tag, picked, limit in plan:
        for j in range(0, len(picked), a.size):
            chunk = picked[j:j + a.size]
            total_units += len(chunk)
            made.append((tag, limit, chunk))
    print('将新建批次 %d 个（批%03d 起），覆盖来源 %d 份' % (len(made), nxt, total_units))
    if a.dry:
        return

    for k, (tag, limit, chunk) in enumerate(made):
        n = nxt + k
        rows = []
        for r in chunk:
            n_lesson = re.search(r'第\s*(\d+)\s*课', r['相对路径'])
            full = ''
            if tag == '增强稿':
                full = r['相对路径']          # 增强稿自身就是阅读对象
            elif r['source_id'] not in only_note:
                for x in rel:
                    if x['source_id'] == r['source_id'] and x['关系'] == '精简稿—完整稿' and x['对象source_id']:
                        t = next((s for s in src if s['source_id'] == x['对象source_id']), None)
                        if t:
                            full = t['相对路径']
                            break
            rows.append({
                'source_id': r['source_id'],
                '课号': n_lesson.group(1) if n_lesson else '',
                '课型': kind_of(r['相对路径']),
                '主题': r['主题'],
                '精简稿(导航用)': r['相对路径'],
                '完整稿(阅读对象)': full,
                '证据限制': limit or ('仅精简稿可核' if r['source_id'] in only_note else ''),
            })
        cols = ['source_id', '课号', '课型', '主题', '精简稿(导航用)', '完整稿(阅读对象)', '证据限制']
        save(SHARD / ('批%03d_清单.tsv' % n), rows, cols)
        for r in rows:
            g = goby.get(r['source_id'])
            if g:
                g['处理状态'] = '已排批'
                g['备注'] = (g['备注'] + '；' if g['备注'] else '') + '批%03d' % n

    save('来源去向.tsv', go, list(go[0].keys()))
    print('已写入 批%03d–批%03d，共 %d 个批次' % (nxt, nxt + len(made) - 1, len(made)))
    print('台账已把这 %d 份标记为「已排批」' % total_units)


if __name__ == '__main__':
    main()
