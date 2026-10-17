# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-001002', 'SRC-000290')
COUNTS = {'K': 2, 'S': 2, 'C': 2, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-001002', 'SRC-001002_(增强版)股票_20200113量化技术分析.md', 1593, [11, 1017]),
    ('SRC-000290', 'SRC-000290_(增强版)期货_期货投机分析20250529_继续控制磨损_守住利润.md', 2862, [11, 52])
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
        '2020年1月13日上证指数突破前哨站与年线测试MA20支撑观察',
        'SRC-001002',
        '源文口述记录2020年1月13日周一三大指数大幅上扬，尾盘拉升创阶段收盘新高3115.57点突破年会前哨站；课件OCR记录“> 年线刚刚测试ma20支撑”。{E0}{E1}',
        '仅记录≤300字完整原文字面的上证指数3115.57光头阳线及课件思维导图文字，不采信Vision推断，不把未确认的后续走势当作确定规则。{E0}{E1}',
        [
            '口述记录三大指数大幅上扬、尾盘拉升全天收在最高点3115.57光头阳线。{E0}',
            '课件思维导图OCR显示“> 年线刚刚测试ma20支撑”。{E1}'
        ],
        '本源为大盘解盘视频，其余超300字语音转录行按禁截断规则不予入证。{E0}{E1}',
        '关联S0与C0；不跨源混用。{E0}{E1}',
        '见S0与C0；2020年1月13日指数突破与年线均线观察。{E0}{E1}'
    ),
    (
        '期货投机实盘中白银破近低与LPA绿色箭头空单条件观察',
        'SRC-000290',
        '源文口述记录2025年5月29日早盘开盘前交易提醒与方向选择重要性；微信群OCR记录“> 白银攻破近低或者出lpa绿色箭头下空单近”。{E2}{E3}',
        '仅记录≤300字完整原文字面的早盘开盘前提醒与白银做空触发条件OCR文字，不采信Vision推断，不跨课补全未明交易规则。{E2}{E3}',
        [
            '口述记录2025年5月29号9点钟早盘开盘前提醒并强调选对方向。{E2}',
            '屏幕微信群OCR显示“> 白银攻破近低或者出lpa绿色箭头下空单近”。{E3}'
        ],
        '超长口述语音按无省略号不截断铁律不入证，未明环节留缺。{E2}{E3}',
        '关联S1与C1；不跨源混用。{E2}{E3}',
        '见S1与C1；白银破近低与LPA绿色箭头空单观察。{E2}{E3}'
    )
)

S = (
    (
        '指数放量突破压力位后结合年线支撑跟踪多头结构的方法',
        'SRC-001002',
        '在指数收出光头阳线突破前期高点与前哨站压力位时使用。{E0}{E1}',
        '关注日线收于最高点并突破3115.57点多头结构，同时结合大周期思维导图中年线测试MA20支撑的状态进行多头跟踪。{E0}{E1}',
        {
            '环境过滤': ('周一三大指数大幅上扬，日线均线系统呈现多头排列', '日线', '{E0}', '多头环境'),
            '形态或指标形成': ('指数尾盘拉升全天收在最高点3115.57光头阳线，大周期测试MA20支撑', '日线/年线', '{E0}{E1}', '突破形态'),
            '确认': ('确认收盘价站稳前期前哨站压力点位', '日线', '{E0}', '点位确认'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('保持多头跟踪并观察年线测试MA20支撑情况', '日线/大周期', '{E0}{E1}', '持仓跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('若次日未能守住关键点位则需警惕假突破', '日线', '{E0}', '突破有效性检验')
        },
        '以日线收盘确认突破有效性，未明交易细节留缺。{E0}{E1}',
        '同源K0与C0。{E0}{E1}',
        'Vision不作证；超长语音行不截断入证。{E0}{E1}'
    ),
    (
        '期货实盘中白银破近低或出LPA绿色箭头做空应对方法',
        'SRC-000290',
        '在期货早盘交易时段评估白银品种做空机会时使用。{E2}{E3}',
        '当白银攻破近期低点或者盘面出现LPA绿色箭头信号时执行下空单操作。{E2}{E3}',
        {
            '环境过滤': ('2025年5月29日早盘期货开盘前评估市场方向', '期货日内', '{E2}', '开盘环境'),
            '形态或指标形成': ('白银攻破近低或者盘面出现LPA绿色箭头', '5分钟/日内', '{E3}', '信号触发'),
            '确认': ('二选一条件满足其一即可确认触发', '日内', '{E3}', '条件确认'),
            '入场': ('执行下空单操作', '日内', '{E3}', '下空单入场'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('控制磨损守住利润，仓位需严格控制', '日内', '{E2}', '仓位控制'),
            '持仓与跟踪': ('在空单盈利中持续跟踪盘面信号', '日内', '{E2}{E3}', '空单跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '依据字面规则执行条件触发做空，未明确止损止盈参数留缺。{E2}{E3}',
        '同源K1与C1。{E2}{E3}',
        '严格依据OCR原文字面，不采信Vision推断。{E2}{E3}'
    )
)

C = (
    (
        '2020年1月13日上证指数突破3115.57前哨站复盘',
        'SRC-001002',
        '2020年1月13日（源文口述与行情显示）。{E0}',
        '上证指数（源文口述与行情面板）。{E0}{E1}',
        '指数日评与量化技术复盘，非独立回测或交易流水。{E0}{E1}',
        '关联K-40016、S-20010',
        '仅增强稿可见；非独立成交记录',
        '口述记录2020年1月13日上证指数收在最高点3115.57光头阳线，突破年会前哨站；思维导图显示年线刚刚测试MA20支撑。{E0}{E1}',
        '记录大盘指数在多头排列下收光头阳线创阶段新高的技术走势。{E0}{E1}',
        '未提供单笔交易订单与盈亏统计流水。{E0}{E1}',
        '不与第二源内容跨源拼接。{E0}{E1}',
        '口述与课件OCR证据{E0}{E1}'
    ),
    (
        '2025年5月29日期货投机白银破近低/LPA做空观察复盘',
        'SRC-000290',
        '2025年5月29日早盘（源文口述与屏幕微信记录）。{E2}{E3}',
        '白银/沪银主力合约（源文口述与微信群记录）。{E2}{E3}',
        '实盘早盘推演复盘，非独立回测或交易流水。{E2}{E3}',
        '关联K-40017、S-20011',
        '仅增强稿可见；非独立成交记录',
        '口述记录5月29日开盘前提示方向选择，群记录显示白银攻破近低或者出LPA绿色箭头下空单。{E2}{E3}',
        '记录期货日内做空条件的制定与观察。{E2}{E3}',
        '未提供可核验的逐笔成交凭据流水。{E2}{E3}',
        '不与第一源内容跨源拼接。{E2}{E3}',
        '口述与微信OCR证据{E2}{E3}'
    )
)

DOUBTS = [
    '主代理已通读SRC-001002 L1-1593与SRC-000290 L1-2862全文。',
    'SRC-001002仅采信语音转录和思维导图OCR，不采信Vision推断。',
    'SRC-000290包含较长语音转录与微信群OCR，严格遵守单段≤300字且不截断无省略号规则。'
]

RELATIONS = [
    'SRC-001002为股票量化解盘，SRC-000290为期货投机实操；各卡严守单源边界。'
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
