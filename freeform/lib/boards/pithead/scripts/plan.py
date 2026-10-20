"""Pithead: the plan every other script reads. The board starts from the composer's micro board seed 96 under rot_180
(`composed-layout.json`, `composed-intent.json`, composer walled-5): its pieces become cuts dug into solid ground,
its play structure is kept, and red's half is moved fourteen blocks along x so the two halves stand off each other.
Red's unit is stated here and blue's is its half turn about the board's centre.

Heights are blocks over the hub's walking level YS. The finish is Seamworks' (`../../seamworks/scripts/look.py`),
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


# ---- the grid: a composed point (x, z) of red's half lies at (x + OX, z + OZ), which puts red's half SHIFT blocks
# off the board's long axis at x = W / 2 and blue's, by the half turn, as far off the other way ------------------------
SHIFT = 14
OX, OZ = 74 - SHIFT, 120
W, H = 148, 240
YS = 24                                  # the hub's walking level; its top block is YS - 1
GROUND = YS + 12                         # the surface's walking level: the ground the cuts are dug down from
MAX_BUILD = YS + 8                       # no block is placed this high, so nobody builds out of a cut
KILL_Y = YS - 8
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
COMPOSED = {k: _moved(_SHAPES[k]["vertices"]) for k in ("frontline-9", "hub-9", "spawn-9", "wool-a-9", "wool-b-9")}

# ---- the cuts, red's half: the composed pieces, each wool corridor moved LANE_SHIFT toward the spawn and its body
# lengthened to meet it. Each is (polygon, level over YS) --------------------------------------------------------------
LANE_SHIFT = 10
CUTS = {"frontline": (COMPOSED["frontline-9"], -2),
        "hub": ([(40, 168), (88, 168), (88, 204), (78, 216), (50, 216), (40, 204)], 0),
        "spawn": (COMPOSED["spawn-9"], 2),
        "red corridor": ([(28, 186), (40, 186), (40, 198), (28, 198)], 0),
        "red body": ([(16, 160), (28, 160), (28, 198), (16, 198)], 5),
        "orange corridor": ([(88, 190), (100, 190), (100, 202), (88, 202)], 0),
        "orange body": ([(100, 164), (112, 164), (112, 202), (100, 202)], 5)}
# flights between cuts: (polygon, (low point, level), (high point, level)); their step edges wander
FLIGHTS = [([(44, 162), (76, 162), (76, 172), (44, 172)], ((60, 162), -2), ((60, 171), 0)),
           ([(50, 206), (78, 206), (78, 216), (52, 216)], ((60, 206), 0), ((60, 215), 2))]
FRONT_EDGE = 144                         # the frontline's open edge over the void: red's ground stops here
MARGIN = (4, 8)                          # how far the ground runs past the cuts to the board's edge, low and high

# ---- the middle: two islands, each standing in front of its own team's frontline, the gap between them crossed
# sideways -------------------------------------------------------------------------------------------------------------
ISLAND = ([(44, 116), (70, 116), (70, 134), (44, 134)], -3)
ISLAND_ROCK = [(44, 116), (51, 116), (50, 119), (47, 122), (44, 121)]
ISLAND_ROCK_RISE = 5
DAIS = (54, 122, 6)                      # the golden apple's dais on red's island
APPLE_DELAY = "45s"
# where a player may build out over the void, inclusive blocks: frontline to island, island to island
BUILD = [(42, 133, 77, 145), (68, 114, 79, 125)]

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
# each wool corridor's bedrock wall and its chests, moved with the corridor
WALLS = [((v["x1"] + OX, v["z1"] + OZ + LANE_SHIFT), (v["x2"] + OX, v["z2"] + OZ + LANE_SHIFT)) for v in _s["walls"]
         if v["stamp"]["image"] == 0]
CHESTS = [((c["x"] + OX, c["z"] + OZ + LANE_SHIFT), c["facing"]) for c in _s["chests"] if c["stamp"]["image"] == 0]
LINES = [((v["x1"] + OX, v["z1"] + OZ), (v["x2"] + OX, v["z2"] + OZ)) for v in _s["redstoneLines"]
         if v["stamp"]["image"] == 0]
WALL_COURSES = 3                         # a defence wall's height over the floor
# the capturing team's monuments on its spawn yard, in front of the hall: red places blue's two wools here
MONUMENTS = [(SPAWN_AT[0] - 5, SPAWN_ROOM[1] - 5), (SPAWN_AT[0] + 4, SPAWN_ROOM[1] - 5)]

# ---- where a wool corridor meets its body, the body stands a ledge over it: a ladder up bare rock on one half of the
# ledge and a panel leaned on the rock over the other. (ladder cell, the side its rock is on), panel foot a -> b -------
LEDGES = [((28, 188), "w", ((28, 191.5), (28, 197.5))), ((99, 192), "e", ((100, 195.5), (100, 201.5)))]

# ---- the works: a hall over the spawn room with the yard in front of it, a works building over each wool room ------
HALL = ([(52, 223), (68, 223), (68, 232), (52, 232)], 3, ((53, 230), "w"))
HALL_DOOR = [(59, 223), (60, 223), (61, 223)]
HALL_CHIMNEY = (65, 229, 66, 230)
WORKS = [([(16, 160), (28, 160), (28, 169), (16, 169)], 2, ((17, 161), "w"), [(21, 168), (22, 168), (23, 168)]),
         ([(100, 164), (112, 164), (112, 173), (100, 173)], 2, ((110, 165), "e"),
          [(105, 172), (106, 172), (107, 172)])]
ROOM_HEIGHT = 9                          # a wool room's region over its floor: both storeys

# ---- the cut walls held back by panels, red's, as feet a -> b along the cut's edge; every other wall is bare rock ----
LIP = 2                                  # how far a panel stands over the ground behind it
PANELS = [((44, 145), (44, 161)), ((76, 161), (76, 145)),
          ((88, 171), (88, 188)), ((40.6, 205), (49.4, 215.4)),
          ((28, 161), (28, 172.5)), ((28, 173.5), (28, 181)),
          ((100, 165), (100, 176.5)), ((100, 177.5), (100, 185))]

# ---- the hub: two plated strips over the seam where the composer's shaft was, the headframe over the middle one ------
SEAM_Y = 4                               # the seam's lava, two deep on the bedrock under every plated strip
STRIPS = [((64, 186), (64, 198), 10, [4, 4, 4], {(1, 0), (2, 1)}),
          ((75.5, 175), (83.5, 185), 6, [4.5, 4.5, 4], {(1, 1)})]
HEADFRAME = 18                           # the legs' height over the floor
HEADFRAME_TAPER = 4                      # how far each leg leans in over that height
HUT = (6, 4, "e", (41, 172))             # length, depth, the side its door faces, its corner: against the west wall
FRONT_ROCK = [(56, 145), (63, 145), (65, 149), (61, 152), (57, 151)]
FRONT_ROCK_RISE = 4

# ---- what the floors carry: chevrons as (tip, the way they point) in red's colour, the emblem on the hub ------------
CHEVRONS = [((60, 157), (0, -1)), ((43, 192), (-1, 0)), ((85, 196), (1, 0)), ((22, 182), (0, -1)),
            ((106, 186), (0, -1)), ((67, 125), (1, 0))]
EMBLEM = ((64, 176), 3)                  # a diamond's centre and its reach
OLIVES = ["olive-7", "olive-9"]
TREES_PER_SIDE = 4
BIOME_MESA, BIOME_SWAMP = 37, 6

# ---- what Seamworks' look reads --------------------------------------------------------------------------------------
CRUST = np.zeros((W, H), int)
_APRON = set()


def ground(x, z):
    return GROUND


def on_apron(x, z):
    return (x, z) in _APRON


def set_apron(cells):
    _APRON.clear()
    _APRON.update(cells)


SP = seamworks("plan", "seamworks_plan")         # its panel layout: outward normals and runs along a wall
