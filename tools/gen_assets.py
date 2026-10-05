"""Resource pack : modèles/ textures des créatures, objets, sons & musiques, langues, icône."""
import json
import os

import itemart
import mobmodels
import music
from lib import RP, rp_json

ASSETS = os.path.join(RP, "assets")

# traductions anglaises des textes (le français est la langue source, utilisée en fallback)
EN = {
    "item.sift.fork": "Singer's Tuning Fork",
    "item.sift.chime": "Soul Chime",
    "item.sift.vial": "Ichor Vial",
    "item.sift.soul_essence": "Soul Essence",
    "item.sift.ichor_shard": "Ichor Shard",
    "sift.bed.no_sleep": "The songs of the Sift keep you awake.",
    "advancements.sift.root.title": "The Sift",
    "advancements.sift.root.description": "The fourth dimension sings, somewhere beneath the Deep Dark…",
    "advancements.sift.sing_to_the_sift.title": "Sing to the Sift",
    "advancements.sift.sing_to_the_sift.description": "Activate a Note Block Machine with the Singer's Tuning Fork.",
    "advancements.sift.enter_the_sift.title": "Where Souls Sing",
    "advancements.sift.enter_the_sift.description": "Step through the Deep Dark portal into the Sift.",
    "advancements.sift.soul_collector.title": "Soul Collector",
    "advancements.sift.soul_collector.description": "Pick up a wandering soul.",
    "advancements.sift.soul_overflow.title": "Soul Overflow",
    "advancements.sift.soul_overflow.description": "Completely fill your soul meter.",
    "advancements.sift.three_tides.title": "Rhythm of the Tides",
    "advancements.sift.three_tides.description": "Experience all three Sift tides: Hush, Surge and Ebb.",
    "advancements.sift.hear_singer.title": "A Pure Song",
    "advancements.sift.hear_singer.description": "Approach a Singer — a \"healthy Warden\".",
    "advancements.sift.ichor_veil.title": "Ichor Veil",
    "advancements.sift.ichor_veil.description": "Don an ichor veil to cross the liquid that gnaws at souls.",
    "advancements.sift.echo_ally.title": "Faithful Echo",
    "advancements.sift.echo_ally.description": "Summon an Echo Golem with the Soul Chime.",
    "advancements.sift.slay_slasher.title": "Claws in the Mist",
    "advancements.sift.slay_slasher.description": "Defeat a Sculk Slasher.",
    "advancements.sift.slay_mage.title": "Silence, Mage",
    "advancements.sift.slay_mage.description": "Defeat a Sculk Mage.",
    "advancements.sift.slay_groobler.title": "Shell Breaker",
    "advancements.sift.slay_groobler.description": "Defeat a Groobler Sentinel.",
    "advancements.sift.sifter.title": "Sift Master",
    "advancements.sift.sifter.description": "Earn every other Sift advancement.",
}


def fr_texts():
    import gen_items
    fr = {
        "item.sift.fork": "Diapason du Chanteur", "item.sift.chime": "Carillon d'âmes", "item.sift.vial": "Fiole d'ichor",
        "item.sift.soul_essence": "Essence d'âme", "item.sift.ichor_shard": "Éclat d'ichor",
        "sift.bed.no_sleep": "Les chants du Sift vous empêchent de dormir.",
        "advancements.sift.root.title": "Le Sift",
        "advancements.sift.root.description": "La quatrième dimension chante, quelque part sous le Deep Dark…",
    }
    for key, _p, _i, title, desc, _f in gen_items.ADV:
        fr[f"advancements.sift.{key}.title"] = title
        fr[f"advancements.sift.{key}.description"] = desc
    return fr


def gen_all():
    # ---- créatures
    for m in mobmodels.all_models():
        m.save(ASSETS)

    # ---- objets 2D
    itemart.save_items(ASSETS)
    for name, tex in (("fork", "fork"), ("chime", "chime"), ("vial", "vial"), ("soul_essence", "soul_essence"),
                      ("ichor_shard", "ichor_shard")):
        rp_json(f"sift/models/item/{name}", {"parent": "minecraft:item/handheld" if name in ("fork", "chime") else "minecraft:item/generated",
                                              "textures": {"layer0": f"sift:item/{tex}"}})
        rp_json(f"sift/items/{name}", {"model": {"type": "minecraft:model", "model": f"sift:item/{name}"}})
    rp_json("sift/models/item/wisp", {"parent": "minecraft:item/generated", "textures": {"layer0": "sift:item/wisp"}})
    rp_json("sift/items/wisp", {"model": {"type": "minecraft:model", "model": "sift:item/wisp"}})

    # ---- fond d'advancements, icône du pack
    bg = os.path.join(ASSETS, "sift", "textures", "gui", "advancements", "backgrounds")
    os.makedirs(bg, exist_ok=True)
    itemart.advancement_bg(os.path.join(bg, "sift.png"))
    itemart.pack_icon(os.path.join(RP, "pack.png"))
    import shutil
    from lib import DP
    shutil.copy(os.path.join(RP, "pack.png"), os.path.join(DP, "pack.png"))

    # ---- langues
    rp_json("sift/lang/en_us", EN)
    rp_json("sift/lang/fr_fr", fr_texts())

    # ---- musiques + sons
    lengths = music.build_all(ASSETS)
    sounds = {}
    for name in lengths:
        sounds[f"music.{name}"] = {"sounds": [{"name": f"sift:music/{name}", "stream": True}]}
    rp_json("sift/sounds", sounds)
