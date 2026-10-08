"""Lantern Karst — a capture-the-wool plan, drawn in polygons.

Karst pillars stand in a void of mist. On them, tea terraces, pavilions and lanterns; between the two teams a
chasm crossed only by building. Each team defends two wools, and the two are built to opposite ideas of what a
wool room is:

  the Pillar Shrine — the wool on top of a karst pillar standing alone in a pit of void, with a horseshoe of
      terrace round three sides of it, thirteen blocks off. It is approached from any point of the horseshoe,
      and from a chain of islets along the board's edge, always by building over the void and up eight blocks
      onto a defended top. Many ways in; every one of them exposed.
  the Tea Store — the wool in a stone storehouse at the dead end of a long terraced lane, in a corner with two
      faces on void, behind a bedrock defence wall across the lane. One way in, held at a line.

Red holds the north (z < 0), blue the south; blue's half is red's turned half a circle about the centre,
(x, z) -> (-1 - x, -1 - z). So on each side of the board one team's Pillar faces the other team's Tea Store.

A piece is a polygon of land at a height. A build zone is a polygon where blocks may be placed over void.
"""

X_MIN, X_MAX = -96, 95
Z_MIN, Z_MAX = -112, 111
BASE_Y = 64
KILL_Y = 40                 # below this a fall kills; the mist lies under it
MIST_Y = (28, 38)
MAX_BUILD = 92              # the late game's ceiling: 28 over the base, room for the sky network


def rot(x, z):
    return -1 - x, -1 - z


def rect(x0, z0, x1, z1):
    """A rectangle of whole blocks, x0..x1 by z0..z1 inclusive, as a polygon on block edges."""
    return [(x0 - 0.5, z0 - 0.5), (x1 + 0.5, z0 - 0.5), (x1 + 0.5, z1 + 0.5), (x0 - 0.5, z1 + 0.5)]


# ---- pieces: (key, name, kind, polygon, floor y) ----------------------------------------------------------
PIECES = [
    # the front: two legs from the band, a bar across them; the void between the legs is 24 across
    dict(key="leg-w", name="the West Stair", kind="frontline", poly=rect(-24, -30, -13, -12), y=64),
    dict(key="leg-e", name="the East Stair", kind="frontline", poly=rect(12, -30, 23, -12), y=64),
    dict(key="bar", name="the Gate Terrace", kind="frontline", poly=rect(-24, -40, 23, -31), y=65),
    # the hub: a ring of tea terraces round a sinkhole, so every crossing has a near side and a far side
    dict(key="hub", name="the Tea Court", kind="hub", poly=rect(-26, -72, 25, -41), y=66,
         hole=rect(-8, -62, 7, -51)),
    # the spawn: behind the hub on a neck, one door
    dict(key="neck", name="the Lantern Steps", kind="spawn", poly=rect(-6, -80, 5, -73), y=68),
    dict(key="spawn", name="the Pavilion of Arrival", kind="spawn", poly=rect(-14, -100, 13, -81), y=70),
    # the west lane to the Pillar: out of the hub's west face, a terrace ten wide
    dict(key="lane-w", name="the Long Terrace", kind="lane", poly=rect(-62, -63, -27, -54), y=66),
    dict(key="lane-w2", name="the Turn", kind="lane", poly=rect(-62, -66, -53, -64), y=66),
    # the horseshoe round the pit: south, west and east arms; open to the north
    dict(key="shoe-s", name="the Horseshoe", kind="approach", poly=rect(-79, -73, -33, -67), y=66),
    dict(key="shoe-w", name="the Horseshoe (west arm)", kind="approach", poly=rect(-79, -106, -73, -74), y=66),
    dict(key="shoe-e", name="the Horseshoe (east arm)", kind="approach", poly=rect(-39, -106, -33, -74), y=66),
    dict(key="pillar", name="the Pillar Shrine", kind="wool", poly=rect(-59, -94, -52, -87), y=74),
    # the east lane to the Tea Store: out of the hub's east face, then north, climbing a block every six
    dict(key="lane-e", name="the Tea Rows", kind="lane", poly=rect(26, -56, 50, -47), y=66, climb=(66, 68)),
    dict(key="lane-e2", name="the Store Road", kind="lane", poly=rect(41, -90, 50, -57), y=68, climb=(68, 70)),
    dict(key="store", name="the Tea Store", kind="wool", poly=rect(39, -103, 52, -91), y=70),
    # the flank: a chain of karst islets along the west edge, from the band's end up to the Horseshoe's west arm
    dict(key="islet-1", name="Mist Step I", kind="islet", poly=rect(-62, -22, -56, -16), y=62),
    dict(key="islet-2", name="Mist Step II", kind="islet", poly=rect(-74, -36, -68, -30), y=63),
    dict(key="islet-3", name="Mist Step III", kind="islet", poly=rect(-84, -50, -78, -44), y=64),
    dict(key="islet-4", name="Mist Step IV", kind="islet", poly=rect(-84, -61, -79, -56), y=65),
]

