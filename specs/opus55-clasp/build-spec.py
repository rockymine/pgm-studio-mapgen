"""Writes opus55-clasp's plan and finish.

The arrangement is composed board p20 rot_180 seed 4 (`composed-seed4.plan.json`, the composer's raw answer),
taken over: the hub is widened two cells toward the clamp so its hole is three cells by four, the clamp wool
moves with it unchanged, the spawn is brought level with the hub's middle piece, the spawn and the back wool
room are deepened, and each wool approach carries one bedrock wall behind a neck.
"""
import copy
import json
from pathlib import Path

HERE = Path(__file__).parent

composed = json.loads((HERE / "composed-seed4.plan.json").read_text())

BASE = 9

# Cell rects [x, z, w, h]. The hub's front and back bars reach two cells further east and its east side moves
# with them, so the hole between the two sides is three cells by four. The clamp keeps its shape with arms a cell
# longer, so its room stands sixteen blocks off the hub's side, the least a gap beside a goal may be; its front
# arm is split two cells from the hub so the wall on it has void past both ends, where a wall at the hub's own
# side is rounded off the bars that run on past it. The back wool leaves the hub through a neck two cells long,
# and its room stands sixteen blocks behind that neck's wall. That depth is what balances the two wools: a cell
# shorter and the clamp is the further walk from the spawn (WL9); the clamp a cell nearer the hub and the back
# wool is the further walk from the front (WL10). The spawn stands level with the hub's middle piece rather than
# its front bar.
RECT = {
    "hub-t1": [-4, 20, 11, 4],
    "hub-t2": [-4, 12, 11, 4],
    "hub-t4": [3, 16, 4, 4],
    "wool-b-t1": [7, 20, 6, 3],
    "wool-b-t2": [9, 14, 4, 3],
    "wool-b-room": [11, 17, 2, 3],
    "wool-a-t1": [-2, 26, 3, 4],
    "wool-a-room": [-2, 30, 3, 4],
    "spawn-t1": [-5, 16, 1, 4],
    "spawn-room": [-9, 16, 4, 4],
}
NECKS = [{"id": "wool-b-neck", "role": "piece", "rect": [7, 14, 2, 3]},
         {"id": "wool-a-neck", "role": "piece", "rect": [-2, 24, 3, 2]}]
BOXES = {"hub": [-4, 12, 11, 12], "spawn": [-9, 16, 5, 4], "wool-a": [-2, 24, 3, 10], "wool-b": [7, 14, 6, 9]}

# The middle is two parallel neutral islands on the build zone's two side edges, each eight blocks wide and
# twenty-four deep, with sixteen blocks of channel between them. The team units stand a cell further out than
# composed, so the void from each frontline to the islands is sixteen blocks.
SHIFT = 1
ISLANDS = [{"id": "mid-west", "role": "piece", "rect": [-4, -3, 2, 6], "mirrors": False},
           {"id": "mid-east", "role": "piece", "rect": [2, -3, 2, 6], "mirrors": False}]
GORGE = [-4, -6 - SHIFT, 8, 12 + 2 * SHIFT]

# The clamp is walled at its front arm only; the back wool is walled across its arm.
WALLS = [{"a": "wool-b-t2", "b": "wool-b-neck"}, {"a": "wool-a-t1", "b": "wool-a-neck"}]

# The two rooms that were deepened hold a building seven deep at the back, with a yard nine deep in front of the
# door and the marker inside the building. A footprint is [x, z, w, h] in blocks from the piece's minimum
# corner. The back wool's room opens south onto its arm and the spawn's east onto the hub, which is the way
# a player arriving there faces. The clamp's room
# keeps the studio's default.
ROOMS = {
    "wool-a-room": {"footprint": [1, 8, 10, 7], "at": [6, 11]},
    "spawn-room": {"footprint": [1, 1, 7, 14], "at": [4, 8], "facing": "right"},
}

# The spawn's iron stands in its yard, where the studio's room read seats a cube clear of the building. Inside a
# spawn piece it renews itself.
IRON = [{"id": "iron-1", "piece": "spawn-room", "at": [11.5, 11.5]}]


