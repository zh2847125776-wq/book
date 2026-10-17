# S-2212 ? Maybe unused, or "KDJ的收盘与盘中处理"("盘中变化？"/"收盘变化"/"ma20盘中止损类比没有"/"等着收盘可能扩大了亏损"/"更像是过滤线指标而不表趋势") — that's a coherent topic: KDJ/均线的盘中与收盘取舍. Evidence: L115 "盘中变化？"; L116 "收盘变化"; L118 "收盘为准？"; L119 "等着收盘可能扩大了亏损"; L120 "更像是过滤线指标而不表趋势". As S-2212 "KDJ用于盯盘时的收盘确认与过滤属性（缺点）". Hmm, but the content is just labels/questions, no decided rule → 完整度：只给名称缺参数 / 待验证组合方案. Could fold into K-31049 instead. Since K-31049 is "缺点", add L120 as a row used by K-31049. Hmm.


Let me now just carefully allocate the 20 evidence rows. I'll aim to satisfy every card and use exactly 20 rows (E-65213…E-65232).

Draft allocation (rows 1–20):

SRC-000002 (say 13 rows):

E-65213 | SRC-000002 | 00:55:30 L5263 | "kdi变化频繁容易短线被扫频繁做错" → K-31049 §一句话定义. Hmm, but L3561 has the same sentence with "kdj" spelled correctly: "kdj变化频繁容易短线被扫频繁做错". Which to use? Use L3561 (correct spelling) for the card, and maybe mention L5263's "kdi" spelling in 疑点 (as OCR typo). But then L5263's typo isn't in evidence list... it's a 疑点 about transcription, fine to mention without needing it as card evidence? The 疑点 section is separate from cards; the rule says evidence for statements cited in cards. The 疑点 section is explicitly allowed to list suspicious numbers. I think mentioning the "kdi" variant in 疑点 is OK. Actually hmm, to be safe I could include it as an evidence row (E-65xxx) with 用途 "K-31049 §数字与证据；底本层级与疑点". The 用途 column says "哪张卡的哪一节" — pointing to 疑点 section might be odd but I did "S-2179 § 版本分歧与证据限制" before. Let me keep it simple: use L3561 as evidence; list the kdi-spelling variant in 疑点 as an OCR异写 (it's a duplicate line, not card basis)...

Hmm, but strictly: "每张卡引用的证据都要在最后的证据清单里逐条列出" — 疑点 section isn't a card; fine.

Hmm, wait. Actually there's a subtlety: are lines L3561 and L5263 REALLY identical? Earlier output: "L5263: kdi变化频繁容易短线被扫频繁做错" and "L3561: kdj变化频繁容易短线被扫频繁做错". Yes different. OK.

E-65214 | L114 "不如拿着不动挣得多" → K-31049 §如何识别. Hmm, weak. Alternatives: "单边多头行情严格遵守KDJ"(L112)? Even weaker alone. Or use L113 "过度交易"? Very weak. Keep L114? Hmm. Or use L120 "更像是过滤线指标而不表趋势" for K-31049 §适用边界 (KDJ被描述为过滤线指标而非趋势指标). That's more substantive. Let me use L120 for K-31049. And maybe L124 "升级到周线可以改善周期" is for K-31051. OK: E-65213: L3561 kdj变化频繁容易短线被扫频繁做错 → K-31049 §一句话定义 E-65214: L120 更像是过滤线指标而不表趋势 → K-31049 §如何识别/§适用边界 Also maybe E-65215: L124 升级到周线可以改善周期 → K-31051 §一句话定义; E-65216: L121 k数值采样仅在10天以内 → K-31051 §如何识别. (2 rows for K-31051.)
E-65217: L126 50以上强势区域 → K-31050
E-65218: L127 50以下弱势区域 → K-31050
证据未逐字回源: L131 参考趋势用法 → K-31050 (hmm; better: L128 金叉行情相对转强 for 如何识别, L131 for 适用). Let me pick 3 rows: L126, L127, L131? or L128/L130? The "参考趋势用法" line is important (KDJ交叉用法要参考趋势). I'll do: L126 (50以上强势区域), L127 (50以下弱势区域), L131 (参考趋势用法). Hmm but then 金叉/死叉转强转弱 unlisted. Budget... I'll do L126, L127, L128, L131 = 4 rows? That's heavy for one card. Let me instead pick L126, L127, L131 (3 rows) and mention 金叉/死叉转强 in card text? No—can't without evidence. Ugh.

Alternatively merge K-31050 with the 金叉/死叉 line: card "KDJ的强弱区域与交叉信号" with rows: L126, L127, L128, L131 → 4 rows. Meanwhile K-31052 超买超卖 uses L134/L133/L913 (3 rows). Let me count the budget again with a spreadsheet mindset.

Total rows available: 20. Cards: 9 K + ~5 S + ~2 C = 16 cards; average ~1.25 rows each. Tight. Must consolidate!

Consolidation strategy: merge related K cards to reduce count, e.g.:

K-31052 超买超卖+钝化 (merge D) — 3 rows (L134 超过80是超买区域; L133 数值连续100不变为超买钝化; L913 低于20是超卖区域; maybe L911 超过三天为低档钝化注意变化). Choose rows: L134, L133, L913, L911 → 4 rows covering both sides; hmm. Or L134, L133, L913 (3 rows) and skip low-side 钝化 mention? The card can say: 超卖侧对应条目为"低于20是超卖区域"等（E-…）… if I mention "等" without evidence row for L911/L912, is that a problem? The evidence list must contain evidence for statements in cards. I'd write only what's evidenced: "超过80是超买区域"(L134), "数值连续100不变为超买钝化"(L133), "超过三天为高档钝化注意变化"(L132), "低于20是超卖区域"(L913), "数值连续0不变为超卖钝化"(L912), "超过三天为低档钝化注意变化"(L911). Six facts → 6 rows is too many; trim facts to 4 rows: L134, L133, L913, L912. Then card states those 4 + notes "高档钝化注意变化的时长为‘超过三天’（对应超卖侧为‘超过三天为低档钝化注意变化’）" — without evidence. Hmm, risky. Just stick to what's evidenced; or include L132 and L911 as well (6 rows) if budget allows. Let's see overall budget.
