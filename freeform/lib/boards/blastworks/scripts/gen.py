"""Blastworks: build the board.

    python3 gen.py <build-dir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import layout as L                                                                     # noqa: E402
import nature                                                                          # noqa: E402
import parts                                                                           # noqa: E402
import objectives as OB                                                                # noqa: E402
from pgmvox import B, World                                                            # noqa: E402
from pgmvox.core.orient import turn_world                                              # noqa: E402
from pgmvox.play.objectives import build_marker                                        # noqa: E402

w = World(L.X0, L.Z0, L.SX, L.SZ, L.SY)
parts.lay(w)
sp = nature.ground(w, L.SPAWN, L.SPAWN_H, seed=11, relief=1.2,
                   joins=[(L.UP_STAIR, L.SPAWN_H), (L.DOWN_STAIR, L.SPAWN_H), (L.EXIT[0], L.SPAWN_H)],
                   flats=[((L.HALL[2] + 1, L.HALL_DOOR[0] - 1, L.HALL[2] + 3, L.HALL_DOOR[1] + 1), L.SPAWN_H)],
                   skip=[L.HALL])
fr = nature.ground(w, L.FRONT, L.FRONT_H, seed=12, relief=1.6,
                   joins=[(L.DESCENT, L.FRONT_H), (L.EAST_STAIR, L.FRONT_H), (L.EXIT[1], L.SPAWN_H)])
import parts as P                                                                      # noqa: E402,F811
eg = P.G.Ground([s for s in P.sections() if s.name == "east-stair"])
P.G.lay(w, eg, P.S.style(), face_of=P.face_of(eg))
nature.green(w, L.SPAWN, sp, keep=[L.HALL, (L.HALL[2] + 1, L.HALL_DOOR[0] - 1, L.UP_STAIR[0], L.HALL_DOOR[1] + 1), L.UP_STAIR, L.DOWN_STAIR, L.EXIT[0], L.SPAWN_AREA], seed=11, spruces=3)
nature.green(w, L.FRONT, fr, keep=[L.DESCENT, L.EAST_STAIR, L.EXIT[1]], seed=12, spruces=2, boulders=3)
turn_world(w, "half", lambda x, z: x < 0)
for (px, pz), dye in ((L.PAD, L.ROOM_DYE), (L.ROOM_PAD, L.PAD_DYE)):    # red's pads take the other wool's colour
    for x in (px, px + 1):
        for z in (pz, pz + 1):
            X, Z = -1 - x, -1 - z
            y = next(y for y in range(L.SY) if w.id(X, y, Z) == B.WOOL)
            w.set(X, y, Z, B.WOOL, dye)
parts.middle(w)
zones = L.ZONES + [parts.image(r) for r in L.ZONES]
cells = {(x, z) for x0, z0, x1, z1 in zones for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)}
X, Z = w.grid()
land = (w.ids[:, 1:, :] != 0).any(axis=1)
terrain = {(int(x), int(z)) for x, z in zip(X[land], Z[land])}
marks = build_marker(cells, terrain)
for x, z in marks:                                       # the zones' outline, as the studio stamps it (ST5)
    if w.id(x, L.MARKER_Y, z) == B.AIR:
        w.set(x, L.MARKER_Y, z, B.REDSTONE_WIRE)
print(f"redstone marking the build zones: {len(marks)} blocks")
unmarked = [(int(x), int(z)) for x, z in zip(X[land], Z[land]) if w.id(int(x), 0, int(z)) == B.AIR
            and (int(x), int(z)) not in cells]
print(f"columns with blocks but no ground at y 0, outside every zone: {len(unmarked)} {unmarked[:8]}")
O = OB.objectives()
O.stamp(w)
problems = O.check(w)
print(f"objectives with a problem: {len(problems)}")
for p in problems:
    print("   ", p)
w.save(sys.argv[1], "Blastworks", L.SPAWN_AT)
print(f"blocks: {int((w.ids != 0).sum())}")
