"""Write Whitecliff Cistern's map.xml, a king of the hill: the teams, spawns and observer from the plan's objectives, the
three hills (the Cistern at two a second, the Garden and the Boatyard at one), a score limit, a twenty-minute clock won
by the higher score, the kit, the fall past the stack, building only over the stack and no higher than the build height.

    python3 mapxml.py > map.xml
"""
import plan as P
from pgmvox.mapxml import Doc, E, item

d = Doc("Whitecliff Cistern", "0.1.0", "Hold the hills: the Cistern pays two a second, the Garden and the Boatyard one.", "koth")
d.add(E("authors", E("author", text="Claude (freeform generator, on pgmvox)")))
P.objectives().write(d, limit=300)
d.time(20 * 60, result="score")
d.kit("spawn-kit",
      item("iron sword", 0, unbreakable=True), item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
      item("iron pickaxe", 2, unbreakable=True), item("iron axe", 3, unbreakable=True),
      item("wood", 4, 64, 0), item("stained clay", 5, 32, team_color=True), item("golden apple", 6, 4),
      item("cooked beef", 8, 16), item("arrow", 28),
      item("leather helmet", unbreakable=True, team_color=True, tag="helmet"),
      item("iron chestplate", unbreakable=True, tag="chestplate"),
      item("chainmail leggings", unbreakable=True, tag="leggings"),
      item("leather boots", unbreakable=True, team_color=True, tag="boots"))
d.kill_below(P.KILL_Y, how="kit")
d.filter("not-void", E("not", E("void")))
d.apply(block_place="not-void", message="You may not build in the void!")
d.add(E("itemkeep", [E("item", text=m) for m in ("iron sword", "bow", "iron pickaxe", "iron axe")]))
d.add(E("maxbuildheight", text=P.MAX_BUILD))
print(d.tostring())
