"""Lantern Karst — a capture-the-wool plan, drawn in polygons. Second version, after the author's review.

Karst pillars stand in a void of mist. On them, tea terraces, pavilions and lanterns; between the two teams a
chasm crossed only by building. Each team defends two wools, both reached two ways:

  the Pillar Shrine — the wool on a karst pillar floating between the two legs of an F. The F's long stroke
      is the lane out of the hub; its two short strokes run back from it; the pillar stands in the pit between
      them, thirteen blocks off each. Bridged to from either leg or from the lane, and from a grid of
      stepping islets that climb from the band's west end onto the lane.
  the Tea Store — the wool in a storehouse at the head of a short road. The road is the long stroke of an F
      whose two short strokes reach back to the hub: the south one terrace, the north one a gap the players
      build. A grid of islets from the band's east end reaches the road's foot. Three ways onto the road,
      one bedrock wall across its last stretch.

Red holds the north (z < 0), blue the south; blue's half is red's turned half a circle about the centre,
(x, z) -> (-1 - x, -1 - z). So on each side of the board one team's Pillar faces the other team's Tea Store.

A piece is a polygon of land at a height. A build zone is a polygon where blocks may be placed over void.
Every column a player may build in (land or build zone) is marked by block 36 at y 0, which is what PGM's
void filter reads; every island stands on a bedrock course FOUNDATION_DEPTH below its floor, so a pit dug
into it stops there.
"""

X_MIN, X_MAX = -96, 95
Z_MIN, Z_MAX = -112, 111
BASE_Y = 64
KILL_Y = 40                 # below this a fall kills; the mist lies under it
MIST_Y = (28, 38)
MAX_BUILD = 92              # the late game's ceiling: 28 over the base, room for the sky network
FOUNDATION_DEPTH = 6        # the bedrock course under every island, this far below its floor
MARKER_Y = 0                # block 36 here under every buildable column


def rot(x, z):
    return -1 - x, -1 - z


def rect(x0, z0, x1, z1):
    """A rectangle of whole blocks, x0..x1 by z0..z1 inclusive, as a polygon on block edges."""
    return [(x0 - 0.5, z0 - 0.5), (x1 + 0.5, z0 - 0.5), (x1 + 0.5, z1 + 0.5), (x0 - 0.5, z1 + 0.5)]


# ---- pieces: (key, name, kind, polygon, floor y) ----------------------------------------------------------
PIECES = [
    # the front: two legs from the band, wide and short, a bar across them; the void between the legs is 20
    dict(key="leg-w", name="the West Stair", kind="frontline", poly=rect(-28, -22, -11, -12), y=64),
    dict(key="leg-e", name="the East Stair", kind="frontline", poly=rect(10, -22, 27, -12), y=64),
    dict(key="bar", name="the Gate Terrace", kind="frontline", poly=rect(-28, -32, 27, -23), y=65),
    # the hub: a ring of tea terraces round a sinkhole, so every crossing has a near side and a far side
    dict(key="hub", name="the Tea Court", kind="hub", poly=rect(-30, -64, 29, -33), y=66,
         hole=rect(-8, -56, 7, -43)),
    # the spawn: three terraces up from the hub, the pavilion on the top one
    dict(key="neck", name="the Lantern Steps", kind="spawn", poly=rect(-5, -72, 4, -65), y=68),
    dict(key="sp-front", name="the Monument Terrace", kind="spawn", poly=rect(-18, -82, 17, -73), y=70),
    dict(key="sp-mid", name="the Pool Terrace", kind="spawn", poly=rect(-14, -92, 13, -83), y=72),
    dict(key="sp-back", name="the Pavilion of Arrival", kind="spawn", poly=rect(-9, -100, 8, -93), y=74),
    # the Pillar's F: the long stroke out of the hub's west face, two short strokes back from it
    dict(key="f-stem", name="the Long Terrace", kind="lane", poly=rect(-76, -52, -31, -43), y=66),
    dict(key="f-west", name="the Far Arm", kind="approach", poly=rect(-76, -84, -71, -53), y=67),
    dict(key="f-east", name="the Near Arm", kind="approach", poly=rect(-36, -84, -31, -53), y=67),
    dict(key="pillar", name="the Pillar Shrine", kind="wool", poly=rect(-57, -78, -50, -71), y=74),
    # the Pillar's flank: a grid of stepping islets from the band's west end up onto the Long Terrace
    dict(key="w-1", name="Mist Step I", kind="islet", poly=rect(-48, -24, -43, -19), y=63),
    dict(key="w-2", name="Mist Step II", kind="islet", poly=rect(-60, -24, -55, -19), y=64),
    dict(key="w-3", name="Mist Step III", kind="islet", poly=rect(-48, -36, -43, -31), y=64),
    dict(key="w-4", name="Mist Step IV", kind="islet", poly=rect(-60, -36, -55, -31), y=65),
    # the Store's F: the long stroke is the road, its south short stroke a terrace back to the hub
    dict(key="rows", name="the Tea Rows", kind="lane", poly=rect(30, -40, 47, -33), y=66),
    dict(key="drying", name="the Drying Floor", kind="lane", poly=rect(30, -64, 47, -57), y=67),
    dict(key="road", name="the Store Road", kind="lane", poly=rect(48, -72, 57, -30), y=66, climb=(66, 70, -52, -72)),
    dict(key="store", name="the Tea Store", kind="wool", poly=rect(45, -85, 60, -73), y=70),
    # the Store's flank: two islets from the band's east end to the road's foot
    dict(key="e-1", name="Tea Step I", kind="islet", poly=rect(41, -23, 46, -18), y=64),
    dict(key="e-2", name="Tea Step II", kind="islet", poly=rect(53, -23, 58, -18), y=65),
]

