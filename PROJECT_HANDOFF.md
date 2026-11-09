# PROJECT HANDOFF — INDIA'S CULINARY MEMORY ARCHIVE

**File Status:** Living Single Source of Truth for Model/Account Handoffs  
**Last Updated:** 2026-11-09T05:40:00+05:30  
**Project Root:** Local workspace root (`culinary-memory-archive`)  
**Git Repository:** `RavenKing45/Food-archive` on branch `main`  
**Baseline Commit SHA:** `fbe9bdb` ("Polish: design token system, typography, responsive layout, accessibility")  
**Git Status:** Working tree contains uncommitted creative overhaul changes in `index.html` and `app.py`. Untracked files and directories exist and are strictly preserved.

---

## A. Project Identity and Purpose

- **Project Name:** India's Culinary Memory Archive
- **Repository Location:** `RavenKing45/Food-archive`
- **Application Architecture:** Streamlit server hosting a custom vanilla HTML5/CSS3/JavaScript frontend via an iframe wrapper (`app.py` serving `index.html`).
- **Purpose & Core Identity:** A digital archive documenting India's culinary heritage across all 36 States and Union Territories. It synthesizes regional cuisines, dishes, ingredients, preparation methods, historical contexts, geography, oral narratives, and researched food stories.
- **Intended Audience & Tone:** Contemporary digital museum, an editorial food-history publication, and an interactive cultural reference book. Archival identity, rigorous citations, and reading comfort take precedence.
- **Current Creative Direction:** **Creative Overhaul Executed & Refined**. Bespoke Astha-Dala compass-star emblem, distinguished typography, photograph-led editorial layouts, rich multi-image story chapters with archival plates, pull quotes, dynamic provenance/classification metadata, atmospheric regional atlas exploration, and purposeful Emil Kowalski physical motion.

---

## B. Original Creative Brief & Skill Framework

### 1. Scope & Goals
- Transform the website into an ambitious, museum-grade cultural archive without breaking underlying functionality or data integrity.
- Redesign the visual identity, emblem, typography, color palette, navigation, hero, story readers, and regional chapters.
- **Story Reader Overhaul (Top Priority — Completed & Polished):** Dynamic reading progress bar, 16:9 museum plate framing with dark lacquer caption bars, dual comparative contextual plates from `STATE_IMAGES`, dynamic provenance and archival classification strips, 76px drop-caps, typographic pull quotes (`\201C`), curatorial memorandum with diamond star insignia (`\2726`), academic dossiers, and tactile navigation controls.
- **Homepage & Hero (Completed):** Arresting editorial entrance with purposeful typography, layered visual composition, catalogue badge, 3-column folio story cards, and 5-column regional atlas with search and match counter.
- **Regional Atlas & Dish Browser (Completed & Polished):** Structure the 36 regions and 72 dishes into an engaging interactive reference experience with seamless switching, gold-accented archival research desiderata cards, and rich context.
- **Strict Data & Functional Preservation:** Retain all 36 regional chapters, 72 dishes, 6 researched food stories, citations, oral histories, template markers (`{{HERO_IMAGE}}`, `{{FOOTER_IMAGE}}`, `{{STORY_IMAGES}}`, `{{STATE_IMAGES}}`, `{{REGION_TYPES}}`), and administrative classifications (e.g., Goa must remain classified accurately). Do not modify `state_pages.json` directly.

### 2. Design Skills Applied
1. **Impeccable (`.agents/skills/impeccable`):**
   - Quality floor standards (contrast ≥4.5:1, generous rhythmic spacing, themed browser surfaces, focus rings, semantic markup).
   - Strict Craft Floor Bans: No eyebrow kickers above headings, no gradient text, no same-size card scaffold repetition, no emoji icons, no fake decorative lines.
   - Operating Mode: **Experience / Read** (archive content leads, interface frames it with quiet authority).
2. **Taste (`.agents/skills/design-taste-frontend`):**
   - Anti-slop frontend craftsmanship.
   - Place/Heritage archetype: photography leads, flat grounding, one cohesive button system, equal bounding edges, browser-based visual QA.
   - Prohibitions: No generic purple/violet palettes, no random scroll-fades on every row, no autoplay carousels.
