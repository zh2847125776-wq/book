import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000555_(增强版)期货_期货投机技术分析20230918_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_555 = f.read()

with open(os.path.join(p_stage, "SRC-001267_(增强版)股票_20210311量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1267 = f.read()

m555 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_555)
m1267 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1267)

q0 = m1267[1][:250]
q1 = m1267[2][:250]
q2 = m1267[4][:250]
q3 = m1267[6][:250]
q4 = m555[2][:250]
q5 = m555[3][:250]
q6 = m555[4][:250]
q7 = m555[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_1267 if i < 4 else text_555
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
