"""Pictures of the composed world, without the floating reference pieces.

    python3 sketches/fire-and-ice/render.py <region> <out.png> top <x0,x1,y0,y1,z0,z1> [scale]
    python3 sketches/fire-and-ice/render.py <region> <out.png> iso <x0,x1,y0,y1,z0,z1> <scale> <quarter>

A box bound written `_` is open.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(HERE, "..", "..", "tools")
sys.path.insert(0, TOOLS); sys.path.insert(0, os.path.join(TOOLS, "render")); sys.path.insert(0, HERE)
from anvil import World
from png import Canvas, write_png
from iso import turned, _visible, iso_bounds, draw_iso, BACKGROUND
from colours import col
w = World(sys.argv[1]); out = sys.argv[2]; mode = sys.argv[3]
box = [int(v) if v != '_' else None for v in sys.argv[4].split(",")]   # x0,x1,y0,y1,z0,z1
def reference(x, y, z):
    return (8 <= x <= 52 and y >= 85 and -22 <= z <= 47) or (x >= 69 and z < 45 and y >= 60) or y >= 100 or z < -140
def keep(x, y, z):
    if reference(x, y, z): return False
    x0, x1, y0, y1, z0, z1 = box
    return all(lo is None or v >= lo for v, lo in ((x, x0), (y, y0), (z, z0))) and \
           all(hi is None or v <= hi for v, hi in ((x, x1), (y, y1), (z, z1)))
def colour(i, d):
    if i == 35 and d in (9, 11, 12, 1, 2, 10, 14):
        return {9: (22, 156, 156), 11: (53, 57, 157), 12: (114, 71, 40), 1: (240, 118, 19), 2: (189, 68, 179),
                10: (121, 42, 172), 14: (220, 40, 34)}[d]
    return col(i, d)
blocks = {(x, y, z): colour(i, d) for x, y, z, i, d in w.blocks() if keep(x, y, z)}
if mode == "top":
    S = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    xs = [c[0] for c in blocks]; zs = [c[2] for c in blocks]; ys = [c[1] for c in blocks]
    minx, maxx, minz, maxz, miny, maxy = min(xs), max(xs), min(zs), max(zs), min(ys), max(ys)
    top = {}
    for (x, y, z), c in blocks.items():
        if (x, z) not in top or y > top[(x, z)][0]: top[(x, z)] = (y, c)
    cv = Canvas((maxx - minx + 1) * S + 50, (maxz - minz + 1) * S + 40, (247, 247, 244))
    for (x, z), (y, c) in top.items():
        f = 0.55 + 0.45 * (y - miny) / max(1, maxy - miny)
        rgb = tuple(min(255, int(v * f)) for v in c)
        for a in range(S):
            for b in range(S): cv.set((x - minx) * S + 40 + a, (z - minz) * S + 20 + b, rgb)
    for g in range((minx // 16) * 16, maxx + 1, 16):
        if g < minx: continue
        px = (g - minx) * S + 40
        for yy in range(20, cv.height - 20, 4): cv.set(px, yy, (255, 0, 0))
        cv.text(px + 1, cv.height - 16, str(g), (200, 0, 0), 1)
    for g in range((minz // 16) * 16, maxz + 1, 16):
        if g < minz: continue
        pz = (g - minz) * S + 20
        for xx in range(40, cv.width, 4): cv.set(xx, pz, (255, 0, 0))
        cv.text(2, pz + 1, str(g), (200, 0, 0), 1)
    write_png(out, cv)
else:
    scale, quarter = int(sys.argv[5]), int(sys.argv[6])
    b = turned(blocks, quarter)
    W, H, K = scale, scale // 2 or 1, scale
    shown = {c: b[c] for c in _visible(b)}
    u0, u1, v0, v1 = iso_bounds(shown, W, H, K)
    cv = Canvas(int(u1 - u0) + 40, int(v1 - v0) + 40, BACKGROUND)
    draw_iso(cv, shown, (20 - u0, 20 - v0), W, H, K)
    write_png(out, cv)
print(out, len(blocks))
