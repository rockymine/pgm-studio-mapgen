"""Writes winding-roads.layout.json — six panels, each an island with one line mark in its relief.

Row 1 is one serpentine stamped three ways, which is the card's whole argument: no tread, a tread, and
a tread with a batter steep enough to expose rock. Row 2 is three other windings, each carrying a fact
the serpentine cannot show — a spiral's pitch against its reach, what happens as passes converge until
they merge, and a hairpin's apex under grain.

No intent and no spawn: the renders read the stored layout through `POST /sketch/columns`, so a card
needs no world and no player.
"""
import json, math, os

PANEL_W, PANEL_D, GAP = 90, 70, 16
COL_X = [-155 + c * (PANEL_W + GAP) for c in range(3)]
ROW_Z = [-80 + r * (PANEL_D + GAP) for r in range(2)]

HIGH, LOW = 36, 6          # the fall the three gaps of this serpentine can carry at a walkable grade
GROUND_TOP = 40            # the island's raw column, before the relief solves it


SKEW = 12                  # degrees off the grid


def turned(points, cx=45, cz=35, degrees=SKEW):
    """The form rotated about the panel's middle. On the grid a winding road's risers land as straight
    bands one cell wide; a few degrees off it and every step is a stair of its own, which is what ground
    cut by a road actually looks like."""
    a = math.radians(degrees)
    cos, sin = math.cos(a), math.sin(a)
    return [[round(cx + (px - cx) * cos - (pz - cz) * sin, 2),
             round(cz + (px - cx) * sin + (pz - cz) * cos, 2)] for px, pz in points]


def serpentine(pitches, limb=66, inset=12, z0=9):
    """Limbs at the stated pitches, so one panel can walk a road through every regime."""
    pts, z, x_a, x_b = [], z0, inset, inset + limb
    for i, pitch in enumerate([0] + list(pitches)):
        z += pitch
        pts += [[x_a, z], [x_b, z]] if i % 2 == 0 else [[x_b, z], [x_a, z]]
    return turned(pts)


def spiral(cx=45, cz=35, r0=34, r1=4, turns=4, per_turn=56):
    n = int(turns * per_turn)
    return [[round(cx + (r0 + (r1 - r0) * k / n) * math.cos(2 * math.pi * turns * k / n), 2),
             round(cz + (r0 + (r1 - r0) * k / n) * math.sin(2 * math.pi * turns * k / n), 2)]
            for k in range(n + 1)]


# The lofted gap is `pitch - 2*tread`, and the grade across it is the fall per limb over that gap.
# At pitch 14 and tread 3 the gap is 8 cells, which puts a 36-block fall on a 56 deg face — rock, not
# road. At pitch 26 the gap is 20 and the same fall grades at 24 deg, which is what a road wants.
EVEN = [26] * 2            # one pitch, the clean case
LADDER = [22, 16, 11, 7]   # 2r is 16 and 2*tread is 6: above, at, inside, and nearly merged


def depth_stack(*bands):
    """A depth stack: one course of the first material over the rest."""
    return {"kind": "layered", "stack": {"ending": "repeat", "bands": [
        {"material": m, "thickness": t} for m, t in bands]}}


SOLID = lambda i, d=0: {"kind": "solid", "id": i, "data": d}

# The ground is finished by its ANGLE, not its height: a thickness on the slope axis is a span of
# degrees, so one stack answers the flat tread, the graded shoulder and the batter's face.
#
# Where the bands cut is the whole decision. A shoulder lofted at one course a cell stands at 45°
# exactly, so a rock band starting there paints every graded shoulder as cliff; starting it at 55°
# leaves the shoulders as scree and keeps rock for the batter, which falls at the angle it states.
MOOR = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": SOLID(1)},
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "wall": SOLID(1),
    "fill": SOLID(1),
    "surface": {"enabled": True, "depth": 3, "material": {
        "kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
            # the road and the fell it crosses
            {"thickness": 15, "material": depth_stack((SOLID(2), 1), (SOLID(3), 2))},
            # the graded shoulder: scree rather than turf, and not yet rock
            {"thickness": 25, "material": depth_stack((SOLID(3, 1), 1), (SOLID(3), 2))},
            # the batter's own face — 23.7% of this board stands at 40 deg or steeper, which is what
            # `incline` answered and what decides the cut. Starting rock at 45 leaves every shoulder
            # lofted at one course a cell reading as turf, because that grade IS 45 deg.
            {"thickness": 50, "material": depth_stack(
                ({"kind": "cell", "cellSize": 11, "palette": [SOLID(1), SOLID(4)]}, 3))},
        ]}}},
}

