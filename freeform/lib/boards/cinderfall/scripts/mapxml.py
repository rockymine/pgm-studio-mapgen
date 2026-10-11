"""Write Cinderfall's map.xml: the teams of sixteen, the spawns (their iron mineable) and the two cores from the plan's
objectives; the kit; the fall below the island; building only over the island, and no higher than the build height.

    python3 mapxml.py > map.xml
"""
import plan as P
from pgmvox.mapxml import Doc, E, item

d = Doc("Cinderfall", "0.1.0", "Break the enemy's core: lava must leak out of it.", "dtc")
d.add(E("authors", E("author", text="Claude (freeform generator, on pgmvox)")))
P.objectives().write(d)
d.kit("spawn-kit",
      item("iron sword", 0, unbreakable=True), item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
      item("diamond pickaxe", 2, unbreakable=True), item("iron axe", 3, unbreakable=True),
      item("wood", 4, 64), item("stained clay", 5, 32, team_color=True), item("golden apple", 6, 4),
      item("water bucket", 7), item("cooked beef", 8, 16), item("arrow", 28),
      item("leather helmet", unbreakable=True, team_color=True, tag="helmet"),
      item("iron chestplate", unbreakable=True, tag="chestplate"),
      item("chainmail leggings", unbreakable=True, tag="leggings"),
      item("leather boots", unbreakable=True, team_color=True, tag="boots"))
d.kill_below(P.KILL_Y, how="kit")
# block 36 at y 0 marks every column of the island: players build there and nowhere over the void
d.filter("not-void", E("not", E("void")))
d.apply(block_place="not-void", message="You may not build in the void!")
d.add(E("maxbuildheight", text=P.MAX_BUILD))
print(d.tostring())
