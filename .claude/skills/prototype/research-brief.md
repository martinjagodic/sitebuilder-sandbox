# Research brief

Send this to a background general-purpose agent. Replace `<NAME>`,
`<LOCATION>`, `<ID>` and the known sources with values from the lead entry.

---

Research the business "<NAME>" in <LOCATION>. We are building a sales-pitch
prototype website for them, so we need every real fact and asset that exists
online. Never invent anything. If you can't verify a fact, say so explicitly.
A missing fact is fine; a made-up one is harmful.

Known starting sources: <source_urls from the lead>.

Also search for and check (WebSearch + WebFetch):

- Delivery and booking platforms first, for food businesses: Wolt, Glovo,
  foodora. They usually have the full priced menu with verbatim ingredients
  and a professional photo shoot. Note any packaging surcharge included in
  the prices.
- Google Maps / Google Business profile: rating, review count, opening hours,
  phone, address, photos, service flags (dine-in, takeaway, delivery…).
  Note whether the profile is owner-managed; if so, its hours outrank
  directories.
- The local tourist board's listing (e.g. Visit Kranj): often professional
  photos, with the photographer credited.
- Facebook and Instagram. Try spelling variants (Slovenian vs Italian vs
  English, with and without the legal form).
- bizi.si and AJPES (CompanyWall shows AJPES figures for free): legal entity
  name, legal form, owner/director, founding year, registered address,
  revenue for the last 3 years, employee count. List **every** entity tied
  to the address or named as merchant on a platform. Don't pick one; the
  user confirms which is the company of record.
- Industry platforms (for food: Wolt, Glovo, TripAdvisor, restavracije.si;
  for trades: mojmojster.net, najdi.si), plus local news mentions
- Anything that sets them apart: history, specialities, equipment,
  certifications, events, payment methods, parking, accessibility

Write everything under
`/Users/martinjagodic/Development/sitebuilder-sandbox/leads/<ID>/`:

1. `research.md` with these sections: Identity, Hours, Services, Offer (the
   full menu, price list or service list, transcribed verbatim in the original
   language, as a markdown table per category with the date and source of the
   prices), Reviews (the best 8–10 verbatim, with author first name or
   initial, date, source and rating, plus the aggregate per platform), Story
   (only what is actually stated somewhere), Social links, Company data, and
   Open questions (every fact a website would normally have that you could
   not find, or that sources contradict). Give the source URL for every fact.
2. Download every usable photo (product, interior, exterior, logo, signage,
   team) to `media/raw/` with curl, using a browser User-Agent. Get the largest
   size available (check srcset, strip WordPress `-300x200` suffixes). Skip
   icons, map tiles and unrelated ads. Use descriptive file names.
3. `media/manifest.md`: filename, what it shows, pixel size
   (`sips -g pixelWidth -g pixelHeight`), source URL, likely owner (business /
   directory / platform / photographer / guest), the date taken if known, and
   a quality flag. Flag dated photos (COVID masks, an old interior, a previous
   operator's signage).

Return a summary under 400 words: what's solid, what's missing, offer size,
photo count and quality, whether a logo exists, and the top questions for the
owner.
