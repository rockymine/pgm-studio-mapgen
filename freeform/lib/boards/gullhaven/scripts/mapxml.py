"""Write Gullhaven's map.xml: a free-for-all under rage, a kill a point, eight minutes; a player respawns at whichever
of the island's points lies farthest from the others; the sea past the island closed, no building, no fall damage,
the clock held.

    python3 mapxml.py > map.xml
"""


from pgmvox.play.objectives import Box, Objectives, Observer, Spawn  # noqa: E402
from pgmvox.play.rules import Bounds, Build, Effect, Item, Kit, Map, Match, Respawn, terrain_of  # noqa: E402

POINTS = [(-44, 42, -30, -90), (-30, 41, -36, 0), (-18, 41, -44, 90), (-34, 41, -16, 180), (-7, 25, -37, 0),
          (-8, 25, -44, 180), (8, 37, -46, 0), (30, 37, -38, 90), (20, 33, -26, 0), (46, 33, -26, 90),
          (-1, 33, -17, 0), (40, 29, -8, 180), (16, 29, -8, 0), (4, 29, 4, 90), (30, 25, 12, 0), (16, 23, 16, 180),
          (26, 23, 31, 180), (9, 23, 33, 0), (-6, 30, 10, 0), (-20, 30, 20, 0), (-12, 31, 30, 90), (-30, 29, 12, 0),
          (-4, 30, 36, 180), (-52, 20, 2, -90), (-50, 21, 16, -90), (-22, 26, 59, 0), (-13, 26, 58, 90),
          (-34, 22, -26, 0), (-20, 22, -4, 180)]      # (x, y, z, yaw): the blocks a player may come back on

O = Objectives()
O.add(Observer((0, 62, 0), yaw=135))
O.add(Spawn(None, POINTS[0][:3], kit="spawn-kit", points=POINTS, far=True, safe=True))
O.add(Bounds(Box(-62, 0, -56, 58, 255, 72), "The sea is too rough past here."))   # for swimming in, not away

M = Map("Gullhaven", "0.1.0", "Kill the most players in 8 minutes. One hit kills; every kill pays an arrow.",
        ["ffa", "rage"],
        terrain=terrain_of(__file__), authors=["Claude (freeform generator)"], includes=[], players=(2, 16),
        objectives=O,
        kit=Kit(Item("iron sword", 0, enchant=[("sharpness", 1)], unbreakable=True, name="Gutting Knife"),
                Item("bow", 1, enchant=[("power", 1)], unbreakable=True, name="Longbow"), Item("arrow", 2),
                Item("leather chestplate", unbreakable=True, team_color=True, locked=True, wear="chestplate"),
                clear=True, effects=[Effect("damage resistance", "2s", amplifier=255)], game_mode="adventure",
                reward=[Item("arrow")]),
        build=Build(never=True, use=False),
        match=Match(rage=True, kills=1, time=8 * 60, respawn=Respawn("2s", auto=True), fall_damage=False,
                    time_of_day=5000))
print(M.xml())
