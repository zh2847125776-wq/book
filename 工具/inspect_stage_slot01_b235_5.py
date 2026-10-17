import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000512_(增强版)期货_期货投机技术分析20230628_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_512 = f.read()

with open(os.path.join(p_stage, "SRC-002955_(增强版)读书_交易择时技术分析_10.md"), "r", encoding="utf-8") as f:
    text_2955 = f.read()

m512 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_512)
m2955 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2955)

q0 = m2955[0][:250]
q1 = m2955[1][:250]
q2 = m2955[3][:250]
q3 = m2955[4][:250]
q4 = m512[2][:250]
q5 = m512[3][:250]
q6 = m512[4][:250]
q7 = m512[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2955 if i < 4 else text_512
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
