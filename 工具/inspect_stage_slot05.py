with open("分片工作区/Shard3_b220_243/slots/slot_05/stage/SRC-001212_(增强版)股票_20201217量化技术分析.md", "r", encoding="utf-8") as f:
    text_1212 = f.read()

import re
m1212 = re.findall(r"\*\*🎙 语音转录\(前后30s\)\*\*: (.*?)\n", text_1212)

# sub-slice <= 280 chars
indices = [5, 6, 8, 9, 10, 12, 25, 27, 28]
quotes = []
for idx in indices:
    s = m1212[idx][:250]
    quotes.append(s)
    ok = s in text_1212 and len(s) <= 300 and "\n" not in s
    print(f"Index {idx}: ok={ok}, len={len(s)}")

print("Total quotes:", len(quotes))
