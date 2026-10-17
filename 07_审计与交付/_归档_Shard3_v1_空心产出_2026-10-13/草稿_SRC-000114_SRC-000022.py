# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-000114', 'SRC-000022')
COUNTS = {'K': 2, 'S': 2, 'C': 2, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-000114', 'SRC-000114_(增强版)专题_交易思变_四象图与异色K线的交易细节若干.md', 18, [11, 15]),
    ('SRC-000022', 'SRC-000022_(增强版)P2_rb实测与细节掌握2.md', 714, [174, 271])
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
        '2024年3月28日四象图与异色K线交易细节专题讲解开场记录',
        'SRC-000114',
        '源文口述记录2024年3月28号9点半开场提醒前世正在交易与观看直播事宜，提出讲一讲四象图和异色K线问题；课件OCR记录“> 四象图与异色K线”。{E0}{E1}',
        '仅记录≤300字完整原文字面的2024年3月28日开场口述与课件四象图与异色K线标题字样，不采信Vision推断，不把未展开的后续细节假定为已明确规则。{E0}{E1}',
        [
            '口述记录2024年3月28号9点半开场并提出讲一讲四项图和一色K线。{E0}',
            '课件OCR显示“> 四象图与异色K线”。{E1}'
        ],
        '短视频开场仅1分钟，后续展开交易规则原稿未包含，未披露内容一律留缺。{E0}{E1}',
        '关联S0与C0；不跨源混用。{E0}{E1}',
        '见S0与C0；2024年3月28日四象图与异色K线专题开场记录。{E0}{E1}'
    ),
    (
        '实盘复盘中RSI与BOLL布林带组合指标参数与数值显示观察',
        'SRC-000022',
        '源文OCR记录实盘复盘软件中RSI与BOLL指标组合参数及读数，显示“> RSE9BOLL(20.2.14) RSt 68.20;A 20.00 D: 80.00”及“> RSEBOLL(20.214)RS529420.00D:80.00MD:56.19:PPERS1T,LOWER47.21”。{E2}{E3}',
        '仅记录≤300字完整原文字面的指标参数与界面读数，不把Vision对买卖点的推断当作老师规则，不补造交易流水。{E2}{E3}',
        [
            'OCR记录“> RSE9BOLL(20.2.14) RSt 68.20;A 20.00 D: 80.00”。{E2}',
            'OCR记录“> RSEBOLL(20.214)RS529420.00D:80.00MD:56.19:PPERS1T,LOWER47.21”。{E3}'
        ],
        '本源无语音转录文字，全部指标判断严格以OCR字面为界，不作衍生推断。{E2}{E3}',
        '关联S1与C1；不跨源混用。{E2}{E3}',
        '见S1与C1；RSI与BOLL组合指标观察。{E2}{E3}'
    )
)

S = (
    (
        '四象图与异色K线交易细节专题观察与学习安排方法',
        'SRC-000114',
        '在2024年3月28日开盘时段安排四象图与异色K线技术细节学习时使用。{E0}{E1}',
        '在开盘时段以不影响实盘交易为原则，观看或课后看录像学习四象图与异色K线相关量化技术分析。{E0}{E1}',
        {
            '环境过滤': ('2024年3月28日9点半盘中交易时段', '日内', '{E0}', '盘中环境'),
            '形态或指标形成': ('识别四象图与异色K线专题', '专题概念', '{E1}', '课件标题'),
            '确认': ('确认不影响当前实盘交易需求', '纪律', '{E0}', '纪律确认'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('根据交易需求选择看直播或稍后看录像', '跟踪', '{E0}', '学习安排'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '在盘中先做好交易与学习安排，四象图具体规则原稿未展开留缺。{E0}{E1}',
        '同源K0与C0。{E0}{E1}',
        '短视频开场证据有限，未披露环节一律留缺。{E0}{E1}'
    ),
    (
        '结合RSI与BOLL布林带组合指标辅助观察盘面动能的方法',
        'SRC-000022',
        '在实盘软件中调取RSI与BOLL指标参数并观察动态读数时使用。{E2}{E3}',
        '在复盘软件中调出RSE9BOLL组合指标，观察RSI数值在阈值（20与80）及中轨附近的动态变化。{E2}{E3}',
        {
            '环境过滤': ('实盘复盘K线环境', '日线', '{E2}', '复盘环境'),
            '形态或指标形成': ('指标窗口显示RSI与BOLL参数配置及数值', '指标形态', '{E2}{E3}', '指标读数'),
            '确认': ('核对RSI数值在20至80区间中的位置', '指标确认', '{E2}{E3}', '数值核对'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('在指标窗口持续跟踪RSI与BOLL通道变化', '指标跟踪', '{E2}{E3}', '持续跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '通过调取组合指标读数进行动能观察，具体交易触发点原稿未给留缺。{E2}{E3}',
        '同源K1与C1。{E2}{E3}',
        'Vision推断不作规则，原稿无语音转录，未明环节留缺。{E2}{E3}'
    )
)

C = (
    (
        '2024年3月28日四象图与异色K线专题开场复盘',
        'SRC-000114',
        '2024年3月28日9点半（源文口述）。{E0}',
        '四象图与异色K线专题（源文课件与口述）。{E0}{E1}',
        '课堂教学开场复盘，非独立回测或交易流水。{E0}{E1}',
        '关联K-40008、S-20005',
        '仅增强稿可见；非独立成交记录',
        '口述于2024年3月28号9点半开场提出四项图和一色K线问题并提醒盘中交易安排；课件显示“> 四象图与异色K线”。{E0}{E1}',
        '记录四象图与异色K线教学开场的纪律提示与主题引入。{E0}{E1}',
        '视频时长仅1分钟，未提供后续完整交易结果。{E0}{E1}',
        '不与第二源内容跨源拼接。{E0}{E1}',
        '口述与课件OCR证据{E0}{E1}'
    ),
    (
        '实盘复盘中RSI与BOLL组合指标参数及读数观察复盘',
        'SRC-000022',
        '源文OCR界面时间（2015/2020年历史K线复盘）。{E2}{E3}',
        '实盘K线与RSE9BOLL组合指标（源文OCR）。{E2}{E3}',
        '软件指标实测复盘，非独立回测或交易流水。{E2}{E3}',
        '关联K-40009、S-20006',
        '仅增强稿可见；非独立成交记录',
        'OCR记录指标窗口显示“> RSE9BOLL(20.2.14) RSt 68.20;A 20.00 D: 80.00”与“> RSEBOLL(20.214)RS529420.00D:80.00MD:56.19:PPERS1T,LOWER47.21”。{E2}{E3}',
        '记录实盘软件中RSI与布林带组合指标的参数设置与数值表现。{E2}{E3}',
        '未提供可核验的逐笔交易订单与盈亏统计。{E2}{E3}',
        '不与第一源内容跨源拼接。{E2}{E3}',
        'OCR原文字面证据{E2}{E3}'
    )
)

DOUBTS = [
    '主代理已通读SRC-000114 L1-18与SRC-000022 L1-714全文。',
    'SRC-000114仅18行（1分钟开场），原稿后续内容缺失；未披露规则严格留缺。',
    'SRC-000022仅有OCR与Vision，无语音转录，严格以OCR字面为据，不采信Vision推断。',
    '严格遵守单段引文≤300字且禁止截断/省略号规则。'
]

RELATIONS = [
    'SRC-000114为四象图与异色K线专题开场，SRC-000022为rb实测指标细节实盘；各卡严守单源边界。'
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
