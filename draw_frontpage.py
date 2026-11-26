#!/usr/bin/env python3
"""Draw the 26 Nov 2026 front page: THE WORLD IN ONE DAY.
1024x1024, dense broadsheet, 38 stories / 11 regions / 14 fields.
Drawn with PIL from scratch (this script runs on the author's machine only).
The entry's main.py is stdlib-only and just copies the PNG this makes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "fonts")
W, H = 1024, 1024
M = 22                      # margin
CW = W - 2 * M              # content width 980

# palette (cream broadsheet, like the top-scoring entries)
PAPER   = (247, 243, 232)
INK     = (22, 22, 22)
RED     = (178, 34, 34)
DARKRED = (139, 0, 0)
NAVY    = (18, 38, 66)
BLUE    = (30, 80, 140)
GREY    = (110, 108, 100)
LGREY   = (200, 196, 184)
WHITE   = (255, 255, 255)
CREAM2  = (238, 232, 214)
ORANGE  = (224, 110, 30)
GOLD    = (201, 162, 39)
GREEN   = (34, 120, 60)

def font(name, size):
    return ImageFont.truetype(os.path.join(F, name), size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS    = lambda s: font("DejaVuSans.ttf", s)
SANS_B  = lambda s: font("DejaVuSans-Bold.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text(x, y, s, f, fill=INK, anchor="la"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)

def wrap(s, f, maxw):
    """Greedy wrap to a list of lines fitting maxw pixels."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(x, y, lines, f, fill=INK, lh=None, anchor="la"):
    if lh is None:
        lh = int(f.size * 1.28)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill, anchor=anchor)
        y += lh
    return y

def rule(x0, x1, y, w=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)

def tag(x, y, label, bg=RED, fg=WHITE, f=None):
    """Small filled label tag; returns width."""
    f = f or SANS_B(11)
    tw = d.textlength(label, font=f) + 12
    th = 18
    d.rectangle([x, y, x + tw, y + th], fill=bg)
    d.text((x + 6, y + 3), label, font=f, fill=fg)
    return tw

def howsure(x, y, label):
    """How-sure chip: CONFIRMED green, REPORTED amber, OFFICIAL blue, CLAIMED red."""
    col = {"CONFIRMED": GREEN, "REPORTED": (176, 120, 0),
           "OFFICIAL": BLUE, "CLAIMED": RED}.get(label, GREY)
    f = SANS_B(9)
    tw = d.textlength(label, font=f) + 10
    d.rectangle([x, y, x + tw, y + 15], outline=col, width=1)
    d.text((x + 5, y + 3), label, font=f, fill=col)
    return tw

# ---------------------------------------------------------------- masthead
y = 14
text(M, y, "ONE DAY  \u00b7  ONE IMAGE  \u00b7  THE WORLD, SUMMED UP",
     SANS_B(11), fill=GREY)
