import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001278_(增强版)股票_20210326量化技术分析_缩量反弹_技术调整_空间不足_时间不够_多看少做_.md"), "r", encoding="utf-8") as f:
    text_1278 = f.read()

with open(os.path.join(p_stage, "SRC-003008_(增强版)读书_其他_期货投机技术分析20250407_原油订单表现出色_其他交易机会难抓.md"), "r", encoding="utf-8") as f:
    text_3008 = f.read()

m1278 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1278)
m3008 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_3008)

q0 = m1278[3][:250]
q1 = m1278[4][:250]
q2 = m1278[6][:250]
q3 = m1278[8][:250]
q4 = m3008[2][:250]
q5 = m3008[3][:250]
q6 = m3008[4][:250]
q7 = m3008[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_1278 if i < 4 else text_3008
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
