# K-30741 uses A+B (2). Could merge A+B into one span? They're adjacent? Line 8 blocks: ... block on 权重分层 then block on 1%. Are they adjacent? Order in line 8: (1) 好各位同学...成也萧何 (2) 我们看今天黄线最惨 (3) 逻辑非常简单 (4) 那我们一起来看看...创业板能不能轮动 (5) 那创业板指数能不能在上证指数倒了以后...不值一提 (6) 大家一定要注意、咱们在所有的均线系统... (7) 那它只是分时图涨了个1%... (8) ... Let me verify adjacency of (6) and (7) and whether combined ≤300. Block (6) ~150 chars, block (7) ~60 chars → combined ~215 ✓. If adjacent (separated by ；), I can use ONE evidence instead of two! Similarly other pairs.


Let me check line 8 of 2178 for adjacency of blocks 5,6,7 (1% quote, 权重 quote, 分时1%日线无变化 quote). If 5&6&7 are adjacent: combined might be ~330 > 300. 5 alone ~120, 6 ~150 → 5+6 = ~275 ✓ maybe. Then I could use one evidence covering 空头排列不值一提 + 权重分层. Hmm, but then the card's other claim (分时1%、日线无变化) unsupported... I could pick 6+7 (~215) covering 权重分层 + 分时1%无变化, and drop 5 (不值一提). The card would then be "权重分层与分时波动" ✓. That saves 1 slot (from 2 → 1) → freeing a slot for Q or U!

Similarly, check other possible consolidations:

D+E (破底翻构成 & 逆势) are adjacent blocks ("那我们再退一步讲...这根本就不是破底翻" then "我们再退一步、大小咱也不管了...那它也不行") → combined length? D ~200, E ~120 → 320 > 300. Hmm. Maybe D alone (~200) and E (~120) separate. Or E+next block (破底翻价值) ~? E ~120 + 价值 block ~150 = 270 ✓ — but 价值 block is a different claim (跌充分后抄底). Actually combining E (逆势) + 价值 would support K-30743's 适用边界 nicely in one evidence. Then D separate. Still 2 evidences for K-30743.

F + G (乖离 + 均线开口) adjacent? Order: "那现在问题就变了...首先最简单的、我们要看看它的正负乖离率有没有扩大过，是吧" (F) then "你比如说我们看一个股票...这才叫跌的多，是不是" then "但是这个总归说的也不明显，是吧，还有什么办法、看均线...就是这么来回切换" (G1) then "我们现在问题就来了、这均线算是发散过没有...没有意义、没有价值" (G2). So F and G are separated by 1 block. Combined F + (F2) = ? F ~90 + F2 ~150 = 240 ✓ (covering both 乖离率 measures: 没扩大不叫充分 / 扩大到极值又捞回来才叫跌得多). Then G2 (~140) separate → but budget. Hmm: Option: E-64379 = F+F2 (~240) covering 跌得充分-乖离 measure; E-64380 = G2 covering 均线开口 measure. That's 2 evidences for K-30744 — same as before (F alone + G2). No savings, but better coverage. OK.

Let me now actually check lengths and adjacency with code, then finalize. Let me be efficient: extract candidate spans with lengths, and pick.

Final target: 20 evidence items that support 19-21 cards.

Let me define the cards finally (aiming 9K + 5S + 5C = 19):

K (9):

K-30741 权重分层与分时波动（均线系统/形态结构主导；创指分时1%无意义）
