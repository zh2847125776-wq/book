import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001236_(增强版)股票_20210119量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1236 = f.read()

with open(os.path.join(p_stage, "SRC-002966_(增强版)读书_其他_100倍超级强势股_05.md"), "r", encoding="utf-8") as f:
    text_2966 = f.read()

m1236 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1236)
m2966 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2966)

q0 = m2966[6][:250]
q1 = m2966[7][:250]
q2 = m2966[8][:250]
q3 = m2966[9][:250]
q4 = m1236[2][:250]
q5 = m1236[3][:250]
q6 = m1236[6][:250]
q7 = m1236[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2966 if i < 4 else text_1236
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
