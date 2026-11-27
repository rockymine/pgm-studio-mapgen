"""Three options for the centre of the author's map, as wool sketches over the turned full map. Superseded first-round sketch; S is the study folder, holding mid/full.pkl from full.py."""
import os, sys, math, pickle, collections
S = sys.argv[1]
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools"))); sys.path.insert(0, os.path.join(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools")), "render")); sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
sys.path.insert(0, S)
from png import Canvas, write_png
from iso import turned, _visible, iso_bounds, draw_iso, BACKGROUND
from colours import col

full = pickle.load(open(S + "/mid/full.pkl", "rb"))
C = (59.5, 86.5)
L = math.hypot(75, 29); d = (75 / L, -29 / L); n = (-d[1], d[0])
def st(x, z): return ((x - C[0]) * d[0] + (z - C[1]) * d[1], (x - C[0]) * n[0] + (z - C[1]) * n[1])

FLOOR, ICE, ICE_FLOOR, CAVE, MARK = (35, 8), (35, 0), (35, 3), (35, 9), (35, 1)
floor_top = {}
for (x, y, z), b in full.items():
    if b == FLOOR and 10 <= y <= 40 and y > floor_top.get((x, z), -1): floor_top[(x, z)] = y

# our floor's edge along the cut, sampled by s; the turned edge is its mirror
edge_t, edge_h = {}, {}
for (x, z), y in floor_top.items():
    s, t = st(x, z)
    if t < 0 and -50 <= s <= 50:
        k = round(s)
        if t > edge_t.get(k, -99): edge_t[k], edge_h[k] = t, y
def smooth(table, s):
    ks = [k for k in table if abs(k - s) <= 4]
    return sum(table[k] for k in ks) / len(ks) if ks else None
def ours(s): return smooth(edge_t, s), smooth(edge_h, s)

def wobble(s, t, seed):
    """Low, irregular noise, the same at (s, t) and (-s, -t) so the result stays point-symmetric."""
    def one(a, b): return math.sin(0.23 * a + seed) * 0.8 + math.sin(0.11 * a - 0.4 * b + 2 * seed) * 0.6
    return (one(s, t) + one(-s, -t)) / 2

def gap_columns():
    cols = {}
    for x in range(5, 115):
        for z in range(45, 130):
            if (x, z) in floor_top: continue
            s, t = st(x, z)
            if abs(s) > 46: continue
            ta, ha = ours(s); tb, hb = ours(-s)
            if ta is None or tb is None: continue
            lo, hi = ta, -tb
            if lo - 1 <= t <= hi + 1:
                f = (t - lo) / max(1e-6, hi - lo)
                cols[(x, z)] = (s, t, ha + (hb - ha) * min(1, max(0, f)))
    return cols

