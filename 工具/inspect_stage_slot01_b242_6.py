import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001272_(增强版)股票_20210318量化技术分析_周五之后_更待如何？临门一脚_却是踢向自家_主力仁.md"), "r", encoding="utf-8") as f:
    text_1272 = f.read()

with open(os.path.join(p_stage, "SRC-003002_(增强版)读书_其他_日内交易策略--06.md"), "r", encoding="utf-8") as f:
    text_3002 = f.read()

m1272 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1272)
m3002 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_3002)

q0 = m3002[2][:250]
q1 = m3002[3][:250]
q2 = m3002[4][:250]
q3 = m3002[6][:250]
q4 = m1272[2][:250]
q5 = m1272[4][:250]
q6 = m1272[6][:250]
q7 = m1272[10][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_3002 if i < 4 else text_1272
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
