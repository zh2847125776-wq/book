# -*- coding: utf-8 -*-
"""把 book 仓库按「内容类型」重排成结构清晰的分类。

目标结构：
  01_量化技术分析_精简笔记/            3,628
  02_量化技术分析_完整稿/              3,629
  03_增强版素材/{股票,期货,读书,解盘,专题,基础课}/
  04_妖股成妖之路/{原稿章节,蒸馏笔记,精要}/
  _归档/元数据/{核数与交付报告,任务书}/     ← 按用户要求「元数据不要」，移出编号体系，不删除

设计要点：
  * 用「文件系统移动 + git add -A」，不用逐文件 git mv（10,846 次进程太慢）。
    内容不变 ⇒ git 自动识别为 rename（100% 相似度），历史保留。
  * **迁移前后逐字节校验**：比对 git blob 集合，必须完全一致，否则中止。
  * 重名冲突：04 与 07 有 11 个同名文件但内容不同
    （04 是「精简版」、07 是「完整版」），04 那份加 `_精简版` 后缀，两份都保留。

用法：
  python -X utf8 工具/迁移_book仓库结构.py <仓库目录>            # 干跑，只打印方案
  python -X utf8 工具/迁移_book仓库结构.py <仓库目录> --apply    # 执行
"""
import collections
import pathlib
import re
import subprocess
import sys

# 增强版素材的子类（按文件名前缀判定）
ENH_KINDS = ('股票', '期货', '读书', '解盘', '专题')
# 04 里混进来的增强版：内容与 07 同名文件不同，加此后缀区分
DEDUP_SUFFIX = '_精简版'


# 旧目录名 → 新目录（**按完整目录名精确匹配，不用前缀**）
# 用前缀会让脚本不幂等：迁移后 `01_量化技术分析_精简笔记` 会撞上旧规则 `01_妖股成妖之路_精要`，
# 重跑一次就把 3,628 份精简笔记丢进 `04_妖股成妖之路/精要`。实测踩过。
OLD_DIRS = {
    '03_量化技术分析_精简笔记_2979-3638课': '01_量化技术分析_精简笔记',
    '05_量化技术分析_完整稿_2979-3638课': '02_量化技术分析_完整稿',
    '06_量化技术分析_完整稿_1-2978课': '02_量化技术分析_完整稿',
    '02_妖股成妖之路_蒸馏笔记': '04_妖股成妖之路/蒸馏笔记',
    '08_妖股成妖之路_原稿章节': '04_妖股成妖之路/原稿章节',
    '01_妖股成妖之路_精要': '04_妖股成妖之路/精要',
    '09_核数与交付报告': '_归档/元数据/核数与交付报告',
    '10_任务书': '_归档/元数据/任务书',
}
# 04 与 07 需要按文件名二次分流，不能整目录映射
SPLIT_DIRS = ('04_量化技术分析_笔记_1-2978课', '07_增强版素材_量化技术分析')


def target_of(rel):
    """旧路径 → 新路径。已在目标结构中的返回原值（**幂等**）。"""
    parts = rel.split('/')
    if len(parts) == 1:
        return rel                      # README.md / .gitattributes 留在根
    top, name = parts[0], parts[-1]
    if top in OLD_DIRS:
        return OLD_DIRS[top] + '/' + name
    if top == '04_量化技术分析_笔记_1-2978课':
        return ('03_增强版素材/基础课/' if '增强版' in name
                else '01_量化技术分析_精简笔记/') + name
    if top == '07_增强版素材_量化技术分析':
        for k in ENH_KINDS:
            if name.startswith('(增强版)' + k):
                return '03_增强版素材/%s/' % k + name
        return '03_增强版素材/基础课/' + name
    return rel                          # 未知/已是新结构 → 不动


def git(repo, *args, check=True):
    # core.quotePath=false：否则 git 会把中文路径转义成 "\345\246..." 八进制，映射会全落空
    r = subprocess.run(['git', '-c', 'core.quotePath=false'] + list(args),
                       cwd=str(repo), capture_output=True, text=True, encoding='utf-8')
    if check and r.returncode != 0:
        raise SystemExit('git %s 失败:\n%s%s' % (' '.join(args), r.stdout, r.stderr))
    return r.stdout


