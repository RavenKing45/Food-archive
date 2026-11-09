"""Streamlit launcher for India's Culinary Memory Archive.

The homepage remains the existing index.html. State chapters are loaded from
state_pages.json and injected into the same page as a client-side book-style
view. Optional state and dish photography is loaded from assets/ without
requiring changes to the HTML or Python whenever images are added.
"""

from __future__ import annotations

import base64
import json
from io import BytesIO
from pathlib import Path

import streamlit as st
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
SUPPORTED_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".avif"}

st.set_page_config(
    page_title="India's Culinary Memory Archive",
    page_icon="✧",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def image_data_uri(path: Path) -> str:
    """Resize and optimize supported images; preserve AVIF bytes for the browser."""
    # Pillow installations do not universally include an AVIF decoder. Browsers
    # support AVIF directly, so embed the original bytes instead of failing to load.
    if path.suffix.lower() == ".avif":
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"data:image/avif;base64,{encoded}"

    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source)
        image.thumbnail((2200, 1500), Image.Resampling.LANCZOS)

        output = BytesIO()
        if image.mode in {"RGBA", "LA"}:
            image.save(output, format="WEBP", quality=88, method=6)
            mime_type = "image/webp"
        else:
            image.convert("RGB").save(
                output,
                format="JPEG",
                quality=88,
                optimize=True,
                progressive=True,
            )
            mime_type = "image/jpeg"

    encoded = base64.b64encode(output.getvalue()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def image_folder_signature(folder_path: str) -> tuple[tuple[str, int, int], ...]:
    """Return a cache key that changes when files in an image folder change."""
    folder = Path(folder_path)
    if not folder.exists():
        return ()
    return tuple(
        (path.name, path.stat().st_size, path.stat().st_mtime_ns)
        for path in sorted(folder.iterdir())
        if path.is_file() and path.suffix.lower() in SUPPORTED_IMAGE_SUFFIXES
    )


@st.cache_data(show_spinner=False)
def image_folder_map(
    folder_path: str,
    file_signature: tuple[tuple[str, int, int], ...] = (),
) -> dict[str, str]:
    """Load optional images keyed by filename stem (without extension)."""
    folder = Path(folder_path)
    images: dict[str, str] = {}
    if not folder.exists():
        return images

    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_IMAGE_SUFFIXES:
            continue
        try:
            images[path.stem.lower()] = image_data_uri(path)
        except (OSError, ValueError) as error:
            st.warning(f"Skipped unreadable image '{path.name}': {error}")

    return images


def load_state_pages(path: Path) -> dict:
    """Read and minimally validate the state content file."""
    if not path.is_file():
        st.error("state_pages.json was not found. Keep it beside app.py.")
        st.stop()

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        st.error(f"Could not read state_pages.json: {error}")
        st.stop()

    if not isinstance(payload, dict):
        st.error("state_pages.json must contain a JSON object keyed by state slug.")
        st.stop()

    return payload


index_path = ROOT / "index.html"
if not index_path.is_file():
    st.error("index.html was not found. Keep it beside app.py in the project folder.")
    st.stop()

html = index_path.read_text(encoding="utf-8")

required_assets = {
    "{{HERO_IMAGE}}": ASSETS / "hero-spices.jpg",
    "{{FOOTER_IMAGE}}": ASSETS / "footer-panorama.jpg",
}
for marker, asset_path in required_assets.items():
    if not asset_path.is_file():
        st.error(f"Required visual asset is missing: {asset_path.relative_to(ROOT)}")
        st.stop()
    html = html.replace(marker, image_data_uri(asset_path))

story_images = image_folder_map(str(ASSETS / "stories"), image_folder_signature(str(ASSETS / "stories")))

# Match the human-readable image filenames in assets/stories/ to the story
# slugs used by index.html. Keep the original stem keys as well.
story_image_aliases = {
    "vada-pav": "vada-pav-mumbai-commuter-food",
    "rasogulla": "rasgulla-two-regional-traditions",
    "dal-bati": "dal-baati-food-for-the-road",
    "masala-dosa": "masala-dosa-udupi-network",
    "chole-bhature": "chole-bhature-post-partition-delhi",
    # The supplied folder screenshot used "chat" (one "a" in the filename).
    # Accept both spellings so either daulat-ki-chat.jpg or daulat-ki-chaat.jpg works.
    "daulat-ki-chat": "daulat-ki-chaat-delhi-winter",
    "daulat-ki-chaat": "daulat-ki-chaat-delhi-winter",
}
for image_stem, story_slug in story_image_aliases.items():
    if image_stem in story_images:
        story_images[story_slug] = story_images[image_stem]

state_images = image_folder_map(str(ASSETS / "states"), image_folder_signature(str(ASSETS / "states")))
dish_images = image_folder_map(str(ASSETS / "dishes"), image_folder_signature(str(ASSETS / "dishes")))

html = html.replace("{{STORY_IMAGES}}", json.dumps(story_images, ensure_ascii=False))
html = html.replace("{{STATE_IMAGES}}", json.dumps(state_images, ensure_ascii=False))

state_pages = load_state_pages(ROOT / "state_pages.json")


def json_for_script(value: object) -> str:
    """Serialize JSON safely for insertion into an inline script."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


region_types = {slug: region.get("administrativeType", "State") for slug, region in state_pages.items()}
html = html.replace("{{REGION_TYPES}}", json_for_script(region_types))


STATE_PAGE_EXTENSION = r"""
<style id="archive-state-page-styles">
  /* ── State/Region page — refined to match main archive design system ── */
  :root {
    --sp-maroon-deep: #150605;
    --sp-maroon:      #230b08;
    --sp-maroon-mid:  #381410;
    --sp-terracotta:  #843422;
    --sp-saffron:     #a34d28;
    --sp-ink:         #241512;
    --sp-ink-mid:     #422922;
    --sp-muted:       #6e5044;
    --sp-paper:       #f4ede0;
    --sp-paper-card:  #fcf8f1;
    --sp-paper-warm:  #eee4d2;
    --sp-paper-deep:  #dfd2bc;
    --sp-gold:        #b89251;
    --sp-gold-light:  #d9b679;
    --sp-gold-pale:   #edd8b2;
    --sp-line:        rgba(70, 36, 22, 0.18);
    --sp-line-brass:  rgba(184, 146, 81, 0.35);
    --sp-serif:       "Cormorant Garamond", Garamond, Georgia, serif;
    --sp-body:        "Libre Baskerville", Baskerville, Georgia, serif;
    --sp-ease-out:    cubic-bezier(0.23, 1, 0.32, 1);
    --sp-btn-scale:   0.972;
  }
  .state-page-root {
    display: none;
    min-height: 100vh;
    color: var(--sp-ink);
    background-color: var(--sp-paper);
    background-image:
      radial-gradient(circle at 10% 8%, rgba(255, 255, 255, 0.4), transparent 28%),
      radial-gradient(circle at 90% 40%, rgba(184, 146, 81, 0.08), transparent 32%),
      repeating-linear-gradient(0deg, rgba(70, 36, 22, 0.012) 0, rgba(70, 36, 22, 0.012) 1px, transparent 1px, transparent 8px);
    font-family: var(--sp-body);
    font-size: 15px;
    animation: statePageFadeIn 240ms var(--sp-ease-out);
  }
  @keyframes statePageFadeIn {
    from { opacity: 0; transform: scale(0.985); }
    to   { opacity: 1; transform: scale(1); }
  }
  .state-page-root * { box-sizing: border-box; }
  .state-page-root button, .state-page-root a { font: inherit; cursor: pointer; }
  .state-page-root a { color: inherit; text-decoration: none; }

  /* Top bar */
  .state-page-topbar {
    min-height: 64px;
    padding: 10px 30px 10px clamp(220px, 18vw, 280px);
    display: flex; align-items: center; justify-content: space-between;
    color: #fff1d8;
    background: var(--sp-maroon-deep);
    border-bottom: 1px solid var(--sp-line-brass);
  }
  .state-page-brand {
    display: flex; align-items: center; gap: 14px;
    font: 700 20px/1 var(--sp-serif);
    color: #f5e9d0;
  }
  .state-page-brand-mark { width: 38px; height: 38px; color: var(--sp-gold-light); filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3)); }

  /* Floating back */
  .archive-floating-back {
    position: fixed; top: 18px; left: 18px; z-index: 2147483000;
    display: inline-flex; align-items: center; justify-content: center; gap: 10px;
    min-width: 190px; min-height: 46px; max-width: calc(100vw - 28px);
    padding: 10px 20px;
    border: 1.5px solid var(--sp-gold); border-radius: 28px;
    color: #ffffff;
    background: var(--sp-maroon-deep);
    box-shadow: 0 6px 22px rgba(15, 4, 3, 0.45);
    font: 700 17px/1 var(--sp-serif);
    letter-spacing: 0.3px;
    white-space: nowrap;
    transition: transform 180ms var(--sp-ease-out), background 180ms var(--sp-ease-out), box-shadow 180ms var(--sp-ease-out);
  }
  .archive-floating-back:hover {
    background: var(--sp-maroon);
    box-shadow: 0 8px 28px rgba(15, 4, 3, 0.6);
    transform: translateY(-2px);
  }
  .archive-floating-back:active { transform: scale(var(--sp-btn-scale)); }
  .archive-floating-back .back-arrow { color: var(--sp-gold-light); font: 700 20px/1 Georgia, serif; transition: transform 180ms var(--sp-ease-out); }
  .archive-floating-back:hover .back-arrow { transform: translateX(-3px); }
  .archive-floating-back:focus-visible { outline: 3px solid var(--sp-gold-light); outline-offset: 3px; }

  /* Masthead */
  .state-masthead {
    min-height: 240px;
    padding: 44px clamp(24px, 6vw, 96px);
    position: relative; isolation: isolate;
    display: flex; flex-direction: column; justify-content: center;
    color: #fff3dc;
    background-color: var(--sp-maroon-deep);
    background-size: cover;
    background-position: center 45%;
    border-bottom: 2px solid var(--sp-line-brass);
  }
  .state-masthead::before {
    content: ""; position: absolute; inset: 0; z-index: -1;
    background: linear-gradient(105deg, rgba(15, 4, 3, 0.95) 0%, rgba(35, 12, 8, 0.88) 45%, rgba(18, 5, 4, 0.35) 100%);
  }
  .state-masthead-kicker {
    margin: 0 0 12px; color: var(--sp-gold-light);
    font-family: var(--sp-serif); font-size: 11px;
    letter-spacing: 2px; text-transform: uppercase; font-weight: 700;
  }
  .state-masthead h1 {
    margin: 0; color: #fff9ee;
    font: 700 clamp(42px, 5.8vw, 72px)/0.94 var(--sp-serif);
    letter-spacing: -0.6px;
  }
  .state-masthead p {
    max-width: 680px; margin: 14px 0 0;
    color: #edd2a8;
    font: italic clamp(19px, 2.2vw, 25px)/1.35 var(--sp-serif);
  }

  /* Spread layout */
  .state-spread {
    width: min(1480px, 100%); margin: 28px auto 0;
    padding: 0 clamp(14px, 2.5vw, 36px) 36px;
  }
  .state-spread-heading {
    display: flex; align-items: center; justify-content: space-between; gap: 16px;
    padding: 16px 8px 14px; border-bottom: 1px solid var(--sp-line);
    color: var(--sp-muted); font: italic 18px var(--sp-serif);
  }

  /* Book grid */
  .state-book {
    display: grid; grid-template-columns: minmax(260px, .75fr) minmax(0, 1.95fr);
    border: 1px solid var(--sp-line);
    background: var(--sp-paper-card);
    box-shadow: 0 8px 32px rgba(40, 18, 12, 0.1);
    border-radius: 6px;
    overflow: hidden;
  }

  /* Context sidebar */
  .state-context {
    padding: 28px 24px 32px;
    border-right: 1px solid var(--sp-line);
    background: var(--sp-paper-warm);
    position: relative;
  }
  .state-context::after {
    content: ""; position: absolute; right: 0; top: 0; bottom: 0; width: 4px;
    background: linear-gradient(90deg, rgba(70, 36, 22, 0.08), transparent);
  }
  .state-context-label {
    display: block; color: var(--sp-terracotta); text-transform: uppercase;
    letter-spacing: 2px; font-size: 10px; font-family: var(--sp-serif); font-weight: 700; margin-bottom: 8px;
  }
  .state-context h2 {
    color: var(--sp-maroon-mid); margin: 0 0 18px;
    font: 700 32px/1 var(--sp-serif); letter-spacing: -0.3px;
  }
  .state-context h3 {
    color: var(--sp-maroon-mid); margin: 22px 0 8px;
    font: 700 22px/1 var(--sp-serif);
  }
  .state-context p {
    color: var(--sp-ink-mid); margin: 0;
    font: 14px/1.8 var(--sp-body);
  }

  /* Region info */
  .region-info-section { margin-top: 20px; }
  .region-info-section-header { margin: 0 0 8px; padding: 0; border: 0; }
  .region-info-section h3 {
    margin: 0; color: var(--sp-maroon-mid);
    font: 700 24px/1.08 var(--sp-serif);
  }
  .region-info-section > p {
    margin: 0; color: var(--sp-ink-mid);
    font: 14px/1.75 var(--sp-body);
  }
  .region-info-divider {
    height: 1px; margin: 18px 0 0;
    background: linear-gradient(90deg, var(--sp-gold), rgba(184, 146, 81, 0.12));
  }
  .state-context-ornament {
    height: 1px; margin: 18px 0;
    background: linear-gradient(90deg, var(--sp-gold), transparent);
  }
  .state-context-note {
    margin-top: 24px; padding: 16px 18px;
    background: rgba(220, 196, 158, 0.35);
    border: 1px solid rgba(132, 52, 34, 0.25); border-radius: 4px;
    color: var(--sp-maroon-mid); font: italic 17px/1.4 var(--sp-serif);
  }

  /* Dish choice list */
  .dish-choice-heading {
    color: var(--sp-muted); margin: 0 0 10px; text-transform: uppercase;
    letter-spacing: 1.5px; font: 700 10px var(--sp-serif);
  }
  .dish-choice-list { display: flex; flex-direction: column; gap: 9px; margin: 0 0 24px; }
  .dish-choice-button {
    width: 100%; min-height: 52px; display: flex; align-items: center; gap: 12px;
    padding: 10px 14px; text-align: left;
    border: 1px solid var(--sp-line); border-radius: 5px;
    color: var(--sp-ink-mid); background: var(--sp-paper-card);
    font: 700 19px/1.08 var(--sp-serif); cursor: pointer;
    transition: background 180ms var(--sp-ease-out), border-color 180ms var(--sp-ease-out), transform 180ms var(--sp-ease-out);
  }
  .dish-choice-button::after {
    content: "›"; margin-left: auto; color: var(--sp-terracotta);
    font: 700 28px/1 var(--sp-serif);
  }
  .dish-choice-button:hover { background: #f7ede0; border-color: var(--sp-gold); transform: translateX(2px); }
  .dish-choice-button:active { transform: scale(var(--sp-btn-scale)); }
  .dish-choice-button[aria-selected="true"] {
    background: linear-gradient(135deg, #f7ecd9 0%, #ecd7b7 100%);
    border-color: var(--sp-gold);
    box-shadow: inset 4px 0 var(--sp-terracotta), 0 3px 10px rgba(40, 18, 12, 0.08);
    color: var(--sp-maroon-deep);
  }
  .dish-choice-button:focus-visible { outline: 3px solid var(--sp-gold); outline-offset: 2px; }
  .dish-choice-index { flex: 0 0 24px; color: var(--sp-terracotta); font: 700 12px var(--sp-serif); }

  /* Dish spread */
  .dish-spread { padding: 26px clamp(16px, 2.2vw, 32px) 36px; min-width: 0; }
  .dish-spread-top {
    display: flex; align-items: baseline; justify-content: space-between; gap: 12px;
    margin: 0 3px 16px; padding-bottom: 12px; border-bottom: 1px solid var(--sp-line);
  }
  .dish-spread-top h2 { margin: 0; color: var(--sp-maroon-mid); font: 700 26px/1 var(--sp-serif); }
  .dish-spread-top span { color: var(--sp-muted); font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; font-family: var(--sp-serif); font-weight: 700; }
  .dish-content { min-width: 0; }
  .dish-record { border: 0; padding: 0; }
  .dish-record-head { margin: 0 3px 16px; }
  .dish-record-number { display: block; color: var(--sp-terracotta); font-family: var(--sp-serif); font-size: 11px; letter-spacing: 2px; text-transform: uppercase; font-weight: 700; }
  .dish-record-head h2 {
    color: var(--sp-maroon-mid); font: 700 clamp(30px, 3.4vw, 44px)/0.96 var(--sp-serif);
    margin: 6px 0 8px; letter-spacing: -0.4px;
  }
  .dish-descriptor { margin: 0; color: var(--sp-muted); font: italic 18px/1.3 var(--sp-serif); }

  /* Classification */
  .dish-classification {
    display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px;
    margin: 12px 0 16px;
  }
  .dish-classification-type {
    display: inline-flex; align-items: center; padding: 4px 12px;
    border: 1px solid var(--sp-line-brass); border-radius: 3px;
    color: var(--sp-maroon-mid); background: var(--sp-paper-warm);
    font: 700 11px var(--sp-serif); letter-spacing: 1px; text-transform: uppercase;
  }
  .dish-classification-form {
    color: var(--sp-muted); font: italic 15px/1.25 var(--sp-serif);
  }

  /* Photo */
  .dish-photo {
    width: 100%; min-height: 0; position: relative; overflow: hidden;
    border-radius: 6px; border: 1px solid var(--sp-line);
    margin: 0; display: flex; align-items: center; justify-content: center;
    color: #fff0d7; box-shadow: 0 6px 20px rgba(40, 18, 12, 0.1);
  }
  .dish-photo.has-image { display: block; min-height: 0; padding: 0; background: #e8dcc6; }
  .dish-photo-image {
    display: block; width: 100%; max-width: 100%; height: auto;
    object-fit: cover; object-position: center;
  }

  /* Main layout */
  .dish-main-layout {
    display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(260px, .92fr);
    gap: 24px; align-items: start;
  }

  /* Highlight stack */
  .dish-highlight-stack { display: flex; flex-direction: column; gap: 18px; }
  .dish-highlight {
    position: relative; padding: 2px 0 14px 18px;
    border-bottom: 1px solid var(--sp-line);
  }
  .dish-highlight:last-child { border-bottom: 0; }
  .dish-highlight h3 {
    margin: 0 0 8px; color: var(--sp-maroon-mid);
    font: 700 22px/1 var(--sp-serif);
  }
  .dish-highlight p { margin: 0; color: var(--sp-ink-mid); font: 14px/1.8 var(--sp-body); }
  .dish-highlight::before {
    content: "✦"; position: absolute; left: 0; top: 2px; color: var(--sp-terracotta); font-size: 11px;
  }

  /* Lower grid */
  .dish-lower-grid {
    display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px;
    margin-top: 20px;
  }
  .dish-info-card {
    min-width: 0; padding: 16px 18px 18px;
    border: 1px solid var(--sp-line); border-radius: 6px;
    background: var(--sp-paper-card);
  }
  .dish-info-card h3 {
    color: var(--sp-maroon-mid); margin: 0 0 10px; padding-bottom: 8px;
    border-bottom: 1px solid var(--sp-line);
    font: 700 21px/1 var(--sp-serif);
  }
  .dish-info-card p { color: var(--sp-ink-mid); margin: 0; font: 13px/1.75 var(--sp-body); }
  .dish-info-card ul, .dish-info-card ol {
    margin: 0; padding-left: 20px; color: var(--sp-ink-mid);
    font: 13px/1.7 var(--sp-body);
  }
  .dish-info-card li { padding-left: 2px; margin: 0 0 6px; }

  /* Oral narrative */
  .oral-narrative {
    margin-top: 18px;
    padding: 16px 18px;
    background: var(--sp-paper-warm);
    border-left: 4px solid var(--sp-terracotta); border-radius: 0 6px 6px 0;
  }
  .oral-narrative h4 { color: var(--sp-maroon-mid); font: 700 20px/1 var(--sp-serif); margin: 0 0 8px; }
  .oral-narrative .oral-person { color: var(--sp-maroon-deep); font: 700 15px var(--sp-serif); margin: 0 0 4px; }
  .oral-narrative .oral-role { color: var(--sp-muted); font: italic 13px/1.5 var(--sp-body); margin: 0 0 10px; }
  .oral-narrative p { color: var(--sp-ink-mid); font: 13px/1.72 var(--sp-body); margin: 0 0 10px; }
  .oral-source {
    padding-top: 8px; border-top: 1px solid var(--sp-line);
    color: var(--sp-muted); font: 12px/1.65 var(--sp-body);
  }

  /* Sources */
  .dish-sources { margin-top: 20px; padding: 14px 16px 0; border-top: 1px solid var(--sp-line); }
  .dish-sources h4 { margin: 0 0 8px; color: var(--sp-maroon-mid); font: 700 21px/1 var(--sp-serif); }
  .dish-sources ol { margin: 0; padding-left: 20px; color: var(--sp-muted); font: 12px/1.72 var(--sp-body); }
  .dish-sources li { margin-bottom: 8px; }

  /* Page end */
  .state-page-end {
    display: flex; justify-content: space-between; gap: 16px; align-items: center;
    padding: 22px clamp(24px, 4vw, 64px); color: #ede4d5;
    background: var(--sp-maroon-deep);
    border-top: 2px solid var(--sp-line-brass);
    font: italic 18px var(--sp-serif);
  }
  .state-page-end button {
    border: 1px solid var(--sp-line-brass); background: var(--sp-paper-card);
    border-radius: 4px; padding: 8px 18px; color: var(--sp-maroon-deep);
    font: 700 16px var(--sp-serif); cursor: pointer;
    transition: background 180ms var(--sp-ease-out), transform 180ms var(--sp-ease-out);
  }
  .state-page-end button:hover { background: #f7ede0; transform: translateY(-1px); }
  .state-page-end button:active { transform: scale(var(--sp-btn-scale)); }

  /* State card interaction (from main page) */
  .state-card[data-has-archive="true"] { cursor: pointer; }
  .state-card[data-has-archive="true"]:focus-visible { outline: 3px solid var(--sp-gold); outline-offset: 3px; }
  .state-card[data-has-archive="false"] { cursor: default; }

  /* Responsive */
  @media(max-width:1050px) {
    .state-book { grid-template-columns: minmax(240px, .7fr) minmax(0, 1.8fr); }
    .dish-main-layout { grid-template-columns: minmax(0, 1fr) minmax(240px, .9fr); gap: 16px; }
  }
  @media(max-width:760px) {
    .state-page-topbar { min-height: auto; padding: 72px 18px 14px; }
    .state-page-brand { font-size: 18px; }
    .archive-floating-back { top: 12px; left: 12px; min-width: 0; min-height: 44px; padding: 9px 16px; font-size: 16px; }
    .state-masthead { min-height: 200px; padding: 36px 20px; }
    .state-masthead p { font-size: 18px; }
    .state-spread { padding-left: 12px; padding-right: 12px; }
    .state-book { grid-template-columns: 1fr; }
    .state-context { border-right: 0; border-bottom: 1px solid var(--sp-line); }
    .state-context::after { display: none; }
    .dish-choice-list { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .dish-choice-button { font-size: 17px; min-height: 48px; }
    .dish-spread { padding: 20px 12px 28px; }
    .dish-main-layout { grid-template-columns: 1fr; }
    .dish-lower-grid { grid-template-columns: 1fr; }
    .state-page-end { flex-direction: column; text-align: center; }
    .state-spread-heading { font-size: 15px; }
  }
  @media(prefers-reduced-motion:reduce) {
    .state-page-root *, .state-page-root *::before, .state-page-root *::after {
      scroll-behavior: auto !important; transition: none !important;
    }
  }
</style>
<div class="state-page-root" id="archive-state-page" aria-live="polite"></div>
<script id="archive-state-page-script">
(function () {
  "use strict";
  const archiveStatePages = __STATE_PAGES__;
  const archiveStateCardImages = STATE_IMAGES;
  const archiveDishImages = __DISH_IMAGES__;
  const root = document.getElementById("archive-state-page");
  const originalSections = [
    document.querySelector(".site-header"),
    document.querySelector("main"),
    document.querySelector(".site-footer")
  ].filter(Boolean);
  const stateGrid = document.getElementById("state-grid");
  if (!root || !stateGrid) return;

  // Keep the ten detailed chapter states visible in the homepage's initial
  // featured row; Karnataka replaces the placeholder-only Himachal card.
  if (typeof featuredStates !== "undefined" && Array.isArray(featuredStates)) {
    const replaceAt = featuredStates.indexOf("Himachal Pradesh");
    if (replaceAt >= 0) {
      featuredStates[replaceAt] = "Karnataka";
      if (typeof renderStates === "function") {
        const currentSearch = document.getElementById("state-search");
        renderStates(currentSearch ? currentSearch.value : "");
      }
    }
  }

  function escapeArchiveText(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (ch) {
      return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch];
    });
  }
  function slugifyState(value) {
    return String(value).toLowerCase().replace(/&/g,"and").replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");
  }
  function scrollArchiveViewToTop() {
    try { window.scrollTo(0, 0); } catch (_) {}
    try { document.documentElement.scrollTop = 0; } catch (_) {}
    try { document.body.scrollTop = 0; } catch (_) {}
    try { if (window.frameElement) window.frameElement.scrollIntoView({ block: "start", behavior: "auto" }); } catch (_) {}
    try { if (window.parent && window.parent !== window) window.parent.scrollTo(0, 0); } catch (_) {}
    try { if (window.top && window.top !== window) window.top.scrollTo(0, 0); } catch (_) {}
  }
  function scheduleArchiveTopReset() {
    scrollArchiveViewToTop();
    requestAnimationFrame(function () {
      scrollArchiveViewToTop();
      requestAnimationFrame(scrollArchiveViewToTop);
    });
    window.setTimeout(scrollArchiveViewToTop, 120);
    window.setTimeout(scrollArchiveViewToTop, 300);
  }
  function linkList(sources) {
    return (sources || []).map(function (source) {
      return '<li><a href="' + escapeArchiveText(source.url) + '" target="_blank" rel="noopener noreferrer">' +
        escapeArchiveText(source.title) + '</a>' +
        (source.publisher ? ' <span>— ' + escapeArchiveText(source.publisher) + '</span>' : '') +
        (source.note ? '<br><span>' + escapeArchiveText(source.note) + '</span>' : '') + '</li>';
    }).join("");
  }
  function renderRegionInfoSection(title, section) {
    const text = section && typeof section.text === "string" ? section.text : "";
    return '<section class="region-info-section">' +
      '<header class="region-info-section-header"><h3>' + escapeArchiveText(title) + '</h3></header>' +
      '<p>' + escapeArchiveText(text) + '</p>' +
    '</section>';
  }
  function dishImage(slug) {
    return archiveDishImages[slug] || "";
  }
  function renderDish(dish, index, state) {
    const image = dishImage(dish.slug);
    const ingredients = (dish.ingredients || []).map(x => "<li>" + escapeArchiveText(x) + "</li>").join("");
    const steps = (dish.steps || []).map(x => "<li>" + escapeArchiveText(x) + "</li>").join("");
    const sources = linkList(dish.sources);
    const classification = dish.classification || {};
    const classificationMarkup = classification.recordType ? (
      '<div class="dish-classification" aria-label="Food type">' +
        '<span class="dish-classification-type">' + escapeArchiveText(classification.recordType) + '</span>' +
        (classification.foodForm
          ? '<span class="dish-classification-form">' + escapeArchiveText(classification.foodForm) + '</span>'
          : '') +
      '</div>'
    ) : "";
    const detailCards = (dish.foodCharacteristics || dish.consumption) ? (
      '<div class="dish-lower-grid">' +
        '<section class="dish-info-card"><h3>Food characteristics</h3><p>' + escapeArchiveText(dish.foodCharacteristics || "") + '</p></section>' +
        '<section class="dish-info-card"><h3>Consumption</h3><p>' + escapeArchiveText(dish.consumption || "") + '</p></section>' +
      '</div>'
    ) : (
      '<div class="dish-lower-grid">' +
        '<section class="dish-info-card"><h3>Ingredients</h3><ul>' + ingredients + '</ul></section>' +
        '<section class="dish-info-card"><h3>Preparation</h3><ol>' + steps + '</ol></section>' +
      '</div>'
    );
    const oral = dish.oralNarrative ? (
      '<section class="oral-narrative">' +
        '<h4>Oral narrative</h4>' +
        '<p class="oral-person">' + escapeArchiveText(dish.oralNarrative.narrator) + '</p>' +
        '<p class="oral-role">' + escapeArchiveText(dish.oralNarrative.role || "") + '</p>' +
        '<p>' + escapeArchiveText(dish.oralNarrative.account || dish.oralNarrative.text || "") + '</p>' +
        '<div class="oral-source">Source: ' +
          '<a href="' + escapeArchiveText(dish.oralNarrative.sourceUrl) + '" target="_blank" rel="noopener noreferrer">' +
          escapeArchiveText(dish.oralNarrative.sourceTitle) + '</a>' +
          (dish.oralNarrative.sourcePublisher ? ' — ' + escapeArchiveText(dish.oralNarrative.sourcePublisher) : '') +
        '</div>' +
      '</section>'
    ) : "";
    return (
      '<article class="dish-record">' +
        '<header class="dish-record-head">' +
          '<h2>' + escapeArchiveText(dish.name) + '</h2>' +
          '<p class="dish-descriptor">' + escapeArchiveText(dish.descriptor || "") + '</p>' +
          classificationMarkup +
        '</header>' +
        '<div class="dish-main-layout">' +
          '<div class="dish-photo has-image">' +
            '<img class="dish-photo-image" src="' + image + '" alt="' + escapeArchiveText(dish.name + ' photograph') + '" loading="lazy" decoding="async">' +
          '</div>' +
          '<div class="dish-highlight-stack">' +
            '<section class="dish-highlight"><h3>About this food</h3><p>' + escapeArchiveText(dish.overview) + '</p></section>' +
            '<section class="dish-highlight"><h3>Historical background</h3><p>' + escapeArchiveText(dish.history) + '</p></section>' +
          '</div>' +
        '</div>' +
        detailCards +
        oral +
        '<div class="dish-sources"><h4>Sources & further reading</h4><ol>' + sources + '</ol></div>' +
      '</article>'
    );
  }
  function renderState(slug) {
    const state = archiveStatePages[slug];
    if (!state) return false;
    const regionType = state.administrativeType || "State";
    const stateImage = archiveStateCardImages[slug] || "";
    const bannerStyle = stateImage ? 'style="background-image:url(' + stateImage + ')"' : "";
    const stateDishes = Array.isArray(state.dishes) ? state.dishes : [];
    if (!stateDishes.length) return false;
    let activeDishIndex = 0;
    const dishButtons = stateDishes.map(function (dish, index) {
      return '<button type="button" class="dish-choice-button" role="tab" data-select-dish="' + index + '" aria-selected="' + (index === 0 ? 'true' : 'false') + '" aria-controls="active-dish-content">' +
        '<span class="dish-choice-index">0' + (index + 1) + '</span><span>' + escapeArchiveText(dish.name) + '</span></button>';
    }).join("");

    root.innerHTML =
      '<button type="button" class="archive-floating-back" data-back-to-home aria-label="Back to regional catalogue" title="Back to regional catalogue"><span class="back-arrow" aria-hidden="true">←</span><span>Back to regions</span><span style="font-size:11px;font-weight:400;opacity:.7;margin-left:4px">(Esc)</span></button>' +
      '<div class="state-page-topbar">' +
        '<div class="state-page-brand"><svg class="state-page-brand-mark" viewBox="0 0 64 64" fill="none" role="img" aria-label="Archive emblem"><circle cx="32" cy="32" r="30" stroke="currentColor" stroke-width="1.2" opacity="0.4"/><circle cx="32" cy="32" r="26.5" stroke="currentColor" stroke-width="1"/><circle cx="32" cy="32" r="18" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 2" opacity="0.6"/><circle cx="32" cy="32" r="6" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/><path d="M32 6 L35 24 L52 18 L38 30 L58 32 L38 34 L52 46 L35 40 L32 58 L29 40 L12 46 L26 34 L6 32 L26 30 L12 18 L29 24 Z" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.08" stroke-linejoin="round"/><circle cx="32" cy="32" r="2" fill="currentColor"/></svg><span>India’s Culinary Memory<br><small style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:var(--sp-gold-light);font-weight:600">National Heritage Archive</small></span></div>' +
      '</div>' +
      '<header class="state-masthead" ' + bannerStyle + '>' +
        '<span class="state-masthead-kicker">' + escapeArchiveText(regionType) + ' chapter · ' + escapeArchiveText(state.region || "India") + '</span>' +
        '<h1>' + escapeArchiveText(state.name) + '</h1>' +
        '<p>' + escapeArchiveText(state.tagline) + '</p>' +
      '</header>' +
      '<div class="state-spread">' +
        '<div class="state-book">' +
          '<aside class="state-context">' +
            '<span class="state-context-label">Regional food culture</span>' +
            '<h2>' + escapeArchiveText(state.name) + ' Archive</h2>' +
            '<div class="dish-choice-list" role="tablist" aria-label="Food records from ' + escapeArchiveText(state.name) + '">' + dishButtons + '</div>' +
            renderRegionInfoSection('Geography & influence', state.regionalGeography) +
            '<div class="region-info-divider"></div>' +
            renderRegionInfoSection('Culinary landscape', state.foodCulture) +
          '</aside>' +
          '<section class="dish-spread">' +
            '<div class="dish-content" id="active-dish-content" role="tabpanel"></div>' +
          '</section>' +
        '</div>' +
      '</div>' +
      '<footer class="state-page-end"><span>A living record of ' + escapeArchiveText(state.name) + ' food heritage</span></footer>';

    const dishContent = root.querySelector("#active-dish-content");
    function activateDish(index) {
      const safeIndex = Number(index);
      if (!Number.isInteger(safeIndex) || safeIndex < 0 || safeIndex >= stateDishes.length) return;
      activeDishIndex = safeIndex;
      root.querySelectorAll("[data-select-dish]").forEach(function (button) {
        const selected = Number(button.dataset.selectDish) === activeDishIndex;
        button.setAttribute("aria-selected", selected ? "true" : "false");
        button.tabIndex = selected ? 0 : -1;
      });
      dishContent.innerHTML = renderDish(stateDishes[activeDishIndex], activeDishIndex, state);
    }
    activateDish(activeDishIndex);

    originalSections.forEach(function (section) { section.style.display = "none"; });
    root.style.display = "block";
    scheduleArchiveTopReset();
    try {
      history.pushState({ statePage: slug }, "", "#region/" + encodeURIComponent(slug));
    } catch (e) {}
    return true;
  }
  function closeStatePage(updateHistory) {
    root.style.display = "none";
    root.innerHTML = "";
    originalSections.forEach(function (section) { section.style.display = ""; });
    scheduleArchiveTopReset();
    if (updateHistory !== false) {
      try {
        if (location.hash.startsWith("#region/")) {
          history.pushState({}, "", location.pathname + location.search);
        }
      } catch (e) {}
    }
  }

  function checkInitialRegionHash() {
    let hash = window.location.hash;
    try {
      if ((!hash || hash === "#top" || hash === "#states") && window.parent && window.parent !== window && window.parent.location && window.parent.location.hash) {
        hash = window.parent.location.hash;
      }
    } catch (e) {}
    if (hash && hash.startsWith("#region/")) {
      const slug = decodeURIComponent(hash.replace("#region/", ""));
      renderState(slug);
    }
  }
  checkInitialRegionHash();
  window.addEventListener("DOMContentLoaded", checkInitialRegionHash);
  window.addEventListener("load", checkInitialRegionHash);
  setTimeout(checkInitialRegionHash, 350);

  stateGrid.addEventListener("click", function (event) {
    const card = event.target.closest(".state-card");
    if (!card) return;
    const nameNode = card.querySelector(".state-copy strong");
    if (!nameNode) return;
    const slug = slugifyState(nameNode.textContent.trim());
    if (renderState(slug)) {
      event.preventDefault();
      event.stopPropagation();
    }
  });
  stateGrid.addEventListener("keydown", function (event) {
    if (event.key !== "Enter" && event.key !== " ") return;
    const card = event.target.closest(".state-card");
    if (!card) return;
    const nameNode = card.querySelector(".state-copy strong");
    if (!nameNode) return;
    const slug = slugifyState(nameNode.textContent.trim());
    if (renderState(slug)) {
      event.preventDefault();
    }
  });
  root.addEventListener("click", function (event) {
    const dishButton = event.target.closest("[data-select-dish]");
    if (dishButton) {
      const content = root.querySelector("#active-dish-content");
      const stateName = root.querySelector(".state-context h2");
      if (content && stateName) {
        const activeState = Object.keys(archiveStatePages).find(function (key) {
          return archiveStatePages[key].name === stateName.textContent.replace(/\s+Archive$/, "");
        });
        const stateData = activeState ? archiveStatePages[activeState] : null;
        const chosenIndex = Number(dishButton.dataset.selectDish);
        if (stateData && stateData.dishes && stateData.dishes[chosenIndex]) {
          root.querySelectorAll("[data-select-dish]").forEach(function (button) {
            const selected = button === dishButton;
            button.setAttribute("aria-selected", selected ? "true" : "false");
            button.tabIndex = selected ? 0 : -1;
          });
          content.innerHTML = renderDish(stateData.dishes[chosenIndex], chosenIndex, stateData);
        }
      }
      return;
    }
    if (event.target.closest("[data-back-to-home]")) closeStatePage();
  });
  root.addEventListener("keydown", function (event) {
    const button = event.target.closest("[data-select-dish]");
    if (!button || (event.key !== "ArrowDown" && event.key !== "ArrowUp")) return;
    const buttons = Array.from(root.querySelectorAll("[data-select-dish]"));
    const current = buttons.indexOf(button);
    const next = (current + (event.key === "ArrowDown" ? 1 : buttons.length - 1)) % buttons.length;
    buttons[next].focus();
    buttons[next].click();
    event.preventDefault();
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && root.style.display === "block") closeStatePage();
  });

  function markStateCards() {
    stateGrid.querySelectorAll(".state-card").forEach(function (card) {
      const node = card.querySelector(".state-copy strong");
      if (!node) return;
      const hasPage = !!archiveStatePages[slugifyState(node.textContent.trim())];
      card.dataset.hasArchive = hasPage ? "true" : "false";
      if (hasPage) {
        card.setAttribute("role","button");
        card.setAttribute("tabindex","0");
        card.setAttribute("aria-label","Open " + node.textContent.trim() + " archive");
      } else {
        card.removeAttribute("role");
        card.removeAttribute("tabindex");
      }
    });
  }
  markStateCards();
  const observer = new MutationObserver(markStateCards);
  observer.observe(stateGrid, {childList:true, subtree:true});
})();
</script>
"""

extension = (
    STATE_PAGE_EXTENSION
    .replace("__STATE_PAGES__", json_for_script(state_pages))
    .replace("__DISH_IMAGES__", json_for_script(dish_images))
)

if "</body>" not in html:
    st.error("Could not locate the end of index.html to attach the state-page module.")
    st.stop()
html = html.replace("</body>", extension + "\n</body>")

# Hide Streamlit chrome and make the embedded archive fill the browser viewport.
# Scrolling stays inside the iframe so the chapter back control remains fixed on screen.
st.markdown(
    """
    <style>
      html, body, .stApp {
          margin: 0 !important; padding: 0 !important;
          height: 100vh !important; max-height: 100vh !important;
          overflow: hidden !important;
      }
      [data-testid="stHeader"], [data-testid="stToolbar"],
      [data-testid="stDecoration"], #MainMenu, header, footer {
          display: none !important; height: 0 !important;
          min-height: 0 !important; visibility: hidden !important;
      }
      [data-testid="stAppViewContainer"], [data-testid="stMain"],
      section.main, section.main > div {
          margin: 0 !important; padding: 0 !important;
          height: 100vh !important; max-height: 100vh !important;
          overflow: hidden !important;
      }
      [data-testid="stMainBlockContainer"], [data-testid="stAppViewBlockContainer"],
      .block-container {
          width: 100% !important; max-width: 100% !important;
          margin: 0 !important; padding: 0 !important;
      }
      [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] { gap: 0 !important; }
      iframe {
          display: block !important; width: 100% !important;
          height: 100vh !important; min-height: 100vh !important;
          max-height: 100vh !important; border: 0 !important;
          margin: 0 !important; padding: 0 !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.iframe(
    html,
    width="stretch",
    height=900,
    alt="India's Culinary Memory Archive homepage and regional chapters",
)
