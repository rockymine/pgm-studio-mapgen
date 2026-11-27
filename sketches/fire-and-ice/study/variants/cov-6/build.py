"""cov-6 — Firnsattel: the cover over the main building.

A firn saddle lies over the building's back. It comes down off the light-blue north mountain, runs along the map's
west edge as a broad rim at y 64-68, and falls gently east to a shelf at y 59 that meets the checkerboard roof and the
stair roof level. South of the stairwell's roof it slopes down onto the south-west mountain. Every surface is a loft
through ordered lines (one line per z station, points along x), the author's way; the lines were read off a smooth
membrane over the cover's ground plan (design.py beside this file) and are written out here.

Run: python3 -I build.py   (writes variant.json, the two renders, and prints the readings)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import kit  # noqa: E402

# ---------------------------------------------------------------- the lines: (z, [(x, y), ...]) per station
NORTH = [
    [
        (-37, [(1.6, 75.5), (6, 75.5), (10.4, 77)]),
        (-34, [(-4.4, 74.2), (-1.1, 74.3), (2.1, 74.7), (5.4, 75.8)]),
        (-31, [(-10.4, 72.9), (-7, 72.8), (-3.7, 72.7), (-0.3, 72.9), (3, 73.5), (6.4, 75)]),
        (-28, [(-16.4, 71.6), (-13, 71.6), (-9.6, 71.5), (-6.2, 71.3), (-2.8, 71.1), (0.6, 71), (4, 71.4), (7.4, 72.4)]),
        (-25, [(-19, 70.2), (-15.4, 70.3), (-11.8, 70.2), (-8.2, 70), (-4.6, 69.6), (-1, 69), (2.6, 68.4), (6.2, 68.2), (9.8, 67.8), (13.4, 68.9)]),
        (-23, [(-19, 69.5), (-15.6, 69.6), (-12.1, 69.5), (-8.7, 69.2), (-5.2, 68.7), (-1.8, 68), (1.6, 66.8), (5.1, 64.6), (8.5, 63.6), (12, 64.4), (15.4, 67.4)]),
        (-21, [(-19, 68.8), (-15.2, 68.9), (-11.4, 68.7), (-7.6, 68.2), (-3.8, 67.4), (0, 66.2), (3.8, 64), (7.6, 61), (11.4, 58.4)]),
        (-18, [(-19, 67.9), (-15.2, 68), (-11.4, 67.7), (-7.6, 67.1), (-3.8, 66.2), (0, 64.8), (3.8, 62.7), (7.6, 59.8), (11.4, 59)]),
        (-16, [(-19, 67.6), (-15.2, 67.5), (-11.4, 67.1), (-7.6, 66.5), (-3.8, 65.5), (0, 64.1), (3.8, 62.1), (7.6, 59.6), (11.4, 59)]),
    ],
]
FIELD = [
    [
        (-15, [(-19, 67.5), (-15.6, 67.3), (-12.2, 67), (-8.9, 66.5), (-5.5, 65.7), (-2.1, 64.6), (1.3, 63.2), (4.6, 61.4), (8, 59.3), (11.4, 59)]),
        (-12, [(-19, 67), (-15.6, 66.8), (-12.2, 66.4), (-8.9, 65.8), (-5.5, 64.9), (-2.1, 63.9), (1.3, 62.6), (4.6, 61), (8, 59.3), (11.4, 59)]),
        (-9, [(-19, 66.6), (-15.6, 66.4), (-12.2, 65.9), (-8.9, 65.2), (-5.5, 64.4), (-2.1, 63.3), (1.3, 62.1), (4.6, 60.7), (8, 59.2), (11.4, 59)]),
        (-6, [(-19, 66.7), (-15.6, 66.2), (-12.2, 65.6), (-8.9, 64.8), (-5.5, 63.9), (-2.1, 62.9), (1.3, 61.7), (4.6, 60.5), (8, 59.2), (11.4, 59)]),
        (-3, [(-19, 66.9), (-15.6, 66.1), (-12.2, 65.3), (-8.9, 64.5), (-5.5, 63.6), (-2.1, 62.6), (1.3, 61.5), (4.6, 60.4), (8, 59.2), (11.4, 59)]),
        (0, [(-19, 67.2), (-15.6, 66), (-12.2, 65.1), (-8.9, 64.2), (-5.5, 63.3), (-2.1, 62.3), (1.3, 61.3), (4.6, 60.2), (8, 59.2), (11.4, 59)]),
        (3, [(-19, 67.1), (-15.6, 65.8), (-12.2, 64.8), (-8.9, 63.9), (-5.5, 63), (-2.1, 62.1), (1.3, 61.2), (4.6, 60.2), (8, 59.1), (11.4, 59)]),
        (6, [(-19, 66.4), (-15.6, 65.4), (-12.2, 64.6), (-8.9, 63.7), (-5.5, 62.8), (-2.1, 61.9), (1.3, 61), (4.6, 60.1), (8, 59.1), (11.4, 59)]),
        (9, [(-19, 65.6), (-15.6, 65), (-12.2, 64.3), (-8.9, 63.5), (-5.5, 62.6), (-2.1, 61.8), (1.3, 60.9), (4.6, 60), (8, 59.1), (11.4, 59)]),
        (12, [(-19, 65), (-15.6, 64.7), (-12.2, 64), (-8.9, 63.2), (-5.5, 62.4), (-2.1, 61.6), (1.3, 60.8), (4.6, 60), (8, 59.1), (11.4, 59)]),
        (15, [(-19, 65.2), (-15.6, 64.6), (-12.2, 63.8), (-8.9, 63), (-5.5, 62.3), (-2.1, 61.5), (1.3, 60.7), (4.6, 59.9), (8, 59.1), (11.4, 59)]),
        (18, [(-19, 65.5), (-15.6, 64.5), (-12.2, 63.6), (-8.9, 62.8), (-5.5, 62.1), (-2.1, 61.4), (1.3, 60.6), (4.6, 59.9), (8, 59.1), (11.4, 59)]),
        (20, [(-19, 65.7), (-15.6, 64.4), (-12.2, 63.5), (-8.9, 62.7), (-5.5, 61.9), (-2.1, 61.3), (1.3, 60.6), (4.6, 60), (8, 59.1), (11.4, 59)]),
    ],
    [
        (21, [(-19, 65.8), (-15.7, 64.4), (-12.4, 63.4), (-9.1, 62.6), (-5.8, 61.9), (-2.5, 61.3), (0.8, 60.6), (4.1, 60.1), (7.4, 59.7)]),
        (24, [(-19, 65.2), (-15.7, 64), (-12.4, 63.1), (-9.1, 62.3), (-5.8, 61.7), (-2.5, 61.1), (0.8, 60.5), (4.1, 60), (7.4, 59.8)]),
        (27, [(-19, 64.3), (-15.7, 63.4), (-12.4, 62.6), (-9.1, 62), (-5.8, 61.4), (-2.5, 60.9), (0.8, 60.3), (4.1, 59.7), (7.4, 59.4)]),
        (30, [(-19, 63.5), (-15.7, 62.7), (-12.4, 62), (-9.1, 61.5), (-5.8, 61.1), (-2.5, 60.7), (0.8, 60.2), (4.1, 59.2), (7.4, 59)]),
        (33, [(-19, 62.7), (-15.7, 61.9), (-12.4, 61.2), (-9.1, 60.8), (-5.8, 60.7), (-2.5, 60.5), (0.8, 60.4), (4.1, 60.3), (7.4, 60.3)]),
        (36, [(-19, 62.2), (-15.7, 61), (-12.4, 60.2), (-9.1, 60), (-5.8, 60.3), (-2.5, 60.4), (0.8, 60.4), (4.1, 60.3), (7.4, 60.3)]),
        (39, [(-19, 61.5), (-15.7, 59.8), (-12.4, 58.7), (-9.1, 58.4), (-5.8, 60.2), (-2.5, 60.3), (0.8, 60.3), (4.1, 60.3), (7.4, 60.3)]),
        (41, [(-19, 60.2), (-15.7, 58.6), (-12.4, 57.5), (-9.1, 56.5), (-5.8, 59.8), (-2.5, 60.3), (0.8, 60.3), (4.1, 60.3), (7.4, 60.3)]),
    ],
]
SOUTH = [
    [
        (41, [(-19, 60.2), (-14.9, 58.3), (-10.7, 57), (-6.6, 57.1)]),
        (44, [(-19, 57.8), (-14.9, 56.4), (-10.7, 54.9), (-6.6, 52.5)]),
        (47, [(-16.4, 54.7), (-13.1, 54.2), (-9.9, 53.2), (-6.6, 51.5)]),
        (49, [(-14.4, 53.6), (-10.5, 52.6), (-6.6, 52.7)]),
    ],
]
SLOTS = [
    [
        (-10, [(11.6, 59), (20.4, 59)]),
        (-8, [(11.6, 59), (20.4, 59)]),
    ],
    [
        (5, [(11.6, 59), (20.4, 59)]),
        (7, [(11.6, 59), (20.4, 59)]),
    ],
]
RIBS = [
    [
        (-10, [(20.6, 60), (25.4, 60)]),
        (-8, [(20.6, 60), (25.4, 60)]),
    ],
    [
        (5, [(20.6, 60), (25.4, 60)]),
        (7, [(20.6, 60), (25.4, 60)]),
    ],
]

def lofts(stations):
    return [[[(x, y, z) for x, y in pts] for z, pts in loft] for loft in stations]


# ---------------------------------------------------------------- the ground plan the blocks are clipped to
WEST = -19
old = kit.existing()
roof = {(x, z) for (x, y, z), (n, g) in old.items() if n == "Hellgrau und Ton" and y >= kit.FLAT_ROOF}
P = kit.PENTHOUSE
house = {(x, z) for x in range(P[0], P[1] + 1) for z in range(P[2], P[3] + 1)}
ground = {(x, z) for (x, y, z), (n, g) in old.items() if g == "Gelände"}
_labels = json.load(open(os.path.join(os.path.dirname(HERE), "..", "labels", "labels.json")))["labels"]
air = {(l["cells"][i], l["cells"][i + 1], l["cells"][i + 2]) for l in _labels for i in range(0, len(l["cells"]), 3)}


def in_plan(x, z):
    """The cover's ground plan: west of the roof and the penthouse, from the map's west edge (x -19) to the north
    mountain's flank and onto the south-west mountain's rim. The roof's two open slots (z -10..-8 and 5..7) and the stair roof west of the penthouse
    (x -6..7, z 32..40) are in it."""
    north = -27 - (x - WEST) * 11 / 23 if x <= 4 else -38
    south = 44 + (x - WEST) if x <= -14 else 49 + (x + 14) / 21
    if not (north - 1e-9 <= z <= south + 1e-9 and WEST <= x <= 25 and z <= 49): return False
    if ((x, z) in roof and not (x <= 7 and 32 <= z <= 40)) or (x, z) in house: return False
    if (x, z) in ground and z < 41: return False
    if z >= 42 and x >= -6: return False      # the south stair's two exits keep the author's ground in front
    if z <= -23 and x > 16: return False
    if x >= 12 and not (-10 <= z <= -8 or 5 <= z <= 7 or z <= -23): return False
    return True


def blocks_of(stations):
    out = set()
    for loft in lofts(stations):
        out |= {b for b in kit.loft_blocks(loft, thickness=2) if b not in old and b not in air and in_plan(b[0], b[2])}
    return out


SPEC = [
    ("Firnsattel Nord", 3, NORTH, "Der Sattel vom Nordberg herab: schließt bündig an die hellblaue Flanke (y 66–77) an und "
     "fällt nach Süden zur Dachterrasse ab."),
    ("Firnfeld", 4, FIELD, "Das sanfte Feld über dem Rücken des Gebäudes: vom Rand an der Westkante (y 64–68) "
     "gleichmäßig hinab zur Terrasse auf y 59, bündig mit dem Schachbrettdach und liegt auf y 60 über dem Dach der Südtreppe (x −6…7, z 32…41)."),
    ("Südhang", 3, SOUTH, "Westlich der Südtreppe (x −19…−7) hinab auf den hellblauen Südwestberg. Vor den beiden "
     "Ausgängen der Südtreppe (x −6…7, z 41; x 8–15, z 43–47) bleibt der Berg des Autors, der ihre Schwellen trifft."),
    ("Dachspalten", 8, SLOTS + RIBS, "Die zwei offenen Spalten im Schachbrettdach (z −10…−8 und 5…7) auf Dachhöhe y 59 "
     "geschlossen; über den Steinrippen x 21–25 auf y 60, wie die Rippen x 26–31 des Autors."),
]
pieces, seen = [], set()
for name, wool, stations, note in SPEC:
    b = blocks_of(stations) - seen
    seen |= b
    pieces.append({"name": name, "note": note, "wool": wool, "lofts": lofts(stations), "blocks": b})

if __name__ == "__main__":
    path = kit.write("cov-6", "cover", "Firnsattel über dem Bunker",
                     "Ein Firnsattel kommt vom Nordberg herab, zieht als breiter Rand an der Westkante entlang und "
                     "legt sich über den ganzen Rücken des Gebäudes. Zur Front hin läuft er flach auf einer Terrasse "
                     "aus, die bündig ins Schachbrettdach übergeht; im Süden gleitet er auf den Südwestberg. Wer aufs "
                     "Dach kommt, steht auf einer durchgehenden Ebene auf y 59, hinter der der Firn sanft ansteigt.",
                     pieces, absolute=False)
    cover = set().union(*(p["blocks"] for p in pieces))
    for p in pieces:
        print(p["name"], p["wool"], "lofts", len(p["lofts"]), "lines", sum(len(l) for l in p["lofts"]),
              "points", sum(len(line) for l in p["lofts"] for line in l), "blocks", len(p["blocks"]))
    print("checks", kit.checks(cover, full=False, region=[]))
    print("exposed", kit.exposed(cover))
    print("cover_rules", kit.cover_rules(cover))
    top = kit.tops(cover)
    for p in pieces:
        area = len(kit.tops(p["blocks"]))
        pts = sum(len(line) for l in p["lofts"] for line in l)
        print(p["name"], "surface columns", area, "points per 100", round(100 * pts / area, 1))
    total = sum(len(line) for p in pieces for l in p["lofts"] for line in l)
    print("all", len(top), "columns", round(100 * total / len(top), 1), "points per 100")
    colours = {b: p["wool"] for p in pieces for b in p["blocks"]}
    kit.render(colours, os.path.join(HERE, "render_q0.png"), q=0, scale=3, box=(-30, 70, 0, 100, -60, 70), full=False)
    kit.render(colours, os.path.join(HERE, "render_q2.png"), q=2, scale=3, box=(-30, 70, 0, 100, -60, 70), full=False)
    print(path)
