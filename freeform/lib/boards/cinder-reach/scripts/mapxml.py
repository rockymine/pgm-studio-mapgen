"""Write Cinder Reach's map.xml: teams of twenty, the spawns, the two cores and the observers' point from the plan's
objectives; the kit; the fissure as the only place to build over the void; a build limit.

    python3 mapxml.py > map.xml
"""
import plan as P
import common as C
from pgmvox.play.rules import Build, Map, terrain_of

M = Map("Cinder Reach", "1.0.0", "Leak the enemy's core: it hangs over a stone platform in the bowl of the cinder cone in front of their "
        "lodge.", "dtc",
        terrain=terrain_of(__file__),
        authors=["Claude (pgmvox trial)"],
        objectives=P.objectives(),
        kit=C.kit(pick="diamond pickaxe"),
        build=Build(areas=[(-P.RENT, P.Z_MIN, P.RENT, P.Z_MAX)], max_height=P.MAX_BUILD,
                        message="You may only build over the void in the fissure!"))
print(M.xml())
