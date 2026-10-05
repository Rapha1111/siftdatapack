"""Modèles 3D (pavés) des créatures du Sift. Avant du modèle = face sud (+z). 16 unités = 1 bloc."""
from modelkit import Model, Part, mirror

P = Part


def eyes(face_w, y, gap, col, size=(1, 2), hi="#ffffff"):
    """Deux yeux symétriques sur une face de largeur face_w."""
    cx = face_w / 2.0
    ex = int(round(cx - gap / 2.0 - size[0]))
    ex2 = int(round(cx + gap / 2.0))
    ops = []
    for x in (ex, ex2):
        ops.append((x, y, size[0], size[1], col))
        ops.append((x, y, 1, 1, hi))
    return ops


# ----------------------------------------------------------------------------------------- Blub
def blub():
    c, belly, ear_in = "#8fd8ff", "#dff6ff", "#ff9ec8"
    parts = [
        P("body", (5, 2.5, 3), (11, 8.5, 11), c),
        P("belly", (5.4, 2.2, 3.6), (10.6, 5.2, 10.6), belly),
        P("head", (4.5, 6, 9), (11.5, 12, 14.5), c,
          decals={"south": eyes(7, 2, 3, "#10202e", (1, 2)) + [(3, 4, 1, 1, "#ff7fb0"), (0, 4, 1, 1, "#ffc2dc"), (6, 4, 1, 1, "#ffc2dc")]}),
        P("ear_l", (5.2, 12, 10), (7, 18.5, 11.6), c, rot=("z", 22.5, (6.1, 12, 10.8))),
        P("ear_in_l", (5.7, 12.4, 11.55), (6.9, 17.6, 11.75), ear_in, rot=("z", 22.5, (6.1, 12, 10.8))),
        P("ear_r", (9, 12, 10), (10.8, 18.5, 11.6), c, rot=("z", -22.5, (9.9, 12, 10.8))),
        P("ear_in_r", (9.1, 12.4, 11.55), (10.3, 17.6, 11.75), ear_in, rot=("z", -22.5, (9.9, 12, 10.8))),
        P("paw_l", (5.4, 0.5, 10), (7.4, 3.2, 12), belly),
        P("paw_r", (8.6, 0.5, 10), (10.6, 3.2, 12), belly),
        P("foot_l", (4.4, 0.5, 3), (7, 3, 8), c),
        P("foot_r", (9, 0.5, 3), (11.6, 3, 8), c),
        P("tail", (6.8, 4, 1.2), (9.2, 7, 3.4), "#ffffff", pattern="spots", accent="#d8f4ff"),
        # l'ampoule lumineuse (« blub ») sur la tête
        P("bulb_stem", (7.4, 12, 11), (8.6, 13.3, 12.2), "#5fb5dd"),
        P("bulb", (6.6, 13.2, 10.4), (9.4, 15.8, 13), "#c9fbff", glow=True, noise=0.03),
    ]
    return Model("blub", parts)


