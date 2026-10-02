"""Halcyon Cays: a tropical atoll resort, one monument a team, joined by sandbars rather than by a build zone.

Writes <slug>.plan.json and <slug>.refinement.json beside itself, every document stated through the kit.
Team 0 stands at z < 0; the image of block z is -z-1 (mirror_z), so everything stated here is stated once.
"""
import json
import math
import os
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from studio_kit import kit  # noqa: E402

SLUG = "sonnet55-halcyon-cays"

# --------------------------------------------------------------------------------------------------------------
# Levels. A mark's h is the surface height it states, the top block standing one under it.
# --------------------------------------------------------------------------------------------------------------
BIOME = 6           # 21 Jungle, 6 Swampland
SEABED = 7          # lagoon floor, top block y6
WATER = 10          # the line the lagoon stands at
FORD = 10           # reef flats and fords: top block y9, one block of water over them
BEACH = 12          # dry sand, top block y11
ISLAND = 14         # jungle crown, top block y13


# --------------------------------------------------------------------------------------------------------------
# Geometry helpers: organic rings stated as points, so a spec re-driven draws the same coast.
# --------------------------------------------------------------------------------------------------------------
def blob(cx, cz, rx, rz, seed=0, wobble=0.12, n=24, turn=0.0):
    """An ellipse pulled in and out by two low harmonics, deterministic in the seed."""
    p1, p2 = seed * 1.7, seed * 2.9
    points = []
    for k in range(n):
        t = 2 * math.pi * k / n
        r = 1 + wobble * (math.sin(3 * t + p1) + 0.6 * math.sin(5 * t + p2))
        x, z = rx * r * math.cos(t), rz * r * math.sin(t)
        c, s = math.cos(math.radians(turn)), math.sin(math.radians(turn))
        points.append([round(cx + x * c - z * s, 1), round(cz + x * s + z * c, 1)])
    return points


def smooth(points, samples=6):
    """Centripetal-ish Catmull-Rom through the points, so a corridor bends the way a polyline shape does."""
    out = []
    pts = [points[0]] + points + [points[-1]]
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for s in range(samples):
            t = s / samples
            t2, t3 = t * t, t * t * t
            out.append([0.5 * ((2 * p1[a]) + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t2
                               + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t3) for a in (0, 1)])
    out.append(list(points[-1]))
    return out


def corridor(points, width, widths=None):
    """The polygon a centreline sweeps out at `width` blocks (or per-point `widths`), smoothed."""
    centre = smooth(points)
    n = len(centre)
    half = []
    for i in range(n):
        w = width if widths is None else widths[min(len(widths) - 1, int(i * len(widths) / n))]
        half.append(w / 2)
    left, right = [], []
    for i in range(n):
        a = centre[max(0, i - 1)]
        b = centre[min(n - 1, i + 1)]
        dx, dz = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dz) or 1
        nx, nz = -dz / length, dx / length
        left.append([round(centre[i][0] + nx * half[i], 1), round(centre[i][1] + nz * half[i], 1)])
        right.append([round(centre[i][0] - nx * half[i], 1), round(centre[i][1] - nz * half[i], 1)])
    return left + right[::-1]


def rect_ring(x0, z0, x1, z1):
    return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]


# --------------------------------------------------------------------------------------------------------------
# The plan: the arrangement and nothing else. One ground piece and a spawn piece; the lagoon is the relief's.
# --------------------------------------------------------------------------------------------------------------
def plan():
    return kit.PlanModel(
        plan=2,
        meta=kit.PlanMeta(name="Halcyon Cays", authors=["Sonnet 5.5"]),
        globals=kit.PlanGlobals(cell=5, symmetry="mirror_z", maxPlayers=12, surface=9),
        pieces=[kit.PlanPiece(id="ground", role="piece", rect=[-10, -17, 20, 17]),
                kit.PlanPiece(id="spawn", role="spawn", rect=[-2, -21, 4, 4])],
        placements=kit.PlanPlacements(
            spawns=[kit.SpawnPlacement(id="spawn-1", piece="spawn", at=[10, 10], facing="back",
                                       footprint=[2, 2, 16, 16])],
            destroyables=[kit.DestroyablePlacement(id="monument-1", piece="ground", at=[58, 32],
                                                   style="pillar-3", materials="obsidian", float=4)]))


# --------------------------------------------------------------------------------------------------------------
# Relief: one group, `team`. The lagoon floor is pinned, the cays and bars are pads that give way to it.
# --------------------------------------------------------------------------------------------------------------
SPIT = [[-2, -47], [6, -38], [3, -29], [-4, -21], [-1, -12], [1, -4]]
EAST_REEF = [[34, -58], [38, -44], [32, -31], [26, -19], [17, -9], [7, -3]]


