import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001280_(增强版)股票_20210330量化技术分析_站上均线_等待回测_压制明显_修复跌多_空间有限_.md"), "r", encoding="utf-8") as f:
    text_1280 = f.read()

with open(os.path.join(p_stage, "SRC-003010_(增强版)读书_其他_止损如何克服贪婪和恐惧一.md"), "r", encoding="utf-8") as f:
    text_3010 = f.read()

m1280 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1280)
m3010 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_3010)

q0 = m3010[2][:250]
q1 = m3010[4][:250]
q2 = m3010[6][:250]
q3 = m3010[8][:250]
q4 = m1280[2][:250]
q5 = m1280[3][:250]
q6 = m1280[4][:250]
q7 = m1280[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_3010 if i < 4 else text_1280
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
