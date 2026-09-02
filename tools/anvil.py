"""A reader for Minecraft 1.8 Anvil worlds — numeric block ids, `region/r.X.Z.mca` — in the standard library
alone, which is what lets every world tool here run from a checkout with nothing installed.

    from anvil import World
    world = World("maps/<slug>/region")
    world.get(x, y, z)          -> (id, data)
    world.blocks()              -> every non-air block as (x, y, z, id, data)
    world.columns()             -> {(x, z): [(y, id, data), ...]} sorted by y, non-air only, cached
    world.bounds()              -> (minx, miny, minz, maxx, maxy, maxz) or None
    world.biome(x, z)           -> the biome id, or None

    python3 tools/anvil.py <regionDir>     a census: chunks, blocks, bounds, the fifteen commonest id:data

Blocks are decoded from a section's raw `Blocks`/`Data`/`Add` arrays on demand rather than unpacked into
per-block objects at load time, so a million-block board loads in seconds and `columns()` is the one pass
that costs anything.
"""

from __future__ import annotations

import gzip
import os
import struct
import zlib

_BYTE = struct.Struct(">b")
_UBYTE = struct.Struct(">B")
_SHORT = struct.Struct(">h")
_USHORT = struct.Struct(">H")
_INT = struct.Struct(">i")
_LONG = struct.Struct(">q")
_FLOAT = struct.Struct(">f")
_DOUBLE = struct.Struct(">d")


class _Reader:
    """A cursor over one NBT byte string. Byte arrays come back as `bytes`, because the block, data, add and
    biome arrays are what a chunk is and materialising them as ints would be most of the load time."""
    __slots__ = ("data", "pos")

    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0

    def ubyte(self) -> int:
        value = _UBYTE.unpack_from(self.data, self.pos)[0]
        self.pos += 1
        return value

    def ushort(self) -> int:
        value = _USHORT.unpack_from(self.data, self.pos)[0]
        self.pos += 2
        return value

    def int(self) -> int:
        value = _INT.unpack_from(self.data, self.pos)[0]
        self.pos += 4
        return value

    def raw(self, count: int) -> bytes:
        value = self.data[self.pos:self.pos + count]
        self.pos += count
        return value

    def string(self) -> str:
        return self.raw(self.ushort()).decode("utf-8", errors="replace")

    def fixed(self, layout):
        value = layout.unpack_from(self.data, self.pos)[0]
        self.pos += layout.size
        return value

    def payload(self, tag_id: int):
        if tag_id == 1:
            return self.fixed(_BYTE)
        if tag_id == 2:
            return self.fixed(_SHORT)
        if tag_id == 3:
            return self.fixed(_INT)
        if tag_id == 4:
            return self.fixed(_LONG)
        if tag_id == 5:
            return self.fixed(_FLOAT)
        if tag_id == 6:
            return self.fixed(_DOUBLE)
        if tag_id == 7:
            return self.raw(self.int())
        if tag_id == 8:
            return self.string()
        if tag_id == 9:
            child_id = self.ubyte()
            count = self.int()
            if child_id == 0 or count <= 0:
                return []
            return [self.payload(child_id) for _ in range(count)]
        if tag_id == 10:
            compound = {}
            while True:
                child_id = self.ubyte()
                if child_id == 0:
                    break
                name = self.string()
                compound[name] = self.payload(child_id)
            return compound
        if tag_id == 11:
            return [self.int() for _ in range(self.int())]
        if tag_id == 12:
            return [self.fixed(_LONG) for _ in range(self.int())]
        raise ValueError(f"unknown NBT tag id {tag_id} at offset {self.pos}")


def parse_nbt(data: bytes):
    """A complete NBT byte string as (root name, root value)."""
    reader = _Reader(data)
    tag_id = reader.ubyte()
    if tag_id == 0:
        return None, None
    name = reader.string()
    return name, reader.payload(tag_id)


_HEADER_ENTRY = struct.Struct(">I")


