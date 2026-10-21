"""Greenery built block by block where the tree library is too large: a hedge of offset leaves, a small round oak,
and a field of flowers in rows.

    hedge(w, cells, ground, rng)              2 by 2 by 2 modules on a two-block grid along a line, each holding four
                                              leaves set diagonally across from each other, so it bends and climbs
    round_oak(w, x, z, ground, rng)           a trunk under a three by three core two deep, a 1 by 2 by 3 piece on
                                              each side with a corner bitten off now and then, a plus on top
    flower_rows(w, cells, ground, flowers)    rows of flowers across a shape, two rows a kind, every cell filled
"""
from pgmvox.core.blocks import B

LEAVES = (B.LEAVES, 4)                       # oak leaves that never decay


def hedge(w, cells, ground, rng, leaves=LEAVES, modules=1, drop=0.15, grass=False):
    """A hedge along `cells` (a line's cells, in order): each cell names the 2 by 2 module of the two-block grid
    it falls in, so the modules step diagonally where the line does. A module stands on the lowest ground under it
    and holds a checker of leaves, the lower course on one diagonal and the upper on the other, `modules` high;
    `drop` of its top leaves are left off so the crown is not ruled; with `grass`, tall grass stands in each gap
    the checker leaves, on the leaf or the ground under it, a cheat that holds while blocks do not update. Returns
    the columns it stands in."""
    seen, out = set(), []
    for x, z in cells:
        mx, mz = x // 2 * 2, z // 2 * 2
        if (mx, mz) in seen:
            continue
        seen.add((mx, mz))
        foot = min(ground(mx + a, mz + b) for a in (0, 1) for b in (0, 1))
        top = 2 * modules - 1
        for a in (0, 1):
            for b in (0, 1):
                for k in range(2 * modules):
                    if (a + b + k) % 2:
                        if grass and w.id(mx + a, foot + 1 + k, mz + b) == B.AIR:
                            w.set(mx + a, foot + 1 + k, mz + b, B.TALLGRASS, 1)
                        continue
                    if k == top and rng.random() < drop:
                        continue
                    for y in range(ground(mx + a, mz + b) + 1, foot + 1 + k):
                        if w.id(mx + a, y, mz + b) == B.AIR:       # down to the ground on a slope
                            w.set(mx + a, y, mz + b, *leaves)
                    w.set(mx + a, foot + 1 + k, mz + b, *leaves)
                out.append((mx + a, mz + b))
    return out


def round_oak(w, x, z, ground, rng, trunk=3, log=(B.LOG, 0), leaves=LEAVES, bite=0.35):
    """A small oak the way the game grows one: `trunk` logs, then a three by three core of leaves two deep with the
    log through it, a 1 by 2 by 3 piece against each side of the core (a corner of it bitten off with chance
    `bite`), and a plus of five on top. Returns its cells."""
    g = ground(x, z)
    y0 = g + 1 + trunk
    cells = set()

    def leaf(a, y, b):
        if w.id(a, y, b) == B.AIR:
            w.set(a, y, b, *leaves)
        cells.add((a, b))
    for dy in (0, 1):
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                leaf(x + a, y0 + dy, z + b)
        for sx, sz in ((2, 0), (-2, 0), (0, 2), (0, -2)):
            for k in (-1, 0, 1):
                a, b = (sx, k) if sx else (k, sz)
                if abs(k) == 1 and rng.random() < bite / 2:
                    continue
                leaf(x + a, y0 + dy, z + b)
    for a, b in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
        leaf(x + a, y0 + 2, z + b)
    for y in range(g + 1, y0 + 2):
        w.set(x, y, z, *log)
    return sorted(cells)


def flower_rows(w, cells, ground, flowers, along="x", rows=2, on=(B.GRASS,)):
    """Every cell of `cells` planted, in rows running `along` the axis, `rows` rows of each of `flowers` in turn, on
    whatever of `on` the ground is topped with. Returns the cells planted."""
    planted = []
    for x, z in cells:
        g = ground(x, z)
        if w.id(x, g, z) not in on or w.id(x, g + 1, z) != B.AIR:
            continue
        row = z if along == "x" else x
        w.set(x, g + 1, z, *flowers[(row // rows) % len(flowers)])
        planted.append((x, z))
    return planted
