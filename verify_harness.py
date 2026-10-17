import re

with open(r'C:\tmp\arena_stage\SRC-005025_第2307课_明日不要低开明日开盘价是最近两周行情走势关键（学习笔记）.md', 'r', encoding='utf-8') as f:
    src_text = f.read()

# 检验函数
def verify_tsv_row(eid, sid, loc, quote, usage):
    assert eid.startswith("E-") and 66861 <= int(eid.split("-")[1]) <= 66880, f"Invalid eid: {eid}"
    assert sid == "SRC-005025", f"Invalid sid: {sid}"
    assert "\t" not in quote, f"Tab in quote: {eid}"
    assert "\n" not in quote, f"Newline in quote: {eid}"
    assert len(quote) <= 300, f"Quote too long: {len(quote)} for {eid}"
    assert len(quote) >= 8, f"Quote too short: {len(quote)} for {eid}"
    assert quote in src_text, f"Quote not found in src_text: {eid} -> {quote}"
    return True

print("Test harness ready")
