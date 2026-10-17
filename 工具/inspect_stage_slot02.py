import json, os, re

slot = "slot_02"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001218_(增强版)股票_20201225量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1218 = f.read()

with open(os.path.join(p_stage, "SRC-002948_(增强版)读书_交易择时技术分析_03.md"), "r", encoding="utf-8") as f:
    text_2948 = f.read()

m1218 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1218)
m2948 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2948)

q0 = m2948[3][:250]
q1 = m2948[4][:250]
q2 = m2948[5][:250]
q3 = m2948[10][:250]
q4 = m1218[3][:250]
q5 = m1218[5][:250]
q6 = m1218[6][:250]
q7 = m1218[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2948 if i < 4 else text_1218
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
