"""Streamlit launcher for India's Culinary Memory Archive homepage.

The HTML page is embedded with content-based sizing so the Streamlit page ends
at the illustrated footer instead of leaving a fixed-height blank area below it.
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
                quality=90,
                optimize=True,
                progressive=True,
            )
            mime_type = "image/jpeg"

    encoded = base64.b64encode(output.getvalue()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def image_folder_map(folder: Path) -> dict[str, str]:
    """Load optional images keyed by filename stem (without extension)."""
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

html = html.replace("{{STORY_IMAGES}}", json.dumps(image_folder_map(ASSETS / "stories")))
html = html.replace("{{STATE_IMAGES}}", json.dumps(image_folder_map(ASSETS / "states")))

# The archive HTML owns its complete visual layout. Remove Streamlit's chrome
# and container padding so the archive begins flush with the top of the page.
st.markdown(
    """
    <style>
      html, body, .stApp {
          margin: 0 !important;
          padding: 0 !important;
      }

      [data-testid="stHeader"],
      [data-testid="stToolbar"],
      [data-testid="stDecoration"],
      #MainMenu,
      header,
      footer {
          display: none !important;
          height: 0 !important;
          min-height: 0 !important;
          visibility: hidden !important;
      }

      [data-testid="stAppViewContainer"],
      [data-testid="stMain"],
      section.main,
      section.main > div {
          margin: 0 !important;
          padding: 0 !important;
      }

      [data-testid="stMainBlockContainer"],
      [data-testid="stAppViewBlockContainer"],
      .block-container {
          width: 100% !important;
          max-width: 100% !important;
          margin: 0 !important;
          padding: 0 !important;
      }

      [data-testid="stVerticalBlock"],
      [data-testid="stHorizontalBlock"] {
          gap: 0 !important;
      }

      iframe {
          display: block !important;
          width: 100% !important;
          border: 0 !important;
          margin: 0 !important;
          padding: 0 !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# IMPORTANT: content sizing replaces the old fixed 2100px iframe height.
# This prevents a blank strip after the footer and lets the embed resize to
# the actual HTML content height, including the expanded state-card grid.
st.iframe(
    html,
    width="stretch",
    height="content",
    alt="India's Culinary Memory Archive homepage",
)
