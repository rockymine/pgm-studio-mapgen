"""Writes designing-a-structure.layout.json — one programme built badly, then three structures built to a
method: a research station, an observatory and a relay mast.

The station and the pile beside it carry the same programme — a laboratory, an annex, a stair tower, a dish,
two tanks and a mast — and differ in four decisions: a module every dimension is a multiple of, one mass to a
layer, a façade stated as paint rather than as shapes, and three material families named before anything is
drawn. The observatory is the round version of the same method, and the relay mast is the thing a hand cannot
draw, compiled from a solid and painted along world Y so its colour costs no layer at all.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools", "sculpt"))
from cards import SOLID, grid, moor
import layers as compiler
import solid

PANEL_W, PANEL_D = 84, 72
COL_X, ROW_Z = grid(2, 3, PANEL_W, PANEL_D)
PLAIN = 8                 # the plain's top block is y7, so a made layer rests at base_y 8

# The module. A bay is four blocks pier to pier and a storey five courses: a slab, a sill, two of glass and a
# head. A side of 4n + 1 cells puts a pier on every corner, because the wall's stripe cycle starts at one.
BAY, STOREY = 4, 5

# Three families, named before anything is drawn: the built family (a white frame and a grey-teal skin), the
# accent (blue glass and a safety orange, and nothing else), and the ground, which is the moor.
FRAME, SKIN, GLASS = SOLID(155), SOLID(159, 9), SOLID(95, 3)
ROOF, PLANT, ACCENT, METAL = SOLID(1, 6), SOLID(1, 5), SOLID(159, 1), SOLID(42)


def by_height(*bands, beyond=None):
    """A stack pinned to world Y from the plain, so every mass that states it lands its bands at the same
    heights — the datum that makes three buildings read as one facility."""
    stack = {"ending": "repeat", "bands": [{"material": m, "thickness": t} for m, t in bands]}
    return {"kind": "layered", "axis": "height", "from": PLAIN, "stack": stack}


# A stack's last band claims everything past it, so a cycle is written out band by band, never implied.
MARKING = by_height(*[(material, 4) for _ in range(8) for material in (ACCENT, FRAME)])
STOREYS = by_height(*[(material, courses) for _ in range(6)
                      for material, courses in ((SKIN, 2), (GLASS, 2), (SKIN, 1))])


def theme(wall, rim=FRAME, surface=ROOF, fill=FRAME):
    return {"bedrock": {"relative": False, "value": 1}, "rimEdges": "boundary", "wallOnTerrainFaces": True,
            "rim": {"enabled": True, "depth": 1, "material": rim},
            "surface": {"enabled": True, "depth": 1, "material": surface},
            "wall": wall, "wallEnabled": True, "fill": fill}


THEMES = {
    "moor": moor(),
    # The façade is one material: a pier every BAY blocks round the perimeter, and the storey bands between.
    "facade": theme({"kind": "wallRun", "runs": [{"material": FRAME, "width": 1},
                                                 {"material": STOREYS, "width": BAY - 1}]}),
    "slab": theme(FRAME),
    # A lintel is the storey bands with no pier: it stands in a bay, and its own perimeter is not the wall's.
    "lintel": theme(STOREYS),
    "frame": theme(FRAME, surface=FRAME),
    "plant": theme(PLANT, rim=PLANT, surface=PLANT, fill=PLANT),
    "tank": theme(by_height((FRAME, 5), (ACCENT, 1), (FRAME, 1)), surface=FRAME),
    "mast": theme(by_height((METAL, 33), (ACCENT, 2)), rim=ACCENT, surface=ACCENT, fill=METAL),
    "plinth": theme(SOLID(98), rim=SOLID(98, 3), surface=SOLID(98), fill=SOLID(98)),
    "drum": theme(SKIN, rim=FRAME, surface=FRAME),
    "dome": theme(METAL, rim=METAL, surface=METAL, fill=METAL),
    # The relay mast's paint is a band every four courses along world Y: aviation marking, and one material.
    "lattice": theme(MARKING, rim=MARKING, surface=MARKING, fill=MARKING),
    "steel": theme(METAL, rim=METAL, surface=METAL, fill=METAL),
    "fence": theme(SOLID(101), rim=SOLID(101), surface=SOLID(101), fill=SOLID(101)),
    # The pile's paints: one a part, which is what a programme looks like before anyone names a family.
    "pile-brick": theme(SOLID(98), rim=SOLID(98), surface=SOLID(98), fill=SOLID(98)),
    "pile-planks": theme(SOLID(5), rim=SOLID(5), surface=SOLID(5), fill=SOLID(5)),
    "pile-glass": theme(SOLID(20), rim=SOLID(20), surface=SOLID(20), fill=SOLID(20)),
    "pile-wool": theme(SOLID(35, 14), rim=SOLID(35, 14), surface=SOLID(35, 14), fill=SOLID(35, 14)),
    "pile-cobble": theme(SOLID(4), rim=SOLID(4), surface=SOLID(4), fill=SOLID(4)),
    "pile-gold": theme(SOLID(41), rim=SOLID(41), surface=SOLID(41), fill=SOLID(41)),
    "pile-fence": theme(SOLID(85), rim=SOLID(85), surface=SOLID(85), fill=SOLID(85)),
}


def rect(shape_id, x0, z0, x1, z1, floor=0, height=1, theme="facade", **words):
    """A rectangle over the cells x0..x1, z0..z1 inclusive."""
    out = {"id": shape_id, "type": "rectangle", "operation": "add", "floor": floor, "base_height": height,
           "min_x": x0, "min_z": z0, "max_x": x1 + 1, "max_z": z1 + 1, "theme": theme}
    out.update(words)
    return out


def disc(shape_id, cx, cz, radius, floor=0, height=1, theme="tank", **words):
    out = {"id": shape_id, "type": "circle", "operation": "add", "floor": floor, "base_height": height,
           "center_x": cx, "center_z": cz, "radius": radius, "theme": theme}
    out.update(words)
    return out


def ring(cx, cz, outer, inner, gap=None, points=64):
    """An annulus as one even-odd outline, or — with `gap`, a (bearing, width in blocks) — a C that leaves
    the gap open: an opening in a round wall is ground nobody drew on, never a subtract."""
    if gap is None:
        def circle(radius, reverse=False):
            order = range(points - 1, -1, -1) if reverse else range(points)
            return [[round(cx + radius * math.cos(2 * math.pi * k / points), 2),
                     round(cz + radius * math.sin(2 * math.pi * k / points), 2)] for k in order]
        out, hole = circle(outer), circle(max(0.5, inner), reverse=True)
        return out + [out[0]] + hole + [hole[0]]
    bearing, width = gap
    def arc(radius, reverse=False):
        half = min(math.pi * 0.95, (width / 2) / max(radius, 0.5))
        a0, a1 = bearing + half, bearing + 2 * math.pi - half
        steps = [a0 + (a1 - a0) * k / points for k in range(points + 1)]
        if reverse:
            steps.reverse()
        return [[round(cx + radius * math.cos(a), 2), round(cz + radius * math.sin(a), 2)] for a in steps]
    return arc(outer) + arc(max(0.5, inner), reverse=True)


def polygon(shape_id, vertices, floor=0, height=1, theme="dome"):
    return {"id": shape_id, "type": "polygon", "operation": "add", "floor": floor, "base_height": height,
            "vertices": vertices, "theme": theme}


class Made:
    """One made thing as named layers. A layer is a mass, or one height's worth of slabs across every mass:
    two masses that touch on one layer fuse, and a wall inside a fused footprint has no place on the
    perimeter, so the façade's stripe cycle reads it as a pier from the ground to the parapet."""

    def __init__(self, name, lintel="lintel"):
        self.name, self.layers, self.lintel = name, {}, lintel

    def put(self, layer, *shapes):
        self.layers.setdefault(layer, []).extend(shapes)

    def mass(self, key, x0, z0, bays_x, bays_z, storeys):
        """A block on the module: its walls and ground floor on a layer of its own, one slab a storey on
        the layer every mass's slab at that height shares. Answers its cell bounds and wall height."""
        x1, z1 = x0 + bays_x * BAY, z0 + bays_z * BAY
        height = storeys * STOREY + 2                       # the storeys, the roof slab and a parapet
        self.put(key, rect(f"{key}-walls", x0, z0, x1, z1, height=height),
                 rect(f"{key}-floor", x0 + 1, z0 + 1, x1 - 1, z1 - 1, theme="slab", override=True))
        for storey in range(1, storeys + 1):
            self.put(f"slab-{storey}", rect(f"{key}-slab-{storey}", x0 + 1, z0 + 1, x1 - 1, z1 - 1,
                                            floor=storey * STOREY, theme="slab"))
        return (x0, z0, x1, z1), height

    def door(self, key, layer, x0, z0, x1, z1, top, head=4, floor=0):
        """A sill and a lintel. The sill is a one-course override on the wall's own layer, which replaces the
        wall's column with the floor course; the lintel is the wall above the head, and since that is a
        second span over the same column it goes on the layer every door's lintel shares. An override floored
        at the head would not do both: an override standing in a wall keeps the wall from its own floor."""
        self.put(layer, rect(f"{key}-sill", x0, z0, x1, z1, floor=floor, theme="slab", override=True))
        self.put("lintels", rect(f"{key}-lintel", x0, z0, x1, z1, floor=head, height=top - head,
                                 theme=self.lintel))

    def build(self, mirrors=False, seat=None):
        out = []
        for key, shapes in self.layers.items():
            for shape in shapes:
                shape["id"] = f"{self.name}-{shape['id']}"
            layer_id = f"{self.name}-{key}"
            out.append({"id": layer_id, "name": layer_id, "base_y": PLAIN, "kind": "made",
                        "part_of": self.name, **({"seat": seat} if seat else {}),
                        "layout": {"shapes": shapes, "groups": [{"id": layer_id, "name": layer_id,
                                   "mirrors": mirrors, "shapeIds": [s["id"] for s in shapes]}]}})
        return out


