"""Write Lantern Karst's map.xml. The teams, their spawns with their iron, the observer point, the four wools
with their monuments, spawners and rooms (entry and block protection) come from the plan's objectives; the kit
and the fall from mapxml; the void filter, item keeping, kill rewards and the build height are written here.
"""
import plan  # noqa: F401  (puts the library on the path)
from plan import KILL_Y, MAX_BUILD, objectives
from pgmvox.mapxml import Doc, E, item

O = objectives()
d = Doc("Lantern Karst", "0.2.0", "Capture the enemy's two wools: the Pillar Shrine's and the Tea Store's.", "ctw")
d.add(E("authors", E("author", text="Claude (freeform generator, ported onto pgmvox)")))
O.write(d)                                       # teams, team filters, spawns, monuments, wools, rooms' entry rule

# the kit every spawn names, and the fall: instant damage below the kill height, as the original had it
d.kit("spawn-kit",
      item("iron sword", 0, unbreakable=True), item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
      item("iron pickaxe", 2, enchant=[("efficiency", 1)], unbreakable=True),
      item("iron axe", 3, enchant=[("efficiency", 1)], unbreakable=True), item("wood", 4, 64, 1),
      item("stained clay", 5, 48, team_color=True), item("golden apple", 6), item("water bucket", 7),
      item("cooked beef", 8, 16), item("arrow", 28), item("shears", 29, unbreakable=True), item("wood", 31, 64, 1),
      item("leather helmet", unbreakable=True, team_color=True, tag="helmet"),
      item("leather chestplate", unbreakable=True, team_color=True, tag="chestplate"),
      item("chainmail leggings", unbreakable=True, tag="leggings"),
      item("leather boots", unbreakable=True, team_color=True, tag="boots"))
d.kill_below(KILL_Y, how="kit")

# building: only over a column carrying block 36 at y 0, and no higher than the build height
d.filter("not-void", E("not", E("void")))
d.apply(block_place="not-void", message="You may not build in the void!")
d.add(E("itemkeep", [E("item", text=m) for m in ("iron sword", "bow", "iron pickaxe", "iron axe", "water bucket",
                                                  "shears")]))
d.add(E("kill-rewards", E("kill-reward", E("item", material="wood", damage=1, amount=16),
                          E("item", material="golden apple"))))
d.add(E("maxbuildheight", text=MAX_BUILD))
print(d.tostring())
