"""Mini-kit de modélisation : boîtes colorées -> modèle d'item JSON + atlas de texture PNG (+ aperçu 3D).

Chaque mob/objet 3D est décrit par une liste de `Part` (pavés). Les faces sont peintes procéduralement
(dégradé, bruit, bordures, motifs, décalques) puis empaquetées dans un atlas. Les UV sont générés automatiquement.
Convention : 16 unités = 1 bloc ; l'avant du modèle est la face SUD (+z), x croît vers l'est.
"""
import hashlib
import math
import os

from PIL import Image, ImageDraw

FACES = ("north", "east", "south", "west", "up", "down")


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3))


def shade(c, f):
    return tuple(max(0, min(255, int(round(v * f)))) for v in c)


def _h(*vals):
    return int(hashlib.md5("|".join(map(str, vals)).encode()).hexdigest()[:8], 16)


class Part:
    """Un pavé [frm, to] de couleur `color`.

    rot : (axe, angle, origine) pour la rotation d'élément (angle multiple de 22.5, |angle| <= 45)
    pattern : 'veins' | 'spots' | 'bands' | 'scales' | 'plates' | None
    accent : couleur d'accent du motif
    decals : {face: [(x, y, w, h, '#hex'), ...]} en pixels de la face (vue de l'extérieur, origine haut-gauche)
    glow : le pavé est dessiné plus clair, sans ombrage de face
    """

    def __init__(self, name, frm, to, color, rot=None, pattern=None, accent=None, decals=None, glow=False,
                 noise=0.07, bands=None, hidden_faces=()):
        self.name, self.frm, self.to = name, tuple(map(float, frm)), tuple(map(float, to))
        self.color, self.rot, self.pattern = hex_rgb(color), rot, pattern
        self.accent = hex_rgb(accent) if accent else None
        self.decals = decals or {}
        self.glow, self.noise = glow, noise
        self.bands = [hex_rgb(b) for b in bands] if bands else None
        self.hidden = hidden_faces

    def size(self):
        return tuple(self.to[i] - self.frm[i] for i in range(3))

    def face_dims(self, face):
        dx, dy, dz = self.size()
        if face in ("north", "south"):
            return dx, dy
        if face in ("east", "west"):
            return dz, dy
        return dx, dz


def mirror(part, name=None, cx=8.0):
    """Copie miroir (par rapport à x = cx) — utile pour les membres gauche/droit."""
    f, t = part.frm, part.to
    p = Part(name or part.name + "_m", (2 * cx - t[0], f[1], f[2]), (2 * cx - f[0], t[1], t[2]), "#000000")
    p.color, p.pattern, p.accent, p.glow, p.noise, p.bands = part.color, part.pattern, part.accent, part.glow, part.noise, part.bands
    p.decals = {}
    for face, ops in part.decals.items():
        mf = {"east": "west", "west": "east"}.get(face, face)
        w = part.face_dims(face)[0]
        p.decals[mf] = [(max(0, round(w) - x - dw), y, dw, dh, c) for (x, y, dw, dh, c) in ops] if face in ("north", "south", "up", "down") else ops
    if part.rot:
        axis, ang, org = part.rot
        p.rot = (axis, -ang if axis in ("z", "y") else ang, (2 * cx - org[0], org[1], org[2]))
    return p


