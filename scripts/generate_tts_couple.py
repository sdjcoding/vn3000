#!/usr/bin/env python3
"""Generate TTS MP3 for the 친구 대화 (couple) cards.

Files per card (no = 801..1100):
  audio/{no}_a_1.mp3  — turn 1, line 1 (speaker A, male voice)
  audio/{no}_a_2.mp3  — turn 1, line 2 (speaker B, female voice)
  audio/{no}_b_1.mp3  — turn 2, line 1 (A, male)
  audio/{no}_b_2.mp3  — turn 2, line 2 (B, female)
  audio/{no}_a_1_jp.mp3 / _a_2_jp.mp3 / _b_1_jp.mp3 / _b_2_jp.mp3
"""
import os, sys, json, re, time, base64
import urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "couple_cards.json"
AUDIO = ROOT / "audio"
AUDIO.mkdir(exist_ok=True)

API_KEY = os.environ.get("GOOGLE_TTS_KEY")
if not API_KEY:
    sys.exit("Set GOOGLE_TTS_KEY env var.")

VOICES = {
    "vn_A": {"languageCode": "vi-VN", "name": "vi-VN-Chirp3-HD-Achird"},   # male
    "vn_B": {"languageCode": "vi-VN", "name": "vi-VN-Chirp3-HD-Leda"},     # female
    "jp_A": {"languageCode": "ja-JP", "name": "ja-JP-Chirp3-HD-Achird"},   # male
    "jp_B": {"languageCode": "ja-JP", "name": "ja-JP-Chirp3-HD-Achernar"}, # female
}
ENDPOINT = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={API_KEY}"
AUDIO_CFG = {"audioEncoding": "MP3", "speakingRate": 0.95, "sampleRateHertz": 24000}


def synth(text, voice):
    payload = json.dumps({
        "input": {"text": text},
        "voice": voice,
        "audioConfig": AUDIO_CFG,
    }).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return base64.b64decode(json.loads(r.read())["audioContent"])


def split_lines(field):
    """Return [(speaker, text), ...] from "A: ...\nB: ..." string."""
    out = []
    for ln in field.split("\n"):
        m = re.match(r'^([AB]):\s*(.+)$', ln.strip())
        if m:
            out.append((m.group(1), m.group(2).strip()))
    return out


cards = json.loads(DATA.read_text(encoding="utf-8"))
print(f"Loaded {len(cards)} couple cards")

jobs = []
for c in cards:
    no = f"{c['no']:04d}"
    for side, vn_field, jp_field in [("a", "vn_a", "jp_a"), ("b", "vn_b", "jp_b")]:
        vn_lines = split_lines(c.get(vn_field, ""))
        jp_lines = split_lines(c.get(jp_field, ""))
        for i, (spk, vn_text) in enumerate(vn_lines, 1):
            jobs.append((AUDIO / f"{no}_{side}_{i}.mp3", vn_text, VOICES[f"vn_{spk}"]))
        for i, (spk, jp_text) in enumerate(jp_lines, 1):
            jobs.append((AUDIO / f"{no}_{side}_{i}_jp.mp3", jp_text, VOICES[f"jp_{spk}"]))

todo = [j for j in jobs if not j[0].exists()]
print(f"Total jobs: {len(jobs)}, already done: {len(jobs)-len(todo)}, to do: {len(todo)}")

t0 = time.time()
done = 0
failed = []
for fname, text, voice in todo:
    try:
        mp3 = synth(text, voice)
        fname.write_bytes(mp3)
        done += 1
        if done % 25 == 0 or done == len(todo):
            elapsed = time.time() - t0
            rate = done / elapsed
            eta = (len(todo) - done) / rate if rate else 0
            print(f"  [{done:>4}/{len(todo)}] {fname.name}  rate={rate:.1f}/s ETA={eta/60:.1f}min")
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")[:150]
        print(f"  ✗ {fname.name}: HTTP {e.code} — {err}")
        failed.append(fname.name)
        if e.code == 429:
            time.sleep(30)
    except Exception as e:
        print(f"  ✗ {fname.name}: {e}")
        failed.append(fname.name)
    time.sleep(0.05)

print(f"\nGenerated: {done}, Failed: {len(failed)}")
if failed:
    print("Failed files (re-run to retry):", failed[:5])
