#!/usr/bin/env python3
"""Render the NERV theme's wallpapers and picker preview (needs rsvg-convert).

Rerun it after editing the text or layout below, then `omarchy theme set nerv`
to pick up the new images.
"""
import math
import pathlib
import subprocess

W, H = 2304, 1440
BG = "#060504"
ORANGE = "#ff6a00"
AMBER = "#ff9d45"
RED = "#ff2a2a"
GREEN = "#3dff7a"
WHITE = "#f4e6d4"
SERIF = "Noto Serif CJK JP"
MONO = "JetBrainsMono Nerd Font"

theme = pathlib.Path(__file__).parent
out = theme / "backgrounds"


def svg(body, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
        f"<defs>{defs}"
        # Soft phosphor glow for the key shapes
        '<filter id="glow" x="-20%" y="-20%" width="140%" height="140%">'
        '<feGaussianBlur stdDeviation="6" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        "</defs>"
        f'<rect width="{W}" height="{H}" fill="{BG}"/>{body}</svg>'
    )


def hexgrid(color, opacity, r=34):
    """A pattern of flat hexagon outlines."""
    w, h = 3 * r, math.sqrt(3) * r
    pts = lambda cx, cy: " ".join(
        f"{cx + r * math.cos(math.radians(a)):.1f},{cy + r * math.sin(math.radians(a)):.1f}"
        for a in range(0, 360, 60)
    )
    return (
        f'<pattern id="hex" width="{w:.1f}" height="{h:.1f}" patternUnits="userSpaceOnUse">'
        f'<g fill="none" stroke="{color}" stroke-opacity="{opacity}" stroke-width="1.5">'
        f'<polygon points="{pts(r, h / 2)}"/>'
        f'<polygon points="{pts(r * 2.5, 0)}"/><polygon points="{pts(r * 2.5, h)}"/>'
        "</g></pattern>"
    )


def text(x, y, s, size, fill, family=SERIF, weight=900, squeeze=1.0, anchor="start", extra=""):
    """Text, optionally squeezed horizontally like Evangelion title cards."""
    return (
        f'<g transform="translate({x},{y}) scale({squeeze},1)">'
        f'<text font-family="{family}" font-weight="{weight}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" {extra}>{s}</text></g>'
    )


def stripes(y, height, id_):
    """A black and warning-orange hazard band."""
    return (
        f'<pattern id="{id_}" width="80" height="80" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<rect width="40" height="80" fill="{ORANGE}"/></pattern>',
        f'<rect x="0" y="{y}" width="{W}" height="{height}" fill="url(#{id_})"/>',
    )


def scanlines():
    return (
        '<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1" fill="#000" fill-opacity="0.35"/></pattern>',
        f'<rect width="{W}" height="{H}" fill="url(#scan)"/>',
    )


# 1. Title card: stacked, squeezed serif in the style of the episode title cards
def title_card():
    body = [
        text(210, 520, "GOD'S IN", 300, WHITE, squeeze=0.62),
        text(210, 820, "HIS HEAVEN.", 300, WHITE, squeeze=0.62),
        text(W - 180, 1080, "ALL'S RIGHT", 150, WHITE, squeeze=0.62, anchor="end"),
        text(W - 180, 1240, "WITH THE WORLD.", 150, WHITE, squeeze=0.62, anchor="end"),
        text(210, 260, "EPISODE:00", 64, AMBER, squeeze=0.7),
        f'<rect x="210" y="880" width="1100" height="6" fill="{ORANGE}" filter="url(#glow)"/>',
        text(210, 950, "SYSTEM NOMINAL · ALL UNITS STANDING BY", 34, AMBER, family=MONO, weight=400),
    ]
    return svg("".join(body))


