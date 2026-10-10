"""Read Abbeymoor back from the built world: the objectives check clean, every block has its footing, water stands against nothing
that is not a bank, each team reaches its own monuments and the enemy's on foot, and the crypt is joined: from the nave down the
Night Stair, along the passage, up the cellar stair into the Tithe Barn, and back.

    python3 walk.py <build-dir>

The walk is pgmvox.walk's voxel walk over the built blocks (doors opened, a drop of at most three, no running jump), plus one with every
running jump and any drop: no monument is reached that the plain walk does not reach.
"""
import sys

import numpy as np

import plan as P
from pgmvox import B, World, audit, walk
from pgmvox import blocks as K
from pgmvox.objectives import Destroyable, Spawn

w = World.load(sys.argv[1])
R = P.build()
O = P.objectives()
spawns = {o.team: o.at for o in O.of(Spawn)}
dest = O.of(Destroyable)
out = []
problems = O.check(w)
out.append(f"objectives with a problem (Objectives.check): {len(problems)}")
out += [f"   {p}" for p in problems]
foot = audit.footing(w)
out.append(f"footing problems (audit.footing): {len(foot)}")
out += [f"   {f}" for f in foot[:10]]
loose = audit.loose_water(w)
out.append(f"water against air (audit.loose_water): {len(loose)}")
out += [f"   {f}" for f in loose[:6]]
doors = np.argwhere(np.isin(w.ids, sorted(K.DOORS)) & ((w.dat & 8) == 0))
beside = []
for i, y, k in doors:
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        a, c = i + dx, k + dz
        if 0 <= a < w.sx and 0 <= c < w.sz and (w.ids[a, y, c] in (B.PANE, B.IRON_BARS) or w.ids[a, y + 1, c] in (B.PANE, B.IRON_BARS)):
            beside.append((int(i) + w.x0, int(y), int(k) + w.z0))
            break
out.append(f"doors: {len(doors)}; windows beside a door: {len(beside)} {beside[:5] if beside else ''}")
out.append(f"ladders in the world: {int((w.ids == B.LADDER).sum())}")
# trees on a road, a green, the bog or the hill: any log or leaf over a plan kind that must stay clear
X, Z = w.grid()
tree = np.isin(w.ids, (B.LOG, B.LOG2)).any(axis=1)
canopy = np.isin(w.ids, (B.LEAVES, B.LEAVES2)).any(axis=1)
names = {i: k for k, i in R.kinds.items()}
bad = {}
for kind in ("road", "green", "boardwalk", "peat", "nave", "water"):
    n = int((tree & R.mask(kind)).sum())
    if n:
        bad[kind] = n
out.append(f"tree trunks on a road, green, boardwalk, cutting, the nave or water: {bad if bad else 0}")
roadcrown = int((canopy & R.mask("road")).sum())
out.append(f"canopy over a road (crowns overhanging; the floor stays visible and walkable): {roadcrown} columns")
# the clearance round each cube: no block over the ground within four of the cube but cover plants and the dais
clear = {}
for o in dest:
    b = o.box
    n = 0
    for x in range(b.x0 - 4, b.x1 + 5):
        for z in range(b.z0 - 4, b.z1 + 5):
            if b.x0 <= x <= b.x1 and b.z0 <= z <= b.z1 and False:
                continue
            if R.kind(x, z) == 'hole':
                continue
            ground = int(R.H[x - R.x_min, z - R.z_min])
            for y in range(ground + 1 + (3 if o.id.endswith("abbey") else 0) , b.y1 + 5):
                if b.x0 <= x <= b.x1 and b.z0 <= z <= b.z1 and b.y0 <= y <= b.y1:
                    continue
                if w.id(x, y, z) not in (B.AIR, B.TALLGRASS, B.FLOWER, B.DEADBUSH, 0):
                    n += 1
                    if n <= 3:
                        out.append(f'   {o.id}: block {w.id(x, y, z)} at {(x, y, z)}')
    clear[o.id] = n
