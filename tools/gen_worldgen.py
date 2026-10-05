"""Génère toute la partie worldgen du pack : dimension, marées, terrain, biomes, features, carvers."""
import os

from lib import dp_json, dp_text, NS, state

REF = os.environ.get("MCREF", "")  # dossier de référence vanilla (facultatif, voir README)


def c(v):
    return {"type": "minecraft:constant", "argument": v} if not isinstance(v, (int, float)) else v


# ---------------------------------------------------------------------------
# Helpers densité
# ---------------------------------------------------------------------------
def absf(i): return {"type": "minecraft:abs", "input": i}
def clamp(i, lo, hi): return {"type": "minecraft:clamp", "input": i, "min": lo, "max": hi}
def noise(n, xz=1.0, y=0.0): return {"type": "minecraft:noise", "noise": n, "xz_scale": xz, "y_scale": y}
def cache(i): return {"type": "minecraft:cache", "input": i}


# Les champs binaires de ce format sont nommés left/right (cf. final_density vanilla 26.3)
def _bin(t):
    return lambda a, b: {"type": f"minecraft:{t}", "left": a, "right": b}


add = _bin("add")
mul = _bin("mul")
_min = _bin("min")
_max = _bin("max")


def sub(a, b):
    return add(a, mul(b, -1.0))


def gradient(y0, v0, y1, v1):
    return {"type": "minecraft:gradient", "axis": "y", "from_coordinate": y0, "from_value": v0,
            "to_coordinate": y1, "to_value": v1}


# ---------------------------------------------------------------------------
# Marées : horloge + timeline
# ---------------------------------------------------------------------------
TIDE_TICKS = 8000
PERIOD = TIDE_TICKS * 3
# multiplicateurs de teinte appliqués au ciel/brouillard (un par marée)
TIDES = [
    # (id, ciel, brouillard, lumière ambiante, nuages)
    ("hush",  "#b8ecff", "#c8f4ff", "#bfe8ff", "#ffbfeaff"),
    ("surge", "#ffb0ff", "#ffc4ff", "#ffb8ff", "#ffffc0ff"),
    ("ebb",   "#ffc888", "#ffd8a0", "#ffd0a0", "#ffffd8a0"),
]


def tide_track(idx, margin=900, ramp=900):
    """Palier de couleur pour la marée idx : plateau entre start+margin et end-margin."""
    s = idx * TIDE_TICKS
    return [s + margin, s + TIDE_TICKS - margin - ramp]


def gen_clock_and_timeline():
    dp_json(f"{NS}/world_clock/tides", {})
    tracks = {}

    def color_track(attr, col_index, modifier="multiply"):
        kfs = []
        for i, t in enumerate(TIDES):
            a, b = tide_track(i)
            kfs.append({"ticks": a, "value": t[col_index]})
            kfs.append({"ticks": b, "value": t[col_index]})
        return {"keyframes": kfs, "modifier": modifier}

    tracks["minecraft:visual/sky_color"] = color_track("sky", 1)
    tracks["minecraft:visual/fog_color"] = color_track("fog", 2)
    # lune géante fixe + étoiles éclatantes en permanence : le ciel du Sift ne dort jamais
    tracks["minecraft:visual/sun_angle"] = {"keyframes": [{"ticks": 0, "value": 190.0}, {"ticks": PERIOD - 1, "value": 190.0}]}
    tracks["minecraft:visual/moon_angle"] = {"keyframes": [{"ticks": 0, "value": 20.0}, {"ticks": PERIOD - 1, "value": 20.0}]}
    tracks["minecraft:visual/star_angle"] = {"keyframes": [{"ticks": 0, "value": 0.0}, {"ticks": PERIOD, "value": 360.0}]}
    tracks["minecraft:visual/moon_phase"] = {"keyframes": [{"ticks": 0, "value": "full_moon"}]}
    dp_json(f"{NS}/timeline/tides", {"clock": f"{NS}:tides", "period_ticks": PERIOD, "tracks": tracks})
    dp_json(f"{NS}/tags/timeline/in_sift", {"values": [f"{NS}:tides", "#minecraft:universal"]})