def plan():
    doc = copy.deepcopy(composed)
    doc["meta"] = {"name": "Clasp"}
    doc["pieces"] = [piece for piece in doc["pieces"] if piece["id"] != "mid-stone-0"] + copy.deepcopy(NECKS)
    for piece in doc["pieces"]:
        x, z, w, h = RECT.get(piece["id"], piece["rect"])
        piece["rect"] = [x, z + SHIFT, w, h]
        piece["surface"] = BASE
    doc["pieces"] += [dict(island, surface=BASE) for island in ISLANDS]
    doc["zones"] = [{"id": "mid-band", "rect": GORGE, "holes": []}]
    doc["walls"] = WALLS
    for marker in doc["placements"]["spawns"] + doc["placements"]["wools"]:
        marker.update(ROOMS.get(marker["piece"], {}))
    doc["placements"]["iron"] = copy.deepcopy(IRON)
    for box in doc.get("boxes", []):
        x, z, w, h = BOXES.get(box["id"], box["rect"])
        box["rect"] = [x, z + SHIFT, w, h]
        if box["id"] == "wool-a":
            box["members"] = ["wool-a-neck", "wool-a-t1", "wool-a-room"]
        if box["id"] == "wool-b":
            box["members"] = ["wool-b-neck", "wool-b-t1", "wool-b-t2", "wool-b-room"]
    return doc


# Block coordinates of red's half, which the symmetry turns onto blue's. The frontline's lip runs along z 28.
TEAM, HOLE = "frontline-t1-9", "void-1-cut"

# The team unit's outline as the compile answers it, and the points it is reshaped by: the flanks of the
# frontline and the hub pushed a few blocks out, the lip pushed out into the build zone at two points (never
# pulled in, which would leave void the zone does not cover), and the clamp's two outer corners chamfered. The
# rooms and the approaches are not touched.
COMPILED_RING = [(-36, 68), (-16, 68), (-16, 28), (16, 28), (16, 52), (28, 52), (28, 60), (52, 60), (52, 96),
                 (28, 96), (28, 100), (4, 100), (4, 140), (-8, 140), (-8, 100), (-16, 100), (-16, 84), (-36, 84)]
RESHAPE = [
    ((-16, 28), (16, 28), [(-6, 24), (7, 23)]),                  # the lip, pushed out into the build zone
    ((-16, 68), (-16, 28), [(-19, 58), (-20, 42), (-18, 33)]),   # west flank of the hub and the frontline
    ((16, 28), (16, 52), [(19, 40)]),                            # the frontline's east flank
    ((16, 52), (28, 52), [(22, 49)]),                            # the hub's front edge beside it
    ((28, 100), (4, 100), [(16, 103)]),                          # the hub's back edge, east of the back wool
    ((-16, 100), (-16, 84), [(-19, 92)]),                        # the hub's west back flank
]
CHAMFER = 3
CHAMFERED = [(52, 60), (52, 96)]


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


# The hub's hole is a hexagon leaning on the diagonal rather than the compiled 12 by 16 square: its four corners
# moved and two points added, eating a block or two into each piece round it.
HOLE_OPS = [
    {"index": 0, "x": -1, "z": 70},
    {"index": 1, "x": 8, "z": 67},
    {"after": 1, "x": 13, "z": 72},
    {"index": 3, "x": 14, "z": 84},
    {"index": 4, "x": 6, "z": 87},
    {"after": 4, "x": 0, "z": 79},
]


# Each island keeps its outer side straight on the build zone's edge and gets an irregular inner side, one point
# pushed toward the channel and one pulled back. The islands are neutral and not fanned, so the east island's
# points are the west island's turned through the centre, and the channel stays fifteen blocks or more across.
ISLAND_OPS = {
    "mid-west-9": [{"index": 1, "x": -9, "z": -12}, {"after": 1, "x": -6, "z": -4}, {"after": 2, "x": -9, "z": 4},
                   {"index": 4, "x": -7, "z": 12}],
    "mid-east-9": [{"index": 0, "x": 7, "z": -12}, {"index": 3, "x": 9, "z": 12}, {"after": 3, "x": 6, "z": 4},
                   {"after": 4, "x": 9, "z": -4}],
}


def area(mark_id, h, x0, z0, x1, z1):
    return {"id": mark_id, "kind": "area", "h": h, "bevel": 0,
            "ring": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]}


def scarp(scarp_id, points, low, high):
    """Drawn west to east, so the high side is the one toward red's spawn."""
    return {"id": scarp_id, "kind": "scarp", "points": points, "low": low, "high": high, "face": 2, "band": 4}


