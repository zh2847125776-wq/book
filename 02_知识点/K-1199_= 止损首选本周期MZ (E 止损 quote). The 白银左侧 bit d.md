# K-1199 = "止损首选本周期MZ" (E: 止损 quote). The 白银左侧 bit: drop. Hmm... actually wait. Let me reconsider cutting E12 (插针) vs E3 (左侧). 插针 case is vivid; 左侧交易 is a rule-relevant concept ("本周期在高周期之上仍可开单——左侧交易"). For a knowledge system, 左侧交易 stance matters more than the 插针 anecdote. So: keep E3 (左侧), cut E12 (插针 C-0891). Then K-1199 = 止损首选本周期MZ + 分歧位置不是硬过滤（左侧交易）with 2 evidences (E2, E3).


And what covers 插针? Nothing card-wise; mention in 底本层级与疑点? It's not a 疑点... The "与已有卡的关系" section? No. It just goes uncarded — acceptable per "宁可少建卡". Hmm, wait — actually, alternatively cut C-0892 (铝) instead and keep C-0891 (插针)? C-0892's 60MA转换点 requires referencing teacher's OTHER video course (基于60MA的多空转换模型) — cross-reference to external course, fine as long as noted. The case: best entry 2:25/2:40pm. It's a good concrete case. 插针 case: event + advice, numbers 830.52.

