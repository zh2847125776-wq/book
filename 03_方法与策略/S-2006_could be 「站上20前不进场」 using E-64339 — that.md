# S-2006 could be 「站上20前不进场」 using E-64339 — that's inside S-2002. Adding cards using the same evidence is allowed but adds redundancy; user prefers fewer cards. However, having S cards only up to S-2005 while the range allows more is fine ("严格只用这些，不许越界" = don't go beyond).


Hmm, but wait: is it better to split S-2002? It currently bundles: (a) 不进场的门槛（站上横盘区间下线、站上20、20穿过去、5穿20、站上60）、(b) 空仓过节/51尾盘再买、(c) 第一次反弹决定颈线. Could split into S-2002「持股过节的门槛（空仓过节的判定）」 and S-2006「第一次反弹决定颈线、第二次反弹才是标准」. The latter is a 观察信号/规则 fragment. Evidence already in list (E-64342). That's legitimate and improves granularity. Hmm, but is 「第一次反弹决定颈线」 complete enough as a method? It's a 完整度: 只给方向（决定颈线）; 判据 unclear → 参数原稿未明确. I kept it as K-30727 anyway. Making both a K and an S for the same content = duplication. Better: keep K-30727 as knowledge, and S-2002 references it. OK.

So 4 S cards. Let me consider adding S-2006 「指数站在20线下不操作（站上20线上头才操作）」(2175) — needs evidence not in list. Could I swap? Which current evidence is least valuable? Candidates: E-64351 (创指没啥可讲, 90字) — cited by S-2004 and C-2820. Its content: 上证多线融合中位线没拦住继续突破、创指中位线没到就掉下来. It supports S-2004's "不推荐操作创业板指数"... hmm, actually the "不推荐操作创指" wording comes from another quote (112字) not in the list; E-64351 supports "创指弱"。 C-2820 needs it as 当时已知信息? C-2820 could instead cite E-64352 (1268) and E-64347? Hmm.

Trade: swap E-64351 (创指啥可讲) for the 20线下不操作 (81)? Then S-2004 loses 创指 evidence, C-2820 loses 当时已知信息 (could cite E-64352 + maybe E-64350?). Hmm, marginal.

Actually is 「指数站在20线下不操作」 more valuable than 「创指没啥可讲（多线融合中位线没到）」? The former is a crisp trading rule from 2175 二 section; the latter is a market observation used in C-2820/C-2819. I think the 20线下不操作 rule is more valuable as a method (S-2006: 指数站位过滤). But then S-2004's "不做创指/中小市值" rests on E-64346 (流通市值大于100亿) + E-64350 (注册制) — good enough; the "不选创指" part would lack direct evidence... K-30729 (注册制与市值) also cites E-64346/64350.

Hmm. Let me think about the 60-分钟小周期 content too: "小周期站上多空线 → 围绕它横盘整固；60分钟到极致要回调；你选的股要比指数强" — that's 2175 五条口诀③. Currently not covered except... not at all! That's a notable gap. Its natural card: S「小周期（60分钟）到极致要回调、要求选的股比指数强」 or K「多空线/60分钟极致」. Evidence would be the 115字 or 102字 quotes.

Ugh, the cap. I have 20 slots and more content. Let me do a final value ranking of "content blocks" and pick the best 20 evidence to maximize coverage:

2174 blocks:

二合一迫近 (multi) — MUST
缺口单论无意义/叠加才重视 — high
跌多反弹命名 — high (part of 实体变小 quote)
实体递减/力量衰减 — MUST
全A跌多弹多（因跌得多所以弹得多）— medium-high
逃跑机会/主力仁慈 — MUST
普通投资者没法参与 — high
5%/10%/20% + 站上横盘下线/20/20穿过去 — high (门槛)
宁德站上向下60 — high (case)
未完成20穿60黄金交叉/打漏60照样看跌 — high
第一次反弹决定颈线/第二次才是标准 — high
3327对3313差14点 — MUST (case)
开空思路=再破较快均线/诱多 — high
空仓过节/51尾盘再买 — MUST
100亿市值选股 — high
60分钟负乖离率修复/空头排列不会改变 — medium
周线3234/本周最低3229/下周一绿柱一 — medium
科创板块：序列第六、50线没站上、60线没测、测距没满足跌幅 — high (2174 部分)
49亿集合竞价超级放量没涨太多 — medium (opening observation)
分时两小时没变化「反弹不能忙」— medium (V1 core, but we don't have direct quote? Let me check: line 8 block? The 反弹不能忙 phrase appears in line 4/9/10 but the direct quote line 8's first block—let me check whether line 8 has a block with "反弹不能忙". Earlier extraction: line 8 keys: 49个亿 (super auction), 迫近压力, 缺口, 实体. Hmm "反弹不能忙" might be in another block of line 8. Let me check all blocks of line 8.)