PANELS = [
    ("serp-plain",   0, 0, serpentine(EVEN),   dict(r=14, tread=None, batter=0)),
    ("serp-tread",   1, 0, serpentine(EVEN),   dict(r=14, tread=3, batter=0)),
    ("serp-batter",  2, 0, serpentine(EVEN),   dict(r=14, tread=3, batter=78)),
    ("spiral",       0, 1, spiral(),           dict(r=6, tread=2, batter=62)),
    ("pitch-ladder", 1, 1, serpentine(LADDER, limb=58, z0=7), dict(r=8, tread=3, batter=0)),
    ("seated",       2, 1, serpentine(EVEN),   dict(r=14, tread=3, batter=0)),
]

shapes, groups, relief = [], [], {}
for name, col, row, local, knobs in PANELS:
    x0, z0 = COL_X[col], ROW_Z[row]
    shapes.append({"id": f"island-{name}", "type": "rectangle", "operation": "add",
                   "floor": 0, "base_height": GROUND_TOP, "theme": "moor",
                   "min_x": x0, "min_z": z0, "max_x": x0 + PANEL_W, "max_z": z0 + PANEL_D})
    groups.append({"id": name, "name": name, "mirrors": False, "shapeIds": [f"island-{name}"]})
    mark = {"id": f"road-{name}", "kind": "line", "h": [HIGH, LOW], "r": knobs["r"],
            "points": [[round(px + x0, 2), round(pz + z0, 2)] for px, pz in local]}
    if knobs["tread"] is not None:
        mark["tread"] = knobs["tread"]
    if knobs["batter"]:
        mark["batter"] = knobs["batter"]
    marks = [mark]
    spec = {"base": LOW, "reach": 0, "step": 1, "marks": marks}
    if name == "seated":
        # Two pads the road crosses: outside a tread the shoulder states its height at falling
        # weight, so where another mark has pinned the ground the two grade into one another.
        marks.append({"id": "upper-fell", "kind": "area", "h": 34, "bevel": 10,
                      "ring": [[x0 + 6, z0 + 2], [x0 + 84, z0 + 2],
                               [x0 + 84, z0 + 24], [x0 + 6, z0 + 24]]})
        marks.append({"id": "lower-holm", "kind": "area", "h": 8, "bevel": 10,
                      "ring": [[x0 + 6, z0 + 48], [x0 + 84, z0 + 48],
                               [x0 + 84, z0 + 68], [x0 + 6, z0 + 68]]})
    if name == "spiral":
        # A haul road ends in a floor rather than at a point: without it the last winding
        # spirals into a column the band never fully claims.
        marks.append({"id": "pit-floor", "kind": "area", "h": LOW, "bevel": 3,
                      "ring": [[round(x0 + 45 + 4 * math.cos(a * math.pi / 4), 2),
                                round(z0 + 35 + 4 * math.sin(a * math.pi / 4), 2)] for a in range(8)]})
    relief[name] = spec

layout = {
    "setup": {"bbox": {"min_x": COL_X[0] - 10, "max_x": COL_X[2] + PANEL_W + 10,
                       "min_z": ROW_Z[0] - 10, "max_z": ROW_Z[1] + PANEL_D + 10},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": {"moor": MOOR},
    "mapTheme": "moor",
    "relief": relief,
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": shapes, "groups": groups}}],
}

out = os.path.join(os.path.dirname(__file__), "winding-roads.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(shapes)} panels, fall {HIGH} -> {LOW} -> {out}")
for name, col, row, local, knobs in PANELS:
    t = knobs["tread"]
    print(f"  {name:13s} {len(local):4d} pts  r={knobs['r']}  tread={t}  batter={knobs['batter']}"
          f"   window 2*tread={0 if t is None else 2*t} .. 2r={2*knobs['r']}")
