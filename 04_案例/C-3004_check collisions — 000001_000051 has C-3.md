# C-3004 check collisions — 000001_000051 has C-3001; 2251_2252 has C-2998,2999,3000; this batch's previous: C-3002, C-3003. So C-3004 free. ✓ (Will verify programmatically.)


Alright. Another check: my chosen SRC-000002 lines must be verified against the actual file, including that e.g. L120 "更像是过滤线指标而不表趋势" — note at 00:13:00 block L884 there's "更像家是过滤线指标而不衣起势" (OCR garbled) and L1035 "更像是过滤线指标而不衣超势" — hmm interesting: those are garbled variants. L120 is the clean one in the first block. ✓ (verifier: L120 must contain the exact string).

Wait, actually, let me double check L120's exact characters from the first read: "120: 更像是过滤线指标而不表趋势" — yes.

And L133: "133: 数值连续100不变为超买钝化" ✓. L134: "超过80是超买区域" ✓. L135: "进入超买卖出" ✓. L136 "容易卖飞不好", L137 "逆势交易".

L908 "脱离超买卖出" ✓ (00:13:00 block; nearby L909 "可以参考").

Hmm — should I use L908+L909 together? Can't (two lines). Use L908; mention "可以参考" as adjacent line in 疑点? Eh, or pick L909 "可以参考" as its own row? No budget. Hmm, "脱离超买卖出" alone loses the "可以参考" endorsement. That's important for stance! The card says: 脱离超买卖出（可参考）. Without "可以参考" evidenced... I could quote L908 and note in the card: 紧随其后的节点为“可以参考”（未列入证据）. Hmm, that references unevidenced text but as a location note. Alternatively swap: make the row quote "可以参考"? worse.

Hmm, what if I include L909 as an additional row and drop something else? Which row is most droppable now... E-65214 (更像是过滤线指标)? Hmm. Or E-65224 (20日线上不做)? If I drop E-65224, S-2207 becomes single-row (J值拐头向上买进). Hmm.

Let me re-derive the 20 rows one final time with a scoring pass:

Essential KDJ (must): L3561 (缺点: 被扫/做错) — K-31049a L120 (过滤线属性) — K-31049b [optional] L126, L127 (50区域) — K-31050 L121, L124 (短期/周线) — K-31051 L134, L133 (超买/钝化) — K-31052 L135, L908 (进入/脱离) — K-31053 L2422 (J值拐头向上买进), L2424 (20日线上不做) — S-2207 L3255 (kdj死叉卖出) — S-2208 [single row] L5402 (问财) — C-3004 [single row] = 14 rows.

Essential 0428: L7 (吊颈线) — K-31054 L16, L19 (走平/无斜率) — K-31055 L38 (三角) — K-31056 L25, L41 (通道/观望) — S-2209 = 6 rows. Total 20. ✓✓

So no room for L909 "可以参考" or L913 or L5624. Fine. In K-31053's card I'll present: 「进入超买卖出」被列为“容易卖飞不好→逆势交易”（E-65221; the follow-on nodes 容易卖飞不好/逆势交易 未列入证据 — hmm, again referencing unevidenced nodes...).

Ugh, the E-65221 row "进入超买卖出" alone doesn't carry the critique. Can I instead quote a line that contains the whole thing? The lines are separate. Hmm. What about using the 00:13:00 block variant? It has: L907 "基础用法" L908 "脱离超买卖出" L909 "可以参考" L910 "超买超卖区域" L911.. L914 "进入超卖买进" L915 "抄底容易失败" L917 "脱离超卖买进". Still single-line. Or the first block: L135 "进入超买卖出" L136 "容易卖飞不好" L137 "逆势交易".

Option: allocate rows L135 AND L136 (drop L120). Then K-31053 = [L135, L136, L908] (3 rows: 进入→卖飞, 脱离→可参考[no...]). Hmm, L909 still missing.

Alternatively re-purpose: drop E-65214 (L120) and use L909 "可以参考" as 2nd row of K-31053? Then K-31053 rows = L908 (脱离超买卖出) + L909 (可以参考) → but "可以参考" alone lacks subject (it refers to the preceding line). As evidence + card text: 「脱离超买卖出」下一条为「可以参考」（证据未逐字回源: "可以参考"）→ card states: 脱离超买卖出，原文标注“可以参考”. That works! And K-31049 then has L3561 + ... only 1 row. Hmm, K-31049 (缺点) with one row "kdj变化频繁容易短线被扫频繁做错" — acceptable (it captures 信号频繁→短线被扫→频繁做错). And add "更像是过滤线指标而不表趋势" to 疑点 as uncarded? Hmm, it's a nice line...

