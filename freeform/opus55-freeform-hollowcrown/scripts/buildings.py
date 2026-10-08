"""Everything built on and under red's mountain.

Crownhold: curtain walls laid along the crown's polygon, a tower at each corner, gates where the Wend and the
Knife arrive, a keep set at 25 degrees, the Deep Stair's head, the lift to the Lower Gate, the court where the
team spawns. The Eyrie: a round tower on the spur, a spiral stair to its open crown and monument A. Wendholm:
houses along the Wend at the road's own angle, some turned 45 degrees to it at the corners, parapets where
the road runs along a drop. Market Cross: the cross, the well, stalls. Wendfoot: a green at the
Wend's foot with three houses at 0, 12 and 45 degrees. The vale: Kingsbridge, the fords' stones, the mill and its wheel, fields set at angles with their
farmhouses. Underground: the Deep Stair, Underhall's delved houses along Undergate, the Hall of Echoes round
monument B, the Lower Gate and its lift, the Mine Road's timbering, the Delving's lining and the Weeping
Gallery.

Every builder claims the blocks it stands on; a claim on a block already claimed is a conflict.
"""
import math

import numpy as np

import geometry as G
import house
import plan as P
from mc import B
from terrain import route_y, route_field

RNG = np.random.default_rng(1066)
RECORDS = []


# ---------------------------------------------------------------------------------------------------------
# ground and claims

def H(F, x, z):
    return int(F.H[x - F.x0, z - F.z0])


def ok_cell(F, x, z):
    return P.X_MIN <= x <= P.X_MAX and P.Z_MIN <= z <= P.Z_MAX


def claim(F, name, cells, layer="surface"):
    """Claim blocks on a layer: the surface and the underground are claimed apart, so a temple under the
    town is not a house on top of it."""
    occ = F.occ[layer]
    hit = set()
    for c in cells:
        o = occ.get(c)
        if o is not None and o != name:
            hit.add(o)
    for o in hit:
        F.conflicts.append((name, o))
    for c in cells:
        occ.setdefault(c, name)
    return not hit


def free(F, cells, layer="surface"):
    return all(c not in F.occ[layer] for c in cells)


def level(w, F, cells, y, top=(B.GRASS, 0)):
    """Make the ground at these blocks exactly y: cut what is higher, fill what is lower with dirt."""
    for (x, z) in cells:
        if x >= 0 or not ok_cell(F, x, z):
            continue
        g = H(F, x, z)
        for yy in range(y + 1, max(g, y) + 4):
            if w.id(x, yy, z) not in (B.WATER,):
                w.set(x, yy, z, B.AIR)
        for yy in range(min(g, y), y):
            w.set(x, yy, z, B.DIRT)
        if top:
            w.set(x, y, z, *top)
        F.H[x - F.x0, z - F.z0] = y


def ground_fn(F):
    return lambda x, z: H(F, x, z)


# ---------------------------------------------------------------------------------------------------------
# houses anywhere

WHY = {}


def place_house(w, F, spec, name, margin_top=(B.GRASS, 0), max_fill=12, max_cut=9, check_only=False,
                allow=lambda x, z: True, layer="surface"):
    """Build a house if its footprint is free, on our half, and the ground under it is within reach.
    Underground, the ground is the cavern's floor rather than the surface."""
    fp = house.footprint(spec, margin=0)
    ring = house.footprint(spec, margin=1) - fp
    under = layer == "under"
    gnd = (lambda x, z: F.cave_floor.get((x, z), -99)) if under else (lambda x, z: H(F, x, z))

    def no(why):
        WHY[why] = WHY.get(why, 0) + 1
        return None
    if any(x >= -1 for x, z in fp | ring):
        return no("crosses the seam")
    if not free(F, fp | ring, layer):
        return no("ground already claimed")
    if not all(allow(x, z) for x, z in fp):
        return no("outside its zone")
    gs = [gnd(x, z) for x, z in fp]
    if max(gs) - spec["floor"] > max_cut:
        return no("too much to cut")
    if spec["floor"] - min(gs) > max_fill:
        return no("too much to fill")
    if check_only:
        return True
    if not under:
        # the ring round the plate is ground at the floor's height where it can be, never a stone rim
        level(w, F, [(x, z) for x, z in ring if abs(H(F, x, z) - spec["floor"]) <= 2], spec["floor"], margin_top)
    res = house.build(w, spec, ground_at=gnd, rng=RNG)
    if not under:
        for x, z in fp:
            F.H[x - F.x0, z - F.z0] = spec["floor"]
    claim(F, name, fp | ring, layer)
    plate = house.footprint(dict(spec, jetty=False))          # the jettied storey overhangs; the plate does not
    RECORDS.append(dict(kind=name, cells=plate, floor=spec["floor"], heading=spec["heading"], storeys=spec.get("storeys", 2)))
    F.houses.append(spec)
    return res


# ---------------------------------------------------------------------------------------------------------
# lines of masonry along a polygon

def thick_line_cells(a, b, half):
    (ax, az), (bx, bz) = a, b
    x0, x1 = int(min(ax, bx) - half - 1), int(max(ax, bx) + half + 1)
    z0, z1 = int(min(az, bz) - half - 1), int(max(az, bz) + half + 1)
    X, Z = np.meshgrid(np.arange(x0, x1 + 1), np.arange(z0, z1 + 1), indexing="ij")
    d, t = G.seg_distance(X, Z, a, b)
    xs, zs = np.nonzero(d <= half)
    return {(x0 + i, z0 + k) for i, k in zip(xs, zs)}


def inset(poly, k):
    cx, cz = G.centroid(poly)
    out = []
    for x, z in poly:
        dx, dz = x - cx, z - cz
        L = math.hypot(dx, dz)
        out.append((x - dx / L * k, z - dz / L * k))
    return out


