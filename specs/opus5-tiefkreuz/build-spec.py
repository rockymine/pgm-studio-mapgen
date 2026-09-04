#!/usr/bin/env python3
"""Write the plan and the finish for Tiefkreuz — a city crossing played on four storeys.

    python3 specs/opus5-tiefkreuz/build-spec.py
    python3 tools/drive.py specs/opus5-tiefkreuz "Tiefkreuz" \
            --out maps/opus5-tiefkreuz --renders specs/opus5-tiefkreuz/renders

Two railways cross at right angles over the same block of city, and the board is played on both of
them. The deep line runs north–south in cut-and-cover under the street and goes on through a tunnel
into the back of the map; the elevated line crosses it east–west on a brick viaduct, with a platform,
a canopy and a train of its own. One monument stands on each line, in the four-foot between its rails.
Behind the crossing is the quarter the two stations serve: an arterial road under the viaduct's
northern flank, an avenue with a planted verge, and six flat-roofed blocks on a grid, the tallest of
which is the spawn.

    y 5      the ballast of the deep tracks
    y 6      their rails, one course proud of it
    y 7      the cess — a step at each track edge, so a track is a trough a player walks through
    y 8      the platforms — an island between two side platforms
    y 18     the concourse mezzanine
    y 29     the street, which is the box's lid where it crosses it
    y 41/42  the viaduct's deck and the elevated platform on it

Everything is stated absolutely: the board carries no relief at all, which is what keeps a four-storey
stack arithmetic rather than a negotiation with a solver.

Two words decide how a shape is painted. A shape that is GROUND — a platform floor, a concourse slab,
the street, a planted verge — carries a `theme`, whose five buckets are resolved per column. A shape
that is a THING MADE OF SOMETHING — a rail, a kerb, a stair tread, a stilt, a road, a parapet, a
carriage side — carries a `material` instead, which paints its whole span with no rim, no wall and no
surface depth. A shape with no interior column can never show a theme's surface (SK23), and every one
of those on this board is a material.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "opus5-tiefkreuz"

# ── the stack, in world Y ──────────────────────────────────────────────────────────────
BALLAST_H = 6     # span [0,6)   -> top y5
RAIL_H    = 7     # span [0,7)   -> top y6, painted ballast-under-iron by a height band stack
CESS_H    = 8     # span [0,8)   -> top y7, the step between platform and ballast
PLAT_H    = 9     # span [0,9)   -> top y8,  walk y9
POST_Y    = 9     # canopy posts [9,15)
CANOPY_Y  = 15    # canopy roof  [15,16)
MEZZ_Y    = 17    # span [17,19) -> top y18, walk y19
TUN_Y     = 12    # tunnel roof  [12,30) -> top y29
LID_Y     = 27    # street lid   [27,30) -> top y29
STREET_H  = 30    # span [0,30)  -> top y29, walk y30   (the plan's own surface)
PIER_H    = 37    # span [0,37)  -> top y36, the girder rests on it
GIRD_Y    = 37    # girders      [37,39)
VIA_Y     = 39    # deck [39,42) top y41; platform [39,43) top y42; parapet [39,45) top y44

CELL = 4

# ── the box, in blocks (all rects are half-open [lo, hi) ) ─────────────────────────────
# Every x-rect is centred on the origin as [-a, a): a rot_180 board mirrors a half-open
# span [lo, hi) onto [-hi, -lo), so a rect is its own image only where min = -max.
BOX   = (-20, 20)
PLATW = (-20, -14)                 # west platform
TRKW  = (-14, -8)                  # west track
ISL   = (-8, 8)                    # island platform
TRKE  = (8, 14)                    # east track
PLATE = (14, 20)                   # east platform
# The two tracks are mirror images of each other about the axis, so the board's own rot_180
# maps one onto the other exactly: column c maps to -1-c.
RAILS = (-13, -10, 9, 12)          # one column each, a course proud of the ballast
CESSES = (-14, -9, 8, 13)          # one column each, a course proud of the rails

PLAT_Z  = (16, 58)                 # platforms, cess and box lining
TRACK_Z = (16, 76)                 # ballast and rails, on through the tunnel
MOUTH_Z = (16, 24)                 # the tunnel throat at the chasm, roofed
BAY_Z   = (24, 42)                 # the open bay: no lid, no mezzanine, daylight
CONC_Z  = (42, 58)                 # the concourse and the lid over it
TUN_Z   = (58, 76)                 # the north tunnel: the two bores alone, roofed at y12

WELL_G = (-14, -8, 52, 58)         # the shaft over the deep monument: street to track, 24 blocks
WELL_E = (14, 20, 46, 52)          # a light well over the east platform

STAIR_A_X = (-3, 3)                # island platform -> concourse, in the open bay
STAIR_A_Z0, STAIR_A_N = 32, 10     # ten treads, one rise each: y8 -> y18
STAIR_B_X = (10, 16)               # concourse -> street
STAIR_B_Z0, STAIR_B_N = 44, 11     # eleven treads, one rise each: y18 -> y29
STAIR_B_HOLE = (9, 17, 44, 55)     # what the street lid gives up for it

# ── the viaduct, and the elevated station on it ────────────────────────────────────────
VIA_X  = (-36, 36)
VP_S   = (57, 58)                  # south parapet
VPLAT  = (58, 61)                  # the elevated platform
VTRK   = (61, 68)                  # the elevated track
VRAILS = (62, 65)                  # one column each
VP_N   = (68, 69)                  # north parapet
GIRD_Z = (57, 69)
PIER_Z = (59, 66)
# Every pier stands inboard of the coast, because a pier flush with it shows its whole buried
# shaft down the cliff face — 29 courses of brick in a wall of city stone.
PIERS_X = ((-34, -30), (-27, -23), (-20, -16), (16, 20), (23, 27), (30, 34))
TOWERS = ((-30, -24), (24, 30))    # the two stair towers up to the elevated platform
TOWER_Z0, TOWER_N = 44, 12         # twelve treads y30..y41, then a landing at y42
TOWER_LAND = (56, 58)

# ── the trains ────────────────────────────────────────────────────────────────────────
TRAIN_X = (9, 13)                  # the deep train, standing at the east platform
TRAIN_CARS = ((28, 39), (41, 52))  # two cars with a gap between them
HTRAIN_Z = (62, 66)                # the elevated train, on the elevated track
HTRAIN_CARS = ((-12, -1), (1, 12))
HTRAIN_Y = 43                      # its underframe stands a course over the rails

# ── the quarter behind the crossing ───────────────────────────────────────────────────
# The whole avenue is 16 blocks wide and sits over the island platform's own footprint,
# which is what keeps its verges off the two tunnel bores either side: an override add drawn
# over a bore fills it, and nothing says the tunnel it filled is gone.
AVE_X    = (-3, 3)                 # the avenue's carriageway
WALK_X   = ((-5, -3), (3, 5))      # its pavements
VERGE_X  = ((-8, -5), (5, 8))      # its planted verges
AVE_Z    = (60, 100)
ART_Z    = (84, 88)                # the arterial, across the quarter behind the crossing
ART_WALK = ((82, 84), (88, 90))
ART_X    = (-34, 34)

# ── goals ─────────────────────────────────────────────────────────────────────────────
TIEF = (-12, 56)                   # in the four-foot of the west deep track, at the portal
HOCH = (24, 63)                    # in the four-foot of the elevated track

# ── the blocks a player is made of ────────────────────────────────────────────────────
def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}


CONCRETE  = solid(43, 8)    # smooth stone: the box lining, every stair, every kerb
MASONRY   = solid(98, 0)    # stone brick: the girders, the stair towers, the pier plinths
BRICK     = solid(45, 0)    # the viaduct
IRON      = solid(42, 0)    # rail head
BALLAST   = solid(13, 0)
GLOW      = solid(89, 0)
ASPHALT   = solid(159, 15)
MARKING   = solid(159, 4)
CAR_BODY  = solid(159, 14)  # the trains
CAR_TRIM  = solid(159, 8)
CAR_FRAME = solid(159, 15)
CAR_GLASS = solid(95, 3)


def banded(frm, bands, beyond):
    """A band stack read up the world's own Y, which is how one shape says 'ballast, then a rail'
    or 'plinth, shaft, impost' without being three shapes contesting one column."""
    return {"kind": "layered", "axis": "height", "from": frm,
            "stack": {"bands": [{"material": m, "thickness": t} for m, t in bands],
                      "ending": "repeat"},
            "beyond": beyond}


RAIL_MAT  = banded(0, ((BALLAST, BALLAST_H), (IRON, 1)), IRON)
VRAIL_MAT = banded(VIA_Y, ((BALLAST, 3), (IRON, 1)), IRON)
PIER_MAT  = banded(0, ((MASONRY, 3), (BRICK, 30), (MASONRY, 4)), MASONRY)
PARA_MAT  = banded(VIA_Y, ((BRICK, 5), (MASONRY, 1)), MASONRY)


# ── rectangle algebra, so a slab can be drawn round its holes ──────────────────────────
def carve(outer, holes):
    """outer minus holes, as a list of non-overlapping half-open rects.

    A layer holds one span per column, so a lid with a stairwell in it is not a rectangle
    with a hole: it is the rectangles that remain once the hole is taken out. Banding by z
    keeps the count low and the pieces long."""
    x0, x1, z0, z1 = outer
    cuts = sorted({z0, z1} | {v for h in holes for v in (h[2], h[3]) if z0 < v < z1})
    out = []
    for a, b in zip(cuts, cuts[1:]):
        spans = [(x0, x1)]
        for hx0, hx1, hz0, hz1 in holes:
            if hz1 <= a or hz0 >= b:
                continue
            nxt = []
            for sx0, sx1 in spans:
                if hx1 <= sx0 or hx0 >= sx1:
                    nxt.append((sx0, sx1))
                    continue
                if sx0 < hx0:
                    nxt.append((sx0, min(hx0, sx1)))
                if hx1 < sx1:
                    nxt.append((max(hx1, sx0), sx1))
            spans = nxt
        for sx0, sx1 in spans:
            if sx1 > sx0:
                out.append((sx0, sx1, a, b))
    # fuse vertically adjacent bands of the same x-span, so the document stays readable
    fused, out = [], sorted(out, key=lambda r: (r[0], r[1], r[2]))
    for r in out:
        if fused and fused[-1][0] == r[0] and fused[-1][1] == r[1] and fused[-1][3] == r[2]:
            fused[-1] = (r[0], r[1], fused[-1][2], r[3])
        else:
            fused.append(r)
    return fused


SHAPES = []


def rect(sid, box, floor, height, paint, override=True, keep=False):
    """One rectangle. `paint` is a theme id (a string) or a TerrainMaterial (a dict): the two
    answer the same question at two grains and stating both is SK24."""
    x0, x1, z0, z1 = box
    s = {"id": sid, "type": "rectangle", "operation": "add",
         "min_x": x0, "max_x": x1, "min_z": z0, "max_z": z1,
         "floor": floor, "base_height": height}
    s["material" if isinstance(paint, dict) else "theme"] = paint
    if override:
        s["override"] = True
        s["height_mode"] = "level"
        s["skirt"] = 0
        s["relief_scope"] = "exclude"
    if keep:
        s["keepClear"] = True
    return s


def ground(sid, box, height, paint, floor=0, keep=True):
    SHAPES.append(rect(sid, box, floor, height, paint, True, keep=keep))


# ══ the ground layer: the street, the box cut into it, the stairs, the roads ═══════════
# The box. Five strips across, clamped side by side so nothing contests anything: a layer
# holds one span per column and the taller add wins it, so a hall is drawn as the shapes
# AROUND its floor rather than as a floor inside a wall.
for name, span, h, paint, zs in (
        ("plat-w", PLATW, PLAT_H, "bahn", PLAT_Z),
        ("trk-w",  TRKW,  BALLAST_H, "schotter", TRACK_Z),
        ("plat-m", ISL,   PLAT_H, "bahn", PLAT_Z),
        ("trk-e",  TRKE,  BALLAST_H, "schotter", TRACK_Z),
        ("plat-e", PLATE, PLAT_H, "bahn", PLAT_Z)):
    ground(f"box-{name}", (span[0], span[1], *zs), h, paint)

# The rails. One shape a rail, painted by a height band stack — ballast to y5, iron at y6 —
# so a rail sits ON the bed instead of being an iron pillar sunk six courses into it.
for i, x in enumerate(RAILS):
    ground(f"schiene-{i}", (x, x + 1, *TRACK_Z), RAIL_H, RAIL_MAT)

# The cess: one column of concrete a course over the rail head at each track edge. It turns
# the two-block scramble out of a track into a stair of single steps, so a track is a trough
# a player walks through — platform y8, cess y7, rail y6, four-foot y5 — and the monument
# standing in the four-foot is reached on foot from either platform.
for i, x in enumerate(CESSES):
    ground(f"bankett-{i}", (x, x + 1, *PLAT_Z), CESS_H, CONCRETE)

# The box lining: one column either side, at the street's own height, so the box's inner
# face reads as concrete rather than as city paving. One course prouder where the shed is
# open, which is the parapet that stops the street's own edge being a flush 21-block drop.
for side, (lx0, lx1) in (("w", (BOX[0] - 1, BOX[0])), ("e", (BOX[1], BOX[1] + 1))):
    for k, (z0, z1) in enumerate(((PLAT_Z[0], BAY_Z[0]), (BAY_Z[1], PLAT_Z[1]))):
        ground(f"box-wand-{side}-{k}", (lx0, lx1, z0, z1), STREET_H, CONCRETE)
    ground(f"box-bruestung-{side}", (lx0, lx1, *BAY_Z), STREET_H + 2, CONCRETE)

# The lamps. A light is a block and a material states blocks, so a lit floor is a one-column
# shape carrying glowstone — there is no lamp prop and none is needed. Without them the two
# storeys under the street are unplayable.
LAMPS = ([(x, z, PLAT_H) for x in (-17, 17) for z in range(20, 57, 6)] +
         [(-4, z, PLAT_H) for z in range(20, 57, 6)] +
         [(x, z, BALLAST_H) for x in (-12, 10) for z in range(60, 76, 5)])
for i, (lx, lz, lh) in enumerate(LAMPS):
    ground(f"lampe-p{i}", (lx, lx + 1, lz, lz + 1), lh, GLOW)

# Stair A — the island platform up to the concourse, one rise to one tread. Ten treads and
# ten blocks of run, drawn down the middle of the island so neither side of it is the drop
# into a track, and walled by a balustrade a course over each tread either way.
for k in range(STAIR_A_N):
    z = STAIR_A_Z0 + k
    ground(f"treppe-p{k}", (STAIR_A_X[0], STAIR_A_X[1], z, z + 1), PLAT_H + k, CONCRETE)
    for side, (bx0, bx1) in (("w", (STAIR_A_X[0] - 1, STAIR_A_X[0])),
                             ("e", (STAIR_A_X[1], STAIR_A_X[1] + 1))):
        ground(f"gelaender-p{side}{k}", (bx0, bx1, z, z + 1), PLAT_H + k + 2, CONCRETE)

# The two stair towers up to the elevated platform: twelve treads from the street and a
# landing level with the platform, so a player steps off the top of the flight onto it.
for t, (tx0, tx1) in enumerate(TOWERS):
    for k in range(TOWER_N):
        z = TOWER_Z0 + k
        ground(f"hochtreppe-{t}-{k}", (tx0, tx1, z, z + 1), STREET_H + 1 + k, MASONRY)
        for side, (bx0, bx1) in (("w", (tx0 - 1, tx0)), ("e", (tx1, tx1 + 1))):
            ground(f"hochgelaender-{t}{side}{k}", (bx0, bx1, z, z + 1),
                   STREET_H + 3 + k, MASONRY)
    ground(f"hochpodest-{t}", (tx0, tx1, *TOWER_LAND), VIA_Y + 4, MASONRY)
    for side, (bx0, bx1) in (("w", (tx0 - 1, tx0)), ("e", (tx1, tx1 + 1))):
        ground(f"hochpodest-{t}{side}", (bx0, bx1, *TOWER_LAND), VIA_Y + 6, MASONRY)

# The viaduct's piers. Three a side, with a clear span of 32 blocks over the station box, so
# nothing stands on either bore. Each is one shape painted plinth-shaft-impost up its own face.
for i, (x0, x1) in enumerate(PIERS_X):
    ground(f"pfeiler-{i}", (x0, x1, *PIER_Z), PIER_H, PIER_MAT)

# ── the roads, which are shapes and not strokes ────────────────────────────────────────
# A stroke seats on whatever surface a column carries, so a road drawn under the viaduct
# paves the viaduct. A road that is a shape lands where it is drawn, states its own material,
# and keeps props off itself exactly, with no margin, through keepClear.
AVENUE = [("allee-fahrbahn", (AVE_X[0], AVE_X[1], *AVE_Z), ASPHALT)]
for i, (wx0, wx1) in enumerate(WALK_X):
    AVENUE.append((f"allee-gehweg-{i}", (wx0, wx1, *AVE_Z), CONCRETE))
for i, z in enumerate(range(AVE_Z[0] + 2, AVE_Z[1] - 2, 6)):
    AVENUE.append((f"allee-strich-{i}", (-1, 1, z, z + 2), MARKING))
for sid, box, mat in AVENUE:
    ground(sid, box, STREET_H, mat)

ground("arterie-fahrbahn", (ART_X[0], ART_X[1], *ART_Z), STREET_H, ASPHALT)
for i, (z0, z1) in enumerate(ART_WALK):
    ground(f"arterie-gehweg-{i}", (ART_X[0], ART_X[1], z0, z1), STREET_H, CONCRETE)
for i, x in enumerate(list(range(-32, -6, 6)) + list(range(8, 33, 6))):
    ground(f"arterie-strich-{i}", (x, x + 2, ART_Z[0] + 2, ART_Z[0] + 4), STREET_H, MARKING)

# The planting: two verges down the avenue and two on the station forecourt, carved where the
# arterial crosses. A verge is ground rather than a made thing, so it carries a theme — turf
# over two courses of soil — which is also what stops six trees standing on bare stone.
# A verge is planted, so it is the one road-side shape the dressing pass may put a tree on:
# keepClear here declines every one of them by name.
for i, (vx0, vx1) in enumerate(VERGE_X):
    for j, (z0, z1) in enumerate(((AVE_Z[0], ART_WALK[0][0]), (ART_WALK[1][1], AVE_Z[1]))):
        ground(f"allee-gruen-{i}{j}", (vx0, vx1, z0, z1), STREET_H, "gruen", keep=False)


# ══ the layers over and under the street ═══════════════════════════════════════════════
def layer(lid, name, base_y, shapes, kind=None, part_of=None):
    e = {"id": lid, "name": name, "base_y": base_y, "shapes": shapes,
         "groups": [{"id": lid + "-g", "name": name, "mirrors": True,
                     "shapeIds": [s["id"] for s in shapes]}]}
    if kind:
        e["kind"] = kind
    if part_of:
        e["part_of"] = part_of
    return e


LAYERS = []


def train(prefix, part, x_span, cars, base, along_x):
    """One train, as four made layers: underframe with its bogies, body with its doors and cab
    ends, a window band with pillars between the windows, and a roof. A colour change inside a
    run splits a layer as surely as air does, so each band is a layer of its own and `made`
    keeps the stacking rules and both reachability walks off all of them.

    `along_x` says which way the train is long. A car's own detail — four bogies, two doorways,
    a pillar every fourth window — is stated in the long axis and mirrored into the rects."""
    def box(a0, a1, b0, b1):
        """(a0, a1) is the interval along the train's length and (b0, b1) across it; this puts
        the pair the rasterizer wants first, which is x."""
        return (a0, a1, b0, b1) if along_x else (b0, b1, a0, a1)

    frame, body, glass, roof = [], [], [], []
    lo, hi = x_span
    mid0, mid1 = lo + 1, hi - 1
    ends = (cars[0][0], cars[-1][1])
    for c, (a0, a1) in enumerate(cars):
        bogies = [(a0 + 1, a0 + 3), (a1 - 3, a1 - 1)]
        doors = [(a0 + 3, a0 + 5), (a1 - 5, a1 - 3)]
        for i, (b0, b1) in enumerate(bogies):
            frame.append(rect(f"{prefix}-drehgestell-{c}{i}", box(b0, b1, lo, hi), 0, 1,
                              CAR_FRAME, override=False))
        for i, (f0, f1, fb0, fb1) in enumerate(carve((mid0, mid1, a0, a1),
                                                     [(mid0, mid1, b0, b1) for b0, b1 in bogies])):
            frame.append(rect(f"{prefix}-rahmen-{c}{i}", box(fb0, fb1, f0, f1), 0, 1,
                              CAR_FRAME, override=False))
        for i, (b0, b1) in enumerate(doors):
            body.append(rect(f"{prefix}-tuer-{c}{i}", box(b0, b1, lo, hi), 0, 3,
                             CAR_TRIM, override=False))
            glass.append(rect(f"{prefix}-tuerkopf-{c}{i}", box(b0, b1, lo, hi), 0, 1,
                              CAR_TRIM, override=False))
        cabs = [(a, a + 1) for a in (a0, a1 - 1) if a in ends or a + 1 in ends]
        for i, (b0, b1) in enumerate(cabs):
            body.append(rect(f"{prefix}-kopf-{c}{i}", box(b0, b1, lo, hi), 0, 3,
                             CAR_TRIM, override=False))
            glass.append(rect(f"{prefix}-front-{c}{i}", box(b0, b1, lo, hi), 0, 1,
                              CAR_GLASS, override=False))
        cut = [(lo, hi, b0, b1) for b0, b1 in doors + cabs]
        for i, (f0, f1, fb0, fb1) in enumerate(carve((lo, hi, a0, a1), cut)):
            body.append(rect(f"{prefix}-kasten-{c}{i}", box(fb0, fb1, f0, f1), 0, 3,
                             CAR_BODY, override=False))
        pillars = [(a0 + 2, a0 + 3), (a1 - 3, a1 - 2)]
        for i, (b0, b1) in enumerate(pillars):
            glass.append(rect(f"{prefix}-saeule-{c}{i}", box(b0, b1, lo, hi), 0, 1,
                              CAR_BODY, override=False))
        for i, (f0, f1, fb0, fb1) in enumerate(carve((lo, hi, a0, a1), cut +
                                                     [(lo, hi, b0, b1) for b0, b1 in pillars])):
            glass.append(rect(f"{prefix}-fenster-{c}{i}", box(fb0, fb1, f0, f1), 0, 1,
                              CAR_GLASS, override=False))
        roof.append(rect(f"{prefix}-dach-{c}", box(a0, a1, lo, hi), 0, 1,
                         CAR_TRIM, override=False))
    for tag, shapes, y in (("fahrwerk", frame, base), ("kasten", body, base + 1),
                           ("fenster", glass, base + 4), ("dach", roof, base + 5)):
        LAYERS.append(layer(f"{prefix}-{tag}", f"{part} {tag}", y, shapes,
                            kind="made", part_of=part))


train("zug", "Triebzug", TRAIN_X, TRAIN_CARS, 7, along_x=False)
train("hochzug", "Hochbahnzug", HTRAIN_Z, HTRAIN_CARS, HTRAIN_Y, along_x=True)

# The platform canopies in the open bay, and the posts under them. A stilt is one column, so
# every column of it is an edge and no theme's surface can ever appear on it: it states the
# concrete it is made of instead.
CANOPIES = ((PLATW, BAY_Z, (-19, -16)), (PLATE, BAY_Z, (15, 18)),
            (ISL, (BAY_Z[0], STAIR_A_Z0 - 1), (-7, 6)))
posts, roofs = [], []
for i, ((cx0, cx1), (cz0, cz1), pxs) in enumerate(CANOPIES):
    roofs.append(rect(f"dach-{i}", (cx0, cx1, cz0, cz1), 0, 1, CONCRETE, override=False))
    for px in pxs:
        for pz in range(cz0 + 2, cz1 - 1, 5):
            posts.append(rect(f"stuetze-{px}-{pz}", (px, px + 1, pz, pz + 1), 0,
                              CANOPY_Y - POST_Y, MASONRY, override=False))
LAYERS.append(layer("perron-fuss", "Bahnsteigstützen", POST_Y, posts, kind="made",
                    part_of="perron"))
LAYERS.append(layer("perron", "Bahnsteigdach", CANOPY_Y, roofs, kind="made", part_of="perron"))

# The north tunnel: the two bores go on under the city with a roof of their own at y12, so the
# rails run out of the station rather than stopping at a buffer. It is a plain layer with the
# city's theme, and its top three courses ARE the street over it.
LAYERS.append(layer("tunnel", "Tunnelröhre", TUN_Y, [
    rect(f"roehre-{i}", (span[0], span[1], *TUN_Z), 0, STREET_H - TUN_Y, "stadt",
         override=False, keep=True)
    for i, span in enumerate((TRKW, TRKE))]))

# The concourse mezzanine: a slab over the whole box at the north end, with two wells dropped
# through it, a parapet along its open south lip, and the street flight standing on it.
mezz = []
HALL_LAMPS = [(x, z) for z in (46, 54) for x in (-16, -4, 4, 16)]
lamp_rects = [(x, x + 2, z, z + 2) for x, z in HALL_LAMPS]
SLAB_Z = (CONC_Z[0] + 1, CONC_Z[1])
for x0, x1, z0, z1 in carve((BOX[0], BOX[1], *SLAB_Z), [WELL_G, WELL_E] + lamp_rects):
    mezz.append(rect(f"halle-{x0}-{z0}", (x0, x1, z0, z1), 0, 2, "bahn",
                     override=False, keep=True))
for i, box in enumerate(lamp_rects):
    mezz.append(rect(f"lampe-h{i}", box, 0, 2, GLOW, override=False, keep=True))
# the south lip: two courses proud of the floor, with one gap where stair A arrives on it
for i, (x0, x1, z0, z1) in enumerate(carve((BOX[0], BOX[1], CONC_Z[0], CONC_Z[0] + 1),
                                           [(STAIR_A_X[0], STAIR_A_X[1], CONC_Z[0],
                                             CONC_Z[0] + 1)])):
    mezz.append(rect(f"halle-bruestung-{i}", (x0, x1, z0, z1), 0, 4, CONCRETE,
                     override=False, keep=True))
mezz.append(rect("halle-schwelle", (STAIR_A_X[0], STAIR_A_X[1], CONC_Z[0], CONC_Z[0] + 1),
                 0, 2, CONCRETE, override=False, keep=True))
# a kerb round each well, so the concourse's own holes read as edges
for name, (wx0, wx1, wz0, wz1) in (("g", WELL_G), ("e", WELL_E)):
    for i, (x0, x1, z0, z1) in enumerate(carve((wx0 - 1, wx1 + 1, wz0 - 1, wz1 + 1),
                                               [(wx0, wx1, wz0, wz1)])):
        if x0 >= BOX[0] and x1 <= BOX[1] and z0 >= SLAB_Z[0] and z1 <= SLAB_Z[1]:
            mezz.append(rect(f"halle-kranz-{name}{i}", (x0, x1, z0, z1), 0, 4, CONCRETE,
                             override=False, keep=True))
# Stair B — the concourse up to the street, one rise to one tread, standing ON the slab rather
# than cut out of it, and walled the same way stair A is.
for k in range(STAIR_B_N):
    z = STAIR_B_Z0 + k
    mezz.append(rect(f"treppe-s{k}", (STAIR_B_X[0], STAIR_B_X[1], z, z + 1), 0, 3 + k,
                     CONCRETE, override=False, keep=True))
    for side, (bx0, bx1) in (("w", (STAIR_B_X[0] - 1, STAIR_B_X[0])),
                             ("e", (STAIR_B_X[1], STAIR_B_X[1] + 1))):
        mezz.append(rect(f"gelaender-s{side}{k}", (bx0, bx1, z, z + 1), 0, 5 + k,
                         CONCRETE, override=False, keep=True))
LAYERS.append(layer("halle", "Zwischengeschoss", MEZZ_Y, mezz))

# The lid: the street where it crosses the box. Absent over the open bay, over the stair
# mouth and over the two wells, which is what makes them wells rather than rooms.
lid = []
for x0, x1, z0, z1 in (carve((BOX[0], BOX[1], MOUTH_Z[0], MOUTH_Z[1] - 1), []) +
                       carve((BOX[0], BOX[1], CONC_Z[0] + 1, CONC_Z[1]),
                             [STAIR_B_HOLE, WELL_G, WELL_E])):
    lid.append(rect(f"deckel-{x0}-{z0}", (x0, x1, z0, z1), 0, STREET_H - LID_Y, "stadt",
                    override=False))
# and the kerbs: along the bay's two ends, and round every hole the lid carries
kerbs = [(BOX[0], BOX[1], BAY_Z[0] - 1, BAY_Z[0]),
         (BOX[0], BOX[1], BAY_Z[1], BAY_Z[1] + 1)]
for wx0, wx1, wz0, wz1 in (STAIR_B_HOLE, WELL_G, WELL_E):
    # the stairwell's north side is left open, because that is where the top tread meets the
    # pavement and a kerb there is a wall across the way out
    walk_out = wz1 if (wx0, wx1, wz0, wz1) == STAIR_B_HOLE else None
    kerbs += [r for r in carve((wx0 - 1, wx1 + 1, wz0 - 1, wz1 + 1), [(wx0, wx1, wz0, wz1)])
              if BOX[0] <= r[0] and r[1] <= BOX[1] and CONC_Z[0] < r[2] and r[3] <= CONC_Z[1]
              and r[2] != walk_out]
for i, (x0, x1, z0, z1) in enumerate(kerbs):
    lid.append(rect(f"kante-{i}", (x0, x1, z0, z1), 0, STREET_H - LID_Y + 2, CONCRETE,
                    override=False))
LAYERS.append(layer("deckel", "Straßendecke", LID_Y, lid))

# The girders: a two-course edge beam down each side of the deck, a cross beam on every pier
# and a soffit course between them, so the deck is carried rather than floating over nine
# blocks of air.
gird = []
notches = [(tx0 - 1, tx1 + 1, TOWER_LAND[0], TOWER_LAND[1]) for tx0, tx1 in TOWERS]
for i, (x0, x1, z0, z1) in enumerate(carve((VIA_X[0], VIA_X[1], GIRD_Z[0], GIRD_Z[0] + 2),
                                           notches) +
                                     carve((VIA_X[0], VIA_X[1], GIRD_Z[1] - 2, GIRD_Z[1]), [])):
    gird.append(rect(f"traeger-rand-{i}", (x0, x1, z0, z1), 0, 2, MASONRY, override=False))
for i, (x0, x1) in enumerate(PIERS_X):
    gird.append(rect(f"traeger-quer-{i}", (x0, x1, GIRD_Z[0] + 2, GIRD_Z[1] - 2), 0, 2,
                     MASONRY, override=False))
for i, (x0, x1, z0, z1) in enumerate(carve((VIA_X[0], VIA_X[1], GIRD_Z[0] + 2, GIRD_Z[1] - 2),
                                           [(px0, px1, GIRD_Z[0] + 2, GIRD_Z[1] - 2)
                                            for px0, px1 in PIERS_X])):
    gird.append(rect(f"traeger-untersicht-{i}", (x0, x1, z0, z1), 1, 1, MASONRY,
                     override=False))
LAYERS.append(layer("traeger", "Überbau", GIRD_Y, gird))

# The viaduct: a parapet, a platform, a track between two rails, a parapet — the elevated
# station, notched at both parapets where a stair tower's landing arrives on it.
via = []
for i, (x0, x1, z0, z1) in enumerate(carve((VIA_X[0], VIA_X[1], *VP_S), notches) +
                                     carve((VIA_X[0], VIA_X[1], *VP_N), [])):
    via.append(rect(f"bruestung-{i}", (x0, x1, z0, z1), 0, 6, PARA_MAT, override=False))
via.append(rect("hochsteig", (VIA_X[0], VIA_X[1], *VPLAT), 0, 4, "bahn",
                override=False, keep=True))
for i, (x0, x1, z0, z1) in enumerate(carve((VIA_X[0], VIA_X[1], *VTRK),
                                           [(VIA_X[0], VIA_X[1], r, r + 1) for r in VRAILS])):
    via.append(rect(f"via-bett-{i}", (x0, x1, z0, z1), 0, 3, "schotter", override=False))
for i, z in enumerate(VRAILS):
    via.append(rect(f"via-schiene-{i}", (VIA_X[0], VIA_X[1], z, z + 1), 0, 4, VRAIL_MAT,
                    override=False))
LAYERS.append(layer("viadukt", "Hochbahn", VIA_Y, via))

# The elevated station's canopy, on its own posts over its own platform.
hposts = [rect(f"hstuetze-{px}", (px, px + 1, VPLAT[0] + 1, VPLAT[0] + 2), 0, 5, MASONRY,
               override=False)
          for px in range(VIA_X[0] + 4, VIA_X[1] - 3, 8)]
LAYERS.append(layer("hochperron-fuss", "Hochbahnsteigstützen", VIA_Y + 4, hposts,
                    kind="made", part_of="hochperron"))
LAYERS.append(layer("hochperron", "Hochbahnsteigdach", VIA_Y + 9, [
    rect("hochdach", (VIA_X[0], VIA_X[1], *VPLAT), 0, 1, CONCRETE, override=False)],
    kind="made", part_of="hochperron"))

LAYERS.sort(key=lambda e: (e["base_y"], e["id"]))


# ── the plan ──────────────────────────────────────────────────────────────────────────
PLAN = {
    "plan": 2,
    "meta": {"name": "Tiefkreuz"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 16,
                "surface": STREET_H, "observerY": 76},
    "pieces": [
        {"id": "kai",       "role": "piece", "rect": [-7,  4, 14, 3], "surface": STREET_H},
        {"id": "bahnhof",   "role": "piece", "rect": [-10, 7, 20, 8], "surface": STREET_H},
        {"id": "stadt",     "role": "piece", "rect": [-9, 15, 18, 7], "surface": STREET_H},
        {"id": "vorplatz",  "role": "piece", "rect": [-9, 22, 18, 3], "surface": STREET_H},
        {"id": "flanke-w",  "role": "piece", "rect": [-9, 25,  7, 3], "surface": STREET_H},
        {"id": "kopfbau",   "role": "spawn", "rect": [-2, 25,  4, 3], "surface": STREET_H},
        {"id": "flanke-e",  "role": "piece", "rect": [2,  25,  7, 3], "surface": STREET_H},
    ],
    "zones": [{"id": "uebergang", "rect": [-7, -4, 14, 8]}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "kopfbau", "at": [8, 6], "facing": "front"}],
        "destroyables": [
            {"id": "tief", "piece": "", "at": list(TIEF), "layer": "ground",
             "style": "pillar-2", "materials": "obsidian", "float": 2,
             "name": "Tiefbahnsteig"},
            {"id": "hoch", "piece": "", "at": list(HOCH), "layer": "viadukt",
             "style": "pillar-2", "materials": "obsidian", "float": 2,
             "name": "Hochbahnsteig"},
        ],
    },
}


# ── the themes: four places, and everything made stated as a material ─────────────────
def noise(seed, scale, stops, octaves=2):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves,
            "stops": [solid(*s) for s in stops], "rise": 0}


def theme(surface, wall, fill, rim=None, depth=2, rim_edges="void"):
    t = {"bedrock": {"relative": False, "value": 1},
         "rimEdges": rim_edges, "wallOnTerrainFaces": True,
         "surface": {"enabled": True, "depth": depth, "material": surface},
         "wall": wall, "wallEnabled": True, "fill": fill}
    t["rim"] = ({"enabled": True, "depth": 1, "material": rim} if rim
                else {"enabled": False, "depth": 1, "material": solid(1)})
    return t


THEMES = {
    # The city is one paved ground, kerbed at every cliff. No field is sampled over it: an
    # octave-2 noise between two blocks of nearly one shade runs eight blocks of a material at a
    # stated scale of 4, which on an 80-block board is blotches of two pavements and reads worse
    # than either block alone (the author's ruling). Every variation the city has is DRAWN — the
    # roads, the pavements, the verges, the station's own checker, the brick of the buildings.
    "stadt": theme(solid(98, 0), solid(98, 0), solid(1, 5),
                   rim=solid(43, 8), depth=3, rim_edges="drop"),
    # the station's concrete: platforms, concourse, the elevated platform. A one-block
    # checker, which at this scale is a tiled floor rather than seven squares across a hall.
    "bahn": theme({"kind": "checker", "size": 1, "even": solid(155, 0),
                   "odd": solid(43, 8)}, solid(43, 8), solid(1, 6),
                  rim=solid(159, 8), depth=2),
    # the ballast under the rails, on the deep tracks and on the deck
    "schotter": theme(solid(13, 0), solid(1, 5), solid(1, 5), depth=2),
    # the planting: turf over two courses of soil, so an avenue tree stands in ground
    "gruen": theme({"kind": "layered", "axis": "depth", "from": 0,
                    "stack": {"bands": [{"material": solid(2, 0), "thickness": 1},
                                        {"material": solid(3, 0), "thickness": 2}],
                              "ending": "repeat"},
                    "beyond": solid(3, 0)}, solid(3, 0), solid(1, 5), depth=3),
}


# ── the dressing ──────────────────────────────────────────────────────────────────────
def house(pid, wings, style, front=None, seed=5):
    p = {"id": pid, "kind": "house", "seed": seed, "style": style,
         "wings": [{"corners": w} for w in wings]}
    if front:
        p["front"] = front
    return p


def tree(pid, x, z, style="platane", seed=11):
    return {"id": pid, "kind": "tree", "seed": seed, "x": x, "z": z, "style": style}


# Six flat-roofed blocks on the grid the avenue and the arterial make, in two rows. The south
# row keeps off the east flank, which is the ground under the elevated monument and the one
# place on this board an objective needs open around it; the north row runs the whole width.
# The signal box is the one building here belonging to the railway rather than to the quarter.
PROPS = [
    # Every block fronts the arterial, which is what keeps six door-marches off each other and
    # off the avenue: a march runs out of a door until it meets something, and a building
    # standing on one is declined by name.
    house("block-s1", [[[-33, 70], [-24, 80]]], "@tk-block", front="posZ"),
    house("block-s2", [[[-20, 70], [-13, 80]]], "@tk-block", front="posZ", seed=7),
    house("block-n1", [[[-33, 91], [-24, 99]]], "@tk-block", front="negZ", seed=9),
    house("block-n2", [[[-20, 91], [-13, 99]]], "@tk-block", front="negZ", seed=11),
    house("block-n3", [[[13, 91], [20, 99]]], "@tk-block", front="negZ", seed=13),
    house("block-n4", [[[24, 91], [33, 99]]], "@tk-block", front="negZ", seed=15),
    house("stellwerk", [[[-34, 32], [-27, 40]]], "@tk-stellwerk", front="posX"),
]
for i, (x, z) in enumerate(((-7, 71), (6, 71), (-7, 76), (6, 76), (-7, 81), (6, 81))):
    PROPS.append(tree(f"allee-{i}", x, z, seed=11 + i))

TREE_STYLE = {"kind": "tree", "form": "template", "species": "oak", "wood": "oak",
              "height": 8, "stems": 1, "leader": 0.55, "flow": 0.45, "branchAngle": 1.1,
              "levels": 2, "whorled": False, "leafSize": 0.6}

FINISH = {
    "authors": ["Opus 5"],
    "created": "2026-09-04",
    "themes": THEMES,
    "mapTheme": "stadt",
    "addShapes": SHAPES,
    "addLayers": LAYERS,
    "roomStyles": {"spawn": "@tk-hochhaus"},
    "dressing": {"props": PROPS, "styles": {"platane": TREE_STYLE}},
}

if __name__ == "__main__":
    with open(f"{HERE}/{BASE}.plan.json", "w") as fh:
        json.dump(PLAN, fh, indent=1)
    with open(f"{HERE}/{BASE}.finish.json", "w") as fh:
        json.dump(FINISH, fh, indent=1)
    print(f"{BASE}.plan.json   {len(PLAN['pieces'])} pieces, {len(PLAN['zones'])} zone")
    print(f"{BASE}.finish.json {len(SHAPES)} shapes on the ground layer, "
          f"{len(LAYERS)} added layers, {len(THEMES)} themes, {len(PROPS)} props")
    materials = sum(1 for s in SHAPES if "material" in s) + \
        sum(1 for e in LAYERS for s in e["shapes"] if "material" in s)
    themed = sum(1 for s in SHAPES if "theme" in s) + \
        sum(1 for e in LAYERS for s in e["shapes"] if "theme" in s)
    print(f"   {themed} shapes carry a theme, {materials} state one material")
    for e in LAYERS:
        print(f"   layer {e['id']:<20} base_y {e['base_y']:>3}  "
              f"{len(e['shapes']):>3} shapes  {e.get('kind','ground')}")
