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

food_stories = json.loads((ROOT / "food_stories.json").read_text(encoding="utf-8"))

# Mirror app.py: explicit contextual slots first, then genuine dish fallbacks.
slot_context_assets = {
    "vada-pav-mumbai-commuter-food-image-01": "mumbai_03-2016_78_dadar_station",
    "vada-pav-mumbai-commuter-food-image-03": "vada-pav-seller",
    "rasgulla-two-regional-traditions-image-01": "family-trip-jagannath-puri-temple-odisha-775864",
    "rasgulla-two-regional-traditions-image-02": "kolkata-confectioner",
    "masala-dosa-udupi-network-image-02": "spreading-dosa-batter-circular-motion",
    "chole-bhature-post-partition-delhi-image-03": "cooked-chole-added-to-pot",
    "daulat-ki-chaat-delhi-winter-image-02": "daulat-ki-chat-2",
}
slot_dish_assets = {
    "vada-pav-mumbai-commuter-food-image-02": "vada-pav",
    "rasgulla-two-regional-traditions-image-03": "banglar-rosogolla",
    "dal-baati-food-for-the-road-image-01": "dal-baati-churma",
    "chole-bhature-post-partition-delhi-image-01": "chole-bhature",
    "daulat-ki-chaat-delhi-winter-image-03": "old-delhi-chaat",
}


def folder_files(folder: Path) -> dict[str, str]:
    return {
        path.stem.lower(): path.name
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".avif"}
    }


context_files = folder_files(ASSETS / "contextual-story-images")
dish_files = folder_files(ASSETS / "dishes")

slot_images: dict[str, str] = {}
for story in food_stories:
    for section in story.get("sections", []):
        slot = section.get("imageAfter")
        if not slot or not slot.get("id"):
            continue
        slot_id = slot["id"]
        context_name = context_files.get(slot_context_assets.get(slot_id, ""))
        if context_name:
            slot_images[slot_id] = f"{PREFIX}/contextual-story-images/{context_name}"
            continue
        dish_name = dish_files.get(slot_dish_assets.get(slot_id, ""))
        if dish_name:
            slot_images[slot_id] = f"{PREFIX}/dishes/{dish_name}"

html = html.replace("{{STORY_IMAGES}}", json.dumps(story_images, ensure_ascii=False))
html = html.replace("{{STATE_IMAGES}}", json.dumps(state_images, ensure_ascii=False))
html = html.replace("{{REGION_TYPES}}", json.dumps(region_types, ensure_ascii=False))
html = html.replace("{{FOOD_STORIES}}", json.dumps(food_stories, ensure_ascii=False))
html = html.replace("{{STORY_SLOT_IMAGES}}", json.dumps(slot_images, ensure_ascii=False))

OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT}")
print("remaining markers:", [m for m in ("{{HERO_IMAGE}}", "{{FOOTER_IMAGE}}", "{{STORY_IMAGES}}", "{{STATE_IMAGES}}", "{{REGION_TYPES}}", "{{FOOD_STORIES}}", "{{STORY_SLOT_IMAGES}}") if m in html])
