"""Islets' plan sketch: from above with red's route to the hill, a true-scale section, the check."""
import subprocess
import sys

from plan import COLOURS, KILL_Y, WALK, build
from pgmvox import plangraph as G
from pgmvox.sketch import Sketch

R = build()
E = G.graph(R, WALK)
D, prev = G.dijkstra(E, [(-24, 0)])
S = Sketch("Islets — the plan")
S.board(R, COLOURS, scale=8)
S.routes(R, [G.path(prev, (0, 0))])
S.jumps(R, G.jumps(R, WALK))
S.section(R, "x", 0, (KILL_Y - 2, 40), scale=8, colours=COLOURS, marks=[(0, KILL_Y, "kill height")])
S.text(subprocess.run([sys.executable, "plan_check.py"], capture_output=True, text=True).stdout.splitlines())
S.save(sys.argv[1])
