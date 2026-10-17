import json, os, re

slot = "slot_11"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000504_(增强版)期货_期货投机技术分析20230613_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_504 = f.read()

with open(os.path.join(p_stage, "SRC-002947_(增强版)读书_交易择时技术分析_02.md"), "r", encoding="utf-8") as f:
    text_2947 = f.read()

m504 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_504)
m2947 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2947)

q0 = m2947[1][:250]
q1 = m2947[2][:250]
q2 = m2947[4][:250]
q3 = m2947[6][:250]
q4 = m504[3][:250]
q5 = m504[4][:250]
q6 = m504[5][:250]
q7 = m504[12][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2947 if i < 4 else text_504
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
