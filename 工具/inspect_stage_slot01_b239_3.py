import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001250_(增强版)股票_20210205量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1250 = f.read()

with open(os.path.join(p_stage, "SRC-002980_(增强版)读书_其他_以交易为生_01.md"), "r", encoding="utf-8") as f:
    text_2980 = f.read()

m1250 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1250)
m2980 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2980)

q0 = m2980[2][:250]
q1 = m2980[4][:250]
q2 = m2980[8][:250]
q3 = m2980[10][:250]
q4 = m1250[2][:250]
q5 = m1250[3][:250]
q6 = m1250[4][:250]
q7 = m1250[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2980 if i < 4 else text_1250
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
