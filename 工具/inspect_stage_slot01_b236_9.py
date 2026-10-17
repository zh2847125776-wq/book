import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001234_(增强版)股票_20210115量化技术分析_午间加更.md"), "r", encoding="utf-8") as f:
    text_1234 = f.read()

with open(os.path.join(p_stage, "SRC-002964_(增强版)读书_其他_100倍超级强势股_03.md"), "r", encoding="utf-8") as f:
    text_2964 = f.read()

m1234 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1234)
m2964 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2964)

q0 = m2964[8][:250]
q1 = m2964[10][:250]
q2 = m2964[12][:250]
q3 = m1234[2][:250]
q4 = m1234[3][:250]
q5 = m1234[4][:250]
q6 = m1234[6][:250]
q7 = m1234[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2964 if i < 3 else text_1234
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
