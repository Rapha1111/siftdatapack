"""Écrivain NBT minimal (gzip) pour fabriquer des structures (.nbt) sans dépendance externe."""
import gzip
import struct

END, BYTE, SHORT, INT, LONG, FLOAT, DOUBLE, BYTEARR, STRING, LIST, COMPOUND, INTARR, LONGARR = range(13)


class Tag:
    def __init__(self, kind, value, sub=None):
        self.kind, self.value, self.sub = kind, value, sub


def b(v): return Tag(BYTE, v)
def i(v): return Tag(INT, v)
def s(v): return Tag(STRING, v)
def lst(sub, items): return Tag(LIST, items, sub)
def comp(d): return Tag(COMPOUND, d)


def _name(n):
    e = n.encode("utf-8")
    return struct.pack(">H", len(e)) + e


def _payload(t):
    k = t.kind
    if k == BYTE:
        return struct.pack(">b", t.value)
    if k == INT:
        return struct.pack(">i", t.value)
    if k == STRING:
        return _name(t.value)
    if k == LIST:
        out = struct.pack(">bi", t.sub, len(t.value))
        return out + b"".join(_payload(x) for x in t.value)
    if k == COMPOUND:
        out = b""
        for key, v in t.value.items():
            out += struct.pack(">b", v.kind) + _name(key) + _payload(v)
        return out + b"\x00"
    raise ValueError(k)


def to_gzip(root: Tag) -> bytes:
    raw = struct.pack(">b", COMPOUND) + _name("") + _payload(root)
    return gzip.compress(raw, 9, mtime=0)


class Structure:
    """Grille de blocs -> structure vanilla."""

    def __init__(self, sx, sy, sz, data_version=5023):
        self.size, self.dv = (sx, sy, sz), data_version
        self.cells = {}

    def set(self, x, y, z, name, nbt=None, **props):
        self.cells[(x, y, z)] = (name if ":" in name else "minecraft:" + name, props, nbt)

    def fill(self, x1, y1, z1, x2, y2, z2, name, **props):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.set(x, y, z, name, None, **props)

    def to_bytes(self):
        palette, index, blocks = [], {}, []
        for (x, y, z), (name, props, nbt) in sorted(self.cells.items()):
            key = (name, tuple(sorted(props.items())))
            if key not in index:
                index[key] = len(palette)
                ent = {"Name": s(name)}
                if props:
                    ent["Properties"] = comp({k: s(str(v).lower() if isinstance(v, bool) else str(v)) for k, v in props.items()})
                palette.append(comp(ent))
            blk = {"pos": lst(INT, [i(x), i(y), i(z)]), "state": i(index[key])}
            if nbt:
                blk["nbt"] = comp(nbt)
            blocks.append(comp(blk))
        root = comp({
            "DataVersion": i(self.dv),
            "size": lst(INT, [i(v) for v in self.size]),
            "palette": lst(COMPOUND, palette),
            "blocks": lst(COMPOUND, blocks),
            "entities": lst(COMPOUND, []),
        })
        return to_gzip(root)
