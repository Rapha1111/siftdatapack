"""Créatures du Sift : entités de base invisibles + modèle 3D (item_display) synchronisé, spawn, capacités, butins."""
import json

from lib import dp_json, fn, NS

N = NS

# id : (nom FR, entité de base, hostile, vie, vitesse(%), dégâts, échelle hitbox, échelle modèle, silencieux, nom lang)
MOBS = {
    "blub":             dict(name="Blub", base="minecraft:rabbit", hostile=False, hp=8, scale=1.0, mscale=1.35, silent=True),
    "singer":           dict(name="Chanteur", base="minecraft:cow", hostile=False, hp=40, scale=1.5, mscale=1.5, silent=True),
    "licker":           dict(name="Lécheur", base="minecraft:cow", hostile=False, hp=22, scale=1.25, mscale=1.25, silent=True),
    "sprout":           dict(name="Pousse", base="minecraft:allay", hostile=False, hp=14, scale=1.3, mscale=1.2, silent=False),
    "echo_golem":       dict(name="Golem d'écho", base="minecraft:iron_golem", hostile=False, hp=80, scale=0.95, mscale=1.35, silent=False),
    "seedling":         dict(name="Plantule", base="minecraft:endermite", hostile=True, hp=10, scale=1.8, mscale=1.1, silent=False),
    "sculk_slasher":    dict(name="Lacérateur de sculk", base="minecraft:endermite", hostile=True, hp=34, scale=3.2, mscale=1.25, silent=False),
    "nester":           dict(name="Nicheur", base="minecraft:husk", hostile=True, hp=30, scale=1.0, mscale=1.2, silent=False),
    "crested_sentinel": dict(name="Sentinelle à crête", base="minecraft:skeleton", hostile=True, hp=24, scale=1.0, mscale=1.2, silent=False),
    "groobler":         dict(name="Sentinelle Groobler", base="minecraft:vindicator", hostile=True, hp=60, scale=1.15, mscale=1.35, silent=False),
    "sculk_mage":       dict(name="Mage de sculk", base="minecraft:witch", hostile=True, hp=32, scale=1.0, mscale=1.2, silent=False),
}

ATTACK = {"seedling": 3, "sculk_slasher": 5, "nester": 4, "groobler": 8}
SPEED = {"sculk_slasher": 0.38, "seedling": 0.34, "nester": 0.30, "blub": 0.3}


def snbt_str(s):
    return json.dumps(s, ensure_ascii=False)


def summon_lines(mid, spec, extra_tags=(), extra_nbt=""):
    tags = ["sift.mob", "sift.native", f"sift.{mid}", "sift.fresh"] + list(extra_tags)
    tag_s = ",".join(snbt_str(t) for t in tags)
    attrs = [f"{{id:\"minecraft:max_health\",base:{spec['hp']}}}", f"{{id:\"minecraft:scale\",base:{spec['scale']}}}"]
    if mid in SPEED:
        attrs.append(f"{{id:\"minecraft:movement_speed\",base:{SPEED[mid]}}}")
    if mid in ATTACK:
        attrs.append(f"{{id:\"minecraft:attack_damage\",base:{ATTACK[mid]}}}")
    nbt = (f"{{Tags:[{tag_s}],Health:{spec['hp']}f,attributes:[{','.join(attrs)}],"
           f"CustomName:{{text:{snbt_str(spec['name'])},color:\"light_purple\"}},"
           f"active_effects:[{{id:\"minecraft:invisibility\",amplifier:0,duration:-1,show_particles:0b,show_icon:0b}}],"
           f"DeathLootTable:\"{N}:entities/{mid}\""
           + (",Silent:1b" if spec["silent"] else "") + extra_nbt + "}")
    disp = (f"{{Tags:[\"sift.model\",\"sift.model.{mid}\",\"sift.fresh\"],item_display:\"none\",teleport_duration:2,view_range:3.0f,"
            f"brightness:{{sky:13,block:9}},"
            f"item:{{id:\"minecraft:stick\",count:1,components:{{\"minecraft:item_model\":\"{N}:mob/{mid}\"}}}},"
            f"transformation:{{translation:[0f,{0.5 * spec['mscale']:.3f}f,0f],left_rotation:[0f,1f,0f,0f],right_rotation:[0f,0f,0f,1f],"
            f"scale:[{spec['mscale']}f,{spec['mscale']}f,{spec['mscale']}f]}}}}")
    return [
        "scoreboard players add #next sift.id 1",
        f"summon {spec['base']} ~ ~ ~ {nbt}",
        f"summon minecraft:item_display ~ ~ ~ {disp}",
        "scoreboard players operation @e[tag=sift.fresh,distance=..2] sift.id = #next sift.id",
        "scoreboard players set @e[tag=sift.fresh,distance=..2] sift.age 0",
    ]


