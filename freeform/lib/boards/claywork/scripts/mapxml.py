"""Write Claywork's map.xml. The teams, their spawns, the observer point, the four wools with their monuments,
spawners and rooms (entry and block protection) come from the plan's objectives; the kit from mapxml; the void
filter, item keeping, kill rewards and the build height are written here. The void below the world is the kill.
"""
import plan  # noqa: F401  (puts the library on the path)
from plan import MAX_BUILD, objectives
from pgmvox.mapxml import Doc, E, item

O = objectives()
d = Doc("Claywork", "1.0.0", "Capture the enemy's two wools from the Kilns in their back corners.", "ctw")
d.add(E("authors", E("author", text="Claude (freeform generator, pgmvox)")))
O.write(d)                                       # teams, team filters, spawns, monuments, wools, rooms' entry rule

d.kit("spawn-kit",
      item("iron sword", 0, unbreakable=True), item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
      item("iron pickaxe", 2, enchant=[("efficiency", 1)], unbreakable=True),
      item("iron axe", 3, enchant=[("efficiency", 1)], unbreakable=True), item("wood", 4, 64, 1),
      item("stained clay", 5, 64, team_color=True), item("golden apple", 6), item("water bucket", 7),
      item("cooked beef", 8, 16), item("arrow", 28), item("shears", 29, unbreakable=True), item("wood", 31, 64, 1),
      item("leather helmet", unbreakable=True, team_color=True, tag="helmet"),
      item("leather chestplate", unbreakable=True, team_color=True, tag="chestplate"),
      item("chainmail leggings", unbreakable=True, tag="leggings"),
      item("leather boots", unbreakable=True, team_color=True, tag="boots"))

# building: only over a column carrying block 36 at y 0 (every piece and every build zone), up to the build height
d.filter("not-void", E("not", E("void")))
d.apply(block_place="not-void", message="You may not build in the void!")
d.add(E("itemkeep", [E("item", text=m) for m in ("iron sword", "bow", "iron pickaxe", "iron axe", "water bucket",
                                                  "shears")]))
d.add(E("kill-rewards", E("kill-reward", E("item", material="wood", damage=1, amount=16),
                          E("item", material="golden apple"))))
d.add(E("maxbuildheight", text=MAX_BUILD))
print(d.tostring())
