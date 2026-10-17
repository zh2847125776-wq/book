import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001258_(增强版)股票_20210225量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1258 = f.read()

with open(os.path.join(p_stage, "SRC-002988_(增强版)读书_其他_像欧奈尔信徒一样交易_04.md"), "r", encoding="utf-8") as f:
    text_2988 = f.read()

m1258 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1258)
m2988 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2988)

q0 = m2988[3][:250]
q1 = m2988[6][:250]
q2 = m2988[8][:250]
# One more quote from 2988: m2988[2]
q3 = m2988[2][:250]

q4 = m1258[3][:250]
q5 = m1258[4][:250]
q6 = m1258[8][:250]
q7 = m1258[10][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2988 if i < 4 else text_1258
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
