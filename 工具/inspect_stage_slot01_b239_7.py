import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000540_(增强版)期货_期货投机技术分析20230817_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_540 = f.read()

with open(os.path.join(p_stage, "SRC-002983_(增强版)读书_其他_以交易为生_04.md"), "r", encoding="utf-8") as f:
    text_2983 = f.read()

m540 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_540)
m2983 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2983)

q0 = m2983[1][:250]
q1 = m2983[3][:250]
q2 = m2983[4][:250]
q3 = m2983[8][:250]
q4 = m540[2][:250]
q5 = m540[3][:250]
q6 = m540[4][:250]
q7 = m540[10][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2983 if i < 4 else text_540
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
