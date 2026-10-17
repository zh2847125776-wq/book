import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000531_(增强版)期货_期货投机技术分析20230801_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_531 = f.read()

with open(os.path.join(p_stage, "SRC-001243_(增强版)股票_20210128量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1243 = f.read()

m531 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_531)
m1243 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1243)

q0 = m531[1][:250]
q1 = m531[2][:250]
q2 = m531[3][:250]
q3 = m531[4][:250]
q4 = m1243[1][:250]
q5 = m1243[2][:250]
q6 = m1243[3][:250]
q7 = m1243[5][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_531 if i < 4 else text_1243
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
