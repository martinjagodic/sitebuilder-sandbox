---
name: prototype
description: Build a sales-pitch prototype website for a lead from leads/leads.json — research the business, gather its real content and media, plan pages from core's modules, set brand tokens, write the content, verify it on mobile, and write a pitch handoff. Use when asked to start, build or continue a prototype for a lead or a named business.
---

# Prototype a lead

A prototype is the pitch: the owner opens it on their phone and sees *their*
business, with their dishes, their reviews and their hours, looking better
than anything they have now. It is built in `sitebuilder-sandbox/<lead-id>/`
on top of `sitebuilder-core` and must be promotable to a client repo as-is.

First run: `pizzerija-gorenc` (Sep 2026). Look at it as the reference for
structure, tone and level of polish. `planet-plus` (Sep 2026) is the reference
for a **migration**: a site we already built, moved onto core with its URLs
and content (see "Migrating a site we built").

## What a prototype must be

- **Visually appealing.** Real photos, a deliberate palette and type pairing,
  generous spacing. It should not look like a template.
- **Simple.** Adding content later is easy and removing it is awkward, so ship
  the fewest pages and sections that tell the story. Default sitemap: **Home,
  the core offer (menu / services / products), Contact**. Add a page only if
  the research turned up content that needs one.
- **Tailored.** Every word is about this business. No lorem ipsum, no generic
  filler ("We are passionate about quality").
- **Mobile-first.** Most owners and customers will see it on a phone. Check
  390 px width before desktop.
- **Truthful.** Never invent facts: hours, prices, founding year, owner names,
  "family-run", "free parking", awards. If research did not find it, **ask
  the user** or leave it out. Copy may paraphrase the business's own words
  (listings, Instagram, Facebook) but must not add claims.

## Where things go

| What | Where |
| --- | --- |
| Research, raw downloads, manifest, handoff | `leads/<lead-id>/` (`research.md`, `media/raw/`, `media/manifest.md`, `handoff.md`) |
| Scripts that prepare media and write pages | `leads/<lead-id>/` (Planet Plus: `media/prepare.py`, `generate_content.py`), so a rerun reproduces the site |
| The site | `<lead-id>/` (scaffolded by `./sb new`) |
| Selected, optimised media | `<lead-id>/static/media/uploads/` (only files a page uses) |
| Logo, favicon | `<lead-id>/static/media/brand/logo.png`, `<lead-id>/static/favicon.png` |
| Business facts (address, geo, phone, email, hours, social) | `<lead-id>/data/business.json`. Drives the header call button, footer, `location` module and JSON-LD. |
| Brand tokens | `<lead-id>/config/_default/hugo.toml` → `[params.theme]` |
| Anything another project could use | `../sitebuilder-core`, never the project |

## Procedure

Steps 2–4 overlap: research runs in the background while you ask
architecture questions, scaffold, and fill gaps in core.

### 1. Claim the lead

Use the `leads` skill: `move "<business name>" in-progress`. Keep the file's
compact formatting (inline primitive arrays) so the diff only shows the move.

### 2. Research (background agent)

Spawn a general-purpose agent with the brief in
[research-brief.md](research-brief.md). It writes `leads/<id>/research.md`,
downloads photos to `media/raw/` and writes `media/manifest.md`. It takes
about 30 minutes. Don't duplicate its searches, and don't touch browser tabs
in its isolated context.

What the first run taught about sources:

- **Delivery platforms (Wolt) are the richest source for restaurants.** They
  have the full priced menu with verbatim ingredients and a professional photo
  shoot (2880 px). Their prices usually include a packaging surcharge, so
  dine-in prices differ.
- Directory listings are often thinner than the lead note claims. Correct
  `leads.json` when they are.
- The tourist board (Visit Kranj) has professional photos with a credited
  photographer, which needs permission.
- Google's own profile is the most authoritative source for hours when it is
  owner-managed.
- bizi.si / CompanyWall can show **more than one legal entity** (an old s.p.
  and a newer d.o.o.). **Confirm the company of record with the user** before
  recording it, and never put a legal entity on the site on a guess.

### 3. Decide structure while research runs