3. **Emil Kowalski Motion (`.agents/skills/emil-design-eng`):**
   - Authoritative, purposeful motion system.
   - Custom bezier curves: `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`, no sluggish ease-in, UI transitions under 300ms, `:active` button press feedback (`scale(0.972)`), entry transitions start at `scale(0.985)` (never `scale(0)`).
   - Strict `prefers-reduced-motion` fallbacks (preserve opacity/color shifts, disable position displacement).

---

## C. Current Implementation Status

### Status Overview
- **Tracked Codebase:** Modified in working tree (`index.html`, `app.py`). Not committed, staged, or pushed.
- **Baseline Fallback:** Commit `fbe9bdb`.
- **Untracked Working Tree Assets & Documents:** Existing untracked files are intentionally preserved and must never be deleted, staged, or committed automatically.
- **Phase 1: Initial Polish & Accessibility Pass:** **COMPLETED & COMMITTED** (`fbe9bdb`).
- **Phase 2: Creative Overhaul Implementation:** **COMPLETED IN WORKING TREE & VISUALLY VERIFIED**.
  - **Task 1 (Homepage & Branding):** Bespoke Astha-Dala compass-star vector SVG emblem, two-line wordmark, refined sticky header, atmospheric exhibition entrance hero with catalogue badge, 3-column folio story cards with photo hover zoom, 5-column responsive regional atlas with match counter, and rich colophon footer.
  - **Task 2 (Curated Story Reader Overhaul):** Multi-part editorial layout with reading progress bar, dramatic masthead, dynamic metadata ribbon with story-specific Provenance and Archival Classification, Primary Archival Plate I (16:9 museum framing with dark lacquer caption and gold typography), 76px drop-caps, typographic exhibition pull quotes, Secondary Contextual Archival Plates matching Plate I museum styling, formal Curatorial Field Memorandum boxes with diamond star insignia, source bibliography dossiers, and reader navigation controls (Prev / Next / Return).
  - **Task 3 (Regional Chapter & Dish Browser):** Harmonized `STATE_PAGE_EXTENSION` in `app.py` with the overhaul tokens, upgraded brand mark, refined floating back pill, 2-dish tab selectors with tactile active states, museum dish photo framing, polished curatorial research desiderata cards (`border-left: 3px solid var(--sp-gold)`), and styled historical / oral narrative blocks.
  - **Task 4 (Emil Kowalski Motion Integration):** Tokenized easings, active button scale feedback (`scale(0.972)`), card lift micro-interactions, smooth entry fades, and complete reduced-motion fallbacks.
  - **Task 5 (Visual QA Suite):** Comprehensive screenshot suite in `artifacts/design-review/creative-overhaul/` covering all devices and deep-links.
  - **Task 6 (Curatorial Rigour Pass):** Dynamically populated story Provenance and Archival Classification for each monograph, verifying geographic accuracy across all 6 stories (e.g. Rasgulla = Eastern India, Confectionery & Ritual Traditions).

---

## D. Exact File Changes & Untracked Inventory

