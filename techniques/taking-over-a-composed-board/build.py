"""Writes the four plans this card is one composed board edited into, and the finish for the last of them.

`pinned.plan.json` is the composer's own answer, committed rather than fetched: it is reproduced exactly by
`POST /api/compose/pin` with

    {"players": 10, "teams": 2, "symmetry": "rot_180", "cell": 4, "seed": 78,
     "composerVersion": "body-first-2", "schema": 1}

and it is an ordinary `PlanModel` from there on. Ten players, `rot_180`, a `double-hole` hub and one `l`
wool: thirteen pieces on an 80 x 160 board, with two enclosed holes the hub's own shape makes.

Taking it over is editing that JSON, and knowing which document an edit belongs to is most of the skill.
A height per piece, a piece split, a piece replaced by a build zone and a wall are edits to the PLAN. A void
ring redrawn, a coast chamfered, a theme, a road and a prop are edits to the LAYOUT the compiler answers
with. And one edit — an add over a hole — is the one that should not be made in either: it stores at 200
with an `SK13` complaint, and the complaint is the only thing that says the document and the world disagree.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
PINNED = json.load(open(os.path.join(HERE, "pinned.plan.json")))

# The height each piece stands at, and the numbers are the point rather than a decoration. A composed
# board is flat, so the author's first decision is where the hard cuts go — and a cut only pays if it is
# somewhere the board is fought over.
#
# So: the FRONT bar stays at the board's own 9, flat and low, and everything behind it is raised to 13.
# That four-block step is a barrier a defender shoots over and an attacker has to climb, and it is what
# gives the paint somewhere to change. The two cross-pieces between the bars are then STAIRCASES — each is
# split into three and stepped 10, 11, 12 — so the climb walks instead of being scrambled. The wool
# approach climbs on from the back at 14, 15, 16, and the neutral mid sits one below everything at 8.
SURFACES = {
    "hub-t2": 9, "hub-t6": 9,                                            # the front bar, flat and low
    "hub-t4-front": 10, "hub-t4-middle": 11, "hub-t4-back": 12,          # the middle staircase
    "hub-t7-front": 10, "hub-t7-middle": 11, "hub-t7-back": 12,          # the spawn's staircase
    "hub-t1": 13, "hub-t5": 13,                                          # the back bar
    "spawn-t1": 11, "spawn-room": 11,                                    # a shelf off the stair
    "wool-a-t1": 14, "wool-a-t2": 15, "wool-a-room": 16,                 # the approach, climbing
    "mid-stone-0": 8,                                                    # the neutral holm
    "hub-t3": 13,
}

# Nine heights and five themes, because a theme is a place and not a number: the risers are where the
# paint changes and the flats either side of one are each a single ground.
ZONES = {8: "mid", 9: "front", 10: "stair", 11: "stair", 12: "stair", 13: "back",
         14: "approach", 15: "approach", 16: "approach"}

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
    """The same heights, plus every other edit a plan takes: two pieces cut into staircases, a piece
    replaced by a build zone, and a wall where the approach wants one."""
    out = plan_with_surfaces(plan)
    pieces = out["pieces"]

    # Two pieces SPLIT, and split into something: each cross-piece between the bars is three cells deep,
    # so cutting it at every cell gives three one-cell treads. Stepped 10, 11, 12 between a front bar at 9
    # and a back bar at 13, that is four one-block risers — a staircase a player walks rather than a wall
    # they scramble. A plan piece has one height, so a slope is a run of pieces and nothing else.
    for cross in ("hub-t4", "hub-t7"):
        original = next(piece for piece in pieces if piece["id"] == cross)
        x, z, w, h = original["rect"]
        index = pieces.index(original)
        pieces.remove(original)
        treads = [f"{cross}-front", f"{cross}-middle", f"{cross}-back"]
        for offset, name in enumerate(treads):
            pieces.insert(index + offset, {"id": name, "role": "piece",
                                           "rect": [x, z + offset, w, 1],
                                           "surface": SURFACES[name]})
        rename(out, cross, treads)

    # A piece REMOVED and a build zone declared over its rect. The zone rides in `zones`, which is what a
    # plan says about the void; the compiler turns it into the intent's own `build.areas`, fanned.
    far = next(piece for piece in pieces if piece["id"] == FAR_LANE)
    pieces.remove(far)
    rename(out, FAR_LANE, [])
    out["zones"].append({"id": "far-lane", "rect": far["rect"], "holes": []})

    # A WALL, on the wool approach and not in the hub (the author's ruling). It stands across the middle
    # of the approach's L, four courses of bedrock over the ground either side — a thing a defender builds
    # on and cannot lose, low enough that an attacker bridges it. `walk` reports it as `barrier +4` and
    # that reading is about WALKING: a four-course bedrock wall is bridged, not walked, and reading the
    # barrier as a fault is why so few maps have ever had one.
    out["walls"] = [{"a": "wool-a-t1", "b": "wool-a-t2"}]
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
    composed board's pieces stand over nothing, so every one of them is rim all the way round.

    The wall is a `teamTint` over the stated stone rather than the stone itself. A tint resolves per
    canonical island and falls back to its `neutral` where nobody owns the ground, and on this board that
    is three answers: red's half, blue's half, and the neutral holm between them. It is put in the WALL
    because a composed board is all rim — every piece stands over void — so the wall is the course a
    player sees from the next piece across."""
    return {"bedrock": {"relative": False, "value": 1},
            "fill": SOLID(1),
            "wall": {"kind": "teamTint", "blockId": 159, "neutral": SOLID(wall)},
            "wallEnabled": True, "wallOnTerrainFaces": True,
            "rim": {"enabled": True, "depth": 1, "material": SOLID(rim)}, "rimEdges": "void",
            "surface": {"enabled": True, "depth": 3, "material": depth((SOLID(surface), 1), (SOLID(3), 2))}}


