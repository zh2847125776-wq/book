import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001230_(增强版)股票_20210112量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1230 = f.read()

with open(os.path.join(p_stage, "SRC-002960_(增强版)读书_交易择时技术分析_15_完结.md"), "r", encoding="utf-8") as f:
    text_2960 = f.read()

m1230 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1230)
m2960 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2960)

q0 = m2960[4][:250]
q1 = m2960[6][:250]
q2 = m2960[8][:250]
q3 = m2960[10][:250]
q4 = m1230[1][:250]
q5 = m1230[2][:250]
q6 = m1230[4][:250]
q7 = m1230[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2960 if i < 4 else text_1230
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
