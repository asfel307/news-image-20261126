#!/usr/bin/env python3
"""Draw "The World Today" front page for Thursday, 26 November 2026.

Six verified world-news stories rendered as a one-page newspaper with
Pillow vector drawing only: no photos, no downloaded assets, no network.
The output is fully deterministic (fixed fonts, layout and colours; the
PNG carries no timestamps).

Usage:  python3 render.py [output.png]     (default: entry.png here)
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

PAGE_W, PAGE_H = 1024, 1024
EDGE = 40          # outer margin
GUTTER = 24        # gap between the two middle columns

# Warm newsprint palette.
PAPER = (248, 242, 228)
INK = (30, 40, 48)
TEAL = (14, 74, 74)
TEAL_SOFT = (34, 112, 112)
GOLD = (186, 140, 32)
GOLD_PALE = (214, 176, 82)
RULE_COL = (172, 150, 112)
MUTED = (92, 102, 110)
CRIMSON = (142, 48, 48)
WHITE = (253, 251, 245)

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF_B = os.path.join(FONT_DIR, "LiberationSerif-Bold.ttf")
SERIF_R = os.path.join(FONT_DIR, "LiberationSerif-Regular.ttf")
SANS_R = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")
SANS_B = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")


def make_font(path, size):
    return ImageFont.truetype(path, size)


def width_of(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap into lines no wider than max_w."""
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            out.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if width_of(draw, trial, fnt) <= max_w:
                line = trial
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