def face_z(points, x):
    for (x0, z0), (x1, z1) in zip(points, points[1:]):
        if x0 <= x <= x1:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
    raise ValueError(x)


def stair(stair_id, points, x, low, high):
    """A flight cut into a scarp at 45 degrees, a block of rise to every block of run, from its foot to its
    head, on cell centres so each cell takes one whole height."""
    z0 = round(face_z(points, x)) - 1
    return {"id": stair_id, "kind": "line", "r": 2, "points": [[x, z0 + 0.5], [x, z0 + high - low + 0.5]],
            "h": [low, high]}


# The ground leans from the lip at 9 to the foot of a scarp at 12, which zigzags across the board like a bolt
# of lightning and stands seven blocks to the hub at 19; two stairs are cut into it. The hub leans on up to 23
# along its back edge and to the spawn yard at 21, and a swell rises at its back corner beside the spawn. The
# clamp is held level at 20 for its wall. The back wool's neck and the first blocks of its arm are held at 23
# for its wall, and past it the arm meets a second scarp, four blocks up to a yard at 27 round the room, with a
# stair of its own.
LIP, FOOT, HEAD, CLAMP, SPAWN_YARD, HUB_BACK, BACK_YARD = 9, 12, 19, 20, 21, 23, 27
FRONT_FACE = [[-26, 40], [-14, 50], [-6, 42], [6, 54], [14, 47], [24, 60], [36, 56]]
BACK_FACE = [[-14, 114], [-4, 118], [10, 115]]
RELIEF = [
    area("lip", LIP, -20, 20, 20, 32),
    scarp("front-face", FRONT_FACE, FOOT, HEAD),
    area("spawn-yard", SPAWN_YARD, -38, 66, -20, 86),
    area("hub-back", HUB_BACK, -16, 96, 20, 100),
    area("clamp", CLAMP, 28, 60, 56, 98),
    area("back-wall", HUB_BACK, -10, 98, 6, 112),
    scarp("back-face", BACK_FACE, HUB_BACK, BACK_YARD),
    area("back-yard", BACK_YARD, -10, 122, 6, 142),
    stair("front-stair-west", FRONT_FACE, -10, FOOT, HEAD),
    stair("front-stair-east", FRONT_FACE, 20, FOOT, HEAD),
    stair("back-stair", BACK_FACE, -2, HUB_BACK, BACK_YARD),
]


def push(push_id, x0, z0, x1, z1, amount, falloff):
    return {"id": push_id, "ring": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]], "amount": amount,
            "falloff": falloff, "crown": 0, "roughness": 0, "seed": 1}


PUSHES = [
    # a canyon six deep across the piece between the hub's hole and the clamp's mouth, its ring reaching into
    # both voids so the trench runs out into each of them rather than leaving a rim at their edges
    push("canyon", 8, 72, 32, 80, -6, 3),
    # a hollow four deep along the clamp's back approach, the length of the mouth, its ring over the mouth's
    # edge and stopping short of the room
    push("clamp-hollow", 30, 80, 42, 90, -4, 3),
    # a swell on the hub's west coast at its back corner beside the spawn, two rows of land inside its ring
    push("spawn-corner", -22, 88, -13, 98, 3, 5),
]

# The islands lean up from their gorge-facing ends at 9 to 11 across the middle. A half-turn solves the neutral
# group's z < 0 half and copies it, so the marks stand there.
ISLAND_RELIEF = [area("island-ends", LIP, -18, -14, 18, -10), area("island-crest", 11, -18, -2, 18, 0)]


def finish():
    return {
        "editShapes": {TEAM: reshape_ops(), HOLE: copy.deepcopy(HOLE_OPS), **copy.deepcopy(ISLAND_OPS)},
        "relief": {"team": {"base": BASE, "reach": 0, "step": 1, "marks": RELIEF, "pushes": PUSHES},
                   "neutral": {"base": LIP, "reach": 0, "step": 1, "marks": ISLAND_RELIEF}},
        "authors": ["Opus 5.5"],
        "created": "2026-09-22",
    }


if __name__ == "__main__":
    for name, doc in (("plan", plan()), ("finish", finish())):
        (HERE / f"{HERE.name}.{name}.json").write_text(json.dumps(doc, indent=1) + "\n")
