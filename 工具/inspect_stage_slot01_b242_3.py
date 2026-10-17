import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001270_(增强版)股票_20210316量化技术分析_短线超跌反弹_20x60死叉共振阳线_小周期下降趋.md"), "r", encoding="utf-8") as f:
    text_1270 = f.read()

with open(os.path.join(p_stage, "SRC-003000_(增强版)读书_其他_日内交易策略--03.md"), "r", encoding="utf-8") as f:
    text_3000 = f.read()

m1270 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1270)
m3000 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_3000)

q0 = m3000[3][:250]
q1 = m3000[4][:250]
q2 = m3000[6][:250]
q3 = m3000[8][:250]
q4 = m1270[3][:250]
q5 = m1270[4][:250]
q6 = m1270[6][:250]
q7 = m1270[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_3000 if i < 4 else text_1270
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
