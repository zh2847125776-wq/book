# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-001007', 'SRC-000295')
COUNTS = {'K': 2, 'S': 2, 'C': 2, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-001007', 'SRC-001007_(增强版)股票_20200120量化技术分析.md', 1011, [11, 230]),
    ('SRC-000295', 'SRC-000295_(增强版)期货_期货投机分析20250609_可上可下_短线为佳.md', 4656, [1264, 3937])
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
        '2020年1月20日节前最后一周指数MA10均线读数观察',
        'SRC-001007',
        '源文口述记录节前最后一周外出录制解盘视频的观测背景；行情OCR显示“> MA10:3091.67”。{E0}{E1}',
        '仅记录≤300字完整原文字面的节前最后一周解盘背景与MA10均线数值读数，不采信Vision推断，不把超长语音行截断入证。{E0}{E1}',
        [
            '口述记录节前最后一周录制解盘视频观测市场走势。{E0}',
            '行情OCR显示“> MA10:3091.67”。{E1}'
        ],
        '本源为大盘解盘视频，其余超300字语音行按禁截断铁律不予入证。{E0}{E1}',
        '关联S0与C0；不跨源混用。{E0}{E1}',
        '见S0与C0；2020年1月20日节前最后一周MA10读数。{E0}{E1}'
    ),
    (
        '期货APL加LPA平台向下顺势给空单与板块分化空间不足放弃观察',
        'SRC-000295',
        '源文口述记录采用APL（平均价格水平）加LPA（最佳交易流动性）结合分析，平台向下不可能给多单、必给转绿色箭头或收K攻破绿线的空单；同时对化工系品种方向不一致、橡胶临近前低空间太小（底部震荡）及玻璃单边过多等情况选择放一放不做。{E2}{E3}',
        '仅记录≤300字完整原文字面的APL与LPA概念区分、平台向下转绿色箭头或破绿线给空单以及空间不足放弃原则，不采信Vision推断，不跨课补全未明交易规则。{E2}{E3}',
        [
            '口述记录APL为平均价格水平、LPA为最佳交易流动性，平台向下绝不给多单，而是按转绿色箭头或收K攻破绿线给空单。{E2}',
            '口述记录等待贴近后再试多单，并对化工系方向分化、橡胶临近前低空间太小（底部震荡）及玻璃单边过多执行放一放不做的过滤。{E3}'
        ],
        '超长口述语音按无省略号不截断铁律不入证，未明环节留缺。{E2}{E3}',
        '关联S1与C1；不跨源混用。{E2}{E3}',
        '见S1与C1；APL加LPA顺势空单与空间过滤观察。{E2}{E3}'
    )
)

