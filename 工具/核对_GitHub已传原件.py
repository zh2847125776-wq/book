# -*- coding: utf-8 -*-
"""核查「原件笔记」是否已完整上传到 GitHub —— 不克隆仓库，直接对 git blob SHA-1。

原理：GitHub 的 tree API 给出每个文件的 **git blob SHA-1**，
      本地对同一份内容算同样的 blob SHA-1，两者相等即「逐字节已上传」。
      所以 427 MB 的仓库也能在几十秒内核完，不用下载。

关键坑：仓库有 .gitattributes `* text=auto eol=lf`，本地是 CRLF。
      git 提交时会把 CRLF 转成 LF，字节一变 blob SHA 就不同。
      本脚本同时算「原始」与「LF 归一」两个 blob，任一命中即算已上传 ——
      否则会产生大量假阴性（实测：不归一 = 4,012 命中，归一 = 14,411 命中）。

用法：
  python -X utf8 工具/核对_GitHub已传原件.py <owner>/<repo>
  python -X utf8 工具/核对_GitHub已传原件.py zh2847125776-wq/book
  python -X utf8 工具/核对_GitHub已传原件.py zh2847125776-wq/book --分支 main --导出 待补.tsv
  python -X utf8 工具/核对_GitHub已传原件.py zh2847125776-wq/book --tree 缓存.json   # 离线，用已存的 tree

  # 存一份 tree 缓存（免得反复吃 API 限额）：
  curl -s "https://api.github.com/repos/<owner>/<repo>/git/trees/<分支>?recursive=1" -o tree.json

退出码：0 = 原件笔记齐全（无内容缺失）；1 = 有内容缺失；2 = 用法/网络错误
"""
import csv
import hashlib
import json
import pathlib
import sys
import urllib.parse
import urllib.request

BASE = pathlib.Path(r'C:\Users\赵豪\dsh')
MANIFEST = BASE / '交易知识体系汇编/01_资料与索引/来源清单.tsv'

# 这些不算「原件笔记」，缺失不判失败（脚本、空文件、工作/交付文档）
NOISE_EXT = {'.py', '.tsv', '.json', '.sh', '.log', '.bak'}
NOISE_DIRS = {'知识库', '_待汇编', '转写结果'}
NOISE_NAMES = {'第195'}  # 0 字节空文件（实测）


def blob_sha(data):
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def api(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'dsh-verify', 'Accept': 'application/vnd.github+json'})
    return json.loads(urllib.request.urlopen(req, timeout=60).read().decode('utf-8'))


