import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000556_(增强版)期货_期货投机技术分析20230919_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_556 = f.read()

with open(os.path.join(p_stage, "SRC-002999_(增强版)读书_其他_日内交易策略--02.md"), "r", encoding="utf-8") as f:
    text_2999 = f.read()

m556 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_556)
m2999 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2999)

q0 = m2999[2][:250]
q1 = m2999[3][:250]
q2 = m2999[5][:250]
q3 = m2999[7][:250]
q4 = m556[1][:250]
q5 = m556[2][:250]
q6 = m556[3][:250]
q7 = m556[4][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2999 if i < 4 else text_556
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
