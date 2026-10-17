import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000511_(增强版)期货_期货投机技术分析20230627_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_511 = f.read()

with open(os.path.join(p_stage, "SRC-001223_(增强版)股票_202100603量化技术分析_60分钟_箱体下限_岌岌可危_明日关注_是否跳空.md"), "r", encoding="utf-8") as f:
    text_1223 = f.read()

m511 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_511)
m1223 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1223)

q0 = m511[1][:250]
q1 = m511[3][:250]
q2 = m511[4][:250]
q3 = m511[6][:250]
q4 = m1223[3][:250]
q5 = m1223[4][:250]
q6 = m1223[5][:250]
q7 = m1223[10][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_511 if i < 4 else text_1223
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
