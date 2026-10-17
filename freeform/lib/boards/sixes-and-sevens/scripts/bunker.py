"""Bunker 06, Red's, in the author's Bunker style: the rooms carved into the mountain and walled in segments, the
upper floor and its switchback stair, ceilings, floors, the facade with its door, the blast walls, and the
yard with its slanted panels. Blue's bunker 07 is the half turn of it.

    build(w)
"""
from pgmvox import B
from pgmvox.built import segments as S
from pgmvox.grammar import bunker as T

import plan as P

F = P.FIELD
ROOMS = {                 # name: (x0, x1, z0, z1), height
    "hall": (P.HALL, 24), "spawn": (P.SPAWN_HALL, 16), "dark": (P.DARK, 24), "tunnel": (P.TUNNEL, 8),
    "yard tunnel": (P.YARD_TUNNEL, 8), "dark tunnel": (P.DARK_TUNNEL, 8), "side tunnel": (P.SIDE_TUNNEL, 8),
    "yard": (P.YARD, P.FRONT_H),
}
STACKS = {                # the tiers of a room's walls, foot first
    "hall": [T.GRAY_CYAN_SEG, T.ANDESITE_SEG, T.STRIPE_OBSIDIAN_SEG],
    "spawn": [T.ANDESITE_SEG, T.STRIPE_GRAY_SEG],
    "dark": [T.DARK_SEG, T.GRAY_CYAN_SEG, T.ANDESITE_SEG],
    "yard": [T.ANDESITE_SEG, T.ANDESITE_SEG, T.ANDESITE_SEG, T.STRIPE_GRAY_SEG],
    "facade": [T.ANDESITE_SEG, T.ANDESITE_SEG, T.ANDESITE_SEG, T.STRIPE_GRAY_SEG],
}
UPPER_MOUTHS = {(-83, 18, -82, 23): P.FIELD + 16, (-73, 18, -72, 23): P.FIELD + 17}   # a mouth that also carries the corridor
BEAM, CEIL, LIGHT = (B.STONE, 6), (B.COBBLE, 0), (B.GLOWSTONE, 0)
RAIL = (B.COBBLE_WALL, 0)
STAIR_FILL = (B.STONE, 6)


def _box_cells(box):
    x0, x1, z0, z1 = box
    return {(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)}


def _carver(upper=None):
    """An opening's lay: carve the face column and the one behind it, through the ground floor's eight rows, and
    the corridor's rows over a floor at 49 where the mouth carries the corridor too."""
    def lay(w, columns, side, y0, y1):
        ix, iz = S.DIRS[S.OPP[side]]
        for x, z in columns:
            for dx, dz in ((0, 0), (ix, iz)):
                for y in range(F + 1, F + 9):
                    w.set(x + dx, y, z + dz, B.AIR)
                if upper:
                    w.set(x + dx, P.UPPER, z + dz, *BEAM)
                    for y in range(P.UPPER + 1, upper + 1):
                        w.set(x + dx, y, z + dz, B.AIR)
    return lay


def door(w, columns, side, y0, y1):
    """The door: open, eighteen by sixteen, framed in obsidian in the face and coal a block back."""
    ix, iz = S.DIRS[S.OPP[side]]
    n = len(columns)
    for s, (x, z) in enumerate(columns):
        for y in range(y0, y1 + 1):
            edge = s in (0, n - 1) or y == y1
            inner = s in (1, n - 2) or y == y1 - 1
            w.set(x, y, z, *(S.OBSIDIAN if edge else S.AIR))
            w.set(x + ix, y, z + iz, *(S.OBSIDIAN if edge else (B.COAL_BLOCK, 0) if inner else S.AIR))


def ceiling(w, box, y):
    """A ceiling of cobblestone crossed by polished-andesite beams on the segments' six, a glowstone in each bay."""
    x0, x1, z0, z1 = box
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            beam = (x - x0) % 6 == 5 or (z - z0) % 6 == 5
            light = (x - x0) % 6 == 2 and (z - z0) % 6 == 2
            w.set(x, y, z, *(BEAM if beam else LIGHT if light else CEIL))


