#!/usr/bin/env python3
"""Generate the Planet Plus prototype's pages from the live site's content.

Copy comes verbatim from planetplus-www's front matter and the client's
"BESEDILA ZA SPLET.docx"; the only edits are the typo fixes in FIXES, which
the handoff lists. Images are the files media/prepare.py optimised, looked up
by their Cloudinary URL in media/map.json.

Writes content/, config/_default/menus.yaml in ../../planet-plus.
"""

import json
import os
import re
import subprocess
import unicodedata

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '../../planet-plus')
WWW = '/Users/martinjagodic/Development/planetplus-www'
DOCX = '/Users/martinjagodic/Desktop/Documents/Planet Plus/BESEDILA ZA SPLET.docx'
UPLOADS = os.path.join(SITE, 'static/media/uploads')

MEDIA = json.load(open(os.path.join(HERE, 'media/map.json')))
DOC = unicodedata.normalize('NFC', subprocess.run(['textutil', '-convert', 'txt', '-stdout', DOCX],
                                                  capture_output=True, text=True, check=True).stdout)

PHONE = 'tel:+38615161663'
EMAIL = 'mailto:info@planetplus.si'

# Obvious typos in the source text, fixed on the way through (listed in the
# handoff). Brand names follow the brands' own spelling.
FIXES = [
    ('standardov,odpornost', 'standardov, odpornost'),
    ('Ustvarimo ambient ki', 'Ustvarimo ambient, ki'),
    ('formmaldehida', 'formaldehida'),
    ('3d vizualizaciji', '3D vizualizaciji'),
    ('  ', ' '),
]
BRANDS = {'Nova Mobili': 'Novamobili', 'Soft Line': 'Softline'}


def fix(text):
    text = text.strip()
    for old, new in FIXES:
        while old in text:
            text = text.replace(old, new)
    return text


def doc(snippet):
    """A sentence or paragraph that must appear in the client's docx."""
    flat = re.sub(r'\s+', ' ', DOC)
    assert re.sub(r'\s+', ' ', snippet) in flat, f'not in docx: {snippet[:60]}'
    return fix(snippet)


def old(path):
    text = open(os.path.join(WWW, 'content', path), encoding='utf-8').read()
    # Some source text is decomposed (s + combining caron), which web fonts
    # draw as a floating accent. Compose it.
    return yaml.safe_load(unicodedata.normalize('NFC', text).split('---')[1])


def media(url):
    return MEDIA[url]


def img(url, alt):
    return {'src': media(url), 'alt': alt}


def is_portrait(url):
    out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight',
                          os.path.join(UPLOADS, os.path.basename(media(url)))],
                         capture_output=True, text=True).stdout
    w, h = map(int, re.findall(r': (\d+)', out))
    return h > w


def brand(name):
    return BRANDS.get(name, name)


def cta():
    return {
        'type': 'cta',
        'title': 'Svetovanje v salonu',
        'text': fix(old('_index.md')['quoteContent']['content'].split('STROKOVNO SVETOVANJE')[1]
                    .split('3D IZRIS')[0]),
        'button': {'text': 'Pokličite', 'href': PHONE, 'icon': 'phone'},
        'secondaryButton': {'text': 'Pišite nam', 'href': EMAIL, 'icon': 'mail'},
        'background': 'primary',
    }


def numbered(text):
    """'01 KAKOVOST\\n\\n( vlagoodporna ...)' blocks -> feature items."""
    items = []
    for block in re.split(r'\n(?=\d\d )', text.strip()):
        lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
        title = re.sub(r'^\d\d\s+', '', lines[0])
        title = title[0] + title[1:].lower()
        title = re.sub(r'\boikos\b', 'Oikos', title)
        item = {'title': fix(title)}
        if len(lines) > 1:
            detail = fix(lines[1].strip('() '))
            detail = detail[0].upper() + detail[1:]
            detail = re.sub(r'ral in ncs-u', 'RAL in NCS', detail)
            item['text'] = detail + '.'
        items.append(item)
    return items


# ---------------------------------------------------------------- categories

