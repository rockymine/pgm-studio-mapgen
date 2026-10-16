"""Crucible's ground: every column of the land laid in rock beds to its top, the top finished by its angle, the rift's
lava sea, and the black flow's channel.

    ground.lay(w) -> top (the heights laid)

The beds are the mountain's: grey rock with beds of slate, brown tuff, black basalt and a thin red scoria, dipping
gently across the board and rising with the land, so every cut, cliff and tunnel wall shows the same beds. The top
course is chosen by slope: ash on the flat, rubble on the middle slopes, the beds themselves on the steep.
"""
import numpy as np

import land
import palette as P
from pgmvox import B
from pgmvox.surface.terrain import slope_deg

BEDS = [("slate", 4), ("basalt", 2), ("slate", 3), ("tuff", 2), ("rock", 2), ("slate", 3), ("red", 1), ("basalt", 3),
        ("tuff", 2), ("slate", 4), ("rock", 1), ("basalt", 2), ("tuff", 1), ("slate", 2), ("red", 1), ("rock", 2)]


def bed_table(n):
    out = []
    while len(out) < n:
        for name, t in BEDS:
            out += [name] * t
    return out[:n]


def lay(w):
    """Lay the land into `w`: (top, slope) of every column, the heights rounded."""
    H = np.round(land.heights()).astype(int)
    inside = land.inside()
    X, Z = land.grid()
    deg = slope_deg(H)
    sx, sy, sz = w.sx, w.sy, w.sz
    # the beds' offset: a gentle dip across the board and a share of the land's own rise, so they climb with it
    from scipy import ndimage
    broad = ndimage.uniform_filter(H.astype(float), 15)
    off = np.round(0.06 * X + 0.04 * Z + 0.35 * (broad - 48)).astype(int)
    off = land.sym(off)
    table = bed_table(512)
    names = sorted(set(table))
    code = np.array([names.index(t) for t in table])
    Y = np.arange(sy)[None, :, None]
    idx = (Y + off[:, None, :] + 200) % len(table)
    which = code[idx]                                          # (sx, sy, sz) set index of every block
    u = P.noise3((sx, sy, sz), (7, 2, 7), seed=11)
    ids = np.zeros((sx, sy, sz), np.uint16)
    dat = np.zeros((sx, sy, sz), np.uint8)
    for k, name in enumerate(names):
        m = which == k
        i, d = P.pick(name, u[m])
        ids[m] = i
        dat[m] = d
    below = (Y >= 1) & (Y <= H[:, None, :])
    below &= inside[:, None, :]
    w.ids[:] = np.where(below, ids, 0)
    w.dat[:] = np.where(below, dat, 0)
    w.biome[:] = 37                                            # mesa: the tinted few go dry and brown

    # the top course by angle: ash on the flat, rubble on the middle slopes, the beds on the steep
    u2 = P.noise2((sx, sz), 4, seed=12)
    u2b = P.noise2((sx, sz), 4, seed=13)
    lobe, _, _, _ = land.flow()
    lobe = land.sym(lobe & (Z >= 0))
    rc = land.sym(np.hypot(X - 50, Z - 33))
    cone = rc < 13.5
    for i in range(sx):
        for k in range(sz):
            if not inside[i, k]:
                continue
            h = int(H[i, k])
            if h <= land.LAVA + 1:
                continue
            g = deg[i, k]
            if g > (62 if h > 72 else 55):
                continue
            name = "rubble" if g > (44 if h > 72 else 36) else "scoria" if cone[i, k] else "basalt" if lobe[i, k] else "ash"
            iid, dd = P.pick(name, np.array([u2[i, k]]))
            w.ids[i, h, k], w.dat[i, h, k] = int(iid[0]), int(dd[0])
            if g <= 36:                                          # a course of the same ground under it
                iid, dd = P.pick("basalt" if name != "scoria" else "scoria", np.array([u2b[i, k]]))
                if h - 1 >= 1:
                    w.ids[i, h - 1, k], w.dat[i, h - 1, k] = int(iid[0]), int(dd[0])

    # the rift: the floor under the lava in obsidian and netherrack, the sea to its surface
    for i in range(sx):
        for k in range(sz):
            if not inside[i, k]:
                continue
            h = int(H[i, k])
            if h < land.LAVA:
                w.ids[i, 1:h + 1, k] = np.where(u[i, 1:h + 1, k] < 0.5, B.OBSIDIAN, B.NETHERRACK)
                w.dat[i, 1:h + 1, k] = 0
                w.ids[i, h + 1:land.LAVA + 1, k] = B.LAVA
                w.dat[i, h + 1:land.LAVA + 1, k] = 0
            elif h <= land.LAVA + 3:                             # the scorched foot of the rift's wall
                w.ids[i, max(1, h - 2):h + 1, k] = np.where(u[i, max(1, h - 2):h + 1, k] < 0.5, B.OBSIDIAN,
                                                            B.NETHERRACK)
                w.dat[i, max(1, h - 2):h + 1, k] = 0
    return H, deg


def channel(w, H):
    """The black flow's channel: lava a block under the lobe's top, obsidian under it, its banks raised where a
    neighbour stands low. Returns the lip cells at the rift, (x, y, z) of the lava, where the lavafall starts."""
    ch = land.lava_channel()
    X, Z = land.grid()
    lip = []
    for i, k in np.argwhere(ch):
        x, z = int(X[i, k]), int(Z[i, k])
        h = int(H[i, k])
        if h > 62:                                               # still under the mountain
            continue
        w.set(x, h, z, B.AIR)
        w.set(x, h - 1, z, B.LAVA)
        w.set(x, h - 2, z, B.OBSIDIAN)
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = i + dx, k + dz
            if not (0 <= a < land.NX and 0 <= b < land.NZ) or ch[a, b]:
                continue
            if H[a, b] < h - 1:
                if H[a, b] <= land.LAVA + 2:
                    lip.append((x, h - 1, z, x + dx, z + dz))
                else:
                    w.set(x + dx, h - 1, z + dz, B.OBSIDIAN)
    # where the channel steps down, the higher lava runs over the step: flowing lava in the air beside it
    for i, k in np.argwhere(ch):
        x, z = int(X[i, k]), int(Z[i, k])
        h = int(H[i, k])
        if h > 62:
            continue
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = i + dx, k + dz
            if 0 <= a < land.NX and 0 <= b < land.NZ and ch[a, b] and w.id(x + dx, h - 1, z + dz) == B.AIR:
                w.set(x + dx, h - 1, z + dz, B.LAVA_FLOW, 2)
    return lip
