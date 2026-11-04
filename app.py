"""Streamlit launcher for India's Culinary Memory Archive homepage."""

from __future__ import annotations

import base64
import json
from io import BytesIO
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
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
        image.thumbnail((1800, 1400), Image.Resampling.LANCZOS)

        output = BytesIO()
        if image.mode in {"RGBA", "LA"}:
            image.save(output, format="WEBP", quality=86, method=6)
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

# Hide Streamlit's surrounding chrome so the archive itself is the visible page.
st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility: hidden; height: 0;}
      .stApp {background: #f4e7ce;}
      .block-container {padding: 0 !important; max-width: 100% !important;}
      iframe {border: 0;}
      [data-testid="stToolbar"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(html, height=1840, scrolling=True)