# Alt text per optimised file, written from the photos.
ALT = {
    'kuhinje-naslovna': 'Kuhinjski pult Doimo Cucine z vazo v jutranji svetlobi',
    'kuhinje-ambient': 'Kuhinjske fronte z marmornim vzorcem in lesene police',
    'kuhinje-partner': 'Temna kuhinja Doimo Cucine z otokom',
    'jedilnice-naslovna': 'Jedilnica s temno mizo in stoli',
    'jedilnice-ambient': 'Stol in okrogla mizica, pogled od zgoraj',
    'jedilnice-partner': 'Jedilna miza iz tikovine Kristalia na leseni terasi',
    'sedezne-garniture-naslovna': 'Svetla zaobljena sedežna garnitura v dnevni sobi',
    'sedezne-garniture-ambient': 'Fotelj in klop ob velikem oknu',
    'sedezne-garniture-detajl': 'Usnjen kavč v temnem prostoru',
    'sedezne-garniture-partner': 'Fotelj ob stenskih policah z vitrino',
    'dnevne-sobe-naslovna': 'Dnevna soba s fotelji, mizico in policami',
    'dnevne-sobe-ambient': 'Temna stenska knjižna polica',
    'dnevne-sobe-detajl': 'Okrogle klubske mizice, pogled od zgoraj',
    'dnevne-sobe-partner': 'Stenska omara z vitrinami in televizorjem',
    'garderobne-omare-naslovna': 'Spalnica s stekleno garderobno omaro',
    'garderobne-omare-ambient': 'Zaobljena zelena garderobna omara z nišo',
    'garderobne-omare-detajl': 'Notranjost predala garderobne omare s predelki',
    'garderobne-omare-partner': 'Okroglo ogledalo in komoda ob oknu',
    'postelje-in-nocne-omarice-naslovna': 'Spalnica z oblazinjeno posteljo in garderobno omaro',
    'postelje-in-nocne-omarice-ambient': 'Oblazinjena postelja na mehki preprogi',
    'postelje-in-nocne-omarice-detajl': 'Spalnica z modro oblazinjeno posteljo pod strešnim oknom',
    'postelje-in-nocne-omarice-partner': 'Nočna omarica z zaobljenim predalom',
    'vrata-naslovna': 'Temna vrata z marmornim vzorcem, poravnana s steno',
    'vrata-ambient': 'Lesena vrata, poravnana s steno, v hodniku',
    'vrata-detajl': 'Steklena krilna vrata s tankim okvirjem',
    'vrata-partner': 'Vhodna vrata Oikos v visokem prostoru',
    'vrata-galerija-steklena-vrata-1': 'Nihajna steklena vrata Midori',
    'vrata-galerija-steklena-vrata-2': 'Nihajna steklena vrata Midori v delovnem kotičku',
    'vrata-galerija-steklena-vrata-3': 'Steklena vrata Divina s prečkami',
    'vrata-galerija-steklena-vrata-4': 'Steklena stena Divina z vrati',
    'vrata-galerija-steklena-vrata-6': 'Drsna vrata Divina z lesenimi lamelami',
    'vrata-galerija-lesena-vrata-2': 'Lesena vrata Invisible v dnevni sobi',
    'kopalniski-elementi-naslovna': 'Kopalnica z umivalnikom in okroglim ogledalom',
    'kopalniski-elementi-ambient': 'Umivalnik Fiora v obliki sklede',
    'kopalniski-elementi-detajl': 'Tuš kotiček z nišo',
    'kopalniski-elementi-partner': 'Kopalniški element s predalom in umivalnikom',
    'zasteklitve-naslovna': 'Steklena krilna vrata med spalnico in garderobo',
    'zasteklitve-ambient': 'Steklena stena s prečkami med kuhinjo in dnevno sobo',
    'zasteklitve-partner': 'Tuš kabina s steklenimi vrati',
    'zasteklitve-galerija-kopalnice-1': 'Steklena tuš kabina ob marmorni steni',
    'zasteklitve-galerija-kopalnice-2': 'Tuš kabina s tankimi črnimi profili',
    'zasteklitve-galerija-kopalnice-3': 'Kopalnica s tušem in umivalnikom',
    'otroske-in-mladinske-sobe-naslovna': 'Mladinska soba z oblazinjeno posteljo in pisalno mizo',
    'otroske-in-mladinske-sobe-ambient': 'Otroka se igrata ob steni',
    'otroske-in-mladinske-sobe-detajl': 'Mladinska soba v mansardi',
    'otroske-in-mladinske-sobe-partner': 'Pisalni kotiček z belim stolom in policami',
    'okovje-naslovna': 'Steklena stena s kovinskimi profili ob stopnišču',
    'okovje-ambient': 'Profil steklenega nadstreška',
    'okovje-detajl': 'Okovje za steklena vrata',
    'okovje-partner': 'Steklena vrata v rdečem hodniku',
}


