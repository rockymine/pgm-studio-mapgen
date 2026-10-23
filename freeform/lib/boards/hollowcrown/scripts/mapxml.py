"""Write Hollowcrown's map.xml: two teams of sixteen, each with a monument atop the Eyrie on its mountain's north spur
and one in the Hall of Echoes beneath it, two spawns a team (the court of Crownhold and the Lower Gate) joined by a
team's own lifts, building up to y 112. Red's half is stated and blue's turned half way round.

    python3 mapxml.py > map.xml
"""


from pgmvox.plan.raster import Symmetry  # noqa: E402
from pgmvox.play.objectives import Box, Destroyable, Objectives, Observer, Portal, Spawn, Teams  # noqa: E402
from pgmvox.play.rules import Build, Item, Kit, Map, terrain_of  # noqa: E402

O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), Symmetry("half"))
O.add(Observer((0, 80, 0), yaw=90))
O.add(Spawn("red-team", (-84, 99, -18), yaw=270, kit="spawn-kit",
            area=[Box(-90, 0, -24, -78, 255, -12), Box(-118, 0, -26, -104, 255, -4)]))   # the court, the Lower Gate
O.add(Portal("red-lift-top", Box(-78, 99, -27, -76, 101, -25), (-112, 22, -14), yaw=90, team="red-team"))
O.add(Portal("red-lift-low", Box(-115, 22, -22, -113, 24, -20), (-84, 99, -18), yaw=270, team="red-team"))
O.add(Destroyable("red-eyrie", "the Eyrie", "red-team", Box(-54, 106, -70, -54, 107, -70)))
O.add(Destroyable("red-echoes", "the Hall of Echoes", "red-team", Box(-66, 23, 16, -66, 24, 16)))

M = Map("Hollowcrown", "0.1.0", "Break both of the enemy's monuments: one atop the Eyrie on their mountain's north "
        "spur, one in the Hall of Echoes in the cavern beneath it.", "dtm",
        terrain=terrain_of(__file__),
        authors=["Claude (freeform generator)"],
        contributors=[("rockymine", "Built the oak and spruce trees (tree showcase)")],
        objectives=O,
        kit=Kit(Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
                Item("diamond pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True),
                Item("wood", 4, 64), Item("wool", 5, 64, team_color=True), Item("wood", 27, 64),
                Item("golden apple", 6), Item("water bucket", 7), Item("cooked beef", 8, 16), Item("arrow", 28),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("iron chestplate", unbreakable=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, wear="leggings"),
                Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=112, void=False))
print(M.xml())
