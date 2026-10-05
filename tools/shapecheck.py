#!/usr/bin/env python3
"""Compare la *forme* (clés JSON) de chaque fichier du pack avec les fichiers vanilla 26.3 du même dossier.

Détecte les clés mal nommées / obsolètes. Nécessite un dossier de référence vanilla :
    git clone --depth 1 --branch 26.3-data-json https://github.com/misode/mcmeta  (puis passer data/minecraft)
Usage : python3 tools/shapecheck.py <dossier data/minecraft vanilla>
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DP = os.path.join(ROOT, "datapack", "data")
VAN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("MC_VANILLA", "")
FREE_MAPS = ("properties", "attributes", "tracks", "spawn_costs", "spawns_by_category", "time_markers", "targets",
             "spawn_overrides", "effects.", "components", "state.", "to_place", "result_state", "biome_source.biomes")


def shape(o, path="", out=None):
    if out is None:
        out = set()
    if isinstance(o, dict):
        t = o.get("type") or o.get("predicate_type") or o.get("element_type") or o.get("feature_type")
        here = path + ("{" + t + "}" if isinstance(t, str) else "")
        out.add(here)
        for k, v in o.items():
            if re.match(r"^(minecraft|sift):", k) or re.match(r"^[a-z_]+$", k) and path.endswith(("properties", "spawn_costs")):
                k = "*"
            shape(v, here + "." + k, out)
    elif isinstance(o, list):
        out.add(path + "[]")
        for v in o:
            shape(v, path + "[]", out)
    return out


def folder_of(rel):
    parts = rel.split("/")
    if parts[0] == "worldgen":
        return "/".join(parts[:2])
    return parts[0]


def main():
    if not VAN or not os.path.isdir(VAN):
        print("dossier vanilla manquant")
        return 2
    vanilla = {}
    for dirpath, _, files in os.walk(VAN):
        for f in files:
            if not f.endswith(".json"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, f), VAN).replace("\\", "/")
            if rel.startswith("tags/"):
                continue
            try:
                d = json.load(open(os.path.join(dirpath, f), encoding="utf-8"))
            except Exception:
                continue
            vanilla.setdefault(folder_of(rel), set()).update(shape(d))
    bad = 0
    for dirpath, _, files in os.walk(DP):
        for f in files:
            if not f.endswith(".json"):
                continue
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, DP).replace("\\", "/").split("/", 1)[1]
            if rel.startswith("tags/"):
                continue
            fold = folder_of(rel)
            if fold not in vanilla:
                continue
            mine = shape(json.load(open(full, encoding="utf-8")))
            for p in sorted(mine - vanilla[fold]):
                if any(m in p for m in ("attributes.", "tracks.", "properties.")):
                    continue
                print(f"  ? {fold}/{os.path.basename(full)}: chemin absent du vanilla : {p}")
                bad += 1
    print(f"{bad} chemin(s) inconnu(s) du vanilla")
    return 0


if __name__ == "__main__":
    sys.exit(main())