def alt(url):
    return ALT[os.path.splitext(os.path.basename(media(url)))[0]]


def pic(url):
    return {'src': media(url), 'alt': alt(url)}


def links(*pairs):
    return 'Več na: ' + ' · '.join(f'[{label}]({href})' for label, href in pairs)


# Per category: what the live site and the docx give, arranged into modules.
CATEGORIES = {
    'kuhinje': dict(
        description='Kuhinje po meri italijanskega proizvajalca Doimo Cucine z individualnim izborom materialov, barv in elementov. Svetovanje in načrtovanje v salonu.',
        extra=doc('Od sodobno zasnovane minimalistične kuhinje do klasične tradicionalne kuhinje. Kuhinje Doimo Cucine s svojim modularnim sistemom omogočajo različne postavitve od U do L form, otokov in polotokov. Kuhinjo prilagodimo vašemu prostoru, vašim zahtevam in željam. Naj kuhinja s svojo funkcionalnostjo in estetsko dovršenostjo postane osrednji element vašega doma.'),
        features_title='Prednosti kuhinj Doimo Cucine',
        brand_block=('Doimo Cucine', 'Več na doimocucine.com', 'https://www.doimocucine.com/en/'),
    ),
    'jedilnice': dict(
        description='Jedilniške mize s čistimi modernimi linijami ter moderni, barviti in funkcionalni stoli proizvajalcev Novamobili in Kristalia.',
        links=links(('novamobili.it', 'https://www.novamobili.it/en/tables'),
                    ('kristalia.it', 'https://www.kristalia.it/en/kind/tables/')),
    ),
    'sedezne-garniture': dict(
        description='Elegantni kavči in modularne sedežne garniture s snemljivimi, pralnimi materiali proizvajalcev Softline, Novamobili in Kristalia.',
        links=links(('softlinefurniture.com', 'https://softlinefurniture.com/en/products/sofas/'),
                    ('novamobili.it', 'https://www.novamobili.it/en/sofas')),
    ),
    'dnevne-sobe': dict(
        description='Pohištvo Novamobili za dnevne sobe: stenske omare, police, klubske mizice in fotelji v salonu Planet Plus v Ljubljani.',
        links=links(('novamobili.it', 'https://www.novamobili.it/en/living-room')),
    ),
    'garderobne-omare': dict(
        description='Modularne garderobne omare in garderobne sobe z drsnimi ali krilnimi vrati proizvajalcev Novamobili, Kristalia, MD House in Cinquanta3.',
        links=links(('novamobili.it', 'https://www.novamobili.it/en/bedroom')),
    ),
    'postelje-in-nocne-omarice': dict(
        description='Oblazinjene dizajnerske postelje z mehkim vzglavjem in postelje iz lesnega furnirja, prilagojene vašim zahtevam. Novamobili in Kristalia.',
        links=links(('novamobili.it', 'https://www.novamobili.it/en/beds')),
    ),
    'vrata': dict(
        description='Notranja vrata po meri, lesena ali steklena, drsna ali krilna, ter vhodna vrata italijanskega proizvajalca Oikos.',
        features_title='Izbira vrat',
        gallery_title='Steklena, lesena in vhodna vrata',
        # The live page repeats three photos; each is shown once here.
        skip=['vrata-galerija-lesena-vrata-1', 'vrata-galerija-steklena-vrata-5', 'vrata-galerija-lesena-vrata-4'],
        partner_in_gallery=True,
        links=links(('oikos.it', 'https://oikos.it/en/')),
    ),
    'kopalniski-elementi': dict(
        description='Kopalniški elementi Fiora: umivalniki, pohištvo in tuš kotički v salonu pohištva Planet Plus v Ljubljani.',
    ),
    'zasteklitve': dict(
        description='Zasteklitve po meri s kaljenim steklom: poslovni prostori, tuš kabine, steklene ograje, zložljive steklene stene in stekleni nadstreški.',
        features_title='Zasteklitve po meri',
        features=[{'title': t} for t in ['Zasteklitve poslovnih prostorov', 'Zasteklitve tuš kabine',
                                         'Steklene ograje', 'Zložljive steklene stene', 'Stekleni nadstreški']],
        features_source=doc('01 ZASTEKLITVE POSLOVNIH PROSTOROV 02 ZASTEKLITVE TUŠ KABINE 03 STEKLENE OGRAJE 04 ZLOŽLJIVE STEKLENE STENE 05 STEKLENI NADSTREŠKI'),
        gallery_title='Kopalnice',
        # Near-identical to the last photo in the Vrata gallery.
        skip=['zasteklitve-detajl'],
        partner_in_gallery=True,
    ),
    'otroske-in-mladinske-sobe': dict(
        description='Otroške in mladinske sobe Nidi po meri: svetle in razigrane, iz lesa in materialov, prijaznih do okolja in alergikov.',
        links=links(('nidi.it', 'https://nidi.it/en')),
    ),
    'okovje': dict(
        description='Okovje za steklo italijanskega proizvajalca Metalglas: rešitve za steklena vrata, stene in nadstreške za dom in poslovni prostor.',
        links=links(('metalglas.it', 'https://metalglas.it/?change_lang=en')),
    ),
}


