"""Which way a block faces, and what its data becomes when a board is mirrored or turned.

One vocabulary for directions: "e", "w", "s", "n" (x east, z south), or a (dx, dz) offset. The helpers write
the data value for a block facing a way, so a generator never types a ladder's 2-5 or a stair's 0-3 by hand.

The turn tables come from two places. For logs, stairs, chests, ladders, wall signs, torches, fence gates and
vines they are the studio's own (`BlockGeometry.Turned`, read from `data/blocks.json`). The studio leaves
doors, trapdoors, rails, sign posts, banners, pumpkins, beds, buttons, levers, repeaters, hay, quartz pillars
and wall banners alone, since a copied studio prop keeps the way it was drawn; a freeform board turns whole
halves, so this module adds those families, each turned through its own direction encoding.

Five operations, named as the studio's export names them:

    cw, ccw     a quarter turn seen from above (east to south is cw)
    half        a half turn
    mirror_x    east and west swapped
    mirror_z    north and south swapped
"""
import numpy as np

from . import blocks as K
from .blocks import B

DIRS = {"e": (1, 0), "w": (-1, 0), "s": (0, 1), "n": (0, -1)}
NAMES = {v: k for k, v in DIRS.items()}
OPS = {
    "cw": lambda x, z: (-z, x),
    "ccw": lambda x, z: (z, -x),
    "half": lambda x, z: (-x, -z),
    "mirror_x": lambda x, z: (-x, z),
    "mirror_z": lambda x, z: (x, -z),
}


def vec(d):
    """A direction as a unit (dx, dz): accepts "e"/"w"/"s"/"n" or an offset."""
    if isinstance(d, str):
        return DIRS[d.lower()[0]]
    dx, dz = d
    if abs(dx) >= abs(dz):
        return (1 if dx > 0 else -1, 0)
    return (0, 1 if dz > 0 else -1)


def opposite(d):
    dx, dz = vec(d)
    return NAMES[(-dx, -dz)]


# ---- writing a block that faces a way --------------------------------------------------------------------
def stair(rises, upside_down=False):
    """Stairs climbing toward a side: walking that way you go up."""
    return {"e": 0, "w": 1, "s": 2, "n": 3}[NAMES[vec(rises)]] | (4 if upside_down else 0)


def ladder(on_wall):
    """A ladder (or wall sign, wall banner) hung on the wall at that side of it."""
    return {"n": 3, "s": 2, "w": 5, "e": 4}[NAMES[vec(on_wall)]]


wall_sign = ladder


def torch(on_wall=None):
    """A torch on the wall at that side, or standing (None)."""
    if on_wall is None:
        return 5
    return {"w": 1, "e": 2, "n": 3, "s": 4}[NAMES[vec(on_wall)]]


def log_axis(along=None, wood=0):
    """A log lying along x or z ("e"/"w" or "n"/"s"), or upright (None)."""
    if along is None:
        return wood
    return wood | (4 if vec(along)[0] else 8)


def slab(kind=0, upper=False):
    return kind | (8 if upper else 0)


def door(facing, upper=False, hinge_right=False, open_=False):
    """A door's two halves: the lower carries the facing (the way it looks when shut), the upper the hinge."""
    if upper:
        return 8 | (1 if hinge_right else 0)
    return {"e": 0, "s": 1, "w": 2, "n": 3}[NAMES[vec(facing)]] | (4 if open_ else 0)


def yaw(d):
    """Minecraft yaw for a player looking that way: 0 south, 90 west, 180 north, -90 east."""
    dx, dz = d if not isinstance(d, str) else DIRS[d]
    return round(np.degrees(np.arctan2(-dx, dz)))


def rotation16(d):
    """A sign post's or standing banner's 0-15 rotation for facing that way (0 south, 4 west)."""
    dx, dz = (d if not isinstance(d, str) else DIRS[d])
    a = np.degrees(np.arctan2(-dx, dz)) % 360
    return int(round(a / 22.5)) % 16


