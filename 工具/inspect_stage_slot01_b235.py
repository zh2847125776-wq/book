import json, os, re

slot = "slot_01"
p_stage = f"分片工作区/Shard3_b220_243/slots/{slot}/stage"

with open(os.path.join(p_stage, "SRC-001222_(增强版)股票_202100408量化技术分析_六十分钟_按部就班_一切就绪_只欠西风_负乖离率.md"), "r", encoding="utf-8") as f:
    text_1222 = f.read()

with open(os.path.join(p_stage, "SRC-002952_(增强版)读书_交易择时技术分析_07.md"), "r", encoding="utf-8") as f:
    text_2952 = f.read()

m1222 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1222)
m2952 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_2952)

q0 = m2952[3][:250]
q1 = m2952[4][:250]
q2 = m2952[6][:250]
q3 = m2952[10][:250]
q4 = m1222[2][:250]
q5 = m1222[3][:250]
q6 = m1222[8][:250]
q7 = m1222[12][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_2952 if i < 4 else text_1222
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
