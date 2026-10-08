"""Generate Whitecliff Cistern from the plan: red's half (x < 0) is built, then mirrored across the town's axis
(orient.turn_world, x' = -1 - x); the hills' pads, and the town's axis (the cistern, the garden, the boatyard, the
north and south plazas), are built whole.

The town is a plateau of pale rock standing out of the sea: sheer cliffs of sandstone and white clay in beds, a taper of
rock under it, its top poured level at 70 and then cut: the quay lowered to 68, the court to 62 with the vault under
it, the dock to 66, the garden raised to 72. Over that, whitewashed blocks banded in blue, flat roofs with parapets,
streets of smooth sandstone, and the cover the plan lists.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np

import kit
import plan as P
from pgmvox import B, World, rng
from pgmvox import facade as F
from pgmvox import props, trees
from pgmvox import terrain as T
from pgmvox.noise import fbm
from pgmvox.orient import stair as stair_data, turn_world

SY = 128
WHITE = (B.STAINED_CLAY, 0)
BLUE = (B.STAINED_CLAY, 3)
CYAN = (B.STAINED_CLAY, 9)
GOLD = (B.STAINED_CLAY, 4)
PALE = (B.SANDSTONE, 2)
STONE = (B.STONEBRICK, 0)


def red_cols(w):
    X, _ = w.grid()
    return X < 0


def plate_mask(w):
    """The stack's top: the board less its four corners cut."""
    X, Z = w.grid()
    m = (X >= -59) & (X <= 58) & (Z >= -49) & (Z <= 48)
    for sx in (-1, 1):
        for sz in (-1, 1):
            cx, cz = (-59 if sx < 0 else 58), (-49 if sz < 0 else 48)
            m &= ~((np.abs(X - cx) + np.abs(Z - cz)) < 7)
    return m


def rock(w, R):
    """The stack: beds of sandstone, andesite and white clay up to 69 under the whole plate, a taper beneath."""
    plate = plate_mask(w)
    strata = T.Strata([((B.SANDSTONE, 0), 3, 4), ((B.STONE, 5), 1.5, 3), ((B.STAINED_CLAY, 0), 1.5, 2),
                       ((B.SANDSTONE, 2), 1.5, 2), ((B.STAINED_CLAY, 8), 0.5, 1)], seed=19, start=0)
    bed = T.beds(strata, T.bed_offset((w.sx, w.sz), dip=(0.0, 0.02), fold=2, cell=16, seed=2), seed=4)
    ed = np.zeros(plate.shape, int)
    from pgmvox.shapes import edge_depth
    ed = edge_depth(plate)
    root = np.maximum(np.round(6 + 0.35 * ed), 1).astype(int)
    r = rng(P.BOARD, "rock")
    for i, k in np.argwhere(plate):
        ys = range(42, P.TOWN)
        for y, blk in zip(ys, bed(i, k, ys)):
            w.ids[i, y, k], w.dat[i, y, k] = blk
        depth = int(root[i, k])
        for j in range(1, depth + 1):
            yy = 42 - j
            if yy < 3:
                break
            if r.random() < 0.9 - 0.04 * j:
                w.ids[i, yy, k], w.dat[i, yy, k] = (B.STONE, 5) if r.random() < 0.6 else (B.SANDSTONE, 0)
    return plate


