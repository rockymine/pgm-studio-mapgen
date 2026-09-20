"""Writes the four plans this card is one composed board edited into, and the finish for the last of them.

`pinned.plan.json` is the composer's own answer, committed rather than fetched: it is reproduced exactly by
`POST /api/compose/pin` with

    {"players": 10, "teams": 2, "symmetry": "rot_180", "cell": 4, "seed": 78,
     "composerVersion": "body-first-2", "schema": 1}

and it is an ordinary `PlanModel` from there on. Ten players, `rot_180`, a `double-hole` hub and one `l`
wool: thirteen pieces on an 80 x 160 board, with two enclosed holes the hub's own shape makes.

Taking it over is editing that JSON, and the four variants are the four kinds of edit there are. Two are
edits to the PLAN — a height per piece, a piece split in two — and one is an edit to the LAYOUT the compiler
answers with, because a void ring is the compiler's statement and not the plan's. The fourth is the one that
cannot be made at all: an add over a hole, which `SK13` refuses at 422.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
PINNED = json.load(open(os.path.join(HERE, "pinned.plan.json")))

# The height each piece stands at, which is what ends the merge. Six distinct values over thirteen pieces:
# the hub's ring at the board's own 9, its arms stepping in and up, the spawn highest and the mid lowest.
SURFACES = {
    "hub-t1": 9, "hub-t2": 9,
    "hub-t3": 10, "hub-t4": 10,
    "hub-t5": 11, "hub-t6": 11,
    "hub-t7": 12,
    "spawn-t1": 13, "spawn-room": 13,
    "wool-a-t1": 10, "wool-a-t2": 11, "wool-a-room": 12,
    "mid-stone-0": 8,
}


def plan_with_surfaces(plan):
    """A height on every piece. `PlanVoids` still reads the void per component, so the holes survive — what
    ends is the merge: there is nothing left to merge once no two pieces share a height."""
    out = json.loads(json.dumps(plan))
    for piece in out["pieces"]:
        if piece["id"] in SURFACES:
            piece["surface"] = SURFACES[piece["id"]]
    return out


def plan_taken_over(plan):
    """The same, plus the one plan edit that is not a number: `hub-t1` split in two at a different height
    each, which makes an interface where there was none, and a `walls` entry to close it."""
    out = plan_with_surfaces(plan)
    pieces = out["pieces"]
    original = next(p for p in pieces if p["id"] == "hub-t1")
    x, z, w, h = original["rect"]
    pieces.remove(original)
    pieces.insert(0, {"id": "hub-t1-west", "role": "piece", "rect": [x, z, 4, h], "surface": 9})
    pieces.insert(1, {"id": "hub-t1-east", "role": "piece", "rect": [x + 4, z, w - 4, h], "surface": 10})
    for box in out.get("boxes", []):
        if "hub-t1" in box.get("members", []):
            box["members"] = [m for m in box["members"] if m != "hub-t1"] + ["hub-t1-west", "hub-t1-east"]
    out["walls"] = [{"a": "hub-t1-west", "b": "hub-t1-east"}]
    return out


def rounded(ring, corner=4):
    """One void ring with its corners taken off. A compiled subtract is the board's statement of its own
    negative space: it may be redrawn — this is what redrawing one looks like — but never deleted and never
    papered over with an add."""
    x0 = min(point[0] for point in ring)
    x1 = max(point[0] for point in ring)
    z0 = min(point[1] for point in ring)
    z1 = max(point[1] for point in ring)
    return [[x0 + corner, z0], [x1 - corner, z0], [x1, z0 + corner], [x1, z1 - corner],
            [x1 - corner, z1], [x0 + corner, z1], [x0, z1 - corner], [x0, z0 + corner]]


# ── the finish for the taken-over board: everything a plan cannot state ───────────────────────────────
SOLID = lambda block, data=0: {"kind": "solid", "id": block, "data": data}


def depth(*bands):
    return {"kind": "layered", "axis": "depth",
            "stack": {"ending": "repeat",
                      "bands": [{"thickness": t, "material": m} for m, t in bands]}}


def ground(surface, wall, rim):
    """One theme per height: a surfacing block, the strata a cut shows, and the cap on the void edge. A
    composed board's pieces stand over nothing, so every one of them is rim all the way round."""
    return {"bedrock": {"relative": False, "value": 1},
            "fill": SOLID(1), "wall": SOLID(wall), "wallEnabled": True, "wallOnTerrainFaces": True,
            "rim": {"enabled": True, "depth": 1, "material": SOLID(rim)}, "rimEdges": "void",
            "surface": {"enabled": True, "depth": 3, "material": depth((SOLID(surface), 1), (SOLID(3), 2))}}


FINISH = {
    # A theme is stated on a SHAPE, and a flat plan has one shape — so `themeByHeight` has nothing to bind
    # to until the heights exist. Heights first, then paint.
    "themes": {
        "mid":    ground(surface=13, wall=24, rim=24),        # gravel over sandstone: the neutral holm
        "ring":   ground(surface=2, wall=1, rim=4),           # the hub's own ring, meadow on stone
        "arm":    ground(surface=2, wall=98, rim=98),         # the arms, brick-faced
        "inner":  ground(surface=2, wall=98, rim=98),
        "keep":   ground(surface=1, wall=98, rim=98),         # the piece nearest the spawn: bare stone
        "camp":   ground(surface=2, wall=4, rim=4),           # spawn and wool room: cobble-faced
    },
    "themeByHeight": {"8": "mid", "9": "ring", "10": "arm", "11": "inner", "12": "keep", "13": "camp"},
    "mapTheme": "ring",
}