def _iter_region_chunks(path: str):
    """The root compound of every chunk present in one region file."""
    with open(path, "rb") as handle:
        data = handle.read()
    if len(data) < 8192:
        return
    for entry_index in range(1024):
        entry = _HEADER_ENTRY.unpack_from(data, entry_index * 4)[0]
        offset = entry >> 8
        sector_count = entry & 0xFF
        if offset == 0 or sector_count == 0:
            continue
        start = offset * 4096
        if start + 5 > len(data):
            continue
        length = _HEADER_ENTRY.unpack_from(data, start)[0]
        if length <= 0 or start + 4 + length > len(data):
            continue
        compression = data[start + 4]
        payload = data[start + 5:start + 4 + length]
        if compression == 1:
            raw = gzip.decompress(payload)
        elif compression == 2:
            raw = zlib.decompress(payload)
        else:
            continue
        _, root = parse_nbt(raw)
        if root is not None:
            yield root


class World:
    """A loaded set of region files, indexed by chunk coordinate."""

    def __init__(self, region_dir: str) -> None:
        self.region_dir = region_dir
        self._chunks: dict[tuple[int, int], dict] = {}
        self._columns_cache = None
        self._bounds_cache = None
        self._bounds_computed = False
        if not os.path.isdir(region_dir):
            raise SystemExit(f"{region_dir}: not a directory (expected a world's region/)")
        for filename in sorted(os.listdir(region_dir)):
            if not (filename.startswith("r.") and filename.endswith(".mca")):
                continue
            for root in _iter_region_chunks(os.path.join(region_dir, filename)):
                level = root.get("Level")
                if level is None:
                    continue
                chunk_x, chunk_z = level.get("xPos"), level.get("zPos")
                if chunk_x is None or chunk_z is None:
                    continue
                self._chunks[(chunk_x, chunk_z)] = level

    @property
    def chunk_count(self) -> int:
        return len(self._chunks)

    def get(self, x: int, y: int, z: int) -> tuple[int, int]:
        """The block at a position as (id, data); air where nothing is."""
        if y < 0 or y > 255:
            return (0, 0)
        level = self._chunks.get((x >> 4, z >> 4))
        if level is None:
            return (0, 0)
        section_y = y >> 4
        for section in level.get("Sections") or ():
            if section.get("Y") != section_y:
                continue
            blocks = section.get("Blocks")
            if blocks is None:
                return (0, 0)
            index = ((y & 15) << 8) | ((z & 15) << 4) | (x & 15)
            block_id = blocks[index]
            add = section.get("Add")
            if add is not None:
                add_byte = add[index >> 1]
                block_id |= ((add_byte >> 4) if (index & 1) else (add_byte & 0x0F)) << 8
            data_arr = section.get("Data")
            data_val = 0
            if data_arr is not None:
                data_byte = data_arr[index >> 1]
                data_val = (data_byte >> 4) if (index & 1) else (data_byte & 0x0F)
            return (block_id, data_val)
        return (0, 0)

    def blocks(self):
        """Every non-air block as (x, y, z, id, data)."""
        for (chunk_x, chunk_z), level in self._chunks.items():
            base_x, base_z = chunk_x << 4, chunk_z << 4
            for section in level.get("Sections") or ():
                blocks = section.get("Blocks")
                if blocks is None:
                    continue
                base_y = section.get("Y", 0) << 4
                add = section.get("Add")
                data_arr = section.get("Data")
                for index in range(4096):
                    block_id = blocks[index]
                    if add is not None:
                        add_byte = add[index >> 1]
                        add_nibble = (add_byte >> 4) if (index & 1) else (add_byte & 0x0F)
                        if add_nibble:
                            block_id |= add_nibble << 8
                    if block_id == 0:
                        continue
                    data_val = 0
                    if data_arr is not None:
                        data_byte = data_arr[index >> 1]
                        data_val = (data_byte >> 4) if (index & 1) else (data_byte & 0x0F)
                    yield (base_x | (index & 15), base_y | (index >> 8), base_z | ((index >> 4) & 15),
                           block_id, data_val)

    def columns(self):
        """`{(x, z): [(y, id, data), ...]}`, each column sorted by y and holding non-air only. Built once."""
        if self._columns_cache is not None:
            return self._columns_cache
        columns: dict[tuple[int, int], list[tuple[int, int, int]]] = {}
        for x, y, z, block_id, data_val in self.blocks():
            columns.setdefault((x, z), []).append((y, block_id, data_val))
        for entry in columns.values():
            entry.sort(key=lambda item: item[0])
        self._columns_cache = columns
        return columns

    def voxels(self):
        """`{(x, y, z): (id, data)}` over every non-air block — the shape a diff between two worlds wants."""
        return {(x, y, z): (i, d) for (x, z), col in self.columns().items() for y, i, d in col}

    def bounds(self):
        """(minx, miny, minz, maxx, maxy, maxz) over non-air blocks, or None for an empty world."""
        if self._bounds_computed:
            return self._bounds_cache
        lo = hi = None
        for x, y, z, _i, _d in self.blocks():
            if lo is None:
                lo, hi = [x, y, z], [x, y, z]
            else:
                lo[0] = min(lo[0], x); lo[1] = min(lo[1], y); lo[2] = min(lo[2], z)
                hi[0] = max(hi[0], x); hi[1] = max(hi[1], y); hi[2] = max(hi[2], z)
        self._bounds_cache = None if lo is None else (lo[0], lo[1], lo[2], hi[0], hi[1], hi[2])
        self._bounds_computed = True
        return self._bounds_cache

    def tile_entities(self):
        return [entity for level in self._chunks.values() for entity in (level.get("TileEntities") or ())]

    def entities(self):
        return [entity for level in self._chunks.values() for entity in (level.get("Entities") or ())]

    def biome(self, x: int, z: int):
        level = self._chunks.get((x >> 4, z >> 4))
        if level is None:
            return None
        biomes = level.get("Biomes")
        if not biomes:
            return None
        index = ((z & 15) << 4) | (x & 15)
        return biomes[index] if index < len(biomes) else None


