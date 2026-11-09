"""Dev-only verification: confirm every story image slot resolves to a single image."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
qa = (ROOT / "artifacts/scratch/qa-index.html").read_text(encoding="utf-8")
m = re.search(r"const STORY_SLOT_IMAGES = (\{.*?\});", qa, re.S)
slot_map = json.loads(m.group(1))

stories = json.loads((ROOT / "food_stories.json").read_text(encoding="utf-8"))
total = 0
missing = []
for story in stories:
    for section in story.get("sections", []):
        slot = section.get("imageAfter")
        if not slot:
            continue
        total += 1
        src = slot_map.get(slot["id"], "")
        if not src:
            missing.append(slot["id"])
        kind = "asset" if src.startswith("../../assets") else ("gen" if src.startswith("http") else "??")
        print(f"{kind:5} {slot['id']}")

print(f"\ntotal slots: {total} | mapped: {len(slot_map)} | missing: {missing}")
urls = [v for v in slot_map.values() if v.startswith("http")]
print(f"generated URLs: {len(urls)} | distinct: {len(set(urls))}")
