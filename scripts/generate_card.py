#!/usr/bin/env python3
import json
import math
import os
import random
import sys
import urllib.request

LOGIN = os.environ.get("GITHUB_LOGIN", "HenriqueSZ5")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
SPRITE_PATH = os.environ.get("SPRITE_PATH", "assets/gtr35.txt")
OUT_PATH = os.environ.get("OUT_PATH", "assets/profile.svg")

NAME = "Henrique Souza"
ROLE = "desenvolvedor full stack"
DRIVER = "Henrique Souza · eng. de software · UCSAL"
CONTACT = f"github.com/{LOGIN} · spaulohenrique511@gmail.com"
CAR = "Nissan GT-R R35 · VR38DETT 3.8 V6 biturbo"

SPEC = [
    ("motor", "linguagens", "python · typescript · javascript"),
    ("pintura", "web", "html5 · css3"),
    ("transmissão", "backend", "django · next.js · nestjs · node.js"),
    ("carroceria", "frontend", "react · vite · tailwind · bootstrap"),
    ("chassi", "banco e orm", "postgresql · redis · prisma"),
    ("pit stop", "devops", "docker · nginx · github actions"),
    ("pista", "servidor", "linux"),
    ("tração", "full stack", "integral: front-end + back-end"),
]

SPEEDS = [287, 291, 296, 301, 305, 309, 312, 306, 298, 293]

BG = "#0a0c14"
BORDER = "#1d2236"
ORANGE = "#ff7a2f"
WHITE = "#eef1f5"
DIM = "#6b7390"
DIMMER = "#3d4462"
BLUE = "#8fb8ff"

SPRITE_COLORS = {
    "K": "#0a0c12", "H": "#ffffff", "S": "#e6eaf0", "M": "#c3cad4", "D": "#8f98a6",
    "G": "#141a26", "g": "#3d4c68", "R": "#ff2a35", "r": "#7a0d16", "p": "#ff9aa0",
    "P": "#f4f6f8", "U": "#1f4fb8", "B": "#1a1d24", "F": "#2c313b", "T": "#15171c",
    "t": "#24272e", "X": "#050507", "E": "#6c78d6", "e": "#c4cad4",
}

FONT = {
    "A": ".###. #...# #...# ##### #...# #...# #...#",
    "B": "####. #...# #...# ####. #...# #...# ####.",
    "C": ".###. #...# #.... #.... #.... #...# .###.",
    "D": "####. #...# #...# #...# #...# #...# ####.",
    "E": "##### #.... #.... ####. #.... #.... #####",
    "F": "##### #.... #.... ####. #.... #.... #....",
    "G": ".###. #...# #.... #.### #...# #...# .####",
    "H": "#...# #...# #...# ##### #...# #...# #...#",
    "I": "### .#. .#. .#. .#. .#. ###",
    "J": "..### ...#. ...#. ...#. #..#. #..#. .##..",
    "K": "#...# #..#. #.#.. ##... #.#.. #..#. #...#",
    "L": "#.... #.... #.... #.... #.... #.... #####",
    "M": "#...# ##.## #.#.# #.#.# #...# #...# #...#",
    "N": "#...# #...# ##..# #.#.# #..## #...# #...#",
    "O": ".###. #...# #...# #...# #...# #...# .###.",
    "P": "####. #...# #...# ####. #.... #.... #....",
    "Q": ".###. #...# #...# #...# #.#.# #..#. .##.#",
    "R": "####. #...# #...# ####. #.#.. #..#. #...#",
    "S": ".#### #.... #.... .###. ....# ....# ####.",
    "T": "##### ..#.. ..#.. ..#.. ..#.. ..#.. ..#..",
    "U": "#...# #...# #...# #...# #...# #...# .###.",
    "V": "#...# #...# #...# #...# #...# .#.#. ..#..",
    "W": "#...# #...# #...# #.#.# #.#.# #.#.# .#.#.",
    "X": "#...# #...# .#.#. ..#.. .#.#. #...# #...#",
    "Y": "#...# #...# .#.#. ..#.. ..#.. ..#.. ..#..",
    "Z": "##### ....# ...#. ..#.. .#... #.... #####",
    "0": ".###. #...# #..## #.#.# ##..# #...# .###.",
    "1": "..#.. .##.. ..#.. ..#.. ..#.. ..#.. .###.",
    "2": ".###. #...# ....# ...#. ..#.. .#... #####",
    "3": "##### ...#. ..#.. ...#. ....# #...# .###.",
    "4": "...#. ..##. .#.#. #..#. ##### ...#. ...#.",
    "5": "##### #.... ####. ....# ....# #...# .###.",
    "6": "..##. .#... #.... ####. #...# #...# .###.",
    "7": "##### ....# ...#. ..#.. .#... .#... .#...",
    "8": ".###. #...# #...# .###. #...# #...# .###.",
    "9": ".###. #...# #...# .#### ....# ...#. .##..",
    ".": ". . . . . . #",
    "·": ". . . # . . .",
    ":": ". . # . . # .",
    "-": "... ... ... ### ... ... ...",
    "+": "..... ..#.. ..#.. ##### ..#.. ..#.. .....",
    "/": "....# ....# ...#. ..#.. .#... #.... #....",
    "@": ".###. #...# #.### #.#.# #.### #.... .####",
    "!": "# # # # # . #",
}
ACCENTED = {
    "Á": ("A", "acute"), "Â": ("A", "circ"), "Ã": ("A", "tilde"), "É": ("E", "acute"),
    "Ê": ("E", "circ"), "Í": ("I", "acute"), "Ó": ("O", "acute"), "Ô": ("O", "circ"),
    "Õ": ("O", "tilde"), "Ú": ("U", "acute"), "Ç": ("C", "cedilla"),
}
MARKS = {
    "acute": (-2, ["...#.", "..#.."]),
    "circ": (-2, ["..#..", ".#.#."]),
    "tilde": (-2, [".##.#", "#..#."]),
    "cedilla": (7, ["..#..", ".##.."]),
}
SPACE_ADVANCE = 3

