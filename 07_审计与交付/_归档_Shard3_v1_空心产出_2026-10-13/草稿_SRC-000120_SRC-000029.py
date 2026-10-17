# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-000120', 'SRC-000029')
COUNTS = {'K': 2, 'S': 2, 'C': 2, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-000120', 'SRC-000120_(增强版)专题_交易思变_如何利用新华富时A50最大可能性的预测超长假期后大致开盘位置.md', 39, [22]),
    ('SRC-000029', 'SRC-000029_(增强版)P2_复盘.md', 1374, [828, 830, 1082])
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
        '元旦短假全球同休与特有超长假期休市特征对比观察',
        'SRC-000120',
        '源文口述记录2024年2月10日春节期间探讨假期后行情怎么走，指出A股有两个特有节日不交易且休息时间较长，而元旦仅停一两天且全球其他主要指数也都停，故元旦一般不考虑。{E0}',
        '仅记录≤300字完整原文字面的元旦短假全球同休不考虑与两个特有长假休市特征对比，不采信Vision推断，不把未展开的后续A50换算细节假定为已明确规则。{E0}',
        [
            '口述记录元旦仅停一两天且全球其他主要指数也停故一般不考虑，而两个特有节日不交易且休息时间较长。{E0}'
        ],
        '短视频仅1分钟开场，后续新华富时A50具体换算公式原稿未包含，未披露内容一律留缺。{E0}',
        '关联S0与C0；不跨源混用。{E0}',
        '见S0与C0；元旦与特有超长假期休市特征对比观察。{E0}'
    ),
    (
        '股票复盘调阅南钢股份与阳谷华泰均线及盘口数据观察',
        'SRC-000029',
        '源文画面文字OCR记录复盘调阅“> 南钢股份600282”及其均线“> 南钢股份MA5:3.34,MA10:3.401MA20:3.491”，以及“> 阳谷华泰300121”。{E1}{E2}{E3}',
        '仅记录≤300字完整原文字面的复盘个股代码与均线数值读数，不采信Vision推断，不补造交易流水。{E1}{E2}{E3}',
        [
            '行情OCR显示“> 南钢股份MA5:3.34,MA10:3.401MA20:3.491”及“> 南钢股份600282”。{E1}{E2}',
            '行情OCR显示“> 阳谷华泰300121”。{E3}'
        ],
        '本源无语音转录文字，全部条件严格以行情画面OCR字面为界，不作衍生推断。{E1}{E2}{E3}',
        '关联S1与C1；不跨源混用。{E1}{E2}{E3}',
        '见S1与C1；南钢股份与阳谷华泰复盘观察。{E1}{E2}{E3}'
    )
)

