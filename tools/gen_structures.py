"""Structures du Sift (templates .nbt générés par code) + jigsaw/structure_set + tables de butin des coffres."""
import json
import math

import nbtw
from lib import dp_json, dp_bytes, NS

N = NS


def chest(st, x, y, z, facing, table):
    st.set(x, y, z, "chest", nbt={"id": nbtw.s("minecraft:chest"), "LootTable": nbtw.s(f"{N}:chests/{table}")}, facing=facing, type="single", waterlogged=False)


def shrine():
    """Sanctuaire du Chanteur : Machine à notes complète au centre d'un cercle de pierre chantante."""
    n = 13
    st = nbtw.Structure(n, 9, n)
    c = 6
    floor_blocks = ["polished_deepslate", "deepslate_tiles", "polished_blackstone_bricks", "smooth_basalt"]
    for x in range(n):
        for z in range(n):
            r = math.hypot(x - c, z - c)
            if r <= 6.4:
                ring = int(r)
                st.set(x, 0, z, floor_blocks[ring % 4 if ring < 6 else 2])
                for y in range(1, 9):
                    st.set(x, y, z, "air")
    # Machine à notes (noyau en dessous du bloc musical)
    st.set(c, 0, c, "sculk_catalyst", bloom=False)
    st.set(c, 1, c, "note_block", instrument="harp", note=12, powered=False)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        st.set(c + dx, 1, c + dz, "sculk_sensor", power=0, sculk_sensor_phase="inactive", waterlogged=False)
    # quatre piliers de calcite et d'améthyste
    for px, pz in ((2, 2), (10, 2), (2, 10), (10, 10)):
        st.set(px, 1, pz, "chiseled_deepslate")
        for y in range(2, 6):
            st.set(px, y, pz, "calcite" if y % 2 == 0 else "amethyst_block")
        st.set(px, 6, pz, "smooth_red_sandstone")
        st.set(px, 7, pz, "soul_lantern", hanging=False, waterlogged=False)
        for dx, dz, f in ((1, 0, "west"), (-1, 0, "east"), (0, 1, "north"), (0, -1, "south")):
            st.set(px + dx, 2, pz + dz, "amethyst_cluster", facing=f, waterlogged=False)
    # petit muret avec ouvertures aux points cardinaux
    for x in range(n):
        for z in range(n):
            r = math.hypot(x - c, z - c)
            if 5.6 <= r <= 6.4 and not (abs(x - c) <= 1 or abs(z - c) <= 1):
                st.set(x, 1, z, "cut_red_sandstone_slab", type="bottom", waterlogged=False)
    chest(st, c + 3, 1, c, "west", "shrine")
    chest(st, c - 3, 1, c, "east", "shrine")
    for (x, z) in ((c, c + 3), (c, c - 3)):
        st.set(x, 1, z, "lodestone")
        st.set(x, 2, z, "amethyst_block")
    # veines de sculk au sol
    for (x, z) in ((4, 4), (8, 4), (4, 8), (8, 8), (6, 2), (6, 10), (2, 6), (10, 6)):
        st.set(x, 0, z, "sculk")
    return st


def outpost():
    """Avant-poste de Sentinelles : tour de terre cuite bleue/cyan, crête rouge et brasero d'âmes."""
    w, h = 7, 17
    st = nbtw.Structure(w, h, w)
    for x in range(w):
        for z in range(w):
            st.set(x, 0, z, "polished_blackstone_bricks")
            for y in range(1, h):
                st.set(x, y, z, "air")
    for y in range(1, 13):
        for x in range(w):
            for z in range(w):
                edge = x in (0, w - 1) or z in (0, w - 1)
                if edge:
                    corner = x in (0, w - 1) and z in (0, w - 1)
                    st.set(x, y, z, "blue_terracotta" if corner else ("cyan_terracotta" if y % 4 == 0 else "blue_terracotta"))
        if y % 4 == 0:
            for x in range(1, w - 1):
                for z in range(1, w - 1):
                    st.set(x, y, z, "dark_oak_planks")
    for y in (3, 7, 10):
        for pos in ((3, y, 0), (3, y, 6), (0, y, 3), (6, y, 3)):
            st.set(*pos, "air")
            st.set(pos[0], pos[1] + 1, pos[2], "air")
    st.set(3, 1, 0, "air")
    st.set(3, 2, 0, "air")
    # échelle intérieure
    for y in range(1, 12):
        st.set(1, y, 3, "ladder", facing="east", waterlogged=False)
    st.set(1, 12, 3, "air")
    # créneaux, crête et brasero
    for x in range(w):
        for z in range(w):
            if x in (0, w - 1) or z in (0, w - 1):
                st.set(x, 13, z, "cut_red_sandstone" if (x + z) % 2 == 0 else "air")
    st.fill(3, 13, 3, 3, 15, 3, "red_terracotta")
    st.set(3, 16, 3, "soul_campfire", facing="north", lit=True, signal_fire=False, waterlogged=False)
    chest(st, 5, 13, 5, "west", "outpost")
    chest(st, 2, 9, 5, "north", "outpost")
    return st


