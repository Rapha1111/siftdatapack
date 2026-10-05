"""Mécaniques de jeu : portail (Machine à notes), marées, âmes, ichor, générateur de mobs, commandes admin."""
import json

from lib import dp_json, fn, NS, state

N = NS


def tj(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def text(t, color=None, **kw):
    d = {"text": t}
    if color:
        d["color"] = color
    d.update(kw)
    return d


# ---------------------------------------------------------------------------
# Chargement, tick, constantes
# ---------------------------------------------------------------------------
OBJECTIVES = [
    ("sift.tmp", "dummy"), ("sift.const", "dummy"), ("sift.timer", "dummy"), ("sift.souls", "dummy"),
    ("sift.cd", "dummy"), ("sift.ox", "dummy"), ("sift.oy", "dummy"), ("sift.oz", "dummy"), ("sift.odim", "dummy"),
    ("sift.veil", "dummy"), ("sift.age", "dummy"), ("sift.id", "dummy"), ("sift.cool", "dummy"),
    ("sift.visits", "dummy"), ("sift_exit", "trigger"),
]


def gen_core():
    load = [f"scoreboard objectives add {o} {c}" for o, c in OBJECTIVES]
    for k, v in (("#24000", 24000), ("#8000", 8000), ("#0", 0), ("#100", 100), ("#2", 2), ("#5", 5), ("#10", 10), ("#20", 20)):
        load.append(f"scoreboard players set {k} sift.const {v}")
    load += [
        "scoreboard players set #tide_last sift.tmp -1",
        "time of sift:tides resume",
        "tellraw @a [{\"text\":\"[Sift] \",\"color\":\"light_purple\",\"bold\":true},{\"text\":\"Data pack chargé — le chant des âmes résonne.\",\"color\":\"aqua\",\"bold\":false}]",
    ]
    fn("load", load)
    dp_json("minecraft/tags/function/load", {"values": [f"{N}:load"]})
    dp_json("minecraft/tags/function/tick", {"values": [f"{N}:tick"]})

    fn("tick", [
        "scoreboard players add #tick sift.timer 1",
        "scoreboard players add #p sift.timer 1",
        f"execute as @a at @s if dimension {N}:the_sift run function {N}:player/tick",
        f"execute if entity @e[type=item_display,tag=sift.wisp,limit=1] if score #p sift.timer matches 5.. run function {N}:souls/wisp_fx",
        f"execute if entity @e[type=marker,tag=sift.portal,limit=1] if score #p sift.timer matches 5.. run function {N}:portal/portal_fx",
        f"execute if entity @e[type=marker,tag=sift.portal,limit=1] run function {N}:portal/portal_tick",
        "execute if score #p sift.timer matches 5.. run scoreboard players set #p sift.timer 0",
        f"execute if entity @e[type=!item_display,tag=sift.mob,limit=1] run function {N}:mob/tick",
        f"execute as @a[scores={{sift_exit=1..}}] run function {N}:portal/trigger_exit",
        f"execute if score #tick sift.timer matches 20.. run function {N}:second",
    ])

    fn("second", [
        "scoreboard players set #tick sift.timer 0",
        f"function {N}:tide/update",
        "scoreboard players remove @a[scores={sift.cd=1..}] sift.cd 1",
        "scoreboard players remove @a[scores={sift.veil=1..}] sift.veil 1",
        "scoreboard players add @a sift.cd 0",
        "scoreboard players add @a sift.souls 0",
        f"execute as @a at @s if dimension {N}:the_sift run function {N}:player/second",
        f"execute as @a at @s if dimension {N}:the_sift run function {N}:ichor/second",
        f"execute as @e[type=item_display,tag=sift.wisp] run function {N}:souls/wisp_tick",
        f"execute as @e[type=marker,tag=sift.portal,tag=!sift.portal.exit] run function {N}:portal/expire_tick",
        f"execute if entity @e[type=!item_display,tag=sift.mob,limit=1] run function {N}:mob/second",
        f"scoreboard players enable @a sift_exit",
    ])


# ---------------------------------------------------------------------------
# Marées
# ---------------------------------------------------------------------------
TIDE_INFO = [
    # nom, couleur, sous-titre, effets
    ("Marée Calme", "aqua", "Les âmes retiennent leur souffle : le sol est léger.", "bleue"),
    ("Marée Haute", "light_purple", "Les âmes affluent par vagues : cueillez-les vite !", "violette"),
    ("Marée Basse", "gold", "L'ichor se retire, les âmes se font rares mais denses.", "ambrée"),
]


def gen_tides():
    fn("tide/update", [
        "execute store result score #clock sift.tmp run time of sift:tides query time",
        "scoreboard players operation #clock sift.tmp %= #24000 sift.const",
        "scoreboard players operation #tide sift.tmp = #clock sift.tmp",
        "scoreboard players operation #tide sift.tmp /= #8000 sift.const",
        f"execute unless score #tide sift.tmp = #tide_last sift.tmp run function {N}:tide/changed",
    ])
    fn("tide/changed", [
        "scoreboard players operation #tide_last sift.tmp = #tide sift.tmp",
        f"execute if score #tide sift.tmp matches 0 as @a if dimension {N}:the_sift run function {N}:tide/announce_0",
        f"execute if score #tide sift.tmp matches 1 as @a if dimension {N}:the_sift run function {N}:tide/announce_1",
        f"execute if score #tide sift.tmp matches 2 as @a if dimension {N}:the_sift run function {N}:tide/announce_2",
    ])
    snd = ["minecraft:block.amethyst_block.resonate", "minecraft:block.note_block.chime", "minecraft:block.sculk_catalyst.bloom"]
    pit = [0.6, 1.2, 0.5]
    for i, (name, col, sub, _) in enumerate(TIDE_INFO):
        fn(f"tide/announce_{i}", [
            f"title @s times 10 70 30",
            f"title @s subtitle {tj(text(sub, 'gray', italic=True))}",
            f"title @s title {tj(text(name, col, bold=True))}",
            f"execute at @s run playsound {snd[i]} ambient @s ~ ~ ~ 1.5 {pit[i]}",
            f"advancement grant @s only {N}:sift/three_tides {['calm', 'surge', 'ebb'][i]}",
        ])


# ---------------------------------------------------------------------------
# Joueur dans le Sift
# ---------------------------------------------------------------------------
def gen_player():
    fn("player/tick", [
        # ramassage des âmes (wisps)
        f"execute if entity @e[type=item_display,tag=sift.wisp,distance=..1.8,limit=1] run function {N}:souls/collect",
    ])
    fn("player/second", [
        # effets de marée
        "execute if score #tide sift.tmp matches 0 run effect give @s minecraft:slow_falling 4 0 true",
        "execute if score #tide sift.tmp matches 0 run effect give @s minecraft:jump_boost 4 1 true",
        "execute if score #tide sift.tmp matches 1 run effect give @s minecraft:speed 4 0 true",
        "execute if score #tide sift.tmp matches 2 run effect give @s minecraft:haste 4 0 true",
        # apparition d'âmes
        "execute store result score @s sift.tmp if entity @e[type=item_display,tag=sift.wisp,distance=..32]",
        f"execute if score @s sift.tmp matches ..11 if score #tide sift.tmp matches 0 if predicate {N}:chance/wisp_calm run function {N}:souls/spawn_wisp",
        f"execute if score @s sift.tmp matches ..17 if score #tide sift.tmp matches 1 if predicate {N}:chance/wisp_surge run function {N}:souls/spawn_wisp",
        f"execute if score @s sift.tmp matches ..7 if score #tide sift.tmp matches 2 if predicate {N}:chance/wisp_ebb run function {N}:souls/spawn_wisp",
        # ichor
        f"execute if block ~ ~ ~ minecraft:water unless score @s sift.veil matches 1.. run function {N}:ichor/burn_player",
        # monstres
        f"function {N}:mob/spawner",
        # interface : âmes + marée + voile
        f"function {N}:player/hud",
        f"function {N}:sift/check_mastery",
    ])
    tide_names = [text("Calme", "aqua"), text("Haute", "light_purple"), text("Basse", "gold")]
    # on produit une ligne par marée (le composant dépend de l'index)
    lines = []
    for i, tn in enumerate(tide_names):
        comp = [text("✦ ", "light_purple"), text("Âmes ", "white"),
                {"score": {"name": "@s", "objective": "sift.souls"}, "color": "aqua"}, text("/100", "gray"),
                text("   ≈ Marée ", "dark_aqua"), tn]
        lines.append(f"execute if score #tide sift.tmp matches {i} unless score @s sift.veil matches 1.. run title @s actionbar {tj(comp)}")
        comp_v = comp + [text("   ❖ Voile d'ichor ", "dark_purple"), {"score": {"name": "@s", "objective": "sift.veil"}, "color": "light_purple"}, text("s", "gray")]
        lines.append(f"execute if score #tide sift.tmp matches {i} if score @s sift.veil matches 1.. run title @s actionbar {tj(comp_v)}")
    fn("player/hud", lines)

    # ----------------------------------------------------------------- ichor
    fn("ichor/burn_player", [
        "execute if entity @s[gamemode=!creative,gamemode=!spectator] run damage @s 2 minecraft:magic",
        "particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.02 14",
        "particle minecraft:sculk_soul ~ ~1.2 ~ 0.3 0.4 0.3 0.02 6",
        "scoreboard players remove @s sift.souls 8",
        "scoreboard players operation @s sift.souls > #0 sift.const",
        "playsound minecraft:block.fire.extinguish player @a ~ ~ ~ 0.6 0.6",
        f"title @s actionbar {tj(text('L’ichor brûle votre âme !', 'dark_purple', bold=True))}",
        "effect give @s minecraft:slowness 2 0 true",
    ])
    fn("ichor/burn_mob", [
        "damage @s 2 minecraft:magic",
        "particle minecraft:soul_fire_flame ~ ~0.5 ~ 0.2 0.3 0.2 0.02 8",
    ])
    fn("ichor/second", [
        f"execute as @e[type=!#{N}:ignored,type=!minecraft:player,tag=!sift.native,distance=..48] at @s if block ~ ~ ~ minecraft:water run function {N}:ichor/burn_mob",
    ])
    # ----------------------------------------------------------------- âmes
    fn("souls/spawn_wisp", [
        f"summon item_display ~ ~ ~ {{Tags:[\"sift.wisp\",\"sift.new\"],billboard:\"center\",view_range:2.0f,"
        f"brightness:{{sky:15,block:15}},"
        f"item:{{id:\"minecraft:stick\",count:1,components:{{\"minecraft:item_model\":\"sift:wisp\"}}}},"
        f"transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.7f],translation:[0f,0f,0f]}}}}",
        "spreadplayers ~ ~ 3 20 false @e[type=item_display,tag=sift.new,distance=..2]",
        "execute as @e[type=item_display,tag=sift.new] at @s positioned over motion_blocking run tp @s ~ ~1.4 ~",
        "scoreboard players set @e[type=item_display,tag=sift.new] sift.age 0",
        "tag @e[type=item_display,tag=sift.new] remove sift.new",
    ])
    fn("souls/wisp_tick", [
        "scoreboard players add @s sift.age 1",
        f"execute if score @s sift.age matches 150.. run function {N}:souls/wisp_fade",
        # petit balancement : alterne deux translations avec interpolation
        f"execute if entity @s[tag=sift.up] run function {N}:souls/wisp_down",
        f"execute unless entity @s[tag=sift.up] run function {N}:souls/wisp_up",
    ])
    fn("souls/wisp_up", [
        "tag @s add sift.up",
        "data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{translation:[0f,0.35f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.7f]}}",
    ])
    fn("souls/wisp_down", [
        "tag @s remove sift.up",
        "data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.7f]}}",
    ])
    fn("souls/wisp_fade", [
        "particle minecraft:poof ~ ~0.4 ~ 0.1 0.1 0.1 0.02 4",
        "kill @s",
    ])
    fn("souls/wisp_fx", [
        "execute as @e[type=item_display,tag=sift.wisp] at @s run particle minecraft:soul ~ ~0.4 ~ 0.08 0.12 0.08 0.004 1",
        "execute as @e[type=item_display,tag=sift.wisp] at @s run particle minecraft:end_rod ~ ~0.4 ~ 0.25 0.25 0.25 0.0 1",
    ])
    fn("souls/collect", [
        "kill @e[type=item_display,tag=sift.wisp,distance=..1.8,limit=1,sort=nearest]",
        "scoreboard players add @s sift.souls 5",
        "execute if score #tide sift.tmp matches 2 run scoreboard players add @s sift.souls 5",
        "particle minecraft:sculk_soul ~ ~1 ~ 0.3 0.5 0.3 0.05 12",
        "playsound minecraft:block.amethyst_cluster.hit player @s ~ ~ ~ 1 1.8",
        "playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.6 1.6",
        f"execute if score @s sift.souls matches 100.. run function {N}:souls/overflow",
        f"advancement grant @s only {N}:sift/soul_collector",
    ])
    fn("souls/overflow", [
        "scoreboard players set @s sift.souls 0",
        "experience add @s 40 points",
        "effect give @s minecraft:absorption 30 1 true",
        "effect give @s minecraft:regeneration 8 1 true",
        "particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.3 40",
        "playsound minecraft:block.beacon.activate player @a ~ ~ ~ 1 1.6",
        f"title @s actionbar {tj(text('✦ Débordement d’âmes ! ✦', 'light_purple', bold=True))}",
        f"advancement grant @s only {N}:sift/soul_overflow",
    ])
    for t, ch in (("calm", 0.22), ("surge", 0.6), ("ebb", 0.12)):
        dp_json(f"{N}/predicate/chance/wisp_{t}", {"type": "minecraft:random_chance", "chance": ch})
    dp_json(f"{N}/predicate/chance/spawn_try", {"type": "minecraft:random_chance", "chance": 0.5})
    dp_json(f"{N}/predicate/chance/spawn_hostile_surge", {"type": "minecraft:random_chance", "chance": 0.8})
    dp_json(f"{N}/predicate/chance/spawn_hostile_calm", {"type": "minecraft:random_chance", "chance": 0.25})
    dp_json(f"{N}/predicate/chance/spawn_hostile_ebb", {"type": "minecraft:random_chance", "chance": 0.5})

    dp_json(f"{N}/tags/entity_type/ignored", {"values": [
        "minecraft:item", "minecraft:marker", "minecraft:item_display", "minecraft:block_display",
        "minecraft:text_display", "minecraft:interaction", "minecraft:experience_orb", "minecraft:area_effect_cloud",
        "minecraft:armor_stand", "minecraft:lightning_bolt", "minecraft:arrow", "minecraft:spectral_arrow"]})


# ---------------------------------------------------------------------------
# Portail : Machine à notes + passerelle de retour
# ---------------------------------------------------------------------------
def gen_portal():
    # --- utilisation du diapason (consommable infini) -> advancement -> fonction
    fn("use/fork", [
        f"advancement revoke @s only {N}:use/fork",
        "scoreboard players set #ray sift.tmp 70",
        f"execute anchored eyes positioned ^ ^ ^ run function {N}:portal/ray",
        f"execute if score #ray sift.tmp matches 0.. run title @s actionbar {tj(text('Le diapason ne trouve aucune Machine à notes…', 'gray'))}",
    ])
    fn("portal/ray", [
        "scoreboard players remove #ray sift.tmp 1",
        f"execute if block ~ ~ ~ minecraft:note_block align xyz positioned ~0.5 ~0.5 ~0.5 run function {N}:portal/try",
        f"execute unless block ~ ~ ~ minecraft:note_block if score #ray sift.tmp matches 1.. positioned ^ ^ ^0.1 run function {N}:portal/ray",
    ])
    fn("portal/try", [
        "scoreboard players set #ray sift.tmp -1",
        "execute if block ~ ~-1 ~ minecraft:sculk_catalyst if block ~1 ~ ~ minecraft:sculk_sensor if block ~-1 ~ ~ minecraft:sculk_sensor "
        f"if block ~ ~ ~1 minecraft:sculk_sensor if block ~ ~ ~-1 minecraft:sculk_sensor run function {N}:portal/open",
        "execute unless block ~ ~-1 ~ minecraft:sculk_catalyst run tellraw @a[distance=..8] "
        + tj([text("[Sift] ", "light_purple"), text("La Machine à notes est incomplète : il manque le noyau (catalyseur de sculk) sous le bloc musical.", "gray")]),
        "execute if block ~ ~-1 ~ minecraft:sculk_catalyst unless block ~1 ~ ~ minecraft:sculk_sensor run tellraw @a[distance=..8] "
        + tj([text("[Sift] ", "light_purple"), text("La Machine à notes est incomplète : un détecteur de sculk doit entourer le bloc musical (4 côtés).", "gray")]),
    ])
    fn("portal/open", [
        f"execute if dimension {N}:the_sift run tellraw @a[distance=..8] {tj([text('[Sift] ', 'light_purple'), text('Vous êtes déjà dans le Sift. Utilisez la passerelle de retour.', 'gray')])}",
        f"execute unless dimension {N}:the_sift unless entity @e[type=marker,tag=sift.portal,distance=..3] run function {N}:portal/open_confirm",
    ])
    fn("portal/open_confirm", [
        f"summon marker ~ ~1.6 ~ {{Tags:[\"sift.portal\",\"sift.portal.entry\"]}}",
        "scoreboard players set @e[type=marker,tag=sift.portal,distance=..3] sift.age 0",
        "playsound minecraft:block.note_block.bell block @a ~ ~ ~ 2 0.5",
        "schedule function sift:portal/melody_2 6t",
        "particle minecraft:end_rod ~ ~1 ~ 0.5 1.2 0.5 0.1 60",
        f"advancement grant @a[distance=..8] only {N}:sift/sing_to_the_sift",
    ])
    notes = [("chime", 0.75), ("chime", 1.0), ("chime", 1.25)]
    for k, (snd, pitch) in enumerate(notes):
        idx = k + 2
        fn(f"portal/melody_{idx}", [
            f"execute at @e[type=marker,tag=sift.portal.entry] run playsound minecraft:block.note_block.{snd} block @a ~ ~ ~ 2 {pitch}",
            f"schedule function {N}:portal/melody_{idx + 1} 6t",
        ])
    fn("portal/melody_5", [
        "execute at @e[type=marker,tag=sift.portal.entry] run playsound minecraft:block.note_block.bell block @a ~ ~ ~ 2 1.5",
        "execute at @e[type=marker,tag=sift.portal.entry] run particle minecraft:reverse_portal ~ ~ ~ 0.8 1.2 0.8 0.3 120",
        "execute at @e[type=marker,tag=sift.portal.entry] run playsound minecraft:block.beacon.power_select block @a ~ ~ ~ 2 1.4",
    ])
    fn("portal/portal_fx", [
        "execute as @e[type=marker,tag=sift.portal] at @s run particle minecraft:reverse_portal ~ ~ ~ 0.5 1.0 0.5 0.15 6",
        "execute as @e[type=marker,tag=sift.portal] at @s run particle minecraft:end_rod ~ ~ ~ 0.9 1.2 0.9 0.01 2",
        "execute as @e[type=marker,tag=sift.portal] at @s run particle minecraft:note ~ ~1 ~ 0.6 0.4 0.6 1 1",
        "execute as @e[type=marker,tag=sift.portal] at @s run particle minecraft:sculk_soul ~ ~ ~ 0.6 0.9 0.6 0.02 2",
    ])
    fn("portal/portal_tick", [
        f"execute as @e[type=marker,tag=sift.portal.entry] at @s as @a[distance=..2.3,scores={{sift.cd=0}}] at @s unless dimension {N}:the_sift run function {N}:portal/enter",
        f"execute as @e[type=marker,tag=sift.portal.exit] at @s as @a[distance=..2.3,scores={{sift.cd=0}}] at @s if dimension {N}:the_sift run function {N}:portal/leave",
    ])
    fn("portal/expire_tick", [
        "scoreboard players add @s sift.age 1",
        f"execute if score @s sift.age matches 300.. at @s run function {N}:portal/close",
    ])
    fn("portal/close", [
        "particle minecraft:poof ~ ~ ~ 0.5 1 0.5 0.05 30",
        "playsound minecraft:block.beacon.deactivate block @a ~ ~ ~ 2 1.2",
        "kill @s",
    ])

    # --- entrée : sauvegarde de l'origine, téléportation, arrivée
    fn("portal/enter", [
        "scoreboard players set @s sift.cd 6",
        "execute store result score @s sift.ox run data get entity @s Pos[0]",
        "execute store result score @s sift.oy run data get entity @s Pos[1]",
        "execute store result score @s sift.oz run data get entity @s Pos[2]",
        "scoreboard players set @s sift.odim 0",
        "execute if dimension minecraft:the_nether run scoreboard players set @s sift.odim 1",
        "execute if dimension minecraft:the_end run scoreboard players set @s sift.odim 2",
        "playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.4 1.6",
        "particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.4 60",
        f"execute in {N}:the_sift run tp @s ~ 220 ~",
        f"execute in {N}:the_sift as @s at @s run function {N}:portal/arrive",
    ])
    fn("portal/arrive", [
        "effect give @s minecraft:slow_falling 12 0 true",
        "effect give @s minecraft:resistance 12 4 true",
        "spreadplayers ~ ~ 0 3 false @s",
        f"function {N}:portal/build_exit",
        "scoreboard players add @s sift.visits 1",
        f"title @s times 20 80 40",
        f"title @s subtitle {tj(text('Là où chantent les âmes…', 'light_purple', italic=True))}",
        f"title @s title {tj(text('LE SIFT', 'aqua', bold=True))}",
        "playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 2 0.5",
        "playsound minecraft:block.note_block.chime player @s ~ ~ ~ 1 1.5",
        f"advancement grant @s only {N}:sift/enter_the_sift",
        f"execute if score #tide sift.tmp matches 0 run function {N}:tide/announce_0",
        f"execute if score #tide sift.tmp matches 1 run function {N}:tide/announce_1",
        f"execute if score #tide sift.tmp matches 2 run function {N}:tide/announce_2",
    ])
    # passerelle de retour : même Machine à notes, plateforme en deepslate, lanternes d'âmes
    exit_cmds = [
        "fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 minecraft:deepslate_tiles",
        "fill ~-2 ~ ~-2 ~2 ~5 ~2 minecraft:air",
        "setblock ~ ~-1 ~ minecraft:sculk_catalyst",
        "setblock ~ ~ ~ minecraft:note_block",
        "setblock ~1 ~ ~ minecraft:sculk_sensor",
        "setblock ~-1 ~ ~ minecraft:sculk_sensor",
        "setblock ~ ~ ~1 minecraft:sculk_sensor",
        "setblock ~ ~ ~-1 minecraft:sculk_sensor",
        "setblock ~2 ~-1 ~2 minecraft:chiseled_deepslate",
        "setblock ~-2 ~-1 ~2 minecraft:chiseled_deepslate",
        "setblock ~2 ~-1 ~-2 minecraft:chiseled_deepslate",
        "setblock ~-2 ~-1 ~-2 minecraft:chiseled_deepslate",
        "setblock ~2 ~ ~2 minecraft:soul_lantern",
        "setblock ~-2 ~ ~2 minecraft:soul_lantern",
        "setblock ~2 ~ ~-2 minecraft:soul_lantern",
        "setblock ~-2 ~ ~-2 minecraft:soul_lantern",
        "kill @e[type=marker,tag=sift.portal.exit,distance=..6]",
        "summon marker ~ ~1.6 ~ {Tags:[\"sift.portal\",\"sift.portal.exit\"]}",
        "tp @s ~1 ~ ~1",
    ]
    fn("portal/build_exit", [f"execute align xyz positioned ~0.5 ~ ~0.5 run function {N}:portal/build_exit_at"])
    fn("portal/build_exit_at", exit_cmds)

    # --- sortie
    fn("portal/leave", [
        "scoreboard players set @s sift.cd 6",
        "playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.4 1.2",
        "particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.4 60",
        f"function {N}:portal/return_home",
    ])
    fn("portal/trigger_exit", [
        "scoreboard players set @s sift_exit 0",
        f"execute unless dimension {N}:the_sift run tellraw @s {tj([text('[Sift] ', 'light_purple'), text('Vous n’êtes pas dans le Sift.', 'gray')])}",
        f"execute if dimension {N}:the_sift run function {N}:portal/return_home",
    ])
    fn("portal/return_home", [
        "execute store result storage sift:tmp x int 1 run scoreboard players get @s sift.ox",
        "execute store result storage sift:tmp y int 1 run scoreboard players get @s sift.oy",
        "execute store result storage sift:tmp z int 1 run scoreboard players get @s sift.oz",
        "effect give @s minecraft:slow_falling 6 0 true",
        f"execute if score @s sift.odim matches 0 run function {N}:portal/return_overworld with storage sift:tmp",
        f"execute if score @s sift.odim matches 1 run function {N}:portal/return_nether with storage sift:tmp",
        f"execute if score @s sift.odim matches 2 run function {N}:portal/return_end with storage sift:tmp",
        "execute unless score @s sift.odim matches 0..2 in minecraft:overworld run tp @s 0 120 0",
        f"title @s actionbar {tj(text('Vous quittez le Sift.', 'gray'))}",
    ])
    for dim, name in (("overworld", "return_overworld"), ("the_nether", "return_nether"), ("the_end", "return_end")):
        fn(f"portal/{name}", [f"$execute in minecraft:{dim} run tp @s $(x) $(y) $(z)"])


# ---------------------------------------------------------------------------
# Objets utilisables : Carillon d'âmes, Fiole d'ichor
# ---------------------------------------------------------------------------
def gen_use():
    fn("use/chime", [
        f"advancement revoke @s only {N}:use/chime",
        f"execute unless dimension {N}:the_sift run title @s actionbar {tj(text('Le carillon ne résonne que dans le Sift.', 'gray'))}",
        f"execute if dimension {N}:the_sift if score @s sift.souls matches ..19 run title @s actionbar {tj(text('Pas assez d’âmes (20 requises).', 'red'))}",
        f"execute if dimension {N}:the_sift if score @s sift.souls matches 20.. run function {N}:use/chime_cast",
    ])
    fn("use/chime_cast", [
        "scoreboard players remove @s sift.souls 20",
        f"execute positioned ^ ^ ^2.2 run function {N}:mob/summon_ally",
        "particle minecraft:sculk_charge_pop ~ ~1 ~ 0.6 0.6 0.6 0.1 30",
        "playsound minecraft:block.sculk_catalyst.bloom player @a ~ ~ ~ 1.5 0.8",
        "playsound minecraft:block.note_block.bell player @a ~ ~ ~ 1.5 0.7",
        "effect give @s minecraft:regeneration 5 1 true",
        f"advancement grant @s only {N}:sift/echo_ally",
    ])
    fn("use/vial", [
        f"advancement revoke @s only {N}:use/vial",
        "scoreboard players set @s sift.veil 180",
        "particle minecraft:witch ~ ~1 ~ 0.4 0.6 0.4 0.1 30",
        "playsound minecraft:entity.allay.item_given player @a ~ ~ ~ 1 0.6",
        f"advancement grant @s only {N}:sift/ichor_veil",
    ])
    for name, items, cd in (("fork", "sift:fork", None), ("chime", "sift:chime", None), ("vial", "sift:vial", None)):
        dp_json(f"{N}/advancement/use/{name}", {
            "criteria": {"used": {"trigger": "minecraft:consume_item", "conditions": {"item": {
                "items": "minecraft:stick" if name != "vial" else "minecraft:potion",
                "predicates": {"minecraft:custom_data": {"sift": name}}}}}},
            "rewards": {"function": f"{N}:use/{name}"},
        })


# ---------------------------------------------------------------------------
# Commandes d'administration / confort
# ---------------------------------------------------------------------------
def gen_admin():
    fn("admin/enter", [
        # `/function sift:admin/enter` : saute directement dans le Sift
        f"execute as @s run function {N}:portal/enter",
    ])
    fn("admin/leave", [f"function {N}:portal/return_home"])
    for i, (name, *_rest) in enumerate(TIDE_INFO):
        fn(f"admin/tide_{i}", [
            f"time of sift:tides set {i * 8000 + 2000}",
            f"function {N}:tide/update",
            f"tellraw @s {tj([text('[Sift] ', 'light_purple'), text(f'Marée forcée : {name}', 'aqua')])}",
        ])
    fn("admin/build_machine", [
        "execute align xyz positioned ~0.5 ~ ~0.5 run function sift:admin/build_machine_at",
    ])
    fn("admin/build_machine_at", [
        "setblock ~ ~-1 ~ minecraft:sculk_catalyst",
        "setblock ~ ~ ~ minecraft:note_block",
        "setblock ~1 ~ ~ minecraft:sculk_sensor",
        "setblock ~-1 ~ ~ minecraft:sculk_sensor",
        "setblock ~ ~ ~1 minecraft:sculk_sensor",
        "setblock ~ ~ ~-1 minecraft:sculk_sensor",
    ])
    fn("admin/souls_full", ["scoreboard players set @s sift.souls 100"])
    fn("admin/reset", [
        "scoreboard players reset @s sift.souls",
        "scoreboard players reset @s sift.veil",
        "kill @e[type=item_display,tag=sift.wisp]",
    ])
    fn("admin/kill_mobs", [
        "kill @e[tag=sift.mob]",
        "kill @e[type=item_display,tag=sift.model]",
    ])
    fn("admin/uninstall_hint", [
        f"tellraw @s {tj(text('Pour désinstaller proprement : /function sift:admin/reset puis retirer le pack.', 'gray'))}",
    ])


def gen_all():
    gen_core()
    gen_tides()
    gen_player()
    gen_portal()
    gen_use()
    gen_admin()
