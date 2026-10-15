"""Copy the red half onto blue across the rift (x' = -1 - x), turning every block that faces a way."""
import numpy as np

from mc import B

STAIRS = [53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 163, 164, 180]
DOORS = [64, 71, 193, 194, 195, 196, 197]
FACING6 = [23, 54, 61, 62, 65, 68, 146, 158, 177, 144]       # 2 north 3 south 4 west 5 east
GATES = [107, 183, 184, 185, 186, 187]


def data_table():
    t = np.tile(np.arange(16, dtype=np.uint8), (256, 1))
    for i in STAIRS:
        for d in range(16):
            f = d & 3
            t[i, d] = (d & ~3) | {0: 1, 1: 0}.get(f, f)
    for i in DOORS:
        for d in range(16):
            if d & 8:
                t[i, d] = d ^ 1                      # upper half: the hinge changes side
            else:
                f = d & 3
                t[i, d] = (d & ~3) | {0: 2, 2: 0}.get(f, f)
    for i in FACING6:
        for d in range(16):
            t[i, d] = {4: 5, 5: 4}.get(d, d)
    for i in (50, 75, 76, 77, 143):
        for d in range(16):
            t[i, d] = {1: 2, 2: 1}.get(d, d)
    for i in (63, 176):
        for d in range(16):
            t[i, d] = (16 - d) % 16
    for i in (86, 91):
        for d in range(16):
            t[i, d] = (d & ~3) | {1: 3, 3: 1}.get(d & 3, d & 3)
    for d in range(16):
        f = d & 3
        t[26, d] = (d & ~3) | {1: 3, 3: 1}.get(f, f)
        t[106, d] = (d & 0b0101) | ((d & 2) << 2) | ((d & 8) >> 2)
        t[96, d] = (d & ~3) | {2: 3, 3: 2}.get(f, f)
        t[167, d] = t[96, d]
        for g in GATES:
            t[g, d] = (d & ~3) | {1: 3, 3: 1}.get(f, f)
        t[66, d] = {2: 3, 3: 2, 6: 7, 7: 6, 8: 9, 9: 8}.get(d, d)
        for r in (27, 28, 157):
            t[r, d] = (d & 8) | {2: 3, 3: 2}.get(d & 7, d & 7)
    return t


def mirror_world(w):
    """Every column x >= 0 becomes the turned image of column -1 - x."""
    assert w.x0 + w.sx - 1 == -1 - w.x0, "the volume must be symmetric about the rift"
    half = -w.x0
    red_ids = w.ids[:half]
    red_dat = w.dat[:half]
    t = data_table()
    w.ids[half:] = red_ids[::-1]
    w.dat[half:] = t[red_ids, red_dat][::-1]
    w.biome[half:] = w.biome[:half][::-1]
    blue = []
    for te in w.tiles:
        if te["x"] < 0:
            m = dict(te)
            m["x"] = -1 - te["x"]
            blue.append(m)
    w.tiles = [te for te in w.tiles if te["x"] < 0] + blue