def obelisk():
    """Obélisque d'ichor du marais : spire de briques de boue avec lanternes d'âmes."""
    st = nbtw.Structure(7, 18, 7)
    for x in range(7):
        for z in range(7):
            st.set(x, 0, z, "mud_bricks")
    layers = [(5, 1, 3), (3, 4, 8), (1, 9, 15)]
    for (size, y0, y1) in layers:
        o = (7 - size) // 2
        for y in range(y0, y1 + 1):
            for x in range(o, o + size):
                for z in range(o, o + size):
                    mat = "mud_bricks"
                    if y % 3 == 0:
                        mat = "packed_mud"
                    if size == 1:
                        mat = "chiseled_deepslate" if y % 2 == 0 else "polished_deepslate"
                    st.set(x, y, z, mat)
    st.set(3, 16, 3, "sea_lantern")
    st.set(3, 17, 3, "soul_lantern", hanging=False, waterlogged=False)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        st.set(3 + dx, 15, 3 + dz, "amethyst_cluster", facing={(1, 0): "east", (-1, 0): "west", (0, 1): "south", (0, -1): "north"}[(dx, dz)], waterlogged=False)
    return st


def loot(table, entries):
    """entries : (item, min, max, poids, composants|None)"""
    pool = {"rolls": {"type": "minecraft:uniform", "min": 3, "max": 6}, "entries": []}
    for item, lo, hi, weight, comps in entries:
        mods = [{"type": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": lo, "max": hi}}]
        if comps:
            mods.append({"type": "minecraft:set_components", "components": comps})
        pool["entries"].append({"type": "minecraft:item", "name": item, "weight": weight, "modifier": mods})
    dp_json(f"{N}/loot_table/chests/{table}", {"type": "minecraft:chest", "pools": [pool]})


def gen_all():
    import gen_items
    items = gen_items.item_defs()
    ess = items["essence"]["components"]
    shard = items["ichor_shard"]["components"]
    vial = items["vial"]["components"]
    loot("shrine", [("minecraft:echo_shard", 1, 3, 10, None), ("minecraft:amethyst_shard", 3, 9, 14, None),
                    ("minecraft:stick", 1, 3, 12, ess), ("minecraft:potion", 1, 1, 5, vial),
                    ("minecraft:copper_ingot", 2, 7, 10, None), ("minecraft:glow_berries", 3, 8, 8, None),
                    ("minecraft:diamond", 1, 2, 3, None), ("minecraft:golden_apple", 1, 1, 2, None),
                    ("minecraft:note_block", 1, 2, 6, None), ("minecraft:sculk_sensor", 1, 2, 3, None)])
    loot("outpost", [("minecraft:arrow", 6, 18, 12, None), ("minecraft:bone", 3, 9, 10, None),
                     ("minecraft:stick", 1, 3, 12, shard), ("minecraft:echo_shard", 1, 2, 6, None),
                     ("minecraft:iron_ingot", 2, 6, 10, None), ("minecraft:gold_ingot", 1, 4, 6, None),
                     ("minecraft:crossbow", 1, 1, 2, None), ("minecraft:stick", 1, 2, 8, ess)])
    loot("obelisk", [("minecraft:stick", 1, 4, 14, ess), ("minecraft:potion", 1, 2, 8, vial),
                     ("minecraft:lapis_lazuli", 3, 9, 10, None), ("minecraft:sea_lantern", 1, 2, 4, None)])

    for name, builder, biomes, step, salt, spacing, sep, start_y in (
            ("singer_shrine", shrine, [f"{N}:singers_meadow"], "surface_structures", 71940116, 22, 8, 0),
            ("sentinel_outpost", outpost, [f"{N}:carapace", f"{N}:resonant_crags"], "surface_structures", 71940117, 26, 10, 0),
            ("ichor_obelisk", obelisk, [f"{N}:ichor_fens"], "surface_structures", 71940118, 20, 8, -1)):
        st = builder()
        dp_bytes(f"{N}/structure/{name}.nbt", st.to_bytes())
        dp_json(f"{N}/worldgen/template_pool/{name}", {
            "elements": [{"element": {"element_type": "minecraft:legacy_single_pool_element", "location": f"{N}:{name}",
                                      "processors": {"processors": []}, "projection": "rigid"}, "weight": 1}],
            "fallback": "minecraft:empty"})
        dp_json(f"{N}/worldgen/structure/{name}", {
            "type": "minecraft:jigsaw", "biomes": biomes, "max_distance_from_center": 80,
            "project_start_to_heightmap": "WORLD_SURFACE_WG", "size": 1, "spawn_overrides": {},
            "start_height": {"absolute": start_y}, "start_pool": f"{N}:{name}", "step": step,
            "terrain_adaptation": "beard_thin", "use_expansion_hack": False})
        dp_json(f"{N}/worldgen/structure_set/{name}", {
            "placement": {"type": "minecraft:random_spread", "salt": salt, "separation": sep, "spacing": spacing},
            "structures": [{"structure": f"{N}:{name}", "weight": 1}]})
