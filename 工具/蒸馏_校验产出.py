# -*- coding: utf-8 -*-
"""阶段2 蒸馏产出通用校验器。

用法:
    python 工具/蒸馏_校验产出.py <回复.json> [资料包.md]

校验口径（回源底本 = 01_资料与索引/证据索引.tsv 全量原文，不采信产出方自检）:
  1) 运行标记 / JSON 可解析
  2) raw_quote 与 unquantifiable.quote 逐字回源（去空白后命中单独计数）
  3) 字段规范（type / confidence / stance / evidence_level 取值域）
  4) 引用纯净性（不得带【…】前缀）
  5) condition 中数字的出处（疑似凭空 → 打印待人工定性，多为 %→小数 换算）
  6) 每卡覆盖情况
退出码: 0 = 通过（无未命中）；1 = 有未命中，该批需重跑。
"""
import json, re, csv, sys, pathlib, collections

REPO = pathlib.Path(__file__).resolve().parent.parent
EV_TSV = REPO / '01_资料与索引/证据索引.tsv'

TYPES = {'entry_long', 'entry_short', 'exit', 'filter', 'position_sizing', 'risk'}
CONF = {'high', 'medium', 'low'}


def load_evidence():
    ev = {}
    with open(EV_TSV, encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            eid = (r.get('证据ID') or '').strip()
            if re.fullmatch(r'E-\d{4,5}', eid):
                ev[eid] = r.get('原文摘录') or ''
    return ev


def load_pack(pack_path):
    if not pack_path or not pathlib.Path(pack_path).exists():
        return {}
    t = pathlib.Path(pack_path).read_text(encoding='utf-8')
    return {s[:6]: s for s in re.split(r'\n=+\n## 资料 \d+ ｜ ', t)[1:]}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    reply = pathlib.Path(sys.argv[1])
    pack = load_pack(sys.argv[2] if len(sys.argv) > 2 else None)
    ev = load_evidence()
    norm = lambda s: re.sub(r'\s+', '', s or '')

    raw = reply.read_text(encoding='utf-8', errors='replace')
    token = re.search(r'RUN-DISTILL-[0-9A-Za-z\-]+', raw)
    i, j = raw.find('{'), raw.rfind('}')
    if i < 0 or j < 0:
        print('✗ 未找到 JSON 主体')
        return 1
    data = json.loads(raw[i:j+1])
    rules, unq = data.get('rules', []), data.get('unquantifiable', [])

    print('运行标记:', token.group(0) if token else '缺失（内容明确时可接受）')
    print('规则 %d 条 ｜ 不可量化 %d 条' % (len(rules), len(unq)))

    print('type 非法:', [r.get('rule_id') for r in rules if r.get('type') not in TYPES] or '无',
          '｜ confidence 非法:', [r.get('rule_id') for r in rules if r.get('confidence') not in CONF] or '无')
    print('stance:', dict(collections.Counter(r.get('stance') for r in rules)))
    print('evidence_level:', dict(collections.Counter(r.get('evidence_level') for r in rules)))
    pre = [r.get('rule_id') for r in rules if (r.get('raw_quote') or '').startswith('【')]
    pre += ['U:' + str(u.get('card_ref')) for u in unq if (u.get('quote') or '').startswith('【')]
    print('带【…】前缀:', len(pre) or '无')

    ex = soft = 0
    miss = []
    for r in rules:
        q = r.get('raw_quote') or ''
        pool = [ev.get(e, '') for e in (r.get('evidence_ids') or [])] + [pack.get(r.get('card_ref', ''), '')]
        if any(q and q in p for p in pool if p):
            ex += 1
        elif any(q and norm(q) in norm(p) for p in pool if p):
            soft += 1
        else:
            miss.append((r.get('rule_id'), q[:60]))
    umiss = []
    for u in unq:
        q = (u.get('quote') or '').strip()
        pool = [pack.get(u.get('card_ref', ''), '')] + list(ev.values())
        if not any(q and norm(q) in norm(p) for p in pool if p):
            umiss.append((u.get('card_ref'), q[:60]))
    print('rules 逐字命中 %d ｜ 去空白命中 %d ｜ **未命中 %d**' % (ex, soft, len(miss)))
    for m in miss[:10]:
        print('   ✗', m[0], '|', m[1])
    print('unquantifiable 未命中 %d' % len(umiss))
    for m in umiss[:10]:
        print('   ✗', m)

    ghost = []
    for r in rules:
        nums = set(re.findall(r'\d+(?:\.\d+)?', str(r.get('condition') or '')))
        hay = pack.get(r.get('card_ref', ''), '') + ' '.join(ev.get(e, '') for e in (r.get('evidence_ids') or []))
        ghost += [(r.get('rule_id'), n) for n in nums if n not in hay]
    print('condition 疑似凭空数字 %d 处（需人工定性：多为百分号→小数 换算）' % len(ghost))
    for g in ghost[:10]:
        print('   ?', g)

    cov = collections.Counter(r.get('card_ref') for r in rules)
    zero = [c for c in pack if c not in cov and c not in {u.get('card_ref') for u in unq}]
    print('每卡规则数:', dict(cov))
    print('完全未处理的卡:', zero or '无')
    return 1 if (miss or umiss) else 0


if __name__ == '__main__':
    sys.exit(main())