def round_tower(w, F, cx, cz, base, top, r=3.5, name="tower", door=None, ladder=True, roof=True):
    cells = set()
    for x in range(int(cx - r) - 1, int(cx + r) + 2):
        for z in range(int(cz - r) - 1, int(cz + r) + 2):
            d = math.hypot(x - cx, z - cz)
            if d > r or x >= 0:
                continue
            cells.add((x, z))
            g = H(F, x, z)
            for y in range(min(g, base) - 6, top + 1):
                shell = d > r - 1.0
                if y <= base:
                    if y > g - 6:
                        w.set(x, y, z, B.STONEBRICK, 0 if RNG.random() < 0.8 else 2)
                elif shell:
                    w.set(x, y, z, *((B.STONEBRICK, 0) if (y - base) % 6 else (B.STONE, 6)))
                else:
                    w.set(x, y, z, B.AIR)
            if d <= r - 1.0:
                w.set(x, top, z, B.STONEBRICK, 0)
            if d > r - 1.0 and (x + z) % 2 == 0:
                w.set(x, top + 1, z, B.STONEBRICK, 0)
    if ladder:
        lx, lz = int(round(cx + r - 1.5)), int(round(cz))
        for y in range(base + 1, top + 1):
            w.set(lx, y, lz, B.LADDER, 4)
        w.set(lx, top, lz, B.LADDER, 4)
    if door:
        dx, dz = door
        for k in range(1, int(r) + 1):
            x, z = int(round(cx + dx * k)), int(round(cz + dz * k))
            for y in (base + 1, base + 2, base + 3):
                w.set(x, y, z, B.AIR)
    claim(F, name, cells)
    return cells


# ---------------------------------------------------------------------------------------------------------
# Crownhold

def crownhold(w, F):
    y = 98
    wall_poly = inset(P.CROWN, 2.5)
    gates = [(P.WEND[-1][0], P.WEND[-1][1]), (P.KNIFE[0][0], P.KNIFE[0][1])]
    wall_cells = set()
    for i in range(len(wall_poly)):
        wall_cells |= thick_line_cells(wall_poly[i], wall_poly[(i + 1) % len(wall_poly)], 1.0)
    gate_cells = set()
    for gx, gz in gates:
        # the gate is where the route crosses the wall line
        best = min(wall_cells, key=lambda c: math.hypot(c[0] - gx, c[1] - gz))
        for c in wall_cells:
            if math.hypot(c[0] - best[0], c[1] - best[1]) <= 1.6:
                gate_cells.add(c)
    for (x, z) in wall_cells:
        if x >= 0:
            continue
        g = H(F, x, z)
        for yy in range(g - 3, y + 8):
            if (x, z) in gate_cells and y + 1 <= yy <= y + 4:
                w.set(x, yy, z, B.AIR)
                continue
            w.set(x, yy, z, *((B.STONEBRICK, 1 if RNG.random() < 0.15 else (2 if RNG.random() < 0.1 else 0))
                              if yy != y + 4 else (B.STONE, 6)))
        if (x + z) % 2 == 0 and (x, z) not in gate_cells:
            w.set(x, y + 8, z, B.STONEBRICK, 0)
        if (x, z) in gate_cells:
            w.set(x, y + 5, z, B.IRON_BARS)
            w.set(x, y, z, B.STONEBRICK, 0)
    claim(F, "Crownhold", wall_cells)
    F.wall_cells = wall_cells
    for i, (vx, vz) in enumerate(wall_poly):
        round_tower(w, F, vx, vz, y, y + 11, r=3.6, name="Crownhold",
                    door=(np.sign(G.centroid(P.CROWN)[0] - vx) * 0.7, np.sign(G.centroid(P.CROWN)[1] - vz) * 0.7))
        w.set(int(round(vx)), y + 13, int(round(vz)), B.FENCE)
        w.set(int(round(vx)), y + 14, int(round(vz)), B.FENCE)
        w.set(int(round(vx)) + 1, y + 14, int(round(vz)), B.WOOL, 14)
        w.set(int(round(vx)) + 1, y + 13, int(round(vz)), B.WOOL, 14)
    # the court: paved between the walls
    court = G.inside(F.X, F.Z, inset(P.CROWN, 3.5))
    for ix, iz in zip(*np.nonzero(court & F.red)):
        x, z = F.x0 + ix, F.z0 + iz
        if (x, z) in F.occ["surface"]:
            continue
        q = RNG.random()
        w.set(x, y, z, *((B.STONEBRICK, 0) if q < 0.45 else (B.STONE, 5) if q < 0.75 else (B.GRAVEL, 0) if q < 0.85 else (B.STONE, 6)))
        for yy in range(y + 1, y + 4):
            if w.id(x, yy, z) not in (B.AIR,):
                w.set(x, yy, z, B.AIR)
    # the keep, at 25 degrees to the walls' grid
    place_house(w, F, dict(cx=-95, cz=-21, heading=25, L=13, W=9, floor=y, storeys=3, style="stone", door=1,
                           chimney=False, pitch=1.0), "the keep", margin_top=(B.STONEBRICK, 0), max_cut=4)
    # the Deep Stair's head: a round house over the shaft, its door to the court
    sx, sz = P.DEEP_STAIR
    # the lift to the Lower Gate: a vaulted stone room off the court, its doorway to the court
    lx, lz = -77, -26
    lift = set()
    for x in range(lx - 2, lx + 3):
        for z in range(lz - 2, lz + 3):
            lift.add((x, z))
            edge = abs(x - lx) == 2 or abs(z - lz) == 2
            for yy in range(y + 1, y + 5):
                w.set(x, yy, z, *((B.STONEBRICK, 0) if edge else (B.AIR, 0)))
            w.set(x, y + 5, z, B.STONE, 6)
            w.set(x, y, z, *((B.STONEBRICK, 3) if not edge else (B.STONEBRICK, 0)))
    for yy in (y + 1, y + 2, y + 3):
        w.set(lx - 2, yy, lz, B.AIR)
    w.set(lx, y + 4, lz, B.GLOWSTONE)
    claim(F, "the upper lift", lift)
    F.lift_top = (lx - 1, y + 1, lz - 1, lx + 1, y + 3, lz + 1)
    F.spawn_top = (P.SPAWN_TOP[0], y + 1, P.SPAWN_TOP[1])
    # a dais in the court where the team spawns, and a chest of blocks
    sx_, sz_ = P.SPAWN_TOP
    for x in range(sx_ - 2, sx_ + 3):
        for z in range(sz_ - 2, sz_ + 3):
            w.set(x, y, z, B.STONE, 6 if (x + z) % 2 else 4)
    w.chest(sx_ + 3, y + 1, sz_ - 3, [(0, "minecraft:planks", 64, 0), (1, "minecraft:cobblestone", 64, 0)], facing=3)
    claim(F, "the spawn dais", {(x, z) for x in range(sx_ - 2, sx_ + 3) for z in range(sz_ - 2, sz_ + 3)})


