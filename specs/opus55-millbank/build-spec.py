"""Writes opus55-millbank's plan and finish.

The arrangement is composed board p20 rot_180 seed 5 (`composed-seed5.plan.json`, the composer's raw answer),
taken over: wool-a's arm is moved so its room is sixteen blocks off the hub, both arms are balanced against the
spawn, each wool approach carries a bedrock wall one interface out from the room, a neutral holm is set in the
gorge, and the whole team unit is stated at one surface so the relief alone gives it its heights.

    python3 build-spec.py [relief] [outdir]

`relief` names one of RELIEFS (the board's own when omitted); `outdir` is where the two documents are written,
named after that directory, so a sketch of a relief can be driven beside the board without replacing it.
"""
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent

composed = json.loads((HERE / "composed-seed5.plan.json").read_text())

BASE = 9

# Each wool arm is made exactly as deep as the hub side it meets, so the wall on that interface spans it end to
# end with no shoulder to step round. wool-a's arm reaches a cell further west so its room stands sixteen blocks
# clear of hub-t1, and wool-b's a cell further east so the two rooms are about the same walk from their spawn.
RECT = {
    "wool-a-t1": [-11, 14, 7, 4],
    "wool-a-room": [-11, 18, 3, 2],
    "wool-b-t1": [8, 14, 5, 4],
    "wool-b-room": [13, 15, 2, 3],
}
BOXES = {"wool-a": [-11, 14, 7, 6], "wool-b": [8, 14, 7, 4]}

# The holm in the gorge is as wide as the build zone and twice as deep as the lip strip. A hop onto it must be
# ten blocks or more, so the team units stand a cell further out than composed and the gorge is ten cells deep.
SHIFT = 1
HOLM = {"id": "mill-holm", "role": "piece", "rect": [-4, -2, 8, 4], "mirrors": False}
GORGE = [-4, -4 - SHIFT, 8, 8 + 2 * SHIFT]

# One wall per approach, on the arm's interface with the hub, sixteen blocks in front of the room.
WALLS = [{"a": "wool-a-t1", "b": "hub-t3"}, {"a": "wool-b-t1", "b": "hub-t4"}]


def plan():
    doc = copy.deepcopy(composed)
    doc["meta"] = {"name": "Millbank"}
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


# Block coordinates of red's half, which the symmetry turns onto blue's. The gorge lip runs along z 20.
LIP_Z = 20
TEAM = "frontline-t1-9"

# The team unit's outline as the compile answers it, and the few points it is reshaped by. Every point moves
# the coast outward except the one on the hub's back flank, which pulls in to keep the bay beside wool-a's room
# at sixteen blocks. The lip, the rooms and the wall interfaces are not touched: the lip is where the build zone
# attaches, and pulling it in would leave void the zone does not cover.
COMPILED_RING = [(-44, 60), (-16, 60), (-16, 20), (16, 20), (16, 28), (32, 28), (32, 60), (52, 60), (52, 64),
                 (60, 64), (60, 76), (32, 76), (32, 92), (24, 92), (24, 108), (8, 108), (8, 92), (-16, 92),
                 (-16, 76), (-32, 76), (-32, 84), (-44, 84)]
RESHAPE = [
    ((-44, 60), (-16, 60), [(-36, 57), (-24, 56)]),   # west orchard's gorge-side edge
    ((-16, 60), (-16, 20), [(-19, 50), (-20, 36), (-18, 26)]),  # west flank of the hub and the meadow
    ((16, 28), (32, 28), [(25, 25)]),                  # the meadow's east shoulder
    ((32, 28), (32, 60), [(35, 36), (36, 48)]),        # east flank
    ((32, 60), (52, 60), [(42, 57)]),                  # east orchard's gorge-side edge
    ((32, 76), (32, 92), [(35, 84)]),                  # hub's east back flank
    ((8, 92), (-16, 92), [(-4, 95)]),                  # hub's back edge beside the spawn
    ((-16, 92), (-16, 76), [(-13, 84)]),               # hub's west back flank, pulled in
    ((-44, 84), (-44, 60), [(-47, 70)]),               # west orchard's far end
]


