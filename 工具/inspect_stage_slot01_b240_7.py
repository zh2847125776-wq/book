import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000547_(增强版)期货_期货投机技术分析20230905_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_547 = f.read()

with open(os.path.join(p_stage, "SRC-001259_(增强版)股票_20210227量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1259 = f.read()

m547 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_547)
m1259 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1259)

q0 = m547[2][:250]
q1 = m547[3][:250]
q2 = m547[4][:250]
q3 = m547[0][:230]

q4 = m1259[1][:250]
q5 = m1259[2][:250]
q6 = m1259[4][:250]
q7 = m1259[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_547 if i < 4 else text_1259
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
