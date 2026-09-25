#!/usr/bin/env python3
"""Collect the media the live planetplus.si uses and optimise it into the
prototype's static/media/uploads/.

Every file comes from the client's Planet Plus folder when one there has the
exact byte size Cloudinary serves (Cloudinary returns the stored original, so
this is the file the client approved). Anything without an exact match is
downloaded from Cloudinary into media/raw/.

Writes media/map.json (Cloudinary URL -> /media/uploads/<name>) for the
content generator, and media/manifest.md.
"""

import glob
import json
import os
import re
import subprocess
import unicodedata
from urllib.parse import unquote

import yaml

WWW = '/Users/martinjagodic/Development/planetplus-www'
SRC = '/Users/martinjagodic/Desktop/Documents/Planet Plus'
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw')
OUT = os.path.join(HERE, '../../../planet-plus/static/media/uploads')

PAGES = {
    '_index.md': 'domov',
    'partnerji.md': 'partnerji',
    'reference.md': 'reference',
}

# (max px, JPEG quality) per role. There is no Bunny Optimizer yet, so these
# files are what browsers get.
SIZES = {
    'naslovna': (1680, 60),
    'galerija': (1400, 68),
    'logo': (420, None),
}
SECTION = (1400, 65)


def norm(s):
    s = unicodedata.normalize('NFC', s).lower()
    s = re.sub(r'[\s\-()]+', '_', s)
    return re.sub(r'_+', '_', s).strip('_')


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def front_matter(path):
    text = open(path, encoding='utf-8').read()
    return yaml.safe_load(text.split('---')[1]) or {}


def uses():
    """Yield (page, role, url) in page order."""
    files = [os.path.join(WWW, 'content', f) for f in PAGES]
    files += sorted(glob.glob(os.path.join(WWW, 'content/prodajni-program/*.md')))
    for f in files:
        name = os.path.basename(f)
        if name == '_index.md' and 'prodajni-program' in f:
            continue
        page = PAGES.get(name, os.path.splitext(name)[0])
        fm = front_matter(f)
        get = lambda *keys: _dig(fm, keys)
        yield page, 'naslovna', get('image', 'src')
        yield page, 'ambient', get('quoteContent', 'image', 'src')
        yield page, 'detajl', get('quoteContent', 'imageCenter', 'src')
        yield page, 'partner', get('imagePartners', 'image', 'src')
        for i, item in enumerate(get('gallery', 'items') or [], 1):
            yield page, f'galerija-{i}', item.get('src')
        for g, gallery in enumerate(fm.get('galleries') or [], 1):
            label = slug(gallery.get('title') or f'projekt-{g}')
            for i, item in enumerate(gallery.get('items') or [], 1):
                yield page, f'galerija-{label}-{i}', item.get('src')
    for p in json.load(open(os.path.join(WWW, 'data/partners.json')))['list']:
        yield 'partner', 'logo-' + slug(p['name']), p['logo']


def _dig(d, keys):
    for k in keys:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def local_files():
    index = {}
    for p in glob.glob(os.path.join(SRC, '**/*'), recursive=True):
        if os.path.isfile(p) and not p.endswith('.DS_Store'):
            stem = os.path.splitext(os.path.basename(p))[0]
            index.setdefault(norm(stem), []).append(p)
    return index


def remote_size(url):
    """Content-Length of the stored original, or None when Cloudinary 404s."""
    out = subprocess.run(['curl', '-sI', '--retry', '3', '--retry-all-errors', url],
                         capture_output=True, text=True).stdout
    if not out.startswith('HTTP/2 200') and not out.startswith('HTTP/1.1 200'):
        return None
    for line in out.splitlines():
        if line.lower().startswith('content-length'):
            return int(line.split(':', 1)[1])
    return None


def source_for(url, index):
    base = unicodedata.normalize('NFC', unquote(os.path.basename(url)))
    stem = re.sub(r'_[a-z0-9]{6}$', '', os.path.splitext(base)[0])
    candidates = index.get(norm(stem), [])
    size = remote_size(url)
    if size is None:
        if len(candidates) == 1:
            return candidates[0], 'client folder — missing on Cloudinary, so broken on the live site'
        raise SystemExit(f'{url}: missing on Cloudinary and {len(candidates)} folder candidates')
    for candidate in candidates:
        if os.path.getsize(candidate) == size:
            return candidate, 'client folder'
    os.makedirs(RAW, exist_ok=True)
    target = os.path.join(RAW, base)
    if not os.path.exists(target):
        subprocess.run(['curl', '-sfL', '--retry', '3', '--retry-all-errors', '-o', target, url], check=True)
    return target, 'Cloudinary (no exact match in the folder)'


