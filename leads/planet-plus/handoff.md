# Planet Plus: prototype handoff

Prototype built 25 Sep 2026 in `sitebuilder-sandbox/planet-plus/`. It migrates
the live planetplus.si (built by us; repo `planetplus-www`) to
sitebuilder-core. It keeps the same URLs, the client's own copy and the
photos the live site shows, in a new dark, warm design. Sources for every fact
are in [research.md](research.md); photo sources are in
[media/manifest.md](media/manifest.md).

**On Bunny:** media is uploaded to the shared zone under `planet-plus/`
(flat, except `brand/` for the logo) and served through `bunnyUrl`, inherited
from core. No Decap Turbo yet, so the CMS still runs through
`npx decap-server`.

Preview: `./sb dev planet-plus`, then open http://localhost:1313. For the CMS,
also run `npx decap-server` inside `planet-plus/` and open `/admin/`.

Regenerate: `leads/planet-plus/media/prepare.py` (media from the client folder)
and `leads/planet-plus/generate_content.py` (pages and menu from
`planetplus-www` and the client's `BESEDILA ZA SPLET.docx`).

## What's on it

| Page | URL | Sections |
| --- | --- | --- |
| Domov | `/` | The studio video over a photo, with "Razmišljamo, prisluhnemo in ustvarjamo lepe stvari" and two buttons; O nas with the company facts; the three services, numbered; 6 category cards; reference photos; Google rating and 2 reviews; the partner logo wall; "Obiščite naš salon" band |
| Prodajni program | `/prodajni-program/` | Title band, cards for all 11 categories, consultation band |
| 11 categories | `/prodajni-program/<slug>/` | Photo hero, the client's text beside a photo, numbered points where the client gave some (kuhinje, vrata, zasteklitve), gallery, the category's partner logos with "Več na" links, consultation band |
| Partnerji | `/partnerji/` | Title band, all 12 logos linking to the brands |
| Reference | `/reference/` | Photo hero, three project galleries |
| Kontakt (new) | `/kontakt/` | Photo, call and email buttons; address, hours, directions and an OSM map |

Every page has the header with the Prodajni program dropdown and the call
button, and a footer with contact details, hours, social links and the
client's EmailOctopus newsletter form. The site sends schema.org
`FurnitureStore` data to Google.

URLs match the live site, so no redirects are needed. `/kontakt/` is new; the
live `/akcija/` pages already return 404.

## Design

- Near-black `#121110` with a brass accent `#c8a26b`. Text is warm off-white.
  Every text colour passes WCAG AA; buttons use dark text on brass (7.9:1).
- EB Garamond for headings and Manrope for text, both from Bunny Fonts.
  Cormorant Garamond was the first pick, but its lowercase caron floats above
  š, č and ž. The comparison is in [font-comparison.png](font-comparison.png).
- Swiss 721, the Bitstream font the live site hosts itself, is gone, and with
  it the question of its webfont licence.

## Real, placeholder or unconfirmed

| Item | Status |
| --- | --- |
| All page copy | The client's own text from the live site and `BESEDILA ZA SPLET.docx`. The only changes are the fixes listed below. The kuhinje second paragraph and the five zasteklitve points come from the docx; the live site doesn't show them. |
| SEO descriptions, section headings, alt texts | Written by us, from the client's text and the photos |
| Address, email, social links | Verified: the current site plus the registries |
| Phone +386 1 516 16 63 | The current site, Oikos and Nidi list this number. **Google shows 051 330 002 and the registries 051 330 001. Confirm, then correct Google.** |
| Hours | Google and the directories agree. The note "Torek–četrtek od 16. do 18. ure po dogovoru" is our reading of "(po dogovoru)". **Confirm.** |
| Map pin 46.1182203, 14.4547834 | The Google pin, which sits on building 40b. The registries say 40. **Confirm 40 or 40b.** |
| "Podjetje deluje od leta 2002 … 400 m² razstavnih površin" | Taken from the register (entry 17 Jul 2002) and from their own 2011 showroom opening notice. **Confirm the 400 m² is still right.** |
| Reviews | Google 4.7 from 15. Two verbatim reviews, from Apr 2018 and Jan 2019. The third text review is by a Trampuš, so it's left out. |
| Dealer claims | Only the client's own words: "predstavnik … Metalglas", "vrhunskega italijanskega proizvajalca Doimo Cucine". Oikos, Nidi and Fiora list Planet Plus on their dealer pages; Novamobili, Varaschin and Doimo don't. The site says "partnerji", never "uradni prodajalec". |
| Reference "Projekt 1" credit "Stanovanje v Spektri · fotografije: Ana Skobe" | From the file names only. **Confirm, and ask for permission to credit.** |
| Photos | The live selection, from the client's folder. Most are manufacturer press photos, used as their dealer. Showroom photos: **none exist.** The studio video is Novamobili's "Home System" brand film. |
| Dnevne sobe, Kopalniški elementi | No text on the live site or in the docx, so these pages are photos, logos and links |
| Category videos (11) | Not used. Only the home video is (3.4 MB, re-encoded). The rest return with Bunny Stream. |

## Fixed on the way

- Two files the live site links are 404 on Cloudinary: the Reference hero and
  the Fiora logo. Both are now served from the client's originals.
- The Instagram link had a trailing `%20`.
- Removed the stale "27.10–31.10 ZAPRTO" (no year) from the hours.
- Vrata showed three photos twice; each is shown once now.
- Typos: "formmaldehida", "standardov,odpornost", "ambient ki", "3d
  vizualizaciji", double spaces. "So vedno elegantna…" on Zasteklitve reads
  "Zasteklitve so vedno elegantna…" now that it's no longer under the page
  title. Brand names follow the brands' own spelling: Novamobili, Softline.
- The site description said "italijanskih proizvajalcev". Softline is Danish,
  so it now follows the client's own "evropskih".

## Questions for the owner

Ready to paste:

> 1. Katera telefonska številka naj bo na strani: 01 516 16 63, 051 330 002 (Google) ali 051 330 001 (poslovni registri)? Nato uskladimo še Google.
> 2. Kaj pomeni »po dogovoru« pri delovnem času od torka do četrtka? Je obisk med 16. in 18. uro samo po dogovoru?
> 3. Je naslov Kajakaška cesta 40 ali 40b? Kako vas stranke najdejo: kateri vhod, kje parkirajo?
> 4. Ali salon še vedno meri 400 m²? Lahko zapišemo, da podjetje deluje od leta 2002?
> 5. Nam lahko pošljete nekaj fotografij salona in ekipe? Stranke rade vidijo, kam prihajajo.
> 6. Kateri oblikovalci svetujejo v salonu? Jih lahko predstavimo z imenom in fotografijo?
> 7. Kdo je oblikoval projekt Stanovanje v Spektri? Smemo navesti fotografinjo Ano Skobe? Kako naj poimenujemo Projekt 2 in Projekt 3?
> 8. Za katere znamke ste uradni prodajalec ali zastopnik? Naj dodamo še Kave Home?
> 9. Nam lahko pošljete nekaj novejših mnenj strank?
> 10. Imate kratek opis za dnevne sobe in kopalniške elemente?
> 11. Kako je z dostavo, montažo in 3D izrisom: so vključeni v ceno? Do kod dostavljate?
> 12. Imate logotip v vektorski obliki (AI, SVG, PDF)?

## Talking points for the pitch

- The current site has no contact page, and the contact details sit on the
  home page next to a closure notice with no year. The new one has a Kontakt
  page with a map, directions and hours, and a call button on every page.
- Two images on the live site are broken today (Reference hero, Fiora logo).
- Google shows a different phone number from the site. Fixing both at once is
  a quick win.
- Facts now in one place: the address, hours and phone edited once in the CMS
  update the header, footer, contact page and Google's business data.
- Product categories are in a dropdown and linked from the home page, so a
  visitor reaches kuhinje or vrata in one tap.
- The design system is maintained centrally: new modules and fixes reach the
  site with the next build, without a redesign.
- 4.7★ on Google shows nowhere on the current site; now it does.

## Before going live

- [ ] Owner answers (questions above), especially the phone and hours
- [ ] Photo rights: confirm the press photos may be used, or replace them (manifest)
- [ ] Showroom photos, and designer photos if they want them
- [ ] Vector logo, then a proper favicon
- [x] Upload media to Bunny and remove `bunnyUrl = ""`. Done 25 Sep 2026: all files uploaded flat under `planet-plus/` (brand logo under `planet-plus/brand/`), local copies removed from the repo.
- [ ] Category videos on Bunny Stream, if they want them back
- [ ] EmailOctopus: its form loads Google reCAPTCHA on every page, and its consent text and button fail contrast (Lighthouse). Set the form colours in the client's EmailOctopus account, and list reCAPTCHA in the privacy notice.
- [ ] Decap Turbo site connected (`cms.backend`, `cms.turboSiteId`)
- [ ] Move the domain from Netlify to Cloudflare Pages. The URLs are the same, so no redirects are needed.
- [ ] Correct the phone on Google, and ask Oikos, Nidi and Fiora to fix the postcode (they show 1000, not 1211)

## Tasks for other agents

**Design agent**

- Vectorise the wordmark (condensed grotesk, PLANET light and PLUS bold) and
  export a white version for the dark header. Draw a favicon from it; the
  current one is a stand-in brass "P".
- Normalise the partner logos to one canvas and optical size. They arrive
  with different padding: nidi looks huge and Metalglas tiny. The MD House
  file shows only "md h".
- Art-direct a showroom shoot: the salon interior, consultation at the
  material table, a designer at the 3D screen.

**Content agent**

- Texts for Dnevne sobe and Kopalniški elementi once the owner answers.
- Names and one-paragraph stories for the three reference projects.
- A short team section if the owner names the designers.
- Review the alt texts, which were written from contact sheets.
- A Google Business Profile description, and the phone correction there.
