import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000514_(增强版)期货_期货投机技术分析20230630_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_514 = f.read()

with open(os.path.join(p_stage, "SRC-002957_(增强版)读书_交易择时技术分析_12.md"), "r", encoding="utf-8") as f:
    text_2957 = f.read()

m514 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_514)
m2957 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2957)

q0 = m2957[1][:250]
q1 = m2957[2][:250]
q2 = m2957[3][:250]
q3 = m2957[4][:250]
q4 = m514[2][:250]
q5 = m514[3][:250]
q6 = m514[4][:250]
q7 = m514[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2957 if i < 4 else text_514
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
