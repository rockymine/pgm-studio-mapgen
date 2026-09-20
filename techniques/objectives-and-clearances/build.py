"""Writes objectives-and-clearances.layout.json and .intent.json — one island carrying a monument, a core
and a wool, and the ground each of them needs around it.

Unlike the terrain cards this one is a map: an objective is a statement in the INTENT, not in the layout,
and the two gates that judge where one may stand are heard for the first time at the export, after the
whole world has been built. So the board is one place with five stations along it, and the card's second
half is the same intent exported again with one fault in it at a time — `faults()` writes those.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cards import SOLID, depth_stack, moor, round_ring

WEST, EAST = -210, 210
NORTH, SOUTH = -50, 50
GROUND_TOP = 40
PLAIN = 12

MOOR = moor(grass_to=35, dirt_to=55)
FLAG = {   # the ten-block square `OB19` keeps clear, painted so it can be seen from above
    "bedrock": {"relative": False, "value": 1}, "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": SOLID(1)},
    "wallEnabled": True, "wallOnTerrainFaces": True, "wall": SOLID(1), "fill": SOLID(1),
    "surface": {"enabled": True, "depth": 3, "material": depth_stack((SOLID(13), 1), (SOLID(3, 1), 2))},
}
ROOM = {   # the wool room, so its walls can be told from the ground they stand on
    "bedrock": {"relative": False, "value": 1}, "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": SOLID(98, 1)},
    "wallEnabled": True, "wallOnTerrainFaces": True, "wall": SOLID(98), "fill": SOLID(98),
    "surface": {"enabled": True, "depth": 1, "material": SOLID(98)},
}

# Where each thing stands. One island, five stations along it, far enough apart that no clearance box
# touches another — which is the first thing an author has to get right and the last thing anything checks.
RED_SPAWN = (-180, 0)
MONUMENT = (-70, 0)
CORE = (30, 0)
WOOL_ROOM = (130, 0)
BLUE_SPAWN = (180, 0)
PROTECT = 10          # half the side of a spawn's protection box
KEEP_OUT = 10         # `OB19`: a ten-block square about a goal's anchor


def box(cx, cz, half_x, half_z):
    return {"min_x": cx - half_x, "min_z": cz - half_z, "max_x": cx + half_x, "max_z": cz + half_z}


def rect(shape_id, cx, cz, half_x, half_z, theme="moor", **words):
    out = {"id": shape_id, "type": "rectangle", "operation": "add", "floor": 0,
           "base_height": GROUND_TOP, "theme": theme, **box(cx, cz, half_x, half_z)}
    out.update(words)
    return out


def area(mark_id, height, ring, bevel=0):
    return {"id": mark_id, "kind": "area", "h": height, "bevel": bevel, "ring": ring}


shapes = [rect("island", 0, 0, (EAST - WEST) / 2, (SOUTH - NORTH) / 2)]
# The keep-out `OB19` will enforce, painted on the ground under the monument so the box is a thing on the
# board rather than a number in a document. It is a patch: same floor and base_height as the island.
shapes.append(rect("keep-out", *MONUMENT, KEEP_OUT, KEEP_OUT, theme="flag"))
# The wool room: four walls standing on the ground with a gap in the west one for the way in. Drawn as
# thin raises rather than as one block, because a solid box is a plinth and a wool has to stand INSIDE
# something. Marked `keepClear`, which is what keeps the dressing pass off a wall drawn as terrain.
WX, WZ = WOOL_ROOM
for wall_id, cx, cz, half_x, half_z in (
        ("wool-n", WX, WZ - 9, 12, 1), ("wool-s", WX, WZ + 9, 12, 1),
        ("wool-e", WX + 11, WZ, 1, 9),
        ("wool-w-n", WX - 11, WZ - 6, 1, 4), ("wool-w-s", WX - 11, WZ + 6, 1, 4)):
    shapes.append(rect(wall_id, cx, cz, half_x, half_z, theme="room",
                       height_mode="raise", base_height=4, skirt=0, keepClear=True))

groups = [{"id": "land", "name": "land", "mirrors": False,
           "shapeIds": [shape["id"] for shape in shapes]}]
# A bank across the middle so the core has a face to sit in and the board is not a table.
relief = {"land": {"base": PLAIN, "reach": 0, "step": 1, "pushes": [], "marks": [
    area("plain", PLAIN, [[WEST + 4, NORTH + 4], [CORE[0] - 16, NORTH + 4],
                          [CORE[0] - 16, SOUTH - 4], [WEST + 4, SOUTH - 4]]),
    area("shelf", 22, [[CORE[0] + 4, NORTH + 4], [EAST - 4, NORTH + 4],
                       [EAST - 4, SOUTH - 4], [CORE[0] + 4, SOUTH - 4]])]}}

layout = {
    "setup": {"bbox": {"min_x": WEST - 10, "max_x": EAST + 10,
                       "min_z": NORTH - 10, "max_z": SOUTH + 10},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": {"moor": MOOR, "flag": FLAG, "room": ROOM},
    "mapTheme": "moor",
    "relief": relief,
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": shapes, "groups": groups}}],
}

here = os.path.dirname(os.path.abspath(__file__))
json.dump(layout, open(os.path.join(here, "objectives-and-clearances.layout.json"), "w"), indent=1)


def spawn(team, at, yaw):
    """A spawn states a point and the rectangle nothing else may stand in. `stamp` is omitted rather than
    stated null: a placement carrying `"stamp": null` is dropped and the whole PUT answers 200 with an
    empty body, having stored nothing."""
    return {"team": team, "yaw": yaw, "iron": [],
            "point": {"x": at[0], "y": GROUND[at] + 1, "z": at[1]},
            "protection": [{"minX": at[0] - PROTECT, "minZ": at[1] - PROTECT,
                            "maxX": at[0] + PROTECT, "maxZ": at[1] + PROTECT}]}


# The built ground under each station, read once off the world with `column` and written down: an anchor is
# an absolute point and the studio seats nothing for you. These are the TOP BLOCK, so a player stands one
# above them.
GROUND = {RED_SPAWN: 11, MONUMENT: 11, CORE: 19, WOOL_ROOM: 21, BLUE_SPAWN: 21, (0, 0): 11}


def ground(at):
    return GROUND[at]


def intent():
    """The intent. Every y is the top block under that station."""
    return {
        "teams": [{"id": "red", "name": "Red", "color": "red"},
                  {"id": "blue", "name": "Blue", "color": "blue"}],
        "maxPlayers": 12,
        "spawns": [spawn("red", RED_SPAWN, 90), spawn("blue", BLUE_SPAWN, 270)],
        "observer": {"point": {"x": 0, "y": ground((0, 0)) + 30, "z": 0}, "yaw": 0},
        "destroyables": [{"owner": "blue", "name": "Fold Monument", "style": "pillar-3",
                          "materials": "obsidian", "float": 4,
                          "anchor": {"x": MONUMENT[0], "y": ground(MONUMENT), "z": MONUMENT[1]}}],
        "cores": [{"owner": "red", "name": "Bank Core", "lava": 3, "lavaHeight": 3,
                   "openTop": False, "float": 6, "leak": 5, "digDepth": 0,
                   "anchor": {"x": CORE[0], "y": ground(CORE), "z": CORE[1]}}],
        "wools": [{"owner": "red", "color": "red",
                   "spawn": {"x": WOOL_ROOM[0], "y": ground(WOOL_ROOM) + 1, "z": WOOL_ROOM[1]},
                   "protection": [box_words(WOOL_ROOM, 12, 10)],
                   "entries": [{"minX": WOOL_ROOM[0] - 12, "minZ": WOOL_ROOM[1] - 2,
                                "maxX": WOOL_ROOM[0] - 12, "maxZ": WOOL_ROOM[1] + 2}],
                   "monuments": []}],
        "meta": {"name": "Objectives And Clearances", "created": "2026-09-19",
                 "authors": ["the technique cards"], "contributors": []},
    }


def box_words(at, half_x, half_z):
    return {"minX": at[0] - half_x, "minZ": at[1] - half_z,
            "maxX": at[0] + half_x, "maxZ": at[1] + half_z}


json.dump(intent(), open(os.path.join(here, "objectives-and-clearances.intent.json"), "w"), indent=1)

if __name__ == "__main__":
    print(f"layout -> {os.path.join(here, 'objectives-and-clearances.layout.json')}")
    print(f"intent -> {os.path.join(here, 'objectives-and-clearances.intent.json')}")
    print(f"  island {EAST - WEST} x {SOUTH - NORTH}, plain {PLAIN}, shelf 22")
    for label, at in (("red spawn", RED_SPAWN), ("monument", MONUMENT), ("core", CORE),
                      ("wool room", WOOL_ROOM), ("blue spawn", BLUE_SPAWN)):
        print(f"  {label:10s} at x{at[0]:5d} z{at[1]:4d}")