# --------------------------------------------------------------------------------------- Singer
def singer():
    teal, teal2, dark, pale, glow = "#1e7a85", "#25919b", "#17535e", "#bff6ff", "#6ff0ff"
    parts = [
        P("leg_l", (4.5, 0, 6), (7.5, 8, 10), teal, pattern="bands", accent=dark),
        P("leg_r", (8.5, 0, 6), (11.5, 8, 10), teal, pattern="bands", accent=dark),
        P("foot_l", (4, 0, 5.5), (8, 1.6, 11), dark),
        P("foot_r", (8, 0, 5.5), (12, 1.6, 11), dark),
        P("torso", (3.5, 8, 5), (12.5, 18, 11), teal, pattern="veins", accent=glow),
        P("chest_glow", (5, 10, 10.9), (11, 16, 11.12), glow, glow=True),
        P("rib1", (4.6, 15, 11), (11.4, 15.9, 11.3), dark),
        P("rib2", (4.6, 12.9, 11), (11.4, 13.8, 11.3), dark),
        P("rib3", (4.6, 10.8, 11), (11.4, 11.7, 11.3), dark),
        P("pad_l", (1.5, 16, 4.6), (4.6, 19.2, 11.4), dark, pattern="plates", accent=teal),
        P("pad_r", (11.4, 16, 4.6), (14.5, 19.2, 11.4), dark, pattern="plates", accent=teal),
        P("arm_l", (0.2, 6, 6), (3.2, 17, 10), teal, pattern="veins", accent=glow),
        P("arm_r", (12.8, 6, 6), (15.8, 17, 10), teal, pattern="veins", accent=glow),
        P("hand_l", (-0.4, 3.8, 5.5), (3.6, 6.8, 10.5), dark),
        P("hand_r", (12.4, 3.8, 5.5), (16.4, 6.8, 10.5), dark),
        P("head", (4, 18, 4.5), (12, 25, 11.5), teal2,
          decals={"south": [(2, 4, 4, 2, "#06242a"), (3, 4, 2, 1, "#6ff0ff"), (1, 1, 2, 1, "#0b3a42"), (5, 1, 2, 1, "#0b3a42")]}),
        P("plate_l", (2.2, 19, 6), (4, 24.5, 10), pale, glow=True, noise=0.04),
        P("plate_r", (12, 19, 6), (13.8, 24.5, 10), pale, glow=True, noise=0.04),
        P("vine1", (4.6, 12, 3.6), (5.6, 23, 4.6), pale, glow=True, noise=0.03),
        P("vine2", (6.4, 10, 3.6), (7.4, 22, 4.6), pale, glow=True, noise=0.03),
        P("vine3", (8.6, 10, 3.6), (9.6, 22, 4.6), pale, glow=True, noise=0.03),
        P("vine4", (10.4, 12, 3.6), (11.4, 23, 4.6), pale, glow=True, noise=0.03),
        P("crest1", (7.4, 25, 6), (8.6, 29.5, 7.4), glow, rot=("x", 22.5, (8, 25, 6.7)), glow=True),
        P("crest2", (5.4, 25, 6.4), (6.6, 28.2, 7.8), glow, rot=("z", 22.5, (6, 25, 7)), glow=True),
        P("crest3", (9.4, 25, 6.4), (10.6, 28.2, 7.8), glow, rot=("z", -22.5, (10, 25, 7)), glow=True),
    ]
    return Model("singer", parts)


# --------------------------------------------------------------------------------- Echo Golem
def echo_golem():
    stone, stone2, dark, cyan = "#b0502f", "#c2623a", "#7a2c1e", "#6ff0ff"
    bands = ["#b0502f", "#9a4126", "#c9703f"]
    parts = [
        P("leg_l", (4, 0, 5.5), (7.6, 6.5, 10.5), "#8a3b2a", bands=bands),
        P("leg_r", (8.4, 0, 5.5), (12, 6.5, 10.5), "#8a3b2a", bands=bands),
        P("torso", (3, 6.5, 4.5), (13, 16.5, 11.5), stone, bands=bands),
        P("core_frame", (5.5, 8.6, 11.35), (10.5, 13.8, 11.7), dark),
        P("core", (6.2, 9.3, 11.6), (9.8, 13.1, 11.9), cyan, glow=True, decals={"south": [(1, 1, 1, 1, "#ffffff"), (2, 2, 1, 1, "#aef9ff")]}),
        P("rune_l", (3.4, 11, 11.5), (5, 11.8, 11.7), cyan, glow=True),
        P("rune_r", (11, 11, 11.5), (12.6, 11.8, 11.7), cyan, glow=True),
        P("pad_l", (1.4, 14.5, 4.2), (4.4, 17.5, 11.8), stone2, bands=bands),
        P("pad_r", (11.6, 14.5, 4.2), (14.6, 17.5, 11.8), stone2, bands=bands),
        P("arm_l", (0, 5.5, 5.6), (3, 15, 10.4), stone, bands=bands),
        P("arm_r", (13, 5.5, 5.6), (16, 15, 10.4), stone, bands=bands),
        P("fist_l", (-0.6, 2.8, 5), (3.6, 6, 11), dark),
        P("fist_r", (12.4, 2.8, 5), (16.6, 6, 11), dark),
        P("head", (5, 16.5, 5.5), (11, 22.5, 11.5), stone2,
          decals={"south": [(1, 2, 4, 1, "#2a0c06"), (1, 3, 4, 1, cyan), (2, 3, 2, 1, "#ffffff")]}),
        P("brow", (4.8, 19.4, 11.3), (11.2, 20.4, 11.8), dark),
        P("horn_l", (5, 22.5, 6.5), (6.4, 25, 8), cyan, glow=True, rot=("z", 22.5, (5.7, 22.5, 7))),
        P("horn_r", (9.6, 22.5, 6.5), (11, 25, 8), cyan, glow=True, rot=("z", -22.5, (10.3, 22.5, 7))),
        P("back_tank", (5, 8, 2.2), (11, 15, 4.5), dark, pattern="plates", accent=stone),
        P("back_glow", (6.2, 9.2, 2.0), (9.8, 13.5, 2.3), cyan, glow=True),
    ]
    return Model("echo_golem", parts)