def build(option):
    add = {}
    cols = gap_columns()
    for (x, z), (s, t, h) in cols.items():
        centre = 2.5 * math.sin(math.pi * s / 46)                     # odd in s: the crack wanders symmetrically
        half_w = 6.0 + 1.2 * math.cos(math.pi * s / 23) + wobble(s, t, 1.3)
        inside = abs(t - centre) < half_w
        a = abs(s)
        if option == "A": crack = inside and not (14 <= a <= 23)
        elif option == "B": crack = inside and a >= 15
        else: crack = abs(t - centre) < half_w + 2
        top = int(round(h + 0.6 * wobble(s, t, 4.1)))
        if not crack:
            add[(x, top, z)] = FLOOR; add[(x, top - 1, z)] = FLOOR
            continue
        if option == "C":                                              # a walkable ice floor, rising to the lane exits
            floor_y = int(round(7 + 9 * (a / 46) ** 2))
            add[(x, floor_y, z)] = ICE_FLOOR; add[(x, floor_y - 1, z)] = ICE_FLOOR
    # the crack's walls: every crack column next to solid ground gets an ice face down to its bottom
    crack_cols = {c for c in cols if not any((c[0], y, c[1]) in add and add[(c[0], y, c[1])] == FLOOR for y in range(5, 40))}
    for (x, z) in crack_cols:
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nb = (x + dx, z + dz)
            if nb in crack_cols: continue
            ground = max([y for (xx, y, zz), b in add.items() if (xx, zz) == nb and b == FLOOR] + [floor_top.get(nb, -1)])
            if ground < 0: continue
            bottom = 0 if option != "C" else int(round(7 + 9 * (abs(cols[(x, z)][0]) / 46) ** 2))
            for y in range(bottom, ground + 1):
                add.setdefault((x, y, z), ICE)
    if option == "C":                                                  # the crumbled spot in the lane's wall, joined to the crack
        path = [(81, z) for z in range(31, 60)] + [(x, 60) for x in range(73, 82)]
        for (x, z) in path:
            for w in (-1, 0, 1):
                cx, cz = (x + w, z) if path[0][0] == x and z < 60 else (x, z + w)
                add[(cx, 9, cz)] = CAVE; add[(cx, 14, cz)] = CAVE
                add[(119 - cx, 9, 173 - cz)] = CAVE; add[(119 - cx, 14, 173 - cz)] = CAVE
    return add

def render(world, path, box, iso_q=None, scale=3):
    x0, x1, z0, z1 = box
    blocks = {c: b for c, b in world.items() if x0 <= c[0] <= x1 and z0 <= c[2] <= z1}
    if iso_q is None:
        top = {}
        for (x, y, z), b in blocks.items():
            if (x, z) not in top or y > top[(x, z)][0]: top[(x, z)] = (y, b)
        cv = Canvas((x1 - x0 + 1) * scale + 40, (z1 - z0 + 1) * scale + 30, (247, 247, 244))
        for (x, z), (y, b) in top.items():
            rgb = col(*b) if b[0] != 22 else (40, 60, 200)
            f = 0.4 + 0.6 * y / 70
            for a in range(scale):
                for c2 in range(scale): cv.set((x - x0) * scale + 30 + a, (z - z0) * scale + 15 + c2, tuple(min(255, int(v * f)) for v in rgb))
        for g in range((x0 // 16) * 16, x1 + 1, 16):
            if g < x0: continue
            px = (g - x0) * scale + 30
            for yy in range(15, cv.height - 15, 3): cv.set(px, yy, (255, 0, 0))
            cv.text(px + 1, cv.height - 12, str(g), (200, 0, 0), 1)
        for g in range((z0 // 16) * 16, z1 + 1, 16):
            if g < z0: continue
            pz = (g - z0) * scale + 15
            for xx in range(30, cv.width, 3): cv.set(xx, pz, (255, 0, 0))
            cv.text(2, pz + 1, str(g), (200, 0, 0), 1)
        write_png(path, cv); return
    cb = {c: (col(*b) if b[0] != 22 else (40, 60, 200)) for c, b in blocks.items()}
    cb = turned(cb, iso_q); W, H, K = scale, scale // 2 or 1, scale
    sh = {c: cb[c] for c in _visible(cb)}
    u0, u1, v0, v1 = iso_bounds(sh, W, H, K)
    cv = Canvas(int(u1 - u0) + 40, int(v1 - v0) + 40, BACKGROUND)
    draw_iso(cv, sh, (20 - u0, 20 - v0), W, H, K); write_png(path, cv)

for option in "ABC":
    add = build(option)
    world = dict(full); world.update(add)
    pickle.dump(add, open(f"{S}/mid/option_{option}.pkl", "wb"))
    render(world, f"{S}/mid/opt{option}_top.png", (0, 120, 40, 135))
    render(world, f"{S}/mid/opt{option}_iso.png", (0, 120, 30, 145), iso_q=1, scale=4)
    sym = sum(1 for (x, y, z), b in add.items() if add.get((119 - x, y, 173 - z)) != b)
    print(option, len(add), "blocks; not mirrored by the turn:", sym)
