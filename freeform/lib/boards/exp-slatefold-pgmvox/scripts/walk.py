"""Read Slatefold back from the built world: the objectives check clean, every block has its footing, and each team
reaches its own monuments on foot and the enemy's rooms by building (and not otherwise).

    python3 walk.py <build-dir>

Two walks from each spawn, pgmvox.walk's voxel walk (doors opened, a drop of at most three, no running jump), plus one with
every running jump on and nothing built:

    on foot     the world as built: the own monuments, every place of the board, and the rooms (not reached: the walls)
    jumps       the same with running jumps: no room is reached, so no jump skips a wall
    building    every build zone's void, from the kill height to the build height, filled with water: a stand-in for "a
                player may build anywhere here", since the walk swims up and across water; and the bedrock walls' tops
"""
import sys

import numpy as np

import plan as P
from pgmvox import B, World, audit, walk
from pgmvox import blocks as K
from pgmvox.objectives import DYES, Spawn, Wool

w = World.load(sys.argv[1])
R = P.build()
O = P.objectives()
spawns = {o.team: o.at for o in O.of(Spawn)}
wools = O.of(Wool)
out = []
problems = O.check(w)
out.append(f"objectives with a problem (Objectives.check): {len(problems)}")
out += [f"   {p}" for p in problems]
missing = [o.color for o in wools if w.get(*o.found) != (B.WOOL, DYES[o.color])]
out.append(f"wools missing from their rooms: {len(missing)} {missing if missing else ''}")
foot_all = audit.footing(w)
outline = [f for f in foot_all if f[1] == 1 and "block 55" in f[3]]          # the build area's redstone outline, at y 1 over the void
foot = [f for f in foot_all if f not in outline]
out.append(f"footing problems (audit.footing): {len(foot)} (and {len(outline)} redstone outline blocks at y 1, over air by design)")
out += [f"   {f}" for f in foot[:10]]
loose = audit.loose_water(w)
out.append(f"water against air (audit.loose_water): {len(loose)}")
# the studio's chests: every wool room has its eight, every wall its two
chests = [t for t in w.tiles if t.get("kind") == "Chest"]
out.append(f"chests: {len(chests)}")

# a window beside a door: any pane or iron bar edge-adjacent to a door block, on the door's rows
doors = np.argwhere(np.isin(w.ids, sorted(K.DOORS)) & ((w.dat & 8) == 0))
beside = []
for i, y, k in doors:
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        a, c = i + dx, k + dz
        if 0 <= a < w.sx and 0 <= c < w.sz and w.ids[a, y, c] in (B.PANE, B.IRON_BARS) or (0 <= a < w.sx and 0 <= c < w.sz and w.ids[a, y + 1, c] in (B.PANE, B.IRON_BARS)):
            beside.append((int(i) + w.x0, int(y), int(k) + w.z0))
            break
out.append(f"doors: {len(doors)}; windows beside a door: {len(beside)} {beside[:5] if beside else ''}")
ladders = int((w.ids == B.LADDER).sum())
out.append(f"ladders in the world: {ladders}")
chest_at = sorted((t["x"], t["y"], t["z"]) for t in chests if t["z"] < 0)
out.append(f"red's chests: {len(chest_at)}: " + ", ".join(map(str, chest_at)))
# every platform: the share of its non-rim columns with a bedrock course six under the floor, and the root under it
from pgmvox.shapes import edge_depth
land = ~R.mask("void")
ed = edge_depth(land & (np.arange(R.nz)[None, :] + R.z_min < 0))
for kind in ("spawn", "row", "yard", "front", "quarry", "landing", "bench"):
    cells = [(i, kk) for i, kk in np.argwhere(R.mask(kind) & ((np.arange(R.nz)[None, :] + R.z_min) < 0) & (ed > 0))]
    have = sum(1 for i, kk in cells if w.ids[i, int(R.base[i, kk]) - 6, kk] == B.BEDROCK)
    out.append(f"platform {kind}: {have} of {len(cells)} non-rim columns carry bedrock at floor - 6")
