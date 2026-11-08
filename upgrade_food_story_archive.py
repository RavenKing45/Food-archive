#!/usr/bin/env python3
from urllib.request import urlopen
from pathlib import Path
import re

SOURCE = "https://raw.githubusercontent.com/RavenKing45/Food-archive/main/index.html"
html = urlopen(SOURCE, timeout=30).read().decode("utf-8")

match = re.search(r'<section class="stories-section section-wrap" id="stories".*?</section>', html, re.S)
if not match:
    raise SystemExit("Could not find the existing Food Stories section.")
section = '''<section class="stories-section section-wrap" id="stories" aria-labelledby="stories-title">
  <div class="section-heading-row">
    <div><h2 class="section-title" id="stories-title">Food Stories</h2>
    <p class="section-intro">Explore India's culinary histories, people and regional foodways.</p></div>
    <span class="scroll-note">A living collection of researched stories</span>
  </div>
  <div class="story-grid" id="story-grid" aria-label="Food story archive"></div>
</section>'''
html = html[:match.start()] + section + html[match.end():]

dialog = re.search(r'\s*<dialog class="food-story-dialog".*?</dialog>', html, re.S)
if dialog:
    page = '''
<section class="story-page-root" id="story-page-root" hidden aria-live="polite">
  <button class="archive-floating-back story-floating-back" id="story-back" type="button">
    <span class="back-arrow" aria-hidden="true">←</span><span>Back to Stories</span>
  </button>
  <div class="story-page-topbar"><div class="story-page-brand">India’s Culinary Memory Archive</div></div>
  <header class="story-page-masthead">
    <p class="story-page-kicker" id="story-page-region"></p>
    <h1 id="story-page-title"></h1><p id="story-page-subtitle"></p>
  </header>
  <article class="story-page-content">
    <div class="story-page-body" id="story-page-body"></div>
    <aside class="story-editorial-note" id="story-page-note" hidden></aside>
    <section class="story-page-sources"><h2>Sources &amp; further reading</h2><ol id="story-page-source-list"></ol></section>
  </article>
  <footer class="story-page-footer">A living record of India’s food heritage</footer>
</section>
'''
    html = html[:dialog.start()] + page + html[dialog.end():]

start = html.find("    function storyCard(story, index) {")
end = html.find('    const stateGrid = document.getElementById("state-grid");', start)
if start < 0 or end < 0:
    raise SystemExit("Could not locate the existing story rendering code.")
