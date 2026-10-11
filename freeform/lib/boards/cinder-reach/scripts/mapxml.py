"""Write Cinder Reach's map.xml: teams of twenty, the spawns, the two cores and the observers' point from the plan's
objectives; the kit; the fissure as the only place to build over the void; a build limit.

    python3 mapxml.py > map.xml
"""
import plan as P
import common as C
from pgmvox.mapxml import Doc, E

d = Doc("Cinder Reach", "1.0.0", "Leak the enemy's core: it hangs over a stone platform in the bowl of the cinder cone in front of their "
        "lodge.", "dtc")
d.add(E("authors", E("author", text="Claude (pgmvox trial)")))
C.kit(d, pick="diamond pickaxe")
P.objectives().write(d)
C.build_only_over(d, E("rectangle", min=f"{-P.RENT},{P.Z_MIN}", max=f"{P.RENT + 1},{P.Z_MAX + 1}"),
                  "You may only build over the void in the fissure!")
d.add(E("maxbuildheight", text=P.MAX_BUILD))
print(d.tostring())
