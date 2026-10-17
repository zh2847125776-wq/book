# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-000115', 'SRC-000024')
COUNTS = {'K': 2, 'S': 2, 'C': 2, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-000115', 'SRC-000115_(增强版)专题_交易思变_均线可靠性的一种定量化衡量标准.md', 35, [11, 30]),
    ('SRC-000024', 'SRC-000024_(增强版)P2_w底部形态.md', 3245, [26, 32])
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
        '均线系统入门价值与定量化可靠性衡量标准专题开场记录',
        'SRC-000115',
        '源文口述记录2024年6月28日周末开场讲解均线可靠性的一种定量化衡量标准，指出均线系统对新手直观入门量化分析的价值；课件OCR显示“> 均线可尽性的一种定量化衡量标准”。{E0}{E1}',
        '仅记录≤300字完整原文字面的均线定量化衡量标准引入与直观入门概念，不采信Vision推断，不把未展开的后续推导假定为已明确规则。{E0}{E1}',
        [
            '口述记录2024年6月28日晚上开场讲均线可靠性的一种定量化衡量标准。{E0}',
            '课件OCR显示“> 均线可尽性的一种定量化衡量标准”。{E1}'
        ],
        '短视频开场仅1分钟，后续展开交易规则原稿未包含，未披露内容一律留缺。{E0}{E1}',
        '关联S0与C0；不跨源混用。{E0}{E1}',
        '见S0与C0；均线可靠性定量化衡量标准开场。{E0}{E1}'
    ),
    (
        'W底形态颈线定义与最低点至颈线距离形态深度H观察',
        'SRC-000024',
        '源文课件OCR明确记录“> 被突破的下降常态前高称为：颈线”，以及“> 由最低点到颈线的距离称为：形态深度或差距H”。{E2}{E3}',
        '仅记录≤300字完整原文字面的W底部形态颈线术语定义与形态深度H几何测距要素，不采信Vision推断，不补造交易流水。{E2}{E3}',
        [
            '课件OCR显示“> 被突破的下降常态前高称为：颈线”。{E2}',
            '课件OCR显示“> 由最低点到颈线的距离称为：形态深度或差距H”。{E3}'
        ],
        '本源无语音转录文字，全部形态定义严格以课件OCR字面为界，不作衍生推断。{E2}{E3}',
        '关联S1与C1；不跨源混用。{E2}{E3}',
        '见S1与C1；W底形态颈线与深度H定义。{E2}{E3}'
    )
)

S = (
    (
        '均线系统直观量化分析学习与可靠性评估方法',
        'SRC-000115',
        '在初学者接触量化技术分析并评估均线系统可靠性时使用。{E0}{E1}',
        '通过均线系统直观入门量化分析，同时建立对均线系统可靠性的定量化衡量意识，防范指标盲信。{E0}{E1}',
        {
            '环境过滤': ('初学者量化分析学习环境', '基础学习', '{E0}', '学习环境'),
            '形态或指标形成': ('调取均线系统观察最简单最直观走势', '均线系统', '{E0}{E1}', '均线引入'),
            '确认': ('确认掌握均线可靠性的定量化衡量意识', '概念确认', '{E0}{E1}', '可靠性确认'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('在模拟学习中持续观察均线有效性表现', '跟踪', '{E0}', '效果跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '建立均线可靠性定量认知，具体量化公式原稿未展开留缺。{E0}{E1}',
        '同源K0与C0。{E0}{E1}',
        '短视频开场证据有限，未披露环节一律留缺。{E0}{E1}'
    ),
    (
        'W底形态识别与基于颈线突破及形态深度H测距的方法',
        'SRC-000024',
        '在图表走势形成两低点并挑战下降常态前高时使用。{E2}{E3}',
        '识别被突破的下降常态前高为颈线，测算由最低点到颈线的距离为形态深度H，依据颈线突破进行形态确立与空间测算。{E2}{E3}',
        {
            '环境过滤': ('走势经历下降常态并出现筑底走升迹象', '日线/各级别', '{E2}', '筑底环境'),
            '形态或指标形成': ('出现双底形态并挑战下降常态前高', '形态结构', '{E2}{E3}', '双底形成'),
            '确认': ('价格有效突破下降常态前高颈线', '颈线确认', '{E2}', '突破颈线'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('以形态深度或差距H垂直测距跟踪后市目标空间', '目标跟踪', '{E3}', '深度测距'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '以颈线确立形态边界，以深度H测算空间，未披露买卖数值留缺。{E2}{E3}',
        '同源K1与C1。{E2}{E3}',
        'Vision推断不作规则，原稿无语音转录，未明环节留缺。{E2}{E3}'
    )
)

C = (
    (
        '2024年6月28日均线可靠性定量化衡量标准专题开场复盘',
        'SRC-000115',
        '2024年6月28日晚上9点（源文口述）。{E0}',
        '均线可靠性定量化衡量标准专题（源文课件与口述）。{E0}{E1}',
        '课堂教学引入复盘，非独立回测或交易流水。{E0}{E1}',
        '关联K-40032、S-20020',
        '仅增强稿可见；非独立成交记录',
        '口述记录2024年6月28日晚开场引入均线系统入门与可靠性定量化衡量标准；课件显示“> 均线可尽性的一种定量化衡量标准”。{E0}{E1}',
        '记录均线可靠性定量化概念的引入过程。{E0}{E1}',
        '视频时长仅1分钟，未提供后续完整交易结果。{E0}{E1}',
        '不与第二源内容跨源拼接。{E0}{E1}',
        '口述与课件OCR证据{E0}{E1}'
    ),
    (
        'W底形态颈线突破与形态深度H空间测距教学复盘',
        'SRC-000024',
        '源文课件讲解时间（历史经典形态复盘）。{E2}{E3}',
        'W底形态与下降常态前高颈线（源文课件OCR）。{E2}{E3}',
        '课件形态教学复盘，非独立回测或交易流水。{E2}{E3}',
        '关联K-40033、S-20021',
        '仅增强稿可见；非独立成交记录',
        '课件明确定义被突破的下降常态前高为颈线，最低点到颈线的距离为形态深度或差距H。{E2}{E3}',
        '记录W底形态的核心定义要素与几何空间测距依据。{E2}{E3}',
        '未提供可核验的逐笔交易订单与盈亏统计流水。{E2}{E3}',
        '不与第一源内容跨源拼接。{E2}{E3}',
        '课件原文字面证据{E2}{E3}'
    )
)

DOUBTS = [
    '主代理已通读SRC-000115 L1-35与SRC-000024 L1-3245全文。',
    'SRC-000115仅35行（1分钟开场），原稿后续内容缺失；未披露规则严格留缺。',
    'SRC-000024仅有课件OCR与Vision，无语音转录，严格以OCR字面为据，不采信Vision推断。',
    '严格遵守单段引文≤300字且禁止截断/省略号规则。'
]

RELATIONS = [
    'SRC-000115为均线定量化标准专题开场，SRC-000024为W底部形态教学课件；各卡严守单源边界。'
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
