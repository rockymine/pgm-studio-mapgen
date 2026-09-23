"""Writes opus55-sedgefall's plan and finish.

The arrangement is composed board p8 rot_180 seed 24 (`composed-seed24.plan.json`, the composer's raw answer),
a nano board: a ring hub, two wools on straight arms — one behind the hub and one off its side — a stepped
frontline and one island in the crossing. Taken over: each wool's arm is walled behind a neck, the side wool's
room is carried sixteen blocks clear of the hub, the rooms and the spawn are deepened with a building at the
back of each, the spawn carries iron, the island stands sixteen blocks off each frontline and is neutral, and
the whole team unit is stated at one surface so the relief alone gives it its heights.
"""
import copy
import json
from pathlib import Path

HERE = Path(__file__).parent

composed = json.loads((HERE / "composed-seed24.plan.json").read_text())

BASE = 9

# Cell rects [x, z, w, h]. Both wool approaches line up with the middle of the hub's hole: the back one leaves the
# back bar straight behind it, and the side one is as deep as the hub's west side and meets it opposite the
# hole. Each leaves the hub through a neck a cell long, and its wall stands on the seam between the neck and the
# arm, where there is void past both of its ends. The side wool's arm is long enough that its room stands
# sixteen blocks clear of the hub, and the back wool's that its room stands sixteen behind its wall, which is
# also what balances the two rooms' walks from the spawn. The hub is a cell wider than composed to the east, and the spawn moves with
# it, so its hole is twelve blocks across rather than a gap a player jumps. The frontline's lip is centred on
# the board's axis, so the two teams' lips face each other squarely across the build zone. The rooms and the
# spawn are sixteen blocks deep along the way their doors face.
RECT = {
    "hub-t1": [-6, 17, 9, 3],
    "hub-t2": [-6, 10, 9, 3],
    "hub-t4": [0, 13, 3, 4],
    "spawn-t1": [3, 13, 2, 3],
    "frontline-t1": [-6, 7, 9, 3],
    "frontline-t2": [-3, 5, 6, 2],
    "wool-a-t1": [-3, 21, 3, 4],
    "wool-a-room": [-3, 25, 3, 4],
    "wool-b-t1": [-13, 13, 6, 4],
    "wool-b-room": [-13, 17, 3, 4],
    "spawn-room": [5, 13, 4, 3],
}
NECKS = [{"id": "wool-a-neck", "role": "piece", "rect": [-3, 20, 3, 1]},
         {"id": "wool-b-neck", "role": "piece", "rect": [-7, 13, 1, 4]}]
BOXES = {"hub": [-6, 10, 9, 10], "wool-a": [-3, 20, 3, 9], "wool-b": [-13, 13, 7, 8], "spawn": [3, 13, 6, 3],
         "frontline": [-6, 5, 9, 5]}
WALLS = [{"a": "wool-a-t1", "b": "wool-a-neck"}, {"a": "wool-b-t1", "b": "wool-b-neck"}]

# The island stands sixteen blocks off each frontline: the team units sit a cell further out than composed.
SHIFT = 1
GORGE = [-3, -5 - SHIFT, 6, 10 + 2 * SHIFT]

# Each deepened room holds a building seven deep at its back and a yard nine deep in front of its door, with
# the marker inside the building. A footprint is [x, z, w, h] in blocks from the piece's minimum corner. Both
# wool rooms open south onto their arms; the spawn opens west onto the hub, the way a player arriving faces.
ROOMS = {
    "wool-a-room": {"footprint": [1, 8, 10, 7], "at": [6, 11]},
    "wool-b-room": {"footprint": [1, 8, 10, 7], "at": [6, 11]},
    "spawn-room": {"footprint": [8, 1, 7, 10], "at": [11, 6], "facing": "left"},
}
IRON = [{"id": "iron-1", "piece": "spawn-room", "at": [4.5, 2.5]}]


