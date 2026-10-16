"""Generate Thawline from land.py and plan.py: the ground laid in rock and soil, painted by season, the waters and
the rift, every place built on both halves through its Side (season.py), the trees, then the objectives stamped
from the plan's objects and the ground marked for PGM's void rule.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np

import flora
import ground
import places
import plan as P
from pgmvox import B, World
from pgmvox.play.rules import mark_ground

SY = 112


def banks(w):
    """Water left standing against air is held: beside the rift the air takes falling water down to the lava, as
    the beck's fall; anywhere else it takes the bank, the ground block under it."""
    from pgmvox.read import audit
    n = 0
    for x, y, z, _ in audit.loose_water(w):
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ax, az = x + dx, z + dz
            if w.id(ax, y, az) != B.AIR:
                continue
            i, k = ax - P.X_MIN, az - P.Z_MIN
            if 0 <= i < P.H.shape[0] and 0 <= k < P.H.shape[1] and P.RIFT[i, k]:
                for yy in range(P.LAVA_Y + 1, y + 1):
                    if w.id(ax, yy, az) == B.AIR:
                        w.set(ax, yy, az, B.WATER_FLOW, 8)
            elif not (0 <= i < P.H.shape[0] and 0 <= k < P.H.shape[1] and P.LAND[i, k]):
                under = w.get(x, y - 1, z)                       # at the coast the water itself becomes bank
                w.set(x, y, z, *(under if under[0] not in (B.AIR, B.WATER) else (B.STONE, 0)))
            else:
                under = w.get(ax, y - 1, az)
                w.set(ax, y, az, *(under if under[0] not in (B.AIR, B.WATER, B.SNOW_LAYER) else (B.STONE, 0)))
            n += 1
    return n


def settle(w):
    """What would fall or pop off once the world is touched, made to hold: gravel over air becomes andesite, and a
    snow layer over air is taken away."""
    below = np.zeros_like(w.ids)
    below[:, 1:, :] = w.ids[:, :-1, :]
    loose = (w.ids == B.GRAVEL) & np.isin(below, [B.AIR, B.WATER, B.LAVA, B.WATER_FLOW, B.LAVA_FLOW])
    w.ids[loose], w.dat[loose] = B.STONE, 5
    hang = (w.ids == B.SNOW_LAYER) & np.isin(below, [B.AIR, B.SNOW_LAYER, B.WATER, B.ICE, B.PACKED_ICE])
    w.ids[hang], w.dat[hang] = 0, 0
    return int(loose.sum() + hang.sum())


def make():
    t0 = time.time()
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=SY)
    stats = {}
    deg = ground.rock(w)
    F = ground.season_fields()
    depth = ground.depth_of(F)
    ground.paint(w, deg, F, np.zeros(P.H.shape, bool))
    stats["glacier"] = ground.glacier(w, deg, ground.bottom())
    stats["water"] = ground.waters(w, F)
    stats["rift"] = ground.rift(w)
    stats["icicles, lava falls"] = ground.rift_walls(w)
    stats["beck falls"] = ground.beck_fall(w)
    stats["paved, bridged"] = places.roads(w, np.random.default_rng(1))
    places.rimehall(w, np.random.default_rng(2))
    places.snout(w)
    places.green(w, np.random.default_rng(3))
    places.kettle(w, np.random.default_rng(4))
    stats["houses"] = len(places.hamlet(w, np.random.default_rng(5)))
    places.watch(w, np.random.default_rng(6))
    stats["field walls"] = places.field_walls(w, np.random.default_rng(11))
    stats["erratics"] = len(places.erratics(w, np.random.default_rng(7)))
    stats["stack"] = places.stack(w, np.random.default_rng(8))
    stats["icicles under the coast"] = places.edges(w, ground.bottom())
    planted, litter, gold, snowy = flora.plant_all(w, np.random.default_rng(9), depth)
    stats["trees"] = len(planted)
    stats["leaf litter"] = ground.litter(w, litter)
    stats["snow on crowns"] = flora.snow_on_crowns(w, snowy)
    flora.biome_tints(w, gold, depth)
    stats["cover"] = flora.cover(w, np.random.default_rng(10), depth, litter)
    stats["banks"] = banks(w)
    stats["settled"] = settle(w)
    O = P.objectives()
    O.stamp(w)
    stats["marked"] = mark_ground(w)
    stats["seconds"] = round(time.time() - t0)
    return w, stats


if __name__ == "__main__":
    w, n = make()
    w.save(sys.argv[1], "Thawline", P.OBSERVER_AT)
    print("generated: " + ", ".join(f"{k} {v}" for k, v in n.items()))
    print(f"build height {P.MAX_BUILD}, kill below {P.KILL_Y}")