# ------------------------------------------------------------------------------- Sculk Slasher
def slasher():
    body, head, cyan, claw = "#14252e", "#1d3440", "#52f2ff", "#e8f2f4"
    parts = [
        P("body", (4.5, 4, 1.5), (11.5, 9.5, 11.5), body, pattern="veins", accent=cyan),
        P("head", (5, 5.2, 11), (11, 10.8, 16.5), head,
          decals={"south": [(0, 1, 2, 1, cyan), (4, 1, 2, 1, cyan), (0, 1, 1, 1, "#ffffff"), (5, 1, 1, 1, "#ffffff"),
                            (1, 4, 4, 1, "#050b0e"), (1, 4, 1, 1, claw), (2, 4, 1, 1, claw), (3, 4, 1, 1, claw), (4, 4, 1, 1, claw)]}),
        P("jaw", (5.4, 4.2, 12), (10.6, 5.4, 16), "#0c171c"),
        P("fore_l", (3, 0, 9.6), (5.2, 6, 12), body, pattern="veins", accent=cyan),
        P("fore_r", (10.8, 0, 9.6), (13, 6, 12), body, pattern="veins", accent=cyan),
        P("claw_l1", (2.4, 0.4, 11.6), (3.4, 1.4, 20), claw),
        P("claw_l2", (3.8, 0.4, 11.6), (4.8, 1.4, 19), claw),
        P("claw_r1", (12.6, 0.4, 11.6), (13.6, 1.4, 20), claw),
        P("claw_r2", (11.2, 0.4, 11.6), (12.2, 1.4, 19), claw),
        P("hind_l", (3.4, 0, 2), (6, 6.5, 5), body),
        P("hind_r", (10, 0, 2), (12.6, 6.5, 5), body),
        P("spine1", (7.4, 9.5, 8), (8.6, 12.5, 9.4), cyan, glow=True, rot=("x", -22.5, (8, 9.5, 8.7))),
        P("spine2", (7.4, 9.5, 5.2), (8.6, 12.8, 6.6), cyan, glow=True, rot=("x", -22.5, (8, 9.5, 5.9))),
        P("spine3", (7.4, 9.5, 2.4), (8.6, 12.2, 3.8), cyan, glow=True, rot=("x", -22.5, (8, 9.5, 3.1))),
        P("tail1", (7, 5.2, -2.5), (9, 7.4, 2), body, pattern="veins", accent=cyan),
        P("tail2", (7.3, 4, -6.5), (8.7, 5.6, -2), head),
        P("tail_tip", (7.4, 3.4, -9), (8.6, 4.6, -6), cyan, glow=True),
    ]
    return Model("sculk_slasher", parts)