def mark(mark_id, ring, h, bevel=0, **words):
    return kit.ReliefMarkJson(id=mark_id, kind="area", ring=ring, h=h, bevel=bevel, **words)


def cay(mark_id, cx, cz, dry_rx, dry_rz, h, bevel, seed, wobble=0.1):
    """A pad whose dry core is dry_rx x dry_rz: the ring is drawn a bevel wider, since the bevel is paid from the ring."""
    return mark(mark_id, blob(cx, cz, dry_rx + bevel, dry_rz + bevel, seed=seed, wobble=wobble), h, bevel)


def relief():
    marks = [
        mark("lagoon-floor", rect_ring(-49, -104, 49, 1), SEABED),
        cay("hotel-cay", -10, -64, 28, 18, BEACH, 7, 1),
        cay("spawn-cay", 0, -95, 8.5, 8.5, BEACH, 3, 2, 0.03),
        mark("neck", corridor([[0, -90], [-1, -80], [-3, -72]], 20 + 2 * 3), BEACH, 3),
        cay("palm-cay", 37, -70, 13, 10, BEACH, 6, 4),
        mark("spit", corridor(SPIT, 8 + 2 * 5), BEACH, 5),
        cay("bar-cay", 0, -1, 11, 6, BEACH, 4, 5, 0.06),
        mark("east-reef", corridor(EAST_REEF, 12 + 2 * 4), FORD, 4),
        cay("lifeguard-bar", 11, -33, 3.5, 3.5, BEACH, 3, 11, 0.05),
        cay("reef-cay", 28, -27, 5, 4, BEACH, 4, 12),
        cay("reef-islet", 21, -13, 4, 3, BEACH, 3, 13),
        cay("tern-i", -38, -40, 6, 4.5, BEACH, 5, 6),
        cay("tern-ii", -31, -23, 5.5, 4, BEACH, 5, 7),
        cay("tern-iii", -20, -8, 6, 3.5, BEACH, 4, 8),
    ]
    pushes = [
        kit.ReliefPushJson(id="garden-hill", ring=blob(4, -68, 6, 4, seed=9), amount=2, falloff=5, crown=1.5,
                           roughness=0, seed=1),
    ]
    return {"team": kit.SketchReliefJson(base=SEABED, reach=0, step=1, marks=marks, pushes=pushes)}


# --------------------------------------------------------------------------------------------------------------
# Paint: three themes, each a place.
# --------------------------------------------------------------------------------------------------------------
def solid(block, data=0):
    return kit.SolidMaterial(id=block, data=data)


def cells(palette, size=3, seed=1, rise=0, warp=1, jitter=60):
    return kit.CellMaterial(seed=seed, cellSize=size, jitter=jitter, warp=warp, palette=palette, rise=rise)


def depth_stack(*bands, ending="repeat"):
    return kit.LayeredMaterial(axis="depth", stack=kit.BandStack(
        bands=[kit.Band(material=m, thickness=t) for m, t in bands], ending=ending))


def slope_stack(*bands):
    return kit.LayeredMaterial(axis="slope", stack=kit.BandStack(
        bands=[kit.Band(material=m, thickness=t) for m, t in bands], ending="repeat"))


SAND = [solid(12), solid(12), solid(24, 0), solid(24, 2)]             # sand, sand, sandstone, smooth sandstone
SANDSTONE = [solid(24, 0), solid(24, 0), solid(24, 2), solid(12)]
GRASS = solid(2)
DIRT_MIX = [solid(3, 0), solid(3, 1), solid(3, 0), solid(3, 1)]
ROCK = [solid(1, 0), solid(1, 0), solid(1, 5), solid(1, 5), solid(1, 3), solid(4, 0), solid(1, 5), solid(1, 0)]


def themes():
    def theme(surface, wall, fill, rim=None, depth=3):
        return kit.TerrainTheme(
            bedrock={"relative": False, "value": 1}, rimEdges="void", wallOnTerrainFaces=True,
            rim=kit.TopBand(enabled=False, depth=1, material=surface),
            surface=kit.TopBand(enabled=True, depth=depth, material=surface),
            wall=wall, wallEnabled=True, fill=fill)

    sandstone_fill = cells(SANDSTONE, size=3, seed=21, rise=2)
    shore_surface = slope_stack(
        (depth_stack((cells(SAND, size=3, seed=11), 2), (solid(24, 0), 1)), 28),
        (depth_stack((cells(SANDSTONE, size=3, seed=12), 3)), 18),
        (depth_stack((cells(ROCK, size=3, seed=13), 3)), 45))
    jungle_surface = slope_stack(
        (depth_stack((GRASS, 1), (solid(3, 0), 2)), 32),
        (depth_stack((cells(DIRT_MIX, size=3, seed=14), 3)), 14),
        (depth_stack((cells(ROCK, size=3, seed=15), 3)), 45))
    karst = cells(ROCK, size=3, seed=16, rise=2)
    return {
        "shore": theme(shore_surface, sandstone_fill, sandstone_fill),
        "jungle": theme(jungle_surface, cells(DIRT_MIX, size=3, seed=17, rise=2), sandstone_fill),
        "karst": theme(depth_stack((karst, 3)), karst, karst),
    }


