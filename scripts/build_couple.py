#!/usr/bin/env python3
"""Convert vietnamese_couple_300.xlsx into 300 dialog cards.

Each scenario has 4 lines (Anh-Em-Anh-Em). One card per scenario,
split as turn 1 (A side) and turn 2 (B side):
  vn   = situation (Korean)
  vn_a = "Anh: ...\nEm: ..."  (turn 1 in Vietnamese)
  vn_b = "Anh: ...\nEm: ..."  (turn 2 in Vietnamese)
  jp_a = JP translation of turn 1 (男:/女: labels)
  jp_b = JP translation of turn 2
  en_a/en_b/en/jp = empty
  cat  = "커플 대화"
  tag  = original Korean situation category
"""
import json, openpyxl, shutil, urllib.parse, urllib.request, time, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SRC = Path("/Users/dj-mbpm3max/Downloads/vietnamese_couple_300.xlsx")
OUT = ROOT / "data" / "couple_cards.json"
CACHE = ROOT / "data" / ".vn_jp_cache.json"

# Translation cache (so reruns skip already-translated lines)
cache = {}
if CACHE.exists():
    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    print(f"Loaded {len(cache)} cached translations")

def translate_vi_ja(text):
    text = text.strip()
    if not text:
        return ""
    if text in cache:
        return cache[text]
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=vi&tl=ja&dt=t&q=" + urllib.parse.quote(text)
    for attempt in range(3):
        try:
            r = urllib.request.urlopen(url, timeout=10)
            data = json.loads(r.read())
            jp = "".join(seg[0] for seg in data[0])
            cache[text] = jp
            return jp
        except Exception as e:
            if attempt == 2:
                print(f"  ⚠ failed for {text!r}: {e}")
                return text  # fallback to original
            time.sleep(1.5 ** attempt)

# Parse Excel
wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
ws = wb["베트남어 커플 대화 300"]
scenarios = []
current = None
for row in ws.iter_rows(min_row=2, values_only=True):
    no, cat_orig, situation, speaker, vn, ko, note = row
    if no is not None:
        if current:
            scenarios.append(current)
        current = {"no": int(no), "cat_orig": cat_orig, "situation": situation, "lines": []}
    if speaker and vn:
        current["lines"].append({"speaker": speaker.strip(), "vn": vn.strip(), "ko": (ko or "").strip()})
if current:
    scenarios.append(current)

print(f"Parsed {len(scenarios)} scenarios, {sum(len(s['lines']) for s in scenarios)} lines")

# Translate all unique VN lines
unique_vn = set()
for sc in scenarios:
    for l in sc["lines"]:
        unique_vn.add(l["vn"])
todo = [v for v in unique_vn if v not in cache]
print(f"Translating {len(todo)} new lines (cache hit: {len(unique_vn) - len(todo)})")

t0 = time.time()
for i, vn in enumerate(todo, 1):
    translate_vi_ja(vn)
    if i % 20 == 0 or i == len(todo):
        elapsed = time.time() - t0
        rate = i / elapsed
        eta = (len(todo) - i) / rate if rate else 0
        print(f"  [{i}/{len(todo)}] rate={rate:.1f}/s ETA={eta:.0f}s")
        # Save cache periodically
        CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    time.sleep(0.05)
CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

# Build cards: 1 per scenario, A=turn1, B=turn2
START_NO = 801
CAT = "커플 대화"
def jp_speaker(s):
    return "男" if s == "Anh" else ("女" if s == "Em" else s)

cards = []
for i, sc in enumerate(scenarios):
    lines = sc["lines"]
    if len(lines) != 4:
        print(f"  ⚠ scenario {sc['no']} has {len(lines)} lines (expected 4)")
        continue
    # Turn 1: lines 0,1   Turn 2: lines 2,3
    def fmt_vn(ls):
        return "\n".join(f"{l['speaker']}: {l['vn']}" for l in ls)
    def fmt_jp(ls):
        return "\n".join(f"{jp_speaker(l['speaker'])}: {cache.get(l['vn'], '')}" for l in ls)
    cards.append({
        "no": START_NO + i,
        "cat": CAT,
        "vn": sc["situation"] or "대화",
        "vn_a": fmt_vn(lines[0:2]),
        "vn_b": fmt_vn(lines[2:4]),
        "jp": "",
        "jp_a": fmt_jp(lines[0:2]),
        "jp_b": fmt_jp(lines[2:4]),
        "en": "",
        "en_a": "",
        "en_b": "",
        "tag": sc["cat_orig"] or "Dialog",
    })

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nWrote {len(cards)} couple cards to {OUT.name}")
print(f"\nFirst card sample:")
print(json.dumps(cards[0], ensure_ascii=False, indent=2))

shutil.copy(SRC, ROOT / "vietnamese_couple_300.xlsx")
print(f"\nCopied source xlsx to project root")
