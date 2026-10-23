"""Frostvault's teams, spawns, wools and seals, read off where the bunker laid them. Nothing is mirrored here: the
composed board already holds both teams' images, and so does everything laid from it.

Each team keeps two wools for the other, one in each of its wool rooms, and places the two it takes on the monuments
outside its spawn's door. A room is sealed by an end stone capsule; nine tenths of it broken opens the room's screen.

    objectives(got)    pgmvox Objectives
    seals(got)         each seal's id and the screen door it opens
"""
import layout as L
from pgmvox import B
from pgmvox.play.objectives import Destroyable, Objectives, Observer, Spawn, Teams, Wool

TEAMS = Teams(*[(*L.TEAMS[k], 24) for k in (0, 1)])
SEAL_COMPLETION = "90%"


class Seal(Destroyable):
    """An end stone capsule laid by `built.bunker`: stamping it is nothing, its region is its box."""

    def stamp(self, w):
        pass

    def check(self, w):
        n = sum(1 for p in self.box.blocks() if w.id(*p) == B.END_STONE)
        return [] if n else [f"seal {self.id}: no end stone in its box"]


def rooms_of(got, k):
    return sorted([r for r in got.rooms if r["k"] == k], key=lambda r: r["found"][0])


def colour(got, r):
    return L.KEPT[r["k"]][rooms_of(got, r["k"]).index(r)]


def seal_id(got, r):
    return f"{L.TEAMS[r['k']][0][:-5]}-{colour(got, r)}-seal"


def objectives(got):
    O = Objectives(TEAMS)
    for s in got.spawns:
        O.add(Spawn(L.TEAMS[s["k"]][0], s["at"], yaw=s["yaw"], kit="spawn-kit", area=s["area"]), mirror=False)
    O.add(Observer((0.5, L.H.ceil - 2, 0.5), yaw=90), mirror=False)
    for s in got.spawns:
        team = L.TEAMS[s["k"]][0]
        slots = sorted(s["slots"])
        for r, slot in zip(rooms_of(got, 1 - s["k"]), slots):
            O.add(Wool(team, colour(got, r), slot, r["found"], r["room"]), mirror=False)
    for r in got.rooms:
        O.add(Seal(seal_id(got, r), f"{colour(got, r).title()} Seal", L.TEAMS[r["k"]][0], r["seal_box"],
                   (B.END_STONE, 0), "end stone", SEAL_COMPLETION, required=False), mirror=False)
    return O


def seals(got):
    return [(seal_id(got, r), r["door"]) for r in got.rooms]
