"""Write Redwash Mesa's map.xml: teams of twenty, the spawns, the four monuments and the observers' point from the
plan's objectives; the kit; the seam as the only place to build over the void; a build limit.

    python3 mapxml.py > map.xml
"""
import plan as P
import common as C
from pgmvox.play.rules import Build, Map, terrain_of

M = Map("Redwash Mesa", "1.0.0", "Destroy both of the enemy's monuments: one out on their table, one in the plaza "
        "of their canyon town.", "dtm",
        terrain=terrain_of(__file__),
        authors=["Claude (pgmvox trial)"],
        objectives=P.objectives(),
        kit=C.kit(pick="diamond pickaxe"),
        build=Build(areas=[(-P.SEAM, P.Z_MIN, P.SEAM, P.Z_MAX)], max_height=P.MAX_BUILD,
                        message="You may only build over the void in the seam!"))
print(M.xml())
