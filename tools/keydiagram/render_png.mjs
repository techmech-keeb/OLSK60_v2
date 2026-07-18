#!/usr/bin/env node
// SVG -> PNG (2x) レンダラ。
// SVG を HTML にインライン展開し、fonts/ のローカル Noto Sans JP ウェブフォントを
// @font-face で適用して Playwright(Chromium) でスクリーンショットを撮る。
// ヘッドレス Chromium の --window-size 直接指定はビューポートが欠けるため使わない。
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

// playwright はローカル node_modules → グローバル (npm root -g) の順で解決する
function loadPlaywright() {
  const req = createRequire(import.meta.url);
  try {
    return req('playwright');
  } catch {
    const globalRoot = execSync('npm root -g', { encoding: 'utf8' }).trim();
    return createRequire(join(globalRoot, 'x.js'))('playwright');
  }
}
const { chromium } = loadPlaywright();

const HERE = dirname(fileURLToPath(import.meta.url));
const [svgPath, pngPath] = process.argv.slice(2);
if (!svgPath || !pngPath) {
  console.error('usage: node render_png.mjs <in.svg> <out.png>');
  process.exit(1);
}

const svg = readFileSync(svgPath, 'utf8');
const m = svg.match(/<svg[^>]*\bwidth="(\d+)"[^>]*\bheight="(\d+)"/);
if (!m) throw new Error('SVG width/height not found');
const [width, height] = [Number(m[1]), Number(m[2])];

const fontDir = join(HERE, 'fonts');
let css = '';
try {
  css = readFileSync(join(fontDir, 'notosansjp.local.css'), 'utf8')
    .replaceAll('url(woff2/', `url(${pathToFileURL(join(fontDir, 'woff2'))}/`);
} catch {
  console.error('warning: fonts/ not found — run fetch_fonts.py first; falling back to system fonts');
}

const html = `<!doctype html><meta charset="utf-8"><style>${css}
html,body{margin:0;padding:0;background:#fff}</style>${svg}`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 2 });
await page.setContent(html, { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: pngPath });
await browser.close();
console.log(`rendered ${pngPath} (${width * 2}x${height * 2})`);
