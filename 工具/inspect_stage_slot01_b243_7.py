import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000567_(增强版)期货_期货投机技术分析20231016_玻璃_甲醇_豆粕_玉米_沪金_焦炭_棉花_白糖.md"), "r", encoding="utf-8") as f:
    text_567 = f.read()

with open(os.path.join(p_stage, "SRC-001279_(增强版)股票_20210329量化技术分析_3-信号_明显卖出_若是做错_轻易修正_箱体压制_.md"), "r", encoding="utf-8") as f:
    text_1279 = f.read()

m567 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_567)
m1279 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1279)

q0 = m1279[2][:250]
q1 = m1279[3][:250]
q2 = m1279[4][:250]
q3 = m1279[6][:250]
q4 = m567[2][:250]
q5 = m567[3][:250]
q6 = m567[4][:250]
q7 = m567[6][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_1279 if i < 4 else text_567
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
