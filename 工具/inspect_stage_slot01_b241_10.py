import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001268_(增强版)股票_20210312量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1268 = f.read()

with open(os.path.join(p_stage, "SRC-002998_(增强版)读书_其他_日内交易策略--01.md"), "r", encoding="utf-8") as f:
    text_2998 = f.read()

m1268 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1268)
m2998 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2998)

q0 = m2998[2][:250]
q1 = m2998[3][:250]
q2 = m2998[9][:250]
q3 = m2998[10][:250]
q4 = m1268[2][:250]
q5 = m1268[3][:250]
q6 = m1268[4][:250]
q7 = m1268[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2998 if i < 4 else text_1268
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
