#!/usr/bin/env python3
"""Medlock Drift — the plan and the finish.

Adapted from a composed board:
    GET /api/compose?players=20&symmetry=mirror_z  seed 34
    composerVersion markers-in-blocks-1, cell 5, score 1.548
    structure: hub double-hole · frontline twin · wools l, clamp

What the composer gave: the smallest board of the four at 80 x 170 — a double-slotted hub, a clamp
wool round a small yard, an L wool on the far flank, and one plain mid band. Its two wools stood
134 and 104 blocks from the door that had to raid them.

What this board does with it. The clamp is kept and re-hung off the hub's east arm; the L wool keeps
the west flank; the spawn comes off the east flank to the back so the two raids come out 167 and
164. The mid, which arrived as one band offset east, becomes two twenty-five-block crossings with
twenty blocks of void between them, and the whole front is drawn out west so the far crossing lands
somewhere an attacker can only go on from by taking the west flank. And the spawn is given a second
exit: a build zone every interfacing component of which touches this team's ground and nobody
else's — the defender-egress bridge, twenty blocks straight across to the far wool's own apron, which
is the difference between rotating to the far wool and going the long way round the hub.

The one idea: a drift mine in red shale — stepped spoil, ochre pans, and a board where the only
two flat places are the pit floor at the front and the mine yard at the back.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-medlock-drift"

SHALE = 12                     # the base; a top block is surface - 1

plan = {
    "plan": 2,
    "meta": {"name": "Medlock Drift"},
    "globals": {"cell": 5, "symmetry": "mirror_z", "maxPlayers": 20, "surface": SHALE,
                "observerY": 44},
    "pieces": [
        # THE FRONT, drawn out west so the far crossing has somewhere to land. The composer's own
        # front is offset east; this keeps the offset and adds the flank rather than centring it.
        {"id": "front-w",   "role": "piece", "rect": [-9, 3, 5, 2]},
        {"id": "front-e",   "role": "piece", "rect": [-1, 3, 5, 2]},
        {"id": "front-bar", "role": "piece", "rect": [-9, 5, 13, 3]},
        # the double-slotted hub, as composed
        {"id": "hub-sw", "role": "piece", "rect": [-4, 8, 5, 2]},
        {"id": "hub-nw", "role": "piece", "rect": [-4, 12, 5, 2]},
        {"id": "hub-w",  "role": "piece", "rect": [-4, 10, 2, 2]},
        {"id": "hub-mid", "role": "piece", "rect": [-1, 10, 2, 2]},
        {"id": "hub-se", "role": "piece", "rect": [1, 8, 4, 2]},
        {"id": "hub-ne", "role": "piece", "rect": [1, 12, 4, 2]},
        {"id": "hub-e",  "role": "piece", "rect": [3, 10, 2, 2]},
        # the spawn off the hub's back rather than its east flank
        {"id": "spawn-t1",   "role": "piece", "rect": [-1, 14, 2, 2]},
        {"id": "spawn-room", "role": "spawn", "rect": [-1, 16, 2, 3]},
        # THE CLAMP, re-hung off the hub's east arm: two arms and a lintel round a ten-by-five yard
        # with the room closing its south side. The yard is a hole and nothing fills it.
        {"id": "clamp-w",     "role": "piece",     "rect": [5, 12, 2, 4]},
        {"id": "clamp-head",  "role": "piece",     "rect": [7, 12, 2, 1]},
        {"id": "clamp-e",     "role": "piece",     "rect": [9, 12, 2, 4]},
        {"id": "wool-a-room", "role": "wool-room", "rect": [7, 14, 2, 2]},
        # the L wool on the west flank, as composed and pulled back to the clamp's own depth. It is
        # the farther of the two from the door that defends it, which is why the bridge below goes
        # to this one and not to the clamp: a shortcut to the near wool is what WL9 is about.
        {"id": "wool-b-t1",   "role": "piece",     "rect": [-6, 12, 2, 2]},
        {"id": "wool-b-t2",   "role": "piece",     "rect": [-8, 12, 2, 3]},
        {"id": "wool-b-room", "role": "wool-room", "rect": [-10, 13, 2, 2]},
        {"id": "wool-b-t3",   "role": "piece",     "rect": [-6, 14, 2, 2]},
        # the apron the spawn's own bridge lands on
        {"id": "back-pad",    "role": "piece",     "rect": [-6, 16, 2, 2]},
    ],
    "zones": [
        # THE MID, CUT IN TWO. Twenty-five blocks of crossing on each flank with twenty of void
        # between them, so an attacker picks a side of the board before he lays a block and the two
        # landings lead to different halves of the hub.
        {"id": "crossing-e", "rect": [-1, -3, 5, 6], "holes": []},
        {"id": "crossing-w", "rect": [-9, -3, 5, 6], "holes": []},
        # THE EGRESS BRIDGE. Every interfacing component of this zone touches this team's ground and
        # no other — the spawn piece at one end and the clamp's own apron at the other. It is what
        # BZ5 calls the defender-egress bridge: the spawn's second exit, mainly for a defender
        # rotating to the far wool while the attackers push the crossings.
        {"id": "egress", "rect": [-4, 16, 3, 2], "holes": []},
        {"id": "egress-2", "rect": [-4, -18, 3, 2], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [5, 7], "facing": "front"}],
        "wools": [{"id": "wool-1", "piece": "wool-a-room", "at": [5, 5]},
                  {"id": "wool-2", "piece": "wool-b-room", "at": [5, 5]}],
        "iron": [], "destroyables": [], "cores": [],
    },
    "walls": [],
    "boxes": [],
}


# ── materials ────────────────────────────────────────────────────────────────────────────────────
# Three families. The GROUND is red — red sand, red sandstone, hardened clay, coarse dirt. What is
# BUILT is pale birch over cobblestone, which is the only light thing on the board. The ACCENT is
# grey andesite: the drift's portal, the erratics, and nowhere else.
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


GRASS, DIRT, COARSE, PODZOL = solid(2), solid(3), solid(3, 1), solid(3, 2)
RED_SAND, RED_SANDSTONE, CLAY = solid(12, 1), solid(179), solid(172)
SMOOTH_RED = solid(179, 2)
GRAVEL, STONE, COBBLE, ANDESITE = solid(13), solid(1), solid(4), solid(1, 5)
POLISHED_ANDESITE, COAL_ORE = solid(1, 6), solid(16)
BIRCH, BIRCH_LOG = solid(5, 2), solid(17, 2)
LAID_BIRCH = {"kind": "laidLog", "id": 17, "data": 2}


def cell_(seed, size, palette, rise=0, jitter=2, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}


def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}


def layered(bands, axis="depth", ending="handOver"):
    return {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}


SHALE_BODY = cell_(81, 9, [RED_SANDSTONE, CLAY, COAL_ORE, RED_SANDSTONE], rise=5)
SHALE_FACE = cell_(82, 7, [RED_SANDSTONE, CLAY, GRAVEL], rise=4)
FLOOR = cell_(83, 5, [GRAVEL, COBBLE, COARSE])         # the pit floor and the mine yard
TRAM = cell_(84, 5, [GRAVEL, ANDESITE, COARSE])        # the tramway

# The spoil finished by its ANGLE. A worked bank is bare where it is steep and green where it has
# stood long enough to take: the cuts are at 24 and 40 degrees, and this board's `step` of 2 puts a
# lot of ground on the shoulder band, which is what a benched tip looks like.
SHALE_SURFACE = layered([
    # a surfacing block is exactly one course and what is under it is soil (PT1), so podzol tops
    # the shoulder band rather than lying under the turf
    (24, layered([(1, GRASS), (1, COARSE), (2, DIRT)])),        # the tip that has taken
    (16, layered([(1, PODZOL), (1, RED_SAND), (2, CLAY)])),     # the working face's shoulder
    (50, SHALE_FACE),                                           # the shale itself
], axis="slope")

STRATA = layered([(2, CLAY), (1, GRAVEL), (3, RED_SANDSTONE), (1, SMOOTH_RED), (2, CLAY)])

themes = {
    "shale": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": SHALE_FACE},
        "surface": {"enabled": True, "depth": 4, "material": SHALE_SURFACE},
        "wall": STRATA, "wallEnabled": True,
        "fill": SHALE_BODY,
    },
    # the two floors somebody levelled: the pit floor at the front and the mine yard at the back
    "working": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": COBBLE},
        "surface": {"enabled": True, "depth": 2, "material": FLOOR},
        "wallEnabled": True,
        "wall": {"kind": "wallRun", "runs": [
            {"material": COBBLE, "width": 3},
            {"material": ANDESITE, "width": 2},
            {"material": CLAY, "width": 3},
        ]},
        "fill": SHALE_BODY,
    },
    # the drift: the stone portal and the retaining work either side of it, grey against the red
    "drift": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": POLISHED_ANDESITE},
        "surface": {"enabled": True, "depth": 2,
                    "material": cell_(85, 6, [ANDESITE, POLISHED_ANDESITE, COBBLE])},
        "wallEnabled": True,
        "wall": {"kind": "wallRun", "runs": [
            {"material": POLISHED_ANDESITE, "width": 2},
            {"material": ANDESITE, "width": 3},
        ]},
        "fill": cell_(86, 7, [STONE, ANDESITE], rise=4),
    },
}

STEP = cell_(87, 4, [COBBLE, ANDESITE, STONE], rise=2)
REVET = cell_(88, 4, [CLAY, RED_SANDSTONE, COBBLE], rise=2)

PIT, YARD = 12, 12


def pad(id_, ring, height, theme=None, scope="exclude"):
    shape = {"id": id_, "type": "polygon", "operation": "add", "group": "team",
             "floor": 0, "base_height": height, "height_mode": "level", "skirt": 0,
             "relief_scope": scope,
             "vertices": [[x, z] for x, z in ring],
             "anchor_heights": [height] * len(ring)}
    if theme:
        shape["theme"] = theme
    return shape


def flight(id_, ring, anchors, top, group="team"):
    return {"id": id_, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "group": group, "floor": 0, "base_height": top, "material": STEP,
            "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
            "vertices": [[x, z] for x, z in ring], "anchor_heights": list(anchors)}


def revetment(id_, points, top, radius=1, group="team"):
    """A retaining wall as a POLYLINE — the rasterizer splines its points before offsetting the band,
    so four clicked points draw as a curve. A polyline states its bounds rather than the points a
    height is stated at, so one base_height and no anchor_heights."""
    return {"id": id_, "type": "polyline", "operation": "add", "override": True, "keepClear": True,
            "group": group, "floor": 0, "base_height": top, "material": REVET,
            "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
            "radius": radius, "stroke_edge": "solid",
            "vertices": [[x, z] for x, z in points]}


add_shapes = [
    # THE PIT FLOOR — the front is the ground this board is fought over, so it is cut flat at the
    # base and taken out of the solve, and the benched spoil behind it meets it at a face. Its
    # outline sits inside the land's own after the vertex edits, because a shape that hangs over the
    # void builds a plinth of bedrock there and nothing declines it.
    pad("pit", [(-38, 20), (-22, 18), (-14, 24), (-7, 24), (2, 18), (17, 19),
                (18, 36), (0, 38), (-20, 37), (-38, 35)], PIT, theme="working"),
    # THE MINE YARD at the back, the other flat place
    pad("yard", [(-9, 76), (7, 75), (10, 97), (-10, 97)], YARD, theme="working"),
    # THE DRIFT — the adit's own portal, cut into the face of the spoil bank where the tramway
    # leaves the pit floor. Grey stone, and the one made thing that is neither floor nor wall.
    pad("portal", [(-4, 40), (6, 40), (6, 48), (-4, 48)], PIT + 4, theme="drift"),
    # the two inclines out of the pit onto the bank: twelve blocks of run for four of rise each
    flight("incline-w", [(-30, 38), (-22, 38), (-22, 50), (-30, 50)],
           [PIT, PIT, PIT + 4, PIT + 4], PIT + 4),
    # the east incline stops short of z 49: the hub's east slot is a subtract, and an override add
    # that reaches into one fills the negative space the board states there (SK13)
    flight("incline-e", [(10, 36), (18, 36), (18, 48), (10, 48)],
           [PIT, PIT, PIT + 4, PIT + 4], PIT + 4),
    # the revetment along the back of the pit, which is what holds a worked face up
    revetment("revet-w", [(-38, 37), (-24, 39), (-14, 38)], PIT + 2),
    revetment("revet-e", [(2, 38), (12, 37), (18, 38)], PIT + 2),
]

# ── the relief ───────────────────────────────────────────────────────────────────────────────────
relief = {
    # A BENCHED TIP. `step` snaps the finished surface to a quantum, which is what ruins a hillside
    # and is exactly what a worked spoil bank wants. Every stated level is a multiple of the step,
    # or the knob rounds it away: base 12, amount 6, crown 6. The benches come out as two-block
    # scrambles rather than barriers, which is the whole difference between a tip and a cliff.
    "team": {
        "base": 12, "reach": 0, "step": 2, "landform": "rolling",
        "grain": {"amplitude": 1, "scale": 13, "seed": 31},
        "marks": [],
        "pushes": [
            # THE BANK: the spoil the hub stands on. Its two gradients are set to agree — 6 over a
            # falloff of 9 is 0.67 a block outside the ring, and a crown of 6 over a half-width of
            # about 10 is 0.60 inside it — so the tip has no step at its own outline beyond the
            # benching, and its skirt dies at z 39 and z 81, which leaves the pit floor and the
            # mine yard on ground the push never touches.
            {"id": "bank", "amount": 6, "crown": 6, "falloff": 9, "roughness": 2, "seed": 32,
             "ring": [(-18, 48), (0, 46), (22, 49), (26, 60), (18, 70), (-2, 72), (-18, 66)],
             "amounts": [6, 6, 6, 4, 6, 6, 6]},
        ],
    },
}


# ── the pithead ──────────────────────────────────────────────────────────────────────────────────
def hall(wall_stack, storeys):
    return {
        "foundation": {"plate": {"stack": stack([(1, COBBLE)], "repeat"), "extent": 1},
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       "footing": None},
        "roof": {"form": "saltbox", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": COBBLE, "verge": LAID_BIRCH, "gable": BIRCH,
                 "gableWindows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0,
                                  "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3}},
        "wall": {"stack": wall_stack, "extent": 5},
        "post": BIRCH_LOG,
        "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                    "sill": 2, "width": 2, "height": 2, "spacing": 3},
        "storeys": storeys,
        "porch": None, "front": None,
        "beams": {"block": 17, "data": 2, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab",
                                            "fillBlock": 126, "fillData": 1},
                    "width": 2, "height": 3},
    }


GROUND_STOREY = {
    "clear": 5, "post": BIRCH_LOG, "deck": None,
    "wall": {"stack": stack([(3, cell_(89, 3, [COBBLE, ANDESITE])), (2, BIRCH)], "repeat"),
             "extent": 5},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 2, "width": 2, "height": 2, "spacing": 3},
}
UPPER_STOREY = {
    "clear": 4, "post": BIRCH_LOG, "deck": None,
    "wall": {"stack": stack([(3, BIRCH), (1, LAID_BIRCH)], "repeat"), "extent": 4},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 1, "width": 1, "height": 2, "spacing": 4},
}

pithead = hall(stack([(1, BIRCH)], "repeat"), [GROUND_STOREY, UPPER_STOREY])
shed = hall(stack([(1, BIRCH)], "repeat"), [dict(GROUND_STOREY, clear=6)])

# ── what stands on the board ─────────────────────────────────────────────────────────────────────
trees = json.load(open(os.path.join(HERE, "trees.json")))
tree_styles = {name: trees[name] for name in ("birk-1", "birk-2", "birk-3", "roundel-1")}

props = [
    # the tramway: the pithead's door, down the incline into the pit, and out to the front. One line,
    # both ends attached, running TO a door.
    {"id": "tramway", "kind": "stroke", "seed": 91, "radius": 2, "style": "solid", "coverage": 1.0,
     "claimsGround": True, "pave": TRAM,
     "points": [[0, 84], [2, 70], [0, 56], [-2, 44], [-6, 30]]},
    # and the level to the west wool, ending at its door
    {"id": "level", "kind": "stroke", "seed": 92, "radius": 2, "style": "solid", "coverage": 1.0,
     "claimsGround": True, "pave": TRAM,
     "points": [[-14, 62], [-24, 64], [-33, 68], [-40, 70]]},
    # ground cover: ONE shape, the whole board, the patchiness left to the density field, and both
    # gameplay numbers low
    {"id": "scrubcover", "kind": "flora", "seed": 93,
     "points": [[-44, 20], [20, 20], [58, 62], [28, 98], [-44, 94]],
     "spec": {"coverage": 0.18, "scale": 22, "octaves": 3, "fernShare": 0.4,
              "flowerShare": 0.03, "flowerScale": 12, "tallShare": 0.03}},
]

# ONE building beside the two stamped rooms, at a seat POST …/sketch/seats answers for a 7 x 5
# footprint rather than at a position that looked right: the weigh cabin at the head of the west
# incline, where the tramway comes off the pit floor onto the bank.
props += [
    {"id": "cabin-1", "kind": "house", "seed": 691, "front": "negZ", "style": "shed",
     "wings": [{"corners": [[-20, 42], [-14, 46]], "spec": {"ridge": "alongX", "storeysHigh": 1}}]},
]
# birches on the tip that has taken, and grey erratics on the flat — a rock cut from the ground's own
# tones reads as a patch of that ground standing up, and this ground is red. Every position is at
# least a dozen blocks from any room, because the pass seats a prop a block or three off the position
# stated and judges it at every image of its orbit, and the seats mask answers for the exact cell.
for i, (x, z, style) in enumerate([(-30, 24, "birk-1"), (10, 30, "birk-2"), (-32, 60, "birk-3"),
                                   (20, 66, "roundel-1"), (40, 84, "birk-1")]):
    props.append({"id": f"birk-{i}", "kind": "tree", "seed": 670 + i, "x": x, "z": z,
                  "style": style})
for i, (x, z) in enumerate([(-25, 72), (-12, 30), (-38, 18)]):
    props.append({"id": f"erratic-{i}", "kind": "boulder", "seed": 680 + i, "x": x, "z": z,
                  "style": "erratic"})

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-16",
    "themes": themes,
    "mapTheme": "shale",
    "biome": {"kind": "solid", "id": 37},
    # THE OUTLINE, ONE POINT AT A TIME. The compile hands back one 28-vertex ring. Read it down:
    #   0 (-50,65)  1 (-40,65)  2 (-40,60)  3 (-20,60)  4 (-20,40)  5 (-45,40)  6 (-45,15)
    #   7 (-20,15)  8 (-20,25)  9 (-5,25)  10 (-5,15)  11 (20,15)  12 (20,40)  13 (25,40)
    #  14 (25,60)  15 (55,60)  16 (55,80)  17 (25,80)  18 (25,70)  19 (5,70)   20 (5,95)
    #  21 (-5,95)  22 (-5,70)  23 (-20,70) 24 (-20,90) 25 (-30,90) 26 (-30,75) 27 (-50,75)
    "editShapes": {
        "back-pad-12": [
            # the west wool's garth, the spawn's yard, the bridge's own apron and the clamp's south
            # side: four rooms whose composed pieces are exactly their own footprint, so each stamps
            # a bedrock plinth on every side that is void
            {"index": 27, "x": -56, "z": 80},
            {"index": 25, "x": -34, "z": 96},
            {"index": 24, "x": -16, "z": 94},
            {"index": 22, "x": -11, "z": 72},
            {"index": 21, "x": -13, "z": 101},
            {"index": 20, "x": 13, "z": 101},
            {"index": 19, "x": 11, "z": 73},
            {"index": 17, "x": 23, "z": 87},
            {"index": 16, "x": 60, "z": 85},
            {"index": 15, "x": 61, "z": 57},
            # the two noses of the front, pushed out and broken
            {"index": 11, "x": 24, "z": 13},
            {"index": 10, "x": -4, "z": 17},
            # the bay between them, pulled back and scalloped so the east crossing aims at a mouth
            {"index": 9, "x": -7, "z": 28},
            {"after": 8, "x": -11, "z": 31},
            {"after": 8, "x": -14, "z": 31},
            {"index": 8, "x": -18, "z": 28},
            {"index": 7, "x": -19, "z": 17},
            # THE CUT. The far-west corner of the front is ground the plan-tier dead read named as
            # off every route, so it comes off the board rather than being decorated.
            {"index": 6, "x": -42, "z": 17},
            {"index": 5, "x": -39, "z": 36},
            {"index": 1, "x": -38, "z": 62},
            {"index": 0, "x": -56, "z": 58},
        ],
    },
    # THE THREE HOLES ARE NOT SCENERY: the hub's two slots and the clamp's yard compile to subtracts,
    # which are the board's own statement of its negative space. They are rounded off and opened a
    # block, and nothing fills them.
    "shapePropsById": {
        "void-1-cut": {"vertices": [[-11, 52], [-4, 52], [-3, 55], [-4, 59], [-11, 59], [-12, 55]]},
        "void-2-cut": {"vertices": [[7, 50], [14, 50], [16, 54], [14, 60], [7, 60], [4, 55]]},
        "void-3-cut": {"vertices": [[37, 64], [44, 64], [46, 67], [44, 71], [37, 71], [34, 67]]},
    },
    "bendShapes": {"back-pad-12": {"wander": 2.2, "step": 10, "seed": 33, "side": "out"}},
    "relief": relief,
    "addShapes": add_shapes,
    "roomStyles": {"spawn": pithead, "wool": shed},
    "dressing": {"styles": dict(tree_styles, shed={"kind": "house", "shell": shed},
                                erratic={"kind": "boulder", "form": "angular", "size": 3,
                                         "rock": cell_(90, 3, [STONE, ANDESITE]),
                                         "mossy": False}),
                 "props": props},
}


if __name__ == "__main__":
    json.dump(plan,   open(os.path.join(HERE, f"{SLUG}.plan.json"),   "w"), indent=1)
    json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
    print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