js = r'''    function storyCard(story, index) {
      const image = STORY_IMAGES[story.slug];
      const visualStyle = image
        ? `background-image: linear-gradient(180deg, rgba(33,13,10,.02), rgba(33,13,10,.64)), url('${image}')`
        : "";
      return `
        <button class="story-card story-archive-card" type="button" data-story-index="${index}" aria-label="Open story: ${escapeHtml(story.title)}">
          <div class="story-visual ${image ? "has-image" : "tone-" + story.tone}" style="${visualStyle}">
            ${image ? "" : `<span class="story-symbol" aria-hidden="true">${story.symbol}</span><span class="image-slot-label">Image to be added</span>`}
          </div>
          <div class="story-copy">
            <span class="story-card-region">${escapeHtml(story.region || "Food story")}</span>
            <h3>${escapeHtml(story.title)}</h3><p>${escapeHtml(story.description)}</p>
            <span class="story-read-link">Read story <span aria-hidden="true">→</span></span>
          </div>
        </button>`;
    }

    const storyGrid = document.getElementById("story-grid");
    storyGrid.innerHTML = stories.map((story, index) => storyCard(story, index)).join("");
    const storyPage = document.getElementById("story-page-root");
    const storyPageRegion = document.getElementById("story-page-region");
    const storyPageTitle = document.getElementById("story-page-title");
    const storyPageSubtitle = document.getElementById("story-page-subtitle");
    const storyPageBody = document.getElementById("story-page-body");
    const storyPageNote = document.getElementById("story-page-note");
    const storyPageSources = document.getElementById("story-page-source-list");
    const archiveMain = document.querySelector("main");
    const archiveFooter = document.querySelector(".site-footer");

    function openFoodStory(index) {
      const story = stories[index];
      if (!story) return;
      storyPageRegion.textContent = story.region || "Food story";
      storyPageTitle.textContent = story.title;
      storyPageSubtitle.textContent = story.description;
      storyPageBody.innerHTML = (story.paragraphs || []).map(p => `<p>${escapeHtml(p)}</p>`).join("");
      storyPageNote.textContent = story.editorialNote || "";
      storyPageNote.hidden = !story.editorialNote;
      storyPageSources.innerHTML = (story.sources || []).map(source => `
        <li><a href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(source.title)}</a>
        <span class="food-story-source-meta">${escapeHtml(source.publisher || "")}${source.date ? " · " + escapeHtml(source.date) : ""}</span></li>`).join("");
      archiveMain.hidden = true;
      if (archiveFooter) archiveFooter.hidden = true;
      storyPage.hidden = false;
      document.body.classList.add("story-page-open");
      window.scrollTo({ top: 0, behavior: "auto" });
      history.pushState({ foodStory: story.slug }, "", "#story/" + encodeURIComponent(story.slug));
    }

    function closeFoodStory(updateHistory = true) {
      if (storyPage.hidden) return;
      storyPage.hidden = true;
      archiveMain.hidden = false;
      if (archiveFooter) archiveFooter.hidden = false;
      document.body.classList.remove("story-page-open");
      if (updateHistory && location.hash.startsWith("#story/")) history.pushState({}, "", location.pathname + location.search);
      window.scrollTo({ top: document.getElementById("stories").offsetTop, behavior: "auto" });
    }

    storyGrid.addEventListener("click", event => {
      const card = event.target.closest("[data-story-index]");
      if (card) openFoodStory(Number(card.dataset.storyIndex));
    });
    document.getElementById("story-back").addEventListener("click", () => closeFoodStory());
    window.addEventListener("popstate", () => {
      if (storyPage && !location.hash.startsWith("#story/")) closeFoodStory(false);
    });
    document.addEventListener("keydown", event => {
      if (event.key === "Escape" && !storyPage.hidden) closeFoodStory();
    });

'''
html = html[:start] + js + html[end:]

