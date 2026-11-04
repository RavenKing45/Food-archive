# India's Culinary Memory Archive

A Streamlit starter for the archive homepage. The visual language follows the approved reference: deep maroon navigation, parchment-like surfaces, serif typography, the spices-and-manuscript hero image, and the illustrated footer panorama.

## What's included

- `app.py` — Streamlit launcher; injects local images into the HTML page.
- `index.html` — the complete homepage layout, styles, and small client-side interactions.
- `assets/hero-spices.jpg` — cropped from the approved homepage reference.
- `assets/footer-panorama.jpg` — cropped from the approved homepage reference.
- `assets/stories/` — add Food Stories images here when ready.
- `assets/states/` — add state/UT images here when ready.
- `.streamlit/config.toml` — theme defaults.
- `.gitignore` — excludes virtual environments, secrets, and local/editor files.

State and Food Story photography is intentionally not included yet. Those cards show image placeholders so the layout is ready for your own images.

## Run locally

Use Python 3.9 or newer.

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`.

## Add your Food Stories images later

Copy each image into `assets/stories/` using the matching filename slug:

| Story | Filename |
|---|---|
| The Journey of Biryani | `journey-of-biryani.jpg` |
| Street Food Traditions | `street-food-traditions.jpg` |
| The Story of Sadya | `story-of-sadya.jpg` |
| Sweets of Celebration | `sweets-of-celebration.jpg` |
| Cooking in Clay | `cooking-in-clay.jpg` |

## Add state images later

Copy the image into `assets/states/` using the state's lowercase name with hyphens, for example `rajasthan.jpg`, `west-bengal.jpg`, or `himachal-pradesh.jpg`. The same naming convention works for all 28 states and 8 union territories.

The app automatically reads supported image files from these two folders. No need to edit the Python code when adding images.

## Update the homepage text or cards

Edit `index.html`:

- Navigation labels and homepage copy are in the HTML near the top of the `<body>`.
- Food Story titles and descriptions are in the `stories` array near the bottom of the file.
- State names and the initial featured state order are in the `featuredStates` and `allStates` arrays.
- Colors, spacing, and responsive layout are in the `<style>` block.

The state search filters all 36 state/UT entries. The “See More States” control expands the first 10 cards to the complete list. Food Story cards move horizontally; hovering over the carousel pauses the motion. Reduced-motion settings disable the animation.

## Deploy on Streamlit Community Cloud

1. Create a Git repository from this folder and push it to GitHub.
2. Open Streamlit Community Cloud and create an app from that repository.
3. Set the main file path to `app.py`.
4. Streamlit installs packages from `requirements.txt`.

No API keys or secrets are required for this starter.

## Suggested Git initialization

```bash
git init
git add .
git commit -m "Initial culinary memory archive homepage"
```

## Notes

- The homepage is intentionally a single page: Home, Explore by State, and Food Stories navigate to sections on the same page.
- The story carousel is an automatic horizontal marquee and pauses on hover/focus.
- State cards are archive entry placeholders; link destinations can be connected to state-specific pages when those are ready.
- The reference area in the footer is intentionally left open for your verified sources.
