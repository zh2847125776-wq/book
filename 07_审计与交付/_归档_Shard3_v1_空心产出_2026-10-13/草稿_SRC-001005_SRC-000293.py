# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-001005', 'SRC-000293')
COUNTS = {'K': 2, 'S': 2, 'C': 2, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-001005', 'SRC-001005_(增强版)股票_20200116-量化技术分析.md', 854, [11, 229]),
    ('SRC-000293', 'SRC-000293_(增强版)期货_期货投机分析20250605_精准识别当日偏见_订单胜率绝高.md', 3452, [166, 1452])
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
        '2020年1月16日大小盘分化与指数通用技术分析观察',
        'SRC-001005',
        '源文口述记录上证指数下跌0.52%而创业板指数上涨、小盘股更活跃的大小盘分化现象，指出主要观测目标为上证指数且创业板分析方法相同；行情OCR显示“> MA5: 3095.76↓ MA10: 3091.26)”。{E0}{E1}',
        '仅记录≤300字完整原文字面的大小盘分化现象、跨指数分析方法通用性与短期均线读数，不采信Vision推断，不把未确认的后续走势当作确定规则。{E0}{E1}',
        [
            '口述记录上证指数下跌0.52%、创业板指数上涨的小盘股活跃状态，明确不同指数技术分析方法相同。{E0}',
            '行情OCR显示“> MA5: 3095.76↓ MA10: 3091.26)”。{E1}'
        ],
        '本源为大盘解盘视频，超长语音转录行按禁截断规则不予入证。{E0}{E1}',
        '关联S0与C0；不跨源混用。{E0}{E1}',
        '见S0与C0；2020年1月16日大小盘分化与均线读数。{E0}{E1}'
    ),
    (
        '期货红色箭头出现且收K站上红线做多加仓条件观察',
        'SRC-000293',
        '源文画面文字OCR明确记录“> 焦煤迎来做多加仓机会出红色箭头做多加仓”以及“> 出了红色箭头且收k站上了红线”。{E2}{E3}',
        '仅记录≤300字完整原文字面的焦煤出红色箭头且收K站上红线做多加仓信号，不采信Vision推断，不跨课补全未明交易规则。{E2}{E3}',
        [
            '画面OCR显示“> 焦煤迎来做多加仓机会出红色箭头做多加仓”。{E2}',
            '画面OCR显示“> 出了红色箭头且收k站上了红线”。{E3}'
        ],
        '超长口述语音按无省略号不截断铁律不入证，未明环节留缺。{E2}{E3}',
        '关联S1与C1；不跨源混用。{E2}{E3}',
        '见S1与C1；红色箭头且收K站上红线做多加仓观察。{E2}{E3}'
    )
)