def station(cx, cz):
    """Three masses on one grid — a two-storey hall, a one-storey annex against its south face, a four-storey
    stair tower against its west end — and the equipment that says what the place is for."""
    made = Made("station")
    (hx0, hz0, hx1, hz1), hall = made.mass("hall", cx - 16, cz - 12, 8, 4, 2)
    (ax0, az0, ax1, az1), annex = made.mass("annex", cx, hz1 + 1, 4, 3, 1)
    (tx0, tz0, tx1, tz1), tower = made.mass("tower", hx0 - 9, hz0 + 4, 2, 2, 4)
    # Doors sit in a bay, never on a pier, and a door through two abutting walls is one on each.
    made.door("entry", "annex", ax0 + 5, az1, ax0 + 7, az1, annex)
    made.door("hall-south", "hall", ax0 + 5, hz1, ax0 + 7, hz1, hall)
    made.door("annex-north", "annex", ax0 + 5, az0, ax0 + 7, az0, annex)
    made.door("tower-east", "tower", tx1, tz0 + 1, tx1, tz0 + 3, tower)
    made.door("hall-west", "hall", hx0, tz0 + 1, hx0, tz0 + 3, hall)
    made.put("annex", rect("canopy", ax0 + 4, az1 + 1, ax0 + 8, az1 + 3, floor=4, theme="frame"))
    # A stair in the hall's north-east bays, one course a cell, and the first floor left open over it.
    for step in range(4):
        made.put("hall", rect(f"step-{step}", hx1 - 8 + step, hz0 + 1, hx1 - 8 + step, hz0 + 2,
                              height=step + 2, theme="frame", override=True))
    made.layers["slab-1"] = [s for s in made.layers["slab-1"] if s["id"] != "hall-slab-1"] + [
        rect("hall-slab-1-w", hx0 + 1, hz0 + 1, hx1 - 9, hz1 - 1, floor=STOREY, theme="slab"),
        rect("hall-slab-1-e", hx1 - 8, hz0 + 3, hx1 - 1, hz1 - 1, floor=STOREY, theme="slab"),
        rect("hall-slab-1-ne", hx1 - 4, hz0 + 1, hx1 - 1, hz0 + 2, floor=STOREY, theme="slab")]
    # Plant stands on the roof course, two bays back from the parapet, where it does not break the skyline.
    made.put("plant", rect("plant-a", hx0 + 9, hz0 + 5, hx0 + 11, hz0 + 7, floor=hall - 1, height=2, theme="plant"),
             rect("plant-b", hx0 + 13, hz0 + 5, hx0 + 15, hz0 + 7, floor=hall - 1, height=2, theme="plant"),
             rect("dish-post", hx1 - 6, hz0 + 8, hx1 - 6, hz0 + 8, floor=hall - 1, height=3, theme="frame"))
    # The dish is a field that falls inward — rim high, middle low — so it is rings, one course thick each.
    for radius in range(4, 0, -1):
        top = hall + 2 + round(3 * (radius / 4) ** 2)
        made.put("dish", polygon(f"dish-{radius}", ring(hx1 - 5.5, hz0 + 8.5, radius + 0.5, radius - 0.5),
                                 floor=top - 1, theme="frame"))
    made.put("mast", rect("mast", tx0 + 4, tz0 + 4, tx0 + 4, tz0 + 4, floor=tower - 1, height=14, theme="mast"))
    # Two tanks in the yard east of the annex, on its grid lines: a drum and a domed head, one layer.
    for k, (tank_x, tank_z) in enumerate([(ax1 + 7, az0 + 3), (ax1 + 7, az0 + 10)]):
        made.put("tanks", disc(f"tank-{k}", tank_x, tank_z, 3, height=9),
                 disc(f"tank-{k}-head", tank_x, tank_z, 2, height=10),
                 disc(f"tank-{k}-crown", tank_x, tank_z, 1, height=11))
    return made.build()