# --------------------------------------------------------------------------------------------------------------
# Shapes on the ground layer: the rock stacks, the paint patches, the resort's made ground.
# --------------------------------------------------------------------------------------------------------------
PAVING = cells([solid(155, 0), solid(155, 0), solid(155, 1), solid(155, 2)], size=2, seed=41, rise=2)
TILE = cells([solid(168, 0), solid(168, 1), solid(168, 0), solid(169, 0)], size=2, seed=42, rise=2)


def polygon(shape_id, vertices, **words):
    return kit.SketchShape(id=shape_id, type="polygon", operation="add", vertices=vertices, **words)


def stack(name, cx, cz, tiers, seed):
    """A rock stack: tiers (rx, rz, top, skirt, dx, dz) laid one over the other, each offset a little off the last.
    Each tier is an erected plate cut to an absolute top, the wide low ones eased into the lagoon floor by a skirt
    and the narrow high ones sheer."""
    out = []
    for i, (rx, rz, top, skirt, dx, dz) in enumerate(tiers):
        out.append(polygon(f"{name}-{i + 1}", blob(cx + dx, cz + dz, rx, rz, seed=seed + i, wobble=0.2, n=18, turn=seed * 11),
                           height_mode="level", skirt=skirt, base_height=top, theme="karst", keepClear=True))
    return out


STACKS = (
    stack("needle", 38, -32, [(8, 7, 14, 6, 0, 0), (5.4, 4.8, 21, 0, 0.8, -0.6), (3.8, 3.4, 27, 0, -0.7, 0.8),
                              (2.2, 2.2, 30, 0, 0.4, -0.3)], 21),
    stack("sentinel", 19, -43, [(7, 6, 13, 5, 0, 0), (4.4, 4, 19, 0, 0.7, 0.5), (2.6, 2.4, 22, 0, -0.4, -0.3)], 31),
    stack("sisters-a", -44, -52, [(6, 5, 12, 4, 0, 0), (3.8, 3.4, 21, 0, 0.5, 0.3), (2.2, 2.2, 25, 0, -0.3, 0.2)], 41),
    stack("sisters-b", -34, -47, [(5, 5, 12, 4, 0, 0), (3.2, 3, 19, 0, -0.4, 0.4)], 51),
    stack("thumb", -27, -30, [(6, 5, 12, 4, 0, 0), (3.4, 3, 20, 0, 0.6, -0.4), (1.9, 1.9, 24, 0, 0, 0)], 61),
)


def jungle_patch(shape_id, cx, cz, rx, rz, seed):
    return polygon(shape_id, blob(cx, cz, rx, rz, seed=seed, wobble=0.14), base_height=9, theme="jungle")


PATCHES = (
    jungle_patch("garden-jungle", 5, -68, 10, 6.5, 71),
    jungle_patch("palm-cay-jungle", 37, -70, 14, 9, 72),
    jungle_patch("tern-i-jungle", -38, -40, 4.5, 3, 73),
    jungle_patch("reef-cay-jungle", 28, -27, 3.8, 2.8, 74),
)

# The resort terrace: made ground at its own height, out of the relief, with a pool sunk into it.
TERRACE = [[-40, -77], [-3, -77], [-3, -70], [-1.5, -64], [-3, -57], [-10, -52.5], [-22, -51.5], [-33, -52], [-40, -55]]
POOL = [[-28, -63], [-19, -63], [-19, -55], [-28, -55]]


def flight(shape_id, corners, low, high):
    """A flight of stairs as one polygon: two anchors at the foot and two at the head, a material, no skirt."""
    return polygon(shape_id, corners, height_mode="level", skirt=0, base_height=high, anchor_heights=[low, low, high, high],
                   material=PAVING, keepClear=True)


def resort_shapes():
    return [
        polygon("resort-terrace", TERRACE, relief_scope="exclude", base_height=14, material=PAVING),
        polygon("pool", POOL, height_mode="sink", skirt=0, base_height=3, material=TILE, keepClear=True),
        flight("stair-beach", [[-26, -52.5], [-20, -52.5], [-20, -47], [-26, -47]], 12, 14),
    ]


def shapes():
    out = []
    for group in STACKS:
        out.extend(group)
    out.extend(PATCHES)
    out.extend(resort_shapes())
    return out