| Path | Git Status | Nature & Purpose | Remaining Work |
|---|---|---|---|
| `PROJECT_HANDOFF.md` | Untracked | Single source of truth for all project context, decisions, status, and continuation instructions. | Keep continuously updated. |
| `artifacts/handoff/SESSION_LOG.md` | Untracked | Chronological audit trail of milestones, actions, tests, and handoffs across sessions. | Keep updated. |
| `index.html` | Modified (`+1679 / -680`) | Complete creative overhaul of homepage, branding, typography, stories collection, multi-image editorial story reader, footer restructuring, and responsive refinements. | Complete in working tree for review. |
| `app.py` | Modified (`+247 / -187`) | Upgraded `STATE_PAGE_EXTENSION` regional chapters, emblem SVG, floating back pill, historical research notes, and dish browser experience. | Complete in working tree for review. |
| `state_pages.json` | Tracked (Clean at `fbe9bdb`) | Contains 36 regional entries and 72 dish records. | **STRICTLY PRESERVED.** No edits made. |
| `checkpoint_backup/app.py.bak` | Untracked | Emergency fallback backup created before previous polish pass. | Strictly preserve. |
| `checkpoint_backup/index.html.bak` | Untracked | Emergency fallback backup created before previous polish pass. | Strictly preserve. |
| `artifacts/design-review/` | Untracked | Viewport review screenshots of baseline commit `fbe9bdb`. | Retain as reference. |
| `artifacts/design-review/creative-overhaul/` | Untracked | Viewport & interaction review screenshots of creative overhaul (`mobile-story-reader-latest.png`, `session2-story-rasgulla-masthead.png`, `session2-story-rasgulla-v2.png`, `desktop-1440-latest.png`, `session2-story-vada-pav-v2.png`, `session2-region-kerala-v2.png`, etc.). | Complete visual audit suite. |
| `artifacts/scratch/extracted.js` | Untracked | Extracted frontend JavaScript used for syntax verification (`node --check`). | Preserve as scratch artifact. |
| `artifacts/scratch/qa_render.py` | Untracked | Dev-only helper that resolves the five template markers into `artifacts/scratch/qa-index.html` for the static taste-skill checkers. Not part of the app. | Preserve as scratch tooling. |
| `artifacts/scratch/qa-index.html` | Untracked | Marker-resolved render of `index.html` consumed by `consistency.mjs` and `shoot.mjs`. | Regenerate after any `index.html` edit. |
| `artifacts/design-review/creative-overhaul/consistency-r2..r5/` | Untracked | Successive re-audit runs (report.json + crops) after the responsive/story-grid fixes. | Retain as audit trail. |
| `artifacts/design-review/creative-overhaul/final-shots/` | Untracked | Final full-page browser screenshots at 1440/1024/768/390 (from `shoot.mjs`). | Retain as verification evidence. |
| `.taste-skill/` | Untracked | Chrome profile folders created by the taste-skill screenshot/audit scripts. | Disposable; safe to ignore. |

---

## E. Design Decisions Implemented

### 1. Palette & Atmosphere
- **Museum Palette:** Charcoal-Maroon (`--maroon-deep: #150605;`, `--maroon: #230b08;`, `--maroon-mid: #381410;`), Saffron Terracotta (`--terracotta: #843422;`, `--saffron-ink: #a34d28;`), Deep Ink (`--ink: #241512;`, `--ink-mid: #422922;`), Warm Archival Parchment (`--paper: #f4ede0;`, `--paper-card: #fcf8f1;`, `--paper-warm: #eee4d2;`), Antique Brass Gold (`--gold: #b89251;`, `--gold-light: #d9b679;`, `--gold-pale: #edd8b2;`).

### 2. Typography
- **Primary Display:** *Cormorant Garamond* (400, 500, 600, 700 + true italics) with tight optical tracking (`-0.02em` to `-0.03em`) and balanced text wrap.
- **Editorial Body:** *Libre Baskerville* (400, 400i, 700) with generous measure (65–75ch) and line height 1.7–2.0.
- **Classification Badges:** Letter-spaced small caps serifs with ornamental brackets.

### 3. Emblem & Iconography
- Bespoke vector SVG emblem: An eight-pointed Astha-Dala star / cartographic compass mandala inscribed inside concentric brass rings with cardinal tick marks.
- Crisp vector SVG icons for navigation hamburger, search, and directional arrows. Zero emoji.

### 4. Story Reader Overhaul Architecture
- Dynamic Reading Progress Bar tracking vertical scroll depth.
- Archival Masthead with Folio Number (`FOLIO · 01`), Classification (`RESEARCHED ESSAY`), Provenance, and Reading Time.
- Primary Photographic Plate I with 16:9 aspect-ratio, dark lacquer caption frame, and gold typography.
- Curated multi-part editorial sections with thematic headings (`§ I. The Social Fabric of the Food`, `§ II. Origins, Technique & Adaptation`, `§ III. Cultural Memory & Contemporary Significance`) with hairline divider rules and 76px drop-caps.
- Typographic Exhibition Pull Quotes with warm brass quotation marks (`\201C`).
- Secondary Contextual Archival Plates (single and dual comparative plates) sharing the same museum plate framing.
- Curatorial Field Memorandum box styled as an archival research record with diamond star insignia (`\2726`).
- Academic Source Dossier with publication metadata.
- Bottom Reader Navigation with Prev / Next Story and Return controls.
- Tactile floating back pill with keyboard shortcut hint (`Esc`).

