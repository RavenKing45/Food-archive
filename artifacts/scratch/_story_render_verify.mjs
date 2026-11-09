#!/usr/bin/env node
/*
  Dev-only check: load each of the six story pages from the QA render in a headless
  Chrome and report (a) the banner/hero image at the top and (b) every contextual
  photograph placed in the vertical reading flow, in DOM order, with its section.
  Reuses the raw CDP approach of the taste-skill shoot.mjs (no puppeteer needed).
*/
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import http from 'node:http';
import { spawn, execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const PAGE_REL = 'artifacts/scratch/qa-index.html';
if (!fs.existsSync(path.join(ROOT, PAGE_REL))) {
  console.error('missing ' + PAGE_REL + ' (run qa_render.py first)');
  process.exit(1);
}
const SLUGS = [
  'vada-pav-mumbai-commuter-food',
  'rasgulla-two-regional-traditions',
  'dal-baati-food-for-the-road',
  'masala-dosa-udupi-network',
  'chole-bhature-post-partition-delhi',
  'daulat-ki-chaat-delhi-winter',
];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.avif': 'image/avif', '.gif': 'image/gif', '.ico': 'image/x-icon' };

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
const base = `http://127.0.0.1:${port}/${PAGE_REL.split(path.sep).join('/')}`;

function findChrome() {
  const local = process.env.LOCALAPPDATA ? path.join(process.env.LOCALAPPDATA, 'Google/Chrome/Application/chrome.exe') : null;
  const c = [process.env.CHROME_PATH, 'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', local,
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium'];
  const f = c.find((p) => p && fs.existsSync(p));
  if (!f) throw new Error('no Chrome found (set CHROME_PATH)');
  return f;
}

const profile = path.join(os.tmpdir(), 'story-verify-' + process.pid);
fs.mkdirSync(profile, { recursive: true });
const portFile = path.join(profile, 'DevToolsActivePort');
try { fs.rmSync(portFile); } catch { /* none */ }
const child = spawn(findChrome(), ['--headless=new', `--user-data-dir=${profile}`, '--remote-debugging-port=0', '--no-first-run',
  '--no-default-browser-check', '--disable-extensions', '--hide-scrollbars', '--mute-audio', '--disable-gpu',
  '--window-size=1440,900', 'about:blank'], { stdio: 'ignore', windowsHide: true });
const kill = () => { if (child.exitCode != null) return; try { execFileSync('taskkill', ['/PID', String(child.pid), '/T', '/F'], { stdio: 'ignore' }); } catch { try { child.kill(); } catch { /* gone */ } } };

const PROBE = `(() => {
  const clean = (s) => (s || '').split('/').pop();
  const out = { hero: null, images: [], paired: 0 };
  const heroImg = document.getElementById('story-page-image');
  const heroWrap = document.getElementById('story-page-image-wrap');
  if (heroImg) out.hero = { file: clean(heroImg.getAttribute('src')), loaded: heroImg.naturalWidth > 0, hidden: !!(heroWrap && heroWrap.hidden) };
  const root = document.getElementById('story-editorial-sections');
  let heading = '';
  if (root) {
    for (const el of root.children) {
      if (el.classList.contains('story-editorial-section')) { const h = el.querySelector('h2'); if (h) heading = h.textContent.trim(); }
      else if (el.classList.contains('story-content-image-slot')) {
        const img = el.querySelector('img');
        const r = el.getBoundingClientRect();
        out.images.push({ slot: el.getAttribute('data-image-slot'), file: img ? clean(img.getAttribute('src')) : null, loaded: img ? img.naturalWidth > 0 : false, w: Math.round(r.width), h: Math.round(r.height), heading });
      }
    }
  }
  const boxes = out.images.map((s) => document.getElementById(s.slot)).filter(Boolean).map((e) => e.getBoundingClientRect());
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    const ov = Math.min(boxes[i].bottom, boxes[j].bottom) - Math.max(boxes[i].top, boxes[j].top);
    const ox = Math.min(boxes[i].right, boxes[j].right) - Math.max(boxes[i].left, boxes[j].left);
    if (ov > 20 && ox > 20) out.paired++;
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

  for (const slug of SLUGS) {
    await S('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
    // a distinct query forces a full load; a hash-only change is same-document and
    // would leave the previously opened story on screen.
    await S('Page.navigate', { url: base + '?s=' + encodeURIComponent(slug) + '#story/' + slug });
    await sleep(1800);
    // walk the page so lazy images load, then return to the top
    await ev(`(async () => { const H = document.scrollingElement.scrollHeight; for (let y = 0; y <= H; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); return 1; })()`);
    await sleep(900);
    const desktop = JSON.parse(await ev(PROBE));
    await S('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
    await sleep(500);
    await ev(`(async () => { const H = document.scrollingElement.scrollHeight; for (let y = 0; y <= H; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } scrollTo(0, 0); return 1; })()`);
    await sleep(700);
    const mobile = JSON.parse(await ev(PROBE));
    console.log('\n=== ' + slug + ' ===');
    console.log(`  banner@1440: ${desktop.hero ? desktop.hero.file + '  loaded=' + desktop.hero.loaded + ' hidden=' + desktop.hero.hidden : 'NONE'}`);
    console.log(`  banner@390 : ${mobile.hero ? mobile.hero.file + '  loaded=' + mobile.hero.loaded + ' hidden=' + mobile.hero.hidden : 'NONE'}`);
    const dump = (view) => {
      console.log(`  contextual photos @${view} (${desktop === mobile ? '' : ''}${view}): ${view === '1440' ? desktop.images.length : mobile.images.length}`);
      for (const im of (view === '1440' ? desktop.images : mobile.images)) {
        console.log(`    [${im.loaded ? 'ok' : 'NOT LOADED'}] ${im.file}  (${im.w}x${im.h})  after: ${im.heading}`);
      }
    };
    dump('1440'); dump('390');
    console.log(`  side-by-side pairs: 1440=${desktop.paired} 390=${mobile.paired}`);
    if (!desktop.hero || !desktop.hero.loaded || desktop.hero.hidden) { console.log('  !! banner problem'); failure++; }
    if (desktop.paired || mobile.paired) { console.log('  !! images paired side by side'); failure++; }
    for (const im of desktop.images) if (!im.loaded) { console.log('  !! not loaded: ' + im.file); failure++; }
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