# --------------------------------------------------------------------------------------------------------------
# Made things: layers of kind "made", one mass or one height of slabs to a layer, a shape stating its own material.
# --------------------------------------------------------------------------------------------------------------
class Made:
    """One made thing as named layers. Every shape of a layer sits at an absolute floor and height, a layer keeps one
    span per column, so a post under a roof is two layers. `mirrors` says whether the symmetry draws it again."""

    def __init__(self, name, mirrors=True):
        self.name, self.mirrors, self.layers = name, mirrors, {}

    def put(self, layer, shape_id, shape):
        self.layers.setdefault(layer, []).append((shape_id, shape))

    def rect(self, layer, shape_id, x0, z0, x1, z1, floor, height, material):
        """Cells x0..x1, z0..z1 inclusive."""
        self.put(layer, shape_id, kit.SketchShape(
            type="rectangle", operation="add", min_x=x0, min_z=z0, max_x=x1 + 1, max_z=z1 + 1, floor=floor,
            base_height=height, material=material))

    def disc(self, layer, shape_id, cx, cz, radius, floor, height, material):
        self.put(layer, shape_id, kit.SketchShape(
            type="circle", operation="add", center_x=cx, center_z=cz, radius=radius, floor=floor,
            base_height=height, material=material))

    def poly(self, layer, shape_id, vertices, floor, height, material):
        self.put(layer, shape_id, kit.SketchShape(
            type="polygon", operation="add", vertices=vertices, floor=floor, base_height=height, material=material))

    def build(self, seat=None):
        out = []
        for key, entries in self.layers.items():
            layer_id = f"{self.name}-{key}"
            shapes = []
            for shape_id, shape in entries:
                shape = dict(shape)
                shape["id"] = f"{self.name}-{key}-{shape_id}"
                shapes.append(shape)
            out.append(kit.AddedLayer(
                id=layer_id, name=layer_id, base_y=0, kind="made", part_of=self.name,
                shapes=shapes,
                groups=[kit.SketchGroup(id=layer_id, name=layer_id, mirrors=self.mirrors,
                                        shapeIds=[sh["id"] for sh in shapes])]))
        return out


TEAK = cells([solid(5, 3), solid(5, 3), solid(5, 4), solid(5, 3)], size=2, seed=81, rise=2)
TEAK_POST = solid(17, 3)
THATCH = solid(170, 0)
CYAN_WOOL = solid(35, 9)
WHITE_WALL = solid(155, 0)
STRIPED_CANOPY = cells([solid(35, 9), solid(35, 0)], size=2, seed=82, rise=2)
STOOL = solid(126, 3)


def beach_bar():
    """The neutral landmark on the axis: an open thatched pavilion on a deck, a counter and stools. Stated once,
    on the symmetry centre, so it is drawn symmetric about z = -0.5 and is not doubled onto itself."""
    bar = Made("driftwood-bar", mirrors=False)
    bar.rect("deck", "deck", -7, -5, 7, 4, 12, 1, TEAK)
    for i, (x, z) in enumerate([(-7, -5), (-3, -5), (3, -5), (7, -5), (-7, 4), (-3, 4), (3, 4), (7, 4)]):
        bar.rect("posts", f"post-{i}", x, z, x, z, 13, 4, TEAK_POST)
    bar.rect("roof-1", "eave", -8, -6, 8, 5, 17, 1, THATCH)
    bar.rect("roof-2", "mid", -6, -4, 6, 3, 18, 1, THATCH)
    bar.rect("roof-3", "crown", -3, -1, 3, 0, 19, 1, THATCH)
    bar.rect("counter", "counter", -3, -1, 3, 0, 13, 2, TEAK)
    for i, x in enumerate([-3, -1, 1, 3]):
        bar.rect("stools", f"north-{i}", x, -3, x, -3, 13, 1, STOOL)
        bar.rect("stools", f"south-{i}", x, 2, x, 2, 13, 1, STOOL)
    return bar


def lifeguard_tower(cx, cz):
    """Four stilts, a platform, an open-fronted white cabin under a turquoise roof, and a ladder."""
    tower = Made("lifeguard-tower")
    for i, (dx, dz) in enumerate([(0, 0), (3, 0), (0, 3), (3, 3)]):
        tower.rect("stilts", f"stilt-{i}", cx + dx, cz + dz, cx + dx, cz + dz, 12, 5, TEAK_POST)
    tower.rect("platform", "platform", cx - 1, cz - 1, cx + 4, cz + 4, 17, 1, TEAK)
    tower.poly("cabin", "walls", ring_polygon(cx + 1.5, cz + 1.5, 3, 1.5, gap=(math.pi, 2)), 18, 3, WHITE_WALL)
    tower.rect("roof", "roof", cx - 1, cz - 1, cx + 4, cz + 4, 21, 1, CYAN_WOOL)
    tower.rect("ladder", "ladder", cx + 5, cz + 1, cx + 5, cz + 1, 12, 6, solid(65, 4))
    return tower


