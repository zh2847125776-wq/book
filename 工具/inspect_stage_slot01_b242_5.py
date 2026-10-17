import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000559_(增强版)期货_期货投机技术分析20230922_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_559 = f.read()

with open(os.path.join(p_stage, "SRC-001271_(增强版)股票_20210317量化技术分析_渡了一场小劫_时间窗口还有两天_周五尾盘周一早盘尤.md"), "r", encoding="utf-8") as f:
    text_1271 = f.read()

m559 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_559)
m1271 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1271)

q0 = m1271[2][:250]
q1 = m1271[3][:250]
q2 = m1271[4][:250]
q3 = m1271[7][:250]
q4 = m559[1][:250]
q5 = m559[2][:250]
q6 = m559[3][:250]
q7 = m559[4][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_1271 if i < 4 else text_559
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
