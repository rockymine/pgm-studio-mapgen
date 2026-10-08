"""Write Tidewell Canals' map.xml: teams of sixteen, their spawns, the three hills (the Campo worth two a second,
each fish market one), a score limit and a time limit, the kit; no building, the lagoon kills.

    python3 mapxml.py > map.xml
"""
import plan as P
import common as C
from pgmvox.mapxml import Doc, E

d = Doc("Tidewell Canals", "1.0.0", "Hold the markets: the Campo is worth two points a second, each fish market one.",
        "koth")
d.add(E("authors", E("author", text="Claude (pgmvox trial)")))
P.objectives().write(d, limit=1000)
C.kit(d, wood=0)
d.time(15 * 60)
d.apply(block="never", message="The quarter is not yours to build on!")
d.no_hunger()
print(d.tostring())
