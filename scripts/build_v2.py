#!/usr/bin/env python3
"""Build data/vn800_v2.json from Vietnamese_3000_v2_FINAL_1.csv."""
import csv, json
from pathlib import Path

ROOT = Path(__file__).parent.parent
SRC = Path("/Users/dj-mbpm3max/Library/CloudStorage/Dropbox/Claude Code Dropbox/KIIP Flashcard/Vietnamese_3000_v2_FINAL_1.csv")
OUT = ROOT / "data" / "vn800_v2.json"
OUT.parent.mkdir(exist_ok=True)

cards = []
with SRC.open(encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        cards.append({
            "no": int(row["No"]),
            "cat": row["Sheet"].strip(),
            "vn": row["VN Word"].strip(),
            "vn_a": row["VN(A)"].strip(),
            "vn_b": row["VN(B)"].strip(),
            "jp": row["JP Word"].strip(),
            "jp_a": row["JP(A)"].strip(),
            "jp_b": row["JP(B)"].strip(),
            "en": row["EN Word"].strip(),
            "en_a": row["EN(A)"].strip(),
            "en_b": row["EN(B)"].strip(),
            "tag": row["Tag"].strip(),
        })
OUT.write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved {len(cards)} v2 cards to {OUT}")

# Also copy the source CSV into project for git tracking
import shutil
dst_csv = ROOT / "Vietnamese_3000_v2_FINAL_1.csv"
shutil.copy(SRC, dst_csv)
print(f"Copied source CSV to {dst_csv}")
