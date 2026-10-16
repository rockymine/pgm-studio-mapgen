"""What stands on Hoarfire's ground and what is cut into it, drawn on Rowan's half (z < 0) and mirrored by gen.py:
the paths, the court and the spring, the buildings, the Thaw's bridge and ford, the Ember Pit and its kilns, the
monument's shelf and seracs, the glacier's crevasses, the Ice Cave, the woods, the harvest field, the falls into the
Rift and the two islets.

Every function takes the world and writes into it; `everything` calls them in the order they must run (ground
cover before trees, trees after everything that claims ground).
"""
import math

import numpy as np

import buildings
import land
import plan as P
from pgmvox import B, rng
from pgmvox.core.orient import stair
from pgmvox.geom import noise, shapes
from pgmvox.scenery import forms
from pgmvox.scenery import trees as TR
from pgmvox.surface import terrain as T
from pgmvox.volume import under

RED = P.Z < 0
SOFT = {B.AIR, B.SNOW_LAYER, B.TALLGRASS, B.FLOWER, B.DANDELION, B.DOUBLE_PLANT, B.DEADBUSH, B.CARPET}


def top(w, x, z):
    """The y of the ground block in a column: the highest block that is not air, a plant or lying snow."""
    i, k = x - w.x0, z - w.z0
    col = w.ids[i, :, k]
    for y in range(w.sy - 1, 0, -1):
        if col[y] not in SOFT and col[y] not in (B.LEAVES, B.LEAVES2, B.LOG, B.LOG2):
            return y
    return -1


def clear_above(w, x, y, z, n=1):
    for yy in range(y + 1, y + 1 + n):
        if w.id(x, yy, z) in SOFT:
            w.set(x, yy, z, B.AIR)


def mix(r, blocks):
    """One of `blocks` drawn evenly: a set laid a share each."""
    return blocks[int(r * len(blocks)) % len(blocks)]


# ---- paths -------------------------------------------------------------------------------------------------------
WINTER_PATH = [(B.GRAVEL, 0), (B.STONE, 5), (B.COBBLE, 0)]
AUTUMN_PATH = [(B.DIRT, 1), (B.DIRT, 2), (B.PLANKS, 1)]
COURT_FLOOR = [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)]


def paths(w, wint, r):
    """Every path of the plan, three blocks wide, laid in the ground's own set: gravel, andesite and cobble on the
    snow, coarse dirt, podzol and spruce planks on the autumn ground. A rise of one gets a stair of the path's
    tone so a path never asks for a jump."""
    X, Z = P.X, P.Z
    wid = np.zeros(X.shape, bool)
    for name, pts in P.PATHS.items():
        d, _ = shapes.polyline(X, Z, pts)
        wid |= d <= 1.5
    wid &= RED & P.LAND & ~P.WET & ~P.G["tarn"].mask
    for i, k in np.argwhere(wid):
        x, z = int(X[i, k]), int(Z[i, k])
        y = top(w, x, z)
        if y < 0 or w.id(x, y, z) in (B.WATER, B.ICE, B.PLANKS):
            continue
        blk = mix(r.random(), WINTER_PATH if wint[i, k] > 0 else AUTUMN_PATH)
        w.set(x, y, z, *blk)
        clear_above(w, x, y, z, 2)


# ---- the court, the spring and the hearth --------------------------------------------------------------------------
def court(w, r):
    x0, z0, x1, z1 = land.COURT
    sp = P.G["spring"].mask
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            i, k = x - w.x0, z - w.z0
            if sp[i, k]:
                continue
            y = land.COURT_Y
            for yy in range(y - 3, y):
                if w.id(x, yy, z) == 0:
                    w.set(x, yy, z, B.STONE, 0)
            edge = x in (x0, x1) or z in (z0, z1)
            w.set(x, y, z, *((B.STONEBRICK, 0) if edge else mix(r.random(), COURT_FLOOR)))
            for yy in range(y + 1, y + 6):
                w.set(x, yy, z, B.AIR)
    # the spring's rim: a kerb of stone brick round the pool, a block proud of the court
    rim = shapes.boundary(np.pad(sp, 1), diagonal=True)
    ring = np.zeros_like(sp)
    from scipy import ndimage
    grown = ndimage.binary_dilation(sp, np.ones((3, 3), bool))
    ring = grown & ~sp
    for i, k in np.argwhere(ring & RED):
        x, z = int(P.X[i, k]), int(P.Z[i, k])
        w.set(x, land.COURT_Y, z, B.STONEBRICK, 0)
        w.set(x, land.COURT_Y + 1, z, B.SLAB, 5)
    # the court is made ground: a retaining wall of stone brick on its open sides, and a flight down where each
    # path leaves it
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if not (x in (x0, x1) or z == z1):
                continue
            for yy in range(top(w, x, z) - 4, land.COURT_Y):
                if w.id(x, yy, z) in (0, B.DIRT, B.GRASS, B.SNOW, B.STONE):
                    w.set(x, yy, z, *((B.STONEBRICK, 0) if r.random() < 0.8 else (B.STONEBRICK, 2)))
    for sx, sz, way, width in ((-12, -80, "w", 3), (12, -80, "e", 3), (5, -74, "s", 4)):
        flight(w, sx, sz, way, width, land.COURT_Y)
    # the hearth: a fire pit on the court's east side, lava under iron bars in a ring of cobble walls
    hx, hz = 7, -79
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            d = max(abs(dx), abs(dz))
            x, z = hx + dx, hz + dz
            if d == 2:
                w.set(x, land.COURT_Y + 1, z, B.COBBLE_WALL, 0)
            elif d == 1:
                w.set(x, land.COURT_Y, z, B.NETHERRACK, 0)
                w.set(x, land.COURT_Y + 1, z, B.IRON_BARS, 0)
            else:
                w.set(x, land.COURT_Y - 1, z, B.NETHERRACK, 0)
                w.set(x, land.COURT_Y, z, B.LAVA, 0)
                w.set(x, land.COURT_Y + 1, z, B.IRON_BARS, 0)
    for dx, dz in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
        w.set(hx + dx, land.COURT_Y + 2, hz + dz, B.JACK, 0)
    # log benches round the west of the spring, facing it
    for x, z, axis in ((-6, -84, 8), (-6, -77, 4), (4, -84, 8)):
        for s in range(3):
            bx, bz = (x, z + s) if axis == 8 else (x + s, z)
            w.set(bx, land.COURT_Y + 1, bz, B.LOG, 1 | axis)