# trees: no crown over a flight or a landing, no trunk standing in a paved lane (house posts and sheds' posts excluded: only leaves count)
crown = np.isin(w.ids, (B.LEAVES, B.LEAVES2)).any(axis=1)
over = crown & R.mask("stair", "landing")
cells = [(int(i) + w.x0, int(kk) + w.z0) for i, kk in np.argwhere(over)]
out.append(f"tree crowns over a flight or a landing: {len(cells)} columns {cells[:6] if cells else ''}")

# revision 1 read-backs ------------------------------------------------------------------------------------------
# (a) the longest straight run of fence anywhere (a fence is a spruce fence or a cobble wall, x or z)
FENCE_IDS = sorted(K.FENCES | {B.COBBLE_WALL})
fence = np.isin(w.ids, FENCE_IDS)
longest = (0, None)
for axis in (0, 2):
    for y in range(w.sy):
        plane = fence[:, y, :] if axis == 0 else fence[:, y, :].T
        for a, row in enumerate(plane):
            run = 0
            for b, v in enumerate(row):
                run = run + 1 if v else 0
                if run > longest[0]:
                    longest = (run, (int(a + (w.x0 if axis == 0 else w.z0)), y, int(b + (w.z0 if axis == 0 else w.x0)), "x" if axis == 0 else "z"))
out.append(f"longest straight run of fence or wall-post blocks: {longest[0]} ending at {longest[1]}")
# (b) wool-room, monument and every other objective: the nearest boulder-like thing (an oven, a heap, an iron outcrop, a stack of slate)
objs = [("magenta monument", -15, -86), ("yellow monument", 15, -86), ("kiln wool", 60, -68), ("kiln door", 54, -68),
        ("winding wool", -76, -91), ("winding door", -71, -91)]
boulders = [("oven", 49, -76), ("oven", 49, -58)] + [("heap", x, z) for x, z, *_ in P.HEAPS] + [("iron", -20, -103), ("iron", 18, -103)] + \
           [("slate stack", x, z) for x, z in ((14, -30), (-12, -22), (8, -22), (-18, -31), (35, -76), (53, -57), (41, -75))]
for name, x, z in objs:
    d, b = min((((x - bx) ** 2 + (z - bz) ** 2) ** 0.5, kind) for kind, bx, bz in boulders if bz < 0 and (z < 0))
    out.append(f"nearest boulder-like object to the {name} ({x}, {z}): {b} {d:.1f} blocks")
# (c) a tree block over any house: a leaf or log within the roofs' cells above the eave
roofs = np.isin(w.ids, (B.STONEBRICK_STAIRS,))
trunk = np.isin(w.ids, (B.LOG, B.LOG2))
out.append("leaf blocks resting directly on a stone-brick stair (a tree on a roof): " +
           str(int((np.isin(w.ids[:, 1:, :], (B.LEAVES, B.LEAVES2)) & roofs[:, :-1, :]).sum())))
# (d) the bedrock wall's depth: the lowest bedrock block in each wall column above the kill height
for name, (x0, x1, z0, z1) in (("gantry wall", (28, 29, -60, -55)), ("path wall", (-60, -59, -85, -79))):
    lows = []
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            col = np.flatnonzero(w.ids[x - w.x0, :, z - w.z0] == B.BEDROCK)
            lows.append(int(col.min()))
    out.append(f"{name}: bedrock from y {min(lows)} to {max(lows)} at the foot, top {P.WALL_G['height'] and ''}")
# (e) the green share of the top surface per terrace: grass over all the red half's walkable top blocks
tops = {}
for kind in ("spawn", "row", "yard", "front", "bench", "quarry"):
    m = R.mask(kind) | (R.piece == R.kinds[kind]) if hasattr(R, "piece") else R.mask(kind)
    cells = [(i, kk) for i, kk in np.argwhere(m & ((np.arange(R.nz)[None, :] + R.z_min) < 0))]
    g = 0
    for i, kk in cells:
        y = w.top(i + w.x0, kk + w.z0)
        g += w.ids[i, y, kk] in (B.GRASS,)
    out.append(f"top blocks that are grass, {kind}: {g} of {len(cells)}")

