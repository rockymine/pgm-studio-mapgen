"""Generate Tidewell Canals from the plan: red's half (x < 0, itself mirrored in z) is built from the raster and
turned half a circle onto blue's; then the centre pad and the objectives are stamped.

The look, decided in the report's plan section and made here:
    streets  grey: stone brick, polished andesite, andesite and stone, a quarter each in cells of three
    campi    warm: brick in cells, a border of polished diorite (Istrian stone)
    houses   one style: a brick ground storey, pale or ochre plaster over it, brick-tiled gable roofs
    stone    the customs house, the column, the loggia's piers, the wellheads: quartz and polished diorite
    water    the canals and the lagoon at 38, quay faces of stone brick, gondolas moored
    accent   the hills' pads, lamps on the quays, the teams' banners

    python3 gen.py <build-dir>
"""
import math
import sys
import time

import numpy as np

import plan as P
import common as C
from pgmvox import B, World, rng
from pgmvox import build as BLD
from pgmvox import facade as F
from pgmvox import props
from pgmvox.orient import stair as stair_data, turn_world

t0 = time.time()
R = P.build()
w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=80)
X, Z = w.grid()
r_ = rng(P.BOARD, "canals")
STREET = [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)]
CAMPO = [(B.BRICK, 0), (B.BRICK, 0), (B.HARDENED_CLAY, 0), (B.STONE, 2)]
ISTRIAN = (B.STONE, 4)
S, W_ = P.STREET, P.WATER

# ---- the lagoon under everything, then red's half from the raster -------------------------------------------
w.fill(P.X_MIN, 1, P.Z_MIN, P.X_MAX, 30, P.Z_MAX, B.STONE)
w.fill(P.X_MIN, 31, P.Z_MIN, P.X_MAX, 33, P.Z_MAX, B.SAND)
w.fill(P.X_MIN, 34, P.Z_MIN, P.X_MAX, W_, P.Z_MAX, B.WATER)
for i, k in np.argwhere(X < 0):
    x, z = int(X[i, k]), int(Z[i, k])
    kd, h = R.kind(x, z), R.h(x, z)
    if kd == "lagoon":
        continue
    if kd in ("canal", "steps"):
        w.column(x, z, 34, 35, B.GRAVEL)
        for y in range(36, W_ + 1):
            w.set(x, y, z, B.WATER)
        if kd == "steps":
            w.column(x, z, 34, W_, B.STONEBRICK)
            w.set(x, W_ + 1, z, B.STONE_SLAB if hasattr(B, "STONE_SLAB") else B.SLAB, 5)
        continue
    w.column(x, z, 34, S - 1, B.STONEBRICK)                     # the made ground: brick to the water's floor
    if kd in ("campo", "market", "court", "pad"):
        blk = C.cell_pick(x, z, CAMPO, 2, 3)
    else:
        blk = C.cell_pick(x, z, STREET, 3, 1)
    w.set(x, S, z, *blk)
    if kd == "bridge":
        w.column(x, z, S, h - 1, B.STONEBRICK)
        w.set(x, h, z, *ISTRIAN)
    elif kd == "stair":
        w.column(x, z, S, h - 1, B.STONEBRICK)
        w.set(x, h, z, B.STONEBRICK_STAIRS, stair_data("e"))
    elif kd in ("wall", "cistern", "cover", "pillar"):
        top = h
        blk = {"wall": (B.STONEBRICK, 0), "cistern": (B.QUARTZ, 0), "cover": (B.PLANKS, 1), "pillar": (B.QUARTZ, 2)}[kd]
        for y in range(S + 1, top + 1):
            w.set(x, y, z, *blk)
        if kd == "cistern":
            w.set(x, top, z, B.STONE, 4)
        if kd == "cover":
            w.set(x, top, z, B.LOG, 1 | 4)
# the bridges' ends as steps: a stair up onto each arch from the street on either side
for i, k in np.argwhere(R.mask("bridge") & (X < 0)):
    x, z = int(X[i, k]), int(Z[i, k])
    h = R.h(x, z)
    for d, (dx, dz) in (("w", (1, 0)), ("e", (-1, 0)), ("n", (0, 1)), ("s", (0, -1))):
        nk = R.kind(x + dx, z + dz)
        if R.h(x + dx, z + dz) == h + 1 and nk == "bridge":
            w.set(x, h, z, B.STONEBRICK_STAIRS, stair_data({"w": "e", "e": "w", "n": "s", "s": "n"}[d]))