### 5. Motion System (Emil Kowalski Framework)
- Custom bezier easing: `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`.
- Active press feedback: `transform: scale(0.972)` on buttons, cards, dish selectors, and floating pills.
- Image hover: subtle scale (`scale(1.035)`) inside masked overflow.
- Entry transition: subtle scale-fade (`scale(0.985)` to `scale(1)` over 240ms).
- Full reduced-motion suppression under `@media (prefers-reduced-motion: reduce)`.

---

## F. Completed Tasks

- [x] Corrected `PROJECT_HANDOFF.md` and `SESSION_LOG.md` to reflect exact working tree state, project-relative paths, and untracked inventory preservation.
- [x] Task 1: Complete creative overhaul of `index.html` (Header, Astha-Dala emblem, typography, hero composition, 3-column folio story cards, 5-column regional atlas, match counter, and footer).
- [x] Task 2: Story Reader Multi-Image Archival Redesign in `index.html` (Progress bar, masthead, Primary Plate I, drop-caps, pull quotes, Secondary Contextual Plates from `STATE_IMAGES`, Curatorial Memorandum, Source Dossier, Prev/Next navigation).
- [x] Task 3: Creative overhaul of Regional Chapter & Dish Browser in `app.py` (`STATE_PAGE_EXTENSION` styles, emblem SVG, floating back pill, 2-dish tab selectors, photo framing, historical/oral narrative blocks).
- [x] Task 4: Motion System Integration (Emil Kowalski physical motion tokens, active scale feedback, smooth transitions, reduced-motion fallbacks).
- [x] Task 5: QA & Verification Suite across Desktop (1440), Laptop (1024), Tablet (768), and Mobile (390), plus full story reader and regional chapter captures in `artifacts/design-review/creative-overhaul/`.
- [x] Task 6: Visual refinement pass on story reader plates (16:9 framing, dark lacquer captions, 76px drop-cap, section dividers) and regional chapter research desiderata card.
- [x] Task 7: Curatorial metadata wiring (dynamic Provenance and Archival Classification across all 6 stories; mobile QA verification).
- [x] Task 8: Story Reader Typographic & Caption Harmonization Pass:
  - Resolved pull quote pseudo-element background color mismatch (`--paper` on `--paper-card`), harmonizing container and quotation mark to `var(--paper-warm)`.
  - Harmonized Secondary Contextual Plate II caption structure with Plate I: itemized captions on left (`.context-plate-desc-line`) paired with an `ARCHIVAL PLATE II` gold small-caps badge on the right, eliminating duplicate plate headers.
  - Expanded `.story-page-content` measure to 980px.
  - Added responsive scaling for the opening drop-cap to 58px on mobile (≤720px).
  - Increased `.story-visual` height to 224px for enhanced photographic weight.
