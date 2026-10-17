# -*- coding: utf-8 -*-
"""核对 GitHub 上的原件是否与本项目清单一致。

背景：原件共 24,652 份 / 约 3.5 GB，分两张清单登记：
  01_资料与索引/来源清单.tsv       14,426 份（课程笔记与完整稿备份）748.9 MB
  01_资料与索引/来源清单_转写.tsv   10,226 份（转写结果）              2.74 GB
两张清单的 SHA256 已全量实测核对过（14,426/14,426 与 10,226/10,226 全部一致），
可直接作为核对基准。

用法：
  python -X utf8 工具/核对_GitHub原件.py <仓库目录>
  python -X utf8 工具/核对_GitHub原件.py <仓库目录> --清单 主        # 只核主清单
  python -X utf8 工具/核对_GitHub原件.py <仓库目录> --清单 转写      # 只核转写清单
  python -X utf8 工具/核对_GitHub原件.py <仓库目录> --sample 300     # 抽查 300 份（快）

匹配策略（文件名不唯一，主清单 14,426 行只有 7,217 个唯一名，所以不能只按文件名）：
  1. 路径优先：仓库里按「相对路径」能找到同名同结构的文件 → 直接比哈希
  2. 哈希兜底：路径对不上时，看该 SHA256 是否出现在仓库里（容忍目录结构不同）
  3. 两者都没有 → 判「缺失」

退出码：0 = 无缺失无哈希不符；1 = 有问题；2 = 用法错误
"""
import csv
import hashlib
import pathlib
import sys

BASE = pathlib.Path(r'C:\Users\赵豪\dsh')
IDX = BASE / '交易知识体系汇编/01_资料与索引'
MANIFESTS = {
    '主': IDX / '来源清单.tsv',
    '转写': IDX / '来源清单_转写.tsv',
}


def load(kind):
    rows = []
    for f in (MANIFESTS[kind],):
        for r in csv.DictReader(open(f, encoding='utf-8'), delimiter='\t'):
            rel = (r.get('相对路径') or '').strip()
            sha = (r.get('SHA256') or '').strip().lower()
            if rel and sha:
                rows.append((r['source_id'], rel, sha))
    return rows


def sha256_of(p, cache):
    st = p.stat()
    key = (str(p), st.st_size, int(st.st_mtime))
    if key not in cache:
        h = hashlib.sha256()
        with open(p, 'rb') as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b''):
                h.update(chunk)
        cache[key] = h.hexdigest()
    return cache[key]


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith('-'):
        print(__doc__)
        return 2
    repo = pathlib.Path(args[0])
    if not repo.is_dir():
        print('目录不存在: %s' % repo)
        return 2
    kind = '全部'
    sample = 0
    for i, a in enumerate(args):
        if a == '--清单' and i + 1 < len(args):
            kind = args[i + 1]
        if a == '--sample' and i + 1 < len(args):
            sample = int(args[i + 1])

    kinds = ['主', '转写'] if kind == '全部' else [kind]
    expected = []
    for k in kinds:
        expected += load(k)
    if sample:
        step = max(1, len(expected) // sample)
        expected = expected[::step][:sample]
    print('清单条目: %d（%s）｜ 仓库: %s' % (len(expected), '+'.join(kinds), repo))

    # 扫仓库：建立 basename→[路径] 与 哈希多重集
    repo_files, by_name = [], {}
    for p in repo.rglob('*'):
        if not p.is_file() or '.git' in p.parts:
            continue
        repo_files.append(p)
        by_name.setdefault(p.name, []).append(p)
    print('仓库文件: %d，开始核对…\n' % len(repo_files))

    cache = {}
    repo_hashes = {}
    for p in repo_files:
        repo_hashes.setdefault(sha256_of(p, cache), []).append(p)

    ok_path = ok_hash = missing = mismatch = 0
    miss_list, mism_list = [], []
    seen_hash = set()
    for sid, rel, sha in expected:
        p = repo / rel.replace('\\', '/')
        if p.is_file():
            if sha256_of(p, cache) == sha:
                ok_path += 1
                seen_hash.add(sha)
                continue
            mismatch += 1
            mism_list.append((sid, rel))
            continue
        if sha in repo_hashes:
            ok_hash += 1
            seen_hash.add(sha)
            continue
        missing += 1
        miss_list.append((sid, rel))

    exp_hashes = {s for _, _, s in expected}
    cov = len(exp_hashes & set(repo_hashes)) / len(exp_hashes) * 100 if exp_hashes else 0

    print('  清单条目 %d ｜ 其中唯一哈希 %d ｜ 仓库文件 %d ｜ 仓库唯一哈希 %d'
          % (len(expected), len(exp_hashes), len(repo_files), len(repo_hashes)))
    print()
    print('  ✓ 路径+哈希一致（强）      : %d' % ok_path)
    print('  ○ 仅哈希命中（路径不同/内容重复，弱）: %d' % ok_hash)
    print('  ✗ 哈希不符                  : %d' % mismatch)
    print('  ✗ 缺失（清单有、仓库没有）  : %d' % missing)
    print()
    print('  ★ 唯一哈希覆盖率: %.2f%%（%d/%d）—— 这是「原件是否完整」的可靠口径'
          % (cov, len(exp_hashes & set(repo_hashes)), len(exp_hashes)))
    print('    注：清单里同一内容存在多处副本（14,426 行只有 7,217 个唯一名），')
    print('        所以「仅哈希命中」会把一份文件算作满足多行，不能单独当通过依据。')

    if mism_list:
        print('\n哈希不符明细（前 20）:')
        for sid, rel in mism_list[:20]:
            print('  %-12s %s' % (sid, rel))
    if miss_list:
        print('\n缺失明细（前 20）:')
        for sid, rel in miss_list[:20]:
            print('  %-12s %s' % (sid, rel))

    bad = mismatch + missing + (len(exp_hashes) - len(exp_hashes & set(repo_hashes)))
    if bad:
        print('\n结论：不通过 —— %d 份有问题，合并前须解决。' % bad)
        return 1
    print('\n结论：通过 —— 清单里 %d 份原件在仓库中全部逐字节一致。' % len(expected))
    return 0


if __name__ == '__main__':
    sys.exit(main())
