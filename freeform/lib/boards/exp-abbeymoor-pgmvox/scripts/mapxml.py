"""Write Abbeymoor's map.xml: the teams, spawns, observer and the four monuments (two a team) come from the plan's objectives; the
kit (a diamond pickaxe, which breaks obsidian), the fall, the void filter, item keeping and the build height are written here.

    python3 mapxml.py > map.xml
"""
import plan as P
from pgmvox.mapxml import Doc, E, item

d = Doc("Abbeymoor", "1.0.0", "Destroy the enemy's two monuments: the one over the abbey and the one on the village green.", "dtm")
d.add(E("authors", E("author", text="Claude Sonnet 5.5 (freeform generator, on pgmvox)")))
P.objectives().write(d)
d.kit("spawn-kit",
      item("iron sword", 0, unbreakable=True), item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
      item("diamond pickaxe", 2, enchant=[("efficiency", 2)], unbreakable=True),
      item("iron axe", 3, enchant=[("efficiency", 1)], unbreakable=True), item("wood", 4, 64, 1),
      item("stained clay", 5, 64, team_color=True), item("golden apple", 6), item("water bucket", 7),
      item("cooked beef", 8, 16), item("arrow", 28), item("shears", 29, unbreakable=True), item("wood", 31, 64, 1),
      item("leather helmet", unbreakable=True, team_color=True, tag="helmet"),
      item("leather chestplate", unbreakable=True, team_color=True, tag="chestplate"),
      item("chainmail leggings", unbreakable=True, tag="leggings"),
      item("leather boots", unbreakable=True, team_color=True, tag="boots"))
d.kill_below(P.KILL_Y, how="kit")
d.filter("not-void", E("not", E("void")))
d.apply(block_place="not-void", message="You may not build in the void!")
d.add(E("itemkeep", [E("item", text=m) for m in ("iron sword", "bow", "diamond pickaxe", "iron axe", "water bucket", "shears")]))
d.add(E("kill-rewards", E("kill-reward", E("item", material="wood", damage=1, amount=16), E("item", material="golden apple"))))
d.add(E("maxbuildheight", text=P.MAX_BUILD))
print(d.tostring())
