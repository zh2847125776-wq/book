import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000519_(增强版)期货_期货投机技术分析20230707_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_519 = f.read()

with open(os.path.join(p_stage, "SRC-001231_(增强版)股票_20210113量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1231 = f.read()

m519 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_519)
m1231 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1231)

q0 = m519[2][:250]
q1 = m519[3][:250]
q2 = m519[4][:250]
q3 = m519[10][:250]
q4 = m1231[2][:250]
q5 = m1231[3][:250]
q6 = m1231[4][:250]
q7 = m1231[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_519 if i < 4 else text_1231
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
