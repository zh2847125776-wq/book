import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000521_(增强版)期货_期货投机技术分析20230711_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_521 = f.read()

with open(os.path.join(p_stage, "SRC-001233_(增强版)股票_20210115量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1233 = f.read()

m521 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_521)
m1233 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1233)

q0 = m521[1][:250]
q1 = m521[2][:250]
q2 = m521[3][:250]
q3 = m521[8][:250]
q4 = m1233[1][:250]
q5 = m1233[4][:250]
q6 = m1233[6][:250]
q7 = m1233[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_521 if i < 4 else text_1233
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