def ring_polygon(cx, cz, outer, inner, gap=None, points=24):
    """A square-ish annulus as one even-odd outline, or a C where `gap` = (bearing, width) leaves it open."""
    def arc(radius, reverse=False):
        if gap is None:
            steps = [2 * math.pi * k / points for k in range(points)]
        else:
            bearing, width = gap
            half = min(math.pi * 0.95, (width / 2) / max(radius, 0.5))
            a0, a1 = bearing + half, bearing + 2 * math.pi - half
            steps = [a0 + (a1 - a0) * k / points for k in range(points + 1)]
        if reverse:
            steps.reverse()
        return [[round(cx + radius * math.cos(a), 2), round(cz + radius * math.sin(a), 2)] for a in steps]
    if gap is None:
        out, hole = arc(outer), arc(max(0.5, inner), reverse=True)
        return out + [out[0]] + hole + [hole[0]]
    return arc(outer) + arc(max(0.5, inner), reverse=True)


def jetty(name, centreline, width, deck_y=11, stilt_every=4, thickness=1):
    """A boardwalk: a planked corridor at deck height over jungle-log stilts driven to the lagoon floor."""
    walk = Made(name)
    walk.poly("deck", "deck", corridor(centreline, width), deck_y, thickness, TEAK)
    centre = smooth(centreline, samples=3)
    for i in range(0, len(centre), stilt_every):
        x, z = round(centre[i][0]), round(centre[i][1])
        for side in (-1, 1):
            walk.rect("stilts", f"stilt-{i}-{side}", x + side, z, x + side, z, 7, deck_y - 7, TEAK_POST)
    return walk


# --------------------------------------------------------------------------------------------------------------
# The hotel, in layers: one made thing (`part_of` halcyon-hotel) on the resort terrace, built on a four-block bay
# and a five-course storey. The facade is paint -- a wallRun of pier and bay, the bay a height stack pinned to
# world Y -- so one mass is one layer; slabs share a layer per height; a door is a sill and a lintel.
# --------------------------------------------------------------------------------------------------------------
BASE = 14           # the first course above the terrace's top block (y13)
BAY, STOREY = 4, 5
PIER = solid(155, 2)                                        # quartz pillar
QUARTZ_BLOCK = solid(155, 0)
GLASS = solid(95, 9)                                        # cyan stained glass
CORNICE = solid(35, 9)                                      # cyan wool: the accent, on the cornice and the roofs


def storey_bands(storeys):
    bands = []
    for _ in range(storeys):
        bands += [(QUARTZ_BLOCK, 2), (GLASS, 2), (QUARTZ_BLOCK, 1)]
    return bands


def height_stack(*bands, start=BASE):
    return kit.LayeredMaterial(axis="height", from_=start, stack=kit.BandStack(
        bands=[kit.Band(material=m, thickness=t) for m, t in bands], ending="repeat"))


BAY_STACK = height_stack(*storey_bands(3), (CORNICE, 2))
FACADE = kit.WallRunMaterial(runs=[{"material": PIER, "width": 1}, {"material": BAY_STACK, "width": BAY - 1}])
LINTEL = BAY_STACK
FLOOR_DECK = cells([solid(5, 3), solid(5, 3), solid(5, 4), solid(5, 3)], size=2, seed=91, rise=2)
SLAB = cells([solid(155, 0), solid(155, 0), solid(155, 1), solid(155, 0)], size=2, seed=92, rise=2)


def hotel_mass(hotel, key, x0, z0, bays_x, bays_z, storeys, floor=0, parapet=2, roofed=True):
    """Walls as one facade-painted rectangle, the interior hollowed by a one-course override floor, and a slab a
    storey on the layer every mass shares at that height. A mass standing on another's storey states `floor`."""
    x1, z1 = x0 + bays_x * BAY, z0 + bays_z * BAY
    hotel.rect(key, f"{key}-walls", x0, z0, x1, z1, BASE + floor, storeys * STOREY + parapet, FACADE)
    low = BASE - 1 if floor == 0 else BASE + floor
    hotel.put(key, f"{key}-floor", kit.SketchShape(
        type="rectangle", operation="add", override=True, min_x=x0 + 1, min_z=z0 + 1, max_x=x1, max_z=z1,
        floor=low, base_height=1, material=FLOOR_DECK))
    for i in range(1, storeys + 1):
        if i == storeys and not roofed:
            continue
        hotel.rect(f"slab-{floor // STOREY + i}", f"{key}-slab-{i}", x0 + 1, z0 + 1, x1 - 1, z1 - 1,
                   BASE + floor + STOREY * i, 1, SLAB)
    return x1, z1


