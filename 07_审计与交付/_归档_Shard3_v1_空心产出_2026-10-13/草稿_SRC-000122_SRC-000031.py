# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-000122', 'SRC-000031')
COUNTS = {'K': 2, 'S': 2, 'C': 2, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-000122', 'SRC-000122_(增强版)专题_交易思变_左侧交易与右侧交易的细节相对论.md', 46, [11]),
    ('SRC-000031', 'SRC-000031_(增强版)P2_扣抵1.md', 414, [102, 105, 123])
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
        '左侧交易与右侧交易细节专题单列讲解缘起观察',
        'SRC-000122',
        '源文口述记录抽时间专门讲解一个远够不上一节课的小知识点，指出原本认为通过系统课程学习（每个课程讲解中都多少有些涉及和带入）大家自然都能懂，但拿出来专门讲几分钟就能彻底讲清楚。{E0}',
        '仅记录≤300字完整原文字面的专题开场说明，不采信Vision推断，不把超过300字的第二段语音截断入证。{E0}',
        [
            '口述记录专门抽出几分钟讲解系统课程中散落涉及的小知识点的教学缘起。{E0}'
        ],
        '短视频仅1分钟开场，第二段语音（L30）总长335字符超过300字上限，按不截断铁律不予入证。{E0}',
        '关联S0与C0；不跨源混用。{E0}',
        '见S0与C0；左侧与右侧交易细节专题开场观察。{E0}'
    ),
    (
        'X日移动平均线扣抵计算原理与20日线核心作用观察',
        'SRC-000031',
        '源文课件OCR定义均线扣抵计算原理为“> X日移动平均线，就是计算从今天开始起过去X天的收盘价平均值。第二”“> 天则加上新一天的数值，去掉之前计算的最早一天，继续计算而得到”，并明确指出“> 20日线的核心作用无可替代”。{E1}{E2}{E3}',
        '仅记录≤300字完整原文字面的X日移动平均线递推去掉最早一天（扣抵）计算定义及20日线核心地位，不采信Vision推断，不补造交易流水。{E1}{E2}{E3}',
        [
            '课件OCR显示“> X日移动平均线，就是计算从今天开始起过去X天的收盘价平均值。第二”“> 天则加上新一天的数值，去掉之前计算的最早一天，继续计算而得到”。{E1}{E2}',
            '课件OCR显示“> 20日线的核心作用无可替代”。{E3}'
        ],
        '本源无语音转录文字，全部条件严格以课件OCR字面为界，不作衍生推断。{E1}{E2}{E3}',
        '关联S1与C1；不跨源混用。{E1}{E2}{E3}',
        '见S1与C1；均线扣抵计算原理与20日线核心作用。{E1}{E2}{E3}'
    )
)