Decision: keep L120 as K-31049's second row (K-31049 richer), and for K-31053 use rows L135 ("进入超买卖出") + L908 ("脱离超买卖出"), and in the card write: 对「进入超买卖出」的评语（“容易卖飞不好”“逆势交易”）紧随其后（未列入证据，见疑点）...

Hmm, you know, I keep going back and forth. Let me just include L135, L136, L908 for K-31053 (3 rows) and drop L120 (E-65214). Final: K-31053 rows: L135 (进入超买卖出), L136 (容易卖飞不好), L908 (脱离超买卖出). Card explains: 进入超买卖出 → 容易卖飞不好（被批评）；脱离超买卖出（对照用法）。Missing "逆势交易" and "可以参考" — mentioned in 疑点 as adjacent nodes.

Hmm, but then K-31049 = 1 row (L3561). And overall rows: KDJ 14 still (swapped L120→L136). Fine. Or keep both L120 and L136 by dropping L2424? S-2207: L2422 + L2424... "20日线上不做" is arguably the weakest (ambiguous direction!). Drop L2424 → S-2207 single-row (J值拐头向上买进) hmm.

ENOUGH. Final commitment (20 rows):

E-65213 | SRC-000002 | 00:40:00 | L3561 | kdj变化频繁容易短线被扫频繁做错 | K-31049 §一句话定义 E-65214 | SRC-000002 | 00:00:00 | L120 | 更像是过滤线指标而不表趋势 | K-31049 §如何识别；§适用边界 E-65215 | SRC-000002 | 00:00:00 | L126 | 50以上强势区域 | K-31050 §一句话定义 E-65216 | SRC-000002 | 00:00:00 | L127 | 50以下弱势区域 | K-31050 §如何识别 E-65217 | SRC-000002 | 00:00:00 | L121 | k数值采样仅在10天以内 | K-31051 §如何识别 E-65218 | SRC-000002 | 00:00:00 | L124 | 升级到周线可以改善周期 | K-31051 §适用边界与失效 证据未逐字回源 | SRC-000002 | 00:00:00 | L134 | 超过80是超买区域 | K-31052 §一句话定义 证据未逐字回源 | SRC-000002 | 00:00:00 | L133 | 数值连续100不变为超买钝化 | K-31052 §如何识别 E-65221 | SRC-000002 | 00:00:00 | L135 | 进入超买卖出 | K-31053 §一句话定义 证据未逐字回源 | SRC-000002 | 00:00:00 | L136 | 容易卖飞不好 | K-31053 §如何识别 E-65223 | SRC-000002 | 00:13:00 | L908 | 脱离超买卖出 | K-31053 §如何识别；§适用边界 E-65224 | SRC-000002 | 00:28:00 | L2422 | J值拐头向上买进 | S-2207 §条件与动作（入场） E-65225 | SRC-000002 | 00:28:00 | L2424 | 20日线上不做 | S-2207 §条件与动作（环境过滤） E-65226 | SRC-000002 | 00:37:00 | L3255 | kdj死叉卖出 | S-2208 §条件与动作（止盈与退出） E-65227 | SRC-000002 | 00:56:30 | L5402 | 2021年3月5日周线周期kdj金叉2021年3月5日日线周期kdj金叉非新股股价大于ma20非次新股m | C-3004 §当时已知信息 E-65228 | SRC-000981 | 一 | L7 | 吊颈线要求下影线长于实体三倍以上，还须已有一定累积涨幅。 | K-31054 §一句话定义 E-65229 | SRC-000981 | 二 | L16 | 价格频繁穿越走平均线时，单次站上或跌破的意义降低。 | K-31055 §一句话定义 E-65230 | SRC-000981 | 二 | L19 | 均线没有斜率时，按其反复进出容易频繁止损。 | K-31055 §适用边界与失效 E-65231 | SRC-000981 | 三 | L25 | 指数仍在通道内部运行，通道下沿是必须遵守的风险边界。 | S-2209 §条件与动作（环境过滤） E-65232 | SRC-000981 | 四 | L38 | 直角三角形应在约三分之二位置以前突破，走到尖端则测距意义下降。 | K-31056 §一句话定义 ... wait I dropped S-2209's second row (L41)! Recount: I have 20 rows listed? Count: 65213..65232 = 20 IDs. Let me count my list: rows listed above: 65213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232 → but I listed 65228 (L7), 65229 (L16), 65230 (L19), 65231 (L25), 65232 (L38). That's 5 0428 rows, total = 15 KDJ + 5 = 20. And L41 (多看少动) is missing! So S-2209 has only L25 → S-2209 single row. Hmm. And K-31056 (三角) has L38 ✓. K-31054 (吊颈线) has L7 ✓. K-31055 has L16+L19 ✓.