def deep_stair(w, F):
    """A spiral stair round a solid newel from Crownhold's court down to Underhall's floor, in a shaft lined
    with stone brick; a round house over its head with a door to the court, an arch at its foot."""
    cx, cz = P.DEEP_STAIR
    top, bot = 98, P.HALL_FLOOR
    ring = sorted({(x, z) for x in range(cx - 4, cx + 5) for z in range(cz - 4, cz + 5)
                   if 1.6 < math.hypot(x - cx, z - cz) <= 2.9}, key=lambda p: math.atan2(p[1] - cz, p[0] - cx))
    path = []
    for p in ring:
        if path and abs(p[0] - path[-1][0]) + abs(p[1] - path[-1][1]) == 2:
            path.append((p[0], path[-1][1], True))
        path.append((p[0], p[1], False))
    # the shaft
    for x in range(cx - 5, cx + 6):
        for z in range(cz - 5, cz + 6):
            d = math.hypot(x - cx, z - cz)
            for y in range(bot + 1, top + 8):
                if d <= 3.2:
                    w.set(x, y, z, *((B.STONEBRICK, 0) if d < 1.6 else (B.AIR, 0)))
                elif d <= 4.3 and y <= top + 6:
                    w.set(x, y, z, *((B.STONEBRICK, 0) if y % 7 else (B.STONE, 6)))
    # steps up from the floor, one a block, a landing at each corner
    y = bot
    i = 0
    steps = []
    while y < top:
        x, z, corner = path[i % len(path)]
        if not corner:
            y += 1
        w.set(x, y, z, B.STONEBRICK, 0)
        steps.append((x, z, y))
        i += 1
    # a landing at the head: a floor across the shaft at the court's level, open only over the last steps
    last = {(x, z) for x, z, yy in steps if yy >= top - 3}
    for x in range(cx - 4, cx + 5):
        for z in range(cz - 4, cz + 5):
            if 1.6 <= math.hypot(x - cx, z - cz) <= 3.2 and (x, z) not in last:
                w.set(x, top, z, B.STONEBRICK, 0)
    # the head: the shaft's top is open to the house over it, a door on the court side
    for x in range(cx - 4, cx + 5):
        for z in range(cz - 4, cz + 5):
            d = math.hypot(x - cx, z - cz)
            if d <= 3.2:
                for yy in range(top + 1, top + 5):
                    if d >= 1.6:
                        w.set(x, yy, z, B.AIR)
                w.set(x, top + 6, z, B.STONE, 6)
            if 3.2 < d <= 4.3:
                w.set(x, top + 7, z, B.STONEBRICK, 0) if (x + z) % 2 == 0 else None
    for k in (4,):
        for yy in (top + 1, top + 2, top + 3):
            w.set(cx + k, yy, cz + 1, B.AIR); w.set(cx + k, yy, cz + 2, B.AIR)
    hx, hz, hy = steps[-1]
    # the foot: an arch out into the cavern on the south
    for z in range(cz + 3, cz + 8):
        for x in (cx - 1, cx, cx + 1):
            for yy in range(bot + 1, bot + 4):
                w.set(x, yy, z, B.AIR)
            w.set(x, bot, z, B.STONEBRICK, 0)
    claim(F, "the Deep Stair", {(x, z) for x in range(cx - 4, cx + 5) for z in range(cz - 4, cz + 5)
                                if math.hypot(x - cx, z - cz) <= 4.3})
    F.deep_stair = steps


# ---------------------------------------------------------------------------------------------------------
# the Eyrie

