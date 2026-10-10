"""Slatefold's surface and what stands on it: the paint of each terrace, the houses, the two wool houses, the walls with
their chests, the rails, the cover on the Dressing Floor, the lamps, the trees; then the build zones' marks and the mist.

Every prop is placed for a reason written beside it; nothing is scattered. A house's windows keep two blocks clear of
its door (the library's rhythm does not), and a house's door is read from the library before the plan trusts it.
"""
import numpy as np

import plan as P
from pgmvox import B, noise, props, trees
from pgmvox import build as BLD
from pgmvox.orient import door as door_data, stair as stair_data, ladder as ladder_data

SLATE = [(B.STONE, 6), (B.STONE, 5), (B.STONE, 0)]               # polished andesite, andesite, stone: slate flags
QSET = [(B.STONE, 0), (B.STONE, 5), (B.COBBLE, 0), (B.STONE, 6)]
PATH = [(B.GRAVEL, 0), (B.STONE, 5), (B.STONE, 6)]


def cellpick(x, z, choices, size=3, salt=0):
    """One block of `choices` for the size-by-size cell this column is in: even shares, three blocks to a cell."""
    k = ((x // size) * 73856093 ^ (z // size) * 19349663 ^ salt * 83492791) & 0xFFFF
    return choices[k % len(choices)]


# red's lanes and lawns, by terrace: rectangles (x0, z0, x1, z1) of laid paving, the rest of a terrace grass
LANES = {
    "spawn": [(-5, -100, 5, -83), (-30, -87, -22, -83), (8, -87, 14, -83), (-5, -87, 14, -84)],
    "row": [(-46, -69, 14, -64), (-5, -81, 5, -64), (-34, -81, -22, -64)],
    "front": [(-6, -47, 6, -14), (-44, -47, -36, -30), (10, -47, 20, -30), (-34, -22, 34, -14)],
    "bench": [(-70, -93, -64, -89), (-66, -85, -64, -79)],
    "landing": [],
}
# grass patches worn into paving and paving worn into grass: (centre x, z, radius x, radius z, what)
PATCHES = [(-20, -95, 9, 5, "worn"), (14, -98, 7, 4, "worn"), (-28, -73, 6, 3, "dirt"), (6, -74, 5, 3, "dirt"),
           (-30, -30, 8, 6, "grass"), (24, -26, 7, 5, "grass"), (-6, -38, 5, 3, "grass"), (-70, -85, 5, 3, "worn"),
           (-74, -96, 6, 3, "worn")]
LAWN_KINDS = ("spawn", "row", "front", "bench", "landing")


def in_rect(x, z, rects):
    return any(a <= x <= c and b <= z <= d for a, b, c, d in rects)


def surface(w, R, land_r, floor, r):
    """The top of every column by its terrace: slate flags laid in cells of three on lanes and the yard, grass with worn
    and podzol patches on the benches, quarried stone on the Quarry Floor and in the Pit, a mixed spoil on the heaps."""
    X, Z = w.grid()
    patchA = noise.fbm((w.sx, w.sz), 7, 2, seed=33)
    patchB = noise.fbm((w.sx, w.sz), 5, 2, seed=44)
    names = {i: k for k, i in R.kinds.items()}
    piece = R.piece
    for i, k in np.argwhere(land_r):
        x, z, h = int(X[i, k]), int(Z[i, k]), int(floor[i, k])
        kind = names[int(piece[i, k])]
        if kind == "stair":
            continue
        top, soil = (B.STONE, 0), None
        if kind in ("yard", "gantry-land"):
            top = cellpick(x, z, SLATE)
        elif kind in ("quarry", "pit"):
            top = cellpick(x, z, QSET, salt=1)
        elif kind == "heap":
            c = r.random()
            if z < -100 or (x, z) in R.grass_heap:
                top, soil = (B.GRASS, 0), (B.DIRT, 0)
            else:
                top = (B.STONE, 0) if c < 0.38 else (B.STONE, 5) if c < 0.62 else (B.COBBLE, 0) if c < 0.84 else (B.GRAVEL, 0) if c < 0.94 else (B.COAL_ORE, 0)
        elif kind in ("landing",):
            top = cellpick(x, z, PATH, salt=2) if P.PIECE.get("gantry-land") and x > 0 else cellpick(x, z, SLATE, salt=2)
            if x < 0 and in_rect(x, z, [(-58, -75, -50, -63), (-60, -85, -50, -79)]) and noise_ok(patchA, i, k, 0.35):
                top, soil = (B.GRASS, 0), (B.DIRT, 0)
        elif kind in LAWN_KINDS:
            lane = in_rect(x, z, LANES.get(kind, []))
            pa, pb = patchA[i, k], patchB[i, k]
            for cx, cz, rx, rz, what in PATCHES:
                if ((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2 <= 1:
                    lane = (what == "worn") or (lane and what != "grass")
                    if what == "grass":
                        lane = False
            if lane:
                top = cellpick(x, z, SLATE if kind in ("row", "front") else PATH, salt=3)
            else:
                top, soil = (B.GRASS, 0), (B.DIRT, 0)
                if pa > 0.55:
                    top = (B.DIRT, 2)                                   # podzol
                elif pb > 0.6:
                    top = (B.DIRT, 1)                                   # coarse dirt
        w.set(x, h, z, *top)
        if soil:
            w.set(x, h - 1, z, *soil)
            w.set(x, h - 2, z, *soil)


def noise_ok(field, i, k, thr):
    return field[i, k] > thr


# ---- houses ---------------------------------------------------------------------------------------------------
def clear_windows(L, base=None, margin=2.6):
    """The library's window rhythm with the middle of the long wall left blank: the door is there (build.house puts it
    on the cell nearest the middle), and a window beside it is a foot-hole in the door's frame."""
    base = base or BLD.windows()

    def f(run, span, t, storey):
        if span == L and abs(run - span / 2) < margin:
            return False
        return base(run, span, t, storey)
    return f


STYLE_SLATE = dict(ground=[(B.COBBLE, 0), (B.STONE, 5), (B.STONEBRICK, 0)], upper=[(B.STONE, 5)], post=1, gable=(B.STONE, 5),
                   floor=(B.PLANKS, 1), roof=(B.STONEBRICK, 0), stair=B.STONEBRICK_STAIRS, slab=(B.SLAB, 5),
                   door=B.SPRUCE_DOOR, window=(B.PANE, 0), chimney=(B.COBBLE, 0))
STYLE_KILN = dict(ground=[(B.BRICK, 0)], upper=[(B.BRICK, 0)], post=1, gable=(B.BRICK, 0), floor=(B.STONEBRICK, 0),
                  roof=(B.STONEBRICK, 0), stair=B.STONEBRICK_STAIRS, slab=(B.SLAB, 5), door=B.DARK_OAK_DOOR,
                  window=(B.IRON_BARS, 0))
STYLE_ENGINE = dict(ground=[(B.STONEBRICK, 0), (B.STONE, 5)], upper=[(B.STONEBRICK, 0), (B.STONE, 5)], post=1,
                    gable=(B.STONEBRICK, 0), floor=(B.PLANKS, 1), roof=(B.STONEBRICK, 0), stair=B.STONEBRICK_STAIRS,
                    slab=(B.SLAB, 5), door=B.DARK_OAK_DOOR, window=(B.IRON_BARS, 0))


def put_house(w, spec, floor_of, r, **kw):
    h = BLD.House(windows=clear_windows(spec["L"]), chimney=False, **spec, **kw)
    res = BLD.house(w, h, floor_of, r)
    return h, res


def cottages(w, R, floor, r, stats):
    """The Terrace Row: three slate cottages on the row's north side, doors to the street, and the Chapel at its west end."""
    ground = lambda x, z: int(floor[x - w.x0, z - w.z0])                      # noqa: E731
    out = {}
    for name, cx, L in (("cottage A", -30, 8), ("cottage B", -14, 8), ("cottage C", 6, 8)):
        out[name] = put_house(w, dict(cx=cx, cz=-72, heading=0, L=L, W=6, floor=P.ROW_H, storeys=1, storey=4, style=STYLE_SLATE,
                                      door=1, roof="gable", pitch=1, overhang=1), ground, r)
    out["chapel"] = put_house(w, dict(cx=-41, cz=-74, heading=0, L=10, W=8, floor=P.ROW_H, storeys=1, storey=5, style=STYLE_SLATE,
                                      door=1, roof="gable", pitch=2, overhang=1), ground, r)
    # chimneys on the cottages: a stack of cobble at the gable end, a course above the ridge
    for name in ("cottage A", "cottage B", "cottage C"):
        h, res = out[name]
        x = int(round(h.cx)) + 3
        z = int(round(h.cz)) - 1
        for y in range(P.ROW_H + 1, res["roof"].crown(x, z) + 3):
            w.set(x, y, z, B.COBBLE, 0)
        w.set(x, res["roof"].crown(x, z) + 3, z, B.COBBLE_WALL, 0)
    # the Quarry Office: the long house behind the spawn, set against the bank
    h, res = put_house(w, dict(cx=-1, cz=-99, heading=0, L=14, W=6, floor=P.SPAWN_H, storeys=1, storey=5, style=STYLE_ENGINE,
                               door=1, roof="gable", pitch=1, overhang=1), ground, r)
    out["office"] = (h, res)
    stats["doors"] = {k: v[1]["door"] for k, v in out.items()}
    return out


def wool_house(w, spec, floor, door, found, wool_dye, banner_colour, name, r):
    """A wool room: the library's house, its door read back, the wool on a pedestal, the studio's wool-room loot in the four
    inner corners, a banner of the wool's colour and a sign over the door."""
    ground = lambda x, z: floor                                               # noqa: E731
    h, res = put_house(w, spec, ground, r)
    dx, dz, face = res["door"]
    if (dx, dz) != door:
        raise RuntimeError(f"{name}: the library put the door at {(dx, dz)}, the plan says {door}")
    x0, z0, x1, z1 = res["footprint_box"] if "footprint_box" in res else box_of(res["footprint"])
    inside = (x0 + 1, z0 + 1, x1 - 1, z1 - 1)
    props.wool_chests(w, inside, floor, door=face if isinstance(face, str) else "w")
    return h, res, inside


def box_of(cells):
    xs = [c[0] for c in cells]
    zs = [c[1] for c in cells]
    return min(xs), min(zs), max(xs), max(zs)


def chimney(w, x, z, y0, top):
    for y in range(y0, top):
        w.set(x, y, z, B.BRICK, 0)
    w.set(x, top, z, B.SLAB, 4)
    w.set(x, top + 1, z, B.COBBLE_WALL, 0)


def headframe(w, box, floor):
    """The winding gear on the High Bench: four spruce legs, cross braces, a wheel of planks and fence at the head, a cable of
    fence hanging into a skip of iron bars beside the engine house. Landmark: it stands on the skyline from the spawn."""
    x0, z0, x1, z1 = box
    top = floor + 16
    for x in (x0, x1):
        for z in (z0, z1):
            for y in range(floor + 1, top + 1):
                w.set(x, y, z, B.LOG, 1)
    for y in (floor + 5, floor + 10, top):
        for x in range(x0, x1 + 1):
            for z in (z0, z1):
                w.set(x, y, z, B.LOG, 1 | 4)
        for z in range(z0, z1 + 1):
            for x in (x0, x1):
                w.set(x, y, z, B.LOG, 1 | 8)
    cx = (x0 + x1) // 2
    cz = (z0 + z1) // 2
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)):
        w.set(cx + dx, top + 2 + dy, cz, B.PLANKS if dx == 0 or dy == 0 else B.FENCE, 1 if dx == 0 or dy == 0 else 0)
    w.set(cx, top + 2, cz, B.LOG, 1 | 4)
    for y in range(floor + 1, top - 1):
        w.set(cx, y, cz, B.FENCE, 0)                                            # the cable
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(cx + dx, floor + 1, cz + dz, B.IRON_BARS if (dx or dz) else B.AIR)


def hung_banner_and_sign(w, x, y, z, side, base, text):
    facing = {"w": 4, "e": 5, "n": 2, "s": 3}[side]
    w.banner(x, y + 2, z, base, wall_facing=facing)
    sx, sz = x, z
    w.sign(sx, y + 1, sz, text, wall_facing=facing)


def kiln_and_winding(w, floor, r, O, stats):
    kx0, kz0, kx1, kz1 = P.KILN
    kcx, kcz = (kx0 + kx1 + 1) / 2, (kz0 + kz1 + 1) / 2
    spec = dict(cx=kcx, cz=kcz, heading=90, L=kz1 - kz0 + 1, W=kx1 - kx0 + 1, floor=P.QUARRY_H, storeys=1, storey=P.ROOM_H,
                style=STYLE_KILN, door=1, roof="gable", pitch=2, overhang=1)
    h, res, inside = wool_house(w, spec, P.QUARRY_H, (kx0, (kz0 + kz1) // 2), None, None, None, "kiln", r)
    stats["kiln door"] = res["door"]
    for (which, (x, z), top) in P.CHIMNEYS:
        if which == "kiln":
            chimney(w, x, z, P.QUARRY_H + 1, top)
    hung_banner_and_sign(w, kx0 - 1, P.QUARRY_H + 3, (kz0 + kz1) // 2, "w", 1, ["", "THE KILN", "orange wool", ""])
    # inside: a firing bench of furnaces along the north wall, a lamp
    for x in range(inside[0] + 1, inside[2], 2):
        w.set(x, P.QUARRY_H + 1, inside[1], B.FURNACE, 3)
    w.set((inside[0] + inside[2]) // 2, P.QUARRY_H + 5, (inside[1] + inside[3]) // 2, B.GLOWSTONE, 0)
    wx0, wz0, wx1, wz1 = P.WIND
    wcx, wcz = (wx0 + wx1 + 1) / 2, (wz0 + wz1 + 1) / 2
    spec = dict(cx=wcx, cz=wcz, heading=90, L=wz1 - wz0 + 1, W=wx1 - wx0 + 1, floor=P.BENCH_H, storeys=1, storey=P.ROOM_H,
                style=STYLE_ENGINE, door=-1, roof="gable", pitch=2, overhang=1)
    h, res, inside = wool_house(w, spec, P.BENCH_H, (wx1, (wz0 + wz1) // 2), None, None, None, "winding", r)
    stats["winding door"] = res["door"]
    for (which, (x, z), top) in P.CHIMNEYS:
        if which == "wind":
            chimney(w, x, z, P.BENCH_H + 1, top)
    headframe(w, P.HEADFRAME, P.BENCH_H)
    hung_banner_and_sign(w, wx1 + 1, P.BENCH_H + 3, (wz0 + wz1) // 2, "e", 6, ["", "WINDING HOUSE", "cyan wool", ""])
    w.set((inside[0] + inside[2]) // 2, P.BENCH_H + 5, (inside[1] + inside[3]) // 2, B.GLOWSTONE, 0)


# ---- walls, rails, cover ---------------------------------------------------------------------------------------
def bedrock_walls(w, R):
    X, Z = w.grid()
    for i, k in np.argwhere(R.mask("barrier") & (Z < 0)):
        x, z, top = int(X[i, k]), int(Z[i, k]), int(R.H[i, k])
        for y in range(1, top + 1):
            w.set(x, y, z, B.BEDROCK)
    # the studio's defence chests, in the front face, apart so two do not make a double chest
    props.defence_chests(w, [(P.WALL_G["x0"], -59), (P.WALL_G["x0"], -56)], 63, "w")
    props.defence_chests(w, [(P.WALL_W["x1"], -84), (P.WALL_W["x1"], -80)], P.LAND2_H + 1, "e")


def clear_ledges(w, R, radius=7):
    """The karst ledges the rock jutted out below a rim, within `radius` of a bedrock wall, are cut away: a ledge beside a wall
    is a way round it. Only void columns are cleared; the wall's own piece keeps its rock."""
    X, Z = w.grid()
    from scipy import ndimage
    barrier = R.mask("barrier") & (Z < 0)
    near = ndimage.binary_dilation(barrier, structure=np.ones((3, 3), bool), iterations=radius)
    void = R.K == R.kinds["void"]
    cols = near & void
    n = 0
    for i, k in np.argwhere(cols):
        col = w.ids[i, P.KILL_Y + 1:, k]
        n += int((col != 0).sum())
        w.ids[i, P.KILL_Y + 1:, k] = 0
        w.dat[i, P.KILL_Y + 1:, k] = 0
    return n


def rails(w, R):
    """A fence along the open edges of the narrow pieces (the landings and the gantry's landing): where a neighbour is void."""
    X, Z = w.grid()
    for i, k in np.argwhere(R.mask("landing") & (Z < 0)):
        x, z, h = int(X[i, k]), int(Z[i, k]), int(R.H[i, k])
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if R.inside(x + dx, z + dz) and R.kind(x + dx, z + dz) == "void":
                if w.id(x, h + 1, z) == B.AIR:
                    w.set(x, h + 1, z, B.SPRUCE_FENCE, 0)
                break


def slate_stack(w, x, z, y, long_x=True):
    """A stack of cut slate, three by two and two high with a slab on top: cover a player crouches behind."""
    a, b = (3, 2) if long_x else (2, 3)
    for dx in range(a):
        for dz in range(b):
            w.set(x + dx, y + 1, z + dz, B.STONE, 6)
            w.set(x + dx, y + 2, z + dz, B.STONE, 5)
            w.set(x + dx, y + 3, z + dz, B.SLAB, 5)


def shed(w, x0, z0, x1, z1, y):
    """An open dressing shed: spruce posts at the corners and every four, a slab roof, slate racks under it."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            w.set(x, y + 4, z, B.WOOD_SLAB, 1)
    for x in range(x0, x1 + 1, 4):
        for z in (z0, z1):
            for yy in range(y + 1, y + 4):
                w.set(x, yy, z, B.LOG, 1)
    for x in range(x0 + 1, x1, 2):
        w.set(x, y + 1, z0 + 1, B.STONE, 6)
        w.set(x, y + 2, z0 + 1, B.STONE, 5)


def oven(w, cx, cz, y):
    """A beehive oven: a shell of red brick, three out and three high, a mouth toward the west, a firebox of netherrack."""
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            for dy in range(0, 4):
                rr = (dx * dx + dz * dz + dy * dy * 1.3) ** 0.5
                if 2.3 < rr <= 3.3 and not (dx == -3 and dz == 0 and dy < 2):
                    w.set(cx + dx, y + 1 + dy, cz + dz, B.BRICK, 0)
    w.set(cx, y + 1, cz, B.NETHERRACK, 0)
    w.set(cx, y + 2, cz, B.FIRE, 0)


def cover_and_dressing(w, R, floor, r, stats):
    F = P.FRONT_H
    # the Dressing Floor: two sheds and four slate stacks in the open ground, the lane between kept clear (x -6..6)
    shed(w, -33, -44, -22, -39, F)
    shed(w, 12, -44, 23, -39, F)
    for x, z, lx in ((-24, -28, True), (14, -30, True), (-12, -22, False), (8, -22, False), (-44, -24, True), (30, -24, False)):
        slate_stack(w, x, z, F, lx)
    # the Cart Yard: the weighbridge (a hut), the cart track, a wagon of slate on it
    ground = lambda x, z: P.YARD_H                                          # noqa: E731
    put_house(w, dict(cx=6, cz=-53, heading=0, L=6, W=5, floor=P.YARD_H, storeys=1, storey=4, style=STYLE_SLATE, door=1,
                      roof="shed", pitch=1, overhang=1), ground, r)
    for x in range(-34, 18):
        if w.id(x, P.YARD_H + 1, -58) == B.AIR and w.id(x, P.YARD_H, -58) != B.AIR:
            w.set(x, P.YARD_H + 1, -58, B.RAIL, 1)
    for x in (-8, -7, -6):
        for dz in (0, 1):
            pass
    w.set(-9, P.YARD_H + 1, -58, B.STONE, 6)
    for x in range(-12, -9):
        w.set(x, P.YARD_H + 1, -58, B.STONEBRICK, 0)
        w.set(x, P.YARD_H + 2, -58, B.STONE, 6)
    for x in range(-12, -9):
        w.set(x, P.YARD_H + 1, -57, B.COBBLE_WALL, 0)
    # the Quarry Floor: a derrick (a mast and its boom), stacks of cut slate beside the Pit, rails to the Kiln
    for y in range(P.QUARRY_H + 1, P.QUARRY_H + 15):
        w.set(36, y, -58, B.LOG, 1)
    for t in range(1, 9):
        w.set(36 + t, P.QUARRY_H + 14 - t // 3, -58, B.FENCE, 0)
    for x, z, lx in ((35, -76, True), (53, -57, True), (41, -75, False)):
        slate_stack(w, x, z, P.QUARRY_H, lx)
    for x in range(33, 52):
        if w.id(x, P.QUARRY_H + 1, -59) == B.AIR and w.id(x, P.QUARRY_H, -59) != B.AIR:
            w.set(x, P.QUARRY_H + 1, -59, B.RAIL, 1)
    for x in (-34, -22, -10, 10, 22, 34):                                       # lamps along the lip: where the bridge begins
        props.lamp(w, x, F, -14, height=2)
    # the Kiln's two beehive ovens, west of the door, and more slate on the Dressing Floor
    for cx, cz in ((50, -75), (50, -57)):
        oven(w, cx, cz, P.QUARRY_H)
    for x, z, lx in ((-40, -34, True), (26, -36, False), (-18, -33, False), (18, -20, True), (-26, -18, True), (-8, -28, False)):
        slate_stack(w, x, z, F, lx)
    # the front lip: a sign at each end and in the middle says where the bridge goes
    for x in (-30, 0, 30):
        w.sign(x, F + 1, -15, ["", "BUILD HERE", "bridge the band", ""], rot=0)
    # lamps where lanes meet flights
    for x, z, y in ((-4, -84, P.SPAWN_H), (4, -84, P.SPAWN_H), (-12, -66, P.ROW_H), (12, -66, P.ROW_H), (-6, -50, P.YARD_H),
                    (6, -50, P.YARD_H), (-8, -44, P.FRONT_H), (8, -44, P.FRONT_H), (-8, -16, P.FRONT_H), (8, -16, P.FRONT_H),
                    (-66, -92, P.BENCH_H), (-66, -80, P.BENCH_H), (-52, -71, P.LAND1_H)):
        props.lamp(w, x, y, z, height=2)


def monuments_and_spawn(w, floor, r):
    """The monuments' lawn: a stone-brick ring round each slot, two lamps, so a player finds it; the spawn's iron."""
    for sx, _, sz in P.MONUMENT_SLOTS:
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                if max(abs(dx), abs(dz)) == 2:
                    w.set(sx + dx, P.SPAWN_H, sz + dz, B.STONEBRICK, 0 if (dx + dz) % 2 else 3)
        for dx in (-2, 2):
            props.lamp(w, sx + dx, P.SPAWN_H, sz + 3, height=2)
    for x0 in (-33, 27):                                                    # the iron: a cube of three, mined and grown back
        for dx in range(3):
            for dy in range(3):
                for dz in range(3):
                    w.set(x0 + dx, P.SPAWN_H + 1 + dy, -93 + dz, B.IRON_ORE, 0)


def trees_(w, R, r, stats):
    """Spruces in a few chosen places, none on a lane, a flight or a doorstep: the bank behind the spawn, the spawn terrace's
    west rim, the row's north bank beside the chapel, the bench's north edge, the Dressing Floor's two far corners."""
    lib = trees.library()
    by = trees.kinds(lib)
    spots = [(-33, -104, P.SPAWN_H + 4, "tall-spruce"), (-26, -103, P.SPAWN_H + 4, "large-pine"), (24, -104, P.SPAWN_H + 4, "tall-spruce"),
             (-34, -96, P.SPAWN_H, "tiny-spruce"), (28, -99, P.SPAWN_H, "tiny-spruce"), (-76, -97, P.BENCH_H, "tiny-spruce"),
             (-66, -97, P.BENCH_H, "tiny-spruce"),              (-48, -26, P.FRONT_H, "tiny-spruce"), (36, -20, P.FRONT_H, "tiny-spruce"), (-49, -44, P.FRONT_H, "tiny-spruce")]
    n = 0
    stats['tree spots'] = []
    for x, z, y, kind in spots:
        ts = by[kind]
        t = ts[int(r.integers(len(ts)))]
        g = int(R.h(x, z)) if R.inside(x, z) else y
        if trees.plant(w, x, z, t, turn=int(r.integers(4))):
            n += 1
            stats['tree spots'].append((x, z, kind))
    stats["trees"] = n


def everything(w, R, land_r, floor, O, stats):
    r = noise_rng("dress")
    cottages(w, R, floor, r, stats)
    kiln_and_winding(w, floor, r, O, stats)
    bedrock_walls(w, R)
    stats['ledges cut'] = clear_ledges(w, R)
    rails(w, R)
    cover_and_dressing(w, R, floor, r, stats)
    monuments_and_spawn(w, floor, r)
    trees_(w, R, r, stats)


def noise_rng(name):
    from pgmvox import rng
    return rng(P.BOARD, name)


# ---- the build zones' marks, the mist -------------------------------------------------------------------------
def marks(w, R, stats):
    """Block 36 at y 0 under every column a player may build in (land and zones, both halves), and the studio's outline of the
    build area: unpowered redstone at y 1, two blocks out from every void-facing edge of a zone, one air clear of zones and
    terrain. A sign on each front lip says where the bridge goes."""
    from scipy import ndimage
    zone = P.zone_mask(R)
    build_cols = ~R.mask("void") | zone
    w.ids[:, 0, :][build_cols] = 36
    zfull = zone | (~R.mask("void") & np.isin(R.K, [R.kinds["front"]]))
    terr = (w.ids[:, P.KILL_Y:P.MAX_BUILD, :] != 0).any(axis=1)
    nx, nz = zone.shape
    sides = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    marker = set()
    for i, k in np.argwhere(zfull):
        fv = [0 <= i + dx < nx and 0 <= k + dz < nz and not zfull[i + dx, k + dz] and not terr[i + dx, k + dz] for dx, dz in sides]
        for s, (dx, dz) in enumerate(sides):
            if fv[s]:
                marker.add((i + 2 * dx, k + 2 * dz))
        for f, g in ((0, 2), (0, 3), (1, 2), (1, 3)):
            if fv[f] and fv[g]:
                (ax, az), (bx, bz) = sides[f], sides[g]
                for st in (1, 2):
                    marker.add((i + ax * st + bx * 2, k + az * st + bz * 2))
                    marker.add((i + ax * 2 + bx * st, k + az * 2 + bz * st))
    crowd = ndimage.maximum_filter(zfull | terr, size=3)
    n = 0
    for i, k in marker:
        if 0 <= i < nx and 0 <= k < nz and not crowd[i, k]:
            w.ids[i, 1, k], w.dat[i, 1, k] = B.REDSTONE_WIRE, 0
            n += 1
    stats["outline"] = n
    stats["marked"] = int(build_cols.sum())


def mist(w, R, stats):
    """A mist of grey glass far under the kill height, so the void reads as a drop and not as nothing."""
    from pgmvox import terrain as T
    before = int((w.ids == B.STAINED_GLASS).sum())
    from scipy import ndimage
    zone = ndimage.binary_dilation(P.zone_mask(R), iterations=4)                # no mist over the zones: the outline shows
    T.cloud_deck(w, 20, mask=~zone, seed=51, cell=16, puff=5, breaks=-0.1, materials=((B.STAINED_GLASS, 0), (B.STAINED_GLASS, 8)))
    stats["mist"] = int((w.ids == B.STAINED_GLASS).sum()) - before
