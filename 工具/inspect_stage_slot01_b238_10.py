import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001248_(增强版)股票_20210203量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1248 = f.read()

with open(os.path.join(p_stage, "SRC-002978_(增强版)读书_其他_亚当理论_完结.md"), "r", encoding="utf-8") as f:
    text_2978 = f.read()

m1248 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1248)
m2978 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2978)

# In text_2978, OCR text has the famous passage:
# “我们应当为我们能在称为市场的伟大的游戏中进行玩乐交易，怀有感恩之心。但请记住，这只是一场游戏”
# Let's verify substrings
q0 = m2978[0][:250]
q1 = m2978[2][:250]
q2 = m1248[4][:250]
q3 = m1248[6][:250]
q4 = m1248[13][:250]
q5 = m1248[14][:250]
q6 = m1248[16][:250]
# We also have m1248[2] about 2646二合一支撑反弹
q7 = m1248[2][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2978 if i < 2 else text_1248
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
