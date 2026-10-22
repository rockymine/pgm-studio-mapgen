"""Write Blastworks' map.xml: teams, spawns, wools, doors and the middle's TNT from objectives.py; stated here are the
kit with its TNT, building over the void only in the build zones the redstone rings and up to y 32, the box's top
inside its bedrock line closed to its own team, and what may be broken.

    python3 mapxml.py > map.xml
"""
import layout as L
import objectives as P
import parts
from pgmvox.play.mapxml import E
from pgmvox.play.objectives import Box
from pgmvox.play.rules import Build, Crafting, Item, Kit, Map, Tnt, terrain_of

BRINGS = ("wood", "tnt", "glass", "ladder")


class OnTheBox:
    """Over each box, inside its bedrock edge, its own team may not go: the roof door is defended from in front."""

    def write(self, doc):
        x0, z0, x1, z1, y0, y1 = L.ON_THE_BOX
        for team, b in (("blue", Box(x0, y0, z0, x1, y1, z1)), ("red", P.red(Box(x0, y0, z0, x1, y1, z1)))):
            rid = doc.region(f"{team}-box-top", b.cuboid())
            doc.apply(enter=f"not-{team}", region=rid, message="You may not stand on your own wool's box!")


class Breaking:
    """What a player brings breaks, and end stone by a blast alone; the works themselves hold."""

    def write(self, doc):
        doc.filter("may-break", E("any", *[E("material", text=m) for m in BRINGS],
                                  E("all", E("material", text="end stone"), E("cause", text="explosion"))))
        doc.apply(block_break="may-break", message="Only what was built breaks, and the doors by a blast!")


M = Map("Blastworks", "1.0.0", "Blow your way into the enemy's box, take their wool and bring it home.", "ctw",
        terrain=terrain_of(__file__), authors=["Claude (freeform generator, on pgmvox)"],
        objectives=P.objectives(),
        kit=Kit(
            Item("stone sword", 0, unbreakable=True), Item("bow", 1, unbreakable=True),
            Item("iron pickaxe", 2, enchant=[("efficiency", 1)], unbreakable=True),
            Item("iron axe", 3, unbreakable=True), Item("wood", 4, 64), Item("tnt", 5, 12),
            Item("glass", 6, 32), Item("golden apple", 7), Item("wood", 8, 64), Item("arrow", 28, 32),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
            Item("leather leggings", unbreakable=True, team_color=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(areas=L.ZONES + [parts.image(r) for r in L.ZONES], max_height=L.MAX_BUILD),
        parts=[OnTheBox(), Breaking(), Tnt(), Crafting()])
print(M.xml())
