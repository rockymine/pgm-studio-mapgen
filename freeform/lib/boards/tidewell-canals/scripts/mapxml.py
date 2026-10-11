"""Write Tidewell Canals' map.xml: teams of sixteen, their spawns, the three hills (the Campo worth two a second,
each fish market one), a score limit and a time limit, the kit; no building, the lagoon kills.

    python3 mapxml.py > map.xml
"""
import plan as P
import common as C
from pgmvox.mapxml import Doc, E
from pgmvox.objectives import Hill

d = Doc("Tidewell Canals", "1.0.0", "Hold the markets: the Campo is worth two points a second, each fish market one.",
        "koth")
d.add(E("authors", E("author", text="Claude (pgmvox trial)")))
O = P.objectives()
O.write(d, limit=1000)
# The pad's blocks that recolour are its white stained clay ring and white wool ring (PGM's default visual-materials
# filter takes wool and stained clay). The progress display is the clay ring; the owner display is the pad, from which
# PGM takes the progress blocks away, so the wool ring is the owner's.
for h in O.of(Hill):
    ring = d.region(f"{h.id}-progress", E("union", *[b.cuboid() for b in P.pad_ring(h.pad, 1)]))
    d.root.find(f".//hills/hill[@id='{h.id}']").set("progress-display-region", ring)
C.kit(d, wood=0)
d.time(15 * 60)
d.apply(block="never", message="The quarter is not yours to build on!")
d.no_hunger()
print(d.tostring())
