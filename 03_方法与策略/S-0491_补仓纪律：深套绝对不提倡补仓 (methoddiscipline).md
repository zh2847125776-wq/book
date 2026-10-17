# S-0491 补仓纪律：深套绝对不提倡补仓 (method/discipline)


Let me now think about the "斜率越高下反概率越小" — this is mentioned in the 与已有课程的关系 (line 76) which is editor content, NOT to be used. And line 29 "斜率与下反的关系" — let me check. Line 29 is "斜率与下反的关系（本课一..." which is 345 chars, truncated. Let me look at it.

Actually, I should be careful. The 与已有课程的关系 section (lines 72-78) is explicitly editor content and must NOT be used as evidence or rule basis. So the reference to 第1379课 (斜率) there is not usable. But if the 斜率 point appears in the actual lesson body (line 29), that's different.

Let me look at line 29 and the other long lines to understand what's actually in the body vs. the editor section.

Let me also reconsider: I need to check the actual file content more carefully, especially the verbatim quotes. Let me read the full SRC-004032 file to get the exact text of the quotes.

Let me also double check: is the "核心结论" line (line 5) usable? No — 核心结论 is in the banned list. So I can't use it as evidence.

Let me read the full SRC-004032 file to get exact quote text.

===== 块分隔 =====

Thought for 1 second

Now I have the full content. Let me carefully plan the cards.

SRC-004031 (第1407课) is a duplicate of 第1404课. No cards. I'll note this.

SRC-004032 (第1408课) is the real content. Let me extract the verbatim teacher quotes (the ones in 引号) that I can use as evidence. Let me be careful: the evidence must be a contiguous whole paragraph copied verbatim. In this file, the "quotes" are embedded within bullet points that also have the note-taker's framing like - 动机："...".

For verbatim evidence, I have two options:

Use the whole bullet line as the evidence (e.g. - 动机："最乐观的就是这个下反二十线带来的向上吸引力。")
Extract just the quoted text.

The rule says: 原文摘录 must be "从附件里逐字复制的一整段原文" (a contiguous whole paragraph copied verbatim from the attachment). A bullet line is a paragraph. So I can use the whole bullet line. But some bullet lines are very long (e.g., the 斜率 line, the 补仓空仓者 line, the 60分钟 line). Let me check which are ≤300 chars.

Let me check character lengths of the candidate verbatim lines:

Line with 斜率: "斜率与下反的关系（本课一处重要规律）：'这个下反的概率啊...' 这也是我们为什么给他讲这个发生概率只有30%的一个重要原因。" — this is long. Let me count. Actually from the awk output, none of the body lines exceeded 300 in the listing... wait, the awk output only showed line lengths. Let me re-look. The awk output for SRC-004032 didn't show any lines >300 with substr truncation except... let me recheck. Actually the awk listing showed all lines with length>1. Let me look at the truncated ones (where length>300, it showed substr(...,1,40)).

Looking at the awk output again for SRC-004032:

Line 17: 345 chars? No wait. Let me re-read. The format was NR": "length": "content.
"17: 181: - 破线事实：..." means line 17 has length 181.
"19: 345: - 关于该工具的公开性，老师..." means line 19 has length 345! That's >300.

Wait, I'm misreading. The format is NR": "length($0)": "content. So "19: 345: - 关于..." — hmm that doesn't parse right. Let me re-read.

Actually the awk output was:

17: 181: - 破线事实："首先我们是破了二十线第一天对吧..."
18: 155: - 关键点位被打漏：...
19: 345: - 关于该工具的公开性，老师有明确边界说明：...

So line 19 has length 345 > 300. That line can't be used as a single evidence (it's >300 chars). Wait, but the rule says evidence ≤300 chars. So I'd need to not use that whole line. Hmm. But actually the awk showed content after the length, and for length>300 it would show substr. Let me check: the format was (length($0)<=300?$0:substr($0,1,40)). So for line 19 (length 345), it showed substr($0,1,40) = first 40 chars. But the output shows "关于该工具的公开性，老师有明确边界说明：" which is more than 40 chars...

