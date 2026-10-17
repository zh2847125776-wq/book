import json, os, re

slot = "slot_06"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000505_(增强版)期货_期货投机技术分析20230614_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_505 = f.read()

with open(os.path.join(p_stage, "SRC-001217_(增强版)股票_20201224量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1217 = f.read()

m505 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_505)
m1217 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1217)

q0 = m505[3][:250]
q1 = m505[6][:250]
q2 = m505[10][:250]
q3 = m505[12][:250]
q4 = m1217[5][:250]
q5 = m1217[7][:250]
q6 = m1217[9][:250]
q7 = m1217[11][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_505 if i < 4 else text_1217
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
