#!/usr/bin/env python3
"""Clints Scar — a limestone crag and the pavement above it, at 120 x 292.

One landform carries the board: a crag running the length of each half, high ground on its east and
a graded apron on its west, with the two crags' inner ends leaving an S-shaped defile through the
origin. Under rot_180 an S is invariant, so the corridor reads as one continuous feature rather than
as the seam between two copies.

Every boundary is drawn by `landform.wander`: a break of slope carrying a drop of H blocks is
displaced perpendicular to its own trend at wavelength 2.5H and amplitude 1.0-1.4H, one vertex every
wavelength/6. Nothing splines a mark, so a landform's plan is whatever is typed here.

The crag is stated as three statements rather than one, because a face standing on flat ground is a
retaining wall:

  scar        the free face, 14 blocks over a 6-block gap — 67 degrees, not crossed on foot
  apron       talus at the angle of repose, following the scar's own wandered trace offset outward,
              so it is thick under the re-entrants and thin on the spurs the way talus actually lies
  footslope   the concave toe the apron decays into, which is what the objective stands on

and the pavement is laid after the scar so its per-vertex heights win inside the ring: the skyline
varies without the scarp needing a height it cannot state.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import landform

SLUG = "opus5-clints-scar"

# The vertical structure, low to high.
BECK, TOE, APRON, FIELD, DEFILE, LEDGE_LOW, LEDGE_HIGH, PAVEMENT, FELL = 14, 17, 20, 22, 24, 29, 34, 40, 46

# The crag's course: five control points, every segment 13-28 degrees off the z axis, because an
# axis-aligned break of slope is the most visible line a voxel lattice can carry.
SCAR_COURSE = [[46, -10], [34, -44], [16, -78], [2, -112], [-6, -146]]

marks, pushes = [], []


def offset(course, distance):
    """The course walked parallel to itself, `distance` blocks to its west. The apron inherits the
    crag's plan-form instead of stating its own, which is both fewer numbers and the correct
    shape."""
    out = []
    for index, (x, z) in enumerate(course):
        ax, az = course[max(0, index - 1)]
        bx, bz = course[min(len(course) - 1, index + 1)]
        dx, dz = bx - ax, bz - az
        length = math.hypot(dx, dz) or 1.0
        out.append([round(x - (-dz / length) * distance, 1), round(z - (dx / length) * distance, 1)])
    return out


# ── the crag ─────────────────────────────────────────────────────────────────────────────────────
# Drop 14 over the face, so the trace wanders at wavelength 35 and amplitude 17: five re-entrants
# down its length, none of them the same width as its neighbour.
scar_trace = landform.wander(SCAR_COURSE, drop=PAVEMENT - LEDGE_HIGH + 8, amplitude=1.1, seed=17)
marks.append({"id": "scar", "kind": "scarp", "points": scar_trace,
              "high": PAVEMENT, "low": APRON, "face": 6, "band": 5})

# ── what lies under it ───────────────────────────────────────────────────────────────────────────
# Talus fails above roughly 33-37 degrees, so the batter is typed as the angle of repose rather than
# chosen. The apron follows the wandered trace, not the control line.
apron_trace = landform.wander(offset(SCAR_COURSE, 11), drop=6, amplitude=1.2, seed=23)
marks.append({"id": "apron", "kind": "line", "r": 8, "tread": 2, "batter": 33,
              "points": apron_trace, "h": [APRON] * len(apron_trace)})

footslope_trace = landform.wander(offset(SCAR_COURSE, 22), drop=4, amplitude=1.3, seed=29)
marks.append({"id": "footslope", "kind": "line", "r": 9, "tread": 4, "batter": 9,
              "points": footslope_trace, "h": [TOE] * len(footslope_trace)})

# ── the pavement above it ────────────────────────────────────────────────────────────────────────
# Laid after the scar, so its heights win inside its own ring and the crag's skyline varies by the
# 3 blocks a scarp's single `high` cannot say.
pavement_ring = landform.wander_ring(
    [[52, -8], [58, -60], [50, -112], [30, -146], [-4, -146], [8, -112], [22, -74], [40, -34]],
    drop=5, amplitude=1.1, seed=31)
pavement_heights = [PAVEMENT + (2 if index % 3 == 0 else -1 if index % 3 == 1 else 1)
                    for index in range(len(pavement_ring))]
marks.append({"id": "pavement", "kind": "area", "bevel": 4,
              "ring": pavement_ring, "h": pavement_heights})

# ── two ledges across the face ───────────────────────────────────────────────────────────────────
# A narrow flat in the middle of a wall is where soil collects, and the painter bands by angle, so
# these are the only two places the crag greens.
for name, height, out in (("ledge-low", LEDGE_LOW, 4), ("ledge-high", LEDGE_HIGH, 1)):
    trace = landform.wander(offset(SCAR_COURSE, out), drop=3, amplitude=1.0, seed=37 + out)
    marks.append({"id": name, "kind": "line", "r": 3, "tread": 2,
                  "points": trace, "h": [height] * len(trace)})

# ── the defile, and the plug in its throat ───────────────────────────────────────────────────────
# Authored for the -z half only; rot_180 supplies the other limb, and the two together are one S
# through the origin rather than two halves meeting at a seam.
defile_trace = landform.wander([[54, -30], [30, -14], [8, -3], [0, 0]],
                               drop=4, amplitude=0.9, seed=41)
marks.append({"id": "defile", "kind": "line", "r": 13, "tread": 6,
              "points": defile_trace, "h": [DEFILE] * len(defile_trace)})
marks.append({"id": "plug", "kind": "point", "at": [0, 0], "r": 9, "h": DEFILE + 8})

# ── the beck: the apron's drainage, reaching the rim ─────────────────────────────────────────────
# Of a channel's total fall, the headwater quarter carries about half. A constant gradient is the
# fluvial twin of a constant-angle hillside.
beck_course = [[-2, -60], [-16, -78], [-26, -100], [-42, -122], [-56, -140]]
beck_trace = landform.wander(beck_course, drop=3, amplitude=1.1, seed=43)
marks.append({"id": "beck", "kind": "line", "r": 5, "tread": 2, "points": beck_trace,
              "h": landform.concave_fall(TOE + 1, BECK, len(beck_trace))})

# ── the fell the team stands on ──────────────────────────────────────────────────────────────────
fell_ring = landform.wander_ring([[-24, -141], [-2, -139], [2, -127], [-20, -129]],
                                 drop=4, amplitude=0.8, seed=47)
marks.append({"id": "fell", "kind": "area", "bevel": 5,
              "ring": fell_ring, "h": [FELL, FELL + 1, FELL - 2, FELL - 1]
              if len(fell_ring) == 4 else [FELL] * len(fell_ring)})

# ── the fell's descent to the field ──────────────────────────────────────────────────────────────
# Three marks, not two. Pinning the fell and the field alone fills a constant 32-degree ramp between
# them, which is walkable, featureless, and the shape a hillside is not: a slope is a convex crest
# over a straight midslope over a concave footslope, and the proportions are what make it read as
# ground. 24 blocks of fall over 39 of run, distributed 10 / 55 / 35 percent.
for name, course, height, reach, batter in (
        ("brow",     [[-40, -124], [-16, -120], [4, -124]], 43, 9, 0),
        ("midslope", [[-44, -110], [-18, -106], [2, -111]], 33, 5, 30),
        ("toe",      [[-48, -96],  [-20, -92],  [0, -97]],  25, 8, 9)):
    trace = landform.wander(course, drop=4, amplitude=1.0, seed=59 + reach)
    mark = {"id": name, "kind": "line", "r": reach, "tread": 3 if name == "brow" else 2,
            "points": trace, "h": [height] * len(trace)}
    if batter:
        mark["batter"] = batter
    marks.append(mark)

# ── the field the objective stands on ────────────────────────────────────────────────────────────
field_ring = landform.wander_ring([[-40, -48], [-2, -56], [6, -88], [-34, -82]],
                                  drop=4, amplitude=0.9, seed=53)
marks.append({"id": "field", "kind": "area", "bevel": 6,
              "ring": field_ring, "h": [FIELD] * len(field_ring)})

# ── the 20-30 block scale, which is the row the last board had nothing in ────────────────────────
# Talus cones at the re-entrant mouths: every third vertex of the apron trace, pushed out and up.
for index in range(3, len(apron_trace) - 3, 5):
    x, z = apron_trace[index]
    pushes.append({"id": f"cone-{index}", "amount": 4, "falloff": 9, "roughness": 0.55,
                   "crown": 2, "seed": 60 + index,
                   "ring": [[x - 7, z - 5], [x + 4, z - 7], [x + 7, z + 4], [x - 5, z + 7]]})

# Gullies biting back into the pavement edge, negative and shallowing as they climb.
for index in range(4, len(scar_trace) - 4, 7):
    x, z = scar_trace[index]
    for step, (reach, depth) in enumerate(((7, -4), (5, -3), (4, -2))):
        gx, gz = x + 5 * (step + 1), z - 2 * (step + 1)
        pushes.append({"id": f"gully-{index}-{step}", "amount": depth, "falloff": 6,
                       "roughness": 0.7, "seed": 90 + index + step,
                       "ring": [[gx - reach, gz - reach], [gx + reach, gz - reach],
                                [gx + reach, gz + reach], [gx - reach, gz + reach]]})

# Clints and grikes: the pavement's own 5-8 block undulation, which is the octave a global grain
# cannot supply without wrecking the flats the map is played on.
for index in range(0, 9):
    angle = index * 2.399
    cx = 34 + 16 * math.cos(angle) + 0.7 * index
    cz = -78 + 46 * math.sin(angle) - 2 * index
    pushes.append({"id": f"clint-{index}", "amount": 2 if index % 2 else -2, "falloff": 5,
                   "roughness": 0.8, "seed": 120 + index,
                   "ring": [[cx - 5, cz - 4], [cx + 4, cz - 5], [cx + 5, cz + 4], [cx - 4, cz + 5]]})

finish = {
    "authors": ["Opus 5"], "created": "2026-09-05",
    "relief": {"*": {"base": FIELD, "reach": 0, "step": 1, "landform": "hills",
                     "grain": {"amplitude": 2.2, "scale": 20, "seed": 13},
                     "marks": marks, "pushes": pushes}},
    "addShapes": [],
    "themes": {}, "mapTheme": "clints",
    "dressing": {"props": [
        {"id": "beck-water", "kind": "water", "shape": "channel", "level": BECK + 2, "depth": 3,
         "points": beck_trace, "radius": 6},
    ]},
}


def solid(i, d=0): return {"kind": "solid", "id": i, "data": d}
def cell(a, b, size): return {"kind": "cell", "cellSize": size, "palette": [solid(*a), solid(*b)]}
def over(top, soil=solid(3), depth=2):
    return {"kind": "layered", "stack": {"ending": "repeat", "bands": [
        {"material": top, "thickness": 1}, {"material": soil, "thickness": depth}]}}


# The angle mask. Cuts to be re-read off `GET …/incline` once it is built: a board budgeted against
# the 10-30 degree band has a different distribution from one that grades everywhere.
MASK = {"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
    {"material": over(cell((2,), (2,), 15)), "thickness": 22},        # pavement, field, defile
    {"material": over(solid(3, 1)), "thickness": 12},                 # the worn shoulder, 22-33
    {"material": cell((1,), (13,), 7), "thickness": 12},              # talus at repose, 34-45
    {"material": cell((1,), (4,), 9), "thickness": 45}]}}             # the crag, 46+

BEDS = {"kind": "layered", "layers": [
    {"material": solid(1), "thickness": 3}, {"material": solid(1, 5), "thickness": 1},
    {"material": solid(1), "thickness": 4}, {"material": solid(13), "thickness": 1},
    {"material": solid(1, 3), "thickness": 2}, {"material": solid(4), "thickness": 2}]}

finish["themes"] = {
    "clints": {"bedrock": {"relative": False, "value": 1}, "rimEdges": "drop",
               "wallOnTerrainFaces": True,
               "rim": {"material": solid(1, 5), "depth": 1, "enabled": False},
               "surface": {"material": MASK, "depth": 3, "enabled": True},
               "wall": {"kind": "wallRun", "runs": [{"material": BEDS, "width": 6}]},
               "wallEnabled": True, "fill": solid(1, 5)},
}
finish["themeByHeight"] = {}

plan = {
    "plan": 2, "meta": {"name": "Clints Scar"},
    "globals": {"cell": 2, "symmetry": "rot_180", "maxPlayers": 24,
                "surface": FIELD, "observerY": 88},
    "pieces": [
        {"id": "fell",  "role": "spawn", "rect": [-10, -70, 10, 6], "surface": FELL},
        {"id": "west",  "role": "piece", "rect": [-30, -64, 30, 64], "surface": FIELD},
        {"id": "east",  "role": "piece", "rect": [0, -64, 30, 64], "surface": FIELD},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "fell", "at": [10, 6], "facing": "back"}],
        "destroyables": [
            # One goal a side, on the apron under the crag. Its distance from the centre is not a
            # taste: at |spawn| 134 the four goal bands intersect in a single interval, and 69.5
            # blocks along the spawn axis is the middle of it.
            {"id": "dt-scar", "piece": "west", "at": [55, 59], "style": "pillar-3",
             "materials": "obsidian", "float": 4, "name": "The Scar"},
        ],
    },
}

for name, doc in (("plan", plan), ("finish", finish)):
    with open(f"{HERE}/{SLUG}.{name}.json", "w") as handle:
        json.dump(doc, handle, indent=1)

vertices = sum(len(mark.get("points", mark.get("ring", []))) for mark in marks)
print(f"{len(marks)} marks ({vertices} vertices), {len(pushes)} pushes, "
      f"{len(plan['pieces'])} pieces a side")
for mark in marks:
    course = mark.get("points") or mark.get("ring") or []
    if len(course) >= 2:
        runs = [math.dist(course[i], course[i + 1]) for i in range(len(course) - 1)]
        print(f"  {mark['id']:<11} {mark['kind']:<6} {len(course):>3} verts  "
              f"longest segment {max(runs):>5.1f}")
