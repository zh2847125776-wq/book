import json, os, re

slot = "slot_08"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000507_(增强版)期货_期货投机技术分析20230616_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_507 = f.read()

with open(os.path.join(p_stage, "SRC-001219_(增强版)股票_20201228量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1219 = f.read()

m507 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_507)
m1219 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1219)

q0 = m507[4][:250]
q1 = m507[6][:250]
q2 = m507[8][:250]
q3 = m507[12][:250]
q4 = m1219[2][:250]
q5 = m1219[4][:250]
q6 = m1219[8][:250]
q7 = m1219[10][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_507 if i < 4 else text_1219
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
