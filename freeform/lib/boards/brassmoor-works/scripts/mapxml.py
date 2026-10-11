"""Write Brassmoor Works' map.xml: the teams, their spawns with their iron, the observers' point, the four wools with
their monuments, spawners and rooms from the plan's objectives; the kit; the fall; building only over a marked
column and the build height. What a player keeps, drops and is rewarded with follows from the kit.

    python3 mapxml.py > map.xml
"""
import plan as P
import common as C
from pgmvox.play.rules import Build, KillHeight, Map

O = P.objectives()

M = Map("Brassmoor Works", "1.0.0", "Capture the enemy's two wools: one from their Boiler House, one from under "
        "their Water Tower.", "ctw",
        authors=["Claude (pgmvox trial)"],
        objectives=O,
        kit=C.kit(),
        build=Build(max_height=P.MAX_BUILD),
        kill=KillHeight(P.KILL_Y))
print(M.xml())
