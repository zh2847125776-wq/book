# -*- coding: utf-8 -*-
"""把卡片字段里混进证据号序列的 `证据未逐字回源` 标记移位。

背景（验收报告 §3.1）：
  批363 的 12 张卡把「证据未逐字回源」写在了证据号位置上，例如
      > 来源：SRC-002703（…）· 证据 E-91580, …, E-91585, 证据未逐字回源, E-91587
      - 外汇标的参数：跟踪USDCNY日线与均线运行状态（E-91585、证据未逐字回源）。
  它其实是「一个未通过逐字回源校验、因此**没有登记编号**的证据位」
  （核对证据索引：SRC-002703 有 E-91580–91585、E-91587，**缺 E-91586**）。
  问题不在内容，在于它长得像证据号 —— 会被当成 ID 解析。

处置：
  1. `> 来源：… · 证据 <列表>` 里剔掉它，紧跟一行
     `> 证据限制：另有 N 处证据未通过逐字回源校验，未登记编号。`
  2. 正文引用列表 `（E-91585、证据未逐字回源）` → `（E-91585）`
  3. 独立出现的 `（证据未逐字回源）` → `（本处未通过逐字回源校验）`
  4. 表格「证据ID」列 → `—`
  5. 区间写法 `E-91588..证据未逐字回源` → `E-91588 等`

用法：
  python -X utf8 工具/修_证据未逐字回源标记.py <目录>            # 干跑
  python -X utf8 工具/修_证据未逐字回源标记.py <目录> --apply    # 执行
"""
import pathlib
import re
import sys

MARK = '证据未逐字回源'
LIMIT_LINE = '> 证据限制：另有 %d 处证据未通过逐字回源校验，未登记编号。'


def fix_text(text):
    """返回 (新文本, 改动条数)。"""
    lines = text.split('\n')
    out = []
    n_fix = 0

    for ln in lines:
        orig = ln

        # 1) 来源行：剔标记 + 追加证据限制行
        if ln.startswith('> 来源：') and MARK in ln:
            cnt = ln.count(MARK)
            ln = re.sub(r'\s*[,，、]\s*' + MARK, '', ln)   # 列表内的
            ln = ln.replace(MARK, '')                       # 兜底
            ln = re.sub(r'\s*[,，、]\s*$', '', ln)          # 去掉尾部逗号
            ln = re.sub(r'\s{2,}', ' ', ln)
            out.append(ln)
            out.append(LIMIT_LINE % cnt)
            n_fix += cnt
            continue

        if MARK not in ln:
            out.append(ln)
            continue

        # 4) 表格「证据ID」单元格
        ln = ln.replace('| %s |' % MARK, '| — |')

        # 5) 区间写法 E-xxxx..证据未逐字回源
        ln = re.sub(r'(E-\d+)\.\.' + MARK, r'\1 等', ln)

        # 2) 引用列表内的：剔掉（连同分隔符）
        ln = re.sub(r'[、，,]\s*' + MARK, '', ln)
        ln = re.sub(MARK + r'\s*[、，,]', '', ln)

        # 3) 剩下的独立出现
        ln = ln.replace('（%s）' % MARK, '（本处未通过逐字回源校验）')
        ln = ln.replace('(%s)' % MARK, '（本处未通过逐字回源校验）')
        ln = ln.replace(MARK, '本处未通过逐字回源校验')

        # 清理：空括号、双顿号
        ln = ln.replace('（）', '').replace('()', '')
        ln = re.sub(r'[、，,]\s*[）)]', '）', ln)
        ln = re.sub(r'[、，,]{2,}', '、', ln)
        ln = re.sub(r'\s{2,}', ' ', ln)

        if ln != orig:
            n_fix += orig.count(MARK)
        out.append(ln)

    return '\n'.join(out), n_fix


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 2
    root = pathlib.Path(a[0])
    apply_ = '--apply' in a
    if not root.is_dir():
        print('不是目录: %s' % root)
        return 2

    targets = []
    for sub in ('02_知识点', '03_方法与策略', '04_案例'):
        d = root / sub
        if d.is_dir():
            targets += sorted(d.glob('*.md'))
    if not targets:
        # 允许直接传卡片目录
        targets = sorted(root.glob('*.md'))

    hit = []
    for p in targets:
        t = p.read_text(encoding='utf-8')
        if MARK not in t:
            continue
        new, n = fix_text(t)
        hit.append((p, n, t, new))

    print('扫描 %d 张卡，命中标记 %d 张' % (len(targets), len(hit)))
    for p, n, old, new in hit:
        print('  %-58s 处理 %d 处' % (p.name[:58], n))

    if not apply_:
        if hit:
            p, n, old, new = hit[0]
            print('\n=== 干跑样例（%s）===' % p.name[:50])
            import difflib
            for l in list(difflib.unified_diff(old.split('\n'), new.split('\n'),
                                               '改前', '改后', lineterm='', n=0))[:30]:
                print('  ' + l[:150])
        print('\n（干跑。加 --apply 执行。）')
        return 0

    for p, n, old, new in hit:
        p.write_text(new, encoding='utf-8')
    print('\n已修改 %d 个文件' % len(hit))
    return 0


if __name__ == '__main__':
    sys.exit(main())
