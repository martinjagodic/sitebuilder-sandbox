---
name: leads
description: Manage the sitebuilder sales pipeline in leads/leads.json — re-evaluate existing prospects, fetch new ones (capped at 20), and move businesses between prospects, in-progress, and active-clients as deals progress. Use when asked to find/refresh leads, search for the next lead, or move a business between pipeline stages.
---

# Leads pipeline

Maintains `leads/leads.json` in this repo (`sitebuilder-sandbox`) — a lead pipeline for pitching Hugo/Decap sites built on `sitebuilder-core` to small businesses.

Three lists, one file:

- **`prospects`** — candidate businesses worth pitching, capped at **20**.
- **`in_progress`** — a prospect you've started actually working/pitching. Removed from `prospects` so `refresh` never re-suggests or re-researches it.
- **`active_clients`** — converted, paying. Same exclusion.

Both `in_progress` and `active_clients` double as **seeds**: businesses in the same industry or area as one that already converted are more likely to convert too, so `refresh` should search near them, not just cold-scan the region.

## Actions

Read `args` for the action. Default to `refresh` when empty.

- `refresh` (default) — re-evaluate every existing prospect, drop stale ones, then search for new ones until `prospects` is back at 20.
- `move "<business name>" in-progress` — move a business from `prospects` to `in_progress` (fuzzy-match by name; ask the user to disambiguate if more than one plausible match).
- `move "<business name>" active` — move a business to `active_clients` from `in_progress` if it's there, else from `prospects`.
- `list` — print the current state of all three lists (grouped, with conversion_potential shown for prospects). No research, no writes.

After any `move`, print the updated counts (`prospects: n/20`, `in_progress: n`, `active_clients: n`).

## Entry schema

Every entry (in any of the three lists) uses this shape:

```json
{
  "id": "kebab-case-slug",
  "business_name": "...",
  "short_description": "...",
  "location": "...",
  "business_type": "...",
  "legal_form": "d.o.o. | s.p. | unknown | ...",
  "has_existing_site": true,
  "existing_site_url": "..." ,
  "existing_site_quality": "none | poor | mediocre | good",
  "revenue_last_3_years": {
    "currency": "EUR",
    "years": { "2025": 123456, "2024": null, "2023": null },
    "source": "bizi.si | ajpes | unavailable",
    "source_url": "...",
    "note": "..."
  },
  "content_availability": {
    "level": "high | medium | low",
    "sources": ["url or description", "..."],
    "notes": "..."
  },
  "conversion_potential": {
    "score": "high | medium | low",
    "reasoning": "one sentence, tied to the factors above"
  },
  "source_urls": ["..."],
  "first_found": "YYYY-MM-DD",
  "last_evaluated": "YYYY-MM-DD",
  "notes": "free text — preserve verbatim across refreshes, append rather than overwrite"
}
```

Never fabricate a revenue figure or a content/site-quality rating. If you couldn't verify something, leave it `null`/`"unavailable"` with a `note` saying so — a missing fact is fine, an invented one isn't.

## `refresh` procedure

This is research-heavy (up to 20 site checks plus new-lead search) — do the legwork via the Agent tool rather than burning the main conversation's context, then merge the results into the JSON yourself so the cap/cull/dedupe logic stays in one place.

1. Read `leads/leads.json`.
2. In parallel (single message, two Agent calls, `run_in_background: false` since you need both before writing the file):
   - **Agent A — re-evaluate existing prospects.** Give it the current `prospects` array. For each: re-check the site (if any) and the content sources listed — has the site improved, has the business gone quiet/closed, is there new content available (Facebook/Instagram/Google Business/reviews)? Also have it look up `revenue_last_3_years` for each via bizi.si (search `"<business name>" bizi.si`, fetch the page — free previews usually show a few years of prihodki/revenue) or AJPES (ajpes.si) as fallback. Sole proprietors (s.p.) often have no public filing — that's an expected "unavailable", not a failure. Ask it to return, per business, the updated field values plus a one-line verdict: `keep` or `drop (reason)`.
   - **Agent B — find new prospects.** Give it: the search region priority (**Kranj, then the wider Gorenjska region, then Ljubljana** — stop expanding outward once enough good candidates turn up), the full list of names+locations already in `prospects` + `in_progress` + `active_clients` (to exclude — dedupe by name and by site domain, fuzzy match on name is fine), and the same evaluation criteria used originally: existing content available online (site/Facebook/Instagram/Google reviews), a "standard" business with no unusual functional requirements (no e-commerce/booking/multi-language complexity), and a bad/missing/outdated current site. Tell it to treat any business currently in `in_progress`/`active_clients` as a **seed**: search for other businesses in the same industry and/or same immediate area first, since related businesses convert at a higher rate — then fall back to general regional search. Ask for enough candidates to refill `prospects` to 20 after drops, each with the same fields as the schema above (revenue can be left unresearched at discovery time — Agent A's lookup pattern applies on the *next* refresh).
3. Merge: apply Agent A's updates in place (bump `last_evaluated`, keep `notes` and `first_found` untouched, append rather than replace free-text `notes`); drop everything Agent A flagged `drop` (auto-drop per standing instruction — no confirmation needed, just record the reason in the run summary); add Agent B's new candidates, skipping any that collide with `in_progress`/`active_clients`/surviving `prospects`.
4. Recompute `conversion_potential` for anything whose inputs changed, using the heuristic below.
5. If `prospects` now exceeds 20, drop the lowest `conversion_potential` entries (low before medium) until back at 20 — never drop from `in_progress` or `active_clients` this way.
6. Write `leads/leads.json` back (bump `last_refresh`).
7. Print a short summary: dropped (with reason), added, and the current top 5 by conversion_potential.

## Conversion potential heuristic

Not a formula — a judgment call weighing:

- **High** — no site or a genuinely bad one (clear before/after story) **and** decent content already available online **and** a standard business type **and** some sign of real ongoing activity (recent posts/reviews, plausible revenue).
- **Medium** — mixed signals: one strong factor offset by another (e.g. good content but the site is merely mediocre, or a standard business but content is thin, or revenue/activity is unclear either way).
- **Low** — already has a reasonably modern/functional site (no before/after story to sell), or isn't really a commercial prospect (dormant, nonprofit, no plausible budget), or needs meaningfully more than a content-forward site (e-commerce, booking engine, heavy custom functionality).

A short `reasoning` string should always say *which* of these tipped the score, not just restate the score.

## Notes on data sources

- **Revenue**: prefer `bizi.si` (search `"<name>" bizi.si`, most Slovenian companies have a free page showing a few years of revenue/employees) since it's easy to fetch directly. Cross-check or fall back to AJPES (ajpes.si) for d.o.o./gospodarske družbe, which must file annual reports. Sole proprietors (s.p.) and very small/registered-society entities frequently have nothing public — record that as the reason, don't guess.
- **Content availability**: check the business's own site (if any), Facebook page, Instagram, and Google Business/Maps reviews. "High" means there's enough real text/photos to build a first draft without writing everything from scratch; "low" means a name and address is roughly all that exists.
- **Existing site quality**: judge on mobile-friendliness, apparent last-updated date, and whether it already tells a complete story (menu/services/photos/contact) — not on visual polish alone. A site that already does its job well is a *weak* prospect even if it looks a bit dated, because there's no compelling before/after.
