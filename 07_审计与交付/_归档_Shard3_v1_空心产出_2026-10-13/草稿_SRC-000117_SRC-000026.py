# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-000117', 'SRC-000026')
COUNTS = {'K': 1, 'S': 1, 'C': 1, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-000117', 'SRC-000117_(增强版)专题_交易思变_基于MA60的几种常见转向模型.md', 7, []),
    ('SRC-000026', 'SRC-000026_(增强版)P2_几不买.md', 524, [127, 128, 130, 401])
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
        '股票几不买负面清单与日线选股积分表80分及格标准观察',
        'SRC-000026',
        '源文课件OCR记录股票几不买条件包含“> 股价小于20日线”（“> 无法设置止损、风险大”）、“> 流通市值小于100亿”；并展示“> 日线选股积分表（80分及格）”作为正面量化评分标准。{E0}{E1}{E2}{E3}',
        '仅记录≤300字完整原文字面的“几不买”负面排除项与“日线选股积分表（80分及格）”标题，不采信Vision推断，不补造交易流水。{E0}{E1}{E2}{E3}',
        [
            '思维导图OCR显示负面清单“> 股价小于20日线”及原因“> 无法设置止损、风险大”。{E0}{E1}',
            '思维导图OCR显示负面清单“> 流通市值小于100亿”。{E2}',
            '文档画面OCR显示正面量化标准“> 日线选股积分表（80分及格）”。{E3}'
        ],
        '本源无语音转录文字，全部条件严格以课件与文档OCR字面为界，不作衍生推断。{E0}{E1}{E2}{E3}',
        '关联S0与C0；同组前源仅含文件头无任何正文已核准为零卡来源，无跨源混用。{E0}{E1}{E2}{E3}',
        '见S0与C0；股票几不买与日线选股积分表观察。{E0}{E1}{E2}{E3}'
    ),
)

S = (
    (
        '排除股价小于20日线及小市值个股并按日线积分表80分选股方法',
        'SRC-000026',
        '在日线级别进行趋势选股与风险标底排除时使用。{E0}{E1}{E2}{E3}',
        '坚决排除股价小于20日线（无法设置止损、风险大）以及流通市值小于100亿的个股；采用日线选股积分表进行量化打分，以80分及格作为选股准入线。{E0}{E1}{E2}{E3}',
        {
            '环境过滤': ('日线级别选股，过滤流通市值小于100亿的小盘股', '日线', '{E2}{E3}', '市值过滤'),
            '形态或指标形成': ('核查个股是否处于股价小于20日线的弱势状态', '日线', '{E0}{E1}', '20日线核查'),
            '确认': ('按日线选股积分表逐项核对打分，确认得分达到80分及格标准', '积分表确认', '{E3}', '80分及格确认'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('排除股价小于20日线无法设置止损的标的，依托20日线体系控制风险', '止损过滤', '{E0}{E1}', '止损前提'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('本证未明确', '—', '—', '留缺'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('凡属股价小于20日线或流通市值小于100亿或积分未达80分及格者一律放弃不买', '负面清单放弃', '{E0}{E1}{E2}{E3}', '几不买放弃')
        },
        '先以负面清单排除高风险无止损基准个股，再以日线选股积分表80分及格准入，未明买卖执行细节留缺。{E0}{E1}{E2}{E3}',
        '同源K0与C0。{E0}{E1}{E2}{E3}',
        'Vision推断不作规则，原稿无语音转录，未明环节留缺。{E0}{E1}{E2}{E3}'
    ),
)

C = (
    (
        '股票几不买思维导图与日线选股积分表80分及格教学复盘',
        'SRC-000026',
        '2020年3月2日（源文界面时间戳）。{E0}{E3}',
        'A股日线选股标的（源文课件与文档OCR）。{E0}{E1}{E2}{E3}',
        '课件选股规则与积分表教学复盘，非独立回测或交易流水。{E0}{E1}{E2}{E3}',
        '关联K-40080、S-20050',
        '仅增强稿可见；非独立成交记录',
        '课件思维导图列出股票几不买：股价小于20日线（无法设置止损、风险大）、流通市值小于100亿等；并展示日线选股积分表（80分及格）。{E0}{E1}{E2}{E3}',
        '记录从负面排除“几不买”到正面量化“日线选股积分表（80分及格）”的选股体系构建。{E0}{E1}{E2}{E3}',
        '未提供可核验的逐笔交易订单与盈亏统计流水。{E0}{E1}{E2}{E3}',
        '同组前源为零卡来源，无跨源拼接。{E0}{E1}{E2}{E3}',
        '课件与文档OCR字面证据{E0}{E1}{E2}{E3}'
    ),
)

DOUBTS = [
    '零卡来源：SRC-000117（主代理完整亲读全文7行152字符/283字节及双hash：视频时长0分20秒，全篇仅标题与3行视频处理说明，无任何语音转录、无任何课件/画面OCR、无任何正文内容；严格遵守不把来源说明当规则、不为覆盖来源强行凑卡的原则，已按规登记零卡来源_已复核.json并在此明确披露）。',
    '主代理已通读SRC-000117 L1-7与SRC-000026 L1-524全文。',
    'SRC-000026仅有课件/文档OCR与Vision，无语音转录，严格以OCR字面为据，不采信Vision推断。',
    '全组3张卡（K1/S1/C1）与4条证据（E4）全部出自SRC-000026，单卡严格单源。'
]

RELATIONS = [
    '同源SRC-000026内部：K0、S0、C0围绕股票几不买负面清单与日线选股积分表（80分及格）紧密关联。',
    '跨源说明：SRC-000117为仅含文件头说明的空内容来源，已核准为零卡来源，故本组无SRC-000117卡片。'
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
        uses = [cid for cid, sid, card in r.cards[-3:] if '[' + e + ']' in card and sid == r.evidence[e][1]]
        assert uses
        r.evidence[e][4] = '；'.join(uses)
    return {
        'counts': COUNTS,
        'new_counts': NEW_COUNTS,
        'supplement_counts': SUPPLEMENT_COUNTS,
        'total_cards': 3,
        'total_evidence': 4,
        'doubts': DOUBTS,
        'relations': q(RELATIONS),
        'reading': R
    }