styles = r'''
    .story-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:15px; }
    .story-archive-card { width:100%; min-width:0; height:auto; min-height:265px; flex:initial; padding:0; text-align:left; cursor:pointer; border-radius:11px; overflow:hidden; border:1px solid rgba(87,53,33,.3); box-shadow:0 3px 9px rgba(88,49,27,.1); background:#d9bd8d; transition:transform .2s ease,box-shadow .2s ease; }
    .story-archive-card:hover { transform:translateY(-3px); box-shadow:0 8px 18px rgba(65,34,22,.18); }
    .story-archive-card:focus-visible { outline:3px solid #ad7a47; outline-offset:3px; }
    .story-archive-card .story-visual { height:160px; flex:0 0 160px; }
    .story-archive-card .story-copy { min-height:118px; padding:11px 13px 13px; }
    .story-card-region { display:block; margin-bottom:5px; color:#e7c99a; font:9px var(--body); letter-spacing:1.2px; text-transform:uppercase; }
    .story-archive-card .story-copy h3 { font-size:22px; line-height:1.05; margin-bottom:6px; }
    .story-archive-card .story-copy p { font-size:11px; line-height:1.5; }
    .story-read-link { display:inline-block; margin-top:9px; color:#f0d09b; font:700 12px var(--body); }
    .story-page-root[hidden] { display:none !important; }
    .story-page-root { min-height:100vh; color:#351915; background-color:#f4e7ce; background-image:radial-gradient(ellipse at 18% 14%,rgba(255,255,255,.34),transparent 34%),radial-gradient(ellipse at 86% 42%,rgba(173,128,75,.08),transparent 30%),repeating-linear-gradient(0deg,rgba(92,57,34,.018) 0,rgba(92,57,34,.018) 1px,transparent 1px,transparent 5px); font-family:"Libre Baskerville",Georgia,serif; }
    .story-page-topbar { min-height:76px; padding:12px 30px 12px 260px; display:flex; align-items:center; color:#fff1d8; background:linear-gradient(100deg,#35100f,#421613 58%,#2c0c0b); border-bottom:1px solid rgba(221,187,129,.55); }
    .story-page-brand { font:700 22px/.9 "Cormorant Garamond",Georgia,serif; }
    .story-floating-back { position:fixed; top:14px; left:14px; z-index:2147483000; display:inline-flex; align-items:center; justify-content:center; gap:10px; min-width:220px; min-height:54px; max-width:calc(100vw - 28px); padding:12px 19px; border:1.5px solid #3d1714; border-radius:30px; color:#3d1714; background:linear-gradient(180deg,#fff5e2 0%,#f0d9b7 100%); box-shadow:0 5px 17px rgba(28,9,7,.23),inset 0 1px 0 rgba(255,255,255,.78); font:700 19px/1 "Cormorant Garamond",Georgia,serif; cursor:pointer; white-space:nowrap; }
    .story-floating-back:hover { background:linear-gradient(180deg,#fff9ec,#f7e8d0); transform:translateY(-1px); }
    .story-floating-back .back-arrow { color:#6a2921; font:700 24px/1 Georgia,serif; }
    .story-page-masthead { min-height:260px; padding:45px clamp(24px,8vw,120px); display:flex; flex-direction:column; justify-content:center; color:#fff3dc; background:linear-gradient(90deg,rgba(39,13,10,.96),rgba(45,17,13,.75)),radial-gradient(ellipse at 75% 20%,#9a7040,#2b100d 70%); border-bottom:1px solid rgba(112,66,40,.28); }
    .story-page-kicker { margin:0 0 12px; color:#e4c28d; text-transform:uppercase; letter-spacing:2px; font-size:11px; }
    .story-page-masthead h1 { max-width:1000px; margin:0; color:#fff1d8; font:700 clamp(42px,6vw,76px)/.95 "Cormorant Garamond",Georgia,serif; }
    .story-page-masthead > p:last-child { max-width:720px; margin:15px 0 0; color:#f4dfbd; font:italic 23px/1.3 "Cormorant Garamond",Georgia,serif; }
    .story-page-content { width:min(900px,calc(100% - 36px)); margin:42px auto 60px; }
    .story-page-body { color:#3f2922; font:16px/2 "Libre Baskerville",Georgia,serif; }
    .story-page-body p { margin:0 0 25px; }
    .story-editorial-note { margin:30px 0; padding:18px 21px; border-left:4px solid #8b4b35; background:rgba(224,201,162,.4); color:#6a4638; font:italic 17px/1.65 "Cormorant Garamond",Georgia,serif; }
    .story-editorial-note[hidden] { display:none; }
    .story-page-sources { margin-top:42px; padding-top:23px; border-top:1px solid rgba(105,65,41,.28); }
    .story-page-sources h2 { margin:0 0 15px; color:#54201b; font:700 29px "Cormorant Garamond",Georgia,serif; }
    .story-page-sources ol { padding-left:23px; color:#705144; font:12px/1.8 "Libre Baskerville",Georgia,serif; }
    .story-page-sources li { margin-bottom:13px; }
    .story-page-sources a { color:#713b2b; text-decoration:underline; text-underline-offset:3px; }
    .story-page-footer { padding:22px; text-align:center; color:#f6e6c9; background:linear-gradient(100deg,#35100f,#4c1917,#2c0c0b); border-top:3px double #b48b58; font:italic 18px "Cormorant Garamond",Georgia,serif; }
    @media(max-width:1050px) { .story-grid { grid-template-columns:repeat(3,minmax(0,1fr)); } }
    @media(max-width:700px) { .story-grid { grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; } .story-archive-card .story-visual { height:125px; flex-basis:125px; } .story-archive-card .story-copy h3 { font-size:18px; } .story-page-topbar { padding-left:245px; min-height:70px; } .story-page-masthead { min-height:220px; padding:38px 24px; } .story-page-content { margin-top:28px; } .story-page-body { font-size:14px; line-height:1.85; } .story-floating-back { min-width:0; min-height:48px; padding:10px 14px; font-size:17px; } }
    @media(max-width:420px) { .story-grid { grid-template-columns:1fr; } }
'''
pos = html.lower().rfind("</style>")
if pos < 0:
    raise SystemExit("Could not find stylesheet closing tag.")
html = html[:pos] + styles + "\n" + html[pos:]

Path("index.html").write_text(html, encoding="utf-8")
print(f"Created replacement index.html ({len(html):,} characters).")
