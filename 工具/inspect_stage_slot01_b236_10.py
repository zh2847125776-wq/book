import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000522_(增强版)期货_期货投机技术分析20230712_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_522 = f.read()

with open(os.path.join(p_stage, "SRC-002965_(增强版)读书_其他_100倍超级强势股_04.md"), "r", encoding="utf-8") as f:
    text_2965 = f.read()

m522 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_522)
m2965 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2965)

q0 = m2965[6][:250]
q1 = m2965[8][:250]
q2 = m2965[10][:250]
q3 = m2965[12][:250]
q4 = m522[2][:250]
q5 = m522[3][:250]
q6 = m522[4][:250]
q7 = m522[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2965 if i < 4 else text_522
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