def reshape_ops():
    ring, ops = list(COMPILED_RING), []
    for a, b, points in RESHAPE:
        at = next(i for i in range(len(ring)) if ring[i] == a and ring[(i + 1) % len(ring)] == b)
        for point in points:
            ops.append({"after": at, "x": point[0], "z": point[1]})
            ring.insert(at + 1, point)
            at += 1
    return {TEAM: ops}


def area(mark_id, h, x0, z0, x1, z1, bevel=0):
    return {"id": mark_id, "kind": "area", "h": h, "bevel": bevel,
            "ring": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]}


def orchards(h):
    """Both orchards held at one height across the seam they share with the hub, so each bedrock wall stands on
    level ground its whole run."""
    return [area("orchard-west", h, -48, 58, -12, 86), area("orchard-east", h, 28, 58, 62, 78)]


def lip(h=BASE, z1=LIP_Z + 6):
    return area("lip", h, -20, LIP_Z - 2, 36, z1)


def spawn_yard(h):
    return area("spawn-yard", h, 6, 94, 26, 110)


def ramp(ramp_id, x, z0, z1, h0, h1, r=3):
    """A lane pinned from h0 at z0 to h1 at z1, flat across its width."""
    return {"id": ramp_id, "kind": "line", "r": r, "points": [[x, z0], [x, z1]], "h": [h0, h1]}


def scarp(scarp_id, points, low, high, face=2, band=4):
    """Drawn west to east, so the high side is the one toward red's spawn."""
    return {"id": scarp_id, "kind": "scarp", "points": points, "low": low, "high": high, "face": face,
            "band": band}


RELIEFS = {
    # One lean from the gorge to the spawn and no face anywhere: the lip at 9, the orchards at 15, the spawn
    # yard at 20, and everything between them solved.
    "lean": [lip(), *orchards(15), spawn_yard(20)],

    # Three benches, each pinned flat, with the ground between them left free so it grades into a walkable
    # shoulder: the meadow at 9, the hamlet at 14, the spawn at 18.
    "benches": [area("meadow", BASE, -20, 18, 36, 34), area("hamlet", 14, -20, 48, 36, 88), *orchards(14),
                spawn_yard(18)],

    # The meadow flat at 9 to a curved scarp that stands seven blocks to the hamlet, whose ground then leans
    # on up to the spawn. Two lanes are cut through the face, each rising the seven blocks over sixteen.
    "scarp": [area("meadow", BASE, -20, 18, 36, 34),
              scarp("hamlet-face", [[-22, 44], [-8, 40], [4, 43], [14, 49], [24, 46], [38, 41]], BASE, 16),
              *orchards(17), spawn_yard(21),
              ramp("lane-west", -12, 34, 50, BASE, 16), ramp("lane-east", 28, 32, 48, BASE, 16)],

    # The frontline sectioned: a low quay strip on the gorge at 9, a four-block bank behind it curving across
    # the whole front, the meadow at 13 on top of the bank, and the hamlet leaning on up to the spawn with no
    # face at all. Two lanes climb the bank from the quay.
    "quay": [lip(BASE, 27),
             scarp("bank", [[-22, 32], [-6, 30], [8, 33], [20, 31], [38, 34]], BASE, 13, face=2, band=3),
             area("meadow", 13, -20, 36, 36, 42), *orchards(16), spawn_yard(20),
             ramp("lane-west", -10, 24, 38, BASE, 13), ramp("lane-east", 10, 24, 38, BASE, 13)],
}
BOARD_RELIEF = "scarp"


def finish(relief):
    return {
        "editShapes": reshape_ops(),
        "relief": {"team": {"base": BASE, "reach": 0, "step": 1, "marks": RELIEFS[relief]}},
        "authors": ["Opus 5.5"],
        "created": "2026-09-22",
    }


if __name__ == "__main__":
    relief = sys.argv[1] if len(sys.argv) > 1 else BOARD_RELIEF
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE
    out.mkdir(parents=True, exist_ok=True)
    for name, doc in (("plan", plan()), ("finish", finish(relief))):
        (out / f"{out.name}.{name}.json").write_text(json.dumps(doc, indent=1) + "\n")