def plan():
    doc = copy.deepcopy(composed)
    doc["meta"] = {"name": "Sedgefall"}
    doc["pieces"] += copy.deepcopy(NECKS)
    for piece in doc["pieces"]:
        x, z, w, h = RECT.get(piece["id"], piece["rect"])
        island = piece["id"] == "mid-stone-0"
        piece["rect"] = [x, z + (0 if island else SHIFT), w, h]
        piece["surface"] = BASE
        if island:
            piece["mirrors"] = False   # it lies across the centre and is its own image, so it is neutral ground
    doc["zones"] = [{"id": "mid-band", "rect": GORGE, "holes": []}]
    doc["walls"] = WALLS
    for marker in doc["placements"]["spawns"] + doc["placements"]["wools"]:
        marker.update(ROOMS.get(marker["piece"], {}))
    doc["placements"]["iron"] = copy.deepcopy(IRON)
    for box in doc.get("boxes", []):
        x, z, w, h = BOXES.get(box["id"], box["rect"])
        box["rect"] = [x, z + SHIFT, w, h]
        if box["id"] in ("wool-a", "wool-b"):
            box["members"].append(f"{box['id']}-neck")
    return doc


# Block coordinates of red's half, which the symmetry turns onto blue's. The frontline's lip runs along z 24.
TEAM, HOLE, ISLAND = "frontline-t1-9", "void-1-cut", "mid-stone-0-9"

# The team unit's outline as the compile answers it, and the points it is reshaped by: the flanks pushed a few
# blocks out, the lip pushed into the crossing at two points (never pulled in, which would leave void the build
# zone does not cover), and the side wool's arm chamfered at its outer corner, sixteen blocks from its room. The
# arms' own edges and the rooms are not touched.
COMPILED_RING = [(-52, 56), (-24, 56), (-24, 32), (-12, 32), (-12, 24), (12, 24), (12, 56), (36, 56), (36, 68),
                 (12, 68), (12, 84), (0, 84), (0, 120), (-12, 120), (-12, 84), (-24, 84), (-24, 72), (-40, 72),
                 (-40, 88), (-52, 88)]
RESHAPE = [
    ((-24, 56), (-24, 32), [(-27, 44)]),     # the frontline's and hub's west flank
    ((-12, 24), (12, 24), [(-5, 21), (4, 20)]),   # the lip
    ((12, 24), (12, 56), [(15, 40)]),        # the frontline's east flank
    ((12, 68), (12, 84), [(15, 76)]),        # the hub's east back flank
]
CHAMFER = 3
CHAMFERED = [(-52, 56)]


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


# The hub's hole is an irregular hexagon, a mere rather than a square, eating a block into each piece round it.
HOLE_POINTS = [(-11, 58), (-3, 55), (1, 62), (-1, 71), (-8, 73), (-13, 66)]
HOLE_OPS = [
    {"index": 0, "x": -11, "z": 58},
    {"index": 1, "x": -3, "z": 55},
    {"after": 1, "x": 1, "z": 62},
    {"index": 3, "x": -1, "z": 71},
    {"index": 4, "x": -8, "z": 73},
    {"after": 4, "x": -13, "z": 66},
]

# The island loses its square corners; it lies across the centre and is not fanned, so its ring is written
# whole and is its own image under the half-turn.
ISLAND_OPS = [
    {"index": 0, "x": -7, "z": -8}, {"after": 0, "x": 2, "z": -9}, {"index": 2, "x": 8, "z": -5},
    {"index": 3, "x": 7, "z": 8}, {"after": 3, "x": -2, "z": 9}, {"index": 5, "x": -8, "z": 5},
]


def area(mark_id, h, x0, z0, x1, z1):
    return {"id": mark_id, "kind": "area", "h": h, "bevel": 0,
            "ring": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]}


def push(push_id, ring, amount, falloff):
    return {"id": push_id, "ring": [list(point) for point in ring], "amount": amount, "falloff": falloff,
            "crown": 0, "roughness": 0, "seed": 1}


