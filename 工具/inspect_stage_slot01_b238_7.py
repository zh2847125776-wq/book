import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001246_(增强版)股票_20210201量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1246 = f.read()

with open(os.path.join(p_stage, "SRC-002976_(增强版)读书_其他_亚当理论_04.md"), "r", encoding="utf-8") as f:
    text_2976 = f.read()

m1246 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1246)
m2976 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2976)

q0 = m2976[3][:250]
q1 = m2976[4][:250]
q2 = m2976[10][:250]
q3 = m2976[12][:250]
q4 = m1246[2][:250]
q5 = m1246[8][:250]
q6 = m1246[10][:250]
q7 = m1246[12][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2976 if i < 4 else text_1246
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
