import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000568_(增强版)期货_期货投机技术分析20231017_玻璃_甲醇_豆粕_玉米_沪金_焦炭_棉花_白糖.md"), "r", encoding="utf-8") as f:
    text_568 = f.read()

with open(os.path.join(p_stage, "SRC-003011_(增强版)读书_其他_止损如何克服贪婪和恐惧七.md"), "r", encoding="utf-8") as f:
    text_3011 = f.read()

m568 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_568)
m3011 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_3011)

q0 = m3011[0][:250]
q1 = m3011[4][:250]
q2 = m3011[6][:250]
q3 = m3011[10][:250]
q4 = m568[1][:250]
q5 = m568[2][:250]
q6 = m568[3][:250]
q7 = m568[4][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_3011 if i < 4 else text_568
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
