import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001244_(增强版)股票_20210129量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1244 = f.read()

with open(os.path.join(p_stage, "SRC-002974_(增强版)读书_其他_亚当理论_02.md"), "r", encoding="utf-8") as f:
    text_2974 = f.read()

m1244 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1244)
m2974 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2974)

q0 = m2974[0][:250]
q1 = '“从事交易不需要了解太多，比你看到的还要少。”他'
q2 = m1244[1][:250]
q3 = m1244[2][:250]
q4 = m1244[3][:250]
q5 = m1244[4][:250]
q6 = m1244[5][:250]
q7 = m1244[7][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2974 if i < 2 else text_1244
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