# ---------------------------------------------------------------------------
# Dimension & type
# ---------------------------------------------------------------------------
def gen_dimension():
    bed = {"can_set_spawn": "never", "can_sleep": "never",
           "error_message": {"translate": "sift.bed.no_sleep", "fallback": "Les chants du Sift vous empêchent de dormir."}}
    dp_json(f"{NS}/dimension_type/the_sift", {
        "ambient_light": 0.1,
        "attributes": {
            "minecraft:audio/ambient_sounds": {"mood": {"block_search_extent": 8, "offset": 2.0, "sound": "minecraft:ambient.cave", "tick_delay": 6000}},
            "minecraft:audio/background_music": {"default": {"min_delay": 3000, "max_delay": 9000, "sound": f"{NS}:music.sift"}},
            "minecraft:gameplay/bed_rule": bed,
            "minecraft:gameplay/straw_bed_rule": dict(bed),
            "minecraft:gameplay/can_start_raid": False,
            "minecraft:gameplay/nether_portal_spawns_piglin": False,
            "minecraft:gameplay/respawn_anchor_works": True,
            "minecraft:gameplay/water_evaporates": False,
            "minecraft:visual/ambient_light_color": "#241a3a",
            "minecraft:visual/cloud_color": "#99ffe0ff",
            "minecraft:visual/cloud_height": 230.0,
            "minecraft:visual/fog_color": "#b8f0ff",
            "minecraft:visual/sky_color": "#78d8ff",
            "minecraft:visual/star_brightness": 1.0,
        },
        "coordinate_scale": 1.0,
        "default_clock": f"{NS}:tides",
        "has_ceiling": False,
        "has_ender_dragon_fight": False,
        "has_skylight": True,
        "height": 384,
        "infiniburn": "#minecraft:infiniburn_overworld",
        "logical_height": 384,
        "min_y": -64,
        "monster_spawn_block_light_limit": 15,
        "monster_spawn_light_level": 15,
        "timelines": f"#{NS}:in_sift",
    })
    dp_json(f"{NS}/dimension/the_sift", {
        "type": f"{NS}:the_sift",
        "generator": {
            "type": "minecraft:noise",
            "biome_source": {"type": "minecraft:multi_noise", "biomes": biome_source_entries()},
            "settings": f"{NS}:the_sift",
        },
    })


# ---------------------------------------------------------------------------
# Biomes : paramètres climatiques
# ---------------------------------------------------------------------------
def P(temp=(-1, 1), hum=(-1, 1), cont=(-1, 1), ero=(-1, 1), weird=(-1, 1), depth=0.0, off=0.0):
    r = lambda v: list(v) if isinstance(v, tuple) else v
    return {"temperature": r(temp), "humidity": r(hum), "continentalness": r(cont), "erosion": r(ero),
            "weirdness": r(weird), "depth": r(depth), "offset": off}


def biome_source_entries():
    e = []

    def surf(biome, **kw):
        for d in (0.0, 1.0):
            e.append({"biome": f"{NS}:{biome}", "parameters": P(depth=d, **kw)})

    surf("ichor_fens", cont=(-1.0, -0.2))
    surf("singers_meadow", cont=(-0.2, 0.3), temp=(-1.0, 0.15))
    surf("carapace", cont=(-0.2, 0.3), temp=(0.15, 1.0))
    surf("resonant_crags", cont=(0.3, 1.0))
    e.append({"biome": f"{NS}:sculk_resonance", "parameters": P(depth=(0.2, 0.9))})
    return e


COL = {
    "meadow": dict(grass="#33b6ff", foliage="#9fe3ff", water="#d24dff", wfog="#7a1fb0", sky="#78d8ff", fog="#b8f0ff"),
    "carapace": dict(grass="#e8a838", foliage="#ffc860", water="#ffb43a", wfog="#a05a00", sky="#ffc880", fog="#ffe0b0"),
    "fens": dict(grass="#4dffc4", foliage="#7affd8", water="#3cf2d0", wfog="#0a7a78", sky="#a58bff", fog="#d4c4ff"),
    "crags": dict(grass="#ff7a9a", foliage="#ffa0b8", water="#ff4f78", wfog="#a01040", sky="#ff9ab0", fog="#ffd0d8"),
    "caves": dict(grass="#6a5aff", foliage="#8a7aff", water="#9b6bff", wfog="#3a1f8a", sky="#78d8ff", fog="#b8f0ff"),
}


