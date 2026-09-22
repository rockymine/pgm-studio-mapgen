"""Writes opus55-millbank's plan and finish.

The arrangement is composed board p20 rot_180 seed 5 (`composed-seed5.plan.json`, the composer's raw answer),
taken over: each wool approach leaves the hub through a neck and carries a bedrock wall behind it, the two
rooms are balanced against the spawn, a neutral holm is set in the
gorge, and the whole team unit is stated at one surface so the relief alone gives it its heights.
"""
import copy
import json
from pathlib import Path

HERE = Path(__file__).parent

composed = json.loads((HERE / "composed-seed5.plan.json").read_text())

BASE = 9

# Each wool arm leaves the hub through a neck one cell long and as deep as the arm, and the bedrock wall
# stands on the seam between the neck and the arm rather than at the hub's side: there the hub runs on past
# both ends of the wall, and a player rounds it off the corner. Behind the neck the wall has void at both ends.
# Each room stands sixteen blocks behind its wall; wool-a's room stands twenty clear of hub-t1, and wool-b's
# neck is a cell longer than wool-a's so the two rooms are about the same walk from their own spawn.
RECT = {
    "wool-a-t1": [-12, 14, 7, 4],
    "wool-a-room": [-12, 18, 3, 2],
    "wool-b-t1": [10, 14, 4, 4],
    "wool-b-room": [14, 15, 2, 3],
}
NECKS = [{"id": "wool-a-neck", "role": "piece", "rect": [-5, 14, 1, 4]},
         {"id": "wool-b-neck", "role": "piece", "rect": [8, 14, 2, 4]}]
BOXES = {"wool-a": [-12, 14, 8, 6], "wool-b": [8, 14, 8, 4]}

# The holm in the gorge is as wide as the build zone and 32 blocks deep. A hop onto it must be ten blocks or
# more, so the team units stand three cells further out than composed, the gorge is fourteen cells deep and
# each hop is twelve blocks.
SHIFT = 3
HOLM = {"id": "mill-holm", "role": "piece", "rect": [-4, -4, 8, 8], "mirrors": False}
GORGE = [-4, -4 - SHIFT, 8, 8 + 2 * SHIFT]

# One wall per approach, on the seam between the neck and the arm, sixteen blocks in front of the room.
WALLS = [{"a": "wool-a-t1", "b": "wool-a-neck"}, {"a": "wool-b-t1", "b": "wool-b-neck"}]


def plan():
    doc = copy.deepcopy(composed)
    doc["meta"] = {"name": "Millbank"}
    doc["pieces"] += copy.deepcopy(NECKS)
    for piece in doc["pieces"]:
        x, z, w, h = RECT.get(piece["id"], piece["rect"])
        piece["rect"] = [x, z + SHIFT, w, h]
        piece["surface"] = BASE
    doc["pieces"].append(dict(HOLM, surface=BASE))
    doc["zones"] = [{"id": "mid-band", "rect": GORGE, "holes": []}]
    doc["walls"] = WALLS
    for box in doc.get("boxes", []):
        x, z, w, h = BOXES.get(box["id"], box["rect"])
        box["rect"] = [x, z + SHIFT, w, h]
    return doc


# Block coordinates of red's half, which the symmetry turns onto blue's. They are stated as they stand with the
# gorge lip at z 20, and `onto_board` moves them out by TEAM_DZ to where the shift puts the lip.
TEAM = "frontline-t1-9"
TEAM_DZ = 4 * (SHIFT - 1)

# The team unit's outline as the compile answers it, and the few points it is reshaped by. The flanks of the
# hub and the meadow are pushed a few blocks out and the hub's west back flank pulled in, which keeps the bay
# beside wool-a's room wide. The wool approaches are only chamfered at their outer corners, never bulged, and the
# lip is not touched: it is where the build zone attaches, and pulling it in would leave void the zone does not
# cover.
COMPILED_RING = [(-48, 60), (-16, 60), (-16, 20), (16, 20), (16, 28), (32, 28), (32, 60), (56, 60), (56, 64),
                 (64, 64), (64, 76), (32, 76), (32, 92), (24, 92), (24, 108), (8, 108), (8, 92), (-16, 92),
                 (-16, 76), (-36, 76), (-36, 84), (-48, 84)]
RESHAPE = [
    ((-16, 60), (-16, 20), [(-19, 50), (-20, 36), (-18, 26)]),  # west flank of the hub and the meadow
    ((16, 28), (32, 28), [(25, 25)]),                            # the meadow's east shoulder
    ((32, 28), (32, 60), [(35, 36), (36, 48)]),                  # east flank
    ((8, 92), (-16, 92), [(-4, 95)]),                            # hub's back edge beside the spawn
    ((-16, 92), (-16, 76), [(-13, 84)]),                         # hub's west back flank, pulled in
]
CHAMFER = 3
CHAMFERED = [(-48, 60), (56, 60)]   # the outer corner of each wool approach on the gorge side


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
    return {TEAM: ops}


def area(mark_id, h, x0, z0, x1, z1, bevel=0):
    return {"id": mark_id, "kind": "area", "h": h, "bevel": bevel,
            "ring": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]}