def hotel_door(hotel, layer, x0, z0, x1, z1, top, name):
    """A sill on the wall's own layer and a lintel on the layer every lintel shares, in a bay."""
    hotel.put(layer, f"{name}-sill", kit.SketchShape(
        type="rectangle", operation="add", override=True, min_x=x0, min_z=z0, max_x=x1 + 1, max_z=z1 + 1,
        floor=BASE - 1, base_height=1, material=FLOOR_DECK))
    hotel.rect("lintels", f"{name}-lintel", x0, z0, x1, z1, BASE + 4, top - 4, LINTEL)


def hotel_complex():
    hotel = Made("halcyon-hotel")
    # the open ground storey: a walled glass lobby under the main block, an arcade of quartz piers round it
    hotel_mass(hotel, "lobby", -34, -73, 5, 1, 1, parapet=0, roofed=False)
    for i, x in enumerate(range(-38, -9, BAY)):
        for tag, z in (("south", -66), ("north", -74)):
            hotel.rect("piers", f"pier-{tag}-{i}", x, z, x, z, BASE, STOREY, PIER)
    hotel_door(hotel, "lobby", -29, -69, -27, -69, 5, "lobby-west")
    hotel_door(hotel, "lobby", -21, -69, -19, -69, 5, "lobby-east")
    # the main block: three storeys in all, two above the arcade; the wings step down to two
    hotel_mass(hotel, "main", -38, -74, 7, 2, 2, floor=STOREY)
    hotel_mass(hotel, "wings", -38, -65, 2, 2, 2)
    hotel_mass(hotel, "wings", -18, -65, 2, 2, 2)
    hotel_door(hotel, "wings", -30, -64, -30, -62, 12, "wing-west")
    hotel_door(hotel, "wings", -18, -64, -18, -62, 12, "wing-east")
    # balconies on the courtyard face of the main block, one level each, railed
    for level, course in enumerate((STOREY, 2 * STOREY), start=1):
        hotel.rect(f"balcony-{level}", "slab", -29, -65, -19, -64, BASE + course, 1, FLOOR_DECK)
        hotel.rect(f"rail-{level}", "front", -29, -64, -19, -64, BASE + course + 1, 1, solid(190, 0))
        hotel.rect(f"rail-{level}", "west", -29, -65, -29, -65, BASE + course + 1, 1, solid(190, 0))
        hotel.rect(f"rail-{level}", "east", -19, -65, -19, -65, BASE + course + 1, 1, solid(190, 0))
    # roof terraces on the wings: loungers and a striped shade
    for tag, x in (("west", -37), ("east", -17)):
        for i in range(3):
            hotel.rect("roof-loungers", f"{tag}-{i}", x + 2 * i, -63, x + 2 * i, -60,
                       BASE + 2 * STOREY + 1, 1, solid(35, 0))
        hotel.rect("roof-poles", f"{tag}-pole", x + 1, -58, x + 1, -58, BASE + 2 * STOREY + 1, 3, solid(190, 0))
        hotel.rect("roof-canopy", f"{tag}-canopy", x, -59, x + 2, -57, BASE + 2 * STOREY + 4, 1, STRIPED_CANOPY)
    return hotel


def pool_furniture():
    """Loungers and umbrellas on the pool deck, south of the water and on the courtyard banks."""
    deck = Made("pool-deck")
    for i, x in enumerate([-27, -25, -23, -21]):
        deck.rect("loungers", f"bed-{i}", x, -54, x, -52, 14, 1, solid(35, 0))
        deck.rect("backrests", f"back-{i}", x, -54, x, -54, 15, 1, solid(35, 0))
    for i, (x, z) in enumerate([(-31, -59), (-16, -59), (-12, -53)]):
        deck.rect("poles", f"pole-{i}", x, z, x, z, 14, 4, solid(190, 0))
        deck.rect("canopies", f"canopy-{i}", x - 1, z - 1, x + 1, z + 1, 18, 1, STRIPED_CANOPY)
    return deck


def cabanas():
    """Beach cabanas along the monument's shore: four posts and a striped canopy each."""
    row = Made("beach-cabanas")
    for i, (x, z) in enumerate([(-34, -49), (-17, -49)]):
        for j, (dx, dz) in enumerate([(0, 0), (3, 0), (0, 3), (3, 3)]):
            row.rect("posts", f"post-{i}-{j}", x + dx, z + dz, x + dx, z + dz, 12, 4, solid(190, 0))
        row.rect("canopies", f"canopy-{i}", x - 1, z - 1, x + 4, z + 4, 16, 1, STRIPED_CANOPY)
    return row


