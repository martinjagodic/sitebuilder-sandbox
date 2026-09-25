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
structure, tone and level of polish.

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

### 4. Scaffold, then check core covers the plan

```bash
./sb new <lead-id>
cd <lead-id> && pnpm install
```

Core has: hero (`overlay` over a photo, `standard` beside a photo, or a text
band without an image), `features`, `imageText`, `reviews`, `location`, `cta`,
`priceList` (categories, optional size columns, tags), `gallery`,
`mediaModule`, `quote`, `content`, and `data/business.json`. See core's
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

### 10. Verify

```bash
./sb build <lead-id>
cd ../sitebuilder-core && node bin/sitebuilder.js lint && (cd demo && pnpm run build)
```

Then run `./sb dev <lead-id> --port <n> --bind 127.0.0.1` in the background,
and check it with the chrome-devtools MCP:

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
  viewport screenshot after `scrollIntoView`.

### 11. Handoff

Write `leads/<id>/handoff.md` (use Gorenc's as the template):

- What's on each page.
- Real, placeholder or unconfirmed, per item.
- Owner questions in Slovenian, ready to paste.
- Pitch talking points drawn from the research.
- A before-go-live checklist.
- Design-agent and content-agent tasks.

Append a dated line to the lead's `notes` in `leads.json`. Then tell the
user: the preview URL, what needs confirming, core changes (uncommitted
unless asked), and the agent tasks.

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
