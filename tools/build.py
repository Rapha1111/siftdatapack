#!/usr/bin/env python3
"""Régénère intégralement le data pack et le resource pack Sift (dossiers datapack/ et resourcepack/)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from lib import reset_output, dp_json, rp_json, DP, RP, ROOT  # noqa: E402
import json  # noqa: E402

import gen_worldgen  # noqa: E402
import gen_features  # noqa: E402

DESC = {"text": "Le Sift — dimension du chant des âmes", "color": "light_purple"}


def meta():
    for base, fmt in ((DP, [121, 0]), (RP, [97, 1])):
        with open(os.path.join(base, "pack.mcmeta"), "w", encoding="utf-8", newline="\n") as f:
            json.dump({"pack": {"description": DESC, "pack_format": fmt[0], "min_format": fmt, "max_format": fmt[0]}}, f, indent=2, ensure_ascii=False)
            f.write("\n")


def main():
    reset_output()
    meta()
    gen_worldgen.gen_all()
    gen_features.gen_all()
    for mod in ("gen_structures", "gen_gameplay", "gen_mobs", "gen_items", "gen_assets"):
        try:
            m = __import__(mod)
        except ModuleNotFoundError as e:
            if e.name == mod:
                continue
            raise
        m.gen_all()


if __name__ == "__main__":
    main()
