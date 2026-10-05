#!/usr/bin/env python3
"""Vérifie la syntaxe de toutes les fonctions .mcfunction contre l'arbre de commandes vanilla 26.3.

L'arbre vient de misode/mcmeta (branche summary, commands/data.json).
Usage : python3 tools/cmdcheck.py [chemin/commands.json]
Vérifie aussi que chaque `function ns:chemin` appelée existe dans le pack.
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DP = os.path.join(ROOT, "datapack", "data")
CMD = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("MC_COMMANDS", "")

NUM = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?[bBsSlLfFdD]?$")
INT = re.compile(r"^[+-]?\d+$")
COORD = re.compile(r"^([~^][+-]?(\d+\.?\d*|\.\d+)?|[+-]?(\d+\.?\d*|\.\d+))$")
ID = re.compile(r"^#?[a-z0-9_.-]*:?[a-z0-9_./-]+(\[.*\])?(\{.*\})?$", re.S)
RANGE = re.compile(r"^(-?\d*\.?\d*)?(\.\.)?(-?\d*\.?\d*)?$")


def tokenize(line):
    toks, cur, depth, q, i = [], "", 0, None, 0
    while i < len(line):
        ch = line[i]
        if q:
            cur += ch
            if ch == "\\" and i + 1 < len(line):
                cur += line[i + 1]
                i += 1
            elif ch == q:
                q = None
        elif ch in "\"'":
            q = ch
            cur += ch
        elif ch in "[{(":
            depth += 1
            cur += ch
        elif ch in "]})":
            depth -= 1
            cur += ch
        elif ch == " " and depth == 0:
            if cur:
                toks.append(cur)
                cur = ""
        else:
            cur += ch
        i += 1
    if cur:
        toks.append(cur)
    if depth != 0 or q:
        raise ValueError("crochets/guillemets non équilibrés")
    return toks


def arg_consumes(parser, props, toks, i):
    """Retourne le nb de tokens consommés par l'argument, ou 0 si invalide."""
    t = toks[i]
    if parser in ("minecraft:vec3", "minecraft:block_pos"):
        ok = i + 2 < len(toks) and all(COORD.match(toks[i + k]) for k in range(3))
        return 3 if ok else 0
    if parser in ("minecraft:vec2", "minecraft:column_pos", "minecraft:rotation"):
        ok = i + 1 < len(toks) and all(COORD.match(toks[i + k]) for k in range(2))
        return 2 if ok else 0
    if parser == "brigadier:string":
        if (props or {}).get("type") == "greedy":
            return len(toks) - i
        return 1
    if parser == "minecraft:message":
        return len(toks) - i
    if parser in ("brigadier:integer", "brigadier:long"):
        return 1 if INT.match(t) else 0
    if parser in ("brigadier:float", "brigadier:double"):
        return 1 if NUM.match(t) else 0
    if parser == "brigadier:bool":
        return 1 if t in ("true", "false") else 0
    if parser in ("minecraft:entity", "minecraft:score_holder", "minecraft:game_profile"):
        if t.startswith("@"):
            return 1 if re.match(r"^@[aeprsn](\[.*\])?$", t, re.S) else 0
        return 1
    if parser == "minecraft:time":
        return 1 if re.match(r"^\d*\.?\d+[dst]?$", t) else 0
    if parser in ("minecraft:int_range", "minecraft:float_range"):
        return 1 if RANGE.match(t) and t else 0
    if parser == "minecraft:angle":
        return 1 if COORD.match(t) else 0
    if parser == "minecraft:operation":
        return 1 if t in ("=", "+=", "-=", "*=", "/=", "%=", "<", ">", "><") else 0
    if parser in ("minecraft:nbt_compound_tag",):
        return 1 if t.startswith("{") and t.endswith("}") else 0
    if parser in ("minecraft:component", "minecraft:style", "minecraft:nbt_tag"):
        return 1
    if parser in ("minecraft:resource_location", "minecraft:resource", "minecraft:resource_or_tag",
                  "minecraft:resource_key", "minecraft:resource_or_tag_key", "minecraft:block_state",
                  "minecraft:block_predicate", "minecraft:item_stack", "minecraft:item_predicate",
                  "minecraft:function", "minecraft:dimension", "minecraft:particle", "minecraft:mob_effect",
                  "minecraft:entity_summon", "minecraft:loot_table", "minecraft:predicate"):
        if t == "*" and parser in ("minecraft:item_predicate", "minecraft:block_predicate"):
            return 1
        return 1 if ID.match(t) else 0
    return 1


def build(tree):
    return tree


