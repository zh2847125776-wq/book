import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001254_(增强版)股票_20210220量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1254 = f.read()

with open(os.path.join(p_stage, "SRC-002984_(增强版)读书_其他_以交易为生_05.md"), "r", encoding="utf-8") as f:
    text_2984 = f.read()

m1254 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1254)
m2984 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2984)

q0 = m2984[1][:250]
q1 = m2984[3][:250]
q2 = m2984[4][:250]
q3 = m2984[6][:250]
q4 = m1254[1][:250]
q5 = m1254[2][:250]
q6 = m1254[4][:250]
q7 = m1254[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2984 if i < 4 else text_1254
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
