"""Option A, widened: a crevasse with two bridges, one smooth surface through irregular points, as the author lofts.
Superseded first-round sketch; S is the study folder, holding mid/full.pkl from full.py."""
import os, sys, math, pickle, collections
S = sys.argv[1]
sys.path.insert(0, S + "/rec"); sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools"))); sys.path.insert(0, os.path.join(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools")), "render")); sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))); sys.path.insert(0, S)
import terrain
from png import Canvas, write_png
from iso import turned, _visible, iso_bounds, draw_iso, BACKGROUND
from colours import col

full = pickle.load(open(S + "/mid/full.pkl", "rb"))
C = (59.5, 86.5); L = math.hypot(75, 29); d = (75 / L, -29 / L); n = (-d[1], d[0])
def st(x, z): return ((x - C[0]) * d[0] + (z - C[1]) * d[1], (x - C[0]) * n[0] + (z - C[1]) * n[1])
def xz(s, t): return (C[0] + s * d[0] + t * n[0], C[1] + s * d[1] + t * n[1])

FLOOR, ICE = (35, 8), (35, 0)
FLOOR_Y = 6
floor_top = {}
for (x, y, z), b in full.items():
    if b == FLOOR and 10 <= y <= 40 and y > floor_top.get((x, z), -1): floor_top[(x, z)] = y
edge_t, edge_h = {}, {}
for (x, z), y in floor_top.items():
    s, t = st(x, z)
    if t < 0 and -50 <= s <= 50:
        k = round(s)
        if t > edge_t.get(k, -99): edge_t[k], edge_h[k] = t, y
def at(table, s):
    ks = [k for k in table if abs(k - s) <= 3] or [min(table, key=lambda k: abs(k - s))]
    return sum(table[k] for k in ks) / len(ks)

BRIDGE = (14.5, 23.0)                                   # along the cut, on the positive side; its twin mirrors it
ACCESS = (-40.0, -27.0)                                 # where our wall runs out gently enough to walk down; and its twin
def jitter(k, amount): return amount * math.sin(k * 2.399 + 0.7)   # irregular, repeatable spacing

points = []
s = -45.0; k = 0
while s <= 45.0:                                        # stations along the crack, irregularly spaced
    ta, ha = at(edge_t, s), at(edge_h, s)
    gentle = ACCESS[0] <= s <= ACCESS[1]
    run = 11.5 if gentle else 6.2
    points.append((s, ta, ha))                                                            # the rim: the floor's edge
    if gentle:
        points.append((s, ta + run * 0.5 + jitter(k, 0.5), (ha + FLOOR_Y) / 2 + jitter(k + 3, 0.4)))   # an even slope
    else:
        points.append((s, ta + 2.6 + jitter(k, 0.6), ha - 5.5 + jitter(k + 3, 0.8)))                  # a steep shoulder
    points.append((s, ta + run + jitter(k + 5, 0.8), FLOOR_Y + 0.4))                                  # the toe
    points.append((s, 0.0 + jitter(k + 1, 1.5), FLOOR_Y + jitter(k + 2, 0.4)))                        # the floor
    s += 5.0 + jitter(k, 1.6); k += 1
points += [(-a, -b, h) for a, b, h in points]           # the turn: every point has its twin
surface = terrain.fit(points, smooth=0.4, scale=8.0)

gap = {}
for x in range(0, 120):
    for z in range(40, 135):
        if (x, z) in floor_top: continue
        s, t = st(x, z)
        if abs(s) > 46: continue
        ta, tb = at(edge_t, s), -at(edge_t, -s)
        if ta - 0.5 <= t <= tb + 0.5:
            rim = max(at(edge_h, s), at(edge_h, -s))
            gap[(x, z)] = min(rim, max(FLOOR_Y - 1, surface(s, t)))