PIXEL = 5
SCENE_W = 180
SCENE_H = 76
HORIZON = 30
ROAD_DEPTH = 200
ROAD_SPREAD = 100
ROAD_PHASES = 6
ROAD_STEP = 0.05
LAMP_HEIGHT = 30
CAR_BOTTOM = 74

W = 900
PAD = 36
SHEET_Y = SCENE_H * PIXEL
CELL_W = 402
CELL_H = 62

used_glyphs = set()


def glyph_rows(ch):
    if ch in ACCENTED:
        base, mark = ACCENTED[ch]
        rows = {y: row for y, row in enumerate(FONT[base].split())}
        offset, mark_rows = MARKS[mark]
        width = len(rows[0])
        shift = (width - 5) // 2
        for i, row in enumerate(mark_rows):
            rows[offset + i] = "".join(row[x - shift] if 0 <= x - shift < 5 else "." for x in range(width))
        return rows
    return {y: row for y, row in enumerate(FONT[ch].split())}


def advance(ch):
    return SPACE_ADVANCE if ch == " " else len(glyph_rows(ch)[0]) + 1


def text_width(text, scale):
    return (sum(advance(c) for c in text.upper()) - 1) * scale


def pixel_text(text, x, y, scale, fill, anchor="start"):
    text = text.upper()
    if anchor == "end":
        x -= text_width(text, scale)
    elif anchor == "middle":
        x -= text_width(text, scale) / 2
    uses = []
    cursor = 0
    for ch in text:
        if ch != " ":
            used_glyphs.add(ch)
            uses.append(f'<use href="#g{ord(ch):x}" x="{cursor}"/>')
        cursor += advance(ch)
    return f'<g transform="translate({x:g} {y:g}) scale({scale})" fill="{fill}">{"".join(uses)}</g>'


def shadow_text(text, x, y, scale, fill, shadow, anchor="start"):
    return pixel_text(text, x + scale, y + scale, scale, shadow, anchor) + pixel_text(text, x, y, scale, fill, anchor)


def glyph_defs():
    defs = []
    for ch in sorted(used_glyphs):
        d = []
        for y, row in glyph_rows(ch).items():
            x = 0
            while x < len(row):
                if row[x] != "#":
                    x += 1
                    continue
                start = x
                while x < len(row) and row[x] == "#":
                    x += 1
                d.append(f"M{start} {y}h{x - start}v1h-{x - start}z")
        defs.append(f'<path id="g{ord(ch):x}" d="{"".join(d)}"/>')
    return "".join(defs)


