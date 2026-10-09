"""Write Sandreach's map.xml: two teams, their spawns, each wool with its room, its entry rule and its spawner; the
kit; building only over the board and its zones.
"""
import plan as P
from pgmvox.mapxml import Doc, E, item

O = P.objectives()
d = Doc("Sandreach", "1.0.0", "Capture the other team's wool!", "ctw")
d.add(E("authors", E("author", text="rockymine"), E("author", text="Claude (freeform generator, pgmvox)")))
O.write(d)
d.kit("spawn-kit",
      item("stone sword", 0, unbreakable=True), item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
      item("iron pickaxe", 2, unbreakable=True), item("iron axe", 3, unbreakable=True), item("wood", 4, 64),
      item("stained clay", 5, 48, team_color=True), item("golden apple", 6), item("cooked beef", 7, 16),
      item("shears", 8, unbreakable=True), item("arrow", 28),
      item("leather helmet", unbreakable=True, team_color=True, tag="helmet"),
      item("leather chestplate", unbreakable=True, team_color=True, tag="chestplate"),
      item("leather leggings", unbreakable=True, team_color=True, tag="leggings"),
      item("leather boots", unbreakable=True, team_color=True, tag="boots"))
d.filter("not-void", E("not", E("void")))
d.apply(block_place="not-void", message="You may not build in the void!")
d.add(E("itemkeep", [E("item", text=m) for m in ("stone sword", "bow", "iron pickaxe", "iron axe", "shears")]))
d.add(E("kill-rewards", E("kill-reward", E("item", material="golden apple"))))
d.add(E("maxbuildheight", text=P.MAX_BUILD))
print(d.tostring())
