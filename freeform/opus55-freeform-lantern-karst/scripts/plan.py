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

X_MIN, X_MAX = -112, 111
Z_MIN, Z_MAX = -128, 127
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
# Widths, as the author set them: lanes 12 to 16, the Store Road 14 and its two ways in 12, the Long Terrace 14
# and its Arms 10; gaps between steps about 12; the pillar 16 off everything; holes 14 x 16 to 40 x 40.
PIECES = [
    # the front: two legs from the band, wide and short, a bar across them; the void between the legs is 20
    dict(key="leg-w", name="the West Stair", kind="frontline", poly=rect(-28, -26, -11, -12), y=64),
    dict(key="leg-e", name="the East Stair", kind="frontline", poly=rect(10, -26, 27, -12), y=64),
    dict(key="bar", name="the Gate Terrace", kind="frontline", poly=rect(-28, -38, 27, -27), y=65),
    # the hub: a ring of tea terraces round a sinkhole, 12 deep in front and behind, 24 at the sides
    dict(key="hub", name="the Tea Court", kind="hub", poly=rect(-32, -78, 31, -39), y=66,
         hole=rect(-8, -66, 7, -51)),
    # the spawn: three terraces up from the hub, the pavilion on the top one
    # two exits down to the hub, 16 apart, one toward the Pillar and one toward the Store
    dict(key="neck-w", name="the West Lantern Steps", kind="spawn", poly=rect(-20, -86, -9, -79), y=68),
    dict(key="neck-e", name="the East Lantern Steps", kind="spawn", poly=rect(8, -86, 19, -79), y=68),
    dict(key="sp-front", name="the Monument Terrace", kind="spawn", poly=rect(-20, -98, 19, -87), y=70),
    dict(key="sp-mid", name="the Pool Terrace", kind="spawn", poly=rect(-16, -110, 15, -99), y=72),
    dict(key="sp-back", name="the Pavilion of Arrival", kind="spawn", poly=rect(-10, -120, 9, -111), y=74),
    # the Pillar's F: the long stroke out of the hub's west face, two short strokes back from it, ending level
    # with the pillar's far side
    dict(key="f-stem", name="the Long Terrace", kind="lane", poly=rect(-92, -73, -33, -60), y=66),
    dict(key="f-west", name="the Far Arm", kind="approach", poly=rect(-92, -97, -83, -74), y=67),
    dict(key="f-east", name="the Near Arm", kind="approach", poly=rect(-42, -97, -33, -74), y=67),
    dict(key="pillar", name="the Pillar Shrine", kind="wool", poly=rect(-66, -97, -59, -90), y=74),
    # the secret way: two small ledges twenty down in front of the pillar; drop with a water bucket, pillar up
    dict(key="ledge-w", name="the West Ledge", kind="ledge", poly=rect(-75, -82, -70, -76), y=46),
    dict(key="ledge-e", name="the East Ledge", kind="ledge", poly=rect(-55, -82, -50, -76), y=46),
    # the Pillar's flank: a grid of stepping islets, 12 apart, from the band's west end onto the Long Terrace
    dict(key="w-1", name="Mist Step I", kind="islet", poly=rect(-50, -29, -45, -24), y=63),
    dict(key="w-2", name="Mist Step II", kind="islet", poly=rect(-68, -29, -63, -24), y=64),
    dict(key="w-3", name="Mist Step III", kind="islet", poly=rect(-50, -47, -45, -42), y=64),
    dict(key="w-4", name="Mist Step IV", kind="islet", poly=rect(-68, -47, -63, -42), y=65),
    # the Store's F: the long stroke is the road, its two short strokes terraces back to the hub
    dict(key="rows", name="the Tea Rows", kind="lane", poly=rect(32, -50, 49, -39), y=66),
    dict(key="drying", name="the Drying Floor", kind="lane", poly=rect(32, -78, 49, -67), y=67),
    dict(key="road", name="the Store Road", kind="lane", poly=rect(50, -86, 63, -39), y=66, climb=(66, 70, -50, -86)),
    dict(key="store", name="the Tea Store", kind="wool", poly=rect(47, -100, 66, -87), y=70),
    # the Store's flank: two islets from the band's east end, one under the Rows and one under the road's foot
    dict(key="e-1", name="Tea Step I", kind="islet", poly=rect(44, -27, 49, -22), y=64),
    dict(key="e-2", name="Tea Step II", kind="islet", poly=rect(62, -27, 67, -22), y=65),
]

