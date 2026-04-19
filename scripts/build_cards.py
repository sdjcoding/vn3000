#!/usr/bin/env python3
"""Build data/vn3000_cards.json from Vietnamese_3000 Phrases_FINAL.csv.

Schema per card:
  { no, cat, vn, vn_ex, jp, jp_ex, en, en_ex, tag }
"""
import csv, json
from pathlib import Path

ROOT = Path(__file__).parent.parent
CSV_FILE = ROOT / "Vietnamese_3000 Phrases_FINAL.csv"
OUT = ROOT / "data" / "vn3000_cards.json"
OUT.parent.mkdir(exist_ok=True)

cards = []
with CSV_FILE.open(encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        cards.append({
            "no": int(row["No"]),
            "cat": row["Sheet"].strip(),
            "vn": row["VN Word"].strip(),
            "vn_ex": row["VN Example"].strip(),
            "jp": row["JP Word"].strip(),
            "jp_ex": row["JP Example"].strip(),
            "en": row["EN Word"].strip(),
            "en_ex": row["EN Example"].strip(),
            "tag": row["Tag"].strip(),
        })

OUT.write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved {len(cards)} cards to {OUT}")

from collections import Counter
cat_counts = Counter(c["cat"] for c in cards)
print(f"\nCategories ({len(cat_counts)}):")
for c, n in cat_counts.most_common():
    print(f"  {c}: {n}")
