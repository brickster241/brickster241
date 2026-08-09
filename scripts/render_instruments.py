#!/usr/bin/env python3
"""Render the profile's banner and instrument panel as SVG, dark + light.

The panel shows measured numbers from my repos' own benchmark/test harnesses.
It is generated rather than drawn so the numbers can be updated the way they
were produced — by editing data, not paths. Animations are SMIL, which GitHub's
image proxy passes through untouched.

Usage:  python3 scripts/render_instruments.py     # writes assets/*.svg
"""

import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,'Segoe UI',system-ui,Helvetica,Arial,sans-serif"

# One gauge per project: (arc fraction, big number, unit, label, sub1, sub2, color key, start delay)
GAUGES = [
    (0.86, '179K', 'req/s', 'PULSEHTTP · THROUGHPUT',
     'p99 2.2 ms · raw TCP, zero deps', '39-test wire conformance suite', 'amber', '0.1s'),
    (1.00, '98/98', '', 'JSON-LP · DIFFERENTIAL',
     '0 disagreements vs RFC-strict stdlib', '572K tokens/s · bounded depth', 'ok', '0.35s'),
    (1.00, 'SHA ≡', 'parity', 'GITENGINE · CORRECTNESS',
     'byte-for-byte vs native git · diff3', '2× git bulk ingest · 28.5K obj/s fsck', 'hud', '0.6s'),
    (1.00, 'SELF', 'hosting', 'GROUNDSCHOOL · SKILL',
     'the skill, run on its own code', 'live demo on GitHub Pages', 'purple', '0.85s'),
]


def theme(dark: bool) -> dict:
    if dark:
        return dict(bg='#0b0f14', panel='#11151d', line='#232b38', ink='#e6edf3',
                    dim='#8b98a9', faint='#5b6675', amber='#ffb454', hud='#7dd3fc',
                    ok='#4ade80', purple='#c4b5fd', grid='#151b26')
    return dict(bg='#f7f8fa', panel='#ffffff', line='#d7dde6', ink='#1a2330',
                dim='#4a5668', faint='#8a93a3', amber='#c77d1f', hud='#0f7fa8',
                ok='#1a8f4e', purple='#7c62c9', grid='#eceff4')


def grid(w, h, t, step=28):
    out = []
    for x in range(0, w, step):
        out.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{t["grid"]}" stroke-width="1"/>')
    for y in range(0, h, step):
        out.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{t["grid"]}" stroke-width="1"/>')
    return ''.join(out)


def corners(x, y, w, h, t, s=14):
    c = t['faint']
    p = []
    for cx, cy, dx, dy in [(x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)]:
        p.append(f'<path d="M{cx} {cy + dy * s} L{cx} {cy} L{cx + dx * s} {cy}" fill="none" stroke="{c}" stroke-width="1.5"/>')
    return ''.join(p)


