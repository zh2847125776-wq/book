import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-000520_(增强版)期货_期货投机技术分析20230710_玻璃_甲醇_豆粕_玉米.md"), "r", encoding="utf-8") as f:
    text_520 = f.read()

with open(os.path.join(p_stage, "SRC-002963_(增强版)读书_其他_100倍超级强势股_02.md"), "r", encoding="utf-8") as f:
    text_2963 = f.read()

m520 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_520)
m2963 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2963)

q0 = m2963[1][:250]
q1 = m2963[2][:250]
q2 = m2963[4][:250]
q3 = m2963[10][:250]
q4 = m520[2][:250]
q5 = m520[3][:250]
q6 = m520[4][:250]
q7 = m520[8][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2963 if i < 4 else text_520
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
