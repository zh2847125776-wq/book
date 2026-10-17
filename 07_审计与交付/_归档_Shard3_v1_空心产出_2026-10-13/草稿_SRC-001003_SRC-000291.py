# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-001003', 'SRC-000291')
COUNTS = {'K': 2, 'S': 2, 'C': 2, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-001003', 'SRC-001003_(增强版)股票_20200114量化技术分析.md', 756, [11, 705]),
    ('SRC-000291', 'SRC-000291_(增强版)期货_期货投机分析20250530_完结头寸_等待节后交易.md', 3541, [11, 590])
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
        '2020年1月14日指数累积涨幅后小幅调整与守好均线规则观察',
        'SRC-001003',
        '源文口述记录三大指数累积涨幅后陷入小幅调整，强调调整正常但需守好均线、趋势线、颈线与缺口；行情OCR显示上证指数MA5与MA10数值。{E0}{E1}',
        '仅记录≤300字完整原文字面的指数回调背景与均线关键位防守原则，不采信Vision推断，不把未确认的后续走势当作确定规则。{E0}{E1}',
        [
            '口述记录三大指数陷入小幅调整，强调累积涨幅后调整正常并守好均线、趋势线、颈线、缺口。{E0}',
            '行情OCR显示上证指数均线数值“> 上证指激MA5:3095.29MA10:3088.38”。{E1}'
        ],
        '本源为大盘解盘视频，超长语音转录行按禁截断规则不予入证。{E0}{E1}',
        '关联S0与C0；不跨源混用。{E0}{E1}',
        '见S0与C0；2020年1月14日指数调整与均线防守。{E0}{E1}'
    ),
    (
        '2025年5月30日月末及节日假期前期货早盘头寸完结与交易安排观察',
        'SRC-000291',
        '源文口述记录2025年5月30日月末最后一个交易日且临近端午节，当晚无夜盘需做好交易安排；行情软件OCR显示“> 09:00期货早盘开盘：原代码/名称/简拼/功能”。{E2}{E3}',
        '仅记录≤300字完整原文字面的月末假期前开盘提醒与早盘时段标识，不采信Vision推断，不跨课补全未明交易规则。{E2}{E3}',
        [
            '口述记录2025年5月30号9点钟月末最后一个交易日且临近端午节假期，提醒无夜盘安排。{E2}',
            '行情软件界面OCR显示“> 09:00期货早盘开盘：原代码/名称/简拼/功能”。{E3}'
        ],
        '超长口述语音按无省略号不截断铁律不入证，未明环节留缺。{E2}{E3}',
        '关联S1与C1；不跨源混用。{E2}{E3}',
        '见S1与C1；月末假期前期货早盘安排观察。{E2}{E3}'
    )
)

