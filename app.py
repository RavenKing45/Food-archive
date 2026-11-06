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
SUPPORTED_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}

st.set_page_config(
    page_title="India's Culinary Memory Archive",
    page_icon="✧",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def image_data_uri(path: Path) -> str:
    """Resize and optimize an image, then return it as an embeddable data URI."""
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


@st.cache_data(show_spinner=False)
def image_folder_map(folder_path: str) -> dict[str, str]:
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

story_images = image_folder_map(str(ASSETS / "stories"))
state_images = image_folder_map(str(ASSETS / "states"))
dish_images = image_folder_map(str(ASSETS / "dishes"))

html = html.replace("{{STORY_IMAGES}}", json.dumps(story_images, ensure_ascii=False))
html = html.replace("{{STATE_IMAGES}}", json.dumps(state_images, ensure_ascii=False))

state_pages = load_state_pages(ROOT / "state_pages.json")


def json_for_script(value: object) -> str:
    """Serialize JSON safely for insertion into an inline script."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


STATE_PAGE_EXTENSION = r"""
<style id="archive-state-page-styles">
  .state-page-root {
    display: none;
    min-height: 100vh;
    color: #351915;
    background-color: #f4e7ce;
    background-image:
      radial-gradient(ellipse at 18% 14%, rgba(255,255,255,.34), transparent 34%),
      radial-gradient(ellipse at 86% 42%, rgba(173,128,75,.08), transparent 30%),
      repeating-linear-gradient(0deg, rgba(92,57,34,.018) 0, rgba(92,57,34,.018) 1px, transparent 1px, transparent 5px);
    font-family: "Libre Baskerville", Georgia, serif;
  }
  .state-page-root * { box-sizing: border-box; }
  .state-page-root button, .state-page-root a { font: inherit; }
  .state-page-root a { color: inherit; }
  .state-page-topbar {
    min-height: 76px; padding: 10px 30px 10px 260px;
    display: flex; align-items: center; justify-content: flex-start; gap: 18px;
    color: #fff1d8; background: linear-gradient(100deg,#35100f,#421613 58%,#2c0c0b);
    border-bottom: 1px solid rgba(221,187,129,.55);
  }
  .state-page-brand { display:flex; align-items:center; gap:11px; font:700 22px/.9 "Cormorant Garamond",Georgia,serif; }
  .state-page-brand-mark { width:39px; height:39px; color:#d6b77f; }
  .archive-floating-back {
    position:fixed; top:14px; left:14px; z-index:2147483000;
    display:inline-flex; align-items:center; justify-content:center; gap:10px;
    min-width:220px; min-height:54px; max-width:calc(100vw - 28px);
    padding:12px 19px; border:1px solid rgba(237,211,167,.92); border-radius:30px;
    color:#fff1d8; background:linear-gradient(110deg,#35100f,#54201b 58%,#2c0c0b);
    box-shadow:0 5px 18px rgba(28,9,7,.38), inset 0 1px 0 rgba(255,245,220,.12);
    font:700 19px/1 "Cormorant Garamond",Georgia,serif; letter-spacing:.1px;
    cursor:pointer; white-space:nowrap; transition:transform .18s ease,background .18s ease,box-shadow .18s ease;
  }
  .archive-floating-back:hover {
    background:linear-gradient(110deg,#4b1916,#6a2c25 58%,#3b1110);
    box-shadow:0 7px 20px rgba(28,9,7,.42); transform:translateY(-1px);
  }
  .archive-floating-back .back-arrow { color:#e7c58f; font:700 24px/1 Georgia,serif; }
  .archive-floating-back:focus-visible { outline:3px solid #e7c58f; outline-offset:3px; }
  .state-masthead {
    min-height:220px; padding:34px clamp(24px, 6vw, 88px);
    position:relative; isolation:isolate; display:flex; flex-direction:column; justify-content:center;
    color:#fff3dc; background-color:#2b100d; background-size:cover; background-position:center 45%;
    border-bottom:1px solid rgba(112,66,40,.28);
  }
  .state-masthead::before {
    content:""; position:absolute; inset:0; z-index:-1;
    background:linear-gradient(90deg,rgba(39,13,10,.94) 0%,rgba(45,17,13,.72) 48%,rgba(45,17,13,.18) 100%);
  }
  .state-masthead-kicker { margin:0 0 8px; color:#e4c28d; text-transform:uppercase; letter-spacing:2.3px; font-size:10px; }
  .state-masthead h1 {
    margin:0; color:#fff1d8; font:700 clamp(44px,6vw,76px)/.9 "Cormorant Garamond",Georgia,serif;
  }
  .state-masthead p { max-width:650px; margin:12px 0 0; color:#f4dfbd; font:italic 23px/1.25 "Cormorant Garamond",Georgia,serif; }
  .state-spread {
    width:min(1500px,100%); margin:24px auto 0; padding:0 clamp(12px,2vw,28px) 28px;
  }
  .state-spread-heading {
    display:flex; align-items:center; justify-content:space-between; gap:16px;
    padding:18px 8px 13px; border-bottom:1px solid rgba(105,65,41,.2);
    color:#704b3b; font:italic 18px "Cormorant Garamond",Georgia,serif;
  }
  .state-book {
    display:grid; grid-template-columns:minmax(250px,.78fr) minmax(0,1.7fr);
    border:1px solid rgba(105,65,41,.25); border-top:1px solid rgba(105,65,41,.25);
    background:rgba(255,249,236,.36); box-shadow:0 8px 24px rgba(69,37,24,.09);
  }
  .state-context {
    padding:28px clamp(18px,2.5vw,38px) 30px;
    border-right:1px solid rgba(105,65,41,.28);
    background:linear-gradient(90deg,rgba(229,207,171,.15),rgba(255,249,234,.25));
    position:relative;
  }
  .state-context::after {
    content:""; position:absolute; right:0; top:0; bottom:0; width:5px;
    background:linear-gradient(90deg,rgba(90,44,28,.08),transparent);
  }
  .state-context-label,.state-dishes-label {
    display:block; color:#94623f; text-transform:uppercase; letter-spacing:1.8px;
    font-size:9px; margin-bottom:8px;
  }
  .state-context h2 {
    color:#4e1b18; margin:0 0 20px; font:700 34px/.95 "Cormorant Garamond",Georgia,serif;
  }
  .state-context h3 {
    color:#5a211b; margin:23px 0 7px; font:700 23px/1 "Cormorant Garamond",Georgia,serif;
  }
  .state-context p { color:#3f2922; margin:0; font:12px/1.8 "Libre Baskerville",Georgia,serif; }
  .state-context-ornament {
    height:1px; margin:18px 0; background:linear-gradient(90deg,#94623f,transparent);
  }
  .state-context-note {
    margin-top:25px; padding:15px 15px 17px; background:rgba(224,201,162,.35);
    border:1px solid rgba(126,79,48,.2); border-radius:5px;
    color:#6a4638; font:italic 17px/1.3 "Cormorant Garamond",Georgia,serif;
  }
  .dish-spread { padding:22px clamp(12px,1.5vw,22px) 28px; min-width:0; }
  .dish-spread-top {
    display:flex; align-items:baseline; justify-content:space-between; gap:12px;
    margin:0 4px 15px; padding-bottom:10px; border-bottom:1px solid rgba(105,65,41,.25);
  }
  .dish-spread-top h2 { margin:0; color:#54201b; font:700 27px/1 "Cormorant Garamond",Georgia,serif; }
  .dish-spread-top span { color:#88634e; font-size:9px; letter-spacing:1px; text-transform:uppercase; }
  .dish-record {
    min-width:0; padding:0 11px 16px; border-right:1px solid rgba(105,65,41,.21);
  }
  .dish-record:last-child { border-right:0; }
  .dish-record-number { color:#9a6b49; font-size:9px; letter-spacing:1.6px; text-transform:uppercase; }
  .dish-record h2 {
    color:#4b1715; font:700 clamp(27px,2.7vw,39px)/.9 "Cormorant Garamond",Georgia,serif;
    margin:5px 0 7px;
  }
  .dish-descriptor { color:#765344; font:italic 17px/1.15 "Cormorant Garamond",Georgia,serif; margin:0 0 12px; }
  .dish-photo {
    min-height:170px; width:100%; position:relative; overflow:hidden; border-radius:7px;
    background:linear-gradient(145deg,#dbc39d,#97704e 72%,#49241b);
    border:1px solid rgba(105,65,41,.3); margin:0 0 13px;
    display:flex; align-items:center; justify-content:center; text-align:center;
    color:#fff0d7; background-size:cover; background-position:center;
  }
  .dish-photo::after { content:""; position:absolute; inset:0; background:linear-gradient(180deg,transparent 48%,rgba(38,14,11,.35)); pointer-events:none; }
  .dish-photo-placeholder { position:relative; z-index:1; padding:12px; text-shadow:0 1px 4px rgba(0,0,0,.4); }
  .dish-photo-placeholder strong { display:block; font:700 20px "Cormorant Garamond",Georgia,serif; }
  .dish-photo-placeholder span { display:block; margin-top:4px; font-size:8px; letter-spacing:1.3px; text-transform:uppercase; }
  .dish-overview { color:#432c24; font:11px/1.7 "Libre Baskerville",Georgia,serif; margin:0 0 14px; }
  .dish-section { margin:15px 0 0; }
  .dish-section h3 {
    color:#57201b; margin:0 0 7px; padding-bottom:5px; border-bottom:1px solid rgba(105,65,41,.18);
    font:700 22px/1 "Cormorant Garamond",Georgia,serif;
  }
  .dish-section p { color:#432c24; margin:0; font:10px/1.75 "Libre Baskerville",Georgia,serif; }
  .dish-section ul,.dish-section ol { color:#432c24; margin:0; padding-left:18px; font:10px/1.75 "Libre Baskerville",Georgia,serif; }
  .dish-section li { padding-left:2px; margin:0 0 3px; }
  .historical-slot {
    margin-top:16px; padding:11px; border:1px dashed rgba(112,70,43,.55);
    background:rgba(233,215,182,.28); border-radius:5px;
  }
  .historical-slot-title {
    color:#6e3c2c; font:700 19px/1 "Cormorant Garamond",Georgia,serif; margin:0 0 5px;
  }
  .historical-slot p { margin:0 0 9px; color:#725344; font:11.5px/1.62 "Libre Baskerville",Georgia,serif; }
  .historical-slot a,.dish-sources a,.oral-source a {
    color:#78352a; text-decoration:underline; text-decoration-color:rgba(120,53,42,.45);
    text-underline-offset:2px;
  }
  .historical-slot a:hover,.dish-sources a:hover,.oral-source a:hover { color:#a04b35; }
  .dish-sources { margin-top:14px; padding-top:10px; border-top:1px solid rgba(105,65,41,.2); }
  .dish-sources h4 { margin:0 0 6px; color:#6a3a2c; font:700 18px/1 "Cormorant Garamond",Georgia,serif; }
  .dish-sources ol { margin:0; padding-left:17px; color:#705144; font:9px/1.65 "Libre Baskerville",Georgia,serif; }
  .dish-sources li { margin-bottom:5px; }
  .oral-narrative {
    margin-top:14px; padding:12px 13px; background:rgba(223,201,165,.38);
    border-left:3px solid #8b4b35; border-radius:0 5px 5px 0;
  }
  .oral-narrative h4 { color:#56211b; font:700 20px/1 "Cormorant Garamond",Georgia,serif; margin:0 0 7px; }
  .oral-narrative .oral-person { color:#4f261e; font:700 15px "Cormorant Garamond",Georgia,serif; margin:0 0 3px; }
  .oral-narrative .oral-role { color:#86614a; font:italic 11px/1.5 "Libre Baskerville",Georgia,serif; margin:0 0 8px; }
  .oral-narrative p { color:#4b332a; font:11.5px/1.65 "Libre Baskerville",Georgia,serif; margin:0 0 8px; }
  .oral-source { padding-top:7px; border-top:1px solid rgba(105,65,41,.18); color:#765444; font:10.5px/1.58 "Libre Baskerville",Georgia,serif; }
  .state-page-end {
    display:flex; justify-content:space-between; gap:14px; align-items:center;
    padding:17px clamp(20px,4vw,58px); color:#f6e6c9;
    background:linear-gradient(100deg,#35100f,#4c1917,#2c0c0b);
    border-top:3px double #b48b58; font:italic 18px "Cormorant Garamond",Georgia,serif;
  }
  .state-page-end button { border:1px solid rgba(246,230,201,.65); background:transparent; border-radius:22px; padding:7px 15px; color:#f6e6c9; cursor:pointer; }
  .state-card[data-has-archive="true"] { cursor:pointer; }
  .state-card[data-has-archive="true"]:focus-visible { outline:3px solid #ad7a47; outline-offset:3px; }
  .state-card[data-has-archive="false"] { cursor:default; }
  @media(max-width:1050px) {
    .state-book { grid-template-columns:minmax(220px,.65fr) minmax(0,1.6fr); }
    .dish-record { padding:0 7px 12px; }
    .dish-photo { min-height:145px; }
  }
  @media(max-width:760px) {
    .state-page-topbar { min-height:128px; padding:78px 18px 14px; align-items:flex-end; justify-content:flex-start; }
    .state-page-brand { font-size:19px; }
    .archive-floating-back { top:10px; left:10px; min-width:205px; min-height:52px; padding:11px 16px; font-size:18px; }
    .state-masthead { min-height:190px; padding:28px 22px; }
    .state-masthead p { font-size:19px; }
    .state-spread { padding-left:10px; padding-right:10px; }
    .state-book { grid-template-columns:1fr; }
    .state-context { border-right:0; border-bottom:1px solid rgba(105,65,41,.28); }
    .state-context::after { display:none; }
    .dish-spread { padding:18px 10px 24px; }
    .dish-record { border-right:0; border-bottom:1px solid rgba(105,65,41,.3); padding:0 5px 20px; }
    .dish-record:last-child { border-bottom:0; }
    .dish-photo { min-height:210px; }
    .state-spread-heading { font-size:15px; }
    .state-page-end { flex-direction:column; text-align:center; }
  }
  @media(prefers-reduced-motion:reduce) {
    .state-page-root *, .state-page-root *::before, .state-page-root *::after { scroll-behavior:auto !important; transition:none !important; }
  }

  /* Single-dish chapter view: choose one dish from the state list at a time. */
  .state-book {
    display:grid; grid-template-columns:minmax(245px,.72fr) minmax(0,1.95fr);
    border:1px solid rgba(105,65,41,.25); border-top:1px solid rgba(105,65,41,.25);
    background:rgba(255,249,236,.36); box-shadow:0 8px 24px rgba(69,37,24,.09);
  }
  .state-context { padding:27px 22px 30px; }
  .state-context h2 { margin-bottom:16px; }
  .dish-choice-heading {
    color:#8c5b3d; margin:0 0 9px; text-transform:uppercase;
    letter-spacing:1.5px; font:10px "Libre Baskerville",Georgia,serif;
  }
  .dish-choice-list { display:flex; flex-direction:column; gap:9px; margin:0 0 24px; }
  .dish-choice-button {
    width:100%; min-height:54px; display:flex; align-items:center; gap:10px;
    padding:9px 11px; text-align:left; border:1px solid rgba(126,79,48,.24);
    border-radius:9px; color:#4d211b; background:rgba(255,248,232,.54);
    font:700 20px/1.05 "Cormorant Garamond",Georgia,serif; cursor:pointer;
    transition:background .18s ease,border-color .18s ease,transform .18s ease;
  }
  .dish-choice-button::after { content:"›"; margin-left:auto; color:#74382a; font:700 29px/1 "Cormorant Garamond",Georgia,serif; }
  .dish-choice-button:hover { background:#f8e6cb; border-color:rgba(126,79,48,.52); transform:translateX(2px); }
  .dish-choice-button[aria-selected="true"] {
    background:linear-gradient(100deg,#f2ddbd,#eed4b5); border-color:#d8b18b;
    box-shadow:inset 3px 0 #85442f,0 2px 7px rgba(90,47,30,.06);
  }
  .dish-choice-index { flex:0 0 25px; color:#9a6b49; font:700 13px "Libre Baskerville",Georgia,serif; }
  .state-context h3 { font-size:24px; }
  .state-context p { font-size:12.5px; line-height:1.68; }
  .dish-spread { padding:22px clamp(13px,1.8vw,27px) 30px; min-width:0; }
  .dish-spread-top { margin:0 3px 14px; padding-bottom:10px; }
  .dish-spread-top h2 { font-size:28px; }
  .dish-spread-top span { font-size:9px; }
  .dish-content { min-width:0; }
  .dish-record { border:0; padding:0; }
  .dish-record-head { margin:0 3px 14px; }
  .dish-record-number { display:block; color:#926242; font-size:10px; letter-spacing:1.4px; text-transform:uppercase; }
  .dish-record-head h2 {
    color:#4b1715; font:700 clamp(32px,3.2vw,44px)/.98 "Cormorant Garamond",Georgia,serif;
    margin:5px 0 7px;
  }
  .dish-descriptor { margin:0; font-size:19px; line-height:1.2; }
  .dish-meta-line {
    display:flex; flex-wrap:wrap; gap:8px 17px; margin-top:10px;
    color:#6f5141; font:11px "Libre Baskerville",Georgia,serif;
  }
  .dish-meta-line span { display:inline-flex; align-items:center; gap:6px; }
  .dish-main-layout {
    display:grid; grid-template-columns:minmax(0,1.15fr) minmax(250px,.9fr);
    gap:20px; align-items:start;
  }
  .dish-photo {
    min-height:330px; margin:0; border-radius:8px;
    background:linear-gradient(145deg,#dbc39d,#97704e 72%,#49241b);
  }
  .dish-photo-placeholder strong { font-size:25px; }
  .dish-photo-placeholder span { font-size:9px; line-height:1.6; }
  .dish-highlight-stack { display:flex; flex-direction:column; gap:17px; }
  .dish-highlight {
    position:relative; padding:2px 0 13px 15px;
    border-bottom:1px solid rgba(105,65,41,.2);
  }
  .dish-highlight:last-child { border-bottom:0; }
  .dish-highlight h3 {
    margin:0 0 6px; color:#56211b; font:700 24px/1 "Cormorant Garamond",Georgia,serif;
  }
  .dish-highlight p { margin:0; color:#432c24; font:12px/1.68 "Libre Baskerville",Georgia,serif; }
  .dish-highlight::before {
    content:"✧"; position:absolute; left:0; top:2px; color:#8d4c34; font-size:12px;
  }
  .dish-lower-grid {
    display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px;
    margin-top:18px;
  }
  .dish-info-card {
    min-width:0; padding:13px 14px 15px; border:1px solid rgba(126,79,48,.2);
    border-radius:7px; background:rgba(255,248,232,.46);
  }
  .dish-info-card h3 {
    color:#57201b; margin:0 0 8px; padding-bottom:6px;
    border-bottom:1px solid rgba(105,65,41,.18);
    font:700 23px/1 "Cormorant Garamond",Georgia,serif;
  }
  .dish-info-card ul,.dish-info-card ol {
    margin:0; padding-left:19px; color:#432c24;
    font:12px/1.62 "Libre Baskerville",Georgia,serif;
  }
  .dish-info-card li { padding-left:2px; margin:0 0 5px; }
  .dish-support-grid {
    display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:15px;
    margin-top:16px; align-items:start;
  }
  .dish-support-grid .historical-slot { margin:0; min-height:100%; }
  .dish-support-grid .oral-narrative { margin:0; }
  .dish-sources { margin-top:16px; padding:11px 13px 0; }
  .dish-sources h4 { font-size:21px; }
  .dish-sources ol { font-size:10.5px; line-height:1.62; }
  @media(max-width:1050px) {
    .state-book { grid-template-columns:minmax(225px,.7fr) minmax(0,1.8fr); }
    .dish-main-layout { grid-template-columns:minmax(0,1fr) minmax(220px,.9fr); gap:13px; }
    .dish-photo { min-height:280px; }
  }
  @media(max-width:760px) {
    .state-book { grid-template-columns:1fr; }
    .state-context { border-right:0; border-bottom:1px solid rgba(105,65,41,.28); }
    .state-context::after { display:none; }
    .dish-choice-list { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); }
    .dish-choice-button { font-size:17px; min-height:50px; }
    .dish-main-layout { grid-template-columns:1fr; }
    .dish-photo { min-height:240px; }
    .dish-lower-grid,.dish-support-grid { grid-template-columns:1fr; }
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
  const unionTerritorySlugs = new Set([
    "andaman-and-nicobar-islands", "chandigarh",
    "dadra-and-nagar-haveli-and-daman-and-diu", "delhi",
    "jammu-and-kashmir", "ladakh", "lakshadweep", "puducherry"
  ]);
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
    ) : (
      '<section class="oral-narrative"><h4>Oral narrative</h4>' +
      '<p>No named, attributable oral account has been verified for this dish in the sources currently available. This space is reserved for a documented interview or community testimony.</p></section>'
    );
    return (
      '<article class="dish-record">' +
        '<header class="dish-record-head">' +
          '<h2>' + escapeArchiveText(dish.name) + '</h2>' +
          '<p class="dish-descriptor">' + escapeArchiveText(dish.descriptor || "") + '</p>' +
        '</header>' +
        '<div class="dish-main-layout">' +
          '<div class="dish-photo" ' + (image ? 'style="background-image:url(' + image + ')"' : '') + '>' +
            (image ? '' : '<div class="dish-photo-placeholder"><strong>Dish photograph to be added</strong><span>Use a real, source-credited photograph — not AI-generated imagery</span></div>') +
          '</div>' +
          '<div class="dish-highlight-stack">' +
            '<section class="dish-highlight"><h3>About the dish</h3><p>' + escapeArchiveText(dish.overview) + '</p></section>' +
            '<section class="dish-highlight"><h3>How it came to be</h3><p>' + escapeArchiveText(dish.history) + '</p></section>' +
          '</div>' +
        '</div>' +
        '<div class="dish-lower-grid">' +
          '<section class="dish-info-card"><h3>Ingredients</h3><ul>' + ingredients + '</ul></section>' +
          '<section class="dish-info-card"><h3>How it is made</h3><ol>' + steps + '</ol></section>' +
        '</div>' +
        '<div class="dish-support-grid">' +
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
    const regionType = unionTerritorySlugs.has(slug) ? "Union Territory" : "State";
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
            '<div class="dish-choice-list" role="tablist" aria-label="Dishes from ' + escapeArchiveText(state.name) + '">' + dishButtons + '</div>' +
            '<h3>Geography & influence</h3>' +
            '<p>' + escapeArchiveText(state.geography) + '</p>' +
            '<div class="state-context-ornament"></div>' +
            '<h3>Culinary landscape</h3>' +
            '<p>' + escapeArchiveText(state.culinaryLandscape) + '</p>' +
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
