#!/usr/bin/env python3
"""Writes sonnet55-vindrift.plan.json and sonnet55-vindrift.finish.json.

Vindrift: two timber lodges on opposite shoulders of a glacier, a crevasse in each team's hub, the wool kept
in a cairn-hall at the cold end of each flank, and the ice between the teams bridged over a windswept void
with a stone holm in the middle.

    python3 specs/sonnet55-vindrift/build-spec.py
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "sculpt"))
import props as sculpt  # noqa: E402  the shape emitters: a spire is concentric discs on one layer

SLUG = "sonnet55-vindrift"

# ---------------------------------------------------------------------------------------------- blocks
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def depth_stack(*bands):
    """One material per course from the top of a bucket down; the last repeats."""
    return {"kind": "layered", "stack": {"ending": "repeat", "bands": [
        {"material": m, "thickness": t} for m, t in bands]}}


SNOW, PACKED_ICE, ICE = solid(80), solid(174), solid(79)
STONE, GRANITE, DIORITE, ANDESITE = solid(1), solid(1, 1), solid(1, 3), solid(1, 5)
COBBLE, DIRT, COARSE_DIRT, PODZOL = solid(4), solid(3), solid(3, 1), solid(3, 2)
BEDROCK = solid(7)

COLD_TAIGA = 30


def noise(seed, scale, octaves, stops, rise=0):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves, "stops": stops, "rise": rise}


def cell(seed, size, palette, jitter=2, warp=2, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp, "palette": palette,
            "rise": rise}


def by_slope(*bands):
    """Bands whose thickness is a span of degrees: one stack finishes the flat, the shoulder and the face."""
    return {"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
        {"material": m, "thickness": t} for m, t in bands]}}


def theme(surface, fill=STONE, wall=None, rim=None):
    """rim is a depth stack, or None for no rim."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "rim": {"enabled": rim is not None, "depth": 3, "material": rim or STONE},
        "wallEnabled": True,
        "wallOnTerrainFaces": True,
        "wall": wall or STONE,
        "fill": fill,
        "surface": {"enabled": True, "depth": 3, "material": surface},
    }


# ---------------------------------------------------------------------------------------------- plan
def build_plan():
    plan = json.load(open(os.path.join(HERE, "pinned.plan.json")))
    plan["meta"]["name"] = "Vindrift"
    piece = {p["id"]: p for p in plan["pieces"]}
    # the right-hand frontline spur is as wide as the left and reaches the band's edge, so both crossings are 16 blocks (FR9)
    piece["frontline-t3"]["rect"] = [1, 6, 4, 2]
    # the holm is 16 blocks shorter than the band, so each strait to it is 16 blocks, never a jump
    piece["mid-stone-0"]["rect"] = [-4, -2, 8, 4]
    return plan


# ---------------------------------------------------------------------------------------------- houses
def house_style(roof_form="gable", wall_block=solid(5, 1)):
    """Spruce-plank timber walls on dark-oak corner posts under a brick roof: the built family is dark wood,
    the accent is the roof's red, and neither is a tone the snow underfoot carries."""
    plate = {"stack": {"bands": [{"material": cell(311, 3, [solid(98), solid(1, 6), solid(1, 5), solid(1)],
                                                   jitter=1, warp=1), "thickness": 1}], "ending": "repeat"},
             "extent": 1}
    return {
        "foundation": {"plate": plate,
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       "footing": None},
        "roof": {"form": roof_form, "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1, "ridgeCap": True,
                 "hole": False, "body": solid(45), "verge": solid(5, 1), "gable": solid(5, 1),
                 "gableWindows": {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                                  "sill": 2, "width": 2, "height": 2, "spacing": 3}},
        "wall": {"stack": {"bands": [{"material": wall_block, "thickness": 1}], "ending": "repeat"}, "extent": 5},
        "post": solid(162, 1),
        "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 2,
                    "width": 1, "height": 2, "spacing": 4},
        "storeys": [],
        "porch": None,
        "front": None,
        "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
        "doorway": {"door": "air",
                    "head": {"form": "arched", "block": 134, "fill": "upperSlab", "fillBlock": 126, "fillData": 1},
                    "width": 2, "height": 4},
    }


