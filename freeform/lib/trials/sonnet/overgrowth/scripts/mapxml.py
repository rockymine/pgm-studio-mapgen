"""Write Overgrowth's map.xml, a team deathmatch: the teams of sixteen, their spawns and the observer from the plan's
objectives; the kit; a score of one a kill to a limit of 75; a forty-minute clock won by the higher score; no fall
damage off the terraces' bridges is not given (a fall hurts); building only up to the build height.

The library has no deathmatch objective, so the score element is written here with E.

    python3 mapxml.py > map.xml
"""
import plan as P
from pgmvox.mapxml import Doc, E, item

d = Doc("Overgrowth", "0.1.0", "Kill the other team: seventy-five points, or the higher score at forty minutes.", "tdm")
d.add(E("authors", E("author", text="Claude (freeform generator, on pgmvox)")))
P.objectives().write(d)
d.add(E("score", E("limit", text=75), E("kills", text=1), E("deaths", text=0)))
d.time(40 * 60, result="score")
d.kit("spawn-kit",
      item("iron sword", 0, unbreakable=True), item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
      item("iron pickaxe", 2, unbreakable=True), item("iron axe", 3, unbreakable=True),
      item("wood", 4, 64, 3), item("stained clay", 5, 32, team_color=True), item("golden apple", 6, 4),
      item("water bucket", 7), item("cooked beef", 8, 16), item("arrow", 28),
      item("leather helmet", unbreakable=True, team_color=True, tag="helmet"),
      item("iron chestplate", unbreakable=True, tag="chestplate"),
      item("chainmail leggings", unbreakable=True, tag="leggings"),
      item("leather boots", unbreakable=True, team_color=True, tag="boots"))
d.add(E("kill-rewards", E("kill-reward", E("item", material="golden apple"))))
d.add(E("itemkeep", [E("item", text=m) for m in ("iron sword", "bow", "iron pickaxe", "iron axe", "water bucket")]))
d.add(E("maxbuildheight", text=P.MAX_BUILD))
print(d.tostring())
