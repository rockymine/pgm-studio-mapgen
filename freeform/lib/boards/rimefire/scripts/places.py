"""The fire half's places, built once in the north half; echo.py turns each onto the ice half in its materials.

    Ashfall Lodge    the spawn: a hall against the back ridge and two wings round a yard
    The Furnace      the core: a ring of nether brick on the tor with the core hung in a pit
    Rustwater        the hamlet in the hollow, round a pond
    The Overlook     a watchtower on the hill between the lanes
"""
import numpy as np

from pgmvox import B, rng
from pgmvox.built import build as BLD
from pgmvox.built import facade as F
from pgmvox.core.orient import ladder as ladder_data, door as door_data
from pgmvox.scenery import forms

import bld
import land as LND

LEVEL = LND.LEVEL

FIRE_STYLE = dict(ground=[(B.STONEBRICK, 0), (B.STONEBRICK, 0), (B.COBBLE, 0)], upper=[(B.RED_SANDSTONE, 0)], post=1,
                  gable=(B.PLANKS, 1), floor=(B.PLANKS, 5), roof=(B.PLANKS, 4), stair=B.ACACIA_STAIRS,
                  slab=(B.WOOD_SLAB, 4), door=B.DARK_OAK_DOOR, window=(B.PANE, 0), chimney=(B.STONEBRICK, 0))

SPAWN_Y = LEVEL + 1                      # the plateau's top block


# ---- Ashfall Lodge -----------------------------------------------------------------------------------------
LODGE = dict(hall=(-14, -83, 17, 8), west=(-25, -75, 11, 6), east=(-3, -75, 11, 6), box=(-29, -90, 1, -66))


def lodge(w, g, claims):
    x0, z0, x1, z1 = LODGE["box"]
    sx, sz = LND.SPAWN
    r = rng("rimefire", "lodge")
    y = SPAWN_Y

    def yard(x, z):
        u, v = x - sx, z - sz
        if abs(u) <= 1 and abs(v - 1) <= 1:
            return (B.NETHER_BRICK, 0) if (abs(u), abs(v - 1)) != (0, 0) else (B.GLOWSTONE, 0)
        edge = x in (x0, x1) or z == z1
        if edge:
            return (B.STONEBRICK, 3)
        if (u + v) % 7 == 0:
            return (B.STONE, 1)
        if abs(u) <= 2 and z > sz - 9:                      # a runner from the hall to the gate
            return (B.GRAVEL, 0) if (x + z) % 3 else (B.STONE, 2)
        return [(B.COBBLE, 0), (B.STONEBRICK, 0), (B.STONE, 1), (B.GRAVEL, 0)][int(r.integers(4))]

    bld.level(w, g, x0, z0, x1, z1, y, top=yard)
    for key, door in (("hall", 1), ("west", -1), ("east", 1)):
        cx, cz, L, W = LODGE[key]
        heading = 0 if key == "hall" else 90
        BLD.house(w, BLD.House(cx, cz, heading, L=L, W=W, floor=y, storeys=2 if key == "hall" else 1, style=FIRE_STYLE,
                               door=door, chimney=key != "east", overhang=1, pitch=1,
                               roof="gambrel" if key == "hall" else "gable"))
    # a porch on the hall's door: two posts and a canopy of stairs
    px = sx
    for dx in (-3, 3):
        for k in range(1, 4):
            w.set(px + dx, y + k, -78, B.LOG2, 1)
    for dx in range(-4, 5):
        bld.stair(w, px + dx, y + 4, -79, B.ACACIA_STAIRS, "n")
        bld.stair(w, px + dx, y + 4, -77, B.ACACIA_STAIRS, "s")
        w.set(px + dx, y + 5, -78, B.WOOD_SLAB, 4)
    for dx in range(-3, 4):
        w.set(px + dx, y + 4, -78, B.WOOD_SLAB, 4 | 8)
    # lamp posts and banners at the yard's mouth
    for x in (x0 + 2, sx - 6, sx + 5, x1 - 2):
        bld.post(w, x, y, z1 - 1, 3)
    for x, base in ((sx - 3, 1), (sx + 3, 1)):
        w.set(x, y + 1, z1 - 1, B.DARK_OAK_FENCE)
        w.set(x, y + 2, z1 - 1, B.DARK_OAK_FENCE)
        w.set(x, y + 3, z1 - 1, B.DARK_OAK_FENCE)
        w.banner(x, y + 4, z1 - 1, base, [("bs", 14), ("ts", 15)], rot=0)
    # a woodpile behind the east wing: stacked logs lying along z, and two hay bales
    for k in range(3):
        for j in range(5):
            w.set(x1 - 4 + (j % 2) * 2, y + 1 + k, z0 + 2 + j, B.LOG2, 1 | 8)
    w.set(x1 - 1, y + 1, -81, B.HAY, 0)
    w.set(x1 - 1, y + 1, -82, B.HAY, 0)
    for bx in (sx - 8, sx + 8):
        brazier(w, bx, y, sz + 3)
    claims.append(("lodge", x0, z0, x1, z1))
    return dict(spawn=(sx, y + 1, sz + 3), area=(x0, y, z0, x1, y + 8, z1))