def banner(dark: bool) -> str:
    t = theme(dark)
    W, H = 1200, 240
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{MONO}">']
    s.append(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')
    s.append(grid(W, H, t))
    s.append(corners(18, 18, W - 36, H - 36, t))

    # left roundel with a slowly rotating tick ring
    cx, cy = 108, 120
    s.append(f'<circle cx="{cx}" cy="{cy}" r="52" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="{t["amber"]}" stroke-width="2"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="{t["amber"]}"/>')
    ticks = []
    for i in range(12):
        a = math.radians(i * 30)
        x1, y1 = cx + 46 * math.sin(a), cy - 46 * math.cos(a)
        x2, y2 = cx + 52 * math.sin(a), cy - 52 * math.cos(a)
        ticks.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{t["faint"]}" stroke-width="2"/>')
    s.append(f'<g>{"".join(ticks)}<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="40s" repeatCount="indefinite"/></g>')

    # name + roles
    s.append(f'<text x="200" y="102" font-family="{SANS}" font-size="46" font-weight="800" letter-spacing="1" fill="{t["ink"]}">ASHISH VERMA</text>')
    s.append(f'<text x="202" y="136" font-size="14" letter-spacing="3" fill="{t["dim"]}">SIMULATION &amp; SYSTEMS ENGINEER</text>')
    s.append(f'<text x="202" y="162" font-size="12" letter-spacing="2" fill="{t["faint"]}">UNITY / C#  ·  GO  ·  PYTHON  ·  TYPESCRIPT</text>')

    # typed tagline with a blinking cursor
    tag = '&gt; builds it from scratch. proves it correct.'
    s.append(f'<text x="202" y="196" font-size="15" fill="{t["amber"]}">{tag}<tspan fill="{t["ink"]}">_<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></tspan></text>')

    # right radar with sweep + blips
    rx, ry, rr = 1050, 120, 74
    s.append(f'<circle cx="{rx}" cy="{ry}" r="{rr}" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>')
    for f in (0.66, 0.33):
        s.append(f'<circle cx="{rx}" cy="{ry}" r="{rr * f:.0f}" fill="none" stroke="{t["line"]}" stroke-width="1"/>')
    s.append(f'<line x1="{rx - rr}" y1="{ry}" x2="{rx + rr}" y2="{ry}" stroke="{t["line"]}" stroke-width="1"/>')
    s.append(f'<line x1="{rx}" y1="{ry - rr}" x2="{rx}" y2="{ry + rr}" stroke="{t["line"]}" stroke-width="1"/>')
    for bx, by, d in [(rx + 30, ry - 24, '0s'), (rx - 38, ry + 18, '1.3s'), (rx + 12, ry + 44, '2.6s')]:
        s.append(f'<circle cx="{bx}" cy="{by}" r="3.5" fill="{t["hud"]}"><animate attributeName="opacity" values="0;1;0" dur="4s" begin="{d}" repeatCount="indefinite"/></circle>')
    s.append(f'<g><line x1="{rx}" y1="{ry}" x2="{rx}" y2="{ry - rr}" stroke="{t["amber"]}" stroke-width="2"/>'
             f'<path d="M{rx} {ry} L{rx} {ry - rr} A{rr} {rr} 0 0 1 {rx + rr * math.sin(math.radians(40)):.1f} {ry - rr * math.cos(math.radians(40)):.1f} Z" fill="{t["amber"]}" opacity="0.12"/>'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {rx} {ry}" to="360 {rx} {ry}" dur="6s" repeatCount="indefinite"/></g>')

    s.append('</svg>')
    return ''.join(s)


def gauge(x, y, t, frac, big, unit, label, sub1, sub2, color, delay):
    """One instrument tile; the arc and needle animate from zero to the value."""
    W = 276
    cx, cy, r = x + W / 2, y + 128, 74
    a0, a1 = -120, -120 + 240 * frac  # 240° gauge span

    def pt(a, rad):
        return (cx + rad * math.sin(math.radians(a)), cy - rad * math.cos(math.radians(a)))

    x1, y1 = pt(a0, r)
    x2, y2 = pt(a1, r)
    large = 1 if (a1 - a0) > 180 else 0
    arc_len = math.radians(240 * frac) * r
    full = f'M{pt(a0, r)[0]:.1f} {pt(a0, r)[1]:.1f} A{r} {r} 0 1 1 {pt(120, r)[0]:.1f} {pt(120, r)[1]:.1f}'
    val = f'M{x1:.1f} {y1:.1f} A{r} {r} 0 {large} 1 {x2:.1f} {y2:.1f}'

    g = []
    g.append(f'<rect x="{x}" y="{y}" width="{W}" height="250" rx="12" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="1.5"/>')
    g.append(f'<text x="{x + 18}" y="{y + 30}" font-size="11" letter-spacing="2.5" fill="{t["faint"]}">{label}</text>')
    g.append(f'<path d="{full}" fill="none" stroke="{t["line"]}" stroke-width="7" stroke-linecap="round"/>')
    for i in range(0, 9):
        a = -120 + i * 30
        p1, p2 = pt(a, r - 13), pt(a, r - 19)
        g.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="{t["faint"]}" stroke-width="1.5"/>')
    g.append(f'<path d="{val}" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round" '
             f'stroke-dasharray="{arc_len:.0f}" stroke-dashoffset="{arc_len:.0f}">'
             f'<animate attributeName="stroke-dashoffset" from="{arc_len:.0f}" to="0" dur="1.4s" begin="{delay}" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/></path>')
    g.append(f'<g><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r + 24}" stroke="{color}" stroke-width="2.5" stroke-linecap="round" transform="rotate({a0} {cx} {cy})">'
             f'<animateTransform attributeName="transform" type="rotate" from="{a0} {cx} {cy}" to="{a1} {cx} {cy}" dur="1.4s" begin="{delay}" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/></line>'
             f'<circle cx="{cx}" cy="{cy}" r="5" fill="{color}"/></g>')
    g.append(f'<text x="{cx}" y="{y + 188}" text-anchor="middle" font-family="{SANS}" font-size="34" font-weight="800" fill="{t["ink"]}">{big}'
             f'<tspan font-size="14" font-weight="600" fill="{t["dim"]}"> {unit}</tspan></text>')
    g.append(f'<text x="{cx}" y="{y + 212}" text-anchor="middle" font-size="11" fill="{t["dim"]}">{sub1}</text>')
    g.append(f'<text x="{cx}" y="{y + 230}" text-anchor="middle" font-size="11" fill="{t["faint"]}">{sub2}</text>')
    return ''.join(g)


def panel(dark: bool) -> str:
    t = theme(dark)
    W, H = 1200, 330
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{MONO}">']
    s.append(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')
    s.append(grid(W, H, t))
    s.append(f'<text x="24" y="40" font-size="13" letter-spacing="3" fill="{t["dim"]}">INSTRUMENT PANEL</text>')
    s.append(f'<text x="{W - 24}" y="40" text-anchor="end" font-size="11" letter-spacing="2" fill="{t["faint"]}">EVERY NUMBER MEASURED BY A HARNESS IN ITS OWN REPO</text>')
    s.append(f'<line x1="24" y1="52" x2="{W - 24}" y2="52" stroke="{t["line"]}" stroke-width="1.5"/>')
    for i, (frac, big, unit, label, sub1, sub2, color, delay) in enumerate(GAUGES):
        s.append(gauge(24 + i * 292, 66, t, frac, big, unit, label, sub1, sub2, t[color], delay))
    s.append('</svg>')
    return ''.join(s)


if __name__ == '__main__':
    out = ROOT / 'assets'
    out.mkdir(exist_ok=True)
    for name, fn in [('banner', banner), ('panel', panel)]:
        for dark in (True, False):
            path = out / f'{name}-{"dark" if dark else "light"}.svg'
            path.write_text(fn(dark))
            print('wrote', path.relative_to(ROOT))