S = (
    (
        '将散落于系统课程中的基础知识点单列微课复用的教学方法',
        'SRC-000122',
        '在系统交易课程之外针对高频基础概念疑问进行专项梳理时使用。{E0}',
        '将原本散落在各个系统课程讲解中顺带提及、远够不上一整节课的小知识点单独抽出来，用几分钟专题视频讲透。{E0}',
        {
            '环境过滤': ('系统课程学习与日常基础概念答疑环境', '教学梳理', '{E0}', '教学环境'),
            '形态或指标形成': ('识别在各课程中均有涉及但未单列成课的小知识点', '知识点提炼', '{E0}', '概念提炼'),
            '确认': ('确认有必要单独拿出来用几分钟讲清楚', '必要性确认', '{E0}', '单列确认'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('结合系统课程整体学习持续深化理解', '系统学习', '{E0}', '课程跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '反映专题微课提炼基础概念的教学逻辑，具体交易参数留缺。{E0}',
        '同源K0与C0。{E0}',
        '短视频开场证据有限且L30超300字禁截断不入证，未披露环节留缺。{E0}'
    ),
    (
        '基于X日均线扣抵（加新日去最早日）原理与20日线核心地位的分析方法',
        'SRC-000031',
        '在运用均线系统与扣抵原理推演均线方向及确立核心均线时使用。{E1}{E2}{E3}',
        '把握X日移动平均线“从今天起算过去X天收盘价均值，第二天加上新一天数值、去掉之前计算的最早一天”的扣抵递推机制，并在均线系统中坚守“20日线的核心作用无可替代”的核心基准。{E1}{E2}{E3}',
        {
            '环境过滤': ('均线系统设置与扣抵方向预判环境', '日线/多周期', '{E1}{E2}{E3}', '均线系统环境'),
            '形态或指标形成': ('计算过去X天收盘价均值，次日加上新一天数值并去掉最早一天数值（扣抵）', 'X日均线与20日线', '{E1}{E2}{E3}', '扣抵递推计算'),
            '确认': ('确认20日线在均线系统中无可替代的核心作用，对比新一日收盘价与被去掉的最早一天收盘价', '扣抵与20日线确认', '{E1}{E2}{E3}', '核心均线与扣抵确认'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('以20日线为核心，每日跟踪加上新一天数值、去掉最早一天数值后的均线演化', '20日线扣抵跟踪', '{E1}{E2}{E3}', '扣抵动态跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '揭示均线扣抵“加新日、去最早日”的数学本质与20日线的核心地位，未披露具体买卖点位留缺。{E1}{E2}{E3}',
        '同源K1与C1。{E1}{E2}{E3}',
        'Vision推断不作规则，原稿无语音转录，未明环节留缺。{E1}{E2}{E3}'
    )
)

C = (
    (
        '左侧交易与右侧交易的细节相对论专题开场复盘',
        'SRC-000122',
        '源文录制时间（专题微课开场）。{E0}',
        '左侧交易与右侧交易基础概念（源文题名与口述）。{E0}',
        '课堂专题引入复盘，非独立回测或交易流水。{E0}',
        '关联K-40200、S-20125',
        '仅增强稿可见；非独立成交记录',
        '口述记录专门抽出几分钟讲解远够不上一节课、但在系统课程讲解中均有涉及的小知识点。{E0}',
        '记录专题微课针对系统课程散落知识点进行单列讲解的缘起。{E0}',
        '视频仅1分钟开场，未提供后续完整交易流水。{E0}',
        '不与第二源内容跨源拼接。{E0}',
        '口述原文字面证据{E0}'
    ),
    (
        'X日均线扣抵定义（加新日去最早日）与20日线核心作用课件教学复盘',
        'SRC-000031',
        '源文课件讲解时间（扣抵1教学复盘）。{E1}{E2}{E3}',
        'X日移动平均线与20日线（源文课件OCR）。{E1}{E2}{E3}',
        '课件均线扣抵基础理论教学复盘，非独立回测或交易流水。{E1}{E2}{E3}',
        '关联K-40201、S-20126',
        '仅增强稿可见；非独立成交记录',
        '课件思维导图界定X日移动平均线为计算从今天起过去X天的收盘价平均值，第二天加上新一天的数值、去掉之前计算的最早一天继续计算，并强调20日线的核心作用无可替代。{E1}{E2}{E3}',
        '记录均线扣抵“加新去旧”底层计算公式与20日线核心地位的教学课件内容。{E1}{E2}{E3}',
        '未提供可核验的逐笔交易订单与盈亏统计流水。{E1}{E2}{E3}',
        '不与第一源内容跨源拼接。{E1}{E2}{E3}',
        '课件OCR字面证据{E1}{E2}{E3}'
    )
)

DOUBTS = [
    '主代理已通读SRC-000122 L1-46与SRC-000031 L1-414全文。',
    'SRC-000122仅46行（1分钟开场），L30语音行长335字符超过300字上限，严格按不截断铁律仅取L11（165字符）入证。',
    'SRC-000031仅有课件/画面OCR与Vision，无语音转录，严格以OCR字面为据，不采信Vision推断。',
    '严格遵守单段≤300字且不截断无省略号规则。'
]

RELATIONS = [
    'SRC-000122为左右侧交易细节专题开场，SRC-000031为均线扣抵定义与20日线核心地位教学课件；各卡严守单源边界。'
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
