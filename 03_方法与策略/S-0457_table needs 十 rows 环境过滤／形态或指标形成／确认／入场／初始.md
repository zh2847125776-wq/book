# S-0457 table needs 十 rows: 环境过滤／形态或指标形成／确认／入场／初始止损／仓位与资金／持仓与跟踪／加减仓／止盈与退出／失效与放弃. Each row: 条件或动作｜时点与周期｜证据ID｜限制或缺口. Many rows will be "原文未明确". That's required honesty.


Let me draft S-0457 (SRC-003907 双MZ四线变色开平仓方法):

性质：规则完整的策略？Hmm — the method as taught: 开单条件 (两色集齐+K线颜色匹配), 平仓 (收K破四条线), 止损 (本周期MZ). But parameters (MZ周期数值, 品种周期配置) 原稿未明确 (15分钟 mentioned for 原油; 白银五分钟 mentioned in 003908). For 003907: 原油 section mentions "用15分钟周期 高周期MZ" — so 本周期15分钟? "15分钟周期 高周期MZ试试" — implies 本周期15分钟 + 高周期(30分钟?)MZ. 高周期具体值 not stated. So 完整度分级：已给方向+部分参数；按模板 grading: "已给方向／只给名称缺参数／完全缺失" — I'd say for each rule row graded. Overall: 局部方法～规则完整的策略. Let me mark 性质：规则完整的策略（开、平、止损三环节齐备）；完整度分级：方向与触发条件已给，MZ的周期参数、仓位规则原稿未明确。

Rows:

环境过滤: 品种趋势状态（横盘区颜色频繁交替时谨慎）；高周期MZ方向过滤（双MZ）→ cite E-5188(氧化铝)/E-5190 — actually 环境过滤 for S-0457: 老师提示横盘区颜色频繁交替（黄金段）。证据: 黄金段 "横盘区特征是颜色互相交叉的比较多" — no evidence ID allocated for that quote! I didn't allocate evidence for 横盘区特征. Don't claim without ID... I can cite E-5188 (氧化铝横盘 双MZ压制) for the 横盘环境 relevance. OK: 环境过滤 row: 横盘区/趋势中的品种差异；用高周期MZ过滤方向（引 E-5188）.
形态或指标形成: 双MZ四条线颜色集齐（两红两黄=多，两绿两蓝=空 — wait is that stated? In file: 原油 "出现了两绿加两蓝 四条线集齐了 但是面对的是一颗阳线 那么下单K线实际上是它" — 两绿两蓝 with 阴线 → 空单 (PVC 9:50 两绿两蓝阴线 → 空单 context: teacher said student didn't open due to 累计跌幅 — the entry was 空单? Actually with 绿蓝 colors and 阴线 → 空单. And 黄金 9:15 两黄两红 → 多单 ("跳空战法...如果是多单的话" — 黄金两黄两红 was the 多单 context: "第一个K线才是出现了两黄两红 确实是第一个变色K线是下单点"). And 铜 5月22日晚 两红两黄 → 多单 ✓. So color mapping: 红黄=多头色, 绿蓝=空头色 — is that EXPLICITLY stated? Not in so many words, but consistently implied: 铜 "集齐了 两红和两黄的这么一个格局" then "这次交易机会...红线 跑到黄线上面去了" → 多单; 烧碱 "正式站上红线 蓝线 你的空单也平掉了...变成了红线 那应该是下多单". Also 003907 黄金: "你看是黄黄黄黄 两黄两红都是出现了的 你就得把单子开出来" (阳线多单能开 context: "订单操作：阳线多单能开"). So yes 红黄多、绿蓝空 is supported: 黄金 E-5184 context + "阳线多单能开...两黄两红都是出现了的 你就得把单子开出来...两蓝两绿没问题 开了单" — wait that says 两蓝两绿 开了单?? "之后'两蓝两绿没问题 开了单'" — hmm! In 黄金 section: 阳线多单能开 with 两黄两红 → 多单; then "两蓝两绿没问题 开了单" — 空单? The narrative: 黄金 was 多单 (阳线), then colors turned 两蓝两绿 → opened 空单? Then "出现变色的第一个K线...这个阳线实际上是在四条线的下面...你手里捏的空单 你怎么会在阴线上平空单呢" — confusing without the chart. I should avoid over-specifying color→direction mapping beyond what's cited. In S-0457 形态 row: "四条线颜色集齐（如两红两黄、两绿两蓝）并出现对应颜色K线（E-5184等）"；direction mapping: 多头=红黄系、空头=绿蓝系，依据铜（两红两黄→多单，E-5202是003908！）— careful, cross-course. Within 003907: 烧碱 not in 003907 (that's 003908). 003907 PVC: 两绿加两蓝 加阴线 → 该开空单? The text: student "没有开这个单子 因为累计跌幅比较多了" and teacher says 该做 — direction implied 空单 (下跌趋势, 绿蓝). Actually "现在这个黑线 收在蓝线上 肯定是不会亏本的" — 空单盈利 as price falls. It's implied. I'll write: 原稿通过实例呈现"红黄两色集齐对应多单、绿蓝两色集齐对应空单"（如PVC两绿两蓝加阴线开空、焦煤/白银等），但未以定义句明示 → 限制：颜色-方向对应为实例归纳，原稿未给出明文定义。Evidence: E-5189 (两绿两蓝加阴线). OK.
确认: 收K确认 — E-5184; 数线（左上角）.
入场: 变色后第一根符合颜色匹配的K线尝试开单（"一变色就尝试" E-5190）；时点周期: 各品种本周期K线收盘（原油15分钟例 — 003907 E? 原油 quote not allocated. Skip specific).
初始止损: 本周期MZ（E-5185）；止损高低最后考察（E-5189 0.36例）.
仓位与资金: 原文未明确（原油1.08减半仓 — that quote not allocated... "你可以把仓位 减半就能知道" — not in my evidence. So write 原文未明确，仅有零星实例提示，未给规则。Hmm — claiming "零星实例提示" without evidence ID... it IS in the file (原油 section). I could cite... no evidence slot. Write: 原文未明确（本卡证据范围内未见规则）。Safer: 原文未明确.
持仓与跟踪: 未触发收K破线不出（E-5184 变色≠平仓）；铜尾盘K必须平（E-5192）.
加减仓: 原文未明确.
止盈与退出: 收K站回/跌破四条线平仓；不在阴线平空单/阳线平多单（E-5184）.
失效与放弃: 止损过高弃单（E-5189 线距远=止损高 → 不开）；累计跌幅不是放弃理由（E-5190）.

衔接: 开单→等收K确认→触发止损或收K反向破线退出→再等待下次集齐。

案例和失败方式: 锡反例 (高周期过滤错失单边 — that's S-0458's), PVC 弃单反例 (E-5190), 黄金阴线平空单误读. Cite available.

版本分歧与证据限制: 与1295课关系 is editor's claim (「与已有课程的关系」段 = editor voice) — mention as 编辑者评注称…, not rule basis. Actually S-0457's 版本分歧 section: the notes' editor section says 1295课讲"变红不平空单"本课精确化为"收K四条线" — I can mention this AS editor's claim with clear labeling (来源立场 rules: editor段不能当规则依据 — but I can REPORT that the editor says this, clearly labeled). Yes, reporting with label is fine.

S-0458 (高周期MZ/双MZ过滤):
