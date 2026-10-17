import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001264_(增强版)股票_20210308量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1264 = f.read()

with open(os.path.join(p_stage, "SRC-002994_(增强版)读书_其他_像欧奈尔信徒一样交易_10.md"), "r", encoding="utf-8") as f:
    text_2994 = f.read()

m1264 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1264)
m2994 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2994)

q0 = m2994[1][:250]
q1 = m2994[2][:250]
q2 = m2994[3][:250]
q3 = m2994[4][:250]
q4 = m1264[2][:250]
q5 = m1264[3][:250]
q6 = m1264[7][:250]
q7 = m1264[9][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2994 if i < 4 else text_1264
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