# --------------------------------------------------------------------------------------- Licker
def licker():
    moss, head, nose, tongue = "#3f8f7a", "#4fa58c", "#e0803c", "#ff6fa0"
    parts = [
        P("body", (3, 4.5, 1.5), (13, 12.5, 12.5), moss, pattern="spots", accent="#7bd35f"),
        P("leg_fl", (3.2, 0, 8.4), (6.4, 5, 11.6), "#2f7563"),
        P("leg_fr", (9.6, 0, 8.4), (12.8, 5, 11.6), "#2f7563"),
        P("leg_bl", (3.2, 0, 2.4), (6.4, 5, 5.6), "#2f7563"),
        P("leg_br", (9.6, 0, 2.4), (12.8, 5, 5.6), "#2f7563"),
        P("head", (4.5, 6.2, 12), (11.5, 13.4, 17.4), head,
          decals={"south": [(1, 2, 1, 1, "#10201a"), (5, 2, 1, 1, "#10201a")]}),
        P("nose", (6, 6.4, 17), (10, 9.4, 19.4), nose, decals={"south": [(1, 1, 1, 1, "#7a3a12"), (2, 1, 1, 1, "#7a3a12")]}),
        P("tongue", (7.2, 5.1, 18.5), (8.8, 5.8, 29), tongue, pattern="spots", accent="#ff9fc0"),
        P("tongue_tip", (6.9, 4.9, 28.4), (9.1, 5.9, 31), "#ff3f7a"),
        P("ear_l", (3.4, 11, 12.6), (4.6, 15.5, 14.8), "#8fd8c0", rot=("z", 22.5, (4, 11, 13.7))),
        P("ear_r", (11.4, 11, 12.6), (12.6, 15.5, 14.8), "#8fd8c0", rot=("z", -22.5, (12, 11, 13.7))),
        P("shroom1", (5, 12.5, 4), (7.4, 14.2, 6.4), "#c73a4a", pattern="spots", accent="#ffe6e6"),
        P("shroom1_s", (5.9, 12.4, 4.9), (6.5, 12.9, 5.5), "#e8e0c8"),
        P("shroom2", (9, 12.5, 7), (11.2, 13.9, 9.2), "#3aa0c7", pattern="spots", accent="#e6f6ff"),
        P("moss1", (3.4, 12.4, 2), (9, 13.4, 5.5), "#68c455", pattern="spots", accent="#9be37c"),
    ]
    return Model("licker", parts)


# --------------------------------------------------------------------------------------- Sprout
def sprout():
    body, light, leaf = "#d6a8ff", "#ecd2ff", "#7dffb0"
    parts = [
        P("bulb", (4.8, 8, 4.8), (11.2, 15.5, 11.2), body, pattern="spots", accent=light,
          decals={"south": eyes(6, 3, 2, "#2a1450", (1, 2), "#ffffff") + [(2, 5, 2, 1, "#a06fe0")]}),
        P("mantle", (5.8, 15.5, 5.8), (10.2, 18.8, 10.2), light),
        P("stem", (7.4, 18.8, 7.4), (8.6, 20.6, 8.6), "#4fbf7c"),
        P("leaf_l", (4.4, 20, 7.2), (7.6, 21, 8.8), leaf, glow=True, rot=("z", 22.5, (7.6, 20, 8))),
        P("leaf_r", (8.4, 20, 7.2), (11.6, 21, 8.8), leaf, glow=True, rot=("z", -22.5, (8.4, 20, 8))),
        P("t1", (5.2, 1, 5.2), (6.6, 8.2, 6.6), body),
        P("t2", (9.4, 2, 5.2), (10.8, 8.2, 6.6), body),
        P("t3", (5.2, 3, 9.4), (6.6, 8.2, 10.8), body),
        P("t4", (9.4, 1, 9.4), (10.8, 8.2, 10.8), body),
        P("t5", (7.4, 0, 7.4), (8.6, 8.2, 8.6), light),
        P("tip1", (5.0, 0.2, 5.0), (6.8, 1.4, 6.8), leaf, glow=True),
        P("tip2", (9.2, 1.2, 5.0), (11, 2.4, 6.8), leaf, glow=True),
        P("tip3", (5.0, 2.2, 9.2), (6.8, 3.4, 11), leaf, glow=True),
        P("tip4", (9.2, 0.2, 9.2), (11, 1.4, 11), leaf, glow=True),
    ]
    return Model("sprout", parts)