def lodge_style():
    return house_style()


def hall_style():
    return house_style()


# ---------------------------------------------------------------------------------------------- seracs
def made_layer(layer, part_of):
    """A sculpt emitter's layer in the form the finish's addLayers takes: a made thing, seated on the ground."""
    return {"id": layer["id"], "name": layer["name"], "base_y": layer["base_y"], "kind": "made",
            "part_of": part_of, "seat": "ground",
            "shapes": layer["layout"]["shapes"], "groups": layer["layout"]["groups"]}


def seracs():
    """Pillars of blue ice standing on the holm: a tall needle on the centre line, and a low stump either side
    of it. They are the cover that cuts the one long sightline between the two lodges, and the landmark a
    player reads the middle of the board by."""
    layers = []
    for layer_id, cx, cz, radius, height in (("serac-needle", 0, -0.5, 3.5, 11),
                                             ("serac-stump", -11, -0.5, 2.5, 5)):
        layer = sculpt.spire(layer_id, cx, cz, radius, 0, height, "serac", sides=6, base_y=10)
        layers.append(made_layer(layer, layer_id))
    return layers


# ---------------------------------------------------------------------------------------------- coast
def coast_edits():
    """Points added along the outer coast of the compiled outline. Edge i runs from vertex i to i+1 of the
    24-point ring the plan compiles to; an edge is edited only where it faces open void and nothing reaches it
    (not the frontline's brink, the wool rooms' ends or the spawn's)."""
    bulges = {
        21: [(-25.5, 92), (-26.5, 87), (-24.5, 82)],       # the back bar's west end
        20: [(-8, 97.5), (-14, 98), (-20, 97)],            # the back bar's west brow
        16: [(20, 97.5), (16, 98)],                        # the back bar's east brow, short of the lodge
        15: [(25.5, 78), (26.5, 86), (25, 92)],            # the back bar's east end
        11: [(25.5, 38), (27, 46), (25.5, 53)],            # the east coast of the hub
        1: [(-25.5, 62), (-27, 53), (-25.5, 45), (-26.5, 38)],  # the west coast of the hub
    }
    ops = []
    for edge in sorted(bulges, reverse=True):
        for x, z in reversed(bulges[edge]):
            ops.append({"after": edge, "x": x, "z": z})
    return ops


# ---------------------------------------------------------------------------------------------- dressing
TREES = [
    # (id, recipe, x, z, soil radius in blocks)
    ("spruce-west-knoll-a", "tall-spruce-7", -16, 87, 4.5),
    ("spruce-west-knoll-b", "tiny-spruce-1", -22, 93, 3.5),
    ("spruce-east-knoll-a", "tall-spruce-7", 19, 87, 4.5),
    ("spruce-east-knoll-b", "tiny-spruce-2", 14, 93, 3.5),
    ("spruce-west-bank-a", "tiny-spruce-1", -22, 53, 3.5),
    ("spruce-west-bank-b", "tiny-spruce-3", -22, 61, 3.5),
    ("spruce-east-bank-a", "tiny-spruce-2", 22, 53, 3.5),
    ("spruce-east-bank-b", "tiny-spruce-5", 22, 61, 3.5),
]


def forest_floors():
    """Ground a tree can root in. Every other cell on the board is snow, so each spruce stands in a disc of
    bare forest floor of its own, drawn level with the island's top so it owns the paint — the snow is kept
    off the ground under a crown."""
    shapes = []
    for index, (tree_id, _recipe, x, z, radius) in enumerate(TREES):
        shapes.append({"id": f"floor-{tree_id}", "type": "polygon", "operation": "add", "floor": 0,
                       "base_height": 9, "theme": "forest-floor",
                       "vertices": round_ring(x, z, radius, radius, 18, lobes=3, depth=0.15, phase=index)})
    return shapes