# the middle: the build band across the chasm, and the Bell Rock standing in it
BAND = rect(-40, -11, 39, 10)
BELL_ROCK = dict(key="bell", name="the Bell Rock", poly=rect(-5, -5, 4, 4), y=68)

# where blocks may be placed over void: the band; the Pillar's pit (to build to the Pillar from the Horseshoe);
# the gaps of the islet chain. Everywhere else the void cannot be built over, at any height.
BUILD_ZONES = [
    dict(key="band", poly=BAND),
    dict(key="pit", poly=rect(-72, -106, -40, -74)),
    dict(key="flank", poly=[(-56, -12), (-40, -12), (-62, -30), (-80, -44), (-86, -55), (-86, -66), (-77, -66),
                            (-78, -55), (-76, -44), (-66, -30), (-62, -24)]),
]

# a bedrock defence wall: one per wool approach that has a line to hold. The Tea Store's is across its road;
# the Pillar has none, since its pit is the line.
WALLS = [dict(wool="store", x0=41, x1=50, z=-83, height=4)]

# the wools (what each team captures is the other team's colour of room: red captures from blue's rooms)
WOOLS = [dict(room="pillar", at=(-55.5, -90.5), y=75, colour="lime", capturer="blue"),
         dict(room="store", at=(45.5, -99.5), y=71, colour="yellow", capturer="blue")]
# the monuments where a team places what it captured: on its own spawn's front terrace, either side of the steps
MONUMENTS = [dict(at=(-10, -84), y=70, colour="lime"), dict(at=(9, -84), y=70, colour="yellow")]
SPAWN_POINT = (-0.5, 71, -92.5)

PLACES = [
    dict(name="the Pavilion of Arrival", why="spawn: a two-storey hall on its own terrace, the monuments either side of its steps"),
    dict(name="the Tea Court", why="the hub: a ring of tea terraces round a sinkhole; every crossing has a near and a far side"),
    dict(name="the Gate Terrace and its two Stairs", why="the frontline: two legs down to the band, a void between them"),
    dict(name="the Bell Rock", why="the middle: a karst islet in the band, a bell pavilion on it, where the staircases meet"),
    dict(name="the Long Terrace and the Horseshoe", why="the Pillar's approach: a lane out to a horseshoe of terrace round a pit"),
    dict(name="the Pillar Shrine", why="WOOL: lime, on a pillar 13 blocks off the Horseshoe and 8 above it"),
    dict(name="the Mist Steps", why="the flank: four islets up the west edge to the Horseshoe's far arm"),
    dict(name="the Tea Rows and the Store Road", why="the Store's approach: a terraced lane climbing four blocks, a wall across it"),
    dict(name="the Tea Store", why="WOOL: yellow, a storehouse in the lane's corner, two faces on void"),
]
