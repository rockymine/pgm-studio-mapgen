"""Set single blocks in a copy of a 1.8 Anvil world, keeping everything else in it (tile entities, entities, lighting
flags) as it was. NBT is read and written losslessly as (tag type, value) pairs."""
import io
import os
import struct
import zlib


def _read(f, t):
    if t == 1: return struct.unpack(">b", f.read(1))[0]
    if t == 2: return struct.unpack(">h", f.read(2))[0]
    if t == 3: return struct.unpack(">i", f.read(4))[0]
    if t == 4: return struct.unpack(">q", f.read(8))[0]
    if t == 5: return struct.unpack(">f", f.read(4))[0]
    if t == 6: return struct.unpack(">d", f.read(8))[0]
    if t == 7: n = struct.unpack(">i", f.read(4))[0]; return bytearray(f.read(n))
    if t == 8: n = struct.unpack(">H", f.read(2))[0]; return f.read(n).decode("utf-8")
    if t == 9:
        et = f.read(1)[0]; n = struct.unpack(">i", f.read(4))[0]
        return (et, [_read(f, et) for _ in range(n)])
    if t == 10:
        out = []
        while True:
            ct = f.read(1)[0]
            if ct == 0: return out
            n = struct.unpack(">H", f.read(2))[0]; name = f.read(n).decode("utf-8")
            out.append([name, ct, _read(f, ct)])
    if t == 11: n = struct.unpack(">i", f.read(4))[0]; return list(struct.unpack(f">{n}i", f.read(4 * n)))
    raise ValueError(f"tag {t}")


def _write(f, t, v):
    if t == 1: f.write(struct.pack(">b", v))
    elif t == 2: f.write(struct.pack(">h", v))
    elif t == 3: f.write(struct.pack(">i", v))
    elif t == 4: f.write(struct.pack(">q", v))
    elif t == 5: f.write(struct.pack(">f", v))
    elif t == 6: f.write(struct.pack(">d", v))
    elif t == 7: f.write(struct.pack(">i", len(v))); f.write(bytes(v))
    elif t == 8: b = v.encode("utf-8"); f.write(struct.pack(">H", len(b))); f.write(b)
    elif t == 9:
        et, items = v; f.write(bytes([et])); f.write(struct.pack(">i", len(items)))
        for item in items: _write(f, et, item)
    elif t == 10:
        for name, ct, cv in v:
            f.write(bytes([ct])); b = name.encode("utf-8"); f.write(struct.pack(">H", len(b))); f.write(b); _write(f, ct, cv)
        f.write(b"\x00")
    elif t == 11: f.write(struct.pack(">i", len(v))); f.write(struct.pack(f">{len(v)}i", *v))


def load(data):
    f = io.BytesIO(data); t = f.read(1)[0]; n = struct.unpack(">H", f.read(2))[0]; name = f.read(n).decode()
    return name, _read(f, t)


def dump(name, root):
    f = io.BytesIO(); f.write(b"\x0a"); b = name.encode(); f.write(struct.pack(">H", len(b))); f.write(b)
    _write(f, 10, root); return f.getvalue()


def get(compound, key):
    for entry in compound:
        if entry[0] == key: return entry
    return None


def set_blocks(region_dir, blocks):
    """blocks: {(x, y, z): (id, data)}. Returns how many were set."""
    by_region = {}
    for (x, y, z), b in blocks.items():
        by_region.setdefault((x >> 9, z >> 9), {})[(x, y, z)] = b
    done = 0
    for (rx, rz), mine in by_region.items():
        path = os.path.join(region_dir, f"r.{rx}.{rz}.mca")
        raw = bytearray(open(path, "rb").read()) if os.path.exists(path) else bytearray(8192)
        chunks = {}
        for i in range(1024):
            off = int.from_bytes(raw[4 * i:4 * i + 3], "big"); cnt = raw[4 * i + 3]
            if off == 0 or cnt == 0: continue
            length = int.from_bytes(raw[off * 4096:off * 4096 + 4], "big")
            comp = raw[off * 4096 + 4]
            payload = bytes(raw[off * 4096 + 5:off * 4096 + 4 + length])
            stamp = raw[4096 + 4 * i:4096 + 4 * i + 4]
            chunks[i] = [comp, payload, bytes(stamp)]
        edits = {}
        for (x, y, z), b in mine.items():
            edits.setdefault(((x & 511) >> 4) + 32 * ((z & 511) >> 4), []).append((x, y, z, b))
        for i, todo in edits.items():
            if i in chunks:
                comp, payload, stamp = chunks[i]
                data = zlib.decompress(payload) if comp == 2 else __import__("gzip").decompress(payload)
                name, root = load(data)
            else:                                    # an empty chunk, as 1.8 saves one
                cx, cz = rx * 32 + i % 32, rz * 32 + i // 32
                name, stamp = "", bytes(4)
                root = [["Level", 10, [["xPos", 3, cx], ["zPos", 3, cz], ["LastUpdate", 4, 0], ["LightPopulated", 1, 0],
                                       ["TerrainPopulated", 1, 1], ["V", 1, 1], ["InhabitedTime", 4, 0],
                                       ["Biomes", 7, bytearray([12] * 256)], ["HeightMap", 11, [0] * 256],
                                       ["Sections", 9, (10, [])], ["Entities", 9, (10, [])], ["TileEntities", 9, (10, [])]]]]
            level = get(root, "Level")[2]
            sections = get(level, "Sections")[2]
            for x, y, z, (bid, bdata) in todo:
                sy = y >> 4
                sec = next((s for s in sections[1] if get(s, "Y")[2] == sy), None)
                if sec is None:
                    sec = [["Y", 1, sy], ["Blocks", 7, bytearray(4096)], ["Data", 7, bytearray(2048)],
                           ["BlockLight", 7, bytearray(2048)], ["SkyLight", 7, bytearray(b"\xff" * 2048)]]
                    sections[1].append(sec)
                idx = ((y & 15) << 8) | ((z & 15) << 4) | (x & 15)
                get(sec, "Blocks")[2][idx] = bid & 255
                d = get(sec, "Data")[2]
                d[idx >> 1] = (d[idx >> 1] & 0xF0) | bdata if idx % 2 == 0 else (d[idx >> 1] & 0x0F) | (bdata << 4)
                done += 1
            lp = get(level, "LightPopulated")
            if lp: lp[2] = 0                       # let the server light the chunk again
            chunks[i] = [2, zlib.compress(dump(name, root)), stamp]
        out = bytearray(8192); sector = 2
        for i in sorted(chunks):
            comp, payload, stamp = chunks[i]
            body = (len(payload) + 1).to_bytes(4, "big") + bytes([comp]) + payload
            n = (len(body) + 4095) // 4096
            out[4 * i:4 * i + 3] = sector.to_bytes(3, "big"); out[4 * i + 3] = n
            out[4096 + 4 * i:4096 + 4 * i + 4] = stamp
            out += body + bytes(n * 4096 - len(body)); sector += n
        open(path, "wb").write(out)
    return done
