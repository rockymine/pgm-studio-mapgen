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

# The height each piece stands at, which is what ends the merge. Six distinct values, and they are chosen
# to say something: the two long bars of the hub at the board's own 9, the crosses between them a step up,
# the wool approach climbing 11-12-13 to its room, the spawn level with the approach's foot, the neutral
# mid one below everything so the middle reads as the low ground it is.
SURFACES = {
    "hub-t1": 9, "hub-t1-west": 9, "hub-t1-mouth": 10, "hub-t1-east": 9,
    "hub-t2": 9, "hub-t5": 9, "hub-t6": 9,
    "hub-t3": 10, "hub-t4": 10, "hub-t7": 10,
    "spawn-t1": 11, "spawn-room": 11,
    "wool-a-t1": 11, "wool-a-t2": 12, "wool-a-room": 13,
    "mid-stone-0": 8,
}

# The piece that comes out and the zone that replaces it, which is the one edit on this card made for a
# reason the studio cannot check. Looking west out of the spawn, the double-hole hub is three bars with a
# void between each pair, and `hub-t3` is the far one — 12 x 12 blocks at the end of that view.
#
# The author's ruling, and the whole of why it is here: the board is rot_180 with one wool a team, so both
# sides spawn, turn the same way and run past each other down the far lane. Taking the far bar out and
# declaring a build zone over it means an attacker either takes the lane nearer their own spawn or bridges
# a void gap under fire, and the two teams meet instead of trading. Two bars could go; one is enough.
FAR_LANE = "hub-t3"


def plan_with_surfaces(plan):
    """A height on every piece. `PlanVoids` still reads the void per component, so the holes survive — what
    ends is the merge: there is nothing left to merge once no two pieces share a height."""
    out = json.loads(json.dumps(plan))
    for piece in out["pieces"]:
        if piece["id"] in SURFACES:
            piece["surface"] = SURFACES[piece["id"]]
    return out


def plan_taken_over(plan):
    """The same heights, plus every other edit a plan takes: a piece cut in three, a piece replaced by a
    build zone, and a wall where the approach wants one."""
    out = plan_with_surfaces(plan)
    pieces = out["pieces"]

    # A piece SPLIT, so the mouth of the wool approach is its own place at its own height. `hub-t1` runs
    # nine cells and the approach leaves it from the middle three; cut there and the mouth can step up to
    # meet the climb instead of the whole bar having to.
    original = next(piece for piece in pieces if piece["id"] == "hub-t1")
    x, z, w, h = original["rect"]
    index = pieces.index(original)
    pieces.remove(original)
    for offset, (name, width) in enumerate([("hub-t1-west", 3), ("hub-t1-mouth", 3), ("hub-t1-east", 3)]):
        pieces.insert(index + offset, {"id": name, "role": "piece",
                                       "rect": [x + offset * 3, z, width, h],
                                       "surface": SURFACES[name]})
    rename(out, "hub-t1", ["hub-t1-west", "hub-t1-mouth", "hub-t1-east"])

    # A piece REMOVED and a build zone declared over its rect. The zone rides in `zones`, which is what a
    # plan says about the void; the compiler turns it into the intent's own `build.areas`, fanned.
    far = next(piece for piece in pieces if piece["id"] == FAR_LANE)
    pieces.remove(far)
    rename(out, FAR_LANE, [])
    out["zones"].append({"id": "far-lane", "rect": far["rect"], "holes": []})

    # No `walls` entry, and the reason is measured rather than chosen. A barrier belongs on the wool
    # approach and not in the hub (the author's ruling) — but this approach is an L of three pieces in a
    # line, so every interface in it IS the route, and a `walls` entry stamped across the middle of it
    # stood four courses over the ground either side with no way through: `walk` called it *"barrier +4 at
    # (-9, 67)"* and the wool was unreachable. `findings.txt` has the reading.
    #
    # So the barrier is drawn instead, in the finish, as two override adds with a gate between them on the
    # road's own line. A `walls` entry closes an interface; a gate is what closes an interface and keeps a
    # route.
    out["walls"] = []
    return out


def rename(plan, gone, arrivals):
    """A box is a list of member ids, so a piece that is split or removed has to leave the box it was in."""
    for box in plan.get("boxes", []):
        if gone in box.get("members", []):
            box["members"] = [m for m in box["members"] if m != gone] + list(arrivals)


def chamfer(ring, at, back=6):
    """One corner of a compiled outline taken off. A piece's own coast is as editable as the void's: the
    vertices are in the layout the compiler answered with, and moving one is the same kind of edit as
    redrawing a subtract. `at` is the corner to replace and `back` how far along each edge to cut it."""
    out = []
    for index, point in enumerate(ring):
        if tuple(point) != tuple(at):
            out.append(point)
            continue
        before = ring[index - 1]
        after = ring[(index + 1) % len(ring)]
        out.append(_towards(point, before, back))
        out.append(_towards(point, after, back))
    return out


