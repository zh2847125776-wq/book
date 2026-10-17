import json, os, re

slot = "slot_04"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000506_(增强版)期货_期货投机技术分析20230615_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_506 = f.read()

with open(os.path.join(p_stage, "SRC-002949_(增强版)读书_交易择时技术分析_04.md"), "r", encoding="utf-8") as f:
    text_2949 = f.read()

m506 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_506)
m2949 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2949)

q0 = m2949[1][:250]
q1 = m2949[2][:250]
q2 = m2949[3][:250]
q3 = m2949[8][:250]
q4 = m506[4][:250]
q5 = m506[5][:250]
q6 = m506[6][:250]
q7 = m506[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2949 if i < 4 else text_506
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
