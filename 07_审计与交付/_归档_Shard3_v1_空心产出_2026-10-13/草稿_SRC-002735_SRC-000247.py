# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-002735', 'SRC-000247')
COUNTS = {'K': 2, 'S': 2, 'C': 2, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-002735', 'SRC-002735_(增强版)读书_13.md', 253, [11, 251]),
    ('SRC-000247', 'SRC-000247_(增强版)妖股成妖之路_25.md', 1354, [1349, 1351])
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
        '反对主观直觉交易与只相信客观数字规则批判观察',
        'SRC-002735',
        '源文口述记录研读《股票大作手回忆录》第52页第6章《相信直觉，坚信自己是对的》时明确提出反对直觉交易，普通人没有直觉，只相信看到的客观数字而不相信大脑无来源判断，并强调极端不提倡靠直觉做空或交易。{E0}{E1}',
        '仅记录≤300字完整原文字面的反对直觉交易、只信客观数字以及区分正确交易与挣钱交易的观点，不采信Vision推断，不把超长语音转录截断入证。{E0}{E1}',
        [
            '口述记录反对相信直觉，强调只相信看到的数字，并且正确的交易不一定等于挣钱的交易。{E0}',
            '口述记录以茅台看空与联合太平洋3000股卖单故事为例，明确极端不提倡直觉交易。{E1}'
        ],
        '其余超300字口述行按无省略号不截断规则不入证，未明规则留缺。{E0}{E1}',
        '关联S0与C0；不跨源混用。{E0}{E1}',
        '见S0与C0；反对直觉交易与客观数字原则。{E0}{E1}'
    ),
    (
        '主升期贡献收益与退潮期确认空仓生存法则观察',
        'SRC-000247',
        '源文明确记录“拉长时间看，大部分收益来自于主升期，大部分回撤来自于退潮期”，并总结核心生存原则“如果确认退潮，最优的交易策略就是空仓”。{E2}{E3}',
        '仅记录≤300字完整原文字面的情绪周期盈亏来源结构与退潮期空仓应对规则，不凭空衍生未披露的具体量化参数。{E2}{E3}',
        [
            '原文明确规定“拉长时间看，大部分收益来自于主升期，大部分回撤来自于退潮期”。{E2}',
            '原文明确规定“如果确认退潮，最优的交易策略就是空仓”。{E3}'
        ],
        '仅限短线短文投资心得记录，不跨接其他来源。{E2}{E3}',
        '关联S1与C1；不跨源混用。{E2}{E3}',
        '见S1与C1；主升期获利与退潮期空仓法则。{E2}{E3}'
    )
)