def pixel_paths(pixels, ox=0, oy=0):
    by_color = {}
    for (x, y), color in pixels.items():
        by_color.setdefault(color, {}).setdefault(y, []).append(x)
    paths = []
    for color in sorted(by_color):
        d = []
        for y, xs in sorted(by_color[color].items()):
            xs.sort()
            i = 0
            while i < len(xs):
                j = i
                while j + 1 < len(xs) and xs[j + 1] == xs[j] + 1:
                    j += 1
                run = (j - i + 1) * PIXEL
                d.append(f"M{ox + xs[i] * PIXEL:g} {oy + y * PIXEL:g}h{run}v{PIXEL}h-{run}z")
                i = j + 1
        paths.append(f'<path fill="{color}" d="{"".join(d)}"/>')
    return "".join(paths)


def slot_style(index, count, step):
    delay = -((count - index) % count) * step
    return f'style="animation: slot{count} {count * step:.2f}s step-end infinite {delay:.2f}s"'


def load_sprite(path):
    with open(path, encoding="utf-8") as f:
        rows = [line.rstrip("\n") for line in f if line.strip()]
    pixels = {(x, y): c for y, row in enumerate(rows) for x, c in enumerate(row) if c in SPRITE_COLORS}
    return pixels, len(rows[0]), len(rows)


def sky():
    rng = random.Random(35)
    stars = []
    for _ in range(40):
        x, y = rng.randint(1, SCENE_W - 2), rng.randint(1, HORIZON - 9)
        stars.append(
            f'<rect class="star" style="animation-delay:{rng.random() * 3:.2f}s" x="{x * PIXEL}" y="{y * PIXEL}" '
            f'width="{PIXEL - 2}" height="{PIXEL - 2}" fill="#dfe6ff"/>'
        )
    moon = {(x, y): "#f5e6b8" for y in range(4, 14) for x in range(127, 137) if math.hypot(x - 131.5, y - 8.5) <= 4.6}
    for x, y in ((129, 7), (130, 7), (133, 10), (133, 11), (128, 10)):
        moon[(x, y)] = "#e0cd96"
    return (
        f'<rect width="{SCENE_W * PIXEL}" height="{HORIZON * PIXEL}" fill="url(#sky)"/>'
        + "".join(stars)
        + f'<circle cx="{131.5 * PIXEL}" cy="{8.5 * PIXEL}" r="{12 * PIXEL}" fill="url(#moonGlow)"/>'
        + pixel_paths(moon)
    )


def fuji():
    cx, peak = 90, 10
    pixels = {}
    for y in range(peak, HORIZON + 1):
        f = (y - peak) / (HORIZON - peak)
        half = 3 + 48 * f ** 1.8
        for x in range(round(cx - half), round(cx + half) + 1):
            snow_line = 15 + (x * 7 + 3) % 4 - (1 if abs(x - cx) < 4 else 0)
            if y < snow_line:
                pixels[(x, y)] = "#e6ecff" if x < cx + 1 else "#b4c0ec"
            else:
                pixels[(x, y)] = "#262a62" if x < cx else "#1d2050"
    return pixel_paths(pixels)


def tokyo_tower():
    cx, top, base = 158, 12, HORIZON
    pixels = {}
    for y in range(top, base + 1):
        f = (y - top) / (base - top)
        half = 0.6 + 4.6 * f ** 1.9
        for x in range(round(cx - half), round(cx + half) + 1):
            if y >= base - 3 and abs(x - cx) < half - 1.6:
                continue
            pixels[(x, y)] = "#ff9a4d" if (x + y) % 2 else "#d4602a"
    for y, half in ((15, 2), (22, 3)):
        for x in range(cx - half, cx + half + 1):
            pixels[(x, y)] = "#ffe2a6"
            pixels[(x, y + 1)] = "#c9541f"
    for y in range(6, top):
        pixels[(cx, y)] = "#ff9a4d"
    return (
        f'<circle cx="{cx * PIXEL}" cy="{20 * PIXEL}" r="{16 * PIXEL}" fill="url(#towerGlow)"/>'
        + pixel_paths(pixels)
        + f'<rect class="beacon" x="{cx * PIXEL}" y="{5 * PIXEL}" width="{PIXEL}" height="{PIXEL}" fill="#ff2a35"/>'
    )


