import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001274_(增强版)股票_20210322量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1274 = f.read()

with open(os.path.join(p_stage, "SRC-003004_(增强版)读书_其他_日内交易策略--08.md"), "r", encoding="utf-8") as f:
    text_3004 = f.read()

m1274 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1274)
m3004 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_3004)

q0 = m3004[0][:250]
q1 = m3004[1][:250]
q2 = m3004[2][:250]
q3 = m3004[3][:250]
q4 = m1274[1][:250]
q5 = m1274[2][:250]
q6 = m1274[3][:250]
q7 = m1274[4][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_3004 if i < 4 else text_1274
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