def put_wrapped(draw, x, y, text, fnt, max_w, fill, spacing=None):
    """Draw wrapped text starting at (x, y); return y below last line."""
    if spacing is None:
        spacing = int(fnt.size * 1.32)
    for line in wrap_text(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += spacing
    return y


def put_tracked(draw, cx, y, text, fnt, fill, gap=5):
    """Centred capitals with letter spacing; return y below the line."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + gap * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + gap
    return y + int(fnt.size * 1.35)


def rule(draw, y, x0=EDGE, x1=PAGE_W - EDGE, fill=RULE_COL, thick=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=thick)


# ------------------------------------------------------------------ pictograms
# Every pictogram fits inside the box (x, y, side).

def pic_candle(draw, x, y, side):
    """A lit memorial candle."""
    cx = x + side // 2
    draw.ellipse([cx - 30, y + 4, cx + 30, y + 58], fill=(235, 200, 96))
    draw.polygon([(cx, y + 8), (cx + 12, y + 32), (cx, y + 46),
                  (cx - 12, y + 32)], fill=GOLD)
    draw.ellipse([cx - 5, y + 28, cx + 5, y + 42], fill=(242, 212, 112))
    draw.line([(cx, y + 46), (cx, y + 54)], fill=INK, width=3)
    draw.rectangle([cx - 17, y + 54, cx + 17, y + side - 10],
                   fill=WHITE, outline=TEAL, width=3)
    draw.rectangle([cx - 17, y + 54, cx + 17, y + 66], fill=TEAL)
    draw.rectangle([cx - 28, y + side - 10, cx + 28, y + side - 4],
                   fill=GOLD)


def pic_tariff(draw, x, y, side):
    """A globe with a percent sign below it (trade tariffs)."""
    cx, cy = x + side // 2, y + 36
    r = 32
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 232, 232),
                 outline=TEAL, width=3)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
                 outline=TEAL_SOFT, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=TEAL_SOFT, width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340,
             fill=TEAL_SOFT, width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 20, 160,
             fill=TEAL_SOFT, width=2)
    pct = make_font(SANS_B, 26)
    t = "%"
    draw.text((cx - width_of(draw, t, pct) / 2, y + 70), t,
              font=pct, fill=CRIMSON)
    draw.line([(x + 8, y + side - 6), (x + side - 8, y + side - 6)],
              fill=GOLD, width=3)


def pic_flag(draw, x, y, side):
    """A flag above a sealed envelope (diplomacy)."""
    draw.line([(x + 20, y + 8), (x + 20, y + side - 28)], fill=GOLD, width=4)
    draw.ellipse([x + 15, y + 3, x + 25, y + 13], fill=GOLD)
    fx0, fy0 = x + 24, y + 12
    fx1, fy1 = x + side - 8, y + 54
    draw.rectangle([fx0, fy0, fx1, fy1], fill=CRIMSON, outline=INK, width=2)
    mx, my = (fx0 + fx1) // 2, (fy0 + fy1) // 2
    draw.rectangle([mx - 5, fy0 + 10, mx + 5, fy1 - 10], fill=WHITE)
    draw.rectangle([fx0 + 10, my - 5, fx1 - 10, my + 5], fill=WHITE)
    ex0, ey0 = x + 10, y + side - 32
    ex1, ey1 = x + side - 10, y + side - 4
    draw.rectangle([ex0, ey0, ex1, ey1], fill=WHITE, outline=TEAL, width=3)
    draw.line([(ex0, ey0), ((ex0 + ex1) // 2, ey0 + 13)], fill=TEAL, width=3)
    draw.line([(ex1, ey0), ((ex0 + ex1) // 2, ey0 + 13)], fill=TEAL, width=3)


def pic_flame(draw, x, y, side):
    """A fireball over a road (tanker fire)."""
    cx = x + side // 2
    draw.polygon([(cx, y + 6), (cx + 26, y + 40), (cx + 14, y + 40),
                  (cx + 22, y + 62), (cx, y + 82), (cx - 22, y + 62),
                  (cx - 14, y + 40), (cx - 26, y + 40)], fill=GOLD)
    draw.polygon([(cx, y + 30), (cx + 13, y + 54), (cx, y + 72),
                  (cx - 13, y + 54)], fill=CRIMSON)
    draw.rectangle([x + 6, y + side - 22, x + side - 6, y + side - 14],
                   fill=INK)
    for dx in (14, 46, 78):
        draw.rectangle([x + dx, y + side - 20, x + dx + 16, y + side - 16],
                       fill=GOLD_PALE)


def pic_shirt(draw, x, y, side):
    """A shirt on a hanger (garment workers)."""
    cx = x + side // 2
    draw.arc([cx - 8, y + 2, cx + 8, y + 18], 180, 360, fill=GOLD, width=3)
    draw.line([(cx, y + 10), (cx, y + 20)], fill=GOLD, width=3)
    draw.line([(cx - 34, y + 30), (cx + 34, y + 30)], fill=GOLD, width=3)
    draw.line([(cx - 34, y + 30), (cx, y + 20)], fill=GOLD, width=3)
    draw.line([(cx + 34, y + 30), (cx, y + 20)], fill=GOLD, width=3)
    draw.polygon([
        (cx - 22, y + 32), (cx - 40, y + 42), (cx - 30, y + 60),
        (cx - 30, y + side - 6), (cx + 30, y + side - 6),
        (cx + 30, y + 60), (cx + 40, y + 42), (cx + 22, y + 32),
        (cx + 10, y + 38), (cx, y + 46), (cx - 10, y + 38),
    ], fill=TEAL, outline=INK, width=2)
    draw.line([(x + 6, y + side - 24), (x + side - 22, y + side - 36)],
              fill=GOLD, width=3)
    draw.ellipse([x + side - 26, y + side - 40, x + side - 18,
                  y + side - 32], outline=GOLD, width=2)


def pic_chess(draw, x, y, side):
    """A small chessboard with a pawn and a rook."""
    cell = side // 4
    for r in range(4):
        for c in range(4):
            col = INK if (r + c) % 2 == 0 else WHITE
            draw.rectangle([x + c * cell, y + r * cell,
                            x + (c + 1) * cell, y + (r + 1) * cell],
                           fill=col, outline=TEAL, width=1)
    px = x + cell + cell // 2
    py = y + 2 * cell + cell // 2
    draw.ellipse([px - 9, py - 16, px + 9, py + 2], fill=GOLD)
    draw.polygon([(px - 12, py + 14), (px + 12, py + 14), (px + 6, py),
                  (px - 6, py)], fill=GOLD)
    draw.rectangle([px - 14, py + 12, px + 14, py + 17], fill=GOLD)
    rx, ry = x + 3 * cell, y + 3 * cell
    draw.rectangle([rx + 3, ry + 8, rx + cell - 3, ry + cell - 3],
                   fill=WHITE, outline=INK, width=2)
    draw.rectangle([rx + 3, ry + 8, rx + cell - 3, ry + 15],
                   fill=WHITE, outline=INK, width=2)
    for k in range(3):
        kx = rx + 5 + k * 7
        draw.rectangle([kx, ry + 8, kx + 5, ry + 14], fill=WHITE,
                       outline=INK, width=1)


# -------------------------------------------------------------------- stories

STORIES = [
    {
        "kicker": "LEAD STORY — RUSSIA",
        "headline": "The Toll, Leaked",
        "body": ("Published on Wednesday, 25 November, a leaked Rosstat "
                 "dataset analysed by BBC Russian and Mediazona puts "
                 "Russian military deaths at at least 490,334 since the "
                 "February 2022 invasion. Experts put the true figure at "
                 "527,295–644,471 — and 65% of Russians aged 18–24 who "
                 "died in 2025 were killed in the war."),
        "pic": pic_candle,
    },
    {
        "kicker": "UNITED STATES",
        "headline": "Trump's New Tariff Salvo",
        "body": ("President Donald Trump on Wednesday, 25 November, "
                 "proposed new tariffs on 14 major trading partners, "
                 "including China, Japan and the EU, to counter excess "
                 "industrial capacity. China faces the highest capped "
                 "rate, 20% — rising to 40% if the trade truce "
                 "unravels."),
        "pic": pic_tariff,
    },
    {
        "kicker": "NORTH KOREA",
        "headline": "Pyongyang Expels Swiss Envoy",
        "body": ("North Korea ordered Swiss diplomat Sylvain Astier to "
                 "leave within 48 hours and demanded the closure of "
                 "Switzerland's diplomatic office in Pyongyang, KCNA "
                 "said on Wednesday, 25 November. The move answers Swiss "
                 "sanctions over the Songdowon children's camp; the office "
                 "only opened in late October."),
        "pic": pic_flag,
    },
    {
        "kicker": "EGYPT",
        "headline": "31 Killed in Cairo Tanker Fire",
        "body": ("At least 31 people were killed and 21 injured when a "
                 "fuel tanker overturned and caught fire on Cairo's ring "
                 "road on Wednesday, 25 November, Egypt's health ministry "
                 "said. The blaze spread to 27 vehicles near Tunnel 10 "
                 "in Giza. The cause of the crash is under "
                 "investigation."),
        "pic": pic_flame,
    },
    {
        "kicker": "BANGLADESH",
        "headline": "Bangladesh Wage Win",
        "body": ("Bangladesh's garment workers have won a 36% "
                 "minimum-wage rise, agreed by the wage board in the early "
                 "hours of Wednesday, 25 November, after weeks of "
                 "protests. Pay rises from 12,500 taka to 17,000 taka — "
                 "about $136 a month — from 1 December."),
        "pic": pic_shirt,
    },
    {
        "kicker": "CHESS",
        "headline": "Chess: Level at 1–1",
        "body": ("Game 2 of the World Championship between Gukesh and "
                 "Sindarov in Geneva ended in a quick 20-move draw in the "
                 "London System on Wednesday, 25 November. The score "
                 "stands level at 1–1; Game 3 is played today, Thursday, "
                 "26 November, with Sindarov holding White."),
        "pic": pic_chess,
    },
]


def kicker_line(draw, x, y, text):
    fnt = make_font(SANS_B, 15)
    draw.text((x, y), text, font=fnt, fill=TEAL)
    return y + 21


def headline_block(draw, x, y, text, size, max_w):
    fnt = make_font(SERIF_B, size)
    return put_wrapped(draw, x, y, text, fnt, max_w, INK,
                       spacing=int(size * 1.12))


def render():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- dateline bar
    f_top = make_font(SANS_B, 17)
    draw.text((EDGE, 26), "THURSDAY, 26 NOVEMBER 2026", font=f_top,
              fill=INK)
    right = "WORLD EDITION  •  No. 330"
    draw.text((PAGE_W - EDGE - width_of(draw, right, f_top), 26), right,
              font=f_top, fill=MUTED)
    rule(draw, 54, thick=2)

    # ---- masthead
    f_mast = make_font(SERIF_B, 96)
    title = "The World Today"
    tw = width_of(draw, title, f_mast)
    draw.text(((PAGE_W - tw) / 2, 58), title, font=f_mast, fill=INK)
    put_tracked(draw, PAGE_W // 2, 164, "SIX STORIES FROM AROUND THE GLOBE",
                make_font(SANS_B, 15), TEAL, gap=5)
    rule(draw, 192, thick=3)
    rule(draw, 197, thick=1)

    # ---- lead story, full width
    lead = STORIES[0]
    y = 212
    y = kicker_line(draw, EDGE, y, lead["kicker"])
    y = headline_block(draw, EDGE, y, lead["headline"], 46, 660)
    y += 6
    y = put_wrapped(draw, EDGE, y, lead["body"], make_font(SERIF_R, 19),
                    660, INK, spacing=25)
    lead["pic"](draw, 760, 216, 200)

    # ---- divider above the grid
    rule(draw, 416)

    # ---- 2 x 2 grid: stories 2-5
    col_w = (PAGE_W - 2 * EDGE - GUTTER) // 2
    rows_y = [430, 650]
    cols_x = [EDGE, EDGE + col_w + GUTTER]
    for idx, story in enumerate(STORIES[1:5]):
        cx = cols_x[idx % 2]
        cy = rows_y[idx // 2]
        cy = kicker_line(draw, cx, cy, story["kicker"])
        cy = headline_block(draw, cx, cy, story["headline"], 27, col_w)
        cy += 4
        pic_side = 104
        story["pic"](draw, cx, cy + 2, pic_side)
        put_wrapped(draw, cx + pic_side + 14, cy + 2, story["body"],
                    make_font(SANS_R, 15), col_w - pic_side - 14, INK,
                    spacing=20)
    mid_x = EDGE + col_w + GUTTER // 2
    draw.line([(mid_x, 430), (mid_x, 856)], fill=RULE_COL, width=1)
    rule(draw, 640)
    rule(draw, 866)

    # ---- bottom strip: story 6
    last = STORIES[5]
    bx = EDGE + 128
    by = 880
    by = kicker_line(draw, bx, by, last["kicker"])
    by = headline_block(draw, bx, by, last["headline"], 27,
                        PAGE_W - 2 * EDGE - 128)
    by += 2
    put_wrapped(draw, bx, by, last["body"], make_font(SANS_R, 16),
                PAGE_W - 2 * EDGE - 128, INK, spacing=21)
    last["pic"](draw, EDGE, 884, 108)

    # ---- footer
    rule(draw, 992, thick=2)
    f_foot = make_font(SANS_R, 14)
    draw.text((EDGE, 1000),
              "Sources: BBC Russian • Mediazona • Reuters • KCNA • AP • "
              "FIDE",
              font=f_foot, fill=MUTED)
    tail = "Compiled Thursday, 26 November 2026 (UTC)"
    draw.text((PAGE_W - EDGE - width_of(draw, tail, f_foot), 1000), tail,
              font=f_foot, fill=MUTED)

    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE,
                                                            "entry.png")
    img = render()
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
