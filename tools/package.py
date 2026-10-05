#!/usr/bin/env python3
"""Empaquette datapack/ et resourcepack/ en archives .zip prêtes à l'emploi dans dist/."""
import os
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def zipdir(src, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for dp, _, fs in os.walk(src):
            for f in sorted(fs):
                full = os.path.join(dp, f)
                info = zipfile.ZipInfo(os.path.relpath(full, src).replace("\\", "/"), (2026, 10, 5, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, open(full, "rb").read())
    print(out, os.path.getsize(out) // 1024, "Ko")


if __name__ == "__main__":
    zipdir(os.path.join(ROOT, "datapack"), os.path.join(ROOT, "dist", "SiftDataPack.zip"))
    zipdir(os.path.join(ROOT, "resourcepack"), os.path.join(ROOT, "dist", "SiftResourcePack.zip"))