S = (
    (
        '指数上涨累积后小幅调整期坚守关键技术位跟踪方法',
        'SRC-001003',
        '在指数经历大幅上涨后出现小幅震荡回调时使用。{E0}{E1}',
        '在指数累积较大涨幅后的调整期不盲目恐慌，以均线、趋势线、颈线及缺口作为持仓与防守基准进行客观跟踪。{E0}{E1}',
        {
            '环境过滤': ('三大指数经历前期大幅上涨后出现小幅调整', '日线', '{E0}', '调整环境'),
            '形态或指标形成': ('指数处于短线震荡休整，MA5与MA10维持多头依托', '日线', '{E0}{E1}', '均线依托'),
            '确认': ('确认价格未跌破所设定的均线、趋势线、颈线及缺口防守位', '关键位确认', '{E0}', '防守确认'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('严格守好所有均线、趋势线、颈线和缺口进行持仓跟踪', '跟踪基准', '{E0}{E1}', '多头跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('若关键均线或颈线支撑被有效跌破则调整性质恶化', '破位失效', '{E0}', '支撑失效')
        },
        '以客观关键支撑位作为调整期防守基准，未明交易细节留缺。{E0}{E1}',
        '同源K0与C0。{E0}{E1}',
        'Vision不作证；超长语音行不截断入证。{E0}{E1}'
    ),
    (
        '月末及长假前期货头寸完结与风控应对操作方法',
        'SRC-000291',
        '在期货交易临近月末最后一个交易日及小长假休市前使用。{E2}{E3}',
        '在长假前最后交易日评估无夜盘风险，完结已有头寸并控制长假隔夜风险，等待节后新机会。{E2}{E3}',
        {
            '环境过滤': ('2025年5月30日月末最后一个交易日且面临小长假休市', '日内/假日周期', '{E2}', '假期临近环境'),
            '形态或指标形成': ('早盘9点开盘前评估头寸状况及假期无夜盘特点', '开盘评估', '{E2}{E3}', '开盘前评估'),
            '确认': ('确认长假休市期间外盘不确定性与跳空风险', '风险确认', '{E2}', '假期间风险'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('月末及休假前以完结头寸、守住利润、防范磨损为原则控制仓位', '风控纪律', '{E2}', '假期风控'),
            '持仓与跟踪': ('在节前最后时段跟踪各品种盘面动向，平稳结清头寸', '日内跟踪', '{E2}{E3}', '头寸完结'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('在节前适时平仓离场，避免承担长假隔夜不确定性', '假期退出', '{E2}', '节前平仓'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '依据节前休市规则执行仓位规避与头寸完结，未明参数留缺。{E2}{E3}',
        '同源K1与C1。{E2}{E3}',
        '严格依据原文字面，不采信Vision推断。{E2}{E3}'
    )
)

C = (
    (
        '2020年1月14日上证指数小幅调整与均线系统依托复盘',
        'SRC-001003',
        '2020年1月14日（源文口述与行情面板）。{E0}',
        '上证指数（源文口述与行情面板）。{E0}{E1}',
        '指数日评与量化技术复盘，非独立回测或交易流水。{E0}{E1}',
        '关联K-40040、S-20025',
        '仅增强稿可见；非独立成交记录',
        '口述记录三大指数累积涨幅后小幅调整，强调守好均线趋势线颈线缺口；行情显示MA5与MA10数值。{E0}{E1}',
        '记录大盘指数在连涨后调整期的技术防守策略。{E0}{E1}',
        '未提供单笔交易订单与盈亏统计流水。{E0}{E1}',
        '不与第二源内容跨源拼接。{E0}{E1}',
        '口述与行情OCR证据{E0}{E1}'
    ),
    (
        '2025年5月30日期货月末及端午节前头寸完结推演复盘',
        'SRC-000291',
        '2025年5月30日早盘（源文口述与屏幕时钟）。{E2}{E3}',
        '商品期货市场及早盘品种（源文口述与行情面板）。{E2}{E3}',
        '实盘早盘推演复盘，非独立回测或交易流水。{E2}{E3}',
        '关联K-40041、S-20026',
        '仅增强稿可见；非独立成交记录',
        '口述记录5月30日早盘9点月末最后交易日且临近端午节，提示无夜盘并完结头寸；界面显示早盘开盘时段。{E2}{E3}',
        '记录期货长假前风险管理与头寸处理的决策过程。{E2}{E3}',
        '未提供可核验的逐笔成交凭据流水。{E2}{E3}',
        '不与第一源内容跨源拼接。{E2}{E3}',
        '口述与界面OCR证据{E2}{E3}'
    )
)

DOUBTS = [
    '主代理已通读SRC-001003 L1-756与SRC-000291 L1-3541全文。',
    'SRC-001003仅采信语音转录和行情OCR，不采信Vision推断。',
    'SRC-000291包含较长语音转录与行情界面OCR，严格遵守单段≤300字且不截断无省略号规则。'
]

RELATIONS = [
    'SRC-001003为股票量化解盘，SRC-000291为期货长假前头寸管理；各卡严守单源边界。'
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
