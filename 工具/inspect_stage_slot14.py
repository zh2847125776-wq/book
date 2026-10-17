import json, os, re

slot = "slot_14"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001220_(增强版)股票_20201229量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1220 = f.read()

with open(os.path.join(p_stage, "SRC-002950_(增强版)读书_交易择时技术分析_05.md"), "r", encoding="utf-8") as f:
    text_2950 = f.read()

m1220 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1220)
m2950 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2950)

q0 = m2950[2][:250]
q1 = m2950[3][:250]
q2 = m2950[4][:250]
q3 = m2950[7][:250]
q4 = m1220[2][:250]
q5 = m1220[5][:250]
q6 = m1220[7][:250]
q7 = m1220[9][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2950 if i < 4 else text_1220
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