S = (
    (
        '节前最后一周跟踪指数MA10均线位置的观测方法',
        'SRC-001007',
        '在春节长假前最后一周观测指数短期均线支撑与运行状态时使用。{E0}{E1}',
        '在节前最后一周保持日常解盘观测，重点关注指数MA10（3091.67）等短期均线位置表现。{E0}{E1}',
        {
            '环境过滤': ('春节前最后一周交易时间窗口', '日线', '{E0}', '节前窗口'),
            '形态或指标形成': ('行情面板显示MA10均线位于3091.67', '日线', '{E1}', 'MA10读数'),
            '确认': ('本证未明确', '—', '—', '留缺'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('节前最后一周持续跟踪指数在MA10（3091.67）附近的运行表现', '日线跟踪', '{E0}{E1}', '均线跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '跟踪节前最后一周指数MA10均线读数，具体买卖指令原稿未展开留缺。{E0}{E1}',
        '同源K0与C0。{E0}{E1}',
        'Vision不作证；超长语音行不截断入证。{E0}{E1}'
    ),
    (
        '结合APL与LPA平台方向顺势开单并过滤小空间震荡品种的方法',
        'SRC-000295',
        '在期货日内交易结合APL与LPA指标判定多空方向并筛选交易品种时使用。{E2}{E3}',
        '结合APL（平均价格水平）与LPA（最佳交易流动性），当平台向下时严禁逆势给多单，仅在转绿色箭头或收K攻破绿线时给空单；做多需等价格贴近后再试；对板块内部方向分化、临近前低空间太小（底部震荡）的品种直接放弃。{E2}{E3}',
        {
            '环境过滤': ('结合APL与LPA评估平台方向，过滤化工系多品种方向分化及临近前低空间过小的震荡环境', '日内/多周期', '{E2}{E3}', '平台方向与空间过滤'),
            '形态或指标形成': ('平台向下阶段观察绿色箭头与绿线；做多候选品种等待价格贴近支撑', '指标与K线', '{E2}{E3}', '指标信号形成'),
            '确认': ('空单确认转绿色箭头或收K攻破绿线；多单确认贴近后转多信号触发', '信号确认', '{E2}{E3}', '信号触发确认'),
            '入场': ('平台向下且转绿色箭头或收K攻破绿线时下空单；多单等待贴近转多后入场', '顺势入场', '{E2}{E3}', '按信号入场'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('比较不同品种潜在盈利空间（如橡胶对比焦煤空间太小则不做），将资金留给空间充足品种', '空间择优', '{E3}', '空间权衡'),
            '持仓与跟踪': ('跟踪前期未触发订单在新交易日贴近后的转多机会', '订单跟踪', '{E3}', '贴近重试跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('平台向下绝不给多单；化工系方向不一、原油涨多空不下、橡胶临近前低底部震荡空间太小、玻璃单边过多均果断放弃不做', '多维放弃条件', '{E2}{E3}', '果断放弃不做')
        },
        '严守平台向下只空不多、收K破绿线或绿箭头触发，并果断过滤空间不足与板块分化品种。{E2}{E3}',
        '同源K1与C1。{E2}{E3}',
        '严格依据原文字面，不采信Vision推断。{E2}{E3}'
    )
)

C = (
    (
        '2020年1月20日节前最后一周指数MA10均线3091.67复盘',
        'SRC-001007',
        '2020年1月20日（源文题名与口述）。{E0}',
        '上证指数（源文行情面板）。{E0}{E1}',
        '指数节前日评复盘，非独立回测或交易流水。{E0}{E1}',
        '关联K-40136、S-20085',
        '仅增强稿可见；非独立成交记录',
        '口述记录节前最后一周录制解盘视频；行情OCR显示MA10:3091.67。{E0}{E1}',
        '记录2020年春节前最后一周首个交易日对指数均线状态的跟踪。{E0}{E1}',
        '未提供单笔交易订单与盈亏统计流水。{E0}{E1}',
        '不与第二源内容跨源拼接。{E0}{E1}',
        '口述与行情OCR证据{E0}{E1}'
    ),
    (
        '2025年6月9日期货黄金APL加LPA平台向下空单与原油化工橡胶玻璃放弃复盘',
        'SRC-000295',
        '2025年6月9日（复盘6月6日周五9:10信号及当日早盘）。{E2}{E3}',
        '黄金、原油、化工系、橡胶、焦煤、玻璃期货（源文口述）。{E2}{E3}',
        '实盘多品种筛选与信号复盘，非独立回测或交易流水。{E2}{E3}',
        '关联K-40137、S-20086',
        '仅增强稿可见；非独立成交记录',
        '口述记录黄金下跌并复盘6月6日周五早上9:10因平台下降结合APL（平均价格水平）与LPA（最佳交易流动性）给出转绿色箭头或收K攻破绿线的空单信号；同时梳理原油涨多空单下不了、化工系好几个品种方向不一样放一放、橡胶要到前低底部震荡空间比焦煤小太多不管它、玻璃单边太多没法空。{E2}{E3}',
        '记录期货实盘中APL加LPA顺平台方向开单以及果断放弃空间不足与方向混乱品种的筛选标准。{E2}{E3}',
        '未提供可核验的逐笔成交凭据流水。{E2}{E3}',
        '不与第一源内容跨源拼接。{E2}{E3}',
        '口述原文字面证据{E2}{E3}'
    )
)

DOUBTS = [
    '主代理已通读SRC-001007 L1-1011与SRC-000295 L1-4656全文。',
    'SRC-001007与SRC-000295仅采信≤300字完整语音转录行和画面OCR，不采信Vision推断。',
    '严格遵守单段≤300字且不截断无省略号规则。'
]

RELATIONS = [
    'SRC-001007为2020年节前股票指数解盘，SRC-000295为期货APL加LPA顺势信号与多品种空间过滤复盘；各卡严守单源边界。'
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
