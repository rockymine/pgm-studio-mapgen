"""The cave off red's gallery: passages and three chambers under the snowfield, lava ponds sunk in their floors,
two windows where a passage breaks out onto the fissure's wall, and a chest in each chamber. It is scenery and
loot, not a route: nothing in it leads anywhere the gallery does not.

Every pond lies more than fifteen blocks from the core's footprint, so no lava it lets out can leak a core.
"""
import numpy as np

import land
import plan as P
from pgmvox import B
from pgmvox.volume import under

LOOT = [
    [(0, "minecraft:golden_apple", 2, 0), (4, "minecraft:arrow", 32, 0), (9, "minecraft:iron_ingot", 6, 0)],
    [(2, "minecraft:cooked_beef", 8, 0), (6, "minecraft:arrow", 24, 0), (13, "minecraft:golden_apple", 1, 0)],
    [(1, "minecraft:iron_ingot", 4, 0), (5, "minecraft:coal", 12, 0), (11, "minecraft:golden_apple", 1, 0)],
]


def build(w, top, bunker_air):
    """Carve and dress red's cave. `top` is the ground's top per column (world grid); `bunker_air` the station's
    carved volume over bunker.BOX, kept clear of the cave's dressing."""
    import bunker
    xs, ys, zs = bunker.grid()

    def keep(x, y, z):
        i, j, k = x - xs[0], y - ys[0], z - zs[0]
        if 0 <= i < len(xs) and 0 <= j < len(ys) and 0 <= k < len(zs):
            return bool(bunker_air[max(0, i - 1):i + 2, max(0, j - 1):j + 2, max(0, k - 1):k + 2].any())
        return False
    for passage in P.CAVE:                                      # carved through the gallery's west wall
        under.tunnel(w, passage, ground=top, cover=4)
    for x, fy, z, rx, h, rz in P.CHAMBERS:
        under.chamber(w, x, fy, z, rx, h, rz, ground=top, cover=4)
    for x, fy, z in P.CAVE_WINDOWS:                              # out to the fissure's wall
        c, _ = land.fissure_line()
        target = int(c[x - land.X0])
        pts = [(x, fy, z, 2.0), (x, fy, max(target + 3, z - 14), 1.8)]
        under.tunnel(w, pts, ground=None, cover=0)
    rng = np.random.default_rng(7)
    under.dress_cave(w, (-66, -14, 2, 40, 20, 46), rng, ground=top, cover=3, keep=keep, ores=160, stalagmites=500,
                     floors=((B.GRAVEL, 0), (B.STONE, 5), (B.COBBLE, 0), (B.STAINED_CLAY, 15)),
                     weights=(0.35, 0.35, 0.15, 0.15), mushrooms=0.0,
                     ore_blocks=((B.COAL_ORE, 0.7), (B.IRON_ORE, 0.3)))
    for x, y, z, r in P.LAVA_PONDS:                              # ponds: lava two deep in a rim of obsidian
        for dx in range(-4, 5):
            for dz in range(-4, 5):
                d = np.hypot(dx, dz)
                if d > r + 1:
                    continue
                X, Z = x + dx, z + dz
                if w.id(X, y, Z) != B.AIR:                       # only under the chamber's open floor
                    continue
                if d <= r:                                       # lava flush with the floor, two deep
                    w.set(X, y - 3, Z, B.OBSIDIAN)
                    w.set(X, y - 2, Z, B.LAVA)
                    w.set(X, y - 1, Z, B.LAVA)
                else:                                            # its rim: solid, so the lava cannot run
                    for yy in (y - 2, y - 1):
                        w.set(X, yy, Z, B.OBSIDIAN if (dx + dz) % 2 else B.NETHERRACK)
    for (x, fy, z, *_), items in zip(P.CHAMBERS, LOOT):
        for dx, dz in ((2, 2), (-2, 2), (2, -2), (-2, -2), (0, 3), (3, 0)):
            X, Z = x + dx, z + dz
            if w.id(X, fy, Z) == B.AIR and w.id(X, fy - 1, Z) not in (B.AIR, B.LAVA):
                w.chest(X, fy, Z, items, facing=3)
                break
