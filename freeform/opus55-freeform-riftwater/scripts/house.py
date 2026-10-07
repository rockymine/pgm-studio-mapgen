"""One building: a site levelled for it, storeys of walls framed in log, a floor per storey, windows and a
door, a gable roof whose verge overhangs the gable, a chimney, and a furnished inside.

Styles (the board's two built families, plus the stone used for the made things that are not houses):
  town     brick ground storey, spruce-framed upper storeys with white clay infill, dark oak roof, spruce gable
  village  cobblestone sill course, spruce plank walls in spruce posts, spruce roof, oak plank gable
  stone    stone brick with andesite, dark oak roof, stone brick gable
"""
import numpy as np

from mc import B

RNG = np.random.default_rng(99)

STYLES = {
    "town": dict(base=(B.BRICK, 0), infill=(B.STAINED_CLAY, 0), post=(B.LOG, 1), laid=(B.LOG, 1),
                 roof=B.DARK_OAK_STAIRS, ridge=(B.WOOD_SLAB, 5), gable=(B.PLANKS, 1), floor=(B.PLANKS, 1),
                 door=B.SPRUCE_DOOR, chimney=(B.BRICK, 0), sill=None),
    "village": dict(base=(B.PLANKS, 1), infill=(B.PLANKS, 1), post=(B.LOG, 1), laid=(B.LOG, 1),
                    roof=B.SPRUCE_STAIRS, ridge=(B.WOOD_SLAB, 1), gable=(B.PLANKS, 0), floor=(B.PLANKS, 0),
                    door=B.SPRUCE_DOOR, chimney=(B.COBBLE, 0), sill=(B.COBBLE, 0)),
    "stone": dict(base=(B.STONEBRICK, 0), infill=(B.STONEBRICK, 0), post=(B.STONE, 6), laid=None,
                  roof=B.DARK_OAK_STAIRS, ridge=(B.WOOD_SLAB, 5), gable=(B.STONEBRICK, 0), floor=(B.PLANKS, 5),
                  door=B.DARK_OAK_DOOR, chimney=(B.STONEBRICK, 0), sill=None),
}

DOOR_FACING = {"e": 0, "s": 1, "w": 2, "n": 3}


def site(w, L, x0, z0, x1, z1, y, margin=2, ground=(B.GRASS, 0)):
    """Level the ground for a footprint at floor y: cut what stands above, fill what is missing below,
    and ease the ground round it over `margin` blocks so the house sits on the land rather than on a step."""
    for x in range(x0 - margin, x1 + margin + 1):
        for z in range(z0 - margin, z1 + margin + 1):
            ix, iz = x - L.x0, z - L.z0
            if not (0 <= ix < L.nx and 0 <= iz < L.nz) or not L.land[ix, iz] or L.water[ix, iz] > 0:
                continue
            dx = max(x0 - x, 0, x - x1)
            dz = max(z0 - z, 0, z - z1)
            d = max(dx, dz)
            old = int(L.H[ix, iz])
            if d == 0:
                target = y
            else:
                t = d / (margin + 1)
                target = int(round(y * (1 - t) + old * t))
            if target == old:
                continue
            if target < old:
                for yy in range(target + 1, old + 1 + 6):
                    if w.id(x, yy, z) in (B.GRASS, B.DIRT, B.STONE, B.COBBLE, B.GRAVEL, B.SAND, B.TALLGRASS, B.FLOWER):
                        w.set(x, yy, z, B.AIR)
            else:
                for yy in range(old, target):
                    w.set(x, yy, z, B.DIRT if yy >= target - 2 else B.STONE)
            w.set(x, target, z, *ground)
            if w.id(x, target - 1, z) == B.GRASS:
                w.set(x, target - 1, z, B.DIRT)
            L.H[ix, iz] = target


