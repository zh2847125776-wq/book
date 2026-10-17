import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001256_(增强版)股票_20210223量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1256 = f.read()

with open(os.path.join(p_stage, "SRC-002986_(增强版)读书_其他_像欧奈尔信徒一样交易_02.md"), "r", encoding="utf-8") as f:
    text_2986 = f.read()

m1256 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1256)
m2986 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2986)

q0 = m2986[4][:250]
q1 = m2986[6][:250]
q2 = m2986[8][:250]
q3 = m2986[10][:250]
q4 = m1256[2][:250]
q5 = m1256[3][:250]
q6 = m1256[8][:250]
q7 = m1256[10][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2986 if i < 4 else text_1256
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
