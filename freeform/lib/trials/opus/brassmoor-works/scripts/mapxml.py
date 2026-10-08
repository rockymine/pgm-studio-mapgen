"""Write Brassmoor Works' map.xml: the teams, their spawns with their iron, the observers' point, the four wools with
their monuments, spawners and rooms from the plan's objectives; the kit; the fall; building only over a marked
column; item keeping, kill rewards and the build height.

    python3 mapxml.py > map.xml
"""
import plan as P
import common as C
from pgmvox.mapxml import Doc, E

O = P.objectives()
d = Doc("Brassmoor Works", "1.0.0", "Capture the enemy's two wools: one from their Boiler House, one from under "
        "their Water Tower.", "ctw")
d.add(E("authors", E("author", text="Claude (pgmvox trial)")))
O.write(d)
C.kit(d, extra=())
d.kill_below(P.KILL_Y, how="kit")
d.filter("not-void", E("not", E("void")))
d.apply(block_place="not-void", message="You may not build in the void!")
d.add(E("itemkeep", [E("item", text=m) for m in ("iron sword", "bow", "iron pickaxe", "iron axe", "water bucket")]))
d.add(E("kill-rewards", E("kill-reward", E("item", material="wood", amount=16), E("item", material="golden apple"))))
d.add(E("maxbuildheight", text=P.MAX_BUILD))
print(d.tostring())