def category(slug, spec):
    src = old(f'prodajni-program/{slug}.md')
    q = src.get('quoteContent') or {}
    partners = src.get('imagePartners') or {}
    names = [brand(n) for n in partners.get('list') or []]
    modules = []

    body = fix(src.get('description') or '')
    if slug == 'zasteklitve':
        body = 'Zasteklitve so' + body[len('So'):]
    if spec.get('extra'):
        body += '\n\n' + spec['extra']
    body = '\n\n'.join(re.split(r'\n+', body))  # a line break in the source starts a paragraph

    used = [src['image']['src']]
    if body and q.get('image'):
        modules.append({
            'type': 'imageText',
            'eyebrow': ' · '.join(names),
            **({'title': q['title'].replace('...', '…')} if q.get('title') else {}),
            'body': body,
            'image': pic(q['image']['src']),
            'portrait': is_portrait(q['image']['src']),
        })
        used.append(q['image']['src'])

    items = spec.get('features') or (numbered(q['content']) if q.get('content') else None)
    if items:
        modules.append({'type': 'features', 'title': spec['features_title'], 'numbered': True,
                        'items': items, 'background': 'surface'})

    if spec.get('brand_block'):
        name, label, href = spec['brand_block']
        modules.append({
            'type': 'imageText', 'eyebrow': 'Partner', 'title': name, 'reverse': True,
            'body': fix(partners['content']),
            'image': pic(partners['image']['src']),
            'button': {'text': label, 'href': href},
        })
        used.append(partners['image']['src'])

    gallery = []
    candidates = [q.get('image', {}).get('src'), q.get('imageCenter', {}).get('src')]
    if not spec.get('brand_block'):
        candidates.append(partners.get('image', {}).get('src'))
    for g in src.get('galleries') or []:
        candidates += [i.get('src') for i in g.get('items') or []]
    if spec.get('partner_in_gallery'):
        candidates.remove(partners['image']['src'])
        candidates.append(partners['image']['src'])
    for url in candidates:
        stem = url and os.path.splitext(os.path.basename(media(url)))[0]
        if url and url not in used and stem not in spec.get('skip', []) and pic(url) not in gallery:
            gallery.append(pic(url))
            used.append(url)
    if gallery:
        modules.append({'type': 'gallery', 'eyebrow': src['title'], 'title': spec.get('gallery_title', 'Navdih'),
                        'items': gallery})

    if not spec.get('brand_block'):
        modules.append({'type': 'partners', 'eyebrow': 'Partnerji',
                        'title': 'Proizvajalci' if len(names) > 1 else names[0],
                        **({'description': spec['links']} if spec.get('links') else {}),
                        'names': names})

    modules.append(cta())
    return {
        'title': src['title'],
        'weight': src['weight'],
        'description': spec['description'],
        'image': pic(src['image']['src']),
        'hero': {'variant': 'overlay', 'eyebrow': 'Prodajni program'},
        'modules': modules,
    }


