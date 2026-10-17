import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001226_(增强版)股票_20210106量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1226 = f.read()

with open(os.path.join(p_stage, "SRC-002956_(增强版)读书_交易择时技术分析_11.md"), "r", encoding="utf-8") as f:
    text_2956 = f.read()

m1226 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1226)
m2956 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2956)

q0 = m2956[4][:250]
q1 = m2956[5][:250]
q2 = m2956[8][:250]
q3 = m2956[10][:250]
q4 = m1226[2][:250]
q5 = m1226[3][:250]
q6 = m1226[4][:250]
q7 = m1226[10][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2956 if i < 4 else text_1226
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