# ------------------------------------------------------------------------------------- Seedling
def seedling():
    seed, shell, leaf = "#7ed957", "#6b4423", "#4fbf3a"
    parts = [
        P("body", (5, 2.2, 5), (11, 8.6, 11), seed, pattern="spots", accent="#a8f07a",
          decals={"south": [(1, 1, 1, 2, "#1a1a00"), (4, 1, 1, 2, "#1a1a00"), (1, 1, 1, 1, "#ffee55"), (4, 1, 1, 1, "#ffee55"), (2, 4, 2, 1, "#2a3a10")]}),
        P("cap", (4.4, 8.4, 4.4), (11.6, 11.2, 11.6), shell, pattern="plates", accent="#4a2d12"),
        P("leaf1", (7.4, 11, 7.4), (8.6, 14.5, 8.6), leaf),
        P("leaf2", (6, 13.5, 7.4), (8, 14.4, 8.6), leaf, rot=("z", 22.5, (8, 13.5, 8))),
        P("leaf3", (8, 13.5, 7.4), (10, 14.4, 8.6), leaf, rot=("z", -22.5, (8, 13.5, 8))),
        P("leg_fl", (5.4, 0, 8.6), (7.2, 2.4, 10.4), shell),
        P("leg_fr", (8.8, 0, 8.6), (10.6, 2.4, 10.4), shell),
        P("leg_bl", (5.4, 0, 5.6), (7.2, 2.4, 7.4), shell),
        P("leg_br", (8.8, 0, 5.6), (10.6, 2.4, 7.4), shell),
        P("claw_l", (4.2, 3, 9.4), (5.2, 4.2, 12), "#f0e8c8"),
        P("claw_r", (10.8, 3, 9.4), (11.8, 4.2, 12), "#f0e8c8"),
    ]
    return Model("seedling", parts)


# ------------------------------------------------------------------------------ Crested Sentinel
def crested_sentinel():
    armor, trim, mask, crest = "#3a6ea5", "#e8c45a", "#e9e0c9", "#ff6a3d"
    parts = [
        P("leg_l", (5, 0, 6.5), (7.6, 9, 9.5), "#2a4f78", pattern="plates", accent=trim),
        P("leg_r", (8.4, 0, 6.5), (11, 9, 9.5), "#2a4f78", pattern="plates", accent=trim),
        P("boot_l", (4.8, 0, 6), (7.8, 2, 10.4), trim),
        P("boot_r", (8.2, 0, 6), (11.2, 2, 10.4), trim),
        P("torso", (4.4, 9, 6), (11.6, 17.2, 10), armor, pattern="plates", accent="#2a4f78"),
        P("belt", (4.3, 9, 5.9), (11.7, 10.4, 10.1), trim),
        P("chest_gem", (7.2, 12.5, 10), (8.8, 14.5, 10.25), crest, glow=True),
        P("arm_l", (2, 9.5, 6.6), (4.4, 17, 9.4), armor, pattern="plates", accent="#2a4f78"),
        P("arm_r", (11.6, 9.5, 6.6), (14, 17, 9.4), armor, pattern="plates", accent="#2a4f78"),
        P("pauldron_l", (1.6, 16, 6), (4.6, 18, 10), trim),
        P("pauldron_r", (11.4, 16, 6), (14.4, 18, 10), trim),
        P("head", (5, 17.2, 6), (11, 23.2, 11), mask,
          decals={"south": [(1, 2, 1, 2, "#14100a"), (4, 2, 1, 2, "#14100a"), (1, 2, 1, 1, "#ffd23a"), (4, 2, 1, 1, "#ffd23a"), (2, 4, 2, 1, "#14100a")]}),
        P("crest1", (7.4, 23.2, 5.2), (8.6, 27.5, 11.2), crest, glow=True, noise=0.04),
        P("crest2", (7.4, 27, 5), (8.6, 31, 8.8), crest, rot=("x", -22.5, (8, 27, 6.9)), glow=True, noise=0.04),
        P("crest3", (7.4, 24, 3.4), (8.6, 28, 5.4), "#ffa34a", rot=("x", -22.5, (8, 24, 4.4)), glow=True, noise=0.04),
    ]
    return Model("crested_sentinel", parts)


