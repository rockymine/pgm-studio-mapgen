"""Hollowstack read through a long match's four phases (pgmvox.read.late): red's walk from its spawn to blue's Vault
monument, on the ground, bridging the chasm, on the sky to the build height, and with the ground dug away; for each,
whether walling the Vault's doors shuts the monument off. Under CTW's usual rules every block breaks; under the
rules this board writes only the kit's wood and glass do.

    python3 late.py <build-dir>
"""
import sys

import numpy as np

import layout as L
import objectives as P
from pgmvox import World
from pgmvox.read import late

w = World.load(sys.argv[1])
X, Z = w.grid()
chasm = (X >= -L.FACE) & (X <= L.FACE - 1)
red_spawn = (-1 - L.SPAWN[0], L.SPAWN[1], -1 - L.SPAWN[2])
vx, vy, vz = P.vault_at()
vi0, vj0, vi1, vj1 = L.VAULT
x0, y0, z0 = L.cell_box(L.UNDERCROFT, vi0, vj0)
x1, _, z1 = L.cell_box(L.UNDERCROFT, vi1, vj1)
x1, z1 = x1 + L.CELL - 1, z1 + L.CELL - 1
door = [(x, y, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1) for y in range(y0 + 1, y0 + 2 * L.STOREY)
        if (x in (x0, x1) or z in (z0, z1)) and w.id(x, y, z) == 0]
rows = [("the Vault - usual rules", late.phases(w, red_spawn, (vx, vy - 1, vz), chasm, P.MAX_BUILD, door=door)),
        ("the Vault - held rules", late.phases(w, red_spawn, (vx, vy - 1, vz), chasm, P.MAX_BUILD, door=door,
                                              breakable={5, 20, 17, 162}))]
print(f"the Vault's doors: {len(door)} blocks of opening in its walls")
print(late.table(rows))
