"""Crucible's surface: what is made on the plain and the mountain.

    the casting pit   its floor paved as the foundry's floors are, the haul ramp and the bench in the haul set
    the gantry        a girder across the pit on two legs, the east one on the cone's shoulder, the crucible hung
                      from its trolley on two chains
    the roads         the slag road from the loading gate and the pit's road, graded and paved, meeting at the tip
    the tip           a timber trestle over the rift where the slag carts empty, slag spilt down the wall under it
    the flow          the black flow's channel falling into the rift, fed by a lavafall out of the cliff
    the stacks        two chimneys on the mountain over the furnace hall
    the heaps         slag heaps by the road, hornitos with a glowing throat, the cone's vent

    surface.build(w, H, C) after the foundry is carved
"""
import math

import numpy as np

import land
import palette as P
import plan as PL
from pgmvox import B
from pgmvox.geom.noise import spline

STONEBRICK = (B.STONEBRICK, 0)
SMOOTH = (B.DSLAB, 0)
POL_ANDESITE = (B.STONE, 6)
IRON = (B.IRON_BLOCK, 0)
NETHER = (B.NETHER_BRICK, 0)
DARK_OAK = (B.PLANKS, 5)
DARK_OAK_LOG = (B.LOG2, 1)
ORANGE = (B.STAINED_CLAY, 1)


def _set(w, x, y, z, b):
    w.set(x, y, z, b[0], b[1])


def top(w, x, z):
    return w.top(x, z)


def paint(w, x, z, name, u):
    y = w.top(x, z)
    if y < 1:
        return
    ids, dat = P.pick(name, np.array([u]))
    w.set(x, y, z, int(ids[0]), int(dat[0]))


# --- the casting pit ------------------------------------------------------------------------------------------
def pit(w, C):
    X, Z = land.grid()
    e, th = land.pit_polar(X, Z)
    p = PL.PIT
    on_ramp = (th >= p["ramp_to"]) & (th <= p["ramp_from"])
    u = P.cells(X, Z, 2, 9)
    for i, k in np.argwhere((e <= 1.0) & (Z >= 0)):
        x, z = int(X[i, k]), int(Z[i, k])
        y = w.top(x, z)
        if e[i, k] <= p["floor_e"] or (PL.APRON[0] <= x <= PL.APRON[1] and PL.APRON[2] <= z <= PL.APRON[3]):
            if y == p["floor"]:
                ids, dat = P.pick("floor", np.array([u[i, k]]))
                w.set(x, y, z, int(ids[0]), int(dat[0]))
        elif (on_ramp[i, k] and e[i, k] <= p["ramp_e"]) or (not on_ramp[i, k] and e[i, k] <= p["bench_e"]):
            ids, dat = P.pick("haul", np.array([u[i, k]]))
            w.set(x, y, z, int(ids[0]), int(dat[0]))
    # a kerb of stone brick along the haul ramp's inner edge where it stands three or more over the floor
    for i, k in np.argwhere(on_ramp & (e > p["floor_e"]) & (e <= p["floor_e"] + 0.07) & (Z >= 0)):
        x, z = int(X[i, k]), int(Z[i, k])
        y = w.top(x, z)
        if y - p["floor"] >= 3:
            _set(w, x, y, z, POL_ANDESITE)
    # casting moulds sunk in the floor: rows of sand-filled trenches either side of the crucible, edged in iron
    cx, cz = p["x"], p["z"]
    for dz in (-6, 6):
        for x in range(cx - 4, cx + 5):
            z = cz + dz
            if w.top(x, z) == p["floor"]:
                w.set(x, p["floor"], z, B.SAND, 1 if x % 2 else 0)


