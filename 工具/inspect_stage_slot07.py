import json, os, re

slot = "slot_07"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000503_(增强版)期货_期货投机技术分析20230612_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_503 = f.read()

with open(os.path.join(p_stage, "SRC-001215_(增强版)股票_20201222量化技术分析.md"), "r", encoding="utf-8") as f:
    text_1215 = f.read()

m503 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_503)
m1215 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1215)

q0 = m503[1][:250]
q1 = m503[2][:250]
q2 = m503[8][:250]
q3 = m503[16][:250]
q4 = m1215[2][:250]
q5 = m1215[4][:250]
q6 = m1215[6][:250]
q7 = m1215[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_503 if i < 4 else text_1215
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