def skyline():
    rng = random.Random(1958)
    pixels = {}
    beacons = []
    x = 0
    while x < SCENE_W:
        w = rng.randint(3, 8)
        if 70 < x < 106:
            height = rng.randint(1, 2)
        elif 146 < x < 170:
            height = rng.randint(2, 4)
        else:
            height = rng.randint(3, 10)
        top = HORIZON - height
        body = "#0f1232" if rng.random() < 0.5 else "#13173d"
        for bx in range(x, min(x + w, SCENE_W)):
            for by in range(top, HORIZON + 1):
                pixels[(bx, by)] = body
        for by in range(top + 1, HORIZON, 2):
            for bx in range(x + 1, min(x + w, SCENE_W) - 1, 2):
                if rng.random() < 0.35:
                    pixels[(bx, by)] = rng.choice(["#ffd88a", "#ffd88a", "#9fd3ff", "#ff9ec7"])
        if height >= 8:
            beacons.append(
                f'<rect class="beacon" style="animation-delay:{rng.random() * 2:.2f}s" x="{(x + w // 2) * PIXEL}" '
                f'y="{(top - 1) * PIXEL}" width="{PIXEL}" height="{PIXEL}" fill="#ff2a35"/>'
            )
        x += w
    return pixel_paths(pixels) + "".join(beacons)


def road():
    base = {}
    phases = [{} for _ in range(ROAD_PHASES)]
    for y in range(HORIZON + 1, SCENE_H):
        d = y - HORIZON
        half = 1 + d / (SCENE_H - HORIZON) * ROAD_SPREAD
        rumble = max(1, round(half * 0.07))
        dash = max(1, round(half * 0.025))
        left, right = 90 - half, 90 + half
        for x in range(SCENE_W):
            if x < left - rumble or x > right + rumble:
                base[(x, y)] = "#07091a"
            elif x < left or x > right:
                base[(x, y)] = "#c8202c"
            else:
                base[(x, y)] = "#23263a"
        for p in range(ROAD_PHASES):
            if math.floor(ROAD_DEPTH / d + 2 * p / ROAD_PHASES) % 2:
                continue
            for x in range(SCENE_W):
                if x < left - rumble or x > right + rumble:
                    phases[p][(x, y)] = "#0f1330"
                elif x < left or x > right:
                    phases[p][(x, y)] = "#eceef4"
            if d >= 3:
                for lane in (90 - half / 2, 90 + half / 2):
                    start = round(lane - dash / 2)
                    for x in range(start, start + dash):
                        phases[p][(x, y)] = "#d7dbe6"
    layers = "".join(
        f'<g {slot_style(p, ROAD_PHASES, ROAD_STEP)}>{pixel_paths(pixels)}{lamps(p)}</g>'
        for p, pixels in enumerate(phases)
    )
    fog = f'<rect y="{HORIZON * PIXEL}" width="{SCENE_W * PIXEL}" height="{8 * PIXEL}" fill="url(#fog)"/>'
    return pixel_paths(base) + fog + layers


def lamps(phase):
    parts = []
    shift = 2 * phase / ROAD_PHASES
    for k in range(2, 40):
        z = 2 * k - shift
        d = ROAD_DEPTH / z
        if not 5 <= d <= SCENE_H - HORIZON + 30:
            continue
        scale = d / (SCENE_H - HORIZON)
        base_y = HORIZON + d
        half = 1 + scale * ROAD_SPREAD
        height = LAMP_HEIGHT * scale
        pole = max(1, round(1.4 * scale))
        arm = max(2, round(7 * scale))
        for side in (-1, 1):
            x = 90 + side * (half + max(1, round(half * 0.07)) + 3 * scale)
            top = base_y - height
            pole_x = x - pole / 2
            arm_x = pole_x if side < 0 else pole_x - arm + pole
            light_x = arm_x + (arm - 2 * pole if side < 0 else 0)
            parts.append(
                f'<circle cx="{(light_x + pole) * PIXEL:.0f}" cy="{(top + pole) * PIXEL:.0f}" r="{8 * scale * PIXEL:.0f}" fill="url(#lampGlow)"/>'
                f'<rect x="{pole_x * PIXEL:.0f}" y="{top * PIXEL:.0f}" width="{pole * PIXEL}" height="{height * PIXEL:.0f}" fill="#2b3150"/>'
                f'<rect x="{arm_x * PIXEL:.0f}" y="{top * PIXEL:.0f}" width="{arm * PIXEL}" height="{pole * PIXEL}" fill="#2b3150"/>'
                f'<rect x="{light_x * PIXEL:.0f}" y="{(top + pole) * PIXEL:.0f}" width="{2 * pole * PIXEL}" height="{pole * PIXEL}" fill="#ffd38a"/>'
            )
    return "".join(parts)


