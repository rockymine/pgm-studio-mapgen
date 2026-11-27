"""cov-2 -- the mountain closes over the back of the bunker.

The main building is a set of hollow boxes, stair tubes and roof plates hung in the air: hall (x 0..29, z -9..19,
y 23..39), stair tubes and back rooms (x -15..0, z 18..31, y 18..55), the upper room (x -1..14, z 21..38, y 47..55),
and over them the checkerboard plates at y 59 (x 12..32, z -22..31, plus the L x -6..29, z 32..40). Everything west
of the plates is meant to sit inside the mountain. This cover is one skin over all of it, at grade with the plates:

    Dachschulter (yellow)    a flatter shelf along the plates' west edge, 58 at the plate (one below the slab),
                             rising to ~60 eight blocks west: the roof plaza runs on into the hill.
    Bergruecken (lightblue)  from the shelf up to a ridge at x ~ -9 (64..67), joined in the north to the north
                             mountain's open west face (x 4..16, y 67..78), falling in the south-west onto the
                             south mountain's edge (y 52..53).

Lines run west -> east at constant z, ordered north -> south; each loft is the ruled mesh between consecutive lines.
Nothing is placed east of the plate edge, so the facade, the core, the corridors, the windows, the plates, the black
roof and the antenna stay as built.
"""
import os
import sys

S = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(S, "variants"))
import kit  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def line(z, pts):
    """A west->east line at depth z from (x, y) pairs."""
    return [(float(x), float(y), float(z)) for x, y in pts]


# ---------------------------------------------------------------- Bergruecken, north: up to the north mountain
# east ends sit one block off the north mountain's west face, at its height there
north_lines = [
    line(-44, [(-5, 73.6), (-1, 75.8), (5, 77.5)]),
    line(-40, [(-10, 71.4), (-5, 73.6), (-1, 75.5), (4, 76.8)]),
    line(-35, [(-13, 69.6), (-8, 72.0), (-1, 74.0), (5, 75.6)]),
    line(-31, [(-14.5, 68.2), (-8, 70.6), (0, 72.6), (6, 74.6)]),
    line(-28, [(-15, 67.4), (-8, 69.6), (0, 70.6), (7, 72.6)]),
    line(-26, [(-15, 67.6), (-8, 68.8), (0, 69.0), (6, 68.6), (11, 68.6), (12, 69.2)]),
    line(-25, [(-15, 67.3), (-8, 68.3), (0, 67.8), (6, 66.6), (11, 66.0), (13, 67.6)]),
    line(-24, [(-15, 67.0), (-8, 67.8), (0, 66.4), (6, 64.6), (11, 63.6), (14, 66.0)]),
    line(-23, [(-15, 66.8), (-8, 67.4), (0, 65.2), (6, 62.6), (11, 61.2), (13, 62.4), (15, 64.0)]),
    line(-22, [(-15, 66.5), (-8, 67.0), (0, 64.0), (3, 62.6), (7, 60.6), (11, 59.0)]),
]

# ---------------------------------------------------------------- the main band beside the plates (z -22..31)
# (x, y) of the west part (blue) and of the shelf (yellow); they share the point at x = 3
band = {
    -22: ([(-15, 66.5), (-8, 67.0), (0, 64.0), (3, 62.6)], [(3, 62.6), (7, 60.6), (11, 59.0)]),
    -18: ([(-14, 64.6), (-9, 66.8), (-2, 63.4), (3, 61.0)], [(3, 61.0), (7, 59.4), (11, 58.2)]),
    -12: ([(-15, 63.8), (-10, 66.2), (-2, 62.8), (3, 60.2)], [(3, 60.2), (7, 58.9), (11, 58.0)]),
    -5: ([(-13.5, 63.4), (-10, 65.4), (-2, 62.2), (3, 59.8)], [(3, 59.8), (7, 58.7), (11, 58.0)]),
    2: ([(-15, 63.6), (-9, 66.4), (-3, 62.6), (3, 59.8)], [(3, 59.8), (7, 58.7), (11, 58.0)]),
    9: ([(-14, 63.6), (-10, 65.6), (-3, 62.0), (3, 59.6)], [(3, 59.6), (7, 58.6), (11, 58.0)]),
    16: ([(-15.2, 61.8), (-10, 64.2), (-3, 61.2), (3, 59.2)], [(3, 59.2), (7, 58.4), (11, 58.0)]),
    24: ([(-15.2, 61.0), (-10, 62.8), (-3, 60.2), (3, 58.8)], [(3, 58.8), (7, 58.2), (11, 58.0)]),
    31: ([(-15.2, 60.2), (-10, 61.2), (-6, 59.4), (-1, 58.6), (3, 58.4)], [(3, 58.4), (7, 58.0), (11, 58.0)]),
}
band_west = [line(z, w) for z, (w, e) in sorted(band.items())]
band_shelf = [line(z, e) for z, (w, e) in sorted(band.items())]

