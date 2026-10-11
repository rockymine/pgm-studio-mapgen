"""Turn the red half onto blue: half a turn about the board's centre, (x, z) -> (-1 - x, -1 - z), with every
block that faces a way turned with it. A half-turn keeps a door's hinge on its own side, which a mirror
does not.
"""
import numpy as np

STAIRS = [53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 163, 164, 180]
DOORS = [64, 71, 193, 194, 195, 196, 197]
FACING6 = [23, 54, 61, 62, 65, 68, 146, 158, 177, 144]       # 2 north 3 south 4 west 5 east
GATES = [107, 183, 184, 185, 186, 187]


def data_table():
    t = np.tile(np.arange(16, dtype=np.uint8), (256, 1))
    for d in range(16):
        f = d & 3
        for i in STAIRS:
            t[i, d] = (d & ~3) | {0: 1, 1: 0, 2: 3, 3: 2}[f]
        for i in DOORS:
            t[i, d] = d if d & 8 else (d & ~3) | ((f + 2) % 4)
        for i in FACING6:
            t[i, d] = {2: 3, 3: 2, 4: 5, 5: 4}.get(d, d)
        for i in (50, 75, 76, 77, 143):
            t[i, d] = {1: 2, 2: 1, 3: 4, 4: 3}.get(d, d)
        for i in (63, 176):
            t[i, d] = (d + 8) % 16
        for i in (86, 91, 26):
            t[i, d] = (d & ~3) | ((f + 2) % 4)
        for g in GATES:
            t[g, d] = (d & ~3) | ((f + 2) % 4)
        t[106, d] = ((d & 1) << 2) | ((d & 4) >> 2) | ((d & 2) << 2) | ((d & 8) >> 2)
        t[96, d] = (d & ~3) | {0: 1, 1: 0, 2: 3, 3: 2}[f]
        t[167, d] = t[96, d]
        t[66, d] = {2: 3, 3: 2, 4: 5, 5: 4, 6: 8, 8: 6, 7: 9, 9: 7}.get(d, d)
        for r in (27, 28, 157):
            t[r, d] = (d & 8) | {2: 3, 3: 2, 4: 5, 5: 4}.get(d & 7, d & 7)
    return t


def rotate_world(w):
    """Every column x >= 0 becomes the turned image of column (-1 - x, -1 - z)."""
    assert w.x0 + w.sx - 1 == -1 - w.x0 and w.z0 + w.sz - 1 == -1 - w.z0, "the volume must be centred"
    half = -w.x0
    t = data_table()
    red_i = w.ids[:half].copy()
    red_d = w.dat[:half].copy()
    w.ids[half:] = red_i[::-1, :, ::-1]
    w.dat[half:] = t[red_i, red_d][::-1, :, ::-1]
    w.biome[half:] = w.biome[:half][::-1, ::-1]
    blue = []
    for te in w.tiles:
        if te["x"] < 0:
            m = dict(te)
            m["x"], m["z"] = -1 - te["x"], -1 - te["z"]
            blue.append(m)
    w.tiles = [te for te in w.tiles if te["x"] < 0] + blue
