import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000518_(增强版)期货_期货投机技术分析20230706_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_518 = f.read()

with open(os.path.join(p_stage, "SRC-002961_(增强版)读书_从本能到纪律_—6.md"), "r", encoding="utf-8") as f:
    text_2961 = f.read()

m518 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_518)
m2961 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2961)

q0 = m2961[0][:250]
q1 = m2961[1][:250]
q2 = m2961[2][:250]
q3 = m2961[3][:250]
q4 = m518[2][:250]
q5 = m518[3][:250]
q6 = m518[4][:250]
q7 = m518[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2961 if i < 4 else text_518
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
