import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000560_(增强版)期货_期货投机技术分析20230925_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_560 = f.read()

with open(os.path.join(p_stage, "SRC-003003_(增强版)读书_其他_日内交易策略--07.md"), "r", encoding="utf-8") as f:
    text_3003 = f.read()

m560 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_560)
m3003 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_3003)

q0 = m3003[0][:250]
q1 = m3003[1][:250]
q2 = m3003[2][:250]
q3 = m3003[3][:250]
q4 = m560[2][:250]
q5 = m560[3][:250]
q6 = m560[4][:250]
q7 = m560[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_3003 if i < 4 else text_560
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