Decision: cut BOTH C-0891 and... no wait, I need exactly 4 cuts: S-0461(2), plus 2 more from {E12 插针, E19 逆势, E3 左侧, E24...}. E24 (C-0895's 本周期不一定) — cut that instead of E3? C-0895 = 铜 case with combined 0.33 span (1 evidence). Its 边界 section: the "本周期不一定要在高周期上面/止损可接受/改用高周期止损" content — that's the KEY lesson of the case. Cutting E24 guts C-0895's meaning. Keep E24.

Cut E12 (插针) and E19 (逆势1比10)? Then K-1205 = 余量+1%上限 only, missing 逆势结构 (a headline 003908 point: "尽量多做顺势交易 想做逆势交易也可以 必须有结构"). Ugh.

Cut E12 (插针) and E3 (左侧交易)?? Then K-1199 = 止损本周期 only (1 ev), and 白银左侧 lost, 插针 lost.

You know what — cut C-0892 (铝) too? That's 5 cuts → 19 evidences, could re-add E12 or E19. Hmm no.

Let me re-examine: maybe I'm over-splitting S-0459's evidence. #17 combined span (0.95 + 跳空战法规则): does the checker accept spans containing the file's structural glue like 跳空战法："? The excerpt column must be "从附件里逐字复制的一整段原文（直接复制粘贴即可）". A contiguous copy-paste including "跳空战法：" label and quote marks IS 逐字. I'll trust it. Similarly E1 combines two quoted spans via ；" glue. And C-0895's span via ；". These are honest contiguous copies. (I'll note this in 底本层级与疑点 that some excerpts span adjacent quotes contiguously.)

Hmm wait, actually let me double check the file's exact characters for those junctions so my excerpt is EXACTLY contiguous. I need to verify with grep. I'll do that in the shell — extract exact substrings and verify char counts ≤300 and contiguity.

Actually, to be safest with the "一整段原文" requirement, maybe prefer excerpts that lie within a single continuous quoted passage when possible, and only use junction-spanning excerpts when necessary. Let me now also double-check each planned excerpt against the file bytes (copy exactly). I'll write a Python script to verify each excerpt is an exact substring of its file and ≤300 chars.

Now final allocation (20 evidences, E-5184..E-5203):

SRC-003907 (课1296):

E-5184 [黄金] combined span: 出现变色的第一个K线实际上是它……（contiguous through）…有四个数字就是四条线 → K-1198 识别/边界; S-0457 确认/止盈退出 Need exact file text: 「出现变色的第一个K线实际上是它……这个阳线实际上是在四条线的下面 它光变色不行 它还得收K价格在四条线的上面 三条线都不行 是在四条线的上面才会触发 不是说一变色就平仓的 那后面这个是阴线 你手里捏的空单 你怎么会在阴线上平空单呢"；"这个K线虽然盘中有一个上影线 刺破了这个红线 但是首先这只有三条线 你看这个地方没有四条线 怎么看我之前教给过大家 看左上角 看这里的数字 有几条线 有四个数字就是四条线」 — count chars: let me estimate ~175. OK. Hmm, includes "；"" junction. Verify later.

Actually hmm, cleaner alternative: just take from 出现变色 to 平空单呢 (E for K-1198 rule) and a second excerpt for 左上角. But budget... I'll test the combined span contiguity programmatically; if exact, use it.

E-5185 [白银] 我个人的建议是...我推荐用本周期损 → K-1199 识别; S-0457 初始止损行

E-5186 [白银] 咱们只要两蓝两绿...左侧交易机会 → K-1199 边界/关系

E-5187 [高周期MZ边界] 不是不行...经历过一段单边行情以后 → K-1200 识别; S-0458 环境过滤/失效

E-5188 [氧化铝] 但如果你有高周期的绿色的MZ...那就没办法了 → K-1200 识别/适用; S-0458 规则

E-5189 [PVC] 这个时间应该是...最好的开单时候 → K-1201 识别; C-0892(编号调整后)

E-5190 [PVC] 有一位同学找我来讲...该做还是得做 → K-1201 识别; S-0457 环境过滤; 案例

E-5191 [焦煤] 它就你在下单之前...赚的时候赚的多来赚钱 → K-1202 识别; S-0457 案例行

E-5192 [铜] 这个K线还有个更大的问题...就把你就搞掉了 (combined contiguous two spans) → K-1203 识别; S-0457 持仓行

E-5193 [白银] 咱们做股票...那就够麻烦了 → K-1203 识别

E-5194 [铝] 其实你要是把中心金线捞过来看看...还是得做多的 → C-0891(铝)

E-5195 [黄金] 插针长span? — CUT (decided). Wait I decided to cut 插针. Let me finalize: cuts = S-0461 (2), 插针 (1), one more.

Ugh, let me do final accounting cleanly:

Evidences needed (v3): 003907:

E-5184 收K四条线combined (K-1198, S-0457)
E-5185 本周期止损 (K-1199, S-0457)
E-5186 左侧交易 (K-1199)
E-5187 高周期MZ边界 (K-1200, S-0458)
E-5188 氧化铝双MZ (K-1200, S-0458)
E-5189 PVC 9:50/0.36 (K-1201, C-0892)
E-5190 一变色就尝试 (K-1201, S-0457, C-0892)
E-5191 焦煤每笔都试 (K-1202, S-0457)
E-5192 铜尾盘combined (K-1203, S-0457)
E-5193 不尾盘交易 (K-1203)
E-5194 铝2点25 (C-0891) 003908:
E-5195 焦煤事件清仓 (K-1204, S-0459)
E-5196 降仓 (S-0459)
E-5197 缺口不可做 (K-1204, S-0460)
E-5198 0.95+跳空战法combined (S-0460, K-1204)
E-5199 余量0.3~0.35 (K-1205, S-0460)
E-5200 逆势1比10 (K-1205)
E-5201 纯碱 (C-0893)
E-5202 铜combined 0.33 (C-0894)
E-5203 本周期不一定 (C-0894)

= exactly 20! ✓✓

Cut: S-0461 (一色K/LPA method) — dropped as card. 插针 case — dropped.

Cards final: K-1198 收K站上四条线才平仓 (003907) — E-5184 K-1199 止损首选本周期MZ (003907) — E-5185, E-5186 K-1200 高周期MZ只表趋势、双MZ取舍 (003907) — E-5187, E-5188 K-1201 开单质量筛选：止损高低+线距远近+不看累计涨跌幅 (003907) — E-5189, E-5190 K-1202 盈利机制：每笔都试、亏小赚大 (003907) — E-5191 K-1203 期货尾盘与隔夜纪律 (003907) — E-5192, E-5193 K-1204 跳空缺口不可做+过周末清仓/降仓 (003908) — E-5195, E-5197, (E-5198) K-1205 余量标准与止损金额筛选 (003908) — E-5199, E-5200 S-0457 双MZ四线变色开平仓方法（003907）— E-5184, E-5185, E-5190, E-5192 (+E-5191?) S-0458 高周期MZ（双MZ）过滤开单 (003907) — E-5187, E-5188 S-0459 跳空战法 (003908) — E-5198, E-5197, E-5199 S-0460 过周末清仓/降仓纪律 (003908) — E-5195, E-5196, E-5197 C-0891 铝60MA转换点入场 (003907) — E-5194 C-0892 PVC 9:50低止损空单 (003907) — E-5189, E-5190 C-0893 纯碱过周末跳高平仓 (003908) — E-5201 C-0894 铜5月22日两次开单对照 (003908) — E-5202, E-5203

16 cards, 20 evidences.

Now, numbering: use all 8 K, 4 S (0457-0460), 4 C (0891-0894). Fine ("宁可少建卡").

Hmm wait — should I reconsider including the 插针 as C-0895 with... no evidence slots left. Done deal.

Also reconsider: is it OK that K-1205 doesn't include 逆势结构? I have E-5200 (逆势1比10) allocated to K-1205! Yes — look at my list: #17 E-5200 逆势1比10 → K-1205. So K-1205 = 余量 + 止损金额筛选 + 逆势需结构 (3 aspects, 2 evidences). The 逆势 quote: "如果今天白银白天是从上面冲下来 又创了个高 形成个SFB 你说你从这个地方打下来 然后这里个亏损是 比如说0.27 向下盈利是个2.85 这盈亏比划算1比10 那我试试就试试 它也没有 所以说白银的空单是做不出来的" — supports "逆势需结构/盈亏比门槛（例1比10）". Also the "尽量多做顺势交易" quote from editor section — skip (editor voice), note in card's 立场? The card stance = 课程讲述者采纳 via E-5199/E-5200 ✓.

Also K-1204 gets E-5198 partially (周末分歧通过跳空缺口兑现 → 机会在缺口后). Good.

Now — verify all excerpts verbatim via script. I must be extremely careful with exact characters including spaces. The file uses spaces between phrases (transcription style). I'll extract programmatically: define start and end markers, find them in file, extract inclusive span, compute length, and ensure my TSV excerpt column matches exactly. Better approach: write a Python script that, for each evidence, takes (file, start_marker, end_marker), extracts file[start:end+1], prints it with length; then I build the TSV from those extracted strings programmatically to guarantee verbatim accuracy. I can even have the script write the final markdown output file. That guarantees byte-exact excerpts.

Plan:

Python script extract.py with list of (eid, file, start, end) markers; verify markers appear exactly once; extract spans; check ≤300 chars; dump to JSON.
Review extracted spans (print) to confirm they look right.
Generate TSV lines by concatenating eid, source_id, 位置, excerpt, 用途 — with excerpt taken from extracted JSON (guaranteed verbatim).
Build final answer markdown. But the final answer is my chat reply — the user wants the reply text itself in a specific format. I'll compose the reply manually but copy excerpts from the verified extraction output. To be extra safe, the script can also verify the final TSV (I'll write the deliverable to a file too? The user didn't ask for a file; they want the reply formatted. But workspace file could help. The instruction: output format with sections in reply. I'll do the reply as specified. Maybe ALSO save a copy as a file? The prompt says "按这个顺序输出，不要加别的话" — the reply should contain exactly those sections. Adding a file is extra; the instructions say don't add other words. I'll keep the reply strictly to the format. I could still save a workspace copy silently? "不要加别的话" refers to the reply text. Saving a file silently is fine but unnecessary; skip to avoid confusion. Actually — hmm, a file copy could be genuinely useful (长内容). But strict reading: reply must contain the 4 sections only. I'll put everything in the reply only. (The RUN marker must be the FIRST line of the reply.)

Now let me carefully define excerpts with exact markers. I need the exact file text. Let me pull specific lines with grep to get exact junction characters.

Key excerpts to verify:

E-5184: start "出现变色的第一个K线实际上是它" end "有四个数字就是四条线" File text (from read): 关键平仓规则："出现变色的第一个K线实际上是它……这个阳线实际上是在四条线的下面 它光变色不行 它还得收K价格在四条线的上面 三条线都不行 是在四条线的上面才会触发 不是说一变色就平仓的 那后面这个是阴线 你手里捏的空单 你怎么会在阴线上平空单呢"；"这个K线虽然盘中有一个上影线 刺破了这个红线 但是首先这只有三条线 你看这个地方没有四条线 怎么看我之前教给过大家 看左上角 看这里的数字 有几条线 有四个数字就是四条线"。

So span from 出 to 线 includes: ...平空单呢"；"这个K线... — includes full-width quotes and semicolon. Length? Count roughly: segment1 ~110, junction 3, segment2 ~85 → ~198. ✓ ≤300.

Hmm, do I want the "；"" junction in the excerpt? It's verbatim contiguous. I'll accept. Alternatively trim to just segment1+segment2 separately as 2 evidences — no budget. Accept combined.

Actually WAIT. Let me reconsider — maybe simpler and safer: E-5184 = segment1 only (出现变色...平空单呢, ~110 chars) and drop 左上角 detail from cards (don't claim 数线方法). Then use saved... no, budget fixed at 20; I don't have a spare use for it. The 左上角数字 method ("有四个数字就是四条线") is genuinely useful for K-1198's 如何识别. Keep combined span. If worried, split into E-5184 (seg1) and E-5185 (seg2) and drop something else... What would I drop? Nothing is droppable. Keep combined. The verification script will confirm exactness — that's what matters for the checker (拿回附件逐字比对). Contiguous region = exact substring ✓.

E-5185: 我个人的建议是 如果你下单了以后 用本周期去做止损 这样的话 止损比较低 更贴合本周期 那么有同学就认为 应该是站在四条线下面 那么他站上绿线 也就给跑掉了 也可以随你 我推荐用本周期损 — start "我个人的建议是" end "我推荐用本周期损" ~95 chars ✓

E-5186: start "咱们只要两蓝两绿" end "左侧交易机会" — file: 老师定性："咱们只要两蓝两绿 没有说朝向 是吧 有同学就是认为 这个单子亏损 是因为蓝线在绿线上面 所以不该做 其实你想想 它实际上是一个左侧交易机会"；~75 ✓

E-5187: start "不是不行 我们在最早讲多周期穿透的时候" end "尤其是经历过一段单边行情以后" — file: 老师回答："不是不行 我们在最早讲多周期穿透的时候 就说过这个问题 你包括你20对60的时候 60能不能下单也行 不是不行 但是高周期也好 60日线也好 还是多周期穿透也好 你比较高周期 比较趋势的品种 在本周期 它就不一定会准 有可能会触发你的订单 尤其是经历过一段单边行情以后"。 ~135 ✓

E-5188: start "但如果你有高周期的绿色的MZ在这里压着" end "会错失机会 那就没办法了" — file: "但如果你有高周期的绿色的MZ在这里压着 你还会去做多单吗 你就不做了 你就只做空单……那么一次磨损 然后就是这里会做 现在还在成本区附近 是不是很好 对吧 尤其是在横盘区 因为有高周期MZ的存在 所以说压的是非常准的 然后对你的指示 也是非常有建设性意义的 当然在某些订单中 会错失机会 那就没办法了"。 ~150 ✓ (contains "……" as in file ✓)

E-5189: start "这个时间应该是" end "所以PVC就是很好的开单时候" — file: "这个时间应该是 昨天午 晚上的9点50 出现了两绿 加两蓝 加阴线 的这么一个节奏 而且还有个问题 我们看到它 止损非常低 0.36 所以说我 几次三番 跟大家去解释 高周期和低周期 本周期和高周期的MZ 离得近的时候 止损低的时候 就是价格和K线离得近 K线和止损离得近 然后两条线 离得有近的时候 这是最好的开单时候 所以PVC就是很好的开单时候"。 ~170 ✓

E-5190: start "有一位同学找我来讲" end "所以说该做还是得做" — file: "有一位同学找我来讲 他说老师 我就没有开这个单子 因为累计跌幅比较多了……所以说为什么 咱们定的规则叫 一变色就尝试 没有咱们交易逻辑 这个里头 没有让你去看 累计跌幅大于小 逻辑很简单 上涨不测底 下跌不测底 是不是 你不要考虑 它累计跌幅有多少 它只要止损合适 蓝线和绿线离得近 你想试试 你就试试……不多一会就脱离成本区了 现在这个黑线 收在蓝线上 肯定是不会亏本的 对吧 所以说该做还是得做"。 ~210 ✓

E-5191: start "它就你在下单之前" end "赚的时候赚的多来赚钱" — file: "它就你在下单之前 你是不能筛选出来这个单子 到底单边行情是大还是小的 我们要是下单之前 一共有五个单子 知道其中两个单子单边行情大 另外三个单边行情小 我们就只选大的做小的 或者不做 那就好了 做不到 所以说你每一笔都得去试 而且试的过程中设置都不是因为胜率高挣钱 而是因为亏的时候亏的少 赚的时候赚的多来赚钱"；~180 ✓

E-5192: start "这个K线还有个更大的问题" end "就把你就搞掉了" — file: 订单操作："这个K线还有个更大的问题 是它是最后一个K线 它是5月19号 就是昨天下午 白天收盘的K线 那马上要晚上开盘了 你不能不出的"；"那你要是不出 它向上跳空之类 就把你就搞掉了"；— combined with junction ~110 ✓

E-5193: start "咱们做股票" end "那就够麻烦了" — file: "咱们做股票 是提高了 提醒大家尽量尾盘交易 做期货是尽量提醒大家 不要尾盘交易 你明明有T加0的优势 你不仅不用 你还要尾盘 去面临第二天的跳空低开 过夜的跳空低开 跳空高开 反向跳空 那就够麻烦了"。 ~110 ✓

E-5194: start "其实你要是把中心金线捞过来看看" end "还是得做多的" — ~185 chars: "其实你要是把中心金线捞过来看看 咱们有一个视频 叫基于60MA的多空转换模型 是不是 里头有讲 它其实就是正好是一个 什么 高周期MZ转过来的 这么一个过程 那么实际上最好的下单机会 是今天下午的2点25分 或者说是今天下午的2点25分 下午的2点40都是可以的 价格差不了太多 现在应该是持有中 刚刚开始 如果一会儿有贴近红线的交易机会转阳线 还是得进 还是得做多的" ✓

E-5195: start "当然这次焦煤这个问题" end "就不会碰上这样的问题" — "当然这次焦煤这个问题 怎么说就预判不了 谁能知道它出这样的问题 解决不了 但是总的来说 你只要是说是清仓过周末 或者干脆不过周末的话 就不会碰上这样的问题" ~85 ✓

E-5196: start "你要是要过周末" end "那回撤实在是太痛了" — file: "你要是想过周末 你就得比平时过夜要有更高的警觉才行 你就是盈利了一万块 结果回撤剩了五千 那也很闹心……你要是要过周末 那你就把仓位降低一点 它要是平开了 你再去接再去追都来得及 高开少赚不要紧 那回撤实在是太痛了"。 Start at "你要是要过周末 那你就把仓位降低一点" end "那回撤实在是太痛了" ~75 ✓. Or include the 前半 (警觉/一万→五千)? Separate sentence before "……". Take from "你要是想过周末 你就得比平时过夜要有更高的警觉才行" through "那回撤实在是太痛了" ~100 chars contiguous ✓ better (covers 警觉 + 一万/五千 + 降仓). Start "你要是想过周末" end "那回撤实在是太痛了". ✓

E-5197: start "黄金的走势" end "太明显了" — "黄金的走势 就是这个跳空缺口 其实是没法做的 折损空间太大 太明显了" ~35 ✓. Wait, in file: 过夜状态："黄金的走势 就是这个跳空缺口 其实是没法做的 折损空间太大 太明显了"；"如果你要是周末过夜..." ✓

E-5198: start "真真正正对应的K线是这个" end "它肯定也触发过了" — combined across bullets: 真开单K线："真真正正对应的K线是这个 这是来到了今天白天9点一刻 第一个K线才是出现了两黄两红 确实是第一个变色K线是下单点 可是这个K线的止损点非常远 0.95 是吧 所以说就不太适合去做"。 跳空战法："我们讲了 这个跳空战法 它其实也比较风险也比较高 高收益高风险 是吧 这个周末的分歧都通过跳空缺口已经兑现了 那么有这么个跳空战法是 第一个K线形成以后下单用 如果是多单的话 就用第一个K的最低价加余量止损 你这目前打眼一看 它肯定也触发过了"。 Junction: 去做"。 跳空战法："我们讲了... — span includes "。 跳空战法：". ~215 chars ✓ contiguous verbatim.

E-5199: start "实际上这个单也开不出来" end "它也没有结构" — "实际上这个单也开不出来 我们看第二个K线收K的时候 要是创新高止损 已经有0.85了 加余量 余量一般在0.3到0.35之间 你算一算 那肯定它也是超过1%了 所以说这个空单 即使你想开 开不出来 它也没有结构" ~110 ✓

E-5200: start "如果今天白银白天是从上面冲下来" end "所以说白银的空单是做不出来的" — ~120 ✓

E-5201: start "倒霉催的纯减啊" end "我手工买的也很少" — "倒霉催的纯减啊 我当时是这里下的止损单 然后过周末的时候的最后一个k线 它虽然高于这个蓝线 但是离我止损还很远 拿着调高开盘了 我就把它平了 那没办法 这就我只能说是庆幸自己没有碰到焦煤 就可以了 挺好啊 赶上买的也不多 然后其他的都交给程旭了 我手工买的也很少" ~140 ✓

E-5202: start "随着时间推移 我们发现来到了" end "其实是非常近的" — "随着时间推移 我们发现来到了 这是5月22号的晚上11点40 又发生了变化了 又再一次集齐了 两红和两黄的这么一个格局 那么上次集齐两红和两黄 收益失败了 没有能够赚到钱 归损离场 那是因为红线在黄线下方没有盘好 可是这次交易机会呢 我们发现他的红线 跑到黄线上面去了 离得还不远"；"以收k价格到本周期止损的话 才只有区区0.33 其实是非常近的" — junction ~185 ✓

E-5203: start "说是不是一定本周期一定要在高周期上面" end "灵活运用" — "说是不是一定本周期一定要在高周期上面 其实是不一定的 对吧 还是看你的止损在哪里 你能接受 那暂时可以 或者你干脆我调转枪头 我用高周期MZ来做这笔交易 我用高周期MZ来止损也是可以的 灵活运用" ~100 ✓

All 20 within budget. Now positions (文件名＋小标题) for TSV column 3:

E-5184: SRC-003907…md ＋ 一、黄金：插针复盘与"收K站上四条线"规则
E-5185: SRC-003907…md ＋ 二、白银：本周期在高周期之上的左侧交易
E-5186: same section 二
E-5187: SRC-003907 ＋ 六、高周期MZ下单的适用边界（锡的反例）
E-5188: SRC-003907 ＋ 五、氧化铝：横盘疯狂变色下的双MZ过滤
E-5189: SRC-003907 ＋ 十、化工系：PVC、PTA、塑料、甲醇、烧碱、纯碱、玻璃
E-5190: same 十
E-5191: SRC-003907 ＋ 八、黑色系：焦煤、铁矿石、螺纹钢、热卷
E-5192: SRC-003907 ＋ 三、铜：尾盘K必须平仓
E-5193: SRC-003907 ＋ 二、白银…（尾盘纪律 bullet）
E-5194: SRC-003907 ＋ 四、铝：60MA多空转换模型的最佳入场
E-5195: SRC-003908 ＋ 一、周五直播取消与过周末纪律
E-5196: same 一
E-5197: SRC-003908 ＋ 二、黄金：跳空战法与缺口不可做
E-5198: same 二
E-5199: SRC-003908 ＋ 三、白银：正管理率3.15与逆势交易的结构要求
E-5200: same 三
E-5201: SRC-003908 ＋ 九、化工系：PVC、PTA、烧碱、苯乙烯、纯碱、玻璃、纸浆
E-5202: SRC-003908 ＋ 四、铜：本周期在高周期之下的分歧处理
E-5203: same 四

TSV with tabs — excerpts contain no tabs (they're Chinese text with spaces) ✓. But excerpts contain quotes ("；") — fine in TSV. The 位置 column contains ＋ and section titles which include ：and （） — no tabs ✓.

Now the source_id column: SRC-003907 / SRC-003908.

Now write the cards.

Card template compliance:

K cards:

Note "底本层级" — files are 学习笔记, no 增强版 marker → 完整稿可见. I'll state that and explain in 底本层级与疑点 section.

S-0457 table needs 十 rows: 环境过滤／形态或指标形成／确认／入场／初始止损／仓位与资金／持仓与跟踪／加减仓／止盈与退出／失效与放弃. Each row: 条件或动作｜时点与周期｜证据ID｜限制或缺口. Many rows will be "原文未明确". That's required honesty.