def gen_all():
    for mid, spec in MOBS.items():
        lines = summon_lines(mid, spec)
        if mid == "echo_golem":
            lines = summon_lines(mid, spec, extra_tags=("sift.ally",), extra_nbt=",PlayerCreated:1b")
        lines.append("execute as @e[tag=sift.fresh,distance=..2] run function sift:mob/finish_fresh")
        fn(f"mob/summon/{mid}", lines)
    fn("mob/finish_fresh", ["tag @s remove sift.fresh"])
    fn("mob/summon_ally", [f"function {N}:mob/summon/echo_golem",
                           "scoreboard players set @e[tag=sift.ally,distance=..3] sift.age 0"])

    # ------------------------------------------------------------------ boucle tick : synchronisation modèles
    fn("mob/tick", [
        f"execute as @e[type=!minecraft:item_display,tag=sift.mob] at @s run function {N}:mob/sync",
        # nettoyage des modèles orphelins
        f"execute as @e[type=minecraft:item_display,tag=sift.model] at @s unless entity @e[type=!minecraft:item_display,tag=sift.mob,distance=..6] run function {N}:mob/orphan",
        "scoreboard players add @e[type=minecraft:item_display,tag=sift.afterimage] sift.age 1",
        "kill @e[type=minecraft:item_display,tag=sift.afterimage,scores={sift.age=7..}]",
    ])
    fn("mob/sync", [
        "scoreboard players operation #cur sift.id = @s sift.id",
        f"execute as @e[type=minecraft:item_display,tag=sift.model,distance=..5] if score @s sift.id = #cur sift.id run tp @s ~ ~ ~ ~ ~",
    ])
    fn("mob/orphan", [
        "particle minecraft:sculk_soul ~ ~0.6 ~ 0.3 0.4 0.3 0.04 12",
        "kill @s",
    ])

    # ------------------------------------------------------------------ boucle seconde : capacités
    fn("mob/second", [
        f"execute as @e[tag=sift.singer] at @s run function {N}:mob/abilities/singer",
        f"execute as @e[tag=sift.blub] at @s if predicate {N}:chance/ambient run function {N}:mob/abilities/blub",
        f"execute as @e[tag=sift.licker] at @s if predicate {N}:chance/ambient run function {N}:mob/abilities/licker",
        f"execute as @e[tag=sift.sprout] at @s run function {N}:mob/abilities/sprout",
        f"execute as @e[tag=sift.nester] at @s run function {N}:mob/abilities/nester",
        f"execute as @e[tag=sift.sculk_slasher] at @s run function {N}:mob/abilities/slasher",
        f"execute as @e[tag=sift.sculk_mage] at @s if predicate {N}:chance/ambient run function {N}:mob/abilities/mage",
        f"execute as @e[tag=sift.ally] at @s run function {N}:mob/abilities/ally",
        f"execute as @e[tag=sift.groobler] at @s run function {N}:mob/abilities/groobler",
    ])
    dp_json(f"{N}/predicate/chance/ambient", {"type": "minecraft:random_chance", "chance": 0.12})
    dp_json(f"{N}/predicate/chance/sing", {"type": "minecraft:random_chance", "chance": 0.35})

    fn("mob/abilities/singer", [
        # le Chanteur chante : notes aléatoires, pacifie les alentours (effets doux sur les joueurs)
        f"execute if predicate {N}:chance/sing run function {N}:mob/abilities/singer_note",
        "effect give @a[distance=..8] minecraft:regeneration 3 0 true",
        f"advancement grant @a[distance=..8] only {N}:sift/hear_singer",
    ])
    fn("mob/abilities/singer_note", [
        "execute store result score #r sift.tmp run random value 0..4",
        "execute if score #r sift.tmp matches 0 run playsound minecraft:block.note_block.chime neutral @a ~ ~1 ~ 2 0.7",
        "execute if score #r sift.tmp matches 1 run playsound minecraft:block.note_block.chime neutral @a ~ ~1 ~ 2 0.84",
        "execute if score #r sift.tmp matches 2 run playsound minecraft:block.note_block.chime neutral @a ~ ~1 ~ 2 1.05",
        "execute if score #r sift.tmp matches 3 run playsound minecraft:block.note_block.bell neutral @a ~ ~1 ~ 2 0.7",
        "execute if score #r sift.tmp matches 4 run playsound minecraft:block.note_block.bell neutral @a ~ ~1 ~ 2 1.26",
        "particle minecraft:note ~ ~3.2 ~ 0.6 0.4 0.6 1 3",
        "particle minecraft:sculk_soul ~ ~2.4 ~ 0.4 0.8 0.4 0.02 4",
    ])
    fn("mob/abilities/blub", [
        "playsound minecraft:entity.allay.ambient_without_item neutral @a ~ ~ ~ 0.8 1.9",
        "particle minecraft:glow ~ ~1 ~ 0.2 0.2 0.2 0.02 3",
    ])
    fn("mob/abilities/licker", [
        "playsound minecraft:entity.sniffer.scenting neutral @a ~ ~ ~ 0.9 1.2",
        "particle minecraft:happy_villager ~ ~0.6 ~ 0.5 0.3 0.5 0 2",
    ])
    fn("mob/abilities/sprout", [
        # soutien : régénère joueurs et alliés proches
        "effect give @a[distance=..6] minecraft:regeneration 3 0 true",
        f"effect give @e[tag=sift.native,tag=!sift.sprout,type=!minecraft:item_display,distance=..6] minecraft:regeneration 3 0 true",
        "particle minecraft:happy_villager ~ ~0.8 ~ 0.6 0.5 0.6 0 3",
    ])
    fn("mob/abilities/nester", [
        # lancer : après un temps de recharge, bond fulgurant vers un joueur proche
        "scoreboard players add @s sift.cool 1",
        f"execute if score @s sift.cool matches 6.. if entity @a[gamemode=!creative,gamemode=!spectator,distance=2..10] run function {N}:mob/abilities/nester_lunge",
    ])
    fn("mob/abilities/nester_lunge", [
        "scoreboard players set @s sift.cool 0",
        "effect give @s minecraft:speed 1 5 true",
        "effect give @s minecraft:jump_boost 1 2 true",
        "particle minecraft:poof ~ ~0.3 ~ 0.3 0.1 0.3 0.05 8",
        "playsound minecraft:entity.silverfish.ambient hostile @a ~ ~ ~ 1 0.5",
    ])
    fn("mob/abilities/slasher", [
        "scoreboard players add @s sift.cool 1",
        f"execute if score @s sift.cool matches 5.. if entity @a[gamemode=!creative,gamemode=!spectator,distance=3..11] run function {N}:mob/abilities/slasher_dash",
    ])
    fn("mob/abilities/slasher_dash", [
        # ruée avec images rémanentes
        "scoreboard players set @s sift.cool 0",
        "effect give @s minecraft:speed 1 6 true",
        "playsound minecraft:entity.warden.sniff hostile @a ~ ~ ~ 1.5 1.8",
        "particle minecraft:sculk_charge_pop ~ ~0.5 ~ 0.4 0.3 0.4 0.05 10",
        f"function {N}:mob/afterimage",
        "schedule function sift:mob/afterimage_2 3t",
        "schedule function sift:mob/afterimage_3 6t",
    ])
    # images rémanentes : copies fantômes du modèle, brièvement visibles
    after = (f"summon minecraft:item_display ~ ~ ~ {{Tags:[\"sift.afterimage\"],item_display:\"none\",view_range:2.0f,"
             f"brightness:{{sky:15,block:15}},item:{{id:\"minecraft:stick\",count:1,components:{{\"minecraft:item_model\":\"{N}:mob/sculk_slasher\"}}}},"
             f"transformation:{{translation:[0f,0.625f,0f],left_rotation:[0f,1f,0f,0f],right_rotation:[0f,0f,0f,1f],scale:[1.25f,1.25f,1.25f]}}}}")
    fn("mob/afterimage", [f"execute as @e[tag=sift.sculk_slasher] at @s run {after}",
                          "execute as @e[type=minecraft:item_display,tag=sift.afterimage,tag=!sift.set] at @s run function sift:mob/afterimage_init"])
    fn("mob/afterimage_2", [f"execute as @e[tag=sift.sculk_slasher] at @s run {after}",
                            "execute as @e[type=minecraft:item_display,tag=sift.afterimage,tag=!sift.set] at @s run function sift:mob/afterimage_init"])
    fn("mob/afterimage_3", [f"execute as @e[tag=sift.sculk_slasher] at @s run {after}",
                            "execute as @e[type=minecraft:item_display,tag=sift.afterimage,tag=!sift.set] at @s run function sift:mob/afterimage_init"])
    fn("mob/afterimage_init", [
        "tag @s add sift.set",
        "scoreboard players set @s sift.age 0",
        "data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{translation:[0f,0.2f,0f],left_rotation:[0f,1f,0f,0f],right_rotation:[0f,0f,0f,1f],scale:[0.05f,0.05f,0.05f]}}",
    ])
    fn("mob/abilities/mage", [
        "particle minecraft:sculk_charge_pop ~ ~1.8 ~ 0.5 0.6 0.5 0.05 6",
        "playsound minecraft:block.sculk_sensor.clicking hostile @a ~ ~ ~ 1 0.8",
    ])
    fn("mob/abilities/groobler", [
        "execute if entity @s[nbt={HurtTime:1s}] run particle minecraft:block{block_state:\"minecraft:moss_block\"} ~ ~1 ~ 0.3 0.5 0.3 0.1 12",
    ])
    fn("mob/abilities/ally", [
        "scoreboard players add @s sift.age 1",
        "particle minecraft:sculk_soul ~ ~1.2 ~ 0.4 0.6 0.4 0.01 2",
        f"execute if score @s sift.age matches 300.. run function {N}:mob/ally_fade",
    ])
    fn("mob/ally_fade", [
        "particle minecraft:poof ~ ~1 ~ 0.4 0.8 0.4 0.05 25",
        "particle minecraft:sculk_soul ~ ~1 ~ 0.4 0.8 0.4 0.05 15",
        "playsound minecraft:block.sculk_catalyst.break neutral @a ~ ~ ~ 1 0.9",
        "kill @s",
    ])

    # ------------------------------------------------------------------ apparition naturelle (par joueur, par biome)
    fn("mob/spawner", [
        "execute store result score @s sift.tmp if entity @e[tag=sift.native,tag=sift.mob,type=!minecraft:item_display,tag=!sift.ally,distance=..48]",
        f"execute if score @s sift.tmp matches ..14 if predicate {N}:chance/spawn_try run function {N}:mob/spawn_roll",
    ])
    fn("mob/spawn_roll", [
        "summon minecraft:marker ~ ~ ~ {Tags:[\"sift.probe\"]}",
        "spreadplayers ~ ~ 14 38 false @e[type=minecraft:marker,tag=sift.probe,distance=..2]",
        f"execute as @e[type=minecraft:marker,tag=sift.probe] at @s run function {N}:mob/spawn_at",
        "kill @e[type=minecraft:marker,tag=sift.probe]",
    ])
    fn("mob/spawn_at", [
        "execute if block ~ ~ ~ minecraft:water run return 0",
        "execute if block ~ ~-1 ~ minecraft:water run return 0",
        "scoreboard players set #h sift.tmp 0",
        f"execute if score #tide sift.tmp matches 0 if predicate {N}:chance/spawn_hostile_calm run scoreboard players set #h sift.tmp 1",
        f"execute if score #tide sift.tmp matches 1 if predicate {N}:chance/spawn_hostile_surge run scoreboard players set #h sift.tmp 1",
        f"execute if score #tide sift.tmp matches 2 if predicate {N}:chance/spawn_hostile_ebb run scoreboard players set #h sift.tmp 1",
        "execute store result score #r sift.tmp run random value 1..100",
        f"execute if biome ~ ~ ~ {N}:singers_meadow run function {N}:mob/pick_meadow",
        f"execute if biome ~ ~ ~ {N}:carapace run function {N}:mob/pick_carapace",
        f"execute if biome ~ ~ ~ {N}:ichor_fens run function {N}:mob/pick_fens",
        f"execute if biome ~ ~ ~ {N}:resonant_crags run function {N}:mob/pick_crags",
        # apparition : léger flash
        "particle minecraft:sculk_soul ~ ~0.5 ~ 0.3 0.5 0.3 0.03 8",
    ])

    def pick(name, passive, hostile):
        lines = []
        for h, table in ((0, passive), (1, hostile)):
            acc = 0
            for mid, w in table:
                lines.append(f"execute if score #h sift.tmp matches {h} if score #r sift.tmp matches {acc + 1}..{acc + w} run function {N}:mob/summon/{mid}")
                acc += w
            assert acc == 100, (name, h, acc)
        fn(f"mob/pick_{name}", lines)

    pick("meadow", [("blub", 40), ("licker", 25), ("sprout", 23), ("singer", 12)],
         [("seedling", 40), ("sculk_slasher", 20), ("nester", 25), ("crested_sentinel", 15)])
    pick("carapace", [("licker", 50), ("blub", 20), ("sprout", 30)],
         [("sculk_slasher", 30), ("nester", 30), ("groobler", 20), ("seedling", 20)])
    pick("fens", [("sprout", 40), ("blub", 30), ("singer", 10), ("licker", 20)],
         [("sculk_mage", 30), ("sculk_slasher", 25), ("seedling", 25), ("crested_sentinel", 20)])
    pick("crags", [("blub", 40), ("sprout", 60)],
         [("sculk_slasher", 30), ("crested_sentinel", 30), ("groobler", 20), ("sculk_mage", 20)])

    gen_loot()
    gen_kill_reward()


