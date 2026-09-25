# Pizzerija Gorenc: prototype handoff

Prototype built 24 Sep 2026 in `sitebuilder-sandbox/pizzerija-gorenc/`. Sources
for every fact are in [research.md](research.md); photo sources and rights are
in [media/manifest.md](media/manifest.md).

Preview: `./sb dev pizzerija-gorenc`, then open http://localhost:1313 (or pass
`--port`).

## What's on it

| Page | Sections |
| --- | --- |
| Domov | Food hero with "Poglejte jedilnik" and "Rezervirajte mizo"; four highlights (wood-fired oven, covered terrace, playground, car park); slider of 8 pizzas with ingredients; the oven story; 3 verbatim reviews and the Google rating; call and Wolt band |
| Jedilnik | All 59 food items from Wolt in 6 categories, with ingredients and prices, sticky category chips, vegetarian and spicy tags; Wolt and call band |
| Kontakt | Building photo, call and Instagram buttons; address, phone, email, opening hours, directions and OSM map |

Every page also has the header call button, a footer with contact, hours and
social links, and schema.org `Restaurant` data for Google.

## Real, placeholder or unconfirmed

| Item | Status |
| --- | --- |
| Address, phone, coordinates, wood-fired oven, terrace for 40, playground, car park, Wolt delivery 11:00–21:30 | Verified, multiple sources |
| Hours 11:00–23:00 daily | The owner-managed Google profile and 5 other sources say this; one stale najdi.si entry says 11–22. **Confirm.** |
| Email pizzerija.gorenc@siol.net | Listed on bizi.si and najdi.si. **Confirm it's still read.** |
| Menu prices | **Wolt prices, which include €0.80 packaging**, shown without a label as agreed. Replace with the printed dine-in menu, which has two price columns per pizza (the price list supports size columns). |
| Menu text | Wolt's descriptions, with three typos fixed ("Pelat", "suha salami", "parezan"). Dine-in-only dishes (lasagne, tortellini, squid) get one line in the menu note. |
| Reviews | Verbatim, attributed, all 5★ or 10/10. Dates are approximate for Google ("2026"). |
| Photos | None are cleared yet. See the rights table in the manifest. |
| Story, founding year, family | **Not on the site.** Nothing verifiable was found. |
| Lunches (malice), student vouchers, events | **Left out.** They exist or existed, but price and hours are unknown. |

## Questions for the owner

Ready to paste:

> 1. Ali je delovni čas še vedno vsak dan od 11. do 23. ure? Do kdaj je odprta kuhinja?
> 2. Nam lahko pošljete trenutni jedilnik s cenami v lokalu? Kaj pomenita dva stolpca cen pri picah (velikosti)?
> 3. Kakšna je ponudba malic: cena, ura, ali je vključena juha ali solata? Sprejemate še študentske bone?
> 4. Katero e-pošto naj objavimo? Je pizzerija.gorenc@siol.net še v uporabi?
> 5. Kako želite sprejemati rezervacije: po telefonu, na Instagramu ali s spletnim obrazcem?
> 6. Ali organizirate zabave, rojstne dneve ali večje skupine? Koliko je sedežev v notranjosti?
> 7. Imate pico brez glutena ali seznam alergenov?
> 8. Od kdaj obstaja picerija in kako je nastala? Od kod ime Gorenc in nagelj v logotipu?
> 9. Ali so fotografije jedi z Wolta vaše? Imate logotip v vektorski obliki (AI, SVG, PDF)?
> 10. Kakšna je vloga podjetja MTRI d.o.o., ki ga Wolt navaja kot ponudnika? Kdo naj bo naveden kot lastnik strani?

## Talking points for the pitch

- They have no website. Google's "Spletno mesto" button and its reservation
  link both point to a travel directory listing.
- Nearly 2,000 Google reviews at 4.5★, and none of that shows on anything
  they own.
- Recent reviews complain about prices. A clear menu online with dine-in
  prices answers that better than Wolt's, which include packaging.
- Every phone order or reservation from their own site skips the delivery
  platform.
- Foreign guests (a German couple on the way to Croatia, whose lost wallet
  with €150 was returned intact) suggest an English page as a later add-on.
- The owner can edit the menu, hours and photos in the CMS. Changing a price
  live in the meeting is a good demo.

## Before going live

- [ ] Dine-in menu and prices from the owner
- [ ] Hours and email confirmed
- [ ] Photo rights cleared or photos replaced (manifest table)
- [ ] Vector logo
- [ ] `bunnyUrl` set in core so images get resized per device (the hero is 455 KB now)
- [ ] Decap Turbo site connected (`cms.backend`, `cms.turboSiteId`)
- [ ] Custom domain on Cloudflare Pages

## Tasks for other agents

**Design agent**

- Vectorise the logo (the carnation emblem and wordmark are simple shapes), and
  export a horizontal lockup for the header and a square emblem for the favicon.
- Pick a hero crop for phones. The current flat-lay is cropped to the egg on
  the Gorenc pizza, which works, but a portrait shot would be stronger.
- Art-direct a replacement for the 2021 terrace photo and the Visit Kranj oven
  shot if their rights can't be cleared. Brief: summer terrace with guests;
  the oven burning with pizzas going in.
- Optional: 2–3 Instagram templates in the site's palette (red `#e01810`,
  green `#00a058`, cream `#f6efe3`, Bree Serif + Source Sans 3).

**Content agent**

- Turn the owner's answers into an "O nas" section once there's a story.
- Write the lunch (malice) block when the price and hours are known.
- Draft an English version of the three pages for tourists (only if the owner
  wants it).
- Write a Google Business Profile description, and reply templates for the
  recent negative reviews.
