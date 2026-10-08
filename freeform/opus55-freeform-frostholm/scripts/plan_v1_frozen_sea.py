"""Frostholm's plan: an archipelago in a frozen sea, played corner to corner. Red holds the north-west, blue
the south-east; blue's half is red's turned half a circle about the centre, (x, z) -> (-1 - x, -1 - z).
The two halves meet along the diagonal x + z = -1, where a lead of open water runs between the teams and
three islands stand astride it.

Coordinates are world x, z (north is -z). Heights are the ground a player stands on.
"""
X_MIN, X_MAX = -90, 89
Z_MIN, Z_MAX = -90, 89
SEA_ICE_Y = 47            # the top of the sea ice; a player on the ice stands at 48
SEA_FLOOR = 30
BAND = 112             # the board is the band |x - z| < BAND: the corners off the diagonal are cut away
LAKE_Y = 57               # Kaldvatn, held high in the south-west horn


def rot(x, z):
    return -1 - x, -1 - z


def red_half(x, z):
    """The cells red's scripts author; blue's are their half-turn."""
    s = x + z
    return s < -1 or (s == -1 and x <= -1)


# ---- the land ------------------------------------------------------------------------------------
# Red's home island, Nordholm: a crescent round its bay, its back in the north-west corner. The spine runs
# from the north-east horn round the corner to the south-west horn; the width is the island's half-width.
SPINE = [(-3, -72, 7), (-20, -75, 10), (-40, -73, 13), (-56, -66, 19), (-63, -63, 22), (-66, -56, 19),
         (-73, -40, 15), (-75, -22, 13), (-72, -4, 8)]
ISLANDS = [  # other islands red authors (centre, radii x/z, peak height over the ice)
    dict(key="tingholm", at=(-0.5, -0.5), r=(19, 19), peak=10),        # astride the seam at the centre
    dict(key="kraakholm", at=(36, -37), r=(17, 13), peak=13),         # astride the seam, north-east
    dict(key="skerry_n", at=(16, -54), r=(6, 4), peak=4),
    dict(key="skerry_w", at=(-50, 20), r=(4, 6), peak=5),
    dict(key="skerry_bay", at=(-24, -22), r=(4, 3), peak=3),
]

# ---- objectives ------------------------------------------------------------------------------------
SPAWN = (-62, 64, -62)                 # Jarlshall's floor
BEACON = (5, -79)                      # the lighthouse on its stack off the north-east horn; the core in its lantern
CORE_Y = 82                            # the core's lowest course
MONUMENT = (-68, -24)                  # on the islet in Kaldvatn

PLACES = [
    dict(key="hall", name="Jarlshall", at=(-62, -62), r=8,
         what="Red's spawn: a long hall of dark timber on a stone plinth, crags at its back in the corner",
         why="spawn; its doors look down the island to the bay", how="the hall's two doors"),
    dict(key="crags", name="Ulvefjell", at=(-74, -74), r=10,
         what="the island's crags, 30 blocks over the ice, snow on their ledges", why="frames the spawn; a high lookout",
         how="a goat path from the hall"),
    dict(key="beacon", name="The Beacon", at=BEACON, r=6,
         what="a stone lighthouse on a sea stack off the north-east horn; the core burns in its lantern",
         why="RED CORE", how="its stair; the stone footbridge from the horn; the sea cave in the stack's foot"),
    dict(key="horn_ne", name="Ravnsodde", at=(-18, -75), r=9,
         what="the north-east horn: a bare rock ridge running out to the Beacon", why="the way to the core, and its guard",
         how="the ridge path from the hall"),
    dict(key="lake", name="Kaldvatn", at=MONUMENT, r=11,
         what="a frozen lake held high in the south-west horn, a frozen fall pouring from its lip into the bay",
         why="RED MONUMENT on its islet, Holmstein", how="across the lake ice; from the pine wood; from the crag above"),
    dict(key="wood", name="Granskog", at=(-74, -44), r=9,
         what="pine and spruce in the valley between the hall and the lake", why="cover from the hall to the monument",
         how="the wood path"),
    dict(key="village", name="Skarvik", at=(-46, -46), r=12,
         what="a fishing village on the bay's shore: boathouses, drying racks, a stave church, the smithy, longhouses",
         why="cover the whole way from the bay to the hall; fought through", how="the shore road; the pier"),
    dict(key="whaler", name="The Whaler", at=(-26, -36), r=7,
         what="a three-masted ship frozen into the bay ice, listing", why="cover and height in the middle of the open bay",
         how="over the ice"),
    dict(key="tingholm", name="Tingholm", at=(-0.5, -0.5), r=19,
         what="the centre island: a ring of standing stones on a low rise, a cairn", why="the middle crossing of the lead",
         how="over the ice from both bays"),
    dict(key="kraakholm", name="Kraakholm", at=(36, -37), r=16,
         what="a rocky island astride the lead: a ruined watchtower on red's side, a sealers' hut on blue's",
         why="the crossing between red's core and blue's monument", how="over the ice; across the lead"),
    dict(key="ridges", name="The Pressure Ridges", at=(-14, -48), r=8,
         what="ridges of broken ice heaved up across the sea ice", why="the only cover on the open ice", how="—"),
]

ROUTES = [
    dict(name="Ridge Path", kind="path", pts=[(-56, -66), (-42, -72), (-26, -75), (-12, -74), (-4, -73)]),
    dict(name="Lake Path", kind="path", pts=[(-66, -56), (-72, -44), (-72, -34), (-70, -28)]),
    dict(name="Shore Road", kind="road", pts=[(-58, -58), (-50, -50), (-42, -44)]),
    dict(name="Bay Road", kind="road", pts=[(-62, -54), (-64, -40), (-62, -28)]),
    dict(name="Village Lane", kind="road", pts=[(-54, -56), (-44, -60), (-34, -64)]),
]
