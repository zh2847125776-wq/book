# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-000121', 'SRC-000030')
COUNTS = {'K': 2, 'S': 2, 'C': 2, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-000121', 'SRC-000121_(增强版)专题_交易思变_定量化确定波段高低点.md', 19, [11]),
    ('SRC-000030', 'SRC-000030_(增强版)P2_太极.md', 1147, [640, 890, 922])
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
        '定量化确定波段高点与低点专题缘起观察',
        'SRC-000121',
        '源文口述记录2024年4月10日18:11利用晚饭前时间撰写PPT讲解如何确定波段高点和低点，指出原本觉得不需要专门讲，但通过长期学习、教学和与同学沟通发现仍有必要专门梳理。{E0}',
        '仅记录≤300字完整原文字面的确定波段高点和低点专题缘起，不采信Vision推断，不把未展开的后续PPT正文假定为已明确规则。{E0}',
        [
            '口述记录2024年4月10日18:11写小PPT讲解如何确定波段高点和低点的教学缘起。{E0}'
        ],
        '短视频仅1分钟开场，后续具体定量化标准原稿未包含，未披露内容一律留缺。{E0}',
        '关联S0与C0；不跨源混用。{E0}',
        '见S0与C0；确定波段高点和低点专题开场观察。{E0}'
    ),
    (
        '太极四象真假突破辨析与建仓失败抽身离场及按表操课观察',
        'SRC-000030',
        '源文课件OCR明确记录“> 四象乃是多空趋势明朗之后的真假之别”、“> 抽身离场，建仓失败，股价再下台阶”，并提出执行准则“> 按表操课，有理有据，理智分析，果断决策”。{E1}{E2}{E3}',
        '仅记录≤300字完整原文字面的四象多空趋势真假之别、建仓失败抽身离场及按表操课果断决策规则，不采信Vision推断，不补造交易流水。{E1}{E2}{E3}',
        [
            '课件OCR显示“> 四象乃是多空趋势明朗之后的真假之别”。{E1}',
            '课件OCR显示“> 抽身离场，建仓失败，股价再下台阶”。{E2}',
            '课件OCR显示“> 按表操课，有理有据，理智分析，果断决策”。{E3}'
        ],
        '本源无语音转录文字，全部条件严格以课件OCR字面为界，不作衍生推断。{E1}{E2}{E3}',
        '关联S1与C1；不跨源混用。{E1}{E2}{E3}',
        '见S1与C1；太极四象真假之别与按表操课观察。{E1}{E2}{E3}'
    )
)

