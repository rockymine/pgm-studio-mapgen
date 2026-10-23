"""Coldstore's teams, spawns, wools and seals. Blue's are drawn, its north half as the image of its south across
v -0.5; red's are blue's under the mirror between the teams.

Each team keeps two wools for the other, one in the wool room of each of its quarters, and places the two it takes
on the monuments by its spawn. A wool room is sealed by an end stone monument in a glass case: breaking nine tenths
of it opens the room's screen (a trigger), and the seal counts for nothing else.

    objectives()    pgmvox Objectives
    seals()         each seal's id and the screen door it opens, for the map's triggers
"""
import layout as L
import rooms
from pgmvox import B
from pgmvox.play.objectives import Box, Destroyable, Objectives, Observer, Spawn, Teams, Wool

TEAMS = Teams(("blue-team", "Blue", "blue", 16), ("red-team", "Red", "red", 16))
MAX_BUILD = L.ROOF[0]
SEAL_COMPLETION = "90%"


def flip_v(p):
    return (p[0], p[1], -1 - p[2])


def room_box(north=False, east=False):
    u0, u1, v0, v1 = L.ROOM
    b = Box(u0, L.ROOM_FLOOR + 1, v0, u1, L.ROOM_FLOOR + 4, v1)
    if north:
        b = Box(b.x0, b.y0, -1 - b.z1, b.x1, b.y1, -1 - b.z0)
    if east:
        b = Box(-1 - b.x1, b.y0, b.z0, -1 - b.x0, b.y1, b.z1)
    return b


def east(p):
    return (-1 - p[0], p[1], p[2])


class Seal(Destroyable):
    """The end stone capsule: built by rooms.wool_block, so stamping it is nothing; the region is its box."""

    def stamp(self, w):
        pass

    def check(self, w):
        n = sum(1 for p in self.box.blocks() if w.id(*p) == B.END_STONE)
        return [] if n else [f"seal {self.id}: no end stone in its box"]


def seal_box(north=False):
    u0, u1, v0, v1, y0, y1 = L.MONUMENT
    if north:
        v0, v1 = -1 - v1, -1 - v0
    return Box(u0, y0, v0, u1, y1, v1)


def objectives():
    O = Objectives(TEAMS, L.SYM)
    s0, s1, sv0, sv1 = L.SPAWN_ROOM
    O.add(Spawn("blue-team", L.SPAWN, yaw=-90, kit="spawn-kit", spread=Box(s0 + 1, L.TOP + 1, sv0 + 2, s1 - 3,
                                                                           L.TOP + 1, sv1 - 2),
                area=Box(s0, L.TOP + 1, sv0, s1, L.TOP + 6, sv1)))
    O.add(Observer((0.5, L.CEIL - 2, 0.5), yaw=90), mirror=False)
    # blue takes purple from red's south room and yellow from its north; red takes orange and lime from blue's
    O.add(Wool("blue-team", "purple", L.SLOT, east(L.WOOL_FOUND), room_box(east=True)), color="orange")
    O.add(Wool("blue-team", "yellow", flip_v(L.SLOT), east(flip_v(L.WOOL_FOUND)), room_box(north=True, east=True)),
          color="lime")
    for north, name in ((False, "South"), (True, "North")):
        O.add(Seal(f"blue-{name.lower()}-seal", f"{name} Seal", "blue-team", seal_box(north), (B.END_STONE, 0),
                   "end stone", SEAL_COMPLETION, required=False))
    return O


def seals():
    """(seal id, the screen's door blocks) for every seal on the board."""
    door = rooms.screen_door()
    out = []
    for team, fx in (("blue", lambda p: p), ("red", east)):
        for north, name in ((False, "south"), (True, "north")):
            out.append((f"{team}-{name}-seal", [fx(flip_v(p) if north else p) for p in door]))
    return out
