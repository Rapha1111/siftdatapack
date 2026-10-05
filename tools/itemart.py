"""Pixel-art procédural : icônes d'objets (16x16), âme errante, icône du pack, fond d'advancements."""
import math
import os

import numpy as np
from PIL import Image, ImageDraw

from modelkit import hex_rgb, mix, shade


def outline(img, col=(20, 10, 40)):
    src = img.copy()
    p, s = img.load(), src.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if s[x, y][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < w and 0 <= yy < h and s[xx, yy][3] > 0:
                        p[x, y] = col + (255,)
                        break
    return img


def px(d, pts, c):
    for x, y in pts:
        d.point((x, y), fill=hex_rgb(c) + (255,))


def grad(c1, c2, t):
    return mix(hex_rgb(c1), hex_rgb(c2), max(0.0, min(1.0, t)))


def fork():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # deux dents + base en U
    for y in range(1, 9):
        t = y / 8
        for x in (4, 11):
            d.point((x, y), fill=grad("#7ff3ff", "#2a9aa6", t) + (255,))
            d.point((x + (1 if x == 4 else -1), y), fill=grad("#d8fdff", "#52d4e0", t) + (255,))
    for x, y in ((5, 9), (6, 10), (7, 10), (8, 10), (9, 10), (10, 9)):
        d.point((x, y), fill=hex_rgb("#3cc4d2") + (255,))
    px(d, [(7, 9), (8, 9), (6, 9), (9, 9)], "#9ff8ff")
    for y in range(11, 15):
        d.point((7, y), fill=hex_rgb("#c18a4a") + (255,))
        d.point((8, y), fill=hex_rgb("#8a5a2e") + (255,))
    px(d, [(6, 14), (7, 14), (8, 14), (9, 14)], "#ffd36b")
    px(d, [(7, 15), (8, 15)], "#e8a53a")
    px(d, [(4, 1), (11, 1)], "#ffffff")
    px(d, [(3, 0), (12, 0), (2, 2), (13, 2)], "#ff9eff")  # étincelles de chant
    return outline(img)


def chime():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    px(d, [(5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1)], "#8a5a2e")
    px(d, [(5, 2), (10, 2)], "#c18a4a")
    # tubes
    for x, ln, col in ((4, 7, "#7ff3ff"), (7, 10, "#bff6ff"), (10, 8, "#ff9eff"), (13, 5, "#ffe08a")):
        for y in range(3, 3 + ln):
            d.point((x, y), fill=shade(hex_rgb(col), 1.0 - 0.25 * ((y - 3) / ln)) + (255,))
            d.point((x + 1, y), fill=shade(hex_rgb(col), 0.7) + (255,))
        d.point((x, 3 + ln), fill=hex_rgb("#ffffff") + (255,))
    px(d, [(5, 3), (8, 3), (11, 3), (14, 3)], "#8a5a2e")
    # battant
    px(d, [(7, 13), (8, 13), (7, 14), (8, 14)], "#ffd36b")
    return outline(img)


def vial():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # bouchon + col
    px(d, [(7, 1), (8, 1), (7, 2), (8, 2)], "#a0703a")
    px(d, [(6, 3), (7, 3), (8, 3), (9, 3)], "#d8f4ff")
    px(d, [(6, 4), (9, 4)], "#d8f4ff")
    # fiole : liquide en dégradé iridescent
    rows = [(5, 4, 11), (6, 3, 12), (7, 2, 13), (8, 2, 13), (9, 2, 13), (10, 2, 13), (11, 3, 12), (12, 4, 11), (13, 5, 10)]
    for y, x1, x2 in rows:
        for x in range(x1, x2 + 1):
            t = ((x - x1) / max(1, x2 - x1)) * 0.6 + (y - 5) / 16
            c = grad("#d24dff", "#3cf2d0", math.sin(t * 5) * 0.5 + 0.5)
            if y < 7:
                c = (216, 244, 255) if (x in (x1, x2)) else (150, 120, 200)
            d.point((x, y), fill=c + (255,))
    px(d, [(4, 8), (4, 9)], "#ffffff")
    px(d, [(10, 9), (11, 10)], "#ffe08a")
    return outline(img)


def soul_essence():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = 7.5, 8.5
    for y in range(16):
        for x in range(16):
            dx, dy = (x - cx), (y - cy) * 0.8
            r = math.hypot(dx, dy)
            # forme de goutte/flamme qui s'effile vers le haut
            width = 5.2 - max(0, (cy - y)) * 0.55
            if y > 2 and abs(dx) < width and r < 6.4:
                t = r / 6.4
                c = grad("#ffffff", "#2ad0e8", t ** 1.2)
                d.point((x, y), fill=c + (255,))
    px(d, [(7, 1), (8, 1), (7, 2), (8, 2)], "#9ff8ff")
    px(d, [(5, 6), (6, 5)], "#ffffff")
    return outline(img, (10, 40, 70))


def ichor_shard():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = [(8, 1), (11, 5), (12, 11), (8, 15), (4, 11), (5, 5)]
    d.polygon(pts, fill=(255, 255, 255, 255))
    p = img.load()
    for y in range(16):
        for x in range(16):
            if p[x, y][3]:
                t = (x + y) / 28.0
                c = grad("#ff4fd8", "#3cf2d0", t + 0.15 * math.sin(y))
                if x > 8:
                    c = shade(c, 0.8)
                p[x, y] = c + (255,)
    px(d, [(8, 3), (8, 4), (7, 6), (7, 7)], "#ffffff")
    return outline(img)


def wisp():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    p = img.load()
    for y in range(16):
        for x in range(16):
            dx, dy = abs(x - 7.5), abs(y - 7.5)
            r = dx + dy  # losange
            if r <= 6.2:
                t = r / 6.2
                c = grad("#ffffff", "#27d4ff", t ** 1.4)
                p[x, y] = c + (255,)
    for (x, y) in ((7, 0), (8, 0), (7, 15), (8, 15), (0, 7), (0, 8), (15, 7), (15, 8)):
        p[x, y] = hex_rgb("#bff6ff") + (255,)
    return img


def save_items(rp_assets):
    tdir = os.path.join(rp_assets, "sift", "textures", "item")
    os.makedirs(tdir, exist_ok=True)
    for name, f in (("fork", fork), ("chime", chime), ("vial", vial), ("soul_essence", soul_essence), ("ichor_shard", ichor_shard), ("wisp", wisp)):
        f().save(os.path.join(tdir, name + ".png"))


def pack_icon(path):
    """Paysage du Sift : ciel dégradé, lune géante, crêtes rouges, arbres bleus, bassin d'ichor."""
    w = h = 128
    rng = np.random.RandomState(5)
    img = Image.new("RGB", (w, h))
    p = img.load()
    for y in range(h):
        t = y / h
        c = mix(hex_rgb("#2a1458"), hex_rgb("#ff8ac0"), min(1, t * 1.3))
        c = mix(c, hex_rgb("#6fe8ff"), max(0, t - 0.55) * 1.6)
        for x in range(w):
            p[x, y] = c
    d = ImageDraw.Draw(img)
    for _ in range(70):
        x, y = rng.randint(0, w), rng.randint(0, 70)
        d.point((x, y), fill=(255, 255, 255))
    d.ellipse((74, 12, 112, 50), fill=(255, 238, 214))
    d.ellipse((82, 20, 92, 30), fill=(236, 214, 190))
    d.ellipse((98, 32, 106, 40), fill=(236, 214, 190))
    # crêtes
    pts = [(0, 90), (18, 70), (30, 80), (48, 58), (64, 82), (80, 66), (100, 84), (128, 72), (128, 128), (0, 128)]
    d.polygon(pts, fill=(176, 58, 44))
    for y in range(72, 128, 4):
        d.line([(0, y), (128, y)], fill=(200, 96, 52) if (y // 4) % 2 else (150, 40, 38))
    d.polygon([(0, 104), (40, 96), (80, 108), (128, 98), (128, 128), (0, 128)], fill=(214, 120, 60))
    # bassin d'ichor
    d.ellipse((20, 106, 100, 124), fill=(210, 77, 255))
    d.ellipse((34, 110, 80, 120), fill=(60, 242, 208))
    # arbres bleus
    for tx, ty, s in ((16, 100, 1.0), (104, 98, 1.2), (60, 96, 0.8)):
        d.rectangle((tx - 1, ty - int(14 * s), tx + 1, ty), fill=(30, 140, 150))
        d.ellipse((tx - int(9 * s), ty - int(26 * s), tx + int(9 * s), ty - int(10 * s)), fill=(143, 216, 255))
        d.ellipse((tx - int(4 * s), ty - int(22 * s), tx + int(2 * s), ty - int(16 * s)), fill=(210, 245, 255))
    # âmes
    for _ in range(18):
        x, y = rng.randint(0, w), rng.randint(60, 120)
        d.rectangle((x, y, x + 1, y + 1), fill=(190, 250, 255))
    img.save(path)


def advancement_bg(path):
    """Fond d'onglet d'advancements : sculk pourpre sombre étoilé de lueurs cyan."""
    s = 256
    rng = np.random.RandomState(3)
    arr = np.zeros((s, s, 3), dtype=np.uint8)
    base = np.array(hex_rgb("#1a0f33"))
    for y in range(s):
        for x in range(s):
            n = rng.rand()
            arr[y, x] = (base * (0.8 + 0.4 * n)).clip(0, 255)
    img = Image.fromarray(arr)
    d = ImageDraw.Draw(img)
    for _ in range(260):
        x, y = rng.randint(0, s), rng.randint(0, s)
        c = [(111, 240, 255), (255, 158, 255), (255, 224, 138)][rng.randint(0, 3)]
        d.point((x, y), fill=c)
        if rng.rand() < 0.2:
            d.point((x + 1, y), fill=shade(c, 0.5))
            d.point((x, y + 1), fill=shade(c, 0.5))
    img.save(path)
