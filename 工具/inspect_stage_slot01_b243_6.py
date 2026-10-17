import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000566_(增强版)期货_期货投机技术分析20231013_玻璃_甲醇_豆粕_玉米_沪金_焦炭_棉花_白糖.md"), "r", encoding="utf-8") as f:
    text_566 = f.read()

with open(os.path.join(p_stage, "SRC-003009_(增强版)读书_其他_期货投机技术分析20250414_大小周期逆反_交易机会不多.md"), "r", encoding="utf-8") as f:
    text_3009 = f.read()

m566 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_566)
m3009 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_3009)

q0 = m3009[2][:250]
q1 = m3009[3][:250]
q2 = m3009[4][:250]
q3 = m3009[6][:250]
q4 = m566[1][:250]
q5 = m566[2][:250]
q6 = m566[3][:250]
q7 = m566[4][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_3009 if i < 4 else text_566
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