def roof_gable(w, x0, z0, x1, z1, plate_y, st, along_x=True, overhang=1):
    """A gable roof over the box, its ridge along x (or z), verge overhanging the gable ends by one."""
    roof, ridge, gable = st["roof"], st["ridge"], st["gable"]
    if along_x:
        a0, a1 = x0 - overhang, x1 + overhang       # along the ridge
        b0, b1 = z0 - 1, z1 + 1                     # across it, eaves one outside the wall
        lo_stair, hi_stair = 2, 3
    else:
        a0, a1 = z0 - overhang, z1 + overhang
        b0, b1 = x0 - 1, x1 + 1
        lo_stair, hi_stair = 0, 1
    k = 0
    top = plate_y
    while b0 + k <= b1 - k:
        y = plate_y + k
        lo, hi = b0 + k, b1 - k
        for a in range(a0, a1 + 1):
            if lo == hi:
                X, Z = (a, lo) if along_x else (lo, a)
                w.set(X, y, Z, *ridge)
            else:
                X, Z = (a, lo) if along_x else (lo, a)
                w.set(X, y, Z, roof, lo_stair)
                X, Z = (a, hi) if along_x else (hi, a)
                w.set(X, y, Z, roof, hi_stair)
        # the gable wall between the two rows, on both end walls
        for b in range(lo + 1, hi):
            for a in ((x0, x1) if along_x else (z0, z1)):
                X, Z = (a, b) if along_x else (b, a)
                w.set(X, y, Z, *gable)
            # attic air inside
            for a in range((x0 + 1) if along_x else (z0 + 1), (x1 if along_x else z1)):
                X, Z = (a, b) if along_x else (b, a)
                w.set(X, y, Z, B.AIR)
        top = y
        k += 1
    return top


