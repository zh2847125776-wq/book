import json, os, re

slot = "slot_12"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000500_(增强版)期货_期货投机分析20260826.md"), "r", encoding="utf-8") as f:
    text_500 = f.read()

with open(os.path.join(p_stage, "SRC-002943_(增强版)读书_交易思变_量化程序自动交易中的静态仓位与动态仓位.md"), "r", encoding="utf-8") as f:
    text_2943 = f.read()

m500 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_500)
m2943 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2943)

q0 = m2943[2][:250]
q1 = m2943[5][:250]
q2 = m2943[9][:250]
q3 = m2943[10][:250]

q4 = m500[3][:250]
q5 = m500[6][:250]
q6 = m500[10][:250]
q7 = m500[12][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2943 if i < 4 else text_500
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
