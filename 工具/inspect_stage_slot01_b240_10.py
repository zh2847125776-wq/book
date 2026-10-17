import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000549_(增强版)期货_期货投机技术分析20230907_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_549 = f.read()

with open(os.path.join(p_stage, "SRC-001261_(增强版)股票_20210302量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1261 = f.read()

m549 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_549)
m1261 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1261)

q0 = m549[0][:250]
q1 = m549[2][:250]
q2 = m549[3][:250]
q3 = m549[4][:250]
q4 = m1261[3][:250]
q5 = m1261[4][:250]
q6 = m1261[6][:250]
q7 = m1261[10][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_549 if i < 4 else text_1261
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
