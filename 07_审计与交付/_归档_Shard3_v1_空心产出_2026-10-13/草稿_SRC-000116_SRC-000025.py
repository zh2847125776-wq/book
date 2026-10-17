# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-000116', 'SRC-000025')
COUNTS = {'K': 2, 'S': 2, 'C': 2, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-000116', 'SRC-000116_(增强版)专题_交易思变_均线滞后性的分类与对策.md', 35, [11, 27]),
    ('SRC-000025', 'SRC-000025_(增强版)P2_乖离率.md', 1246, [138, 143])
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
        '均线滞后性分类与对策专题开场及系统课程回顾记录',
        'SRC-000116',
        '源文口述记录2024年7月14日周末开场讲解均线滞后性问题，回顾系统课程第四章关于技术指标缺点的介绍，并提出讲解不同种类滞后性的要命点及对策。{E0}{E1}',
        '仅记录≤300字完整原文字面的均线滞后性专题引入与学习脉络，不采信Vision推断，不把未展开的后续对策假定为已明确规则。{E0}{E1}',
        [
            '口述记录2024年7月14日开场提出讲均线滞后性并回顾系统课程第四章。{E0}',
            '口述记录专门把均线滞后性摘出来讲解不同种类要命点及相应对策。{E1}'
        ],
        '短视频开场仅1分钟，后续展开对策规则原稿未包含，未披露内容一律留缺。{E0}{E1}',
        '关联S0与C0；不跨源混用。{E0}{E1}',
        '见S0与C0；均线滞后性分类与对策开场。{E0}{E1}'
    ),
    (
        '乖离率基于20日线测距定义与正乖离率判定标准观察',
        'SRC-000025',
        '源文课件OCR明确记录乖离率定义为“> 表述股价距离20日线的距离远近的测距数值”，以及“> 股价大于20日线且20日线向上叫做正乖离率”。{E2}{E3}',
        '仅记录≤300字完整原文字面的20日线乖离率测距定义与正乖离率方向条件，不采信Vision推断，不补造交易流水。{E2}{E3}',
        [
            '课件OCR显示“> 表述股价距离20日线的距离远近的测距数值”。{E2}',
            '课件OCR显示“> 股价大于20日线且20日线向上叫做正乖离率”。{E3}'
        ],
        '本源无语音转录文字，全部指标定义严格以课件OCR字面为界，不作衍生推断。{E2}{E3}',
        '关联S1与C1；不跨源混用。{E2}{E3}',
        '见S1与C1；20日线乖离率与正乖离率定义。{E2}{E3}'
    )
)

S = (
    (
        '结合系统课程第四章审视均线滞后性缺陷与分类应对方法',
        'SRC-000116',
        '在研究均线交易体系并排查均线滞后性导致的亏损风险时使用。{E0}{E1}',
        '结合系统课程第四章关于技术分析缺点的总结，识别不同种类均线滞后性的致命点，并匹配相应对策加以解决。{E0}{E1}',
        {
            '环境过滤': ('均线交易策略评估与优化环境', '方法研究', '{E0}', '研究环境'),
            '形态或指标形成': ('识别均线系统在不同行情中的滞后性表现', '均线滞后', '{E0}{E1}', '滞后识别'),
            '确认': ('区分不同种类滞后性的要命点', '分类确认', '{E1}', '问题确认'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('在交易复盘中跟踪均线滞后性的影响与对策效果', '复盘跟踪', '{E0}{E1}', '对策跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '建立均线滞后性分类应对意识，具体对策参数原稿未展开留缺。{E0}{E1}',
        '同源K0与C0。{E0}{E1}',
        '短视频开场证据有限，未披露环节一律留缺。{E0}{E1}'
    ),
    (
        '基于20日均线方向与股价距离判定正乖离率的方法',
        'SRC-000025',
        '在日线级别观察股价与20日均线空间偏离程度时使用。{E2}{E3}',
        '以股价距离20日线的远近作为乖离率测距基准；当股价大于20日线且20日线方向向上时判定为正乖离率。{E2}{E3}',
        {
            '环境过滤': ('日线级别调取20日均线观察趋势方向', '日线', '{E2}{E3}', '20日线环境'),
            '形态或指标形成': ('测算股价距离20日线的远近测距数值', '距离测算', '{E2}', '乖离测距'),
            '确认': ('确认股价大于20日线且20日线方向向上，确立正乖离率状态', '方向与位置确认', '{E3}', '正乖离确认'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('在20日线向上条件下跟踪股价与20日线的偏离程度', '偏离跟踪', '{E2}{E3}', '正乖离跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('若20日线未向上或股价未在20日线之上则不构成正乖离率', '条件不符', '{E3}', '非正乖离')
        },
        '严格以20日线位置及方向判定正乖离率，未披露买卖数值留缺。{E2}{E3}',
        '同源K1与C1。{E2}{E3}',
        'Vision推断不作规则，原稿无语音转录，未明环节留缺。{E2}{E3}'
    )
)

C = (
    (
        '2024年7月14日均线滞后性分类与对策专题开场复盘',
        'SRC-000116',
        '2024年7月14日周末（源文口述）。{E0}',
        '均线滞后性分类与对策专题（源文口述）。{E0}{E1}',
        '课堂教学引入复盘，非独立回测或交易流水。{E0}{E1}',
        '关联K-40056、S-20035',
        '仅增强稿可见；非独立成交记录',
        '口述记录2024年7月14日开场回顾系统课第四章，提出专门讲解均线滞后性的分类要命点及对策。{E0}{E1}',
        '记录均线滞后性专题课程的引入与问题界定。{E0}{E1}',
        '视频时长仅1分钟，未提供后续完整交易结果。{E0}{E1}',
        '不与第二源内容跨源拼接。{E0}{E1}',
        '口述原文字面证据{E0}{E1}'
    ),
    (
        '20日线乖离率测距定义与正乖离率判定课件教学复盘',
        'SRC-000025',
        '源文课件讲解时间（指标基础教学复盘）。{E2}{E3}',
        '乖离率BIAS与20日均线（源文课件OCR）。{E2}{E3}',
        '课件指标定义教学复盘，非独立回测或交易流水。{E2}{E3}',
        '关联K-40057、S-20036',
        '仅增强稿可见；非独立成交记录',
        '课件明确定义乖离率为表述股价距离20日线远近的测距数值，股价大于20日线且20日线向上叫做正乖离率。{E2}{E3}',
        '记录体系内乖离率唯一定义与正乖离率严格判定条件。{E2}{E3}',
        '未提供可核验的逐笔交易订单与盈亏统计流水。{E2}{E3}',
        '不与第一源内容跨源拼接。{E2}{E3}',
        '课件原文字面证据{E2}{E3}'
    )
)

DOUBTS = [
    '主代理已通读SRC-000116 L1-35与SRC-000025 L1-1246全文。',
    'SRC-000116仅35行（1分钟开场），原稿后续内容缺失；未披露规则严格留缺。',
    'SRC-000025仅有课件OCR与Vision，无语音转录，严格以OCR字面为据，不采信Vision推断。',
    '严格遵守单段引文≤300字且禁止截断/省略号规则。'
]

RELATIONS = [
    'SRC-000116为均线滞后性专题开场，SRC-000025为乖离率指标教学课件；各卡严守单源边界。'
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