def eyrie(w, F):
    cx, cz = P.MON_A
    base = 92
    top = base + 12
    r = 5.2
    cells = set()
    for x in range(int(cx - r) - 1, int(cx + r) + 2):
        for z in range(int(cz - r) - 1, int(cz + r) + 2):
            d = math.hypot(x - cx, z - cz)
            if d > r:
                continue
            cells.add((x, z))
            g = H(F, x, z)
            for y in range(min(g, base) - 4, top + 1):
                if y <= base:
                    w.set(x, y, z, B.STONEBRICK, 0)
                elif d > r - 1.0:
                    w.set(x, y, z, *((B.STONEBRICK, 0 if RNG.random() < 0.8 else 1) if (y - base) % 4 else (B.STONE, 6)))
                else:
                    w.set(x, y, z, B.AIR)
            w.set(x, top, z, B.STONEBRICK, 0) if d <= r - 1.0 else None
            if d > r - 1.0:
                w.set(x, top + 1, z, B.STONEBRICK, 0)
                if (x + z) % 2 == 0:
                    w.set(x, top + 2, z, B.STONEBRICK, 0)
    # arrow slits
    for k in range(8):
        a = 2 * math.pi * k / 8 + 0.2
        x, z = int(round(cx + (r - 0.5) * math.cos(a))), int(round(cz + (r - 0.5) * math.sin(a)))
        w.set(x, base + 6, z, B.AIR); w.set(x, base + 7, z, B.AIR)
    # the spiral stair round a newel
    ring = sorted({(x, z) for x in range(cx - 5, cx + 6) for z in range(cz - 5, cz + 6)
                   if 1.6 < math.hypot(x - cx, z - cz) <= 3.6}, key=lambda p: math.atan2(p[1] - cz, p[0] - cx))
    ring = [p for p in ring if 2.4 < math.hypot(p[0] - cx, p[1] - cz) <= 3.6]
    path = []
    for p in ring:
        if path and abs(p[0] - path[-1][0]) + abs(p[1] - path[-1][1]) == 2:
            path.append((p[0], path[-1][1], True))
        path.append((p[0], p[1], False))
    for y in range(base + 1, top):
        w.set(cx, y, cz, B.STONEBRICK, 0)
        for x, z in ((cx + 1, cz), (cx - 1, cz), (cx, cz + 1), (cx, cz - 1)):
            w.set(x, y, z, B.STONEBRICK, 0)
    y, i = base, 0
    last = None
    while y < top - 1:
        x, z, corner = path[i % len(path)]
        if not corner:
            y += 1
        w.set(x, y, z, B.STONEBRICK, 0)
        for k in (1, 2, 3):
            if y + k < top:
                w.set(x, y + k, z, B.AIR)
        last = (x, z, y)
        i += 1
    w.set(last[0], top, last[1], B.AIR)
    w.set(last[0], top + 1, last[1], B.AIR) if math.hypot(last[0] - cx, last[1] - cz) > r - 1 else None
    # doors: south to the Knife, east to the Goat Stair
    for (dx, dz) in ((0, 1), (1, 0)):
        for k in range(3, int(r) + 1):
            x, z = cx + dx * k, cz + dz * k
            for yy in (base + 1, base + 2, base + 3):
                w.set(x, yy, z, B.AIR)
                for s in (-1, 1):
                    if math.hypot(x + dz * s - cx, z + dx * s - cz) > r - 1.0:
                        pass
    # the monument at the open crown, on a pedestal
    w.set(cx, top + 1, cz, B.STONEBRICK, 3)
    w.set(cx, top + 2, cz, B.OBSIDIAN)
    w.set(cx, top + 3, cz, B.OBSIDIAN)
    F.mon_a = (cx, top + 2, cz)
    claim(F, "the Eyrie", cells)
    RECORDS.append(dict(kind="the Eyrie", cells=cells, floor=base, heading=0, storeys=3))


# ---------------------------------------------------------------------------------------------------------
# Wendholm

def heading_deg(dx, dz):
    return math.degrees(math.atan2(dz, dx))


def wendfoot(w, F):
    """The green at the Wend's foot: three houses round it at 0, 12 and 45 degrees to the grid, the same
    plan rasterised three ways, and a maypole on the grass between them."""
    gx, gz = P.GREEN
    for spec, name in ((dict(cx=gx + 3, cz=gz - 7, heading=0, L=9, W=6, storeys=2, style="plaster", jetty=True, door=1), "the 0-degree house"),
                       (dict(cx=gx + 4, cz=gz + 9, heading=12, L=9, W=6, storeys=2, style="town", jetty=True, door=-1), "the 12-degree house"),
                       (dict(cx=gx - 9, cz=gz + 2, heading=45, L=9, W=6, storeys=2, style="brick", jetty=True, door=1), "the 45-degree house")):
        fp = house.footprint(dict(spec, jetty=False))
        spec["floor"] = int(np.median([H(F, x, z) for x, z in fp]))
        WHY.clear()
        if place_house(w, F, spec, name, max_fill=3, max_cut=3) is None:
            F.conflicts.append((name, "could not be placed: " + ", ".join(WHY)))
    y = H(F, gx, gz)
    for yy in range(y + 1, y + 8):
        w.set(gx, yy, gz, B.FENCE)
    for k, col in enumerate((14, 4, 0, 5)):
        dx, dz = ((1, 0), (0, 1), (-1, 0), (0, -1))[k]
        for t in (1, 2):
            w.set(gx + dx * t, y + 7 - t, gz + dz * t, B.WOOL, col)
    claim(F, "the maypole", {(gx, gz)})