def stair(w):
    """The switchback in the spawn hall: four treads three deep climbing west, a landing, three climbing east, and
    the upper landing at 49 over the first flight's foot."""
    (sx, sz), _, _ = P.STAIR_FLIGHTS[0]
    for k in range(4):                                         # 41 .. 44, climbing west
        xa = sx - 3 * k
        w.fill(xa - 2, F + 1, sz, xa, F + 1 + k, sz + 2, *STAIR_FILL)
    lx = sx - 12
    w.fill(lx - 2, F + 1, sz, lx, F + 5, sz + 5, *STAIR_FILL)  # the landing, 45, the full width
    (tx, tz), _, _ = P.STAIR_FLIGHTS[1]
    for k in range(3):                                         # 46 .. 48, climbing east
        xa = tx + 3 * k
        w.fill(xa, F + 1, tz, xa + 2, F + 6 + k, tz + 2, *STAIR_FILL)
    x0, x1, z0, z1 = P.STAIR_TOP
    w.fill(tx + 9, P.UPPER, z0, x1, P.UPPER, z1, *BEAM)        # the upper landing, over the first treads


def gallery(w):
    """The upper floor in the tall hall: a slab at 49 round its back and south side, pillars under its edge on the
    segments' six, a rail along it."""
    hall = _box_cells(P.HALL[:2] + P.HALL[2:])
    floor = set()
    for box in P.GALLERY:
        floor |= _box_cells(box)
    for x, z in floor:
        w.set(x, P.UPPER, z, *BEAM)
    edge = {(x, z) for x, z in floor if any((x + dx, z + dz) in hall and (x + dx, z + dz) not in floor
                                            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    for x, z in edge:
        w.set(x, P.UPPER + 1, z, *RAIL)
        along_x = (x + 1, z) in edge or (x - 1, z) in edge             # an edge running east to west
        if ((x - P.HALL[0]) if along_x else (z - P.HALL[2])) % 6 == 5:
            w.fill(x, F + 1, z, x, P.UPPER - 1, z, *BEAM)
    for x, z in edge:                                          # the corridor's mouth onto the gallery stays open
        if z >= 18 and x <= -70:
            w.set(x, P.UPPER + 1, z, B.AIR)


def yard_panels(w):
    """The yard's back wall in panels set out of line, as tall as the facade: each bay a block further out toward the
    field than the one north of it, each tier a block back from the one under it."""
    x0, x1, z0, z1 = P.YARD
    for i in range(4):
        for j in range(4):
            xf = x0 - 1 + i - j
            za = z0 + 6 * i
            y0 = F + 1 + 8 * j
            w.fill(xf - 1, y0, za, xf, y0 + 7, za + 5, *S.COBBLE)
            w.fill(xf + 1, y0, za, x0 - 1, y0 + 7, za + 5, B.AIR)      # nothing stands in front of a stepped-back panel
            S.lay_segment(w, STACKS["yard"][j], [(xf, za + 5 - s) for s in range(6)], "e", y0, 8)


def blast_wall(w, z0, length=14, h_hi=19, h_lo=16, width=4, band=F + 10):
    """A blast wall four wide out from the facade, painted like the lofted walls, a gray-wool line round it, its top
    falling from h_hi at the facade to h_lo at its end."""
    for k, x in enumerate(range(P.FACADE_X + 1, P.FACADE_X + 1 + length)):
        top = round(h_hi - (h_hi - h_lo) * k / max(1, length - 1))
        for z in range(z0, z0 + width):
            rim = z in (z0, z0 + width - 1) or k == length - 1
            for y in range(F + 1, F + 1 + top):
                v = (y - F - 1) / max(1, top - 1)
                block, _ = T.LOFT.at(v, v, v, (x, y, z))
                w.set(x, y, z, *(S.GRAY_WOOL if rim and y == band else block))


def build(w):
    air = {}
    for name, (box, h) in ROOMS.items():
        for c in _box_cells(box):
            air[c] = name
    mouths = {}
    for box, faces in P.MOUTHS:
        for c in _box_cells((box[0], box[2], box[1], box[3])):
            mouths[c] = box
    # carve the rooms; the yard to the sky
    for name, (box, h) in ROOMS.items():
        x0, x1, z0, z1 = box
        w.fill(x0, F + 1, z0, x1, (w.sy - 2) if name == "yard" else F + h, z1, B.AIR)
    # the walls: every column within two of a room, the facade, each as tall as what it faces
    near = lambda x, z, r: [air[(x + i, z + j)] for i in range(-r, r + 1) for j in range(-r, r + 1)
                            if (x + i, z + j) in air]
    height = lambda name: ROOMS[name][1]
    facade = {(x, z) for x in (P.FACADE_X - 1, P.FACADE_X) for z in range(P.FACADE_Z[0], P.FACADE_Z[1] + 1)}
    cells, owner = set(facade), {c: "facade" for c in facade}
    xs = [b[0][0] for b in ROOMS.values()] + [b[0][1] for b in ROOMS.values()]
    zs = [b[0][2] for b in ROOMS.values()] + [b[0][3] for b in ROOMS.values()]
    for x in range(min(xs) - 2, max(xs) + 3):
        for z in range(min(zs) - 2, max(zs) + 3):
            if (x, z) in air or (x, z) in facade or x >= P.FACADE_X:
                continue
            for r in (1, 2):
                names = near(x, z, r)
                if names:
                    cells.add((x, z))
                    owner[(x, z)] = (min if r == 1 else max)(names, key=height)
                    break
    heights = {c: (P.FRONT_H if n == "facade" else height(n)) for c, n in owner.items()}
    field = lambda x, z: x > P.FACADE_X and P.FACADE_Z[0] <= z <= P.FACADE_Z[1]

    def choose(side, i, j, run, over):
        name = owner[run[0]]
        if over and name != "facade":
            return T.ANDESITE_SEG
        stack = STACKS.get(name)
        return stack[min(j, len(stack) - 1)] if stack else T.ANDESITE_SEG

    door_hi = F + 16
    openings = [S.Opening("e", P.DOOR_Z[0], P.DOOR_Z[1], F + 1, door_hi, door, line=P.FACADE_X),
                S.Opening("w", P.DOOR_Z[0], P.DOOR_Z[1], F + 1, door_hi, lambda *a: None, line=P.FACADE_X - 1)]
    for box, faces in P.MOUTHS:
        upper = UPPER_MOUTHS.get(box)
        lo, hi = (box[1], box[3]) if faces[0][0] in ("e", "w") else (box[0], box[2])
        for side, line in faces:
            openings.append(S.Opening(side, lo, hi, F + 1, (upper or F + 8), _carver(upper), line=line))
    yard_back = {(x, z) for x, z in cells if owner[(x, z)] == "yard" and x < P.YARD[0]}
    S.wall(w, cells - yard_back, F + 1, heights, T.ANDESITE_SEG, lambda x, z: (x, z) in air or field(x, z),
           segment_of=choose, openings=openings)
    yard_panels(w)
    (mx0, mz0, mx1, mz1), _ = P.MOUTHS[3]                     # the yard tunnel's mouth, through the panels
    w.fill(mx0, F + 1, mz0, P.YARD[0] - 1 + 1, F + 8, mz1, B.AIR)
    # the corridor over the spawn tunnel, a segment tall, on the tunnel's walls
    cx0, cx1, cz0, cz1 = P.UPPER_CORRIDOR
    w.fill(cx0, P.UPPER, cz0, cx1, P.UPPER, cz1, *BEAM)
    w.fill(cx0, P.UPPER + 1, cz0, cx1, P.UPPER + 8, cz1, B.AIR)
    corridor = _box_cells(P.UPPER_CORRIDOR)
    ring = {(x, z) for x in range(cx0, cx1 + 1) for z in (cz0 - 2, cz0 - 1, cz1 + 1, cz1 + 2)}
    S.wall(w, ring, P.UPPER + 1, 8, T.ANDESITE_SEG, lambda x, z: (x, z) in corridor)
    ceiling(w, P.UPPER_CORRIDOR, P.UPPER + 9)
    # ceilings, floors, the upper floor, the stair
    for name, (box, h) in ROOMS.items():
        if name != "yard":
            ceiling(w, box, F + h + 1)
        seg = T.FLOOR_DARK if name == "dark" else T.FLOOR_L
        if name != "yard":
            S.floor(w, (box[0], box[2], box[1], box[3]), F, seg, module=T.FLOOR_MODULE, align=(box[0], box[2]))
    for box, _ in P.MOUTHS:
        S.floor(w, box, F, T.FLOOR_L, module=T.FLOOR_MODULE, align=(box[0], box[1]))
    gallery(w)
    stair(w)
    for z0 in (P.DOOR_Z[0] - 6, P.DOOR_Z[1] + 3):
        blast_wall(w, z0)
