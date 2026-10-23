"""Frostvault: build the board.

    python3 gen.py <build-dir>

The composed board is drawn as a bunker plan, laid, dressed, and its objectives stamped and read back.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", ".."))
import board                                                                           # noqa: E402
import layout as L                                                                     # noqa: E402
import objectives as OB                                                                # noqa: E402
from pgmvox import World                                                               # noqa: E402
from pgmvox.built import bunker as BB                                                  # noqa: E402
from pgmvox.plan import bunker as PB                                                   # noqa: E402

b = board.plan()
print(PB.ascii(b))
print(f"cuts: {b.cuts}; islands: {sorted(len(i) for i in b.islands)} cells; dropped {b.dropped}; "
      f"pillars {len(b.cells(PB.PILLAR))} cells; walls on {len(b.walls)} seams")
blk, x0, z0 = BB.raster(b)
w = World(x0, z0, blk.shape[0], blk.shape[1], L.SY)
got = BB.lay(w, b, L.H)
clear = [s["slots"][0] for s in got.spawns] + [s["slots"][1] for s in got.spawns] + [s["at"] for s in got.spawns]
BB.dress(w, got, L.H, clear=clear)
O = OB.objectives(got)
O.stamp(w)
problems = O.check(w)
print(f"objectives with a problem: {len(problems)}")
for p in problems:
    print("   ", p)
w.save(sys.argv[1], "Frostvault", got.spawns[0]["at"])
print(f"blocks: {int((w.ids != 0).sum())}")