# the middle: the build band across the chasm, and the Bell Rock standing in it
BAND = rect(-57, -11, 56, 10)       # reaches to the middle of each chain of steps, between its two columns
BELL_ROCK = dict(key="bell", name="the Bell Rock", poly=rect(-5, -5, 4, 4), y=68)

# where blocks may be placed over void. Everywhere else the void cannot be built over, at any height.
BUILD_ZONES = [
    dict(key="band", name="the band", poly=BAND),
    dict(key="pit", name="the Pillar's pit", poly=rect(-82, -97, -43, -74)),
    dict(key="w-steps", name="the Mist Steps", poly=rect(-70, -59, -43, -12)),
    dict(key="e-steps", name="the Tea Steps", poly=rect(40, -38, 69, -12)),
]

# a bedrock defence wall: one across the Store Road's last stretch, where its three ways in have met.
# The Pillar has none, since its pit is the line.
WALLS = [dict(wool="store", x0=50, x1=63, z=-82, height=4)]

# the wools (what each team captures is the other team's colour of room: red captures from blue's rooms)
WOOLS = [dict(room="pillar", at=(-62.5, -93.5), y=75, colour="lime", capturer="blue"),
         dict(room="store", at=(56.5, -95.5), y=71, colour="yellow", capturer="blue")]
# the monuments where a team places what it captured: on the Monument Terrace between its two exits
MONUMENTS = [dict(at=(-4, -89), y=70, colour="lime"), dict(at=(3, -89), y=70, colour="yellow")]
SPAWN_POINT = (-0.5, 73, -104.5)

# the spawn's relief, planned now so it is not a flat yard: (what, rect, y of its top)
SPAWN_DETAIL = [
    ("the pavilion: two storeys, its hall open to the Pool Terrace", rect(-8, -119, 7, -112), 84),
    ("the pool, one block deep, a stepping-stone path across it", rect(-13, -108, -6, -102), 71),
    ("the karst outcrop, a rock four high with a pine on it", rect(6, -108, 11, -102), 76),
    ("west lantern tower, the spawn's lookout over the Pillar", rect(-20, -96, -17, -93), 78),
    ("east lantern tower, the lookout over the Store", rect(16, -96, 19, -93), 78),
    ("the tea beds, rows of leaves either side of the monuments", rect(-12, -97, -7, -92), 71),
]

# the secret way has no pool: a player who drops onto a Ledge places a water bucket as they land, or dies

PLACES = [
    dict(name="the Pavilion of Arrival", why="spawn: three terraces up from the hub, a pool, an outcrop, two lantern towers"),
    dict(name="the Tea Court", why="the hub: a ring of tea terraces round a sinkhole; every crossing has a near and a far side"),
    dict(name="the Gate Terrace and its two Stairs", why="the frontline: two wide short legs down to the band, a void between them"),
    dict(name="the Bell Rock", why="the middle: a karst islet in the band, a bell pavilion on it, where the staircases meet"),
    dict(name="the Long Terrace and its two Arms", why="the Pillar's F: a lane out of the hub, two arms back from it"),
    dict(name="the Pillar Shrine", why="WOOL: lime, on a pillar between the Arms, 16 off each and 7 above them"),
    dict(name="the West and East Ledges", why="the secret way: twenty blocks down in front of the pillar; drop, then pillar up"),
    dict(name="the Mist Steps", why="the Pillar's flank: four islets on a grid from the band onto the Long Terrace"),
    dict(name="the Tea Rows, the Drying Floor and the Store Road", why="the Store's F: two ways from the hub onto a short road"),
    dict(name="the Tea Steps", why="the Store's flank: two islets from the band, under the Rows and the road's foot"),
    dict(name="the Tea Store", why="WOOL: yellow, a storehouse at the road's head, two faces on void"),
]
