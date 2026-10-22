"""Write land.layers.json: the ground the board stands on, before anything is built on it.

    the fell     rising south to a ridge with spurs reaching north; two sizes of noise, tilted on both axes
    the scar     a limestone step twelve high across the fell, its edge ragged; past it a plateau
    the lip      a second ground at the plateau's own height, resting on it and reaching five blocks out over
                 the scar's foot: the rock shelter under it, and the old adit opening in its back wall
    the gill     a gorge cut through the strand, its beck running west into the tarn
    the tarn     an outline no hand would draw, a beach on its open north shore, rock where the fell comes down
                 to it on the south, a tongue of land running out into it
    the brig     a stone arch over the gill where the road crosses
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SCAR = [[60, 70], [80, 63], [100, 60], [120, 63], [139, 58]]        # the foot of the scar, west to east
TOP = 58                                                              # the plateau behind it
GILL = [[139, 40], [112, 36], [88, 41], [62, 37], [40, 34], [22, 30]]
TARN = [[4, 18], [14, 12], [26, 15], [34, 22], [32, 33], [24, 40], [10, 41], [2, 32]]
TONGUE = [[22, 12], [26, 13], [24, 24], [20, 26], [19, 18]]
dist = {"sub": ["z", {"line_z": {"pts": SCAR}}]}                       # blocks south of the scar's foot

fields = {
    "small": {"fbm": {"cell": 16, "octaves": 2, "seed": 1}},
    "big": {"fbm": {"cell": 34, "octaves": 3, "seed": 2}},
    "patch": {"fbm": {"cell": 3, "octaves": 2, "seed": 3}},
    "crag": {"ridged": {"cell": 7, "octaves": 2, "seed": 16}},
    "grain": {"fbm": {"cell": 2, "octaves": 1, "seed": 4}},
    "jag": {"mul": [{"fbm": {"cell": 4, "octaves": 2, "seed": 5}}, 2.5]},
    "ridge-foot": {"line": {"along": "x", "cell": 18, "seed": 6, "amp": 5, "base": 86}},
    "scar-d": dist,
    "fade": {"mul": [{"smoothstep": [64, 88, "x"]}, {"sub": [1, {"smoothstep": [116, 139, "x"]}]}]},
    "reach": {"line": {"along": "x", "cell": 14, "seed": 13, "amp": 2.2, "base": 4, "clip": [1, 6]}},
    "reach-in": {"mul": ["reach", {"smoothstep": [0.25, 0.9, "fade"]}]},
    "plateau": {"add": [TOP, {"mul": ["small", 0.6]}, {"mul": [0.1, {"sub": ["x", 100]}]},
                        {"mul": [-0.22, {"pow": [{"max": [0, {"sub": [{"abs": {"sub": ["x", 101]}}, 16]}]}, 1.35]}]}]},
}
ground = [
    {"id": "land", "op": "outline", "box": [0, 0, 139, 109]},
    {"id": "fell", "op": "base", "height": 40,
     "terms": [{"tilt": {"dx": 0.03, "dz": 0.06}}, {"gauss": {"at": [40, 80], "r": 30, "rise": 4, "rz": 22, "angle": 25}},
               {"noise": {"field": "big", "rise": 2.0}}],
     "note": "the fell: rising south and a little east, a swell south-west, rolling in two sizes"},
    {"id": "scar", "op": "set", "where": {"gt": ["scar-d", -6]},
     "height": {"profile": {"d": "scar-d", "floor": "H", "mode": "lift",
                            "steps": [{"start": {"add": [-1, "jag"]}, "end": {"add": [1.5, "jag"]},
                                       "top": {"add": ["H", {"mul": ["fade", {"max": [0, {"sub": ["plateau", "H"]}]}]}]}}]}},
     "note": "the scar: a step of limestone up to the plateau, its edge ragged, dying into the fell at both ends"},
    {"id": "back-ridge", "op": "set",
     "height": {"ridge": {"coord": "z", "foot": "ridge-foot", "reach": -22, "crest": 66,
                          "rough": {"mul": ["big", 3]},
                          "spurs": [{"d": {"line_distance": {"pts": [[48, 96], [30, 70], [20, 54]]}}, "top": 50,
                                     "reach": [16, 3]}]}},
     "note": "the ridge along the back, a spur reaching north-west toward the tarn"},
    {"id": "crags", "op": "noise", "mode": "lift", "field": "crag", "rise": 4,
     "areas": [{"polygon": [[0, 84], [139, 80], [139, 106], [0, 106]]},
               {"line": {"pts": [[48, 96], [30, 70], [20, 54]], "width": 10}}],
     "note": "rock breaking out of the ridge's flank and the spur in ribs"},
    {"id": "tarn", "op": "crater", "floor": 33, "flat": 3, "slope": 0.45, "melt": 6,
     "areas": [{"polygon": TARN, "rough": {"amp": 0.12, "cell": 5, "seed": 7}}],
     "note": "the tarn's bowl, shelving gently"},
    {"id": "tongue", "op": "level", "mode": "set", "top": 37, "inner": 0.7, "outer": 1.2,
     "areas": [{"polygon": TONGUE, "rough": {"amp": 0.1, "cell": 3, "seed": 8}}],
     "note": "a tongue of land running out into the tarn from its north shore"},
    {"id": "beach-side", "op": "level", "mode": "cut", "top": 37, "inner": 0.45, "outer": 1.7,
     "areas": [{"ellipse": {"at": [16, 8], "rx": 22, "rz": 12}, "rough": {"amp": 0.1, "cell": 6, "seed": 14}}],
     "note": "the fell let down gently to the tarn's north shore, where the beach is"},
    {"id": "gill", "op": "level", "mode": "cut", "top": 34, "inner": 0.5, "outer": 1.0,
     "areas": [{"line": {"pts": GILL, "width": 11}, "rough": {"amp": 0.15, "cell": 4, "seed": 9}}],
     "note": "the gill: a gorge eight to ten deep"},
    {"id": "bay", "op": "level", "mode": "cut", "top": 37, "inner": 0.3, "outer": 2.0,
     "areas": [{"ellipse": {"at": [100, 47], "rx": 12, "rz": 8, "angle": -10}}],
     "note": "a bay in the gill's south side, where its wall stands back and the ground comes down gently"},
    {"id": "beck", "op": "river", "line": GILL, "width": 4, "depth": 2, "water": 2, "bank": 1,
     "note": "the beck down the gill into the tarn"},
    {"id": "tarn-water", "op": "water", "level": 36,
     "where": {"and": [{"lt": ["H", 36]}, {"lt": [{"distance": {"polygon": TARN, "rough": {"amp": 0.12, "cell": 5, "seed": 7}}}, 1.15]}]}},
]
paint = [
    {"block": "SAND", "slope": [None, 30], "height": [None, 37],
     "area": {"polygon": TARN, "plus": -0.12}, "note": "the beach: every gentle cell a block over the water"},
    {"block": "SAND", "slope": [None, 24], "height": [None, 38],
     "area": {"polygon": TARN, "plus": -0.08}, "noise": {"field": "patch", "lo": 0.1},
     "note": "and ragged a block higher, so its edge is not a contour"},
    {"block": "GRAVEL", "slope": [None, 30], "area": {"line": {"near": "beck", "width": 8}}, "noise": {"field": "patch", "lo": 0}},
    {"block": ["STONE", 5], "slope": [38, None], "noise": {"field": "patch", "lo": 0.15}},
    {"block": "COBBLE", "slope": [46, None], "noise": {"field": "grain", "lo": 0.6}},
    {"block": "GRAVEL", "slope": [38, 48], "noise": {"field": "patch", "lo": 0.35}},
    {"block": ["STONE", 0], "slope": [38, None]},
]
doc = {
    "document": "layers", "version": "draft-1",
    "board": {"name": "Chantry Gill land", "x": [0, 139], "z": [0, 109], "floor": 40, "height": 90, "seed": 3},
    "fields": fields, "ground": ground, "paint": paint,
    "lay": {"soil": [[30, 3], [38, 1]], "ledges": False},
    "water": {"bed": [{"block": "GRAVEL", "noise": {"field": "patch", "lo": 0.1}}, {"block": "SAND", "noise": {"field": "patch", "lo": -0.3}}, {"block": "CLAY"}]},
    "levels": [
        {"id": "brow", "floor": TOP,
         "ground": [{"id": "brow-outline", "op": "outline",
                     "where": {"and": [{"gt": ["scar-d", {"neg": "reach-in"}]}, {"lt": ["scar-d", 3]},
                                       {"gt": ["fade", 0.25]}]}},
                    {"id": "brow-ground", "op": "set", "height": "plateau"}],
         "paint": [{"block": ["STONE", 5], "noise": {"field": "patch", "lo": 0.2}}, {"block": ["STONE", 0]}], "soil": 0,
         "underside": {"bottom": {"sub": ["plateau", {"add": [2, {"mul": [2.0, {"add": ["reach-in", "scar-d"]}]}]}]},
                       "clear": 2},
         "note": "the scar's brow: its face leaning out over its foot, a block out for every two up"}],
    "carve": [
        {"id": "adit", "op": "tunnel", "mouths": [0], "cover": 3,
         "pts": [[100, 47, 61, 2.0], [101, 46, 68, 2.0], [100, 44, 78, 2.2]],
         "dress": {"seed": 12, "stalagmites": 20, "ores": 30}, "note": "the old adit in the back of the shelter"}],
    "volume": [
        {"id": "brig", "op": "arch", "line": {"pts": [[62, 24], [62, 50]], "spline": False}, "width": 5,
         "deck": [44, 42, 2], "camber": 0, "thick": [2, 10, 2.5], "clear": 3, "top": "GRAVEL", "under": "STONE",
         "rock": "STONE", "note": "the brig: a stone arch carrying the road over the gill"}],
}

# where the ground is, read before the brig and the adit are placed on it
import sys                                                                         # noqa: E402
sys.path.insert(0, os.path.join(HERE, "..", "..", ".."))
from pgmvox.document import layers                                                 # noqa: E402
c, _ = layers.ground({k: v for k, v in doc.items() if k not in ("levels", "carve", "volume")})
H = c.H
at = lambda x, z: float(H[x, z])                                                    # noqa: E731
BX = 62
col = [at(BX, z) for z in range(110)]
deep = [z for z in range(16, 60) if col[z] < 40]
rim_n, rim_s = max(col[min(deep) - 8:min(deep)]), max(col[max(deep) + 1:max(deep) + 9])
bank = round(max(rim_n, rim_s))
zn = max(z for z in range(min(deep) - 8, min(deep)) if col[z] >= rim_n - 0.6)       # where each rim begins to fall
zs = min(z for z in range(max(deep) + 1, max(deep) + 9) if col[z] >= rim_s - 0.6)
doc["volume"][0]["line"]["pts"] = [[BX, zn - 1], [BX, zs + 1]]
doc["volume"][0]["deck"] = [bank + 1, bank, 2]
doc["volume"][0]["note"] = f"the brig: from bank to bank of the gill, z {zn} to {zs}, its deck at the banks' height"
AX = 104
(x0, z0), (x1, z1) = next((a, b) for a, b in zip(SCAR, SCAR[1:]) if a[0] <= AX <= b[0])
foot = round(z0 + (z1 - z0) * (AX - x0) / (x1 - x0))
mz = foot - 3
fy = round(at(AX, mz)) + 1
doc["carve"][0]["pts"] = [[AX, fy, mz - 3, 1.5], [AX, fy, foot - 1, 4.4], [AX - 1, fy, foot + 3, 4.6], [AX + 1, fy, foot + 7, 3.4],
                          [AX, fy - 1, foot + 12, 2.0], [AX - 1, fy - 3, foot + 22, 2.2]]
doc["carve"][0]["dress"] = {"seed": 12, "stalagmites": 60, "ores": 40, "stalactites": 0.08}
doc["carve"][0]["note"] = "a shelter worn into the foot of the leaning face, nine wide, the old adit running on from its back"
doc["build"] = [{"id": "erratics", "op": "boulders", "seed": 17, "sink": 0.3, "rough": 0.5,
                 "at": [[30, 44, 3.5, {"rz": 2.6, "angle": 20}], [52, 18, 2.5], [86, 24, 4, {"rz": 3, "angle": -30, "height": 3.5}],
                        [120, 18, 2.2], [70, 74, 3, {"angle": 60}], [36, 50, 1.8], [128, 70, 3.2, {"rz": 2.2}],
                        [10, 88, 2.6]],
                 "note": "erratics the ice left on the fell, one rock each, a few of them big"}]
json.dump(doc, open(os.path.join(HERE, "land.layers.json"), "w"), indent=1)
print(f"brig over z {zn}-{zs}, banks {col[zn]:.0f} and {col[zs]:.0f}; adit mouth at ({AX}, {fy}, {mz})")
