"""Pithead: the plan every other script reads. The board is the composer's micro board seed 96 under rot_180
(`composed-layout.json`, `composed-intent.json`, composer walled-5), moved onto a positive grid and taken over:
red's unit is stated here and blue's is its half turn about the board's centre.

Heights are blocks over the floor's walking level YS. The finish is Seamworks' (`../../seamworks/scripts/look.py`),
which reads W, H, CRUST and on_apron from this module."""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".."))

import numpy as np  # noqa: E402

from pgmvox.plan.raster import Symmetry  # noqa: E402

SEAMWORKS = os.path.join(HERE, "..", "..", "seamworks", "scripts")


def seamworks(name, alias):
    """One of Seamworks' scripts loaded under its own name, so it does not shadow this board's."""
    if alias in sys.modules:
        return sys.modules[alias]
    spec = importlib.util.spec_from_file_location(alias, os.path.join(SEAMWORKS, f"{name}.py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[alias] = module
    spec.loader.exec_module(module)
    return module


# ---- the grid: the composed board's -56..56 by -116..116 moved by OX, OZ, with room round it for the outline ------
OX, OZ = 60, 120
W, H = 120, 240
YS = 34                                  # the floor's walking level; its top block is YS - 1
KILL_Y = YS - 28
SYM = Symmetry("half", axis=((W - 1) / 2, (H - 1) / 2))


def R(p):
    """A vertex under the half turn."""
    return (W - p[0], H - p[1])


def RC(c):
    """A block under the half turn."""
    return (W - 1 - c[0], H - 1 - c[1])


def _moved(points):
    return [(x + OX, z + OZ) for x, z in points]


_LAYOUT = json.load(open(os.path.join(HERE, "composed-layout.json")))
_INTENT = json.load(open(os.path.join(HERE, "composed-intent.json")))
_SHAPES = {s["id"]: s for s in _LAYOUT["layers"][0]["layout"]["shapes"]}
PIECES = {k: _moved(_SHAPES[k]["vertices"]) for k in
          ("frontline-9", "hub-9", "spawn-9", "wool-a-9", "wool-b-9", "mid-stone-0-9")}
HOLE = _moved(_SHAPES["void-1-cut"]["vertices"])
_b = _INTENT["build"]["areas"][0]
BUILD = (_b["minX"] + OX, _b["minZ"] + OZ, _b["maxX"] + OX - 1, _b["maxZ"] + OZ - 1)     # inclusive blocks

# ---- play, red's side ------------------------------------------------------------------------------------------------
TEAMS = (("red-team", "Red", "red"), ("blue-team", "Blue", "blue"))
_spawn = next(s for s in _INTENT["spawns"] if s["team"] == "red")
_p = _spawn["protection"][0]
SPAWN_ROOM = (_p["minX"] + OX, _p["minZ"] + OZ, _p["maxX"] + OX - 1, _p["maxZ"] + OZ - 1)
SPAWN_AT = (_spawn["point"]["x"] + OX, _spawn["point"]["z"] + OZ)
SPAWN_YAW = _spawn["yaw"]


def _room(w):
    p = w["protection"][0]
    door = w["doors"][0]
    return dict(color=w["color"], room=(p["minX"] + OX, p["minZ"] + OZ, p["maxX"] + OX - 1, p["maxZ"] + OZ - 1),
                at=(w["spawn"]["x"] + OX, w["spawn"]["z"] + OZ), door=(door["x"] + OX, door["z"] + OZ),
                edge=door["edge"])


WOOL_ROOMS = [_room(w) for w in _INTENT["wools"] if w["owner"] == "red"]       # red keeps these, blue takes them
_s = _INTENT["structures"]
WALLS = [((v["x1"] + OX, v["z1"] + OZ), (v["x2"] + OX, v["z2"] + OZ), v["topY"] - 9) for v in _s["walls"]
         if v["stamp"]["image"] == 0]
CHESTS = [((c["x"] + OX, c["z"] + OZ), c["facing"]) for c in _s["chests"] if c["stamp"]["image"] == 0]
LINES = [((v["x1"] + OX, v["z1"] + OZ), (v["x2"] + OX, v["z2"] + OZ)) for v in _s["redstoneLines"]
         if v["stamp"]["image"] == 0]
# the capturing team's monuments on its spawn yard, in front of the hall: red places blue's two wools here
MONUMENTS = [(SPAWN_AT[0] - 5, SPAWN_ROOM[1] - 5), (SPAWN_AT[0] + 4, SPAWN_ROOM[1] - 5)]

# ---- the floor's levels over YS, red's half. The stone is the floor the diggers cut: the hub, the corridors to the
# wool, the spawn and the middle. The ground they left is the orange surface SURFACE_RISE over YS, walked on the
# frontline and round each wool's works, and a ramp is cut up through it wherever the two meet ------------------------
LEVELS = [(PIECES["mid-stone-0-9"], -3), (PIECES["spawn-9"], 2)]
SURFACE_RISE = 3
SURFACE = [PIECES["frontline-9"], [(16, 160), (28, 160), (28, 188), (16, 188)],
           [(100, 164), (112, 164), (112, 192), (100, 192)]]
FLIGHTS = [([(55, 158), (65, 158), (65, 168), (55, 168)], ((60, 168), 0), ((60, 159), 3)),
           ([(22, 176), (28, 176), (28, 188), (22, 188)], ((28, 182), 0), ((23, 182), 3)),
           ([(100, 180), (106, 180), (106, 192), (100, 192)], ((100, 186), 0), ((105, 186), 3)),
           ([(52, 205), (76, 205), (76, 216), (52, 216)], ((60, 205), 0), ((60, 215), 2))]
# the walls of panels holding the surface and the banks back from the stone, as (a, b, the way into the ground); two
# walls meeting at an outside corner each stop short of it, so neither runs through the other
FACES = [((44, 168), (52, 168), (0, -1)), ((68, 168), (76, 168), (0, -1)),
         ((55, 158), (55, 165.5), (-1, 0)), ((65, 165.5), (65, 158), (1, 0)),
         ((22, 176), (28, 176), (0, -1)), ((100, 180), (106, 180), (0, -1)),
         ((40, 202), (47.5, 202), (0, 1)), ((51, 204.5), (51, 216), (-1, 0)),
         ((80.5, 202), (88, 202), (0, 1)), ((77, 216), (77, 204.5), (1, 0))]

# ---- the works: a hall over the spawn room with the yard in front of it, a works building over each wool room ------
HALL = ([(52, 223), (68, 223), (68, 232), (52, 232)], 3, ((53, 230), "w"))
HALL_DOOR = [(59, 223), (60, 223), (61, 223)]
HALL_CHIMNEY = (65, 229, 66, 230)
WORKS = [([(16, 160), (28, 160), (28, 169), (16, 169)], 2, ((17, 161), "w"), [(21, 168), (22, 168), (23, 168)]),
         ([(100, 164), (112, 164), (112, 173), (100, 173)], 2, ((110, 165), "e"),
          [(105, 172), (106, 172), (107, 172)])]
ROOM_HEIGHT = 9                                   # a wool room's region over its floor: both storeys

# ---- the hub's back corners stand undug: banks of orange ground under soot, BANK_RISE over the floor, faced with
# panels toward the hub -----------------------------------------------------------------------------------------------
BANK_RISE = 6
LIP = 2                                           # how far a panel stands over the bank behind it
BANKS = [[(40, 202), (51, 202), (51, 216), (40, 216)], [(77, 202), (88, 202), (88, 216), (77, 216)]]

# ---- the shaft's headframe, and the rock and clutter that break up each open floor -----------------------------------
HEADFRAME = 18                                    # the legs' height over the floor
HEADFRAME_TAPER = 4                               # how far each leg leans in over that height
HUT = (6, 4, "e", (43, 190))                      # length, depth, the side its door faces, its corner
SPOIL = ([(78, 170), (85, 170), (87, 175), (84, 179), (78, 178)], [(80.5, 172.5), (83.5, 176.5)], 3)
SURFACE_OLIVES = [(49, 151), (71, 152)]           # where the frontline's bare olives stand
MID_ROCK = [(48, 108), (56, 108), (55, 111), (52, 114), (48, 114)]
MID_ROCK_RISE = 5
FRONT_ROCK = [(56, 145), (63, 145), (65, 149), (61, 152), (57, 151)]
FRONT_ROCK_RISE = 4
DAIS = (57, 117, 6)
APPLE_DELAY = "45s"

# ---- the outline: a void edge is pushed out by up to OUTLINE blocks, but never into the build zone, the shaft, or
# past a defence wall's ends ------------------------------------------------------------------------------------------
OUTLINE = 2

# ---- chevrons, red's: on the hub, pointing at blue ------------------------------------------------------------------
CHEVRONS = [((60, 178), (0, -1))]
OLIVES = ["olive-7", "olive-9"]
BIOME_MESA, BIOME_SWAMP = 37, 6

# ---- what Seamworks' look reads --------------------------------------------------------------------------------------
CRUST = np.zeros((W, H), int)
_APRON = set()


def ground(x, z):
    return YS


def on_apron(x, z):
    return (x, z) in _APRON


def set_apron(cells):
    _APRON.clear()
    _APRON.update(cells)


SP = seamworks("plan", "seamworks_plan")         # its panel layout: outward normals and runs along a wall