2175 blocks: 21. 三极分化 — MUST 22. 突破3326/20/横盘高点 — MUST 23. 看多结构 — MUST 24. 两个瑕疵（5穿20死叉、绿柱3360/3351未突破）— high 25. 注册制/市值 — high 26. 指数站在20线下不操作/连续两天站上可做 — high 27. 2600对2100涨跌比 — medium-high 28. 3223底线 — medium-high 29. 小周期站上多空线→围绕整固 — medium 30. 60分钟到极致要回调 / 比指数强 / 600开头 — high 31. 周线多空线没拐头（三五周七八周）— medium 32. 银行2.8/正压凿 — high (五条④) 33. 科创50跌2.4/跌深反弹/满足跌幅 — high (五条④) 34. 创指没啥可讲/50线上反回测 — medium 35. 全A 1268 — MUST (五条⑤) 36. 倒压凿加速下跌三到四个周期 — medium 37. 空头排列被套逢高减仓清仓 — high 38. 不追高（中特估、三五年没法操作）— high 39. 强者恒强/有的话吃没有甭追 — medium 40. 中石化50%/元旦组合传媒股涨停 — medium

Way more than 20. So I accept partial coverage and document the gap. Priority: "must" items (9) + best highs. Let me finalize 20 with the goal of supporting a coherent card set of ~15 cards:

Final 20 (with assigned 用途):

迫近二合一 (96) [2174 §1] — K-30723, C-2816
缺口单论 (119) [2174 §1] — K-30723
实体变小 (119) [2174 §1] — K-30724, C-2816
逃跑机会 (69) [2174 §2] — K-30725, C-2816
没法参与 (109) [2174 §2] — K-30725, S-2002
5%/10%/20%门槛 (128) [2174 §2] — S-2002
宁德站上向下60 (84) [2174 §3] — K-30726, C-2818
未完成20穿60黄金交叉 (127) [2174 §3] — K-30726, C-2818
第一次反弹决定颈线 (123) [2174 §3] — K-30727, S-2002
3327对3313 (73) [2174 §4] — C-2817
开空思路/诱多 (123) [2174 §4] — K-30728, S-2003
空仓就可以了 (92) [2174 §4] — S-2002, C-2817
100亿市值/不选创指中小市值 (104) [2174 §4] — S-2004, K-30729
三极分化 (142) [2175 §1] — K-30730, C-2819
突破3326 (101) [2175 §1] — C-2819
看多结构 (124) [2175 §1] — K-30731, C-2819
两个瑕疵 (205) [2175 §1] — C-2819
注册制/市值 (124) [2175 §2] — K-30729, S-2004
1268 (132) [2175 §5] — C-2820
逢高减仓清仓 (133) [2175 §5] — S-2005

Count 20. Coverage check again: K: 30723(1,2) ✓; 30724(3) ✓; 30725(4,5) ✓; 30726(7,8) ✓; 30727(9) ✓; 30728(11) ✓; 30729(13,18) ✓; 30730(14) ✓; 30731(16) ✓ = 9 K cards, all with evidence ✓ (fits exactly 30723–30731!) S: 2002(5,6,9,12) ✓; 2003(11) ✓; 2004(13,18) ✓; 2005(20) ✓ = 4 S cards ✓ C: 2816(1,3,4) ✓; 2817(10,12) ✓; 2818(7,8) ✓; 2819(14,15,16,17) ✓; 2820(19) ✓ = 5 C cards ✓

Nice, this is balanced: 9K + 4S + 5C = 18 cards, 20 evidence.