S = (
    (
        '区分元旦全球同休与特有超长假期休市差异的盘前观察方法',
        'SRC-000120',
        '在节假日期间评估假期后开盘行情预测必要性时使用。{E0}',
        '区分不同假期的休市特征：对仅停一两天且全球主要指数同休的元旦假期一般不作特殊考虑；重点针对A股两个特有的超长休市节日开展节后行情研判准备。{E0}',
        {
            '环境过滤': ('节假日休市期间评估节后行情走向环境', '节假日窗口', '{E0}', '假期分类过滤'),
            '形态或指标形成': ('对比元旦（停一两天、全球主要指数同停）与两个特有长假（休息时间长）的差异', '假期特征', '{E0}', '休市时长对比'),
            '确认': ('确认元旦一般不考虑，聚焦两个特有长假后的行情研判', '研判重心确认', '{E0}', '重心聚焦'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('在特有超长假期期间关注节后行情走向', '假期跟踪', '{E0}', '长假跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('元旦短假且全球主要指数同休时放弃特殊长假预测模型', '元旦不考虑', '{E0}', '短假不考虑')
        },
        '区分元旦同休与特有超长假期的差异，未披露具体A50换算细节留缺。{E0}',
        '同源K0与C0。{E0}',
        '短视频开场证据有限，未披露环节一律留缺。{E0}'
    ),
    (
        '复盘调阅自选个股均线读数与多标的切换审阅方法',
        'SRC-000029',
        '在盘后或盘中利用行情软件对自选板块个股依次开展技术复盘时使用。{E1}{E2}{E3}',
        '在复盘过程中依次调取南钢股份（600282）、阳谷华泰（300121）等自选个股，核查MA5、MA10、MA20等短期均线数值与排列状态。{E1}{E2}{E3}',
        {
            '环境过滤': ('行情软件自选股技术分析复盘环境', '日线', '{E1}{E2}{E3}', '软件复盘环境'),
            '形态或指标形成': ('读取南钢股份（600282）MA5:3.34、MA10:3.40、MA20:3.49等均线数据，并切换审阅阳谷华泰（300121）', '日线均线', '{E1}{E2}{E3}', '均线与个股调阅'),
            '确认': ('本证未明确', '—', '—', '留缺'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('通过复盘持续跟踪南钢股份（600282）与阳谷华泰（300121）等个股的均线变化', '复盘跟踪', '{E1}{E2}{E3}', '多股跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '客观记录复盘调阅个股与均线读数流程，未披露具体买卖指令留缺。{E1}{E2}{E3}',
        '同源K1与C1。{E1}{E2}{E3}',
        'Vision推断不作规则，原稿无语音转录，未明环节留缺。{E1}{E2}{E3}'
    )
)

C = (
    (
        '2024年2月10日春节超长假期与元旦全球同休对比专题开场复盘',
        'SRC-000120',
        '2024年2月10日14:45（源文口述）。{E0}',
        'A股特有超长假期与全球主要指数休市制度对比（源文口述）。{E0}',
        '课堂专题引入复盘，非独立回测或交易流水。{E0}',
        '关联K-40152、S-20095',
        '仅增强稿可见；非独立成交记录',
        '口述记录2024年2月10日春节期间讲解A股有两个特有节日不交易且休息时间较长，而元旦仅停一两天且全球其他主要指数也都停故一般不考虑。{E0}',
        '记录超长假期开盘位置预测专题的假期特征界定。{E0}',
        '视频仅1分钟开场，未提供后续完整换算过程与交易流水。{E0}',
        '不与第二源内容跨源拼接。{E0}',
        '口述原文字面证据{E0}'
    ),
    (
        '南钢股份600282与阳谷华泰300121软件均线复盘演示',
        'SRC-000029',
        '源文软件复盘演示时间（行情画面OCR）。{E1}{E2}{E3}',
        '南钢股份（600282）、阳谷华泰（300121）（源文画面文字OCR逐字包含代码）。{E1}{E2}{E3}',
        '软件复盘个股切换与均线审阅演示，非独立回测或交易流水。{E1}{E2}{E3}',
        '关联K-40153、S-20096',
        '仅增强稿可见；非独立成交记录',
        '行情画面OCR记录复盘调阅南钢股份600282（显示MA5:3.34、MA10:3.40、MA20:3.49）及阳谷华泰300121。{E1}{E2}{E3}',
        '记录复盘教学中对南钢股份与阳谷华泰的面板调阅。{E1}{E2}{E3}',
        '未提供可核验的逐笔交易订单与盈亏统计流水。{E1}{E2}{E3}',
        '不与第一源内容跨源拼接。{E1}{E2}{E3}',
        '画面OCR字面证据{E1}{E2}{E3}'
    )
)

DOUBTS = [
    '主代理已通读SRC-000120 L1-39与SRC-000029 L1-1374全文。',
    'SRC-000120仅39行（1分钟开场），严格依据≤300字完整语音行抽取。',
    'SRC-000029仅有画面OCR与Vision，无语音转录，严格以OCR字面为据，不采信Vision推断；C1品种栏所写600282与300121均由所引OCR原行逐字包含。',
    '严格遵守单段≤300字且不截断无省略号规则。'
]

RELATIONS = [
    'SRC-000120为春节超长假期与元旦休市对比开场，SRC-000029为南钢股份与阳谷华泰软件复盘演示；各卡严守单源边界。'
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
