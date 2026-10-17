import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000557_(增强版)期货_期货投机技术分析20230920_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_557 = f.read()

with open(os.path.join(p_stage, "SRC-001269_(增强版)股票_20210315量化技术分析_技术指标完美契合_多看少动绝不抄底_警惕十日线发威.md"), "r", encoding="utf-8") as f:
    text_1269 = f.read()

m557 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_557)
m1269 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1269)

q0 = m1269[3][:250]
q1 = m1269[4][:250]
q2 = m1269[5][:250]
q3 = m1269[7][:250]
q4 = m557[1][:250]
q5 = m557[2][:250]
q6 = m557[3][:250]
q7 = m557[4][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_1269 if i < 4 else text_557
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
