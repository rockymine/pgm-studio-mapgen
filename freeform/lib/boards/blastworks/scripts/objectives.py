"""Blastworks' teams, spawns, wools and doors. Blue's are drawn; red's are their images under the half turn.

Each team keeps one wool for the other, sealed in the concept's box behind its two doors of end stone (the roof and
the east wall). The doors are destroyables that do not count to win: they are there to be blown open, and their bars
say how far. Over the box, inside its bedrock edge, the box's own team may not go: it defends from in front of it.

    objectives()    pgmvox Objectives
"""
import layout as L
from pgmvox import B
from pgmvox.play.objectives import Box, Destroyable, Objectives, Observer, Spawn, Teams, Wool

TEAMS = Teams(("blue-team", "Blue", "blue", 16), ("red-team", "Red", "red", 16))


class Door(Destroyable):
    """A door of end stone laid by build.box: stamping it is nothing, its region is its box."""

    def stamp(self, w):
        pass

    def check(self, w):
        n = sum(1 for p in self.box.blocks() if w.id(*p) == B.END_STONE)
        return [] if n == len(self.box.blocks()) else [f"door {self.id}: {n} of its blocks are end stone"]


def image(p):
    return (-1 - p[0], p[1], -1 - p[2])


def room_box():
    x0, z0, x1, z1, y0, y1 = L.ROOM
    return Box(x0, y0, z0, x1, y1, z1)



def red(b):
    return Box(-1 - b.x1, b.y0, -1 - b.z1, -1 - b.x0, b.y1, -1 - b.z0)


def objectives():
    O = Objectives(TEAMS, L.SYM)
    sx0, sz0, sx1, sz1 = L.SPAWN_AREA
    O.add(Spawn("blue-team", L.SPAWN, yaw=-90, kit="spawn-kit",
                spread=Box(sx0 + 2, L.SPAWN_H + 1, sz0 + 2, sx1 - 2, L.SPAWN_H + 1, sz1 - 2),
                area=Box(sx0, L.SPAWN_H + 1, sz0, sx1, L.SPAWN_H + 6, sz1)))
    O.add(Observer((0.5, 30, 0.5), yaw=90), mirror=False)
    # blue takes orange from red's box; red takes lime from blue's
    O.add(Wool("blue-team", "orange", L.SLOT, image(L.BOX_WOOL), red(room_box())), color="lime")
    for did, name, (x0, z0, x1, z1, y0, y1) in (("blue-roof-door", "Roof Door", L.ROOF_DOOR),
                                                ("blue-side-door", "Side Door", L.SIDE_DOOR)):
        O.add(Door(did, name, "blue-team", Box(x0, y0, z0, x1, y1, z1), (B.END_STONE, 0), "end stone", "100%",
                   required=False))
    return O