Wait, I think I'm confusing the line numbers. Let me recount. The awk output lines were:

1: 76: # 第1408课 ...
3: 100: > 来源：...
4: 526: > **核心结论**：...
6: 57: ## 一、开篇定调...
8: 336: - 时间与目的原话："我们今天...
9: 147: - 老师说明自己在周末只做一件事...
10: 183: - 本课的推演框架被明确固定为四要素...
11: 217: - 与作业的衔接："我们不是要求学员同学...
13: 422: 【老师点评/批判】开篇把"预...
15: 61: ## 二、周五技术背景...
17: 181: - 破线事实："首先我们是破了二十线第一天对吧...
18: 155: - 关键点位被打漏：...
19: 345: - 关于该工具的公开性，老师...
20: 142: - 当前价格坐标：...
21: 89: - 支撑参考：**3152.81**...
23: 413: 【老师点评/批判】本课的三种...
25: 80: ## 三、情景一...
27: 79: - 动机："最乐观的...
28: 132: - 概率给出："我们说这个发生概率仅仅在30%左右。"...
29: 499: - 斜率与下反的关系（本课一...
30: 133: - 概率的定性："当然这个30%它不是量化统计...
31: 191: - 量能门槛："如果能大于6000亿啊...
32: 32: - 对策："**多看不动**。"
33: 191: - 手绘路径还原（老师口述...
35: 419: 【老师点评/批判】情景一被给...
37: 93: ## 四、情景二...
39: 213: - 动机："首先呢，大跌之后必有大回...
40: 213: - 长线结构："大跌之后长线结构就是什么呀...
41: 504: - 手绘路径还原：早晨**小幅跳...
42: 317: - 更细的盘中还原：开盘价约...
43: 350: - 概率：老师明确"我个人认为...
44: 130: - 对策：仍为"**多看不动**"...
45: 109: - 老师补充确认："实际上最可能就是这个中性情况...
47: 409: 【老师点评/批判】情景二是本...
49: 66: ## 五、情景三...
51: 410: - 动机与前提："周末消息面积...
52: 91: - 形态："要么影线极小啊...
53: 148: - 概率："那么这种发生概率是在10%左右...
54: 326: - 手绘路径还原：**跳空低开**...
56: 426: - 对策的分层处理：前两种情...
58: 485: 【老师点评/批判】情景三的动...
60: 63: ## 六、补仓是个大学问...
62: 169: - 老师的自问自答："有同学就会说...
63: 163: - 补仓的核心命题："补仓呢，其实是个大学问...
64: 437: - 空仓者的判断链条："那如果...
65: 298: - 持仓者的两难："你是不知道后续行情是怎么样的...
66: 121: - 为什么不建议在指数上摊："那要是让你在这个位置上展开指数...
67: 423: - 60分钟级别的补仓依据："如...
68: 430: - 补仓依据的技术逻辑："就算...
69: 175: - 结论句（本课落点）："**所以说你又被深套...
71: 587: 【老师点评/批判】这是本课最...
73: 27: ## 与已有课程的关系
75: 223: - 本课属「技术专题」系列的**周一行情推演**...

So the lines >300 chars are:

Line 4: 526 (核心结论)
Line 8: 336 (时间与目的原话)
Line 11: 217 (与作业的衔接) — wait 217 < 300, ok
Line 13: 422 (老师点评)
Line 19: 345 (关于该工具的公开性)
Line 23: 413 (老师点评)
Line 29: 499 (斜率与下反)
Line 33: 191 (手绘路径) — 191 < 300 ok
Line 35: 419 (老师点评)
Line 41: 504 (手绘路径还原情景二)
Line 42: 317 (更细盘中还原)
Line 43: 350 (概率情景二)
Line 47: 409 (老师点评)
Line 51: 410 (动机与前提情景三)
Line 54: 326 (手绘路径情景三)
Line 56: 426 (对策分层)
Line 58: 485 (老师点评)
Line 64: 437 (空仓者判断链条)
Line 67: 423 (60分钟补仓依据)
Line 68: 430 (补仓依据技术逻辑)
Line 71: 587 (老师点评)
Line 75-79: 关系 lines