def house(w, L, x0, z0, x1, z1, storeys=2, style="town", door="s", kind="house", floor_y=None,
          along_x=None, chimney=True, door_at=None, roof=True, upper_style=None, windows=True):
    """Build a framed house on the footprint (walls included) and return its record."""
    st = STYLES[style]
    if floor_y is None:
        hs = L.H[x0 - L.x0:x1 - L.x0 + 1, z0 - L.z0:z1 - L.z0 + 1]
        floor_y = int(np.median(hs))
    site(w, L, x0, z0, x1, z1, floor_y)
    if along_x is None:
        along_x = (x1 - x0) >= (z1 - z0)
    # foundations: solid under the floor, so nothing floats over a dip
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            yy = floor_y - 1
            while yy > 0 and w.id(x, yy, z) in (B.AIR, B.WATER, B.TALLGRASS):
                w.set(x, yy, z, B.STONE)
                yy -= 1
            w.set(x, floor_y, z, *st["floor"])
            for y in range(floor_y + 1, floor_y + 4 * storeys + 1):
                w.set(x, y, z, B.AIR)
    corners = {(x0, z0), (x0, z1), (x1, z0), (x1, z1)}
    for s in range(storeys):
        fy = floor_y + 4 * s
        sst = STYLES[upper_style] if (upper_style and s > 0) else st
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if x not in (x0, x1) and z not in (z0, z1):
                    if s > 0:
                        w.set(x, fy, z, *sst["floor"])
                    continue
                for y in range(fy + 1, fy + 4):
                    if (x, z) in corners and sst["post"]:
                        w.set(x, y, z, *sst["post"])
                    elif s == 0:
                        if y == fy + 1 and sst["sill"]:
                            w.set(x, y, z, *sst["sill"])
                        else:
                            w.set(x, y, z, *sst["base"])
                    else:
                        w.set(x, y, z, *sst["infill"])
                # the seam: a laid log course running along the wall, sawn ends at the corners
                seam = fy + 4
                if sst["laid"]:
                    run_x = z in (z0, z1) and (x, z) not in corners
                    if (x, z) in corners:
                        w.set(x, seam, z, sst["post"][0], sst["post"][1])
                    else:
                        w.set(x, seam, z, sst["laid"][0], sst["laid"][1] | (4 if run_x else 8))
                else:
                    w.set(x, seam, z, *sst["base"])
        # mid-wall posts on long timber walls, every four blocks
        if sst["post"] and s > 0 and sst is STYLES["town"]:
            for x in range(x0 + 4, x1 - 1, 4):
                for z in (z0, z1):
                    for y in range(fy + 1, fy + 4):
                        w.set(x, y, z, *sst["post"])
            for z in range(z0 + 4, z1 - 1, 4):
                for x in (x0, x1):
                    for y in range(fy + 1, fy + 4):
                        w.set(x, y, z, *sst["post"])
        # windows: panes in the wall between posts, two tall in town, one in the village
        if windows:
            tall = style != "village"
            for x in range(x0 + 2, x1 - 1, 2 if (x1 - x0) < 6 else 3):
                for z in (z0, z1):
                    if w.id(x, fy + 2, z) in (B.LOG,):
                        continue
                    w.set(x, fy + 2, z, B.PANE)
                    if tall:
                        w.set(x, fy + 3 if s > 0 else fy + 2, z, B.PANE)
            for z in range(z0 + 2, z1 - 1, 2 if (z1 - z0) < 6 else 3):
                for x in (x0, x1):
                    if w.id(x, fy + 2, z) in (B.LOG,):
                        continue
                    w.set(x, fy + 2, z, B.PANE)
                    if tall and s > 0:
                        w.set(x, fy + 3, z, B.PANE)
    plate = floor_y + 4 * storeys
    # the door, two high, with the step outside it kept clear
    if door_at is None:
        door_at = {"n": ((x0 + x1) // 2, z0), "s": ((x0 + x1) // 2, z1),
                   "w": (x0, (z0 + z1) // 2), "e": (x1, (z0 + z1) // 2)}[door]
    dx_, dz_ = door_at
    if (dx_, dz_) in corners:
        dx_ += 1 if door in "ns" else 0
        dz_ += 1 if door in "ew" else 0
    out = {"n": (0, -1), "s": (0, 1), "w": (-1, 0), "e": (1, 0)}[door]
    w.set(dx_, floor_y + 1, dz_, st["door"], DOOR_FACING[door])
    w.set(dx_, floor_y + 2, dz_, st["door"], 8)
    w.set(dx_, floor_y + 3, dz_, *st["laid"]) if st["laid"] else None
    ox, oz = dx_ + out[0], dz_ + out[1]
    for y in range(floor_y + 1, floor_y + 3):
        if w.id(ox, y, oz) not in (B.AIR,):
            w.set(ox, y, oz, B.AIR)
    # a step if the ground outside is lower than the sill
    gy = w.top(ox, oz)
    if gy < floor_y:
        w.set(ox, floor_y, oz, B.SLAB if style != "village" else B.WOOD_SLAB, 3 if style != "village" else 1)
    top = plate
    if roof:
        top = roof_gable(w, x0, z0, x1, z1, plate, st, along_x)
        # a floor under the attic so the top storey has a ceiling
        for x in range(x0 + 1, x1):
            for z in range(z0 + 1, z1):
                w.set(x, plate, z, *st["floor"])
    if chimney:
        cx, cz = (x0 + 1, (z0 + z1) // 2 + 1) if along_x else ((x0 + x1) // 2 + 1, z0 + 1)
        for y in range(floor_y + 1, top + 2):
            w.set(cx, y, cz, *st["chimney"])
        w.set(cx, floor_y + 1, cz, B.FURNACE if kind != "smithy" else B.FURNACE, 3)
    # stairs between storeys: a ladder on the inside of the back wall
    lx, lz = (x1 - 1, z0 + 1) if door != "n" else (x1 - 1, z1 - 1)
    lf = 3 if door != "n" else 2
    for s in range(storeys - 1):
        fy = floor_y + 4 * s
        for y in range(fy + 1, fy + 5):
            w.set(lx, y, lz, B.LADDER, lf)
        w.set(lx, fy + 4, lz, B.LADDER, lf)
    rec = dict(x0=x0, z0=z0, x1=x1, z1=z1, floor=floor_y, storeys=storeys, style=style, door=(dx_, dz_),
               out=(ox, oz), kind=kind, top=top)
    furnish(w, rec)
    return rec


def furnish(w, r):
    """A room's worth of things, by what the building is."""
    x0, z0, x1, z1, fy = r["x0"], r["z0"], r["x1"], r["z1"], r["floor"]
    kind = r["kind"]
    ix0, iz0, ix1, iz1 = x0 + 1, z0 + 1, x1 - 1, z1 - 1

    def free(x, y, z):
        return w.id(x, y, z) == B.AIR and w.id(x, y - 1, z) not in (B.AIR, B.LADDER)

    def put(x, y, z, b, d=0):
        if free(x, y, z):
            w.set(x, y, z, b, d)

    if kind in ("house", "cottage", "inn", "hall", "gaol", "shop", "bakery"):
        # a table and a chair by the window side
        tx, tz = (ix0 + ix1) // 2, (iz0 + iz1) // 2
        if kind == "inn":
            for x in range(ix0 + 1, ix1, 3):
                for z in range(iz0 + 1, iz1, 3):
                    put(x, fy + 1, z, B.FENCE); put(x, fy + 2, z, B.PLATE_WOOD)
                    put(x + 1, fy + 1, z, B.SPRUCE_STAIRS, 1)
            for z in range(iz0, iz1 + 1):
                put(ix1 - 1, fy + 1, z, B.PLANKS, 5)
        elif kind == "hall":
            for x in range(ix0 + 1, ix1):
                put(x, fy + 1, tz, B.PLANKS, 5)
                put(x, fy + 1, tz - 1, B.SPRUCE_STAIRS, 2)
                put(x, fy + 1, tz + 1, B.SPRUCE_STAIRS, 3)
        else:
            put(tx, fy + 1, tz, B.FENCE); put(tx, fy + 2, tz, B.PLATE_WOOD)
            put(tx + 1, fy + 1, tz, B.SPRUCE_STAIRS, 1)
            put(ix0, fy + 1, iz1, B.CRAFTING)
            put(ix0, fy + 1, iz0, B.BOOKSHELF if kind == "house" else B.CRAFTING)
        put(ix1, fy + 1, iz1, B.CHEST, 2) if kind != "hall" else None
        if kind == "bakery":
            put(ix0 + 1, fy + 1, iz0, B.FURNACE, 3)
            put(ix0 + 2, fy + 1, iz0, B.FURNACE, 3)
        # a bed upstairs, or in the corner of a one-storey cottage
        by = fy + 4 if r["storeys"] > 1 else fy
        bx, bz = ix0, iz0 + 1 if r["storeys"] > 1 else iz0 + 1
        if free(bx, by + 1, bz) and free(bx + 1, by + 1, bz):
            w.set(bx, by + 1, bz, B.BED, 3)
            w.set(bx + 1, by + 1, bz, B.BED, 3 | 8)
        # a carpet and a flower pot
        if r["storeys"] > 1:
            for x in range(ix0 + 1, min(ix1, ix0 + 4)):
                for z in range(iz0 + 2, min(iz1, iz0 + 4)):
                    put(x, fy + 5, z, B.CARPET, 14 if r["style"] == "town" else 12)
    # light
    for (tx, tz, f) in ((ix0, (iz0 + iz1) // 2, 1), (ix1, (iz0 + iz1) // 2, 2)):
        for s in range(r["storeys"]):
            if w.id(tx, fy + 4 * s + 3, tz) == B.AIR:
                w.set(tx, fy + 4 * s + 3, tz, B.TORCH, f)
