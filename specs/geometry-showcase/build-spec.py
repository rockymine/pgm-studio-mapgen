#!/usr/bin/env python3
"""Geometry Showcase — the whole board written out of sketch shapes.

Nothing here is a building, a prop or a relief. Every climb, span, wall and mound is a rectangle,
a polygon with per-vertex anchor heights, or a polyline with heights along its arc, and the joints
between them are arithmetic rather than eyeballing: `geometry.treads` runs the rasterizer's own
reading, so a landing's height is stated from what the flight above it will actually build.

Writes geometry-showcase.plan.json, .layout.json and .intent.json beside this file.
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry import rect, flight, stroke, ring, spiral_arcs, rot180, treads

HERE = os.path.dirname(os.path.abspath(__file__))

# ── the three levels the board is played on, as top blocks (a player stands one course above) ──
FIELD, SHELF, PLATEAU = 7, 19, 31
WALL_WALK, MERLON, PIER = 13, 14, 15

half = []          # shapes drawn on the red half; the blue half is their rot_180 image
middle = []        # shapes that are their own image about the origin

# ── the ground plane, with a gorge across the middle that stops short of both flanks ──────────
half += [rect("gs-r-plate", -100, -136, 100, -12, 0, 8, theme="gs-field"),
         rect("gs-r-flank", -100, -12, -56, 12, 0, 8, theme="gs-field")]

# ── the curtain wall. Every shape here states floor 0 and its full thickness rather than being
#    perched on the plate at floor 8: on one layer the taller add wins a column floor and all, so
#    a wall drawn from the bedrock up builds exactly the same column as one standing on the
#    ground — and states nothing for SK9 to read as a lost slab (see NOTES.md).
for side, x0, x1 in (("w", -100, -8), ("e", 8, 100)):
    half.append(rect(f"gs-r-wall-{side}", x0, -112, x1, -109, 0, WALL_WALK + 1,
                     keepClear=True, theme="gs-rampart"))
    # A merlon is the same column one course taller, not a block laid on the walk: two adds on one
    # layer do not stack, and the taller takes the column floor and all.
    for mx in range(x0, x1 - 2, 6):
        half.append(rect(f"gs-r-merlon-{side}{mx}", mx, -112, mx + 3, -109, 0, MERLON + 1,
                         keepClear=True, theme="gs-rampart"))
# the gate piers, standing one course over the crenellation
for side, x0 in (("w", -11), ("e", 8)):
    half.append(rect(f"gs-r-pier-{side}", x0, -114, x0 + 3, -107, 0, PIER + 1,
                     keepClear=True, theme="gs-rampart"))
# and the way up onto the rampart walk — six cells, six courses, one tread each
half.append(flight("gs-r-wall-stair", -26, -109, -20, -103, "z", WALL_WALK, FIELD + 1,
                   keepClear=True, theme="gs-stair"))

# ── the comparison: one shelf, two ways up it, the same twelve courses ────────────────────────
half.append(rect("gs-r-shelf", -72, -96, -48, -78, 0, SHELF + 1, theme="gs-shelf"))
half.append(flight("gs-r-stair-1to1", -66, -108, -58, -96, "z", FIELD + 1, SHELF,
                   keepClear=True, theme="gs-stair"))          # 12 cells, 12 courses
half.append(flight("gs-r-ramp-1to2", -96, -92, -72, -84, "x", FIELD + 1, SHELF,
                   keepClear=True, theme="gs-stair"))          # 24 cells, 12 courses

# ── the monument plateau, cut by a stair notch on its north face and a corridor through it ────
# One concave polygon; the notch is a re-entrant rather than a subtract, so SK13 has nothing to
# refuse and the plateau keeps its own ground.
half.append(dict(id="gs-r-plateau-w", type="polygon", operation="add", floor=0,
                 base_height=PLATEAU + 1, theme="gs-plateau",
                 vertices=[[-40, -80], [10, -80], [10, -36], [-2, -36],
                           [-2, -57], [-14, -57], [-14, -36], [-40, -36]]))
# The east half carries a lobe out to x 50 at its southern end. That lobe is the flank ramp's
# landing: a flight that tops out level with the ground beside it for one cell has not arrived
# anywhere, because the cell in front of it is still the drop it climbed.
half.append(dict(id="gs-r-plateau-e", type="polygon", operation="add", floor=0,
                 base_height=PLATEAU + 1, theme="gs-plateau",
                 vertices=[[22, -80], [50, -80], [50, -68], [40, -68],
                           [40, -36], [22, -36]]))

# ── the switchback, inside the notch: up +z... in, turn 180, up -z... out, twelve cells each ──
# Four pieces, not three. A flight needs a floor at both ends: the apron is where a player
# steps off the field and squares up, the head is where they arrive and turn onto the plateau —
# which is open along the head's whole east side, rather than for the one cell a bare last tread
# would give.
half.append(rect("gs-r-sb-apron", -14, -41, -8, -36, 0, FIELD + 2,
                 keepClear=True, theme="gs-stair"))
half.append(flight("gs-r-sb-up", -14, -53, -8, -41, "z", SHELF, FIELD + 1,
                   keepClear=True, theme="gs-stair"))
half.append(rect("gs-r-sb-landing", -14, -57, -2, -53, 0, SHELF + 1,
                 keepClear=True, theme="gs-stair"))
half.append(flight("gs-r-sb-out", -8, -53, -2, -41, "z", SHELF + 1, PLATEAU,
                   keepClear=True, theme="gs-stair"))
half.append(rect("gs-r-sb-head", -8, -41, -2, -36, 0, PLATEAU + 1,
                 keepClear=True, theme="gs-stair"))

# ── the south face: the same 24 courses as the switchback, taken straight. Two flights and a
#    landing between them, and it is the measurement the switchback exists to be read against —
#    28 cells of depth here against 18 there, for exactly the same climb. ────────────────────
half.append(flight("gs-r-south-lower", -8, -108, 8, -97, "z", FIELD + 1, 18,
                   keepClear=True, theme="gs-stair"))
half.append(rect("gs-r-south-landing", -12, -97, 12, -92, 0, SHELF + 1,
                 keepClear=True, theme="gs-stair"))
half.append(flight("gs-r-south-upper", -8, -92, 8, -80, "z", SHELF + 1, PLATEAU,
                   keepClear=True, theme="gs-stair"))

# ── the long way up: a graded ramp along the plateau's east flank, 44 cells for 23 courses ────
half.append(flight("gs-r-ramp-flank", 40, -68, 50, -36, "z", PLATEAU, FIELD + 1,
                   keepClear=True, theme="gs-stair"))

# ── the third way up: a polyline, splined, its heights read along the arc it draws ────────────
# The climb finishes at the point BEFORE the last: a stroke that is still rising where it meets
# the plateau leaves a two-course lip along the whole seam, because the plateau is the taller add
# and wins those columns. The last segment runs level, at the plateau's own top, and laps into it.
SERP = [(-48, -30), (-60, -44), (-52, -62), (-42, -73), (-36, -78)]
_cum = [0.0]
for a, b in zip(SERP, SERP[1:]):
    _cum.append(_cum[-1] + math.dist(a, b))
_climb = _cum[-2]
half.append(stroke("gs-r-serpentine", SERP,
                   [FIELD + 2 + (PLATEAU - FIELD - 1) * min(c, _climb) / _climb for c in _cum],
                   radius=4, stroke_edge="solid", keepClear=True, theme="gs-stair"))

# ── the corridor under the plateau: no subtract at all. The plateau is two polygons with a gap
#    between them, the base plate floors the gap, and one shape on a second layer roofs it. ────
vault = [rect("gs-r-vault", 10, -80, 22, -36, 0, 18, theme="gs-plateau")]

# ── the monument podium: three nested circles on the plateau, one course each. Nesting is the
#    whole mechanism — the taller add wins the columns it covers, so discs whose tops rise inward
#    write a stepped field with no subtract and no per-column authoring. Kept clear of the
#    corridor at x >= 10, since a disc reaching over it would fill the tunnel to bedrock. ──────
for n, (r, h) in enumerate(((9, 1), (6, 2), (3, 3))):
    half.append(dict(id=f"gs-r-podium-{n}", type="circle", operation="add",
                     center_x=0, center_z=-69, radius=r, floor=0,
                     base_height=PLATEAU + 1 + h,
                     keepClear=True, theme="gs-podium"))

# ── a hollow drum redoubt in the mid-field: ONE polygon per arc, wound even-odd — the outer
#    circle, a slit inward, the inner circle traced the other way round. An outer disc minus an
#    inner one would be a subtract, and SK13 refuses an add over one anywhere on the board. ──
half += ring("gs-r-drum", 26, -23, 9, 6, 0, 16, gaps=((30, 60), (210, 240)),
             keepClear=True, theme="gs-rampart")
# the way onto its walk, inside the court: twelve cells for seven courses, ending in the annulus
# itself, where the ring's own top is the same 15 the flight arrives at
half.append(flight("gs-r-drum-stair", 23, -29, 29, -20, "z", 15, FIELD + 1,
                   keepClear=True, theme="gs-stair"))

# ── the stepped mound: nine nested circles, each two blocks wide and one course up ────────────
for n in range(9):
    half.append(dict(id=f"gs-r-mound-{n}", type="circle", operation="add",
                     center_x=-78, center_z=-26, radius=18 - 2 * n,
                     floor=0, base_height=9 + n, theme="gs-mound"))

# ── the spiral ramp: one polyline whose radius shrinks as it winds, so the turns lie beside
#    one another. A constant radius would be a helix, and a layer holds one span per column. ──
half += spiral_arcs("gs-r-spiral", 74, -38, 20, 4, turns=2.5,
                    t_start=FIELD + 1, t_end=FIELD + 19, band=4, start_deg=90,
                    keepClear=True, theme="gs-spiral")
# The eye. A coil that shrinks to nothing leaves a shaft down the middle at field level, and the
# last thing the ramp does is walk into it. The cap stands at the height the last turn arrives at.
half.append(dict(id="gs-r-spiral-cap", type="circle", operation="add",
                 center_x=74, center_z=-38, radius=6, floor=0, base_height=FIELD + 20,
                 keepClear=True, theme="gs-spiral"))

# ── the bridge: a graded bank on each shore and a deck hung over the void between them ────────
half.append(flight("gs-r-br-bank", -8, -34, 8, -12, "z", FIELD + 1, SHELF,
                   keepClear=True, theme="gs-deck"))
half.append(rect("gs-r-br-kerb", -8, -12, -6, 12, 17, 4, keepClear=True, theme="gs-deck"))
middle.append(rect("gs-br-deck", -8, -12, 8, 12, 17, 3, keepClear=True, theme="gs-deck"))

# ── both halves ───────────────────────────────────────────────────────────────────────────────
shapes = half + [rot180(s) for s in half] + middle
vault_shapes = vault + [rot180(s) for s in vault]


def theme(surface, wall, rim, depth=3, soil=None):
    def solid(id, data=0):
        return {"kind": "solid", "id": id, "data": data}
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"material": solid(*rim), "depth": 1, "enabled": True},
        # A surfacing block — grass, podzol, mycelium — is exactly one course and what is under it
        # is soil, so it goes at the top of a layered stack rather than filling the whole depth
        # (PT1). Everything else here is a rock and fills its bucket.
        "surface": {"material": ({"kind": "layered", "layers": [
                        {"material": solid(*surface), "thickness": 1},
                        {"material": solid(*soil), "thickness": depth - 1}]}
                    if soil else solid(*surface)),
                    "depth": depth, "enabled": True},
        "wall": {"kind": "wallRun", "runs": [{"material": solid(*wall), "width": 4}]},
        "wallEnabled": True,
        # never (1, 0): the stone-only invariant is what stops an upper layer's fill band painting
        # through the ground beneath it, and it compares against stone exactly.
        "fill": {"kind": "solid", "id": 1, "data": 5},
    }


THEMES = {
    "gs-field":   theme((2,), (3,), (13,), soil=(3,)),  # grass over dirt, gravel lip
    "gs-shelf":   theme((24, 2), (24,), (24, 1)),      # sandstone mesa
    "gs-stair":   theme((155,), (155, 2), (155, 1)),   # quartz: every climb reads as one family
    "gs-plateau": theme((98,), (98, 1), (98, 3)),      # stone brick
    "gs-rampart": theme((4,), (48,), (98,)),           # cobble wall, mossy skirt
    "gs-deck":    theme((5, 1), (17,), (5,)),          # planks and log
    "gs-podium":  theme((159, 4), (159, 1), (155,)),   # yellow clay under the monument
    "gs-mound":   theme((172,), (159, 1), (159, 14)),  # hardened clay steps
    "gs-spiral":  theme((251, 4), (251, 1), (251, 14)),# concrete coil
}

layout = {
    "setup": {"mirror_mode": "rot_180", "center": {"cx": 0, "cz": 0},
              "bbox": {"min_x": -100, "max_x": 100, "min_z": -136, "max_z": 136}},
    "layers": [
        {"id": "ground", "name": "Ground", "base_y": 0,
         "layout": {"shapes": shapes, "groups": []}},
        # The corridor's roof, and the mass over it up to the plateau's own top. Its own layer
        # because one layer keeps one span per column and the corridor needs a floor and a lid.
        {"id": "vault", "name": "Vault", "base_y": 14,
         "layout": {"shapes": vault_shapes, "groups": []}},
    ],
    "themes": THEMES,
    "mapTheme": "gs-field",
}

MONUMENT_Y = PLATEAU + 1 + 3 + 1     # the podium's top step, plus one to stand on

intent = {
    "teams": [{"id": "red", "name": "Red", "color": "red"},
              {"id": "blue", "name": "Blue", "color": "blue"}],
    "maxPlayers": 16,
    "spawns": [
        {"team": "red", "point": {"x": 0, "y": 8, "z": -125}, "yaw": 0,
         "protection": [{"minX": -9, "minZ": -134, "maxX": 9, "maxZ": -116}],
         "iron": []},
        {"team": "blue", "point": {"x": 0, "y": 8, "z": 125}, "yaw": 180,
         "protection": [{"minX": -9, "minZ": 116, "maxX": 9, "maxZ": 134}],
         "iron": []},
    ],
    "observer": {"point": {"x": 0, "y": 48, "z": 0}, "yaw": 0},
    "build": {"maxHeight": 40, "areas": [], "holes": []},
    "waterLanes": None, "wools": [],
    "destroyables": [
        {"owner": "red", "name": "Red Gnomon", "style": "cube-3", "materials": "ender stone",
         "anchor": {"x": 0, "y": MONUMENT_Y, "z": -69}, "float": 4, "box": None},
        {"owner": "blue", "name": "Blue Gnomon", "style": "cube-3", "materials": "ender stone",
         "anchor": {"x": 0, "y": MONUMENT_Y, "z": 69}, "float": 4, "box": None},
    ],
    "cores": None,
    "meta": {"name": "Geometry Showcase", "created": "2026-09-05",
             "authors": ["Claude Opus 5"], "contributors": []},
    "symmetry": None, "islandTeams": {"1": "red"}, "structures": None,
}

plan = {
    # Version 2: a marker's offset is stated in BLOCKS from its piece's corner, not in cells.
    "plan": 2, "meta": {"name": "Geometry Showcase"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 16,
                "surface": 8, "observerY": 48},
    # The arrangement only. Everything the board is actually made of is drawn in the layout, so
    # these say which ground is where and at what height and nothing about its shape.
    "pieces": [
        {"id": "spawn", "role": "spawn", "rect": [-2, -26, 4, 4], "surface": 8},
        {"id": "yard", "role": "piece", "rect": [-10, -22, 20, 6], "surface": 8},
        {"id": "plateau", "role": "piece", "rect": [-8, -16, 16, 9], "surface": 32},
        {"id": "midfield", "role": "piece", "rect": [-10, -7, 20, 5], "surface": 8},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [10, 5], "facing": "back"}],
        "destroyables": [{"id": "destroyable-1", "piece": "plateau", "at": [40, 11],
                          "style": "cube-3", "materials": "ender stone", "float": 4,
                          "name": "Gnomon"}],
    },
}

for name, doc in (("plan", plan), ("layout", layout), ("intent", intent)):
    with open(f"{HERE}/geometry-showcase.{name}.json", "w") as fh:
        json.dump(doc, fh, indent=1)

print(f"ground {len(shapes)} shapes, vault {len(vault_shapes)}, themes {len(THEMES)}")
print("joints the flights have to make:")
print(f"  1:1  stair   {treads(FIELD+1, SHELF, 12)[-1]:>3}  -> shelf {SHELF}")
print(f"  1:2  ramp    {treads(FIELD+1, SHELF, 24)[-1]:>3}  -> shelf {SHELF}")
print(f"  switchback   in {treads(SHELF, FIELD+1, 12)}")
print(f"               out {treads(SHELF+1, PLATEAU, 12)}")
print(f"  flank ramp   {treads(PLATEAU, FIELD+1, 44)[0]:>3}  -> plateau {PLATEAU}")
