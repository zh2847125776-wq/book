import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000561_(增强版)期货_期货投机技术分析20230926_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_561 = f.read()

with open(os.path.join(p_stage, "SRC-001273_(增强版)股票_20210319量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1273 = f.read()

m561 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_561)
m1273 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1273)

q0 = m1273[3][:250]
q1 = m1273[5][:250]
q2 = m1273[7][:250]
q3 = m1273[9][:250]
q4 = m561[1][:250]
q5 = m561[2][:250]
q6 = m561[3][:250]
q7 = m561[4][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_1273 if i < 4 else text_561
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
