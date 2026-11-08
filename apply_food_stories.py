from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
DATA = ROOT / "food_stories.json"
OUTPUT = ROOT / "index_food_stories_updated.html"

STORY_CSS = r"""
    .story-card {
      padding: 0;
      color: inherit;
      font-family: inherit;
      text-align: left;
      cursor: pointer;
      appearance: none;
      -webkit-appearance: none;
      transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
    }
    .story-card:hover {
      transform: translateY(-2px);
      border-color: rgba(197,161,106,.9);
      box-shadow: 0 7px 16px rgba(74,38,22,.18);
    }
    .story-card:focus-visible {
      outline: 3px solid #c5a16a;
      outline-offset: 4px;
    }
    .food-story-dialog {
      width: min(760px, calc(100% - 28px));
      max-width: 760px;
      max-height: 88vh;
      padding: 0;
      border: 1px solid #b58b55;
      border-radius: 12px;
      color: #351915;
      background: transparent;
      box-shadow: 0 18px 60px rgba(23,8,6,.42);
    }
    .food-story-dialog::backdrop {
      background: rgba(31,10,8,.72);
      backdrop-filter: blur(2px);
    }
    .food-story-panel {
      max-height: 88vh;
      overflow-y: auto;
      padding: clamp(22px, 4vw, 38px);
      background-color: #fbf3e4;
      background-image:
        radial-gradient(ellipse at 18% 14%, rgba(255,255,255,.4), transparent 34%),
        repeating-linear-gradient(0deg, rgba(92,57,34,.018) 0, rgba(92,57,34,.018) 1px, transparent 1px, transparent 5px);
    }
    .food-story-dialog-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding-bottom: 12px;
      border-bottom: 1px solid rgba(91,48,34,.28);
    }
    .food-story-dialog-region {
      margin: 0;
      color: #845a40;
      font-family: var(--body);
      font-size: 8px;
      letter-spacing: 1.7px;
      line-height: 1.5;
      text-transform: uppercase;
    }
    .food-story-close {
      border: 1px solid rgba(91,48,34,.35);
      border-radius: 50%;
      width: 34px;
      height: 34px;
      color: #4b1c18;
      background: rgba(255,248,232,.8);
      font-family: Georgia, serif;
      font-size: 22px;
      line-height: 1;
    }
    .food-story-close:hover { background: #f0dfc2; }
    .food-story-title {
      margin: 20px 0 5px;
      color: #4d1715;
      font-family: var(--serif);
      font-size: clamp(30px, 5vw, 43px);
      line-height: .98;
      font-weight: 700;
    }
    .food-story-subtitle {
      margin: 0 0 20px;
      color: #805a45;
      font-family: var(--serif);
      font-size: 20px;
      font-style: italic;
      line-height: 1.25;
    }
    .food-story-body p {
      margin: 0 0 13px;
      color: #40221b;
      font-family: var(--body);
      font-size: 11px;
      line-height: 1.9;
    }
    .food-story-note {
      margin: 18px 0 0;
      padding: 12px 14px;
      border-left: 3px solid #9a6948;
      background: rgba(232,211,175,.38);
      color: #6c4a37;
      font-family: var(--body);
      font-size: 9px;
      line-height: 1.7;
    }
    .food-story-sources {
      margin-top: 24px;
      padding-top: 15px;
      border-top: 1px solid rgba(91,48,34,.28);
    }
    .food-story-sources h3 {
      margin: 0 0 10px;
      color: #57201b;
      font-family: var(--serif);
      font-size: 23px;
      line-height: 1;
    }
    .food-story-sources ol {
      margin: 0;
      padding-left: 20px;
    }
    .food-story-sources li {
      margin: 0 0 10px;
      padding-left: 3px;
      color: #56372b;
      font-family: var(--body);
      font-size: 9px;
      line-height: 1.65;
    }
    .food-story-sources a {
      color: #5a211b;
      font-weight: 700;
      text-decoration: underline;
      text-decoration-color: rgba(90,33,27,.5);
      text-underline-offset: 2px;
    }
    .food-story-source-meta {
      display: block;
      margin-top: 2px;
      color: #806858;
      font-size: 8px;
    }
    @media (max-width: 640px) {
      .food-story-panel { padding: 21px 18px 24px; }
      .food-story-body p { font-size: 10px; }
      .food-story-sources li { font-size: 8px; }
    }
"""

DIALOG_HTML = r"""
  <dialog class="food-story-dialog" id="food-story-dialog" aria-labelledby="food-story-dialog-title">
    <div class="food-story-panel">
      <div class="food-story-dialog-top">
        <p class="food-story-dialog-region" id="food-story-dialog-region"></p>
        <button class="food-story-close" id="food-story-close" type="button" aria-label="Close story">×</button>
      </div>
      <h2 class="food-story-title" id="food-story-dialog-title"></h2>
      <p class="food-story-subtitle" id="food-story-dialog-subtitle"></p>
      <div class="food-story-body" id="food-story-dialog-body"></div>
      <p class="food-story-note" id="food-story-dialog-note" hidden></p>
      <section class="food-story-sources" aria-labelledby="food-story-sources-title">
        <h3 id="food-story-sources-title">Sources &amp; further reading</h3>
        <ol id="food-story-source-list"></ol>
      </section>
    </div>
  </dialog>
"""

