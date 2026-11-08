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
    --sp-maroon: #2e0e0c;
    --sp-wine: #5c2420;
    --sp-ink: #301510;
    --sp-ink-mid: #4a2920;
    --sp-muted: #6b4a3c;
    --sp-paper: #f5e8d0;
    --sp-paper-light: #fdf6ea;
    --sp-paper-warm: #f1e2c5;
    --sp-gold: #b8945a;
    --sp-gold-light: #d4b07a;
    --sp-line: rgba(80, 44, 28, .2);
    --sp-serif: "Cormorant Garamond", Georgia, serif;
    --sp-body: "Libre Baskerville", Georgia, serif;
  }
  .state-page-root {
    display: none;
    min-height: 100vh;
    color: var(--sp-ink);
    background-color: var(--sp-paper);
    background-image:
      radial-gradient(ellipse at 15% 10%, rgba(255,255,255,.26), transparent 30%),
      repeating-linear-gradient(0deg, rgba(80,44,28,.016) 0, rgba(80,44,28,.016) 1px, transparent 1px, transparent 6px);
    font-family: var(--sp-body);
    font-size: 15px;
  }
  .state-page-root * { box-sizing: border-box; }
  .state-page-root button, .state-page-root a { font: inherit; cursor: pointer; }
  .state-page-root a { color: inherit; text-decoration: none; }

  /* Top bar */
  .state-page-topbar {
    min-height: 68px;
    padding: 10px 30px 10px clamp(220px, 18vw, 260px);
    display: flex; align-items: center;
    color: #fff1d8;
    background: var(--sp-maroon);
    border-bottom: 1px solid rgba(212,176,122,.28);
  }
  .state-page-brand {
    display: flex; align-items: center; gap: 12px;
    font: 700 20px/.93 var(--sp-serif);
    color: #f5e9d0;
  }
  .state-page-brand-mark { width: 36px; height: 36px; color: var(--sp-gold-light); }

  /* Floating back */
  .archive-floating-back {
    position: fixed; top: 14px; left: 14px; z-index: 2147483000;
    display: inline-flex; align-items: center; justify-content: center; gap: 10px;
    min-width: 200px; min-height: 48px; max-width: calc(100vw - 28px);
    padding: 11px 18px;
    border: 1.5px solid rgba(58,21,18,.8); border-radius: 28px;
    color: #3a1512;
    background: linear-gradient(180deg, #fff5e2 0%, #edd8b5 100%);
    box-shadow: 0 5px 18px rgba(22,7,5,.22), inset 0 1px 0 rgba(255,255,255,.8);
    font: 700 18px/1 var(--sp-serif);
    white-space: nowrap;
    transition: transform .18s ease, background .18s ease, box-shadow .18s ease;
  }
  .archive-floating-back:hover {
    background: linear-gradient(180deg, #fff9ed 0%, #f6e9d2 100%);
    box-shadow: 0 7px 24px rgba(22,7,5,.28), inset 0 1px 0 rgba(255,255,255,.9);
    transform: translateY(-1px);
  }
  .archive-floating-back .back-arrow { color: #682620; font: 700 22px/1 Georgia, serif; }
  .archive-floating-back:focus-visible { outline: 3px solid var(--sp-gold); outline-offset: 3px; }

  /* Masthead */
  .state-masthead {
    min-height: 220px;
    padding: 38px clamp(24px, 6vw, 88px);
    position: relative; isolation: isolate;
    display: flex; flex-direction: column; justify-content: center;
    color: #fff3dc;
    background-color: #1e0c09;
    background-size: cover;
    background-position: center 45%;
    border-bottom: 1px solid rgba(100,62,36,.26);
  }
  .state-masthead::before {
    content: ""; position: absolute; inset: 0; z-index: -1;
    background: linear-gradient(90deg, rgba(32,10,8,.94) 0%, rgba(38,14,11,.72) 48%, rgba(38,14,11,.18) 100%);
  }
  .state-masthead-kicker {
    margin: 0 0 10px; color: #dfbf88;
    font-family: var(--sp-body); font-size: 10px;
    letter-spacing: 2.3px; text-transform: uppercase;
  }
  .state-masthead h1 {
    margin: 0; color: #fff1d8;
    font: 700 clamp(42px,6vw,72px)/.92 var(--sp-serif);
  }
  .state-masthead p {
    max-width: 640px; margin: 14px 0 0;
    color: #f0dcbc;
    font: italic clamp(18px,2vw,23px)/1.3 var(--sp-serif);
  }

  /* Spread layout */
  .state-spread {
    width: min(1480px, 100%); margin: 24px auto 0;
    padding: 0 clamp(12px,2vw,28px) 32px;
  }
  .state-spread-heading {
    display: flex; align-items: center; justify-content: space-between; gap: 16px;
    padding: 16px 8px 12px; border-bottom: 1px solid var(--sp-line);
    color: var(--sp-muted); font: italic 17px var(--sp-serif);
  }

  /* Book grid */
  .state-book {
    display: grid; grid-template-columns: minmax(245px, .72fr) minmax(0, 1.95fr);
    border: 1px solid rgba(100,62,36,.22);
    background: rgba(255,249,236,.4);
    box-shadow: 0 6px 22px rgba(60,32,18,.09);
    border-radius: 4px;
    overflow: hidden;
  }

  /* Context sidebar */
  .state-context {
    padding: 26px 22px 30px;
    border-right: 1px solid rgba(100,62,36,.22);
    background: linear-gradient(90deg, rgba(230,208,172,.18), rgba(255,249,234,.28));
    position: relative;
  }
  .state-context::after {
    content: ""; position: absolute; right: 0; top: 0; bottom: 0; width: 4px;
    background: linear-gradient(90deg, rgba(90,44,28,.07), transparent);
  }
  .state-context-label {
    display: block; color: var(--sp-gold); text-transform: uppercase;
    letter-spacing: 1.8px; font-size: 9px; font-family: var(--sp-body); margin-bottom: 8px;
  }
  .state-context h2 {
    color: var(--sp-wine); margin: 0 0 18px;
    font: 700 32px/.95 var(--sp-serif);
  }
  .state-context h3 {
    color: #5a211b; margin: 22px 0 7px;
    font: 700 22px/1 var(--sp-serif);
  }
  .state-context p {
    color: var(--sp-ink-mid); margin: 0;
    font: 13px/1.78 var(--sp-body);
  }

  /* Region info */
  .region-info-section { margin-top: 18px; }
  .region-info-section-header { margin: 0 0 7px; padding: 0; border: 0; }
  .region-info-section h3 {
    margin: 0; color: #57201b;
    font: 700 25px/1.05 var(--sp-serif);
  }
  .region-info-section > p {
    margin: 0; color: var(--sp-ink-mid);
    font: 14px/1.65 var(--sp-body);
  }
  .region-info-divider {
    height: 1px; margin: 16px 0 0;
    background: linear-gradient(90deg, var(--sp-gold), rgba(184,148,90,.1));
  }
  .state-context-ornament {
    height: 1px; margin: 16px 0;
    background: linear-gradient(90deg, var(--sp-gold), transparent);
  }
  .state-context-note {
    margin-top: 22px; padding: 14px 15px 16px;
    background: rgba(220,196,158,.35);
    border: 1px solid rgba(126,79,48,.2); border-radius: 5px;
    color: #6a4638; font: italic 17px/1.35 var(--sp-serif);
  }

  /* Dish choice list */
  .dish-choice-heading {
    color: var(--sp-muted); margin: 0 0 9px; text-transform: uppercase;
    letter-spacing: 1.5px; font: 10px var(--sp-body);
  }
  .dish-choice-list { display: flex; flex-direction: column; gap: 8px; margin: 0 0 22px; }
  .dish-choice-button {
    width: 100%; min-height: 50px; display: flex; align-items: center; gap: 10px;
    padding: 9px 11px; text-align: left;
    border: 1px solid rgba(126,79,48,.22); border-radius: 7px;
    color: var(--sp-ink-mid); background: rgba(255,248,232,.6);
    font: 700 19px/1.05 var(--sp-serif); cursor: pointer;
    transition: background .18s ease, border-color .18s ease, transform .18s ease;
  }
  .dish-choice-button::after {
    content: "›"; margin-left: auto; color: #74382a;
    font: 700 27px/1 var(--sp-serif);
  }
  .dish-choice-button:hover { background: #f8e6cb; border-color: rgba(126,79,48,.5); transform: translateX(2px); }
  .dish-choice-button[aria-selected="true"] {
    background: linear-gradient(100deg, #f2ddbd, #eed4b5); border-color: #d8b18b;
    box-shadow: inset 3px 0 #85442f, 0 2px 7px rgba(90,47,30,.06);
  }
  .dish-choice-button:focus-visible { outline: 3px solid var(--sp-gold); outline-offset: 2px; }
  .dish-choice-index { flex: 0 0 24px; color: #9a6b49; font: 700 12px var(--sp-body); }

  /* Dish spread */
  .dish-spread { padding: 22px clamp(13px,1.8vw,27px) 32px; min-width: 0; }
  .dish-spread-top {
    display: flex; align-items: baseline; justify-content: space-between; gap: 12px;
    margin: 0 3px 14px; padding-bottom: 10px; border-bottom: 1px solid var(--sp-line);
  }
  .dish-spread-top h2 { margin: 0; color: var(--sp-wine); font: 700 26px/1 var(--sp-serif); }
  .dish-spread-top span { color: var(--sp-muted); font-size: 9px; letter-spacing: 1px; text-transform: uppercase; }
  .dish-content { min-width: 0; }
  .dish-record { border: 0; padding: 0; }
  .dish-record-head { margin: 0 3px 14px; }
  .dish-record-number { display: block; color: #926242; font-family: var(--sp-body); font-size: 10px; letter-spacing: 1.4px; text-transform: uppercase; }
  .dish-record-head h2 {
    color: var(--sp-wine); font: 700 clamp(30px,3.2vw,42px)/.98 var(--sp-serif);
    margin: 5px 0 7px;
  }
  .dish-descriptor { margin: 0; color: var(--sp-muted); font: italic 18px/1.25 var(--sp-serif); }

  /* Classification */
  .dish-classification {
    display: flex; flex-wrap: wrap; align-items: center; gap: 7px 12px;
    margin: 10px 0 14px;
  }
  .dish-classification-type {
    display: inline-flex; align-items: center; padding: 4px 10px;
    border: 1px solid rgba(126,79,48,.34); border-radius: 4px;
    color: var(--sp-wine); background: rgba(255,248,232,.6);
    font: 700 11px var(--sp-body);
  }
  .dish-classification-form {
    color: var(--sp-muted); font: italic 15px/1.2 var(--sp-serif);
  }

  /* Photo */
  .dish-photo {
    width: 100%; min-height: 0; position: relative; overflow: hidden;
    border-radius: 7px; border: 1px solid rgba(100,62,36,.26);
    margin: 0; display: flex; align-items: center; justify-content: center;
    color: #fff0d7;
  }
  .dish-photo.has-image { display: block; min-height: 0; padding: 0; background: #eee1cb; }
  .dish-photo-image {
    display: block; width: 100%; max-width: 100%; height: auto;
    object-fit: contain; object-position: center;
  }
  .dish-photo.no-image {
    min-height: 300px; margin: 0; border-radius: 7px;
    background: linear-gradient(145deg, #dbc39d, #97704e 72%, #49241b);
  }
  .dish-photo.no-image::after {
    content: ""; position: absolute; inset: 0;
    background: linear-gradient(180deg, transparent 50%, rgba(32,12,8,.35));
    pointer-events: none;
  }
  .dish-photo-placeholder { position: relative; z-index: 1; padding: 12px; text-shadow: 0 1px 4px rgba(0,0,0,.4); text-align: center; }
  .dish-photo-placeholder strong { display: block; font: 700 22px var(--sp-serif); }
  .dish-photo-placeholder span { display: block; margin-top: 5px; font-size: 9px; letter-spacing: 1.3px; text-transform: uppercase; }

  /* Main layout */
  .dish-main-layout {
    display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(240px, .9fr);
    gap: 20px; align-items: start;
  }

  /* Highlight stack */
  .dish-highlight-stack { display: flex; flex-direction: column; gap: 16px; }
  .dish-highlight {
    position: relative; padding: 2px 0 13px 16px;
    border-bottom: 1px solid var(--sp-line-soft, rgba(80,44,28,.12));
  }
  .dish-highlight:last-child { border-bottom: 0; }
  .dish-highlight h3 {
    margin: 0 0 7px; color: var(--sp-wine);
    font: 700 22px/1 var(--sp-serif);
  }
  .dish-highlight p { margin: 0; color: var(--sp-ink-mid); font: 14px/1.75 var(--sp-body); }
  .dish-highlight::before {
    content: "✧"; position: absolute; left: 0; top: 2px; color: #8d4c34; font-size: 11px;
  }

  /* Lower grid */
  .dish-lower-grid {
    display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 15px;
    margin-top: 18px;
  }
  .dish-info-card {
    min-width: 0; padding: 13px 14px 15px;
    border: 1px solid rgba(126,79,48,.18); border-radius: 6px;
    background: rgba(255,248,232,.5);
  }
  .dish-info-card h3 {
    color: var(--sp-wine); margin: 0 0 8px; padding-bottom: 6px;
    border-bottom: 1px solid rgba(100,62,36,.16);
    font: 700 21px/1 var(--sp-serif);
  }
  .dish-info-card p { color: var(--sp-ink-mid); margin: 0; font: 12px/1.72 var(--sp-body); }
  .dish-info-card ul, .dish-info-card ol {
    margin: 0; padding-left: 18px; color: var(--sp-ink-mid);
    font: 12px/1.65 var(--sp-body);
  }
  .dish-info-card li { padding-left: 2px; margin: 0 0 5px; }

  /* Support grid */
  .dish-support-grid {
    display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 15px;
    margin-top: 16px; align-items: start;
  }
  .dish-support-grid.no-oral { grid-template-columns: 1fr; }
  .dish-support-grid .historical-slot { margin: 0; }
  .dish-support-grid .oral-narrative { margin: 0; }

  /* Historical slot */
  .historical-slot {
    padding: 12px 13px 14px;
    border: 1px dashed rgba(112,70,43,.5);
    background: rgba(230,210,178,.26); border-radius: 5px;
  }
  .historical-slot-title {
    color: #6e3c2c; font: 700 18px/1 var(--sp-serif); margin: 0 0 6px;
  }
  .historical-slot p { margin: 0 0 9px; color: var(--sp-muted); font: 12px/1.65 var(--sp-body); }
  .historical-slot a, .dish-sources a, .oral-source a {
    color: #78352a; text-decoration: underline;
    text-decoration-color: rgba(120,53,42,.4); text-underline-offset: 2px;
  }
  .historical-slot a:hover, .dish-sources a:hover, .oral-source a:hover { color: #a04b35; }

  /* Oral narrative */
  .oral-narrative {
    padding: 13px 14px 14px;
    background: rgba(220,196,158,.35);
    border-left: 3px solid #8b4b35; border-radius: 0 5px 5px 0;
  }
  .oral-narrative h4 { color: var(--sp-wine); font: 700 19px/1 var(--sp-serif); margin: 0 0 7px; }
  .oral-narrative .oral-person { color: #4f261e; font: 700 14px var(--sp-serif); margin: 0 0 3px; }
  .oral-narrative .oral-role { color: var(--sp-muted); font: italic 12px/1.5 var(--sp-body); margin: 0 0 9px; }
  .oral-narrative p { color: var(--sp-ink-mid); font: 12px/1.68 var(--sp-body); margin: 0 0 8px; }
  .oral-source {
    padding-top: 7px; border-top: 1px solid rgba(100,62,36,.18);
    color: var(--sp-muted); font: 11px/1.6 var(--sp-body);
  }

  /* Sources */
  .dish-sources { margin-top: 18px; padding: 12px 14px 0; border-top: 1px solid var(--sp-line); }
  .dish-sources h4 { margin: 0 0 7px; color: var(--sp-wine); font: 700 20px/1 var(--sp-serif); }
  .dish-sources ol { margin: 0; padding-left: 18px; color: var(--sp-muted); font: 11px/1.68 var(--sp-body); }
  .dish-sources li { margin-bottom: 6px; }

  /* Page end */
  .state-page-end {
    display: flex; justify-content: space-between; gap: 14px; align-items: center;
    padding: 18px clamp(20px,4vw,56px); color: #f0dfc0;
    background: linear-gradient(100deg, var(--sp-maroon), #42150f, #250a09);
    border-top: 2px solid #a07840;
    font: italic 18px var(--sp-serif);
  }
  .state-page-end button {
    border: 1px solid rgba(240,223,192,.6); background: transparent;
    border-radius: 5px; padding: 7px 15px; color: #f0dfc0;
    font: 700 16px var(--sp-serif); cursor: pointer;
    transition: background .2s ease;
  }
  .state-page-end button:hover { background: rgba(240,223,192,.12); }

  /* State card interaction (from main page) */
  .state-card[data-has-archive="true"] { cursor: pointer; }
  .state-card[data-has-archive="true"]:focus-visible { outline: 3px solid var(--sp-gold); outline-offset: 3px; }
  .state-card[data-has-archive="false"] { cursor: default; }

  /* Responsive */
  @media(max-width:1050px) {
    .state-book { grid-template-columns: minmax(220px,.68fr) minmax(0,1.8fr); }
    .dish-main-layout { grid-template-columns: minmax(0,1fr) minmax(220px,.9fr); gap: 14px; }
    .dish-photo.no-image { min-height: 260px; }
  }
  @media(max-width:760px) {
    .state-page-topbar { min-height: auto; padding: 70px 18px 14px; }
    .state-page-brand { font-size: 18px; }
    .archive-floating-back { top: 10px; left: 10px; min-width: 0; min-height: 46px; padding: 10px 15px; font-size: 17px; }
    .state-masthead { min-height: 190px; padding: 32px 22px; }
    .state-masthead p { font-size: 18px; }
    .state-spread { padding-left: 10px; padding-right: 10px; }
    .state-book { grid-template-columns: 1fr; }
    .state-context { border-right: 0; border-bottom: 1px solid rgba(100,62,36,.22); }
    .state-context::after { display: none; }
    .dish-choice-list { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); }
    .dish-choice-button { font-size: 17px; min-height: 48px; }
    .dish-spread { padding: 18px 10px 26px; }
    .dish-main-layout { grid-template-columns: 1fr; }
    .dish-photo.no-image { min-height: 230px; }
    .dish-lower-grid, .dish-support-grid { grid-template-columns: 1fr; }
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
    const searchUrl = "https://commons.wikimedia.org/wiki/Special:MediaSearch?type=image&search=" +
      encodeURIComponent(dish.imageQuery || (dish.name + " historical photograph"));
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
          '<div class="dish-photo ' + (image ? 'has-image' : 'no-image') + '">' +
            (image
              ? '<img class="dish-photo-image" src="' + image + '" alt="' + escapeArchiveText(dish.name + ' photograph') + '" loading="lazy" decoding="async">'
              : '<div class="dish-photo-placeholder"><strong>Food photograph to be added</strong><span>Use a real, source-credited photograph — not AI-generated imagery</span></div>') +
          '</div>' +
          '<div class="dish-highlight-stack">' +
            '<section class="dish-highlight"><h3>About this food</h3><p>' + escapeArchiveText(dish.overview) + '</p></section>' +
            '<section class="dish-highlight"><h3>Historical background</h3><p>' + escapeArchiveText(dish.history) + '</p></section>' +
          '</div>' +
        '</div>' +
        detailCards +
        '<div class="dish-support-grid ' + (dish.oralNarrative ? 'has-oral' : 'no-oral') + '">' +
          '<div class="historical-slot">' +
            '<h3 class="historical-slot-title">Historical photograph / document</h3>' +
            '<p>' + escapeArchiveText(dish.imageHint || "Historical image slot — add a dated and source-credited item after verification.") + '</p>' +
            '<a href="' + escapeArchiveText(searchUrl) + '" target="_blank" rel="noopener noreferrer">Search historical image material ↗</a>' +
          '</div>' + oral +
        '</div>' +
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
      '<button type="button" class="archive-floating-back" data-back-to-home aria-label="Back to regional catalogue" title="Back to regional catalogue"><span class="back-arrow" aria-hidden="true">←</span><span>Back to regions</span></button>' +
      '<div class="state-page-topbar">' +
        '<div class="state-page-brand"><svg class="state-page-brand-mark" viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="32" cy="32" r="27"/><circle cx="32" cy="32" r="19"/><circle cx="32" cy="32" r="7"/><path d="M32 3v11M32 50v11M3 32h11M50 32h11M11 11l8 8m26 26 8 8M53 11l-8 8M19 45l-8 8"/></svg><span>India’s<br>Culinary Memory Archive</span></div>' +
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
    return true;
  }
  function closeStatePage() {
    root.style.display = "none";
    root.innerHTML = "";
    originalSections.forEach(function (section) { section.style.display = ""; });
    scheduleArchiveTopReset();
  }

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
