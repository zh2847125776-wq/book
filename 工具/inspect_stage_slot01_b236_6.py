import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001232_(增强版)股票_20210114量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1232 = f.read()

with open(os.path.join(p_stage, "SRC-002962_(增强版)读书_其他_100倍超级强势股_01.md"), "r", encoding="utf-8") as f:
    text_2962 = f.read()

m1232 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1232)
m2962 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2962)

q0 = m2962[3][:250]
q1 = m2962[4][:250]
q2 = m2962[8][:250]
q3 = m2962[10][:250]
q4 = m1232[1][:250]
q5 = m1232[2][:250]
q6 = m1232[6][:250]
q7 = m1232[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2962 if i < 4 else text_1232
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