def particles(*items):
    out = []
    for name, prob in items:
        out.append({"particle": {"type": f"minecraft:{name}"}, "probability": prob})
    return {"argument": out, "modifier": "append"}


def biome_json(key, carvers, features, temp, parts, music=None, extra_attr=None):
    col = COL[key]
    attrs = {
        "minecraft:visual/sky_color": col["sky"],
        "minecraft:visual/fog_color": col["fog"],
        "minecraft:visual/water_fog_color": col["wfog"],
        "minecraft:visual/ambient_particles": parts,
    }
    if music:
        attrs["minecraft:audio/background_music"] = {"default": {"min_delay": 3000, "max_delay": 9000, "sound": music}}
    if extra_attr:
        attrs.update(extra_attr)
    return {
        "attributes": attrs,
        "carvers": carvers,
        "downfall": 0.0,
        "effects": {"foliage_color": col["foliage"], "grass_color": col["grass"], "water_color": col["water"]},
        "features": features,
        "has_precipitation": False,
        "temperature": temp,
    }


def step(*names):
    return [f"{NS}:{n}" if ":" not in n else n for n in names]


UNDERGROUND = ["ore_coal", "ore_iron", "ore_copper", "ore_gold", "ore_redstone", "ore_lapis", "ore_diamond",
               "ore_emerald", "ore_soul_soil", "ore_sculk_blob", "ore_amethyst_cluster"]


def gen_biomes():
    cave = [f"{NS}:cave", f"{NS}:canyon"]

    def feats(lakes=(), local=(), surface=(), veg=(), springs=(), top=(), under_deco=(), underground_struct=()):
        return [[], step(*lakes), step(*local), step(*underground_struct), step(*surface), [],
                step(*UNDERGROUND), step(*under_deco), step(*springs), step(*veg), step(*top)]

    meadow_f = feats(
        lakes=["ichor_pool"],
        local=["crag_geode_rare"],
        surface=[],
        under_deco=["sculk_vein_cave", "crystal_cluster_cave"],
        springs=["ichor_spring"],
        veg=["sculk_carpet", "trees_meadow", "tall_blue_grass", "blue_grass", "flowers_meadow", "wildflowers_meadow", "bloom_orbs"],
    )
    dp_json(f"{NS}/worldgen/biome/singers_meadow", biome_json(
        "meadow", cave, meadow_f, 0.7,
        particles(("note", 0.0009), ("soul", 0.002), ("firefly", 0.0012), ("end_rod", 0.0008)),
        music=f"{NS}:music.meadow"))

    carapace_f = feats(
        lakes=["ichor_pool_rare"],
        local=["bone_ribs"],
        under_deco=["sculk_vein_cave", "crystal_cluster_cave"],
        springs=["ichor_spring"],
        veg=["bone_spires", "amber_grass_disk", "amber_grass", "dry_scrub", "carapace_cactus", "amber_wildflowers"],
    )
    dp_json(f"{NS}/worldgen/biome/carapace", biome_json(
        "carapace", cave + [], carapace_f, 1.6,
        particles(("white_ash", 0.012), ("soul", 0.0016), ("sculk_soul", 0.0007)),
        music=f"{NS}:music.carapace"))

    fens_f = feats(
        lakes=[],
        local=[],
        under_deco=["sculk_vein_cave"],
        springs=[],
        veg=["fen_trees", "fen_sculk", "fen_kelp", "fen_seagrass", "fen_lilies", "fen_lights", "grass_fen"],
        top=[],
    )
    dp_json(f"{NS}/worldgen/biome/ichor_fens", biome_json(
        "fens", cave, fens_f, 0.9,
        particles(("sculk_soul", 0.0016), ("bubble_pop", 0.0008), ("firefly", 0.002), ("soul", 0.0012)),
        music=f"{NS}:music.fens"))

    crags_f = feats(
        lakes=[],
        local=["crag_geode", "crag_geode_rare"],
        surface=[],
        under_deco=["sculk_vein_cave", "crystal_cluster_cave"],
        springs=["ichor_spring"],
        veg=["crag_crystals", "sculk_vein_crags", "crag_blossoms", "blue_grass_sparse"],
    )
    dp_json(f"{NS}/worldgen/biome/resonant_crags", biome_json(
        "crags", cave, crags_f, 0.3,
        particles(("end_rod", 0.0018), ("glow", 0.0012), ("soul", 0.0015), ("note", 0.0004)),
        music=f"{NS}:music.crags"))

    caves_f = feats(
        lakes=[],
        local=[],
        under_deco=["sculk_cavern_patch", "sculk_sensors", "cavern_crystals", "cavern_blossoms", "sculk_vein_cave"],
        springs=["ichor_spring"],
        veg=[],
    )
    dp_json(f"{NS}/worldgen/biome/sculk_resonance", biome_json(
        "caves", cave, caves_f, 0.5,
        particles(("sculk_soul", 0.002), ("sculk_charge_pop", 0.0007), ("note", 0.0006)),
        music=f"{NS}:music.resonance"))


