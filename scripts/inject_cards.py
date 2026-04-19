#!/usr/bin/env python3
"""Inject data/vn3000_cards.json into flashcard.html replacing the `const D=[...]` line."""
import json, re
from pathlib import Path

ROOT = Path(__file__).parent.parent
CARDS = ROOT / "data" / "vn3000_cards.json"
HTML = ROOT / "flashcard.html"

data = json.loads(CARDS.read_text(encoding="utf-8"))
line = f"const D={json.dumps(data, ensure_ascii=False)};"
html = HTML.read_text(encoding="utf-8")
new_html, n = re.subn(r"const D=\[.*?\];", line, html, count=1, flags=re.DOTALL)
if n != 1:
    raise SystemExit("Could not find `const D=[...]` in flashcard.html")
HTML.write_text(new_html, encoding="utf-8")
print(f"Injected {len(data)} items into {HTML} (new size: {len(new_html):,} bytes)")
