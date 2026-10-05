"""Petits utilitaires partagés par les générateurs du pack Sift."""
import json
import os
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DP = os.path.join(ROOT, "datapack")          # data pack (dossier brut)
RP = os.path.join(ROOT, "resourcepack")      # resource pack (dossier brut)
NS = "sift"


def _write(path, data, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode, **({} if "b" in mode else {"encoding": "utf-8", "newline": "\n"})) as f:
        f.write(data)


def dp_json(rel, obj):
    _write(os.path.join(DP, "data", rel + ".json"), json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def rp_json(rel, obj):
    _write(os.path.join(RP, "assets", rel + ".json"), json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def dp_text(rel, text):
    _write(os.path.join(DP, "data", rel), text if text.endswith("\n") else text + "\n")


def dp_bytes(rel, data):
    _write(os.path.join(DP, "data", rel), data, "wb")


def fn(name, lines):
    """Écrit une fonction mcfunction `sift:<name>`."""
    body = "\n".join(l for l in lines)
    dp_text(f"{NS}/function/{name}.mcfunction", body)


def reset_output():
    for d in (DP, RP):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)


def blk(name, **props):
    d = {"Name": name if ":" in name else "minecraft:" + name}
    if props:
        d["Properties"] = {k: str(v).lower() if isinstance(v, bool) else str(v) for k, v in props.items()}
    return d


def state(name, **props):
    """BlockState pour les JSON worldgen ({'id':..., 'properties':...})."""
    d = {"id": name if ":" in name else "minecraft:" + name}
    if props:
        d["properties"] = {k: str(v).lower() if isinstance(v, bool) else str(v) for k, v in props.items()}
    return d
