import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000565_(增强版)期货_期货投机技术分析20231012_玻璃_甲醇_豆粕_玉米_沪金_焦炭_棉花_白糖.md"), "r", encoding="utf-8") as f:
    text_565 = f.read()

with open(os.path.join(p_stage, "SRC-001277_(增强版)股票_20210325量化技术分析_因录制设备故障_今日视频分辨率稍差_请大家多包涵.md"), "r", encoding="utf-8") as f:
    text_1277 = f.read()

m565 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_565)
m1277 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1277)

q0 = m1277[2][:250]
q1 = m1277[3][:250]
q2 = m1277[4][:250]
q3 = m1277[6][:250]
q4 = m565[1][:250]
q5 = m565[2][:250]
q6 = m565[3][:250]
q7 = m565[4][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_1277 if i < 4 else text_565
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
