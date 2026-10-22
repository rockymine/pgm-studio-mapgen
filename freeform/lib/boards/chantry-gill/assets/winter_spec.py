"""Write winter.layers.json: the land sheet put into winter with smooth snow, three ways, side by side in strips so
the smoothness can be compared on the same ground.

    x   0 -  45   smoothness 2, added 0.2   snow that keeps the ground's every step
    x  46 -  92   smoothness 6, added 0.4   the tool's default
    x  93 - 139   smoothness 10, added 0.6  a deep, soft blanket

Snow falls on grass, soil, scree, sand and leaves, never on the rock, so the faces stand dark out of it; at a
face's foot the drift is capped at four blocks.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
doc = json.load(open(os.path.join(HERE, "land.layers.json")))
doc["board"]["name"] = "Chantry Gill in winter"
doc["board"]["biome"] = 12                                          # ice plains: grass and leaves tinted cold
ON = ["GRASS", "DIRT", "GRAVEL", "SAND", "LEAVES"]                  # the mask, as //ss 7 grass: rock stays bare
doc["snow"] = [
    {"id": f"snow-{n}", "smoothness": sm, "added": ad, "on": ON, "max_depth": 4, "jitter": 0.3, "jitter_cell": 6, "seed": 30 + n,
     "where": {"and": [{"ge": ["x", x0]}, {"le": ["x", x1]}]}}
    for n, (x0, x1, sm, ad) in enumerate(((0, 45, 2, 0.2), (46, 92, 6, 0.4), (93, 139, 10, 0.6)))]
json.dump(doc, open(os.path.join(HERE, "winter.layers.json"), "w"), indent=1)
