# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-002732', 'SRC-000244')
COUNTS = {'K': 2, 'S': 2, 'C': 2, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-002732', 'SRC-002732_(增强版)读书_11聪明的投资者.md', 2836, [11, 1237]),
    ('SRC-000244', 'SRC-000244_(增强版)妖股成妖之路_22.md', 1238, [287, 725])
]:
    p = root / 'stage' / name
    b = p.read_bytes()
    t = p.read_text(encoding='utf-8')
    ls = t.splitlines()
    assert len(ls) == lines
    R[sid] = dict(
        chars=len(t),
        raw_bytes=len(b),
        raw_sha256=hashlib.sha256(b).hexdigest(),
        text_sha256=hashlib.sha256(t.encode('utf-8')).hexdigest(),
        ranges=[(0, len(t))],
        reader='主代理'
    )
    for ln in picks:
        i = ln - 1
        x = ls[i]
        E.append((sid, ln, x))
        marks = [z for z in ls[:ln] if z.startswith(('**🎙', '**📝', '**📈'))]
        fr = [z for z in ls[:ln] if z.startswith(('## ⏱', '# '))][-1]
        col = '**🎙 语音转录(前后30s)**:' if (marks and marks[-1].startswith('**🎙')) else (marks[-1] if marks else '正文段落')
        L.append((fr, col))

K = (
    (
        '聪明的投资者研读记录与道琼斯指数低价低市盈率选股策略对比',
        'SRC-002732',
        '源文口述记录研读《聪明的投资者》第121页略过国债投资内容，课件OCR记录道琼斯工业平均指数中投资价格最低的6种或10种股票假设，讲述者对比A股年会低价股策略。{E0}{E1}',
        '仅记录≤300字完整原文字面的研读进度背景与道琼斯工业指数低价低市盈率选股假设，不采信Vision推断，不截断超长语音行。{E0}{E1}',
        [
            '口述记录研读《聪明的投资者》进展至121页并略过国债内容。{E0}',
            '课件OCR记录投资道琼斯指数价格与利润比最低的6种或10种股票假设。{E1}'
        ],
        '其余超300字语音转录单行按禁截断无省略号铁律不予入证。{E0}{E1}',
        '关联S0与C0；不跨源混用。{E0}{E1}',
        '见S0与C0；研读聪明的投资者与道琼斯低价股策略对比。{E0}{E1}'
    ),
    (
        '妖股情绪退潮期管住手控仓与核心情绪风向标个股观察',
        'SRC-000244',
        '源文记录情绪全面退潮期务必管住手并控制住仓位，个股方面将四川长虹、海能达、常山北明、欧菲光等作为情绪风向标加入自选跟踪。{E2}{E3}',
        '仅记录≤300字完整原文字面的退潮期控仓规则与风向标标的记录，不凭空编造未披露的买卖点。{E2}{E3}',
        [
            '原文明确提示“情绪全面退潮期，务必管住手，控制住仓位”。{E2}',
            '原文明确列示“个股方面，情绪风向标：四川长虹、海能达、常山北明、欧菲光等等”。{E3}'
        ],
        '仅限短线短文记录，不跨接其他来源。{E2}{E3}',
        '关联S1与C1；不跨源混用。{E2}{E3}',
        '见S1与C1；退潮期控仓与风向标跟踪。{E2}{E3}'
    )
)

