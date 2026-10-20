"""Write Pithead's map.xml: capture the wool for two teams. Each team spawns in the hall at its back, keeps two wools in
the works at the ends of its two approaches, each behind a bedrock wall and up a ledge, and places the other team's
two on the monuments in its own spawn yard. Building over the void is allowed only across the middle's gaps, and no
block is placed high enough to climb out of a cut.

    python3 mapxml.py > map.xml
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

import plan as P  # noqa: E402
from pgmvox.play.objectives import Box, Objectives, Observer, Spawn, Teams, Wool  # noqa: E402
from pgmvox.play.rules import Build, Item, KillHeight, Kit, Map, Match, Spawner, terrain_of  # noqa: E402

YS = P.YS
IMAGE = {"red": "blue", "orange": "light_blue"}           # a red room's wool and the wool blue keeps in its image

x0, z0, x1, z1 = P.SPAWN_ROOM
spawn_box = Box(x0, YS + 2, z0, x1, YS + 2 + 3 * 5, z1)
OBJECTIVES = Objectives(Teams(*[(t, n, c, 7) for t, n, c in P.TEAMS]), P.SYM)
OBJECTIVES.add(Observer((74, YS + 34, 120), yaw=0, pitch=70), mirror=False)
OBJECTIVES.add(Spawn("red-team", (P.SPAWN_AT[0], YS + 2, P.SPAWN_AT[1]), yaw=P.SPAWN_YAW, kit="spawn-kit",
                     area=spawn_box))
for k, room in enumerate(P.WOOL_ROOMS):
    rx0, rz0, rx1, rz1 = room["room"]
    ax, az = room["at"]
    mx, mz = P.RC(P.MONUMENTS[k])                         # blue places red's wools in blue's own yard
    floor = YS + P.CUTS["red body"][1]
    OBJECTIVES.add(Wool("blue-team", room["color"], slot=(mx, YS + 2, mz), found=(ax, floor, az),
                        room=Box(rx0, floor, rz0, rx1, floor + P.ROOM_HEIGHT - 1, rz1)), color=IMAGE[room["color"]])
dx, dz, size = P.DAIS
apple_y = YS + P.ISLAND[1] + 2                            # the block over the dais' plinth, on the island's floor
middles = (("red", (dx + size // 2 - 1, dz + size // 2 - 1)), ("blue", P.RC((dx + size // 2, dz + size // 2))))
for name, (ax, az) in middles:
    OBJECTIVES.add(Spawner(f"golden-apple-{name}-island", (ax, apple_y, az), [("golden apple", 1)], delay=P.APPLE_DELAY,
                           box=Box(ax, apple_y, az, ax + 1, apple_y + 1, az + 1)), mirror=False)

M = Map("Pithead", "0.1.0", "Capture the enemy's two wools from the works at the ends of their approaches, and place "
        "them on the monuments in your spawn yard.", "ctw",
        terrain=terrain_of(__file__),
        authors=["Claude (freeform generator)"],
        objectives=OBJECTIVES,
        kit=Kit(Item("iron sword", 0, unbreakable=True), Item("bow", 1, unbreakable=True),
                Item("iron pickaxe", 2, unbreakable=True, enchant=[("efficiency", 2)]),
                Item("iron axe", 3, unbreakable=True), Item("wood", 4, 64), Item("golden apple", 5, 2),
                Item("wood", 6, 64), Item("shears", 7, unbreakable=True), Item("arrow", 9, 32),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, wear="leggings"),
                Item("iron boots", unbreakable=True, wear="boots"), clear=True),
        build=Build(areas=P.BUILD + [(*P.RC(b[2:]), *P.RC(b[:2])) for b in P.BUILD], max_height=P.MAX_BUILD),
        kill=KillHeight(P.KILL_Y),
        match=Match(time="25m"))

if __name__ == "__main__":
    print(M.xml())