# ── the road and the props the taken-over board carries ───────────────────────────────────────────────
# A composed board is corridors: every piece is a few cells wide with nothing around it, so a road runs
# ALONG a corridor and a prop stands where a search says it can, never where it looks right.
ROAD = {"kind": "cell", "seed": 7701, "cellSize": 3, "jitter": 55, "warp": 1, "rise": 0,
        "palette": [SOLID(4), SOLID(1), SOLID(1, 6)]}

# Where a prop may stand, computed rather than eyed. The search is over every built cell: keep the cell and
# its eight neighbours, all at one height, none of them claimed, three clear of every paved cell — and the
# same of the cell's own rot_180 image, because a prop is judged at every image of its orbit. On this board
# that is 1,899 cells, thinning to 56 once an oak's crown is spaced for, images included. These are the
# first twenty of that list; every one of them is in the authored half and the fan draws its twin.
#
# What the search answers depends on what it searched against, and two passes of this one were wrong. Run
# before the compiled INTENT was stored it answered 3,164 cells, because the rooms, the doors and the
# spawns are not in the claims map until the intent is: five of its twenty were then declined `DR-KEEP`.
# Run without the ORBIT it answered 2,293, and a tree sat two blocks from another tree's image.
SEARCHED = [(-30, 22), (-30, 34), (-30, 52), (-26, -27), (-25, 22), (-25, 34), (-25, 52), (-21, -54),
            (-21, -22), (-20, 27), (-18, 65), (-18, 75), (-16, -27), (-15, 22), (-13, 60), (-11, -54),
            (-11, -25), (-10, -6), (-10, 4), (-10, 27)]

# And five placed the way an author places them when the board looks like a landscape: down the middle of
# the corridor, beside the road, over a hole, in the wool room, in the spawn. Each names a different rule.
BY_EYE = [("eye-on-the-road", 0, 46), ("eye-beside-it", 0, 43), ("eye-over-a-hole", -14, 38),
          ("eye-in-the-wool-room", 0, 74), ("eye-in-the-spawn", 36, 34)]

DRESSING = {
    "styles": {
        "oak-9": {"kind": "tree", "form": "template", "species": "oak", "height": 9},
        "rock-3": {"kind": "boulder", "form": "round", "size": 3, "mossy": True,
                   "rock": {"kind": "turbulence", "seed": 7702, "scale": 3, "octaves": 3, "rise": 3,
                            "stops": [SOLID(4), SOLID(48), SOLID(1, 5)]}},
    },
    # The spine of the hub, drawn ALONG a corridor rather than across one: a stroke repaints the top block
    # of every column it crosses, and a corridor is what there is to cross.
    "props": [
        {"id": "spine", "kind": "stroke", "seed": 7703, "radius": 2, "style": "solid",
         "claimsGround": True, "pave": ROAD,
         "points": [[-30, 46], [-10, 46], [10, 46], [26, 46]]},
    ] + [
        # All twenty are oaks: a boulder rests on a footprint seven cells across and the search above
        # tests a cell and its eight neighbours, so a rock wants its own wider test — which is
        # `techniques/trees-and-boulders`, not this card.
        {"id": f"searched-{index}", "kind": "tree", "seed": 7710 + index, "x": x, "z": z,
         "style": "oak-9"}
        for index, (x, z) in enumerate(SEARCHED)
    ] + [
        {"id": name, "kind": "tree", "seed": 7740 + index, "x": x, "z": z, "style": "oak-9"}
        for index, (name, x, z) in enumerate(BY_EYE)
    ],
}

VARIANTS = [
    ("1-as-pinned", PINNED, None),
    ("2-void-redrawn", PINNED, "redraw"),
    ("3-a-surface-per-piece", plan_with_surfaces(PINNED), None),
    ("4-taken-over", plan_taken_over(PINNED), "finish"),
]

if __name__ == "__main__":
    for name, plan, _ in VARIANTS:
        if name == "2-void-redrawn":
            continue                                   # the same plan; its edit is to the compiled layout
        path = os.path.join(HERE, f"{name}.plan.json")
        json.dump(plan, open(path, "w"), indent=1)
        heights = sorted({piece.get("surface", plan["globals"]["surface"]) for piece in plan["pieces"]})
        print(f"{name:24s} {len(plan['pieces']):3d} pieces, {len(plan.get('walls') or []):2d} wall(s), "
              f"heights {heights}")
    json.dump(FINISH | {"dressing": DRESSING}, open(os.path.join(HERE, "4-taken-over.finish.json"), "w"),
              indent=1)
    print(f"{'4-taken-over.finish':24s} {len(FINISH['themes'])} themes, "
          f"{len(DRESSING['props'])} prop(s), {len(DRESSING['styles'])} style(s)")