def pile(cx, cz):
    """The same programme with none of the four decisions made: sizes off no grid, a paint a part, windows
    as strips stuck on the wall, and a dome drawn on the roof's own layer."""
    made = Made("pile")
    made.put("body",
             rect("hall", cx - 15, cz - 11, cx + 14, cz + 2, height=11, theme="pile-brick"),
             rect("hall-in", cx - 14, cz - 10, cx + 13, cz + 1, theme="pile-brick", override=True),
             rect("annex", cx - 2, cz + 5, cx + 11, cz + 14, height=6, theme="pile-planks"),
             rect("tower", cx - 24, cz - 6, cx - 18, cz + 1, height=19, theme="pile-cobble"),
             # the dome and the roof it stands on are one layer, so the taller add takes the roof's columns
             disc("dome-1", cx - 4, cz - 5, 5, floor=10, height=3, theme="pile-gold"),
             disc("dome-2", cx - 4, cz - 5, 3, floor=10, height=5, theme="pile-gold"),
             disc("tank", cx + 18, cz + 9, 3, height=7, theme="pile-wool"),
             disc("tank-2", cx + 21, cz - 2, 2, height=10, theme="pile-wool"))
    made.put("roof", rect("hall-roof", cx - 15, cz - 11, cx + 14, cz + 2, floor=11, theme="pile-planks"))
    made.put("windows", *[rect(f"window-{k}", cx - 13 + k * 7, cz + 3, cx - 10 + k * 7, cz + 3, floor=3, height=3,
                               theme="pile-glass") for k in range(4)])
    made.put("mast", rect("mast", cx - 21, cz - 3, cx - 21, cz - 3, floor=21, height=9, theme="pile-fence"))
    return made.build()