def flight(w, x, z, way, width, y0):
    """A flight of stone-brick stairs out of made ground: from the edge cell (x, z) at y0 down toward `way`, a
    block a block, until it meets the ground, `width` wide, filled under with stone."""
    from pgmvox.core.orient import vec
    dx, dz = vec(way)
    rx, rz = -dz, dx
    up = {"w": "e", "e": "w", "s": "n", "n": "s"}[way]
    y = y0
    for k in range(1, 12):
        cx, cz = x + dx * k, z + dz * k
        ground = min(top(w, cx + rx * j, cz + rz * j) for j in range(-(width // 2), width - width // 2))
        if ground >= y - 1:
            for j in range(-(width // 2), width - width // 2):
                gx, gz = cx + rx * j, cz + rz * j
                if top(w, gx, gz) < y - 1:
                    w.set(gx, y - 1, gz, B.STONEBRICK, 0)
            break
        y -= 1
        for j in range(-(width // 2), width - width // 2):
            gx, gz = cx + rx * j, cz + rz * j
            for yy in range(top(w, gx, gz), y):
                w.set(gx, yy, gz, B.STONE, 0)
            w.set(gx, y, gz, B.STONEBRICK_STAIRS, stair(up))
            for yy in range(y + 1, y + 4):
                w.set(gx, yy, gz, B.AIR)
        for j in (-(width // 2) - 1, width - width // 2):
            gx, gz = cx + rx * j, cz + rz * j
            for yy in range(top(w, gx, gz), y + 1):
                w.set(gx, yy, gz, B.STONEBRICK, 0)


# ---- the Thaw's bridge and ford ----------------------------------------------------------------------------------
def thaw_crossings(w, r):
    a, b, c, d = P.BRIDGE
    deck = max(top(w, a - 1, b), top(w, c + 1, b), top(w, a - 1, d), top(w, c + 1, d))
    for x in range(a - 1, c + 2):
        for z in range(b, d + 1):
            edge = z in (b, d)
            ab = x in (a - 1, c + 1)
            w.set(x, deck, z, *((B.LOG, 1 | 4) if edge else (B.PLANKS, 1)))
            for y in range(deck + 1, deck + 4):
                w.set(x, y, z, B.AIR)
            if edge:
                w.set(x, deck + 1, z, *((B.LOG, 1) if ab or x == (a + c) // 2 else (B.SPRUCE_FENCE, 0)))
            if ab:
                g = top(w, x, z)
                for y in range(min(g, deck) - 3, deck):
                    w.set(x, y, z, B.COBBLE if r.random() < 0.4 else B.STONE, 0 if r.random() < 0.5 else 5)
    for x in ((a + c) // 2,):
        for z in (b, d):
            w.set(x, deck + 2, z, B.JACK, 0 if z == b else 2)
    # the ford: stepping stones of andesite and cobble across the water
    fx0, fz0, fx1, fz1 = P.FORD
    zz = (fz0 + fz1) // 2
    for x in range(fx0, fx1 + 1):
        if w.id(x, top(w, x, zz) + 1, zz) == B.WATER or w.id(x, top(w, x, zz), zz) in (B.GRAVEL,):
            y = int(P.G["thaw"].surface[x - w.x0, zz - w.z0])
            if y > 0 and x % 2 == 0:
                w.set(x, y, zz, *((B.STONE, 5) if r.random() < 0.6 else (B.COBBLE, 0)))


# ---- the Ember Pit, its kilns and log stacks -------------------------------------------------------------------------
def ember_pit(w, r):
    cx, cz = land.CORE
    g0 = P.H[cx - w.x0, cz - w.z0]
    for x in range(cx - land.PIT_R - 1, cx + land.PIT_R + 1):
        for z in range(cz - land.PIT_R - 1, cz + land.PIT_R + 1):
            dd = math.hypot(x - cx + 0.5, z - cz + 0.5)
            if dd > land.PIT_R + 0.5:
                continue
            y = top(w, x, z)
            if dd <= land.PIT_R - 1.5:
                w.set(x, y, z, *mix(r.random(), [(B.COAL_BLOCK, 0), (B.NETHERRACK, 0), (B.GRAVEL, 0), (B.COAL_BLOCK, 0)]))
            else:
                w.set(x, y, z, *mix(r.random(), [(B.STONE, 0), (B.STONE, 5), (B.COBBLE, 0)]))
            clear_above(w, x, y, z, 3)
    # a ring of stone-brick kerb round the pit's lip, broken where the Hollow Way comes in
    for a in range(0, 360, 4):
        t = math.radians(a)
        x = int(math.floor(cx - 0.5 + (land.PIT_R + 1.2) * math.cos(t) + 0.5))
        z = int(math.floor(cz - 0.5 + (land.PIT_R + 1.2) * math.sin(t) + 0.5))
        if 200 < a < 250:
            continue
        y = top(w, x, z)
        if y >= g0 - 2:
            w.set(x, y, z, B.STONEBRICK, 0)
            clear_above(w, x, y, z)
    for kx, kz in P.KILNS:
        kiln(w, kx, kz, r)
    # log stacks at the clearing's edge: felled oak laid along x and along z
    for x, z, axis, n in ((22, -56, 4, 4), (50, -50, 8, 4), (42, -40, 4, 4)):
        y = top(w, x, z)
        for s in range(n):
            bx, bz = (x + s, z) if axis == 4 else (x, z + s)
            yy = top(w, bx, bz)
            w.set(bx, yy + 1, bz, B.LOG, 0 | axis)
            if s < n - 1:
                w.set(bx, yy + 2, bz, B.LOG, 0 | axis)
            if 0 < s < n - 2:
                w.set(bx, yy + 3, bz, B.LOG, 0 | axis)


def kiln(w, kx, kz, r):
    """A charcoal kiln: a low dome of earth over a stack, its crown smouldering (a jack-o-lantern's glow under a
    netherrack cap), an opening at its foot."""
    y0 = top(w, kx, kz)
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            d = math.hypot(dx, dz)
            if d > 3.2:
                continue
            hgt = int(round(3.2 * math.sqrt(max(0, 1 - (d / 3.3) ** 2))))
            g = top(w, kx + dx, kz + dz)
            for y in range(g + 1, y0 + hgt + 1):
                blk = mix(r.random(), [(B.DIRT, 1), (B.DIRT, 0), (B.DIRT, 2)]) if y == y0 + hgt else (B.DIRT, 1)
                if d > 2.4 and y == y0 + hgt and r.random() < 0.4:
                    blk = (B.COAL_BLOCK, 0)
                w.set(kx + dx, y, kz + dz, *blk)
    w.set(kx, y0 + 3, kz, B.NETHERRACK, 0)
    w.set(kx, y0 + 2, kz, B.JACK, 0)
    w.set(kx, y0 + 4, kz, B.COBBLE_WALL, 0)


# ---- the monument's shelf and the seracs -------------------------------------------------------------------------
def rime_shelf(w, r):
    """The shelf under the monument: a disc of packed ice (the old tarn's last ice) in the snow, ringed with
    snow; the four seracs about it."""
    b = P.MONUMENT_BOX
    cx, cz = (b.x0 + b.x1) / 2, (b.z0 + b.z1) / 2
    for x in range(int(cx) - 5, int(cx) + 6):
        for z in range(int(cz) - 5, int(cz) + 6):
            d = math.hypot(x - cx, z - cz)
            y = top(w, x, z)
            if d <= 3.6:
                w.set(x, y, z, B.PACKED_ICE, 0)
                clear_above(w, x, y, z)
    for sx, sz, h in P.SERACS:
        stone(w, sx, sz, h, r)


def stone(w, sx, sz, h, r):
    """A standing stone of the Rime Shelf's ring: a leaning slab of andesite and stone, rime (packed ice) on its
    windward face and snow on its crown."""
    y = top(w, sx, sz)
    m = forms.spike(w, [(sx + 0.5, y - 1, sz + 0.5), (sx + 0.5 + 0.06 * h, y + h, sz + 0.5 - 0.04 * h)],
                    (1.7, 0.7, 0.8), sides=4, twist=20, rough=0.12, seed=abs(sx * 7 + sz))
    ii, yy, kk = np.nonzero(m)
    for i, y_, k in zip(ii, yy, kk):
        windward = not m[i, y_, k - 1] if k > 0 else True
        w.ids[i, y_, k] = B.PACKED_ICE if windward and r.random() < 0.6 else (B.STONE if r.random() < 0.6 else B.STONE)
        w.dat[i, y_, k] = 0 if w.ids[i, y_, k] == B.PACKED_ICE else (5 if r.random() < 0.55 else 0)
    for i, k in {(int(a), int(c)) for a, c in zip(ii, kk)}:
        col = np.nonzero(m[i, :, k])[0]
        t = int(col.max()) + 1
        if w.ids[i, t, k] == 0:
            w.ids[i, t, k], w.dat[i, t, k] = B.SNOW_LAYER, 1


# ---- the glacier: crevasses, a snout face, the drift --------------------------------------------------------------
def glacier(w, r):
    pts = land.GLACIER
    total = shapes.length(pts)
    ice = P.G["ice"]
    for t, depth in ((0.42, 4), (0.6, 3), (0.76, 3)):
        (px, pz), (ux, uz) = shapes.point_at(pts, t * total)
        for s in np.arange(-14, 14, 0.5):
            wob = 0.8 * math.sin(s * 0.5 + t * 9)
            x = int(round(px - uz * s + ux * wob))
            z = int(round(pz + ux * s + uz * wob))
            if not (P.X_MIN <= x <= P.X_MAX and P.Z_MIN <= z < 0) or ice[x - w.x0, z - w.z0] < 4:
                continue
            for dx in (0, 1):
                y = top(w, x + dx, z)
                for yy in range(y - depth + 1, y + 1):
                    w.set(x + dx, yy, z, B.AIR)
    # the snout's face: bands of snow in the ice
    # (the ground pass laid the ice in bands already; nothing to add)


# ---- the Ice Cave -------------------------------------------------------------------------------------------------
def ice_cave(w, r):
    """A passage from the Rime Tarn's south-west bank to a ledge in the Rift's cliff: carved round, its walls and
    ceiling lined in packed ice, its floor gravel and andesite; its mouth on the bank cut as a notch in the snow."""
    pts = [(x, y, z, 2.2) for x, z, y in P.CAVE]
    before = w.ids.copy()
    carved, floor = under.tunnel(w, pts, ground=None, cover=0)
    open_ = (before != 0) & (w.ids == 0)
    from scipy import ndimage
    shell = ndimage.binary_dilation(open_, np.ones((3, 3, 3), bool)) & ~open_ & (w.ids != 0)
    ii, yy, kk = np.nonzero(shell)
    for i, y, k in zip(ii, yy, kk):
        x, z = int(i) + w.x0, int(k) + w.z0
        below_open = y + 1 < w.sy and open_[i, y + 1, k]
        if below_open:                                    # a floor
            w.ids[i, y, k], w.dat[i, y, k] = mix(r.random(), [(B.GRAVEL, 0), (B.STONE, 5), (B.STONE, 0)])
        elif w.ids[i, y, k] not in (B.WATER, B.ICE, B.SNOW_LAYER):
            w.ids[i, y, k], w.dat[i, y, k] = (B.PACKED_ICE, 0) if r.random() < 0.75 else (B.SNOW, 0)
    # the mouth on the bank: cut down from the ground to the passage's first floor
    x0, z0, y0 = P.CAVE[0]
    for dz in range(-3, 3):
        for dx in (-1, 0, 1):
            x, z = x0 + dx, z0 + dz
            g = top(w, x, z)
            fl = y0 + max(0, -dz - 1)
            for y in range(fl + 1, g + 1):
                w.set(x, y, z, B.AIR)
            w.set(x, fl, z, B.SNOW, 0)
    # the ledge under the cliff mouth: a lip of packed ice the cave opens onto
    x1, z1, y1 = P.CAVE[-1]
    for dx in range(-2, 3):
        for dz in range(0, 3):
            x, z = x1 + dx, z1 + dz
            if w.id(x, y1, z) == 0:
                w.set(x, y1, z, B.PACKED_ICE, 0)
                if abs(dx) < 2 and dz < 2:
                    w.set(x, y1 - 1, z, B.PACKED_ICE, 0)


# ---- the harvest field ---------------------------------------------------------------------------------------------
def field(w, r):
    from pgmvox.built import props
    x0, z0, x1, z1 = land.FIELD
    props.crop_field(w, (x0, z0, x1, z1), land.FIELD_Y, [(B.WHEAT, 7), (B.CARROTS, 7), (B.WHEAT, 7), (B.POTATOES, 7)],
                     r, rows=4, ditch=None, fence="w", gate=(z0 + z1) // 2)
    # pumpkins left in the last strip, and the scarecrow
    for x in range(x0 + 2, x1 - 1, 2):
        for z in (z1 - 2,):
            w.set(x, land.FIELD_Y + 1, z, B.PUMPKIN, int(r.integers(4)))
    props.scarecrow(w, (x0 + x1) // 2, (z0 + z1) // 2 - 1, facing="s")
    # hay ricks at the field's top
    for hx, hz in ((x1 + 2, z0 + 1), (x1 + 2, z0 + 4)):
        y = top(w, hx, hz)
        for dx in (0, 1):
            for dz in (0, 1):
                w.set(hx + dx, y + 1, hz + dz, B.HAY, 0)
        w.set(hx, y + 2, hz, B.HAY, 4)


# ---- woods -----------------------------------------------------------------------------------------------------------
def spruce(w, x, z, h, r, snow=0.75):
    """A snowy spruce: a trunk `h` high under tiers of spruce leaves that widen every other course, snow on every
    leaf with sky over it. Refused (False) where it would stand in anything but air."""
    y0 = top(w, x, z)
    if y0 < 0:
        return False
    tiers = []
    rmax = max(2, h // 4)
    for k in range(2, h + 1):
        frac = (k - 2) / max(1, h - 2)
        rad = rmax * (1 - frac) + 0.2
        if k % 2 == 1:
            rad *= 0.6
        tiers.append((y0 + k, rad))
    cells = []
    for yy, rad in tiers:
        rr = int(math.ceil(rad))
        for dx in range(-rr, rr + 1):
            for dz in range(-rr, rr + 1):
                if dx * dx + dz * dz <= rad * rad + 0.3 and (dx, dz) != (0, 0):
                    cells.append((x + dx, yy, z + dz))
    for c in cells + [(x, y0 + k, z) for k in range(1, h + 2)]:
        if w.id(*c) not in (0, B.SNOW_LAYER, B.TALLGRASS):
            return False
    for k in range(1, h):
        w.set(x, y0 + k, z, B.LOG, 1)
    for c in cells + [(x, y0 + h, z), (x, y0 + h + 1, z)]:
        w.set(*c, B.LEAVES, 1 | 4)
    for c in cells + [(x, y0 + h + 1, z)]:
        if w.id(c[0], c[1] + 1, c[2]) == 0 and r.random() < snow:
            w.set(c[0], c[1] + 1, c[2], B.SNOW_LAYER, 0)
    w.set(x, y0, z, B.DIRT, 2)
    return True


MAPLE = [[(B.WOOL, 14), (B.WOOL, 1)], [(B.WOOL, 1), (B.STAINED_CLAY, 1)], [(B.WOOL, 14), (B.WOOL, 14), (B.WOOL, 1)]]


def maple(w, x, z, crown, r, share=0.5):
    """Turn an oak's crown to a maple's: clumps of red and orange through the russet leaves, each clump a ball
    about two blocks across round a leaf drawn at random, so the colour comes in handfuls and not as speckle."""
    pal = MAPLE[int(r.integers(len(MAPLE)))]
    rad = int(crown) + 2
    i0, i1 = max(0, x - rad - w.x0), min(w.sx, x + rad + 1 - w.x0)
    k0, k1 = max(0, z - rad - w.z0), min(w.sz, z + rad + 1 - w.z0)
    sub = w.ids[i0:i1, :, k0:k1]
    lv = sub == B.LEAVES
    around = np.zeros(lv.shape, int)
    for ax in range(3):
        for sh in (1, -1):
            around += np.roll(lv, sh, axis=ax)
    leaves = np.argwhere(lv & (around >= 4))
    if len(leaves) == 0:
        return 0
    n = max(3, int(len(leaves) * share / 9))
    for c in leaves[r.choice(len(leaves), size=min(n, len(leaves)), replace=False)]:
        blk = pal[int(r.integers(len(pal)))]
        for i, y, k in leaves:
            if (i - c[0]) ** 2 + (y - c[1]) ** 2 + (k - c[2]) ** 2 <= 2.2 + r.random():
                w.ids[i0 + i, y, k0 + k], w.dat[i0 + i, y, k0 + k] = blk
    return 1


def keep_clear():
    """Columns no tree may stand on or crown over: paths and a margin, the court, the buildings, the Rift's brink,
    the objectives' clearances, the field, the pit, the Hollow Way, the cave's mouth."""
    X, Z = P.X, P.Z
    m = np.zeros(X.shape, bool)
    for pts in P.PATHS.values():
        m |= shapes.polyline(X, Z, pts)[0] <= 3.5
    m |= shapes.polyline(X, Z, land.HOLLOW)[0] <= 4
    m |= shapes.polyline(X, Z, land.THAW)[0] <= 3
    for key, x0, z0, x1, z1, *_ in P.BUILDINGS:
        m |= (X >= x0 - 3) & (X <= x1 + 3) & (Z >= z0 - 3) & (Z <= z1 + 3)
    x0, z0, x1, z1 = land.COURT
    m |= (X >= x0 - 2) & (X <= x1 + 2) & (Z >= z0 - 2) & (Z <= z1 + 2)
    x0, z0, x1, z1 = land.FIELD
    m |= (X >= x0 - 2) & (X <= x1 + 4) & (Z >= z0 - 2) & (Z <= z1 + 2)
    b = P.MONUMENT_BOX
    m |= np.hypot(X - (b.x0 + b.x1) / 2, Z - (b.z0 + b.z1) / 2) <= 11
    m |= np.hypot(X - land.CORE[0], Z - land.CORE[1]) <= 11
    for kx, kz in P.KILNS:
        m |= np.hypot(X - kx, Z - kz) <= 4
    m |= Z > -18                                         # nothing on the brink a bridger leaves from
    m |= P.WET | P.G["tarn"].mask
    m |= shapes.polyline(X, Z, [(x, z) for x, z, _ in P.CAVE[:2]])[0] <= 4
    return m


def woods(w, wint, r, stats):
    X, Z = P.X, P.Z
    clear = keep_clear()
    ok_land = RED & P.LAND & ~clear & (P.G["ice"] < 1)
    # the Frostwood: on the Frost Knoll and the west knoll, spruce to the outside of the clearings
    frost = np.zeros(X.shape, bool)
    for (cx, cz), rad in (((-22, -30), 13), ((-58, -25), 10), ((-46, -84), 9), ((-62, -46), 6)):
        frost |= np.hypot(X - cx, Z - cz) <= rad
    frost &= ok_land & (wint > 1)
    n = 0
    planted = []
    cells = np.argwhere(frost)
    r.shuffle(cells)
    for i, k in cells[:2500]:
        x, z = int(X[i, k]), int(Z[i, k])
        if any((x - a) ** 2 + (z - b) ** 2 < 4.6 ** 2 for a, b in planted):
            continue
        h = int(r.integers(8, 15))
        if spruce(w, x, z, h, r):
            planted.append((x, z))
            n += 1
    stats["spruce"] = n
    # the Russet Wood: oaks under the autumn biome, some of them golden (savanna) for a second autumn colour
    lib = TR.library()
    kinds = TR.kinds(lib)
    russet = np.zeros(X.shape, bool)
    for (cx, cz), rad in (((46, -27), 17), ((18, -34), 8), ((60, -40), 7), ((60, -74), 8), ((-30, -88), 0)):
        russet |= np.hypot(X - cx, Z - cz) <= rad
    russet &= ok_land & (wint < -3)
    oaks = []
    stood = TR.scatter(w, russet, kinds, {"dense-oak": 0.45, "tiny-oak": 0.55}, r, spacing=1.15,
                       tries=1600, planted=oaks)
    stats["oaks"] = stood
    gold = 0
    for x, z, c in oaks:
        if r.random() < 0.5:
            rad = int(c) + 3
            for dx in range(-rad, rad + 1):
                for dz in range(-rad, rad + 1):
                    if dx * dx + dz * dz <= rad * rad and w.inside(x + dx, 0, z + dz) and z + dz < 0:
                        w.biome[x + dx - w.x0, z + dz - w.z0] = 35
                        yy = top(w, x + dx, z + dz)
                        if w.id(x + dx, yy, z + dz) == B.GRASS:
                            w.set(x + dx, yy, z + dz, B.DIRT, 2 if r.random() < 0.55 else 1)
            gold += 1
    stats["golden oaks"] = gold
    stats["maples"] = sum(maple(w, x, z, c, r) for x, z, c in oaks if r.random() < 0.55)
    # the forest floor under the oaks: podzol and coarse dirt where a crown shades the grass
    shade = np.isin(w.ids, (B.LEAVES, B.LEAVES2)).any(axis=1)
    for i, k in np.argwhere(shade & RED & ~clear):
        x, z = int(X[i, k]), int(Z[i, k])
        y = top(w, x, z)
        if w.id(x, y, z) == B.GRASS and r.random() < 0.55:
            w.set(x, y, z, B.DIRT, 2 if r.random() < 0.6 else 1)
    # frost-killed trees along the seam: bare spruce trunks
    for x, z in ((-8, -64), (-10, -38), (6, -56), (-12, -22)):
        y = top(w, x, z)
        if y > 0 and not clear[x - w.x0, z - w.z0]:
            TR.dead_tree(w, x, y, z, r, int(r.integers(5, 8)), log=B.LOG, kind=1)


# ---- the Rift: the falls of fire and ice, the Thaw's fall, the islets -----------------------------------------------
def rift(w, r, stats):
    X, Z = P.X, P.Z
    land_ = P.LAND
    # the brink: for each x, Rowan's last land row
    brink = {}
    for x in range(P.X_MIN, P.X_MAX + 1):
        col = [z for z in range(-24, 0) if land_[x - w.x0, z - w.z0]]
        if col:
            brink[x] = max(col)
    # the Ember Falls: lava out of vents in the cliff's top under the Russet Wood, down the face into the void
    lava = 0
    for x0, wide, length in ((42, 1, 24), (47, 2, 34), (53, 1, 18)):
        if x0 not in brink:
            continue
        z = brink[x0]
        y = top(w, x0, z)
        # a vent: netherrack and coal round a notch cut into the brink
        for dx in (-1, 0, 1):
            for dz in (-1, 0):
                yy = top(w, x0 + dx, z + dz)
                w.set(x0 + dx, yy, z + dz, *((B.NETHERRACK, 0) if (dx + dz) % 2 else (B.COAL_BLOCK, 0)))
        for xx in range(x0, x0 + wide):
            w.set(xx, y, z, B.LAVA, 0)
            w.set(xx, y - 1, z, B.NETHERRACK, 0)
            for yy in range(y, y - length, -1):
                if w.id(xx, yy, z + 1) == 0:
                    w.set(xx, yy, z + 1, B.LAVA_FLOW, 8)
                    lava += 1
        # the cliff face beside the fall scorched: netherrack, coal, obsidian
        for yy in range(y - 18, y):
            for dx in (-1, 1):
                if w.id(x0 + dx, yy, z) not in (0, B.LAVA_FLOW) and r.random() < 0.7:
                    w.set(x0 + dx, yy, z, *mix(r.random(), [(B.NETHERRACK, 0), (B.OBSIDIAN, 0), (B.COAL_BLOCK, 0)]))
    stats["lava falls"] = lava
    # the Rime Falls: frozen falls hanging down the west cliff, packed ice tapering into the void
    for x0 in (-58, -52, -45, -38, -26):
        if x0 not in brink:
            continue
        z = brink[x0]
        y = top(w, x0, z)
        length = int(r.integers(12, 20))
        m = forms.spike(w, [(x0 + 0.5, y + 0.5, z + 0.3), (x0 + 0.5, y - length * 0.5, z + 1.2),
                            (x0 + 0.5, y - length, z + 0.8)], (1.8, 0.3, 1.0), sides=0, rough=0.25, seed=abs(x0 + 99))
        w.ids[m & (w.ids == 0)] = B.PACKED_ICE
    # the Thaw's fall: off the headland into the void
    th = P.G["thaw"]
    lvl = np.where(th.mask & RED, th.surface, 0)
    stats["thaw fall"] = T.waterfall(w, lvl[:, :], (w.x0, w.z0), toward="south", to=4, to_y=8) if False else \
        _fall(w, lvl)
    # the islets
    for (cx, cz), rx, rz, top_, seed in land.ISLETS:
        islet(w, cx, cz, rx, rz, cx > 0, r)


def _fall(w, lvl):
    """The Thaw's water off the brink: the southernmost wet cell of each wet column falls one row south of it."""
    laid = 0
    for i in range(lvl.shape[0]):
        wet = np.nonzero(lvl[i] > 0)[0]
        if len(wet) == 0:
            continue
        k = wet.max()
        x, z, y = i + w.x0, k + w.z0, int(lvl[i, k])
        if z < -16:
            continue
        for zz in (z + 1,):
            for yy in range(8, y + 1):
                if w.id(x, yy, zz) == 0:
                    w.set(x, yy, zz, B.WATER_FLOW, 8)
                    laid += 1
    return laid


def islet(w, cx, cz, rx, rz, cinder, r):
    """The Berg and the Cinder, each its own image across the Rift and so drawn whole here: a floating rock whose
    underside narrows to a point. The Berg is packed ice in snow bands under a snow top, a serac leaning out of
    it; the Cinder is grey rock under a crust of netherrack and coal, a lava eye under iron bars at its crown and a
    spill of lava over its west lip."""
    X, Z = P.X, P.Z
    m = P.G["islets"] & (np.abs(X - cx) <= rx + 2) & (np.abs(Z - cz) <= rz + 2)
    rough = noise.fbm(X.shape, 3, 1, seed=int(abs(cx)))
    for i, k in np.argwhere(m):
        x, z = int(X[i, k]), int(Z[i, k])
        h = int(P.H[i, k])
        e = float(shapes.ellipse_distance(np.array(x + 0.5), np.array(z + 0.5), (cx + 0.5, cz + 0.5), rx, rz))
        depth = int(round(3 + 15 * max(0.0, 1 - e) ** 1.4 + 2 * rough[i, k]))
        w.ids[i, :h + 1, k] = 0
        for y in range(h - depth, h + 1):
            k_down = h - y
            if cinder:
                if k_down <= 1:
                    blk = mix(r.random(), [(B.NETHERRACK, 0), (B.COAL_BLOCK, 0), (B.NETHERRACK, 0), (B.STONE, 5)])
                else:
                    blk = mix(r.random(), [(B.STONE, 0), (B.STONE, 5), (B.STONE, 0), (B.COAL_ORE, 0)])
            else:
                blk = (B.SNOW, 0) if k_down == 0 or (y + int(rough[i, k] * 2)) % 6 == 0 else (B.PACKED_ICE, 0)
            w.set(x, y, z, *blk)
        for y in range(h + 1, h + 5):
            w.set(x, y, z, B.AIR)
    if cinder:
        ex, ez = int(cx), int(math.floor(cz))
        y = top(w, ex, ez)
        for dx in (0, 1):
            for dz in (0, 1):
                w.set(ex + dx, y, ez + dz, B.LAVA, 0)
                w.set(ex + dx, y - 1, ez + dz, B.NETHERRACK, 0)
                w.set(ex + dx, y + 1, ez + dz, B.IRON_BARS, 0)
        for dx in (-1, 2):
            for dz in (-1, 2):
                w.set(ex + dx, y + 1, ez + dz, B.NETHER_FENCE, 0)
        # the spill: a channel of lava from the eye to the west lip, then falling
        lip = ex - 1
        while P.G["islets"][lip - w.x0, ez - w.z0]:
            lip -= 1
        for x in range(lip + 1, ex - 1):
            yy = top(w, x, ez)
            w.set(x, yy, ez, B.LAVA_FLOW, 2)
            w.set(x, yy - 1, ez, B.NETHERRACK, 0)
        for yy in range(top(w, lip + 1, ez), top(w, lip + 1, ez) - 22, -1):
            if w.id(lip, yy, ez) == 0:
                w.set(lip, yy, ez, B.LAVA_FLOW, 8)
    else:
        y = top(w, int(cx) - 2, int(cz))
        mk = forms.spike(w, [(cx - 1.5, y - 1, cz + 0.5), (cx - 3.0, y + 8, cz + 1.0)], (2.0, 0.3, 1.2), sides=5,
                         rough=0.2, seed=5)
        w.ids[mk & (w.ids == 0)] = B.PACKED_ICE


# ---- the underside: icicles under the snow ----------------------------------------------------------------------------
def underside(w, wint, r):
    X, Z = P.X, P.Z
    under_snow = RED & P.LAND & (wint > 2) & (Z < -20)
    cells = np.argwhere(under_snow)
    r.shuffle(cells)
    taken = []
    for i, k in cells[:600]:
        x, z = int(X[i, k]), int(Z[i, k])
        if any((x - a) ** 2 + (z - b) ** 2 < 49 for a, b in taken):
            continue
        col = w.ids[i, :, k]
        ys = np.nonzero(col)[0]
        if len(ys) == 0:
            continue
        bottom = int(ys.min())
        if bottom < 12:
            continue
        L = int(r.integers(4, 10))
        m = forms.spike(w, [(x + 0.5, bottom + 0.5, z + 0.5), (x + 0.5, bottom - L, z + 0.5)], (1.4, 0.3, 1.2), rough=0.2,
                        seed=abs(x * 31 + z))
        w.ids[m & (w.ids == 0)] = B.PACKED_ICE
        taken.append((x, z))


BOULDERS = [(-44, -30, 2.2), (-26, -60, 1.8), (-60, -52, 2.4), (-30, -20, 1.6), (-14, -76, 1.8), (-52, -70, 2.0)]


def cover(w, wint, r, stats):
    """What grows and lies on the ground: on the autumn grass a few tufts, ferns, dead bushes and late flowers;
    under a maple's crown its fallen leaves; on the snow, boulders of one rock with snow on their crowns."""
    X, Z = P.X, P.Z
    clear = keep_clear()
    n = 0
    for i, k in np.argwhere(RED & P.LAND & (wint < -1) & ~clear):
        x, z = int(X[i, k]), int(Z[i, k])
        y = top(w, x, z)
        if w.id(x, y, z) != B.GRASS or w.id(x, y + 1, z) != 0:
            continue
        v = r.random()
        blk = (B.TALLGRASS, 1) if v < 0.05 else (B.TALLGRASS, 2) if v < 0.075 else (B.DEADBUSH, 0) if v < 0.085 \
            else (B.FLOWER, 5) if v < 0.09 else (B.FLOWER, 0) if v < 0.093 else None
        if blk:
            w.set(x, y + 1, z, *blk)
            n += 1
    stats["ground cover"] = n
    litter = 0
    shade = np.isin(w.ids, (B.WOOL, B.STAINED_CLAY)).any(axis=1)
    from scipy import ndimage
    shade = ndimage.binary_dilation(shade, np.ones((5, 5), bool))
    for i, k in np.argwhere(shade & RED & P.LAND & ~clear & (wint < -2)):
        x, z = int(X[i, k]), int(Z[i, k])
        y = top(w, x, z)
        if w.id(x, y + 1, z) in (0, B.TALLGRASS) and w.id(x, y, z) in (B.GRASS, B.DIRT) and r.random() < 0.3:
            w.set(x, y + 1, z, B.CARPET, mix(r.random(), [1, 12, 14, 1]))
            litter += 1
    stats["leaf litter"] = litter
    for bx, bz, rad in BOULDERS:
        y0 = top(w, bx, bz)
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                for dy in range(-1, 4):
                    d = math.sqrt(dx * dx + (dy * 1.3) ** 2 + dz * dz)
                    if d <= rad + 0.3 * r.random():
                        w.set(bx + dx, y0 + dy, bz + dz, *mix(r.random(), [(B.STONE, 0), (B.STONE, 5), (B.STONE, 0), (B.COBBLE, 0)]))
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                yy = top(w, bx + dx, bz + dz)
                if w.id(bx + dx, yy, bz + dz) in (B.STONE, B.COBBLE) and w.id(bx + dx, yy + 1, bz + dz) == 0:
                    w.set(bx + dx, yy + 1, bz + dz, B.SNOW_LAYER, int(r.integers(0, 2)))


def hold_water(w):
    """Water with air beside it that is not a fall: the air filled with andesite, so nothing pours on load."""
    from pgmvox.read import audit
    n = 0
    for x, y, z, _ in audit.loose_water(w):
        if z >= 0:
            continue
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if w.id(x + dx, y, z + dz) == 0:
                w.set(x + dx, y, z + dz, B.STONE, 5)
                n += 1
    return n


def beacon(w, r):
    """The fire on Kiln Hill's snowy crown: a stone plinth, lava under iron bars in a ring of nether-brick posts,
    where the charcoal burners signal across the Rift."""
    cx, cz = land.KILN_HILL
    y = max(top(w, cx + dx, cz + dz) for dx in (-2, -1, 0, 1, 2) for dz in (-2, -1, 0, 1, 2))
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            g = top(w, cx + dx, cz + dz)
            for yy in range(g + 1, y + 1):
                w.set(cx + dx, yy, cz + dz, *mix(r.random(), [(B.STONEBRICK, 0), (B.STONE, 0), (B.STONE, 5)]))
            for yy in range(y + 1, y + 4):
                w.set(cx + dx, yy, cz + dz, B.AIR)
            edge = max(abs(dx), abs(dz)) == 2
            if edge and (dx + dz) % 2 == 0:
                w.set(cx + dx, y + 1, cz + dz, B.NETHER_FENCE, 0)
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(cx + dx, y, cz + dz, B.NETHERRACK, 0)
            if abs(dx) + abs(dz) <= 1:
                w.set(cx + dx, y, cz + dz, B.LAVA, 0)
                w.set(cx + dx, y - 1, cz + dz, B.NETHERRACK, 0)
            w.set(cx + dx, y + 1, cz + dz, B.IRON_BARS, 0)


def settle(w):
    """Gravel with air under it would fall when the world loads: andesite there instead."""
    g = (w.ids[:, 1:, :] == B.GRAVEL) & (w.ids[:, :-1, :] == 0)
    sub = w.ids[:, 1:, :]
    sub[g] = B.STONE
    w.dat[:, 1:, :][g] = 5
    return int(g.sum())


def everything(w, R, deg, wint, O, stats):
    r = rng(P.BOARD, "dress")
    glacier(w, rng(P.BOARD, "glacier"))
    ice_cave(w, rng(P.BOARD, "cave"))
    paths(w, wint, rng(P.BOARD, "paths"))
    court(w, rng(P.BOARD, "court"))
    thaw_crossings(w, rng(P.BOARD, "bridge"))
    ember_pit(w, rng(P.BOARD, "pit"))
    rime_shelf(w, rng(P.BOARD, "shelf"))
    field(w, rng(P.BOARD, "field"))
    buildings.everything(w, rng(P.BOARD, "buildings"), stats)
    rift(w, rng(P.BOARD, "rift"), stats)
    underside(w, wint, rng(P.BOARD, "underside"))
    woods(w, wint, r, stats)
    beacon(w, rng(P.BOARD, "beacon"))
    cover(w, wint, rng(P.BOARD, "cover"), stats)
    stats["gravel settled"] = settle(w)
    stats["water held"] = hold_water(w)
