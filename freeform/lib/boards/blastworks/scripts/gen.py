"""Blastworks: build the board: the concept set down as blue's base, the board's additions round it, the half turn
for red, the objectives, the void rule's marks and the redstone round the build zones.

    python3 gen.py <build-dir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", ".."))
import build                                                                           # noqa: E402
import layout as L                                                                     # noqa: E402
import objectives as OB                                                                # noqa: E402
from pgmvox import World                                                               # noqa: E402
from pgmvox.core.orient import turn_world                                              # noqa: E402
from pgmvox.play.rules import mark_ground                                              # noqa: E402

w = World(L.X0, L.Z0, L.SX, L.SZ, L.SY)
build.concept(w)
build.land(w)
turn_world(w, "half", lambda x, z: x < 0)
O = OB.objectives()
O.stamp(w)
print(f"ground marked under {mark_ground(w)} columns; redstone on {build.markers(w)} columns round the build zones")
problems = O.check(w)
print(f"objectives with a problem: {len(problems)}")
for p in problems:
    print("   ", p)
w.save(sys.argv[1], "Blastworks", L.SPAWN)
print(f"blocks: {int((w.ids != 0).sum())}")