def observatory(cx, cz):
    """The round version of the method: a plinth, a drum and a dome, each a span over the one below it and so
    a layer each, with a door and a slit that are gaps rather than cuts, and a telescope compiled because a
    tilted tube is not a thing shapes can say."""
    made = Made("observatory", lintel="drum")
    made.put("plinth", disc("plinth", cx + 0.5, cz + 0.5, 12.5, height=2, theme="plinth"),
             rect("steps", cx - 2, cz + 13, cx + 3, cz + 14, height=1, theme="plinth"))
    # The drum is a ring one block thick on the plinth, and its door a sill and a lintel like any other.
    drum_top = 2 + 8
    made.put("drum", polygon("drum", ring(cx + 0.5, cz + 0.5, 8.5, 7.5), floor=2, height=8, theme="drum"),
             # a cornice one block proud at the drum's head: its own columns, so the drum's own layer
             polygon("cornice", ring(cx + 0.5, cz + 0.5, 9.5, 8.5), floor=9, theme="frame"))
    made.door("door", "drum", cx - 1, cz + 8, cx + 1, cz + 8, drum_top, head=6, floor=2)
    # The dome: one ring per block of radius, its floor and top both taken off a shell as wide as the drum,
    # and a slit three blocks wide facing south — a gap between the two ends of each ring, never a cut.
    radius, thickness = 8.5, 1.6
    for r in range(8, 0, -1):
        top = math.sqrt(max(0.0, radius * radius - r * r))
        floor = math.sqrt(max(0.0, (radius - thickness) ** 2 - r * r))
        made.put("dome", polygon(f"dome-{r}", ring(cx + 0.5, cz + 0.5, r + 0.5, max(0.0, r - 0.5),
                                                  gap=(math.pi / 2, 3)),
                                 floor=drum_top + round(floor), height=max(1, round(top) - round(floor) + 1)))
    # The telescope: a tube from the pier to the slit, compiled — its runs go on layers of its own.
    tube = solid.union(solid.beam((cx + 0.5, PLAIN + 3, cz - 1.5), (cx + 0.5, PLAIN + 14, cz + 5.5), 1.2),
                       solid.box(cx, cx + 1, PLAIN + 2, PLAIN + 4, cz - 3, cz - 1))
    compiled = compiler.compile_layers({cell: "steel" for cell in tube.cells()}, prefix="scope-",
                                       layer_prefix="observatory-scope-", group_name="observatory-scope",
                                       part_of="observatory", mirrors=False)
    return made.build() + compiled


