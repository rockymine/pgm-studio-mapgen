"""Hollowstack: build the board.

    python3 gen.py <build-dir>
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import layout as L                                                                     # noqa: E402
import body                                                                            # noqa: E402
import passages                                                                        # noqa: E402
import places                                                                          # noqa: E402
import objectives as OB                                                                # noqa: E402
from pgmvox import World                                                               # noqa: E402
from pgmvox.core.orient import turn_world                                              # noqa: E402
from pgmvox.play.rules import mark_ground                                              # noqa: E402

w = World(L.X0, L.Z0, L.SX, L.SZ, L.SY)
S = body.rock(w)
wood_floor, wood_roof = body.underwood(w)
deep = body.deep(w)
body.wells(w, S, wood_roof)
places.keep(w)                                   # before the Workings, whose well house stands in its yard
rng = np.random.default_rng(7)
under = passages.undercroft(w, rng)
mine = passages.workings(w, rng)
passages.descent(w)
for name, (g, p, laid) in (("Undercroft", under), ("Workings", mine)):
    print(f"{name}: {len(laid['pass'])} passage cells, {len(p.links)} links, {len(p.rooms)} rooms, "
          f"{len(p.stairs)} stairs, {len(p.shafts)} wells, {len(p.ports)} ports")
d = places.underwood(w, wood_floor, wood_roof, rng)
print(f"Underwood: {d['trees']} trees, {d['stars']} stars in the roof, {d['vines']} vines")
shrine_at = places.shrine(w)
vault_at = places.vault(w)
places.deep(w, deep, rng)
print(f"Tops: {places.tops(w, S, rng)} trees")
places.watch(w, S)
places.fronts(w)
made = places.made_mask(w, [under[:2], mine[:2]])
print(f"face: {places.pocks(w, made, rng)} hollows")
places.stubs(w, rng)
print(f"settled: {places.settle(w)} loose blocks over air made fast")
print(f"face: {places.face(w, rng)} vines")
print(f"rock: {int((w.ids != 0).sum())} blocks; Tops y {int(S[S > 0].min())} to {int(S.max())}")
m = wood_floor >= 0
print(f"Underwood: {int(m.sum())} columns, floors y {int(wood_floor[m].min())} to {int(wood_floor[m].max())}, "
      f"roof to y {int(wood_roof[m].max())}")
print(f"the shrine's altar at {shrine_at}, the vault's dais at {vault_at}")
turn_world(w, "half", lambda x, z: x >= 0)
O = OB.objectives()
O.stamp(w)
print(f"objectives stamped; ground marked under {mark_ground(w)} columns")
problems = O.check(w)
print(f"objectives with a problem: {len(problems)}")
for p in problems:
    print("   ", p)
w.save(sys.argv[1], "Hollowstack", (0, 112, 0))
import json                                                                            # noqa: E402
with open(os.path.join(sys.argv[1], "segments.json"), "w") as f:     # the cells the passages take, for the walk
    json.dump({name: sorted(list(c) for c in p.taken()) for name, (g, p, _) in
               (("Undercroft", under), ("Workings", mine))}, f)
print("generated")
