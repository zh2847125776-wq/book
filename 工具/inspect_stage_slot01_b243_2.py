with open("分片工作区/Shard3_b220_243/slots/slot_01/stage/SRC-001276_(增强版)股票_20210324量化技术分析_三种情况_三种结构_殊途同归_不做多_不放空_多看.md", "r", encoding="utf-8") as f:
    text_1276 = f.read()

with open("分片工作区/Shard3_b220_243/slots/slot_01/stage/SRC-003006_(增强版)读书_其他_晨报20220318.md", "r", encoding="utf-8") as f:
    text_3006 = f.read()

import re
m1276 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1276)

q0 = "创指冲高回落突破失败 前低正好压制 20日线提供稳定压制"
q1 = "商业指数方面 混沌逻辑映射公式压制明显"
q2 = m1276[4][:250]
q3 = m1276[6][:250]
q4 = m1276[8][:250]
q5 = m1276[10][:250]
q6 = m1276[12][:250]
q7 = m1276[14][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7]
for i, q in enumerate(quotes):
    src = text_3006 if i < 2 else text_1276
    ok = q in src and len(q) <= 300 and "\n" not in q and len(q) >= 8
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