# ── the structure the mid carries: a double deck on four legs ──────────────────────────────────────────
# The neutral holm is the one piece both teams bridge to, and a flat stone island is nothing to arrive at.
# A deck gives it what a contested middle wants: a roof to stand on for the height, and a room under it to
# stand in for the cover, with the legs at the corners so neither is a box.
#
# It is drawn as four MADE layers, because a sketch layer is one span per column — `[floor, floor +
# base_height)` — and a leg passing a deck would be two. So the legs are cut at each deck instead: y8-10
# under the lower floor, y12-15 between the two. Nothing overlaps, and `kind: "made"` is what says the
# layers are a built thing rather than terrain driven into itself.
#
# The footprint is odd in both axes about the origin (x -8..8, z -4..4 in columns), so it is its own rot_180
# image and needs no mirror: a board whose middle is one block off-centre is one team's middle.
# `rise` is the field's vertical period and `PT4` refuses a nought on a fill: a plane-sampled field resolves
# every block of a column alike, so a face of it comes out in vertical stripes. Two courses is enough here,
# where the thickest thing the paint covers is a four-block leg.
DECK_STONE = {"kind": "cell", "cellSize": 4, "rise": 2,
              "palette": [SOLID(98), SOLID(98, 1), SOLID(1, 6)]}
LEG_STONE = SOLID(4)
DECK = (-8, 9, -4, 5)                    # min/max exclusive, so columns -8..8 by rows -4..4


def deck_layers():
    """The mid's deck, one layer per span: legs, floor, legs, floor. Clear under the lower deck is three
    blocks and between the decks four, so both storeys are stood in rather than crawled through."""
    x0, x1, z0, z1 = DECK
    legs = [(x0, x0 + 2, z0, z0 + 2), (x1 - 2, x1, z0, z0 + 2),
            (x0, x0 + 2, z1 - 2, z1), (x1 - 2, x1, z1 - 2, z1)]
    floors = [(x0, x1, z0, z1)]
    out = []
    for name, rects, floor, thickness, paint in (
            ("legs-lower", legs, 8, 3, LEG_STONE),
            ("floor-lower", floors, 11, 1, DECK_STONE),
            ("legs-upper", legs, 12, 4, LEG_STONE),
            ("floor-upper", floors, 16, 1, DECK_STONE)):
        shapes = [{"id": f"deck-{name}-{index}", "type": "rectangle", "operation": "add",
                   "floor": floor, "base_height": thickness, "material": paint,
                   "min_x": a, "max_x": b, "min_z": c, "max_z": d}
                  for index, (a, b, c, d) in enumerate(rects)]
        # The `addLayers` shape `tools/drive.py` takes: `shapes` and `groups` at the top level, which the
        # driver wraps into the layer's own `layout` when it posts them.
        out.append({"id": f"deck-{name}", "name": f"deck {name}", "base_y": 0, "kind": "made",
                    "part_of": "mid-deck", "shapes": shapes,
                    "groups": [{"id": f"deck-{name}", "name": "the mid's deck", "mirrors": False,
                                "shapeIds": [shape["id"] for shape in shapes]}]})
    return out


