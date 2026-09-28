"""Gypsum Reach — writes opus55-gypsum-reach.plan.json and .finish.json.

A pale desert lane: each team's obsidian monument stands in the open on a low shelf, with a dry wash
sunk in front of it (the way in from below), a mesa standing off its outer flank (the way in from above)
and a pair of stone houses behind it (the way in through). The two halves meet across a 32-block build
zone over void that spans the board's whole width.

Team 0 is the west half (x < 0); rot_180 fans the rest. Plan units are 4-block cells; everything in the
finish is in blocks.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus55-gypsum-reach"
CELL = 4
SURFACE = 20

# --- the plan: a spawn bench and one field a team, the build zone between them -------------------------
plan = {
    "plan": 2,
    "meta": {"name": "Gypsum Reach", "authors": ["Opus 5.5"]},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 16, "surface": SURFACE},
    "pieces": [
        {"id": "spawn", "role": "spawn", "rect": [-31, -3, 5, 6], "surface": 24},
        {"id": "field", "rect": [-26, -12, 22, 24]},
    ],
    "zones": [{"id": "strait", "rect": [-4, -12, 4, 24]}],
    "placements": {
        "spawns": [{"id": "sp", "piece": "spawn", "at": [10, 12], "facing": "right",
                    "footprint": [2, 5, 14, 14]}],
        # field min corner is (-104, -48); the monument at (-66, -16) is 38, 32 blocks in
        "destroyables": [{"id": "mon", "piece": "field", "at": [38, 32], "style": "pillar-3",
                          "name": "Gypsum Monument"}],
    },
}


def ring(cx, cz, rx, rz, n=28, wobble=0.0, lobes=3, phase=0.0):
    out = []
    for k in range(n):
        a = 2 * math.pi * k / n
        f = 1 + wobble * math.cos(lobes * a + phase)
        out.append([round(cx + rx * f * math.cos(a), 1), round(cz + rz * f * math.sin(a), 1)])
    return out


S = lambda i, d=0: {"kind": "solid", "id": i, "data": d}


def depth(top, under, n_top=1, n_under=2):
    return {"kind": "layered", "stack": {"ending": "repeat", "bands": [
        {"material": top, "thickness": n_top}, {"material": under, "thickness": n_under}]}}


# Strata: sandstone beds with a thin hardened-clay bed, following the ground averaged 16 cells either side.
# The last band of a stack claims everything past it, so the cycle is written out bed by bed from 40 below
# the ground to well above the mesa.
BEDS = [(S(24, 0), 3), (S(24, 2), 2), (S(172), 1), (S(24, 0), 2), (S(159, 1), 1)] * 8 + [(S(24, 0), 1)]
STRATA = {"kind": "layered", "axis": "height", "from": -40, "follow": 100, "reach": 16, "beyond": S(24, 0),
          "stack": {"ending": "repeat", "bands": [{"material": m, "thickness": t} for m, t in BEDS]}}

# Flat ground: sand as the ground, sandstone in small patches at one end of the stop list.
SAND = {"kind": "noise", "scale": 2, "seed": 11, "stops": [S(24, 0), S(12), S(12), S(12)]}
SHOULDER = {"kind": "cell", "cellSize": 2, "seed": 12, "palette": [S(24, 0), S(24, 2), S(12)]}

desert = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": S(24)},
    "wallEnabled": True, "wallOnTerrainFaces": True,
    "wall": STRATA, "fill": STRATA,
    "surface": {"enabled": True, "depth": 3, "material": {
        "kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
            {"thickness": 28, "material": depth(SAND, S(24, 0), 1, 2)},
            {"thickness": 17, "material": depth(SHOULDER, S(24, 0), 1, 2)},
            {"thickness": 45, "material": STRATA}]}}},
}

# The monument's shelf and the spawn yard: a floor of four sandstone-family blocks would vanish into the
# ground, so the made floor is the warm path set — granite and polished granite with brick.
PAVE = {"kind": "cell", "cellSize": 2, "seed": 21, "palette": [S(1, 1), S(1, 2), S(45), S(1, 1)]}

finish = {
    "created": "2026-09-28",
    "authors": ["Opus 5.5"],
    "biome": {"kind": "solid", "id": 2},
    "themes": {"desert": desert},
    "mapTheme": "desert",
    "relief": {"team": {
        "base": SURFACE, "reach": 0, "step": 1, "landform": "rolling",
        "marks": [
            # the spawn bench, a little proud of the field
            {"id": "bench", "kind": "area", "h": 24, "bevel": 3,
             "ring": [[-124, -14], [-100, -14], [-100, 14], [-124, 14]]},
            # the spawn door grades down to the field (SP8's own edit)
            {"id": "ramp-spawn-field", "kind": "line", "r": 3, "points": [[-109, 0], [-99, 0]], "h": [24, 20]},
            # the monument's shelf: the ground a defender stands on, pinned and no more
            {"id": "shelf", "kind": "area", "h": 22, "bevel": 3, "ring": ring(-68, -16, 13, 11)},
            # the lip toward the strait, wandering, lower than the field
            {"id": "lip", "kind": "line", "r": 4, "h": [17, 16, 18, 16, 17],
             "points": [[-19, -46], [-20, -24], [-18, 0], [-20, 24], [-19, 46]]},
        ],
        "pushes": [
            # the dry wash in front of the monument: the way in from below
            {"id": "wash", "ring": ring(-40, -12, 7, 19, wobble=0.12, lobes=3, phase=0.5),
             "amount": -6, "falloff": 5, "roughness": 0.35, "crown": 0, "seed": 3},
            # the mesa off the monument's outer flank, centred near the coast: the way in from above
            {"id": "mesa", "ring": ring(-70, -46, 16, 11, wobble=0.1, lobes=4),
             "amount": 13, "falloff": 3, "roughness": 0.4, "crown": 0, "seed": 4},
            # a low swell on the north flank so the far side of the lane is not a table
            {"id": "swell", "ring": ring(-58, 34, 16, 12, wobble=0.15, lobes=3),
             "amount": 4, "falloff": 10, "roughness": 0.3, "crown": 0, "seed": 5},
        ],
    }},
    "roomStyles": {"spawn": "@sb-spawn"},
    "dressing": {
        "styles": {"stonehouse": {"kind": "house", "shell": json.load(open(os.path.join(
            HERE, "..", "..", "tools", "styles", "hw-stonehouse.json")))}},
        "props": [
            # the two houses behind the monument, on its inner side: the way in through
            {"kind": "house", "id": "house-a", "seed": 31, "style": "stonehouse", "front": "posX",
             "wings": [{"corners": [[-86, -4], [-77, 4]]}]},
            {"kind": "house", "id": "house-b", "seed": 32, "style": "stonehouse", "front": "posX",
             "wings": [{"corners": [[-90, 12], [-81, 19]], "spec": {"storeysHigh": 2}}]},
            # paths: spawn door to the monument, and a branch off it to the lip past the wash's north end
            {"kind": "stroke", "id": "path-mon", "seed": 41, "style": "solid", "radius": 1.5,
             "claimsGround": True, "wander": 2, "wanderLength": 14, "pave": PAVE,
             "points": [[-102, 0], [-88, -8], [-74, -14]]},
            {"kind": "stroke", "id": "path-lip", "seed": 42, "style": "solid", "radius": 1.5,
             "claimsGround": True, "wander": 2, "wanderLength": 14, "pave": PAVE,
             "points": [[-88, -8], [-70, -2], [-50, 12], [-34, 16], [-22, 12]]},
        ],
    },
}

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print("wrote", SLUG)
