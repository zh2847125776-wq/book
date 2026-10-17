import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000552_(增强版)期货_期货投机技术分析20230913_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_552 = f.read()

with open(os.path.join(p_stage, "SRC-002995_(增强版)读书_其他_学习社群学员免费福利交易记录本介绍.md"), "r", encoding="utf-8") as f:
    text_2995 = f.read()

m552 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_552)
m2995 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2995)

q0 = m2995[2][:250]
q1 = m2995[3][:250]
q2 = m2995[4][:250]
q3 = m2995[5][:250]
q4 = m552[1][:250]
q5 = m552[2][:250]
q6 = m552[3][:250]
q7 = m552[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2995 if i < 4 else text_552
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
