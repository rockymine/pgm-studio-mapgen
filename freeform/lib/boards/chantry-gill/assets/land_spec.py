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
    "small": {"fbm": {"cell": 9, "octaves": 3, "seed": 1}},
    "big": {"fbm": {"cell": 34, "octaves": 3, "seed": 2}},
    "patch": {"fbm": {"cell": 3, "octaves": 2, "seed": 3}},
    "grain": {"fbm": {"cell": 2, "octaves": 1, "seed": 4}},
    "jag": {"mul": [{"fbm": {"cell": 4, "octaves": 2, "seed": 5}}, 2.5]},
    "ridge-foot": {"line": {"along": "x", "cell": 18, "seed": 6, "amp": 5, "base": 86}},
    "scar-d": dist,
    "plateau": {"add": [TOP, {"mul": ["small", 0.7]},
                        {"mul": [-0.22, {"pow": [{"max": [0, {"sub": [{"abs": {"sub": ["x", 101]}}, 16]}]}, 1.35]}]}]},
}
ground = [
    {"id": "land", "op": "outline", "box": [0, 0, 139, 109]},
    {"id": "fell", "op": "base", "height": 40,
     "terms": [{"tilt": {"dx": 0.03, "dz": 0.06}}, {"gauss": {"at": [40, 80], "r": 30, "rise": 4, "rz": 22, "angle": 25}},
               {"noise": {"field": "small", "rise": 1.0}}, {"noise": {"field": "big", "rise": 2.4}}],
     "note": "the fell: rising south and a little east, a swell south-west, rolling in two sizes"},
    {"id": "scar", "op": "set", "where": {"gt": ["scar-d", -6]},
     "height": {"profile": {"d": "scar-d", "floor": "H", "mode": "lift",
                            "steps": [{"start": {"add": [-1, "jag"]}, "end": {"add": [1.5, "jag"]}, "top": "plateau"}]}},
     "note": "the scar: a step of limestone up to the plateau, its edge ragged"},
    {"id": "back-ridge", "op": "set",
     "height": {"ridge": {"coord": "z", "foot": "ridge-foot", "reach": -22, "crest": 66,
                          "rough": {"mul": ["big", 3]},
                          "spurs": [{"d": {"line_distance": {"pts": [[48, 96], [30, 70], [20, 54]]}}, "top": 50,
                                     "reach": [16, 3]}]}},
     "note": "the ridge along the back, a spur reaching north-west toward the tarn"},
    {"id": "tarn", "op": "crater", "floor": 33, "flat": 3, "slope": 0.45, "melt": 6,
     "areas": [{"polygon": TARN, "rough": {"amp": 0.12, "cell": 5, "seed": 7}}],
     "note": "the tarn's bowl, shelving gently"},
    {"id": "tongue", "op": "level", "mode": "set", "top": 38, "inner": 0.7, "outer": 1.2,
     "areas": [{"polygon": TONGUE, "rough": {"amp": 0.1, "cell": 3, "seed": 8}}],
     "note": "a tongue of land running out into the tarn from its north shore"},
    {"id": "gill", "op": "level", "mode": "cut", "top": 34, "inner": 0.5, "outer": 1.0,
     "areas": [{"line": {"pts": GILL, "width": 11}, "rough": {"amp": 0.15, "cell": 4, "seed": 9}}],
     "note": "the gill: a gorge eight to ten deep"},
    {"id": "beck", "op": "river", "line": GILL, "width": 4, "depth": 2, "water": 2, "bank": 1,
     "note": "the beck down the gill into the tarn"},
    {"id": "tarn-water", "op": "water", "level": 36,
     "where": {"and": [{"lt": ["H", 36]}, {"lt": [{"distance": {"polygon": TARN, "rough": {"amp": 0.12, "cell": 5, "seed": 7}}}, 1.15]}]}},
]
paint = [
    {"block": "SAND", "slope": [None, 26], "height": [None, 38],
     "area": {"polygon": [[0, 0], [40, 0], [40, 24], [0, 24]]}, "noise": {"field": "patch", "lo": -0.35}},
    {"block": ["SAND", 0], "slope": [None, 20], "height": [None, 37], "area": {"polygon": TONGUE}},
    {"block": "GRAVEL", "slope": [None, 30], "area": {"line": {"near": "beck", "width": 8}}, "noise": {"field": "patch", "lo": 0}},
    {"block": ["STONE", 5], "slope": [44, None], "noise": {"field": "patch", "lo": 0.15}},
    {"block": "COBBLE", "slope": [52, None], "noise": {"field": "grain", "lo": 0.55}},
    {"block": ["STONE", 0], "slope": [44, None]},
    {"block": ["DIRT", 1], "slope": [34, 44], "noise": {"field": "patch", "lo": 0.45}},
]
doc = {
    "document": "layers", "version": "draft-1",
    "board": {"name": "Chantry Gill land", "x": [0, 139], "z": [0, 109], "floor": 40, "height": 90, "seed": 3},
    "fields": fields, "ground": ground, "paint": paint,
    "water": {"bed": [{"block": "GRAVEL", "noise": {"field": "patch", "lo": 0.1}}, {"block": "SAND", "noise": {"field": "patch", "lo": -0.3}}, {"block": "CLAY"}]},
    "levels": [
        {"id": "lip", "floor": TOP,
         "ground": [{"id": "lip-outline", "op": "outline",
                     "area": {"polygon": [[84, 56], [96, 55], [110, 56], [118, 58], [118, 72], [84, 72]],
                              "rough": {"amp": 0.07, "cell": 4, "seed": 10}}},
                    {"id": "lip-ground", "op": "set", "height": "plateau"}],
         "paint": paint[3:], "soil": 1,
         "underside": {"taper": [2, 0.25], "rough": 1, "seed": 11, "clear": 3},
         "note": "the scar's lip, the plateau's own ground carried out over its foot"}],
    "carve": [
        {"id": "adit", "op": "tunnel", "mouths": [0], "cover": 3,
         "pts": [[100, 47, 61, 2.0], [101, 46, 68, 2.0], [100, 44, 78, 2.2]],
         "dress": {"seed": 12, "stalagmites": 20, "ores": 30}, "note": "the old adit in the back of the shelter"}],
    "volume": [
        {"id": "brig", "op": "arch", "line": {"pts": [[62, 24], [62, 50]], "spline": False}, "width": 5,
         "deck": [44, 42, 2], "camber": 0, "thick": [2, 10, 2.5], "clear": 3, "top": "GRAVEL", "under": "STONE",
         "rock": "STONE", "note": "the brig: a stone arch carrying the road over the gill"}],
}
json.dump(doc, open(os.path.join(HERE, "land.layers.json"), "w"), indent=1)
