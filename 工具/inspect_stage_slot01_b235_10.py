import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001228_(增强版)股票_20210108量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1228 = f.read()

with open(os.path.join(p_stage, "SRC-002958_(增强版)读书_交易择时技术分析_13.md"), "r", encoding="utf-8") as f:
    text_2958 = f.read()

m1228 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1228)
m2958 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2958)

q0 = m2958[1][:250]
q1 = m2958[2][:250]
q2 = m2958[3][:250]
q3 = m2958[4][:250]
q4 = m1228[3][:250]
q5 = m1228[4][:250]
q6 = m1228[8][:250]
q7 = m1228[10][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2958 if i < 4 else text_1228
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