def car(sprite, sprite_w, sprite_h):
    ox, oy = (SCENE_W - sprite_w) // 2 * PIXEL, (CAR_BOTTOM - sprite_h + 1) * PIXEL
    body = {pos: SPRITE_COLORS[c] for pos, c in sprite.items() if c != "t"}
    tread = [pos for pos, c in sprite.items() if c == "t"]
    tread_a = {pos: SPRITE_COLORS["t"] for pos in tread}
    tread_b = {(x, y + 1): SPRITE_COLORS["t"] for x, y in tread if sprite.get((x, y + 1)) == "T"}

    lights = [(x + 1, y + 1) for (x, y), c in sprite.items() if c == "p"]
    tips = [(x + 1, y + 1) for (x, y), c in sprite.items()
            if c == "X" and sprite.get((x - 1, y)) != "X" and sprite.get((x, y - 1)) != "X"]

    glows = "".join(
        f'<circle class="tailglow" cx="{ox + x * PIXEL}" cy="{oy + y * PIXEL}" r="{7 * PIXEL}" fill="url(#tailGlow)"/>'
        for x, y in lights
    )
    flame = {}
    for x, y in tips:
        for dx, dy, color in ((-1, -2, "#ffb347"), (0, -2, "#ffb347"), (-2, -1, "#ff7a2f"), (-1, -1, "#fff3c4"),
                              (0, -1, "#fff3c4"), (1, -1, "#ff7a2f"), (-2, 0, "#ff7a2f"), (-1, 0, "#ffd166"),
                              (0, 0, "#ffd166"), (1, 0, "#ff7a2f"), (-1, 1, "#ff3b3b"), (0, 1, "#ff3b3b")):
            flame[(x + dx, y + dy)] = color
    shadow = (
        f'<ellipse cx="{SCENE_W / 2 * PIXEL}" cy="{(CAR_BOTTOM + 0.6) * PIXEL}" rx="{(sprite_w / 2 + 1) * PIXEL}" '
        f'ry="{1.6 * PIXEL}" fill="#000000" opacity="0.55"/>'
    )
    return (
        f'<g class="sway">{shadow}<g class="bounce">'
        f'{glows}{pixel_paths(body, ox, oy)}'
        f'<g {slot_style(0, 2, 0.06)}>{pixel_paths(tread_a, ox, oy)}</g>'
        f'<g {slot_style(1, 2, 0.06)}>{pixel_paths(tread_b, ox, oy)}</g>'
        f'<g class="flame">{pixel_paths(flame, ox, oy)}</g>'
        f'</g></g>'
    )


def hud(stats):
    sw = SCENE_W * PIXEL
    name = (
        f'<rect x="14" y="14" width="{text_width(NAME, 4) + 36}" height="96" rx="6" fill="#05060f" opacity="0.5"/>'
        + shadow_text(NAME, 28, 26, 4, "#ffffff", "#ff5a1f")
        + pixel_text(ROLE, 28, 70, 2, "#ffb380")
        + pixel_text(f"@{LOGIN}", 28, 90, 2, BLUE)
    )

    panel_y = 262
    rows = [("repositórios", stats["repos"]), ("estrelas", stats["stars"]), ("seguidores", stats["followers"])]
    left = f'<rect x="14" y="{panel_y}" width="232" height="104" rx="6" fill="#05060f" opacity="0.6"/>'
    left += pixel_text("github", 28, panel_y + 12, 2, ORANGE)
    for i, (label, value) in enumerate(rows):
        y = panel_y + 38 + i * 22
        left += pixel_text(label, 28, y, 2, WHITE)
        left += pixel_text(value.zfill(2), 232, y, 2, ORANGE, "end")

    px = sw - 260
    right = f'<rect x="{px}" y="{panel_y}" width="246" height="104" rx="6" fill="#05060f" opacity="0.6"/>'
    right += pixel_text("rpm", px + 14, panel_y + 14, 2, DIM)
    segments_off, segments_on = [], []
    for i in range(16):
        color = "#3ddc84" if i < 10 else ("#ffd166" if i < 13 else "#ff3b3b")
        x = px + 62 + i * 11
        segments_off.append(f'<rect x="{x}" y="{panel_y + 12}" width="8" height="14" fill="#1c2133"/>')
        segments_on.append(f'<rect x="{x}" y="{panel_y + 12}" width="8" height="14" fill="{color}"/>')
    right += "".join(segments_off) + f'<g clip-path="url(#rpmClip)">{"".join(segments_on)}</g>'
    right += (
        f'<rect x="{px + 14}" y="{panel_y + 40}" width="40" height="52" rx="4" fill="none" '
        f'stroke="{ORANGE}" stroke-width="2"/>'
    )
    right += pixel_text("6", px + 22, panel_y + 49, 5, ORANGE)
    for i, speed in enumerate(SPEEDS):
        right += f'<g {slot_style(i, len(SPEEDS), 0.45)}>{pixel_text(str(speed), px + 186, panel_y + 46, 6, WHITE, "end")}</g>'
    right += pixel_text("km/h", px + 232, panel_y + 80, 2, DIM, "end")
    rpm_clip = (
        f'<clipPath id="rpmClip"><rect class="rpm" x="{px + 62}" y="{panel_y + 12}" '
        f'width="{16 * 11}" height="14"/></clipPath>'
    )

    countdown = "".join(
        f'<g class="count" style="animation-delay:{i * 0.45:.2f}s">'
        f'{shadow_text(word, sw / 2, 96, 10, ORANGE if word == "go!" else "#ffffff", "#ff2a35", "middle")}</g>'
        for i, word in enumerate(["3", "2", "1", "go!"])
    )
    return rpm_clip, name + left + right + countdown


