"""Thawline's ground: heights over the whole board, drawn for the Frost half (z < 0) and carried to the Ember half by
the half turn (x, z) -> (-1 - x, -1 - z), so the two halves are the same ground and only their season differs.

    the field        rising from the rift's lip at 40 to 50 under the spawn, rolling a block or two
    the Glacier      the ridge behind the spawn, 14 to 22 over the field, with two spurs and an icefall between them
    Rimehall         the spawn's terrace, made ground at 53, a face of four toward the field
    the Kettle       a round hollow 7 deep at the core: a glacial kettle hole, the core hung over it
    Hoarcrag         a tor at the west coast beside the Kettle, 60 at its top
    Coldwater        a tarn between the middle and the Kettle
    the Knoll        a low rise in the middle field, five over the ground
    Lantern Green    the monument's terrace, made ground at 48
    Hoarstead        the hamlet's house pads, east of the green, either side of the beck
    the Rime Beck    a stream from the Glacier's foot to the rift, where it falls in
    the Thawline     the rift between the halves, 12 to 14 across, wider round the Stack in its middle

H is the y of the floor block; a player stands at H + 1. LAND is where there is ground; the rift and the sea are
void, and the lava under the rift is laid by the generator, not here.
"""
import numpy as np

from pgmvox.geom import noise, shapes
from pgmvox.geom.noise import smoothstep as ss
from pgmvox.ground import landform as L
from pgmvox.plan.raster import Symmetry

X0, Z0 = -64, -100
NX, NZ = 128, 200
SYM = Symmetry("half")

LIP = 40                      # the field at the rift's lip
SPAWN_Y = 53                  # Rimehall's terrace
GREEN_Y = 48                  # Lantern Green
STACK_Y = 44                  # the Stack's island in the rift
KETTLE_FLOOR = 40

