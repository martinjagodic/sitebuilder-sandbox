#!/usr/bin/env node
// Screenshots and page checks over the Chrome DevTools Protocol, for when the
// chrome-devtools MCP can't start (its profile is locked by another session).
// Launches its own headless Chrome with a throwaway profile; needs nothing
// beyond Node 22+ (built-in WebSocket) and Google Chrome.
//
//   node shots.mjs <base-url> <out-dir> <path> [<path> ...]
//
// For every path it writes <slug>-mobile.png (390×844, touch, full page) and
// <slug>-desktop.png (1440×900, full page), then prints one JSON line per
// viewport: horizontal overflow, broken images, console errors.
//
// Full-page captures scroll the page first so lazy images load, and pin the
// sticky header to the top; still check anything odd in a viewport shot
// (SHOTS_VIEWPORT=1 captures the viewport only, SHOTS_SCROLL=<selector>
// scrolls that element into view first, SHOTS_CLICK=<sel>,<sel> clicks
// those elements first, e.g. to open the menu, SHOTS_JS=<expression> runs
// in the page after that, SHOTS_WAIT=<ms> waits after it).

import { spawn } from 'node:child_process'
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

const [base, outDir, ...paths] = process.argv.slice(2)
if (!base || !outDir || !paths.length) {
  console.error('usage: node shots.mjs <base-url> <out-dir> <path> [<path> ...]')
  process.exit(1)
}
mkdirSync(outDir, { recursive: true })

const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
const PORT = 9300 + Math.floor(Math.random() * 600)
const VIEWPORTS = [
  { name: 'mobile', width: 390, height: 844, mobile: true },
  { name: 'desktop', width: 1440, height: 900, mobile: false },
]
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

const chrome = spawn(CHROME, [
  '--headless=new', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--hide-scrollbars', '--mute-audio',
  '--autoplay-policy=no-user-gesture-required',
  `--remote-debugging-port=${PORT}`, `--user-data-dir=${mkdtempSync(join(tmpdir(), 'shots-'))}`,
  'about:blank',
], { stdio: 'ignore' })

async function connect () {
  for (let i = 0; i < 50; i++) {
    try {
      const targets = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json()
      const page = targets.find((t) => t.type === 'page')
      if (page) return page.webSocketDebuggerUrl
    } catch {}
    await sleep(200)
  }
  throw new Error('Chrome did not start')
}

const ws = new WebSocket(await connect())
await new Promise((resolve) => ws.addEventListener('open', resolve, { once: true }))
let id = 0
const pending = new Map()
const listeners = []
ws.addEventListener('message', ({ data }) => {
  const msg = JSON.parse(data)
  if (msg.id && pending.has(msg.id)) {
    const { resolve, reject } = pending.get(msg.id)
    pending.delete(msg.id)
    msg.error ? reject(new Error(msg.error.message)) : resolve(msg.result)
  } else if (msg.method) {
    listeners.forEach((fn) => fn(msg))
  }
})
const send = (method, params = {}) => new Promise((resolve, reject) => {
  pending.set(++id, { resolve, reject })
  ws.send(JSON.stringify({ id, method, params }))
})
const evaluate = async (expression) =>
  (await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true })).result.value

let errors = []
listeners.push((msg) => {
  if (msg.method === 'Runtime.exceptionThrown') errors.push(msg.params.exceptionDetails.exception?.description || msg.params.exceptionDetails.text)
  if (msg.method === 'Log.entryAdded' && msg.params.entry.level === 'error') errors.push(msg.params.entry.text)
  if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
    errors.push(msg.params.args.map((a) => a.value ?? a.description ?? '').join(' ').slice(0, 800))
  }
})
await send('Page.enable')
await send('Runtime.enable')
await send('Log.enable')

async function load (url) {
  const loaded = new Promise((resolve) => {
    const fn = (msg) => { if (msg.method === 'Page.loadEventFired') { listeners.splice(listeners.indexOf(fn), 1); resolve() } }
    listeners.push(fn)
  })
  await send('Page.navigate', { url })
  await Promise.race([loaded, sleep(15000)])
  await sleep(800)
}

for (const path of paths) {
  const slug = path.replace(/^\/|\/$/g, '').replace(/[^a-z0-9]+/gi, '-') || 'home'
  for (const vp of VIEWPORTS) {
    errors = []
    await send('Emulation.setDeviceMetricsOverride', { width: vp.width, height: vp.height, deviceScaleFactor: 1, mobile: vp.mobile })
    await send('Emulation.setTouchEmulationEnabled', { enabled: vp.mobile })
    await load(new URL(path, base).href)

    // Scroll through so lazy images load, then back to the top.
    await evaluate(`(async () => {
      for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight / 2) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)) }
      scrollTo(0, 0); await new Promise(r => setTimeout(r, 400))
    })()`)
    // SHOTS_CLICK="sel1,sel2" clicks each in turn (e.g. open the menu), then
    // captures the viewport.
    for (const selector of (process.env.SHOTS_CLICK || '').split(',').filter(Boolean)) {
      await evaluate(`document.querySelector(${JSON.stringify(selector)})?.click()`)
      await sleep(500)
    }
    // SHOTS_JS="<expression>" runs in the page (after the clicks), e.g. to
    // change the hash route of a single-page app such as the CMS.
    let js
    if (process.env.SHOTS_JS) {
      js = await evaluate(process.env.SHOTS_JS)
      await sleep(Number(process.env.SHOTS_WAIT || 3000))
    }
    if (process.env.SHOTS_SCROLL) {
      await evaluate(`document.querySelector(${JSON.stringify(process.env.SHOTS_SCROLL)})?.scrollIntoView({ block: 'start' })`)
      await sleep(600)
    }

    const report = await evaluate(`({
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      // Past the right edge and not clipped by a scroller or overflow: hidden.
      wide: [...document.querySelectorAll('body *')].filter(el => {
        if (el.getBoundingClientRect().right <= document.documentElement.clientWidth + 1) return false
        for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
          if (getComputedStyle(a).overflowX !== 'visible') return false
        }
        return true
      }).slice(0, 5).map(el => el.tagName.toLowerCase() + '.' + [...el.classList].join('.')),
      brokenImages: [...document.images].filter(img => img.complete && !img.naturalWidth).map(img => img.currentSrc || img.src),
      height: document.documentElement.scrollHeight,
    })`)

    const file = join(outDir, `${slug}-${vp.name}.png`)
    const viewportOnly = process.env.SHOTS_VIEWPORT === '1' || process.env.SHOTS_SCROLL || process.env.SHOTS_CLICK || process.env.SHOTS_JS
    const shot = await send('Page.captureScreenshot', viewportOnly
      ? { format: 'png' }
      : { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: 0, width: vp.width, height: Math.min(report.height, 16000), scale: 1 } })
    writeFileSync(file, Buffer.from(shot.data, 'base64'))
    const text = process.env.SHOTS_JS ? await evaluate('document.body.innerText.slice(0, 600)') : undefined
    console.log(JSON.stringify({ path, viewport: vp.name, file, overflow: report.overflow, wide: report.wide, brokenImages: report.brokenImages, errors, js, text }))
  }
}

ws.close()
chrome.kill()
process.exit(0)
