"""Coldstore: build the board.

    python3 gen.py <build-dir>

The drawn quarter is built, mirrored across v -0.5 into its team's half, and that half across u -0.5 into the
enemy's; then the objectives are stamped and read back.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", ".."))
import dress                                                                          # noqa: E402
import layout as L                                                                     # noqa: E402
import objectives as OB                                                                # noqa: E402
import rooms                                                                           # noqa: E402
import shell                                                                           # noqa: E402
from pgmvox import World                                                               # noqa: E402
from pgmvox.core.orient import turn_world                                              # noqa: E402

w = World(L.X0, L.Z0, L.SX, L.SZ, L.SY)
k = shell.shell(w)
print(f"quarter: {int((k == shell.ROCK).sum())} columns of rock, {int((k == shell.ISLAND).sum())} of island, "
      f"{int((k == shell.VOID).sum())} of void")
rooms.wool_block(w)
rooms.spawn(w)
dress.alcoves(w)
dress.vault_door(w)
dress.faces(w, k)
dress.ceiling(w)
dress.drifts(w, k)
dress.surface(w)
turn_world(w, "mirror_z", lambda x, z: z >= 0)
turn_world(w, "mirror_x", lambda x, z: x < 0)
rooms.paint_arrows(w)
O = OB.objectives()
O.stamp(w)
problems = O.check(w)
print(f"objectives with a problem: {len(problems)}")
for p in problems:
    print("   ", p)
w.save(sys.argv[1], "Coldstore", L.SPAWN)
print(f"blocks: {int((w.ids != 0).sum())}")