def index_blobs(repo):
    """git 索引里的 path → blob sha。"""
    out = git(repo, 'ls-files', '-s')
    m = {}
    for line in out.splitlines():
        if not line.strip():
            continue
        meta, path = line.split('\t', 1)
        m[path] = meta.split()[1]
    return m


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith('-'):
        print(__doc__)
        return 2
    repo = pathlib.Path(a[0]).resolve()
    apply_ = '--apply' in a
    if not (repo / '.git').is_dir():
        print('不是 git 仓库: %s' % repo)
        return 2

    before = index_blobs(repo)
    print('仓库: %s' % repo)
    print('索引文件数: %d' % len(before))

    # 计算目标 + 冲突
    plan = {}
    buckets = collections.defaultdict(list)
    for rel in before:
        buckets[target_of(rel)].append(rel)
    collisions = {k: v for k, v in buckets.items() if len(v) > 1}

    rename_map = {}
    for tgt, srcs in collisions.items():
        # 04 来源的加 _精简版 后缀
        c04 = [s for s in srcs if s.split('/')[0].startswith('04_')]
        c07 = [s for s in srcs if s.split('/')[0].startswith('07_')]
        if len(srcs) == 2 and len(c04) == 1 and len(c07) == 1:
            stem, dot, ext = tgt.rpartition('.')
            rename_map[c04[0]] = '%s%s.%s' % (stem, DEDUP_SUFFIX, ext)
        else:
            raise SystemExit('未预期的冲突组合，需人工裁决: %s -> %s' % (tgt, srcs))

    for rel in before:
        tgt = rename_map.get(rel) or target_of(rel)
        plan[rel] = tgt

    # 目标重名二次检查
    dup = collections.Counter(plan.values())
    bad = {k: v for k, v in dup.items() if v > 1}
    if bad:
        print('!! 处理后仍有重名:')
        for k, v in bad.items():
            print('   %s x%d' % (k, v))
            for r, t in plan.items():
                if t == k:
                    print('       ← %s' % r)
        return 1

    dist = collections.Counter(t.rsplit('/', 1)[0] for t in plan.values())
    print('\n目标目录分布:')
    for k, v in sorted(dist.items()):
        print('  %-34s %d' % (k, v))
    if rename_map:
        print('\n重名冲突处理（%d 处，均保留两份）:' % len(rename_map))
        for s, t in sorted(rename_map.items()):
            print('  %s' % s)
            print('    → %s' % t)

    if not apply_:
        print('\n（干跑。加 --apply 执行。）')
        return 0

    # ---- 执行 ----
    print('\n开始迁移…')
    moved = 0
    for rel, tgt in sorted(plan.items()):
        if rel == tgt:
            continue
        src, dst = repo / rel, repo / tgt
        if not src.exists():
            print('!! 源不存在: %s' % rel)
            return 1
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)
        moved += 1
    print('移动 %d 个文件' % moved)

    # 清理空目录
    removed = 0
    for p in sorted(repo.rglob('*'), key=lambda x: -len(x.parts)):
        if p.is_dir() and '.git' not in p.parts:
            try:
                if not any(p.iterdir()):
                    p.rmdir()
                    removed += 1
            except OSError:
                pass
    print('清理空目录 %d 个' % removed)

    git(repo, 'add', '-A')
    after = index_blobs(repo)

    # ---- 逐字节校验 ----
    cb, ca = collections.Counter(before.values()), collections.Counter(after.values())
    print('\n=== 内容完整性校验 ===')
    print('  迁移前 blob 集合: %d 个（%d 个文件）' % (len(cb), sum(cb.values())))
    print('  迁移后 blob 集合: %d 个（%d 个文件）' % (len(ca), sum(ca.values())))
    if cb == ca:
        print('  ✓ 逐字节一致 —— 内容零改动，纯路径重排')
    else:
        lost = cb - ca
        gained = ca - cb
        print('  ✗ 内容有变化！')
        for s, n in list(lost.items())[:10]:
            print('     丢失 blob %s x%d' % (s[:12], n))
        for s, n in list(gained.items())[:10]:
            print('     新增 blob %s x%d' % (s[:12], n))
        print('\n已中止，未提交。请检查后手工处理。')
        return 1

    r = git(repo, 'status', '--short', '--find-renames')
    stats = collections.Counter()
    for line in r.splitlines():
        if line.strip():
            stats[line[:2].strip()] += 1
    print('\n  git status 摘要: %s' % dict(stats))
    print('\n下一步（确认无误后）：')
    print('  git -C "%s" commit -m "重排目录结构：按内容类型分类"' % repo)
    print('  git -C "%s" push origin main' % repo)
    return 0


if __name__ == '__main__':
    sys.exit(main())
