"""Writes destroy-goals.layout.json and .intent.json — every destroy goal the studio can build, in a row.

A destroyable is a **style** and a **material**, and both are authored words from a closed set the studio
publishes at `GET /api/objectives/vocabulary`. Choosing one is a decision about what a player sees and how
long it takes to break, and neither is recoverable from a plan view — so the board is a flat island with
one goal a station, the six styles along the north row and the four materials along the south, and a core
beside them for the one goal that has no material knob at all.

Nothing here is a playable map. It is eleven objectives on one board so the shapes can be compared.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from cards import SOLID, moor  # noqa: E402

WEST, EAST, NORTH, SOUTH = -210, 210, -60, 60
GROUND = 12                     # the island's base_height: the top block is y11
TOP = GROUND - 1
FLOAT = 4                       # the vocabulary's own default, held the same at every station

# `GET /api/objectives/vocabulary` answers both of these, and they are the whole authoring surface.
STYLES = ["pillar-1", "pillar-2", "pillar-3", "cube-3", "cube-4", "column-plus"]
MATERIALS = ["obsidian", "emerald block", "gold block", "ender stone"]

STYLE_ROW_Z, MATERIAL_ROW_Z = -28, 28
STYLE_X = [-100 + 40 * i for i in range(len(STYLES))]
MATERIAL_X = [-90 + 60 * i for i in range(len(MATERIALS))]
CORE_AT = (150, 0)
RED_SPAWN, BLUE_SPAWN = (-180, 0), (180, 0)
PROTECT = 10

MOOR = moor()
# A flat island and nothing else: every station stands on the same ground, so the only difference between
# two goals is the words that made them.
shapes = [{"id": "island", "type": "rectangle", "operation": "add", "floor": 0, "base_height": GROUND,
           "theme": "moor", "min_x": WEST, "max_x": EAST, "min_z": NORTH, "max_z": SOUTH}]

layout = {
    "setup": {"bbox": {"min_x": WEST - 10, "max_x": EAST + 10,
                       "min_z": NORTH - 10, "max_z": SOUTH + 10},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": {"moor": MOOR},
    "mapTheme": "moor",
    "relief": {},
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0, "layout": {
        "shapes": shapes,
        "groups": [{"id": "land", "name": "land", "mirrors": False, "shapeIds": ["island"]}]}}],
}


def station(name, style, materials, at):
    """One destroyable. `anchor.y` is the TOP BLOCK under it — the studio seats nothing for you — and the
    structure stands `float` above that."""
    return {"owner": "blue", "name": name, "style": style, "materials": materials, "float": FLOAT,
            "anchor": {"x": at[0], "y": TOP, "z": at[1]}}


def spawn(team, at, yaw):
    return {"team": team, "yaw": yaw, "iron": [],
            "point": {"x": at[0], "y": TOP + 1, "z": at[1]},
            "protection": [{"minX": at[0] - PROTECT, "minZ": at[1] - PROTECT,
                            "maxX": at[0] + PROTECT, "maxZ": at[1] + PROTECT}]}


intent = {
    "teams": [{"id": "red", "name": "Red", "color": "red"},
              {"id": "blue", "name": "Blue", "color": "blue"}],
    "maxPlayers": 12,
    "spawns": [spawn("red", RED_SPAWN, 90), spawn("blue", BLUE_SPAWN, 270)],
    "observer": {"point": {"x": 0, "y": TOP + 40, "z": 0}, "yaw": 0},
    "destroyables":
        [station(style, style, "obsidian", (x, STYLE_ROW_Z)) for style, x in zip(STYLES, STYLE_X)] +
        [station(material, "cube-4", material, (x, MATERIAL_ROW_Z))
         for material, x in zip(MATERIALS, MATERIAL_X)],
    # A core has no material field anywhere in the pipeline: casing, lava and leak are all it states.
    "cores": [{"owner": "red", "name": "core", "lava": 3, "lavaHeight": 3, "openTop": False,
               "float": 6, "leak": 5, "digDepth": 0,
               "anchor": {"x": CORE_AT[0], "y": TOP, "z": CORE_AT[1]}}],
    "wools": [],
    "meta": {"name": "Destroy Goals", "created": "2026-09-20",
             "authors": ["the technique cards"], "contributors": []},
}

if __name__ == "__main__":
    json.dump(layout, open(os.path.join(HERE, "destroy-goals.layout.json"), "w"), indent=1)
    json.dump(intent, open(os.path.join(HERE, "destroy-goals.intent.json"), "w"), indent=1)
    print(f"island {EAST - WEST} x {SOUTH - NORTH}, ground top y{TOP}, float {FLOAT}")
    for style, x in zip(STYLES, STYLE_X):
        print(f"  style     {style:12s} at ({x:4d}, {STYLE_ROW_Z})")
    for material, x in zip(MATERIALS, MATERIAL_X):
        print(f"  material  {material:12s} at ({x:4d}, {MATERIAL_ROW_Z})  cube-4")
    print(f"  core                      at {CORE_AT}")