def fetch_tree(repo, branch):
    info = api('https://api.github.com/repos/%s' % repo)
    branch = branch or info.get('default_branch', 'main')
    t = api('https://api.github.com/repos/%s/git/trees/%s?recursive=1' % (repo, branch))
    if t.get('truncated'):
        print('!! 警告：tree 被截断，结果可能不全')
    return branch, [x for x in t['tree'] if x['type'] == 'blob']


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith('-'):
        print(__doc__)
        return 2
    repo = a[0]
    branch = None
    export = None
    treefile = None
    for i, x in enumerate(a):
        if x == '--分支' and i + 1 < len(a):
            branch = a[i + 1]
        if x == '--导出' and i + 1 < len(a):
            export = a[i + 1]
        if x == '--tree' and i + 1 < len(a):
            treefile = a[i + 1]

    if treefile:
        d = json.loads(pathlib.Path(treefile).read_text(encoding='utf-8'))
        if 'tree' not in d:
            print('缓存文件不含 tree:', treefile)
            return 2
        branch = branch or '(缓存)'
        tree = [x for x in d['tree'] if x['type'] == 'blob']
        if d.get('truncated'):
            print('!! 警告：缓存的 tree 被截断，结果可能不全')
    else:
        try:
            branch, tree = fetch_tree(repo, branch)
        except Exception as e:
            print('拉取失败: %s %s' % (type(e).__name__, e))
            print('（未认证 API 限额 60 次/小时。可用 --tree 缓存文件离线跑。）')
            return 2

    blobs = {x['sha']: x['path'] for x in tree}
    by_name = {}
    for x in tree:
        by_name.setdefault(x['path'].split('/')[-1], []).append(x['path'])
    print('仓库 %s@%s ｜ blob 数 %d ｜ 唯一 %d' % (repo, branch, len(tree), len(blobs)))
    print('本地清单 %s\n' % MANIFEST.name)

    rows = list(csv.DictReader(open(MANIFEST, encoding='utf-8'), delimiter='\t'))
    ok_raw = ok_lf = 0
    missing, diverged = [], []
    for r in rows:
        rel = (r['相对路径'] or '').strip()
        p = BASE / rel.replace('\\', '/')
        if not p.is_file():
            missing.append((r['source_id'], rel, '本地缺'))
            continue
        raw = p.read_bytes()
        if blob_sha(raw) in blobs:
            ok_raw += 1
            continue
        if blob_sha(raw.replace(b'\r\n', b'\n')) in blobs:
            ok_lf += 1
            continue
        # 内容对不上：看仓库里有没有同名文件（= 仓库版本更新）
        same = by_name.get(p.name)
        if same:
            diverged.append((r['source_id'], rel, same[0]))
        else:
            missing.append((r['source_id'], rel, '仓库无'))

    print('  ✓ 原始字节一致        : %d' % ok_raw)
    print('  ✓ LF 归一后一致        : %d' % ok_lf)
    print('  → 已上传合计          : %d / %d' % (ok_raw + ok_lf, len(rows)))
    print('  ⚠ 仓库版本更新（本地旧）: %d' % len(diverged))
    print('  ✗ 仓库无               : %d' % len(missing))

    if diverged:
        print('\n仓库版本更新的（不算缺失，是本地旧了）:')
        for sid, l, rp in diverged[:20]:
            print('  %-12s 本地 %s' % (sid, l))
            print('  %-12s 仓库 %s' % ('', rp))
    if missing:
        print('\n仓库没有的:')
        for sid, rel, why in missing:
            print('  %-12s %-8s %s' % (sid, why, rel))

    if export:
        out = pathlib.Path(export)
        lines = ['source_id\t本地相对路径\t原因']
        lines += ['%s\t%s\t%s' % (s, r, w) for s, r, w in missing]
        lines += ['%s\t%s\t仓库版本更新' % (s, r) for s, r, _ in diverged]
        out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        print('\n已导出: %s（%d 行）' % (out, len(lines) - 1))

    # 分类：只有「课程笔记」判失败；其余只提示
    def category(rel):
        pre = rel.split('\\')[0]
        name = rel.split('\\')[-1]
        f = BASE / rel.replace('\\', '/')
        # 先排噪声：脚本 / 空文件 / 无扩展名杂项
        if (pathlib.PurePath(name).suffix.lower() in NOISE_EXT
                or name in NOISE_NAMES
                or (f.is_file() and f.stat().st_size == 0)):
            return '脚本/空文件'
        if pre in NOISE_DIRS or name.startswith('交付书_') or name.startswith('核数'):
            return '交付/工作文档'
        if pre == '学习笔记' or pre.startswith('_完整稿备份'):
            return '课程笔记'
        return '其他'

    cat = {}
    for s, r, w in missing:
        cat.setdefault(category(r), []).append((s, r))
    print('\n缺失分类:')
    for k in ('课程笔记', '交付/工作文档', '脚本/空文件', '其他'):
        if k in cat:
            print('  %-14s %d 份%s' % (k, len(cat[k]), '  ← 需要处理' if k == '课程笔记' else ''))
            for s, r in cat[k][:8]:
                print('        %-12s %s' % (s, r))

    notes = cat.get('课程笔记', [])
    if notes:
        print('\n结论：不齐全 —— 还有 %d 份课程笔记没上传。' % len(notes))
        return 1
    print('\n结论：齐全 —— 课程笔记已全部上传（逐字节一致或仓库版本更新）。')
    if cat.get('交付/工作文档'):
        print('       另有 %d 份交付/工作文档未上传（非课程笔记，按需补）。' % len(cat['交付/工作文档']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
