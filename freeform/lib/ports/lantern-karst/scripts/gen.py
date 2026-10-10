"""Generate Lantern Karst from the plan: red's half (z < 0) is built, then turned half a circle onto blue's
(orient.turn_world); the objectives are stamped on both halves from their objects; the mist, the karst towers
and the build area's redstone outline are laid over both halves with no symmetry.

Every island is its plan floor at its height, exactly, so the gaps the plan measured are the gaps in the world.
Under the floor, by terrain.lay per floor height: grass, a block of dirt, four of rock in beds (terrain.Strata);
the bedrock course six under the floor, under all but the island's rim; and the root below it, a karst cone
fluted and spired (terrain.root_depth, terrain.underside) down into the mist, no lower than 26.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np

import plan  # noqa: F401  (puts the library on the path)
import dress as D
from plan import (FOUNDATION, KILL_Y, MAX_BUILD, MIST_Y, OBSERVER_AT, WALL, X_MAX, X_MIN, Z_MAX, Z_MIN, build,
                  objectives, zone_mask)
from pgmvox import B, World, forms, noise, rng
from pgmvox import terrain as T
from pgmvox.objectives import Wool
from pgmvox.orient import turn_world
from pgmvox.shapes import edge_depth

BOARD = "lantern-karst"
ROOT_FLOOR = 26                          # the deepest a root hangs, inside the mist


def strata():
    """The karst's beds: stone carrying andesite courses, dark beds of cyan clay (dark grey in 1.8), a pale bed of
    light grey clay; one rock read in several tones."""
    return T.Strata([((B.STONE, 0), 0.42, 3), ((B.STONE, 5), 0.25, 2), ((B.STAINED_CLAY, 9), 0.18, 2),
                     ((B.STAINED_CLAY, 8), 0.15, 1)], seed=13, start=0)


def islands(w, g, beds, offset, r):
    """The rock of every island on red's half: lay per floor height, the bedrock course, the root."""
    land = g.land
    fill = T.beds(beds, offset, flecks=[((B.STONE, 0), (B.COBBLE, 0), 0.06), ((B.STONE, 5), (B.GRAVEL, 0), 0.02)],
                  seed=6)
    root = T.root_depth(land, cone=3.2, power=0.85, rough=0.35, flutes=4.5, spires=9, seed=11)
    root = np.minimum(root, np.maximum(g.floor - FOUNDATION - ROOT_FLOOR, 1))
    T.slab(w, g.floor, land, fill, root, r, plate=5, foundation=FOUNDATION, dirt_depth=1,
           paint=lambda k, x, z, h: beds(h - 5 - k - int(offset[x - w.x0, z - w.z0])),
           rim=((B.MOSSY, 0), 0.18))                              # the course, and moss on the rim's faces


def skirt(w, g, beds, r):
    """Karst faces, not box sides: rock bulges out under the rim as ledges (never above floor - 2, so the walked
    top and the plan's gaps are untouched), and the face is cut back where the noise is low."""
    from scipy import ndimage
    land = g.land
    near = ndimage.distance_transform_edt(~land)
    Hn = ndimage.maximum_filter(np.where(land, g.floor, -1), size=5)
    bulge = noise.fbm(land.shape, 5, 2, seed=15)
    X, Z = w.grid()
    out = ~land & g.red & (near <= 2.2) & (Hn >= 0)
    for i, k in np.argwhere(out):
        b = bulge[i, k]
        reach = (b > 0.05) + (b > 0.3)
        if near[i, k] > reach:
            continue
        x, z, h = int(X[i, k]), int(Z[i, k]), int(Hn[i, k])
        top = h - 2 - int(near[i, k]) - (b < 0.2)
        bot = h - 6 - int(4 * max(0, b)) - int(r.integers(0, 3))
        for y in range(bot, top + 1):
            w.set(x, y, z, *((B.MOSSY, 0) if r.random() < 0.12 else beds(y)))
        if r.random() < 0.5 and w.id(x, top + 1, z) == B.AIR:
            w.set(x, top + 1, z, B.TALLGRASS, 2 if r.random() < 0.5 else 1)
    rim = land & (edge_depth(land) == 0) & (bulge < -0.25) & ~np.isin(g.piece, [g.R.kinds["pillar"],
                                                                              g.R.kinds["store"]])
    for i, k in np.argwhere(rim):
        x, z, h = int(X[i, k]), int(Z[i, k]), int(g.floor[i, k])
        for y in range(h - 5, h - 2):
            w.set(x, y, z, B.AIR)


def markers(w, R):
    """Block 36 at y 0 under every column a player may build in: land and build zones, both halves."""
    build_cols = ~R.mask("void") | zone_mask(R)
    w.ids[:, 0, :][build_cols] = 36
    return int(build_cols.sum())


def outline(w, R):
    """The build area's outline as the studio stamps it (rules.md ST5): unpowered redstone at y 1, two out from
    every void-facing edge of a build zone, one clear of the zones and of anything standing in play, turning
    into each other at a convex corner. Both halves."""
    from scipy import ndimage
    zone = zone_mask(R)
    zfull = zone | (~R.mask("void") & np.isin(R.K, [R.kinds[k] for k in ("w-1", "w-2", "w-3", "w-4", "e-1", "e-2",
                                                                        "bell")]))
    terr = (w.ids[:, KILL_Y:100, :] != 0).any(axis=1)
    nx, nz = zone.shape
    sides = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    marker = set()
    for i, k in np.argwhere(zfull):
        fv = [0 <= i + dx < nx and 0 <= k + dz < nz and not zfull[i + dx, k + dz] and not terr[i + dx, k + dz]
              for dx, dz in sides]
        for s, (dx, dz) in enumerate(sides):
            if fv[s]:
                marker.add((i + 2 * dx, k + 2 * dz))
        for f, gg in ((0, 2), (0, 3), (1, 2), (1, 3)):
            if fv[f] and fv[gg]:
                (ax, az), (bx, bz) = sides[f], sides[gg]
                for st in (1, 2):
                    marker.add((i + ax * st + bx * 2, k + az * st + bz * 2))
                    marker.add((i + ax * 2 + bx * st, k + az * 2 + bz * st))
    crowd = ndimage.maximum_filter(zfull | terr, size=3)
    n = 0
    for i, k in marker:
        if 0 <= i < nx and 0 <= k < nz and not crowd[i, k]:
            w.ids[i, 1, k], w.dat[i, 1, k] = B.REDSTONE_WIRE, 0
            n += 1
    return n