def item_entry(item, count, comps=None, chance=None, looting=False):
    e = {"type": "minecraft:item", "name": item}
    mods = [{"type": "minecraft:set_count", "count": count}]
    if comps:
        mods.append({"type": "minecraft:set_components", "components": comps})
    if looting:
        mods.append({"type": "minecraft:enchanted_count_increase", "count": {"type": "minecraft:uniform", "min": 0, "max": 1},
                     "enchantment": "minecraft:looting"})
    e["modifier"] = mods
    return e


def gen_loot():
    essence = {"minecraft:item_model": f"{N}:soul_essence", "minecraft:custom_data": {"sift": "essence"},
               "minecraft:item_name": {"translate": "item.sift.soul_essence", "fallback": "Essence d'âme"}}
    vial_shard = {"minecraft:item_model": f"{N}:ichor_shard", "minecraft:custom_data": {"sift": "ichor_shard"},
                  "minecraft:item_name": {"translate": "item.sift.ichor_shard", "fallback": "Éclat d'ichor"}}
    table = {
        "blub": [("minecraft:rabbit_hide", {"type": "minecraft:uniform", "min": 0, "max": 2}, None), ("minecraft:glow_berries", {"type": "minecraft:uniform", "min": 0, "max": 2}, None)],
        "singer": [("minecraft:echo_shard", {"type": "minecraft:uniform", "min": 0, "max": 1}, None), ("minecraft:amethyst_shard", {"type": "minecraft:uniform", "min": 2, "max": 5}, None)],
        "licker": [("minecraft:torchflower_seeds", {"type": "minecraft:uniform", "min": 1, "max": 2}, None), ("minecraft:slime_ball", {"type": "minecraft:uniform", "min": 0, "max": 2}, None)],
        "sprout": [("minecraft:glow_ink_sac", {"type": "minecraft:uniform", "min": 0, "max": 2}, None), ("minecraft:bone_meal", {"type": "minecraft:uniform", "min": 1, "max": 3}, None)],
        "echo_golem": [("minecraft:copper_ingot", {"type": "minecraft:uniform", "min": 1, "max": 3}, None), ("minecraft:red_sandstone", {"type": "minecraft:uniform", "min": 1, "max": 4}, None)],
        "seedling": [("minecraft:wheat_seeds", {"type": "minecraft:uniform", "min": 1, "max": 3}, None)],
        "sculk_slasher": [("minecraft:bone", {"type": "minecraft:uniform", "min": 0, "max": 2}, None), ("minecraft:string", {"type": "minecraft:uniform", "min": 0, "max": 2}, None)],
        "nester": [("minecraft:honeycomb", {"type": "minecraft:uniform", "min": 0, "max": 2}, None), ("minecraft:spider_eye", {"type": "minecraft:uniform", "min": 0, "max": 1}, None)],
        "crested_sentinel": [("minecraft:arrow", {"type": "minecraft:uniform", "min": 0, "max": 3}, None), ("minecraft:bone", {"type": "minecraft:uniform", "min": 0, "max": 2}, None)],
        "groobler": [("minecraft:moss_block", {"type": "minecraft:uniform", "min": 1, "max": 4}, None), ("minecraft:iron_ingot", {"type": "minecraft:uniform", "min": 0, "max": 2}, None)],
        "sculk_mage": [("minecraft:amethyst_shard", {"type": "minecraft:uniform", "min": 1, "max": 3}, None), ("minecraft:glowstone_dust", {"type": "minecraft:uniform", "min": 0, "max": 3}, None)],
    }
    for mid, entries in table.items():
        pools = [{"rolls": 1, "entries": [item_entry(i, c, comps, looting=True)]} for i, c, comps in entries]
        # essence d'âme : chance de base, plus pour les hostiles
        chance = 0.5 if MOBS[mid]["hostile"] else 0.25
        pools.append({"rolls": 1, "condition": {"type": "minecraft:random_chance", "chance": chance},
                      "entries": [item_entry("minecraft:stick", 1, essence)]})
        if MOBS[mid]["hostile"]:
            pools.append({"rolls": 1, "condition": {"type": "minecraft:random_chance", "chance": 0.2},
                          "entries": [item_entry("minecraft:stick", 1, vial_shard)]})
        dp_json(f"{N}/loot_table/entities/{mid}", {"type": "minecraft:entity", "pools": pools})


def gen_kill_reward():
    # tuer une créature native rapporte des âmes (advancement répétable)
    dp_json(f"{N}/advancement/kill/native", {
        "criteria": {"kill": {"trigger": "minecraft:player_killed_entity", "conditions": {
            "entity": {"type": "minecraft:entity_properties", "entity": "this", "predicate": {"minecraft:entity_tags": {"any_of": ["sift.native"]}}}}}},
        "rewards": {"function": f"{N}:mob/kill_reward"},
    })
    fn("mob/kill_reward", [
        f"advancement revoke @s only {N}:kill/native",
        f"execute unless dimension {N}:the_sift run return 0",
        "scoreboard players add @s sift.souls 8",
        "particle minecraft:sculk_soul ~ ~1 ~ 0.4 0.6 0.4 0.05 14",
        f"execute if score @s sift.souls matches 100.. run function {N}:souls/overflow",
    ])