S = (
    (
        '大小盘指数分化下统一技术分析框架迁移跟踪方法',
        'SRC-001005',
        '在沪市主板下跌而创业板小盘股活跃的大小盘分化行情中使用。{E0}{E1}',
        '以主要观测目标上证指数演示量化技术分析框架（如关注MA5、MA10等均线变化），并将完全相同的技术分析方法迁移应用于创业板指数。{E0}{E1}',
        {
            '环境过滤': ('上证指数下跌0.52%而创业板上涨的大小盘分化环境', '日线', '{E0}', '大小盘分化'),
            '形态或指标形成': ('上证指数短期均线呈现MA5:3095.76↓与MA10:3091.26结构', '日线', '{E1}', '均线结构'),
            '确认': ('确认相同的技术分析方法适用于上证指数与创业板指', '方法确认', '{E0}', '跨指数通用'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('同步跟踪上证指数均线支撑与创业板指活跃节奏', '日线跟踪', '{E0}{E1}', '分化跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '统一分析框架跨指数应用，具体买卖点位原稿未展开留缺。{E0}{E1}',
        '同源K0与C0。{E0}{E1}',
        'Vision不作证；超长语音行不截断入证。{E0}{E1}'
    ),
    (
        '期货底仓盈利下出现红色箭头且收K站上红线做多加仓方法',
        'SRC-000293',
        '在期货多单持仓顺势运行并出现指标共振加仓信号时使用。{E2}{E3}',
        '在焦煤等期货品种迎来做多加仓机会时，等待盘面出现红色箭头信号且K线收盘站上红线，确认后执行做多加仓。{E2}{E3}',
        {
            '环境过滤': ('品种处于多头偏见顺势推升阶段并迎来加仓机会窗口', '日内周期', '{E2}', '加仓环境'),
            '形态或指标形成': ('盘面指标发出红色箭头信号且K线向红线上方运行', '指标与K线', '{E2}{E3}', '红色箭头信号'),
            '确认': ('确认出了红色箭头且K线收盘正式站上红线', '收K确认', '{E3}', '站上红线确认'),
            '入场': ('首次底仓入场时点本证未展开', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('在已有底仓基础上执行顺势加仓管理', '加仓资金', '{E2}', '加仓安排'),
            '持仓与跟踪': ('加仓后依托红线持续跟踪多头趋势延续性', '日内跟踪', '{E2}{E3}', '红线跟踪'),
            '加减仓': ('当出红色箭头且收K站上红线时执行做多加仓', '加仓动作', '{E2}{E3}', '红色箭头加仓'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('若未出红色箭头或收盘未能站上红线则放弃加仓', '条件未成', '{E3}', '未站上放弃')
        },
        '严格以出红色箭头且收K站上红线作为做多加仓触发条件，未披露数值留缺。{E2}{E3}',
        '同源K1与C1。{E2}{E3}',
        '严格依据原文字面，不采信Vision推断。{E2}{E3}'
    )
)

C = (
    (
        '2020年1月16日上证跌0.52%与创业板活跃分化复盘',
        'SRC-001005',
        '2020年1月16日（源文口述与行情面板）。{E0}',
        '上证指数、创业板指数（源文口述与行情面板）。{E0}{E1}',
        '指数日评与量化技术复盘，非独立回测或交易流水。{E0}{E1}',
        '关联K-40088、S-20055',
        '仅增强稿可见；非独立成交记录',
        '口述记录上证指数跌0.52%而创业板上涨、小盘股活跃，说明分析方法通用；行情OCR显示MA5:3095.76↓、MA10:3091.26。{E0}{E1}',
        '记录大小盘指数分化现象及统一技术分析方法的应用。{E0}{E1}',
        '未提供单笔交易订单与盈亏统计流水。{E0}{E1}',
        '不与第二源内容跨源拼接。{E0}{E1}',
        '口述与行情OCR证据{E0}{E1}'
    ),
    (
        '2025年6月5日焦煤期货出红色箭头且收K站上红线做多加仓复盘',
        'SRC-000293',
        '2025年6月5日（源文题名与复盘画面）。{E2}{E3}',
        '焦煤期货（源文画面文字OCR）。{E2}{E3}',
        '实盘交易笔记与信号复盘，非独立回测或交易流水。{E2}{E3}',
        '关联K-40089、S-20056',
        '仅增强稿可见；非独立成交记录',
        '画面文字记录焦煤迎来做多加仓机会，出了红色箭头且收K站上了红线执行做多加仓。{E2}{E3}',
        '记录期货顺势交易中红色箭头配合收K站上红线的加仓执行标准。{E2}{E3}',
        '未提供可核验的逐笔成交凭据流水。{E2}{E3}',
        '不与第一源内容跨源拼接。{E2}{E3}',
        '画面OCR字面证据{E2}{E3}'
    )
)

DOUBTS = [
    '主代理已通读SRC-001005 L1-854与SRC-000293 L1-3452全文。',
    'SRC-001005仅采信语音转录和行情OCR，不采信Vision推断。',
    'SRC-000293包含实盘图面批注OCR，严格遵守单段≤300字且不截断无省略号规则。'
]

RELATIONS = [
    'SRC-001005为股票大小盘分化解盘，SRC-000293为期货红色箭头加仓复盘；各卡严守单源边界。'
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