def spec_sheet():
    y0 = SHEET_Y
    curb = "".join(
        f'<rect x="{x}" y="{y0}" width="12" height="6" fill="{"#e3242b" if (x // 12) % 2 else "#eef1f5"}"/>'
        for x in range(0, W + 24, 12)
    )
    parts = [f'<g class="curb">{curb}</g>']
    parts.append(shadow_text("ficha técnica", PAD, y0 + 30, 3, ORANGE, "#5a1a00"))
    parts.append(pixel_text(CAR, W - PAD, y0 + 36, 2, DIM, "end"))
    parts.append(f'<rect x="{PAD}" y="{y0 + 66}" width="{W - 2 * PAD}" height="2" fill="{BORDER}"/>')

    grid_y = y0 + 84
    for i, (label, tag, value) in enumerate(SPEC):
        x = PAD + i // 4 * (CELL_W + 24)
        y = grid_y + i % 4 * CELL_H
        cell = f'<rect x="{x}" y="{y}" width="4" height="46" fill="{ORANGE}"/>'
        cursor = x + 16
        for text, color in ((f"{i + 1:02d}", DIMMER), (label, ORANGE), ("· " + tag, DIM)):
            cell += pixel_text(text, cursor, y + 6, 2, color)
            cursor += text_width(text, 2) + 2 * (SPACE_ADVANCE + 1)
        cell += pixel_text(value, x + 16, y + 30, 2, WHITE)
        parts.append(f'<g class="cell" style="animation-delay:{1.2 + i * 0.12:.2f}s">{cell}</g>')

    footer_y = grid_y + 4 * CELL_H + 6
    parts.append(f'<rect x="{PAD}" y="{footer_y}" width="{W - 2 * PAD}" height="2" fill="{BORDER}"/>')
    for i, (label, value) in enumerate((("piloto", DRIVER), ("contato", CONTACT))):
        y = footer_y + 20 + i * 26
        parts.append(pixel_text(label, PAD, y, 2, ORANGE))
        parts.append(pixel_text(value, PAD + 112, y, 2, WHITE))
    return "".join(parts), footer_y + 76


def fetch_json(url, token):
    request = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    )
    with urllib.request.urlopen(request, timeout=15) as resp:
        return json.load(resp)


def fetch_github_stats(login, token):
    stats = {"repos": "--", "stars": "--", "followers": "--"}
    if not token:
        return stats
    try:
        user = fetch_json(f"https://api.github.com/users/{login}", token)
        stats["followers"] = str(user.get("followers", "--"))
        stats["repos"] = str(user.get("public_repos", "--"))

        repos = fetch_json(f"https://api.github.com/users/{login}/repos?per_page=100&type=owner", token)
        stats["stars"] = str(sum(r.get("stargazers_count", 0) for r in repos if not r.get("fork")))
    except Exception as e:
        print(f"warning: failed to fetch live stats: {e}", file=sys.stderr)
    return stats