def wendholm(w, F):
    pts2 = [(x, z) for x, z, y in P.WEND]
    L = G.length(pts2)
    town = G.inside(F.X, F.Z, P.TOWN)

    def in_town(x, z):
        return (bool(town[x - F.x0, z - F.z0]) and F.wend[x - F.x0, z - F.z0] > 2.8 and F.corr[x - F.x0, z - F.z0] > 0.8
                and not F.market[x - F.x0, z - F.z0])
    n = 0
    for sd in (1, -1):                               # each side of the road is filled on its own
        s = 4.0
        while s < L - 6:
            (px, pz), (hx, hz) = G.point_at(pts2, s)
            y = int(round(route_y(P.WEND, s)))
            nx, nz = -hz * sd, hx * sd                   # the normal on this side of the road
            placed = False
            sizes = [(11, 7, 2), (9, 6, 2), (9, 6, 3), (8, 6, 2), (7, 6, 2), (7, 5, 2), (6, 5, 1), (6, 4, 1)]
            first = sizes[int(RNG.integers(1, 6)):]           # mostly middling houses; the large only now and then
            for Lh, Wh, storeys in (sizes[:1] if RNG.random() < 0.15 else []) + first:
                q = RNG.random()
                base_h = heading_deg(hx, hz)
                turn = 0 if q < 0.55 else (RNG.choice([-11, -7, 8, 12]) if q < 0.85 else 45)
                jetty = storeys >= 2 and Wh <= 6 and RNG.random() < 0.6
                off = 2.7 + Wh / 2 + (1 if jetty else 0)
                if turn == 45:
                    off = 2.7 + math.hypot(Lh, Wh) / 2 - 1
                cx, cz = px + nx * off, pz + nz * off
                # the door faces the road: which side of the house's own v axis the road is on
                th = math.radians(base_h + turn)
                vx, vz = -math.sin(th), math.cos(th)
                door = 1 if (px - cx) * vx + (pz - cz) * vz > 0 else -1
                style = RNG.choice(["town", "town", "plaster", "brick"])
                spec = dict(cx=cx, cz=cz, heading=base_h + turn, L=Lh, W=Wh, floor=y, storeys=storeys,
                            style=style, jetty=jetty, door=door)
                if place_house(w, F, spec, f"house {n}", allow=in_town):
                    n += 1
                    placed = True
                    s += Lh / 2 + 3
                    break
            s += 1.0
    F.town_houses = n
    # parapets: where the road runs along a drop of three or more, a low wall on its edge
    road = (F.wend < 2.6) & F.red & G.inside(F.X, F.Z, P.TOWN)
    for ix, iz in zip(*np.nonzero(road)):
        x, z = F.x0 + ix, F.z0 + iz
        g = H(F, x, z)
        if F.wend[ix, iz] < 1.6:
            continue
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            jx, jz = ix + dx, iz + dz
            if F.wend[jx, jz] >= 2.6 and H(F, x + dx, z + dz) <= g - 3 and (x + dx, z + dz) not in F.occ["surface"]:
                w.set(x, g + 1, z, B.COBBLE_WALL)
                break


def market(w, F):
    y = P.MARKET_Y
    # the cross, the well, two stalls
    cx, cz = -45, -3
    for yy in range(y + 1, y + 5):
        w.set(cx, yy, cz, B.COBBLE_WALL)
    w.set(cx, y + 5, cz, B.STONEBRICK, 3)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        w.set(cx + dx, y + 1, cz + dz, B.STONEBRICK_STAIRS, {(1, 0): 1, (-1, 0): 0, (0, 1): 3, (0, -1): 2}[(dx, dz)])
    claim(F, "the market cross", {(cx + dx, cz + dz) for dx in (-1, 0, 1) for dz in (-1, 0, 1)})
    wx, wz = -45, 6
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            if dx or dz:
                w.set(wx + dx, y + 1, wz + dz, B.COBBLE)
            else:
                for yy in range(y - 6, y + 1):
                    w.set(wx, yy, wz, B.WATER)
    for dx, dz in ((-1, -1), (1, 1)):
        for yy in (y + 2, y + 3):
            w.set(wx + dx, yy, wz + dz, B.FENCE)
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(wx + dx, y + 4, wz + dz, B.WOOD_SLAB, 1)
    claim(F, "the well", {(wx + dx, wz + dz) for dx in (-1, 0, 1) for dz in (-1, 0, 1)})
    for (sx, sz, col) in ((-46, -7, 14), (-37, 9, 4)):
        for dx in (0, 2):
            for dz in (0, 1):
                for yy in (y + 1, y + 2):
                    w.set(sx + dx, yy, sz + dz * 1, B.FENCE) if dz == 0 else None
        for dx in (-1, 0, 1, 2, 3):
            for dz in (-1, 0, 1):
                w.set(sx + dx, y + 3, sz + dz, B.WOOL, col if (dx % 2) else 0)
        w.set(sx + 1, y + 1, sz, B.HAY, 0)
        claim(F, f"stall {sx}", {(sx + dx, sz + dz) for dx in range(-1, 4) for dz in (-1, 0, 1)})


# ---------------------------------------------------------------------------------------------------------
# the vale

def kingsbridge(w, F):
    """A stone bridge along x across the river at z -0.5, its deck arched from 44 at the banks to 46, an arch
    under it, cobble-wall parapets. Red builds the west half; the half-turn completes it."""
    x0 = P.BRIDGE["x0"]
    cells = set()
    for x in range(x0, 0):
        t = (x - x0) / (-0.5 - x0)
        deck = int(round(44 + 2 * math.sin(math.pi / 2 * t)))
        for z in range(-3, 3):
            cells.add((x, z))
            edge = z in (-3, 2)
            w.set(x, deck, z, *((B.STONEBRICK, 0) if edge else (B.STONE, 5 if (x + z) % 3 else 0)))
            for yy in range(deck + 1, deck + 4):
                w.set(x, yy, z, B.AIR)
            if edge:
                w.set(x, deck + 1, z, B.COBBLE_WALL)
            # the arch: solid to the water, open under the middle
            arch = 41 + 3 * math.cos(math.pi * (x + 0.5) / (2 * abs(x0 + 0.5) * 0.55)) if abs(x + 0.5) < abs(x0 + 0.5) * 0.55 else -1
            for yy in range(30, deck):
                if arch > 0 and yy < arch:
                    continue
                if w.id(x, yy, z) in (B.AIR, B.WATER) or yy >= 40:
                    w.set(x, yy, z, B.STONEBRICK, 0)
        F.H[x - F.x0, :][2 + 96 - 3 - 2:0] if False else None
    claim(F, "Kingsbridge", cells)
    for (x, z) in cells:
        F.bridge.add((x, z))


