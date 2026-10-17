# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-002734', 'SRC-000246')
COUNTS = {'K': 2, 'S': 2, 'C': 2, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-002734', 'SRC-002734_(增强版)读书_12聪明的投资者.md', 1844, [11, 84]),
    ('SRC-000246', 'SRC-000246_(增强版)妖股成妖之路_24.md', 1366, [637, 645])
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
        '聪明的投资者积极型证券组合策略研读与标的选择审视',
        'SRC-002734',
        '源文口述记录研读《聪明的投资者》渐入佳境，针对具体投资标的与组合选择提出必须甄别其与当前实际情况的契合度；课件OCR显示“> 积极型投资者的证券组合策略”。{E0}{E1}',
        '仅记录≤300字完整原文字面的积极型投资策略研读口述与课件小节标题，不采信Vision推断，不把未确认的个股买卖当作确定规则。{E0}{E1}',
        [
            '口述记录研读《聪明的投资者》渐入佳境并开始讨论组合具体标的选择。{E0}',
            '课件思维导图OCR显示“> 积极型投资者的证券组合策略”。{E1}'
        ],
        '本源为读书教学视频，其余超长口述行按禁截断铁律不予入证。{E0}{E1}',
        '关联S0与C0；不跨源混用。{E0}{E1}',
        '见S0与C0；积极型证券组合策略研读。{E0}{E1}'
    ),
    (
        '短线操作不干杂毛与市场龙头不做T持有至情绪见顶规则观察',
        'SRC-000246',
        '源文记录操作原则“不干杂毛，做龙头或者潜在龙头，没地位不想做”；对于龙头操作明确指出“做市场龙头时，一般不做T，持有到情绪见顶或预计停牌才走”。{E2}{E3}',
        '仅记录≤300字完整原文字面的短线聚焦龙头与不做T持有规则，不凭空衍生未披露的具体价位参数。{E2}{E3}',
        [
            '原文明确规定“做市场龙头时，一般不做T，持有到情绪见顶或预计停牌才走”。{E2}',
            '原文明确规定“不干杂毛，做龙头或者潜在龙头，没地位不想做”。{E3}'
        ],
        '仅限短线短文投资心得记录，不跨接其他来源。{E2}{E3}',
        '关联S1与C1；不跨源混用。{E2}{E3}',
        '见S1与C1；聚焦龙头与不做T规则观察。{E2}{E3}'
    )
)

S = (
    (
        '积极型投资者证券组合标的审视与策略研读方法',
        'SRC-002734',
        '在研读价值投资经典并构建积极型证券组合标的时使用。{E0}{E1}',
        '在研读《聪明的投资者》积极型组合策略时，审视经典书本标的选择与当前市场环境的差异，理性评估标的适用性。{E0}{E1}',
        {
            '环境过滤': ('研读积极型投资者证券组合策略背景', '组合构建', '{E0}{E1}', '研读环境'),
            '形态或指标形成': ('识别课件积极型投资组合策略章节要点', '策略结构', '{E1}', '章节结构'),
            '确认': ('审视所选标的是否适合当前实际市场特征', '适用性核验', '{E0}', '标的甄别'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('在组合跟踪中持续甄别标的质地与契合度', '组合跟踪', '{E0}', '持仓审视'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '立足书本策略审视标的适用性，未披露交易数值留缺。{E0}{E1}',
        '同源K0与C0。{E0}{E1}',
        '超长口述行不截断入证，未明环节留缺。{E0}{E1}'
    ),
    (
        '短线聚焦市场龙头与全程持仓不做T交易方法',
        'SRC-000246',
        '在短线超短投机中选择标的并进行持仓管理时使用。{E2}{E3}',
        '坚决放弃杂毛品种，仅介入市场核心龙头或潜在龙头；在介入市场龙头后避免频繁做T，坚定持有至情绪见顶或预计停牌时退出。{E2}{E3}',
        {
            '环境过滤': ('短线题材投机与市场主线发酵环境', '短线/情绪周期', '{E2}{E3}', '短线投机环境'),
            '形态或指标形成': ('个股确认成为引领市场情绪的龙头或潜在龙头', '龙头形态', '{E3}', '龙头地位确认'),
            '确认': ('确认标的具备市场地位与板块带动效应，坚决放弃杂毛', '地位确认', '{E3}', '过滤杂毛'),
            '入场': ('确认龙头地位后介入建仓', '龙头介入', '{E3}', '龙头买入'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('聚焦核心龙头，集中兵力操作', '仓位聚焦', '{E3}', '资金聚焦'),
            '持仓与跟踪': ('全程坚定持股，一般不做T，避免频繁日内操作错失利润', '持股跟踪', '{E2}', '不做T持股'),
            '加减仓': ('不进行盘中频繁做T', '加减仓禁忌', '{E2}', '禁止做T'),
            '止盈与退出': ('持有到情绪见顶或预计停牌才坚决离场', '退出时机', '{E2}', '情绪见顶退出'),
            '失效与放弃': ('非龙头或缺乏地位的杂毛品种坚决放弃不参与', '纪律放弃', '{E3}', '放弃杂毛')
        },
        '严格执行龙头不做T与持有至见顶的超短纪律，未披露数值留缺。{E2}{E3}',
        '同源K1与C1。{E2}{E3}',
        '正文原话字面支持，未明细节留缺。{E2}{E3}'
    )
)

C = (
    (
        '《聪明的投资者》积极型投资组合策略研读复盘',
        'SRC-002734',
        '课堂研读录制时间（源文口述）。{E0}',
        '积极型证券组合与投资标的（源文课件与口述）。{E0}{E1}',
        '读书思考与组合策略研读复盘，非独立回测或交易流水。{E0}{E1}',
        '关联K-40048、S-20030',
        '仅增强稿可见；非独立成交记录',
        '口述记录研读《聪明的投资者》积极型组合策略并对具体标的选择进行理性审视；课件显示“> 积极型投资者的证券组合策略”。{E0}{E1}',
        '记录积极型投资者标的选择策略的思考过程。{E0}{E1}',
        '未提供单笔交易账单流水。{E0}{E1}',
        '不与第二源内容跨源拼接。{E0}{E1}',
        '口述与课件OCR证据{E0}{E1}'
    ),
    (
        '短线投机聚焦龙头与不做T持有至情绪见顶复盘',
        'SRC-000246',
        '2024年11月下旬（源文第434章等上下文）。{E2}{E3}',
        '短线市场核心龙头股（源文正文）。{E2}{E3}',
        '短线龙头实战心得复盘，非独立回测或交易流水。{E2}{E3}',
        '关联K-40049、S-20031',
        '仅增强稿可见；非独立成交记录',
        '作者明确总结龙头操作秘籍：不干杂毛只做龙头，做市场龙头一般不做T并持有至情绪见顶。{E2}{E3}',
        '记录短线极客交易中聚焦龙头与克服频繁做T弊端的原则。{E2}{E3}',
        '未提供可核验的逐笔交易凭据流水。{E2}{E3}',
        '不与第一源内容跨源拼接。{E2}{E3}',
        '正文原话字面证据{E2}{E3}'
    )
)

DOUBTS = [
    '主代理已通读SRC-002734 L1-1844与SRC-000246 L1-1366全文。',
    'SRC-002734口述语音行较长，严格采信符合≤300字完整行。',
    'SRC-000246明确记录了关于龙头股不做T与不干杂毛的规则原话，严格逐字摘录。',
    '严格遵守单段≤300字且不截断无省略号规则。'
]

RELATIONS = [
    'SRC-002734为经典价值投资研读，SRC-000246为超短龙头战法心得；各卡严守单源边界。'
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
