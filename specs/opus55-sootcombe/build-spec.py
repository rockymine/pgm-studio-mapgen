"""Sootcombe — writes opus55-sootcombe.plan.json and .refinement.json.

A capture board on an ash field: a combe of grey slag falling from each team's brick hamlet, standing on a
terrace four blocks over its hub, down to a flat frontline and a slag stone in the middle of the build band
with a ruined engine house on it. Two wools a team: one at the end of a spur west of the hub behind a
bedrock wall, one at the east end of the terrace behind another. A timber headframe stands over the shaft
at the hub bar's west end, beside the slag heap the shaft threw up.

The arrangement is composed board p12 t2 #21 (`composed-p12-seed21.plan.json`, pinned off GET /api/compose),
taken whole: this spec states its elevation, its paint, its made things and its dressing, and nothing about
where the pieces are. Team 0 is the z > 0 half; rot_180 fans the rest.

Second pass, after the author's review: the first build was bare ash. The outer coasts were cut point by
point, and birch and tiny spruce stand on regrowth along the hub's outer rims.

Third pass, after the author's notes 6, 8, 10 and 33–35: the ground is back to black clay on grey stained clay,
in larger patches, over granite; the slag heap, the engine house and the timber stacks are gone; the
headframe is now a shorter archer tower on each frontline with a one-course deck; the frontline and the mid
stone carry granite boulders; the paths are wider and laid in dirt, coarse dirt and spruce planks; and every
room is a timber lodge in the headframe's own language.

Fourth pass, after the author's notes 33 and 44–50: the rocks are cyan stained clay; the archer tower has a
spruce platform at its frame's course with a nether-brick fence on its beams and a ladder up through it; the
ash is a turbulence field with more black and a little dark oak; the faces and the fill are tilted beds of
hardened clay, granite and a mix, parted by thin lines of hardened clay; the hub's north-west corner rises
five blocks; a second build zone lies east of each hub; and a coast cut that pushed ground past the east
wall's end is turned the right way.

Fifth pass, after the author's notes 7, 10, 33 and 61–64: the mid stone rises a block in its middle and dips
at the lips facing the frontlines, and each frontline dips along part of its edge; every room is the stone
house of Gypsum Reach under a pitched roof; the boulders are andesite and cobble, two larger ones on the
mid stone; grass patches lie at the frontline's back, on the mid stone and on the west rise; and a willow
written for the board stands in the regrowth and on the mid stone's edge.

Sixth pass, after the author's notes 10, 64, 70 and 71: the doors are three tall and the wool rooms' doors
are stained glass in the wool's colour; two more willows stand on the west rise and at the terrace's edge;
and a grass patch lies on each frontline's west front.

Seventh pass, after the author's notes 75–77: the mid stone's corners and the frontline's front corners are
chamfered, with the mid band reaching into the land; the west wool's wall, inner approach and room stand a cell
further out with grass across the wall; and a channel with lily pads splits the east wool's lane in a dip.

Eighth pass, once the studio grew what the board had worked round: the archer tower's ladder is stated once and
the fan turns it; the chest the author asked for in note 45 stands on the platform with a Power I bow among four
stacks of arrows; the willows are the studio's own; and the channel is two wide on both teams.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "tools", "sculpt"))
from studio_kit import kit
import props

SLUG = "opus55-sootcombe"
plan = json.load(open(os.path.join(HERE, "composed-p12-seed21.plan.json")))
plan["meta"] = {"name": "Sootcombe", "authors": ["Opus 5.5"],
                "notes": "composed p12 t2 seed 21 (walled-4), arrangement unchanged but for one build zone"}
# A build zone along the hub's east side (note 50): four blocks of void east of the hub between the frontline
# and the east approach, overlapping the hub by eight so a bridge leaves it with no gap, and ending seven
# blocks short of the east wool's wall. Twelve blocks wide because G2 wants a zone corridor of ten.
plan["zones"].append({"id": "hub-flank", "rect": [-2, 10, 3, 7], "holes": []})
# Note 76: the west wool's rise had come close to its wall, so the piece in front of the wall is a cell longer
# and the wall, the inner approach and the room each stand a cell further out.
MOVED = {"wool-a-t1": [-7, 14, 2, 3], "wool-a-t1-inner": [-10, 14, 3, 3], "wool-a-room": [-12, 14, 2, 3]}
for piece in plan["pieces"]:
    piece["rect"] = MOVED.get(piece["id"], piece["rect"])
for box in plan["boxes"]:
    if box["id"] == "wool-a":
        box["rect"] = [-12, 14, 7, 3]
# Note 75: the mid band reaches four blocks into each frontline, so where the frontline's front corners are
# cut away there is build zone rather than a gap nobody can bridge.
for zone in plan["zones"]:
    if zone["id"] == "mid-band":
        zone["rect"] = [-4, -6, 8, 12]

# Note 75: corners cut back three blocks along both their edges. Each corner moves back along the edge before
# it and a point goes in along the edge after it, the corners taken last to first so each op's index is still
# the ring's own. The frontline's two front corners are points 4 and 5 of the fused ground shape the plan
# compiles to, at (-16, 20) and (16, 20); the mid stone's four are its corners at (±12, ±8).
FRONT_CHAMFER = [kit.VertexEdit(index=5, x=13.0, z=20.0), kit.VertexEdit(after=5, x=16.0, z=23.0),
                 kit.VertexEdit(index=4, x=-16.0, z=23.0), kit.VertexEdit(after=4, x=-13.0, z=20.0)]
# The mid stone lies across the centre and is its own image, so its four corners are each stated and made
# where they are written.
MID_CHAMFER = [kit.VertexEdit(index=3, x=-9.0, z=8.0, fan=False), kit.VertexEdit(after=3, x=-12.0, z=5.0, fan=False),
               kit.VertexEdit(index=2, x=12.0, z=5.0, fan=False), kit.VertexEdit(after=2, x=9.0, z=8.0, fan=False),
               kit.VertexEdit(index=1, x=9.0, z=-8.0, fan=False), kit.VertexEdit(after=1, x=12.0, z=-5.0, fan=False),
               kit.VertexEdit(index=0, x=-12.0, z=-5.0, fan=False), kit.VertexEdit(after=0, x=-9.0, z=-8.0, fan=False)]
# The outer coasts, cut point by point on the chamfered ring: each point goes in after the one its op names,
# counted with every point before it already in, a block or three in from its coast. The frontline's face to
# the band, the wall seams at x -24 and x 12, and the wool rooms' own faces stay as the composer cut them.
FRONT_COAST = [
    # the spur's south coast, west of its wall
    kit.VertexEdit(after=0, x=-41.0, z=57.0), kit.VertexEdit(after=1, x=-34.0, z=58.0),
    # the hub's west coast
    kit.VertexEdit(after=3, x=-18.0, z=51.2), kit.VertexEdit(after=4, x=-17.0, z=44.8),
    # the frontline's west coast
    kit.VertexEdit(after=7, x=-14.0, z=34.9), kit.VertexEdit(after=8, x=-15.0, z=28.9),
    # the frontline's east coast
    kit.VertexEdit(after=13, x=14.0, z=29.8), kit.VertexEdit(after=14, x=15.0, z=35.8),
    # the hub's east coast, along the hole
    kit.VertexEdit(after=17, x=-2.0, z=47.0), kit.VertexEdit(after=18, x=-3.0, z=54.0),
    kit.VertexEdit(after=19, x=-1.0, z=62.4),
    # the east approach's south coast, short of its wall
    kit.VertexEdit(after=21, x=5.0, z=70.0),
    # the spur's north coast
    kit.VertexEdit(after=30, x=-32.0, z=66.0), kit.VertexEdit(after=31, x=-38.7, z=67.0),
]


# --- paint -----------------------------------------------------------------------------------------------
def solid(block, data=0):
    return kit.SolidMaterial(id=block, data=data)


def stack(*bands, **reading):
    """A layered material: (material, thickness) bands repeating, read along `reading`."""
    return kit.LayeredMaterial(stack=kit.BandStack(ending="repeat", bands=[
        kit.Band(material=material, thickness=thickness) for material, thickness in bands]), **reading)


def finish(surface, wall, fill, depth=3, rim=None, rim_edges="void"):
    return kit.TerrainTheme(bedrock=kit.BedrockSpec(relative=False, value=1), rimEdges=rim_edges,
                            rim=kit.TopBand(enabled=rim is not None, depth=1, material=rim or solid(1)),
                            wallEnabled=True, wallOnTerrainFaces=True, wall=wall, fill=fill,
                            surface=kit.TopBand(enabled=True, depth=depth, material=surface))


def one(material):
    """A theme answering one material in every bucket — a made thing too thin to have a core."""
    return finish(material, material, material, depth=1, rim=material, rim_edges="boundary")


# Families: the ground dark (black clay on grey stained clay, granite under it), the built timber (spruce
# planks between dark-oak logs), the accent the granite of the rock, the boulders and the odd path block.
GREY, BLACK = solid(159, 7), solid(159, 15)
WORN = kit.CellMaterial(cellSize=2, seed=7, palette=[solid(3, 1), solid(3, 0)])
# The author's ruling on note 6: the black clay on grey stained clay of the first build, in larger patches;
# and on note 46, more black and a little dark oak, as a turbulence field. A turbulence folds the field, so
# the low stops run as creases through it and the high ones billow: black in the creases, grey and worn
# earth between, black again and a few dark-oak plank patches at the top.
ASH = kit.TurbulenceMaterial(seed=5, scale=7, octaves=3,
                             stops=[BLACK, BLACK, GREY, GREY, WORN, GREY, BLACK, BLACK, solid(5, 5)])
# The rock under it is granite and polished granite (note 6), and it is also the steepest band.
GRANITE = kit.CellMaterial(cellSize=2, seed=8, palette=[solid(1, 1), solid(1, 2), solid(1, 1), solid(1, 2)], rise=2)
SHOULDER = kit.CellMaterial(cellSize=2, seed=6, palette=[GREY, solid(1, 1), solid(1, 2)])
# The faces (note 47): tilted beds of three kinds, mostly hardened clay, mostly granite, and a wider mix,
# each parted from the next by a thin line of hardened clay; the mix is granite with grey and black clay, so
# the clay lines read against it. A diagonal wall pattern shears its stripes one
# arc cell per two courses, so a bed eight cells wide stands four courses thick and a line two wide is one.
CLAY_BED = kit.CellMaterial(cellSize=3, seed=71, palette=[solid(172), solid(172), solid(172), solid(1, 1)], rise=2)
GRANITE_BED = kit.CellMaterial(cellSize=3, seed=72, palette=[solid(1, 1), solid(1, 2), solid(1, 1), solid(1, 2)],
                               rise=2)
MIXED_BED = kit.CellMaterial(cellSize=2, seed=73, palette=[solid(1, 1), GREY, solid(1, 2), solid(159, 15), GREY],
                             rise=2)
LINE = solid(172)
STRATA = kit.WallDiagonalMaterial(slope=2, runs=[
    kit.WallStripe(material=GRANITE_BED, width=8), kit.WallStripe(material=LINE, width=2),
    kit.WallStripe(material=MIXED_BED, width=6), kit.WallStripe(material=LINE, width=2),
    kit.WallStripe(material=CLAY_BED, width=8),
    kit.WallStripe(material=GRANITE_BED, width=6), kit.WallStripe(material=LINE, width=2),
    kit.WallStripe(material=MIXED_BED, width=8), kit.WallStripe(material=LINE, width=2)])
ash = finish(stack((stack((ASH, 1), (GREY, 2)), 30), (stack((SHOULDER, 1), (solid(1, 1), 2)), 15), (GRANITE, 45),
                   axis="slope"),
             wall=STRATA, fill=STRATA)
# Regrowth: grass and worn earth where birch has taken hold.
regrowth = finish(stack((stack((kit.NoiseMaterial(scale=2, seed=12, stops=[WORN, solid(2), solid(2), solid(2)]), 1),
                               (solid(3), 2)), 30),
                        (GRANITE, 60), axis="slope"),
                  wall=STRATA, fill=STRATA)
# Made: the archer tower's dark-oak logs and planks, the headframe's own two blocks.
timber = one(solid(5, 5))
post = one(solid(162, 1))
# The archer tower's platform (note 45): spruce planks, nether-brick fence, and a ladder set against a beam.
# The ladder faces north onto its south beam; the fan turns it with the layer, so the image faces its own.
planks = one(solid(5, 1))
fence = one(solid(113))
ladder = one(solid(65, 2))

# The paths (note 6): dirt, coarse dirt and spruce planks, with very little granite — one entry in seven.
PAVE = kit.CellMaterial(cellSize=2, seed=21, palette=[solid(3), solid(3, 1), solid(5, 1), solid(3), solid(3, 1),
                                                      solid(5, 1), solid(1, 1)])


# The rooms (notes 10, twice): the lodge's timber read brown on the brown ash, so every room is the stone
# house of Gypsum Reach, which the author named as fitting: polished-andesite posts, walls of stone brick and
# andesite in alternate courses, a hardened-clay gable under a pitched jungle-plank roof. It is the lodge's own
# room style with the stone laid over it, so the room's entry and floor stay what a room needs; only the paint
# and the roof's form change, and it stands on no footing. The plate's band and the storey are stated whole,
# because a list laid over a library row replaces the row's.
def stone_wall(extent):
    # a stack's `repeat` carries its last band on rather than cycling, so the courses are written out
    return kit.RoomPart(stack=kit.BandStack(ending="repeat", bands=[
        kit.Band(material=solid(98) if course % 2 == 0 else solid(1, 5), thickness=1) for course in range(12)]),
        extent=extent)


STONE_ROOM = {
    "foundation": {"plate": {"stack": {"bands": [kit.Band(material=solid(98), thickness=1)]}}, "footing": None},
    "wall": stone_wall(5),
    "post": solid(1, 6),
    "roof": {"form": "gable", "ridgeCap": True, "body": solid(5, 3), "verge": solid(5, 3), "gable": solid(172),
             "slab": 126, "slabData": 3},
    "storeys": [kit.Storey(clear=6, wall=stone_wall(6), post=solid(1, 6), deck=None, headroom=6,
                           surface=kit.FloorSurface(field=None, border=None, borderWidth=1, inlay=None, inlayInset=2),
                           windows=kit.WindowStyle(form="pane", block=102, hostBlock=-1, hostData=0, data=0, sill=2,
                                                   width=3, height=3, spacing=2))],
}

relief = {"team": kit.SketchReliefJson(
    base=10, reach=0, step=1, landform="rolling",
    marks=[
        kit.ReliefMarkJson(id="terrace", kind="area", h=13, ring=[[-20, 70], [36, 70], [36, 97], [-20, 97]]),
        kit.ReliefMarkJson(id="front", kind="area", h=9, ring=[[-17, 20], [17, 20], [17, 33], [-17, 33]]),
        kit.ReliefMarkJson(id="spur", kind="line", r=6, tread=4, points=[[-22, 62], [-42, 62]], h=[11, 10]),
    ],
    # The slag heap is gone (note 8): the board is too small to carry a rock that size. In its place the
    # hub's north-west corner, where the spur meets it, rises five blocks over the terrain (note 49).
    pushes=[
        # note 7: the mid stone rises a block or two in its middle, from two offset bumps that the fan
        # overlaps (a push on its centre would be fanned onto itself and doubled), and dips at the lip
        # facing each frontline. The stone takes its relief from its z < 0 half and fans it, so its pushes
        # are stated there. Each frontline dips two blocks along part of its edge, in a curve.
        kit.ReliefPushJson(id="mid-rise", amount=1, falloff=3, roughness=0.2, crown=0, seed=11),
        kit.ReliefPushJson(id="mid-lip", amount=-2, falloff=2, roughness=0.2, crown=0, seed=12),
        kit.ReliefPushJson(id="front-dip", amount=-2, falloff=4, roughness=0.2, crown=0, seed=13),
        # note 77: the east wool's lane dips two blocks where the channel crosses it
        kit.ReliefPushJson(id="east-dip", amount=-2, falloff=3, roughness=0.2, crown=0, seed=15),
        kit.ReliefPushJson(id="west-rise", amount=5, falloff=7, roughness=0.3, crown=0, seed=9)],
)}

# Every lobed outline on the board, by the id of what it outlines.
outlines = {
    "mid-rise": kit.Outline(at=[-3, 0], radius=4, radiusZ=3, points=28, wobble=0.1, lobes=3),
    "mid-lip": kit.Outline(at=[3, -8], radius=5, radiusZ=2, points=28, wobble=0.1, lobes=3),
    "front-dip": kit.Outline(at=[2, 20], radius=6, radiusZ=3, points=28, wobble=0.1, lobes=3),
    "east-dip": kit.Outline(at=[17, 74], radius=3, radiusZ=6, points=28, wobble=0.1, lobes=3),
    "west-rise": kit.Outline(at=[-19, 74], radius=3, radiusZ=6, points=28, wobble=0.1, lobes=3),
    "regrowth-front": kit.Outline(at=[2, 38], radius=4, radiusZ=3, points=16, wobble=0.2, lobes=3),
    "regrowth-mid": kit.Outline(at=[-8, -5], radius=4, radiusZ=3, points=16, wobble=0.2, lobes=3, phase=0.5),
    "regrowth-rise": kit.Outline(at=[-18, 74], radius=3, radiusZ=5, points=16, wobble=0.2, lobes=3),
    "regrowth-wall": kit.Outline(at=[-28, 62], radius=6, radiusZ=4, points=16, wobble=0.2, lobes=3, phase=0.3),
    "regrowth-front-west": kit.Outline(at=[-9, 24], radius=6, radiusZ=4, points=16, wobble=0.2, lobes=3, phase=0.8),
}


# --- made things -----------------------------------------------------------------------------------------
def made(layers, part_of, seat=None):
    """`tools/sculpt/props.py` layers as storeys of made ground, all of one `part_of`."""
    return [kit.AddedLayer(id=layer["id"], name=layer["name"], base_y=layer["base_y"], kind="made", part_of=part_of,
                           shapes=layer["layout"]["shapes"], groups=layer["layout"]["groups"],
                           **({"seat": seat} if seat else {}))
            for layer in (layers if isinstance(layers, list) else [layers])]


layers = []

# The archer tower on each frontline (note 35): the headframe, shorter and moved to the front — four dark-oak
# log legs, a plank frame halfway up, and a deck one course thick. The engine house on the mid stone is gone
# (note 33), and the timber stacks are boulders now (note 34).
AX, AZ, AW = 9, 33, 5            # its west-north corner and its width, at the frontline's back east corner
FLOOR = 9                        # the frontline is pinned at 9, so its top course is y8
legs = props.LayerBuilder("archer-legs")
for dx in (0, AW - 1):
    for dz in (0, AW - 1):
        legs.rect(AX + dx, AZ + dz, AX + dx + 1, AZ + dz + 1, FLOOR, 9, "post")
frame = props.LayerBuilder("archer-frame")
for x0, z0, x1, z1 in [(AX + 1, AZ, AX + AW - 1, AZ + 1), (AX + 1, AZ + AW - 1, AX + AW - 1, AZ + AW),
                       (AX, AZ + 1, AX + 1, AZ + AW - 1), (AX + AW - 1, AZ + 1, AX + AW, AZ + AW - 1)]:
    frame.rect(x0, z0, x1, z1, FLOOR + 4, 1, "timber")
# The platform (note 45): the four beams ring a 3 x 3 floor of spruce planks at the frame's course, open in
# one cell against the south beam, where a ladder climbs from the ground; a nether-brick fence stands on
# every beam, and the roof is the deck one course thick over it. A rect covers x0 .. x1 - 1.
HX, HZ = AX + 2, AZ + AW - 2                     # the ladder's hole, against the beam at z = AZ + AW - 1
floor_ = props.LayerBuilder("archer-floor")
for x in range(AX + 1, AX + AW - 1):
    for z in range(AZ + 1, AZ + AW - 1):
        if (x, z) != (HX, HZ):
            floor_.rect(x, z, x + 1, z + 1, FLOOR + 4, 1, "planks", keepClear=False)
rail = props.LayerBuilder("archer-rail")
for x0, z0, x1, z1 in [(AX + 1, AZ, AX + AW - 1, AZ + 1), (AX + 1, AZ + AW - 1, AX + AW - 1, AZ + AW),
                       (AX, AZ + 1, AX + 1, AZ + AW - 1), (AX + AW - 1, AZ + 1, AX + AW, AZ + AW - 1)]:
    rail.rect(x0, z0, x1, z1, FLOOR + 5, 1, "fence", keepClear=False)
climb = props.LayerBuilder("archer-ladder")
climb.rect(HX, HZ, HX + 1, HZ + 1, FLOOR, 5, "ladder", keepClear=False)
deck = props.LayerBuilder("archer-deck")
deck.rect(AX - 1, AZ - 1, AX + AW + 1, AZ + AW + 1, FLOOR + 9, 1, "timber")
layers += made([legs.done(), frame.done(), floor_.done(), rail.done(), climb.done(), deck.done()],
               "archer-tower")

# Lily pads on the channel (note 77), a course over its water line at y10.
pads = props.LayerBuilder("lily-pads")
for x, z in [(16, 70), (17, 73), (17, 76), (16, 78)]:
    pads.rect(x, z, x + 1, z + 1, 11, 1, "lily", keepClear=False)
layers += made(pads.done(), "lily-pads")


# --- patches -------------------------------------------------------------------------------------------
def patch(pid, vertices=None):
    """A patch of regrowth: a polygon at the height of the ground it lies on, in the team's group, painting the
    cells it forms the surface of and nothing else. Its outline is `vertices`, or the outline stated under its
    id."""
    return {**kit.SketchShape(id=pid, type="polygon", operation="add", base_height=9, theme="regrowth",
                              **({"vertices": vertices} if vertices else {})),
            **kit.ShapeJoin(group="team")}


shapes = [
    patch("regrowth-west", [[-20, 42], [-14, 43], [-13, 52], [-15, 60], [-14, 67], [-20, 67]]),
    patch("regrowth-bar", [[-2, 76], [10, 76], [12, 80], [-2, 80]]),
    # grass at the frontline's back, on the mid stone round its willow, and on the west rise's top (61, 62, 64)
    patch("regrowth-front"),
    patch("regrowth-mid"),
    patch("regrowth-rise"),
    # grass either side of the west wool's wall where it stands now (note 76)
    patch("regrowth-wall"),
    # grass on the frontline's west front (note 71)
    patch("regrowth-front-west"),
]

# --- dressing ------------------------------------------------------------------------------------------
# One willow in the regrowth and smaller ones at the mid stone's edge, on the west rise and at the terrace
# (notes 62, 63, 64, 70): the studio's willow, dark-oak bark under oak leaves hanging from the crown's rim.
styles = {"willow": kit.TreeStyle(form="template", species="willow", height=11),
          "willow-small": kit.TreeStyle(form="template", species="willow", height=9)}
# The boulders (notes 34 and 33), small and medium, all of cyan stained clay, which the 1.8 textures draw
# as a dark grey.
# note 33 again: andesite and cobblestone, whose texture stands off the flat clay ground; two larger rocks on
# the mid stone in place of four
ROCK_MIX = kit.CellMaterial(cellSize=2, seed=33, palette=[solid(1, 5), solid(4), solid(1, 5), solid(4), solid(1, 6)])
styles["rock-small"] = kit.BoulderStyle(form="round", size=1.6, rock=ROCK_MIX, mossy=False)
styles["rock-medium"] = kit.BoulderStyle(form="angular", size=2.4, rock=ROCK_MIX, mossy=False)
styles["rock-large"] = kit.BoulderStyle(form="angular", size=3.0, rock=ROCK_MIX, mossy=False)


def path(pid, seed, points, radius=1.5, wander=2):
    return kit.StrokeProp(id=pid, seed=seed, style="solid", radius=radius, claimsGround=True, wander=wander,
                          wanderLength=14, pave=PAVE, points=points)


props_ = [
    # wider than before (note 6): four blocks across the front path, three to the wools
    path("path-front", 51, [[-10, 86], [-10, 72], [-8, 54], [-4, 38], [0, 23]], radius=2),
    path("path-wool-a", 52, [[-12, 60], [-24, 62], [-37, 62]], radius=2, wander=1),
    # the east wool's path stops either side of the channel: a stroke paves over water
    path("path-wool-b", 53, [[-6, 75], [8, 74], [13, 74]], radius=2, wander=1),
    path("path-wool-b2", 54, [[22, 74], [27, 74]], radius=2, wander=0),
    # note 77: a channel across the east wool's lane, in a dip, coast to coast so an attacker has to cross
    # it. Its bed is x 16..17 on both teams: the wall's keep-out is x 15, and blue's door approach reaches the
    # image of x 18, and a kept column is filled and never cut, so a channel over either carves no water there
    # (DR-HELD) and would run narrower on one team than the other.
    kit.FluidProp(id="east-channel", shape="channel", form="canal", layer="ground", points=[[17, 66], [17, 82]],
                  radius=1.0, depth=2, shore=1, shoreWander=True, edge=1.5,
                  bank=kit.CellMaterial(cellSize=2, seed=77, palette=[solid(13), solid(3, 1), solid(1, 1)])),
    # boulders on the frontline where the timber stacks stood, and on the mid stone where the engine house did
    kit.BoulderProp(id="front-1", x=-11, z=27, style="rock-medium", seed=21),
    kit.BoulderProp(id="front-2", x=5, z=29, style="rock-small", seed=22),
    kit.BoulderProp(id="front-3", x=-9, z=35, style="rock-small", seed=23),
    kit.BoulderProp(id="front-4", x=12, z=25, style="rock-medium", seed=24),
    kit.BoulderProp(id="mid-1", x=5, z=-4, style="rock-large", seed=26),
    kit.TreeProp(id="willow-1", x=-18, z=50, style="willow", seed=1),
    kit.TreeProp(id="willow-mid", x=-9, z=-5, style="willow-small", seed=2),
    # two more willows (notes 64, 70): on the west rise's top, and at the terrace's north edge by the stem
    kit.TreeProp(id="willow-rise", x=-18, z=74, style="willow-small", seed=4),
    kit.TreeProp(id="willow-terrace", x=2, z=79, style="willow-small", seed=5),
    # the archer's chest on the tower's platform (note 45): a Power I bow in the middle slot and four stacks of
    # eight arrows round it, in the corner away from the ladder's hole, opening onto the platform
    kit.ChestProp(id="archer-chest", x=AX + 1, z=AZ + 1, facing="posZ", y=FLOOR + 5, items=[
        kit.ChestItem(item="bow", count=1, enchantments=[kit.ChestEnchantment(name="power", level=1)], slot=13),
        kit.ChestItem(item="arrow", count=8, slot=4), kit.ChestItem(item="arrow", count=8, slot=12),
        kit.ChestItem(item="arrow", count=8, slot=14), kit.ChestItem(item="arrow", count=8, slot=22)]),
    kit.FloraProp(id="regrowth-cover", seed=8, points=[[-21, 41], [-12, 41], [-12, 68], [-21, 68]],
                  spec=kit.FloraSpec(coverage=0.3, scale=6, octaves=2, fernShare=0.4, flowerShare=0.03,
                                     flowerScale=12, tallShare=0.02, deadBushShare=0.0, cactusShare=0.0)),
]

refinement = kit.Refinement(
    created="2026-09-28",
    authors=["Opus 5.5"],
    biome=kit.SolidBiome(id=32),
    themes={"ash": ash, "regrowth": regrowth, "timber": timber, "post": post, "planks": planks,
            "fence": fence, "lily": one(solid(111)), "ladder": ladder},
    mapTheme="ash",
    relief=relief,
    outlines=outlines,
    # Note 75: the frontline's two front corners and the mid stone's four are chamfered three blocks first,
    # and the frontline's outer coasts are cut on the chamfered ring.
    editShapes={"frontline-t1-9": FRONT_CHAMFER + FRONT_COAST, "mid-stone-0-9": MID_CHAMFER},
    addShapes=shapes,
    addLayers=layers,
    # note 10 again: a door three tall. Its width is not the style's: the studio cuts a room's door to its wall
    # (WX7), four on these walls. The wool rooms' doors are filled with stained-glass panes in the wool's colour,
    # which an attacker breaks through; the spawn rooms keep an open door.
    roomStyles={"spawn": kit.library("lk-spawn", **STONE_ROOM, doorway={"width": 2, "height": 3}),
                "wool": kit.library("lk-spawn", **STONE_ROOM,
                                    doorway={"width": 2, "height": 3, "door": "stainedGlassPane"})},
    dressing=kit.DressingDoc(styles=styles, props=props_),
)

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(refinement, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
print("wrote", SLUG)
