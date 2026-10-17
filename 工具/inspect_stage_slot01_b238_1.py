import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001242_(增强版)股票_20210127量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1242 = f.read()

with open(os.path.join(p_stage, "SRC-002972_(增强版)读书_其他_100倍超级强势股_11.md"), "r", encoding="utf-8") as f:
    text_2972 = f.read()

m1242 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1242)
m2972 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2972)

q0 = m2972[6][:250]
q1 = m2972[8][:250]
q2 = m2972[10][:250]
q3 = m2972[12][:250]
q4 = m1242[2][:250]
q5 = m1242[4][:250]
q6 = m1242[6][:250]
q7 = m1242[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2972 if i < 4 else text_1242
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
