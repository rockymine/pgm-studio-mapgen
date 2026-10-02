"""Where the showcase's props stand, and the ground they stand on.

The ground's top course is y4, so a prop on it starts at y5. The harbour's water surface is y4, so a boat's
hull starts there. x runs east, z south; `turns` is quarter turns clockwise from the prop's own drawing, in
which a vehicle's nose points east.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                "tools", "sculpt"))
import board                    # noqa: E402
import props as sculpt_props    # noqa: E402  -- tools/sculpt/props.py: LayerBuilder

TOP = 5            # ground occupies y0..y4
WATER = 4          # the harbour's surface course

BOX = (-72, -64, 72, 58)
SPAWN = (0, TOP + 1, 50)
OBSERVER = (0, TOP + 40, 58)

GROUND = {
    "grass": board.shaded(surface=(2, 0), wall=(3, 0), rim=(2, 0)),
    "asphalt": board.solid(1, 5),
    "dash": board.solid(155, 0),
    "kerb": board.solid(43, 8),
    "cobble": board.solid(4, 0),
    "setts": board.solid(98, 0),
    "gravel": board.solid(13, 0),
    "farmland": board.shaded(surface=(60, 7), wall=(3, 0), rim=(60, 7)),
    "water": board.solid(9, 0),
    "sand": board.solid(12, 0),
    "pad": board.solid(155, 0),
    "bed": board.solid(1, 6),
    "dirt": board.solid(3, 1),
}

# Street: north kerb z -36..-34, road -33..-23 (centre line -28), south kerb -22..-20.
NORTH_LANE = -30        # a westbound vehicle's origin row (turned twice, its body runs z -32..-30)
SOUTH_LANE = -26        # an eastbound vehicle's origin row (body z -26..-24)
RAIL_Z = -44

PLACEMENTS = [
    # street — eastbound on the south lane, westbound on the north lane
    ("hatchback", -52, TOP, SOUTH_LANE, 0),
    ("jeep", -36, TOP, SOUTH_LANE, 0),
    ("quad", -22, TOP, SOUTH_LANE, 0),
    ("box-truck", 52, TOP, NORTH_LANE, 2),
    ("bus", 22, TOP, NORTH_LANE, 2),
    ("hatchback", -6, TOP, NORTH_LANE, 2),
    # north kerb
    ("phone-box", -12, TOP, -36, 0),
    ("bus-stop", 13, TOP, -36, 0),
    ("hydrant", 34, TOP, -35, 0),
    ("traffic-light", 2, TOP, -34, 0),
    # south kerb
    ("traffic-light", -2, TOP, -22, 0),
    ("park-bench", -46, TOP, -21, 0),
    ("park-bench", -30, TOP, -21, 0),
    ("ice-cream", -14, TOP, -17, 0),
    # filling station
    ("fuel-pumps", 30, TOP, -15, 0),
    ("double-lamp", 32, TOP, -9, 0),
    ("jeep", 26, TOP, -18, 0),
    # village square
    ("well", -45, TOP, 4, 0),
    ("stall-red", -58, TOP, -6, 0),
    ("stall-blue", -38, TOP, -6, 0),
    ("hand-cart", -61, TOP, 9, 0),
    ("signpost", -45, TOP, 15, 0),
    ("log-bench", -55, TOP, 15, 0),
    ("barrels", -30, TOP, 10, 0),
    ("lantern-post", -64, TOP, -10, 0),
    ("lantern-post", -26, TOP, -10, 2),
    ("lantern-post", -64, TOP, 19, 0),
    ("lantern-post", -26, TOP, 19, 2),
    # farm
    ("tractor", -10, TOP, -9, 0),
    ("hay-wagon", 4, TOP, -11, 0),
    ("scarecrow", -2, TOP, 5, 0),
    # harbour
    ("rowboat", 50, WATER, 13, 0),
    ("canoe", 34, WATER, 18, 0),
    ("canoe", 34, WATER, 21, 0),
    ("fishing-boat", 48, WATER, 24, 0),
    ("crates", 38, TOP, 2, 0),
    ("forklift", 30, TOP, 1, 0),
    # railway
    ("locomotive", -16, TOP, RAIL_Z, 0),
    ("mine-cart", 44, TOP, RAIL_Z, 0),
    # more
    ("pickup", 6, TOP, SOUTH_LANE, 0),
    ("scooter", -9, TOP, -21, 0),
    ("vending", 24, TOP, -36, 0),
    ("sailboat", 56, WATER, 31, 0),
    ("wheelbarrow", 15, TOP, -12, 0),
    ("cannon", -36, TOP, 16, 0),
    ("tent", -36, TOP, 31, 0),
    ("campfire", -28, TOP, 34, 0),
    ("picnic-table", -24, TOP, 29, 0),
    ("log-bench", -31, TOP, 37, 0),
    # airstrip
    ("airplane", -42, TOP, -56, 0),
    ("balloon", 12, TOP, -56, 0),
]

# The street's lamps stand on both kerbs with their arms over the road.
for x in (-60, -40, -20, 0, 20, 40, 60):
    if x != 0:
        PLACEMENTS.append(("street-lamp", x, TOP, -35, 1))
        PLACEMENTS.append(("street-lamp", x + 10, TOP, -21, 3))


def ground_layer():
    layer = sculpt_props.LayerBuilder("ground", name="Ground", mirrors=False)
    x0, z0, x1, z1 = BOX
    layer.rect(x0, z0, x1, z1, 0, TOP, "grass")

    # railway bed, street and kerbs
    layer.rect(x0, RAIL_Z - 2, x1, RAIL_Z + 3, 0, TOP, "bed")
    layer.rect(x0, -36, x1, -33, 0, TOP, "kerb")
    layer.rect(x0, -33, x1, -22, 0, TOP, "asphalt")
    layer.rect(x0, -22, x1, -19, 0, TOP, "kerb")
    for x in range(x0 + 2, x1 - 2, 6):
        layer.rect(x, -28, x + 3, -27, 0, TOP, "dash")

    # filling station forecourt
    layer.rect(22, -19, 42, -6, 0, TOP, "kerb")

    # village square, with a gravel road out to the farm
    layer.rect(-68, -14, -22, 24, 0, TOP, "cobble")
    layer.rect(-50, -1, -39, 10, 0, TOP, "setts")
    layer.rect(-22, -12, 20, -7, 0, TOP, "gravel")

    # the farm: farmland with a water channel every nine rows
    layer.rect(-18, -6, 14, 22, 0, TOP, "farmland")
    for z in (-2, 7, 16):
        layer.rect(-18, z, 14, z + 1, 0, TOP, "water")
    layer.rect(-5, 3, 2, 8, 0, TOP, "dirt")

    # harbour: a sand shore round a pond whose bed is two courses down
    layer.rect(22, -2, 70, 44, 0, TOP, "sand")
    layer.rect(26, 6, 66, 40, 0, TOP - 2, "sand", override=True)

    # airstrip
    layer.rect(-66, -60, -6, -51, 0, TOP, "asphalt")
    for x in range(-62, -10, 6):
        layer.rect(x, -56, x + 3, -55, 0, TOP, "dash")

    # spawn pad
    layer.rect(-6, 46, 7, 55, 0, TOP, "pad")
    return layer.done()


def decor():
    """Blocks that belong to the ground rather than to a prop: rails, crops, water, the pier."""
    out = {}
    # the railway runs the width of the board; a prop on the track takes its own cells
    occupied = set()
    for name, x, _, z, _ in PLACEMENTS:
        if name in ("locomotive", "mine-cart"):
            span = range(x - 4, x + 10) if name == "locomotive" else range(x - 2, x + 11)
            occupied |= {(cx, RAIL_Z) for cx in span}
    for x in range(BOX[0] + 1, BOX[2] - 1):
        if (x, RAIL_Z) not in occupied:
            out[(x, TOP, RAIL_Z)] = (66, 1)

    # wheat on every farmland row, kept off the scarecrow's dirt patch
    for x in range(-18, 14):
        for z in range(-6, 22):
            if z in (-2, 7, 16) or (-5 <= x < 2 and 3 <= z < 8):
                continue
            out[(x, TOP, z)] = (59, 7)

    # the harbour: two courses of water, and a pier on posts
    for x in range(26, 66):
        for z in range(6, 40):
            out[(x, TOP - 2, z)] = (9, 0)
            out[(x, WATER, z)] = (9, 0)
    for x in range(42, 45):
        for z in range(2, 22):
            out[(x, WATER, z)] = (5, 0)
    for z in range(6, 22, 4):
        for x in (41, 45):
            out[(x, TOP - 2, z)] = (17, 0)
            out[(x, WATER, z)] = (17, 0)
            out[(x, TOP, z)] = (85, 0)
    return out


# --- the catalogue: every prop once, alone on a tile ---------------------------------------------------------
CATALOGUE_STEP = 18
CATALOGUE_COLUMNS = 8
CATALOGUE_SPAWN = (0, TOP + 1, -12)


def catalogue(props):
    """`(placements, ground layer, decor)` for a board holding each prop once, on a grid of tiles."""
    layer = sculpt_props.LayerBuilder("ground", name="Ground", mirrors=False)
    placements, water = [], {}
    rows = (len(props) + CATALOGUE_COLUMNS - 1) // CATALOGUE_COLUMNS
    half = CATALOGUE_STEP // 2
    width = CATALOGUE_COLUMNS * CATALOGUE_STEP
    x_start = -width // 2 + half
    layer.rect(-width // 2 - 4, -24, width // 2 + 4, rows * CATALOGUE_STEP + 4, 0, TOP, "grass")
    layer.rect(-8, -18, 8, -6, 0, TOP, "pad")
    for index, prop in enumerate(props):
        cx = x_start + (index % CATALOGUE_COLUMNS) * CATALOGUE_STEP
        cz = half + (index // CATALOGUE_COLUMNS) * CATALOGUE_STEP
        cells = prop.voxels()
        xs = [c[0] for c in cells]
        zs = [c[2] for c in cells]
        ox = cx - (min(xs) + max(xs) + 1) // 2
        oz = cz - (min(zs) + max(zs) + 1) // 2
        boat = prop.theme == "harbour" and prop.name != "crates"
        tile = half - 2
        if boat:
            layer.rect(cx - tile, cz - tile, cx + tile, cz + tile, 0, TOP, "kerb")
            layer.rect(cx - tile + 1, cz - tile + 1, cx + tile - 1, cz + tile - 1, 0, TOP - 2, "sand",
                       override=True)
            for x in range(cx - tile + 1, cx + tile - 1):
                for z in range(cz - tile + 1, cz + tile - 1):
                    water[(x, TOP - 2, z)] = (9, 0)
                    water[(x, WATER, z)] = (9, 0)
        else:
            layer.rect(cx - tile, cz - tile, cx + tile, cz + tile, 0, TOP, "kerb")
        placements.append((prop.name, ox, WATER if boat else TOP, oz, 0))
    return placements, layer.done(), water
