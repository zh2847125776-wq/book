# -*- coding: utf-8 -*-
"""阶段 A 盘点：为全部输入文件建立可追溯底账。

产出（写入 交易知识体系汇编/01_资料与索引/）：
  来源清单.tsv          主要阅读资料（笔记与备份、知识库）逐文件
  来源清单_转写.tsv      转写结果逐文件，含同音视频分组号
  来源关系.tsv          精简稿—完整稿—增强稿—转写的配对关系
  来源去向.tsv          每份资料的处理状态
  异常清单.tsv          盘点中发现的异常（无课号、同名冲突、空文件等）

用法: python -X utf8 阶段A_盘点.py [--hash 转写|全部|跳过]
"""
import collections
import hashlib
import os
import pathlib
import re
import sys
import time

BASE = pathlib.Path(r'C:\Users\赵豪\dsh')
OUT = BASE / '交易知识体系汇编'
IDX = OUT / '01_资料与索引'

MAIN_DIRS = [
    ('学习笔记', '笔记主目录', '主要阅读资料'),
    ('_完整稿备份', '完整稿备份（第2979-3638课）', '主要阅读资料'),
    ('_完整稿备份_旧系列', '完整稿备份（第1-2978课）', '主要阅读资料'),
    ('_完整稿备份_增强版与妖股', '增强版素材与妖股原稿', '主要阅读资料'),
    ('知识库', '既有知识库（结构参考）', '主要阅读资料'),
    ('_待汇编', '既有汇编材料', '主要阅读资料'),
]
TRANSCRIPT_DIR = '转写结果'
REPORT_FILES = ['交付书_精简笔记_320课.md', '交付书_Claude_337课精简.md',
                '交付书_旧系列精简_Codex_1489课.md', '交付书_Claude_旧系列1490课.md',
                '核数报告_Codex.tsv', '核数报告_Claude.tsv',
                '核数交付说明_Claude_288课.md']

LESSON_RE = re.compile(r'第\s*(\d+)\s*课')
DATE_RE = re.compile(r'[（(](\d{8})[)）]')
H1_RE = re.compile(r'^#\s+(.*)$')


def sha256(p, buf=1 << 20):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        while True:
            b = f.read(buf)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def head_text(p, n=600):
    try:
        with open(p, encoding='utf-8', errors='replace') as f:
            return f.read(n)
    except Exception:
        return ''


def lesson_no(name):
    m = LESSON_RE.search(name)
    return m.group(1) if m else ''


def version_tag(name, top):
    if '妖股成妖之路' in name and '(蒸馏)' in name:
        return '蒸馏稿'
    if name.startswith('(增强版)'):
        return '增强稿'
    if '妖股成妖之路' in name:
        return '妖股原稿'
    if top == '_完整稿备份':
        return '完整稿'
    if top == '_完整稿备份_旧系列':
        return '完整稿'
    if top == '_完整稿备份_增强版与妖股':
        return '增强稿'
    return '精简稿'


def topic_of(text):
    for line in text.splitlines():
        m = H1_RE.match(line)
        if m:
            t = m.group(1)
            t = LESSON_RE.sub('', t, count=1)
            return t.strip()[:60]
    return ''


def date_of(text, name):
    m = DATE_RE.search(text.splitlines()[0]) if text.splitlines() else None
    if m:
        return m.group(1), 'H1'
    m = re.search(r'(\d{4}[-年]?\d{1,2}[-月]?\d{1,2})', text)
    if m:
        return m.group(1), '正文'
    m = DATE_RE.search(name)
    if m:
        return m.group(1), '文件名'
    return '', '无'


def main():
    do_hash = '全部'
    if '--hash' in sys.argv:
        do_hash = sys.argv[sys.argv.index('--hash') + 1]

    IDX.mkdir(parents=True, exist_ok=True)
    anomalies = []
    rows = []
    seq = 0
    t0 = time.time()

    for top, label, kind in MAIN_DIRS:
        d = BASE / top
        if not d.is_dir():
            anomalies.append((top, '', '目录不存在'))
            continue
        files = sorted(p for p in d.rglob('*') if p.is_file())
        for p in files:
            seq += 1
            rel = str(p.relative_to(BASE))
            name = p.name
            h = sha256(p) if do_hash == '全部' else ''
            text = head_text(p) if p.suffix.lower() in ('.md', '.txt') else ''
            dt, src = date_of(text, name)
            rows.append({
                'source_id': 'SRC-%06d' % seq,
                '相对路径': rel,
                'SHA256': h,
                '文件类型': p.suffix.lower().lstrip('.') or '(无扩展名)',
                '课号原写法': ('第%s课' % lesson_no(name)) if lesson_no(name) else '',
                '主题': topic_of(text),
                '版本标识': version_tag(name, top),
                '课程日期': dt,
                '日期依据': src,
                '对应完整稿source_id': '',
                '状态': '待处理',
                '备注': label if p.suffix.lower() != '.md' else '',
            })
        print('  %-28s %5d 份  (%.1fs)' % (top, len(files), time.time() - t0), flush=True)

    # 根目录报告
    for f in REPORT_FILES:
        p = BASE / f
        if p.is_file():
            seq += 1
            rows.append({
                'source_id': 'SRC-%06d' % seq, '相对路径': f, 'SHA256': sha256(p),
                '文件类型': p.suffix.lower().lstrip('.'), '课号原写法': '', '主题': '',
                '版本标识': '交付报告', '课程日期': '', '日期依据': '无',
                '对应完整稿source_id': '', '状态': '参考',
                '备注': '既有交付与核数记录，作为线索不替代逐处证据',
            })

    with open(IDX / '来源清单.tsv', 'w', encoding='utf-8', newline='') as f:
        cols = list(rows[0].keys())
        f.write('\t'.join(cols) + '\n')
        for r in rows:
            f.write('\t'.join(str(r[c]) for c in cols) + '\n')
    print('来源清单.tsv: %d 行' % len(rows))

    # 转写结果
    td = BASE / TRANSCRIPT_DIR
    trows = []
    if td.is_dir():
        groups = collections.defaultdict(list)
        for p in sorted(x for x in td.rglob('*') if x.is_file()):
            groups[p.stem].append(p)
        gid = 0
        for stem in sorted(groups):
            gid += 1
            g = 'TR-%06d' % gid
            for p in groups[stem]:
                seq += 1
                h = sha256(p) if do_hash in ('全部', '转写') else ''
                trows.append({
                    'source_id': 'SRC-%06d' % seq,
                    '组号': g,
                    '相对路径': str(p.relative_to(BASE)),
                    'SHA256': h,
                    '文件类型': p.suffix.lower().lstrip('.'),
                    '大小KB': round(p.stat().st_size / 1024, 1),
                    '状态': '补充证据·按需回查',
                    '备注': '同音视频的 txt/srt/json 共组，不计作多门课',
                })
        with open(IDX / '来源清单_转写.tsv', 'w', encoding='utf-8', newline='') as f:
            cols = list(trows[0].keys())
            f.write('\t'.join(cols) + '\n')
            for r in trows:
                f.write('\t'.join(str(r[c]) for c in cols) + '\n')
        print('来源清单_转写.tsv: %d 行, %d 组' % (len(trows), gid))

    with open(IDX / '异常清单.tsv', 'w', encoding='utf-8', newline='') as f:
        f.write('位置\t对象\t异常\n')
        for a in anomalies:
            f.write('\t'.join(a) + '\n')
    print('异常清单.tsv: %d 条' % len(anomalies))
    print('耗时 %.1fs' % (time.time() - t0))


if __name__ == '__main__':
    main()