# 2. MAGI: three supercomputers voting, over a hex grid
def magi():
    defs = [hexgrid(ORANGE, 0.10)]
    body = [f'<rect width="{W}" height="{H}" fill="url(#hex)"/>']

    def unit(x, y, w, h, name, number, vote):
        return (
            f'<g filter="url(#glow)">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{GREEN}" fill-opacity="0.12" '
            f'stroke="{GREEN}" stroke-width="5"/></g>'
            + text(x + w / 2, y + 140, name, 92, GREEN, squeeze=0.7, anchor="middle")
            + text(x + w / 2, y + h - 55, vote, 110, GREEN, anchor="middle")
            + text(x + 24, y + 56, number, 36, GREEN, family=MONO, weight=700)
        )

    cx = W / 2
    body += [
        unit(cx - 330, 250, 660, 330, "BALTHASAR", "·2", "承認"),
        unit(cx - 900, 700, 660, 330, "CASPER", "·3", "承認"),
        unit(cx + 240, 700, 660, 330, "MELCHIOR", "·1", "承認"),
        # MAGI label in the middle, wired to each unit
        f'<g stroke="{ORANGE}" stroke-width="4" fill="none" filter="url(#glow)">'
        f'<line x1="{cx}" y1="580" x2="{cx}" y2="790"/>'
        f'<line x1="{cx - 240}" y1="865" x2="{cx - 150}" y2="865"/>'
        f'<line x1="{cx + 150}" y1="865" x2="{cx + 240}" y2="865"/></g>',
        text(cx, 900, "MAGI", 120, ORANGE, squeeze=0.7, anchor="middle"),
        text(120, 150, "MAGI SYSTEM", 80, ORANGE, squeeze=0.65),
        text(120, 205, "提訴 · 決議 · 全会一致", 44, AMBER, weight=700),
        text(W - 120, 150, "DELIBERATION: UNANIMOUS", 36, AMBER, family=MONO, weight=700, anchor="end"),
        text(W - 120, 200, "CODE: 000", 36, AMBER, family=MONO, weight=400, anchor="end"),
        f'<rect x="120" y="{H - 170}" width="{W - 240}" height="3" fill="{ORANGE}" fill-opacity="0.6"/>',
        text(120, H - 110, "SELF-DESTRUCT SEQUENCE: DISABLED", 32, AMBER, family=MONO, weight=400),
    ]
    sd, sb = scanlines()
    return svg("".join(body) + sb, "".join(defs) + sd)


# 3. Emergency: hazard bands and an alert, over a red hex grid
def emergency():
    d1, b1 = stripes(0, 110, "hz1")
    d2, b2 = stripes(H - 110, 110, "hz2")
    defs = [hexgrid(RED, 0.12), d1, d2]
    body = [
        f'<rect width="{W}" height="{H}" fill="url(#hex)"/>',
        b1,
        b2,
        f'<g filter="url(#glow)"><rect x="300" y="430" width="{W - 600}" height="420" fill="none" '
        f'stroke="{RED}" stroke-width="8"/></g>',
        text(W / 2, 760, "EMERGENCY", 330, RED, squeeze=0.62, anchor="middle", extra='filter="url(#glow)"'),
        text(W / 2, 1000, "緊急事態発生", 120, RED, anchor="middle"),
        text(W / 2, 1120, "PATTERN BLUE · ANGEL CONFIRMED", 44, AMBER, family=MONO, weight=700, anchor="middle"),
        text(340, 400, "警告", 90, ORANGE, anchor="start"),
        text(W - 340, 400, "WARNING", 60, ORANGE, family=MONO, weight=700, anchor="end"),
    ]
    sd, sb = scanlines()
    return svg("".join(body) + sb, "".join(defs) + sd)


def render(svg_text, png, width=W):
    subprocess.run(["rsvg-convert", "-w", str(width), "-o", str(png)], input=svg_text.encode(), check=True)


out.mkdir(exist_ok=True)
for name, fn in [("1-title-card", title_card), ("2-magi", magi), ("3-emergency", emergency)]:
    render(fn(), out / f"{name}.png")
    print(out / f"{name}.png")

render(magi(), theme / "preview.png", width=W // 2)