# ----------------------------------------------------------------------------- Groobler Sentinel
def groobler():
    moss, bark, shell = "#5f7a3a", "#4a3a22", "#7b5a2e"
    parts = [
        P("leg_l", (3.6, 0, 5), (7.6, 7, 10.8), bark),
        P("leg_r", (8.4, 0, 5), (12.4, 7, 10.8), bark),
        P("torso", (2.4, 7, 3.6), (13.6, 17.4, 12.4), moss, pattern="spots", accent="#8fb050"),
        P("belly_plate", (4, 8, 12.3), (12, 14.5, 12.8), shell, pattern="plates", accent=bark),
        P("shell_back", (3, 8, 0.4), (13, 18, 3.6), shell, pattern="plates", accent=bark),
        P("shell_top", (4, 18, 1.4), (12, 19.6, 4.6), shell, pattern="plates", accent=bark),
        P("pad_l", (-0.4, 15, 3.6), (3.2, 19, 12), shell, pattern="plates", accent=bark),
        P("pad_r", (12.8, 15, 3.6), (16.4, 19, 12), shell, pattern="plates", accent=bark),
        P("arm_l", (0, 6, 5), (3, 16, 11), moss),
        P("arm_r", (13, 6, 5), (16, 16, 11), moss),
        P("fist_l", (-0.8, 3, 4.4), (3.6, 7, 11.6), bark),
        P("fist_r", (12.4, 3, 4.4), (16.8, 7, 11.6), bark),
        P("head", (5, 16.4, 6), (11, 22, 12.6), moss,
          decals={"south": [(1, 2, 1, 1, "#ffd23a"), (4, 2, 1, 1, "#ffd23a"), (1, 4, 4, 1, "#1a2208")]}),
        P("tusk_l", (5.4, 15, 12.2), (6.4, 17.4, 13.8), "#f0e8c8"),
        P("tusk_r", (9.6, 15, 12.2), (10.6, 17.4, 13.8), "#f0e8c8"),
        P("shield", (16.2, 6, 2.5), (18, 18.5, 13), shell, pattern="plates", accent="#a97a3a"),
        P("shield_boss", (18, 11, 6.5), (19, 14, 9), "#e8c45a"),
    ]
    return Model("groobler", parts)


# --------------------------------------------------------------------------------------- Nester
def nester():
    amber, dark, nest = "#c7a24a", "#8a6a2e", "#6e5226"
    parts = [
        P("leg_l", (4.6, 0, 5), (7.2, 6.4, 8.6), dark),
        P("leg_r", (8.8, 0, 5), (11.4, 6.4, 8.6), dark),
        P("torso", (4, 6, 3.6), (12, 13, 10), amber, pattern="bands", accent=dark),
        P("nest", (2.6, 9.5, 0.4), (13.4, 18.5, 7), nest, pattern="plates", accent="#4a3818"),
        P("hole1", (4, 12, 0.2), (6, 14, 0.5), "#0a0604"),
        P("hole2", (9, 14.5, 0.2), (11, 16.5, 0.5), "#0a0604"),
        P("larva1", (4.4, 11.8, -0.4), (5.6, 13, 0.4), "#fff6d8"),
        P("larva2", (9.4, 14.3, -0.4), (10.6, 15.5, 0.4), "#fff6d8"),
        P("arm_l", (1.6, 3.5, 7), (4, 12.6, 9.4), amber),
        P("arm_r", (12, 3.5, 7), (14.4, 12.6, 9.4), amber),
        P("claw_l", (1.4, 1.6, 7.4), (2.6, 3.8, 12), "#f4ecd0"),
        P("claw_r", (13.4, 1.6, 7.4), (14.6, 3.8, 12), "#f4ecd0"),
        P("head", (5, 9.4, 8.6), (11, 14.6, 14), amber,
          decals={"south": [(1, 1, 1, 2, "#1a1000"), (4, 1, 1, 2, "#1a1000"), (1, 1, 1, 1, "#ff9a3a"), (4, 1, 1, 1, "#ff9a3a")]}),
        P("mandible_l", (4.6, 8.6, 12.4), (5.8, 10, 15.6), "#f4ecd0", rot=("y", 22.5, (5.2, 9, 13))),
        P("mandible_r", (10.2, 8.6, 12.4), (11.4, 10, 15.6), "#f4ecd0", rot=("y", -22.5, (10.8, 9, 13))),
        P("antenna_l", (5.4, 14.4, 11), (6.2, 18, 11.8), dark, rot=("z", 22.5, (5.8, 14.4, 11.4))),
        P("antenna_r", (9.8, 14.4, 11), (10.6, 18, 11.8), dark, rot=("z", -22.5, (10.2, 14.4, 11.4))),
    ]
    return Model("nester", parts)


