"""The author's half and its 180-degree turn about the centre block pair, as one dict; scratch only."""
import os, sys
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools")))
from anvil import World

def turned_block(block):
    i, d = block
    if i in (53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 163, 164, 180):
        return (i, (d & 4) | ({0: 1, 1: 0, 2: 3, 3: 2}[d & 3]))
    if i in (50, 75, 76, 77, 143, 65, 54, 146, 61, 62, 23, 158):
        m = {2: 3, 3: 2, 4: 5, 5: 4} if i in (65, 54, 146, 61, 62, 23, 158) else {1: 2, 2: 1, 3: 4, 4: 3}
        return (i, m.get(d & 7, d & 7) | (d & 8))
    if i in (131, 183, 184, 185, 186, 187, 107, 96, 167, 26, 64, 71, 193, 194, 195, 196, 197):
        return (i, (d & ~3) | ((d + 2) & 3))
    return block

def load(region):
    w = World(region)
    half = {(x, y, z): (i, d) for x, y, z, i, d in w.blocks()
            if -16 <= x <= 105 and -57 <= z <= 102 and not (i == 169)}
    full = dict(half)
    for (x, y, z), b in half.items():
        full[(119 - x, y, 173 - z)] = turned_block(b)
    return half, full