def paint_face(part, face, w, h, seed):
    """Retourne une image RGBA w x h pour une face du pavé."""
    w, h = max(1, int(round(w))), max(1, int(round(h)))
    img = Image.new("RGBA", (w, h))
    px = img.load()
    base = part.color
    top = {"up": 1.12, "down": 0.68, "north": 0.88, "south": 1.0, "east": 0.82, "west": 0.92}[face]
    if part.glow:
        top = 1.0
    for y in range(h):
        for x in range(w):
            c = shade(base, top * (1.06 - 0.12 * (y / max(1, h - 1))))
            n = (_h(seed, face, x, y) % 1000) / 1000.0 - 0.5
            c = shade(c, 1 + n * 2 * part.noise)
            if part.pattern and part.accent:
                a = part.accent
                if part.pattern == "veins":
                    v = _h(seed, "vein", (x + 2 * (y // 3)) // 2, y // 4) % 100
                    if (x * 3 + y * 2 + _h(seed, face) % 7) % 9 in (0, 1) and v < 62:
                        c = mix(c, a, 0.85)
                elif part.pattern == "spots":
                    if _h(seed, face, x // 2, y // 2) % 100 < 14:
                        c = mix(c, a, 0.8)
                elif part.pattern == "bands":
                    if (y // 2) % 3 == 0:
                        c = mix(c, a, 0.55)
                elif part.pattern == "scales":
                    if (x + (y % 2) * 1) % 3 == 0 or y % 3 == 0:
                        c = shade(c, 0.82)
                    elif (x + y) % 5 == 0:
                        c = mix(c, a, 0.5)
                elif part.pattern == "plates":
                    if x % 4 == 0 or y % 4 == 0:
                        c = mix(c, a, 0.6)
            if part.bands:
                c = mix(c, part.bands[(y // 2) % len(part.bands)], 0.55)
            # liseré sombre sur les bords de la face
            if not part.glow and (x == 0 or y == 0 or x == w - 1 or y == h - 1) and w > 2 and h > 2:
                c = shade(c, 0.88)
            px[x, y] = c + (255,)
    for (dx, dy, dw, dh, col) in part.decals.get(face, []):
        cc = hex_rgb(col) if col != "clear" else None
        for yy in range(int(dy), int(dy + dh)):
            for xx in range(int(dx), int(dx + dw)):
                if 0 <= xx < w and 0 <= yy < h:
                    px[xx, yy] = (cc + (255,)) if cc else (0, 0, 0, 0)
    return img


class Model:
    def __init__(self, name, parts, tex=None):
        self.name, self.parts = name, parts
        self.tex = tex or f"sift:item/mob/{name}"
        self.atlas = None

    def build(self):
        # empaquetage "étagères" dans un atlas carré
        tiles = []
        for pi, p in enumerate(self.parts):
            for f in FACES:
                if f in p.hidden:
                    continue
                w, h = p.face_dims(f)
                tiles.append((pi, f, max(1, int(round(w))), max(1, int(round(h)))))
        tiles.sort(key=lambda t: -t[3])
        size = 32
        while True:
            x = y = row_h = 0
            placed, ok = {}, True
            for pi, f, w, h in tiles:
                if x + w + 2 > size:
                    x, y, row_h = 0, y + row_h + 2, 0
                if y + h + 2 > size:
                    ok = False
                    break
                placed[(pi, f)] = (x + 1, y + 1, w, h)
                x += w + 2
                row_h = max(row_h, h)
            if ok:
                break
            size *= 2
        atlas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        for (pi, f), (x, y, w, h) in placed.items():
            tile = paint_face(self.parts[pi], f, w, h, f"{self.name}{pi}")
            atlas.paste(tile, (x, y))
            # extrusion d'un pixel autour de la tuile (évite les franges aux bords avec le mipmapping)
            atlas.paste(tile.crop((0, 0, w, 1)), (x, y - 1))
            atlas.paste(tile.crop((0, h - 1, w, h)), (x, y + h))
            atlas.paste(tile.crop((0, 0, 1, h)), (x - 1, y))
            atlas.paste(tile.crop((w - 1, 0, w, h)), (x + w, y))
        self.atlas, self.placed, self.size = atlas, placed, size
        elements = []
        for pi, p in enumerate(self.parts):
            faces = {}
            for f in FACES:
                if f in p.hidden:
                    continue
                x, y, w, h = placed[(pi, f)]
                k = 16.0 / self.size  # les UV vanilla sont toujours exprimés dans un repère 0..16
                faces[f] = {"uv": [round(x * k, 4), round(y * k, 4), round((x + w) * k, 4), round((y + h) * k, 4)], "texture": "#0"}
            el = {"name": p.name, "from": list(p.frm), "to": list(p.to), "faces": faces}
            if p.rot:
                axis, ang, org = p.rot
                el["rotation"] = {"angle": ang, "axis": axis, "origin": list(org)}
            if p.glow:
                el["light_emission"] = 15
            elements.append(el)
        return {"textures": {"0": self.tex, "particle": self.tex}, "elements": elements}

    def save(self, rp_assets):
        data = self.build()
        mdir = os.path.join(rp_assets, "sift", "models", "item", "mob")
        tdir = os.path.join(rp_assets, "sift", "textures", "item", "mob")
        idir = os.path.join(rp_assets, "sift", "items", "mob")
        for d in (mdir, tdir, idir):
            os.makedirs(d, exist_ok=True)
        import json
        with open(os.path.join(mdir, self.name + ".json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, indent=1)
            f.write("\n")
        self.atlas.save(os.path.join(tdir, self.name + ".png"))
        with open(os.path.join(idir, self.name + ".json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump({"model": {"type": "minecraft:model", "model": f"sift:item/mob/{self.name}"}}, f, indent=1)
            f.write("\n")

    # ------------------------------------------------------------ aperçu rapide (non texturé finement)
    def preview(self, path, yaw=35, pitch=22, scale=14, size=360):
        if self.atlas is None:
            self.build()
        img = Image.new("RGB", (size, size), (28, 22, 44))
        d = ImageDraw.Draw(img)
        cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

        def rotp(pt, rot):
            x, y, z = pt
            if rot:
                axis, ang, org = rot
                a = math.radians(ang)
                ox, oy, oz = org
                x, y, z = x - ox, y - oy, z - oz
                if axis == "z":
                    x, y = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
                elif axis == "x":
                    y, z = y * math.cos(a) - z * math.sin(a), y * math.sin(a) + z * math.cos(a)
                else:
                    x, z = x * math.cos(a) + z * math.sin(a), -x * math.sin(a) + z * math.cos(a)
                x, y, z = x + ox, y + oy, z + oz
            return x - 8, y, z - 8

        def proj(pt):
            x, y, z = pt
            x2 = x * cy - z * sy
            z2 = x * sy + z * cy
            y2 = y * cp - z2 * sp
            z3 = y * sp + z2 * cp
            return (size / 2 + x2 * scale, size * 0.82 - y2 * scale), z3

        polys = []
        for pi, p in enumerate(self.parts):
            (x1, y1, z1), (x2, y2, z2) = p.frm, p.to
            corners = {
                "north": [(x2, y2, z1), (x1, y2, z1), (x1, y1, z1), (x2, y1, z1)],
                "south": [(x1, y2, z2), (x2, y2, z2), (x2, y1, z2), (x1, y1, z2)],
                "east": [(x2, y2, z2), (x2, y2, z1), (x2, y1, z1), (x2, y1, z2)],
                "west": [(x1, y2, z1), (x1, y2, z2), (x1, y1, z2), (x1, y1, z1)],
                "up": [(x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2)],
                "down": [(x1, y1, z2), (x2, y1, z2), (x2, y1, z1), (x1, y1, z1)],
            }
            for f, pts in corners.items():
                if f in p.hidden:
                    continue
                pts = [rotp(q, p.rot) for q in pts]
                pr = [proj(q) for q in pts]
                depth = sum(z for _, z in pr) / 4
                x, y, w, h = self.placed[(pi, f)]
                tile = self.atlas.crop((x, y, x + w, y + h)).convert("RGB").resize((1, 1), Image.BOX).getpixel((0, 0))
                polys.append((depth, [pt for pt, _ in pr], tile, f))
        polys.sort(key=lambda t: -t[0])
        for depth, pts, col, f in polys:
            d.polygon(pts, fill=col, outline=shade(col, 0.6))
        img.save(path)
