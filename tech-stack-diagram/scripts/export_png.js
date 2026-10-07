#!/usr/bin/env node
// Export an SVG to a crisp PNG with headless Chrome (puppeteer).
//   NODE_PATH="$(npm root -g)" node export_png.js diagram.svg diagram.png [scale=2]
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
(async () => {
  const [svgPath, pngPath, scale = '2'] = process.argv.slice(2);
  if (!svgPath || !pngPath) { console.error('usage: export_png.js in.svg out.png [scale]'); process.exit(2); }
  const svg = fs.readFileSync(svgPath, 'utf8');
  const w = +svg.match(/width="(\d+(?:\.\d+)?)"/)[1];
  const h = +svg.match(/height="(\d+(?:\.\d+)?)"/)[1];
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: Math.ceil(w), height: Math.ceil(h), deviceScaleFactor: +scale });
  await page.goto('file://' + path.resolve(svgPath));
  await page.screenshot({ path: pngPath });
  await browser.close();
  console.log(`wrote ${pngPath} (${Math.ceil(w * scale)}×${Math.ceil(h * scale)})`);
})();