# ------------------------------------------------------------------------------------ Sculk Mage
def sculk_mage():
    robe, trim, cyan, hood = "#2a1f5e", "#1a1340", "#52f2ff", "#33267a"
    parts = [
        P("robe_low", (3.6, 0, 5), (12.4, 7, 11), robe, pattern="veins", accent=cyan),
        P("robe_mid", (4.2, 7, 5.4), (11.8, 14, 10.6), robe),
        P("hem_glow", (3.5, 0.2, 4.9), (12.5, 0.9, 11.1), cyan, glow=True),
        P("sleeve_l", (1.8, 8.4, 6.6), (4.2, 13.2, 11.2), hood),
        P("sleeve_r", (11.8, 8.4, 6.6), (14.2, 13.2, 11.2), hood),
        P("hand_l", (2, 8.4, 11), (4, 10.4, 13), "#8a7ad0"),
        P("hand_r", (12, 8.4, 11), (14, 10.4, 13), "#8a7ad0"),
        P("head", (4.6, 14, 5.4), (11.4, 21, 11.6), hood,
          decals={"south": [(1, 2, 5, 3, "#07040f"), (1, 3, 1, 1, cyan), (4, 3, 1, 1, cyan), (1, 3, 1, 1, "#ffffff"), (4, 3, 1, 1, "#ffffff")]}),
        P("horn_l", (3.8, 19, 6.4), (5.2, 25.5, 7.8), cyan, rot=("z", 22.5, (4.5, 19, 7.1)), glow=True),
        P("horn_r", (10.8, 19, 6.4), (12.2, 25.5, 7.8), cyan, rot=("z", -22.5, (11.5, 19, 7.1)), glow=True),
        P("shard1", (0.4, 14, 3), (1.8, 17.5, 4.4), cyan, rot=("z", 22.5, (1.1, 14, 3.7)), glow=True),
        P("shard2", (14.2, 17, 4.4), (15.6, 20.5, 5.8), cyan, rot=("z", -22.5, (14.9, 17, 5.1)), glow=True),
        P("shard3", (7.2, 22, 2.4), (8.8, 25.5, 3.8), cyan, glow=True),
        P("tendril_l", (4.8, 3, 4.4), (5.8, 14, 5.4), "#52f2ff", glow=True, noise=0.03),
        P("tendril_r", (10.2, 3, 4.4), (11.2, 14, 5.4), "#52f2ff", glow=True, noise=0.03),
    ]
    return Model("sculk_mage", parts)


ALL = [blub, singer, echo_golem, slasher, licker, sprout, seedling, crested_sentinel, groobler, nester, sculk_mage]


def all_models():
    return [f() for f in ALL]


if __name__ == "__main__":
    import os
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp"
    os.makedirs(out, exist_ok=True)
    for m in all_models():
        m.build()
        m.preview(os.path.join(out, m.name + "_a.png"), yaw=35)
        m.preview(os.path.join(out, m.name + "_b.png"), yaw=-140)
        print(m.name, len(m.parts), "parts, atlas", m.size)
