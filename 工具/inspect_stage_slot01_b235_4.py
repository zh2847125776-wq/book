import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001224_(增强版)股票_20210104量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1224 = f.read()

with open(os.path.join(p_stage, "SRC-002954_(增强版)读书_交易择时技术分析_09.md"), "r", encoding="utf-8") as f:
    text_2954 = f.read()

m1224 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1224)
m2954 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2954)

q0 = m2954[2][:250]
q1 = m2954[6][:250]
q2 = m2954[8][:250]
q3 = m2954[10][:250]
q4 = m1224[3][:250]
q5 = m1224[6][:250]
q6 = m1224[8][:250]
q7 = m1224[10][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2954 if i < 4 else text_1224
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