# ---------------------------------------------------------------------------
# Carvers
# ---------------------------------------------------------------------------
def gen_carvers():
    dp_json(f"{NS}/worldgen/carver/cave", {
        "type": "minecraft:cave",
        "count": {"type": "minecraft:very_biased_to_bottom", "max_inclusive": 14, "min_inclusive": 0},
        "floor_level": {"type": "minecraft:uniform", "max_exclusive": -0.4, "min_inclusive": -1.0},
        "horizontal_radius_multiplier": {"type": "minecraft:uniform", "max_exclusive": 1.6, "min_inclusive": 0.8},
        "probability": 0.2,
        "room_vertical_radius_multiplier": {"type": "minecraft:uniform", "max_exclusive": 0.9, "min_inclusive": 0.1},
        "thickness": {"type": "minecraft:trapezoid", "max": 3.0, "min": 0.0, "plateau": 1.0},
        "vertical_radius_multiplier": {"type": "minecraft:uniform", "max_exclusive": 1.3, "min_inclusive": 0.8},
        "weird_thickness_bias": True,
        "y": {"type": "minecraft:uniform", "max_inclusive": {"absolute": 90}, "min_inclusive": {"above_bottom": 8}},
    })
    dp_json(f"{NS}/worldgen/carver/canyon", {
        "type": "minecraft:canyon",
        "probability": 0.012,
        "shape": {
            "distance_factor": {"type": "minecraft:uniform", "max_exclusive": 1.0, "min_inclusive": 0.75},
            "horizontal_radius_factor": {"type": "minecraft:uniform", "max_exclusive": 1.0, "min_inclusive": 0.75},
            "thickness": {"type": "minecraft:trapezoid", "max": 6.0, "min": 0.0, "plateau": 2.0},
            "vertical_radius_center_factor": 0.0,
            "vertical_radius_default_factor": 1.0,
            "width_smoothness": 3,
            "y_scale": 3.0,
        },
        "vertical_rotation": {"type": "minecraft:uniform", "max_exclusive": 0.125, "min_inclusive": -0.125},
        "y": {"type": "minecraft:uniform", "max_inclusive": {"absolute": 67}, "min_inclusive": {"absolute": 10}},
    })


# ---------------------------------------------------------------------------
# Bruits, fonctions de densité, noise settings, material rules
# ---------------------------------------------------------------------------
NOISES = {
    # nom: (octave de base, nb d'octaves, amplitudes)
    "continents": (-9, 6, None),
    "temperature": (-9, 4, None),
    "humidity": (-8, 4, None),
    "erosion": (-9, 5, None),
    "weirdness": (-7, 4, None),
    "ravine": (-8, 3, None),
    "patch": (-5, 3, None),
    "surface": (-6, 3, None),
}


