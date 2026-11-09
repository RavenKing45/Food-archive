#!/usr/bin/env node
/*
  Dev-only check: build a QA harness that includes the state-page module (appended
  by app.py, which qa_render.py does not do), then load the first / middle / last
  regional archive pages in headless Chrome and verify the new regional navigation.
  Reuses the raw CDP approach of the taste-skill shoot.mjs (no puppeteer needed).
*/
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import http from 'node:http';
import { spawn, execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const SCRATCH = path.join(ROOT, 'artifacts', 'scratch');
const QA_INDEX = path.join(SCRATCH, 'qa-index.html');
const QA_REGIONS = path.join(SCRATCH, 'qa-regions.html');
const PREFIX = '../../assets';
if (!fs.existsSync(QA_INDEX)) { console.error('run qa_render.py first'); process.exit(1); }

// ── Build qa-regions.html = qa-index.html + the state-page extension from app.py ──
const appSrc = fs.readFileSync(path.join(ROOT, 'app.py'), 'utf8');
const openTag = 'STATE_PAGE_EXTENSION = r"""';
const o = appSrc.indexOf(openTag);
const c = appSrc.indexOf('"""', o + openTag.length);
if (o < 0 || c < 0) { console.error('could not extract STATE_PAGE_EXTENSION'); process.exit(1); }
let ext = appSrc.slice(o + openTag.length, c);

const statePages = JSON.parse(fs.readFileSync(path.join(ROOT, 'state_pages.json'), 'utf8'));
const dishImages = {};
for (const f of fs.readdirSync(path.join(ROOT, 'assets', 'dishes'))) {
  const m = /^(.*)\.(jpe?g|png|webp|avif)$/i.exec(f);
  if (m) dishImages[m[1].toLowerCase()] = `${PREFIX}/dishes/${f}`;
}
ext = ext.replace('__STATE_PAGES__', JSON.stringify(statePages)).replace('__DISH_IMAGES__', JSON.stringify(dishImages));
let html = fs.readFileSync(QA_INDEX, 'utf8');
html = html.replace('</body>', ext + '\n</body>');
fs.writeFileSync(QA_REGIONS, html, 'utf8');
console.log(`wrote ${QA_REGIONS} (regions in dataset: ${Object.keys(statePages).length})`);

const CASES = [
  { label: 'first', slug: 'andhra-pradesh', expectPrev: false, expectNext: true, nextSlug: 'arunachal-pradesh', nextName: 'Arunachal Pradesh' },
  { label: 'middle', slug: 'odisha', expectPrev: true, expectNext: true, prevSlug: 'nagaland', prevName: 'Nagaland', nextSlug: 'punjab', nextName: 'Punjab' },
  { label: 'last', slug: 'puducherry', expectPrev: true, expectNext: false, prevSlug: 'lakshadweep', prevName: 'Lakshadweep' },
];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.avif': 'image/avif', '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  try {
    let f = path.resolve(path.join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname)));
    if (f !== ROOT && !f.startsWith(ROOT + path.sep)) { res.writeHead(403); return res.end(); }
    if (fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
    res.writeHead(200, { 'content-type': MIME[path.extname(f).toLowerCase()] || 'application/octet-stream', 'content-length': fs.statSync(f).size, 'cache-control': 'no-store' });
    fs.createReadStream(f).pipe(res);
  } catch { res.writeHead(404); res.end('not found'); }
});
const port = await new Promise((res) => { server.listen(0, '127.0.0.1', () => res(server.address().port)); });
const base = `http://127.0.0.1:${port}/artifacts/scratch/qa-regions.html`;

