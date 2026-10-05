"""Objets custom (item_model + composants), recettes, advancements, commandes /function sift:give/*."""
import json
import re

from lib import dp_json, fn, NS

N = NS


def snbt(v):
    """Python -> SNBT."""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        return "[" + ",".join(snbt(x) for x in v) + "]"
    if isinstance(v, dict):
        out = []
        for k, x in v.items():
            key = k if re.match(r"^[A-Za-z0-9_.+-]+$", k) else json.dumps(k)
            out.append(f"{key}:{snbt(x)}")
        return "{" + ",".join(out) + "}"
    raise TypeError(v)


def tr(key, fallback, **style):
    d = {"translate": key, "fallback": fallback}
    d.update(style)
    return d


def lore(*lines):
    return [{"text": l, "color": "gray", "italic": False} for l in lines]


# ---------------------------------------------------------------------------------------- définitions
def item_defs():
    items = {}
    consumable_horn = lambda sound, secs: {"consume_seconds": secs, "animation": "toot_horn", "sound": sound,
                                           "has_consume_particles": False}

    def mk(key, base, model, name_fr, lines, extra=None, rarity="rare", glint=True):
        comps = {
            "minecraft:item_model": f"{N}:{model}",
            "minecraft:custom_data": {"sift": key},
            "minecraft:item_name": tr(f"item.{N}.{key}", name_fr, color="light_purple"),
            "minecraft:lore": lore(*lines),
            "minecraft:rarity": rarity,
            "minecraft:max_stack_size": 1 if extra and "minecraft:consumable" in extra and "minecraft:use_remainder" in extra else 64,
        }
        if glint:
            comps["minecraft:enchantment_glint_override"] = True
        if extra:
            comps.update(extra)
        return {"id": base, "components": comps}

    fork = mk("fork", "minecraft:stick", "fork", "Diapason du Chanteur",
              ["Accordé sur le chant des Chanteurs.", "Pointez une Machine à notes puis maintenez",
               "clic droit pour ouvrir la porte du Sift."], extra={
                  "minecraft:consumable": consumable_horn("minecraft:block.note_block.chime", 1.4)}, rarity="epic")
    fork["components"]["minecraft:use_remainder"] = {"id": "minecraft:stick", "count": 1, "components": dict(fork["components"])}
    items["fork"] = fork

    chime = mk("chime", "minecraft:stick", "chime", "Carillon d'âmes",
               ["Clic droit dans le Sift : dépense 20 âmes", "pour invoquer un Golem d'écho allié (5 min)."], extra={
                   "minecraft:consumable": consumable_horn("minecraft:block.note_block.bell", 1.0)}, rarity="epic")
    chime["components"]["minecraft:use_remainder"] = {"id": "minecraft:stick", "count": 1, "components": dict(chime["components"])}
    items["chime"] = chime

    items["vial"] = mk("vial", "minecraft:potion", "vial", "Fiole d'ichor",
                       ["Un voile d'ichor : vous traversez l'ichor", "sans qu'il ne ronge votre âme (3 min)."],
                       extra={"minecraft:potion_contents": {"custom_color": 12603647}}, rarity="rare")
    items["vial"]["components"].pop("minecraft:max_stack_size", None)
    items["essence"] = mk("essence", "minecraft:stick", "soul_essence", "Essence d'âme",
                          ["Une âme cristallisée.", "Consommez-la dans le Sift : +20 âmes."],
                          extra={"minecraft:consumable": {"consume_seconds": 0.8, "animation": "drink",
                                                          "sound": "minecraft:block.amethyst_block.resonate", "has_consume_particles": True}},
                          rarity="uncommon")
    items["essence"]["components"]["minecraft:max_stack_size"] = 64
    items["ichor_shard"] = mk("ichor_shard", "minecraft:stick", "ichor_shard", "Éclat d'ichor",
                              ["Ichor solidifié. Consommé, il offre", "un court voile d'ichor (60 s)."],
                              extra={"minecraft:consumable": {"consume_seconds": 0.8, "animation": "eat",
                                                              "sound": "minecraft:entity.allay.item_given", "has_consume_particles": True}},
                              rarity="uncommon")
    items["ichor_shard"]["components"]["minecraft:max_stack_size"] = 64
    return items


ITEMS = None


