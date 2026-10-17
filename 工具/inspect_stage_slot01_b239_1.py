import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000536_(增强版)期货_期货投机技术分析20230809_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_536 = f.read()

with open(os.path.join(p_stage, "SRC-002979_(增强版)读书_其他_交易尽头的光.md"), "r", encoding="utf-8") as f:
    text_2979 = f.read()

m536 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_536)

# 2979 is very short artistic transcript. Let's see if we can use a quote from 2979
q_2979_0 = "漸漸走K纖 傷心的慌張 靈魂說請 換手字接近量子"
q_2979_1 = "換手字接近量子"

q0 = q_2979_0
q1 = m536[0][:250]
q2 = m536[1][:250]
q3 = m536[2][:250]
q4 = m536[3][:250]
q5 = m536[5][:250]
q6 = m536[9][:250]
q7 = m536[16][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2979 if i == 0 else text_536
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