Do I want L41? "没有合适标的或结构确认时，继续多看少动。" is a nice actionable line and would make S-2209 two-row. To fit, drop one KDJ row: candidates: E-65214 (L120 过滤线) or 证据未逐字回源 (L136 容易卖飞不好) or E-65225 (L2424). Hmm hmm.

Let me weigh: K-31053's critique needs "容易卖飞不好" (its the evidence that 进入超买卖出 is criticized). Keep. K-31049's "过滤线" line — distinctive knowledge (KDJ as filter indicator not trend indicator). Keep? S-2207's L2424 — ambiguous direction, low value. DROP L2424 (E-65225) and ADD L41! Then S-2207 = [L2422] single row... hmm, S-2207 then thin. Or keep L2424 and drop L136, letting K-31053 = [L135, L908]?

Hmm, what about dropping E-65214 (L120) instead — K-31049 keeps L3561 (its core: 信号频繁/被扫) and the 过滤线 point moves to 疑点 as uncarded? That's a shame.

Decision by value: L41 (多看少动 — actionable rule) > L120 (过滤线属性, knowledge but vague) ≈ L2424 (ambiguous). I'll drop L120. Then: K-31049 = [L3561] (1 row). K-31053 = [L135, L136, L908] (3 rows). S-2207 = [L2422, L2424] (2 rows). S-2209 = [L25, L41] (2 rows). Total: 65213 L3561, 65214 L126, 65215 L127, 65216 L121, 65217 L124, 65218 L134, 65219 L133, 65220 L135, 65221 L136, 65222 L908, 65223 L2422, 65224 L2424, 65225 L3255, 65226 L5402, 65227 L7, 65228 L16, 65229 L19, 65230 L25, 65231 L38, 65232 L41 = 20 ✓.

Card-row mapping: K-31049 ← E-65213 (1) K-31050 ← E-65214, E-65215 (2) K-31051 ← E-65216, E-65217 (2) K-31052 ← E-65218, 证据未逐字回源 (2) K-31053 ← 证据未逐字回源, E-65221, 证据未逐字回源 (3) S-2207 ← E-65223, E-65224 (2) S-2208 ← E-65225 (1) C-3004 ← E-65226 (1) K-31054 ← E-65227 (1) K-31055 ← E-65228, E-65229 (2) K-31056 ← E-65231 (1) S-2209 ← E-65230, E-65232 (2) Wait, I mismatched: E-65230 is L25 (通道) and E-65231 is L38 (三角) and E-65232 is L41. Let me redo: E-65227 = L7 (吊颈线) → K-31054 E-65228 = L16 (走平穿越) → K-31055 E-65229 = L19 (无斜率) → K-31055 E-65230 = L25 (通道下沿) → S-2209 E-65231 = L38 (三角) → K-31056 E-65232 = L41 (多看少动) → S-2209 ✓. Total rows 20; cards 12 (8K, 3S, 1C).

Hmm, only 1 C card. Range allows C-3004–C-3009. Fine — "宁可少建卡". But hmm, could I justify another C? E.g., C-3005 = "0428 当日盘面观察" needing L39 (创业板2.16%) — no budget. Skip. Note in 疑点.

Hmm, ok, wait. Let me reconsider ONE thing: is it wise to spend 1 row on C-3004 (问财 screening) rather than on, say, 多周期共振 (L5273)? The 问财 example is a dated, concrete, structured artifact — good for a knowledge base and it's the ONLY "case-like" material. Keep it. Also it provides the concrete parameters (周线金叉+日线金叉+非新股+股价>ma20+非次新股) — arguably a strategy fragment. Good value. Keep.

Now the cards' content. For each card, I must fill the template sections. Let me draft carefully, only using evidenced facts + clearly-marked "原文未明确".

Also note: card titles should be descriptive Chinese. And "> 来源：SRC-xxxxxx（第N课 课名）· 证据 E-xxxx" — for SRC-000002, 课名 = P1_KDJ (course type 其他 per user); for SRC-000981 = 第09课 0428解盘（日评）. I'll write: "来源：SRC-000002（P1_KDJ）· 证据 E-65213" and for cards with multiple evidence: "· 证据 E-65214、E-65215". Also add "来源立场" and "底本层级" lines.

For multi-source cards? None (I won't mix sources in one card). ✓ (except no).

Now draft each card:

K-31049 KDJ的信号频繁与被扫单（缺点）
