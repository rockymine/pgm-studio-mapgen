"""Blastworks: build the board.

    python3 gen.py <build-dir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", ".."))
import layout as L                                                                     # noqa: E402
import nature                                                                          # noqa: E402
import parts                                                                           # noqa: E402
from pgmvox import World                                                               # noqa: E402

w = World(L.X0, L.Z0, L.SX, L.SZ, L.SY)
parts.lay(w)
sp = nature.ground(w, L.SPAWN, L.SPAWN_H, seed=11, relief=1.2,
                   joins=[(L.UP_STAIR, L.SPAWN_H), (L.DOWN_STAIR, L.SPAWN_H), (L.EXIT[0], L.SPAWN_H)],
                   flats=[((L.SLOT[0] - 3, L.SLOT[2] - 2, L.SLOT[0] + 3, L.SLOT[2] + 2), L.SPAWN_H),
                          ((L.SPAWN_AT[0] - 1, L.SPAWN_AT[2] - 1, L.SPAWN_AT[0] + 1, L.SPAWN_AT[2]), L.SPAWN_H)],
                   skip=[L.HALL])
fr = nature.ground(w, L.FRONT, L.FRONT_H, seed=12, relief=1.6,
                   joins=[(L.DESCENT, L.FRONT_H), (L.EAST_STAIR, L.FRONT_H), (L.EXIT[1], L.SPAWN_H)])
import parts as P                                                                      # noqa: E402,F811
eg = P.G.Ground([s for s in P.sections() if s.name == "east-stair"])
P.G.lay(w, eg, P.S.style(), face_of=P.face_of(eg))
nature.green(w, L.SPAWN, sp, keep=[L.HALL, L.UP_STAIR, L.DOWN_STAIR, L.EXIT[0], L.SPAWN_AREA], seed=11, spruces=3)
nature.green(w, L.FRONT, fr, keep=[L.DESCENT, L.EAST_STAIR, L.EXIT[1]], seed=12, spruces=2, boulders=3)
w.save(sys.argv[1], "Blastworks", L.SPAWN_AT)
print(f"blocks: {int((w.ids != 0).sum())}")