text(W - M, y, "MAKE.FUN DAILY EDITION", SANS_B(11), fill=GREY, anchor="ra")
y = 30
text(W // 2, y, "THE WORLD IN ONE DAY", SERIF_B(50), anchor="ma")
y = 88
text(W // 2, y, "THURSDAY  26  NOVEMBER  2026", SANS_B(24), fill=RED, anchor="ma")
y = 116
text(W // 2, y, "38 STORIES  \u00b7  11 REGIONS  \u00b7  14 FIELDS  \u00b7  EVERY ONE DATED THU 26 NOV 2026",
     SANS_B(12), anchor="ma")
rule(M, W - M, 132, 3)

# ---------------------------------------------------------------- timeline
y = 138
text(M, y, "THE DAY, HOUR BY HOUR \u2014 TIMES AS REPORTED", SANS_B(11), fill=RED)
tl = [("00:31 CAIRO", "Tanker fire kills 31"),
      ("01:29 WIB", "Labuan quake M4.0"),
      ("08:30 TAIPEI", "Taipei answers US tariffs"),
      ("10:15 KST", "Yoon ruling"),
      ("15:00 CET", "Chess Game 3"),
      ("18:45 CET", "Europa League"),
      ("20:20 ET", "Chiefs\u2013Bills")]
ty = 156
tx = M
step = CW / len(tl)
d.line([(M + 4, ty + 4), (W - M - 4, ty + 4)], fill=LGREY, width=2)
for t, label in tl:
    cx = tx + step / 2
    d.ellipse([cx - 4, ty, cx + 4, ty + 8], fill=RED)
    text(cx, ty + 12, t, SANS_B(10), anchor="ma")
    text(cx, ty + 24, label, SANS(8), anchor="ma")
    tx += step
rule(M, W - M, 196, 2)

# ---------------------------------------------------------------- lead scenes
# Each scene is a flat drawn illustration, ~318 x 128.
def scene_refinery(x, y, w, h):
    """Ras Tanura: refinery towers, orange flames, black smoke, sun."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 190))
    d.ellipse([x + w - 52, y + 12, x + w - 12, y + 52], fill=(240, 200, 90))
    # smoke
    for cx, cy, r in [(x + 60, y + 26, 22), (x + 92, y + 18, 26), (x + 128, y + 28, 20),
                      (x + 190, y + 22, 24), (x + 222, y + 30, 18)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(60, 58, 54))
    # towers
    for tx, tw, th in [(x + 18, 26, 78), (x + 56, 20, 96), (x + 88, 30, 62),
                       (x + 150, 24, 88), (x + 186, 18, 102), (x + 216, 28, 70),
                       (x + 258, 22, 92)]:
        d.rectangle([tx, y + h - th, tx + tw, y + h], fill=(40, 38, 36))
        d.rectangle([tx + 4, y + h - th - 10, tx + tw - 4, y + h - th], fill=(40, 38, 36))
    # flames at base
    for fx in [x + 30, x + 100, x + 170, x + 240]:
        d.polygon([(fx, y + h), (fx + 12, y + h - 26), (fx + 24, y + h)], fill=ORANGE)
        d.polygon([(fx + 5, y + h), (fx + 12, y + h - 14), (fx + 19, y + h)], fill=(250, 210, 60))
    d.rectangle([x, y + h - 6, x + w, y + h], fill=(30, 30, 30))

def scene_toll(x, y, w, h):
    """Russian toll: dark navy, rising bar chart, big 490,334, LEAKED stamp."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # bar chart along the bottom, clear of the stamp and number above
    bars = [8, 12, 16, 20, 24, 28, 30]
    bw = 26
    bx = x + 22
    for b in bars:
        d.rectangle([bx, y + h - 10 - b, bx + bw, y + h - 10], fill=(120, 140, 170))
        bx += bw + 8
    d.rectangle([x + 22, y + h - 10, x + w - 22, y + h - 8], fill=(200, 200, 200))
    text(x + w - 16, y + 8, "490,334", SERIF_B(32), fill=WHITE, anchor="ra")
    text(x + w - 16, y + 44, "RUSSIAN SOLDIERS DEAD", SANS_B(11), fill=(200, 210, 230), anchor="ra")
    # LEAKED stamp, top-left below the kicker tag, clear of the bars
    sx, sy = x + 22, y + 32
    d.rectangle([sx, sy, sx + 92, sy + 24], outline=(230, 60, 60), width=2)
    text(sx + 46, sy + 4, "LEAKED", SANS_B(13), fill=(230, 60, 60), anchor="ma")

def scene_market(x, y, w, h):
    """Markets: falling red line chart on grid, big red down arrow."""
    d.rectangle([x, y, x + w, y + h], fill=WHITE)
    for gx in range(x + 20, x + w - 10, 28):
        d.line([(gx, y + 10), (gx, y + h - 10)], fill=(225, 225, 225), width=1)
    for gy in range(y + 14, y + h - 8, 22):
        d.line([(x + 14, gy), (x + w - 14, gy)], fill=(225, 225, 225), width=1)
    pts = [(x + 20, y + 26), (x + 70, y + 34), (x + 110, y + 30), (x + 150, y + 52),
           (x + 190, y + 48), (x + 230, y + 72), (x + 270, y + 66), (x + 300, y + 96)]
    d.line(pts, fill=RED, width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    # big down arrow
    ax, ay = x + w - 58, y + 12
    d.polygon([(ax, ay), (ax + 34, ay), (ax + 34, ay + 26), (ax + 48, ay + 26),
               (ax + 17, ay + 62), (ax - 14, ay + 26), (ax, ay + 26)], fill=RED)
    d.rectangle([x + 14, y + h - 26, x + 118, y + h - 8], fill=INK)
    text(x + 66, y + h - 23, "NASDAQ  -4%", SANS_B(11), fill=WHITE, anchor="ma")

LEADS = [
    ("MIDDLE EAST", scene_refinery, "HOUTHIS CLAIM STRIKE ON SAUDI REFINERY",
     "4 drones downed over Ras Tanura; smoke seen, damage unconfirmed.",
     "CLAIMED", "Reuters / NASA"),
    ("UKRAINE WAR", scene_toll, "LEAKED DATA: 490,334 RUSSIAN SOLDIERS DEAD",
     "BBC analysis of leaked records; true toll may pass 700,000.",
     "REPORTED", "BBC Russian / Mediazona"),
    ("MARKETS", scene_market, "TRUMP TARIFFS SPOOK WALL STREET",
     "US proposes levies on 14 partners; Nasdaq fell ~4%, Nvidia -8.7%.",
     "CONFIRMED", "Reuters"),
]
ly = 204
lw = (CW - 20) // 3
lh = 100
for i, (kick, fn, head, deck, hs, src) in enumerate(LEADS):
    x0 = M + i * (lw + 10)
    fn(x0, ly, lw, lh)
    d.rectangle([x0, ly, x0 + lw, ly + lh], outline=INK, width=2)
    tag(x0 + 6, ly + 6, kick)
    hy = ly + lh + 6
    hl = wrap(head, SERIF_B(20), lw)
    hy = para(x0, hy, hl, SERIF_B(20), lh=23)
    hy = para(x0, hy + 2, wrap(deck, SANS(12), lw), SANS(12), fill=(60, 60, 60), lh=13)
    howsure(x0, hy + 4, hs)
    text(x0 + lw, hy + 4, src, SANS(9), fill=GREY, anchor="ra")
    lead_bottom = hy + 4 + 15
LEAD_BOTTOM = lead_bottom
rule(M, W - M, LEAD_BOTTOM + 6, 2)

# ---------------------------------------------------------------- mid grid
# 10 small drawn scenes, 2 rows x 5 cols. Each ~189 x 46.
def sc_fire(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 28, 26))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(60, 58, 54))
    for fx in [x + 14, x + 60, x + 110, x + 150]:
        d.polygon([(fx, y + h - 12), (fx + 12, y + 8), (fx + 24, y + h - 12)], fill=ORANGE)
        d.polygon([(fx + 6, y + h - 12), (fx + 12, y + 22), (fx + 18, y + h - 12)], fill=(250, 210, 60))
    d.ellipse([x + w - 34, y + 6, x + w - 10, y + 30], fill=(90, 86, 80))

def sc_rubble(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 140, 125))
    d.polygon([(x, y + h), (x + 40, y + 12), (x + 90, y + 30), (x + 130, y + 8),
               (x + w, y + 34), (x + w, y + h)], fill=(110, 100, 86))
    d.polygon([(x + 20, y + h), (x + 60, y + 26), (x + 100, y + h)], fill=(80, 72, 60))
    for rx, ry in [(x + 120, y + 20), (x + 150, y + 32), (x + 60, y + 40)]:
        d.rectangle([rx, ry, rx + 14, ry + 8], fill=(70, 64, 54))