# --------------------------------------------------------------------- pages

def home():
    src = old('_index.md')
    q = src['quoteContent']['content']
    services = []
    for title in ['CELOVIT PREGLED PONUDBE', 'STROKOVNO SVETOVANJE', '3D IZRIS OPREME']:
        text = q.split(title)[1]
        for nxt in ['STROKOVNO SVETOVANJE', '3D IZRIS OPREME']:
            text = text.split(nxt)[0]
        services.append({'title': (title[0] + title[1:].lower()).replace('3d', '3D'), 'text': fix(text)})
    about = fix(src['description'])
    about = about.replace(' Vizija podjetja', '\n\nVizija podjetja')
    # Company register (2002) and the showroom's opening notice on their old
    # site (400 m², 2011): confirm with the owner.
    about += '\n\nPodjetje deluje od leta 2002, v salonu na Kajakaški cesti 40 pa vas pričakamo na 400 m² razstavnih površin.'
    gallery_text = fix(src['gallery']['text'])
    refs = old('reference.md')['galleries']
    return {
        'title': 'Planet Plus',
        'linkTitle': 'Domov',
        'description': 'Salon pohištva v Ljubljani: notranja oprema priznanih evropskih proizvajalcev, strokovno svetovanje in 3D izris opreme.',
        'image': {'src': media(src['image']['src']), 'alt': 'Ženska za delovno mizo v temnem prostoru z velikim oknom'},
        'hero': {
            'variant': 'overlay',
            'eyebrow': 'Salon pohištva · Ljubljana',
            'title': fix(src['quoteContent']['title']).replace('...', ''),
            'description': 'Notranja oprema priznanih evropskih proizvajalcev in svetovanje izkušenih oblikovalcev interierja.',
            'video': '/media/uploads/domov-video.mp4',
            'button': {'text': 'Prodajni program', 'href': '/prodajni-program/'},
            'secondaryButton': {'text': 'Obiščite salon', 'href': '/kontakt/'},
        },
        'modules': [
            {'type': 'imageText', 'eyebrow': 'O nas', 'title': 'Kreativnost, svežina in dolgoletna praksa',
             'body': about,
             'image': {'src': media(src['quoteContent']['image']['src']),
                       'alt': 'Izbiranje vzorcev tkanin in materialov ob katalogu'},
             'portrait': True},
            {'type': 'features', 'eyebrow': 'Kako delamo', 'title': 'Svetovanje, načrtovanje in 3D izris',
             'numbered': True, 'items': services, 'background': 'surface'},
            {'type': 'pages', 'eyebrow': 'Prodajni program', 'title': 'Od kuhinje do otroške sobe',
             'pages': ['/prodajni-program/kuhinje', '/prodajni-program/sedezne-garniture',
                       '/prodajni-program/dnevne-sobe', '/prodajni-program/postelje-in-nocne-omarice',
                       '/prodajni-program/vrata', '/prodajni-program/zasteklitve'],
             'button': {'text': 'Celoten prodajni program', 'href': '/prodajni-program/'}},
            {'type': 'gallery', 'eyebrow': 'Reference', 'title': 'Pisano na kožo naročniku',
             'description': f'{gallery_text} [Oglejte si reference](/reference/)',
             'items': [
                 {'src': media(src['gallery']['items'][0]['src']), 'alt': 'Svetla kuhinja z otokom in jedilno mizo'},
                 {'src': media(src['gallery']['items'][1]['src']), 'alt': 'Pogrnjena jedilna miza pred stekleno steno'},
                 {'src': media(src['gallery']['items'][2]['src']), 'alt': 'Spalnica z oblazinjeno posteljo in nočno lučko'},
                 {'src': media(refs[1]['items'][0]['src']), 'alt': 'Kuhinja z oranžno jedilno mizo in visečo lučjo'},
                 {'src': media(refs[2]['items'][3]['src']), 'alt': 'Dnevna soba s kaminom in sedežno garnituro'},
                 {'src': media(refs[0]['items'][1]['src']), 'alt': 'Dnevni prostor s kuhinjo in sedežno garnituro'},
             ]},
            # Google, retrieved 25 Sep 2026 (research.md). Verbatim.
            {'type': 'reviews', 'eyebrow': 'Mnenja strank', 'title': 'Kaj pravijo stranke',
             'summary': '**4,7/5** iz 15 ocen na Googlu', 'background': 'surface',
             'items': [
                 {'text': 'Velika izbira pohištva, ugodne cene in prijazno osebje.', 'author': 'Al S.',
                  'source': 'Google', 'date': 'april 2018', 'rating': 5},
                 {'text': 'Vse pohvale zaposlenim. Profesionalen pristop kvalitetni izdelki in veliko znanja!!!',
                  'author': 'Darko S.', 'source': 'Google', 'date': 'januar 2019', 'rating': 5},
             ]},
            {'type': 'partners', 'eyebrow': 'Partnerji', 'title': 'Priznani evropski proizvajalci'},
            {'type': 'cta', 'title': 'Obiščite naš salon',
             'text': 'Kajakaška cesta 40, Ljubljana – Šmartno. ' + fix(q.split('STROKOVNO SVETOVANJE')[1].split('3D IZRIS')[0]),
             'button': {'text': 'Pokličite', 'href': PHONE, 'icon': 'phone'},
             'secondaryButton': {'text': 'Kontakt in delovni čas', 'href': '/kontakt/'},
             'background': 'primary'},
        ],
    }