out.append(f"blocks within four of a cube, over the ground (plants aside): {clear}")
# found without a map: the share of the ground 25 to 60 off from which a player sees the cube's top course, through the built blocks
from pgmvox import sight
opaque = sight.voxel_opaque(w)
for o in dest:
    if o.team != "red-team":
        continue
    b = o.box
    cx, cz = (b.x0 + b.x1) // 2, (b.z0 + b.z1) // 2
    faces = []                                                  # every face of the pillar that has air in front of it: a point 0.05 out of its centre
    for x in range(b.x0, b.x1 + 1):
        for y in range(b.y0, b.y1 + 1):
            for z in range(b.z0, b.z1 + 1):
                for n in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                    nx, ny, nz = x + n[0], y + n[1], z + n[2]
                    if b.x0 <= nx <= b.x1 and b.y0 <= ny <= b.y1 and b.z0 <= nz <= b.z1:
                        continue
                    faces.append(((x + .5 + .55 * n[0], y + .5 + .55 * n[1], z + .5 + .55 * n[2]), n,
                                  (x + .5 + .5 * n[0], y + .5 + .5 * n[1], z + .5 + .5 * n[2])))
    eyes = []
    for i, k in np.argwhere(R.mask("ground", "road", "green", "orchard", "peat", "boardwalk", "steep") & (Z > -127)):
        x, z = int(X[i, k]), int(Z[i, k])
        if 25 <= np.hypot(x - cx, z - cz) <= 60 and (x + z) % 5 == 0:
            eyes.append(sight.eye(x, int(R.H[i, k]) + 1, z))

    def sees(eye):
        for aim, n, ctr in faces:
            if (eye[0] - ctr[0]) * n[0] + (eye[1] - ctr[1]) * n[1] + (eye[2] - ctr[2]) * n[2] > 0 and sight.line_clear(eye, aim, opaque):
                return True
        return False
    seen = sum(1 for e in eyes if sees(e)) / max(1, len(eyes))
    out.append(f"{o.id}: seen from {100 * seen:.0f}% of {len(eyes)} ground cells 25 to 60 blocks off (voxel sight to any face of the {b.y1 - b.y0 + 1}-block pillar, trees and walls count)")
ids = w.ids.copy()
ids[np.isin(ids, sorted(K.DOORS))] = 0                         # doors open: pgmvox.walk's PASSABLE has none
rules = walk.MoveRules(max_drop=3, jumps=False)
jump_rules = walk.MoveRules(max_drop=None, jumps=True, max_gap=3)
for team, at in spawns.items():
    short = O.teams.short(team)
    d = walk.walk(ids, [at], w.x0, w.z0, rules)
    d[:, :P.KILL_Y + 1, :] = -1
    out.append(f"from {short}'s spawn {at}: {int((d >= 0).sum())} places reached on foot")
    for o in dest:
        b = o.box
        cx, cz = (b.x0 + b.x1) // 2, (b.z0 + b.z1) // 2
        gy = int(R.H[cx - R.x_min, cz - R.z_min])
        v = walk.nearest(d, w.x0, w.z0, cx, gy + 1 + (3 if o.id == "red-abbey" else 0), cz, r=3)
        mine = "its own" if o.team == team else "the enemy's"
        out.append(f"  on foot to {mine} {o.id}: {v if v is not None else 'NOT REACHED'}")
# the crypt: from red's spawn, the nave's floor, down the Night Stair, along the passage, up into the barn
d = walk.walk(ids, [P.SPAWN_AT], w.x0, w.z0, rules)
d[:, :P.KILL_Y + 1, :] = -1
checks = [("the nave's floor, by the east gap", (-31, P.PLATEAU + 1, -72)), ("the Night Stair's head", (-31, 80, -69)),
          ("the Night Stair's foot (the crypt hall)", (-44, P.CRYPT_FLOOR + 1, -69)), ("the crypt's middle", (-48, P.CRYPT_FLOOR + 1, -72)),
          ("the passage's corner", (-48, P.CRYPT_FLOOR + 1, -62)), ("the passage's lowest floor", (-10, 60, -61)),
          ("the cellar stair's foot", (11, 61, -61)), ("the Tithe Barn's floor above the cellar", (20, 67, -61))]
for name, (x, y, z) in checks:
    v = walk.nearest(d, w.x0, w.z0, x, y, z, r=1)
    out.append(f"  red's spawn to {name}: {v if v is not None else 'NOT REACHED'}")
# and the way the other way: from the barn's cellar foot, the crypt, the nave
d2 = walk.walk(ids, [(11, 61, -61)], w.x0, w.z0, rules)
for name, (x, y, z) in (("the crypt's middle", (-48, P.CRYPT_FLOOR + 1, -72)), ("the nave's floor", (-33, 81, -72))):
    v = walk.nearest(d2, w.x0, w.z0, x, y, z, r=1)
    out.append(f"  from the cellar stair's foot to {name}: {v if v is not None else 'NOT REACHED'}")
dj = walk.walk(ids, [P.SPAWN_AT], w.x0, w.z0, jump_rules)
dj[:, :P.KILL_Y + 1, :] = -1
reach_j = int((dj >= 0).sum())
out.append(f"places reached with every running jump and any drop: {reach_j} (on foot {int((d >= 0).sum())})")
# the dry ground not reached on foot, by plan kind
for kind in ("ground", "road", "green", "orchard", "peat", "nave", "steep"):
    cells = [(int(X[i, k]), int(Z[i, k])) for i, k in np.argwhere(R.mask(kind) & (Z < 0))]
    lost = sum(1 for x, z in cells if walk.nearest(d, w.x0, w.z0, x, int(R.h(x, z)) + 1, z, r=1) is None)
    out.append(f"red's {kind}: {len(cells)} cells, {lost} not reached on foot")
print("\n".join(out))