Hmm, C-2819 has 4 evidence, C-2820 only 1, C-2821 dropped (银行/科创). And S-2005 only 1 evidence. And missing: 20线下不操作, 2600对2100, 3223, 比指数强/600开头, 银行/科创, 不追高, 全A跌多弹多, 周线, 科创板块2174, 49亿, 负乖离率修复.

Alternatively, rebalance: drop E-11? No, K-30728 needs it. Hmm, what if K-30728 (诱多结构) merged into S-2003 → frees E-11? No — E-11 would still be carded as S-2003's rule (S-2003 IS the 开空思路). K-30728 is the concept "诱多结构". Dropping K-30728 frees no evidence. So dropping K cards doesn't free evidence slots. Only dropping evidence items frees slots.

So the question is: are there any of the 20 I'd swap for higher-value uncovered content? Let me weigh:

E-17 两个瑕疵 (205) [C-2819]: covers 5穿20死叉 + 绿柱3360/3351. C-2819 would still have 3 evidence without it. Swap candidate.
E-6 5%/10%/20% (128): covers 门槛+概率. S-2002 would still have 3. Swap candidate.
E-2 缺口单论 (119): K-30723 would still have 1. Swap candidate.

Candidates to include: A) 指数站在20线下不操作 (81) → S-2006 新卡 B) 银行2.8 + 科创2.4 (131+88=2 slots) → C-2821 新卡 C) 比指数强/600开头 (2175) → S card D) 2600对2100 (126) → K-30729 second evidence E) 不要去追高/三五年 (102/114) → S-2005 second evidence F) 不推荐操作创指 (112) → S-2004

Given 2175's 五条口诀 ④ (银行2.8/科创2.4) is claimed as a key contribution of the lesson, and it's a clean case → I lean to include B (2 slots). Then drop which 2? Drop E-17 (两个瑕疵) and E-6 (5%/10%/20%+门槛)? Hmm, the 门槛 content ("你得把横盘区间下线站上去、你得把20站上去、20得穿过去") is arguably THE most actionable sentence in 2174 for a strategy card. I'd rather keep it and drop something else.

Alternatively drop E-18 (注册制 124)? It's cited by K-30729 and S-2004 — dropping it leaves K-30729 with E-13 (100亿) only, and S-2004 with E-13 only. Hmm, but 注册制 rationale is valuable.

Or drop E-15 (突破3326, 101)? C-2819 would lose the core "突破" fact... no.

Or drop E-5 (没法参与 109)? K-30725 keeps E-4; S-2002 keeps 3. Then include A (20线下不操作 81) for a new S-2006. Hmm, that swaps 重复的风险警示 for a distinct 2175 rule. Actually E-5 is quite similar to E-4 in content (逃跑机会 theme). Dropping E-5 loses "再次逃跑的机会，而不是让你进场...这个风险因素你一定要搞清楚" — decent but partially redundant with E-4.

And drop E-17 (两个瑕疵 205)? That loses 3360/3351 数字 and 5穿20死叉瑕疵. Hmm, the 3351/3360 numbers are notable (2175 五条 mention "3360对3351").

Ugh. OK, decision time. I'll optimize for: (i) each of the 12 "五条口诀" of both lessons gets representation; (ii) balanced card set.

2174 五条: ①反弹不能忙/49亿 → not carded (I don't have a 反弹不能忙 direct quote necessarily; 49亿 is available at 69字). ②二合一 ✓ (E1,E2). ③忘了五连阴/实体变小 ✓ (E3). ④逃跑机会 ✓ (E4,E5). ⑤诱多/21号阴线压 ✓ (E11, partially). 2175 五条: ①三极分化/突破3326成看多结构 ✓ (E14,E15,E16). ②市值大小/2600对2100/600开头 — partially (E13, E18; missing 2600对2100). ③小周期站上多空线/60分钟极致/比指数强 — ✗ missing. ④银行2.8/科创2.4 — ✗ missing. ⑤全A1268/中特估别追高 — partially (E19; missing 追高).

Missing blocks: 49亿, 2600对2100, 小周期/比指数强, 银行/科创, 不追高. That's a lot of 五条口诀 material. To include these I'd need ~5-6 more slots. So I must cut deeper into cards.

Radical option: reduce C card evidence usage (cases can cite fewer). E.g.:

C-2816 could cite just E1+E3 (drop E4 from it) — doesn't free slots (E4 still needed by K-30725).