def tops(w, R, plate, r):
    """Every cell of the plan at its own floor: the surface by kind, cut down or built up from the poured plate."""
    X, Z = w.grid()
    for i, k in np.argwhere(plate):
        x, z = int(X[i, k]), int(Z[i, k])
        kind = R.kind(x, z)
        h = R.h(x, z)
        if kind in ("void",):
            # a hole in the plan inside the plate: the oculus, a stairwell, the cellar: carved to the vault
            for y in range(P.VAULT + 1, P.TOWN + 1):
                w.ids[i, y, k] = 0
            continue
        if h < P.TOWN:
            w.ids[i, h + 1:P.TOWN + 1, k] = 0
            w.dat[i, h + 1:P.TOWN + 1, k] = 0
        elif h > P.TOWN:
            for y in range(P.TOWN, h + 1):
                w.ids[i, y, k], w.dat[i, y, k] = STONE
        if kind in ("house", "cover", "wall", "stair", "gate"):
            continue
        c = r.random()
        blk = {"street": ((B.SANDSTONE, 2) if c < 0.55 else (B.STONE, 6) if c < 0.8 else (B.SANDSTONE, 0)),
               "yard": (B.SANDSTONE, 0), "plaza": (B.SANDSTONE, 2), "ring": (B.SANDSTONE, 2),
               "quay": ((B.PLANKS, 1) if (x + z) % 2 else (B.PLANKS, 5)), "court": (B.STONE, 6),
               "garden": (B.GRASS, 0), "dock": ((B.SAND, 0) if c < 0.6 else (B.GRAVEL, 0) if c < 0.8 else (B.PLANKS, 5)),
               "hill": (B.STAINED_CLAY, 4), "vault": (B.SANDSTONE, 2), "tunnel": (B.SANDSTONE, 2)}.get(kind)
        if blk:
            w.ids[i, h, k], w.dat[i, h, k] = blk


def blocks(w, R, r):
    """The whitewashed blocks: poured mass banded in blue, windows, a parapet round a flat roof; the two roof walks
    cut with the steps up and the plank bridge between."""
    fn = lambda x, y, z: WHITE if (y - P.TOWN) % 5 != 4 else BLUE                    # noqa: E731
    for key, (x0, z0, x1, z1) in P.BLOCKS:
        cells = {(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)}
        top = {"A1": 74, "A2": 74}.get(key, 73 + (hash(key) % 4))
        F.extrude(w, cells, P.TOWN, top, base=fn, faces_=[F.windows(3, 1, 2, (B.STAINED_PANE, 3)),
                                                         F.windows(3, 3, 3, (B.STAINED_PANE, 3)),
                                                         F.band(top - P.TOWN - 1, top - P.TOWN - 1, CYAN, inset=False)],
                  top="parapet-slotted", top_block=PALE)
        # a doorway niche on the street face: two high, set back one
        for x, z in sorted(cells)[::7]:
            pass
    # the plank walk over the Middle Way between the two roofs, three wide, a rail each side
    for x in range(-35, -32):
        for z in range(-3, 3):
            w.set(x, 74, z, B.PLANKS, 1)
            for y in range(75, 78):
                w.set(x, y, z, B.AIR)
    for z in range(-3, 3):
        for x in (-36, -32):
            w.set(x, 75, z, B.SPRUCE_FENCE, 0) if z not in (-3, 2) else None
    for x in range(-35, -32):
        for z in (-3, 2):
            w.set(x, 75, z, B.AIR)
    # the roof walks: parapet cleared where the steps meet it
    for z in range(-13, -10):
        w.set(-30, 75, z, B.AIR)
    for z in range(10, 13):
        w.set(-30, 75, z, B.AIR)


def court(w, R, r):
    """The cistern court: the ring's drop face in arches, columns, planters, the oculus and the stairwells' rails."""
    for key in ("column",):
        pass
    # the face of the sunken court: a band of blue and a cornice, arches as insets
    ring = {(x, z) for x in range(-16, 16) for z in range(-16, 16) if not (-12 <= x <= 11 and -12 <= z <= 11)}
    inner = {(x, z) for x in range(-12, 12) for z in range(-12, 12)}
    for x in range(-13, 13):
        for z in (-13, 12):
            for y in range(P.COURT + 1, P.TOWN):
                if (x, z - (1 if z < 0 else -1)) in inner or True:
                    pass
    # a low parapet round the ring's inner edge, open at the four flights
    edge = [(x, z) for x in range(-16, 16) for z in range(-16, 16)
            if (x in (-13, 12) and -13 <= z <= 12) or (z in (-13, 12) and -13 <= x <= 12)]
    for x, z in edge:
        if R.kind(x, z) in ("ring",):
            w.set(x, P.TOWN + 1, z, B.SLAB, 7)
    # the oculus's rim and the stairwells' rails
    for x, z in ((-3, -3), (-3, 2), (2, -3), (2, 2)):
        pass
    for x in range(-3, 3):
        for z in (-3, 2):
            w.set(x, P.COURT + 1, z, B.IRON_BARS, 0)
    for z in range(-3, 3):
        for x in (-3, 2):
            w.set(x, P.COURT + 1, z, B.IRON_BARS, 0)


