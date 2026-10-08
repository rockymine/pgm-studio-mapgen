"""Write Vinewatch Ruins' map.xml: teams of twelve, their gate-court spawns, the observers' point; the kit; a kill
scores a point, fifty win, ten minutes; no building at all.

    python3 mapxml.py > map.xml
"""
import plan as P
import common as C
from pgmvox.mapxml import Doc, E

d = Doc("Vinewatch Ruins", "1.0.0", "Kill the enemy: the first team to fifty kills, or the most in ten minutes, wins.",
        "tdm")
d.add(E("authors", E("author", text="Claude (pgmvox trial)")))
P.objectives().write(d)
C.kit(d, wood=0)
d.add(E("score", E("kills", text=1), E("limit", text=50)))
d.time(600)
d.apply(block="never", message="The ruins are not yours to build on!")   # a deathmatch is fought on the board as made
d.no_hunger()
print(d.tostring())
