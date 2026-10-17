import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000544_(增强版)期货_期货投机技术分析20230824_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_544 = f.read()

with open(os.path.join(p_stage, "SRC-002987_(增强版)读书_其他_像欧奈尔信徒一样交易_03.md"), "r", encoding="utf-8") as f:
    text_2987 = f.read()

m544 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_544)
m2987 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2987)

q0 = m2987[2][:250]
q1 = m2987[3][:250]
q2 = m2987[4][:250]
q3 = m2987[10][:250]
q4 = m544[1][:250]
q5 = m544[2][:250]
q6 = m544[3][:250]
q7 = m544[4][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2987 if i < 4 else text_544
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