def gen_noise_and_density():
    for name, (octave, count, amps) in NOISES.items():
        dp_json(f"{NS}/worldgen/noise/{name}", {"base_amplitude": 1.0, "base_octave": octave, "octave_count": count})

    def mk(name, obj):
        dp_json(f"{NS}/worldgen/density_function/{name}", obj)

    ref = lambda n: f"{NS}:{n}"
    mk("continents", cache(noise(ref("continents"), 0.7, 0.0)))
    mk("temperature", cache(noise(ref("temperature"), 0.6, 0.0)))
    mk("humidity", cache(noise(ref("humidity"), 0.6, 0.0)))
    mk("erosion", cache(noise(ref("erosion"), 0.6, 0.0)))
    mk("weirdness", cache(noise(ref("weirdness"), 0.6, 0.0)))

    cont = ref("continents")
    # relief : collines douces, bassins d'ichor, crêtes résonantes
    base = mul(cont, 0.2)
    basin = mul(clamp(sub(-0.2, cont), 0.0, 1.0), -1.2)
    crag = mul(clamp(sub(cont, 0.3), 0.0, 1.0), 1.6)
    mk("offset", cache(add(add(base, basin), crag)))
    mk("depth", add(gradient(-64, 1.5, 192, -1.5), ref("offset")))

    # masque de crêtes (amplitude du bruit 3D) et rubans de ravins (Carapace uniquement)
    crag_mask = clamp(mul(sub(cont, 0.25), 3.0), 0.0, 1.0)
    detail_amp = add(0.8, mul(crag_mask, 2.0))
    ribbon = clamp(sub(1.0, mul(absf(noise(ref("ravine"), 1.0, 0.0)), 22.0)), 0.0, 1.0)
    hot = clamp(mul(sub(ref("temperature"), 0.1), 6.0), 0.0, 1.0)
    not_basin = clamp(mul(add(cont, 0.15), 6.0), 0.0, 1.0)
    ravines = mul(mul(ribbon, mul(hot, not_basin)), 3.2)

    sloped = sub(add(mul(ref("depth"), 6.0), mul("minecraft:overworld/base_3d_noise", detail_amp)), ravines)
    mk("sloped", sloped)

    final = {
        "type": "minecraft:add",
        "left": {
            "type": "minecraft:squeeze",
            "input": {
                "type": "minecraft:interpolated",
                "cell_size_xz": 4,
                "cell_size_y": 8,
                "input": mul({
                    "type": "minecraft:blend_density",
                    "input": {
                        "type": "minecraft:lerp",
                        "alpha": gradient(-64, 0.0, -40, 1.0),
                        "first": 0.1171875,
                        "second": {
                            "type": "minecraft:lerp",
                            "alpha": gradient(300, 1.0, 320, 0.0),
                            "first": -0.078125,
                            "second": ref("sloped"),
                        },
                    },
                }, 0.64),
            },
        },
        "right": {"type": "minecraft:beardifier"},
    }
    mk("final_density", final)


def gen_noise_settings():
    ref = lambda n: f"{NS}:{n}"
    dp_json(f"{NS}/worldgen/noise_settings/the_sift", {
        "default_block": "minecraft:terracotta",
        "default_fluid": "minecraft:water",
        "disable_mob_generation": False,
        "legacy_random_source": False,
        "material_rule": f"{NS}:surface",
        "noise": {"height": 384, "min_y": -64},
        "noise_router": {
            "chunk_surface_level": 0.0,
            "continents": ref("continents"),
            "depth": ref("depth"),
            "erosion": ref("erosion"),
            "final_density": ref("final_density"),
            "ridges": ref("weirdness"),
            "temperature": ref("temperature"),
            "vegetation": ref("humidity"),
        },
        "sea_level": 62,
        "spawn_target": [],
    })


def cond(if_true, then):
    return {"type": "minecraft:condition", "if_true": if_true, "then_run": then}


def blockr(b):
    return {"type": "minecraft:block", "result_state": b}


def seq(*rules):
    return {"type": "minecraft:sequence", "sequence": list(rules)}