- [x] Task 8.5: Handoff-Resume Verification & Responsive Correction Pass (see SESSION_LOG 2026-11-09 04:00–05:40):
  - **Footer restructuring verified:** `.footer-panorama` was already fully replaced by `.site-footer::after` (with the functional `{{FOOTER_IMAGE}}` marker) and `.footer-sub` moved into `.footer-colophon` as `.footer-legal`. Markup and styles match; no stale classes; no content lost.
  - **Responsive story-grid regression fixed:** at ≤880px the outer `.story-grid` now drives a 2-column layout and `.story-row` becomes `display: contents` so the six folio cards reflow evenly (a 3-card row could not halve into two columns without stranding a card). The ≤440px override was corrected from the inert `.story-row` to `.story-grid` (single column).
  - **Dead CSS removed:** the `@media (max-width: 1100px)` block that only re-declared base `.story-row` / `.state-grid` values was deleted.
  - **Mobile tap-target fix:** `.brand` gains `min-height: 44px` at ≤400px (the shrunk 36px emblem had dropped the brand link below the 44px mobile minimum).
  - **Verification:** QA render regenerated (all 5 markers resolve), `py_compile app.py` PASS, JS `node --check` PASS, and `consistency.mjs` re-run four times (r2→r5: 50→46→43→43 FAIL, 28→28→28→26 WARN). `row-gap`, `hole`, `cut-text`, `overlap-text`, `no-visual`, and `tap-size` now PASS.
  - **Final screenshots:** `artifacts/design-review/creative-overhaul/final-shots/{1440,1024,768,390}.png`.

---

## G. Remaining Tasks

### Task 9: Owner Inspection & Creative Feedback Review
- **Objective:** Present the experimental creative overhaul to the repository owner with complete screenshot evidence and architectural explanations.
- **Files:** `index.html`, `app.py`, `PROJECT_HANDOFF.md`
- **Dependencies:** Complete.
- **Testing:** Inspect working tree review screenshots.
- **Guard:** Await explicit owner instructions before committing or staging any changes.

---

## H. Current Stopping Point & Immediate Next Action