def towers(w, R, beds, r, count=16):
    """Karst towers standing alone in the mist round the board: scenery, never play. Each stands at least 16
    plus its radius off any island or build zone of either half and rises from the mist to 60..96 as
    forms.tower: rings tapering up the stack, a ledge every nine courses, faces bulging between them, laid in
    the karst's beds, a pine or two on the crown and vines down the faces."""
    from scipy import ndimage
    solid = ~R.mask("void") | zone_mask(R)
    clear = ndimage.distance_transform_edt(~solid)
    X, Z = w.grid()
    sites = []
    tries = 0
    while len(sites) < count and tries < 4000:
        tries += 1
        i, k = int(r.integers(4, w.sx - 4)), int(r.integers(4, w.sz - 4))
        rad = float(r.uniform(3, 7))
        if clear[i, k] < 16 + rad or any(np.hypot(i - a, k - b) < rad + q + 6 for a, b, q, _ in sites):
            continue
        sites.append((i, k, rad, int(r.integers(60, 97))))

    def rock(y, b):
        bed = beds(y + int(4 * b))
        return (B.COBBLE, 0) if bed == (B.STONE, 0) and r.random() < 0.06 else bed
    for n, (i, k, rad, peak) in enumerate(sites):
        cx, cz = int(X[i, k]), int(Z[i, k])

        def crown(w, x, y, z, rr, rad=rad):
            D.pine(w, x, y, z, int(rr.integers(7, 12)))
            if rad > 5:
                c = int(rad * 0.7)
                D.pine(w, x + c - 1, y, z - 1, int(rr.integers(5, 8)))
        forms.tower(w, cx, cz, 28, peak, rad, rock, r, seed=int(i * 31 + k), tree=crown)
    return len(sites)


def make():
    R, flights, walls = build()
    O = objectives()
    w = World(X_MIN, Z_MIN, X_MAX - X_MIN + 1, Z_MAX - Z_MIN + 1, sy=128)
    g = D.Ground(R, w)
    r = rng(BOARD, "rock")
    beds = strata()
    offset = T.bed_offset((w.sx, w.sz), dip=(0.0, 0.0), fold=4, cell=14, seed=13)
    islands(w, g, beds, offset, r)
    skirt(w, g, beds, rng(BOARD, "skirt"))
    D.paint(w, g, rng(BOARD, "paint"))
    n_slabs = D.joins(w, g, R, walls)
    wools = {o.color: o for o in O.of(Wool)}
    D.spawn(w, g, rng(BOARD, "spawn"))
    D.gate(w)
    D.bell_rock(w)
    D.shrine(w, wools["lime"].found)
    D.store(w, wools["yellow"].found)
    D.store_wall(w, g, WALL)
    D.lanes(w, g, rng(BOARD, "lanes"))
    n_ferns = D.ferns(w, g, rng(BOARD, "ferns"))
    solid = w.ids[:, 1:, :] != 0                                 # each column's lowest block: its root's tip
    bottom = 1 + np.argmax(solid, axis=1)
    n_vines = forms.root_vines(w, g.land & g.red, g.floor, bottom, rng(BOARD, "vines"),
                               keep=np.isin(g.piece, [g.R.kinds["pillar"], g.R.kinds["store"]]))
    n_marked = markers(w, R)
    # blue's half: red's turned half a circle. Its team banners are recoloured: turn_world's recolour reaches
    # block ids and data, not a banner's colour, which lives in its tile entity
    turn_world(w, "half", lambda x, z: z < 0)
    for te in w.tiles:
        if te["kind"] == "Banner" and te["z"] >= 0:
            te["base"] = 4
    O.stamp(w)                                                   # the monument slots and the wools, both halves
    before = int((w.ids == B.STAINED_GLASS).sum())
    T.cloud_deck(w, 31, seed=50, cell=18, puff=5, breaks=0.02, materials=((B.STAINED_GLASS, 0), (B.STAINED_GLASS, 8)))
    n_mist = int((w.ids == B.STAINED_GLASS).sum()) - before
    n_towers = towers(w, R, beds, rng(BOARD, "towers"))
    n_red = outline(w, R)
    loose = (w.ids[:, 1:, :] == B.GRAVEL) & (w.ids[:, :-1, :] == B.AIR)     # gravel the undercuts left hanging
    w.ids[:, 1:, :][loose], w.dat[:, 1:, :][loose] = B.STONE, 5
    w.biome[:, :] = 3
    return w, dict(slabs=n_slabs, ferns=n_ferns, vines=n_vines, marked=n_marked, mist=n_mist, towers=n_towers,
                   redstone=n_red)


if __name__ == "__main__":
    t0 = time.time()
    w, n = make()
    w.save(sys.argv[1], "Lantern Karst", (OBSERVER_AT[0], OBSERVER_AT[1], OBSERVER_AT[2]))
    print(f"generated in {time.time() - t0:.0f}s: " + ", ".join(f"{k} {v}" for k, v in n.items()))
    print(f"build height {MAX_BUILD}, kill below {KILL_Y}")
