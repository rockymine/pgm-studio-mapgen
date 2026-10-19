"""Write Seamworks' map.xml: destroy the monument and capture the flag. Each team spawns in the back of its hall,
defends a monument floating over its crust and a flag that comes back to one of three posts, and scores a flag by
carrying it into its own spawn.

    python3 mapxml.py > map.xml
"""
import os
import sys
from dataclasses import dataclass, replace

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

import plan as P  # noqa: E402
from pgmvox.play.mapxml import E  # noqa: E402
from pgmvox.play.objectives import Box, Destroyable, Flag, Objective, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.play.rules import Build, Item, Kit, Map, Match, terrain_of  # noqa: E402

YS = P.YS


@dataclass
class Net(Objective):
    """Where a team scores the flags it carries: a box, the flag ids it takes, the points it pays its owner."""
    id: str
    team: str
    flags: str
    box: Box
    points: int = 1

    def write(self, doc, teams):
        rid = doc.region(f"{self.id}-region", self.box.cuboid())
        doc.child("flags").append(E("net", id=self.id, owner=self.team, flags=self.flags, points=self.points,
                                    region=rid))

    def cells(self):
        return set()


x0, z0, x1, z1 = P.SPAWN_BOX
spawn_box = Box(x0, YS - 8, z0, x1, YS + 1, z1)
OBJECTIVES = Objectives(Teams(*P.TEAMS), P.SYM)
OBJECTIVES.add(Observer((150, YS + 16, 70), yaw=0, pitch=60))
OBJECTIVES.add(Spawn("green-team", (P.SPAWN_AT[0], YS - 8, P.SPAWN_AT[1]), yaw=270, kit="spawn-kit",
                     area=spawn_box))
OBJECTIVES.add(Flag("green-flag", "Green Flag", "green",
                    [(name, (x, YS + d, z), 270) for name, (x, z), d in P.FLAG_POSTS],
                    shared=False, points_rate=0, respawn_time="10s", team="green-team"), name="Purple Flag", color="purple")
mx, mz = P.MONUMENT
OBJECTIVES.add(Destroyable("green-monument", "Green Monument", "green-team", Box(mx, YS + 3, mz, mx + 1, YS + 4, mz + 1)),
               name="Purple Monument")
# a net is the capturing team's own spawn, taking the other team's flag: written for each team by hand, because
# its flag is the other team's and an image would carry the flag id with the wrong team
OBJECTIVES.add(Net("purple-net", "purple-team", "green-flag", spawn_box.image(P.SYM)), mirror=False)
OBJECTIVES.add(Net("green-net", "green-team", "purple-flag", spawn_box), mirror=False)

M = Map("Seamworks", "0.1.0",
        f"Destroy the enemy monument, or carry their flag into your spawn {P.CAPTURES} times.", ["dtm", "ctf"],
        terrain=terrain_of(__file__),
        authors=["Claude (freeform generator)"],
        objectives=OBJECTIVES,
        kit=Kit(Item("iron sword", 0, unbreakable=True), Item("bow", 1, unbreakable=True),
                Item("iron pickaxe", 2, unbreakable=True, enchant=[("efficiency", 2)]),
                Item("iron axe", 3, unbreakable=True), Item("wood", 4, 64), Item("golden apple", 5, 2),
                Item("wood", 6, 64), Item("arrow", 9, 32),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, wear="leggings"),
                Item("iron boots", unbreakable=True, wear="boots"), clear=True),
        build=Build(max_height=YS + 20),
        match=Match(score=P.CAPTURES, time="20m"))

if __name__ == "__main__":
    print(M.xml())