def gen_all():
    global ITEMS
    ITEMS = item_defs()

    # ---- /function sift:give/*
    for key, it in ITEMS.items():
        comps = ",".join(f"{k}={snbt(v)}" for k, v in it["components"].items())
        fn(f"give/{key}", [f"give @s {it['id']}[{comps}] 1"])
    fn("give/all", [f"function {N}:give/{k}" for k in ITEMS])
    fn("give/starter", [
        f"function {N}:give/fork", f"function {N}:give/chime", f"function {N}:give/vial",
        "give @s minecraft:sculk_catalyst 1", "give @s minecraft:sculk_sensor 4", "give @s minecraft:note_block 1",
        "tellraw @s " + json.dumps([{"text": "[Sift] ", "color": "light_purple"},
                                    {"text": "Kit de départ : bâtissez la Machine à notes (catalyseur de sculk sous un bloc musical, 4 détecteurs de sculk autour) puis utilisez le Diapason.", "color": "gray"}], ensure_ascii=False),
    ])

    # ---- consommables à effet
    fn("use/essence", [f"advancement revoke @s only {N}:use/essence", "scoreboard players add @s sift.souls 20",
                       "particle minecraft:sculk_soul ~ ~1 ~ 0.3 0.5 0.3 0.05 14",
                       f"execute if score @s sift.souls matches 100.. run function {N}:souls/overflow"])
    fn("use/ichor_shard", [f"advancement revoke @s only {N}:use/ichor_shard", "scoreboard players set @s sift.veil 60",
                           "particle minecraft:witch ~ ~1 ~ 0.4 0.6 0.4 0.1 20",
                           f"advancement grant @s only {N}:sift/ichor_veil"])
    for key in ("essence", "ichor_shard"):
        dp_json(f"{N}/advancement/use/{key}", {
            "criteria": {"used": {"trigger": "minecraft:consume_item", "conditions": {"item": {
                "items": "minecraft:stick", "predicates": {"minecraft:custom_data": {"sift": key}}}}}},
            "rewards": {"function": f"{N}:use/{key}"}})

    # ---- recettes
    def recipe(name, pattern, key, result_id, count=1, comps=None, category="misc"):
        res = {"id": result_id, "count": count}
        if comps:
            res["components"] = comps
        dp_json(f"{N}/recipe/{name}", {"type": "minecraft:crafting_shaped", "category": category, "key": key,
                                        "pattern": pattern, "result": res})

    A, E, C = "minecraft:amethyst_shard", "minecraft:echo_shard", "minecraft:copper_ingot"
    recipe("fork", ["A A", "AEA", " C "], {"A": A, "E": E, "C": C}, "minecraft:stick", comps=ITEMS["fork"]["components"], category="equipment")
    recipe("chime", [" C ", "AEA", "A A"], {"A": A, "E": E, "C": C}, "minecraft:stick", comps=ITEMS["chime"]["components"], category="equipment")
    recipe("vial", ["S", "G"], {"S": "minecraft:slime_ball", "G": "minecraft:glass_bottle"}, "minecraft:potion",
           comps=ITEMS["vial"]["components"], category="misc")
    recipe("machine_catalyst", ["EBE", "DDD"], {"E": E, "B": "minecraft:bone_block", "D": "minecraft:deepslate"}, "minecraft:sculk_catalyst")
    recipe("machine_sensor", ["AEA", "DCD"], {"A": A, "E": E, "D": "minecraft:deepslate", "C": C}, "minecraft:sculk_sensor")
    dp_json(f"{N}/advancement/recipes/unlock", {
        "criteria": {"echo": {"trigger": "minecraft:inventory_changed", "conditions": {"items": [{"items": "minecraft:echo_shard"}]}}},
        "rewards": {"recipes": [f"{N}:fork", f"{N}:chime", f"{N}:vial", f"{N}:machine_catalyst", f"{N}:machine_sensor"]}})

    gen_advancements()


# ---------------------------------------------------------------------------------------- advancements
def icon(item, model=None):
    d = {"id": item}
    if model:
        d["components"] = {"minecraft:item_model": f"{N}:{model}"}
    return d


