import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000564_(增强版)期货_期货投机技术分析20231010_玻璃_甲醇_豆粕_玉米_沪金_焦炭_棉花_白糖.md"), "r", encoding="utf-8") as f:
    text_564 = f.read()

with open(os.path.join(p_stage, "SRC-003007_(增强版)读书_其他_期货投机技术分析20250106_菜粕出现交易机会_其他订单盈利继续持有.md"), "r", encoding="utf-8") as f:
    text_3007 = f.read()

m564 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_564)
m3007 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_3007)

q0 = m3007[2][:250]
q1 = m3007[3][:250]
q2 = m3007[4][:250]
q3 = m3007[6][:250]
q4 = m564[1][:250]
q5 = m564[2][:250]
q6 = m564[3][:250]
q7 = m564[4][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_3007 if i < 4 else text_564
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
