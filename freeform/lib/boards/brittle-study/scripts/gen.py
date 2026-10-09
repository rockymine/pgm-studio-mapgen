"""A study in the Brittlebush style: a few platforms at three heights, flights of grey stairs between them, a
tiered tower with its heart, built from style.py. No objectives and no match: it is a swatch, to set beside the
originals and see whether the look carries.

    python3 gen.py <build-dir>

    the garden      the low platform at 10: a long bed with a birch tree, a sand field, a striped path
    the terrace     the middle platform at 13, up a flight from the garden: two beds and sand
    the tower yard  the high platform at 16, up a flight from the terrace: the tiered tower and its heart
    two islets      sand and cacti at 10 and 9, across gaps a player would bridge
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import B, World, rng  # noqa: E402
from pgmvox.orient import stair  # noqa: E402

import style as S  # noqa: E402

X0, X1, Z0, Z1 = -36, 35, -30, 29
w = World(X0, Z0, X1 - X0 + 1, Z1 - Z0 + 1, sy=64)
r = rng("brittle-study", "dress")
YELLOW = 4

# pieces: name, box, floor; a later piece is laid over an earlier one
PIECES = [("garden", (-32, -6, -5, 16), 10),
          ("terrace", (-4, -12, 20, 8), 13),
          ("yard", (10, -27, 31, -13), 16),
          ("islet-west", (-24, -24, -13, -14), 10),
          ("islet-east", (24, 13, 33, 23), 9)]
# flights of stairs: box, the way they rise, the floor at their foot
FLIGHTS = [((-8, 1, -5, 4), "e", 10),
           ((14, -16, 17, -13), "n", 13)]

H = np.full((w.sx, w.sz), -1, int)
K = np.full((w.sx, w.sz), "", object)
X, Z = w.grid()
for name, (x0, z0, x1, z1), h in PIECES:
    m = (X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1)
    H[m], K[m] = h, name
for (x0, z0, x1, z1), d, lo in FLIGHTS:
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            n = {"e": x - x0, "w": x1 - x, "s": z - z0, "n": z1 - z}[d]
            H[x - X0, z - Z0], K[x - X0, z - Z0] = lo + 1 + n, "flight"


def h_at(x, z):
    return H[x - X0, z - Z0] if X0 <= x <= X1 and Z0 <= z <= Z1 else -1


def edge(x, z):
    """The side a column's face looks out of, where its neighbour stands two or more lower; None inside."""
    h = h_at(x, z)
    for d, (dx, dz) in (("e", (1, 0)), ("w", (-1, 0)), ("s", (0, 1)), ("n", (0, -1))):
        if h_at(x + dx, z + dz) < h - 1:
            return d
    return None


def run(x, z, out):
    """Where a face column falls in its straight run of face at one height: (index, length)."""
    h = h_at(x, z)
    ax, az = (0, 1) if out in ("e", "w") else (1, 0)
    lo = hi = 0
    while edge(x - ax * (lo + 1), z - az * (lo + 1)) == out and h_at(x - ax * (lo + 1), z - az * (lo + 1)) == h:
        lo += 1
    while edge(x + ax * (hi + 1), z + az * (hi + 1)) == out and h_at(x + ax * (hi + 1), z + az * (hi + 1)) == h:
        hi += 1
    return lo, lo + hi + 1


def depth(x, z):
    """Blocks in from the piece's own edge (0 on the edge), within the piece the column belongs to."""
    k, d = K[x - X0, z - Z0], 0
    while True:
        ring = [(x + dx, z + dz) for dx in range(-d - 1, d + 2) for dz in range(-d - 1, d + 2)
                if max(abs(dx), abs(dz)) == d + 1]
        if any(not (X0 <= a <= X1 and Z0 <= b <= Z1) or K[a - X0, b - Z0] != k for a, b in ring):
            return d
        d += 1


# 1. every column: the base, then the face on an edge, the frame and the field inside
fields = {}
for i, k in np.argwhere(H >= 0):
    x, z, h = int(X[i, k]), int(Z[i, k]), int(H[i, k])
    S.base(w, x, z, h)
    w.set(x, h, z, *S.SPRUCE_PLANKS)
    out = edge(x, z)
    if K[i, k] == "flight":
        w.set(x, h, z, B.STONEBRICK_STAIRS, stair({"e": "e", "n": "n"}[[f for f in FLIGHTS
              if f[0][0] <= x <= f[0][2] and f[0][1] <= z <= f[0][3]][0][1]]))
        if out:
            for y in range(h - 4, h):
                w.set(x, y, z, B.STONEBRICK)
        continue
    if out:
        pos, length = run(x, z, out)                               # one panel, three wide, in each face's middle
        mid = (length - 3) // 2
        S.face(w, x, z, h, S.OPP[out], panel=length >= 7 and mid <= pos < mid + 3)
        continue
    d = depth(x, z)
    if d >= 2:
        fields.setdefault(K[i, k], []).append((x, z))

# 2. the fields: sand by default, beds and paths laid over it
for name, cells in fields.items():
    h = dict((n, hh) for n, _, hh in PIECES)[name]
    S.sand_field(w, cells, h, r)
S.striped_path(w, (-30, 0, -9, 5), 10, along="x")
S.kerbed_bed(w, (-28, 8, -12, 14), 10, r, tree=(-20, 11))
S.kerbed_bed(w, (-28, -4, -18, -2), 10, r)
S.kerbed_bed(w, (-2, -10, 8, -4), 13, r, tree=(3, -7))
S.kerbed_bed(w, (8, 0, 18, 6), 13, r)
S.striped_path(w, (12, -10, 18, -2), 13, along="z")
S.striped_path(w, (-2, 1, 6, 5), 13, along="x")

# 3. the tower: three narrow storeys stepping back to the north, the wool's room in the first with its door to the
# south, a crown of sandstone stairs round gold on the last, and the heart over it
S.tier(w, (14, -25, 22, -17), 16, 22, YELLOW, door=(17, 19))
S.tier(w, (15, -25, 21, -19), 22, 27, YELLOW)
S.tier(w, (16, -24, 20, -20), 27, 32, YELLOW)
for x in range(17, 20):
    for z in range(-23, -20):
        d = "e" if x == 17 else "w" if x == 19 else "s" if z == -23 else "n" if z == -21 else None
        w.set(x, 32, z, *((B.SANDSTONE_STAIRS, stair(d)) if d else (B.GOLD_BLOCK, 0)))
for x in range(16, 21):                                       # the wool's room: a floor of smooth sandstone, the wool
    for z in range(-23, -18):
        w.set(x, 16, z, B.SANDSTONE, 2)
w.set(18, 17, -21, B.WOOL, YELLOW)
for y in range(33, 40):                                       # the pane that hangs the heart
    w.set(18, y, -22, B.STAINED_PANE, YELLOW)
S.heart(w, 18, 39, -22, YELLOW)

# 4. a dotted line of cobwebs on the floor of the void, round the board, as Brittlebush marks its bounds
for x in range(X0, X1 + 1, 5):
    for z in (Z0, Z1):
        if h_at(x, z) < 0:
            w.set(x, 1, z, B.COBWEB)
for z in range(Z0, Z1 + 1, 5):
    for x in (X0, X1):
        if h_at(x, z) < 0:
            w.set(x, 1, z, B.COBWEB)

w.save(sys.argv[1], "Brittle Study", (0, 40, 0))
print(f"saved: {int(np.count_nonzero(w.ids))} blocks")
