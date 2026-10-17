# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-002733', 'SRC-000245')
COUNTS = {'K': 2, 'S': 2, 'C': 2, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-002733', 'SRC-002733_(增强版)读书_12.md', 317, [11, 16]),
    ('SRC-000245', 'SRC-000245_(增强版)妖股成妖之路_23.md', 1188, [427, 428])
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
        '利弗莫尔回忆录研读记录与老帕特里奇大势领悟观察',
        'SRC-002733',
        '源文口述记录研读《股票大作手回忆录》第48页最下面反思大势判断正确却未赚到钱的错误，领悟老帕特里奇教诲；视频画面OCR显示版权网址。{E0}{E1}',
        '仅记录≤300字完整原文字面的研读书页反思与背景信息，不采信Vision推断，不把超长语音转录截断入证。{E0}{E1}',
        [
            '口述记录研读回忆录第48页反思踩空与老帕特里奇教诲。{E0}',
            '画面OCR显示背景标识行。{E1}'
        ],
        '其余超300字口述行按无省略号不截断规则不入证，未明规则留缺。{E0}{E1}',
        '关联S0与C0；不跨源混用。{E0}{E1}',
        '见S0与C0；回忆录大势研读记录。{E0}{E1}'
    ),
    (
        '投资前设定止损点与目标价位及坚决执行规则观察',
        'SRC-000245',
        '源文记录在每次投资前都要给自己设定一个止损点和一个目标价位；当股价达到止损点时坚决卖出，达到目标价位时适当减仓锁定利润。{E2}{E3}',
        '仅记录≤300字完整原文字面的投资前风控计划与止损止盈执行规则，不凭空衍生未披露的具体价位参数。{E2}{E3}',
        [
            '原文明确规定“在每次投资前，都要给自己设定一个止损点和一个目标价位”。{E2}',
            '原文明确规定“当股价达到止损点时，不管盈亏都要坚决卖出；而当股价达到目标价位时，可以适当减仓锁定利润”。{E3}'
        ],
        '仅限短线短文投资心得记录，不跨接其他来源。{E2}{E3}',
        '关联S1与C1；不跨源混用。{E2}{E3}',
        '见S1与C1；事前止损止盈设定与执行。{E2}{E3}'
    )
)

S = (
    (
        '研读经典趋势大势教诲与顺应大势持仓心得方法',
        'SRC-002733',
        '在研读交易心理与大作手回忆录大势哲学时使用。{E0}{E1}',
        '反思对大势判断正确却因频繁小波动离场踩空的教训，建立顺应大趋势、抵御微小波动诱惑的心态认知。{E0}{E1}',
        {
            '环境过滤': ('研读交易经典第48页背景', '大势研读', '{E0}', '读书研读背景'),
            '形态或指标形成': ('对大势判断正确但面临小波动的诱惑与踩空风险', '大势形态', '{E0}', '大势反思'),
            '确认': ('领悟老帕特里奇关于坚守大势的经验教训', '理念确认', '{E0}', '理念确认'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('在顺应大势的过程中抵御诱惑并保持耐心', '大势持仓', '{E0}', '大势跟踪'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('本证未明确', '—', '—', '留缺')
        },
        '建立顺应大势的心态认知，具体买卖指标原稿未展开留缺。{E0}{E1}',
        '同源K0与C0。{E0}{E1}',
        '超长口述行不截断入证，未明环节留缺。{E0}{E1}'
    ),
    (
        '事前设定止损点与目标价位的试错与执行操作方法',
        'SRC-000245',
        '在任何个股投资与试错建仓决策前使用。{E2}{E3}',
        '在每次投资前预先设定明确的止损点和目标价位；触及止损点坚决卖出离场，触及目标价位适当减仓锁定利润。{E2}{E3}',
        {
            '环境过滤': ('在进行单笔投资或试错操作前', '计划阶段', '{E2}', '事前规划'),
            '形态或指标形成': ('选定标的并完成初步逻辑分析', '标的选择', '{E2}', '标的选定'),
            '确认': ('确认止损点与目标价位已预先设定完毕', '计划确认', '{E2}', '计划核对'),
            '入场': ('按计划买入建仓', '执行', '{E2}', '试错买入'),
            '初始止损': ('设定明确止损点，触及止损点时不计盈亏坚决卖出', '止损规则', '{E2}{E3}', '坚决止损'),
            '仓位与资金': ('控制试错亏损，防止更大回撤', '资金管理', '{E2}{E3}', '风控保护'),
            '持仓与跟踪': ('跟踪股价运行并密切关注止损点与目标价位', '跟踪', '{E2}{E3}', '运行监控'),
            '加减仓': ('当股价达到目标价位时可以适当减仓锁定利润', '减仓操作', '{E3}', '目标减仓'),
            '止盈与退出': ('股价达到目标价位后减仓止盈，触及止损点坚决全部退出', '退出规则', '{E3}', '坚决退出'),
            '失效与放弃': ('若计划未设定好止损点与目标价位则不执行交易', '纪律', '{E2}', '放弃交易')
        },
        '严格执行事前设定的止损与目标价位规则，未披露数值留缺。{E2}{E3}',
        '同源K1与C1。{E2}{E3}',
        '正文原话字面支持，未明细节留缺。{E2}{E3}'
    )
)

C = (
    (
        '《股票大作手回忆录》老帕特里奇大势反思复盘',
        'SRC-002733',
        '2020年5月26日（源文口述录制背景）。{E0}',
        '股票大势与回忆录研读案例（源文口述）。{E0}{E1}',
        '读书反思与大势交易哲学复盘，非独立回测或交易流水。{E0}{E1}',
        '关联K-40024、S-20015',
        '仅增强稿可见；非独立成交记录',
        '口述记录研读回忆录第48页老帕特里奇教诲，反思大势判断正确却踩空的错误教训。{E0}{E1}',
        '记录大势与小波动辩证关系的教学反思。{E0}{E1}',
        '未提供单笔交易账单流水。{E0}{E1}',
        '不与第二源内容跨源拼接。{E0}{E1}',
        '口述与OCR证据{E0}{E1}'
    ),
    (
        '短线投资事前设定止损点与目标价位试错复盘',
        'SRC-000245',
        '2024年11月中旬（源文第401章等上下文）。{E2}{E3}',
        '短线个股投资标的（源文正文）。{E2}{E3}',
        '短线交易心得与风控案例复盘，非独立回测或交易流水。{E2}{E3}',
        '关联K-40025、S-20016',
        '仅增强稿可见；非独立成交记录',
        '作者分享投资心得：事前设定止损点与目标价位，到止损点坚决卖出，到目标价位适当减仓。{E2}{E3}',
        '记录短线试错策略中设定止损与止盈目标的风控执行流程。{E2}{E3}',
        '未提供可核验的逐笔交易凭据流水。{E2}{E3}',
        '不与第一源内容跨源拼接。{E2}{E3}',
        '正文原话字面证据{E2}{E3}'
    )
)

DOUBTS = [
    '主代理已通读SRC-002733 L1-317与SRC-000245 L1-1188全文。',
    'SRC-002733大部分口述语音行长度在300-400字之间，因禁止截断与无省略号铁律，仅采信符合≤300字完整行。',
    '严格遵守单段≤300字且不截断无省略号规则。'
]

RELATIONS = [
    'SRC-002733为回忆录研读，SRC-000245为短线妖股心得；各卡严守单源边界。'
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