# ---- the supplement: families the studio leaves alone ---------------------------------------------------
def _dir_family(table):
    """A turn for a family whose low bits name a direction: table maps value -> (dx, dz)."""
    inv = {v: k for k, v in table.items()}

    def turn(d, op, mask):
        low = d & mask
        if low not in table:
            return d
        t = vec(OPS[op](*table[low]))
        return (d & ~mask) | inv[t]
    return turn


_RAIL_STRAIGHT = {0: "ns", 1: "ew"}
_RAIL_SLOPE = {2: (1, 0), 3: (-1, 0), 4: (0, -1), 5: (0, 1)}               # ascending toward
_RAIL_CURVE = {6: ((0, 1), (1, 0)), 7: ((0, 1), (-1, 0)), 8: ((0, -1), (-1, 0)), 9: ((0, -1), (1, 0))}


def _rail(d, op, low_mask=15, curves=True):
    low = d & low_mask
    hi = d & ~low_mask
    if low in _RAIL_STRAIGHT:
        if op in ("cw", "ccw"):
            return hi | (1 - low)
        return d
    if low in _RAIL_SLOPE:
        t = vec(OPS[op](*_RAIL_SLOPE[low]))
        return hi | {v: k for k, v in _RAIL_SLOPE.items()}[t]
    if curves and low in _RAIL_CURVE:
        a, b = _RAIL_CURVE[low]
        ta, tb = vec(OPS[op](*a)), vec(OPS[op](*b))
        for k, (ca, cb) in _RAIL_CURVE.items():
            if {ca, cb} == {ta, tb}:
                return hi | k
    return d


_door_lower = _dir_family({0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)})
_trapdoor = _dir_family({0: (0, 1), 1: (0, -1), 2: (1, 0), 3: (-1, 0)})
_pumpkin = _dir_family({0: (0, 1), 1: (-1, 0), 2: (0, -1), 3: (1, 0)})
_button = _dir_family({1: (1, 0), 2: (-1, 0), 3: (0, 1), 4: (0, -1)})
_repeater = _dir_family({0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)})
_wall = _dir_family({2: (0, -1), 3: (0, 1), 4: (-1, 0), 5: (1, 0)})


def _door(d, op):
    if d & 8:                                                    # the upper half: a mirror swaps the hinge
        return d ^ 1 if op.startswith("mirror") else d
    return _door_lower(d, op, 3)


def _rotation16(d, op):
    a = np.radians(d * 22.5)
    dx, dz = -np.sin(a), np.cos(a)                               # 0 faces south
    tx, tz = OPS[op](dx, dz)
    return int(round((np.degrees(np.arctan2(-tx, tz)) % 360) / 22.5)) % 16


def _axis_bits(d, op, x_bit, z_bit):
    if op not in ("cw", "ccw"):
        return d
    if d & (x_bit | z_bit) in (x_bit, z_bit):
        return d ^ (x_bit | z_bit)
    return d


def _quartz(d, op):
    if op in ("cw", "ccw") and d in (3, 4):
        return 7 - d
    return d


SUPPLEMENT = {
    **{i: _door for i in K.DOORS},
    B.TRAPDOOR: lambda d, op: _trapdoor(d, op, 3),
    B.IRON_TRAPDOOR: lambda d, op: _trapdoor(d, op, 3),
    B.RAIL: lambda d, op: _rail(d, op),
    **{i: (lambda d, op: _rail(d, op, 7, curves=False)) for i in (B.RAIL_POWERED, B.RAIL_DETECTOR, B.RAIL_ACTIVATOR)},
    B.SIGN_POST: _rotation16,
    B.BANNER: _rotation16,
    B.WALL_BANNER: lambda d, op: _wall(d, op, 7),
    B.PUMPKIN: lambda d, op: _pumpkin(d, op, 3),
    B.JACK: lambda d, op: _pumpkin(d, op, 3),
    B.BED: lambda d, op: _pumpkin(d, op, 3),
    B.BUTTON_STONE: lambda d, op: _button(d, op, 7),
    B.BUTTON_WOOD: lambda d, op: _button(d, op, 7),
    B.LEVER: lambda d, op: _button(d, op, 7),
    93: lambda d, op: _repeater(d, op, 3), 94: lambda d, op: _repeater(d, op, 3),
    149: lambda d, op: _repeater(d, op, 3), 150: lambda d, op: _repeater(d, op, 3),
    B.HAY: lambda d, op: _axis_bits(d, op, 4, 8),
    B.QUARTZ: _quartz,
}


