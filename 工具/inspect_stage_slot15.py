import json, os, re

slot = "slot_15"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000502_(增强版)期货_期货投机分析20260831.md"), "r", encoding="utf-8") as f:
    text_502 = f.read()

with open(os.path.join(p_stage, "SRC-002945_(增强版)读书_交易思变_防瀑布机制设置悖论.md"), "r", encoding="utf-8") as f:
    text_2945 = f.read()

m502 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_502)
m2945 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2945)

q0 = m2945[0][:250]
q1 = m2945[2][:250]
q2 = m2945[3][:250]
q3 = m502[3][:250]
q4 = m502[5][:250]
q5 = m502[8][:250]
q6 = m502[10][:250]
q7 = m502[16][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2945 if i < 3 else text_502
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
