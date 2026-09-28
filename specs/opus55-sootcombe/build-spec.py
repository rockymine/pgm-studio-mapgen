"""Sootcombe — writes opus55-sootcombe.plan.json and .finish.json.

A capture board on an ash field: a combe of grey slag falling from each team's brick hamlet, standing on a
terrace four blocks over its hub, down to a flat frontline and a flat slag stone in the middle of the build
band. Two wools a team: one at the end of a spur west of the hub behind a bedrock wall, one at the east end
of the terrace behind another.

The arrangement is composed board p12 t2 #21 (`composed-p12-seed21.plan.json`, pinned off GET /api/compose),
taken whole: this spec states its elevation, its paint and its dressing, and nothing about where the pieces
are. Team 0 is the z > 0 half; rot_180 fans the rest.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus55-sootcombe"

plan = json.load(open(os.path.join(HERE, "composed-p12-seed21.plan.json")))
plan["meta"] = {"name": "Sootcombe", "authors": ["Opus 5.5"],
                "notes": "composed p12 t2 seed 21 (walled-4), arrangement unchanged"}

S = lambda i, d=0: {"kind": "solid", "id": i, "data": d}


def depth(top, under, n_top=1, n_under=2):
    return {"kind": "layered", "stack": {"ending": "repeat", "bands": [
        {"material": top, "thickness": n_top}, {"material": under, "thickness": n_under}]}}


def ring(cx, cz, rx, rz, n=28, wobble=0.0, lobes=3, phase=0.0):
    out = []
    for k in range(n):
        a = 2 * math.pi * k / n
        f = 1 + wobble * math.cos(lobes * a + phase)
        out.append([round(cx + rx * f * math.cos(a), 1), round(cz + rz * f * math.sin(a), 1)])
    return out


GREY, BLACK, LGREY = S(159, 7), S(159, 15), S(159, 8)
# The ash: grey stained clay as the ground, black at one end of the stop list and a worn set of coarse
# dirt and dirt at the other, each a patch inside the grey.
WORN = {"kind": "cell", "cellSize": 2, "seed": 7, "palette": [S(3, 1), S(3, 0)]}
ASH = {"kind": "noise", "scale": 2, "seed": 5, "stops": [WORN, GREY, GREY, GREY, BLACK]}
SHOULDER = {"kind": "cell", "cellSize": 2, "seed": 6, "palette": [GREY, S(1, 5), S(1, 6)]}
ROCK = {"kind": "cell", "cellSize": 2, "rise": 2, "seed": 8, "palette": [S(1), S(1, 5), S(1), S(4)]}

ash = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": GREY},
    "wallEnabled": True, "wallOnTerrainFaces": True,
    "wall": ROCK, "fill": ROCK,
    "surface": {"enabled": True, "depth": 3, "material": {
        "kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
            {"thickness": 30, "material": depth(ASH, GREY, 1, 2)},
            {"thickness": 15, "material": depth(SHOULDER, S(1, 5), 1, 2)},
            {"thickness": 45, "material": ROCK}]}}},
}

# A warm path through grey ground: granite and polished granite with brick.
PAVE = {"kind": "cell", "cellSize": 2, "seed": 21, "palette": [S(1, 1), S(1, 2), S(45), S(1, 1)]}


def path(pid, seed, points, wander=2):
    return {"kind": "stroke", "id": pid, "seed": seed, "style": "solid", "radius": 1.5,
            "claimsGround": True, "wander": wander, "wanderLength": 14, "pave": PAVE, "points": points}


finish = {
    "created": "2026-09-28",
    "authors": ["Opus 5.5"],
    "biome": {"kind": "solid", "id": 32},
    "themes": {"ash": ash},
    "mapTheme": "ash",
    "relief": {"team": {
        "base": 10, "reach": 0, "step": 1, "landform": "rolling",
        "marks": [
            # the hamlet's terrace: hub bar, spawn and the east wool's approach, four over the frontline
            {"id": "terrace", "kind": "area", "h": 13,
             "ring": [[-20, 70], [36, 70], [36, 97], [-20, 97]]},
            # the frontline, flat to its edge: ground fought over under fire carries no landform
            {"id": "front", "kind": "area", "h": 9, "ring": [[-17, 20], [17, 20], [17, 33], [-17, 33]]},
            # the west spur falls gently toward its room
            {"id": "spur", "kind": "line", "r": 6, "tread": 4, "points": [[-22, 62], [-42, 62]], "h": [11, 10]},
        ],
        "pushes": [
            # a slag heap off the hub bar's west end, centred over the void so only its flank is on the board
            {"id": "heap", "ring": ring(-28, 80, 10, 8, wobble=0.12, lobes=3), "amount": 7, "falloff": 4,
             "roughness": 0.4, "crown": 0, "seed": 9},
        ],
    }},
    "roomStyles": {"spawn": "@lk-spawn", "wool": "@lk-spawn"},
    "dressing": {
        "props": [
            path("path-front", 51, [[-10, 86], [-10, 72], [-8, 54], [-4, 38], [0, 23]]),
            path("path-wool-a", 52, [[-12, 60], [-24, 62], [-33, 62]], wander=1),
            path("path-wool-b", 53, [[-6, 75], [8, 74], [25, 74]], wander=1),
        ],
    },
}

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print("wrote", SLUG)