def fords(w, F):
    """Stepping stones across the river at each ford: every other block a stone top a block above the water,
    two abreast."""
    for fz in P.FORDS:
        rx = P.river_x(fz)
        for x in range(int(rx - 9), int(rx + 10)):
            if x >= 0 or not F.river[x - F.x0, fz - F.z0]:
                continue
            if x % 2 == 0:
                for z in (fz, fz + 1):
                    w.set(x, P.WATER_Y, z, B.STONE, 0)
                    w.set(x, P.WATER_Y + 1, z, B.STONE, 5 if (x // 2) % 2 else 0)


def mill(w, F):
    mx, mz = P.MILL
    spec = dict(cx=mx, cz=mz, heading=-7, L=10, W=7, floor=46, storeys=2, style="town", jetty=False, door=-1)
    res = place_house(w, F, spec, "the mill", max_fill=6, max_cut=5)
    # the wheel: a ring of planks with spokes, upright in the brook beside the mill's south wall
    wz = mz + 6
    wx = mx - 1
    for k in range(48):
        a = 2 * math.pi * k / 48
        for rr in (3.5,):
            x = int(round(wx + rr * math.cos(a)))
            y = int(round(46 + rr * math.sin(a)))
            w.set(x, y, wz, B.PLANKS, 1)
    for k in range(8):
        a = 2 * math.pi * k / 8
        for t in (1, 2, 3):
            x = int(round(wx + t * math.cos(a)))
            y = int(round(46 + t * math.sin(a)))
            w.set(x, y, wz, B.FENCE)
    w.set(wx, 46, wz, B.LOG, 8)
    w.set(wx, 46, wz - 1, B.LOG, 8)
    claim(F, "the mill wheel", {(wx + dx, wz) for dx in range(-4, 5)})


def fields(w, F):
    """Fields laid at the angle of their first edge: rows of crops with a channel of water every fourth row,
    a fence round, a farmhouse at the gate set to the same angle."""
    gates = []
    for k, poly in enumerate(P.FIELDS):
        m = G.inside(F.X, F.Z, poly) & F.red
        (ax, az), (bx, bz) = poly[0], poly[1]
        hd = math.atan2(bz - az, bx - ax)
        c, s = math.cos(hd), math.sin(hd)
        ys = [int(F.H[i, j]) for i, j in zip(*np.nonzero(m))]
        y = int(np.median(ys))
        crop = [(B.WHEAT, 7), (B.CARROTS, 7), (B.POTATOES, 7)][k % 3]
        edge = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1))
        cells = set()
        for i, j in zip(*np.nonzero(m)):
            x, z = F.x0 + i, F.z0 + j
            cells.add((x, z))
            level(w, F, [(x, z)], y, None)
            v = -(x - ax) * s + (z - az) * c
            if edge[i, j]:
                w.set(x, y, z, B.GRASS)
                w.set(x, y + 1, z, B.FENCE)
            elif abs((v % 4) - 2) < 0.5:
                w.set(x, y, z, B.WATER)
            else:
                w.set(x, y, z, B.FARMLAND, 7)
                w.set(x, y + 1, z, *crop)
        claim(F, f"field {k}", cells)
        gates.append((k, poly, y, hd, cells))
    for k, poly, y, hd, cells in gates:
        (ax, az), (bx, bz) = poly[0], poly[1]
        c, s = math.cos(hd), math.sin(hd)
        # the gate and a farmhouse beside it at the field's angle
        gx, gz = int(round((ax + bx) / 2)), int(round((az + bz) / 2))
        for dx in (-1, 0, 1):
            if (gx + dx, gz) in cells:
                w.set(gx + dx, y + 1, gz, B.AIR)
        nx, nz = -s, c
        for off in (8, 10, 12):
            cx, cz = gx - nx * off, gz - nz * off
            spec = dict(cx=cx, cz=cz, heading=math.degrees(hd), L=9, W=6, floor=H(F, int(round(cx)), int(round(cz))),
                        storeys=1, style="town", door=1)
            if place_house(w, F, spec, f"farmhouse {k}", max_fill=4, max_cut=4, allow=lambda x, z: not F.water_any[x - F.x0, z - F.z0]):
                break


# ---------------------------------------------------------------------------------------------------------
# underground

def hall_of_echoes(w, F):
    """Monument B's temple: an octagon turned 22.5 degrees, pillared, a doorway in four of its faces, the
    monument on a stepped dais under a lantern of glowstone."""
    cx, cz = P.TEMPLE
    f = P.HALL_FLOOR
    R = 9.0
    oct_ = [(cx + R * math.cos(math.radians(22.5 + 45 * k)), cz + R * math.sin(math.radians(22.5 + 45 * k))) for k in range(8)]
    inner = G.inside(F.X, F.Z, oct_)
    edge = inner & ~(np.roll(inner, 1, 0) & np.roll(inner, -1, 0) & np.roll(inner, 1, 1) & np.roll(inner, -1, 1)
                     & np.roll(np.roll(inner, 1, 0), 1, 1) & np.roll(np.roll(inner, -1, 0), -1, 1)
                     & np.roll(np.roll(inner, 1, 0), -1, 1) & np.roll(np.roll(inner, -1, 0), 1, 1))
    cells = set()
    for i, j in zip(*np.nonzero(inner & F.red)):
        x, z = F.x0 + i, F.z0 + j
        cells.add((x, z))
        w.set(x, f, z, *((B.STONE, 6) if (x + z) % 2 else (B.STONEBRICK, 0)))
        for yy in range(f + 1, f + 10):
            w.set(x, yy, z, B.AIR)
        if edge[i, j]:
            door = min(abs(x - cx), abs(z - cz)) <= 1.2
            for yy in range(f + 1, f + 9):
                if door and yy <= f + 4:
                    continue
                w.set(x, yy, z, *((B.STONEBRICK, 0) if yy % 4 else (B.STONE, 6)))
        w.set(x, f + 9, z, B.STONEBRICK, 0)
    for k in range(8):
        a = math.radians(45 * k)
        x, z = int(round(cx + 5.5 * math.cos(a))), int(round(cz + 5.5 * math.sin(a)))
        for yy in range(f + 1, f + 9):
            w.set(x, yy, z, B.QUARTZ, 2)
    for r_, yy in ((3, f + 1), (2, f + 2)):
        for x in range(cx - r_, cx + r_ + 1):
            for z in range(cz - r_, cz + r_ + 1):
                w.set(x, yy, z, B.STONEBRICK, 0 if max(abs(x - cx), abs(z - cz)) == r_ else 3)
    w.set(cx, f + 3, cz, B.OBSIDIAN)
    w.set(cx, f + 4, cz, B.OBSIDIAN)
    w.set(cx, f + 8, cz, B.GLOWSTONE)
    F.mon_b = (cx, f + 3, cz)
    claim(F, "the Hall of Echoes", cells, "under")
    RECORDS.append(dict(kind="the Hall of Echoes", cells=cells, floor=f, heading=22.5, storeys=2))


