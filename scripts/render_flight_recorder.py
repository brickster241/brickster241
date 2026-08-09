#!/usr/bin/env python3
"""Render the multi-channel flight-data recorder: assets/recorder-{dark,light}.svg.

A real FDR is many channels on parallel strips — so is this: one channel per
repository, each tracing 52 weeks of commit activity, auto-gained like a real
recorder channel (every strip is scaled to its own peak; the peak is printed
so the gain is never a lie).

The usual contribution decorations — the snake, the 3D skyline — are rented.
This one is drawn in the profile's own instrument language and redrawn daily
by a workflow.

Data: REST `stats/commit_activity` (52 weekly buckets per repo). GitHub
computes these lazily and answers 202 while it works, so the fetch retries.
Auth: GITHUB_TOKEN env (what Actions provides), else the local `gh` CLI.

Usage:  python3 scripts/render_flight_recorder.py
"""

import json
import math
import os
import pathlib
import subprocess
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OWNER = 'brickster241'

# (repo, display label, color key) — order is display order, colors match the
# instrument panel above it in the README.
CHANNELS = [
    ('groundschool-skill', 'GROUNDSCHOOL', 'purple'),
    ('GitEngine', 'GITENGINE', 'hud'),
    ('PulseHTTP', 'PULSEHTTP', 'amber'),
    ('JSON-Lexer-Parser-From-Scratch', 'JSON-LP', 'ok'),
    ('wc-Go', 'WC-GO', 'dim'),
]


def fetch(repo: str) -> list[int]:
    url = f'https://api.github.com/repos/{OWNER}/{repo}/stats/commit_activity'
    token = os.environ.get('GITHUB_TOKEN')
    for attempt in range(6):
        if token:
            req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
            with urllib.request.urlopen(req, timeout=30) as r:
                status, body = r.status, r.read()
        else:
            p = subprocess.run(['gh', 'api', url], capture_output=True, text=True)
            status, body = (200 if p.returncode == 0 else 202), p.stdout
        try:
            data = json.loads(body)
            if isinstance(data, list) and data:
                return [w['total'] for w in data]
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
        time.sleep(5)  # 202: stats still being computed
    raise RuntimeError(f'no stats for {repo}')


def theme(dark: bool) -> dict:
    if dark:
        return dict(bg='#0b0f14', line='#232b38', ink='#e6edf3', dim='#8b98a9',
                    faint='#5b6675', amber='#ffb454', hud='#7dd3fc', ok='#4ade80',
                    purple='#c4b5fd', grid='#151b26')
    return dict(bg='#f7f8fa', line='#d7dde6', ink='#1a2330', dim='#4a5668',
                faint='#8a93a3', amber='#c77d1f', hud='#0f7fa8', ok='#1a8f4e',
                purple='#7c62c9', grid='#eceff4')


MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


def render(series: dict, dark: bool) -> str:
    t = theme(dark)
    ROW, HEAD, FOOT = 58, 56, 30
    W = 1200
    H = HEAD + ROW * len(CHANNELS) + FOOT
    px0, px1 = 196, 1028   # trace area
    n = 52

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{MONO}">']
    s.append(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')
    for x in range(0, W, 28):
        s.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{t["grid"]}" stroke-width="1"/>')
    for y in range(0, H, 28):
        s.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{t["grid"]}" stroke-width="1"/>')

    s.append(f'<text x="24" y="34" font-size="13" letter-spacing="3" fill="{t["dim"]}">FLIGHT DATA RECORDER · COMMITS PER WEEK, PER REPO</text>')
    s.append(f'<text x="{W - 24}" y="34" text-anchor="end" font-size="11" letter-spacing="2" fill="{t["faint"]}">TRAILING 52 WEEKS · EACH CHANNEL AUTO-GAINED TO ITS PEAK</text>')
    s.append(f'<line x1="24" y1="46" x2="{W - 24}" y2="46" stroke="{t["line"]}" stroke-width="1.5"/>')

    def x_at(i):
        return px0 + (px1 - px0) * (i / (n - 1))

    for ci, (repo, label, ckey) in enumerate(CHANNELS):
        weeks = series[repo][-n:]
        total, peak = sum(weeks), max(max(weeks), 1)
        color = t[ckey]
        top = HEAD + ci * ROW
        base = top + ROW - 12
        amp = ROW - 26

        # channel separator + label
        s.append(f'<line x1="24" y1="{top + ROW}" x2="{W - 24}" y2="{top + ROW}" stroke="{t["line"]}" stroke-width="1" stroke-dasharray="2 5"/>')
        s.append(f'<circle cx="34" cy="{top + ROW / 2 - 4}" r="3.5" fill="{color}"/>')
        s.append(f'<text x="46" y="{top + ROW / 2}" font-size="12" letter-spacing="1.5" fill="{t["ink"]}">{label}</text>')

        # trace, auto-gained; flat weeks stay flat on the baseline
        pts = [(x_at(i), base - amp * (v / peak)) for i, v in enumerate(weeks)]
        line = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
        area = f'{line} L{pts[-1][0]:.1f} {base} L{pts[0][0]:.1f} {base} Z'
        length = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
        delay = 0.15 + ci * 0.18
        s.append(f'<line x1="{px0}" y1="{base}" x2="{px1}" y2="{base}" stroke="{t["line"]}" stroke-width="1"/>')
        s.append(f'<path d="{area}" fill="{color}" opacity="0"><animate attributeName="opacity" from="0" to="0.10" dur="0.6s" begin="{delay + 1.5:.2f}s" fill="freeze"/></path>')
        s.append(f'<path d="{line}" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round" '
                 f'stroke-dasharray="{length:.0f}" stroke-dashoffset="{length:.0f}">'
                 f'<animate attributeName="stroke-dashoffset" from="{length:.0f}" to="0" dur="1.6s" begin="{delay:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.3 0 0.2 1"/></path>')

        # right cluster: totals, and the gain so the scaling is honest
        s.append(f'<text x="{W - 24}" y="{top + ROW / 2 - 4}" text-anchor="end" font-size="15" font-weight="700" fill="{t["ink"]}">{total} <tspan font-size="10" font-weight="400" fill="{t["dim"]}">commits</tspan></text>')
        s.append(f'<text x="{W - 24}" y="{top + ROW / 2 + 13}" text-anchor="end" font-size="10" fill="{t["faint"]}">pk {peak}/wk</text>')

    # shared month ticks (approximate: 52 weeks back from now, tick every ~2 months)
    from datetime import date, timedelta
    today = date.today()
    seen = None
    for i in range(n):
        d = today - timedelta(weeks=n - 1 - i)
        if d.month != seen and seen is not None and d.month % 2 == 1:
            x = x_at(i)
            lbl = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'][d.month - 1]
            s.append(f'<line x1="{x:.1f}" y1="{H - FOOT + 2}" x2="{x:.1f}" y2="{H - FOOT + 7}" stroke="{t["faint"]}" stroke-width="1.5"/>')
            s.append(f'<text x="{x:.1f}" y="{H - 8}" text-anchor="middle" font-size="10" letter-spacing="1" fill="{t["faint"]}">{lbl}</text>')
        seen = d.month

    s.append('</svg>')
    return ''.join(s)


if __name__ == '__main__':
    series = {repo: fetch(repo) for repo, _, _ in CHANNELS}
    out = ROOT / 'assets'
    for dark in (True, False):
        path = out / f'recorder-{"dark" if dark else "light"}.svg'
        path.write_text(render(series, dark))
        print('wrote', path.relative_to(ROOT))