# --- the gantry -----------------------------------------------------------------------------------------------
def gantry(w, C):
    g = PL.GANTRY
    y = g["y"]
    east = g["x1"]
    for x in range(g["x0"], east + 1):
        for z in range(g["z0"], g["z1"] + 1):
            if z == g["z0"] or z == g["z1"]:
                _set(w, x, y - 1, z, IRON)                     # the girder's two flanges
            _set(w, x, y, z, SMOOTH)                           # the deck a player walks
    # the legs: a pier of stone brick under each end, down to the ground
    for xs in ((g["x0"], g["x0"] + 2),):
        for x in range(xs[0], xs[1] + 1):
            for z in range(g["z0"], g["z1"] + 1):
                yy = y - 2
                while yy > 1 and w.id(x, yy, z) in (B.AIR,):
                    corner = x in xs and z in (g["z0"], g["z1"])
                    _set(w, x, yy, z, POL_ANDESITE if corner else STONEBRICK)
                    yy -= 1
    # the east end rests on the cone's shoulder: rock under the deck where the cone falls short of it
    for x in range(east - 4, east + 1):
        for z in range(g["z0"], g["z1"] + 1):
            yy = y - 1 if z in (g["z0"], g["z1"]) else y - 1
            yy = y - 2 if z in (g["z0"], g["z1"]) else y - 1
            while yy > 1 and w.id(x, yy, z) == B.AIR:
                _set(w, x, yy, z, STONEBRICK)
                yy -= 1
    # the trolley over the crucible and its two chains down to the casing's top
    c = PL.CORE
    mx = (c.x0 + c.x1) // 2
    for x in range(mx - 1, mx + 2):
        for z in range(g["z0"], g["z1"] + 1):
            _set(w, x, y + 1, z, IRON if z != (g["z0"] + g["z1"]) // 2 else (B.DSLAB, 0))
    w.set(mx, y + 2, (g["z0"] + g["z1"]) // 2, B.SLAB, 0)
    for x in (c.x0 + 1, c.x1 - 1):
        for yy in range(c.y1 + 1, y - 1):
            w.set(x, yy, (c.z0 + c.z1) // 2, B.IRON_BARS)
    # the hook's beam under the girder: an iron course the chains hang from
    for x in range(c.x0, c.x1 + 1):
        _set(w, x, y - 2, (c.z0 + c.z1) // 2, IRON)


# --- roads -----------------------------------------------------------------------------------------------------
def roads(w, C):
    """Each road graded along its line, at most a block a step, three wide, paved in the haul set."""
    u = None
    for road in land.ROADS:
        pts = spline(road, 0.5)
        cells = []
        for x, z in pts:
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    c = (int(round(x + dx)), int(round(z + dz)))
                    if c not in cells:
                        cells.append(c)
        hs = np.array([w.top(x, z) for x, z in cells], float)
        # smooth the line's heights by their neighbours along it
        sm = np.array([np.median(hs[max(0, i - 6):i + 7]) for i in range(len(hs))])
        for (x, z), h in zip(cells, np.round(sm).astype(int)):
            y = w.top(x, z)
            if y < 0 or abs(h - y) > 3 or C.is_air(x, h, z):
                continue
            if h > y:
                for yy in range(y + 1, h + 1):
                    _set(w, x, yy, z, (B.STONE, 5))
            elif h < y:
                for yy in range(h + 1, y + 1):
                    w.set(x, yy, z, B.AIR)
            ids, dat = P.pick("haul", np.array([P.cells(np.array([x]), np.array([z]), 1, 4)[0]]))
            w.set(x, h, z, int(ids[0]), int(dat[0]))


# --- the tip ----------------------------------------------------------------------------------------------------
def tip(w):
    t = PL.TIP
    deck = max(w.top(x, t["z1"] + 1) for x in range(t["x0"], t["x1"] + 1))
    for x in range(t["x0"], t["x1"] + 1):
        for z in range(t["z0"], t["z1"] + 1):
            if w.id(x, deck, z) == B.AIR:
                _set(w, x, deck, z, DARK_OAK)
    # the trestle's legs: dark oak posts at its corners and halfway, down to the rift's wall
    for x in (t["x0"], t["x1"]):
        for z in (t["z0"], (t["z0"] + t["z1"]) // 2):
            yy = deck - 1
            while yy > land.LAVA and w.id(x, yy, z) == B.AIR:
                _set(w, x, yy, z, DARK_OAK_LOG)
                yy -= 1
    # the bracing beam across the legs, a course under the deck
    for x in range(t["x0"], t["x1"] + 1):
        w.set(x, deck - 1, t["z0"], B.LOG2, 1 + 4)
    # the buffer at the end: a log course and an iron stop either side
    for x in range(t["x0"], t["x1"] + 1):
        w.set(x, deck + 1, t["z0"], B.LOG2, 1 + 4)
    for x in (t["x0"], t["x1"]):
        _set(w, x, deck + 1, t["z0"], IRON)
    # slag spilt down the wall under the tip, a talus of slag to the lava
    rng = np.random.default_rng(31)
    for x in range(t["x0"] - 2, t["x1"] + 3):
        for z in range(t["z0"] - 4, t["z1"] + 1):
            y = w.top(x, z)
            if land.LAVA < y < deck - 1 and rng.random() < 0.8:
                for yy in range(y + 1, y + 1 + int(rng.integers(1, 3))):
                    if w.id(x, yy, z) == B.AIR and w.id(x, yy, z - 1) != B.LAVA:
                        ids, dat = P.pick("basalt", np.array([rng.random()]))
                        w.set(x, yy, z, int(ids[0]), int(dat[0]))


# --- lava --------------------------------------------------------------------------------------------------------
def lavafall(w, x, z, y_top, step):
    """Lava falling from (x, y_top, z) one block out along `step` (dz) down to the sea: the falling column cut into
    whatever wall stands there, so it pours down the face."""
    zz = z + step
    for y in range(y_top, land.LAVA, -1):
        if w.id(x, y, zz) in (B.AIR,) or w.id(x, y, zz) != B.LAVA:
            w.set(x, y, zz, B.LAVA_FLOW, 8)


def flow_falls(w, lip):
    """The black flow's channel pouring into the rift where it reaches the rim, and its source: a lavafall out of
    the cliff into the channel's head."""
    ch = land.lava_channel()
    X, Z = land.grid()
    red = [(int(X[i, k]), int(Z[i, k])) for i, k in np.argwhere(ch) if Z[i, k] >= 0]
    by_x = {}
    for x, z in red:
        by_x.setdefault(x, []).append(z)
    # the lip: the lowest z of each column of the channel, where the rim falls away
    for x, zs in by_x.items():
        z = min(zs)
        y = None
        for yy in range(90, 0, -1):
            if w.id(x, yy, z) == B.LAVA:
                y = yy
                break
        if y is None:
            continue
        if w.top(x, z - 1) < y - 1:
            lavafall(w, x, z, y, -1)
    # the head: where the channel meets the cliff, a notch high in the face pouring down into it
    def lava_y(x, z):
        for yy in range(90, 0, -1):
            if w.id(x, yy, z) == B.LAVA:
                return yy
        return None
    wet = [(x, z) for x, z in red if lava_y(x, z) is not None]
    hx, hz = max(wet, key=lambda c: c[1])
    hy = lava_y(hx, hz)
    if hy is not None:
        for zz in range(hz + 1, hz + 4):
            if w.top(hx, zz) > hy:
                notch = hy + 9
                for yy in range(hy, notch + 1):
                    w.set(hx, yy, zz, B.AIR)
                    w.set(hx, yy, zz - 1, B.LAVA_FLOW, 8) if yy > hy else None
                w.set(hx, notch, zz, B.LAVA)
                for yy in range(hy + 1, notch):
                    w.set(hx, yy, zz, B.LAVA_FLOW, 8)
                w.set(hx, hy, zz, B.LAVA)
                break


def vents(w):
    """The hornitos' throats and the cone's crater: netherrack round a glowstone throat, a lick of fire sheltered
    in it, no lava anywhere near the pit."""
    for hx, hz, hr, hh in land.HORNITOS:
        y = w.top(hx, hz)
        w.set(hx, y, hz, B.GLOWSTONE)
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
            yy = w.top(hx + dx, hz + dz)
            w.set(hx + dx, yy, hz + dz, B.NETHERRACK)
    cx, cz, cr = land.CONE
    for x in range(cx - 3, cx + 4):
        for z in range(cz - 3, cz + 4):
            r = math.hypot(x - cx, z - cz)
            y = w.top(x, z)
            if r < 1.6:
                w.set(x, y, z, B.GLOWSTONE)
            elif r < 3.4:
                w.set(x, y, z, B.NETHERRACK if (x + z) % 3 else B.OBSIDIAN)


def cooling_pond(w):
    """A pond of lava at the foot of the cliff between the facades, fed by a fall from a notch above: thirty blocks
    from the crucible and over its leak line, held in an obsidian kerb."""
    x0, x1, z0, z1 = -14, -8, 52, 56
    y = max(w.top(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1))
    for x in range(x0 - 1, x1 + 2):
        for z in range(z0 - 1, z1 + 2):
            edge = x in (x0 - 1, x1 + 1) or z in (z0 - 1, z1 + 1)
            t = w.top(x, z)
            if edge:
                for yy in range(t + 1, y + 1):
                    w.set(x, yy, z, B.OBSIDIAN)
                w.set(x, y, z, B.OBSIDIAN)
            else:
                for yy in range(y + 1, t + 1):
                    w.set(x, yy, z, B.AIR)
                w.set(x, y - 1, z, B.OBSIDIAN)
                w.set(x, y, z, B.LAVA)
    fx = (x0 + x1) // 2
    zc = z1 + 1
    while w.top(fx, zc) <= y + 2 and zc < z1 + 8:
        zc += 1
    notch = y + 12
    for yy in range(y + 1, notch + 1):
        w.set(fx, yy, zc - 1, B.LAVA_FLOW, 8)
        w.set(fx, yy, zc, B.AIR) if yy < notch else None
    w.set(fx, notch, zc, B.LAVA)


def stacks(w):
    """Two chimneys on the mountain over the furnace hall: hollow, stone brick with polished andesite corners, an
    orange band under a nether brick crown."""
    for cx, cz, top_y in ((9, 70, 104), (25, 73, 108)):
        ground = min(w.top(x, z) for x in range(cx - 2, cx + 3) for z in range(cz - 2, cz + 3))
        for y in range(ground - 2, top_y + 1):
            r = 2 if y < ground + 4 else 1
            for x in range(cx - r - 1, cx + r + 2):
                for z in range(cz - r - 1, cz + r + 2):
                    edge = x in (cx - r - 1, cx + r + 1) or z in (cz - r - 1, cz + r + 1)
                    if not edge:
                        w.set(x, y, z, B.AIR) if y > ground + 1 else None
                        continue
                    corner = x in (cx - r - 1, cx + r + 1) and z in (cz - r - 1, cz + r + 1)
                    b = NETHER if y >= top_y - 1 else ORANGE if y == top_y - 4 else \
                        POL_ANDESITE if corner else STONEBRICK
                    _set(w, x, y, z, b)
        for x in range(cx - 1, cx + 2):
            for z in range(cz - 1, cz + 2):
                w.set(x, ground + 1, z, B.NETHERRACK)
                w.set(x, ground + 1, z, B.GLOWSTONE) if (x, z) == (cx, cz) else None


def rails(w, C):
    """The slag line's rails down the slag run and across the loading hall to the gate."""
    run = next(s for s in PL.SPACES if s.name == "slag run")
    for x in range(run.x0, run.x1 + 1):
        if w.id(x, run.feet, 65) == B.AIR:
            w.set(x, run.feet, 65, B.RAIL, 1)
    gate = next(s for s in PL.SPACES if s.name == "loading gate")
    hall = next(s for s in PL.SPACES if s.name == "loading hall")
    rx = (gate.x0 + gate.x1) // 2
    for z in range(gate.z0, hall.z1 - 1):
        if w.id(rx, PL.L0, z) == B.AIR:
            w.set(rx, PL.L0, z, B.RAIL, 0)


def build(w, H, C, lip):
    pit(w, C)
    roads(w, C)
    gantry(w, C)
    tip(w)
    flow_falls(w, lip)
    vents(w)
    cooling_pond(w)
    stacks(w)
    rails(w, C)