heights = {c: int(round(h)) for c, h in gap.items()}
add = {}
steps = collections.Counter()
for (x, z), top in heights.items():
    lows = [heights.get((x + a, z + b), floor_top.get((x + a, z + b), top)) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))]
    bottom = min([top] + lows)
    slope = max(abs(top - l) for l in lows)
    steps[slope] += 1
    s_, t_ = st(x, z)
    rim = min(at(edge_h, s_), at(edge_h, -s_))
    block = FLOOR if top <= FLOOR_Y + 1 or top >= rim - 1 else ICE    # walls are ice; the floor and the decks walk
    for y in range(min(bottom, top - 1), top + 1): add[(x, y, z)] = block
# the bridges: decks spanning rim to rim, a little arched, two thick, the floor running on underneath
decks = 0
for (x, z) in list(gap):
    s_, t_ = st(x, z)
    for lo, hi in (BRIDGE, (-BRIDGE[1], -BRIDGE[0])):
        if lo <= s_ <= hi:
            ta, tb = at(edge_t, s_), -at(edge_t, -s_)
            ha, hb = at(edge_h, s_), at(edge_h, -s_)
            f = (t_ - ta) / max(1e-6, tb - ta)
            deck = int(round(ha + (hb - ha) * f + 1.2 * math.sin(math.pi * min(1, max(0, f)))))
            for y in (deck - 1, deck): add[(x, y, z)] = FLOOR
            decks += 1
print("deck columns", decks, "| clearance under the decks", min(deck_y - 1 - heights[c] for c, deck_y in
      [((x, z), max(y for (xx, y, zz), b in add.items() if (xx, zz) == (x, z))) for (x, z) in gap
       if any(lo <= st(x, z)[0] <= hi for lo, hi in (BRIDGE, (-BRIDGE[1], -BRIDGE[0])))]))
pickle.dump(add, open(S + "/mid/ravine.pkl", "wb"))
asym = sum(1 for (x, y, z), b in add.items() if add.get((119 - x, y, 173 - z)) != b)
print(f"{len(points)} points ({len(points)//2} placed, each with its twin); {len(add)} blocks; not mirrored by the turn: {asym}")
print("steepest step between neighbouring columns:", max(steps), "| steps:", sorted(steps.items()))

def render(world, path, box, q=None, scale=3):
    x0, x1, z0, z1 = box
    blocks = {c: b for c, b in world.items() if x0 <= c[0] <= x1 and z0 <= c[2] <= z1}
    if q is None:
        top = {}
        for (x, y, z), b in blocks.items():
            if (x, z) not in top or y > top[(x, z)][0]: top[(x, z)] = (y, b)
        cv = Canvas((x1 - x0 + 1) * scale + 40, (z1 - z0 + 1) * scale + 30, (247, 247, 244))
        for (x, z), (y, b) in top.items():
            rgb = col(*b) if b[0] != 22 else (40, 60, 200); f = 0.35 + 0.65 * y / 60
            for a in range(scale):
                for c2 in range(scale): cv.set((x - x0) * scale + 30 + a, (z - z0) * scale + 15 + c2, tuple(min(255, int(v * f)) for v in rgb))
        write_png(path, cv); return
    cb = {c: (col(*b) if b[0] != 22 else (40, 60, 200)) for c, b in blocks.items()}
    cb = turned(cb, q); W, H, K = scale, scale // 2 or 1, scale
    sh = {c: cb[c] for c in _visible(cb)}
    u0, u1, v0, v1 = iso_bounds(sh, W, H, K)
    cv = Canvas(int(u1 - u0) + 40, int(v1 - v0) + 40, BACKGROUND); draw_iso(cv, sh, (20 - u0, 20 - v0), W, H, K); write_png(path, cv)

world = dict(full); world.update(add)
render(world, S + "/mid/ravine_top.png", (0, 120, 40, 135))
render(world, S + "/mid/ravine_iso1.png", (0, 120, 30, 145), q=1, scale=4)
render(world, S + "/mid/ravine_iso3.png", (0, 120, 30, 145), q=3, scale=4)
render(add, S + "/mid/ravine_only.png", (0, 120, 30, 145), q=0, scale=5)
render(world, S + "/mid/ravine_close.png", (15, 105, 55, 120), q=0, scale=6)
