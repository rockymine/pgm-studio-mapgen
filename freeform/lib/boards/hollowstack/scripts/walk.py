"""Read Hollowstack back from the built world: footing and water; every place a player stands in the laid passages
and the air over it; each team's walk to its own monuments and to the enemy's, bridging the chasm where it must;
and the ways between the storeys the plan names.

    python3 walk.py <build-dir>
"""
import json
import os
import sys

import numpy as np

import layout as L
import objectives as P
import passages
import places
from pgmvox import B, World
from pgmvox.play.objectives import Destroyable, Spawn
from pgmvox.read import audit
from pgmvox.read.walk import MoveRules, nearest, standing, walk

w = World.load(sys.argv[1])
O = P.objectives()
print(f"footing problems: {len(audit.footing(w))}; water against air: {len(audit.loose_water(w))}")

st, _ = standing(w.ids)
reach = walk(w.ids, [L.SPAWN], w.x0, w.z0, MoveRules(max_drop=3, jumps=False))
OPEN = (B.AIR, B.TORCH, B.RAIL, B.LADDER, B.COBWEB, B.VINE)
taken = json.load(open(os.path.join(sys.argv[1], "segments.json")))
for name, spec in (("Undercroft", L.UNDERCROFT), ("Workings", L.WORKINGS)):
    g = passages.grid_of(spec)
    low3, low4, spots = [], 0, 0
    for i, j, l in taken[name]:
        x0, y0, z0 = g.corner(i, j, l)
        for x in range(x0 + 1, x0 + g.cell - 1):
            for z in range(z0 + 1, z0 + g.cell - 1):
                for y in range(y0 + 1, y0 + g.height):
                    ii, kk = x - w.x0, z - w.z0
                    if not st[ii, y, kk] or reach[ii, y, kk] < 0:
                        continue
                    clear = 0
                    while y + clear < L.SY - 1 and w.ids[ii, y + clear, kk] in OPEN:
                        clear += 1
                    spots += 1
                    if clear < 3:
                        low3.append((x, y, z))
                    low4 += clear == 3
    print(f"{name}: {spots} places a player reaches in its cells; with under three blocks of air over them "
          f"{len(low3)} {low3[:4]}, with three {low4}")

X, Z = w.grid()
chasm = (X >= -L.FACE) & (X <= L.FACE - 1)
foot = MoveRules(max_drop=3, jumps=False)
built = MoveRules(max_drop=3, jumps=False, build=(chasm, (8, 112)))
spawns = {o.team: o.at for o in O.of(Spawn)}
mons = O.of(Destroyable)


def under(m):
    b = m.box
    return (b.x0, b.y0 - 3, b.z0)                                  # the floor under the floating monument


for team, at in spawns.items():
    d0 = walk(w.ids, [at], w.x0, w.z0, foot)
    d1 = walk(w.ids, [at], w.x0, w.z0, built)
    for m in mons:
        own = m.team == team
        n = nearest(d0 if own else d1, w.x0, w.z0, *under(m), r=2)
        print(f"{team:9} to {m.id:11} ({'own, on foot' if own else 'enemy, bridging the chasm'}): "
              f"{n if n is not None else 'not reached'}")


def via(points, rules):
    total = 0
    for a, b in zip(points, points[1:]):
        d = walk(w.ids, [a], w.x0, w.z0, rules)
        n = nearest(d, w.x0, w.z0, *b, r=2)
        if n is None:
            return None, (a, b)
        total += n
    return total, None


uc, wk = passages.grid_of(L.UNDERCROFT), passages.grid_of(L.WORKINGS)
gx, gy, gz = uc.centre(*L.GATEHOUSE, 3)
F = L.UNDERWOOD_FLOORS
VAULT_WOOL = P.vault_at()
WAYS = {
    "keep well, the yard down into the Workings": [L.SPAWN, wk.centre(12, L.KEEP_WELL[1], 0)],
    "keep well, the yard down into the Undercroft": [L.SPAWN, uc.centre(12, L.KEEP_WELL[1], 1)],
    "descent cave, the Workings down into the Underwood": [wk.centre(4, 7, 0), (57, 61, -11)],
    "gatehouse, the Underwood's court down into the Undercroft": [(gx - 4, gy, gz), uc.centre(6, 3, 1)],
    "stair, the Undercroft's lower level up to its upper": [uc.centre(3, 3, 0), uc.centre(6, 3, 1)],
    "deep well, the Undercroft down into the grotto": [uc.centre(13, 6, 0), (76, 22, 9)],
    "Underwood mouth to the shrine": [(30, F["mid"] + 1, 0), places.shrine_room()[:3]],
    "postern, the keep well into the Underwood's back": [uc.centre(12, L.KEEP_WELL[1], L.POSTERN_LEVEL), (58, 60, -3)],
    "Undercroft's upper balcony to the vault's monument": [uc.centre(0, 0, 1), VAULT_WOOL],
    "the gallery on the chasm to the vault's monument": [uc.centre(1, 3, 0), VAULT_WOOL],
    "Workings' gallery out to its timber stage": [wk.centre(0, 1, 0), (L.FACE, L.WORKINGS["y0"] + 1, -13)],
}
for name, pts in WAYS.items():
    n, leg = via(pts, foot)
    print(f"way {name}: {n if n is not None else f'broken between {leg[0]} and {leg[1]}'}")
void = w.ids[:, 0, :] == 0
for name, start in (("the Deep's hall", (40, L.DEEP["floor"] + 1, -12)), ("the Underwood's mouth", (30, F["mid"] + 1, 0)),
                    ("the gallery", uc.centre(1, 3, 0)), ("the Workings", wk.centre(0, 1, 0))):
    d = walk(w.ids, [start], w.x0, w.z0, foot)
    edge = [(d[i, y, k], i + w.x0, y, k + w.z0) for i, y, k in np.argwhere(d >= 0)
            if i > 0 and void[i - 1, k] and i + w.x0 < 30]
    print(f"{name} out onto the chasm's face: {min(edge)[0] if edge else 'not reached'}")
for name, (x, z, r) in (("light well", L.LIGHT_WELL), ("Root Well", L.ROOT_WELL), ("plunge", L.PLUNGE)):
    col = w.ids[x - w.x0, :, z - w.z0]
    rim = w.ids[x + int(r) + 2 - w.x0, :, z - w.z0]                # the ground at the drop's rim
    top = max(y for y in range(L.SY) if rim[y] not in (B.AIR,) and rim[y] not in (B.LEAVES, B.LEAVES2, B.TALLGRASS))
    if name == "Root Well":
        top = F["mouth"]                                           # it opens in the Underwood's floor
    pool = [y for y in range(1, top) if col[y] == B.WATER and col[y + 1] == B.AIR]
    print(f"{name}: water at the foot of its drop {"yes, y " + str(max(pool)) if pool else "NO"}; "
          f"its top y {top}, a fall of {top - max(pool) if pool else "?"}")
drops = MoveRules(max_drop=None, jumps=False)
for team, at in spawns.items():
    d = walk(w.ids, [at], w.x0, w.z0, drops)
    for m in mons:
        if m.team == team:
            n = nearest(d, w.x0, w.z0, *under(m), r=2)
            print(f"{team:9} to {m.id:11} (own), taking the drops into water: {n}")
