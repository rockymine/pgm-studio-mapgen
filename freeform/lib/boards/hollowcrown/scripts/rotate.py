"""Turn red's half onto blue's across the diagonal: half a turn about the board's centre,
(x, z) -> (-1 - x, -1 - z), every facing block turned with it. Red's half is x + z < -1, plus the
cells on the diagonal with x <= -1."""
import numpy as np

STAIRS = [53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 163, 164, 180]
DOORS = [64, 71, 193, 194, 195, 196, 197]
FACING6 = [23, 54, 61, 62, 65, 68, 146, 158, 177, 144]
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
        t[66, d] = {2: 3, 3: 2, 4: 5, 5: 4, 6: 8, 8: 6, 7: 9, 9: 7}.get(d, d)
    return t


def rotate_world(w, red):
    """red: bool[sx, sz] of the cells red authored. Every other cell becomes the turned image of its partner."""
    assert w.x0 + w.sx - 1 == -1 - w.x0 and w.z0 + w.sz - 1 == -1 - w.z0
    t = data_table()
    src_i = w.ids[::-1, :, ::-1]
    src_d = t[src_i, w.dat[::-1, :, ::-1]]
    m = red[:, None, :]
    w.ids[:] = np.where(m, w.ids, src_i)
    w.dat[:] = np.where(m, w.dat, src_d)
    w.biome[:] = np.where(red, w.biome, w.biome[::-1, ::-1])
    blue = []
    for te in w.tiles:
        x, z = te["x"], te["z"]
        if red[x - w.x0, z - w.z0]:
            m2 = dict(te); m2["x"], m2["z"] = -1 - x, -1 - z
            blue.append(m2)
    w.tiles = [te for te in w.tiles if red[te["x"] - w.x0, te["z"] - w.z0]] + blue
