"""Read the built Lantern Pass back: walk it on the real blocks and measure sight through them.

1. THE RUN. From the boathouse, on foot, every drop allowed, sprint jumps over gaps of up to three: whether the
   door holds until the warm-up ends, how far the bell is, and how far each of the gorge's three crossings
   makes it when the other two are taken away.
2. THE SIDES. Nothing a runner reaches is on a walkway, and nothing a shooter reaches is on the lane.
3. SIGHT. For every place a runner reaches on the lane, the share of shooter positions within forty blocks that
   see the runner's body or head through the built blocks, by section, against the plan's figure.

    python3 walk.py <build-dir>
"""
import sys

import numpy as np

import gen as G
import plan as P
import plan_check as PC
import render_iso
import walk_core as W

RANGE = 40


def load(build):
    x0, z0, ids, dat = render_iso.load(build)
    return x0, z0, ids


def walker(ids, x0, z0):
    passable, water, ladder, solid = W.grid(ids)
    st = W.standable(passable, water, solid) | (ladder & passable)
    return st, passable, (lambda start: W.bfs(st, ladder, water, passable, start, x0, z0, jumps=True))


def opened(ids, x0, z0):
    ids = ids.copy()
    for bx0, by0, bz0, bx1, by1, bz1 in G.GATE_REGIONS["warmup"]:
        ids[bx0 - x0:bx1 - x0 + 1, by0:by1 + 1, bz0 - z0:bz1 - z0 + 1] = 0
    return ids


def without(ids, x0, z0, keep):
    """The gorge with only one crossing left: the others' walking surfaces taken out."""
    ids = ids.copy()
    g = P.GORGE
    zs = slice(g["z0"] - z0, g["z1"] - z0 + 1)
    if keep != "rope":
        ids[P.ROPE["x0"] - x0:P.ROPE["x1"] - x0 + 1, :, zs] = 0
    if keep != "pillars":
        for x, z, hh in P.PILLARS:
            ids[x - x0:x - x0 + 2, :, z - z0:z - z0 + 2] = 0
    if keep != "arch":
        ids[P.ARCH["x0"] - x0:P.ARCH["x1"] - x0 + 1, 20:40, zs] = 0
    return ids


def bell_dist(d, x0, z0):
    bx0, bx1, bz0, bz1 = P.BELL["box"]
    sub = d[bx0 - x0:bx1 - x0 + 1, P.BELL["y"] - 1:P.BELL["y"] + 3, bz0 - z0:bz1 - z0 + 1]
    v = sub[sub >= 0]
    return int(v.min()) if v.size else None


def spawn_cells():
    lx0, lx1 = P.LANE
    return [(x, 21, z) for x in range(lx0 + 4, lx1 - 2) for z in range(-8, 4)]


def sight(ids, x0, z0, reach):
    """The share of shooter positions that see each reached place on the lane, through the built blocks."""
    passable, water, ladder, solid = W.grid(ids)
    see_through = passable | water
    eyes = []
    for side, (a, b) in P.WALKS.items():
        xe = (b if side == "left" else a) + 0.5
        for z in range(P.Z_MIN + 2, P.Z_MAX - 1):
            eyes.append((xe, G.HW[P.iz(z)] + 1.62, z + 0.5))
    eyes = np.array(eyes)
    S = np.linspace(0.02, 0.97, 90)[None, :]
    out = {}
    lx0, lx1 = P.LANE
    xs, ys, zs = np.nonzero(reach)
    for i, y, k in zip(xs, ys, zs):
        x, z = int(i) + x0, int(k) + z0
        if not (lx0 <= x <= lx1 and P.Z_MIN <= z <= P.Z_MAX):
            continue
        tx, tz = x + 0.5, z + 0.5
        near = eyes[np.abs(eyes[:, 2] - tz) <= RANGE]
        seen = np.zeros(len(near), bool)
        for ty in (y + 0.9, y + 1.6):
            ex, ey, ez = near[:, 0:1], near[:, 1:2], near[:, 2:3]
            px, py, pz = ex + (tx - ex) * S, ey + (ty - ey) * S, ez + (tz - ez) * S
            ci = np.clip(np.floor(px).astype(int) - x0, 0, ids.shape[0] - 1)
            cy = np.clip(np.floor(py).astype(int), 0, ids.shape[1] - 1)
            cj = np.clip(np.floor(pz).astype(int) - z0, 0, ids.shape[2] - 1)
            own = (ci == i) & (cj == k)
            seen |= ~(~see_through[ci, cy, cj] & ~own).any(axis=1)
        out[(x, int(y), z)] = seen.mean()
    return out


def main(build):
    x0, z0, ids0 = load(build)
    out = []
    # the door holds for the warm-up
    _, _, wk = walker(ids0, x0, z0)
    d = wk(spawn_cells())
    out.append(f"before the warm-up ends, the runners reach the bell: {bell_dist(d, x0, z0)}; "
               f"leave the boathouse: {'yes' if (d[:, :, 6 - z0:] >= 0).any() else 'no'}")
    ids = opened(ids0, x0, z0)
    st, passable, wk = walker(ids, x0, z0)
    d = wk(spawn_cells())
    out.append(f"door open, the boathouse to the bell: {bell_dist(d, x0, z0)} blocks walked")
    for keep in ("rope", "pillars", "arch"):
        _, _, wk2 = walker(without(ids, x0, z0, keep), x0, z0)
        out.append(f"   with only the {keep} across the gorge: {bell_dist(wk2(spawn_cells()), x0, z0)}")
    # the sides
    reach = d >= 0
    on_walks = sum(int(reach[a - x0:b - x0 + 1].sum()) for a, b in P.WALKS.values())
    hw = int(G.HW[P.iz(-6)]) + 1
    shooters = [(x, hw, z) for a, b in P.WALKS.values() for x in range(a + 1, b) for z in range(-8, -3)]
    ds = wk(shooters)
    lx0, lx1 = P.LANE
    on_lane = int((ds[lx0 - x0:lx1 - x0 + 1] >= 0).sum())
    out.append(f"places on a walkway a runner reaches: {on_walks}; places on the lane a shooter reaches: {on_lane}")
    reach_s = ds >= 0
    span = [P.Z_MIN + 2 + int(np.nonzero(reach_s[a - x0:b - x0 + 1].any(axis=(0, 1)))[0].max() - (P.Z_MIN + 2 - z0))
            for a, b in P.WALKS.values()]
    out.append(f"the shooters walk each walkway from its spawn to z {span}: its whole length, to the temple")
    # sight, by section, against the plan
    vis = sight(ids, x0, z0, reach)
    out.append("section          sight, built (plan)")
    for key, name, za, zb in P.SECTIONS[1:]:
        v = [s for (x, y, z), s in vis.items() if za <= z <= zb]
        cs = PC.cells(lx0, lx1, za, zb)
        plan = np.mean([PC.VIS[c] for c in cs]) if cs else 0
        out.append(f"{key} {name:<14} {np.mean(v) if v else 0:4.0%} ({plan:4.0%})  over {len(v)} places")
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main(sys.argv[1])