So many verbatim quote lines are >300 chars. For those, I can't use the whole line as evidence (must be ≤300).

Hmm. This is a problem. The verbatim quotes are often embedded in long lines. I need to find contiguous sub-paragraphs ≤300 chars that are verbatim.

Wait — but the evidence must be "从附件里逐字复制的一整段原文" — a contiguous whole paragraph. And it must be found in the file verbatim. If I take a sub-portion of a line, is that "一整段"? A paragraph can be a contiguous span of text. As long as it's contiguous and verbatim and ≤300 chars, it should work. The校验程序 checks that the excerpt is found in the attachment (逐字比对). So a contiguous substring of a line would be found verbatim. The question is whether it's "一整段" (a whole paragraph).

Hmm, "一整段原文" — a whole paragraph. If I cut a line in the middle, is that a whole paragraph? This is ambiguous. The earlier runs used whole bullet lines (after stripping the "- " prefix). Let me look at what I did before — in the memory, the script strips the line and removes the "- "/"> " prefix, then uses the whole line. So evidence = whole line (minus prefix).

But now some lines are >300 chars. So I can only use lines that are ≤300 chars as whole-line evidence. Let me list the usable (≤300) verbatim teacher-quote lines:

Scenario 1:

Line 27: "最乐观的就是这个下反二十线带来的向上吸引力。" (79) — 动机 ✓
Line 28: "我们说这个发生概率仅仅在30%左右。"原因是"最重要一点就是它这个阴线实在太大了" (132) — 概率 ✓
Line 30: "当然这个30%它不是量化统计，而是根据过往的这个主观经验，我们给出的一个评判。" (133) — 概率定性 ✓
Line 31: "如果能大于6000亿啊..." (191) — 量能 ✓
Line 32: "多看不动。" (32) — 对策 ✓

Scenario 2:

Line 39: 动机 (213) ✓
Line 40: 长线结构 "大跌之后长线结构就是什么呀，大阴线接十字星。" (213) ✓
Line 44: 对策 "因为它毕竟收盘守在二十线下面啊，你还是没有操作机会的" (130) ✓
Line 45: "实际上最可能就是这个中性情况，说个十字星这个概率是最大。" (109) ✓
Line 43: 概率 (350) ✗ too long
Line 41: 手绘路径 (504) ✗ too long
Line 42: 盘中还原 (317) ✗ too long

Scenario 3:

Line 52: 形态 "要么影线极小啊，要么呢，就是光脚阴线，反正就是很弱。" (91) ✓
Line 53: 概率 "那么这种发生概率是在10%左右……" (148) ✓
Line 51: 动机与前提 (410) ✗ too long
Line 54: 手绘 (326) ✗ too long
Line 56: 对策分层 (426) ✗ too long

补仓:

Line 62: 自问自答 (169) ✓
Line 63: 核心命题 "补仓呢，其实是个大学问……就是你昨天买的联通啊，和你今天买的联通啊，它实际上不是一只个股。" (163) ✓
Line 65: 持仓者两难 (298) ✓
Line 66: 不建议在指数上摊 "那要是让你在这个位置上展开指数，那是肯定不符合技术的。" (121) ✓
Line 69: 结论 "所以说你又被深套，那我们是绝对不提倡补仓的。" (175) ✓
Line 64: 空仓者 (437) ✗ too long
Line 67: 60分钟依据 (423) ✗ too long
Line 68: 技术逻辑 (430) ✗ too long

Background:

