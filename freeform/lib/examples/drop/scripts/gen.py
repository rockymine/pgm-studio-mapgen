"""Generate Drop from plan.py: every piece of the course as a slab floating over the void at its own top, and the
two water pieces as pools a fall lands in.

    a piece        three courses: its top in its kind's block, two of stone under it
    a water piece  water three deep to its edges, on a stone floor, in a glass rim one cell outside it that
                   stops a block under the surface, so no fall reaching the edge clips it
    the void       nothing below; a player who misses falls out of the world

The generator prints the blocks each piece laid.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import B, World  # noqa: E402

from plan import build  # noqa: E402

TOPS = {"start": (B.STONEBRICK, 3), "floor": (B.GRASS, 0), "roof": (B.STAINED_CLAY, 14),
        "beam": (B.PLANKS, 1)}
DEPTH = 3

C = build()
xs = [x for p in C.pieces for x, _ in p.cells]
zs = [z for p in C.pieces for _, z in p.cells]
w = World(min(xs) - 2, min(zs) - 2, max(xs) - min(xs) + 5, max(zs) - min(zs) + 5, sy=128)

for p in C.pieces:
    laid = 0
    if p.kind == "water":
        for x, z in p.cells:
            w.set(x, p.y - DEPTH, z, B.STONE)
            for y in range(p.y - DEPTH + 1, p.y + 1):
                w.set(x, y, z, B.WATER)
            laid += DEPTH + 1
        rim = {(x + dx, z + dz) for x, z in p.cells for dx in (-1, 0, 1) for dz in (-1, 0, 1)} - p.cells
        for x, z in rim:
            for y in range(p.y - DEPTH, p.y):
                w.set(x, y, z, B.GLASS)
            laid += DEPTH
    else:
        for x, z in p.cells:
            for y in range(p.y - DEPTH + 1, p.y):
                w.set(x, y, z, B.STONE)
            w.set(x, p.y, z, *TOPS.get(p.kind, (B.STONE, 0)))
            laid += DEPTH
    print(f"{p.label}: {laid} blocks at y {p.y}")

start = next(p for p in C.pieces if p.data.get("spawn"))
cx, cz = start.centre()
w.save(sys.argv[1], "Drop", (int(cx), start.y + 1, int(cz)))
print("generated")
