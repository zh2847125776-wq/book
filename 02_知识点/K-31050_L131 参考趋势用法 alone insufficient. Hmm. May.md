# K-31050 L131 "参考趋势用法"?? alone insufficient. Hmm. Maybe merge K-31050 into... no. 1 row: L126 "50以上强势区域"? The card would need 50分界 both sides. Ugh.


Hmm, this is really tight. Alternative: drop some SRC-000981 K cards (K-31055/56) and put 0428 content into fewer cards? But SRC-000981 deserves coverage (it's a whole source with clean sentences).

Alternative: reduce the KDJ card count by merging:

Merge K-31050 (区域+交叉) & K-31051 (短期/周期升级)? Different topics. Hmm.
Merge K-31053 (超买超卖触发方式) into K-31052 (超买超卖与钝化) as one card "KDJ超买超卖：区域、钝化与买卖触发（进入 vs 脱离）" — rows: L134 (超买80), L133 (钝化100), L135 (进入超买卖出), L908 (脱离超买卖出), L913 (低于20超卖), L912 (钝化0), L915 (抄底失败) = up to 7 rows, but could trim to 4: L134, L133, L135, L908 + maybe L915. Merged card = fewer cards, similar rows. Cards count isn't the problem; ROWS are. So merging doesn't save rows... but it does save "minimum 1 row per card" overhead. With 20 rows and, say, 10 cards, average 2 rows/card.

Let me now decide a lean card set (target 10 cards) & allocate exactly 20 rows:

KDJ (SRC-000002) — 5 cards, 12 rows: K-31049 KDJ的缺点与适用性 [rows: L3561, L120] (2) K-31050 KDJ的强弱区域与交叉信号 [rows: L126, L127, L131] (3) K-31051 KDJ的短期属性与周期升级 [rows: L121, L124] (2) K-31052 KDJ超买超卖与钝化 [rows: L134, L133, L913] (3) K-31053 超买超卖触发方式（进入/脱离） [rows: L135, L908] (2) ← hmm or merge into K-31052. total 12 rows for 5 cards. But then K-31054 背离 dropped, S-2207/2208/2209 and C-3004 still need rows → over budget again (12 + 4.5 ≥ 20 total leaves 8 for 0428(6-7) + S/C(4-5)). Doesn't fit.

OK let me flip the approach: decide the 20 rows FIRST (the strongest verbatim material across both sources), then define cards to match. Cards: 9 K + 6 S + 6 C slots, but I'll use fewer.

Candidate rows ranked by self-containedness & importance:

SRC-000981 (clean sentences — high value):

L7 吊颈线要求下影线长于实体三倍以上，还须已有一定累积涨幅。
L8 当时市场已调整较久，不具备该前置条件，不能仅凭长下影判定。 (good! rule application)
L11 单根或少数K线形态只作参考，不能独立提供完整交易架构。
L12 买卖和止损依据应来自均线系统或更大的形态边界。
L16 价格频繁穿越走平均线时，单次站上或跌破的意义降低。
L19 均线没有斜率时，按其反复进出容易频繁止损。
L25 指数仍在通道内部运行，通道下沿是必须遵守的风险边界。
L27 当日为高点回落后的第三日，后续是否到达下轨仍待验证。
L28 MACD在零轴下方连续两根红柱缩短，反弹力量减弱。
L38 直角三角形应在约三分之二位置以前突破，走到尖端则测距意义下降。
L39 创业板指数当日约涨2.16%，权重与中小盘表现仍有差别。
L41 没有合适标的或结构确认时，继续多看少动。
L18 近期主要核心均线是六十日线，二十日线的回测已经不精准。
L17 不能因为今日收盘站上二十日线，就直接恢复买入。

SRC-000002 (OCR fragments): 15. L3561 kdj变化频繁容易短线被扫频繁做错 16. L126 50以上强势区域 / L127 50以下弱势区域 17. L121 k数值采样仅在10天以内 / L124 升级到周线可以改善周期 18. L134 超过80是超买区域 / L133 数值连续100不变为超买钝化 19. L908 脱离超买卖出 / L135 进入超买卖出 20. L2422 J值拐头向上买进 / L2414 突破100以后向下拐头卖出 21. L2424 20日线上不做 / L5254 20日线下不做 / L3560 20日线走平无明显方向 22. L5273 多周期共振 / L3562 转换到下一周期为3的倍数 23. L5402 2021年3月5日周线周期kdj金叉...(问财条件) 24. L2413 钝化不可怕越钝化单边行情越激烈 25. L120 更像是过滤线指标而不表趋势

That's ~25 candidates for 20 slots. Need to cut ~5-6. Hmm. And cards must map.

Let me allocate by CARD first with target rows, prioritizing coverage of both sources:

K cards (7): K-31049 (KDJ缺点: 信号频繁/被扫; 过滤线属性) — rows: [15 L3561], [25 L120] → 2 K-31050 (KDJ强弱区域与交叉) — rows: [16a L126], [16b L127], [L131 参考趋势用法] → 3 K-31051 (KDJ短期属性与周线升级) — rows: [17a L121], [17b L124] → 2 K-31052 (KDJ超买超卖与钝化) — rows: [18a L134], [18b L133], [24? L2413] → 2-3 K-31053 (进入/脱离超买超卖) — rows: [19a L135], [19b L908] → 2 K-31054 → drop? or make it 吊颈线 card...

Hmm wait: I have 9 K slots; using 7 K cards: the 0428 ones: K-31xxx 吊颈线前置条件 — rows [1 L7], [2 L8], [3 L11] → 3 K-31xxx 走平均线的信号衰减 — rows [5 L16], [6 L19], [13 L18]? → 2 K-31xxx 直角三角形突破位置 — rows [10 L38] → 1 K-31xxx 通道下沿风险边界 — rows [7 L25] → 1 (or fold into S-2211)

Hmm, that's a lot of cards. Let me count total: if I make 7 KDJ+0428 K cards + 4 S + 2 C = 13 cards; rows: 2+3+2+3+2 (KDJ K) = 12 for 5 KDJ K cards... plus 0428 K cards 3 cards (3+2+1=6 rows) = 18 rows for 8 K cards; then 2 rows left for 4 S + 2 C cards — IMPOSSIBLE.

So I MUST reduce cards drastically, or reuse rows across cards (a row can serve a K card and an S card!). Reuse is the key: e.g., row L7 (吊颈线) serves K card & any S card referencing it. Since 用途 column can list multiple cards, rows aren't consumed per card. The real constraint is only 20 rows total; cards can share.

So: choose 20 rows, then build cards that each cite ≥1 row, allowing sharing. With smart sharing, I can support ~12-14 cards from 20 rows.

Number of cards: let me settle on: K (8): K-31049 KDJ缺点（信号频繁/被扫/过滤线）← rows L3561, L120 K-31050 KDJ强势弱势区域与交叉参考趋势 ← rows L126, L127, L131 K-31051 KDJ短期属性与周线升级 ← rows L121, L124 K-31052 KDJ超买超卖区域与钝化 ← rows L134, L133, L913 K-31053 超买超卖的触发（进入 vs 脱离）← rows L135, L908 K-31054 吊颈线的前置条件与参考地位 ← rows L7, L11 K-31055 走平/无斜率均线不提供有效信号 ← rows L16, L19 K-31056 直角三角形突破位置与测距 ← row L38 K-31057 通道下沿作为风险边界（0428） ← row L25 → that's 9 K cards. Rows used: 2+3+2+3+2+2+2+1+1 = 18. Only 2 left for S and C!! NO.

I need to cut K cards to ~6 and rows to ~12 for K, leaving 8 for S/C.

Cut decisions (which KDJ/0428 knowledge is least essential or least supported):

K-31051 (短期属性/周线升级): keep — good, 2 rows (L121, L124). Actually merge into K-31050? "KDJ的周期与区域用法"? Meh. Keep separate; 2 rows.