# The one coast this board chamfers, and where. `hub-t1-13` is the compiled polygon the hub's own bar
# becomes; its vertex 2 is the corner the front line and the mid band both meet, and taking it off is what
# stops a bridger arriving at a point. The ring is the compiler's, read off `POST /api/plan/compile`.
CHAMFER_SHAPE, CHAMFER_AT = "hub-t1-13", 2
CHAMFERED = chamfer([[-32, 44], [28, 44], [28, 56], [-32, 56]], (28, 56))

FINISH = {
    # A theme is stated on a SHAPE, and a flat plan has one shape — so `themeByHeight` has nothing to bind
    # to until the heights exist. Heights first, then paint.
    "themes": {
        # Five grounds, one a place. The risers are where they change, which is what makes the cut read
        # as a boundary and not as a stripe.
        "mid":      ground(surface=13, wall=24, rim=24),   # gravel on sandstone: the neutral holm
        "front":    ground(surface=2, wall=1, rim=4),      # the low flat bar both teams fight over
        "stair":    ground(surface=1, wall=98, rim=98),    # the treads: bare stone, brick-faced
        "back":     ground(surface=2, wall=98, rim=98),    # the raised ground behind the front
        "approach": ground(surface=2, wall=4, rim=4),      # the climb to the wool, cobble-faced
    },
    "themeByHeight": {str(height): zone for height, zone in ZONES.items()},
    "mapTheme": "front",
    # The coast's own corner, taken off. `chamfer` answers the ring; `editShapes` is how the ring is said
    # to the studio — one point moved back along the first edge, one inserted on the second — which is the
    # same two routes the canvas uses to drag a vertex and add one.
    "editShapes": {CHAMFER_SHAPE: [
        {"index": CHAMFER_AT, "x": CHAMFERED[CHAMFER_AT][0], "z": CHAMFERED[CHAMFER_AT][1]},
        {"after": CHAMFER_AT, "x": CHAMFERED[CHAMFER_AT + 1][0], "z": CHAMFERED[CHAMFER_AT + 1][1]}]},
    "addLayers": deck_layers(),
}


# ── the road and the props the taken-over board carries ───────────────────────────────────────────────
# A composed board is corridors: every piece is a few cells wide with nothing around it, so a road runs
# ALONG a corridor and a prop stands where a search says it can, never where it looks right.
ROAD = {"kind": "cell", "seed": 7701, "cellSize": 3, "jitter": 55, "warp": 1, "rise": 0,
        "palette": [SOLID(4), SOLID(1), SOLID(1, 6)]}