def orchards(h):
    """Both wool approaches held at one height across their necks and a strip of the hub, so each bedrock wall
    stands on level ground its whole run."""
    return [area("orchard-west", h, -52, 58, -12, 86), area("orchard-east", h, 28, 58, 68, 78)]


# The ground leans from the gorge to the spawn and breaks once, at a curved scarp seven blocks tall between the
# meadow and the hamlet. The lip is pinned at 9 and the scarp's foot at 12, and the meadow between them is
# solved into a gentle lean; above the face the hamlet leans on up to the approaches at 20 and the spawn yard at
# 23. The scarp is drawn west to east, so its high side is the one toward red's spawn.
LIP, FOOT, HEAD, APPROACHES, SPAWN_YARD = 9, 12, 19, 20, 23
FACE = [[-22, 44], [-8, 40], [4, 43], [14, 49], [24, 46], [38, 41]]


def face_z(x):
    """Where the scarp's line crosses x."""
    for (x0, z0), (x1, z1) in zip(FACE, FACE[1:]):
        if x0 <= x <= x1:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
    raise ValueError(x)


def stair(stair_id, x, r=2):
    """A flight cut into the face at 45 degrees: a block of rise to every block of run, from the scarp's foot on
    the meadow side to its head on the hamlet side. Its points sit on cell centres, so each cell takes one whole
    height, and it runs the face's own rise rather than out into the meadow."""
    rise = HEAD - FOOT
    z0 = round(face_z(x)) - 1
    return {"id": stair_id, "kind": "line", "r": r,
            "points": [[x, z0 + 0.5], [x, z0 + rise + 0.5]], "h": [FOOT, HEAD]}


RELIEF = [
    area("lip", LIP, -20, 18, 36, 24),
    {"id": "hamlet-face", "kind": "scarp", "points": FACE, "low": FOOT, "high": HEAD, "face": 2, "band": 4},
    *orchards(APPROACHES),
    area("spawn-yard", SPAWN_YARD, 6, 94, 26, 110),
    stair("stair-west", -12),
    stair("stair-east", 28),
]


# The holm is the river's island, and the river has cut a bed through its middle along the gorge. The bed
# floor is held at 7 across the whole holm and past both of its ends; a curved scarp stands four blocks sheer
# from it to a bank top held flat at 11 out to the gorge edge, a low knoll swells on the bank, and a stair is
# cut into the bank at 45 degrees, so the holm can be crossed on foot. Every one of these stands on the
# holm's north half (z < 0): a half-turn solves that half and copies it onto the south, so the south bank, its
# knoll and its stair are the north's images, and the river's width wanders as the two curves pass each other.
BED, BANK = 7, 11
BANK_LINE = [[24, -5], [22, -5], [10, -3], [-2, -4], [-12, -6], [-22, -4], [-24, -4]]   # traced east to west,
HOLM_RELIEF = [                                                                           # so its high side is north
    area("river-bed", BED, -24, -3, 24, 3),
    {"id": "bank", "kind": "scarp", "points": BANK_LINE, "low": BED, "high": BANK, "face": 1, "band": 6},
    {"id": "bank-stair", "kind": "line", "r": 2, "points": [[6, -2.5], [6, -6.5]], "h": [BED, BANK]},
]
HOLM_PUSHES = [{"id": "bank-knoll", "ring": [[-14, -12], [-4, -12], [-4, -8], [-14, -8]], "amount": 2,
                "falloff": 8, "crown": 0, "roughness": 0, "seed": 1}]

# The river fills its bed a block deep. Its ring runs half a block into each bank, so it reaches the foot of each cut,
# and runs past both ends of the holm so it meets the gorge rather than stopping in a basin.
NORTH_SHORE = [[x, z - 0.5] for x, z in reversed(BANK_LINE)]
RIVER = {"id": "river", "kind": "water", "shape": "pool", "form": "natural", "layer": "ground",
         "points": NORTH_SHORE + [[-x, -z] for x, z in NORTH_SHORE], "radius": 1, "depth": 1,
         "level": BED + 1, "shore": 0}


def onto_board(marks, ops):
    """Red's half stated with the lip at z 20, moved out to the board's own lip."""
    for mark in marks:
        for key in ("ring", "points"):
            if key in mark:
                mark[key] = [[x, z + TEAM_DZ] for x, z in mark[key]]
    for op in ops:
        if "z" in op:
            op["z"] += TEAM_DZ
    return marks, ops


def finish():
    marks, ops = onto_board(copy.deepcopy(RELIEF), reshape_ops()[TEAM])
    return {
        "editShapes": {TEAM: ops},
        "relief": {"team": {"base": BASE, "reach": 0, "step": 1, "marks": marks},
                   "neutral": {"base": BANK, "reach": 0, "step": 1, "marks": HOLM_RELIEF,
                               "pushes": HOLM_PUSHES}},
        "dressing": {"props": [RIVER]},
        "authors": ["Opus 5.5"],
        "created": "2026-09-22",
    }


if __name__ == "__main__":
    for name, doc in (("plan", plan()), ("finish", finish())):
        (HERE / f"{HERE.name}.{name}.json").write_text(json.dumps(doc, indent=1) + "\n")
