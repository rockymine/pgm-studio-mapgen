"""Writes opus55-lymedown's plan and finish.

The arrangement is composed board p8 rot_180 seed 8 (`composed-seed8.plan.json`, the composer's raw answer),
a nano board: a g-shaped hub with two holes, one wool on an L at its back, no frontline and a wide build band
with one island in it. Taken over: the wool box is centred on the hub's hole and turned to face the spawn, walled
behind a neck, the build band narrowed to the span between the spawn's leg and the hole, the wool room and the
spawn deepened with a building at the back of each, the spawn carries iron, the island stands sixteen blocks off
each hub, and the whole team unit is stated at one surface so the relief alone gives it its heights.
"""
import copy
import json
from pathlib import Path

HERE = Path(__file__).parent

composed = json.loads((HERE / "composed-seed8.plan.json").read_text())

BASE = 9

# Cell rects [x, z, w, h]. The wool box leaves the hub's back bar with its neck centred on the hole below it, and
# turns west, so its room stands at the west end of the L with its door facing east: from the spawn a player
# sees the room's yard and door rather than its back wall. The wall stands on the seam between the neck and the
# arm, where there is void past both of its ends. The arm is long enough that the room stands sixteen blocks
# clear of the back bar. The wool room and the spawn are sixteen blocks deep along the way their doors face.
RECT = {
    "wool-a-t1": [-5, 15, 3, 3],
    "wool-a-t2": [-6, 18, 4, 3],
    "wool-a-room": [-10, 18, 4, 3],
    "spawn-room": [8, 10, 4, 3],
}
NECKS = [{"id": "wool-a-neck", "role": "piece", "rect": [-5, 14, 3, 1]}]
BOXES = {"wool-a": [-10, 14, 8, 7], "spawn": [7, 10, 5, 3]}
WALLS = [{"a": "wool-a-t1", "b": "wool-a-neck"}]

# The island stands sixteen blocks off each hub's front: the team units sit a cell further out than composed.
# The build band runs only from the outer edge of the hub's leg out of the spawn to the far end of the hole,
# not the whole width of the G, so a team leaving its spawn has to choose a side of the hole rather than run
# straight across. The team units sit a cell further west than composed, which centres that span on the
# board's axis, so the two sides face each other squarely across a band twelve cells wide.
SHIFT = 1
SHIFT_X = -1
GORGE = [-6, -5 - SHIFT, 12, 10 + 2 * SHIFT]

# Each deepened room holds a building seven deep at its back and a yard nine deep in front of its door, with
# the marker inside the building. A footprint is [x, z, w, h] in blocks from the piece's minimum corner. The wool
# room opens east onto its arm and the spawn west onto the hub, the way a player arriving there faces.
ROOMS = {
    "wool-a-room": {"footprint": [1, 1, 7, 10], "at": [4, 6]},
    "spawn-room": {"footprint": [8, 1, 7, 10], "at": [11, 6], "facing": "left"},
}
IRON = [{"id": "iron-1", "piece": "spawn-room", "at": [4.5, 2.5]}]


def plan():
    doc = copy.deepcopy(composed)
    doc["meta"] = {"name": "Lymedown"}
    doc["pieces"] += copy.deepcopy(NECKS)
    for piece in doc["pieces"]:
        x, z, w, h = RECT.get(piece["id"], piece["rect"])
        team = piece["id"] != "mid-stone-0"
        piece["rect"] = [x + (SHIFT_X if team else 0), z + (SHIFT if team else 0), w, h]
        piece["surface"] = BASE
        if piece["id"] == "mid-stone-0":
            piece["mirrors"] = False   # it lies across the centre and is its own image, so it is neutral ground
    doc["zones"] = [{"id": "mid-band", "rect": GORGE, "holes": []}]
    doc["walls"] = WALLS
    for marker in doc["placements"]["spawns"] + doc["placements"]["wools"]:
        marker.update(ROOMS.get(marker["piece"], {}))
    doc["placements"]["iron"] = copy.deepcopy(IRON)
    for box in doc.get("boxes", []):
        x, z, w, h = BOXES.get(box["id"], box["rect"])
        box["rect"] = [x + SHIFT_X, z + SHIFT, w, h]
        if box["id"] == "wool-a":
            box["members"].append("wool-a-neck")
    return doc


# Block coordinates of red's half, which the symmetry turns onto blue's. The hub's front runs along z 24.
TEAM, HOLE, ISLAND = "hub-t1-9", "void-1-cut", "mid-stone-0-9"

# The team unit's outline as the compile answers it, and the points it is reshaped by: the flanks and the back
# bar pushed a few blocks out, the front pushed into the build band at two points (never pulled in, which would
# leave void the zone does not cover), and the wool L's east corner chamfered, sixteen blocks from its room.
COMPILED_RING = [(-44, 76), (-24, 76), (-24, 60), (-36, 60), (-36, 24), (0, 24), (0, 48), (12, 48), (12, 24),
                 (24, 24), (24, 44), (44, 44), (44, 56), (24, 56), (24, 60), (-12, 60), (-12, 88), (-44, 88)]
RESHAPE = [
    ((-36, 24), (0, 24), [(-22, 21), (-10, 20)]),  # the front, pushed into the build band
    ((24, 24), (24, 44), [(27, 34)]),              # the east flank
    ((24, 60), (-12, 60), [(6, 63)]),              # the back bar's north edge
    ((-36, 60), (-36, 24), [(-39, 42)]),           # the west flank
]
CHAMFER = 3
CHAMFERED = [(-12, 88)]