def optimise(src, dest_stem, role):
    ext = os.path.splitext(src)[1].lower()
    if role.startswith('logo'):
        if ext == '.svg':
            dest = dest_stem + '.svg'
            subprocess.run(['cp', src, dest], check=True)
            return dest
        dest = dest_stem + '.png'
        subprocess.run(['sips', '-s', 'format', 'png', '-Z', str(SIZES['logo'][0]), src, '--out', dest],
                       check=True, capture_output=True)
        return dest
    key = 'naslovna' if role == 'naslovna' else 'galerija' if role.startswith('galerija') else None
    px, quality = SIZES.get(key, SECTION)
    dest = dest_stem + '.jpg'
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', str(quality), '-Z', str(px),
                    src, '--out', dest], check=True, capture_output=True)
    # The hero is the LCP image, so it stays under 500 KB. A source that
    # misses that at q60 is noisy (print scans with halftone grain): a light
    # denoise first costs less detail than a lower quality would.
    if key == 'naslovna' and os.path.getsize(dest) > 480 * 1024:
        clean = dest_stem + '.denoised.png'
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', src, '-vf',
                        f'scale={px}:{px}:force_original_aspect_ratio=decrease:flags=lanczos,hqdn3d=4:3:0:0',
                        clean], check=True)
        subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', str(quality), clean,
                        '--out', dest], check=True, capture_output=True)
        os.remove(clean)
    return dest


def dims(path):
    if path.endswith('.svg'):
        return 'vector'
    out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', path],
                         capture_output=True, text=True).stdout
    w, h = re.findall(r'pixel(?:Width|Height): (\d+)', out)
    return f'{w}×{h}'


def main():
    os.makedirs(OUT, exist_ok=True)
    index = local_files()
    mapping, rows = {}, []
    for page, role, url in uses():
        if not url:
            continue
        if url in mapping:
            rows[[r['url'] for r in rows].index(url)]['used'].append(f'{page} {role}')
            continue
        src, origin = source_for(url, index)
        stem = f'{page}-{role}' if not role.startswith('logo') else role.replace('logo-', 'partner-')
        dest = optimise(src, os.path.join(OUT, stem), role)
        mapping[url] = '/media/uploads/' + os.path.basename(dest)
        rows.append(dict(url=url, file=os.path.basename(dest), src=os.path.relpath(src, SRC) if src.startswith(SRC) else os.path.relpath(src, HERE),
                         origin=origin, used=[f'{page} {role}'], dims=dims(dest), kb=os.path.getsize(dest) // 1024))
        print(f"{rows[-1]['file']:55} {rows[-1]['dims']:>10} {rows[-1]['kb']:>5} KB  {origin}")

    json.dump(mapping, open(os.path.join(HERE, 'map.json'), 'w'), indent=2, ensure_ascii=False)
    with open(os.path.join(HERE, 'manifest.md'), 'w') as m:
        m.write('# Planet Plus — media manifest\n\n')
        m.write('Generated by `prepare.py`. Every file is one the live planetplus.si shows; the source is the '
                "client's Planet Plus folder (exact byte match with Cloudinary's original) unless noted. "
                'Rights: supplied by the client for their current site. Many are manufacturer press photos '
                '(Novamobili, Doimo Cucine, Nidi, Kristalia, Metalglas, Oikos, Soft Line, Fiora) used as '
                'their dealer; the reference project "Stanovanje v Spektri" is credited "foto Ana Skobe" in '
                'the file names.\n\n')
        m.write('| File | Size | Used as | Source |\n| --- | --- | --- | --- |\n')
        for r in rows:
            m.write(f"| `{r['file']}` | {r['dims']}, {r['kb']} KB | {', '.join(r['used'])} | {r['src']} ({r['origin']}) |\n")
    print(len(rows), 'files')


if __name__ == '__main__':
    main()
