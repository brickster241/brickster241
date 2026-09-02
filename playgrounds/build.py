#!/usr/bin/env python3
"""Inject the self-hosted Routed Gothic faces into every playground template.

Each playground ships as one file. The two woff2 faces are embedded as data
URIs so index.html has no sibling dependencies; the template keeps the
placeholders so the 27 KB of base64 never has to be read by a human.
"""
import base64, pathlib, sys
root = pathlib.Path(__file__).resolve().parent
rg  = base64.b64encode((root / 'fonts' / 'routed-gothic.woff2').read_bytes()).decode()
rgn = base64.b64encode((root / 'fonts' / 'routed-gothic-narrow.woff2').read_bytes()).decode()
targets = sys.argv[1:] or [p.parent.name for p in root.glob('*/index.template.html')]
for name in targets:
    t = (root / name / 'index.template.html').read_text()
    out = t.replace('__RG__', rg).replace('__RGN__', rgn)
    (root / name / 'index.html').write_text(out)
    bad = {k: out.count(k) for k in ('—', '–', '·') if out.count(k)}
    print(f'{name:10s} {len(out):7d} bytes' + (f'  BANNED GLYPHS: {bad}' if bad else ''))
