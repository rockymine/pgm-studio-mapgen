"""Writes opus55-redcut's plan and finish.

The arrangement is composed board p8 rot_180 seed 32 (`composed-seed32.plan.json`, the composer's raw answer),
a nano board: a single hub, one wool whose approach curls round a hole in a U, a bar frontline and an open
crossing. Taken over: the wool room moved to the spawn's end of the U's spine, the spine walled across its
middle, the wool room and the spawn deepened with a building at the back of each, the spawn carries iron, and the whole team unit is stated at one surface so
the relief alone gives it its heights.
"""
import copy
import json
from pathlib import Path

HERE = Path(__file__).parent

composed = json.loads((HERE / "composed-seed32.plan.json").read_text())

BASE = 9

# Cell rects [x, z, w, h]. The wool room stands at the spawn's end of the U's spine, flush with its corner, so it
# is the nearer walk from the spawn. The spine is split at its middle and the wall stands on that seam, level
# with the middle of the hole: its east end faces the hole and its west end the void south of the room, so a
# player crosses it rather than rounding it. The wool room and the spawn are sixteen blocks deep along the way
# their doors face.
RECT = {
    "wool-a-t1": [-9, 9, 3, 5],
    "wool-a-room": [-13, 15, 4, 3],
    "spawn-room": [1, 20, 3, 4],
}
SPINE_NORTH = [{"id": "wool-a-spine", "role": "piece", "rect": [-9, 14, 3, 4]}]
BOXES = {"wool-a": [-13, 9, 10, 9], "spawn": [1, 19, 3, 5]}
WALLS = [{"a": "wool-a-t1", "b": "wool-a-spine"}]

# Each deepened room holds a building seven deep at its back and a yard nine deep in front of its door, with
# the marker inside the building. A footprint is [x, z, w, h] in blocks from the piece's minimum corner. The
# wool room opens east onto the U's spine and the spawn south onto the hub.
ROOMS = {
    "wool-a-room": {"footprint": [1, 1, 7, 10], "at": [4, 6]},
    "spawn-room": {"footprint": [1, 8, 10, 7], "at": [6, 11]},
}
IRON = [{"id": "iron-1", "piece": "spawn-room", "at": [9.5, 4.5]}]


def plan():
    doc = copy.deepcopy(composed)
    doc["meta"] = {"name": "Redcut"}
    doc["pieces"] += copy.deepcopy(SPINE_NORTH)
    for piece in doc["pieces"]:
        piece["rect"] = RECT.get(piece["id"], piece["rect"])
        piece["surface"] = BASE
    doc["walls"] = WALLS
    for marker in doc["placements"]["spawns"] + doc["placements"]["wools"]:
        marker.update(ROOMS.get(marker["piece"], {}))
    doc["placements"]["iron"] = copy.deepcopy(IRON)
    for box in doc.get("boxes", []):
        box["rect"] = BOXES.get(box["id"], box["rect"])
        if box["id"] == "wool-a":
            box["members"].append("wool-a-spine")
    return doc


# Block coordinates of red's half, which the symmetry turns onto blue's. The frontline's lip runs along z 16.
TEAM, HOLE = "frontline-t1-9", "void-1-cut"

# The team unit's outline as the compile answers it, and the points it is reshaped by: the flanks of the
# frontline and the hub pushed a few blocks out, the lip pushed out into the crossing at two points (never pulled
# in, which would leave void the build zone does not cover), and the U chamfered at its outer corner away from
# the room. The U's own edges and the rooms are not touched.
COMPILED_RING = [(-52, 60), (-36, 60), (-36, 36), (-12, 36), (-12, 16), (12, 16), (12, 36), (0, 36), (0, 64),
                 (20, 64), (20, 76), (16, 76), (16, 96), (4, 96), (4, 76), (-12, 76), (-12, 72), (-52, 72)]
