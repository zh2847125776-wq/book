import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001240_(增强版)股票_20210125量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1240 = f.read()

with open(os.path.join(p_stage, "SRC-002970_(增强版)读书_其他_100倍超级强势股_09.md"), "r", encoding="utf-8") as f:
    text_2970 = f.read()

m1240 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1240)
m2970 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2970)

q0 = m2970[2][:250]
q1 = m2970[3][:250]
q2 = m2970[4][:250]
q3 = m2970[6][:250]
q4 = m1240[2][:250]
q5 = m1240[3][:250]
q6 = m1240[6][:250]
q7 = m1240[10][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2970 if i < 4 else text_1240
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
