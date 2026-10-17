import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000525_(增强版)期货_期货投机技术分析20230717_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_525 = f.read()

with open(os.path.join(p_stage, "SRC-001237_(增强版)股票_20210120量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1237 = f.read()

m525 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_525)
m1237 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1237)

q0 = m525[2][:250]
q1 = m525[3][:250]
q2 = m525[6][:250]
q3 = m525[7][:250]
q4 = m1237[2][:250]
q5 = m1237[3][:250]
q6 = m1237[4][:250]
q7 = m1237[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_525 if i < 4 else text_1237
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