S = (
    (
        '结合大盘指数与多重过滤条件的低价股筛选与技术买卖方法',
        'SRC-002732',
        '在研读经典价值投资著作并结合A股低价股策略时使用。{E0}{E1}',
        '针对《聪明的投资者》中单纯投资道琼斯指数低价低市盈率股票的假设，指出A股必须配合非ST非亏损及大周期技术走好等条件，以日线作为买卖标准。{E0}{E1}',
        {
            '环境过滤': ('研读聪明的投资者背景下关注低价股票投资策略', '日线', '{E0}', '读书研讨背景'),
            '形态或指标形成': ('道琼斯工业平均指数中价格与利润之比最低的6种或10种股票假设', '日线', '{E1}', '课件原书假设'),
            '确认': ('结合A股市场实际增加大周期走好与非ST非亏损等多重过滤确认', '日线', '{E0}{E1}', '综合条件过滤'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('跟踪选出的低价标的在自选股中的表现', '日线', '{E0}{E1}', '自选跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '在研读道琼斯低价股策略时，补充A股多重过滤逻辑。{E0}{E1}',
        '同源K0与C0。{E0}{E1}',
        'Vision不作证；超长语音行不截断入证。{E0}{E1}'
    ),
    (
        '市场情绪退潮期仓位控制与情绪风向标跟踪应对方法',
        'SRC-000244',
        '在短线市场经历高位分歧并确认进入全面退潮期时使用。{E2}{E3}',
        '在情绪全面退潮期严格管住手并控制住仓位，同时将核心龙头及风向标（四川长虹、海能达、常山北明、欧菲光）加入自选密切跟踪其跌停与反馈。{E2}{E3}',
        {
            '环境过滤': ('市场确认进入情绪全面退潮期', '日内/短线', '{E2}', '情绪退潮环境'),
            '形态或指标形成': ('核心龙头跌停且情绪风向标集体出现负反馈', '日内/短线', '{E3}', '风向标负反馈'),
            '确认': ('核对风向标标的反馈确认退潮深度', '日内/短线', '{E2}{E3}', '退潮确认'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('全面退潮期务必管住手，严格控制住仓位，防范亏钱效应扩散', '短线', '{E2}', '仓位严格控制'),
            '持仓与跟踪': ('将四川长虹、海能达、常山北明、欧菲光等风向标加入自选跟踪', '短线', '{E3}', '风向标自选跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('若风向标未现负反馈则退潮假设需修正', '短线', '{E3}', '风向标未走弱')
        },
        '在情绪退潮期管住手控仓，通过跟踪核心风向标决定下一步动作。{E2}{E3}',
        '同源K1与C1。{E2}{E3}',
        '原文未披露具体买卖点数值，未明环节一律留缺。{E2}{E3}'
    )
)

C = (
    (
        '《聪明的投资者》研读与低价股投资策略对比复盘',
        'SRC-002732',
        '2021年1月18日（源文课件时间）。{E0}{E1}',
        '道琼斯工业平均指数成分股与A股低价标的（源文课件与口述）。{E0}{E1}',
        '课堂读书与策略对比复盘，非独立回测或交易流水。{E0}{E1}',
        '关联K-40000、S-20000',
        '仅增强稿可见；非独立成交记录',
        '口述于研读《聪明的投资者》第121页时略过国债内容；课件显示道琼斯工业平均指数中投资价格与利润之比最低的6种或10种股票假设。{E0}{E1}',
        '记录研读《聪明的投资者》关于低价股策略的讨论，并指出A股不能单纯买低价股。{E0}{E1}',
        '未提供可核验的完整交割单与逐笔成交流水。{E0}{E1}',
        '不与第二源内容跨源拼接。{E0}{E1}',
        '口述与课件OCR证据{E0}{E1}'
    ),
    (
        '2024年11月初市场情绪全面退潮与核心风向标个股观察复盘',
        'SRC-000244',
        '2024年11月初（源文第368章、第378章等上下文）。{E2}{E3}',
        '四川长虹、海能达、常山北明、欧菲光等情绪风向标（源文正文）。{E2}{E3}',
        '短线实盘日记与情绪复盘，非独立回测或交易流水。{E2}{E3}',
        '关联K-40001、S-20001',
        '仅增强稿可见；非独立成交记录',
        '作者提示情绪全面退潮期务必管住手控制仓位，并明确将四川长虹、海能达、常山北明、欧菲光等作为情绪风向标列入自选。{E2}{E3}',
        '记录退潮期管住手控制仓位的原则，以及通过核心风向标观察市场情绪修复与退潮节奏。{E2}{E3}',
        '未提供可核验的完整逐笔交易流水。{E2}{E3}',
        '不与第一源内容跨源拼接。{E2}{E3}',
        '正文原话证据{E2}{E3}'
    )
)

DOUBTS = [
    '主代理已通读SRC-002732 L1-2836与SRC-000244 L1-1238全文。',
    '严格遵守单段引文≤300字且禁止截断/省略号规则。'
]

RELATIONS = [
    'SRC-002732为读书_11聪明的投资者解盘，SRC-000244为妖股成妖之路_22短线日记；各卡严守单源边界。'
]

def build(r, e_start, k_start, s_start, c_start):
    import hashlib
    assert tuple(r.group['picks']) == SOURCE_IDS
    st = {'E': e_start, 'K': k_start, 'S': s_start, 'C': c_start}
    ids = {x: [x + '-' + str(st[x] + i) for i in range(COUNTS[x])] for x in st}
    for x in st:
        assert st[x] == r.group[x.lower() + 'min']
    o = {}
    for sid in SOURCE_IDS:
        p, t = r.original[sid]
        m = R[sid]
        assert len(t) == m['chars'] and len(p.read_bytes()) == m['raw_bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest() == m['raw_sha256']
        assert hashlib.sha256(t.encode()).hexdigest() == m['text_sha256']
        o[sid] = (p, t.splitlines())
        r.layers[sid] = '仅增强稿可见'
        r.stances[sid] = '课程讲述者采纳'
    for i, (eid, (sid, ln, e)) in enumerate(zip(ids['E'], E)):
        p, ls = o[sid]
        assert ls[ln - 1] == e
        fr, col = L[i]
        r.e(int(eid[2:]), sid, e, line_number=ln)
        r.evidence[eid][2] = p.name + '｜' + fr + '｜' + col + '｜L' + str(ln)
    def q(v):
        if isinstance(v, str):
            for i, e in enumerate(ids['E']):
                v = v.replace('{E' + str(i) + '}', '[' + e + ']')
            for typ in 'KSC':
                for i, c in enumerate(ids[typ]):
                    v = v.replace(typ + str(i), c)
            return v
        if isinstance(v, dict):
            return {k: q(x) for k, x in v.items()}
        if isinstance(v, list):
            return [q(x) for x in v]
        if isinstance(v, tuple):
            return tuple(q(x) for x in v)
        return v
    for cid, a in zip(ids['K'], K):
        r.k(cid, *q(a))
    for cid, a in zip(ids['S'], S):
        r.s(cid, *q(a), fields='- 性质：' + a[2] + '\n- 规则版本：仅限本课证据，不跨课拼接\n- 完整度分级：观察框架；未明环节留缺\n- 效果证据：课堂复盘，未有独立订单或回测\n')
    for cid, a in zip(ids['C'], C):
        r.c(cid, *q(a))
    for e in ids['E']:
        uses = [cid for cid, sid, card in r.cards[-6:] if '[' + e + ']' in card and sid == r.evidence[e][1]]
        assert uses
        r.evidence[e][4] = '；'.join(uses)
    return {
        'counts': COUNTS,
        'new_counts': NEW_COUNTS,
        'supplement_counts': SUPPLEMENT_COUNTS,
        'total_cards': 6,
        'total_evidence': 4,
        'doubts': DOUBTS,
        'relations': q(RELATIONS),
        'reading': R
    }
