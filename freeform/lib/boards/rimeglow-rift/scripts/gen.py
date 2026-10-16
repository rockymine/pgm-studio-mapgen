"""Generate Rimeglow Rift."""
import sys

import numpy as np

import land as LD
import ground as G
import rift as RF
import bridges as BR
import halls as HL
import beacon as BC
import plan as PL
import flora as FL
import gates as GT
import mere as ME
import dress as DR
import camps as CP
import outer as OU
import signs as SG
from pgmvox.play.rules import mark_ground
from pgmvox import B, World
from stamp import Stamp

w = World(LD.X0, LD.Z0, LD.SX, LD.SZ, sy=LD.SY)
ctx = G.build(w)
H = ctx["H"]
RF.lava(w, ctx)
print('stones', RF.stones(w, ctx), 'streak columns', RF.streaks(w, ctx))
north, south = Stamp(w, False), Stamp(w, True)
for S in (north, south):
    GT.causeway_gate(S, H)
    GT.pylons(S, H, -39)
    GT.pylons(S, H, 38)
    for xc in (-38, 0, 38):
        GT.plaza(S, H, xc)
    BR.causeway(S, H)
    BR.trestle(S, H, -39)
    BR.trestle(S, H, 38)
for sd in (False, True):
    HL.build(w, H, sd)
    BC.build(w, H, sd)
O = PL.objectives()
O.stamp(w)

ME.build(w, ctx)
camp = CP.build(w, ctx)
print('camp at', camp)
# ---- the plantings: sites on the north half, written twice
X, Z = ctx["X"], ctx["Z"]
excl = np.ones(X.shape, bool)
excl &= ~((X > -8) & (X < 34) & (Z < -58))                                   # the hall and its court
excl &= ~(np.hypot(X - 46, Z + 48) < 16)                                     # the beacon
excl &= ~((np.abs(X - np.array([-38, 0, 38])[:, None, None]) < 17).any(axis=0) & (Z > -36))   # the gate plazas
excl &= ~(np.hypot((X + 8) / 27.0, (Z + 42) / 15.0) < 1.0)                  # the mere
excl &= ~((X > camp[0] - 12) & (X < camp[0] + 12) & (Z > camp[1] - 9) & (Z < camp[1] + 9))
ok = FL.masks(ctx, excl)
rng = np.random.default_rng(5)
from pgmvox.geom.shapes import polyline
dridge, _ = polyline(X, Z, [(-50, -88), (-52, -68), (-47, -48), (-43, -34)])
dcore = np.hypot(X - 46, Z + 48)
taken = []
zones = [
    ("ridge", ok & (dridge < 17), 110, 2.6, False),
    ("foot", ok & (dcore > 17) & (dcore < 34), 30, 3.6, False),
    ("plain", ok & (Z < -36), 60, 5.0, False),
    ("thaw", ok & (Z > -36), 34, 4.4, True),
]
planted = []
for name, m, n, spacing, swap in zones:
    got = FL.sites(ctx, rng, m, n, spacing, taken)
    print('zone', name, 'cells', int(m.sum()), 'wanted', n, 'got', len(got))
    for (x, z) in got:
        taken.append((x, z))
        planted.append((name, x, z, swap))
for name, x, z, swap in planted:
    g = int(H[x - w.x0, z - w.z0])
    h = int(rng.integers(8, 14)) if name != "thaw" else int(rng.integers(6, 10))
    tone = ("ember", "gold", "crimson", "rust")[int(rng.integers(0, 4))]
    th = int(rng.integers(5, 8))
    nx, nz = -1 - x, -1 - z
    if swap:                                      # the banks trade: autumn in the snow, spruce on the warm ground
        FL.autumn_oak(w, x, z, g, th, rng, tone)
        FL.spruce(w, nx, nz, g, h, rng)
        FL.needle_floor(w, nx, nz, rng)
    else:
        FL.spruce(w, x, z, g, h, rng)
        FL.needle_floor(w, x, z, rng)
        FL.autumn_oak(w, nx, nz, g, th, rng, tone)
print("trees:", len(planted) * 2)
rng2 = np.random.default_rng(12)
print("lamps", DR.lamps(w, ctx), "boulders", DR.rockfall(w, ctx, rng2), "spires", DR.spires(w, ctx, rng2), "drifts", DR.drifts(w, ctx), "cover", DR.cover(w, ctx, rng2), "steps", DR.steps(w, ctx))
rng3 = np.random.default_rng(31)
print("outer: hangings", OU.hangings(w, ctx, rng3), "seams", OU.seams(w, ctx, rng3), "dead trees", OU.dead_trees(w, ctx, rng3))
print("signs", SG.build(w, H))
# fire is kept off anything that burns: a fence beside it becomes nether fence, anything else puts the fire out
FLAM = {B.PLANKS, B.LOG, B.LOG2, B.LEAVES, B.LEAVES2, B.WOOL, B.CARPET, B.HAY, B.WOOD_SLAB, B.OAK_STAIRS,
        B.SPRUCE_STAIRS, B.DARK_OAK_STAIRS, B.ACACIA_STAIRS, B.BIRCH_STAIRS, B.JUNGLE_STAIRS, B.BOOKSHELF, B.TALLGRASS,
        B.VINE, B.SPRUCE_DOOR, B.DARK_OAK_DOOR, B.DEADBUSH}
FENCES = {B.FENCE, B.SPRUCE_FENCE, B.DARK_OAK_FENCE}
for i, y, k in np.argwhere(w.ids == B.FIRE):
    for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
        a, b, c = i + dx, y + dy, k + dz
        if 0 <= a < w.sx and 0 <= b < w.sy and 0 <= c < w.sz:
            if w.ids[a, b, c] in FENCES:
                w.ids[a, b, c], w.dat[a, b, c] = B.NETHER_FENCE, 0
            elif w.ids[a, b, c] in FLAM:
                w.ids[i, y, k], w.dat[i, y, k] = 0, 0
                break
# whatever lies flat or stands on a plant needs a block under it
for bid in (B.SNOW_LAYER, B.CARPET, B.TALLGRASS, B.DEADBUSH):
    m = w.ids == bid
    below = np.zeros_like(m)
    below[:, 1:, :] = np.isin(w.ids[:, :-1, :], (0, B.WATER, B.LAVA, B.TALLGRASS, B.DEADBUSH, B.SNOW_LAYER, B.CARPET))
    loose = m & below
    w.ids[loose] = 0
    w.dat[loose] = 0
print("ground marks:", mark_ground(w))
print('lavafalls', OU.lavafalls(w, ctx, rng3))
OU.shards(w, ctx, rng3)               # beyond the marks: nothing there can be built on
# the biome: the cold one in the north's winter, the mesa's where the leaves turn
w.biome[:] = np.where(ctx['S'] >= 0.55, 30, 37).astype(np.uint8)
w.save(sys.argv[1], "Rimeglow Rift", (13, 72, -76))
print("generated")
