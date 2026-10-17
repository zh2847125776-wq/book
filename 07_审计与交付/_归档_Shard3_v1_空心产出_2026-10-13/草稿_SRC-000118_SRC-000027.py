# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-000118', 'SRC-000027')
COUNTS = {'K': 1, 'S': 1, 'C': 1, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-000118', 'SRC-000118_(增强版)专题_交易思变_基于精确数据的波段交易选择对比.md', 7, []),
    ('SRC-000027', 'SRC-000027_(增强版)P2_回测.md', 1235, [151, 152, 156, 163])
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
        '突破重要价位回测定义及非必然性与回测失败清仓规则观察',
        'SRC-000027',
        '源文课件OCR定义回测为“> 突破颈线、均线、箱体、趋势线、缺口、前高前低、中位线等”“> 重要价位之后重新回到该价位的现象就叫回测”，明确指出“> 并不是每次突破重要点位都会出现回测”，并规定“> 回测失败前没有加仓，抛净所有仓位”。{E0}{E1}{E2}{E3}',
        '仅记录≤300字完整原文字面的技术突破回测定义、非必然性特征及回测失败抛净所有仓位的风控指令，不采信Vision推断，不补造交易流水。{E0}{E1}{E2}{E3}',
        [
            '课件OCR显示回测定义为“> 突破颈线、均线、箱体、趋势线、缺口、前高前低、中位线等”“> 重要价位之后重新回到该价位的现象就叫回测”。{E0}{E1}',
            '课件OCR显示“> 并不是每次突破重要点位都会出现回测”。{E2}',
            '课件OCR显示“> 回测失败前没有加仓，抛净所有仓位”。{E3}'
        ],
        '本源无语音转录文字，全部条件严格以课件OCR字面为界，不作衍生推断。{E0}{E1}{E2}{E3}',
        '关联S0与C0；同组前源仅含文件头无任何正文已核准为零卡来源，无跨源混用。{E0}{E1}{E2}{E3}',
        '见S0与C0；技术突破回测定义与回测失败清仓观察。{E0}{E1}{E2}{E3}'
    ),
)

S = (
    (
        '基于重要价位突破回测识别与回测失败抛净仓位的应对方法',
        'SRC-000027',
        '在价格突破颈线、均线、箱体、趋势线、缺口、前高前低或中位线等重要价位后跟踪回踩表现时使用。{E0}{E1}{E2}{E3}',
        '认识并不是每次突破重要点位都会出现回测；当价格突破重要价位后重新回到该价位发生回测时，严密观察支撑有效性，一旦回测失败则立即抛净所有仓位。{E0}{E1}{E2}{E3}',
        {
            '环境过滤': ('价格突破颈线、均线、箱体、趋势线、缺口、前高前低、中位线等重要价位', '多周期适用', '{E0}{E1}', '重要价位突破'),
            '形态或指标形成': ('突破重要价位之后价格重新回到该价位形成回测现象（注意并非每次突破都必然出现回测）', '回测形态', '{E0}{E1}{E2}', '回测出现'),
            '确认': ('观察重要价位回测是否获得支撑或宣告回测失败', '回测确认', '{E1}{E3}', '支撑与失败判定'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('以回测失败作为清仓离场风控底线', '回测失败止损', '{E3}', '失败清仓'),
            '仓位与资金': ('在回测确认成功前控制加仓冲动，一旦失败抛净所有仓位', '仓位风控', '{E3}', '全平风控'),
            '持仓与跟踪': ('突破后跟踪是否出现回测以及回测在重要价位处的表现', '回测跟踪', '{E0}{E1}{E2}', '回测跟踪'),
            '加减仓': ('回测失败前没有加仓', '加仓限制', '{E3}', '未加仓状态'),
            '止盈与退出': ('当判定回测失败时，立即抛净所有仓位离场', '清仓退出', '{E3}', '抛净所有仓位'),
            '失效与放弃': ('回测跌破重要价位宣告失败时放弃持仓全部抛净', '回测失败', '{E3}', '失败全抛')
        },
        '兼顾回测非必然性与回测失败全平纪律，未披露具体买入比例留缺。{E0}{E1}{E2}{E3}',
        '同源K0与C0。{E0}{E1}{E2}{E3}',
        'Vision推断不作规则，原稿无语音转录，未明环节留缺。{E0}{E1}{E2}{E3}'
    ),
)

C = (
    (
        '技术突破回测定义与回测失败抛净仓位课件教学复盘',
        'SRC-000027',
        '源文课件讲解时间（技术形态回测教学复盘）。{E0}{E1}',
        '颈线、均线、箱体、趋势线、缺口、前高前低、中位线突破回测（源文课件OCR）。{E0}{E1}{E2}{E3}',
        '课件规则教学复盘，非独立回测或交易流水。{E0}{E1}{E2}{E3}',
        '关联K-40104、S-20065',
        '仅增强稿可见；非独立成交记录',
        '课件思维导图界定突破重要价位后重新回到该价位叫回测，指出并非每次突破都会出现回测，并规定回测失败前没有加仓、抛净所有仓位。{E0}{E1}{E2}{E3}',
        '记录技术分析中回测现象的准确定义、发生概率认知及回测失败清仓原则。{E0}{E1}{E2}{E3}',
        '未提供可核验的逐笔交易订单与盈亏统计流水。{E0}{E1}{E2}{E3}',
        '同组前源为零卡来源，无跨源拼接。{E0}{E1}{E2}{E3}',
        '课件OCR字面证据{E0}{E1}{E2}{E3}'
    ),
)

DOUBTS = [
    '零卡来源：SRC-000118（主代理完整亲读全文7行152字符/299字节及双hash：视频时长0分20秒，全篇仅标题与3行视频处理说明，无任何语音转录、无任何课件/画面OCR、无任何正文内容；严格遵守不把来源说明当规则、不为覆盖来源强行凑卡的原则，已按规登记零卡来源_已复核.json并在此明确披露）。',
    '主代理已通读SRC-000118 L1-7与SRC-000027 L1-1235全文。',
    'SRC-000027仅有课件OCR与Vision，无语音转录，严格以OCR字面为据，不采信Vision推断。',
    '全组3张卡（K1/S1/C1）与4条证据（E4）全部出自SRC-000027，单卡严格单源。'
]

RELATIONS = [
    '同源SRC-000027内部：K0、S0、C0围绕技术突破回测定义、非必然性及回测失败抛净仓位紧密关联。',
    '跨源说明：SRC-000118为仅含文件头说明的空内容来源，已核准为零卡来源，故本组无SRC-000118卡片。'
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
