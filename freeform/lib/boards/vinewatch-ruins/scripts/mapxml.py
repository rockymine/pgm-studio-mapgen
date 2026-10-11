"""Write Vinewatch Ruins' map.xml: teams of twelve, their gate-court spawns, the observers' point; the kit; a kill
scores a point, fifty win, ten minutes; no building at all.

    python3 mapxml.py > map.xml
"""
import plan as P
import common as C
from pgmvox.play.rules import Build, Map, Match

M = Map("Vinewatch Ruins", "1.0.0", "Kill the enemy: the first team to fifty kills, or the most in ten minutes, wins.",
        "tdm",
        authors=["Claude (pgmvox trial)"],
        objectives=P.objectives(),
        kit=C.kit(wood=0),
        build=Build(never=True, message="The ruins are not yours to build on!"),
        match=Match(score=50, kills=1, time=600))
print(M.xml())
