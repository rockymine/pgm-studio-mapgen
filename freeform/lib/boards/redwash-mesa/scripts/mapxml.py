"""Write Redwash Mesa's map.xml: teams of twenty, the spawns, the four monuments and the observers' point from the
plan's objectives; the kit; the seam as the only place to build over the void; a build limit.

    python3 mapxml.py > map.xml
"""
import plan as P
import common as C
from pgmvox.mapxml import Doc, E

d = Doc("Redwash Mesa", "1.0.0", "Destroy both of the enemy's monuments: one out on their table, one in the plaza "
        "of their canyon town.", "dtm")
d.add(E("authors", E("author", text="Claude (pgmvox trial)")))
C.kit(d, pick="diamond pickaxe")
P.objectives().write(d)
C.build_only_over(d, E("rectangle", min=f"{-P.SEAM},{P.Z_MIN}", max=f"{P.SEAM + 1},{P.Z_MAX + 1}"),
                  "You may only build over the void in the seam!")
d.add(E("maxbuildheight", text=P.MAX_BUILD))
print(d.tostring())
