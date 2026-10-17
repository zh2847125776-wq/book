# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib

SOURCE_IDS = ('SRC-000129', 'SRC-000038')
COUNTS = {'K': 2, 'S': 2, 'C': 2, 'E': 4}
NEW_COUNTS = dict(COUNTS)
SUPPLEMENT_COUNTS = {'K': 0, 'S': 0, 'C': 0, 'E': 0}

root = Path(__file__).resolve().parents[2]
R = {}
E = []
L = []

for sid, name, lines, picks in [
    ('SRC-000129', 'SRC-000129_(增强版)专题_交易思变_背离的化解方法与实盘交易的影响.md', 7, [(3, '> 视频:')]),
    ('SRC-000038', 'SRC-000038_(增强版)P2_箱体3.md', 1884, [(1817, '> 均线是否站稳有均量可以衡量'), (1837, '> 你并无法预知一次突破的真假'), (1853, '> 箱体突破伴随boll发出相应信号')])
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
    for ln, pref in picks:
        i = ln - 1
        x = ls[i]
        E.append((sid, ln, x, pref))
        marks = [z for z in ls[:ln] if z.startswith(('**🎙', '**📝', '**📈'))]
        fr = [z for z in ls[:ln] if z.startswith(('## ⏱', '# '))][-1]
        col = '**🎙 语音转录(前后30s)**:' if (marks and marks[-1].startswith('**🎙')) else (marks[-1] if marks else '正文段落')
        L.append((fr, col))

K = (
    (
        '《背离的化解方法与实盘交易的影响》20秒短视频原稿无抽帧语音记录观察',
        'SRC-000129',
        '源文记录专题视频元数据“> 视频: `背离的化解方法与实盘交易的影响.mp4`,时长 0 分 20 秒”，因视频总时长仅20秒且处理方式为每30秒抽帧，故增强版原稿全文仅7行头部信息，未生成任何30秒抽帧、语音转录或课件OCR文字。{E0}',
        '仅如实记录原稿“视频: `背离的化解方法与实盘交易的影响.mp4`,时长 0 分 20 秒”及无正文的客观状态，绝不凭题名臆造任何背离化解方法，亦不跨源借用其他课程内容。{E0}',
        [
            '原稿头部记录“> 视频: `背离的化解方法与实盘交易的影响.mp4`,时长 0 分 20 秒”，全文共7行无抽帧与语音正文。{E0}'
        ],
        '原稿仅7行（152字符），无语音与OCR正文，所有具体规则严格留缺。{E0}',
        '关联S0与C0；不跨源混用。{E0}',
        '见S0与C0；20秒短视频原稿留白核查观察。{E0}'
    ),
    (
        '均线站稳有均量衡量、箱体突破无法预知真假与伴随BOLL信号观察',
        'SRC-000038',
        '源文课件OCR明确对比均线与箱体量能标准：“> 均线是否站稳有均量可以衡量”（而箱体无对应均量）；指出真假突破的认知前提：“> 你并无法预知一次突破的真假”；并给出箱体突破的指标共振特征：“> 箱体突破伴随boll发出相应信号”。{E1}{E2}{E3}',
        '仅记录≤300字完整原文字面的均线是否站稳有均量衡量、无法预知一次突破的真假及箱体突破伴随boll发出相应信号，不采信Vision推断，不补造交易流水。{E1}{E2}{E3}',
        [
            '课件OCR显示“> 均线是否站稳有均量可以衡量”。{E1}',
            '课件OCR显示“> 你并无法预知一次突破的真假”。{E2}',
            '课件OCR显示“> 箱体突破伴随boll发出相应信号”。{E3}'
        ],
        '本源无语音转录文字，全部条件严格以课件OCR字面为界，不作衍生推断。{E1}{E2}{E3}',
        '关联S1与C1；不跨源混用。{E1}{E2}{E3}',
        '见S1与C1；均量衡量均线、无法预知突破真假与BOLL信号配合。{E1}{E2}{E3}'
    )
)

S = (
    (
        '针对《背离的化解方法与实盘交易的影响》20秒无正文原稿保持全环节留缺的核查方法',
        'SRC-000129',
        '在梳理《背离的化解方法与实盘交易的影响》20秒短视频原稿、发现无30秒抽帧及语音正文时使用。{E0}',
        '核验原稿元数据确认视频时长仅0分20秒，在每30秒抽帧机制下未产生任何语音转录与OCR段落，严格遵循无依据不立卡则的原则，将十项交易生命周期环节全部如实留缺。{E0}',
        {
            '环境过滤': ('20秒短视频原稿核查环境（无抽帧正文）', '原稿核查', '{E0}', '20秒原稿核查'),
            '形态或指标形成': ('本证未明确', '—', '—', '留缺'),
            '确认': ('确认原稿仅含标题与20秒时长元数据，无具体规则文本', '原稿状态确认', '{E0}', '无正文确认'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('本证未明确', '—', '—', '留缺'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('本证未明确', '—', '—', '留缺'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('当原稿因时长仅20秒而无任何正文内容时，放弃凭题名主观脑补任何背离化解规则', '无正文放弃脑补', '{E0}', '严禁凭题名脑补')
        },
        '如实记录20秒短视频原稿无正文的事实，严守不脑补、不跨源拼接铁律。{E0}',
        '同源K0与C0。{E0}',
        '原稿仅7行无正文，全部未披露环节留缺。{E0}'
    ),
    (
        '承认箱体突破无法预知真假并结合均量与BOLL相应信号后知后觉应对的方法',
        'SRC-000038',
        '在应对箱体上下限突破、辨析真假突破及配合布林线（BOLL）指标操作时使用。{E1}{E2}{E3}',
        '区分均线与箱体：均线是否站稳有均量可以衡量，而面对箱体突破时必须清醒认识到“你并无法预知一次突破的真假”；不试图主观猜测定性，而是结合BOLL指标（箱体突破伴随boll发出相应信号）进行后知后觉的验证与纪律应对。{E1}{E2}{E3}',
        {
            '环境过滤': ('箱体震荡面临上下限方向突破及BOLL指标共振环境', '日线/多周期', '{E1}{E2}{E3}', '箱体突破与BOLL环境'),
            '形态或指标形成': ('均线站稳配均量衡量；箱体发生突破且伴随BOLL发出相应信号', '均量与BOLL信号', '{E1}{E3}', '箱体突破伴BOLL信号'),
            '确认': ('用均量确认均线是否站稳；用BOLL发出的相应信号辅助确认箱体突破有效性', '均量与BOLL确认', '{E1}{E3}', 'BOLL信号辅助确认'),
            '入场': ('本证未明确', '—', '—', '留缺'),
            '初始止损': ('鉴于“你并无法预知一次突破的真假”，入场后必须做好假突破的防守准备', '防假突破风控', '{E2}', '不预设立场防假突破'),
            '仓位与资金': ('本证未明确', '—', '—', '留缺'),
            '持仓与跟踪': ('在箱体突破后持续跟踪BOLL指标发出的相应信号变化', 'BOLL信号跟踪', '{E3}', '跟踪BOLL共振信号'),
            '加减仓': ('本证未明确', '—', '—', '留缺'),
            '止盈与退出': ('本证未明确', '—', '—', '留缺'),
            '失效与放弃': ('放弃“事先预知一次突破真假”的主观幻想；当箱体突破未伴随BOLL发出相应信号时保持警惕', '弃预知幻想', '{E2}{E3}', '放弃预知突破真假')
        },
        '揭示“均线站稳有均量衡量”与“无法预知一次箱体突破真假”的差异，确立箱体突破伴随BOLL发出相应信号的辅助验证法则。{E1}{E2}{E3}',
        '同源K1与C1。{E1}{E2}{E3}',
        'Vision推断不作规则，原稿无语音转录，未明环节留缺。{E1}{E2}{E3}'
    )
)

C = (
    (
        '《背离的化解方法与实盘交易的影响》20秒短视频原稿状态核查记录',
        'SRC-000129',
        '源文视频元数据记录（时长0分20秒）。{E0}',
        '背离化解方法专题短视频原稿（源文头部信息）。{E0}',
        '原稿元数据状态核查，非独立回测或交易流水。{E0}',
        '关联K-40368、S-20230',
        '仅增强稿可见；非独立成交记录',
        '原稿记录视频名为`背离的化解方法与实盘交易的影响.mp4`，时长0分20秒，全文共7行无抽帧画面、语音转录与OCR文字。{E0}',
        '如实存证20秒短视频原稿无正文内容的客观状态。{E0}',
        '原稿无任何实质正文内容与交易记录。{E0}',
        '不与第二源内容跨源拼接。{E0}',
        '原稿头部字面证据{E0}'
    ),
    (
        '2020年3月26日箱体突破无法预知真假与伴随BOLL发出信号课件教学复盘',
        'SRC-000038',
        '2020年3月26日23:17（源文课件界面时间戳）。{E1}{E2}{E3}',
        '均线均量、箱体真假突破与BOLL指标信号（源文课件OCR）。{E1}{E2}{E3}',
        '课件箱体3真假突破与BOLL共振理论教学复盘，非独立回测或交易流水。{E1}{E2}{E3}',
        '关联K-40369、S-20231',
        '仅增强稿可见；非独立成交记录',
        '课件思维导图指出“均线是否站稳有均量可以衡量”（而箱体无对应均量），强调在真假突破上“你并无法预知一次突破的真假”，并指出“箱体突破伴随boll发出相应信号”。{E1}{E2}{E3}',
        '记录箱体突破真假不可预知性及借助BOLL指标相应信号进行辅助判断的教学要点。{E1}{E2}{E3}',
        '未提供可核验的逐笔交易订单与盈亏统计流水。{E1}{E2}{E3}',
        '不与第一源内容跨源拼接。{E1}{E2}{E3}',
        '课件OCR字面证据{E1}{E2}{E3}'
    )
)

DOUBTS = [
    '主代理已通读SRC-000129 L1-7与SRC-000038 L1-1884全文。',
    'SRC-000129原视频时长仅0分20秒，增强版原稿全文仅7行（152字符）头部信息，无任何语音转录或OCR正文，严格按L3字面记录原稿状态，绝不凭题名编造规则。',
    'SRC-000038仅有课件OCR与Vision，无语音转录，严格以OCR字面为据，不采信Vision推断。',
    '严格遵守单段≤300字且不截断无省略号规则。'
]

RELATIONS = [
    'SRC-000129为20秒无正文短视频原稿状态记录，SRC-000038为箱体真假突破与BOLL信号配合教学课件；各卡严守单源边界。'
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
    for i, (eid, (sid, ln, e, pref)) in enumerate(zip(ids['E'], E)):
        p, ls = o[sid]
        assert ls[ln - 1] == e
        fr, col = L[i]
        r.e(int(eid[2:]), sid, pref, line_number=ln)
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
