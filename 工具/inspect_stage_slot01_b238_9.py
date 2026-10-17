import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000535_(增强版)期货_期货投机技术分析20230808_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_535 = f.read()

with open(os.path.join(p_stage, "SRC-001247_(增强版)股票_20210202量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1247 = f.read()

m535 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_535)
m1247 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1247)

q0 = m535[1][:250]
q1 = m535[2][:250]
q2 = m535[3][:250]
q3 = m535[6][:250]
q4 = m1247[2][:250]
q5 = m1247[3][:250]
q6 = m1247[6][:250]
q7 = m1247[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_535 if i < 4 else text_1247
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
