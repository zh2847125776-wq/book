import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000532_(增强版)期货_期货投机技术分析20230802_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_532 = f.read()

with open(os.path.join(p_stage, "SRC-002975_(增强版)读书_其他_亚当理论_03.md"), "r", encoding="utf-8") as f:
    text_2975 = f.read()

m532 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_532)
m2975 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2975)

q0 = m2975[0][:250]
q1 = m2975[6][:250]
q2 = m2975[7][:250]
q3 = m2975[8][:250]
q4 = m532[1][:250]
q5 = m532[2][:250]
q6 = m532[3][:250]
q7 = m532[4][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2975 if i < 4 else text_532
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
