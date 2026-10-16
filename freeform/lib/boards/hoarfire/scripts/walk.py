"""Read Hoarfire back from the built world: the objectives check clean, every block has its footing, water stands
against nothing it should not, and the voxel walk (doors opened, a step of one, a running jump of three, no blocks
placed) reaches from Rowan's spawn every place the plan names on Rowan's half; then, building over the Rift, each
team reaches the enemy's goals. The goals' four-block clearance is counted, and Sloe's numbers are checked equal to
Rowan's.

    python3 walk.py <build-dir>
"""
import sys

import numpy as np

import land
import plan as P
from pgmvox import B, World
from pgmvox.read import audit, walk

w = World.load(sys.argv[1])
O = P.objectives()
out = []
problems = O.check(w)
out.append(f"objectives with a problem (Objectives.check): {len(problems)}")
out += [f"   {p}" for p in problems]
foot = audit.footing(w)
out.append(f"footing problems (audit.footing): {len(foot)}")
out += [f"   {f}" for f in foot[:8]]
loose = audit.loose_water(w)
out.append(f"water against air (audit.loose_water): {len(loose)}")
out += [f"   {f}" for f in loose[:6]]

X, Z = w.grid()
bz = (X >= P.BUILD_ZONE[0]) & (X <= P.BUILD_ZONE[2]) & (Z >= P.BUILD_ZONE[1]) & (Z <= P.BUILD_ZONE[3])
foot_rules = walk.MoveRules(max_drop=None, kill_y=P.KILL_Y)
build_rules = walk.MoveRules(max_drop=None, kill_y=P.KILL_Y, build=(bz, (P.KILL_Y + 6, 75)))


def feet(p):
    return (p[0], p[1], p[2])


def img(p):
    x, z = P.SYM.point(p[0], p[2])
    return (x, p[1], z)


red = feet(P.SPAWN_AT)
blue = img(red)
MB, CB = P.MONUMENT_BOX, P.CORE_BOX
mon = ((MB.x0 + MB.x1) // 2, land.SHELF + 1, (MB.z0 + MB.z1) // 2)
pit = (land.CORE[0], int(P.H[land.CORE[0] - w.x0, land.CORE[1] - w.z0]) + 1, land.CORE[1])
TARGETS = {
    "Rime Monument (on the shelf under it)": (mon, 3),
    "Ember Pit (under the core)": (pit, 3),
    "the snout's top, over the monument": ((-47, 0, -64), 3),
    "Kiln Hill's crown": ((land.KILN_HILL[0], 0, land.KILN_HILL[1]), 3),
    "the Rime Tarn's ice": ((land.TARN_AT[0], land.TARN_ICE + 1, land.TARN_AT[1]), 2),
    "the Ice Cave's ledge in the Rift's cliff": ((P.CAVE[-1][0], P.CAVE[-1][2] + 1, P.CAVE[-1][1] + 1), 2),
    "the Thaw Bridge": ((0, 0, -48), 2),
    "the Hollow Way's foot at the brink": ((land.HOLLOW[1][0], 0, land.HOLLOW[1][1]), 2),
    "the barn's door": ((27, land.HAMLET_Y + 1, -77), 2),
    "the Ice Hut (inside, at its stove)": ((-62, 52, -40), 1),
    "the falls' headland": ((1, 0, -16), 3),
}


def ground_y(x, z):
    ys = np.nonzero(~np.isin(w.ids[x - w.x0, :, z - w.z0], (0, B.SNOW_LAYER, B.TALLGRASS, B.LEAVES, B.LEAVES2)))[0]
    return int(ys.max()) + 1 if len(ys) else 0


def reached(dist, p, r):
    x, y, z = p
    if y == 0:
        y = ground_y(x, z)
    best = None
    for dy in range(-3, 4):
        n = walk.nearest(dist, w.x0, w.z0, x, y + dy, z, r)
        if n is not None and (best is None or n < best):
            best = n
    return best


d_red = walk.walk(w.ids, [red], w.x0, w.z0, foot_rules)
d_blue = walk.walk(w.ids, [blue], w.x0, w.z0, foot_rules)
out.append("on foot from each spawn, no blocks placed (moves; Sloe's to the image of each place):")
for name, (p, r) in TARGETS.items():
    a = reached(d_red, p, r)
    b = reached(d_blue, img(p) if p[1] else (P.SYM.point(p[0], p[2])[0], 0, P.SYM.point(p[0], p[2])[1]), r)
    out.append(f"   {name:<46} Rowan {a!s:>5}   Sloe {b!s:>5}")
db_red = walk.walk(w.ids, [red], w.x0, w.z0, build_rules)
out.append("building over the Rift (moves; the enemy's goals):")
emon, epit = img(mon), img(pit)
out.append(f"   Rowan to Sloe's monument {reached(db_red, emon, 3)}, to Sloe's Ember Pit {reached(db_red, epit, 3)}")
db_blue = walk.walk(w.ids, [blue], w.x0, w.z0, build_rules)
out.append(f"   Sloe to Rowan's monument {reached(db_blue, mon, 3)}, to Rowan's Ember Pit {reached(db_blue, pit, 3)}")
crossing = walk.walk(w.ids, [red], w.x0, w.z0, walk.MoveRules(max_drop=None, kill_y=P.KILL_Y))
out.append(f"   Rowan reaches Sloe's half without building: {reached(crossing, img(TARGETS['the Thaw Bridge'][0] if False else (0, 0, -48)) if False else (0, ground_y(0, 47), 47), 3) is not None}")
# the clearance: nothing built or grown within four blocks of a goal, over the ground
for name, box in (("monument", MB), ("core", CB)):
    n = 0
    for x in range(box.x0 - 4, box.x1 + 5):
        for z in range(box.z0 - 4, box.z1 + 5):
            g = ground_y(x, z)
            for y in range(max(g, 1), box.y1 + 5):
                if box.x0 <= x <= box.x1 and box.z0 <= z <= box.z1 and box.y0 <= y <= box.y1:
                    continue
                if w.id(x, y, z) not in (0, B.SNOW_LAYER, B.TALLGRASS, B.FLOWER, B.DANDELION, B.CARPET):
                    n += 1
    out.append(f"blocks within four of the {name}, over the ground: {n}")
# trunks on a path
logs = np.isin(w.ids, (B.LOG, B.LOG2)).any(axis=1)
from pgmvox.geom import shapes  # noqa: E402
onpath = np.zeros(X.shape, bool)
for pts in P.PATHS.values():
    onpath |= shapes.polyline(X, Z, pts)[0] <= 1.5
a, b, c, d = P.BRIDGE
deck = (X >= a - 1) & (X <= c + 1) & (Z >= b) & (Z <= d)
out.append(f"columns of path with a log over them, the bridge's rails aside: {int((logs & onpath & (Z < 0) & ~deck).sum())}")
print("\n".join(out))
