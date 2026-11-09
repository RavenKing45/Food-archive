"""Dev-only QA helper: resolve index.html template markers to file paths so the
taste-skill browser checkers can analyse the real markup/CSS as a single document.

This is NOT part of the application. It writes artifacts/scratch/qa-index.html and
does not touch app.py, index.html or any committed file.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"
OUT = Path(__file__).resolve().parent / "qa-index.html"

# Relative to artifacts/scratch/qa-index.html
PREFIX = "../../assets"

html = (ROOT / "index.html").read_text(encoding="utf-8")

html = html.replace("{{HERO_IMAGE}}", f"{PREFIX}/hero-spices.jpg")
html = html.replace("{{FOOTER_IMAGE}}", f"{PREFIX}/footer-panorama.jpg")

aliases = {
    "vada-pav": "vada-pav-mumbai-commuter-food",
    "rasogulla": "rasgulla-two-regional-traditions",
    "dal-bati": "dal-baati-food-for-the-road",
    "masala-dosa": "masala-dosa-udupi-network",
    "chole-bhature": "chole-bhature-post-partition-delhi",
    "daulat-ki-chat": "daulat-ki-chaat-delhi-winter",
    "daulat-ki-chaat": "daulat-ki-chaat-delhi-winter",
}

story_images: dict[str, str] = {}
for path in sorted((ASSETS / "stories").iterdir()):
    if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        continue
    story_images[path.stem.lower()] = f"{PREFIX}/stories/{path.name}"
for stem, slug in aliases.items():
    if stem in story_images:
        story_images[slug] = story_images[stem]

state_images: dict[str, str] = {}
for path in sorted((ASSETS / "states").iterdir()):
    if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        continue
    state_images[path.stem.lower()] = f"{PREFIX}/states/{path.name}"

state_pages = json.loads((ROOT / "state_pages.json").read_text(encoding="utf-8"))
region_types = {
    slug: region.get("administrativeType", "State") for slug, region in state_pages.items()
}

html = html.replace("{{STORY_IMAGES}}", json.dumps(story_images, ensure_ascii=False))
html = html.replace("{{STATE_IMAGES}}", json.dumps(state_images, ensure_ascii=False))
html = html.replace("{{REGION_TYPES}}", json.dumps(region_types, ensure_ascii=False))

OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT}")
print("remaining markers:", [m for m in ("{{HERO_IMAGE}}", "{{FOOTER_IMAGE}}", "{{STORY_IMAGES}}", "{{STATE_IMAGES}}", "{{REGION_TYPES}}") if m in html])
