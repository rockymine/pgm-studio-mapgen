"""Read Curio Square back from the built blocks.

1. THE PLOTS. Every plot's check, alone, by the plot kit: places to stand, the highest, out of sight; and that what
   stands in the square in its box is the same, block for block, as what the kit checked.
2. THE STREETS. Every street block is paving with nothing over it, so the plots never spill.
3. THE WALK. From the hiders' spawn, on foot: every plot's highest place reached in the square as it was alone.
4. THE VANISHING. Every block a plot set lies inside the plot's region that map.xml fills with air.
5. THE SPAWNS AND THE CAGE. The hiders' spawn is clear street; the cage is glass all round with room inside.

    python3 walk.py <build-dir>
"""
import os
import sys

import numpy as np

import gen as G
import plan as P
import plotkit as K
import render_iso
import sketch
import walk_core as W
from mc import World, B

HERE = os.path.dirname(os.path.abspath(__file__))


def main(build):
    x0w, z0w, ids, dat = render_iso.load(build)
    Y = P.STREET_Y
    out = []

    # 1. every plot alone, and the same blocks in the square
    lines, same, fails = [], 0, 0
    lay = sketch.layout()
    for (i, j), (builder, row) in sorted(lay.items()):
        path = os.path.join(HERE, "..", "plots", builder, row["file"]) if row else None
        if not path or not os.path.exists(path):
            lines.append(f"  plot {i},{j} {builder}: missing")
            fails += 1
            continue
        m = K.load(path)
        w = World(-4, -4, 19, 19, sy=Y - 60 + K.Y_MAX + 6)
        w.fill(-4, 0, -4, 14, 3, 14, B.STONE)
        c = K.draw(w, m, 0, 0, 4)
        r = K.check(w, 0, 0, 4, 4)
        bad = K.verdict(c, r, w, 0, 0, 4)
        fails += bool(bad)
        alone = w.ids[4:15, 3:4 + K.Y_MAX + 1, 4:15]
        x0, z0 = P.origin(i, j)
        here = ids[x0 - x0w:x0 - x0w + 11, Y - 1:Y + K.Y_MAX + 1, z0 - z0w:z0 - z0w + 11]
        same += int(np.array_equal(alone, here))
        lines.append(f"  {m.NAME:32s} {builder:7s} {m.KIND:9s} {r['spots']:4d} places, highest {r['top']:2d}, "
                     f"{r['hidden']:3d} out of sight  {'pass' if not bad else 'FAIL ' + bad[0]}")
    out.append(f"the plots: {len(lay)} placed, {len(lay) - fails} pass the kit alone, {same} identical in the square "
               f"block for block")
    out += lines

    # 2. the streets
    plot_mask = np.zeros(ids.shape[0:3:2], bool)
    for (i, j) in P.plots() + [P.CENTRE]:
        x0, z0 = P.origin(i, j)
        plot_mask[x0 - x0w:x0 - x0w + 11, z0 - z0w:z0 - z0w + 11] = True
    spill = 0
    for x in range(-P.HALF, P.HALF + 1):
        for z in range(-P.HALF, P.HALF + 1):
            if plot_mask[x - x0w, z - z0w]:
                continue
            if ids[x - x0w, Y:Y + 30, z - z0w].any() or ids[x - x0w, Y - 1, z - z0w] in (0, B.WATER):
                spill += 1
    out.append(f"the streets: {spill} street blocks with anything over them or no paving")

    # 3. the walk from the hiders' spawn
    sub = (slice(-P.HALF - x0w, P.HALF + 1 - x0w), slice(0, Y + 30), slice(-P.HALF - z0w, P.HALF + 1 - z0w))
    a = ids[sub]
    passable, water, ladder, solid = W.grid(a)
    st = W.standable(passable, water, solid)
    dist = W.bfs(st, ladder, water, passable, [(-8, Y, -8), (8, Y, 8)], -P.HALF, -P.HALF, jumps=True)
    lower = []
    for (i, j), (builder, row) in sorted(lay.items()):
        x0, z0 = P.origin(i, j)
        box = dist[x0 + P.HALF:x0 + P.HALF + 11, :, z0 + P.HALF:z0 + P.HALF + 11]
        top = int(np.argwhere(box >= 0)[:, 1].max()) - Y if (box >= 0).any() else -1
        alone = [ln for ln in lines if row and row["name"] in ln]
        want = int(alone[0].split("highest")[1].split(",")[0]) if alone else top
        if top < want:
            lower.append((row["name"] if row else (i, j), top, want))
    out.append(f"the walk from the hiders' spawn: every plot's highest place reached as alone, but for {lower}")

    # 4. every block a plot set lies in its fill region: the region is the plot's box from the street up
    outside = 0
    for (i, j) in P.plots():
        x0, z0 = P.origin(i, j)
        col = ids[x0 - x0w - 1:x0 - x0w + 12, Y + K.Y_MAX + 1:, z0 - z0w - 1:z0 - z0w + 12]
        outside += int(col.any())
    out.append(f"the vanishing: {outside} plots with anything above the top of their region (y {Y + K.Y_MAX + 1})")

    # 5. the spawns and the cage
    cx0, cy0, cz0, cx1, cy1, cz1 = G.CAGE
    shell = all(ids[x - x0w, y, z - z0w] == B.GLASS for x in range(cx0, cx1 + 1) for y in range(cy0, cy1 + 1)
                for z in range(cz0, cz1 + 1) if x in (cx0, cx1) or y in (cy0, cy1) or z in (cz0, cz1))
    inside = not ids[cx0 + 1 - x0w:cx1 - x0w, cy0 + 1:cy1, cz0 + 1 - z0w:cz1 - z0w].any()
    spawn_bad = 0
    for x0, z0, x1, z1 in ((-8, -8, 8, -7), (-8, 7, 8, 8), (-8, -6, -7, 6), (7, -6, 8, 6)):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if ids[x - x0w, Y, z - z0w] or ids[x - x0w, Y + 1, z - z0w] or not ids[x - x0w, Y - 1, z - z0w]:
                    spawn_bad += 1
    out.append(f"the spawns: {spawn_bad} hider spawn blocks not clear street; the cage glass all round: {shell}, "
               f"empty inside: {inside}")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1])