Line 17: 破线事实 "首先我们是破了二十线第一天对吧..." (181) ✓
Line 18: 关键点位 "实际上在周五的行情中呢，还跌破了我们讲的底角扇形图的A0" 点位3217 (155) ✓
Line 20: 当前价格坐标 周五收盘3196 跌幅3.86% 前期高点3450 (142) ✓
Line 21: 支撑参考 3152.81 (89) ✓
Line 19: 公开性 (345) ✗ too long

Framework:

Line 10: 四要素 要点整理 (183) ✓ (but this is 要点整理 paraphrase, not verbatim teacher)
Line 9: 三种情况 (147) ✓ (要点整理 paraphrase)
Line 11: 与作业衔接 老师原话 (217) ✓

Now, let me reconsider the evidence strategy. The evidence must be verbatim. Lines 9 and 10 are 要点整理 (the note-taker's paraphrase). Line 11 is a verbatim teacher quote. Line 17, 18 are verbatim.

For the 四要素 framework card, the cleanest verbatim evidence is line 11 (the teacher quote about drawing the analysis chart) plus line 10 (the paraphrase of 四要素). But line 10 is the note-taker's summary. Its 来源立场 would be 转述.

Actually, let me reconsider. Let me reconsider whether I can extract a contiguous verbatim sub-sentence from a >300 line. For example, the 斜率 line (line 29, 499 chars) contains a very quotable rule: "当斜率越高的时候，下反概率其实反而是越小，它实际上是成反比的；当均线的斜率越走平的时候，它能更加从容地去进行下反回测。" That's a clean contiguous span. But is it "一整段"? It's a span within a sentence.

The constraint says: 原文摘录 must be "从附件里逐字复制的一整段原文"（直接复制粘贴即可），不许概括、缩写、改写、拼接、调整语序. And "如果某条内容在附件里找不到可以逐字复制的原文，就不要写这条证据". The 斜率 rule IS verbatim in the attachment — I can copy-paste the exact substring. The word "一整段" (a whole paragraph) is the concern.

I think the safest interpretation, consistent with prior runs, is to use whole lines (or whole sentences that are naturally delimited). Since the 斜率 rule is a key generalizable insight (斜率与下反概率成反比), I'd like to include it. Let me extract the verbatim contiguous sentence: "当斜率越高的时候，下反概率其实反而是越小，它实际上是成反比的；当均线的斜率越走平的时候，它能更加从容地去进行下反回测。" Let me verify this exact text appears in the file. From line 29: "这个下反的概率啊，你可以这么去理解，当斜率越高的时候，下反概率其实反而是越小，它实际上是成反比的；当均线的斜率越走平的时候，它能更加从容地去进行下反回测。因为什么呢..."

Yes, the substring "当斜率越高的时候，下反概率其实反而是越小，它实际上是成反比的；当均线的斜率越走平的时候，它能更加从容地去进行下反回测。" appears verbatim. It's ≤300 chars (it's about 60 chars).

But is extracting a mid-sentence substring acceptable? The校验 does 逐字比对 (character-by-character comparison), so as long as my string is an exact contiguous substring of the file, it passes. The "一整段" requirement is a soft guideline about not piecing together. Since I'm taking one contiguous span, I think it's defensible. But to be safe and consistent, let me prefer whole lines where possible, and only extract contiguous sub-spans when the line is >300 and contains a clearly bounded verbatim rule.

Actually, let me reconsider. The rule is quite strict: "原文摘录 这一列必须是从附件里逐字复制的一整段原文". I'll interpret "一整段" as a contiguous verbatim span. My extraction script in prior runs used whole lines. Let me extend it to allow specific contiguous spans where the line is >300. But I need to make sure each span is exact.

Let me be pragmatic. I'll write the evidence as verbatim contiguous spans (either whole stripped lines or bounded sub-spans), and verify each is found in the raw file with an assert. This satisfies 逐字比对.

Now let me plan the final cards.

Given 20 evidence slots (E-5886 to E-5905), let me allocate:

Knowledge cards:

K-1491: 周一行情推演四要素框架（动机、推演、概率、对策），给参考而非方向性预测