# ---- The Furnace -------------------------------------------------------------------------------------------
FURNACE_CORE = LND.FURNACE
TOR_Y = LEVEL + LND.TOR                 # 72: the plateau's top block
PIT_Y = TOR_Y - 7                       # the pit's floor: the core's lava has five blocks to fall
CORE_BOX = LND.CORE_BOX                 # 5 by 5 by 5, hung five blocks over the pit floor


def _wall_block(t, x, z, r):
    """The ring wall's block at course t (1 at the foot): two courses of stone brick, nether brick above them worn
    with stone brick, a course of red sandstone under the parapet."""
    if t <= 2:
        return (B.STONEBRICK, 0 if (x + z + t) % 4 else 3)
    if t == 5:
        return (B.RED_SANDSTONE, 2)
    return (B.STONEBRICK, 2) if (x * 7 + z * 3 + t * 5) % 11 == 0 else (B.NETHER_BRICK, 0)


def furnace(w, g, claims):
    """A ring of nether brick on the tor with a gate to the west, one north and one south and the east side solid over
    the drop; round each gate two towers, and buttresses between. Inside, a ledge, a pit five blocks deep with a stair down
    on each side, and the core hung over its floor. A stack stands over the eastern drop."""
    cx, cz = FURNACE_CORE
    r = rng("rimefire", "furnace")
    y = TOR_Y

    def polar(x, z):
        return np.hypot(x - cx, z - cz), np.degrees(np.arctan2(z - cz, x - cx))

    def in_gate(x, z):
        return ((abs(z - cz) <= 2 and x < cx) or (abs(x - cx) <= 1 and z < cz) or (abs(x - cx) <= 1 and z > cz))

    for x in range(cx - 14, cx + 15):
        for z in range(cz - 14, cz + 15):
            if g["H"][x - LND.X0, z - LND.Z0] <= 0:
                continue
            d, a = polar(x, z)
            gh = bld.ground_y(g, x, z)
            if d <= 12.4:                                         # the plateau: solid up to y, clear above
                for yy in range(max(1, min(gh, y) - 8), y):
                    if w.id(x, yy, z) in (B.AIR, B.SNOW_LAYER, B.TALLGRASS):
                        w.set(x, yy, z, B.STONEBRICK if (x + z) % 3 else B.COBBLE, 0)
                for yy in range(y + 1, y + 24):
                    if w.id(x, yy, z) != B.AIR:
                        w.set(x, yy, z, B.AIR)
                if d > 11.0:                                        # the outer terrace
                    w.set(x, y, z, B.STONEBRICK, 0 if (x + z) % 2 else 2)
            if 9.0 <= d < 11.0:
                gate = in_gate(x, z)
                for yy in range(max(1, min(gh, y) - 10), y):
                    if w.id(x, yy, z) in (B.AIR, B.SNOW_LAYER, B.TALLGRASS):
                        w.set(x, yy, z, B.STONEBRICK, 3 if (x + yy + z) % 5 == 0 else 0)
                if gate:
                    w.set(x, y, z, B.STONEBRICK, 3)
                    for yy in range(y + 1, y + 5):
                        w.set(x, yy, z, B.AIR)
                    w.set(x, y + 5, z, B.NETHER_BRICK, 0)
                    continue
                for t in range(1, 6):
                    w.set(x, y + t, z, *_wall_block(t, x, z, r))
                if int(a // 11.25) % 2 == 0:
                    w.set(x, y + 6, z, B.NETHER_BRICK, 0)
                    if d >= 10.0:
                        w.set(x, y + 7, z, B.NETHER_FENCE, 0)
            elif d < 9.0:
                if d >= 7.6:                                         # the ledge round the pit
                    w.set(x, y, z, *((B.NETHER_BRICK, 0) if d < 8.2 else
                                     [(B.RED_SANDSTONE, 2), (B.STONEBRICK, 0), (B.RED_SANDSTONE, 0)][int(r.integers(3))]))
                else:                                                # the pit
                    for yy in range(PIT_Y + 1, y + 1):
                        w.set(x, yy, z, B.AIR)
                    for yy in range(PIT_Y - 2, PIT_Y):
                        w.set(x, yy, z, B.NETHER_BRICK, 0)
                    w.set(x, PIT_Y, z, *((B.NETHER_BRICK, 0) if (x + z) % 3 else (B.OBSIDIAN, 0)))
                    if d > 6.6:                                      # the pit's lining
                        for yy in range(PIT_Y + 1, y):
                            lamp = yy == PIT_Y + 3 and abs(((a % 45) - 22.5)) < 3
                            w.set(x, yy, z, *((B.GLOWSTONE, 0) if lamp else (B.NETHER_BRICK, 0) if (yy + x + z) % 3 else (B.STONEBRICK, 2)))
    # four lava basins in the pit floor's corners, rimmed in obsidian
    for ang in (45, 135, -45, -135):
        bx = int(round(cx + 4.6 * np.cos(np.radians(ang))))
        bz = int(round(cz + 4.6 * np.sin(np.radians(ang))))
        for dx in (0, 1):
            for dz in (0, 1):
                w.set(bx + dx, PIT_Y, bz + dz, B.LAVA, 0)
                w.set(bx + dx, PIT_Y - 1, bz + dz, B.OBSIDIAN, 0)
    # buttresses on the wall's outer face between the gates, with a stepped top
    for ang in (45, 135, -45, -135, 90, -90, 20, -20, 160, -160):
        bx = int(round(cx + 11.4 * np.cos(np.radians(ang))))
        bz = int(round(cz + 11.4 * np.sin(np.radians(ang))))
        if in_gate(bx, bz) or g["H"][bx - LND.X0, bz - LND.Z0] <= 0:
            continue
        for dx in (0, 1):
            for dz in (0, 1):
                gh = bld.ground_y(g, bx + dx, bz + dz)
                for yy in range(max(1, gh - 6), y + 4):
                    if w.id(bx + dx, yy, bz + dz) in (B.AIR, B.SNOW_LAYER, B.TALLGRASS) or yy > y:
                        w.set(bx + dx, yy, bz + dz, B.NETHER_BRICK if yy > y else B.STONEBRICK, 0)
        w.set(bx, y + 4, bz, B.NETHER_STAIRS, 0)
    # two towers at the west gate, with a glowstone cap each
    for tz in (-5, 5):
        tx = cx - 11
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                for yy in range(y - 3, y + 10):
                    edge = abs(dx) == 1 or abs(dz) == 1
                    w.set(tx + dx, yy, cz + tz + dz, *(_wall_block(yy - y, tx + dx, cz + tz + dz, r) if edge and yy > y else (B.NETHER_BRICK, 0) if yy > y else (B.STONEBRICK, 0)))
                    if yy == y + 9 and edge:
                        w.set(tx + dx, yy, cz + tz + dz, B.NETHER_BRICK, 0)
        w.set(tx, y + 10, cz + tz, B.GLOWSTONE, 0)
        for dx, dz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            w.set(tx + dx, y + 10, cz + tz + dz, B.NETHER_FENCE, 0)
    # four stairs down, three wide, each from the ledge toward the core
    for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        for step in range(7):
            d = 7 - step
            for lateral in (-1, 0, 1):
                x = cx + dx * d + (lateral if dz else 0)
                z = cz + dz * d + (lateral if dx else 0)
                yy = y - 1 - step
                for up in range(yy + 1, y + 1):
                    w.set(x, up, z, B.AIR)
                w.set(x, yy, z, B.NETHER_BRICK, 0)
                bld.stair(w, x, yy, z, B.NETHER_STAIRS, (dx, dz))
    # the stack: a tapering chimney of nether brick over the eastern drop, a glowstone at its head
    sx_, sz_ = cx + 13, cz
    for yy in range(y - 6, y + 22):
        half_ = 2 if yy < y + 8 else 1
        for dx in range(-half_, half_ + 1):
            for dz in range(-half_, half_ + 1):
                if g["H"][sx_ + dx - LND.X0, sz_ + dz - LND.Z0] <= 0 and yy < y:
                    continue
                w.set(sx_ + dx, yy, sz_ + dz, *((B.NETHER_BRICK, 0) if (yy + dx + dz) % 4 else (B.STONEBRICK, 2)))
    w.set(sx_, y + 22, sz_, B.GLOWSTONE, 0)
    for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        w.set(sx_ + dx, y + 22, sz_ + dz, B.NETHER_FENCE, 0)
    # the ground round it scorched: ash, coal and netherrack thinning out to the grass
    for x in range(cx - 20, cx + 21):
        for z in range(cz - 20, cz + 21):
            d, _ = polar(x, z)
            if d < 12.4 or d > 19 or g["H"][x - LND.X0, z - LND.Z0] <= 0:
                continue
            if r.random() > (19 - d) / 8.0 - 0.1:
                continue
            gy = bld.ground_y(g, x, z)
            if w.id(x, gy, z) in (B.GRASS, B.DIRT, B.GRAVEL, B.STONE) and w.id(x, gy + 1, z) in (B.AIR, B.TALLGRASS, B.DEADBUSH, B.SNOW_LAYER):
                w.set(x, gy, z, *[(B.COAL_BLOCK, 0), (B.NETHERRACK, 0), (B.DIRT, 1), (B.GRAVEL, 0), (B.DIRT, 1)][int(r.integers(5))])
    claims.append(("furnace", cx - 14, cz - 14, cx + 16, cz + 14))
    return dict(core=CORE_BOX)


# ---- Rustwater ---------------------------------------------------------------------------------------------
POND = dict(at=(-44, -40), rx=5.5, rz=3.2, water=54)
GREEN = (-38, -44)
HOUSES = [  # centre x, z, heading, L, W, storeys, door, roof
    (-31, -52, 0, 11, 7, 2, 1, "gable"),
    (-50, -47, 90, 8, 6, 1, -1, "gable"),
    (-30, -40, 90, 9, 6, 2, 1, "hip"),
    (-47, -54, 0, 9, 6, 1, 1, "gable"),
]


def hamlet(w, g, claims):
    r = rng("rimefire", "hamlet")
    px, pz = POND["at"]
    wl = POND["water"]
    for x in range(px - 8, px + 9):
        for z in range(pz - 6, pz + 7):
            d = np.hypot((x - px) / POND["rx"], (z - pz) / POND["rz"])
            if d > 1.0 or g["H"][x - LND.X0, z - LND.Z0] <= 0:
                continue
            for yy in range(wl - 2, wl + 8):
                w.set(x, yy, z, B.AIR)
            w.set(x, wl - 3, z, B.GRAVEL if d > 0.6 else B.CLAY, 0)
            for yy in range(wl - 2, wl):
                w.set(x, yy, z, B.WATER, 0)
            w.set(x, wl, z, B.WATER, 0)
    # a bank of stones round it where the ground stands above the water
    for x in range(px - 9, px + 10):
        for z in range(pz - 7, pz + 8):
            d = np.hypot((x - px) / POND["rx"], (z - pz) / POND["rz"])
            if 1.0 < d < 1.35 and w.id(x, wl + 1, z) == B.AIR and w.id(x, wl, z) in (B.GRASS, B.DIRT, B.GRAVEL, B.STONE):
                w.set(x, wl, z, *[(B.GRAVEL, 0), (B.COBBLE, 0), (B.STONE, 5)][int(r.integers(3))])
    for cx, cz, heading, L, W, st, door, roof in HOUSES:
        fr = BLD.Frame(cx, cz, heading)
        cells = fr.cells(L, W)
        floor = max(bld.ground_y(g, x, z) for x, z in cells)
        BLD.house(w, BLD.House(cx, cz, heading, L=L, W=W, floor=floor, storeys=st, style=FIRE_STYLE, door=door, roof=roof,
                               chimney=True, overhang=1, pitch=1), ground_at=lambda x, z: bld.ground_y(g, x, z))
        claims.append(("house", cx - L // 2 - 3, cz - L // 2 - 3, cx + L // 2 + 3, cz + L // 2 + 3))
    # the green: a well with a roof of its own
    gx, gz = GREEN
    gy = bld.ground_y(g, gx, gz)
    for x in range(gx - 4, gx + 5):
        for z in range(gz - 3, gz + 4):
            d = np.hypot(x - gx, (z - gz) * 1.2)
            if d < 4.2:
                for yy in range(gy + 1, gy + 8):
                    if w.id(x, yy, z) != B.AIR:
                        w.set(x, yy, z, B.AIR)
                w.set(x, gy, z, *[(B.GRAVEL, 0), (B.STONE, 1), (B.COBBLE, 0), (B.GRAVEL, 0)][int(r.integers(4))])
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            if (dx, dz) == (0, 0):
                for yy in range(gy - 3, gy + 1):
                    w.set(gx, yy, gz, B.WATER, 0) if yy < gy else w.set(gx, yy, gz, B.WATER, 0)
            else:
                w.set(gx + dx, gy + 1, gz + dz, B.COBBLE, 0)
    for dx, dz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        for k in range(2, 4):
            w.set(gx + dx, gy + k, gz + dz, B.DARK_OAK_FENCE)
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(gx + dx, gy + 4, gz + dz, B.WOOD_SLAB, 4)
    brazier(w, gx, gy, gz - 4)
    # two stalls on the green, awnings in the half's colours
    from pgmvox.built import props
    props.stall(w, gx - 5, gy, gz + 1, "e", awning=1, stripe=14, post=(B.DARK_OAK_FENCE, 0), goods=(B.PUMPKIN, 3))
    props.stall(w, gx + 5, gy, gz + 2, "w", awning=14, stripe=1, post=(B.DARK_OAK_FENCE, 0), goods=(B.HAY, 0))
    claims.append(("green", gx - 8, gz - 6, gx + 8, gz + 6))
    # lamps along the green's edge
    for lx, lz in ((gx - 3, gz - 5), (gx + 3, gz - 5), (gx - 8, gz), (gx + 8, gz)):
        gyl = bld.ground_y(g, lx, lz)
        bld.post(w, lx, gyl, lz, 3)


# ---- The Overlook ------------------------------------------------------------------------------------------
TOWER = (-10, -40, -6, -36)          # x0, z0, x1, z1 of a five by five tower on the hill


def watchtower(w, g, claims):
    x0, z0, x1, z1 = TOWER
    y = max(bld.ground_y(g, x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1))
    # a terrace for it: the hill's top levelled and bordered
    bld.level(w, g, x0 - 3, z0 - 3, x1 + 3, z1 + 3, y, top=lambda x, z: (B.STONEBRICK, 0) if (x + z) % 3 else (B.COBBLE, 0))
    forms.masonry_tower(w, x0, z0, x1, z1, y, 15,
                        wall=((B.NETHER_BRICK, 0), (B.STONEBRICK, 0), (B.STONEBRICK, 2), (B.NETHER_BRICK, 0)),
                        corner=(B.RED_SANDSTONE, 2), floor=(B.PLANKS, 5), door_side="s", ladder_on="n",
                        crown=(B.NETHER_BRICK, 0), crenel=(B.NETHER_FENCE, 0), light=(B.GLOWSTONE, 0),
                        rng=rng("rimefire", "tower"))
    w.chest(x0 + 1, y + 1, z1 - 1, SUPPLY, facing=3)
    claims.append(("tower", x0 - 4, z0 - 4, x1 + 4, z1 + 4))


# ---- the seam's falls and the rim's hoodoos ----------------------------------------------------------------
def lava_falls(w, g, xs=(-14, 17, -52)):
    """A vein of lava down the north wall of the seam at each x: a recess one block into the rock, lava in it from near the rim
    to the stream, and a pane of orange glass across its face, so the lava is held and shows through."""
    n = 0
    for x in xs:
        c = float(LND.centre(x))
        for y in range(LEVEL - 3, LND.FLOOR - 1, -1):
            face = None
            for z in range(int(c) - 1, int(c) - 18, -1):          # from the stream outward: the first solid block
                if w.id(x, y, z) not in (B.AIR, B.LAVA, B.LAVA_FLOW, B.STAINED_GLASS):
                    face = z + 1
                    break
            if face is None or face >= c - 1:
                continue
            w.set(x, y, face - 1, B.LAVA, 0)
            w.set(x, y, face, B.STAINED_GLASS, 1)
            n += 1
    return n


def hoodoos(w, g, rim_sites, rng_name="hoodoos"):
    """Clusters of stone needles from banded clay: hoodoos on the fire half, the ice half's crystals once turned."""
    from pgmvox.scenery.forms import spike
    r = rng("rimefire", rng_name)
    n = 0
    for sx_, sz_, count, hmin, hmax in rim_sites:
        for k in range(count):
            x = sx_ + r.normal(0, 3.2)
            z = sz_ + r.normal(0, 3.2)
            ix, iz = int(round(x)) - LND.X0, int(round(z)) - LND.Z0
            if g["H"][ix, iz] <= 0:
                continue
            base = int(g["H"][ix, iz]) - 2
            h = r.uniform(hmin, hmax)
            lean = r.normal(0, 0.12, 2) * h
            vol = spike(w, [(x, base, z), (x + lean[0], base + h, z + lean[1])], (r.uniform(2.0, 3.6), 0, r.uniform(0.9, 1.5)),
                        flutes=(5, 0.2), sides=int(r.choice([0, 0, 6])), rough=0.18, cell=5, seed=int(r.integers(1, 9999)))
            idx = np.argwhere(vol & (w.ids == 0))
            for i, j, kk in idx:
                tone = [(B.HARDENED_CLAY, 0), (B.STAINED_CLAY, 12), (B.STAINED_CLAY, 1), (B.HARDENED_CLAY, 0)][(j // 3 + k) % 4]
                w.ids[i, j, kk], w.dat[i, j, kk] = tone
            n += int(vol.sum())
    return n


# ---- braziers and the waystation ---------------------------------------------------------------------------
def brazier(w, x, y, z):
    """A bowl on a post: cobble wall, netherrack, a fire at head height. Turned onto the ice half it is an ice bowl
    with a sea lantern."""
    w.set(x, y + 1, z, B.COBBLE_WALL, 0)
    w.set(x, y + 2, z, B.COBBLE_WALL, 0)
    w.set(x, y + 3, z, B.NETHERRACK, 0)
    w.set(x, y + 4, z, B.FIRE, 0)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        w.set(x + dx, y + 3, z + dz, B.COBBLE_WALL, 0)


SUPPLY = [(0, 'minecraft:golden_apple', 2, 0), (1, 'minecraft:arrow', 16, 0), (2, 'minecraft:cooked_beef', 8, 0)]
WAYSTATION = (-26, -38)            # on the pass between the hollow and the overlook


def waystation(w, g, claims):
    """An open shelter where the lanes cross: four posts and a roof of acacia stairs over a long table of slabs, a bench
    each side, a brazier at each end and a stack of logs behind."""
    cx, cz = WAYSTATION
    y = max(bld.ground_y(g, x, z) for x in range(cx - 4, cx + 5) for z in range(cz - 3, cz + 4))
    bld.level(w, g, cx - 5, cz - 4, cx + 5, cz + 4, y, top=lambda x, z: (B.STONEBRICK, 0) if (x + z) % 2 else (B.COBBLE, 0))
    for dx in (-3, 3):
        for dz in (-2, 2):
            for k in range(1, 4):
                w.set(cx + dx, y + k, cz + dz, B.LOG2, 1)
    for dx in range(-4, 5):
        bld.stair(w, cx + dx, y + 4, cz - 3, B.ACACIA_STAIRS, "s")
        bld.stair(w, cx + dx, y + 4, cz + 3, B.ACACIA_STAIRS, "n")
        for dz in (-2, -1, 0, 1, 2):
            w.set(cx + dx, y + 4, cz + dz, B.WOOD_SLAB, 4)
    for dx in range(-3, 4):
        w.set(cx + dx, y + 1, cz, B.WOOD_SLAB, 5 | 8)
    for dx in range(-2, 3):
        bld.stair(w, cx + dx, y + 1, cz - 2, B.SPRUCE_STAIRS, "s")
        bld.stair(w, cx + dx, y + 1, cz + 2, B.SPRUCE_STAIRS, "n")
    brazier(w, cx - 5, y, cz)
    brazier(w, cx + 5, y, cz)
    w.chest(cx - 4, y + 1, cz - 1, SUPPLY, facing=3)
    for j in range(4):
        base = bld.ground_y(g, cx - 2 + j, cz - 5)
        for k in range(3):
            w.set(cx - 2 + j, base + 1 + k, cz - 5, B.LOG2, 1 | 4)
    claims.append(("waystation", cx - 6, cz - 5, cx + 6, cz + 5))


def road_lamps(w, g, every=14, side=2.4):
    """A lamp post beside each north road every so many blocks, the sides taken in turn."""
    from pgmvox.geom import shapes
    n = 0
    for name, _, pts in g["roads"]:
        if name.endswith("-s"):
            continue
        total = shapes.length(pts)
        s, k = 8.0, 0
        while s < total - 6:
            (x, z), (dx, dz) = shapes.point_at(pts, s)
            px, pz = -dz, dx
            sign = 1 if k % 2 == 0 else -1
            lx, lz = int(round(x + sign * side * px)), int(round(z + sign * side * pz))
            ix, iz = lx - LND.X0, lz - LND.Z0
            if (0 <= ix < g["H"].shape[0] and 0 <= iz < g["H"].shape[1] and g["H"][ix, iz] > 44 and not g["seam"][ix, iz]
                    and lz < -2):
                y = int(g["H"][ix, iz])
                if w.id(lx, y + 1, lz) == B.AIR:
                    bld.post(w, lx, y, lz, 2)
                    n += 1
            s += every
            k += 1
    return n