def program():
    q = old('_index.md')['quoteContent']['content']
    return {
        'title': 'Prodajni program',
        'description': 'Kuhinje, jedilnice, sedežne garniture, dnevne sobe, garderobne omare, postelje, vrata, zasteklitve, otroške sobe in okovje v salonu Planet Plus.',
        'hero': {'eyebrow': 'Salon pohištva Planet Plus',
                 'description': fix(q.split('CELOVIT PREGLED PONUDBE')[1].split('STROKOVNO SVETOVANJE')[0])},
        'modules': [cta()],
    }


def partnerji():
    about = fix(old('_index.md')['description'])
    return {
        'title': 'Partnerji',
        'description': about.split('. ')[1] + '.',
        'hero': {'eyebrow': 'Salon pohištva Planet Plus'},
        'modules': [{'type': 'partners'}, cta()],
    }


def reference():
    src = old('reference.md')
    alts = {
        0: ['Spalnica z oblazinjeno posteljo in nočno lučko', 'Dnevni prostor s kuhinjo in sedežno garnituro',
            'Jedilni kotiček s stekleno steno', 'Spalnica s kopalno kadjo in obešalnikom'],
        1: ['Kuhinja z oranžno jedilno mizo in visečo lučjo', 'Kuhinja z otokom in opečno steno',
            'Kuhinja s pogledom na jedilnico za stekleno steno', 'Pogrnjena jedilna miza pred stekleno steno',
            'Spalnica s temno garderobno omaro'],
        2: ['Stopnišče z osvetljenimi lesenimi stopnicami', 'Kuhinja z otokom in jedilno mizo',
            'Kopalnica z lesenim umivalnim elementom', 'Dnevna soba s kaminom in sedežno garnituro',
            'Svetla kuhinja z otokom in jedilno mizo'],
    }
    modules = []
    for g, gallery in enumerate(src['galleries']):
        items = [{'src': media(i['src']), 'alt': alts[g][n]} for n, i in enumerate(gallery['items'])]
        module = {'type': 'gallery', 'eyebrow': 'Reference', 'title': gallery['title'], 'items': items}
        if g == 0:
            # From the file names (Stanovanje_v_Spektri-foto_anaskobe): confirm.
            module['description'] = 'Stanovanje v Spektri · fotografije: Ana Skobe'
        modules.append(module)
    modules.append(cta())
    return {
        'title': 'Reference',
        'description': fix(old('_index.md')['gallery']['text']) + ' Izbor opremljenih stanovanj.',
        'image': {'src': media(src['image']['src']), 'alt': 'Bela knjižna stena in dnevni prostor z visokim stropom'},
        'hero': {'variant': 'overlay', 'eyebrow': 'Salon pohištva Planet Plus'},
        'modules': modules,
    }