def paving(seed):
    """A trodden way: coarse dirt, podzol and spruce plank, three dark browns a reader cannot quite tell apart,
    laid a third each."""
    return cell(seed, 3, [COARSE_DIRT, PODZOL, solid(5, 1)], jitter=55, warp=1)


def road(road_id, points, seed, wander=2.0):
    return {"id": road_id, "kind": "stroke", "seed": seed, "radius": 2, "style": "solid", "claimsGround": True,
            "pave": paving(seed + 1), "points": points, "wander": wander, "wanderLength": 16}


def build_dressing():
    trees = json.load(open(os.path.join(HERE, "trees.json")))
    styles = dict(trees)
    styles["erratic"] = {"kind": "boulder", "form": "round", "size": 2, "mossy": False,
                         "rock": cell(4201, 4, [STONE, COBBLE, ANDESITE, STONE], jitter=2, warp=3)}

    def tree(tree_id, style, x, z, seed):
        return {"id": tree_id, "kind": "tree", "seed": seed, "x": x, "z": z, "style": style}

    def rock(rock_id, style, x, z, seed):
        return {"id": rock_id, "kind": "boulder", "seed": seed, "x": x, "z": z, "style": style}

    props = [
        # spawn door -> the west arm -> the west wool hall's wall; the same road carries on to the front
        road("road-west", [[4, 97], [1, 90], [-8, 84], [-14, 78], [-14, 70], [-13, 62], [-11, 54], [-9, 46],
                           [-9, 38], [-12, 30], [-12, 26]], 4301),
        road("road-west-wool", [[-16, 74], [-21, 74], [-25, 74]], 4311, wander=1.0),
        road("road-west-hall", [[-31, 74], [-35, 74], [-38, 74]], 4321, wander=0.0),
        # spawn door -> the east arm -> the east wool hall's wall; and on to the front
        road("road-east", [[4, 97], [8, 90], [15, 84], [17, 77], [17, 68], [15, 60], [12, 52], [10, 44],
                           [10, 36], [12, 30], [12, 26]], 4331),
        road("road-east-wool", [[18, 66], [22, 66], [25, 66]], 4341, wander=1.0),
        road("road-east-hall", [[31, 66], [35, 66], [38, 66]], 4351, wander=0.0),
        *[tree(tree_id, recipe, x, z, 4401 + index)
          for index, (tree_id, recipe, x, z, _radius) in enumerate(TREES)],
        rock("erratic-east-coast", "erratic", 23, 45, 4421),
        rock("erratic-holm", "erratic", -13, 4, 4423),
    ]
    return {"styles": styles, "props": props}


# ---------------------------------------------------------------------------------------------- relief
def rect_ring(x0, z0, x1, z1):
    return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]


def round_ring(cx, cz, rx, rz, points=24, lobes=0, depth=0.0, phase=0.0):
    out = []
    for k in range(points):
        a = 2 * math.pi * k / points
        r = 1 + depth * math.cos(lobes * a + phase)
        out.append([round(cx + rx * r * math.cos(a), 2), round(cz + rz * r * math.sin(a), 2)])
    return out


def area(mark_id, ring, height, bevel=None):
    mark = {"id": mark_id, "kind": "area", "ring": ring, "h": height}
    if bevel:
        mark["bevel"] = bevel
    return mark


def push(push_id, ring, amount, falloff, crown=0, roughness=0.15, seed=1):
    return {"id": push_id, "ring": ring, "amount": amount, "falloff": falloff, "crown": crown,
            "roughness": roughness, "seed": seed}


