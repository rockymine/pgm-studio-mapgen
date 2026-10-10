"""Generate Slatefold from the plan: red's half (z < 0) is built, then mirrored (orient.turn_world, z' = -1 - z) with the
team colours swapped; the monuments, wools and the build zones' marks are stamped over both halves from the plan's
objects and zones.

The hill is stacked platforms: each column is its plan floor exactly, five courses of slate beds under it, a bedrock
course six under the floor (skipped on the rim), and a fluted root of rock below that. A face between two terraces is
a retaining wall of dressed stone; a face to the void is bedded rock with ledges.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np
from scipy import ndimage

import plan as P
import dress
from pgmvox import B, World, noise, rng
from pgmvox import terrain as T
from pgmvox import forms
from pgmvox.orient import stair as stair_data, turn_world

SY = 128
ROOT_FLOOR = 40
PLATE = 5                                    # courses of bedded rock under a floor, before the bedrock course


def red_cols(w):
    _, Z = w.grid()
    return Z < 0


def floors(R, w):
    """The plan's ground as world-shaped arrays: each column's floor (a wall column's is the ground it stands on), its
    kind (the piece under any wall), and where there is land."""
    floor = R.base.copy()
    kind = R.piece.copy()
    land = kind != R.kinds["void"]
    return floor, kind, land


def strata():
    return T.Strata([((B.STONE, 5), 3, 3), ((B.STONE, 0), 3, 3), ((B.COBBLE, 0), 1, 2), ((B.STONE, 6), 1.2, 2),
                     ((B.COAL_ORE, 0), 0.25, 1), ((B.STONEBRICK, 2), 0.3, 1)], seed=21, start=0)


def islands(w, R, beds, offset, r):
    floor, kind, land = floors(R, w)
    red = red_cols(w)
    land_r = land & red
    root = T.root_depth(land_r, cone=3.0, power=0.85, rough=0.4, flutes=3.0, spires=10, seed=11)
    cap = np.maximum(floor - P.FOUNDATION - ROOT_FLOOR, 1)
    root = np.minimum(root, cap)
    fill = T.beds(beds, offset, flecks=[((B.STONE, 0), (B.COBBLE, 0), 0.05), ((B.STONE, 5), (B.STONE, 6), 0.05)], seed=6)

    def paint(k, x, z, h):
        c = r.random()
        return (B.STONE, 5) if c < 0.45 else (B.STONE, 0) if c < 0.8 else (B.COBBLE, 0) if c < 0.93 else (B.STONE, 6)
    T.slab(w, floor, land_r, fill, root, r, plate=PLATE, foundation=P.FOUNDATION, paint=paint,
           top=lambda deg, hh: (B.STONE, 0), under=(B.DIRT, 0), dirt_depth=0)
    forms.skirt(w, land_r, floor, lambda y: fill(0, 0, [y])[0] if False else (B.STONE, 5 if y % 3 else 0), rng(P.BOARD, "skirt"),
                moss=0.10, grass=0.25)
    return land_r, floor, kind


def retaining_walls(w, R, floor, kind, land_r, r):
    """Where a terrace stands above a walkable one beside it, the face between is a wall of dressed stone, top to
    foot: stone brick, a little cracked, a course of andesite brick at the foot."""
    X, Z = w.grid()
    walk = land_r & np.isin(R.K, [R.kinds[k] for k in ("spawn", "row", "yard", "front", "landing", "bench", "quarry", "pit")])
    n = 0
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        lo = np.roll(floor, (-dx, -dz), axis=(0, 1))
        lo_land = np.roll(land_r & walk, (-dx, -dz), axis=(0, 1))
        face = land_r & lo_land & (floor - lo >= 2)
        for i, k in np.argwhere(face):
            if not (0 < i < floor.shape[0] - 1 and 0 < k < floor.shape[1] - 1):
                continue
            x, z, h, hl = int(X[i, k]), int(Z[i, k]), int(floor[i, k]), int(lo[i, k])
            for y in range(hl + 1, h):
                c = r.random()
                w.set(x, y, z, *((B.STONEBRICK, 0) if c < 0.8 else (B.STONEBRICK, 2) if c < 0.95 else (B.STONEBRICK, 1)))
            n += 1
    return n


def flights(w, R, r):
    """Stairs laid on the plan's stair cells: stone brick stairs on a stone brick mass, four of air over each, and a
    cobble wall along each side where the ground beside it is lower."""
    X, Z = w.grid()
    stair = R.mask("stair") & (Z < 0)
    n = 0
    for i, k in np.argwhere(stair):
        x, z, y = int(X[i, k]), int(Z[i, k]), int(R.H[i, k])
        rises = R.stair.get((x, z), "n")
        for yy in range(y - 6, y):
            w.set(x, yy, z, *((B.STONEBRICK, 0) if r.random() < 0.85 else (B.STONEBRICK, 2)))
        w.set(x, y, z, B.STONEBRICK_STAIRS, stair_data(rises))
        for yy in range(y + 1, y + 5):
            w.set(x, yy, z, B.AIR)
        n += 1
    # a rail on a flight's side cells where the neighbour beside it, across the climb, is lower by two or more
    for i, k in np.argwhere(stair):
        x, z, y = int(X[i, k]), int(Z[i, k]), int(R.H[i, k])
        rises = R.stair.get((x, z), "n")
        side = ((1, 0), (-1, 0)) if rises in ("n", "s") else ((0, 1), (0, -1))
        for dx, dz in side:
            nx_, nz_ = x + dx, z + dz
            if R.inside(nx_, nz_) and R.kind(nx_, nz_) != "stair" and (R.h(nx_, nz_) <= y - 1 or R.kind(nx_, nz_) == "void"):
                w.set(x, y + 1, z, B.COBBLE_WALL, 0)
                break
    return n


def make():
    R = P.build()
    O = P.objectives()
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=SY)
    stats = {}
    t0 = time.time()
    r = rng(P.BOARD, "rock")
    beds = strata()
    offset = T.bed_offset((w.sx, w.sz), dip=(0.0, 0.0), fold=3, cell=14, seed=13)
    land_r, floor, kind = islands(w, R, beds, offset, r)
    stats["rock"] = int(land_r.sum())
    stats["retaining"] = retaining_walls(w, R, floor, kind, land_r, rng(P.BOARD, "walls"))
    dress.surface(w, R, land_r, floor, rng(P.BOARD, "surface"))
    stats["stairs"] = flights(w, R, rng(P.BOARD, "flights"))
    dress.everything(w, R, land_r, floor, O, stats)
    turn_world(w, "mirror_z", red_cols(w),
               recolour={(B.CARPET, 14): (B.CARPET, 11), (B.STAINED_CLAY, 14): (B.STAINED_CLAY, 11),
                         (B.WOOL, 14): (B.WOOL, 11)},
               banners={14: 13, 6: 11, 1: 4})
    O.stamp(w)
    dress.marks(w, R, stats)
    dress.mist(w, R, stats)
    w.biome[:, :] = P.BIOME
    return w, stats


if __name__ == "__main__":
    t0 = time.time()
    w, n = make()
    w.save(sys.argv[1], "Slatefold", P.OBSERVER_AT)
    print(f"generated in {time.time() - t0:.0f}s: " + ", ".join(f"{k} {v}" for k, v in n.items()))
    print(f"build height {P.MAX_BUILD}, kill below {P.KILL_Y}")
