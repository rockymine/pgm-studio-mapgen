"""Write Riftwater's map.xml: teams of sixteen, the spawns, the four monuments and the observer point from the
plan's objectives; the original board's kit; the rift as the only place to build over the void; a build limit.

    python3 mapxml.py > map.xml
"""
import plan as P
from pgmvox.mapxml import Doc, E

d = Doc("Riftwater", "0.2.0", "Destroy both of the enemy's monuments: one in their market square, one on their "
        "village green.", "dtm")
d.add(E("authors", E("author", text="Claude (freeform generator, ported onto pgmvox)")))
d.add(E("contributors", E("contributor", text="rockymine", contribution="Built the oak and birch trees (tree showcase)")))
item = lambda slot, mat, **k: E("item", slot=slot, material=mat, **k)   # noqa: E731
d.add(E("kits", E("kit",
                  item(0, "iron sword", unbreakable=True),
                  E("item", E("enchantment", text="infinity", level=1), slot=1, material="bow", unbreakable=True),
                  item(2, "diamond pickaxe", unbreakable=True), item(3, "iron axe", unbreakable=True),
                  item(4, "wood", amount=64), item(5, "stained clay", amount=32, team_color=True),
                  item(6, "golden apple", amount=1), item(7, "water bucket"), item(8, "cooked beef", amount=16),
                  item(28, "arrow"),
                  E("helmet", material="leather helmet", unbreakable=True, team_color=True),
                  E("chestplate", material="iron chestplate", unbreakable=True),
                  E("leggings", material="chainmail leggings", unbreakable=True),
                  E("boots", material="leather boots", unbreakable=True, team_color=True), id="spawn-kit")))
P.objectives().write(d)
d.filter("no-void", E("not", E("void")))
d.region("not-build-area", E("negative", E("rectangle", min=f"{-P.RIFT},{P.Z_MIN}", max=f"{P.RIFT},{P.Z_MAX + 1}")))
d.apply(block="no-void", region="not-build-area", message="You may only bridge over the rift!")
d.add(E("maxbuildheight", text=90))
print(d.tostring())