S = (
    (
        '针对教学沟通痛点开展波段高点与低点认定的梳理方法',
        'SRC-000121',
        '在波段交易教学与实盘沟通中梳理波段高点与低点判定标准时使用。{E0}',
        '针对日常学习、教学及学员沟通中暴露出的波段高低点认知模糊问题，专门编写课件明确如何确定波段高点和低点。{E0}',
        {
            '环境过滤': ('波段交易教学与学员沟通反馈环境', '全周期', '{E0}', '教学反馈环境'),
            '形态或指标形成': ('围绕如何确定波段高点和低点建立统一认知框架', '波段高低点', '{E0}', '高低点界定'),
            '确认': ('通过教学与沟通确认专门讲解波段高低点认定的必要性', '需求确认', '{E0}', '教学痛点确认'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('跟踪波段高点和低点的形成', '波段跟踪', '{E0}', '高低点跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '明确波段高低点定量化界定的教学目标，未展开的具体量化参数留缺。{E0}',
        '同源K0与C0。{E0}',
        '短视频开场证据有限，未披露环节一律留缺。{E0}'
    ),
    (
        '基于太极四象辨别多空突破真假并按表操课果断离场的方法',
        'SRC-000030',
        '在股票脱离盘整选择多空方向后辨别突破真假及应对建仓失败时使用。{E1}{E2}{E3}',
        '遵循“按表操课，有理有据，理智分析，果断决策”原则，在多空趋势初显时运用“四象”思维甄别突破真假；一旦判定建仓失败、股价再下台阶，立即抽身离场。{E1}{E2}{E3}',
        {
            '环境过滤': ('股票由混沌盘整转向多空方向选择与真假突破分化环境', '日线/多周期', '{E1}{E3}', '趋势明朗与真假分化'),
            '形态或指标形成': ('多空趋势初步明朗后演化出真突破或假突破（四象真假之别）', '趋势与突破', '{E1}', '四象真假演化'),
            '确认': ('理智分析确认突破真假，鉴别是否发生建仓失败、股价再下台阶', '真假确认', '{E1}{E2}{E3}', '有理有据确认'),
            '入场': ('按表操课、有理有据地在趋势确认时执行决策', '按表入场', '{E3}', '按表操课决策'),
            '初始止损': ('若判定建仓失败、股价再下台阶，果断执行抽身离场止损', '失败离场止损', '{E2}{E3}', '抽身离场'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('持仓期间按表操课跟踪多空趋势持续性', '按表跟踪', '{E1}{E3}', '理智跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('当出现建仓失败、股价再下台阶时立即抽身离场退出', '抽身退出', '{E2}{E3}', '果断抽身离场'),
            '失效与放弃': ('突破被证伪、建仓失败下台阶时果断放弃原有看多假设', '建仓失败放弃', '{E1}{E2}', '证伪放弃')
        },
        '以四象辨别多空真假，建仓失败下台阶即抽身离场，全程按表操课。{E1}{E2}{E3}',
        '同源K1与C1。{E1}{E2}{E3}',
        'Vision推断不作规则，原稿无语音转录，未明环节留缺。{E1}{E2}{E3}'
    )
)

C = (
    (
        '2024年4月10日定量化确定波段高低点专题开场复盘',
        'SRC-000121',
        '2024年4月10日18:11（源文口述）。{E0}',
        '波段高点与波段低点判定（源文口述）。{E0}',
        '课堂专题引入复盘，非独立回测或交易流水。{E0}',
        '关联K-40176、S-20110',
        '仅增强稿可见；非独立成交记录',
        '口述记录2024年4月10日6点11分利用晚饭前时间写PPT讲解如何确定波段高点和低点，源于长期学习、教学和沟通中的实际需要。{E0}',
        '记录定量化确定波段高低点专题的背景与教学初衷。{E0}',
        '视频仅1分钟开场，未提供后续完整课件参数与交易流水。{E0}',
        '不与第二源内容跨源拼接。{E0}',
        '口述原文字面证据{E0}'
    ),
    (
        '太极之道四象真假之别与建仓失败抽身离场课件教学复盘',
        'SRC-000030',
        '源文课件讲解时间（太极之道选股操作逻辑教学复盘）。{E1}{E2}{E3}',
        '股票太极、两仪、四象、八卦选股操作逻辑体系（源文课件OCR）。{E1}{E2}{E3}',
        '课件交易哲学与操作逻辑教学复盘，非独立回测或交易流水。{E1}{E2}{E3}',
        '关联K-40177、S-20111',
        '仅增强稿可见；非独立成交记录',
        '课件思维导图阐述四象乃是多空趋势明朗之后的真假之别，指出建仓失败、股价再下台阶时需抽身离场，并总结按表操课、有理有据、理智分析、果断决策的准则。{E1}{E2}{E3}',
        '记录将传统文化太极四象映射为股市趋势真假辨析与按表操课果断离场的教学框架。{E1}{E2}{E3}',
        '未提供可核验的逐笔交易订单与盈亏统计流水。{E1}{E2}{E3}',
        '不与第一源内容跨源拼接。{E1}{E2}{E3}',
        '课件OCR字面证据{E1}{E2}{E3}'
    )
)

DOUBTS = [
    '主代理已通读SRC-000121 L1-19与SRC-000030 L1-1147全文。',
    'SRC-000121仅19行（1分钟开场），严格依据≤300字完整语音行抽取。',
    'SRC-000030仅有课件OCR与Vision，无语音转录，严格以OCR字面为据，不采信Vision推断。',
    '严格遵守单段≤300字且不截断无省略号规则。'
]

RELATIONS = [
    'SRC-000121为定量化确定波段高低点专题开场，SRC-000030为太极四象真假辨析与按表操课课件；各卡严守单源边界。'
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