- **Last Completed Action:** Handoff-resume verification + responsive correction pass (2026-11-09 04:00–05:40). Confirmed the footer restructuring was already fully applied (`.site-footer::after` + `.footer-colophon .footer-legal`, `{{FOOTER_IMAGE}}` functional, no stale classes). Fixed the responsive `.story-grid`/`.story-row` regression at ≤880px and ≤440px, removed a dead `@media (max-width: 1100px)` block, and added a 44px mobile tap target to `.brand` at ≤400px.
- **Current Action:** All checks re-run and final screenshots captured. Working tree remains uncommitted at baseline `fbe9bdb`.
- **Exact Point Where Implementation Stopped:** Implementation, visual polish, responsive/correction pass, verification, and documentation fully complete in the working tree. No new work in progress.
- **Running Processes:** Streamlit server running on port 8501 (PID **21868**), responding HTTP 200. Do not start a second instance.
- **Errors/Warnings:** None blocking. `py_compile app.py` PASS (exit 0); JS `node --check` PASS (exit 0). `consistency.mjs` reports 43 FAIL / 26 WARN — all FAILs are the taste-skill structural conventions (SR-2 fixed 1–2-screen sections, SR-4 one-section-per-screen, SR-6 exact container/`.hero-text` naming + `.skip-link` bypass-link, SR-8 split lines). These conflict with the deliberate editorial scroll design and were intentionally not chased (per the user's instruction not to damage the design to satisfy checker rules).
- **EXACT INSTRUCTION FOR RESUMING MODEL:**
  1. Inspect this `PROJECT_HANDOFF.md` and `artifacts/handoff/SESSION_LOG.md`, then check `git status`.
  2. `index.html` and `app.py` are modified in the working tree and complete; all untracked files/artifacts are preserved.
  3. To re-verify: regenerate the QA render (`.\.venv\Scripts\python.exe artifacts\scratch\qa_render.py`), run `node --check` on the extracted script, re-run `consistency.mjs`, and re-shoot with `shoot.mjs`. Do **not** restart the running server.
  4. Await owner review; do not stage, commit, push, or deploy without explicit instruction.

---

## I. Testing and Verification Log

- **Python Compilation:** `.\.venv\Scripts\python.exe -m py_compile app.py` → **PASSED** (Exit 0).
- **JavaScript Syntax:** largest `<script>` extracted from the QA render (`artifacts/scratch/extracted.js`, 34,332 bytes) → `node --check` **PASSED** (Exit 0).
- **QA Render:** `.\.venv\Scripts\python.exe artifacts\scratch\qa_render.py` → wrote `artifacts/scratch/qa-index.html`; `remaining markers: []`.
- **Design Audit (`consistency.mjs`, 1440/1024/768/390, `--page place`):**
  - r2: 50 FAIL / 28 WARN · r3: 46 FAIL / 28 WARN · r4: 43 FAIL / 26 WARN · r5: **43 FAIL / 26 WARN**.
  - Resolved to PASS by the fixes: `row-gap`, `hole`, `cut-text`, `overlap-text`, `no-visual`, `tap-size`.
  - Remaining FAILs are the SR-2/SR-4/SR-6/SR-8 structural conventions (fixed-height sections, one-section-per-screen, exact container/`.hero-text` naming, split lines) — intentionally accepted as design conflicts, not defects.
- **Template Markers Verification:**
  - `{{HERO_IMAGE}}`: **Present** (`index.html:286`) and resolves
  - `{{FOOTER_IMAGE}}`: **Present** (`index.html:906`, inside `.site-footer::after`) and resolves
  - `{{STORY_IMAGES}}`: **Present** (`index.html:1872`) and resolves
  - `{{STATE_IMAGES}}`: **Present** (`index.html:1873`) and resolves
  - `{{REGION_TYPES}}`: **Present** (`index.html:1874`) and resolves
- **Asset Integrity:** 36 regional images, 72 dish images, 6 story images → **100% Present**.
- **Final Viewport Screenshots (`artifacts/design-review/creative-overhaul/final-shots/`):**
  - `1440.png` (5.1 MB, 1440×3409, 4 screens) · `1024.png` (3.5 MB, 1024×3325, 5 screens) · `768.png` (3.9 MB, 768×4540, 5 screens) · `390.png` (2.3 MB, 390×5520, 7 screens).
- **Historical Overhaul Screenshots (`artifacts/design-review/creative-overhaul/`):**
  - `session6-story-vada-pav-refined.png` (1.81 MB) — Verified seamless pull quote background, aligned margins, and harmonized Plate II caption.
  - `session6-story-rasgulla-refined.png` (1.89 MB) — Verified dual comparative plates (Puri & Kolkata) with itemized captions and right-aligned `ARCHIVAL PLATE II` badge.
  - `session6-mobile-390.png` (408 KB) — Mobile viewport at 390×844 with stroke hamburger and museum entrance.
  - `session6-desktop-1440.png` (1.56 MB) — Full hero and header at 1440×900.
  - `session2-region-kerala-v2.png` (1.28 MB) — Refined Kerala regional chapter with gold-bordered archival research note card.
  - `mobile-story-reader-latest.png` (256 KB) — Mobile view of curated story reader with dynamic provenance and 16:9 plate.
  - `session2-story-rasgulla-masthead.png` (1.10 MB) — Verified dynamic masthead metadata.
  - `desktop-overview-1800.png` (3.19 MB) — Full view of hero and 6 curated story folios.
  - `laptop-1024.png` (1.00 MB) — Laptop viewport at 1024×768.
  - `tablet-768.png` (1.08 MB) — Tablet viewport at 768×1024.

---

## J. Git and Recovery Information

- **Current Branch:** `main` (synchronized with `origin/main`).
- **Baseline Commit SHA:** `fbe9bdb` ("Polish: design token system, typography, responsive layout, accessibility").
- **Tracked Files Status:** `app.py` and `index.html` are modified in the working tree.
- **Untracked Inventory:** `PROJECT_HANDOFF.md`, `artifacts/handoff/SESSION_LOG.md`, `checkpoint_backup/app.py.bak`, `checkpoint_backup/index.html.bak`, `artifacts/design-review/` (incl. `creative-overhaul/consistency/`, `consistency-r2..r5/`, `final-shots/`, session screenshots), `artifacts/scratch/` (`extracted.js`, `qa_render.py`, `qa-index.html`), and `.taste-skill/` (disposable Chrome profiles). All untracked files are intentionally kept and preserved.
- **Experimental Safety:** No code changes have been staged, committed, pushed, or deployed. Commit `fbe9bdb` remains the baseline recovery point.
- **Safety Precaution:** Never run `git reset --hard` or `git clean`. Do not overwrite or delete checkpoint backups or review screenshots.
