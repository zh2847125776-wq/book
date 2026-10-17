# -*- coding: utf-8 -*-
"""卡片充实度质检 —— 抓「guard 通过、内容却是空的」这一失败模式。

背景：2026-10-13 发现 Shard3（gd6/gpt-6.1-sol）47 组产出全部空心 ——
抽取规矩被当正文抄进卡片字段、关系段与案例段只剩占位符、每节挂同一组证据号。
而 `严格官方入库` 的 guard 只验正确性（证据数==验证通过数 / 新卡数==回复卡数 / 逐字回源），
**抓不到内容空心**，所以 47 组全是 guard: PASS。这个脚本补上那道闸门。

用法：
  python -X utf8 工具/质检_卡片充实度.py <回复文件或产出文件> [更多文件...]
  python -X utf8 工具/质检_卡片充实度.py --dir <目录>        # 质检目录下全部 .md

判级：
  ✗ 不通过 —— 抽取规矩被抄进正文 / 关系段是空占位 / 案例段无内容（实质空心）
  △ 告警   —— 来源头课号为空（外观）/ 同一组证据铺满多个节（疑似未逐节取证）
  ✓ 通过

退出码：0=无实质问题；1=有文件实质不通过；2=用法错误
"""
import pathlib
import re
import sys

# ---- 硬失败：不该出现在卡片正文里的东西 ----

# 1) 来源头模板破损（课号为空）—— 实测 47/47 命中
BROKEN_HEADER = [
    re.compile(r'（第\s*课'),          # 「（第课 」
    re.compile(r'（第%s课'),
    re.compile(r'第\s*课\s*[，,]?\s*课型'),
]

# 2) 抽取规矩被当正文抄进卡片（规矩是「约束写什么」，不是「拿来抄」）
RULE_ECHO = [
    ('仅记录≤300字完整原文字面', re.compile(r'仅记录\s*≤?\s*300\s*字完整原文字面')),
    ('不采信Vision推断',        re.compile(r'不采信\s*Vision\s*推断')),
    ('禁截断铁律',              re.compile(r'禁截断铁律')),
    ('不补造',                  re.compile(r'不补造')),
    ('不把超长语音行截断入证',  re.compile(r'超长语音行.{0,6}截断')),
    ('按无省略号不截断',        re.compile(r'无省略号不截断')),
]

# 3) 空关系段：整段只有「关联Sx与Cx；不跨源混用」这类占位
EMPTY_RELATION = re.compile(r'关联\s*S\d+\s*与\s*C\d+\s*[；;]\s*不跨源混用\s*。?\s*(?:\{E\d+\}|\[E-\d+\])*\s*$')

# 4) 空案例段：整段只有「见Sx与Cx」+ 泛泛一句
EMPTY_CASE = re.compile(r'^见\s*S\d+\s*与\s*C\d+\s*[；;]')

SECTION = re.compile(r'(?m)^##\s+(.+?)\s*$')


def sections(text):
    """切成 {节名: 正文} 的列表，保留出现顺序。"""
    out = []
    marks = list(SECTION.finditer(text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out.append((m.group(1), text[m.end():end]))
    return out


def e_ids(text):
    return set(re.findall(r'E-\d{4,5}', text))


def check_file(path):
    raw = path.read_text(encoding='utf-8', errors='replace')
    problems, warns = [], []

    # 来源头课号为空 = 外观缺陷（Claude 片 100% 命中但内容合格），只告警不判死
    for pat in BROKEN_HEADER:
        if pat.search(raw):
            warns.append('来源头课号为空（外观缺陷，不阻断）')
            break

    for name, pat in RULE_ECHO:
        if pat.search(raw):
            problems.append('抽取规矩被抄进正文：%s' % name)

    secs = sections(raw)
    if secs:
        rel = [(n, b) for n, b in secs if '关系' in n]
        for n, b in rel:
            body = re.sub(r'(\{E\d+\}|\[E-\d+\])', '', b).strip()
            if not body or EMPTY_RELATION.search(body) or ('不跨源混用' in body and len(body) < 60):
                problems.append('「%s」是空占位' % n)
        for n, b in [(n, b) for n, b in secs if '案例' in n or '证据' in n]:
            body = re.sub(r'(\{E\d+\}|\[E-\d+\])', '', b).strip()
            body = re.sub(r'^[-*\d.\s]+', '', body)
            if not body or EMPTY_CASE.search(body):
                problems.append('「%s」没有实际案例内容' % n)

    # 5) 证据引用单一（告警）：同一组证据号铺满 >=3 个节
    if secs:
        sets = [frozenset(e_ids(b)) for _, b in secs if e_ids(b)]
        if len(sets) >= 3:
            from collections import Counter
            c = Counter(sets)
            top, cnt = c.most_common(1)[0]
            if cnt >= 3 and len(sets) >= 3 and cnt / len(sets) >= 0.6:
                warns.append('同一组证据（%s）铺满 %d/%d 个节，疑似未逐节取证'
                             % (','.join(sorted(top)) or '空', cnt, len(sets)))

    return problems, warns


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    files = []
    if args[0] == '--dir':
        if len(args) < 2:
            print('用法：--dir <目录>')
            return 2
        files = sorted(pathlib.Path(args[1]).glob('*.md'))
    else:
        files = [pathlib.Path(a) for a in args]

    bad = 0
    for p in files:
        if not p.is_file():
            print('!! 文件不存在: %s' % p)
            bad += 1
            continue
        probs, warns = check_file(p)
        if probs:
            bad += 1
            print('✗ %s' % p.name)
            for x in dict.fromkeys(probs):
                print('    - %s' % x)
        elif warns:
            print('△ %s' % p.name)
            for x in warns:
                print('    ~ %s' % x)
        else:
            print('✓ %s' % p.name)

    print('\n质检：%d 个文件，%d 个不通过' % (len(files), bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
