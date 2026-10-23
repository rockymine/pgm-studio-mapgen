"""Blastworks' teams, spawns, wools, doors and the middle's TNT. Blue's are drawn; red's are their images under the
half turn.

Each team keeps one wool for the other, sealed in the concept's box behind its two doors of end stone (the roof and
the east wall). The doors are destroyables that do not count to win: they are there to be blown open, and their bars
say how far. The wool's monument stands in the spawn's hall, in the corner beside its door.

    objectives()    pgmvox Objectives
"""
import layout as L
from pgmvox import B
from pgmvox.play.objectives import DYES, Box, Destroyable, Objectives, Observer, Spawn, Teams, Wool
from pgmvox.play.rules import Spawner

TEAMS = Teams(("blue-team", "Blue", "blue", 16), ("red-team", "Red", "red", 16))


class Door(Destroyable):
    """A door of end stone laid by parts.box: stamping it is nothing, its region is its box."""

    def stamp(self, w):
        pass

    def check(self, w):
        n = sum(1 for p in self.box.blocks() if w.id(*p) == B.END_STONE)
        return [] if n == len(self.box.blocks()) else [f"door {self.id}: {n} of its blocks are end stone"]


class PadWool(Wool):
    """A wool no block of which lies in its room: PGM's spawner hands it to an attacker in the room, over the middle
    of the room's 2x2 pad. Only the monument is stamped."""

    def stamp(self, w):
        x, y, z = self.slot
        w.set(x, y - 1, z, B.BEDROCK)
        w.set(x, y, z, B.AIR)
        w.set(x, y + 1, z, B.STAINED_GLASS, DYES[self.color])

    def check(self, w):
        return [p for p in super().check(w) if "no wool at" not in p]


def image(p):
    return (-1 - p[0], p[1], -1 - p[2])


def red(b):
    return Box(-1 - b.x1, b.y0, -1 - b.z1, -1 - b.x0, b.y1, -1 - b.z0)


def room_box():
    x0, z0, x1, z1, y0, y1 = L.ROOM
    return Box(x0, y0, z0, x1, y1, z1)


def hall_but_slot():
    """The spawn's area: the hall's room, less the monument's column, where the wool must be placed."""
    x0, z0, x1, z1, y0, y1 = L.HOLLOW
    sx, _, sz = L.SLOT
    assert sx == x1
    return [Box(x0, y0, z0, x1 - 1, y1, z1), Box(x1, y0, z0, x1, y1, sz - 1), Box(x1, y0, sz + 1, x1, y1, z1)]


def objectives():
    O = Objectives(TEAMS, L.SYM)
    x0, z0, x1, z1, y0, y1 = L.HOLLOW
    O.add(Spawn("blue-team", L.SPAWN_AT, yaw=-90, kit="spawn-kit",
                spread=Box(x0 + 1, y0, z0 + 1, x1 - 3, y0, z1 - 1),
                area=hall_but_slot()))
    O.add(Observer((0.5, 30, 0.5), yaw=90), mirror=False)
    # blue takes orange from red's box; red takes lime from blue's
    px, pz = L.ROOM_PAD                                  # the pad's middle, a corner of four blocks
    mid = (px + 0.5, L.BOX_WOOL[1], pz + 0.5)
    O.add(PadWool("blue-team", "orange", L.SLOT, image(L.BOX_WOOL), red(room_box()), spawn_at=image(mid)),
          color="lime", spawn_at=mid)
    for did, name, (x0, z0, x1, z1, y0, y1) in (("blue-roof-door", "Roof Door", L.ROOF_DOOR),
                                                ("blue-side-door", "Side Door", L.SIDE_DOOR)):
        O.add(Door(did, name, "blue-team", Box(x0, y0, z0, x1, y1, z1), (B.END_STONE, 0), "end stone", "100%",
                   required=False), id=did.replace("blue", "red"))
    x0, z0, x1, z1 = L.TNT
    O.add(Spawner("tnt-spawner", (-1, L.MID_H + 1, -1), [("tnt", 2)], delay="20s", max_entities=4, reach=None,
                  box=Box(x0 + 1, L.MID_H + 1, z0 + 1, x1 - 1, L.MID_H + 1, z1 - 1)), mirror=False)
    return O