def match(node, toks, i, root, memo):
    """DFS : True si `toks[i:]` est valide depuis les enfants de node."""
    key = (id(node), i)
    if key in memo:
        return memo[key]
    res = False
    if i >= len(toks):
        res = bool(node.get("executable"))
    else:
        children = node.get("children", {})
        if "redirect" in node and not children:
            tgt = root
            for p in node["redirect"]:
                tgt = tgt["children"][p]
            res = match(tgt, toks, i, root, memo)
        else:
            for name, ch in children.items():
                if ch["type"] == "literal":
                    if toks[i] == name:
                        res = after(ch, toks, i + 1, root, memo)
                else:
                    n = arg_consumes(ch.get("parser", ""), ch.get("properties"), toks, i)
                    if n:
                        res = after(ch, toks, i + n, root, memo)
                if res:
                    break
    memo[key] = res
    return res


def after(ch, toks, j, root, memo):
    if j >= len(toks):
        return bool(ch.get("executable"))
    if ch["type"] == "literal" and not ch.get("children") and "redirect" not in ch and not ch.get("executable"):
        return match(root, toks, j, root, memo)  # `run` : retour à la racine
    if "redirect" in ch:
        tgt = root
        for p in ch["redirect"]:
            tgt = tgt["children"][p]
        return match(tgt, toks, j, root, memo)
    return match(ch, toks, j, root, memo)


def main():
    if not CMD or not os.path.exists(CMD):
        print("commands.json introuvable (MC_COMMANDS)")
        return 2
    root = json.load(open(CMD, encoding="utf-8"))
    funcs = set()
    files = []
    for ns in os.listdir(DP):
        base = os.path.join(DP, ns, "function")
        for dp, _, fs in os.walk(base):
            for f in fs:
                if f.endswith(".mcfunction"):
                    p = os.path.join(dp, f)
                    files.append(p)
                    rel = os.path.relpath(p, base)[:-11].replace("\\", "/")
                    funcs.add(f"{ns}:{rel}")
    errors = 0
    nlines = 0
    sys.path.insert(0, os.path.dirname(__file__))
    import validate as V
    vids, vtags = V.load_registries()
    pids, ptags = V.pack_ids()
    sj = os.path.join(ROOT, "resourcepack", "assets", "sift", "sounds.json")
    extra = {"sift:" + k for k in json.load(open(sj))} if os.path.exists(sj) else set()
    extra |= {"sift:mob/" + f[:-5] for f in os.listdir(os.path.join(ROOT, "resourcepack", "assets", "sift", "items", "mob"))} if os.path.isdir(os.path.join(ROOT, "resourcepack", "assets", "sift", "items", "mob")) else set()
    extra |= {"sift:" + f[:-5] for f in os.listdir(os.path.join(ROOT, "resourcepack", "assets", "sift", "items"))
              if f.endswith(".json")} if os.path.isdir(os.path.join(ROOT, "resourcepack", "assets", "sift", "items")) else set()
    for p in files:
        for ln, raw in enumerate(open(p, encoding="utf-8").read().split("\n"), 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            nlines += 1
            if line.startswith("$"):
                continue
            try:
                toks = tokenize(line)
            except ValueError as e:
                print(f"  ✗ {os.path.relpath(p, ROOT)}:{ln}: {e}: {line[:100]}")
                errors += 1
                continue
            if toks[0].startswith("/"):
                toks[0] = toks[0][1:]
            if not match(root, toks, 0, root, {}):
                print(f"  ✗ {os.path.relpath(p, ROOT)}:{ln}: syntaxe invalide: {line[:140]}")
                errors += 1
            for m in re.finditer(r"(?<![A-Za-z0-9_.])(#?(?:minecraft|sift):[a-z0-9_./-]+)", line):
                tid = m.group(1)
                if vids is None or tid.startswith("#") and (tid in ptags or tid in vtags):
                    continue
                if tid in vids or tid in pids or tid in extra or tid.startswith("sift:") and tid[5:] in ("tmp", "const"):
                    continue
                if re.match(r"^(text|translate|fallback|color|score|name|objective|selector|bold|italic|block_state|id|count|type):", tid):
                    continue
                print(f"  ✗ {os.path.relpath(p, ROOT)}:{ln}: identifiant inconnu {tid}")
                errors += 1
            for m in re.finditer(r"(?:^|\s)function\s+(#?[a-z0-9_.-]+:[a-z0-9_./-]+)", line):
                fid = m.group(1)
                if not fid.startswith("#") and fid not in funcs and not fid.startswith("minecraft:"):
                    print(f"  ✗ {os.path.relpath(p, ROOT)}:{ln}: fonction inconnue {fid}")
                    errors += 1
    print(f"{len(files)} fonctions, {nlines} commandes vérifiées, {errors} erreur(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
