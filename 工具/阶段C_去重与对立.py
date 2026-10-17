# -*- coding: utf-8 -*-
"""入库后的去重与对立筛查。只登记，不删除卡片、不改写规则。

用法:
  python -X utf8 工具/阶段C_去重与对立.py
  python -X utf8 工具/阶段C_去重与对立.py --since K-0780

结果追加到 07_审计与交付/去重与对立_待核.tsv。
"""
import pathlib
import re
import sys

OUT = pathlib.Path(r'C:\Users\赵豪\dsh\交易知识体系汇编')
REPORT = OUT / '07_审计与交付/去重与对立_待核.tsv'
TERMS = (
    '20线', '60线', '均线', '止损', '止盈', '仓位', '加仓', '减仓', '突破', '跌破',
    '背离', '缺口', '粘合', '回测', '做空', '做多', '过夜', '换月', 'MACD', 'RSI',
    '布林', '趋势线', '颈线', '支撑', '压力', '成交量', '杠杆', '盈亏比'
)
OPPOSITE = (
    ('做多', '做空'), ('加仓', '减仓'), ('持有', '离场'), ('上移', '下移'),
    ('有效', '无效'), ('确认', '否决'), ('允许', '禁止'), ('必须', '不能')
)


def cards(since):
    found = []
    for folder, letter in (('02_知识点', 'K'), ('03_方法与策略', 'S'), ('04_案例', 'C')):
        for path in (OUT / folder).glob('%s-*.md' % letter):
            number = int(path.stem.split('_')[0].split('-')[1])
            if number < since:
                continue
            text = path.read_text(encoding='utf-8')
            title = text.splitlines()[0].lstrip('# ').strip()
            found.append((path.stem.split('_')[0], title, text, path))
    return found


def existing(since):
    found = []
    for folder in ('02_知识点', '03_方法与策略', '04_案例'):
        for path in (OUT / folder).glob('*.md'):
            number = int(path.stem.split('_')[0].split('-')[1])
            if number >= since:
                continue
            text = path.read_text(encoding='utf-8')
            found.append((path.stem.split('_')[0], text.splitlines()[0].lstrip('# ').strip(), text))
    return found


def terms_of(text):
    return {term for term in TERMS if term in text}


def opposite_pairs(left, right):
    return [a + '/' + b for a, b in OPPOSITE if (a in left and b in right) or (b in left and a in right)]


def main():
    since = 0
    if '--since' in sys.argv:
        since = int(sys.argv[sys.argv.index('--since') + 1].split('-')[-1])
    new_cards = cards(since)
    old_cards = existing(since)
    rows = []
    for cid, title, text, _path in new_cards:
        mine = terms_of(title + '\n' + text[:1200])
        if len(mine) < 2:
            continue
        for oid, otitle, otext in old_cards:
            shared = mine & terms_of(otitle + '\n' + otext[:1200])
            opposed = opposite_pairs(text[:1600], otext[:1600])
            if len(shared) >= 4:
                rows.append((cid, oid, '疑似重复', '、'.join(sorted(shared)), title, otitle))
            elif len(shared) >= 2 and opposed:
                rows.append((cid, oid, '疑似对立', '、'.join(sorted(shared)) + '；对立词:' + '、'.join(opposed), title, otitle))
    header = '新卡\t对照卡\t类型\t依据\t新卡标题\t对照卡标题\t处理状态\n'
    if not REPORT.exists():
        REPORT.write_text(header, encoding='utf-8')
    current = REPORT.read_text(encoding='utf-8')
    add = [row for row in rows if row[0] + '\t' + row[1] + '\t' + row[2] not in current]
    with REPORT.open('a', encoding='utf-8') as handle:
        for row in add:
            handle.write('\t'.join(row + ('待核',)) + '\n')
    print('新卡 %d | 对照 %d | 候选 %d | 新登记 %d' % (len(new_cards), len(old_cards), len(rows), len(add)))
    print(REPORT)


if __name__ == '__main__':
    main()