def made_layers():
    layers = []
    for thing in (hotel_complex(), beach_bar(), lifeguard_tower(9, -36), pool_furniture(), cabanas(),
                  jetty("palm-walk", [[13, -70], [19, -71.5], [26, -70.5]], 3),
                  jetty("sunset-pier", [[-14, -46], [-15, -40], [-15, -34]], 3)):
        layers.extend(thing.build())
    return layers


# --------------------------------------------------------------------------------------------------------------
# House styles: three forks of library rows, named for what they are (HS19). A fork states the library row it
# starts from and the whole of every top-level part it changes.
# --------------------------------------------------------------------------------------------------------------
STUDIO = kit.Studio()
PLAIN_FLOOR = {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True}
QUARTZ = solid(155, 0)
TEAK_PLANK = solid(5, 3)                      # jungle planks
TEAK_LOG = solid(17, 3)                       # jungle log
TURQUOISE_WOOL = solid(35, 9)                 # cyan wool: the one turquoise that is bright at a distance
TEAK_FLOOR = cells([solid(5, 3), solid(5, 3), solid(5, 4), solid(5, 3)], size=3, seed=71)


def library_style(name):
    rows = STUDIO.get_room_styles()
    row = next(r for r in rows if r["name"] == name)
    return json.loads(STUDIO.get_room_styles_json(row["id"])["styleJson"])


def wall_of(material, extent):
    return {"stack": {"bands": [{"material": material, "thickness": extent}], "ending": "repeat"}, "extent": extent}


def window(form="pane", block=102, sill=2, width=2, height=2, spacing=3):
    return {"form": form, "block": block, "hostBlock": -1, "hostData": 0, "data": 0, "sill": sill, "width": width,
            "height": height, "spacing": spacing}


def storey(clear, wall, post, windows, deck):
    return {"clear": clear, "wall": wall, "post": post, "windows": windows, "surface": PLAIN_FLOOR, "deck": deck,
            "headroom": clear}


def fork(base_name, **parts):
    """A library row with the whole of each named top-level part replaced: what is stated is the fork, and the
    full style is what the preview and the dressing registry see."""
    full = library_style(base_name)
    full.update(parts)
    return {"library": base_name, "kind": "house", "shell": parts}, full


def bungalow_parts():
    base = library_style("jungle-trimmed-stilt-house")
    thatch = dict(base["roof"], body=solid(170, 0), verge=TEAK_PLANK, gable=solid(5, 4), ridgeCap=False)
    plank_wall = wall_of(TEAK_PLANK, 4)
    upper = dict(base["storeys"][1], wall=plank_wall, post=TEAK_LOG,
                 windows=window("stairLattice", 136, 2, 2, 2, 3), deck=TEAK_FLOOR)
    lower = dict(base["storeys"][0], post=TEAK_LOG,
                 wall={"stack": {"bands": [{"material": solid(0, 0), "thickness": 5},
                                           {"material": {"kind": "laidLog", "id": 17, "data": 3}, "thickness": 1}],
                                 "ending": "repeat"}, "extent": 5})
    return dict(roof=thatch, post=TEAK_LOG, storeys=[lower, upper], beams=dict(base["beams"], block=17, data=3))


def pavilion_parts():
    glass = window("pane", 102)
    roof = {"form": "hip", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 2, "ridgeCap": True, "hole": False,
            "body": TURQUOISE_WOOL, "verge": TEAK_PLANK, "gable": QUARTZ,
            "gableWindows": window("none", 102, 2, 2, 2, 3)}
    return dict(roof=roof, wall=wall_of(QUARTZ, 5), post=TEAK_LOG, windows=glass, storeys=[],
                beams={"block": -1, "data": 0, "reach": 1, "any": False},
                foundation={"plate": {"stack": {"bands": [{"material": TEAK_FLOOR, "thickness": 1}], "ending": "repeat"},
                                      "extent": 1}, "surface": PLAIN_FLOOR, "footing": None},
                doorway={"door": "air", "head": {"form": "arched", "block": 156, "fill": "upperSlab", "fillBlock": 44,
                                                 "fillData": 7}, "width": 3, "height": 4})


BUNGALOW = "thatched-jungle-plank-stilt-bungalow"
PAVILION = "cyan-wool-roofed-quartz-pavilion"
FORKS = {BUNGALOW: ("jungle-trimmed-stilt-house", bungalow_parts),
         PAVILION: ("cyan-roofed-white-clay-house", pavilion_parts)}


def house_styles():
    stated, full = {}, {}
    for name, (base, parts) in FORKS.items():
        stated[name], full[name] = fork(base, **parts())
    return stated, full