RESHAPE = [
    ((-12, 36), (-12, 16), [(-15, 26)]),     # the frontline's west flank
    ((-12, 16), (12, 16), [(-4, 13), (5, 12)]),   # the lip
    ((12, 16), (12, 36), [(15, 27)]),        # the frontline's east flank
    ((12, 36), (0, 36), [(6, 39)]),          # the frontline's back edge, facing the bay behind it
    ((0, 36), (0, 64), [(3, 50)]),           # the hub's east side, facing the same bay
    ((0, 64), (20, 64), [(10, 61)]),         # the hub's back bar, facing the bay
    ((20, 64), (20, 76), [(23, 70)]),        # the back bar's east end
    ((4, 76), (-12, 76), [(-4, 79)]),        # the back bar's north edge
]
CHAMFER = 3
CHAMFERED = [(-36, 36)]


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


# The hole inside the U is an irregular hexagon rather than the compiled square, eating a block into each piece
# round it.
HOLE_OPS = [
    {"index": 0, "x": -23, "z": 50},
    {"index": 1, "x": -15, "z": 47},
    {"after": 1, "x": -11, "z": 53},
    {"index": 3, "x": -13, "z": 61},
    {"index": 4, "x": -21, "z": 60},
    {"after": 4, "x": -25, "z": 55},
]


def area(mark_id, h, x0, z0, x1, z1):
    return {"id": mark_id, "kind": "area", "h": h, "bevel": 0,
            "ring": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]}


def scarps(scarp_id, points, low, high):
    """A face along a drawn line, one mark per straight run: a single mark stands a one-block ridge of its high
    side past every corner pointing at its low side. Drawn west to east, so the high side is toward the spawn."""
    return [{"id": f"{scarp_id}-{i}", "kind": "scarp", "points": points[i:i + 2], "low": low, "high": high,
             "face": 1, "band": 2} for i in range(len(points) - 1)]


def face_z(points, x):
    for (x0, z0), (x1, z1) in zip(points, points[1:]):
        if x0 <= x <= x1:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
    raise ValueError(x)


def stair(stair_id, points, x, low, high):
    """A flight cut into a face at 45 degrees, a block of rise to every block of run, on cell centres."""
    z0 = round(face_z(points, x)) - 1
    return {"id": stair_id, "kind": "line", "r": 2, "points": [[x, z0 + 0.5], [x, z0 + high - low + 0.5]],
            "h": [low, high]}


# A mesa: the frontline climbs from the lip at 9 by two sheer steps, three blocks to a bench at 12 and five more
# to the butte the hub stands on at 17, each crossed by a stair: the bench's at the east, the butte's at the
# west where it arrives on the hub, so the climb turns along the bench.
# The butte leans up to the spawn yard at 19, and its west edge is held at 17 where the U's arms leave it. From
# there both arms fall into a box canyon at 13 along the U's spine, where the wall stands on level ground and the
# wool room opens.
LIP, BENCH, BUTTE, SPAWN_YARD, CANYON = 9, 12, 17, 19, 13
BENCH_FACE = [[-18, 25], [-6, 23], [4, 25], [16, 24]]
BUTTE_FACE = [[-18, 33], [-8, 31], [2, 34], [18, 32]]
RELIEF = [
    area("lip", LIP, -16, 8, 18, 20),
    *scarps("bench-face", BENCH_FACE, LIP, BENCH),
    *scarps("butte-face", BUTTE_FACE, BENCH, BUTTE),
    area("spawn-yard", SPAWN_YARD, 2, 78, 18, 98),
    area("hub-west", BUTTE, -14, 34, -8, 66),
    area("canyon", CANYON, -54, 34, -24, 74),
    stair("bench-stair", BENCH_FACE, 8, LIP, BENCH),
    stair("butte-stair", BUTTE_FACE, -4, BENCH, BUTTE),
]


def finish():
    return {
        "editShapes": {TEAM: reshape_ops(), HOLE: copy.deepcopy(HOLE_OPS)},
        "relief": {"team": {"base": BASE, "reach": 0, "step": 1, "marks": RELIEF}},
        "authors": ["Opus 5.5"],
        "created": "2026-09-23",
    }


if __name__ == "__main__":
    for name, doc in (("plan", plan()), ("finish", finish())):
        (HERE / f"{HERE.name}.{name}.json").write_text(json.dumps(doc, indent=1) + "\n")
