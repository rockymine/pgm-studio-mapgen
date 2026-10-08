"""The voxel volume a generator writes into, and the bridge to the studio's Anvil writer.

Everything is numpy: ids uint16 and data uint8 over (x, y, z), offset by the world origin, so a builder says
`w.set(x, y, z, B.STONE)` in world coordinates and a terrain pass can write whole columns at once. y runs from 0
to sy - 1 and is the block's own height; a player standing on a block at y stands at y + 1.

    w = World(-100, -100, 200, 200, sy=160)
    ...
    w.save(build_dir, "Name", spawn)          # volume.bin, tiles.json, level.json
    write(build_dir, world_dir)               # region files through data/write_world.cs
    w2 = World.load(build_dir)                # read a build back
"""
import hashlib
import json
import os
import struct
import subprocess

import numpy as np

from .blocks import B, NOT_GROUND

HERE = os.path.dirname(os.path.abspath(__file__))


def seed(board, name):
    """A reproducible seed for one named random stream of one board, distinct from every other name: pass the
    generator it makes round explicitly rather than keeping one at module level."""
    h = hashlib.sha256(f"{board}/{name}".encode()).digest()
    return int.from_bytes(h[:8], "little")


def rng(board, name):
    return np.random.default_rng(seed(board, name))


class World:
    """A box of the world: x in [x0, x0+sx), y in [0, sy), z in [z0, z0+sz)."""

    def __init__(self, x0, z0, sx, sz, sy=128):
        self.x0, self.z0, self.sx, self.sy, self.sz = x0, z0, sx, sy, sz
        self.ids = np.zeros((sx, sy, sz), dtype=np.uint16)
        self.dat = np.zeros((sx, sy, sz), dtype=np.uint8)
        self.biome = np.full((sx, sz), 1, dtype=np.uint8)
        self.tiles = []

    # --- coordinates -----------------------------------------------------------------------------------
    def inside(self, x, y, z):
        return 0 <= x - self.x0 < self.sx and 0 <= y < self.sy and 0 <= z - self.z0 < self.sz

    def index(self, x, y, z):
        return x - self.x0, y, z - self.z0

    def grid(self):
        """X and Z arrays of the world coordinates of every column, shaped (sx, sz)."""
        return np.meshgrid(np.arange(self.x0, self.x0 + self.sx), np.arange(self.z0, self.z0 + self.sz),
                           indexing="ij")

    # --- blocks ----------------------------------------------------------------------------------------
    def set(self, x, y, z, bid, d=0):
        if self.inside(x, y, z):
            self.ids[x - self.x0, y, z - self.z0] = bid
            self.dat[x - self.x0, y, z - self.z0] = d

    def get(self, x, y, z):
        if not self.inside(x, y, z):
            return (0, 0)
        return int(self.ids[x - self.x0, y, z - self.z0]), int(self.dat[x - self.x0, y, z - self.z0])

    def id(self, x, y, z):
        return self.get(x, y, z)[0]

    def fill(self, xa, ya, za, xb, yb, zb, bid, d=0):
        """Inclusive box, clipped to the volume."""
        xa, xb = sorted((xa, xb)); ya, yb = sorted((ya, yb)); za, zb = sorted((za, zb))
        xa = max(xa, self.x0); xb = min(xb, self.x0 + self.sx - 1)
        za = max(za, self.z0); zb = min(zb, self.z0 + self.sz - 1)
        ya = max(ya, 0); yb = min(yb, self.sy - 1)
        if xa > xb or ya > yb or za > zb:
            return
        sl = (slice(xa - self.x0, xb - self.x0 + 1), slice(ya, yb + 1), slice(za - self.z0, zb - self.z0 + 1))
        self.ids[sl] = bid
        self.dat[sl] = d

    def column(self, x, z, y0, y1, bid, d=0):
        """Fill one column from y0 to y1 inclusive."""
        if 0 <= x - self.x0 < self.sx and 0 <= z - self.z0 < self.sz:
            a, b = max(0, min(y0, y1)), min(self.sy - 1, max(y0, y1))
            self.ids[x - self.x0, a:b + 1, z - self.z0] = bid
            self.dat[x - self.x0, a:b + 1, z - self.z0] = d

    def top(self, x, z, ignore=NOT_GROUND):
        """The y of the highest ground block in a column, or -1."""
        if not (0 <= x - self.x0 < self.sx and 0 <= z - self.z0 < self.sz):
            return -1
        col = self.ids[x - self.x0, :, z - self.z0]
        keep = ~np.isin(col, sorted(ignore))
        nz = np.nonzero(keep)[0]
        return int(nz[-1]) if len(nz) else -1

    def heightmap(self, ignore=NOT_GROUND):
        """The top() of every column, shaped (sx, sz)."""
        keep = ~np.isin(self.ids, sorted(ignore))
        any_ = keep.any(axis=1)
        top = self.sy - 1 - np.argmax(keep[:, ::-1, :], axis=1)
        return np.where(any_, top, -1)

    # --- tile entities ---------------------------------------------------------------------------------
    def chest(self, x, y, z, items, facing=2):
        """items: [(slot, 'minecraft:id', count, damage)]. facing 2 north 3 south 4 west 5 east."""
        self.set(x, y, z, B.CHEST, facing)
        self.tiles.append({"kind": "Chest", "x": x, "y": y, "z": z,
                           "items": [{"slot": s, "id": i, "count": c, "damage": d} for s, i, c, d in items]})

    def sign(self, x, y, z, lines, wall_facing=None, rot=0):
        if wall_facing is None:
            self.set(x, y, z, B.SIGN_POST, rot)
        else:
            self.set(x, y, z, B.WALL_SIGN, wall_facing)
        self.tiles.append({"kind": "Sign", "x": x, "y": y, "z": z, "lines": list(lines)})

    def banner(self, x, y, z, base, patterns=(), wall_facing=None, rot=0):
        """A banner, standing (rot 0..15) or on a wall (facing 2 north 3 south 4 west 5 east); base is the dye
        colour in the banner's own numbering (0 black .. 15 white); patterns are (code, dye) pairs."""
        if wall_facing is None:
            self.set(x, y, z, B.BANNER, rot)
        else:
            self.set(x, y, z, B.WALL_BANNER, wall_facing)
        self.tiles.append({"kind": "Banner", "x": x, "y": y, "z": z, "base": base,
                           "patterns": [{"pattern": p, "color": c} for p, c in patterns]})

    # --- output ----------------------------------------------------------------------------------------
    def save(self, build_dir, name, spawn):
        os.makedirs(build_dir, exist_ok=True)
        with open(os.path.join(build_dir, "volume.bin"), "wb") as f:
            f.write(b"RWV1")
            f.write(struct.pack("<6i", self.x0, 0, self.z0, self.sx, self.sy, self.sz))
            f.write(np.ascontiguousarray(self.ids, dtype="<u2").tobytes())
            f.write(np.ascontiguousarray(self.dat).tobytes())
            f.write(np.ascontiguousarray(self.biome).tobytes())
        with open(os.path.join(build_dir, "tiles.json"), "w") as f:
            json.dump(self.tiles, f)
        with open(os.path.join(build_dir, "level.json"), "w") as f:
            json.dump({"name": name, "spawn": list(spawn)}, f)

    @classmethod
    def load(cls, build_dir):
        """A world back from what save() wrote."""
        with open(os.path.join(build_dir, "volume.bin"), "rb") as f:
            assert f.read(4) == b"RWV1"
            x0, y0, z0, sx, sy, sz = struct.unpack("<6i", f.read(24))
            n = sx * sy * sz
            w = cls(x0, z0, sx, sz, sy)
            w.ids = np.frombuffer(f.read(n * 2), dtype="<u2").reshape(sx, sy, sz).copy()
            w.dat = np.frombuffer(f.read(n), dtype=np.uint8).reshape(sx, sy, sz).copy()
            rest = f.read(sx * sz)
            if len(rest) == sx * sz:
                w.biome = np.frombuffer(rest, dtype=np.uint8).reshape(sx, sz).copy()
        tiles = os.path.join(build_dir, "tiles.json")
        if os.path.exists(tiles):
            with open(tiles) as f:
                w.tiles = json.load(f)
        return w


def studio_root():
    """Where the studio is checked out: PGM_STUDIO_ROOT, else the sibling of this repository."""
    env = os.environ.get("PGM_STUDIO_ROOT")
    if env:
        return env
    return os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "pgm-studio"))


def write(build_dir, world_dir):
    """Write region files and level.dat from a saved build, through the studio's own Anvil writer."""
    script = os.path.join(HERE, "data", "write_world.cs")
    env = dict(os.environ, PGM_STUDIO_ROOT=studio_root())
    r = subprocess.run(["dotnet", "run", script, "--", os.path.abspath(build_dir), os.path.abspath(world_dir)],
                       cwd="/tmp", env=env, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-2000:] or r.stdout[-2000:])
    return r.stdout.strip()