# --------------------------------------------------------------------------------------------------------------
# The sea: a basin over the whole lagoon fills every column that stands under the line and cuts nothing.
# --------------------------------------------------------------------------------------------------------------
def tree_style(name):
    with open(os.path.join(ROOT, "corpus", "tree-showcase", "trees.json")) as handle:
        return json.load(handle)["trees"][name]["style"]


def house(prop_id, style, wings, front="posZ", seed=1):
    return kit.HouseProp(id=prop_id, layer="ground", seed=seed, front=front, style=style,
                         wings=[kit.AuthoredWing(corners=corners, spec=kit.WingSpec(**spec)) for corners, spec in wings])


def tree(prop_id, style, x, z):
    return kit.TreeProp(id=prop_id, layer="ground", seed=zlib.crc32(prop_id.encode()) % 997, x=x, z=z, style=style)


def path(prop_id, points, pave, radius=1.5, wander=2, wander_length=14):
    return kit.StrokeProp(id=prop_id, layer="ground", points=points, radius=radius, style="solid", claimsGround=True,
                          wander=wander, wanderLength=wander_length, pave=pave)


STONE_PATH = cells([solid(1, 4), solid(1, 3), solid(1, 5)], size=2, seed=51)
SOIL_PATH = cells([solid(3, 0), solid(3, 1), solid(5, 1)], size=2, seed=52)


def dressing():
    stated, _ = house_styles()
    styles = dict(stated)
    styles["jungle-slim"] = tree_style("jungle-2")
    styles["jungle-tall"] = tree_style("jungle-5")
    styles["acacia-shade"] = tree_style("acacia-3")
    props = [
        kit.FluidProp(id="lagoon", layer="ground", shape="basin", points=rect_ring(-60, -120, 60, 3), level=WATER,
                      radius=1, depth=1, shore=0, bank=cells(SAND, size=3, seed=31)),
        kit.FluidProp(id="pool-water", layer="ground", shape="basin", points=POOL, level=12, radius=1, depth=1,
                      shore=0, bank=TILE),
        house("bungalow-a", BUNGALOW, [([[28, -75], [34, -70]], {})], seed=5),
        house("bungalow-b", BUNGALOW, [([[40, -75], [46, -70]], {})], seed=6),
        tree("palm-1", "jungle-slim", 30, -63),
        tree("palm-2", "jungle-tall", 44, -65),
        tree("islet-1", "jungle-slim", -38, -40),
        tree("reef-1", "jungle-tall", 28, -27),
        path("path-spawn", [[0, -92], [-2, -82], [-3, -71], [0, -62], [6, -55]], STONE_PATH, 1.5, 2),
        path("path-palm-walk", [[8, -58], [10, -63], [13, -69]], STONE_PATH, 1.5, 1.5),
        kit.FloraProp(id="garden-cover", layer="ground", seed=3, points=blob(5, -68, 10, 6.5, seed=71, wobble=0.14),
                      spec=kit.FloraSpec(coverage=0.3, scale=5, fernShare=0.5, flowerShare=0.15, flowerScale=4,
                                         tallShare=0.0)),
        kit.FloraProp(id="palm-cover", layer="ground", seed=4, points=blob(37, -70, 14, 9, seed=72, wobble=0.14),
                      spec=kit.FloraSpec(coverage=0.3, scale=5, fernShare=0.5, flowerShare=0.15, flowerScale=4,
                                         tallShare=0.0)),
        path("path-spit", [[-3, -47], [5, -38], [2, -29], [-4, -21], [-1, -12], [1, -4]], STONE_PATH, 1.5, 1.5),
    ]
    return kit.DressingDoc(styles=styles, props=props)


# the compiled spawn pad is held at the beach's own height instead of being seated on whatever the lagoon left
SHAPE_PROPS = {"spawn-red": {"relief_scope": "hold", "base_height": BEACH, "height_authored": True}}


def refinement():
    return kit.Refinement(
        created="2026-10-02", authors=["Sonnet 5.5"],
        biome=kit.SolidBiome(id=BIOME),
        roomStyles=kit.SketchRoomStyles(spawn=house_styles()[1][PAVILION]),
        themes=themes(), mapTheme="shore",
        relief=relief(),
        addShapes=shapes(),
        addLayers=made_layers(),
        shapePropsById=SHAPE_PROPS,
        dressing=dressing(),
    )


def main():
    base = os.path.basename(HERE)
    with open(os.path.join(HERE, f"{base}.plan.json"), "w") as handle:
        json.dump(plan(), handle, indent=1)
    with open(os.path.join(HERE, f"{base}.refinement.json"), "w") as handle:
        json.dump(refinement(), handle, indent=1)
    print("spec written")


if __name__ == "__main__":
    main()