S = (
    (
        '排斥主观直觉并以客观数字为依据的理性交易方法',
        'SRC-002735',
        '在交易决策中面临突发主观预感或研读历史直觉交易案例时使用。{E0}{E1}',
        '坚决摒弃无来源的大脑直觉判断，坚持只依据客观可见的数字与规则执行交易，不因个别违规盈利案例而模仿直觉交易。{E0}{E1}',
        {
            '环境过滤': ('日常交易决策与研读《回忆录》第6章直觉案例环境', '全周期', '{E0}{E1}', '决策环境'),
            '形态或指标形成': ('只认可在盘面上看到的客观数字与明确信号', '客观数字', '{E0}', '数字依据'),
            '确认': ('确认交易理由来自客观数字而非大脑无来源直觉', '依据确认', '{E0}', '排除直觉'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('理性区分“正确的交易”与“挣钱的交易”，不被偶然盈利误导', '认知跟踪', '{E0}{E1}', '纪律跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('凡属说不出客观原因的直觉冲动或盲目摸顶做空一律放弃', '纪律放弃', '{E0}{E1}', '放弃直觉单')
        },
        '以客观数字取代主观直觉，具体指标参数原稿未展开留缺。{E0}{E1}',
        '同源K0与C0。{E0}{E1}',
        '超长口述行不截断入证，未明环节留缺。{E0}{E1}'
    ),
    (
        '基于主升期与退潮期划分的周期择时与确认退潮空仓方法',
        'SRC-000247',
        '在短线题材情绪周期从主升期向退潮期演变时使用。{E2}{E3}',
        '聚焦主升期获取主要收益；一旦市场确认进入退潮期，停止折腾并坚决执行空仓策略以规避回撤。{E2}{E3}',
        {
            '环境过滤': ('划分市场情绪周期所处阶段（主升期或退潮期）', '情绪周期', '{E2}{E3}', '周期划分'),
            '形态或指标形成': ('观察高位股表现与市场整体赚钱效应判定是否退潮', '情绪信号', '{E2}{E3}', '退潮识别'),
            '确认': ('确认市场进入退潮期', '退潮确认', '{E3}', '周期确认'),
            '入场': ('在主升期积极参与，确认退潮期严禁开新仓', '周期择时', '{E2}{E3}', '择时纪律'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('确认退潮后将仓位降至零（空仓），守住主升期利润', '空仓风控', '{E2}{E3}', '空仓防守'),
            '持仓与跟踪': ('空仓期间耐心观望，不在退潮期折腾', '空仓等待', '{E2}{E3}', '观望跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('在退潮确认时清仓退出观望', '周期退出', '{E3}', '清仓空仓'),
            '失效与放弃': ('确认退潮期坚决放弃折腾与勉强出手', '放弃交易', '{E2}{E3}', '退潮空仓')
        },
        '严格执行确认退潮即空仓的生存铁律，未披露数值留缺。{E2}{E3}',
        '同源K1与C1。{E2}{E3}',
        '正文原话字面支持，未明细节留缺。{E2}{E3}'
    )
)

C = (
    (
        '《股票大作手回忆录》第6章直觉卖空联合太平洋批判复盘',
        'SRC-002735',
        '课堂读书录制时间（源文口述）。{E0}{E1}',
        '联合太平洋股票与贵州茅台参考提及（源文口述）。{E0}{E1}',
        '读书批判与交易哲学复盘，非独立回测或交易流水。{E0}{E1}',
        '关联K-40072、S-20045',
        '仅增强稿可见；非独立成交记录',
        '口述记录研读回忆录第52页第6章利弗莫尔凭直觉卖空3000股联合太平洋的故事，明确批判直觉交易并强调只信客观数字。{E0}{E1}',
        '记录对主观直觉交易的批判以及“正确交易不等于挣钱交易”的方法论辨析。{E0}{E1}',
        '未提供单笔交易账单流水。{E0}{E1}',
        '不与第二源内容跨源拼接。{E0}{E1}',
        '口述原文字面证据{E0}{E1}'
    ),
    (
        '短线情绪周期主升期获利与退潮期空仓防回撤复盘',
        'SRC-000247',
        '2024年11月底（源文第480章等上下文）。{E2}{E3}',
        '短线情绪周期与高位妖股（源文正文）。{E2}{E3}',
        '短线周期生存心得复盘，非独立回测或交易流水。{E2}{E3}',
        '关联K-40073、S-20046',
        '仅增强稿可见；非独立成交记录',
        '作者总结大部分收益来自主升期、大部分回撤来自退潮期，确认退潮最优策略就是空仓。{E2}{E3}',
        '记录短线交易中通过识别退潮期并执行空仓以锁住主升期利润的核心教训。{E2}{E3}',
        '未提供可核验的逐笔交易凭据流水。{E2}{E3}',
        '不与第一源内容跨源拼接。{E2}{E3}',
        '正文原话字面证据{E2}{E3}'
    )
)

DOUBTS = [
    '主代理已通读SRC-002735 L1-253与SRC-000247 L1-1354全文。',
    'SRC-002735仅L11与L251两条完整语音转录行≤300字，其余超长行严格按禁截断铁律不入证；老师明确批判原书直觉观点，立场已如实标定。',
    '严格遵守单段≤300字且不截断无省略号规则。'
]

RELATIONS = [
    'SRC-002735为回忆录第6章批判研读，SRC-000247为超短退潮期空仓法则；各卡严守单源边界。'
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
