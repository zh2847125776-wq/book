import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000569_(增强版)期货_期货投机技术分析20231018_玻璃_甲醇_豆粕_玉米_沪金_焦炭_棉花_白糖.md"), "r", encoding="utf-8") as f:
    text_569 = f.read()

with open(os.path.join(p_stage, "SRC-001281_(增强版)股票_20210331量化技术分析_上反回测_红二共振_共同要求_阴线必出_等待信号_.md"), "r", encoding="utf-8") as f:
    text_1281 = f.read()

m569 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_569)
m1281 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1281)

q0 = m1281[2][:250]
q1 = m1281[3][:250]
q2 = m1281[4][:250]
q3 = m1281[6][:250]
q4 = m569[1][:250]
q5 = m569[2][:250]
q6 = m569[3][:250]
q7 = m569[4][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_1281 if i < 4 else text_569
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