def toward(corner, other, run):
    (cx, cz), (ox, oz) = corner, other
    length = max(abs(ox - cx), abs(oz - cz))
    return (cx + (ox - cx) * run // length, cz + (oz - cz) * run // length)


def reshape_ops():
    ring, ops = list(COMPILED_RING), []
    for a, b, points in RESHAPE:
        at = next(i for i in range(len(ring)) if ring[i] == a and ring[(i + 1) % len(ring)] == b)
        for point in points:
            ops.append({"after": at, "x": point[0], "z": point[1]})
            ring.insert(at + 1, point)
            at += 1
    for corner in CHAMFERED:
        at = ring.index(corner)
        before, after = ring[at - 1], ring[(at + 1) % len(ring)]
        moved, inserted = toward(corner, after, CHAMFER), toward(corner, before, CHAMFER)
        ops.append({"index": at, "x": moved[0], "z": moved[1]})
        ring[at] = moved
        ops.append({"after": (at - 1) % len(ring), "x": inserted[0], "z": inserted[1]})
        ring.insert(at, inserted)
    return ops


# The hub's hole is a rounded, irregular hexagon rather than the compiled square — a dene in the down.
HOLE_POINTS = [(-23, 38), (-16, 35), (-11, 40), (-12, 47), (-19, 49), (-25, 44)]
HOLE_OPS = [
    {"index": 0, "x": -23, "z": 38},
    {"index": 1, "x": -16, "z": 35},
    {"after": 1, "x": -11, "z": 40},
    {"index": 3, "x": -12, "z": 47},
    {"index": 4, "x": -19, "z": 49},
    {"after": 4, "x": -25, "z": 44},
]

# The island loses its square corners; it lies across the centre and is not fanned, so its ring is written
# whole and is its own image under the half-turn.
ISLAND_OPS = [
    {"index": 0, "x": -10, "z": -8}, {"after": 0, "x": 2, "z": -9}, {"index": 2, "x": 12, "z": -6},
    {"index": 3, "x": 10, "z": 8}, {"after": 3, "x": -2, "z": 9}, {"index": 5, "x": -12, "z": 6},
]


def area(mark_id, h, x0, z0, x1, z1):
    return {"id": mark_id, "kind": "area", "h": h, "bevel": 0,
            "ring": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]}


def push(push_id, ring, amount, falloff, crown=0):
    return {"id": push_id, "ring": [list(point) for point in ring], "amount": amount, "falloff": falloff,
            "crown": crown, "roughness": 0, "seed": 1}


def proud(points, margin):
    """A ring traced on `points`, pushed `margin` blocks out from their centre at every point."""
    cx = sum(x for x, _ in points) / len(points)
    cz = sum(z for _, z in points) / len(points)
    ring = []
    for x, z in points:
        length = ((x - cx) ** 2 + (z - cz) ** 2) ** 0.5
        ring.append((round(x + margin * (x - cx) / length, 1), round(z + margin * (z - cz) / length, 1)))
    return ring


# Chalk downs: nothing is sheer. The hub leans from its front at the build band, held at 9, up to its back bar at
# 13, and a rounded down swells on its west coast. The wool's neck and the first blocks of its arm are held at 13
# for the wall; past it the arm climbs onto a second rounded down at the L's corner, whose shoulder falls west
# to the room. Each down's skirt climbs at about the rate its crown does, so neither steps at its own outline. The spawn
# yard is held at 14. The hub dips two blocks toward its hole, which reads as a dene in the down.
FRONT, BACK, SPAWN_YARD = 9, 13, 14
RELIEF = [
    area("front-edge", FRONT, -40, 18, 28, 27),
    area("back-bar", BACK, -34, 56, 22, 62),
    area("wall", BACK, -26, 58, -10, 70),
    area("spawn-yard", SPAWN_YARD, 26, 42, 46, 58),
]
PUSHES = [
    push("west-down", [(-44, 34), (-32, 32), (-30, 42), (-34, 50), (-44, 50)], 3, 12, crown=2),
    push("wool-down", [(-20, 82), (-10, 80), (-6, 86), (-10, 94), (-20, 94)], 3, 10, crown=2),
    push("dene-lip", proud(HOLE_POINTS, 2), -2, 5),
]

# The island is level at 10 along its two gorge-facing edges and rises a single block to 11 across its middle,
# so most of it is ground to stand on. A half-turn solves the neutral group's z < 0 half and copies it, so the
# marks stand there.
ISLAND_RELIEF = [area("island-edge", 10, -14, -11, 14, -6), area("island-crest", 11, -14, -4, 14, 0)]


def finish():
    return {
        "editShapes": {TEAM: reshape_ops(), HOLE: copy.deepcopy(HOLE_OPS), ISLAND: copy.deepcopy(ISLAND_OPS)},
        "relief": {"team": {"base": FRONT, "reach": 0, "step": 1, "marks": RELIEF, "pushes": PUSHES},
                   "neutral": {"base": FRONT, "reach": 0, "step": 1, "marks": ISLAND_RELIEF}},
        "authors": ["Opus 5.5"],
        "created": "2026-09-23",
    }


if __name__ == "__main__":
    for name, doc in (("plan", plan()), ("finish", finish())):
        (HERE / f"{HERE.name}.{name}.json").write_text(json.dumps(doc, indent=1) + "\n")
