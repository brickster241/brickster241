// Stress the three cases the user raised, driving the pages through their real controls (the scripts are modules).
import { chromium } from 'playwright-core'
const exe = '/Users/ashishverma/Library/Caches/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-mac-arm64/chrome-headless-shell'
const base = process.argv[3] || 'http://localhost:5310', out = process.argv[2], only = process.argv[4] || ''
const browser = await chromium.launch({ executablePath: exe })
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 })
const page = await ctx.newPage()
const errors = []
page.on('pageerror', (e) => errors.push(String(e)))
page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()) })
const report = {}
const svgTexts = (sel) => [...document.querySelectorAll(sel)].map((t) => t.textContent)

// ---- wc-Go: a 1.4 MB markdown file dropped on the page ----
await page.goto(`${base}/wcgo/`, { waitUntil: 'load' })
await page.waitForTimeout(800)
await page.evaluate(() => {
  const text = ('# Heading\n\nSome words here, with ünïcödé and emoji 🚀 to force carries at the seams.\n').repeat(18000)
  const dt = new DataTransfer(); dt.items.add(new File([text], 'big.md', { type: 'text/markdown' }))
  document.dispatchEvent(new DragEvent('drop', { dataTransfer: dt, bubbles: true, cancelable: true }))
})
await page.waitForFunction(() => [...document.querySelectorAll('#soroban text')].some((t) => /agrees|mismatch|MB\/s/.test(t.textContent)), null, { timeout: 60000 })
await page.waitForTimeout(300)
report.wcgo = await page.evaluate(() => {
  const heavens = [...document.querySelectorAll('.heaven')].sort((a, b) => (+a.getAttribute('cy') - +b.getAttribute('cy')) || (+a.getAttribute('cx') - +b.getAttribute('cx')))
  const earths = [...document.querySelectorAll('.earth')]
  const dy = (e) => +((e.getAttribute('transform') || '').match(/translate\(0 (-?[\d.]+)\)/)?.[1] ?? 0)
  const rodDigit = (h) => { const cx = h.getAttribute('cx'), hy = +h.getAttribute('cy'); const up = earths.filter((e) => e.getAttribute('cx') === cx && +e.getAttribute('cy') > hy && +e.getAttribute('cy') < hy + 240 && dy(e) < 0).length; return (dy(h) > 0 ? 5 : 0) + up }
  const per = heavens.length / 4
  const groups = [0, 1, 2, 3].map((g) => heavens.slice(g * per, (g + 1) * per).map(rodDigit).join(''))
  const disp = [...document.querySelectorAll('#soroban text.disp')].map((t) => t.textContent)
  return { rodsPerGroup: per, beads: { lines: groups[0], words: groups[1], bytes: groups[2], chars: groups[3] }, printed: disp, verdict: [...document.querySelectorAll('#soroban text')].map((t) => t.textContent).find((s) => /agrees|mismatch|MB\/s/.test(s)), textareaChars: document.getElementById('src').value.length, status: document.getElementById('statusMsg').textContent }
})
await page.locator('#frame').screenshot({ path: `${out}/wcgo/stress-bigfile.png` })

if (only && only !== 'wcgo') {} 
if (only === 'wcgo') { report.errors = errors; console.log(JSON.stringify(report, null, 1)); await browser.close(); process.exit(0) }
// ---- GitEngine: many files, twelve more commits, through the notebook and the command line ----
await page.goto(`${base}/gitengine/`, { waitUntil: 'load' })
await page.waitForFunction(() => [...document.querySelectorAll('#term .out')].some((el) => el.textContent.includes('survey complete')), null, { timeout: 75000 })
const run = async (c) => { await page.fill('#cmd', c); await page.press('#cmd', 'Enter'); await page.waitForTimeout(220) }
for (let i = 0; i < 9; i++) { await page.fill('#newPath', `notes/part${i}.md`); await page.click('#addFileBtn') }
for (let i = 0; i < 12; i++) { await page.fill('#newPath', `rev/r${i}.txt`); await page.click('#addFileBtn'); await run('add .'); await run(`commit -m 'revision ${i}'`) }
await page.waitForTimeout(400)
report.gitengine = await page.evaluate(() => {
  const blobs = document.getElementById('recBlobs'), commits = document.getElementById('recCommits')
  const texts = [...document.querySelectorAll('#chart text')].map((t) => t.textContent)
  return { counts: ['nCommits', 'nTrees', 'nBlobs'].map((id) => document.getElementById(id).textContent), blobsScroll: blobs.scrollHeight > blobs.clientHeight, commitsScroll: commits.scrollHeight > commits.clientHeight, firstCommitPill: commits.firstElementChild?.textContent, oxbows: [...commits.children].filter((b) => /oxbow/.test(b.textContent)).length, commitsDrawn: document.querySelectorAll('#chart circle.conf').length, lanesUsed: new Set([...document.querySelectorAll('#chart circle.conf')].map((c) => c.getAttribute('cy'))).size, upstreamNote: texts.find((s) => /earlier commit/.test(s)) || null, pagingNote: texts.find((s) => /Next page/.test(s)) || null, poolClipped: document.querySelector('.poollvl').getAttribute('clip-path'), tribs: document.querySelectorAll('.trib').length, head: document.getElementById('headRef').textContent, log: [...document.querySelectorAll('#term .out, #term .err')].map((e) => e.textContent).filter((s) => /rebased|CONFLICT|sealed|fast-forward|survey complete/i.test(s)) }
})
await page.locator('#frame').screenshot({ path: `${out}/gitengine/stress-crowded.png` })
await page.locator('.records').screenshot({ path: `${out}/gitengine/stress-records.png` })
await page.click('#chart text.more')
await page.waitForTimeout(200)
report.gitengine.afterNext = await page.evaluate(() => [...document.querySelectorAll('#chart text')].map((t) => t.textContent).find((s) => /page 2/.test(s)) || null)

// ---- JSON-LP: the stamps and the seal, valid then refused ----
await page.goto(`${base}/jsonlp/`, { waitUntil: 'load' })
await page.waitForFunction(() => document.getElementById('vBig')?.textContent === 'Sealed', null, { timeout: 120000 })
await page.waitForTimeout(600)
await page.locator('#frame').screenshot({ path: `${out}/jsonlp/stress-sealed.png` })
report.jsonlp = { valid: await page.evaluate(() => ({ stamps: [...document.querySelectorAll('text.stampt')].map((t) => t.textContent).filter(Boolean), sealOpacity: document.querySelector('.sealg').style.opacity, seal: document.querySelector('text.sealt').textContent, big: document.getElementById('vBig').textContent })) }
await page.click('#presets button[data-name="trailing comma"]')
await page.waitForFunction(() => document.getElementById('hisRes').textContent === 'Refused', null, { timeout: 15000 })
await page.waitForTimeout(600)
report.jsonlp.refused = await page.evaluate(() => ({ stamps: [...document.querySelectorAll('text.stampt')].map((t) => t.textContent).filter(Boolean), seal: document.querySelector('text.sealt').textContent, bad: document.querySelector('.sealg').classList.contains('bad'), big: document.getElementById('vBig').textContent, his: document.getElementById('hisRes').textContent, std: document.getElementById('stdRes').textContent }))
await page.locator('#frame').screenshot({ path: `${out}/jsonlp/stress-refused.png` })

report.errors = errors
console.log(JSON.stringify(report, null, 1))
await browser.close()
