"""Features (configured + placed) du Sift : végétation, minerais, cristaux, ossements, ichor..."""
from lib import dp_json, NS, state

AIR = {"type": "minecraft:matching_block_tag", "tag": "minecraft:air"}


def feat(name, config):
    dp_json(f"{NS}/worldgen/feature/{name}", config)


def placed(name, feature, placement):
    dp_json(f"{NS}/worldgen/placed_feature/{name}", {"feature": feature, "placement": placement})


# ---- modificateurs de placement ------------------------------------------
def count(n): return {"type": "minecraft:count", "count": n}
def rarity(n): return {"type": "minecraft:rarity_filter", "chance": n}
IN_SQUARE = {"type": "minecraft:in_square"}
BIOME = {"type": "minecraft:biome"}
def heightmap(h): return {"type": "minecraft:heightmap", "heightmap": h}
def pred(p): return {"type": "minecraft:block_predicate_filter", "predicate": p}
def trap(a): return {"type": "minecraft:trapezoid", "max": a, "min": -a, "plateau": 0}


def spread(xz, y):
    return {"type": "minecraft:offset", "x": trap(xz), "y": trap(y), "z": trap(xz)}


def uniform(lo, hi):
    return {"type": "minecraft:uniform", "min_inclusive": lo, "max_inclusive": hi}


def hrange(lo, hi, kind="uniform"):
    return {"type": "minecraft:height_range",
            "height": {"type": f"minecraft:{kind}", "min_inclusive": lo, "max_inclusive": hi}}


def absolute(y): return {"absolute": y}
def above_bottom(y): return {"above_bottom": y}


def patch(placed_name, feature, patches, tries, xz=7, y=3, hm="WORLD_SURFACE_WG", extra=None, predicate=AIR, rare=None):
    pl = []
    if rare:
        pl.append(rarity(rare))
    pl += [count(patches), IN_SQUARE, heightmap(hm), BIOME, count(tries), spread(xz, y), pred(predicate)]
    if extra:
        pl = extra + pl
    placed(placed_name, feature, pl)


def weighted_state(entries):
    return {"type": "minecraft:weighted",
            "entries": [{"data": e, "weight": w} for e, w in entries]}


def simple_block(name, block_state):
    feat(name, {"type": "minecraft:simple_block", "to_place": block_state})


def ore(name, size, target_states, discard=0.0):
    feat(name, {
        "type": "minecraft:ore",
        "discard_chance_on_air_exposure": discard,
        "size": size,
        "targets": [{"state": st, "target": {"predicate_type": "minecraft:tag_match", "tag": f"{NS}:ore_replaceables"}}
                    for st in target_states],
    })


