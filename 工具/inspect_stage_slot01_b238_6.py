import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000533_(增强版)期货_期货投机技术分析20230803_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_533 = f.read()

with open(os.path.join(p_stage, "SRC-001245_(增强版)股票_20210130量化技术分析_周一盘前加更.md"), "r", encoding="utf-8") as f:
    text_1245 = f.read()

m533 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_533)
m1245 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1245)

q0 = m533[2][:250]
q1 = m533[5][:250]
q2 = m533[6][:250]
q3 = m533[8][:250]
q4 = m1245[2][:250]
q5 = m1245[3][:250]
q6 = m1245[4][:250]
q7 = m1245[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_533 if i < 4 else text_1245
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
