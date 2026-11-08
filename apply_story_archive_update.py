
from pathlib import Path
import json, sys

HERE = Path(__file__).resolve().parent
HTML = HERE / "index.html"
DATA = HERE / "food_stories.json"
BACKUP = HERE / "index.before_story_archive_update.html"

def array_end(src, start):
    depth, quote, escaped = 0, None, False
    for i in range(start, len(src)):
        c = src[i]
        if quote:
            if escaped: escaped = False
            elif c == "\\\\": escaped = True
            elif c == quote: quote = None
            continue
        if c in ("'", '"', "`"): quote = c
        elif c == "[": depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0: return i + 1
    raise ValueError("Could not find the end of the stories array.")

def main():
    if not HTML.is_file() or not DATA.is_file():
        raise FileNotFoundError("Keep this script, food_stories.json and the project's index.html together.")
    if BACKUP.exists():
        raise FileExistsError("Backup already exists; rename index.before_story_archive_update.html first.")
    original = HTML.read_text(encoding="utf-8")
    src = original
    stories = json.loads(DATA.read_text(encoding="utf-8"))
    if len(stories) != 6: raise ValueError("Expected exactly six stories.")

    marker = "const stories = "
    if src.count(marker) != 1: raise ValueError("Expected one embedded stories array.")
    start = src.index(marker) + len(marker)
    end = array_end(src, start)
    src = src[:start] + json.dumps(stories, ensure_ascii=False, separators=(",", ":")) + src[end:]

    tag = '<section class="stories-section section-wrap" id="stories"'
    a = src.find(tag); b = src.find("</section>", a)
    if a < 0 or b < 0: raise ValueError("Could not find the Food Stories section.")
    b += len("</section>")
    section = '''<section class="stories-section section-wrap" id="stories" aria-labelledby="stories-title">
      <div class="section-heading-row">
        <div><h2 class="section-title" id="stories-title">Food Stories</h2>
        <p class="section-intro">Six carefully selected stories about the people, places and histories behind India's food.</p></div>
        <span class="scroll-note">A selective culinary archive</span>
      </div>
      <div class="story-archive-grid" id="story-archive-grid" aria-live="polite"></div>
    </section>'''
    src = src[:a] + section + src[b:]

    tag = '<dialog class="food-story-dialog" id="food-story-dialog"'
    a = src.find(tag); b = src.find("</dialog>", a)
    if a < 0 or b < 0: raise ValueError("Could not find the old story dialog.")
    b += len("</dialog>")
    reader = '''<div class="story-page-root" id="story-page-root" aria-hidden="true">
      <button class="archive-floating-back story-floating-back" id="story-back-button" type="button">
        <span class="back-arrow" aria-hidden="true">←</span><span>Back to stories</span>
      </button>
      <article class="story-page-article">
        <p class="story-page-region" id="story-page-region"></p>
        <h1 class="story-page-title" id="story-page-title"></h1>
        <p class="story-page-deck" id="story-page-deck"></p><div class="story-page-rule"></div>
        <div class="story-page-body" id="story-page-body"></div>
        <aside class="story-page-note" id="story-page-note" hidden></aside>
        <section class="story-page-sources"><h2>Sources &amp; further reading</h2><ol id="story-page-source-list"></ol></section>
      </article>
    </div>'''
    src = src[:a] + reader + src[b:]

    css = r'''<style id="selective-story-archive-styles">
.story-archive-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;margin-top:24px}
.story-archive-card{appearance:none;width:100%;padding:0;overflow:hidden;border:1px solid rgba(83,43,29,.24);border-radius:13px;background:#f8edda;color:#351915;text-align:left;cursor:pointer;box-shadow:0 4px 12px rgba(74,38,22,.10);display:flex;flex-direction:column;transition:transform .22s,box-shadow .22s}
.story-archive-card:hover{transform:translateY(-4px);box-shadow:0 10px 24px rgba(74,38,22,.16)}
.story-archive-card:focus-visible{outline:3px solid #9a633f;outline-offset:4px}
.story-archive-visual{min-height:190px;position:relative;display:grid;place-items:center;background:linear-gradient(135deg,#8b6745,#3e1d17);background-position:center;background-size:cover;color:#f8e8cb}
.story-archive-visual:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent,rgba(24,10,8,.4))}
.story-archive-visual.tone-market{background-image:linear-gradient(135deg,#9a7040,#452019)}
.story-archive-visual.tone-sweet{background-image:linear-gradient(135deg,#9a564b,#3b1715)}
.story-archive-visual.tone-clay{background-image:linear-gradient(135deg,#98643e,#382018)}
.story-archive-visual.tone-leaf{background-image:linear-gradient(135deg,#526044,#251b13)}
.story-archive-visual.tone-spice{background-image:linear-gradient(135deg,#6c3a20,#30130f)}
.story-archive-mark{position:relative;z-index:1;font:42px Georgia,serif}
.story-archive-copy{padding:17px 18px 20px;display:flex;flex:1;flex-direction:column;gap:8px}
.story-archive-region{color:#8a5a3d;font:700 10px/1.4 Arial,sans-serif;letter-spacing:1.25px;text-transform:uppercase}
.story-archive-copy h3{margin:0;color:#351915;font:600 25px/1.12 "Cormorant Garamond",Georgia,serif}
.story-archive-copy p{margin:0;color:#74584a;font:12px/1.65 Arial,sans-serif}
.story-archive-read{margin-top:7px;color:#8a4d31;font:700 11px/1.3 Arial,sans-serif}
.story-page-root{display:none;position:fixed;inset:0;z-index:2147482000;overflow-y:auto;color:#351915;background:#f4e7ce;background-image:radial-gradient(ellipse at 18% 14%,rgba(255,255,255,.34),transparent 34%),repeating-linear-gradient(0deg,rgba(92,57,34,.018) 0,rgba(92,57,34,.018) 1px,transparent 1px,transparent 5px);font-family:"Libre Baskerville",Georgia,serif}
.story-page-root.is-open{display:block}
.story-page-article{width:min(850px,calc(100% - 44px));margin:0 auto;padding:112px 0 72px}
.story-page-region{margin:0 0 14px;color:#966542;font:700 11px/1.4 Arial,sans-serif;letter-spacing:2px;text-transform:uppercase}
.story-page-title{margin:0;max-width:780px;color:#351915;font:600 clamp(42px,7vw,76px)/.98 "Cormorant Garamond",Georgia,serif}
.story-page-deck{max-width:680px;margin:20px 0 0;color:#795b49;font:italic 18px/1.65 "Libre Baskerville",Georgia,serif}
.story-page-rule{height:1px;margin:34px 0;background:linear-gradient(90deg,#9b6c49,transparent)}
.story-page-body{max-width:720px;color:#40271e;font:16px/2 "Libre Baskerville",Georgia,serif}
.story-page-body p{margin:0 0 23px}
.story-page-note{max-width:720px;margin:35px 0 0;padding:17px 20px;border-left:3px solid #9a6a45;background:rgba(255,250,237,.58);color:#72533f;font:12px/1.75 Arial,sans-serif}
.story-page-sources{max-width:720px;margin-top:46px;padding-top:24px;border-top:1px solid rgba(91,55,35,.25)}
.story-page-sources h2{margin:0 0 15px;color:#563626;font:600 27px/1.1 "Cormorant Garamond",Georgia,serif}
.story-page-sources ol{padding-left:20px;color:#765944;font:12px/1.7 Arial,sans-serif}
.story-page-sources li{margin-bottom:13px}
.story-page-sources a{color:#81482f;text-decoration:underline;text-underline-offset:3px}
.story-page-source-meta{display:block;color:#94765f;font-size:10px}
body.story-page-active{overflow:hidden}
@media(max-width:900px){.story-archive-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:600px){.story-archive-grid{grid-template-columns:1fr;gap:16px}.story-archive-visual{min-height:180px}.story-page-article{width:calc(100% - 38px);padding-top:100px}.story-page-body{font-size:14px;line-height:1.9}.story-page-deck{font-size:15px}.story-floating-back{min-width:0!important;min-height:44px!important;padding:10px 14px!important;font-size:16px!important}}
</style>'''
    if "</head>" not in src: raise ValueError("Could not find </head>.")
    src = src.replace("</head>", css + "\n</head>", 1)

    js_a = src.find("    function storyCard(story, index) {")
    js_b = src.find("    const stateGrid = document.getElementById", js_a)
    if js_a < 0 or js_b < 0: raise ValueError("Could not find old story JavaScript.")
    js = r'''    const storyGrid = document.getElementById("story-archive-grid");
    const storyPage = document.getElementById("story-page-root");
    const storyPageRegion = document.getElementById("story-page-region");
    const storyPageTitle = document.getElementById("story-page-title");
    const storyPageDeck = document.getElementById("story-page-deck");
    const storyPageBody = document.getElementById("story-page-body");
    const storyPageNote = document.getElementById("story-page-note");
    const storyPageSources = document.getElementById("story-page-source-list");

    function storyCard(story, index) {
      const image = STORY_IMAGES[story.slug];
      const visualStyle = image ? `background-image:linear-gradient(180deg,rgba(33,13,10,.02),rgba(33,13,10,.4)),url('${escapeHtml(image)}')` : "";
      return `<button class="story-archive-card" type="button" data-story-index="${index}" aria-label="Read story: ${escapeHtml(story.title)}">
        <div class="story-archive-visual ${image ? "has-image" : "tone-" + story.tone}" style="${visualStyle}">
          ${image ? "" : `<span class="story-archive-mark" aria-hidden="true">${escapeHtml(story.symbol || "✦")}</span>`}
        </div><div class="story-archive-copy">
          <span class="story-archive-region">${escapeHtml(story.region || "Food story")}</span>
          <h3>${escapeHtml(story.title)}</h3><p>${escapeHtml(story.description)}</p>
          <span class="story-archive-read">READ THE STORY&nbsp; →</span>
        </div></button>`;
    }
    storyGrid.innerHTML = stories.map((story, index) => storyCard(story, index)).join("");

    function openFoodStory(index) {
      const story = stories[index];
      if (!story) return;
      storyPageRegion.textContent = story.region || "Food story";
      storyPageTitle.textContent = story.title;
      storyPageDeck.textContent = story.description;
      storyPageBody.innerHTML = (story.paragraphs || []).map(p => `<p>${escapeHtml(p)}</p>`).join("");
      storyPageNote.textContent = story.editorialNote || "";
      storyPageNote.hidden = !story.editorialNote;
      storyPageSources.innerHTML = (story.sources || []).map(source => `<li>
        <a href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(source.title)}</a>
        <span class="story-page-source-meta">${escapeHtml(source.publisher)} · ${escapeHtml(source.date)}</span>
      </li>`).join("");
      storyPage.classList.add("is-open");
      storyPage.setAttribute("aria-hidden", "false");
      document.body.classList.add("story-page-active");
      storyPage.scrollTop = 0;
      document.getElementById("story-back-button").focus();
    }
    function closeFoodStory() {
      storyPage.classList.remove("is-open");
      storyPage.setAttribute("aria-hidden", "true");
      document.body.classList.remove("story-page-active");
    }
    storyGrid.addEventListener("click", event => {
      const card = event.target.closest("[data-story-index]");
      if (card) openFoodStory(Number(card.dataset.storyIndex));
    });
    document.getElementById("story-back-button").addEventListener("click", closeFoodStory);
    document.addEventListener("keydown", event => {
      if (event.key === "Escape" && storyPage.classList.contains("is-open")) closeFoodStory();
    });

'''
    src = src[:js_a] + js + src[js_b:]

    BACKUP.write_text(original, encoding="utf-8")
    HTML.write_text(src, encoding="utf-8")
    print("Updated index.html with six selected stories and the full-page story reader.")
    print("Original backup: " + BACKUP.name)
    print("app.py, state_pages.json, Goa's classification and image assets are unchanged.")

if __name__ == "__main__":
    try: main()
    except Exception as exc:
        print("Update stopped safely: " + str(exc))
        sys.exit(1)
