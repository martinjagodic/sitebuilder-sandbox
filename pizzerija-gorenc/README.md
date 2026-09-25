# Pizzerija Gorenc

A [Sitebuilder](https://github.com/martinjagodic/sitebuilder-core) project. Layouts, styles, scripts and the CMS schema come from `sitebuilder-core`. This repo holds only branding, content and customizations.

## Develop

```bash
pnpm install
hugo mod tidy          # standalone repo only
pnpm run dev           # http://localhost:1313
npx decap-server       # second terminal, for the CMS at /admin
```

While this project still lives in `sitebuilder-sandbox`, run it from the sandbox root instead — `./sb dev pizzerija-gorenc` — so Hugo uses the local core checkout.

## Where things live

| What | Where |
| --- | --- |
| Pages and posts | `content/`, one file per language: `about.sl.md`, `about.en.md` |
| Languages, and which are on | `config/_default/hugo.toml` → `[languages]` |
| Logo, favicon, uploads | `static/media/` |
| Title, colors, spacing, fonts | `config/_default/hugo.toml` → `[params.theme]` |
| Navigation, shared by every language | `config/_default/menus.yaml` |
| Footer copyright | `data/footer.json` |
| Brand-only CSS | `assets/styles/_custom.scss` |
| Overriding a core component | copy it to `layouts/partials/<name>.html` |
| Overriding the CMS schema | copy core's `assets/admin/config.template.yml` |

Anything reusable belongs in core, not here. There are no lint or PostCSS configs in this repo on purpose — `sitebuilder lint` and Hugo both read core's.

## Media

Images go through the shared Bunny zone. Set `mediaPrefix` in `hugo.toml` to this project's folder in that zone; the zone URL itself is configured once in core. Leave it empty to serve media from the repo with no transforms.

## CMS

Local only for now: `npx decap-server` plus `/admin`. Uploads land in
`static/media/uploads`.

The CMS config is rendered by Hugo on every build from the schema in
sitebuilder-core — there is nothing to generate and nothing to commit here.
To go live, set `cms.backend = "turbo-github"` and `cms.turboSiteId` in
`hugo.toml` and rebuild.

## Update core

```bash
pnpm exec sitebuilder update
```
