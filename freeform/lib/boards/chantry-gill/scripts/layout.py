"""Chantry Gill's layout: the land in the void, one team's half drawn, the other its half turn.

Blue holds the south (z > 0), red is blue's image under (x, z) -> (-1 - x, -1 - z). Each team has a main island,
the fell with the town, and a side island, the Scar, east of it; between them runs the Gill, a gorge, not void.
Between the two teams lies the void, crossed by a build zone the board's whole width.
"""
import math

# the main island: the fell, the town on its east rim over the gill, the spawn under the knott at its back
MAIN = [(-78, 40), (-70, 22), (-52, 13), (-30, 16), (-12, 11), (6, 14), (20, 20), (27, 30), (26, 46), (29, 62),
        (27, 78), (30, 92), (22, 106), (4, 116), (-20, 118), (-44, 112), (-62, 100), (-76, 80), (-82, 60)]
# the side island: the Scar, its leaning brow facing west over the gill, the tarn at its front
SIDE = [(40, 24), (52, 15), (68, 17), (80, 30), (84, 50), (79, 70), (72, 88), (58, 100), (44, 98), (39, 84),
        (40, 66), (38, 50), (41, 36)]
# the gill: the gorge between them, its floor 9 under the main island's rim
GILL = [MAIN[7], MAIN[8], MAIN[9], MAIN[10], MAIN[11], (36, 98), (44, 98), SIDE[9], SIDE[10], SIDE[11], SIDE[12],
        SIDE[0], (31, 22)]
# scenery: the edge down the west and the knott across the back, high ground fenced off from play by its own
# faces; it frames the board and nobody fights on it
EDGE = [(-82, 60), (-76, 80), (-62, 100), (-44, 112), (-56, 96), (-66, 78), (-70, 58), (-68, 38), (-78, 40)]
KNOTT = [(-44, 112), (-20, 118), (4, 116), (22, 106), (30, 92), (20, 100), (2, 106), (-20, 106), (-40, 104),
         (-56, 96)]
BUILD_Z = (-14, 13)                       # the build zone over the void between the teams, the board's whole width
X_RANGE = (-90, 89)

PLACES = {                                 # name: (x, z, what it is)
    "spawn": (4, 94, "the spawn, at the foot of the knott, the hall behind it"),
    "town monument": (20, 56, "the town monument: three obsidian over the market square, on the town's east rim"),
    "scar monument": (58, 84, "the Scar monument: three obsidian on the plateau behind the brow"),
    "square": (10, 60, "the market square, stalls along its west edge"),
    "chapel": (8, 72, "the chapel on the square's south side, the crypt under it, the ladder up into its nave"),
    "town": (-10, 64, "the town: houses on the main street and a lane, the wall broken on its west"),
    "front gate": (-6, 26, "the north gate, where the street leaves the town for the front"),
    "knott": (-10, 111, "the knott: a crag across the back, its face to the north over the spawn; scenery"),
    "edge": (-70, 74, "the edge: a scarp down the west, its face to the fell; scenery"),
    "fields": (-44, 46, "the byre, its field and the flower meadow, between the edge and the town"),
    "brig": (33, 36, "the brig: a stone arch over the gill, from the front of the town to the tarn"),
    "tarn": (60, 30, "the tarn on the Scar's front, its beach to the north, the beck running in from the gill"),
    "brow": (46, 70, "the Scar's brow: its face leaning out over the gill, 14 over the square and 22 off it"),
    "shelter": (40, 66, "the shelter worn into the brow's foot on the gill floor; the adit runs on from it"),
    "plateau": (68, 66, "the plateau behind the brow, reached up a slope at its north end"),
    "back brig": (34, 91, "a timber bridge over the gill behind the brow: the spawn's way to the Scar"),
    "chimney": (44, 74, "a chimney in the rock from the shelter up to the plateau, a ladder in it"),
}
SPAWN = PLACES["spawn"][:2]
MONUMENTS = [PLACES["town monument"][:2], PLACES["scar monument"][:2]]
MONUMENT = MONUMENTS[0]

# the ways an attacker landing on this half comes at each monument
ROUTES = {
    "town: through": [(-6, 14), (-6, 26), (-4, 44), (6, 52), (20, 56)],
    "town: around": [(-46, 16), (-50, 34), (-40, 52), (-18, 60), (6, 64), (20, 56)],
    "town: brig": [(46, 18), (44, 34), (33, 36), (24, 42), (20, 56)],
    "town: from the brow": [(62, 16), (74, 40), (64, 58), (48, 66), "bridge", (20, 56)],
    "town: below": [(46, 18), (33, 30), (34, 50), (38, 66), "adit", (12, 70), "ladder", (14, 62), (20, 56)],
    "scar: front": [(62, 16), (74, 40), (72, 62), (64, 76), (58, 84)],
    "scar: chimney": [(46, 18), (33, 30), (34, 50), (40, 66), "chimney", (48, 72), (58, 84)],
}
DEFENCES = [[(4, 94), (4, 80), (10, 66), (20, 56)],
            [(4, 94), (30, 92), (44, 92), (58, 84)]]
DEFENCE = DEFENCES[0]
ADIT = [(39, 66, 33), (30, 67, 29), (18, 70, 30), (12, 72, 33)]      # (x, z, floor y): shelter to crypt
CRYPT = (4, 68, 16, 76)


def turn(p):
    return (-1 - p[0], -1 - p[1])


def length(pts):
    pts = [p for p in pts if not isinstance(p, str)]
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))