def build_relief():
    """One group carries the whole board: the compiled unit and the holm. The floors a player stands on are
    pinned and the ground between them is left to the solver, so the shelf the spawn lodge stands on steps down
    toward the front a course at a time."""
    marks = [
        area("spawn-shelf", rect_ring(-8, 94, 16, 112), 15),
        area("front-apron", rect_ring(-24, 24, 24, 46), 9),
        area("holm", rect_ring(-16, -8, 16, 8), 10),
        area("wool-west", rect_ring(-48, 66, -30, 82), 10),
        area("wool-east", rect_ring(30, 58, 48, 74), 10),
    ]
    pushes = [
        # a cornice, wind-packed snow lipped round the crevasse
        push("cornice", round_ring(0, 72, 11, 11, 28, lobes=4, depth=0.06), 2, 6, 0),
        # two snow berms across the holm: low cover to cross behind, not a hill in the middle of the lane
        push("berm-west", round_ring(-8, -3, 7, 2, 20), 2, 4, 0, seed=21),
        push("berm-east", round_ring(8, -3, 7, 2, 20), 2, 4, 0, seed=22),
        push("drift-west", round_ring(-16, 88, 6, 5, 20, lobes=3, depth=0.2), 3, 7, 2, seed=11),
        push("drift-east", round_ring(17, 90, 6, 5, 20, lobes=3, depth=0.2, phase=1.0), 3, 7, 2, seed=12),
    ]
    return {"base": 10, "reach": 0, "step": 1, "marks": marks, "pushes": pushes}


# ---------------------------------------------------------------------------------------------- finish
def build_finish():
    # ground: snow, with packed ice only as sparse small windswept patches; ice where it steepens, rock where
    # it is too steep to hold snow
    flat = noise(4101, 3, 2, [SNOW, SNOW, SNOW, SNOW, PACKED_ICE])
    glacier = cell(4102, 3, [PACKED_ICE, SNOW, PACKED_ICE])
    scree = cell(4103, 4, [STONE, ANDESITE, STONE, COBBLE])
    snowfield = theme(
        by_slope((depth_stack((flat, 1), (SNOW, 2)), 40),
                 (depth_stack((glacier, 1), (STONE, 2)), 20),
                 (depth_stack((scree, 3)), 30)),
        # a cut face is glacier: a snow cap, blue ice, and the dark rock the ice is lying on
        wall=depth_stack((SNOW, 1), (PACKED_ICE, 7), (cell(4104, 4, [STONE, ANDESITE, STONE], rise=2), 8)),
        rim=depth_stack((SNOW, 1), (PACKED_ICE, 2)))
    forest_floor = theme(depth_stack((noise(4121, 2, 2, [COARSE_DIRT, PODZOL, PODZOL, PODZOL, PODZOL]), 1),
                                     (DIRT, 2)),
                         wall=snowfield["wall"])
    serac = theme(depth_stack((PACKED_ICE, 3)), fill=PACKED_ICE, wall=PACKED_ICE)
    return {
        "authors": ["Sonnet 5.5"],
        "created": "2026-10-01",
        "biome": {"kind": "solid", "id": COLD_TAIGA},
        "themes": {"snowfield": snowfield, "forest-floor": forest_floor, "serac": serac},
        "mapTheme": "snowfield",
        "addShapes": forest_floors(),
        "addLayers": seracs(),
        "dressing": build_dressing(),
        "roomStyles": {"wool": hall_style(), "spawn": lodge_style()},
        "relief": {"*": build_relief()},
        # the crevasse is drawn as a rift rather than a ruled square, and the glacier's outer coast bulges out
        # of the compiled outline one vertex at a time; the edges the build zones and the wool rooms meet stay
        # exactly where the plan put them
        "editShapes": {"frontline-t1-9": coast_edits()},
        "bendShapes": {"void-1-cut": {"k": 0.25, "wander": 2.0, "step": 4, "seed": 12, "side": "both"}},
    }


def main():
    json.dump(build_plan(), open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
    json.dump(build_finish(), open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
