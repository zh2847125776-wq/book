# -*- coding: utf-8 -*-
"""阶段 C 批次驱动：从底账里取下一批未处理的资料，生成批次清单。

用法:
  python -X utf8 阶段C_取批.py --size 20                 # 取下一批
  python -X utf8 阶段C_取批.py --size 20 --theme 均线      # 按主题关键词取
  python -X utf8 阶段C_取批.py --status                  # 只看进度
  python -X utf8 阶段C_取批.py --done 001                # 标记某批完成

规则（按任务书阶段 C）：
  - 一批 20—50 份独立正文；精简稿只做导航，阅读对象是完整稿
  - 优先取"有对应完整稿"的精简稿；「仅精简稿可核」的单独成组，标注证据限制
  - 不按主题挑好写的：混合抽取（定义课 + 日评 + 读书 + 期货），只在 --theme 时收窄
  - 状态写入 来源去向.tsv，批次清单写入 工作分片/
"""
import argparse
import sys
import csv
import pathlib
import re
import collections

BASE = pathlib.Path(r'C:\Users\赵豪\dsh')
OUT = BASE / '交易知识体系汇编'
IDX = OUT / '01_资料与索引'
SHARD = OUT / '工作分片'
SHARD.mkdir(parents=True, exist_ok=True)


def load(name):
    with open(IDX / name, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def save(name, rows, cols):
    with open(IDX / name, 'w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(cols) + '\n')
        for r in rows:
            f.write('\t'.join(str(r.get(c, '')) for c in cols) + '\n')


def kind_of(rel):
    n = pathlib.Path(rel).name
    if '读书' in n:
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
    ap.add_argument('--theme', default='')
    ap.add_argument('--status', action='store_true')
    ap.add_argument('--done', default='')
    a = ap.parse_args()

    src = load('来源清单.tsv')
    go = load('来源去向.tsv')
    goby = {r['source_id']: r for r in go}
    rel = load('来源关系.tsv')
    rel_ok = {r['source_id'] for r in rel if r['关系'] == '精简稿—完整稿'}
    only_note = {r['source_id'] for r in go if r['处理状态'] == '仅精简稿可核'}

    if a.status:
        c = collections.Counter(r['处理状态'] for r in go)
        print('来源去向状态分布：')
        for k, v in c.most_common():
            print('  %-16s %d' % (k, v))
        batches = sorted(SHARD.glob('批*_清单.tsv'))
        print('\n已完成批次：%d' % len(batches))
        for b in batches[-5:]:
            print('  ', b.name, sum(1 for _ in open(b, encoding='utf-8')) - 1, '份')
        return

    if a.done:
        m = list(SHARD.glob('批%s_清单.tsv' % a.done))
        if not m:
            print('找不到批次', a.done)
            return
        rows = list(csv.DictReader(open(m[0], encoding='utf-8'), delimiter='\t'))
        for r in rows:
            g = goby.get(r['source_id'])
            if g:
                g['处理状态'] = '已抽取'
                g['备注'] = (g['备注'] + '；' if g['备注'] else '') + '批%s' % a.done
        save('来源去向.tsv', go, list(go[0].keys()))
        print('批次 %s 的 %d 份已标记为「已抽取」' % (a.done, len(rows)))
        return

    # 取批：优先有完整稿的精简稿，混合课型
    done = set()
    for b in SHARD.glob('批*_清单.tsv'):
        for x in csv.DictReader(open(b, encoding='utf-8'), delimiter='	'):
            done.add(x['source_id'])
    PICKABLE = ('已配对完整稿', '仅精简稿可核', '待处理')
    cand = [r for r in src if r['版本标识'] == '精简稿'
            and goby.get(r['source_id'], {}).get('处理状态') in PICKABLE
            and r['source_id'] not in done]
    if a.theme:
        cand = [r for r in cand if a.theme in r['相对路径'] or a.theme in r['主题']]
    # 混合：按课型轮流取，避免只挑好写的
    buckets = collections.defaultdict(list)
    for r in cand:
        buckets[kind_of(r['相对路径'])].append(r)
    order = ['专题', '其他', '日评', '期货', '读书', '妖股']
    picked = []
    i = 0
    while len(picked) < a.size and any(buckets[k] for k in order):
        k = order[i % len(order)]
        if buckets[k]:
            picked.append(buckets[k].pop(0))
        i += 1

    if not picked:
        print('没有可取的来源了：候选池已空（所有「精简稿」都已进过批次清单）。')
        sys.exit(0)

    nums = [int(m.group(1)) for m in (re.match(r'批(\d+)_清单', x.name) for x in SHARD.glob('批*_清单.tsv')) if m]
    n = (max(nums) + 1) if nums else 1
    tag = '%03d' % n
    cols = ['source_id', '课号', '课型', '主题', '精简稿(导航用)', '完整稿(阅读对象)', '证据限制']
    rows = []
    for r in picked:
        n_lesson = re.search(r'第\s*(\d+)\s*课', r['相对路径'])
        full = ''
        limit = ''
        if r['source_id'] in only_note:
            limit = '仅精简稿可核'
        else:
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
            '证据限制': limit,
        })
    save(SHARD / ('批%s_清单.tsv' % tag), rows, cols)

    for r in rows:
        g = goby.get(r['source_id'])
        if g:
            g['处理状态'] = '进行中'
    save('来源去向.tsv', go, list(go[0].keys()))

    print('批次 %s：%d 份' % (tag, len(rows)))
    print('课型分布:', dict(collections.Counter(r['课型'] for r in rows)))
    print('有完整稿:', sum(1 for r in rows if r['完整稿(阅读对象)']), ' 仅精简稿可核:', sum(1 for r in rows if r['证据限制']))
    print('清单: 工作分片/批%s_清单.tsv' % tag)


if __name__ == '__main__':
    main()
