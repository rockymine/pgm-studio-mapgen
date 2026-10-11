"""Houses at any angle.

A house is drawn in its own frame: u runs along its ridge and v across it, and (cx, cz, heading) places
that frame on the board. Every block is decided by asking where its centre falls in the frame. So a wall
at 45 degrees comes out as a staircase one block at a time, and a wall at 12 degrees as a straight run
with a jog every five blocks. Nothing in this module assumes the walls lie along x or z.

What a block is, in the frame:
  inside a storey's rectangle, with any of 8 neighbours out  -> wall
  a wall block near two edges at once                       -> a post (an upright log)
  a wall block on a frame line every four blocks along u    -> a post
  the top course of a storey                                -> laid log along the wall's run, beam ends out
  a wall block on the window rows, between posts            -> glass
  under the roof surface r(v) = eave + (half-width - |v|)   -> roof, two thick so a 45 degree roof is closed
  a gable-end wall block under the roof surface             -> gable, never the roof's block

The ground storey stands on its plate: what is under the plate is filled in stone down to the ground, and
nothing rings the plate (no footing). The upper storey may be jettied out a block on its long sides.
"""
import math

import numpy as np

from mc import B

STYLES = {
    # ground storey, upper storey, frame log (data), gable, roof planks, roof slab
    "town": dict(ground=[(B.COBBLE, 0), (B.STONE, 5), (B.STONE, 0)], upper=[(B.PLANKS, 1)], post=0,
                 gable=(B.PLANKS, 1), roof=(B.PLANKS, 5), slab=(B.WOOD_SLAB, 5), floor=(B.PLANKS, 0)),
    "plaster": dict(ground=[(B.STONE, 0), (B.STONE, 5)], upper=[(B.STAINED_CLAY, 0)], post=1,
                    gable=(B.PLANKS, 1), roof=(B.PLANKS, 5), slab=(B.WOOD_SLAB, 5), floor=(B.PLANKS, 1)),
    "brick": dict(ground=[(B.BRICK, 0)], upper=[(B.PLANKS, 2)], post=0,
                  gable=(B.PLANKS, 1), roof=(B.PLANKS, 5), slab=(B.WOOD_SLAB, 5), floor=(B.PLANKS, 0)),
    "stone": dict(ground=[(B.STONEBRICK, 0), (B.STONEBRICK, 0), (B.STONEBRICK, 2)], upper=[(B.STONEBRICK, 0)], post=None,
                  gable=(B.COBBLE, 0), roof=(B.PLANKS, 5), slab=(B.WOOD_SLAB, 5), floor=(B.PLANKS, 1)),
    "delved": dict(ground=[(B.STONEBRICK, 0), (B.STONE, 6), (B.STONEBRICK, 1)], upper=[(B.STONE, 6)], post="chisel",
                   gable=None, roof=(B.STONEBRICK, 0), slab=(B.SLAB, 5), floor=(B.STONE, 6)),
}

LOG = B.LOG


class Frame:
    def __init__(self, cx, cz, heading_deg):
        self.cx, self.cz = cx, cz
        self.t = math.radians(heading_deg)
        self.c, self.s = math.cos(self.t), math.sin(self.t)

    def local(self, x, z):
        dx, dz = x - self.cx, z - self.cz
        return dx * self.c + dz * self.s, -dx * self.s + dz * self.c

    def world(self, u, v):
        return self.cx + u * self.c - v * self.s, self.cz + u * self.s + v * self.c


def rect_mask(fr, L, W, x0, z0, x1, z1):
    """Which blocks of the box have their centre inside the frame's L by W rectangle."""
    X, Z = np.meshgrid(np.arange(x0, x1 + 1), np.arange(z0, z1 + 1), indexing="ij")
    dx, dz = X - fr.cx, Z - fr.cz
    U = dx * fr.c + dz * fr.s
    V = -dx * fr.s + dz * fr.c
    return (np.abs(U) <= L / 2) & (np.abs(V) <= W / 2), U, V


def boundary(m):
    """The blocks of a mask with any of their eight neighbours outside it. Eight, not four: a wall at 45
    degrees drawn from four-neighbours touches only at its corners and can be seen through; from eight it
    steps two blocks at a time and is closed."""
    p = np.pad(m, 1)
    out = np.zeros(m.shape, bool)
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            if dx or dz:
                out |= ~p[1 + dx:p.shape[0] - 1 + dx, 1 + dz:p.shape[1] - 1 + dz]
    return m & out