def data_table(op):
    """A (256, 16) table: the data each (id, data) takes under the operation."""
    t = np.zeros((256, 16), dtype=np.uint8)
    for i in range(256):
        row = K.TABLE[i]["turned"][op]
        for d in range(16):
            t[i, d] = SUPPLEMENT[i](d, op) if i in SUPPLEMENT else row[d]
    return t


_TABLES = {}


def turn_data(bid, data, op):
    if op not in _TABLES:
        _TABLES[op] = data_table(op)
    return int(_TABLES[op][int(bid), int(data) & 15])


def turn_xz(x, z, op, axis=(-0.5, -0.5)):
    """Where a block lands under the operation, about the axis (cx, cz): the half-integer -0.5 is the line
    between blocks -1 and 0, so (x, z) -> (-1 - x, -1 - z) under a half turn; 0.0 turns about block 0."""
    cx, cz = axis
    dx, dz = OPS[op](x - cx, z - cz)
    return int(round(cx + dx)), int(round(cz + dz))


def turn_world(w, op, keep, axis=(-0.5, -0.5), recolour=None):
    """Copy the part of the world where keep(x, z) is True onto its image under the operation, turning every
    block's data with it. Only mirrors and the half turn are supported on a whole world, so the image stays
    inside the volume; recolour maps (id, data) -> (id, data) on the image, for a team's colours."""
    assert op in ("half", "mirror_x", "mirror_z"), "a whole world turns by half or by a mirror"
    t = data_table(op)
    ids, dat = w.ids, w.dat
    xs = np.arange(w.x0, w.x0 + w.sx)
    zs = np.arange(w.z0, w.z0 + w.sz)
    src_x, src_z = np.meshgrid(xs, zs, indexing="ij")
    k = np.vectorize(keep)(src_x, src_z) if callable(keep) else keep
    img = np.vectorize(lambda x, z: turn_xz(x, z, op, axis), otypes=[int, int])(src_x[k], src_z[k])
    ix, iz = img[0] - w.x0, img[1] - w.z0
    ok = (0 <= ix) & (ix < w.sx) & (0 <= iz) & (iz < w.sz)
    si, sk = np.nonzero(k)
    si, sk, ix, iz = si[ok], sk[ok], ix[ok], iz[ok]
    col_ids = ids[si, :, sk]
    col_dat = t[col_ids, dat[si, :, sk]]
    if recolour:
        for (a, ad), (b, bd) in recolour.items():
            m = (col_ids == a) & ((col_dat == ad) if ad is not None else True)
            col_ids = np.where(m, b, col_ids)
            col_dat = np.where(m, bd if bd is not None else col_dat, col_dat)
    ids[ix, :, iz] = col_ids
    dat[ix, :, iz] = col_dat
    w.biome[ix, iz] = w.biome[si, sk]
    kept = k if not callable(keep) else None

    def in_keep(x, z):
        if callable(keep):
            return bool(keep(x, z))
        return bool(kept[x - w.x0, z - w.z0])
    images = []
    for te in w.tiles:                                           # chests, signs, banners go with their blocks
        if in_keep(te["x"], te["z"]):
            m = dict(te)
            m["x"], m["z"] = turn_xz(te["x"], te["z"], op, axis)
            images.append(m)
    taken = {(m["x"], m["y"], m["z"]) for m in images}
    w.tiles = [te for te in w.tiles if (te["x"], te["y"], te["z"]) not in taken] + images
    return w
