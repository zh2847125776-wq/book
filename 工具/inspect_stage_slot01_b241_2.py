import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000550_(增强版)期货_期货投机技术分析20230911_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_550 = f.read()

with open(os.path.join(p_stage, "SRC-002993_(增强版)读书_其他_像欧奈尔信徒一样交易_09.md"), "r", encoding="utf-8") as f:
    text_2993 = f.read()

m550 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_550)
m2993 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2993)

q0 = m2993[1][:250]
q1 = m2993[2][:250]
q2 = m2993[3][:250]
q3 = m2993[6][:250]
q4 = m550[2][:250]
q5 = m550[3][:250]
q6 = m550[4][:250]
q7 = m550[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2993 if i < 4 else text_550
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
