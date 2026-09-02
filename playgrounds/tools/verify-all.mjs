// Headless verification of the four playgrounds: per-site readiness, mechanism evidence, review captures.
// Usage: node tools/verify-all.mjs <outDir> [site] [baseUrl]
import { chromium } from 'playwright-core'
import { mkdirSync } from 'node:fs'
const EXE = '/Users/ashishverma/Library/Caches/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-mac-arm64/chrome-headless-shell'
const OUT = process.argv[2]; const ONLY = process.argv[3]; const BASE = process.argv[4] ?? 'http://localhost:5310'
const browser = await chromium.launch({ executablePath: EXE, headless: true })
const sites = {
  pulsehttp: async (p) => { await p.waitForTimeout(5000); await p.click('#burst'); await p.waitForTimeout(3600); return p.evaluate(() => ({ service: document.getElementById('serviceMsg').textContent, warn: document.getElementById('service').classList.contains('warn'), tallies: [...document.querySelectorAll('.dep .v')].map(e => e.textContent) })) },
  gitengine: async (p) => {
    await p.waitForFunction(() => [...document.querySelectorAll('#term .out')].some(el => el.textContent.includes('merge commit')), null, { timeout: 75000 }); await p.waitForTimeout(1200)
    await p.screenshot({ path: `${OUT}/gitengine/desktop-merged.png` })
    const run = async (cmd) => { await p.fill('#cmd', cmd); await p.press('#cmd', 'Enter'); await p.waitForTimeout(350) }
    await run('checkout exp'); await p.click('[aria-label="open README.md"]'); await p.fill('#editor', '# sandbox\nexp rewrote this line\n'); await run('add .'); await run("commit -m 'exp edits readme'"); await run('checkout main'); await run('merge exp'); await p.waitForTimeout(400)
    return p.evaluate(() => ({ gauge: document.getElementById('gaugeMsg').textContent, warn: document.getElementById('gauge').classList.contains('warn') }))
  },
  jsonlp: async (p) => {
    await p.waitForFunction(() => document.getElementById('vBig')?.textContent === 'SEALED', null, { timeout: 90000 }); await p.waitForTimeout(800)
    await p.screenshot({ path: `${OUT}/jsonlp/desktop-sealed.png` })
    await p.click('#presets button[data-name="trailing comma"]'); await p.waitForFunction(() => document.getElementById('hisRes').textContent === 'RETURN', null, { timeout: 15000 }); await p.waitForTimeout(700)
    return p.evaluate(() => ({ stamp: document.getElementById('stampMsg').textContent, bad: document.getElementById('stampbox').classList.contains('bad') }))
  },
  wcgo: async (p) => {
    await p.waitForFunction(() => document.getElementById('status').classList.contains('carry'), null, { timeout: 8000 }); await p.screenshot({ path: `${OUT}/wcgo/desktop-carry.png` })
    await p.waitForFunction(() => [...document.querySelectorAll('#soroban text')].some(t => t.textContent === 'agrees'), null, { timeout: 10000 }); await p.waitForTimeout(300)
    return p.evaluate(() => ({ status: document.getElementById('statusMsg').textContent, counts: [...document.querySelectorAll('#soroban text.disp')].map(t => t.textContent) }))
  },
}
const PATHS = { pulsehttp: 'pulsehttp', gitengine: 'gitengine', jsonlp: 'jsonlp', wcgo: 'wcgo' }
const LIVE = { pulsehttp: 'PulseHTTP', gitengine: 'GitEngine', jsonlp: 'JSON-Lexer-Parser-From-Scratch', wcgo: 'wc-Go' }
const report = {}
for (const [name, ready] of Object.entries(sites)) {
  if (ONLY && name !== ONLY) continue
  mkdirSync(`${OUT}/${name}`, { recursive: true })
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, colorScheme: 'dark' })
  const page = await ctx.newPage(); const errors = []
  page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()) })
  const path = BASE.includes('github.io') ? LIVE[name] : PATHS[name]
  await page.goto(`${BASE}/${path}/`, { waitUntil: 'domcontentloaded' })
  let evidence = {}; try { evidence = await ready(page) } catch (e) { evidence = { readyError: String(e) } }
  await page.screenshot({ path: `${OUT}/${name}/desktop.png` }); await page.screenshot({ path: `${OUT}/${name}/desktop-full.png`, fullPage: true })
  await page.setViewportSize({ width: 390, height: 844 }); await page.waitForTimeout(700); await page.screenshot({ path: `${OUT}/${name}/mobile.png`, fullPage: true })
  report[name] = { ...evidence, errors }; await ctx.close()
}
console.log(JSON.stringify(report, null, 1)); await browser.close()