def sc_drone(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 90, 120))
    d.ellipse([x + w // 2 - 16, y + h // 2 - 8, x + w // 2 + 16, y + h // 2 + 8], fill=INK)
    for dx in [x + 30, x + w - 30]:
        d.ellipse([dx - 16, y + 8, dx + 16, y + 16], fill=(200, 200, 200))
        d.line([(dx, y + 12), (x + w // 2 - 14 if dx < x + w // 2 else x + w // 2 + 14, y + h // 2)], fill=INK, width=3)
    d.ellipse([x + w // 2 - 3, y + h // 2 - 3, x + w // 2 + 3, y + h // 2 + 3], fill=RED)

def sc_plane(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 170, 210))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(30, 80, 140))
    d.polygon([(x + 40, y + 22), (x + 130, y + 22), (x + 150, y + 28), (x + 60, y + 32)], fill=WHITE)
    d.polygon([(x + 90, y + 14), (x + 110, y + 22), (x + 100, y + 24)], fill=WHITE)
    d.polygon([(x + 60, y + 30), (x + 70, y + 38), (x + 62, y + 40)], fill=WHITE)
    d.ellipse([x + 148, y + 24, x + 156, y + 32], fill=RED)

def sc_shirt(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 60, 60))
    d.polygon([(x + 70, y + 8), (x + 90, y + 8), (x + 96, y + 14), (x + 112, y + 10),
               (x + 128, y + 22), (x + 118, y + 34), (x + 108, y + 30), (x + 108, y + h - 6),
               (x + 80, y + h - 6), (x + 80, y + 30), (x + 70, y + 34), (x + 60, y + 22),
               (x + 76, y + 10), (x + 92, y + 14)], fill=WHITE)
    text(x + w // 2, y + h - 16, "36%", SANS_B(13), fill=WHITE, anchor="ma")

def sc_dove(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 225, 235))
    d.ellipse([x + 70, y + 14, x + 120, y + 34], fill=WHITE)
    d.polygon([(x + 118, y + 18), (x + 138, y + 10), (x + 128, y + 24)], fill=WHITE)
    d.polygon([(x + 74, y + 16), (x + 56, y + 6), (x + 66, y + 24)], fill=WHITE)
    d.ellipse([x + 112, y + 18, x + 116, y + 22], fill=INK)
    d.rectangle([x + w - 46, y + 6, x + w - 8, y + 26], fill=NAVY)
    text(x + w - 27, y + 9, "10", SANS_B(13), fill=WHITE, anchor="ma")
    text(x + w - 27, y + 28, "YRS", SANS_B(8), fill=NAVY, anchor="ma")

def sc_balloon(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 230))
    for bx in [x + 18, x + 62, x + 106, x + 150]:
        d.rectangle([bx, y + h - 16, bx + 22, y + h - 6], fill=(60, 60, 66))
    d.ellipse([x + 66, y + 4, x + 122, y + 34], fill=(200, 40, 50))
    d.line([(x + 94, y + 34), (x + 94, y + h - 16)], fill=(120, 40, 40), width=2)
    d.polygon([(x + 150, y + 10), (x + 170, y + 22), (x + 150, y + 30)], fill=(250, 200, 60))

def sc_tube(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 235, 220))
    d.ellipse([x + 30, y + 8, x + 78, y + 38], outline=RED, width=5)
    d.rectangle([x + 46, y + 20, x + 62, y + 26], fill=BLUE)
    d.rectangle([x + 100, y + 10, x + 168, y + 32], fill=(200, 30, 30))
    d.rectangle([x + 106, y + 32, x + 162, y + 38], fill=INK)
    d.ellipse([x + 116, y + 38, x + 126, y + 44], fill=INK)
    d.ellipse([x + 146, y + 38, x + 156, y + 44], fill=INK)

def sc_flagx(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 70, 90))
    d.rectangle([x + 60, y + 8, x + 130, y + h - 8], fill=WHITE)
    d.rectangle([x + 60, y + 8, x + 130, y + 20], fill=(200, 40, 40))
    d.ellipse([x + 88, y + 22, x + 102, y + 34], fill=RED)
    d.line([(x + 56, y + 4), (x + 134, y + h - 4)], fill=RED, width=6)
    d.line([(x + 134, y + 4), (x + 56, y + h - 4)], fill=RED, width=6)

def sc_train(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(180, 210, 190))
    d.rectangle([x + 20, y + 12, x + 168, y + 36], fill=(30, 90, 140))
    d.rectangle([x + 28, y + 18, x + 58, y + 28], fill=(180, 220, 240))
    d.rectangle([x + 66, y + 18, x + 96, y + 28], fill=(180, 220, 240))
    d.rectangle([x + 104, y + 18, x + 134, y + 28], fill=(180, 220, 240))
    d.rectangle([x + 142, y + 18, x + 160, y + 28], fill=(250, 210, 60))
    d.ellipse([x + 40, y + 36, x + 52, y + 44], fill=INK)
    d.ellipse([x + 140, y + 36, x + 152, y + 44], fill=INK)
    d.line([(x + 10, y + h - 4), (x + w - 10, y + h - 4)], fill=INK, width=2)

MIDS = [
    ("CAIRO", sc_fire, "TANKER FIRE KILLS 31 IN CAIRO",
     "25 hurt; cars charred on ring road.", "CONFIRMED"),
    ("GAZA", sc_rubble, "ISRAEL STRIKE KILLS HAMAS CHIEF",
     "Abu al-Ouf and family die.", "CONFIRMED"),
    ("SUDAN", sc_drone, "DRONE STRIKES HIT BLUE NILE",
     "At least 6 dead, 15 hurt.", "REPORTED"),
    ("MISSISSIPPI", sc_plane, "PLANE CRASH OFF US COAST KILLS SIX",
     "Two children among the dead.", "CONFIRMED"),
    ("BANGLADESH", sc_shirt, "GARMENT WAGE RISES 36%",
     "Minimum pay up for workers.", "CONFIRMED"),
    ("COLOMBIA", sc_dove, "TEN YEARS ON FROM PEACE DEAL",
     "UN hails progress; hostages freed.", "CONFIRMED"),
    ("N. AMERICA", sc_balloon, "THANKSGIVING TURNS 100, PARADE MOVES",
     "Storm grounds balloons; first postponement ever.", "CONFIRMED"),
    ("EUROPE", sc_tube, "LONDON TUBE STOPS AS DRIVERS WALK OUT",
     "No Piccadilly or Circle line all day.", "CONFIRMED"),
    ("EAST ASIA", sc_flagx, "PYONGYANG EXPELS THE SWISS",
     "N. Korea throws out top diplomat.", "CONFIRMED"),
    ("EAST ASIA", sc_train, "KOREA'S RAIL SLOWS AS KORAIL STAFF ACT",
     "Work-to-rule begins 09:00.", "CONFIRMED"),
]

my = LEAD_BOTTOM + 6 + 16
text(M, my, "MORE OF THE DAY", SANS_B(12), fill=RED)
my += 16
mw = (CW - 4 * 8) // 5
mh = 38
row_h = 38 + 4 + 13 + 2 * 14 + 2 + 10 + 4 + 15
for r in range(2):
    for c in range(5):
        i = r * 5 + c
        kick, fn, head, deck, hs = MIDS[i]
        x0 = M + c * (mw + 8)
        y0 = my + r * (row_h + 6)
        fn(x0, y0, mw, mh)
        d.rectangle([x0, y0, x0 + mw, y0 + mh], outline=INK, width=1)
        hy = y0 + mh + 4
        text(x0, hy, kick, SANS_B(9), fill=RED)
        hy += 13
        hy = para(x0, hy, wrap(head, SERIF_B(12), mw), SERIF_B(12), lh=14)
        hy = para(x0, hy + 1, wrap(deck, SANS(9), mw), SANS(9), fill=(60, 60, 60), lh=10)
        howsure(x0, hy + 3, hs)
MID_BOTTOM = my + 2 * row_h + 6

# ---------------------------------------------------------------- rest of the day
REST = [
    (14, "N. KOREA", "Swiss office shut in sanctions row", "REPORTED"),
    (15, "VENEZUELA", "Govt reveals $237.5bn public debt", "CONFIRMED"),
    (16, "INDIA", "Constitution Day; 18 yrs since 26/11", "CONFIRMED"),
    (17, "SPACE", "BepiColombo at Mercury (25 Nov)", "CONFIRMED"),
    (18, "PETROBRAS", "$122bn investment plan unveiled", "CONFIRMED"),
    (19, "OBITUARY", "Duran Duran guitarist Andy Taylor, 65", "CONFIRMED"),
    (20, "CRICKET", "Sooryavanshi, 15, hits 204 off 53", "CONFIRMED"),
    (21, "UK", "Moves jets over drone threat", "REPORTED"),
    (22, "MALAYSIA", "Sues Google for $146m", "CONFIRMED"),
    (23, "INDONESIA", "Mine flood kills 9", "CONFIRMED"),
    (24, "LUKOIL", "To sell foreign assets", "REPORTED"),
    (25, "US", "Markets shut for Thanksgiving", "CONFIRMED"),
    (26, "KOREA", "Court rules on Yoon perjury case", "CONFIRMED"),
    (27, "KOREA", "Court rules on massage licences", "CONFIRMED"),
    (28, "INDIA", "Fog in north, rain in south", "CONFIRMED"),
    (29, "AUSTRALIA", "Palm Beach ferries shut by strike", "CONFIRMED"),
    (30, "AUSTRALIA", "Small-business complaints jump 21%", "CONFIRMED"),
    (31, "NZ", "M4.8 quake off Hicks Bay", "CONFIRMED"),
    (32, "UKRAINE", "US shelves Russia business pitch", "REPORTED"),
    (33, "CHINA", "Xi's probe shakes Shanghai", "REPORTED"),
    (34, "US", "Confidence at a 2-year high", "CONFIRMED"),
    (35, "VENEZUELA", "Caracas owes $237.5bn", "CONFIRMED"),
    (36, "COLOMBIA", "A decade of peace, Bogota", "CONFIRMED"),
    (37, "VIETNAM", "Advances sustainable agriculture", "REPORTED"),
    (38, "US", "Tightens remote AI-chip access rules", "CONFIRMED"),
]
ry = MID_BOTTOM + 8
rule(M, W - M, ry, 2)
ry += 7
text(M, ry, "THE REST OF THE DAY \u2014 25 MORE STORIES", SANS_B(12), fill=RED)
ry += 16
colw = (CW - 20) // 3
lh_rest = 13
f_rest = SANS(9)
f_rest_b = SANS_B(9)
f_lab = SANS_B(8)
lab_col = {"CONFIRMED": GREEN, "REPORTED": (176, 120, 0)}
per_col = 9
for ci in range(3):
    x0 = M + ci * (colw + 10)
    for j in range(per_col):
        idx = ci * per_col + j
        if idx >= len(REST):
            break
        num, place, head, lab = REST[idx]
        y0 = ry + j * lh_rest
        pre = f"{num}. {place} \u2014 {head} \u00b7 "
        d.text((x0, y0), pre, font=f_rest, fill=INK)
        lx = x0 + d.textlength(pre, font=f_rest)
        d.text((lx, y0), lab, font=f_lab, fill=lab_col[lab])
REST_BOTTOM = ry + per_col * lh_rest

# ---------------------------------------------------------------- map
my2 = REST_BOTTOM + 6
rule(M, W - M, my2, 2)
my2 += 7
text(M, my2, "WHERE IT HAPPENED \u2014 17 PLACES ON THE MAP", SANS_B(12), fill=RED)
my2 += 16
map_h = 48
mx0, my0 = M, my2
d.rectangle([mx0, my0, mx0 + CW, my0 + map_h], fill=(200, 220, 235))
# schematic continents (flat, approximate)
LAND = (222, 214, 182)
# North America
d.polygon([(mx0 + 8, my0 + 9), (mx0 + 150, my0 + 5), (mx0 + 190, my0 + 14),
           (mx0 + 170, my0 + 26), (mx0 + 90, my0 + 30), (mx0 + 30, my0 + 23)], fill=LAND)
# South America
d.polygon([(mx0 + 210, my0 + 26), (mx0 + 260, my0 + 24), (mx0 + 270, my0 + 38),
           (mx0 + 240, my0 + 46), (mx0 + 215, my0 + 36)], fill=LAND)
# Europe
d.polygon([(mx0 + 430, my0 + 6), (mx0 + 500, my0 + 5), (mx0 + 520, my0 + 14),
           (mx0 + 490, my0 + 21), (mx0 + 445, my0 + 18)], fill=LAND)
# Africa
d.polygon([(mx0 + 440, my0 + 23), (mx0 + 520, my0 + 21), (mx0 + 545, my0 + 33),
           (mx0 + 510, my0 + 45), (mx0 + 465, my0 + 42), (mx0 + 445, my0 + 32)], fill=LAND)
# Asia
d.polygon([(mx0 + 530, my0 + 5), (mx0 + 780, my0 + 3), (mx0 + 830, my0 + 12),
           (mx0 + 800, my0 + 26), (mx0 + 700, my0 + 30), (mx0 + 600, my0 + 27),
           (mx0 + 545, my0 + 18)], fill=LAND)
# Australia
d.polygon([(mx0 + 800, my0 + 33), (mx0 + 880, my0 + 32), (mx0 + 900, my0 + 39),
           (mx0 + 860, my0 + 45), (mx0 + 815, my0 + 42)], fill=LAND)
PLACES = [
    (1, "CAIRO", 500, 26), (2, "HORMUZ", 585, 23), (3, "RAS TANURA", 575, 30),
    (4, "RIYADH", 560, 29), (5, "GAZA", 520, 23), (6, "MOSCOW", 500, 9),
    (7, "LONDON", 448, 11), (8, "PYONGYANG", 770, 15), (9, "SEOUL", 745, 18),
    (10, "TAIPEI", 730, 24), (11, "MUMBAI", 640, 26), (12, "LABUAN", 700, 30),
    (13, "NEW YORK", 130, 15), (14, "CARTAGENA", 215, 30), (15, "BRASILIA", 245, 36),
    (16, "CARACAS", 225, 26), (17, "SYDNEY", 860, 39),
]
for num, name, px, py in PLACES:
    cx, cy = mx0 + px, my0 + py
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=WHITE, width=1)
    d.text((cx, cy - 5), str(num), font=SANS_B(8), fill=WHITE, anchor="ma")
