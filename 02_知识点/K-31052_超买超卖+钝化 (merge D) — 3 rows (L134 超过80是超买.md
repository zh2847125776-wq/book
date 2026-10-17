# K-31052 超买超卖+钝化 (merge D) — 3 rows (L134 超过80是超买区域; L133 数值连续100不变为超买钝化; L913 低于20是超卖区域; maybe L911 超过三天为低档钝化注意变化). Choose rows: L134, L133, L913, L911 → 4 rows covering both sides; hmm. Or L134, L133, L913 (3 rows) and skip low-side 钝化 mention? The card can say: 超卖侧对应条目为"低于20是超卖区域"等（E-…）… if I mention "等" without evidence row for L911/L912, is that a problem? The evidence list must contain evidence for statements in cards. I'd write only what's evidenced: "超过80是超买区域"(L134), "数值连续100不变为超买钝化"(L133), "超过三天为高档钝化注意变化"(L132), "低于20是超卖区域"(L913), "数值连续0不变为超卖钝化"(L912), "超过三天为低档钝化注意变化"(L911). Six facts → 6 rows is too many; trim facts to 4 rows: L134, L133, L913, L912. Then card states those 4 + notes "高档钝化注意变化的时长为‘超过三天’（对应超卖侧为‘超过三天为低档钝化注意变化’）" — without evidence. Hmm, risky. Just stick to what's evidenced; or include L132 and L911 as well (6 rows) if budget allows. Let's see overall budget.


Let me try a full allocation with 20 rows and count cards:

Row plan (tentative, subject to final):

E-65213: SRC-000002, L3561, "kdj变化频繁容易短线被扫频繁做错" — 用途: K-31049 §一句话定义；S-2212? no. → K-31049.
E-65214: L120, "更像是过滤线指标而不表趋势" — K-31049 §如何识别/适用边界.
E-65215: L126, "50以上强势区域" — K-31050.
E-65216: L127, "50以下弱势区域" — K-31050.
E-65217: L131, "参考趋势用法" — K-31050 §如何识别（交叉用法需参考趋势）.
E-65218: L121, "k数值采样仅在10天以内" — K-31051.
证据未逐字回源: L124, "升级到周线可以改善周期" — K-31051 §适用边界/修正.
证据未逐字回源: L134, "超过80是超买区域" — K-31052.
E-65221: L133, "数值连续100不变为超买钝化" — K-31052.
证据未逐字回源: L913, "低于20是超卖区域" — K-31052.
E-65223: L912, "数值连续0不变为超卖钝化" — K-31052.
E-65224: L135, "进入超买卖出" — K-31053.
E-65225: L136, "容易卖飞不好" — K-31053.
E-65226: L908, "脱离超买卖出" — K-31053.
E-65227: L915, "抄底容易失败" — K-31053. (+L917 脱离超卖买进? skip)
E-65228: L919 "股价创新高"... hmm and L920/L922. For K-31054 背离: L920 "指标不创新高" + L922 "指标背离" + L924 "指标不创新低"? 2 rows: E-65228 L922 "指标背离"; E-65229 L924 "指标不创新低". Then card states 定义 + 高低两侧依据 (创新高/不创新高 from L919/L920 not evidenced...). Hmm.

This is ballooning: 16 rows already for 6 K cards, leaving 4 rows for 3 more K + 5 S + 2 C. NOT viable. Need to cut.

Revised approach: fewer cards, more focus. Let me cut aggressively and merge:

FINAL FINAL plan (10 cards, 20 rows):

K cards (7):

K-31049 KDJ的两类缺点：信号频繁被扫单；单边行情过度交易（含"更像是过滤线指标而不表趋势"）— rows: L3561, L120 [2 rows]
