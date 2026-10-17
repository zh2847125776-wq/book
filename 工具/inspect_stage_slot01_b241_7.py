with open("分片工作区/Shard3_b220_243/slots/slot_01/stage/SRC-001266_(增强版)股票_20210310量化技术分析.md", "r", encoding="utf-8") as f:
    text_1266 = f.read()

import re
m1266 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1266)

q0 = "小型适指当月连续"
q1 = "20200331上证指"
q2 = m1266[2][:250]
q3 = m1266[3][:250]
q4 = m1266[7][:250]
q5 = m1266[9][:250]
q6 = m1266[11][:250]
q7 = m1266[13][:250]

with open("分片工作区/Shard3_b220_243/slots/slot_01/stage/SRC-002996_(增强版)读书_其他_所有交易者必然出现的一种现象_人生中的必然之事_看了你就恍然大悟.md", "r", encoding="utf-8") as f:
    text_2996 = f.read()

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2996 if i < 2 else text_1266
    ok = q in src and len(q) <= 300 and "\n" not in q and len(q) >= 8
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