SPAWN = (0, -86)              # the middle of Rimehall's terrace
KETTLE = (-36, -56)           # the core hangs over its middle
GREEN = (31, -55)             # the monument floats over its middle
CRAG = (-55, -64)
TARN = (-20, -37)
KNOLL = (10, -30)
BECK = [(47, -84), (48, -80), (46, -66), (44, -50), (42, -36), (39, -22), (36, -12), (35, -6)]
MORAINE = [(-16, -49), (-6, -45), (6, -43), (18, -44), (26, -48)]
MORAINE_GAP = 22.5            # the Knoll Road's pass through it, in blocks along the line from its west end
MORAINE_RISE = 5.0
DRUMLINS = [(-50, -30, 5, 11, 5, 8), (-44, -15, 4, 8, 3.5, -6), (22, -27, 4.5, 10, 4.5, 10), (-6, -27, 4, 8, 3.5, -4)]
# the hamlet's pads: (centre x, centre z, half x, half z), each a level house plot at the ground's own height
HOUSES = [                    # (key, cx, cz, heading, L, W, door, storeys, name): Hoarstead's houses, Frost's
    ("h1", 53, -56, 0, 9, 6, 1, 2, "the Reeve's House"),
    ("h2", 54, -42, 90, 9, 6, -1, 1, "the Smithy"),
    ("h3", 27, -36, 0, 7, 5, 1, 1, "Beck Cottage"),
    ("h4", 47, -30, 0, 9, 6, -1, 2, "the Mill House"),
]
DOMES = [(51, -21), (28, -26)]                 # an ice house for Frost, a charcoal kiln for Ember
# each house's pad: its footprint and a block round it, level at the ground's median there
PADS = [(cx, cz, (L if h % 180 == 0 else W) // 2 + 1, (W if h % 180 == 0 else L) // 2 + 1)
        for _, cx, cz, h, L, W, _, _, _ in HOUSES] + [(x, z, 4, 4) for x, z in DOMES]

# the roads: polylines a player walks, graded to a gentle grade, and paved by the generator
ROADS = {
    "the Hall Road": [(0, -77), (1, -70), (3, -63)],
    "the Kettle Road": [(3, -63), (-8, -60), (-18, -58), (-25, -57)],
    "the Green Road": [(3, -63), (12, -60), (20, -57)],
    "the Knoll Road": [(3, -63), (5, -52), (8, -42), (8, -36)],
    "the Rift Road": [(8, -24), (4, -16), (0, -11)],
    "the Wood Path": [(-30, -50), (-36, -40), (-40, -28), (-38, -14)],
    "the Beck Lane": [(32, -44), (35, -38), (37, -30), (34, -21), (30, -13)],
    "the Mill Road": [(35, -38), (42, -36), (50, -36)],
    "the Reeve's Walk": [(41, -56), (49, -56)],
    "the Crag Path": [(-46, -44), (-50, -50), (-55, -53), (-58, -58)],
}


def grid():
    return np.meshgrid(np.arange(X0, X0 + NX), np.arange(Z0, Z0 + NZ), indexing="ij")


def symnoise(shape, cell, octaves, seed):
    return SYM.field(noise.fbm(shape, cell, octaves, seed=seed))


def rift_half_width(X):
    """Half the rift's width at each x: 6 to 8 along most of its length, widened round the Stack in the middle so a
    gap of five stays between the Stack's island and either lip."""
    xc = X + 0.5
    wander = 0.9 * np.sin(xc / 9.0) ** 2 + 0.7 * np.cos(xc / 23.0) ** 2           # even in x: the same at -1 - x
    return 6.2 + wander + 4.6 * (1 - ss(9.0, 17.0, np.abs(xc)))


def stack_field(X, Z):
    """The Stack's island: below 1 inside, an ellipse 17 by 11 about the board's middle with a ragged rim."""
    xc, zc = X + 0.5, Z + 0.5
    return np.hypot(xc / 8.5, zc / 5.4) * (1 + 0.08 * symnoise(X.shape, 4, 2, 31))


def land_mask(X, Z):
    """The board's land: a body 124 across at the front narrowing to about 84 behind the spawn, its coast ragged
    by noise, two bays cut into it behind the goals, the rift taken out across its middle and the Stack left
    standing in the rift."""
    zc = np.abs(Z + 0.5)
    half = 61.5 - 21 * ss(58, 100, zc)
    rag = 2.6 * symnoise(X.shape, 9, 3, 11) + 1.2 * symnoise(X.shape, 4, 2, 12)
    body = np.abs(X + 0.5) < half + rag
    bays = np.zeros(X.shape, bool)
    for bx, bz, rx, rz in ((-64, -78, 13, 7), (63, -85, 12, 6)):
        for sx, sz in ((bx, bz), (-1 - bx, -1 - bz)):
            e = np.hypot((X - sx) / rx, (Z - sz) / rz) * (1 + 0.15 * symnoise(X.shape, 5, 2, 13))
            bays |= e < 1
    outline = body & ~bays
    rift = zc < rift_half_width(X) + 0.9 * symnoise(X.shape, 5, 2, 14)
    stack = stack_field(X, Z) < 1
    return outline & (~rift | stack), outline & rift & ~stack, stack


def ground():
    """(X, Z, H, LAND, RIFT, STACK, WET, WATERS, MADE): heights as ints (0 off the land), the masks of the rift, the
    Stack and the water, the waters laid, and the made ground (the terraces) the generator dresses as built."""
    X, Z = grid()
    LAND, RIFT, STACK = land_mask(X, Z)
    n1 = symnoise(X.shape, 26, 3, 3)
    n2 = symnoise(X.shape, 8, 2, 4)
    zf = -Z                                                           # the Frost half drawn; depth from the middle
    H = LIP + 3 * ss(10, 40, zf) + 4 * ss(40, 68, zf) + 3 * ss(68, 84, zf) + 2.6 * n1 + 0.9 * n2
    # the Moraine: the low ridge the glacier left across the middle field, broken where the Knoll Road passes
    d, along = shapes.polyline(X, Z, MORAINE)
    gap = 1 - (1 - ss(2.5, 6.0, np.abs(along - MORAINE_GAP)))
    H = H + MORAINE_RISE * (1 - ss(0.5, 5.5, d + 0.8 * n2)) * gap * (0.85 + 0.25 * n1)
    # the drumlins: long low mounds the ice shaped, lying the way it flowed
    for cx, cz, rx, rz, rise, ang in DRUMLINS:
        e = shapes.ellipse_distance(X, Z, (cx, cz), rx, rz, angle=ang) + 0.06 * n2
        H = L.mound(H, e, rise, power=2.2)
    # the Glacier: a ridge behind the spawn, with two spurs reaching forward either side of the hall
    foot = -90 + noise.line(X.shape, 0, 20, 2, seed=21, amp=2.0)
    rough = 4 * noise.fbm(X.shape, 10, 3, seed=22)
    spur_w = shapes.polyline(X, Z, [(-30, -100), (-24, -88), (-20, -82)])[0]
    spur_e = shapes.polyline(X, Z, [(30, -100), (25, -89), (22, -84)])[0]
    H = L.ridge(H, Z, foot, 8, 68 + 3 * n1, rough=rough,
                spurs=[(spur_w, 60 + 2 * n2, (7, 2.5)), (spur_e, 59 + 2 * n2, (7, 2.5))])
    # the back corners climb with the coast, so the hall sits in a bowl of ice open to the south
    corner = ss(70, 98, zf) * ss(22, 40, np.abs(X + 0.5))
    H = H + 9 * corner * (0.8 + 0.3 * n1)
    # Hoarcrag: a tor at the coast, 60 at its top, its talus running into the field
    H = L.butte(H, X, Z, CRAG, 6.5, 60, cliff=1.6, talus=7, talus_height=0.35, jag=0.18, seed=5, rz=8.5, angle=20)
    # the Knoll: a low rise in the middle field
    e = shapes.ellipse_distance(X, Z, KNOLL, 12, 8, angle=-15) + 0.08 * n2
    H = L.mound(H, e, 5, power=1.8)
    # the Kettle: the ring round it lifted a block, then the hollow cut, a floor of 40 out to 4 and walls of one
    e = np.hypot(X + 0.5 - KETTLE[0] - 0.5, Z + 0.5 - KETTLE[1] - 0.5)
    ring = 1.0 - ss(8, 13, e)
    H = H + 1.2 * ring * ss(5, 8, e)
    H = L.crater(H, e + 0.5 * n2, KETTLE_FLOOR, 12, flat=4.5, slope=1.0)
    # the terraces: made ground, level, met by a face (the generator dresses each face as a wall)
    made = np.zeros(X.shape, bool)
    e_hall = np.hypot((X + 0.5 - SPAWN[0]) / 17.0, (Z + 0.5 - SPAWN[1]) / 7.5)
    hall = e_hall < 1
    H = np.where(hall, SPAWN_Y, H)
    made |= hall
    e_green = np.hypot(X + 0.5 - GREEN[0] - 0.5, Z + 0.5 - GREEN[1] - 0.5) + 0.6 * n2
    green = e_green < 9.5
    H = np.where(green, GREEN_Y, H)
    made |= green
    # the hamlet's pads: each held level at its own median, eased back over three
    for cx, cz, hx, hz in PADS:
        e = np.maximum(np.abs(X - cx) / (hx + 0.5), np.abs(Z - cz) / (hz + 0.5))
        H = L.level(H, e, top="median", inner=1.0, outer=1.5)
    # the roads, graded so none climbs more than one in four
    roads = np.zeros(X.shape, bool)
    for name, pts in ROADS.items():
        H, _ = L.grade(H, X, Z, pts, width=4 if name != "the Crag Path" else 3,
                       max_grade=0.25 if name != "the Crag Path" else 0.8, shoulder=3, keep=made | roads)
        roads |= shapes.polyline(X, Z, pts)[0] <= 2
    # the waters
    waters = []
    H, tarn = L.lake(H, X, Z, TARN, 7.5, int(np.round(H[TARN[0] - X0, TARN[1] - Z0])) - 1, depth=3, shore=3,
                     rz=5.5, jag=0.22, seed=41)
    waters.append(tarn)
    H, beck = L.watercourse(H, X, Z, BECK, width=3, depth=2, bank=3, fall_min=2, reach_min=9, lowest=LIP - 3)
    waters.append(beck)
    H = L.hold(H, *waters)
    # the Stack's island: level at its top, a dome a block higher in its middle
    H = np.where(STACK, STACK_Y + (stack_field(X, Z) < 0.55), H)
    keep = Z < 0
    H = SYM.field(H, keep=keep)
    waters = [L.Water(SYM.field(w_.mask, keep=keep), SYM.field(w_.surface, keep=keep), w_.falls or []) for w_ in waters]
    made = SYM.field(made, keep=keep)
    H = np.where(LAND, np.round(H), 0).astype(int)
    wet = np.zeros(H.shape, bool)
    for wat in waters:
        wet |= wat.mask
    wet &= LAND
    return X, Z, H, LAND, RIFT, STACK, wet, waters, made