def axis_of(dx, dz):
    """The log data bit for a beam lying along (dx, dz): 4 along x, 8 along z."""
    return 4 if abs(dx) >= abs(dz) else 8


def footprint(spec, margin=0):
    """The blocks the house stands on (its widest storey), with a margin: a set of (x, z)."""
    fr = Frame(spec["cx"], spec["cz"], spec["heading"])
    L, W = spec["L"], spec["W"] + (2 if spec.get("jetty") else 0)
    R = int(math.ceil(math.hypot(L, W) / 2)) + 2 + margin
    x0, z0 = int(math.floor(spec["cx"])) - R, int(math.floor(spec["cz"])) - R
    m, U, V = rect_mask(fr, L + 2 * margin, W + 2 * margin, x0, z0, x0 + 2 * R + 1, z0 + 2 * R + 1)
    xs, zs = np.nonzero(m)
    return {(x0 + i, z0 + k) for i, k in zip(xs, zs)}


def build(w, spec, ground_at=None, rng=None):
    """Build one house. spec: cx, cz, heading (degrees), L (along the ridge), W (across), floor (y of the
    plate), storeys (1-3), style, jetty (bool), door (+1 or -1: which long side), chimney (bool).
    ground_at(x, z) gives the ground's height so the plate can be filled down to it."""
    rng = rng or np.random.default_rng(int(abs(spec["cx"] * 31 + spec["cz"] * 17)))
    st = STYLES[spec.get("style", "town")]
    fr = Frame(spec["cx"], spec["cz"], spec["heading"])
    L, W = spec["L"], spec["W"]
    n = spec.get("storeys", 2)
    jetty = spec.get("jetty", False) and n >= 2
    f = spec["floor"]
    sh = 4                                           # a storey: three of wall and its top course
    R = int(math.ceil(math.hypot(L + 2, W + 4) / 2)) + 3
    x0, z0 = int(math.floor(spec["cx"])) - R, int(math.floor(spec["cz"])) - R
    x1, z1 = x0 + 2 * R + 1, z0 + 2 * R + 1

    def put(i, k, y, blk):
        w.set(x0 + i, y, z0 + k, *blk)

    dims = [(L, W + (2 if jetty and s > 0 else 0)) for s in range(n)]
    masks = []
    for s, (Ls, Ws) in enumerate(dims):
        m, U, V = rect_mask(fr, Ls, Ws, x0, z0, x1, z1)
        masks.append((m, boundary(m), U, V, Ls, Ws))
    base, base_wall, U, V, _, _ = masks[0]
    # --- the plate, and what is under it -----------------------------------------------------------
    for i, k in zip(*np.nonzero(base)):
        x, z = x0 + i, z0 + k
        g = ground_at(x, z) if ground_at else f
        for y in range(min(g, f), f):
            put(i, k, y, (B.STONE, 0) if rng.random() < 0.7 else (B.COBBLE, 0))
        put(i, k, f, st["floor"] if not base_wall[i, k] else st["ground"][0])
        for y in range(f + 1, f + 1 + n * sh + 12):
            put(i, k, y, (B.AIR, 0))
    # --- storeys ------------------------------------------------------------------------------------
    for s, (m, wall, U, V, Ls, Ws) in enumerate(masks):
        y0 = f + s * sh
        mats = st["ground"] if s == 0 else st["upper"]
        for i, k in zip(*np.nonzero(m)):
            u, v = U[i, k], V[i, k]
            if not wall[i, k]:
                if s > 0:
                    put(i, k, y0, st["floor"])          # the upper floor
                continue
            corner = abs(u) > Ls / 2 - 1.0 and abs(v) > Ws / 2 - 1.0
            longwall = abs(v) > Ws / 2 - 1.0
            run_u = u + Ls / 2
            frame_line = longwall and abs(((run_u + 2) % 4) - 2) < 0.5 and not corner
            post = st["post"] is not None and (corner or (frame_line and s > 0))
            # the run of this wall in the world, for the laid course's log axis
            dx, dz = (fr.c, fr.s) if longwall else (-fr.s, fr.c)
            for y in range(y0 + 1, y0 + sh + 1):
                top = y == y0 + sh
                if post and st["post"] == "chisel":
                    blk = (B.STONEBRICK, 3)
                elif post:
                    blk = (LOG, st["post"])
                elif top and st["post"] is not None and st["post"] != "chisel":
                    blk = (LOG, st["post"] | axis_of(dx, dz))        # the laid course at the storey's head
                else:
                    blk = mats[int(rng.integers(len(mats)))]
                    win_row = y in (y0 + 2, y0 + 3) if s > 0 else y == y0 + 2
                    run = run_u if longwall else V[i, k] + Ws / 2
                    span = Ls if longwall else Ws
                    if win_row and 1.5 < run < span - 1.5 and abs((run % 3) - 1.5) < 0.6:
                        blk = (B.PANE, 0) if st["post"] != "chisel" else (B.IRON_BARS, 0)
                put(i, k, y, blk)
        # beam ends: where a jettied storey sits on the one under it, the floor joists show past its wall
        if jetty and s == 1:
            for i, k in zip(*np.nonzero(m & ~masks[0][0])):
                put(i, k, y0, (LOG, (st["post"] or 0) | axis_of(-fr.s, fr.c)))
    # --- the door -----------------------------------------------------------------------------------
    side = spec.get("door", 1)
    wall0 = masks[0][1]
    cands = [(abs(U[i, k]), -side * V[i, k], i, k) for i, k in zip(*np.nonzero(wall0))
             if abs(U[i, k]) < max(1.2, L / 2 - 2) and side * V[i, k] > W / 2 - 1.0]
    U0, V0 = masks[0][2], masks[0][3]
    cands = [(abs(U0[i, k]), i, k) for i, k in zip(*np.nonzero(wall0)) if side * V0[i, k] > W / 2 - 1.0 and abs(U0[i, k]) < L / 2 - 1.5]
    door_at = None
    if cands:
        _, i, k = min(cands)
        nx, nz = -side * fr.s, side * fr.c                   # the door's outward normal
        facing = (0 if nx > 0 else 2) if abs(nx) >= abs(nz) else (1 if nz > 0 else 3)
        door = B.SPRUCE_DOOR if st["post"] != "chisel" else B.DARK_OAK_DOOR
        put(i, k, f + 1, (door, facing))
        put(i, k, f + 2, (door, 8))
        door_at = (x0 + i, z0 + k, (round(nx), round(nz)) if abs(nx) != abs(nz) else (int(math.copysign(1, nx)), 0))
    # --- the roof -------------------------------------------------------------------------------------
    mt, wt, Ut, Vt, Lt, Wt = masks[-1]
    eave = f + n * sh
    if st["gable"] is None:
        # a flat roof with a parapet: the delved houses of Underhall
        for i, k in zip(*np.nonzero(mt)):
            put(i, k, eave + 1, st["roof"])
            if wt[i, k] and (i + k) % 2 == 0:
                put(i, k, eave + 2, st["slab"])
    else:
        half = Wt / 2 + 1
        rm, Ur, Vr = rect_mask(fr, Lt + 2, Wt + 2, x0, z0, x1, z1)
        for i, k in zip(*np.nonzero(rm)):
            r = eave + (half - abs(Vr[i, k])) * spec.get("pitch", 1.0)
            yt = int(math.floor(r))
            inside_top = mt[i, k]
            low = yt - 1 if inside_top else yt
            for y in range(max(eave + 1, low), yt + 1):
                put(i, k, y, st["roof"])
            if r - yt >= 0.5:
                put(i, k, yt + 1, st["slab"])
            if not inside_top and yt <= eave:
                put(i, k, eave, st["slab"]) if False else None
            # the gable: the end walls of the top storey, up to the roof's underside
            if inside_top and wt[i, k] and abs(Ur[i, k]) > Lt / 2 - 1.0:
                for y in range(eave + 1, low):
                    put(i, k, y, st["gable"])
                if (yt - eave) > 3 and abs(Vr[i, k]) < 0.8:
                    put(i, k, eave + 2, (B.PANE, 0))          # a window in the gable
        if spec.get("chimney", True):
            cu = Lt / 4
            hx, hz = fr.world(cu, Wt / 4)
            ci, ck = int(round(hx)) - x0, int(round(hz)) - z0
            top = int(eave + (half - Wt / 4) * spec.get("pitch", 1.0)) + 3
            for y in range(f + 1, top + 1):
                if y > f + n * sh or y <= f + 1 or True:
                    put(ci, ck, y, (B.COBBLE, 0) if y < top else (B.COBBLE_WALL, 0))
    return dict(door=door_at, footprint=footprint(spec), eave=eave)