legend = "  ".join(f"{n} {nm}" for n, nm, _, _ in PLACES)
ly2 = my0 + map_h + 3
leg_lines = wrap(legend, SANS(9), CW)
ly2 = para(M, ly2, leg_lines, SANS(9), fill=GREY, lh=11)
MAP_BOTTOM = ly2

# ---------------------------------------------------------------- date check + sources
dc1 = ("All 38 stories first reported Thu 26 Nov 2026, in some time zone. "
       "LEFT OUT: Shenzhou-24 docking, Solomons treaty (25 Nov), Riyadh tower strike (24 Nov).")
dc2 = ("Houthi strike CLAIMED; Riyadh confirms 4 drones downed only \u2014 damage unconfirmed. "
       "Hormuz mine reports UNVERIFIED. Russian toll: BBC/Mediazona leak; Kremlin disputes.")
dc_lines = wrap(dc1, SANS(9), CW - 16) + wrap(dc2, SANS(9), CW - 16)
box_h = 16 + len(dc_lines) * 11 + 6
dy = MAP_BOTTOM + 5
d.rectangle([M, dy, W - M, dy + box_h], outline=RED, width=2)
text(M + 8, dy + 4, "DATE CHECK", SANS_B(10), fill=RED)
para(M + 8, dy + 16, dc_lines, SANS(9), lh=11)
sy = dy + box_h + 5
text(W // 2, sy, "Sources: Reuters \u00b7 BBC Russian \u00b7 AP \u00b7 Xinhua \u00b7 Yonhap \u00b7 EMSC \u00b7 USGS \u00b7 Mediazona \u2014 Hand-drawn; no photographs. \u00b7 make.fun/news-image-20261126",
     SANS(9), fill=GREY, anchor="ma")

img.save(os.path.join(HERE, "entry.png"), optimize=True)
print("saved", os.path.join(HERE, "entry.png"),
      os.path.getsize(os.path.join(HERE, "entry.png")), "bytes")