Architecture questions that are the user's call go to `AskUserQuestion`
early, so answers arrive in parallel. Settled defaults (don't re-ask):

- Sitemap: Home + offer page + Contact.
- Location: OpenStreetMap embed plus an "open in Google Maps" button (no
  Google cookies).
- Fonts: Bunny Fonts, named in `[params.theme] fonts`.
- Language: Slovenian only, unless the user asks for English. Page files are
  `<page>.sl.md`; an English version is `<page>.en.md` beside it, plus
  `disabled = false` under `[languages.en]`. Menu items use `pageRef` so they
  follow the translation (core's CLAUDE.md, "Languages").

Ask per lead: how to show prices the business hasn't confirmed (for Gorenc
the user chose Wolt prices, unlabelled), and whether to use photos whose
rights aren't clear (for Gorenc: yes, flagged in the handoff).

Also ask, rather than assume, about the brand direction. Offer three concrete
palette-and-type pairs with their contrast ratios, as Planet Plus did. Ask too
about anything the current site does that core doesn't, such as video heroes,
dropdown menus or a newsletter form. Whether it goes into core or stays in the
project is the user's call. A client's own third-party service (Planet Plus's
EmailOctopus form) stays in the project, through a hook partial such as
`layouts/partials/hooks/footer.html`. The user won't promote a client's vendor
to other sites.

### 4. Scaffold, then check core covers the plan

```bash
./sb new <lead-id>
cd <lead-id> && pnpm install
```

Core has: hero (`overlay` over a photo or a muted background `video`,
`standard` beside a photo, or a text band without an image), `features`
(icons, or `numbered`), `imageText` (optionally `portrait`), `reviews`,
`location`, `cta`, `priceList` (categories, optional size columns, tags),
`gallery`, `mediaModule`, `quote`, `content`, `pages` (cards linking to a
section's pages, as on every list page), `partners` (a one-colour logo wall
from `data/partners.json`), `data/business.json`, dropdown menus (`parent` /
`identifier` in `menus.yaml`), a dark `scheme`, and a `hooks/footer` partial
for project-only footer content. See core's
CLAUDE.md, "Building blocks". A missing piece goes in **core**: partial with
doc comment, SCSS, CMS type, editor preview, i18n strings (`sl` and `en`),
and a demo usage. A class that only JavaScript adds goes in the PurgeCSS
`safelist` in core's `postcss.config.js`.

Layout and SCSS changes in core show up in the project immediately. A change
to core's CLI, `package.json` or PostCSS/lint config needs the project's copy
refreshed, and then the dev server restarted:

```bash
cd <lead-id> && rm -rf node_modules/sitebuilder-core && pnpm install
```

### 5. Gap analysis → questions

When research lands, sort every content need into one table: have (source),
generate (AI), ask. Ask the user about business facts in one batch
(`AskUserQuestion`, max four per call, most important first). A fact that
most sources agree on can go in, marked "confirm" in the handoff. Anything
unknown stays off the site.

### 6. Brand tokens

- **Colours:** sample them from the logo. There's no PIL, so convert with
  `sips -s format bmp` and read the pixels with a short Python script (see the
  Gorenc run). Set `color_primary`, `color_on_primary`, `color_secondary`,
  `color_surface`, `color_dark`, `color_text`, `color_heading`.
- **Contrast:** check text and buttons against WCAG AA (4.5:1). Brand colours
  that fail as a background (Gorenc's green is 3.4:1) become accents: icons
  and tags, never text on the colour. Bright colours usually need a dark
  `color_on_primary`.
- **Type:** a display face with the business's character plus a readable text
  face, both on Bunny Fonts. Check the family names with `curl
  "https://fonts.bunny.net/css?family=<name>:400"`. Set
  `font_heading_weight` to a weight the font actually has; single-weight
  display faces like Bree Serif need `"400"`.
- **Check š, č and ž at heading size, in the browser, before committing to a
  face.** Cormorant Garamond draws a detached caron that looks broken in
  "Razmišljamo". EB Garamond, Playfair Display, Bodoni Moda, Gilda Display,
  Newsreader and Fraunces render it well. A small HTML page that loads the
  candidates from Bunny, screenshotted with `shots.mjs`, is a quick
  comparison to show the user.
- **Dark sites:** set `scheme = "dark"` in `[params.theme]`, a near-black
  `color_background`, a slightly lighter `color_surface`, a darker
  `color_dark`, and light `color_text` and `color_heading`. A bright accent
  then needs a dark `color_on_primary`.
- **Width:** set `content_width` to about `calc(1280px + (2 * var(--container-padding)))`.
  Core's 1680px default looks sparse for a small business.

### 7. Logo and favicon

- **A JPEG logo on white** becomes a transparent PNG through a canvas
  colour-to-alpha pass in the dev-server tab (chrome-devtools
  `evaluate_script`, `filePath` inside a workspace root such as
  `leads/<id>/`). For each pixel, alpha is the largest channel distance from
  white divided by 255, and each channel becomes `255 - (255 - c) / alpha`.
  Then decode the data URL with Python and resize with `sips -Z 300`.
- **Crop tight first:** `sips --cropToHeightWidth H W`. For the favicon, crop
  just the emblem (`sips -c H W --cropOffset Y X`), pad it square
  (`sips -p N N --padColor FFFFFF`) and save it as a 192 px PNG.
- **Without a browser:** ffmpeg dumps raw pixels (`-f rawvideo -pix_fmt
  rgba -`) for a Python colour-to-alpha pass, and encodes them back to PNG.
  Planet Plus's logo was dark text on an opaque light-grey box (alpha 224
  everywhere, so check it). It became a white transparent PNG for the dark
  header.
- A favicon without an emblem can be a letter drawn with ffmpeg `drawtext`,
  using the site's display font (a `.woff` from Bunny works).
- A vector logo is a design-agent task. Don't redraw it in the prototype.

### 8. Media

- Pick only what the pages use: hero, one or two section photos, a gallery of
  about 8 products. Optimise into `static/media/uploads/` with descriptive
  Slovenian kebab-case names:
  - Hero: `sips -Z 1680 --setProperty formatOptions 60`, keep it under 500 KB
    because it's the LCP image.
  - Section photos: `-Z 1400`, `formatOptions 65`.
  - Gallery and product photos: `-Z 1000`, `formatOptions 78`.
  - In zsh, `set -- $pair` does not split words, so pass pairs as separate
    arguments to a function.
- **Local first (no Bunny zone yet):** set `bunnyUrl = ""` in the project's
  `[params]`. Nothing resizes the files then, so these sizes are what every
  device downloads. A hero still over 500 KB at q60 is usually a noisy print
  scan. A light ffmpeg denoise (`hqdn3d=4:3:0:0`) before encoding costs less
  detail than lowering the quality does.
- **Video:** `ffmpeg -an -c:v libx264 -preset slow -crf 30 -pix_fmt yuv420p
  -movflags +faststart` gives about 3.4 MB for 32 s at 1080p. Set it as the
  overlay hero's `video`; the hero image stays as the poster. Look at the
  frames first: Planet Plus's "studio" video was a manufacturer's brand film,
  not their showroom, so no copy may call it theirs.
- **Duplicates:** sites often show the same photo twice. A 16×16 greyscale
  thumbnail from ffmpeg per file, compared pairwise, finds them. Show each
  photo once.
- **Alt text:** a labelled contact sheet (ffmpeg `xstack` plus `drawtext`, 16
  per sheet) lets you see and describe 80 photos in five images.
- Skip dated photos (COVID masks, a pre-renovation interior) and anything
  that hints at a previous operator.
- Delete optimised files no page references before handing off.
- Record in `media/manifest.md` what is used where, with its rights status.
- **AI placeholders:** only when real photos can't cover a section. The Figma
  MCP's Weave tools can generate them (`weave_find_model` →
  `weave_run_model`). That needs the user's Figma account linked to Weave
  (https://app.weavy.ai/settings?section=profile); without the link the tools
  return an error, and the prompts go to the user or a design agent instead.
  Every run costs credits and needs explicit user approval of the quoted
  cost. Never use AI to depict something the business doesn't have.

### 9. Content

- **Home, restaurant recipe:**
  - overlay hero: best food shot, the business's own tagline, two buttons
    (offer page, call)
  - `features`: 4 verified facts with icons
  - `gallery`: 8 products with ingredients as captions
  - `imageText`: what makes them special, told with the real photo
  - `reviews`: 3 verbatim reviews plus the Google aggregate
  - `cta` on the primary colour: call and order
- **Offer page:** a text-band hero plus `priceList`. **Generate it from the
  research tables with a script**, not by retyping, so nothing is mistyped.
  Fix only obvious typos, and list them in the handoff.
- **Contact:** a standard hero with the building photo, plus `location` on a
  surface background.
- Every page needs a `title`, a `description` (about 150 characters, used for
  SEO and social) and a hero. Copy lives in front matter modules, never in
  templates.
- Use `+386 …` phone numbers so `tel:` links work from foreign phones too.
- NFC-normalise text taken from files (`unicodedata.normalize('NFC', …)`).
  Content edited on a Mac can hold "s + combining caron", which web fonts
  draw as a floating accent.

### 10. Verify

```bash
./sb build <lead-id>
cd ../sitebuilder-core && node bin/sitebuilder.js lint && (cd demo && pnpm run build)
```

Then run `./sb dev <lead-id> --port <n> --bind 127.0.0.1` in the background,
and check it with the chrome-devtools MCP. Stop it later by its PID or task
ID, never with `pkill -f 'hugo server'`, which also kills other sessions'
servers.

**When the MCP says the browser is already running** (another session holds
its profile), use `shots.mjs` in this folder instead. It drives its own
headless Chrome over CDP:

```bash
node .claude/skills/prototype/shots.mjs http://127.0.0.1:<n> <out-dir> / /kontakt/
.claude/skills/prototype/tile.sh <out-dir>/home-mobile.png <out-dir>/t-home 1300 4
```

It writes full-page mobile (390 px, touch) and desktop (1440 px) captures, and
reports overflow, broken images and console errors per page. `SHOTS_CLICK`
opens menus, `SHOTS_SCROLL` takes a viewport shot of one section, and
`SHOTS_JS` runs a script (it prints the result). Plain `chrome --headless
--screenshot` hangs on pages with a looping video. Lighthouse runs with
`CHROME_PATH=<chrome> npx -y lighthouse@12 <url> --form-factor=mobile
--only-categories=accessibility`.

Check:

- Screenshots at 390×844 (mobile emulation) and 1440×900 for every page.
- `document.documentElement.scrollWidth === clientWidth` on phones, to catch
  horizontal overflow. Absolutely positioned `.visually-hidden` labels inside
  horizontal scrollers are the usual cause.
- Lighthouse, mobile: accessibility ≥ 95. SEO is low on the dev server
  because of the intentional `noindex`.
- Click the gallery: the lightbox should open, and the page shouldn't
  navigate.
- **Full-page screenshots lie:** they draw the sticky header mid-page, skip
  lazy images and squash cross-origin iframes. Check anything odd with a
  viewport screenshot after `scrollIntoView`. The OSM map needs WebGL, which
  headless Chrome only has with `--use-angle=swiftshader` (`shots.mjs`
  passes it).
- **The CMS:** run `npx decap-server` in the project folder and open an entry
  of every page type. Check that the fields hold values, not just that the
  editor renders. Log in with `SHOTS_JS` that clicks the Login button and then
  sets `location.hash`, and wait about 6 s before reading. An entry that
  opens with empty fields and "No Entries" in the list means the CMS is
  requesting the wrong folder: look at the paths it sends to `:8081`.

### 11. Handoff

Write `leads/<id>/handoff.md` (use Gorenc's as the template):

- What's on each page.
- Real, placeholder or unconfirmed, per item.
- Owner questions in Slovenian, ready to paste.
- Pitch talking points drawn from the research.
- What was fixed on the way (a migration finds broken images and stale
  notices on the live site; they make good pitch points).
- A before-go-live checklist.
- Design-agent and content-agent tasks.

Append a dated line to the lead's `notes` in `leads.json`. Then tell the
user: the preview URL, what needs confirming, core changes (uncommitted
unless asked), and the agent tasks.

## Migrating a site we built

When the lead is a site we already built (the user is its developer), the
content already exists, so the work is moving it over rather than finding it:

- **Sitemap:** keep every live URL (for Planet Plus: `/prodajni-program/<slug>/`
  as `content/prodajni-program/<slug>.sl.md`), so nothing needs a redirect.
  This replaces the three-page default.
- **Sources:** the old repo's front matter and data files hold the copy and
  the curated photo list. The client's own folder has the originals and often
  a Word file of texts the site never used. Media on Cloudinary serves the
  stored original, so match each live file to the folder by exact byte size.
  Download from Cloudinary only when nothing matches, and record any URL that
  returns 404: it is broken on the live site today.
- **Generate the pages with a script** from the old front matter, the client's
  document and a media map. Assert that every quoted sentence exists in its
  source, list the typo fixes in the script, and have it report optimised
  files that no page uses.
- **Research** is lighter: skip photo downloads and verify facts instead. The
  Google profile, the registry (bizi.si, CompanyWall), dealer locators of the
  brands they claim, and the Wayback Machine for history. Registries and
  Google often disagree on the phone number; ask.

## Delegating

Coding-agent work is covered above. These suit other agents:

- **Design agent:**
  - vector logo and horizontal lockup
  - hero crop for phones
  - art direction or replacement shots for photos whose rights can't be cleared
  - social templates in the site palette
  - a Figma mockup when the owner wants alternatives
- **Content agent:**
  - "O nas" once the owner tells the story
  - lunch or daily offer blocks
  - an English version for tourists
  - the Google Business Profile description
  - replies to negative reviews