def lower_gate(w, F):
    sx, sz = P.SPAWN_LOW
    f = P.HALL_FLOOR + 1
    for x in range(sx - 2, sx + 3):
        for z in range(sz - 2, sz + 3):
            w.set(x, f, z, B.STONE, 6 if (x + z) % 2 else 4)
    claim(F, "the lower spawn", {(x, z) for x in range(sx - 2, sx + 3) for z in range(sz - 2, sz + 3)}, "under")
    # the lift back up
    lx, lz = sx - 2, sz - 7
    lift = set()
    for x in range(lx - 2, lx + 3):
        for z in range(lz - 2, lz + 3):
            lift.add((x, z))
            edge = abs(x - lx) == 2 or abs(z - lz) == 2
            for yy in range(f + 1, f + 5):
                w.set(x, yy, z, *((B.STONEBRICK, 0) if edge else (B.AIR, 0)))
            w.set(x, f, z, B.STONEBRICK, 3 if not edge else 0)
    for yy in (f + 1, f + 2, f + 3):
        w.set(lx, yy, lz + 2, B.AIR)
    w.set(lx, f + 4, lz, B.GLOWSTONE)
    claim(F, "the lower lift", lift, "under")
    F.lift_low = (lx - 1, f + 1, lz - 1, lx + 1, f + 3, lz + 1)
    F.spawn_low = (sx, f + 1, sz)
    # lanterns round the gate hall
    for (x, z) in ((sx + 4, sz + 4), (sx - 4, sz + 5), (sx + 5, sz - 4)):
        for yy in (f + 1, f + 2):
            w.set(x, yy, z, B.FENCE)
        w.set(x, f + 3, z, B.GLOWSTONE)


def underhall_town(w, F):
    pts2 = [(x, z) for x, z, y in P.UNDERGATE]
    L = G.length(pts2)
    hall = (F.underhall < -2) & (F.mere > 3) & F.red
    # keep the ways through the cavern clear: the street, the tunnels' mouths, the stair's foot
    for t in P.TUNNELS:
        d, _ = G.polyline(F.X, F.Z, [(x, z) for x, z, y in t["pts"]])
        hall &= d > (t["half"] + (0.8 if t["name"] == "Undergate" else 2.5))
    sx_, sz_ = P.DEEP_STAIR
    hall &= np.hypot(F.X - sx_, F.Z - (sz_ + 6)) > 6

    def allow(x, z):
        return bool(hall[x - F.x0, z - F.z0]) and (x, z) in F.cave_floor
    s, side, n = 3.0, 1, 0
    while s < L - 3:
        (px, pz), (hx, hz) = G.point_at(pts2, s)
        placed = False
        for sd in (side, -side):
            nx, nz = -hz * sd, hx * sd
            for Lh, Wh in ((9, 6), (7, 6), (7, 5)):
                turn = RNG.choice([0, 0, 45, 15, -15])
                off = 2 + 1.5 + (math.hypot(Lh, Wh) / 2 if turn == 45 else Wh / 2)
                cx, cz = px + nx * off, pz + nz * off
                th = math.radians(heading_deg(hx, hz) + turn)
                door = 1 if (px - cx) * -math.sin(th) + (pz - cz) * math.cos(th) > 0 else -1
                spec = dict(cx=cx, cz=cz, heading=heading_deg(hx, hz) + turn, L=Lh, W=Wh, floor=P.HALL_FLOOR,
                            storeys=1 + int(RNG.random() < 0.4), style="delved", door=door, chimney=False)
                if place_house(w, F, spec, f"delved house {n}", margin_top=(B.STONE, 5), allow=allow, max_cut=2, max_fill=2,
                               layer="under"):
                    n += 1
                    placed = True
                    s += Lh * 0.6 + 1
                    break
            if placed:
                break
        side = -side
        if not placed:
            s += 1.5
    F.delved_houses = n
    # lantern posts along the street
    for k, (cx, cz) in enumerate(G.walk_cells(pts2)):
        if k % 7 == 3:
            for x, z in ((cx + 3, cz), (cx, cz + 3)):
                if (x, z) in F.cave_floor and (x, z) not in F.occ["under"]:
                    f = F.cave_floor[(x, z)]
                    for yy in (f + 1, f + 2, f + 3):
                        w.set(x, yy, z, B.FENCE)
                    w.set(x, f + 4, z, B.GLOWSTONE)
                    break
    # a pier out into Deepmere
    for x in range(-86, -79):
        for z in (11, 12, 13):
            if F.mere[x - F.x0, z - F.z0] < 1.5:
                w.set(x, P.MERE_Y + 1, z, B.PLANKS, 1)
        if x % 3 == 0:
            for z in (11, 13):
                for yy in range(P.MERE_Y - 4, P.MERE_Y + 1):
                    if w.id(x, yy, z) in (B.WATER, B.AIR):
                        w.set(x, yy, z, B.LOG, 1)