# The block ids the world tools agree on: what a tree is, what water is, what a plant is, and the names a
# census prints. One place, so the diff, the lift and the tree tools cannot drift apart on what a leaf is.
WOOD = {17, 162}
LEAF = {18, 161}
PLANT = {31, 175, 37, 38, 6, 30, 78}
TREE = WOOD | LEAF | PLANT
CARPENTRY = {125, 126, 85, 106, 53, 134, 135, 136, 163, 164}
WATER = {8, 9}

NAMES = {1: "stone", 2: "grass", 3: "dirt", 4: "cobble", 5: "planks", 7: "bedrock", 9: "water", 8: "water",
         12: "sand", 13: "gravel", 17: "log", 18: "leaves", 20: "glass", 24: "sandstone", 30: "cobweb",
         31: "tallgrass", 35: "wool", 41: "gold", 42: "iron", 43: "dslab", 44: "slab", 45: "brick",
         47: "bookshelf", 48: "mossy", 49: "obsidian", 53: "oakstair", 54: "chest", 57: "diamond", 64: "door",
         65: "ladder", 67: "cobstair", 85: "fence", 89: "glowstone", 95: "sglass", 98: "sbrick", 101: "ironbars",
         102: "pane", 106: "vine", 108: "brickstair", 109: "sbstair", 126: "wslab", 129: "emeraldore",
         134: "sprstair", 135: "birstair", 136: "junstair", 138: "beacon", 139: "cobwall", 140: "flowerpot",
         144: "skull", 145: "anvil", 155: "quartz", 156: "qstair", 159: "clay", 160: "spane", 161: "leaves2",
         162: "log2", 163: "acastair", 164: "doakstair", 168: "prismarine", 171: "carpet", 174: "packedice",
         175: "dplant"}


def name(block) -> str:
    """`mossy`, `clay:9`, `35:14` — a block as a census prints it."""
    block_id, data = block
    base = NAMES.get(block_id, str(block_id))
    return f"{base}:{data}" if data else base


def census(counter, limit=8) -> str:
    total = sum(counter.values())
    if not total:
        return "(nothing)"
    return ", ".join(f"{name(block)} {count * 100 / total:.0f}%" for block, count in counter.most_common(limit))


if __name__ == "__main__":
    import sys
    import time
    from collections import Counter

    if len(sys.argv) < 2:
        raise SystemExit(f"usage: python3 {sys.argv[0]} <regionDir>")
    started = time.perf_counter()
    world = World(sys.argv[1])
    counts = Counter()
    total = 0
    for _x, _y, _z, block_id, data_val in world.blocks():
        counts[(block_id, data_val)] += 1
        total += 1
    print(f"region dir: {sys.argv[1]}")
    print(f"chunks: {world.chunk_count}   non-air blocks: {total}   bounds: {world.bounds()}")
    print("the fifteen commonest id:data")
    for (block_id, data_val), count in counts.most_common(15):
        print(f"  {block_id:3}:{data_val:<3} {count:9}  {name((block_id, data_val))}")
    print(f"read in {time.perf_counter() - started:.1f}s")