print(f"ground and water {time.time() - t0:.1f}s")

# ---- the canal faces and the edge of the lagoon: stone brick quays with a course of Istrian stone -------------------
for i, k in np.argwhere(X < 0):
    x, z = int(X[i, k]), int(Z[i, k])
    if R.kind(x, z) in ("street", "campo", "market", "court") and any(
            R.kind(x + dx, z + dz) in ("canal", "lagoon") for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))):
        w.set(x, S, z, *ISTRIAN)

# ---- the houses: one style, two plasters ------------------------------------------------------------------------
STYLE = {o: dict(ground=[(B.BRICK, 0)], upper=[(B.STAINED_CLAY, o)], post=None, gable=(B.STAINED_CLAY, o),
                 floor=(B.PLANKS, 1), roof=(B.BRICK, 0), stair=B.BRICK_STAIRS, slab=(B.SLAB, 4),
                 door=B.SPRUCE_DOOR, window=(B.PANE, 0), chimney=(B.BRICK, 0)) for o in (0, 4)}
n_h = 0
for j, (x0, z0, x1, z1, n) in enumerate(P.HOUSES):
    for (a, b) in ((z0, z1), (-1 - z1, -1 - z0)):
        L_, W2 = x1 - x0 + 1, b - a + 1
        heading = 0 if L_ >= W2 else 90
        Lh, Wh = (L_, W2) if heading == 0 else (W2, L_)
        hs = BLD.House((x0 + x1 + 1) / 2, (a + b + 1) / 2, heading, L=Lh, W=Wh, floor=S, storeys=n,
                       style=STYLE[0 if (j + a) % 2 else 4], door=1 if a < 0 else -1, chimney=True)
        BLD.house(w, hs, ground_at=lambda x, z: S, rng=rng(P.BOARD, f"house {j} {a}"))
        n_h += 1
for b in P.SHOPS:                                              # the fishmongers' fronts: low brick with awnings
    for x0, z0, x1, z1 in (b, (b[0], -1 - b[3], b[2], -1 - b[1])):
        for z in range(z0, z1 + 1):
            for y in range(S + 1, S + 9):
                w.set(x0, y, z, *((B.BRICK, 0) if y < S + 4 else (B.STAINED_CLAY, 1)))
            w.set(x0 + 1, S + 4, z, B.WOOL, 14 if z % 2 else 0)

# ---- the customs house: quartz and diorite, a portico, banners -----------------------------------------------------
for x0, z0, x1, z1 in P.CUSTOMS_WINGS:
    for (a, b) in ((z0, z1), (-1 - z1, -1 - z0)):
        for x in range(x0, x1 + 1):
            for z in range(a, b + 1):
                edge = x in (x0, x1) or z in (a, b)
                for y in range(S + 1, S + 12):
                    w.set(x, y, z, *((B.QUARTZ, 2) if (edge and (x + z) % 4 == 0) else
                                     (B.PANE, 0) if edge and y in (S + 3, S + 7) and (x + z) % 4 == 2 else
                                     (B.STONE, 4)))
                w.set(x, S + 12, z, *((B.SLAB, 7) if edge else (B.QUARTZ, 0)))
cx0, cz0, cx1, cz1 = P.CUSTOMS
for z in (cz0, -1 - cz0):                                      # the portico's beam over the court's open side
    for x in range(cx0, cx1 + 1):
        w.set(x, S + 7, z, B.QUARTZ, 1)
for x in range(cx0, cx1 + 1, 4):
    w.banner(x, S + 6, cz0 - 1 + 1, 1, wall_facing=3)
print(f"buildings {time.time() - t0:.1f}s: {n_h} houses")

