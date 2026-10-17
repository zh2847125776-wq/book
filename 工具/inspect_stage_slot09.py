with open("分片工作区/Shard3_b220_243/slots/slot_09/stage/SRC-000499_(增强版)期货_期货投机分析20260825.md", "r", encoding="utf-8") as f:
    text_499 = f.read()

with open("分片工作区/Shard3_b220_243/slots/slot_09/stage/SRC-001211_(增强版)股票_20201216量化技术分析.md", "r", encoding="utf-8") as f:
    text_1211 = f.read()

import re
m499 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_499)
m1211 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1211)

# E-87700: 499 #2 本周期MZ变色与无需死叉穿轴机理
q0 = m499[2][:250]
# E-87701: 499 #3 等待高MZ掉下来共振与止损权衡
q1 = m499[3][:250]
# E-87702: 499 #18 蓝线断掉后首次贴近K线有效性判据
q2 = m499[18][:250]
# E-87703: 499 #16 单MZ系统破线收K止损与重新接回规则
q3 = m499[16][:250]
# E-87704: 1211 #2 上涨1000家下跌3000家之指数微幅波动个股普跌吊诡现象
q4 = m1211[2][:250]
# E-87705: 1211 #3 白线走平黄线下杀与白黄线分化
q5 = m1211[3][:250]
# E-87706: 1211 #6 早盘集合竞价量能萎缩预警个股杀破20日线
q6 = m1211[6][:250]
# E-87707: 1211 #10 无量站上向下5日线无效性定性
q7 = m1211[10][:250]
# E-87708: 1211 #12 量价关系重置后放量收阳缩量收阴预判律
q8 = m1211[12][:250]

quotes = [q0, q1, q2, q3, q4, q5, q6, q7, q8]
for i, q in enumerate(quotes):
    src = text_1211 if i >= 4 else text_499
    ok = q in src and len(q) <= 300 and "\n" not in q
    print(f"Quote {i}: ok={ok}, len={len(q)}")
    if not ok:
        print("  failed:", repr(q[:30]))
