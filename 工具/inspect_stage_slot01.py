import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000508_(增强版)期货_期货投机技术分析20230619_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_508 = f.read()

with open(os.path.join(p_stage, "SRC-002951_(增强版)读书_交易择时技术分析_06.md"), "r", encoding="utf-8") as f:
    text_2951 = f.read()

m508 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_508)
m2951 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2951)

q0 = m2951[1][:250]
q1 = m2951[3][:250]
q2 = m2951[4][:250]
q3 = m2951[6][:250]
q4 = m508[3][:250]
q5 = m508[4][:250]
q6 = m508[6][:250]
q7 = m508[10][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2951 if i < 4 else text_508
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
