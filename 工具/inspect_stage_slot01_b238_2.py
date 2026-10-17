import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000530_(增强版)期货_期货投机技术分析20230731_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_530 = f.read()

with open(os.path.join(p_stage, "SRC-002973_(增强版)读书_其他_亚当理论_01.md"), "r", encoding="utf-8") as f:
    text_2973 = f.read()

m530 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_530)
m2973 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2973)

q0 = m2973[3][:250]
q1 = m2973[4][:250]
q2 = m2973[5][:250]
q3 = m2973[6][:250]
q4 = m530[1][:250]
q5 = m530[3][:250]
q6 = m530[4][:250]
q7 = m530[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2973 if i < 4 else text_530
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
