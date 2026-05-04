#!/usr/bin/env python3
"""Generates site/index.html from captures/ for GitHub Pages."""
import json
import shutil
from pathlib import Path

CAPTURES_DIR = Path("captures")
SITE_DIR = Path("site")
INDEX_FILE = CAPTURES_DIR / "index.json"

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
VIDEO_EXTS = {".mp4", ".mov", ".webm"}


def load_index() -> dict:
    if INDEX_FILE.exists():
        with open(INDEX_FILE) as f:
            return {item["file"]: item for item in json.load(f)}
    return {}


def build() -> None:
    SITE_DIR.mkdir(exist_ok=True)

    captures_site = SITE_DIR / "captures"
    if captures_site.exists():
        shutil.rmtree(captures_site)
    shutil.copytree(
        CAPTURES_DIR,
        captures_site,
        ignore=shutil.ignore_patterns("*.json", ".gitkeep"),
    )

    index = load_index()
    entries = []

    for f in sorted(CAPTURES_DIR.iterdir(), reverse=True):
        if f.suffix.lower() not in IMAGE_EXTS | VIDEO_EXTS:
            continue
        meta = index.get(f.name, {})
        entries.append({
            "file": f.name,
            "caption": meta.get("caption", ""),
            "timestamp": meta.get("timestamp", ""),
            "is_video": f.suffix.lower() in VIDEO_EXTS,
        })

    (SITE_DIR / "index.html").write_text(render_html(entries), encoding="utf-8")
    print(f"Built site with {len(entries)} entr{'y' if len(entries) == 1 else 'ies'}.")


def render_html(entries: list) -> str:
    cards = ""
    for e in entries:
        src = f"captures/{e['file']}"
        date = e["timestamp"][:10] if e["timestamp"] else ""
        caption = e["caption"] or e["file"]
        safe_caption = caption.replace("<", "&lt;").replace(">", "&gt;")

        if e["is_video"]:
            media = f'<video src="{src}" controls loop muted playsinline></video>'
        else:
            media = f'<img src="{src}" alt="{safe_caption}" loading="lazy">'

        cards += f"""
    <article class="card">
      <div class="media">{media}</div>
      <div class="meta">
        <p class="caption">{safe_caption}</p>
        <time>{date}</time>
      </div>
    </article>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Postgal</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: system-ui, -apple-system, sans-serif;
      background: #0d0d0d;
      color: #d0d0d0;
      padding: 2rem 1rem;
    }}
    h1 {{
      text-align: center;
      margin-bottom: 2rem;
      font-size: 1.4rem;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: #fff;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 1.5rem;
      max-width: 1200px;
      margin: 0 auto;
    }}
    .card {{
      background: #1a1a1a;
      border-radius: 8px;
      overflow: hidden;
    }}
    .media {{
      aspect-ratio: 16 / 9;
      background: #111;
      overflow: hidden;
    }}
    .media img,
    .media video {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .meta {{
      padding: 0.75rem 1rem;
    }}
    .caption {{
      font-size: 0.875rem;
      line-height: 1.4;
      margin-bottom: 0.3rem;
    }}
    time {{
      font-size: 0.75rem;
      color: #666;
    }}
  </style>
</head>
<body>
  <h1>Postgal</h1>
  <div class="grid">{cards}
  </div>
</body>
</html>"""


if __name__ == "__main__":
    build()
