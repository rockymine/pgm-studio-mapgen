"""What every technique card's board is made of: a grid of panels, one island each, and the ground they
are finished with.

A card is a row or two of small islands standing side by side, each carrying one instrument set one way,
so the difference between two panels is the one knob between them. Nothing here is a map: there is no
intent, no spawn and no objective, because the renders read the stored layout through
`POST /api/map/{slug}/sketch/columns` and that needs neither.
"""
import math


def grid(columns, rows, panel_w=96, panel_d=76, gap=14):
    """The x of each column and the z of each row, centred on the origin."""
    span_x, span_z = columns * panel_w + (columns - 1) * gap, rows * panel_d + (rows - 1) * gap
    return ([round(-span_x / 2 + c * (panel_w + gap)) for c in range(columns)],
            [round(-span_z / 2 + r * (panel_d + gap)) for r in range(rows)])


def turned(points, cx, cz, degrees=12):
    """The form rotated about a point. On the grid a relief's risers land as straight bands one cell wide;
    a few degrees off it and every step is a stair of its own, which is what cut ground looks like."""
    a = math.radians(degrees)
    cos, sin = math.cos(a), math.sin(a)
    return [[round(cx + (px - cx) * cos - (pz - cz) * sin, 2),
             round(cz + (px - cx) * sin + (pz - cz) * cos, 2)] for px, pz in points]


def rect_ring(cx, cz, width, depth):
    """A rectangular ring, clockwise from its north-west corner."""
    hw, hd = width / 2, depth / 2
    return [[cx - hw, cz - hd], [cx + hw, cz - hd], [cx + hw, cz + hd], [cx - hw, cz + hd]]


def round_ring(cx, cz, radius, points=32, squash=1.0):
    return [[round(cx + radius * math.cos(2 * math.pi * k / points), 2),
             round(cz + radius * squash * math.sin(2 * math.pi * k / points), 2)] for k in range(points)]


def lobed_ring(cx, cz, radius, lobes=5, depth=0.22, points=48, phase=0.0):
    """A round ring pulled in and out as it goes round, which is what a landform's outline actually is."""
    return [[round(cx + radius * (1 + depth * math.cos(lobes * (2 * math.pi * k / points + phase)))
                   * math.cos(2 * math.pi * k / points), 2),
             round(cz + radius * (1 + depth * math.cos(lobes * (2 * math.pi * k / points + phase)))
                   * math.sin(2 * math.pi * k / points), 2)] for k in range(points)]


SOLID = lambda block, data=0: {"kind": "solid", "id": block, "data": data}


def depth_stack(*bands):
    """A depth stack: one course of the first material over the rest."""
    return {"kind": "layered", "stack": {"ending": "repeat", "bands": [
        {"material": m, "thickness": t} for m, t in bands]}}


# The ground is finished by its ANGLE, not its height: a thickness on the slope axis is a span of degrees,
# so one stack answers a flat top, a graded skirt and a bank steep enough to be rock.
#
# Where the bands cut is the whole decision. A grade of one course a cell stands at 45 deg exactly, so a
# rock band starting there paints every gentle shoulder as cliff; starting it at 40 leaves a skirt under
# 0.84 blocks a cell as scree and keeps rock for what is genuinely a face.
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
            {"thickness": 15, "material": depth_stack((SOLID(2), 1), (SOLID(3), 2))},
            {"thickness": 25, "material": depth_stack((SOLID(3, 1), 1), (SOLID(3), 2))},
            {"thickness": 50, "material": depth_stack(
                ({"kind": "cell", "cellSize": 11, "palette": [SOLID(1), SOLID(4)]}, 3))},
        ]}}},
}
