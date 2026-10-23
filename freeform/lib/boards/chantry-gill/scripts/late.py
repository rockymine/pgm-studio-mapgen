"""Chantry Gill read through a long match's four phases (pgmvox.read.late): red's walk from its spawn to blue's
town monument, on the ground, bridging the zone, on the sky to the build height, and with the ground dug away, at
the build height the map writes and at a ceiling six blocks over the town's square.

    python3 late.py <build-dir>
"""
import sys

import objectives as P
import zone as ZN
from layout import FLOOR
from pgmvox import World
from pgmvox.read import late

w = World.load(sys.argv[1])
X, Z = w.grid()
zone = ZN.mask(X, Z)
x, y, z = P.TOWN
goal = (x, y + 1, z)
red = (-1 - P.SPAWN_AT[0], P.SPAWN_AT[1], -1 - P.SPAWN_AT[2])
rows = []
for name, top in ((f"the town - build height {P.MAX_BUILD}", P.MAX_BUILD), (f"the town - ceiling {FLOOR + 8}", FLOOR + 8)):
    rows.append((name, late.phases(w, red, goal, zone, top)))
print(late.table(rows))
