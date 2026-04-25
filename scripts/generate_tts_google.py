#!/usr/bin/env python3
"""Generate MP3 audio for vn800_v2.json using Google Cloud Text-to-Speech.

Usage:
    export GOOGLE_TTS_KEY='AIzaSy...'
    python3 scripts/generate_tts_google.py

Outputs:
    audio/<no>_<field>.mp3   (e.g. audio/0001_vn.mp3, audio/0001_jp_a.mp3)

Generates 6 files per card:
    vn / vn_a / vn_b   (Vietnamese: word, example A, example B)
    jp / jp_a / jp_b   (Japanese:   word, example A, example B)

Resumable: skips files that already exist. Re-run after errors.
"""

import os
import sys
import json
import re
import time
import base64
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_FILE = ROOT / "data" / "vn800_v2.json"
AUDIO_DIR = ROOT / "audio"
AUDIO_DIR.mkdir(exist_ok=True)

API_KEY = os.environ.get("GOOGLE_TTS_KEY")
if not API_KEY:
    sys.exit("ERROR: set GOOGLE_TTS_KEY env var first.\n"
             "  export GOOGLE_TTS_KEY='AIzaSy...'")

# Voice config
VN_VOICE = {"languageCode": "vi-VN", "name": "vi-VN-Neural2-A"}  # female
JP_VOICE = {"languageCode": "ja-JP", "name": "ja-JP-Neural2-B"}  # female
AUDIO_CONFIG = {"audioEncoding": "MP3", "speakingRate": 0.95, "sampleRateHertz": 24000}

ENDPOINT = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={API_KEY}"
RUBY_RE = re.compile(r"<rt>.*?</rt>", re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")

def strip_ruby(text):
    """Remove <ruby><rt>...</rt></ruby> furigana, keep base kanji.
    e.g. '<ruby>会<rt>あ</rt></ruby>いできて' -> '会いできて'
    """
    if not text:
        return ""
    # Drop the <rt>kana</rt> portion entirely (TTS knows pronunciation from kanji)
    t = RUBY_RE.sub("", text)
    # Drop remaining <ruby> / </ruby> tags, keeping inner content
    t = TAG_RE.sub("", t)
    return t.strip()


def synthesize(text, voice):
    """Call Google TTS REST API; return MP3 bytes or raise."""
    payload = json.dumps({
        "input": {"text": text},
        "voice": voice,
        "audioConfig": AUDIO_CONFIG,
    }).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.loads(r.read())
    return base64.b64decode(result["audioContent"])


def main():
    cards = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    print(f"Loaded {len(cards)} cards from {DATA_FILE.name}")

    # Build job list: (filename, text, voice)
    jobs = []
    for card in cards:
        no = f"{card['no']:04d}"
        for field, voice in [
            ("vn",   VN_VOICE),
            ("vn_a", VN_VOICE),
            ("vn_b", VN_VOICE),
            ("jp",   JP_VOICE),
            ("jp_a", JP_VOICE),
            ("jp_b", JP_VOICE),
        ]:
            raw = card.get(field, "")
            text = strip_ruby(raw) if field.startswith("jp") else raw
            if not text:
                continue
            fname = AUDIO_DIR / f"{no}_{field}.mp3"
            jobs.append((fname, text, voice))

    total = len(jobs)
    skipped = sum(1 for f, _, _ in jobs if f.exists())
    todo = [j for j in jobs if not j[0].exists()]
    print(f"Total jobs: {total}  |  Already done: {skipped}  |  To do: {len(todo)}\n")

    char_count = 0
    done = 0
    failed = []
    t0 = time.time()
    for fname, text, voice in todo:
        try:
            mp3 = synthesize(text, voice)
            fname.write_bytes(mp3)
            char_count += len(text)
            done += 1
            if done % 25 == 0 or done == len(todo):
                elapsed = time.time() - t0
                rate = done / elapsed
                eta = (len(todo) - done) / rate if rate else 0
                print(f"  [{done:>4}/{len(todo)}] {fname.name}  "
                      f"chars={char_count:>6}  "
                      f"rate={rate:.1f}/s  ETA={eta/60:.1f}min")
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")[:200]
            print(f"  ✗ HTTP {e.code} on {fname.name}: {err}")
            failed.append((fname, text, str(e)))
            if e.code == 429:
                print("  Rate-limited. Sleeping 60s...")
                time.sleep(60)
        except Exception as e:
            print(f"  ✗ {fname.name}: {e}")
            failed.append((fname, text, str(e)))
        # Tiny delay to be polite (Google allows 1000 req/min, we use ~5/s here)
        time.sleep(0.05)

    print(f"\n=== Done ===")
    print(f"Generated: {done} files, {char_count:,} chars (~${char_count/1_000_000*16:.4f} if billed)")
    print(f"Total audio files: {len(list(AUDIO_DIR.glob('*.mp3')))}")
    if failed:
        print(f"Failed: {len(failed)} (re-run script to retry)")
        for fname, _, err in failed[:5]:
            print(f"  - {fname.name}: {err[:80]}")


if __name__ == "__main__":
    main()