def relay(cx, cz):
    """A lattice mast: four legs raking in, a cross brace every section, a platform and a whip, compiled from
    a solid. Its paint is one material banded along world Y, so the runs split on air alone."""
    parts, base, sections, top = [], PLAIN, 5, PLAIN + 40
    for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        parts.append(solid.beam((cx + 5 * sx, base, cz + 5 * sz), (cx + 1.5 * sx, top, cz + 1.5 * sz), 0.6, square=True))
    for s in range(1, sections + 1):
        y0, y1 = base + (s - 1) * 8, base + s * 8
        def at(y, sx, sz):
            k = (y - base) / (top - base)
            half = 5 - 3.5 * k
            return (cx + half * sx, y, cz + half * sz)
        for a, b in (((-1, -1), (1, -1)), ((1, -1), (1, 1)), ((1, 1), (-1, 1)), ((-1, 1), (-1, -1))):
            parts.append(solid.beam(at(y0, *a), at(y1, *b), 0.5))
            parts.append(solid.beam(at(y1, *a), at(y1, *b), 0.5))
    parts.append(solid.box(cx - 3, cx + 3, top, top, cz - 3, cz + 3))
    body = solid.union(*parts)
    whip = solid.box(cx, cx, top + 1, top + 9, cz, cz)
    model = {cell: "lattice" for cell in body.cells()}
    model.update({cell: "steel" for cell in whip.cells()})
    compiled = compiler.compile_layers(model, prefix="relay-", layer_prefix="relay-run-", group_name="relay",
                                       part_of="relay", mirrors=False)
    # The hut and the compound are drawn: a mass on the same module as the station, and a fence ring.
    made = Made("relay-base")
    (x0, z0, x1, z1), hut = made.mass("hut", cx + 6, cz + 5, 2, 1, 1)
    made.door("hut-door", "hut", x0 + 1, z1, x0 + 3, z1, hut)
    made.put("fence", polygon("fence", ring(cx + 4.5, cz + 4.5, 15.5, 14.5, gap=(math.pi / 2, 4)), height=2,
                              theme="fence"))
    return compiled + made.build(), model


def one_layer(cx, cz):
    """The station's hall and annex with the two shortcuts the method refuses: both masses on one layer, so
    they fuse and the wall between them leaves the perimeter, and doors made by one override floored at the
    head, which keeps the wall it was meant to open."""
    made = Made("one-layer")
    x0, z0 = cx - 16, cz - 14
    hall, annex = 2 * STOREY + 2, STOREY + 2
    made.put("masses",
             rect("hall-walls", x0, z0, x0 + 32, z0 + 16, height=hall),
             rect("hall-floor", x0 + 1, z0 + 1, x0 + 31, z0 + 15, theme="slab", override=True),
             rect("annex-walls", x0 + 16, z0 + 16, x0 + 32, z0 + 28, height=annex),
             rect("annex-floor", x0 + 17, z0 + 17, x0 + 31, z0 + 27, theme="slab", override=True),
             rect("entry", x0 + 21, z0 + 28, x0 + 23, z0 + 28, floor=4, height=annex - 4, override=True),
             rect("through", x0 + 21, z0 + 16, x0 + 23, z0 + 16, floor=4, height=hall - 4, override=True))
    made.put("slab-1", rect("hall-slab-1", x0 + 1, z0 + 1, x0 + 31, z0 + 15, floor=STOREY, theme="slab"),
             rect("annex-slab-1", x0 + 17, z0 + 17, x0 + 31, z0 + 27, floor=STOREY, theme="slab"))
    made.put("slab-2", rect("hall-slab-2", x0 + 1, z0 + 1, x0 + 31, z0 + 15, floor=2 * STOREY, theme="slab"))
    return made.build()