def _towards(point, other, distance):
    span = math.hypot(other[0] - point[0], other[1] - point[1]) or 1
    return [round(point[0] + (other[0] - point[0]) * distance / span),
            round(point[1] + (other[1] - point[1]) * distance / span)]


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


# The barrier on the wool approach: two override adds across the t1/t2 interface with six blocks of gate
# between them, where the road runs. `keepClear` is what makes the dressing pass see it and `height_mode`
# with `skirt` is what makes the relief leave its stated top alone — both, or it is neither.
def barrier(shape_id, min_x, max_x):
    return {"id": shape_id, "type": "rectangle", "operation": "add", "override": True,
            "keepClear": True, "height_mode": "level", "skirt": 0,
            "floor": 0, "base_height": 15, "theme": "keep",
            "min_x": min_x, "min_z": 66, "max_x": max_x, "max_z": 69}


BARRIER = [barrier("gate-west", -20, -17), barrier("gate-east", -11, -8)]

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
    "barrier": BARRIER,
}


# ── the road and the props the taken-over board carries ───────────────────────────────────────────────
# A composed board is corridors: every piece is a few cells wide with nothing around it, so a road runs
# ALONG a corridor and a prop stands where a search says it can, never where it looks right.
ROAD = {"kind": "cell", "seed": 7701, "cellSize": 3, "jitter": 55, "warp": 1, "rise": 0,
        "palette": [SOLID(4), SOLID(1), SOLID(1, 6)]}

# Where a prop may stand, computed rather than eyed. The search is over every built cell: keep the cell and
# its eight neighbours, all at one height, none of them claimed, three clear of every paved cell — and the
# same of the cell's own rot_180 image, because a prop is judged at every image of its orbit. On this board
# it answers 272 cells and fifteen sites, and the roads are why: 886 paved cells on 5,280 of land, each
# owing a tree three blocks, is most of the board gone.
#
# Every pass of this search that left something out was wrong, and the numbers are worth keeping. Against
# the layout alone it said 512 cells: the rooms, the doors and the spawns are not in the claims map until
# the compiled INTENT is stored. With the intent but not the ORBIT it said 404, and a tree landed two
# blocks from another tree's image. And it is re-run after every edit that moves ground — an earlier list
# was searched before the far lane came out and the roads were redrawn, and six of its twenty sites were
# then refused.
SEARCHED = [(-30, 51), (-26, -27), (-25, 51), (-24, 22), (-21, -27), (-21, -22), (-20, 30), (-18, 76),
            (-16, -27), (-16, -22), (-14, 22), (-11, -24), (-10, -6), (-10, 5), (-8, 28)]

# And five placed the way an author places them when the board looks like a landscape: on the road, beside
# it, over a hole, in the doorway of the wool room, and on one jamb of the gate. Four rules between them.
BY_EYE = [("eye-on-the-road", 0, 50), ("eye-beside-it", 0, 47), ("eye-over-a-hole", 10, 38),
          ("eye-in-the-doorway", -12, 77), ("eye-on-the-gate-jamb", -19, 67)]

DRESSING = {
    "styles": {
        "oak-9": {"kind": "tree", "form": "template", "species": "oak", "height": 9},
        "rock-3": {"kind": "boulder", "form": "round", "size": 3, "mossy": True,
                   "rock": {"kind": "turbulence", "seed": 7702, "scale": 3, "octaves": 3, "rise": 3,
                            "stops": [SOLID(4), SOLID(48), SOLID(1, 5)]}},
    },
    # Two roads, and both go somewhere. A road on a board of corridors runs ALONG one and never across
    # one, because a stroke repaints the top block of every column it crosses — and it is drawn down the
    # middle of a piece rather than along its lip, because a corridor's lip is its rim.
    #
    # `spine` leaves the spawn, turns down the hub's far bar, climbs the wool approach and ends on the
    # room's own floor. `sally` drops off it through the middle cross-piece to the brink facing the mid,
    # which is this board's front: the seed composed no frontline piece, so the front is the bridge.
    "props": [
        {"id": "spine", "kind": "stroke", "seed": 7703, "radius": 2, "style": "solid",
         "claimsGround": True, "pave": ROAD,
         "points": [[36, 34], [30, 34], [26, 36], [22, 41], [22, 47], [16, 50], [4, 50], [-8, 50],
                    [-12, 51], [-14, 55], [-14, 62], [-14, 70], [-10, 74], [0, 74]]},
        {"id": "sally", "kind": "stroke", "seed": 7704, "radius": 2, "style": "solid",
         "claimsGround": True, "pave": ROAD,
         "points": [[-2, 50], [-2, 44], [-2, 38], [-2, 32], [-2, 26], [-2, 21]]},
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