def build_svg(sprite, sprite_w, sprite_h, stats):
    scene = sky() + fuji() + tokyo_tower() + skyline() + road() + car(sprite, sprite_w, sprite_h)
    rpm_clip, hud_svg = hud(stats)
    sheet, H = spec_sheet()
    slot_css = "\n      ".join(
        f"@keyframes slot{n} {{ 0% {{ opacity: 1; }} {100 / n:.3f}% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}"
        for n in sorted({ROAD_PHASES, 2, len(SPEEDS)})
    )

    return f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{NAME}, {ROLE}">
  <defs>
    <style>
      .star {{ animation: twinkle 2.6s ease-in-out infinite; }}
      .beacon {{ animation: twinkle 1.2s steps(2) infinite; }}
      .tailglow {{ animation: glow 1.6s ease-in-out infinite; }}
      .sway {{ animation: sway 3.4s ease-in-out infinite; }}
      .bounce {{ animation: bounce 0.32s ease-in-out infinite; }}
      .flame {{ opacity: 0; animation: pop 3.6s linear infinite 2.4s; }}
      .count {{ animation: count 0.45s linear both; }}
      .rpm {{ transform-box: fill-box; transform-origin: left; animation: rev 2.4s steps(16) infinite; }}
      .cell {{ animation: reveal 0.5s ease-out both; }}
      .curb {{ animation: curb 0.5s linear infinite; }}
      {slot_css}
      @keyframes twinkle {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.25; }} }}
      @keyframes glow {{ 0%, 100% {{ opacity: 0.75; }} 50% {{ opacity: 1; }} }}
      @keyframes sway {{ 0%, 100% {{ transform: translateX(-8px); }} 50% {{ transform: translateX(8px); }} }}
      @keyframes bounce {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-2px); }} }}
      @keyframes pop {{ 0%, 80% {{ opacity: 0; }} 81%, 84% {{ opacity: 1; }} 85%, 88% {{ opacity: 0; }} 89%, 92% {{ opacity: 1; }} 93%, 100% {{ opacity: 0; }} }}
      @keyframes count {{ 0% {{ opacity: 0; }} 1%, 85% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}
      @keyframes rev {{ 0% {{ transform: scaleX(0.35); }} 80% {{ transform: scaleX(1); }} 100% {{ transform: scaleX(0.55); }} }}
      @keyframes reveal {{ from {{ opacity: 0; transform: translateX(-12px); }} to {{ opacity: 1; transform: translateX(0); }} }}
      @keyframes curb {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-24px); }} }}
    </style>
    <clipPath id="cardClip"><rect width="{W}" height="{H}" rx="12"/></clipPath>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#060a1c"/><stop offset="0.7" stop-color="#1d1240"/><stop offset="1" stop-color="#4a1a5c"/>
    </linearGradient>
    <linearGradient id="fog" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2a1448" stop-opacity="0.8"/><stop offset="1" stop-color="#2a1448" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="moonGlow"><stop offset="0" stop-color="#f5e6b8" stop-opacity="0.25"/><stop offset="1" stop-color="#f5e6b8" stop-opacity="0"/></radialGradient>
    <radialGradient id="towerGlow"><stop offset="0" stop-color="#ff8a3d" stop-opacity="0.3"/><stop offset="1" stop-color="#ff8a3d" stop-opacity="0"/></radialGradient>
    <radialGradient id="lampGlow"><stop offset="0" stop-color="#ffb347" stop-opacity="0.45"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
    <radialGradient id="tailGlow"><stop offset="0" stop-color="#ff2a35" stop-opacity="0.6"/><stop offset="1" stop-color="#ff2a35" stop-opacity="0"/></radialGradient>
    {rpm_clip}
    {glyph_defs()}
  </defs>
  <g clip-path="url(#cardClip)">
    <rect width="{W}" height="{H}" fill="{BG}"/>
    <g shape-rendering="crispEdges">{scene}</g>
    <g shape-rendering="crispEdges">{hud_svg}</g>
    <g shape-rendering="crispEdges">{sheet}</g>
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{BORDER}"/>
</svg>
'''


def main():
    sprite, sprite_w, sprite_h = load_sprite(SPRITE_PATH)
    stats = fetch_github_stats(LOGIN, TOKEN)
    svg = build_svg(sprite, sprite_w, sprite_h, stats)
    os.makedirs(os.path.dirname(OUT_PATH) or ".", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
