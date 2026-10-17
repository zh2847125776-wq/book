import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000546_(增强版)期货_期货投机技术分析20230904_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_546 = f.read()

with open(os.path.join(p_stage, "SRC-002989_(增强版)读书_其他_像欧奈尔信徒一样交易_05.md"), "r", encoding="utf-8") as f:
    text_2989 = f.read()

m546 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_546)
m2989 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2989)

q0 = m2989[1][:250]
q1 = m2989[4][:250]
q2 = m2989[6][:250]
q3 = m2989[10][:250]
q4 = m546[2][:250]
q5 = m546[3][:250]
q6 = m546[4][:250]
q7 = m546[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2989 if i < 4 else text_546
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
