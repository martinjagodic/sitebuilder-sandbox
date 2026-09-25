# Sitebuilder sandbox

Prototypes in development, one folder per project. Each folder is a Hugo site using sitebuilder-core. When ready to launch, it can be just moved to its own repo.

Shared layouts, styles and CMS schema come from [`sitebuilder-core`](https://github.com/martinjagodic/sitebuilder-core). A project here holds only branding, content, and customizations.

## Requirements

```bash
brew install hugo go node pnpm   # Node 22 or newer
```

`sitebuilder-core` must be checked out next to this repo:

```
Development/
├── sitebuilder-core/
└── sitebuilder-sandbox/
```

## Working on a project

The `./sb` script points Hugo at your local core checkout, so changes to core show up here immediately.

```bash
./sb new new-site            # scaffold a project
cd new-site && pnpm install
cd .. && ./sb dev new-site   # http://localhost:1313
```

| Command | Does |
| --- | --- |
| `./sb new <name>` | Scaffold a project wired to the local core |
| `./sb dev <name>` | Run the dev server |
| `./sb build <name>` | Lint + production build |
| `./sb lint <name>` | Lint only |

Set `SITEBUILDER_CORE` if your core checkout is somewhere else.

## Setting up a new prototype

1. `./sb new <name>` and `pnpm install` inside it
2. Fill in `config/_default/hugo.toml` — title, baseURL, branding, `mediaPrefix`, `[cms]`
3. Drop the logo in `static/media/brand/`, write `content/`
4. Brand-only CSS goes in `assets/styles/_custom.scss`

The CMS config is rendered by Hugo on every build from the schema in sitebuilder-core — there is nothing to generate and nothing to commit. It is local-only for now: run `npx decap-server` next to the dev server and open `/admin`. Uploads land in `static/media/uploads`.

When a site is ready to go live, connect it in the [Decap Turbo](https://decapcms.org/docs/turbo-connecting-a-site/) dashboard and set `cms.backend = "turbo-github"` and `cms.turboSiteId` in `hugo.toml`. Connect it to this repo; the build prefixes the CMS paths with the project's folder.

## Promoting to a client

When a prototype becomes a paying customer:

```bash
cd <name>
pnpm exec sitebuilder promote     # swap the local core dep for the published one
hugo mod tidy && pnpm install
```

Then move the folder into a new `sitebuilder-client-<name>` repo and point Cloudflare Pages at it:

| Setting | Value |
| --- | --- |
| Build command | `pnpm run build` |
| Output directory | `public` |
| `GITHUB_TOKEN` | PAT with `repo` scope — core is private |
| `HUGO_VERSION` | `0.166.0` |
| `GO_VERSION` | `1.27.1` |
| `NODE_VERSION` | `24` |

Cloudflare Pages detects `pnpm-lock.yaml` and installs with pnpm automatically.

If the site is connected to Decap Turbo, change its repo in the Turbo dashboard to the new one. Nothing in the project changes: the CMS paths drop the folder prefix on their own once the project is the repo root.
