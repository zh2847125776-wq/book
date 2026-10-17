import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000526_(增强版)期货_期货投机技术分析20230719_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_526 = f.read()

with open(os.path.join(p_stage, "SRC-002969_(增强版)读书_其他_100倍超级强势股_08.md"), "r", encoding="utf-8") as f:
    text_2969 = f.read()

m526 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_526)
m2969 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2969)

q0 = m2969[1][:250]
q1 = m2969[3][:250]
q2 = m2969[4][:250]
q3 = m2969[6][:250]
q4 = m526[2][:250]
q5 = m526[3][:250]
q6 = m526[4][:250]
q7 = m526[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2969 if i < 4 else text_526
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
