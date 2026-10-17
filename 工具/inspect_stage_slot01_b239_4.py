import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000538_(增强版)期货_期货投机技术分析20230815_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_538 = f.read()

with open(os.path.join(p_stage, "SRC-002981_(增强版)读书_其他_以交易为生_02.md"), "r", encoding="utf-8") as f:
    text_2981 = f.read()

m538 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_538)
m2981 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2981)

q0 = m2981[5][:250]
q1 = m2981[6][:250]
q2 = m2981[10][:250]
q3 = m2981[12][:250]
q4 = m538[3][:250]
q5 = m538[4][:250]
q6 = m538[8][:250]
q7 = m538[10][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2981 if i < 4 else text_538
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