def biome_is(b):
    return {"type": "minecraft:biome", "biome_is": f"{NS}:{b}"}


def noise_gate(noise_id, lo, hi=1.7976931348623157e308):
    return {"type": "minecraft:noise_threshold", "noise": noise_id, "min_threshold": lo, "max_threshold": hi}


def y_above(y, mult=0, stone=False):
    return {"type": "minecraft:y_above", "anchor": {"absolute": y}, "surface_depth_multiplier": mult, "add_stone_depth": stone}


def gen_material_rule():
    on_floor, under_floor = "minecraft:on_floor", "minecraft:under_floor"
    not_underwater = "minecraft:not_underwater"
    patch = f"{NS}:patch"

    meadow = cond(biome_is("singers_meadow"), seq(
        cond(on_floor, seq(
            cond(not_underwater, seq(
                cond(noise_gate(patch, 0.35), blockr("minecraft:sculk")),
                blockr("minecraft:grass_block"))),
            blockr("minecraft:gravel"))),
        cond(under_floor, seq(
            cond(noise_gate(patch, -0.1, 0.2), blockr("minecraft:red_terracotta")),
            blockr("minecraft:orange_terracotta"))),
    ))

    carapace = cond(biome_is("carapace"), seq(
        cond(on_floor, seq(
            cond(not_underwater, seq(
                cond(noise_gate(patch, 0.5), blockr("minecraft:grass_block")),
                cond(noise_gate(patch, -0.5, -0.3), blockr("minecraft:bone_block")),
                blockr("minecraft:sand"))),
            blockr("minecraft:gravel"))),
        cond(under_floor, seq(
            cond(noise_gate(patch, 0.0), blockr("minecraft:blue_terracotta")),
            blockr("minecraft:cyan_terracotta"))),
    ))

    fens = cond(biome_is("ichor_fens"), seq(
        cond(on_floor, seq(
            cond(noise_gate(patch, 0.25), blockr("minecraft:soul_soil")),
            blockr("minecraft:mud"))),
        cond(under_floor, seq(
            cond(noise_gate(patch, -0.1), blockr("minecraft:packed_mud")),
            blockr("minecraft:mud"))),
    ))

    crags = cond(biome_is("resonant_crags"), seq(
        cond(on_floor, seq(
            cond(y_above(112), blockr("minecraft:calcite")),
            cond(noise_gate(patch, 0.3), blockr("minecraft:smooth_red_sandstone")),
            blockr("minecraft:red_sandstone"))),
        cond(under_floor, blockr("minecraft:red_terracotta")),
    ))

    caves = cond(biome_is("sculk_resonance"), seq(
        cond("minecraft:on_floor", blockr("minecraft:sculk")),
        cond("minecraft:on_ceiling", blockr("minecraft:sculk")),
        cond(under_floor, blockr("minecraft:deepslate")),
    ))

    rule = seq(
        "minecraft:bedrock_floor",
        cond({"type": "minecraft:vertical_gradient", "random_name": f"{NS}:deepslate",
              "true_at_and_below": {"absolute": -8}, "false_at_and_above": {"absolute": 4}},
             blockr("minecraft:deepslate")),
        caves, meadow, carapace, fens, crags,
        {"type": "minecraft:bandlands"},
    )
    dp_json(f"{NS}/worldgen/material_rule/surface", rule)
    # tag des blocs minables par les filons du Sift
    dp_json(f"{NS}/tags/block/ore_replaceables", {"values": [
        "minecraft:terracotta", "minecraft:red_terracotta", "minecraft:orange_terracotta",
        "minecraft:yellow_terracotta", "minecraft:white_terracotta", "minecraft:brown_terracotta",
        "minecraft:light_gray_terracotta", "minecraft:blue_terracotta", "minecraft:cyan_terracotta",
        "minecraft:red_sandstone", "minecraft:deepslate", "minecraft:sculk"]})


def gen_all():
    gen_clock_and_timeline()
    gen_dimension()
    gen_biomes()
    gen_carvers()
    gen_noise_and_density()
    gen_noise_settings()
    gen_material_rule()