# ---- the column, the loggia, the gallery, the wellheads, the markets' stalls, lamps, gondolas ------------------------
x0, z0, x1, z1 = P.COLUMN
for (a, b) in ((z0, z1), (-1 - z1, -1 - z0)):
    for x in range(x0, x1 + 1):                                # a plinth of Istrian stone with a column on it
        for z in range(a, b + 1):
            for y in range(S + 1, S + 3):
                w.set(x, y, z, *ISTRIAN)
    mx, mz = (x0 + x1) // 2, (a + b) // 2
    for y in range(S + 3, S + 13):
        w.set(mx, y, mz, B.QUARTZ, 2)
    w.set(mx, S + 13, mz, B.GOLD_BLOCK)
lx0, lz0, lx1, lz1 = P.LOGGIA
for x in range(lx0, 0):                                         # the loggia's roof: timber under brick tiles
    for z in range(lz0, lz1 + 1):
        w.set(x, P.LOGGIA_ROOF, z, B.PLANKS, 5)
        w.set(x, P.LOGGIA_ROOF + 1, z, *((B.SLAB, 4) if (x in (lx0,) or z in (lz0, lz1)) else (B.BRICK, 0)))
for z in range(lz0, lz1 + 1):
    w.set(-1, P.LOGGIA_ROOF + 2, z, B.BRICK)
gx0, gz0, gx1, gz1 = P.GALLERY_SPAN
for (a, b) in ((gz0, gz1), (-1 - gz1, -1 - gz0)):
    for x in range(gx0, gx1 + 1):
        for z in range(a, b + 1):
            w.set(x, P.GALLERY, z, B.PLANKS, 1)
            w.set(x, P.GALLERY - 1, z, B.LOG, 1 | 4)
        front = b if a < 0 else a
        w.set(x, P.GALLERY + 1, front, B.SPRUCE_FENCE)          # a rail on the Campo side
    for x in range(gx0, gx1 + 1, 4):                            # the arcade's back piers under the gallery
        back = a if a < 0 else b
        for y in range(S + 1, P.GALLERY):
            w.set(x, y, back, B.QUARTZ, 2)
mk = P.MARKET
for z in (-40, -56):                                            # stalls along the market's sides, off the pad
    props.stalls(w, [(x, z) for x in range(-12, -6)], S, "s" if z == -40 else "n", every=5, awnings=(14, 0, 11))
for (x0, z0, x1, z1) in ((-20, -60, -16, -1),):                  # gondolas moored along the Grand Canal
    for zc in (-56, -34, -24):
        for (a,) in ((zc,), (-1 - zc,)):
            for x in (-19, -18):
                for z in range(a - 3, a + 4):
                    if R.kind(x, z) == "canal":
                        w.set(x, W_, z, B.STAINED_CLAY, 15)
            for x in (-19, -18):
                for z in (a - 4, a + 4):
                    if R.kind(x, z) == "canal":
                        w.set(x, W_ + 1, z, B.STAINED_CLAY, 15)
for i, k in np.argwhere(R.mask("street") & (X < 0)):              # lamps along the quays, every eight
    x, z = int(X[i, k]), int(Z[i, k])
    if x == P.GRAND[0] - 2 and z % 8 == 0 and R.kind(x + 1, z) == "quay" and w.id(x, S + 1, z) == B.AIR:
        props.lamp(w, x, S + 1, z, post=(B.DARK_OAK_FENCE, 0))
print(f"dressing {time.time() - t0:.1f}s")

turn_world(w, "half", X < 0, banners={1: 4})
# the middle column x 0 belongs to blue's turn of red's x -1: the pads straddle it, so stamp their carpets now
for o in P.objectives().items:
    if hasattr(o, "pad"):
        b = o.pad
        # a hill's pad must hold what PGM recolours (wool, stained clay): a ring of white stained clay for the capture's
        # progress, a ring of white wool inside it for the owner, the Istrian border outside and quartz at the heart
        field = F.first_of(F.border(1, ISTRIAN), F.border(1, (B.STAINED_CLAY, 0), at=1),
                           F.border(1, (B.WOOL, 0), at=2), lambda c: (B.QUARTZ, 0))
        F.carpet(w, b.x0, b.z0, b.x1, b.z1, S, field)
w.biome[:, :] = 0
O = P.objectives()
O.stamp(w)
w.save(sys.argv[1], "Tidewell Canals", (0, 70, 0))
print(f"saved {time.time() - t0:.1f}s: {int(np.count_nonzero(w.ids))} blocks, {len(w.tiles)} tile entities")
