import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000548_(增强版)期货_期货投机技术分析20230906_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_548 = f.read()

with open(os.path.join(p_stage, "SRC-002991_(增强版)读书_其他_像欧奈尔信徒一样交易_07.md"), "r", encoding="utf-8") as f:
    text_2991 = f.read()

m548 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_548)
m2991 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2991)

q0 = m2991[1][:250]
q1 = m2991[2][:250]
q2 = m2991[4][:250]
q3 = m2991[6][:250]
q4 = m548[2][:250]
q5 = m548[3][:250]
q6 = m548[5][:250]
q7 = m548[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2991 if i < 4 else text_548
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
