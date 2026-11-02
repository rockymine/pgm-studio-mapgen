"""Write a {(x,y,z): (id,data)} dict as Minecraft 1.8 Anvil region files."""
import os, struct, zlib, time

def _tag_name(t, name):
    b = name.encode()
    return bytes([t]) + struct.pack(">H", len(b)) + b

def _payload(t, v):
    if t == 1: return struct.pack(">b", v)
    if t == 3: return struct.pack(">i", v)
    if t == 4: return struct.pack(">q", v)
    if t == 7: return struct.pack(">i", len(v)) + bytes(v)
    if t == 8:
        b = v.encode(); return struct.pack(">H", len(b)) + b
    if t == 11: return struct.pack(">i", len(v)) + struct.pack(">%di" % len(v), *v)
    if t == 9:
        et, items = v
        return bytes([et]) + struct.pack(">i", len(items)) + b"".join(_payload(et, i) for i in items)
    if t == 10:
        return b"".join(_tag_name(ct, k) + _payload(ct, cv) for k, (ct, cv) in v.items()) + b"\0"
    raise ValueError(t)

def nbt(root):
    return _tag_name(10, "") + _payload(10, root)

def write_world(blocks, region_dir, biome=12, tile_entities=()):
    os.makedirs(region_dir, exist_ok=True)
    for f in os.listdir(region_dir):
        if f.endswith(".mca"): os.remove(os.path.join(region_dir, f))
    chunks = {}
    for (x, y, z), (i, d) in blocks.items():
        if i == 0 or not (0 <= y < 256): continue
        chunks.setdefault((x >> 4, z >> 4), []).append((x & 15, y, z & 15, i, d))
    tes = {}
    for te in tile_entities:
        tes.setdefault((te["x"] >> 4, te["z"] >> 4), []).append(te)
    regions = {}
    now = int(time.time())
    for (cx, cz), cells in chunks.items():
        secs = {}
        height = [0] * 256
        for lx, y, lz, i, d in cells:
            s = secs.get(y >> 4)
            if s is None:
                s = secs[y >> 4] = [bytearray(4096), bytearray(2048)]
            idx = ((y & 15) * 16 + lz) * 16 + lx
            s[0][idx] = i & 255
            if d:
                if idx & 1: s[1][idx >> 1] |= (d & 15) << 4
                else: s[1][idx >> 1] |= d & 15
            h = lz * 16 + lx
            if y + 1 > height[h]: height[h] = y + 1
        sections = []
        for sy in sorted(secs):
            b, dd = secs[sy]
            sections.append({"Y": (1, sy), "Blocks": (7, b), "Data": (7, dd),
                             "BlockLight": (7, bytes(2048)), "SkyLight": (7, b"\xff" * 2048)})
        te_list = [{"id": (8, t["id"]), "x": (3, t["x"]), "y": (3, t["y"]), "z": (3, t["z"])} for t in tes.get((cx, cz), [])]
        level = {"xPos": (3, cx), "zPos": (3, cz), "LastUpdate": (4, 0), "InhabitedTime": (4, 0),
                 "TerrainPopulated": (1, 1), "LightPopulated": (1, 0), "V": (1, 1),
                 "Biomes": (7, bytes([biome]) * 256), "HeightMap": (11, height),
                 "Sections": (9, (10, sections)), "Entities": (9, (10, [])), "TileEntities": (9, (10, te_list))}
        data = zlib.compress(nbt({"Level": (10, level)}))
        regions.setdefault((cx >> 5, cz >> 5), {})[(cx & 31, cz & 31)] = data
    for (rx, rz), cks in regions.items():
        header = bytearray(8192); body = bytearray(); sector = 2
        for (lx, lz), data in cks.items():
            payload = struct.pack(">IB", len(data) + 1, 2) + data
            payload += b"\0" * ((-len(payload)) % 4096)
            n = len(payload) // 4096
            off = 4 * (lx + lz * 32)
            header[off:off + 4] = struct.pack(">I", (sector << 8) | n)
            header[4096 + off:4096 + off + 4] = struct.pack(">I", now)
            body += payload; sector += n
        with open(os.path.join(region_dir, f"r.{rx}.{rz}.mca"), "wb") as fh:
            fh.write(header + body)
    return len(chunks), len(regions)
