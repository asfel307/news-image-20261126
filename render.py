"""Front page of 'The World Today' for 26 November 2026.

Renders a single 1024x1024 newspaper page from six news items dated
25 November 2026. Everything is drawn with Pillow primitives; no image
assets are loaded. Run directly or through main.py:

    python3 render.py [output_dir]
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
PAPER = (253, 251, 243)
INK = (17, 17, 17)
FAINT = (90, 88, 80)
ACCENT = (139, 26, 26)
RULE = (17, 17, 17)
PANEL = (240, 236, 224)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill=INK, gap=4):
    """Draw lines top-down; returns the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def hrule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker_head_body(draw, x, y, w, kick, head, body, source,
                     head_size=22, body_size=15):
    """One story block: small red kicker, bold headline, body, source."""
    kf = font(SANS_BOLD, 12)
    hf = font(SERIF, head_size)
    bf = font(SANS, body_size)
    sf = font(SERIF_REG, 12)
    draw.text((x, y), kick, font=kf, fill=ACCENT)
    y += 20
    y = draw_lines(draw, x, y, wrap(draw, head, hf, w), hf, gap=2)
    y += 4
    y = draw_lines(draw, x, y, wrap(draw, body, bf, w), bf, gap=3)
    y += 6
    draw.text((x, y), source, font=sf, fill=FAINT)
    return y


def bar_panel(draw, x, y, w, h):
    """Small horizontal-bar pictogram for the lead death tolls."""
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    tf = font(SANS_BOLD, 13)
    lf = font(SANS, 12)
    draw.text((x + 14, y + 10), "WAR DEAD SINCE FEB 2022", font=tf, fill=INK)
    rows = [
        ("Leaked count", 490334, 644471),
        ("Low estimate", 527295, 644471),
        ("High estimate", 644471, 644471),
    ]
    by = y + 40
    for label, value, top in rows:
        draw.text((x + 14, by), label, font=lf, fill=INK)
        bar_x = x + 14
        bar_y = by + 17
        bar_w = w - 28
        draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + 14],
                       outline=INK, width=1)
        fill_w = int(bar_w * value / top)
        draw.rectangle([bar_x, bar_y, bar_x + fill_w, bar_y + 14],
                       fill=ACCENT)
        draw.text((x + 14, bar_y + 17), f"{value:,}", font=lf, fill=INK)
        by += 50
    draw.text((x + 14, by + 2), "Source: Rosstat leak / experts",
              font=font(SERIF_REG, 11), fill=FAINT)


def chessboard(draw, x, y, size):
    """8x8 board pictogram with two kings marked."""
    sq = size // 8
    for r in range(8):
        for c in range(8):
            fill = (235, 230, 215) if (r + c) % 2 == 0 else (60, 60, 60)
            draw.rectangle([x + c * sq, y + r * sq,
                            x + (c + 1) * sq, y + (r + 1) * sq], fill=fill)
    draw.rectangle([x, y, x + size, y + size], outline=INK, width=2)
    # Kings as filled discs with a contrasting ring: black king on the
    # top rank, white king on the bottom rank (both on the e-file).
    kx = x + 4 * sq + sq // 2
    r = sq // 2 - 2
    d_top = y + sq // 2
    d_bot = y + 7 * sq + sq // 2
    draw.ellipse([kx - r, d_top - r, kx + r, d_top + r],
                 fill=(20, 20, 20), outline=(255, 255, 255), width=2)
    draw.ellipse([kx - r, d_bot - r, kx + r, d_bot + r],
                 fill=(255, 255, 255), outline=(20, 20, 20), width=2)