def mine_road(w, F):
    """Timber sets every four blocks down the Mine Road, and Delver's Door: a heavy frame at its mouth."""
    pts = P.MINE_ROAD
    cells = G.walk_cells([(x, z) for x, z, y in pts])
    L = G.length([(x, z) for x, z, y in pts])
    for k, (cx, cz) in enumerate(cells):
        y = int(round(route_y(pts, L * k / max(1, len(cells) - 1))))
        if k % 4 == 0 and 0 < k < len(cells) - 1:
            nx_, nz_ = cells[k + 1][0] - cx, cells[k + 1][1] - cz
            px_, pz_ = (-nz_, nx_)
            for sgn in (-1, 1):
                X, Z = cx + px_ * 2 * sgn, cz + pz_ * 2 * sgn
                if (X, Z) in F.tunnel_floor:
                    continue                            # where the road turns, its other leg is here
                for yy in range(y + 1, y + 4):
                    if w.id(X, yy, Z) == B.AIR:
                        w.set(X, yy, Z, B.FENCE)
            for t in (-2, -1, 0, 1, 2):
                X, Z = cx + px_ * t, cz + pz_ * t
                if w.id(X, y + 4, Z) == B.AIR:
                    w.set(X, y + 4, Z, B.PLANKS, 1)
        if k % 9 == 5:
            w.set(cx, y + 1, cz, B.RAIL, 0) if w.id(cx, y + 1, cz) == B.AIR else None
    # the door frame at the mouth
    mx, mz, my = pts[0]
    for dz in (-3, 3):
        for yy in range(my + 1, my + 6):
            w.set(mx, yy, mz + dz, B.LOG, 1)
    for dz in range(-3, 4):
        w.set(mx, my + 6, mz + dz, B.LOG, 1 | 8)
    w.sign(mx + 1, my + 3, mz - 3, ["Delver's", "Door", "", "to Underhall"], wall_facing=5)


def delving(w, F):
    """The Delving's walls lined in stone brick, and the Weeping Gallery at its middle: a round chamber under
    the river with a spring pool, moss, and water seeping in at its crown."""
    for (x, z), y in F.tunnel_floor.items():
        pass
    cx, cz = -0.5, -0.5
    f = 18
    for x in range(-9, 0):
        for z in range(-9, 9):
            d = math.hypot(x - cx, z - cz)
            if d > 7.5:
                continue
            vault = f + 6 + int(2 * (1 - d / 7.5))
            for yy in range(f + 1, vault + 1):
                w.set(x, yy, z, B.AIR)
            w.set(x, vault + 1, z, *((B.MOSSY, 0) if RNG.random() < 0.5 else (B.STONEBRICK, 1)))
            w.set(x, f, z, *((B.STONEBRICK, 1) if RNG.random() < 0.4 else (B.STONEBRICK, 0)))
            if d < 2.6:
                w.set(x, f, z, B.WATER)
                w.set(x, f - 1, z, B.CLAY)
            elif d > 6.6:
                for yy in range(f + 1, vault + 1):
                    w.set(x, yy, z, *((B.MOSSY, 0) if RNG.random() < 0.4 else (B.STONEBRICK, 1 if RNG.random() < 0.5 else 0)))
    for (x, z) in ((-3, -6), (-6, 2)):
        w.set(x, f + 7, z, B.WATER_FLOW, 8)
    claim(F, "the Weeping Gallery", {(x, z) for x in range(-8, 0) for z in range(-8, 8)}, "under")


# ---------------------------------------------------------------------------------------------------------
# paths: steps on the Goat Stair and the Knife

def path_steps(w, F, pts, name):
    d, s, ys = route_field(F, pts)
    cells = G.walk_cells([(x, z) for x, z, y in pts])
    L = G.length([(x, z) for x, z, y in pts])
    prev = None
    for k, (cx, cz) in enumerate(cells):
        if cx >= 0:
            continue
        y = H(F, cx, cz)
        if prev is not None:
            px_, pz_, py_ = prev
            if y == py_ + 1:
                dx, dz = cx - px_, cz - pz_
                data = {(1, 0): 0, (-1, 0): 1, (0, 1): 2, (0, -1): 3}.get((dx, dz))
                if data is not None and w.id(cx, y, cz) not in (B.AIR, B.WATER):
                    w.set(cx, y, cz, B.COBBLE_STAIRS, data)
        prev = (cx, cz, y)


def build(w, F):
    F.occ, F.conflicts, F.houses, F.bridge = {"surface": {}, "under": {}}, [], [], set()
    WHY.clear()
    RECORDS.clear()
    crownhold(w, F)
    deep_stair(w, F)
    eyrie(w, F)
    market(w, F)
    wendfoot(w, F)
    wendholm(w, F)
    kingsbridge(w, F)
    fords(w, F)
    mill(w, F)
    fields(w, F)
    hall_of_echoes(w, F)
    lower_gate(w, F)
    underhall_town(w, F)
    mine_road(w, F)
    delving(w, F)
    path_steps(w, F, P.GOAT_STAIR, "the Goat Stair")
    path_steps(w, F, P.KNIFE, "the Knife")
    F.records = RECORDS
    print(f"  {F.town_houses} houses in Wendholm, {F.delved_houses} in Underhall, {len(F.conflicts)} conflicts")
    print("  refusals:", WHY)
