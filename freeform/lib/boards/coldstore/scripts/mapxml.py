"""Write Coldstore's map.xml: teams, spawns, wools and seals come from objectives.py; stated here are the kit with its
TNT, building anywhere under the roof, what may be broken, each seal's trigger opening its screen, and the islands'
drifts growing back.

**Only what a player brings, the islands' drifts, the seals' glass cases and, by a blast alone, their end stone may
be broken.** Everything the bunker is made of holds: a wall is a wall for the whole match, and the void stays void
unless a player bridges it.

    python3 mapxml.py > map.xml
"""
import layout as L
import objectives as P
from pgmvox.play.logic import Fill, Trigger, Completed
from pgmvox.play.mapxml import E
from pgmvox.play.objectives import Box
from pgmvox.play.rules import Build, Crafting, Item, Kit, Map, Renewables, Tnt, terrain_of

BRINGS = ("wood", "tnt", "glass", "ladder")                     # what the kit carries
DRIFTS = ("snow block", "snow", "packed ice", "ice", "gravel")  # what lies on the islands, and grows back
CASE = ("stained glass",)


class Breaking:
    """Breaking, by hand or by blast: what a player brings, the drifts and the cases, and end stone only by a blast."""

    def write(self, doc):
        doc.filter("may-break", E("any", *[E("material", text=m) for m in BRINGS + DRIFTS + CASE],
                                  E("all", E("material", text="end stone"), E("cause", text="explosion"))))
        doc.apply(block_break="may-break", message="Only what was built, the drifts and the seals break here!")


def span(blocks):
    """The box round a list of blocks."""
    xs, ys, zs = zip(*blocks)
    return Box(min(xs), min(ys), min(zs), max(xs), max(ys), max(zs))


def islands():
    """Every island's drift layer on the whole board: the drawn quarter's and its three images."""
    out = []
    for u0, u1, v0, v1 in L.ISLANDS:
        for fu in (False, True):
            for fv in (False, True):
                a0, a1 = (-1 - u1, -1 - u0) if fu else (u0, u1)
                b0, b1 = (-1 - v1, -1 - v0) if fv else (v0, v1)
                out.append(Box(a0, L.TOP + 1, b0, a1, L.TOP + 4, b1))
    return out


M = Map("Coldstore", "1.0.0", "Blow open the enemy's wool rooms and bring their two wools home.", "ctw",
        terrain=terrain_of(__file__), authors=["Claude (freeform generator, on pgmvox)"],
        objectives=P.objectives(),
        kit=Kit(
            Item("stone sword", 0, unbreakable=True), Item("bow", 1, unbreakable=True),
            Item("iron pickaxe", 2, enchant=[("efficiency", 1)], unbreakable=True),
            Item("iron axe", 3, unbreakable=True), Item("wood", 4, 64), Item("tnt", 5, 16),
            Item("glass", 6, 32), Item("golden apple", 7), Item("wood", 8, 64), Item("arrow", 28, 32),
            Item("iron spade", 29, unbreakable=True),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
            Item("leather leggings", unbreakable=True, team_color=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(void=False, max_height=P.MAX_BUILD),
        parts=[Breaking(), Tnt(), Crafting(),
               Renewables(islands(), rate=0.5, avoid=4, id="drifts")]
        + [Trigger(Completed(sid), [Fill([span(door)], "air")]) for sid, door in P.seals()])
print(M.xml())