def render():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(img)

    # Double outer frame.
    d.rectangle([10, 10, PAGE - 11, PAGE - 11], outline=INK, width=3)
    d.rectangle([18, 18, PAGE - 19, PAGE - 19], outline=INK, width=1)

    # Masthead.
    title = font(SERIF, 66)
    tw = d.textlength("The World Today", font=title)
    d.text(((PAGE - tw) / 2, 30), "The World Today", font=title, fill=INK)
    hrule(d, 36, PAGE - 36, 112, width=2)

    # Dateline row with rules on both sides.
    date_f = font(SANS_BOLD, 16)
    date = "THURSDAY, 26 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    cx = (PAGE - dw) / 2
    hrule(d, 36, cx - 18, 130, width=1)
    hrule(d, cx + dw + 18, PAGE - 36, 130, width=1)
    d.text((cx, 120), date, font=date_f, fill=INK)
    hrule(d, 36, PAGE - 36, 146, width=4)

    # ---- Lead story (full width, text left, bar panel right) ----
    lead_x, lead_y = 36, 162
    lead_w = 600
    kf = font(SANS_BOLD, 13)
    d.text((lead_x, lead_y), "LEAD STORY  •  RUSSIA–UKRAINE WAR",
           font=kf, fill=ACCENT)
    hf = font(SERIF, 31)
    y = draw_lines(d, lead_x, lead_y + 24,
                   wrap(d, "Leaked figures put Russian war dead above 490,000",
                        hf, lead_w), hf, gap=2)
    bf = font(SANS, 17)
    y = draw_lines(d, lead_x, y + 6,
                   wrap(d, "Rosstat data shows at least 490,334 soldiers "
                           "dead since February 2022. Expert estimates run "
                           "from 527,295 to 644,471. Of Russians aged 18–24 "
                           "who died in 2025, 65% were killed in the war.",
                        bf, lead_w), bf, gap=4)
    d.text((lead_x, y + 8), "BBC Russian / Mediazona",
           font=font(SERIF_REG, 13), fill=FAINT)
    bar_panel(d, 668, 162, 320, 208)

    hrule(d, 36, PAGE - 36, 392, width=2)

    # ---- Row A: tariffs | North Korea ----
    col_w = 452
    kicker_head_body(
        d, 36, 408, col_w,
        "TRADE  •  UNITED STATES",
        "Trump proposes new tariffs on 14 partners",
        "China faces the highest rate, 20%, rising to 40% if the "
        "trade truce fails. Japan and the EU are among the others named.",
        "Reuters")
    d.line([(512, 408), (512, 596)], fill=FAINT, width=1)
    kicker_head_body(
        d, 536, 408, col_w,
        "DIPLOMACY  •  KOREAN PENINSULA",
        "North Korea expels Swiss diplomat",
        "Pyongyang orders envoy Sylvain Astier out within 48 hours and "
        "demands the Swiss office close, in retaliation for Swiss "
        "sanctions over the Songdowon children's camp.",
        "KCNA via AP / Reuters")

    hrule(d, 36, PAGE - 36, 612, width=2)

    # ---- Row B: Cairo fire | Bangladesh wages ----
    kicker_head_body(
        d, 36, 628, col_w,
        "EGYPT  •  CAIRO",
        "Tanker fire on ring road kills 31",
        "A fuel tanker overturns and catches fire near Tunnel 10 in "
        "Giza. The blaze spreads to 27 vehicles; 21 people are injured.",
        "BBC / Egyptian Health Ministry")
    d.line([(512, 628), (512, 816)], fill=FAINT, width=1)
    kicker_head_body(
        d, 536, 628, col_w,
        "LABOUR  •  BANGLADESH",
        "Garment workers win 36% pay rise",
        "The minimum wage rises from 12,500 to 17,000 taka — about "
        "$136 a month — from 1 December, after weeks of protests.",
        "AP / Reuters")

    hrule(d, 36, PAGE - 36, 832, width=2)

    # ---- Bottom strip: chess, text left, board right ----
    strip_y = 848
    kicker_head_body(
        d, 36, strip_y, 700,
        "SPORT  •  WORLD CHESS CHAMPIONSHIP, GENEVA",
        "Gukesh–Sindarov Game 2 drawn in 20 moves",
        "The score stands at 1–1. Game 3 is played on Thursday 26 "
        "November, with Sindarov to have White.",
        "Chess.com / FIDE",
        head_size=22, body_size=15)
    chessboard(d, 856, 852, 112)

    # Footer.
    hrule(d, 36, PAGE - 36, 978, width=1)
    ff = font(SANS, 11)
    foot = "All stories dated 25 November 2026  •  Sources: BBC, Reuters, AP, Chess.com / FIDE"
    fw = d.textlength(foot, font=ff)
    d.text(((PAGE - fw) / 2, 986), foot, font=ff, fill=FAINT)

    return img


def main(argv):
    out_dir = argv[1] if len(argv) > 1 else os.environ.get(
        "MAKEFUN_OUTPUT_DIR", os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    render().save(path, format="PNG")
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