# the middle: the build band across the chasm, and the Bell Rock standing in it
BAND = rect(-40, -11, 39, 10)
BELL_ROCK = dict(key="bell", name="the Bell Rock", poly=rect(-5, -5, 4, 4), y=68)

# where blocks may be placed over void. Everywhere else the void cannot be built over, at any height.
BUILD_ZONES = [
    dict(key="band", name="the band", poly=BAND),
    dict(key="pit", name="the Pillar's pit", poly=rect(-70, -92, -37, -53)),
    dict(key="w-steps", name="the Mist Steps", poly=rect(-62, -42, -41, -12)),
    dict(key="e-steps", name="the Tea Steps", poly=rect(40, -29, 59, -12)),
]

# a bedrock defence wall: one across the Store Road's last stretch, where its three ways in have met.
# The Pillar has none, since its pit is the line.
WALLS = [dict(wool="store", x0=48, x1=57, z=-68, height=4)]

# the wools (what each team captures is the other team's colour of room: red captures from blue's rooms)
WOOLS = [dict(room="pillar", at=(-53.5, -74.5), y=75, colour="lime", capturer="blue"),
         dict(room="store", at=(52.5, -81.5), y=71, colour="yellow", capturer="blue")]
# the monuments where a team places what it captured: on the Monument Terrace either side of the steps
MONUMENTS = [dict(at=(-10, -76), y=70, colour="lime"), dict(at=(9, -76), y=70, colour="yellow")]
SPAWN_POINT = (-0.5, 73, -88.5)

# the spawn's relief, planned now so it is not a flat yard: (what, rect, y of its top)
SPAWN_DETAIL = [
    ("the pavilion: two storeys, its hall open to the Pool Terrace", rect(-7, -99, 6, -94), 84),
    ("the pool, one block deep, a stepping-stone path across it", rect(-11, -90, -4, -85), 71),
    ("the karst outcrop, a rock four high with a pine on it", rect(6, -91, 11, -86), 76),
    ("west lantern tower, the spawn's lookout over the Pillar", rect(-18, -80, -15, -77), 78),
    ("east lantern tower, the lookout over the Store", rect(14, -80, 17, -77), 78),
    ("the tea beds, rows of leaves on both sides of the steps", rect(-14, -82, -7, -80), 71),
]

PLACES = [
    dict(name="the Pavilion of Arrival", why="spawn: three terraces up from the hub, a pool, an outcrop, two lantern towers"),
    dict(name="the Tea Court", why="the hub: a ring of tea terraces round a sinkhole; every crossing has a near and a far side"),
    dict(name="the Gate Terrace and its two Stairs", why="the frontline: two wide short legs down to the band, a void between them"),
    dict(name="the Bell Rock", why="the middle: a karst islet in the band, a bell pavilion on it, where the staircases meet"),
    dict(name="the Long Terrace and its two Arms", why="the Pillar's F: a lane out of the hub, two arms back from it"),
    dict(name="the Pillar Shrine", why="WOOL: lime, on a pillar between the Arms, 13 off each and 7 above them"),
    dict(name="the Mist Steps", why="the Pillar's flank: four islets on a grid from the band onto the Long Terrace"),
    dict(name="the Tea Rows, the Drying Floor and the Store Road", why="the Store's F: two ways from the hub onto a short road"),
    dict(name="the Tea Steps", why="the Store's flank: two islets from the band to the road's foot"),
    dict(name="the Tea Store", why="WOOL: yellow, a storehouse at the road's head, two faces on void"),
]