# ---------------------------------------------------------------- south-west: past the L plate onto the south mountain
# the last line runs one block north-west of the south mountain's edge (x -15 z 50 ... x -7 z 42), at its height
south_lines = [
    line(31, [(-15.2, 60.2), (-10, 61.2), (-7, 59.8)]),
    line(36, [(-15, 60.0), (-11, 60.0), (-7, 58.2)]),
    line(40, [(-14, 57.4), (-11, 57.6), (-7, 56.6)]),
    [(-15.0, 53.2, 49.0), (-12.0, 52.6, 46.0), (-9.5, 52.6, 43.0), (-7.0, 54.6, 41.0)],
]


def blocks_of(lofts, keep):
    out = set()
    for lines in lofts:
        out |= kit.loft_blocks(lines, thickness=2)
    return {c for c in out if keep(c)}


def main():
    old = kit.existing()
    terrain_cols = {(x, z) for (x, y, z), (n, g) in old.items() if g == "Gelände"}
    occupied = set(old)
    plate = {(x, z) for (x, y, z), (n, g) in old.items() if y in (59, 60) and g == "Bauwerke"}

    def keep(c):
        x, y, z = c
        # the author's mountains already hold their columns; the roof plates and their beams stay uncovered
        return (x, z) not in terrain_cols and (x, z) not in plate

    shelf = blocks_of([band_shelf], keep)
    ridge = blocks_of([north_lines, band_west, south_lines], keep) - shelf

    pieces = [
        {"name": "Dachschulter", "wool": 4,
         "note": "Gelb, flacheres Gelände: Schulter längs der Westkante der Schachbrettplatten, eine Stufe unter "
                 "der Platte (58), nach Westen sanft auf ~60 steigend.",
         "lofts": [band_shelf], "blocks": shelf},
        {"name": "Bergrücken über dem Bunker", "wool": 3,
         "note": "Hellblau, Berg: Rücken bei x ~ -9 (64..67), im Norden an die offene Westflanke des Nordbergs "
                 "(bis 78) angeschlossen, im Südwesten auf die Kante des Südbergs (52..53) fallend. Deckt "
                 "Hallendach, Treppenröhren und Hinterzimmer.",
         "lofts": [north_lines, band_west, south_lines], "blocks": ridge},
    ]
    allb = shelf | ridge
    res = kit.checks(allb, full=False, region=[])
    for k in ("overlap", "overlap_at", "walls", "walls_at", "void", "steps", "seams"):
        print(k, res[k])
    for p in pieces:
        print(p["name"], "lofts", len(p["lofts"]), "lines", sum(len(l) for l in p["lofts"]),
              "points", sum(len(x) for l in p["lofts"] for x in l), "blocks", len(p["blocks"]))
    path = kit.write("cov-2", "cover", "Bunker unterm Berg",
                     "Der Berg schließt sich hinter dem Bunker: ein Rücken (bis 67) zieht vom Nordberg über Halle, "
                     "Treppenröhren und Hinterzimmer bis auf den Südberg, und eine flache Schulter führt ihn auf "
                     "Höhe der Schachbrettplatten heran. Vom Tal aus bleibt die Fassade mit dem Kern frei, oben liegen "
                     "die Schachbrettplatten wie Terrassen im Hang, Schwarzdach und Antenne ragen darüber.",
                     pieces, absolute=False)
    print(path)
    cols = {c: p["wool"] for p in pieces for c in p["blocks"]}
    if "--render" in sys.argv:
        box = (-20, 45, 0, 95, -50, 55)
        kit.render(cols, os.path.join(HERE, "render_q0.png"), q=0, scale=6, box=box, full=False)
        kit.render(cols, os.path.join(HERE, "render_q2.png"), q=2, scale=6, box=box, full=False)


if __name__ == "__main__":
    main()
