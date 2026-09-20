"""Writes walls-and-iron.plan.json — a defence wall placed three ways, and a spawn's iron cube.

A wall and an iron cube are the two structures nothing generated ever asks for: `Composer` writes neither
list, so both exist only where an author states them on a PLAN. That makes this card a plan rather than a
layout, and deliberately a **non-symmetric** one — every station is authored once and stands on its own, so
nothing here is an orbit image of anything else.

What separates the three wall stations is not the wall. It is where it stands and what ground is beside it.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
CELL = 4                       # blocks a cell, so a 4-cell piece is 16 blocks across
SURFACE = 9
SPAWN_SIDE = 5                 # cells: 20 blocks, which is ST10's whole allowance for a protection region

# Cells: [x, z, width, depth]. Each station runs north to south — the room at the top, its approach under
# it, the board's own ground below that — so a wall placed on the approach's OUTER interface is the far
# edge of the middle piece.
PIECES = [
    # `line` — the wall where the approach meets the board, and no ground past its ends.
    ("line-room", "wool-room", [0, 0, 4, 4]),
    ("line-approach", "piece", [0, 4, 4, 4]),
    ("line-field", "piece", [0, 8, 4, 8]),
    # `shoulder` — the same wall, with ground pulled out past both of its ends.
    ("shoulder-room", "wool-room", [14, 0, 4, 4]),
    ("shoulder-approach", "piece", [14, 4, 4, 4]),
    ("shoulder-west", "piece", [10, 4, 4, 4]),
    ("shoulder-east", "piece", [18, 4, 4, 4]),
    ("shoulder-field", "piece", [10, 8, 12, 8]),
    # `sealed` — two walls in series on one approach, which is a room rather than a line.
    ("sealed-room", "wool-room", [32, 0, 4, 4]),
    ("sealed-inner", "piece", [32, 4, 4, 4]),
    ("sealed-middle", "piece", [32, 8, 4, 4]),
    ("sealed-outer", "piece", [32, 12, 4, 4]),
    # One spawn, with a yard in front of its door and two iron cube markers on it. One spawn because a
    # plan stating `symmetry: "none"` has one orbit image, and a team is an orbit image: a non-symmetric
    # plan compiles to a one-team board however many spawn markers it carries.
    ("spawn-red", "spawn", [46, 4, SPAWN_SIDE, SPAWN_SIDE]),
    ("spawn-red-yard", "piece", [46, 4 + SPAWN_SIDE, SPAWN_SIDE, 5]),
]

# A wall is authored as the pair of pieces whose shared interface it stands on. `PlanWall` carries those two
# ids and nothing else — no side, no length, no thickness — because the interface decides all three.
WALLS = [("line-field", "line-approach"),
         ("shoulder-field", "shoulder-approach"),
         ("sealed-outer", "sealed-middle"),
         ("sealed-middle", "sealed-inner")]

SPAN = SPAWN_SIDE * CELL       # 20 blocks square
# A building smaller than its piece, stated in blocks from the piece's minimum corner, so there is a yard
# left for a cube to stand in. `WX1`'s default shell is the piece inset one block, which leaves none.
FOOTPRINT = [4, 1, 12, 12]
# `at` is an [x, z] offset in BLOCKS from the piece's minimum corner, on a half-block lattice, and it is the
# cube's CENTRE. Red's stands in the yard, two clear of the shell; blue's is inside the building.
IRON = [("iron-yard", "spawn-red", [SPAN / 2, FOOTPRINT[1] + FOOTPRINT[3] + 2 + 1.5]),
        ("iron-inside", "spawn-red", [SPAN / 2, SPAN / 2])]

plan = {
    "plan": 2,
    "meta": {"name": "Walls And Iron", "authors": ["the technique cards"]},
    "globals": {"cell": CELL, "symmetry": "none", "maxPlayers": 10, "surface": SURFACE},
    "pieces": [{"id": name, "role": role, "rect": rect} for name, role, rect in PIECES],
    # One build zone along the board's southern edge, docking the three fields, so there is a frontline
    # to judge an approach from. It reaches no further than the ground it meets.
    "zones": [{"id": "mid", "rect": [0, 16, 36, 4], "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-red", "at": [SPAN / 2, SPAN / 2],
                    "facing": "back", "footprint": FOOTPRINT}],
        "wools": [{"id": "wool-line", "piece": "line-room", "at": [8, 8]},
                  {"id": "wool-shoulder", "piece": "shoulder-room", "at": [8, 8]},
                  {"id": "wool-sealed", "piece": "sealed-room", "at": [8, 8]}],
        "iron": [{"id": name, "piece": piece, "at": at} for name, piece, at in IRON],
        "destroyables": [],
        "cores": [],
    },
    "walls": [{"a": a, "b": b} for a, b in WALLS],
    "boxes": [
        {"id": "line", "kind": "wool", "rect": [0, 0, 4, 16],
         "members": ["line-room", "line-approach", "line-field"]},
        {"id": "shoulder", "kind": "wool", "rect": [10, 0, 12, 16],
         "members": ["shoulder-room", "shoulder-approach", "shoulder-west", "shoulder-east",
                     "shoulder-field"]},
        {"id": "sealed", "kind": "wool", "rect": [32, 0, 4, 16],
         "members": ["sealed-room", "sealed-inner", "sealed-middle", "sealed-outer"]},
        {"id": "spawn", "kind": "spawn", "rect": [46, 4, 5, 10],
         "members": ["spawn-red", "spawn-red-yard"]},
    ],
}

if __name__ == "__main__":
    json.dump(plan, open(os.path.join(HERE, "walls-and-iron.plan.json"), "w"), indent=1)
    print(f"{len(PIECES)} pieces, {len(WALLS)} walls, {len(IRON)} iron marker(s), symmetry none")
    for a, b in WALLS:
        print(f"  wall on the interface '{a}' — '{b}'")
    for name, piece, at in IRON:
        print(f"  {name:12s} on {piece} at {at} blocks from its minimum corner")