def cover(w, R, r):
    """The plan's cover, built: crates and barricades of dark oak, hedges and planters of leaves and flowers, stalls,
    fountains, columns, hulls, piers, baffles."""
    n = 0
    for c in P.COVER:
        x0, z0, x1, z1 = c["rect"]
        g = R.h(x0, z0) - c["h"]
        if c["kind"] in ("pier", "lowwall"):
            g = P.VAULT
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for y in range(g + 1, g + c["h"] + 1):
                    k = c["kind"]
                    if k == "crate":
                        blk = (B.PLANKS, 5)
                    elif k == "barricade":
                        blk = (B.PLANKS, 5) if y < g + c["h"] else (B.SPRUCE_FENCE, 0)
                    elif k in ("hedge", "planter"):
                        blk = (B.LEAVES, 7)
                    elif k == "column":
                        blk = (B.QUARTZ, 2)
                    elif k == "pier":
                        blk = (B.QUARTZ, 2) if y < g + c["h"] else (B.QUARTZ, 1)
                    elif k == "fountain":
                        blk = PALE
                    elif k == "hull":
                        blk = (B.PLANKS, 5)
                    elif k == "baffle":
                        blk = WHITE if y < g + c["h"] else BLUE
                    elif k == "stall":
                        blk = (B.PLANKS, 1)
                    elif k == "lowwall":
                        blk = STONE
                    else:
                        blk = PALE
                    w.set(x, y, z, *blk)
        top = g + c["h"] + 1
        if c["kind"] == "planter":
            for x in range(x0, x1 + 1):
                for z in range(z0, z1 + 1):
                    if r.random() < 0.6:
                        w.set(x, top, z, B.FLOWER, int(r.integers(4, 8)))
        if c["kind"] == "fountain":
            w.set((x0 + x1) // 2, g + 2, (z0 + z1) // 2, B.WATER, 0)
            w.set((x0 + x1) // 2 + 1, g + 2, (z0 + z1) // 2, B.WATER, 0)
        if c["kind"] == "stall":
            for x in range(x0, x1 + 1):
                for z in range(z0, z1 + 1):
                    w.set(x, g + c["h"] + 1, z, B.CARPET, 14 if (x + z) % 2 else 0)
        if c["kind"] == "hull":
            w.set((x0 + x1) // 2, top, (z0 + z1) // 2, B.SPRUCE_FENCE, 0)
            w.set((x0 + x1) // 2, top + 1, (z0 + z1) // 2, B.SPRUCE_FENCE, 0)
            w.set((x0 + x1) // 2, top + 2, (z0 + z1) // 2, B.SPRUCE_FENCE, 0)
        n += 1
    return n


def stairs(w, R):
    """The plan's flights laid in stairs, the mass under each filled, the air over each cleared."""
    for u, base in ((R, 0), (R.storey(1), 1)):
        for i, k in np.argwhere(u.mask("stair")):
            x, z, y = int(u.X[i, k]), int(u.Z[i, k]), int(u.H[i, k])
            rise = u.stair.get((x, z), "e")
            for yy in range(y - 3, y):
                if w.id(x, yy, z) in (0, B.SAND):
                    w.set(x, yy, z, *PALE)
            w.set(x, y, z, B.SANDSTONE_STAIRS, stair_data(rise))
            for yy in range(y + 1, y + 5):
                w.set(x, yy, z, B.AIR)
            if base == 1:
                for yy in range(y - 6, y):
                    if w.id(x, yy, z) in (0,):
                        w.set(x, yy, z, *PALE)
        # the stair's walls: nothing; the mass round it is the plate


def underground(w, R, r):
    """The vault: a hall under the court, air over its floor to the court's underside, the piers, the pad's
    paving; the undercroft's two passages and the cellar stair's slot."""
    for x in range(-8, 8):
        for z in range(-8, 8):
            for y in range(P.VAULT + 1, P.COURT):
                w.set(x, y, z, B.AIR)
            w.set(x, P.VAULT, z, *PALE)
            w.set(x, P.COURT, z, B.STONE, 6) if R.kind(x, z) not in ("void",) else None
    for x in range(-26, -8):
        for z in range(-2, 2):
            for y in range(P.VAULT + 1, P.VAULT + 5):
                w.set(x, y, z, B.AIR)
            w.set(x, P.VAULT, z, *((B.STONE, 6) if (x + z) % 2 else PALE))
    # arches along the undercroft: lamps every sixth block, a pier pair every eighth
    for x in range(-24, -9, 6):
        w.set(x, P.VAULT + 4, 1, B.SEA_LANTERN, 0)
        w.set(x, P.VAULT + 4, -2, B.SEA_LANTERN, 0)
    for x in range(-22, -9, 8):
        for z in (-2, 1):
            for y in range(P.VAULT + 1, P.VAULT + 4):
                w.set(x, y, z, B.QUARTZ, 2)
    # the pad: a medallion of gold and blue under the oculus
    F.carpet(w, -3, -3, 2, 2, P.VAULT, F.first_of(F.border(0, (B.STAINED_CLAY, 3)), F.medallion(0.0, 0.5, (B.STAINED_CLAY, 4)),
                                                  default=(B.STAINED_CLAY, 4)))
    for x, z in ((-8, -8), (7, -8), (-8, 7), (7, 7)):
        for y in range(P.VAULT + 1, P.COURT):
            w.set(x, y, z, B.SANDSTONE, 1 if y == P.VAULT + 1 else 2)
    for x in range(-7, 7, 4):
        for z in (-8, 7):
            w.set(x, P.COURT - 1, z, B.SEA_LANTERN, 0)
    for z in range(-7, 7, 4):
        for x in (-8, 7):
            w.set(x, P.COURT - 1, z, B.SEA_LANTERN, 0)


def quay(w, R, r):
    """The quay: white walls six high round its deck, a gate on three sides, mooring posts and lamps, chests."""
    x0, z0, x1, z1 = -58, -9, -47, 8
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1):
                if R.kind(x, z) == "gate":
                    for y in range(P.QUAY + 1, P.QUAY + 7):
                        w.set(x, y, z, B.AIR)
                    continue
                for y in range(P.QUAY + 1, P.QUAY + 7):
                    w.set(x, y, z, *(WHITE if (y - P.QUAY) % 3 else BLUE))
                w.set(x, P.QUAY + 7, z, B.SLAB, 7)
            else:
                for y in range(P.QUAY + 1, P.QUAY + 8):
                    w.set(x, y, z, B.AIR)
    for x, z in ((-56, -7), (-56, 6), (-49, -7), (-49, 6)):
        kit.brazier(w, x, P.QUAY, z, post=(B.SPRUCE_FENCE, 0), light=(B.SEA_LANTERN, 0), base=(B.COBBLE_WALL, 0))
    w.chest(-57, P.QUAY + 1, -1, [(0, "minecraft:golden_apple", 4, 0), (1, "minecraft:cooked_beef", 32, 0)], 5)
    w.chest(-57, P.QUAY + 1, 0, [(0, "minecraft:arrow", 32, 0), (1, "minecraft:golden_apple", 4, 0)], 5)


def garden_and_dock(w, R, r):
    """The garden: white walls six high with arched gates, olive trees in its bays; the dock: a quay of its own, walls
    four high, a crane."""
    for x in range(-14, 14):
        for z in range(-47, -33):
            if x in (-14, 13) or z in (-47, -34):
                if R.kind(x, z) == "gate":
                    for y in range(P.GARDEN + 1, P.GARDEN + 7):
                        w.set(x, y, z, B.AIR)
                    continue
                for y in range(P.GARDEN + 1, P.GARDEN + 7):
                    w.set(x, y, z, *(WHITE if (y - P.GARDEN) % 3 else BLUE))
                w.set(x, P.GARDEN + 7, z, B.SLAB, 7)
    for x in range(-14, 14):
        for z in range(-33, -31):
            for y in range(P.TOWN + 1, P.TOWN + 3):
                w.set(x, y, z, *(WHITE if R.kind(x, z) == "wall" else (B.AIR, 0)))
    for x in range(-13, 13):
        for z in range(32, 36):
            if R.kind(x, z) == "wall":
                for y in range(P.DOCK + 1, P.TOWN + 3):
                    w.set(x, y, z, *(WHITE if (y - P.DOCK) % 3 else BLUE))
    # the dock's side walls and the garden's carpet around the pad
    for z in range(36, 48):
        for x in (-13, 12):
            if R.kind(x, z) == "dock" and R.kind(x + (1 if x < 0 else -1), z) == "dock":
                pass
    F.carpet(w, -3, -45, 2, -40, P.GARDEN, F.first_of(F.border(0, (B.STAINED_CLAY, 3)), F.medallion(0.0, 0.5, (B.STAINED_CLAY, 4)),
                                                      default=(B.STAINED_CLAY, 4)))
    F.carpet(w, -3, 40, 2, 45, P.DOCK, F.first_of(F.border(0, (B.STAINED_CLAY, 3)), F.medallion(0.0, 0.5, (B.STAINED_CLAY, 4)),
                                                  default=(B.STAINED_CLAY, 4)))


def olives(w, R, r):
    lib = trees.library()
    by = trees.kinds(lib)
    kinds = by["olive"] + by["small-olive"]
    spots = [(-10, -43), (9, -43), (-11, -38), (10, -38), (-8, 24), (7, 24), (-12, 30), (11, 30), (-15, -18), (14, -18),
             (-33, -25), (-33, 24), (-52, -20), (-52, 21)]
    n = 0
    for x, z in spots:
        t = kinds[int(r.integers(len(kinds)))]
        h = R.h(x, z)
        if R.kind(x, z) in ("garden", "plaza", "yard", "ring", "street") and trees.plant(w, x, z, t, turn=int(r.integers(4))):
            n += 1
    return n


def lamps(w, R):
    for x, z in ((-43, -30), (-43, 30), (-24, -30), (-24, 30), (-30, -24), (-30, 21), (-14, -20), (-14, 28)):
        props.lamp(w, x, P.TOWN, z, height=3, post=(B.SPRUCE_FENCE, 0), light=(B.SEA_LANTERN, 0), cap=None)


def rim(w, plate, R):
    """A low parapet and a fence round the plate's edge."""
    from pgmvox.shapes import boundary
    X, Z = w.grid()
    for i, k in np.argwhere(boundary(plate)):
        x, z = int(X[i, k]), int(Z[i, k])
        h = R.h(x, z) if R.inside(x, z) else P.TOWN
        if h <= 0:
            h = P.TOWN
        w.set(x, h + 1, z, B.SLAB, 7)
        if (x + z) % 3 == 0:
            w.set(x, h + 2, z, B.IRON_BARS, 0)


def make():
    R = P.build()
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=SY)
    t0 = time.time()
    r = rng(P.BOARD, "all")
    plate = rock(w, R)
    tops(w, R, plate, rng(P.BOARD, "tops"))
    underground(w, R, r)
    blocks(w, R, r)
    stairs(w, R)
    court(w, R, r)
    n_cover = cover(w, R, rng(P.BOARD, "cover"))
    quay(w, R, r)
    garden_and_dock(w, R, r)
    n_olive = olives(w, R, rng(P.BOARD, "olives"))
    lamps(w, R)
    rim(w, plate, R)
    turn_world(w, "mirror_x", red_cols(w), recolour={(B.CARPET, 14): (B.CARPET, 11)})
    P.objectives().stamp(w)
    w.ids[:, 0, :][plate] = 36
    # the sea, far under the stack
    sea = (w.ids[:, 22:28, :] == 0)
    w.ids[:, 22:28, :][sea] = B.WATER
    loose = (w.ids[:, 1:, :] == B.GRAVEL) & (w.ids[:, :-1, :] == B.AIR)
    w.ids[:, 1:, :][loose], w.dat[:, 1:, :][loose] = B.STONE, 5
    w.biome[:, :] = 1
    return w, dict(cover=n_cover, olives=n_olive)


if __name__ == "__main__":
    t0 = time.time()
    w, n = make()
    w.save(sys.argv[1], "Whitecliff Cistern", (0, 100, 0))
    print(f"generated in {time.time() - t0:.0f}s: " + ", ".join(f"{k} {v}" for k, v in n.items()))
    print(f"build height {P.MAX_BUILD}, kill below {P.KILL_Y}")