# Where a prop MAY stand is computed; which of those places takes one, and how many, is the author's. The
# search is over every built cell: keep the cell and its eight neighbours, all at one height, none of them
# claimed, three clear of every paved cell — and the same of the cell's own rot_180 image, because a prop is
# judged at every image of its orbit. On this board it answers 1,062 cells and 34 spaced sites. Planting all
# 34 is a forest on a board of ten-block corridors, which is not what the arrangement is for.
#
# So the sites below are chosen out of that legal set, to the author's rules for where a tree belongs:
#
#   * toward the OUTSIDE of a piece, never down its middle. With no road on it a player still runs down the
#     centre of a corridor, and trees along the rim read as an alley rather than as an obstacle course.
#   * two in front of each hole, on the rim between the bar and the void, and nothing on the mid-facing
#     brink, which is the edge the front line is bridged from.
#   * nothing where a build zone is ARRIVED at. Three trees stood eight blocks from the far lane's north
#     shore, so a player who crossed the lane landed in them; the pair that stays is on the bar's far side.
#   * nothing on the approach in front of the wall, and one tree in the corner behind it, in front of the
#     room.
#   * nothing on the mid. A contested holm is where a structure goes, and this one carries the deck below.
#
# The board's own arithmetic does much of this unasked. The whole spawn-to-wall run answers ZERO legal
# cells except the back bar's west end: a one-cell tread can never hold a prop, because its eight
# neighbours are at another height by construction; the spawn shelf is claimed; and the approach in front
# of the wall is kept clear by the wall's own keep-out. 916 paved cells each owing a tree three blocks is
# what takes the rest.
#
# Three things the search itself has to get right, each of which cost a list. It is asked of the board
# WITHOUT these props on it, because a tree raises its own column's top and claims the cells its crown
# covers — the same board answers 1,062 cells stripped and 748 with these seven on it. It is asked with the
# compiled INTENT stored, because the rooms, the doors and the spawns are not in the claims map until then:
# without it the board answers 1,398 cells and 52 sites, four of the first twenty then refused `DR-KEEP`.
# And it tests every cell's ORBIT IMAGE as well as the cell, which is the last 212 cells of the field.
# And the last three are outside what that search offers, which is the whole reason it is not the authority.
# The search keeps a cell whose eight neighbours are ground at one height, so it refuses every RIM cell on
# the board — beyond the rim is void, and a neighbour that is not ground fails the test. The studio's own
# rules ask something narrower: ground under the trunk (`DR-SITE`), three clear of the paving (`DR-ROAD`),
# unclaimed (`DR-CLAIM`), not kept clear (`DR-KEEP`). The back bar's outer rim passes all four and the
# search's silence there is conservatism, not a refusal — so a site is checked against the DRESSING PASS,
# and the search is only a way of proposing sites nobody has to think about.
#
# On a bar twelve deep with a five-wide road down it, the rim is the only place left: three blocks off the
# paving puts a tree at z 54 or 55, and its crown then hangs over the void, which is the configuration
# `WS71` is about. The trade is the author's and he wants the trees.
TREES = [
    ("oak-front-west-a", -18, 30),   # in front of hole-1, on the rim between the bar and the void
    ("oak-front-west-b", -11, 30),
    ("oak-front-east-a", 5, 30),     # and in front of hole-2
    ("oak-front-east-b", 11, 30),
    ("oak-lane-far-a", -29, 54),     # the far side of the back bar, eight blocks off the lane's shore
    ("oak-lane-far-b", -23, 54),
    ("oak-room-corner", -18, 78),    # behind the wall, in the corner in front of the room
    ("oak-path-a", 16, 55),          # three along the road itself, on the bar's outer rim
    ("oak-path-b", 6, 54),
    ("oak-path-c", -4, 55),
]

# And five placed the way an author places them when the board looks like a landscape: on the road, beside
# it, over a hole, in the doorway of the wool room, and against the bedrock wall. Four rules between them.
BY_EYE = [("eye-on-the-road", 0, 50), ("eye-beside-it", 0, 47), ("eye-over-a-hole", 10, 38),
          ("eye-in-the-doorway", -12, 77), ("eye-against-the-wall", -14, 67)]

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
    # `spine` leaves the spawn, climbs the spawn's own staircase onto the back bar, runs its length and
    # climbs the wool approach to the room's doorstep. `sally` drops off it down the MIDDLE staircase to
    # the front bar and on to the brink facing the mid, which is where a bridge lands: the seed composed
    # no frontline piece, so the mid band is the front.
    "props": [
        {"id": "spine", "kind": "stroke", "seed": 7703, "radius": 2, "style": "solid",
         "claimsGround": True, "pave": ROAD,
         "points": [[36, 34], [30, 34], [26, 36], [22, 42], [22, 50], [10, 50], [-4, 50], [-12, 50],
                    [-14, 54], [-14, 62], [-14, 70], [-10, 74], [0, 74]]},
        {"id": "sally", "kind": "stroke", "seed": 7704, "radius": 2, "style": "solid",
         "claimsGround": True, "pave": ROAD,
         "points": [[-2, 50], [-2, 46], [-2, 42], [-2, 38], [-2, 34], [-2, 28], [-2, 21]]},
    ] + [
        # All ten are oaks: a boulder rests on a footprint seven cells across and the search above tests a
        # cell and its eight neighbours, so a rock wants its own wider test — which is
        # `techniques/trees-and-boulders`, not this card.
        {"id": name, "kind": "tree", "seed": 7710 + index, "x": x, "z": z, "style": "oak-9"}
        for index, (name, x, z) in enumerate(TREES)
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
