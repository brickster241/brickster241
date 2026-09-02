// Profile README screenshots of the four worlds, from the live pages, each caught mid-performance.
// Usage: node tools/shoot-readme.mjs <outDir> [baseUrl]
import { chromium } from 'playwright-core'
const EXE = '/Users/ashishverma/Library/Caches/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-mac-arm64/chrome-headless-shell'
const OUT = process.argv[2] ?? '.'; const BASE = process.argv[3] ?? 'https://brickster241.github.io'
const browser = await chromium.launch({ executablePath: EXE, headless: true })
const ctx = await browser.newContext({ viewport: { width: 1100, height: 687 }, deviceScaleFactor: 2, colorScheme: 'dark' })
async function shoot(name, path, choreography) { const page = await ctx.newPage(); page.setDefaultTimeout(90_000); await page.goto(`${BASE}/${path}/`, { waitUntil: 'domcontentloaded' }); await choreography(page); await page.screenshot({ path: `${OUT}/play-${name}.png` }); console.log('shot:', name); await page.close() }
const P = BASE.includes('github.io') ? { pulsehttp: 'PulseHTTP', gitengine: 'GitEngine', jsonlp: 'JSON-Lexer-Parser-From-Scratch', wcgo: 'wc-Go' } : { pulsehttp: 'pulsehttp', gitengine: 'gitengine', jsonlp: 'jsonlp', wcgo: 'wcgo' }
await shoot('pulsehttp', P.pulsehttp, async (p) => { await p.waitForTimeout(5000); await p.click('#burst'); await p.waitForTimeout(3600) })
await shoot('gitengine', P.gitengine, async (p) => { await p.waitForFunction(() => [...document.querySelectorAll('#term .out')].some(el => el.textContent.includes('merge commit')), null, { timeout: 75_000 }); await p.waitForTimeout(1200) })
await shoot('jsonlp', P.jsonlp, async (p) => { await p.waitForFunction(() => document.getElementById('vBig')?.textContent === 'SEALED', null, { timeout: 90_000 }); await p.waitForTimeout(800) })
await shoot('wcgo', P.wcgo, async (p) => { await p.waitForFunction(() => document.getElementById('status').classList.contains('carry'), null, { timeout: 8000 }); await p.waitForTimeout(150) })
await browser.close(); console.log('done')
