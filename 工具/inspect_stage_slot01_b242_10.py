import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000562_(增强版)期货_期货投机技术分析20230927_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_562 = f.read()

with open(os.path.join(p_stage, "SRC-003005_(增强版)读书_其他_日内交易策略--完结.md"), "r", encoding="utf-8") as f:
    text_3005 = f.read()

m562 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_562)
m3005 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_3005)

q0 = m3005[2][:250]
q1 = m3005[3][:250]
q2 = m3005[4][:250]
q3 = m3005[6][:250]
q4 = m562[2][:250]
q5 = m562[3][:250]
q6 = m562[4][:250]
q7 = m562[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_3005 if i < 4 else text_562
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