def seated(cx, cz):
    """An outpost dug into a grade: one mass and a mast, stated with no height at all. `seat` drops every
    layer naming the same `part_of` together, onto the lowest ground under the feet, and cuts the hill out of
    the footprint — so the uphill wall is retained by the hill and the downhill one stands clear."""
    made = Made("outpost")
    (x0, z0, x1, z1), top = made.mass("bunker", cx - 6, cz - 4, 3, 2, 1)
    made.door("door", "bunker", x0 + 5, z1, x0 + 7, z1, top)
    made.put("mast", rect("mast", x0 + 2, z0 + 2, x0 + 2, z0 + 2, floor=top - 1, height=14, theme="mast"))
    return made.build(seat="ground")


def ramp(cx, z0):
    """Two facing bands, y20 along the north edge and y8 along the south, so the pad between is one grade."""
    half = PANEL_W / 2 - 4
    def band(mark_id, height, z_from, z_to):
        return {"id": mark_id, "kind": "area", "h": height, "bevel": 0,
                "ring": [[cx - half, z_from], [cx + half, z_from], [cx + half, z_to], [cx - half, z_to]]}
    return [band("fell", 20, z0 + 4, z0 + 14), band("dale", 8, z0 + PANEL_D - 14, z0 + PANEL_D - 4)]


PANELS = [("pile", pile), ("station", station), ("observatory", observatory), ("relay", relay),
          ("one-layer", one_layer), ("seated", seated)]

shapes, groups, relief, layers, relay_model = [], [], {}, [], None
for index, (name, emit) in enumerate(PANELS):
    x0, z0 = COL_X[index % 2], ROW_Z[index // 2]
    cx, cz = x0 + PANEL_W // 2, z0 + PANEL_D // 2
    shapes.append({"id": f"pad-{name}", "type": "rectangle", "operation": "add", "floor": 0,
                   "base_height": PLAIN, "theme": "moor",
                   "min_x": x0, "min_z": z0, "max_x": x0 + PANEL_W, "max_z": z0 + PANEL_D})
    groups.append({"id": name, "name": name, "mirrors": False, "shapeIds": [f"pad-{name}"]})
    relief[name] = {"base": PLAIN, "reach": 0, "step": 1, "pushes": [],
                    "marks": ramp(cx, z0) if name == "seated" else []}
    built = emit(cx, cz)
    if name == "relay":
        built, relay_model = built
    layers.extend(built)

layout = {
    "setup": {"bbox": {"min_x": COL_X[0] - 8, "max_x": COL_X[-1] + PANEL_W + 8,
                       "min_z": ROW_Z[0] - 8, "max_z": ROW_Z[-1] + PANEL_D + 8},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": THEMES,
    "mapTheme": "moor",
    "relief": relief,
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0, "layout": {"shapes": shapes, "groups": groups}}]
              + layers,
}
out = os.path.join(HERE, "designing-a-structure.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(PANELS)} panels, {len(layout['layers'])} layers -> {out}")
for name, _ in PANELS:
    owner = {"one-layer": "one-layer", "seated": "outpost"}.get(name, name)
    mine = [l for l in layers if l.get("part_of", "").startswith(owner)]
    print(f"  {name:12s} {len(mine):3d} layer(s) {sum(len(l['layout']['shapes']) for l in mine):4d} shape(s)")
stats = compiler.stats(relay_model, [l for l in layers if l["id"].startswith("relay-run-")])
print(f"  relay compiled: {stats}")
