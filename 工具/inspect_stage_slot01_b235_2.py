import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000510_(增强版)期货_期货投机技术分析20230626_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_510 = f.read()

with open(os.path.join(p_stage, "SRC-002953_(增强版)读书_交易择时技术分析_08.md"), "r", encoding="utf-8") as f:
    text_2953 = f.read()

m510 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_510)
m2953 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2953)

q0 = m2953[1][:250]
q1 = m2953[2][:250]
q2 = m2953[3][:250]
q3 = m2953[6][:250]
q4 = m510[2][:250]
q5 = m510[4][:250]
q6 = m510[6][:250]
q7 = m510[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2953 if i < 4 else text_510
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
