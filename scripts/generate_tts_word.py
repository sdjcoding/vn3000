#!/usr/bin/env python3
"""TTS for 단어 (flashcard.html) cards using vi-VN-Chirp3-HD-Achernar.

Generates 2 files per card (word + example). Filename prefix `w_` to
avoid colliding with practice.html's audio files.
  audio/w_{no}_vn.mp3      — the word (d.vn)
  audio/w_{no}_vn_ex.mp3   — the example sentence (d.vn_ex)
"""
import os, sys, json, re, time, base64
import urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).parent.parent
HTML = ROOT / "flashcard.html"
AUDIO = ROOT / "audio"
AUDIO.mkdir(exist_ok=True)
API_KEY = os.environ.get("GOOGLE_TTS_KEY")
if not API_KEY:
    sys.exit("Set GOOGLE_TTS_KEY env var.")

VOICE = {"languageCode": "vi-VN", "name": "vi-VN-Chirp3-HD-Achernar"}
ENDPOINT = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={API_KEY}"
AUDIO_CFG = {"audioEncoding": "MP3", "speakingRate": 0.95, "sampleRateHertz": 24000}

def synth(text):
    payload = json.dumps({"input": {"text": text}, "voice": VOICE, "audioConfig": AUDIO_CFG}).encode()
    req = urllib.request.Request(ENDPOINT, data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return base64.b64decode(json.loads(r.read())["audioContent"])

# Extract data from flashcard.html
html = HTML.read_text(encoding="utf-8")
m = re.search(r'const D=(\[.*?\]);', html, re.DOTALL)
cards = json.loads(m.group(1))
print(f"Loaded {len(cards)} cards from flashcard.html")

jobs = []
for c in cards:
    no = f"{c['no']:04d}"
    if c.get("vn"):
        jobs.append((AUDIO / f"w_{no}_vn.mp3", c["vn"]))
    if c.get("vn_ex"):
        jobs.append((AUDIO / f"w_{no}_vn_ex.mp3", c["vn_ex"]))
todo = [j for j in jobs if not j[0].exists()]
print(f"Total: {len(jobs)}  Done: {len(jobs)-len(todo)}  To do: {len(todo)}")

t0 = time.time()
done = 0
failed = []
for fname, text in todo:
    try:
        fname.write_bytes(synth(text))
        done += 1
        if done % 25 == 0 or done == len(todo):
            elapsed = time.time() - t0
            rate = done / elapsed
            eta = (len(todo) - done) / rate if rate else 0
            print(f"  [{done:>4}/{len(todo)}] {fname.name}  rate={rate:.1f}/s ETA={eta/60:.1f}min")
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")[:120]
        print(f"  ✗ {fname.name}: HTTP {e.code} — {err}")
        failed.append(fname.name)
        if e.code == 429: time.sleep(30)
    except Exception as e:
        print(f"  ✗ {fname.name}: {e}")
        failed.append(fname.name)
    time.sleep(0.05)
print(f"\nGenerated: {done}, Failed: {len(failed)}")