ids = w.ids.copy()
ids[np.isin(ids, sorted(K.DOORS))] = 0                         # doors open: pgmvox.walk's PASSABLE has none
wb = World(w.x0, w.z0, w.sx, w.sz, w.sy)
wb.ids, wb.dat = ids.copy(), w.dat.copy()
zm = P.zone_mask(R)
for i, k in np.argwhere(zm):
    col = wb.ids[i, P.KILL_Y + 1:P.MAX_BUILD + 1, k]
    col[col == B.AIR] = B.WATER
for i, kk in np.argwhere(R.mask("barrier")):                    # a wall built over: its three courses are water for the swimmer
    floor_y = int(R.base[i, kk])
    wb.ids[i, floor_y + 1:int(R.H[i, kk]) + 1, kk] = B.WATER
foot_rules = walk.MoveRules(max_drop=3, jumps=False)
jump_rules = walk.MoveRules(max_drop=None, jumps=True, max_gap=3)
for team, at in spawns.items():
    short = O.teams.short(team)
    d = walk.walk(ids, [at], w.x0, w.z0, foot_rules)
    d[:, :P.KILL_Y + 1, :] = -1
    out.append(f"from {short}'s spawn {at}: {int((d >= 0).sum())} places reached on foot")
    for o in wools:
        if o.team == team:
            v = walk.nearest(d, w.x0, w.z0, o.slot[0], o.slot[1] + 0, o.slot[2], r=2)
            out.append(f"  on foot to its own {o.color} monument: {v if v is not None else 'NOT REACHED'}")
    for o in wools:
        if o.team != team:
            v = walk.nearest(d, w.x0, w.z0, *o.found, r=2)
            out.append(f"  on foot into its own {o.color} room (the keepers'): {v if v is not None else 'not reached (the wall)'}")
    dj = walk.walk(ids, [at], w.x0, w.z0, jump_rules)
    dj[:, :P.KILL_Y + 1, :] = -1
    for o in wools:
        v = walk.nearest(dj, w.x0, w.z0, *o.found, r=2)
        out.append(f"  with every running jump, no building, to the {o.color} room: {v if v is not None else 'not reached (no jump skips a wall)'}")
    db = walk.walk(wb.ids, [at], wb.x0, wb.z0, foot_rules)
    db[:, :P.KILL_Y + 1, :] = -1
    for o in wools:
        if o.team == team:
            v = walk.nearest(db, w.x0, w.z0, *o.found, r=2)
            out.append(f"  building, to the enemy's {o.color} room: {v if v is not None else 'NOT REACHED'}")
    # every named place of the board reached on foot, from this spawn
    for name, (x, z) in P.PLACES:
        if (z < 0) == (team == "red-team"):
            y = int(R.base[R.ix(x), R.iz(z)])
            v = walk.nearest(d, w.x0, w.z0, x, y + 1, z, r=3)
            if v is None:
                out.append(f"  place not reached on foot: {name} ({x}, {z})")
# every walkable terrace cell of red's half is reached from red's spawn on foot, apart from the rooms' insides
d = walk.walk(ids, [spawns["red-team"]], w.x0, w.z0, foot_rules)
d[:, :P.KILL_Y + 1, :] = -1
X, Z = w.grid()
for kind in ("spawn", "row", "yard", "front", "landing", "bench", "quarry", "pit"):
    m = R.mask(kind) & (Z < 0)
    cells = [(int(X[i, k]), int(Z[i, k])) for i, k in np.argwhere(m)]
    lost = 0
    for x, z in cells:
        y = int(R.h(x, z)) + 1
        if walk.nearest(d, w.x0, w.z0, x, y, z, r=1) is None:
            lost += 1
    out.append(f"red's {kind}: {len(cells)} cells, {lost} not reached on foot")
print("\n".join(out))
