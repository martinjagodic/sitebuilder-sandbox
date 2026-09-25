# CLAUDE.md

## What this is

A monorepo of Sitebuilder prototypes — one folder per project, each a Hugo site. These are sales pitch prototypes; the ones that convert move to `sitebuilder-client-<name>` repos.

Shared code lives in `sitebuilder-core`, checked out as a sibling directory and consumed as a Hugo module + npm package.

A project here holds only branding, content and customizations.

If a change could benefit another site — a component, a style, a CMS field, a build tweak — it belongs in `../sitebuilder-core`. Adding a layout or partial to a project should be deliberate.

## What belongs in a project folder

| Path | Holds |
| --- | --- |
| `content/` | Pages and posts, one file per language: `about.sl.md`, `about.en.md` |
| `static/media/` | Logo, favicon, uploads |
| `config/_default/hugo.toml` | Title, baseURL, module import, `[languages]`, branding, theme, `mediaPrefix`, `[cms]`. CMS edits this file — it preserves keys it does not declare, so the structural blocks survive. |
| `config/_default/menus.yaml` | Navigation, one list for every language (`pageRef` items) |
| `data/` | Data files, mostly content for global components |
| `assets/styles/_custom.scss` | Brand-only CSS |
| `static/admin/` | Only if overriding the Decap shell — normally absent |

Anything else appearing in a project is a sign it should have gone to core. In particular there are **no lint or PostCSS configs** in a project — the CLI points eslint/stylelint at core's, and Hugo reads core's PostCSS config from `node_modules/sitebuilder-core`. Do not add copies back.

## Media and CMS

Images go through one shared Bunny pull zone (set once in core) so a single Bunny Optimizer subscription covers every project. A project only sets `mediaPrefix`. Never hand-build a media URL — core's `bunny` partial does it.

The CMS config is rendered by Hugo on every build to `/admin/config.yml` from core's `assets/admin/config.template.yml`. Nothing is generated into a project and nothing is committed. Exceptions are possible.

The CMS is local-only right now: `npx decap-server` plus `/admin`, uploads into `static/media/uploads`. Going live means setting `cms.backend = "turbo-github"` and `cms.turboSiteId` in `hugo.toml` and rebuilding.

## Commands

Always go through `./sb` — it sets `HUGO_MODULE_REPLACEMENTS` so Hugo uses the local core checkout instead of trying to fetch the private module.

```bash
./sb new <name>       # scaffold (--lang en for an English-main site)
./sb dev <name>       # dev server
./sb build <name>     # lint + build
./sb lint <name>      # lint only
```

Running bare `hugo` inside a project folder fails — the module has no published version to fetch.

## Setup notes

- Each project installs its own `node_modules` with **pnpm**. There is no workspace on purpose: a project folder must stay byte-identical to what ships in a client repo, so promoting it is just a move. pnpm shares packages from a global store, so a project costs ~3 MB of disk, not ~55 MB.
- Every project ships `pnpm-workspace.yaml` with `nodeLinker: hoisted`. It is load-bearing: Sass and esbuild resolve `swiper`/`lightgallery` from the project's `node_modules`, but those are declared in core. pnpm's default layout hides them and the build fails with a misleading `Can't find stylesheet to import`. Do not delete it.
- After changing core's `package.json`, CLI, lint or PostCSS config, refresh the project's copy of core: the `file:` core dep is packed and copied, not symlinked, and a plain `pnpm install` keeps the cached pack, so run `rm -rf node_modules/sitebuilder-core && pnpm install`. Layout/SCSS changes need no refresh — those come through the Hugo module, and PurgeCSS purges against the rendered HTML (`hugo_stats.json`), not the copy's layouts.

## Verifying a change

```bash
./sb build <name>
```

This runs the same lint + build path as CI. If you touched core, build a sandbox project **and** `../sitebuilder-core/demo` — they resolve the module differently.

## Promoting

`pnpm exec sitebuilder promote` inside the project swaps the local core dependency for the published git URL. Then `hugo mod tidy && pnpm install`, move the folder to its own repo, and set `GITHUB_TOKEN` in the deploy environment (core is private).

If the site already uses Decap Turbo, change its repo in the Turbo dashboard to the new one — Turbo ignores `repo` in the config. The CMS paths need no change: `build.sh` prefixes them with the project's folder from git (`pizzerija-gorenc/content` here, `content` in its own repo).
