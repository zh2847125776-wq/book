import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000524_(增强版)期货_期货投机技术分析20230714_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_524 = f.read()

with open(os.path.join(p_stage, "SRC-002967_(增强版)读书_其他_100倍超级强势股_06.md"), "r", encoding="utf-8") as f:
    text_2967 = f.read()

m524 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_524)
m2967 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2967)

q0 = m2967[4][:250]
q1 = m2967[8][:250]
q2 = m2967[10][:250]
q3 = m524[1][:250]
q4 = m524[2][:250]
q5 = m524[4][:250]
q6 = m524[6][:250]
q7 = m524[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2967 if i < 3 else text_524
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