def proud(points, margin):
    """A ring traced on `points`, pushed `margin` blocks out from their centre at every point."""
    cx = sum(x for x, _ in points) / len(points)
    cz = sum(z for _, z in points) / len(points)
    ring = []
    for x, z in points:
        length = ((x - cx) ** 2 + (z - cz) ** 2) ** 0.5
        ring.append((round(x + margin * (x - cx) / length, 1), round(z + margin * (z - cz) / length, 1)))
    return ring


# A fen: the frontline lies low, leaning from 9 at the lip to 10 at the foot of a bank that curves across it
# and rises three blocks over three to a turf knoll at 13, walked anywhere along it. The bank is one mark per
# straight run, so no corner stands a ridge past it, and the lip is held up to an inner edge that follows the
# bank's curve twelve blocks short of it, so the fen's contours curve with the bank rather than lying straight.
# One reed pool, soft-edged and off the line from the lip to the hub, sinks two blocks into the fen. Both walls
# stand on level ground at 13; past them the arms fall to the reed-bed yards round the rooms at 11. The spawn
# yard is held at 14, and the hub dips two blocks toward its mere.
FEN, FOOT, BANK_TOP, REED_BED, SPAWN_YARD = 9, 10, 13, 11, 14
BANK = [[-30, 42], [-20, 45], [-10, 42], [0, 46], [8, 43], [16, 46]]
LIP_REACH = 12
LIP_RING = [[-30, 16], [18, 16], [18, BANK[-1][1] - LIP_REACH],
            *[[x, z - LIP_REACH] for x, z in reversed(BANK)], [-30, BANK[0][1] - LIP_REACH]]
RELIEF = [
    {"id": "fen", "kind": "area", "h": FEN, "bevel": 0, "ring": LIP_RING},
    *[{"id": f"bank-{i}", "kind": "scarp", "points": BANK[i:i + 2], "low": FOOT, "high": BANK_TOP, "face": 3,
       "band": 2} for i in range(len(BANK) - 1)],
    area("spawn-yard", SPAWN_YARD, 18, 54, 38, 70),
    area("back-wall", BANK_TOP, -14, 82, 2, 94),
    area("side-wall", BANK_TOP, -34, 54, -22, 74),
    area("back-reeds", REED_BED, -14, 102, 2, 122),
    area("side-reeds", REED_BED, -54, 70, -38, 90),
]
PUSHES = [
    # a reed pool in the fen west of the line from the lip to the hub, its outline drawn rather than square
    push("reed-pool", [(-21, 29), (-15, 26), (-9, 28), (-8, 33), (-13, 36), (-20, 35)], -2, 4),
    # the hub dips two blocks toward its mere
    push("mere-lip", proud(HOLE_POINTS, 2), -2, 4),
]

# The island is level at 9 along its two gorge-facing edges and rises a block to 10 across its middle. A
# half-turn solves the neutral group's z < 0 half and copies it, so the marks stand there.
ISLAND_RELIEF = [area("island-edge", FEN, -10, -11, 10, -5), area("island-crest", 10, -10, -3, 10, 0)]


def finish():
    return {
        "editShapes": {TEAM: reshape_ops(), HOLE: copy.deepcopy(HOLE_OPS), ISLAND: copy.deepcopy(ISLAND_OPS)},
        "relief": {"team": {"base": FEN, "reach": 0, "step": 1, "marks": RELIEF, "pushes": PUSHES},
                   "neutral": {"base": FEN, "reach": 0, "step": 1, "marks": ISLAND_RELIEF}},
        "authors": ["Opus 5.5"],
        "created": "2026-09-23",
    }


if __name__ == "__main__":
    for name, doc in (("plan", plan()), ("finish", finish())):
        (HERE / f"{HERE.name}.{name}.json").write_text(json.dumps(doc, indent=1) + "\n")
