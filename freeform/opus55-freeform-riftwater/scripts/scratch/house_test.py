# Scratch: the house builder's first test — four houses, one per style, on a flat slab.
# python3 scratch/house_test.py; then render_iso.py /tmp/claude-0/rw/ht <out.png> --scale 6
import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from mc import World, B
import house
class FL: pass
w = World(-40, -20, 80, 40, sy=80)
L = FL(); L.x0, L.z0, L.nx, L.nz = -40, -20, 80, 40
L.H = np.full((80, 40), 50); L.land = np.ones((80, 40), bool); L.water = np.zeros((80, 40), int)
w.fill(-40, 40, -20, 39, 49, 19, B.DIRT); w.fill(-40, 50, -20, 39, 50, 19, B.GRASS)
house.house(w, L, -30, -6, -22, 0, storeys=2, style="town", door="s", kind="house")
house.house(w, L, -15, -6, -10, 0, storeys=3, style="town", door="s", kind="shop")
house.house(w, L, 0, -5, 5, 2, storeys=1, style="village", door="e", kind="cottage")
house.house(w, L, 12, -8, 22, 2, storeys=2, style="stone", door="s", kind="hall")
w.save('/tmp/claude-0/rw/ht', 't', (0, 60, 0))