def gen_all():
    # ------------------------------------------------------------------ arbres bleus
    def tree(name, trunk_placer, foliage_placer, size, decorators, trunk="minecraft:warped_stem"):
        feat(name, {
            "type": "minecraft:tree",
            "below_trunk_provider": "minecraft:soil_beneath_tree",
            "decorators": decorators,
            "foliage_placer": foliage_placer,
            "foliage_provider": state("oak_leaves", distance=7, persistent=False, waterlogged=False),
            "ignore_vines": True,
            "minimum_size": size,
            "trunk_placer": trunk_placer,
            "trunk_provider": state(trunk, axis="y"),
        })

    vines = [{"type": "minecraft:trunk_vine"}, {"type": "minecraft:leave_vine", "probability": 0.3}]
    tree("blue_tree",
         {"type": "minecraft:straight_trunk_placer", "base_height": 5, "height_rand_a": 3, "height_rand_b": 1},
         {"type": "minecraft:blob_foliage_placer", "height": 3, "offset": 0, "radius": 3},
         {"type": "minecraft:two_layers_feature_size"}, vines)
    tree("blue_tree_tall",
         {"type": "minecraft:fancy_trunk_placer", "base_height": 5, "height_rand_a": 11, "height_rand_b": 0},
         {"type": "minecraft:fancy_foliage_placer", "height": 4, "offset": 4, "radius": 3},
         {"type": "minecraft:two_layers_feature_size", "limit": 0, "min_clipped_height": 4, "upper_size": 0}, vines)
    feat("trees_meadow", {
        "type": "minecraft:random_selector",
        "default": {"feature": f"{NS}:blue_tree", "placement": []},
        "features": [{"chance": 0.3, "feature": {"feature": f"{NS}:blue_tree_tall", "placement": []}}],
    })
    survive = pred({"type": "minecraft:would_survive", "state": "minecraft:oak_sapling"})
    tree_pl = lambda weights: [
        {"type": "minecraft:count", "count": {"type": "minecraft:weighted_list",
                                              "distribution": [{"data": d, "weight": w} for d, w in weights]}},
        IN_SQUARE, {"type": "minecraft:surface_water_depth_filter", "max_water_depth": 0},
        heightmap("OCEAN_FLOOR"), survive, BIOME]
    placed("trees_meadow", f"{NS}:trees_meadow", tree_pl([(0, 10), (1, 6), (2, 3), (3, 1)]))
    placed("fen_trees", f"{NS}:trees_meadow", tree_pl([(0, 14), (1, 4), (2, 1)]))

    # ------------------------------------------------------------------ herbes & fleurs
    patch("tall_blue_grass", "minecraft:tall_grass", 2, 80, extra=None, hm="MOTION_BLOCKING", rare=2)
    patch("blue_grass", "minecraft:grass", 6, 40)
    patch("blue_grass_sparse", "minecraft:grass", 1, 20)
    patch("grass_fen", "minecraft:grass", 3, 30)
    simple_block("flowers_meadow", {"type": "minecraft:weighted", "entries": [
        {"data": "minecraft:cornflower", "weight": 3}, {"data": "minecraft:blue_orchid", "weight": 3},
        {"data": "minecraft:azure_bluet", "weight": 2}, {"data": "minecraft:dandelion", "weight": 2},
        {"data": "minecraft:torchflower", "weight": 1}, {"data": "minecraft:allium", "weight": 1}]})
    patch("flowers_meadow", f"{NS}:flowers_meadow", 1, 32, xz=6, y=2, hm="MOTION_BLOCKING", rare=3)
    patch("wildflowers_meadow", "minecraft:wildflower", 1, 24, xz=6, y=2, hm="MOTION_BLOCKING", rare=4)
    simple_block("bloom_orbs", state("lilac", half="lower"))
    patch("bloom_orbs", f"{NS}:bloom_orbs", 1, 14, xz=5, y=2, hm="MOTION_BLOCKING", rare=5)

    # ------------------------------------------------------------------ sculk
    feat("sculk_carpet", {"type": "minecraft:sculk_patch", "amount_per_charge": 28, "charge_count": 8,
                          "growth_rounds": 0, "spread_attempts": 64, "spread_rounds": 1})
    placed("sculk_carpet", f"{NS}:sculk_carpet", [rarity(4), IN_SQUARE, heightmap("WORLD_SURFACE_WG"), BIOME])
    placed("fen_sculk", f"{NS}:sculk_carpet", [rarity(3), IN_SQUARE, heightmap("WORLD_SURFACE_WG"), BIOME])
    feat("sculk_cavern_patch", {"type": "minecraft:sequence", "features": [
        {"feature": {"type": "minecraft:sculk_patch", "amount_per_charge": 32, "charge_count": 10,
                     "growth_rounds": 0, "spread_attempts": 64, "spread_rounds": 1}, "placement": []},
        {"feature": {"type": "minecraft:simple_block", "to_place": state("sculk_catalyst", bloom=False)},
         "placement": [{"type": "minecraft:random_chance", "chance": 0.5},
                       pred({"type": "minecraft:has_sturdy_face", "direction": "up", "offset": [0, -1, 0]})]}]})
    placed("sculk_cavern_patch", f"{NS}:sculk_cavern_patch", [count(160), IN_SQUARE, hrange(above_bottom(0), absolute(90)), BIOME])
    simple_block("sculk_sensor", state("sculk_sensor"))
    placed("sculk_sensors", f"{NS}:sculk_sensor", [
        count(90), IN_SQUARE, hrange(above_bottom(0), absolute(90)),
        {"type": "minecraft:environment_scan", "allowed_search_condition": AIR, "direction_of_search": "down",
         "max_steps": 12, "target_condition": {"type": "minecraft:solid"}},
        {"type": "minecraft:random_chance", "chance": 0.6},
        pred({"type": "minecraft:all_of", "predicates": [AIR, {"type": "minecraft:would_survive", "state": "minecraft:sculk_sensor"}]}),
        BIOME])
    terrain = ["minecraft:terracotta", "minecraft:red_terracotta", "minecraft:orange_terracotta",
               "minecraft:yellow_terracotta", "minecraft:white_terracotta", "minecraft:brown_terracotta",
               "minecraft:blue_terracotta", "minecraft:cyan_terracotta", "minecraft:red_sandstone",
               "minecraft:deepslate", "minecraft:calcite", "minecraft:smooth_red_sandstone"]
    feat("sculk_vein", {"type": "minecraft:multiface_growth", "block": "minecraft:sculk_vein",
                        "can_be_placed_on": terrain, "can_place_on_ceiling": True, "can_place_on_floor": True,
                        "can_place_on_wall": True, "chance_of_spreading": 1.0, "search_range": 20})
    placed("sculk_vein_cave", f"{NS}:sculk_vein", [count(uniform(60, 110)), IN_SQUARE, hrange(above_bottom(0), absolute(100)), BIOME])
    placed("sculk_vein_crags", f"{NS}:sculk_vein", [count(uniform(10, 24)), IN_SQUARE, hrange(absolute(60), absolute(140)), BIOME])

    # ------------------------------------------------------------------ ichor
    for name, rare in (("ichor_pool", 7), ("ichor_pool_rare", 22)):
        placed(name, f"{NS}:ichor_pool", [rarity(rare), IN_SQUARE, heightmap("WORLD_SURFACE_WG"), BIOME])
    not_protected = {"type": "minecraft:not", "predicate": {"type": "minecraft:matching_block_tag", "tag": "minecraft:features_cannot_replace"}}
    feat("ichor_pool", {"type": "minecraft:lake", "barrier": state("red_terracotta"),
                        "can_place_feature": {"type": "minecraft:true"},
                        "can_replace_with_air_or_fluid": not_protected,
                        "can_replace_with_barrier": not_protected,
                        "fluid": state("water", level=0)})
    feat("ichor_spring", {"type": "minecraft:spring_feature", "state": state("water", falling=True),
                          "valid_blocks": terrain})
    placed("ichor_spring", f"{NS}:ichor_spring", [count(20), IN_SQUARE, hrange(above_bottom(0), absolute(120)), BIOME])

    # ------------------------------------------------------------------ Carapace : os & ossements
    feat("bone_spire", {"type": "minecraft:block_column", "allowed_placement": AIR, "direction": "up",
                        "layers": [{"height": {"type": "minecraft:biased_to_bottom", "min_inclusive": 3, "max_inclusive": 11},
                                    "provider": state("bone_block", axis="y")}],
                        "prioritize_tip": False})
    placed("bone_spires", f"{NS}:bone_spire", [
        rarity(3), IN_SQUARE, heightmap("WORLD_SURFACE_WG"), BIOME, count(2), spread(7, 2),
        pred({"type": "minecraft:all_of", "predicates": [AIR, {"type": "minecraft:matching_blocks", "blocks": "minecraft:sand", "offset": [0, -1, 0]}]})])
    # côtes géantes : arches d'os
    feat("bone_rib", {"type": "minecraft:block_column", "allowed_placement": AIR, "direction": "up",
                      "layers": [{"height": {"type": "minecraft:uniform", "min_inclusive": 5, "max_inclusive": 9},
                                  "provider": state("bone_block", axis="y")},
                                 {"height": 1, "provider": state("bone_block", axis="x")},
                                 {"height": 1, "provider": state("bone_block", axis="z")}],
                      "prioritize_tip": True})
    placed("bone_ribs", f"{NS}:bone_rib", [
        count({"type": "minecraft:uniform", "min_inclusive": 2, "max_inclusive": 4}), rarity(5), IN_SQUARE,
        heightmap("WORLD_SURFACE_WG"), BIOME, spread(3, 1), pred(AIR)])
    feat("amber_grass_disk", {"type": "minecraft:disk", "half_height": 1,
                              "radius": {"type": "minecraft:uniform", "min_inclusive": 2, "max_inclusive": 5},
                              "state_provider": {"type": "minecraft:simple", "state": state("grass_block")},
                              "target": {"type": "minecraft:matching_blocks", "blocks": "minecraft:sand"}})
    placed("amber_grass_disk", f"{NS}:amber_grass_disk", [rarity(2), IN_SQUARE, heightmap("OCEAN_FLOOR_WG"), BIOME])
    patch("amber_grass", "minecraft:grass", 3, 30,
          predicate={"type": "minecraft:all_of", "predicates": [AIR, {"type": "minecraft:would_survive", "state": "minecraft:short_grass"}]})
    patch("dry_scrub", "minecraft:dead_bush", 1, 4)
    placed("carapace_cactus", "minecraft:cactus", [count(4), IN_SQUARE, heightmap("WORLD_SURFACE_WG"), BIOME, spread(7, 3),
                                                   pred({"type": "minecraft:all_of", "predicates": [AIR, {"type": "minecraft:would_survive", "state": "minecraft:cactus"}]})])
    patch("amber_wildflowers", "minecraft:wildflower", 1, 20, xz=6, y=2, hm="MOTION_BLOCKING", rare=6,
          predicate={"type": "minecraft:all_of", "predicates": [AIR, {"type": "minecraft:would_survive", "state": "minecraft:dandelion"}]})

    # ------------------------------------------------------------------ Marais d'ichor
    fl = [{"type": "minecraft:in_square"}]
    placed("fen_kelp", "minecraft:kelp", [count(8), IN_SQUARE, heightmap("OCEAN_FLOOR_WG"), BIOME,
                                          pred({"type": "minecraft:matching_blocks", "blocks": "minecraft:water"})])
    placed("fen_seagrass", "minecraft:seagrass_tall", [IN_SQUARE, count(24), spread(7, 0), heightmap("OCEAN_FLOOR"),
                                                       pred({"type": "minecraft:matching_blocks", "blocks": "minecraft:water"}), BIOME])
    patch("fen_lilies", "minecraft:waterlily", 4, 10, hm="WORLD_SURFACE_WG")
    # lanternes d'âmes : points lumineux flottants dans le marais
    simple_block("fen_light", state("sea_lantern"))
    feat("fen_light_pillar", {"type": "minecraft:block_column", "allowed_placement": {"type": "minecraft:any_of", "predicates": [AIR, {"type": "minecraft:matching_blocks", "blocks": "minecraft:water"}]},
                              "direction": "up",
                              "layers": [{"height": {"type": "minecraft:uniform", "min_inclusive": 2, "max_inclusive": 4},
                                          "provider": state("mud_bricks")},
                                         {"height": 1, "provider": state("soul_lantern", hanging=False)}],
                              "prioritize_tip": True})
    placed("fen_lights", f"{NS}:fen_light_pillar", [rarity(4), IN_SQUARE, heightmap("OCEAN_FLOOR_WG"), BIOME, pred(
        {"type": "minecraft:matching_blocks", "blocks": ["minecraft:mud", "minecraft:soul_soil", "minecraft:water"]})])

    # ------------------------------------------------------------------ cristaux
    simple_block("crystal_cluster", state("amethyst_cluster", facing="up", waterlogged=False))
    sturdy_below = {"type": "minecraft:has_sturdy_face", "direction": "up", "offset": [0, -1, 0]}
    patch("crag_crystals", f"{NS}:crystal_cluster", 4, 12, xz=6, y=3,
          predicate={"type": "minecraft:all_of", "predicates": [AIR, sturdy_below]})
    placed("crystal_cluster_cave", f"{NS}:crystal_cluster", [
        count(60), IN_SQUARE, hrange(above_bottom(0), absolute(80)),
        {"type": "minecraft:environment_scan", "allowed_search_condition": AIR, "direction_of_search": "down",
         "max_steps": 12, "target_condition": {"type": "minecraft:solid"}},
        {"type": "minecraft:random_chance", "chance": 0.4}, BIOME])
    placed("cavern_crystals", f"{NS}:crystal_cluster", [
        count(120), IN_SQUARE, hrange(above_bottom(0), absolute(90)),
        {"type": "minecraft:environment_scan", "allowed_search_condition": AIR, "direction_of_search": "down",
         "max_steps": 12, "target_condition": {"type": "minecraft:solid"}},
        BIOME])
    placed("cavern_blossoms", "minecraft:spore_blossom", [
        count(35), IN_SQUARE, hrange(above_bottom(0), absolute(100)),
        {"type": "minecraft:environment_scan", "allowed_search_condition": AIR, "direction_of_search": "up",
         "max_steps": 12, "target_condition": {"type": "minecraft:solid"}},
        {"type": "minecraft:offset", "x": 0, "y": -1, "z": 0}, BIOME])
    placed("crag_blossoms", "minecraft:spore_blossom", [
        count(10), IN_SQUARE, hrange(absolute(40), absolute(110)),
        {"type": "minecraft:environment_scan", "allowed_search_condition": AIR, "direction_of_search": "up",
         "max_steps": 12, "target_condition": {"type": "minecraft:solid"}},
        {"type": "minecraft:offset", "x": 0, "y": -1, "z": 0}, BIOME])
    placed("crag_geode", "minecraft:amethyst_geode", [rarity(14), IN_SQUARE, hrange(absolute(-10), absolute(70)), BIOME])
    placed("crag_geode_rare", "minecraft:amethyst_geode", [rarity(40), IN_SQUARE, hrange(absolute(-10), absolute(60)), BIOME])

    # ------------------------------------------------------------------ minerais
    ore("ore_coal", 17, ["minecraft:coal_ore"])
    ore("ore_iron", 9, ["minecraft:iron_ore"])
    ore("ore_copper", 10, ["minecraft:copper_ore"])
    ore("ore_gold", 9, ["minecraft:gold_ore"])
    ore("ore_redstone", 8, ["minecraft:redstone_ore"])
    ore("ore_lapis", 7, ["minecraft:lapis_ore"])
    ore("ore_diamond", 6, ["minecraft:diamond_ore"], discard=0.5)
    ore("ore_emerald", 3, ["minecraft:emerald_ore"])
    feat("ore_soul_soil", {"type": "minecraft:ore", "discard_chance_on_air_exposure": 0.0, "size": 33,
                           "targets": [{"state": "minecraft:soul_soil", "target": {"predicate_type": "minecraft:tag_match", "tag": f"{NS}:ore_replaceables"}}]})
    feat("ore_sculk_blob", {"type": "minecraft:ore", "discard_chance_on_air_exposure": 0.0, "size": 20,
                            "targets": [{"state": "minecraft:sculk", "target": {"predicate_type": "minecraft:tag_match", "tag": f"{NS}:ore_replaceables"}}]})
    feat("ore_amethyst_cluster", {"type": "minecraft:ore", "discard_chance_on_air_exposure": 0.0, "size": 8,
                                  "targets": [{"state": "minecraft:amethyst_block", "target": {"predicate_type": "minecraft:tag_match", "tag": f"{NS}:ore_replaceables"}}]})

    def ore_pl(name, n, lo, hi, kind="uniform"):
        placed(name, f"{NS}:{name}", [count(n), IN_SQUARE, hrange(lo, hi, kind), BIOME])

    ore_pl("ore_coal", 24, absolute(-10), absolute(140))
    ore_pl("ore_iron", 20, absolute(-40), absolute(110), "trapezoid")
    ore_pl("ore_copper", 14, absolute(-20), absolute(100), "trapezoid")
    ore_pl("ore_gold", 8, absolute(-60), absolute(40), "trapezoid")
    ore_pl("ore_redstone", 10, absolute(-64), absolute(20))
    ore_pl("ore_lapis", 6, absolute(-60), absolute(30), "trapezoid")
    ore_pl("ore_diamond", 5, absolute(-64), absolute(10), "trapezoid")
    ore_pl("ore_emerald", 4, absolute(-20), absolute(90))
    ore_pl("ore_soul_soil", 12, absolute(-64), absolute(90))
    ore_pl("ore_sculk_blob", 8, absolute(-64), absolute(70))
    ore_pl("ore_amethyst_cluster", 5, absolute(-30), absolute(80))
