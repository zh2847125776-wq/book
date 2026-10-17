import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000563_(增强版)期货_期货投机技术分析20231009_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_563 = f.read()

with open(os.path.join(p_stage, "SRC-001275_(增强版)股票_20210323量化技术分析_颈线与向下ma20压制明显_底角扇形图与3390支.md"), "r", encoding="utf-8") as f:
    text_1275 = f.read()

m563 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_563)
m1275 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1275)

q0 = m1275[1][:250]
q1 = m1275[2][:250]
q2 = m1275[3][:250]
q3 = m1275[4][:250]
q4 = m563[1][:250]
q5 = m563[2][:250]
q6 = m563[3][:250]
q7 = m563[4][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_1275 if i < 4 else text_563
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