function findChrome() {
  const local = process.env.LOCALAPPDATA ? path.join(process.env.LOCALAPPDATA, 'Google/Chrome/Application/chrome.exe') : null;
  const c = [process.env.CHROME_PATH, 'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', local,
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium'];
  const f = c.find((p) => p && fs.existsSync(p));
  if (!f) throw new Error('no Chrome found (set CHROME_PATH)');
  return f;
}
const profile = path.join(os.tmpdir(), 'state-verify-' + process.pid);
fs.mkdirSync(profile, { recursive: true });
const portFile = path.join(profile, 'DevToolsActivePort');
try { fs.rmSync(portFile); } catch { /* none */ }
const child = spawn(findChrome(), ['--headless=new', `--user-data-dir=${profile}`, '--remote-debugging-port=0', '--no-first-run',
  '--no-default-browser-check', '--disable-extensions', '--hide-scrollbars', '--mute-audio', '--disable-gpu',
  '--window-size=1440,900', 'about:blank'], { stdio: 'ignore', windowsHide: true });
const kill = () => { if (child.exitCode != null) return; try { execFileSync('taskkill', ['/PID', String(child.pid), '/T', '/F'], { stdio: 'ignore' }); } catch { try { child.kill(); } catch { /* gone */ } } };

const PROBE = `(() => {
  const root = document.getElementById('archive-state-page');
  const out = { display: root ? root.style.display : null, h1: null, buttons: [], scrollY: Math.round(window.scrollY), statesTop: null, statesViewTop: null, hash: location.hash };
  const states = document.getElementById('states');
  if (states) { const r = states.getBoundingClientRect(); out.statesTop = Math.round(r.top + (window.pageYOffset || 0)); out.statesViewTop = Math.round(r.top); }
  if (root && root.style.display === 'block') {
    const h1 = root.querySelector('.state-masthead h1'); out.h1 = h1 ? h1.textContent.trim() : null;
    root.querySelectorAll('[data-region-nav]').forEach((b) => out.buttons.push({ dir: b.dataset.regionNav, visible: getComputedStyle(b).visibility !== 'hidden', text: b.textContent.trim() }));
  }
  return JSON.stringify(out);
})()`;

let failure = 0;
try {
  let wsPort = null;
  for (let i = 0; i < 150 && !wsPort; i++) { await sleep(100); try { wsPort = parseInt(fs.readFileSync(portFile, 'utf8'), 10) || null; } catch { /* not yet */ } }
  if (!wsPort) throw new Error('Chrome did not start');
  const ver = await (await fetch(`http://127.0.0.1:${wsPort}/json/version`)).json();
  const ws = new WebSocket(ver.webSocketDebuggerUrl);
  await new Promise((r, j) => { ws.addEventListener('open', r, { once: true }); ws.addEventListener('error', j, { once: true }); });
  let id = 0; const pend = new Map(); const subs = []; const logs = [];
  ws.addEventListener('message', (e) => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } else subs.forEach((f) => f(m)); });
  const send = (method, params = {}, sessionId) => new Promise((r) => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params, sessionId })); });
  const { result: { targetId } } = await send('Target.createTarget', { url: 'about:blank' });
  const { result: { sessionId } } = await send('Target.attachToTarget', { targetId, flatten: true });
  const S = async (m, p) => { const r = await send(m, p, sessionId); if (r.error) throw new Error(`${m}: ${r.error.message}`); return r.result; };
  const ev = async (x) => (await S('Runtime.evaluate', { expression: x, awaitPromise: true, returnByValue: true })).result.value;
  subs.push((m) => { if (m.method === 'Runtime.exceptionThrown') logs.push((m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text || '').split('\n')[0]); });
  await S('Page.enable'); await S('Runtime.enable');

  let navN = 0;
  for (const t of CASES) {
    // A unique query token forces a genuine document load: identical query strings
    // with only a differing hash are same-document and would not re-run the
    // initial-region hash check.
    const openCase = async () => { await S('Page.navigate', { url: base + '?r=' + encodeURIComponent(t.slug) + '&n=' + (++navN) + '#region/' + t.slug }); await sleep(1400); return JSON.parse(await ev(PROBE)); };

    await S('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
    const st = await openCase();
    console.log(`\n=== ${t.label}: #region/${t.slug} ===`);
    console.log(`  state page display=${st.display}  heading="${st.h1}"  hash=${st.hash}`);
    const prev = st.buttons.find((b) => b.dir === 'prev');
    const next = st.buttons.find((b) => b.dir === 'next');
    const cat = st.buttons.find((b) => b.dir === 'catalogue');
    console.log(`  buttons: prev=${prev ? prev.visible : 'MISSING'}("${prev ? prev.text : ''}")  catalogue=${cat ? cat.visible : 'MISSING'}("${cat ? cat.text : ''}")  next=${next ? next.visible : 'MISSING'}("${next ? next.text : ''}")`);
    if (st.display !== 'block' || !st.h1) { console.log('  !! region page did not open'); failure++; }
    if (!prev || prev.visible !== t.expectPrev) { console.log(`  !! prev visible=${prev && prev.visible}, expected ${t.expectPrev}`); failure++; }
    if (!next || next.visible !== t.expectNext) { console.log(`  !! next visible=${next && next.visible}, expected ${t.expectNext}`); failure++; }
    if (!cat || !cat.visible) { console.log('  !! catalogue button not visible'); failure++; }

    // Next navigation (first/middle only)
    if (t.nextSlug) {
      await ev(`document.querySelector('[data-region-nav="next"]').click()`);
      await sleep(600);
      const nx = JSON.parse(await ev(PROBE));
      console.log(`  after Next → hash=${nx.hash} heading="${nx.h1}"`);
      if (nx.hash !== '#region/' + t.nextSlug || nx.h1 !== t.nextName) { console.log(`  !! Next did not open ${t.nextSlug} (${t.nextName})`); failure++; }
    }

    // Previous navigation (middle/last only) — reload the case first.
    if (t.prevSlug) {
      await openCase();
      await ev(`document.querySelector('[data-region-nav="prev"]').click()`);
      await sleep(600);
      const pv = JSON.parse(await ev(PROBE));
      console.log(`  after Prev → hash=${pv.hash} heading="${pv.h1}"`);
      if (pv.hash !== '#region/' + t.prevSlug || pv.h1 !== t.prevName) { console.log(`  !! Prev did not open ${t.prevSlug} (${t.prevName})`); failure++; }
    }

    // Return to Regional Catalogue: closes and lands on the atlas — reload the case first.
    // The scroll helper subtracts #states' 30px scroll-margin-top, so the section
    // settles just below the viewport top (statesViewTop ~= 30).
    await openCase();
    await ev(`document.querySelector('[data-region-nav="catalogue"]').click()`);
    await sleep(700);
    const after = JSON.parse(await ev(PROBE));
    const nearAtlas = after.display !== 'block' && after.statesViewTop != null && after.statesViewTop > -60 && after.statesViewTop < 200;
    console.log(`  after Return to Catalogue → statePage display=${after.display}  #states viewTop=${after.statesViewTop}  hash=${after.hash}  landedOnAtlas=${nearAtlas}`);
    if (after.display === 'block') { console.log('  !! catalogue button did not close the region page'); failure++; }
    if (!nearAtlas) { console.log(`  !! did not settle on the regional catalogue (#states viewTop ${after.statesViewTop})`); failure++; }
  }
  if (logs.length) console.log('\nconsole errors:', logs.slice(0, 8).join(' | '));
  console.log('\n' + (failure ? `FAILURES: ${failure}` : 'ALL CHECKS PASSED'));
} catch (e) {
  console.error('verify:', e.message);
  process.exitCode = 1;
} finally {
  try { await sleep(200); } catch { /* */ }
  kill();
  server.close();
}