ADV = [
    # clé, parent, icône, titre, description, cadre, critères(dict) / None=impossible(accordé par fonction)
    ("sing_to_the_sift", "root", icon("minecraft:stick", "fork"), "Chanter pour le Sift",
     "Activez une Machine à notes avec le Diapason du Chanteur.", "task"),
    ("enter_the_sift", "sing_to_the_sift", icon("minecraft:echo_shard"), "Là où chantent les âmes",
     "Franchissez le portail du Deep Dark et entrez dans le Sift.", "goal"),
    ("soul_collector", "enter_the_sift", icon("minecraft:stick", "soul_essence"), "Cueilleur d'âmes",
     "Ramassez une âme errante.", "task"),
    ("soul_overflow", "soul_collector", icon("minecraft:experience_bottle"), "Débordement d'âmes",
     "Remplissez entièrement votre jauge d'âmes.", "goal"),
    ("three_tides", "enter_the_sift", icon("minecraft:clock"), "Au rythme des marées",
     "Vivez les trois marées du Sift : Calme, Haute et Basse.", "goal"),
    ("hear_singer", "enter_the_sift", icon("minecraft:note_block"), "Un chant pur",
     "Approchez-vous d'un Chanteur — un « avertisseur en bonne santé ».", "task"),
    ("ichor_veil", "enter_the_sift", icon("minecraft:potion", "vial"), "Voile d'ichor",
     "Revêtez un voile d'ichor pour traverser le liquide qui ronge les âmes.", "task"),
    ("echo_ally", "soul_collector", icon("minecraft:stick", "chime"), "Écho fidèle",
     "Invoquez un Golem d'écho avec le Carillon d'âmes.", "goal"),
    ("slay_slasher", "enter_the_sift", icon("minecraft:bone"), "Griffes dans la brume",
     "Terrassez un Lacérateur de sculk.", "task"),
    ("slay_mage", "slay_slasher", icon("minecraft:amethyst_shard"), "Silence, Mage",
     "Terrassez un Mage de sculk.", "task"),
    ("slay_groobler", "slay_slasher", icon("minecraft:moss_block"), "Bris de carapace",
     "Terrassez une Sentinelle Groobler.", "task"),
    ("sifter", "slay_mage", icon("minecraft:stick", "soul_essence"), "Maître du Sift",
     "Obtenez tous les autres accomplissements du Sift.", "challenge"),
]


def gen_advancements():
    base = {}
    dp_json(f"{N}/advancement/sift/root", {
        "criteria": {"auto": {"trigger": "minecraft:tick"}},
        "display": {
            "icon": icon("minecraft:stick", "fork"),
            "title": tr("advancements.sift.root.title", "Le Sift", color="light_purple"),
            "description": tr("advancements.sift.root.description", "La quatrième dimension chante, quelque part sous le Deep Dark…"),
            "background": f"{N}:gui/advancements/backgrounds/sift",
            "show_toast": False, "announce_to_chat": False,
        },
    })
    for key, parent, ic, title, desc, frame in ADV:
        crit = {"granted": {"trigger": "minecraft:impossible"}}
        reqs = None
        extra = {}
        if key == "enter_the_sift":
            crit = {"changed": {"trigger": "minecraft:changed_dimension", "conditions": {"to": f"{N}:the_sift"}}, "fn": {"trigger": "minecraft:impossible"}}
            reqs = [["changed", "fn"]]
        if key == "three_tides":
            crit = {"calm": {"trigger": "minecraft:impossible"}, "surge": {"trigger": "minecraft:impossible"}, "ebb": {"trigger": "minecraft:impossible"}}
            reqs = [["calm"], ["surge"], ["ebb"]]
        if key.startswith("slay_"):
            tag = {"slay_slasher": "sift.sculk_slasher", "slay_mage": "sift.sculk_mage", "slay_groobler": "sift.groobler"}[key]
            crit = {"kill": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": {
                "type": "minecraft:entity_properties", "entity": "this", "predicate": {"minecraft:entity_tags": {"any_of": [tag]}}}}}}
        if key == "sifter":
            others = [k for k, *_ in ADV if k != "sifter"]
            crit = {k: {"trigger": "minecraft:impossible"} for k in ["x"]}
            crit = {k: {"trigger": "minecraft:impossible"} for k in others}
            reqs = [[k] for k in others]
        adv = {
            "parent": f"{N}:sift/{parent}",
            "criteria": crit,
            "display": {
                "icon": ic,
                "title": tr(f"advancements.sift.{key}.title", title),
                "description": tr(f"advancements.sift.{key}.description", desc),
                "frame": frame, "show_toast": True, "announce_to_chat": True,
            },
            "rewards": {"experience": 30 if frame == "task" else 80 if frame == "goal" else 300},
        }
        if reqs:
            adv["requirements"] = reqs
        dp_json(f"{N}/advancement/sift/{key}", adv)

    # le « maître » se débloque via un critère par succès : on les accorde depuis une fonction de bilan
    fn("sift/check_mastery", [
        f"execute if entity @s[advancements={{{N}:sift/{k}=true}}] run advancement grant @s only {N}:sift/sifter {k}"
        for k, *_ in ADV if k != "sifter"
    ])
