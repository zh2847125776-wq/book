import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000558_(增强版)期货_期货投机技术分析20230921_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_558 = f.read()

with open(os.path.join(p_stage, "SRC-003001_(增强版)读书_其他_日内交易策略--04.md"), "r", encoding="utf-8") as f:
    text_3001 = f.read()

m558 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_558)
m3001 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_3001)

# Text 3001 has 3 rich voice segments; let's get another quote from OCR or 3001 voice #0
m3001_all = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_3001)

q0 = m3001[0][:250]
q1 = m3001[1][:250]
q2 = m3001[2][:250]
q3 = m3001[3][:250]
q4 = m558[1][:250]
q5 = m558[2][:250]
q6 = m558[3][:250]
q7 = m558[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_3001 if i < 4 else text_558
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
