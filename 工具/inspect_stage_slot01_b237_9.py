import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000528_(增强版)期货_期货投机技术分析20230726_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_528 = f.read()

with open(os.path.join(p_stage, "SRC-002971_(增强版)读书_其他_100倍超级强势股_10.md"), "r", encoding="utf-8") as f:
    text_2971 = f.read()

m528 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_528)
m2971 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2971)

q0 = m2971[1][:250]
q1 = m2971[2][:250]
q2 = m2971[4][:250]
q3 = m2971[6][:250]
q4 = m528[1][:250]
q5 = m528[2][:250]
q6 = m528[3][:250]
q7 = m528[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2971 if i < 4 else text_528
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
