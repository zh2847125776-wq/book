# -*- coding: utf-8 -*-
"""阶段 A（续）：建立来源关系与处理去向。

产出：
  来源关系.tsv  精简稿—完整稿—增强稿—蒸馏稿—转写 的配对与版本关系
  来源去向.tsv  每份资料的处理状态
  重复来源组.tsv 内容相同的物理文件分组（备份与主目录的重复）
"""
import collections
import csv
import pathlib
import re

BASE = pathlib.Path(r'C:\Users\赵豪\dsh')
IDX = BASE / '交易知识体系汇编' / '01_资料与索引'
LESSON_RE = re.compile(r'第\s*(\d+)\s*课')


def load():
    with open(IDX / '来源清单.tsv', encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def lesson(rel):
    m = LESSON_RE.search(pathlib.Path(rel).name)
    return int(m.group(1)) if m else None


def main():
    rows = load()
    for r in rows:
        r['_lesson'] = lesson(r['相对路径'])

    jing = [r for r in rows if r['版本标识'] == '精简稿']
    quan = [r for r in rows if r['版本标识'] == '完整稿']
    zeng = [r for r in rows if r['版本标识'] == '增强稿']
    yao = [r for r in rows if r['版本标识'] == '蒸馏稿']

    # 完整稿按课号索引（同一课号可能有多份）
    qby = collections.defaultdict(list)
    for r in quan:
        if r['_lesson'] is not None:
            qby[r['_lesson']].append(r)

    # SHA256 重复分组
    byhash = collections.defaultdict(list)
    for r in rows:
        if r['SHA256']:
            byhash[r['SHA256']].append(r)
    dup_groups = {h: v for h, v in byhash.items() if len(v) > 1}

    rel_rows, go_rows = [], []
    paired = unpaired = 0
    for r in jing:
        n = r['_lesson']
        targets = qby.get(n, []) if n is not None else []
        if targets:
            paired += 1
            for t in targets:
                rel_rows.append((r['source_id'], t['source_id'], '精简稿—完整稿', '按课号配对',
                                 '' if len(targets) == 1 else '同课号完整稿 %d 份' % len(targets)))
            go = '已配对完整稿'
            note = ''
        else:
            unpaired += 1
            rel_rows.append((r['source_id'], '', '精简稿—无完整稿', '课号在原备份中不存在',
                             '仅精简稿可核'))
            go = '仅精简稿可核'
            note = '找不到对应完整稿，收录时须标注证据限制'

        dup = dup_groups.get(r['SHA256'])
        if dup:
            others = [x['source_id'] for x in dup if x['source_id'] != r['source_id']]
            rel_rows.append((r['source_id'], ','.join(others), '内容重复组', 'SHA256 相同',
                             '物理文件保留，不重复计入课程数'))
            note = (note + '；' if note else '') + ('与 %d 份文件内容相同' % len(others))
        go_rows.append((r['source_id'], r['相对路径'], r['版本标识'], go, note))

    for r in quan:
        n = r['_lesson']
        has_j = any(j['_lesson'] == n for j in jing) if n is not None else False
        rel_rows.append((r['source_id'], '', '完整稿—精简稿', '有对应精简稿' if has_j else '无对应精简稿',
                         ''))
        go_rows.append((r['source_id'], r['相对路径'], r['版本标识'],
                        '参考·核对底本' if has_j else '待核·无对应精简稿', ''))

    for r in zeng:
        rel_rows.append((r['source_id'], '', '增强稿—独立来源', '增强版与主题稿，独立登记', ''))
        go_rows.append((r['source_id'], r['相对路径'], r['版本标识'], '待处理·独立来源', ''))

    # 蒸馏稿 ↔ 妖股原稿章节
    def yao_no(rel):
        m = re.search(r'妖股成妖之路_(\d+)', pathlib.Path(rel).name)
        return int(m.group(1)) if m else None
    yao_ch = {}
    for r in zeng:
        k = yao_no(r['相对路径'])
        if k is not None:
            yao_ch.setdefault(k, r)
    for r in yao:
        k = yao_no(r['相对路径'])
        t = yao_ch.get(k)
        rel_rows.append((r['source_id'], t['source_id'] if t else '', '蒸馏稿—原稿章节',
                         '按编号配对' if t else '未找到同号原稿章节', ''))
        go_rows.append((r['source_id'], r['相对路径'], r['版本标识'],
                        '已配对原稿章节' if t else '待核·未配对', ''))

    for r in rows:
        if r['版本标识'] == '交付报告':
            go_rows.append((r['source_id'], r['相对路径'], r['版本标识'], '参考·已知问题线索',
                            '不能替代逐处证据'))

    with open(IDX / '来源关系.tsv', 'w', encoding='utf-8', newline='') as f:
        f.write('source_id\t对象source_id\t关系\t依据\t备注\n')
        for x in rel_rows:
            f.write('\t'.join(x) + '\n')

    with open(IDX / '来源去向.tsv', 'w', encoding='utf-8', newline='') as f:
        f.write('source_id\t相对路径\t版本标识\t处理状态\t备注\n')
        for x in go_rows:
            f.write('\t'.join(x) + '\n')

    with open(IDX / '重复来源组.tsv', 'w', encoding='utf-8', newline='') as f:
        f.write('SHA256\t份数\tsource_id列表\t说明\n')
        for h, v in sorted(dup_groups.items(), key=lambda kv: -len(kv[1])):
            f.write('%s\t%d\t%s\t内容相同，物理文件各自保留\n' %
                    (h, len(v), ','.join(x['source_id'] for x in v)))

    print('来源关系.tsv: %d 行' % len(rel_rows))
    print('来源去向.tsv: %d 行' % len(go_rows))
    print('重复来源组.tsv: %d 组' % len(dup_groups))
    print()
    print('精简稿 %d 份：有完整稿 %d，无完整稿（仅精简稿可核）%d' % (len(jing), paired, unpaired))
    print('完整稿 %d 份，增强稿 %d 份，蒸馏稿 %d 份' % (len(quan), len(zeng), len(yao)))
    print('内容重复的物理文件: %d 份' % sum(len(v) for v in dup_groups.values()))


if __name__ == '__main__':
    main()
