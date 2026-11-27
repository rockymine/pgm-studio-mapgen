"""Design aid (not the construction): a smooth membrane over the cover's ground plan, from which build.py's lines are read."""
import sys, math, pickle
sys.path.insert(0, '.')
from common import *

def interp(pts, t):
    if t <= pts[0][0]: return pts[0][1]
    for (a, va), (b, vb) in zip(pts, pts[1:]):
        if t <= b: return va + (vb - va) * (t - a) / (b - a)
    return pts[-1][1]

WEST = -19
def zn(x): return -27 - (x - WEST) * 11 / 23 if x <= 4 else -38
def zs(x): return 44 + (x - WEST) if x <= -14 else 49 + (x + 14) / 21
RIM_W = [(-27, 71), (-18, 68), (-8, 66.5), (2, 67.5), (12, 65), (22, 66), (32, 63), (40, 61.5), (44, 58)]
def rim(x, z):
    if x == WEST: return interp(RIM_W, z)
    if z < -26: return interp([(WEST, 71), (4, 76)], x)
    return interp([(WEST, 58), (-14, 53)], x)

stair_roof = {c for c in roof if c[0] <= 7 and 32 <= c[1] <= 40}
roof = roof - stair_roof
for c in stair_roof: behind[c] = 59
D = set()
for x in range(WEST, 26):
    for z in range(-40, 52):
        c = (x, z)
        if z < zn(x) - 1e-9 or z > zs(x) + 1e-9: continue
        if c in roof or c in house: continue
        if c in terr and z < 41: continue
        if z >= 48 and x > 7: continue
        if z > 49: continue
        if z <= -23 and x > 16: continue
        if x >= 12 and not (-10 <= z <= -8 or 5 <= z <= 7 or z <= -23): continue
        D.add(c)
front = set()
for (x, y, z), (dx, dz) in kit.doorways().items():
    for k in range(4):
        front.add((x + dx * k, z + dz * k))
D -= {c for c in D if c[1] >= 42 and c[0] >= -6}
missing = [c for c in behind if c not in D]
print("behind not in D:", missing[:20], len(missing))
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
north_terr = {c: y for c, y in terr.items() if c not in D}
def cheb(c, S, r):
    return any((c[0] + dx, c[1] + dz) in S for dx in range(-r, r + 1) for dz in range(-r, r + 1))
fixed = {}
lo, hi = {}, {}
for c in D:
    x, z = c
    if c in behind: lo[c] = max(behind[c], terr.get(c, -99)) + 1.3
    elif c in terr: lo[c] = terr[c] + 0.7
    if 7 <= x <= 31 and 20 <= z <= 48: hi[c] = 60.4
    nb_t = [north_terr[(x + dx, z + dz)] for dx, dz in N4 if (x + dx, z + dz) in north_terr]
    nb_r = [1 for dx, dz in N4 if (x + dx, z + dz) in roof]
    edge = (x == WEST) or not all((x + dx, z + dz) in D or (x + dx, z + dz) in roof or (x + dx, z + dz) in house
                                   or (x + dx, z + dz) in north_terr or (x+dx, z+dz) in terr or x+dx >= 26 for dx, dz in N4)
    near_mtn = cheb(c, {k for k in north_terr if k[1] < 0}, 2)
    if nb_t and c in terr and z >= 41: fixed[c] = terr[c] + 0.6
    elif nb_t: fixed[c] = sum(nb_t) / len(nb_t)
    elif -25 <= z <= -22 and 6 <= x <= 15: fixed[c] = {-22: 61.5, -23: 65.0, -24: 67.0, -25: 69.0}[z]
    elif nb_r and -21 <= z <= 40: fixed[c] = 59.0
    elif cheb(c, roof, 3) and -19 <= z <= 40: fixed[c] = 59.0
    elif edge and x < 12: fixed[c] = rim(x, z) if (x == WEST or z < -20 or z > 40) else None
    if c in fixed and fixed[c] is None: del fixed[c]
fixed[(-7, 41)] = 57.3
fixed[(-7, 42)] = 54.3
H = {c: fixed.get(c, 62.0) for c in D}
order = sorted(D)
for it in range(2500):
    for c in order:
        if c in fixed: v = fixed[c]
        else:
            nb = [H[(c[0] + dx, c[1] + dz)] for dx, dz in N4 if (c[0] + dx, c[1] + dz) in H]
            nb += [north_terr[(c[0] + dx, c[1] + dz)] for dx, dz in N4 if (c[0] + dx, c[1] + dz) in north_terr]
            v = H[c] + 1.7 * (sum(nb) / len(nb) - H[c])
        if c in lo: v = max(v, lo[c])
        if c in hi: v = min(v, hi[c])
        H[c] = v
pickle.dump((D, H), open("design.pkl", "wb"))
enc = lambda v: '%2d' % (round(v) % 100)
print('    ' + ''.join('%3d' % x for x in range(WEST, 26)))
for z in range(-40, 52):
    print('%4d' % z + ''.join((' ' + enc(H[(x, z)])) if (x, z) in H else ('  R' if (x, z) in roof else '  H' if (x, z) in house else '  m' if (x, z) in terr else '   ') for x in range(WEST, 26)))
w = 0
for c in D:
    for dx, dz in ((1, 0), (0, 1)):
        n = (c[0] + dx, c[1] + dz)
        if n in H and abs(round(H[n]) - round(H[c])) >= 4: w += 1; print("wall", c, n, H[c], H[n])
print("walls", w)