def kontakt():
    home_src = old('_index.md')
    return {
        'title': 'Kontakt',
        'description': 'Salon pohištva Planet Plus na Kajakaški cesti 40 v Ljubljani – Šmartnem: telefon, e-pošta, delovni čas in zemljevid.',
        'image': {'src': media(home_src['imagePartners']['image']['src']),
                  'alt': 'Temen dnevni prostor z jedilno mizo in knjižno steno'},
        'hero': {'eyebrow': 'Salon pohištva', 'title': 'Obiščite nas',
                 'description': 'Pokličite, pišite ali se oglasite v salonu na Kajakaški cesti 40.',
                 'button': {'text': 'Pokličite', 'href': PHONE, 'icon': 'phone'},
                 'secondaryButton': {'text': 'Pišite nam', 'href': EMAIL, 'icon': 'mail'}},
        'modules': [{'type': 'location', 'eyebrow': 'Kje smo', 'title': 'Salon pohištva Planet Plus',
                     'background': 'surface'}],
    }


# -------------------------------------------------------------------- output

class Dumper(yaml.SafeDumper):
    pass


def _str(dumper, value):
    style = '|' if '\n' in value else None
    return dumper.represent_scalar('tag:yaml.org,2002:str', value, style=style)


Dumper.add_representer(str, _str)


def write(path, data):
    full = os.path.join(SITE, 'content', path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    fm = yaml.dump(data, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=100)
    open(full, 'w', encoding='utf-8').write(f'---\n{fm}---\n')
    print('wrote', path)


def menus():
    lines = [
        '# One menu for every language. `pageRef` is the page\'s path in content/',
        '# ("/kontakt" for content/kontakt.sl.md). An item with `parent` goes in the',
        '# dropdown of the item whose `identifier` it names.',
        'main:',
        '  - pageRef: /prodajni-program',
        '    identifier: program',
        '    weight: 10',
    ]
    for slug in sorted(CATEGORIES, key=lambda s: old(f'prodajni-program/{s}.md')['weight']):
        lines += [f'  - pageRef: /prodajni-program/{slug}', '    parent: program',
                  f"    weight: {old(f'prodajni-program/{slug}.md')['weight']}"]
    lines += ['  - pageRef: /partnerji', '    weight: 20', '  - pageRef: /reference', '    weight: 30',
              '  - pageRef: /kontakt', '    weight: 40']
    open(os.path.join(SITE, 'config/_default/menus.yaml'), 'w').write('\n'.join(lines) + '\n')
    print('wrote menus.yaml')


def main():
    write('_index.sl.md', home())
    write('prodajni-program/_index.sl.md', program())
    for slug, spec in CATEGORIES.items():
        write(f'prodajni-program/{slug}.sl.md', category(slug, spec))
    write('partnerji.sl.md', partnerji())
    write('reference.sl.md', reference())
    write('kontakt.sl.md', kontakt())
    menus()

    # Brand names in the shared partner list follow the brands' spelling too.
    path = os.path.join(SITE, 'data/partners.json')
    data = json.load(open(path))
    for p in data['items']:
        p['name'] = brand(p['name'])
    json.dump(data, open(path, 'w'), indent=2, ensure_ascii=False)
    open(path, 'a').write('\n')

    # Optimised files no page references.
    text = ''
    for root, _, files in os.walk(os.path.join(SITE, 'content')):
        text += ''.join(open(os.path.join(root, f)).read() for f in files)
    text += open(path).read() + open(os.path.join(SITE, 'config/_default/hugo.toml')).read()
    unused = [f for f in sorted(os.listdir(UPLOADS)) if not f.startswith('.') and f'/media/uploads/{f}' not in text]
    print('unused:', unused)


if __name__ == '__main__':
    main()