NEW_STORY_CARD = r"""    function storyCard(story, index) {
      const image = STORY_IMAGES[story.slug];
      const visualStyle = image
        ? `background-image: linear-gradient(180deg, rgba(33,13,10,.04), rgba(33,13,10,.12)), url('${image}')`
        : "";
      return `
        <button class="story-card" type="button" data-story-index="${index}" aria-haspopup="dialog" aria-label="Read story: ${escapeHtml(story.title)}">
          <div class="story-visual ${image ? "has-image" : "tone-" + story.tone}" style="${visualStyle}">
            ${image ? "" : `<span class="story-symbol" aria-hidden="true">${story.symbol}</span><span class="image-slot-label">Image to be added</span>`}
          </div>
          <div class="story-copy"><h3>${escapeHtml(story.title)}</h3><p>${escapeHtml(story.description)}</p></div>
        </button>`;
    }
"""

NEW_STORY_INIT = r"""    const groupA = document.getElementById("story-group-a");
    const groupB = document.getElementById("story-group-b");
    groupB.setAttribute("inert", "");
    groupA.innerHTML = stories.map((story, index) => storyCard(story, index)).join("");
    groupB.innerHTML = stories.map((story, index) => storyCard(story, index)).join("");

    const storyDialog = document.getElementById("food-story-dialog");
    const storyDialogRegion = document.getElementById("food-story-dialog-region");
    const storyDialogTitle = document.getElementById("food-story-dialog-title");
    const storyDialogSubtitle = document.getElementById("food-story-dialog-subtitle");
    const storyDialogBody = document.getElementById("food-story-dialog-body");
    const storyDialogNote = document.getElementById("food-story-dialog-note");
    const storySourceList = document.getElementById("food-story-source-list");

    function openFoodStory(index) {
      const story = stories[index];
      if (!story) return;
      storyDialogRegion.textContent = story.region || "Food story";
      storyDialogTitle.textContent = story.title;
      storyDialogSubtitle.textContent = story.description;
      storyDialogBody.innerHTML = (story.paragraphs || []).map(paragraph => `<p>${escapeHtml(paragraph)}</p>`).join("");
      storyDialogNote.textContent = story.editorialNote || "";
      storyDialogNote.hidden = !story.editorialNote;
      storySourceList.innerHTML = (story.sources || []).map(source => `
        <li>
          <a href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(source.title)}</a>
          <span class="food-story-source-meta">${escapeHtml(source.publisher)} · ${escapeHtml(source.date)}</span>
        </li>`).join("");
      storyDialog.showModal();
    }

    groupA.addEventListener("click", event => {
      const card = event.target.closest("[data-story-index]");
      if (!card) return;
      openFoodStory(Number(card.dataset.storyIndex));
    });
    document.getElementById("food-story-close").addEventListener("click", () => storyDialog.close());
    storyDialog.addEventListener("click", event => {
      if (event.target === storyDialog) storyDialog.close();
    });
"""


def main() -> int:
    if not INDEX.is_file():
        print("ERROR: index.html was not found. Put this script beside your current index.html.")
        return 1
    if not DATA.is_file():
        print("ERROR: food_stories.json was not found beside this script.")
        return 1

    html = INDEX.read_text(encoding="utf-8")
    data = json.loads(DATA.read_text(encoding="utf-8"))
    stories = data.get("stories", [])
    if len(stories) != 8:
        print(f"ERROR: Expected 8 approved stories in food_stories.json, found {len(stories)}.")
        return 1

    if 'id="food-story-dialog"' in html or "function openFoodStory(index)" in html:
        print("ERROR: Food Stories detail view already appears to be installed. Restore the original index.html before running this installer again.")
        return 1

    required_fragments = [
        "    const stories = [",
        "    function storyCard(story) {",
        '    groupB.innerHTML = stories.map(storyCard).join("");',
        "  </style>\n</head>",
        "  <script>\n",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in html]
    if missing:
        print("ERROR: The current index.html does not match the expected Food Stories template.")
        print("Missing template markers:")
        for item in missing:
            print(" -", repr(item))
        print("No file has been modified.")
        return 1

    stories_js = "    const stories = " + json.dumps(stories, ensure_ascii=False, separators=(",", ":")) + ";"
    html = re.sub(r"    const stories = \[.*?\n    \];", lambda _: stories_js, html, count=1, flags=re.S)

    html = html.replace("  </style>\n</head>", STORY_CSS + "\n  </style>\n</head>", 1)
    html = html.replace("  <script>\n", DIALOG_HTML + "\n  <script>\n", 1)

    old_card_start = html.index("    function storyCard(story) {")
    old_group_start = html.index("    const groupA = document.getElementById(\"story-group-a\");", old_card_start)
    html = html[:old_card_start] + NEW_STORY_CARD + "\n" + html[old_group_start:]

    old_init = (
        '    const groupA = document.getElementById("story-group-a");\n'
        '    const groupB = document.getElementById("story-group-b");\n'
        '    groupA.innerHTML = stories.map(storyCard).join("");\n'
        '    groupB.innerHTML = stories.map(storyCard).join("");'
    )
    if old_init not in html:
        print("ERROR: Could not locate the story carousel initialisation block. No output file written.")
        return 1
    html = html.replace(old_init, NEW_STORY_INIT.rstrip(), 1)

    # Sanity checks on the generated source before writing it.
    if html.count('id="food-story-dialog"') != 1:
        print("ERROR: Dialog insertion check failed. No output file written.")
        return 1
    if html.count("function openFoodStory(index)") != 1:
        print("ERROR: Story interaction insertion check failed. No output file written.")
        return 1
    if "const STORY_IMAGES = {{STORY_IMAGES}};" not in html:
        print("ERROR: Story-image injection placeholder was unexpectedly changed. No output file written.")
        return 1

    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Created: {OUTPUT.name}")
    print(f"Approved stories: {len(stories)}")
    print("Updated only the Food Stories carousel and its story-detail dialog.")
    print("No image files, app.py, state_pages.json, or other homepage sections were changed.")
    print("Review the new file, then rename it to index.html to replace the old homepage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
