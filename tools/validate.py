#!/usr/bin/env python3
"""Validation hors-jeu : JSON valides + toutes les références `ns:id` existent (vanilla 26.3 ou pack).

Les listes d'IDs vanilla viennent du dépôt misode/mcmeta (branche `summary`, registries/data.json).
Usage : python3 tools/validate.py [chemin/registries.json]
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DP = os.path.join(ROOT, "datapack")
RP = os.path.join(ROOT, "resourcepack")
REG = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("MC_REGISTRIES", "")
ID_RE = re.compile(r"^#?[a-z0-9_.-]+:[a-z0-9_./-]+$")


def load_registries():
    if not REG or not os.path.exists(REG):
        print("! registries.json introuvable : validation des références vanilla ignorée")
        return None, None
    r = json.load(open(REG, encoding="utf-8"))
    ids, tags = set(), set()
    for k, v in r.items():
        names = v if isinstance(v, list) else list(v)
        for n in names:
            if k.startswith("tag/"):
                tags.add("#minecraft:" + n)
            else:
                ids.add("minecraft:" + n)
    return ids, tags


def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + f"[{i}]")
    elif isinstance(o, str):
        yield path, o


def pack_ids():
    ids, tags = set(), set()
    base = os.path.join(DP, "data")
    for ns in os.listdir(base):
        for dirpath, _, files in os.walk(os.path.join(base, ns)):
            for f in files:
                rel = os.path.relpath(os.path.join(dirpath, f), os.path.join(base, ns)).replace("\\", "/")
                parts = rel.split("/", 1)
                if len(parts) < 2:
                    continue
                kind, rest = parts
                if kind == "worldgen" and "/" in rest:
                    rest = rest.split("/", 1)[1]
                stem = re.sub(r"\.(json|mcfunction|nbt)$", "", rest)
                if kind == "tags":
                    k2, r2 = rest.split("/", 1)
                    if k2 == "worldgen":
                        k2, r2 = r2.split("/", 1)
                    tags.add(f"#{ns}:{re.sub(r'.json$', '', r2)}")
                else:
                    ids.add(f"{ns}:{stem}")
    return ids, tags


def main():
    errors, warnings = [], []
    vids, vtags = load_registries()
    pids, ptags = pack_ids()
    sounds = set()
    sj = os.path.join(RP, "assets", "sift", "sounds.json")
    if os.path.exists(sj):
        sounds = {"sift:" + k for k in json.load(open(sj, encoding="utf-8"))}
    # ressources du resource pack référencées depuis le data pack (item_model, fonds d'advancement…)
    rp_base = os.path.join(RP, "assets", "sift")
    for sub, ext in (("items", ".json"), ("textures", ".png")):
        for dp_, _, fs in os.walk(os.path.join(rp_base, sub)):
            for f in fs:
                if f.endswith(ext):
                    rel = os.path.relpath(os.path.join(dp_, f), os.path.join(rp_base, sub)).replace("\\", "/")[:-len(ext)]
                    pids.add("sift:" + rel)
    count = 0
    for dirpath, _, files in os.walk(DP):
        for f in files:
            p = os.path.join(dirpath, f)
            if not f.endswith((".json", ".mcmeta")):
                continue
            try:
                data = json.load(open(p, encoding="utf-8"))
            except Exception as e:
                errors.append(f"{p}: JSON invalide ({e})")
                continue
            count += 1
            for path, s in walk(data):
                if "background_music" in path and path.endswith("/sound") and ID_RE.match(s):
                    errors.append(f"{os.path.relpath(p, ROOT)}{path}: son personnalisé : utiliser {{\"sound_id\": ...}}")
                    continue
                if not ID_RE.match(s) or path.endswith("/random_name"):
                    continue
                if s.startswith("#"):
                    ok = s in ptags or (vtags is None) or s in vtags
                else:
                    ok = (s in pids or s in sounds or vids is None or s in vids
                          or ("#" + s) in ptags or ("#" + s) in (vtags or ()))
                if not ok:
                    errors.append(f"{os.path.relpath(p, ROOT)}{path}: référence inconnue {s}")
    print(f"{count} fichiers JSON analysés ; {len(errors)} erreur(s)")
    for e in errors[:200]:
        print("  ✗", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
