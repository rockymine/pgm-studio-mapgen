"""Writes a-research-campus.layout.json — one facility of seven buildings in five styles, and the detail each
style is built to.

The site states one language every building shares — one ground, one paving family, one accent pair (a safety
orange and a blue glass) and one datum at the plain — and each building states a style inside it: a curtain-
walled laboratory with fins, a glazed lobby and a dish on its roof; two brick administration houses from the
house stamper; a barrel-vaulted hangar; a lattice signal tower with platforms, a ladder, a cabin and a radar; a
ribbed glass biodome; a tank farm joined to the laboratory by a pipe rack; and a fenced perimeter with a gate.

What is drawn is drawn with `techniques/made.py`, which is the method `designing-a-structure` measures; what
cannot be drawn — the tower, the dish, the vault, the trees — is a voxel model compiled by run index with
`tools/sculpt/layers.py`, several materials at once.
"""
import copy, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools", "sculpt"))
from cards import SOLID, moor
from made import Made, by_height, disc, one, polygon, rect, ring, theme
import layers as compiler
import solid

PLAIN = 8                 # the plain's top block is y7, so a made layer rests at base_y 8
BAY, STOREY = 4, 5

# ── the site's language ──────────────────────────────────────────────────────────────────────────────────
# Ground is the moor. The built family is a white frame, a grey-teal skin and a grey roof; the old houses are
# brick, the hangar stone and andesite under a green clay vault. The accent is one orange and one blue glass, on every building.
FRAME, SKIN, GLASS, ROOF = SOLID(155), SOLID(159, 9), SOLID(95, 3), SOLID(1, 6)
ACCENT, METAL, BARS, LAMP = SOLID(159, 1), SOLID(42), SOLID(101), SOLID(89)
CLAY, ANDESITE, STONEBRICK = SOLID(159, 13), SOLID(1, 5), SOLID(98)


def pinned(*bands):
    return by_height(*bands, start=PLAIN)


STOREYS = pinned(*[(m, c) for _ in range(6) for m, c in ((SKIN, 2), (GLASS, 2), (SKIN, 1))])
# The lobby is glass floor to ceiling between its mullions: one course of frame at each slab line.
CURTAIN = pinned(*[(m, c) for _ in range(4) for m, c in ((FRAME, 1), (GLASS, 4))])
# The plant room reads as louvres: a course of andesite, a course of bars, all the way up.
LOUVRE = pinned(*[(m, 1) for _ in range(20) for m in (ANDESITE, BARS)])
MARKING = pinned(*[(m, 4) for _ in range(12) for m in (ACCENT, FRAME)])
# Corrugation is a stripe round the perimeter, one block of clay to one of andesite.
CORRUGATED = {"kind": "wallRun", "runs": [{"material": SOLID(1), "width": 1}, {"material": ANDESITE, "width": 1}]}

THEMES = {
    "moor": moor(),
    "road": theme(ANDESITE, ANDESITE, {"kind": "cell", "cellSize": 9, "palette": [ANDESITE, SOLID(13), SOLID(4)]},
                  SOLID(1)),
    "plaza": theme(STONEBRICK, STONEBRICK, {"kind": "checker", "size": 3, "even": STONEBRICK,
                                            "odd": SOLID(98, 3)}, SOLID(1)),
    "facade": theme({"kind": "wallRun", "runs": [{"material": FRAME, "width": 1},
                                                 {"material": STOREYS, "width": BAY - 1}]}, FRAME, ROOF, FRAME),
    "curtain": theme({"kind": "wallRun", "runs": [{"material": FRAME, "width": 1},
                                                  {"material": CURTAIN, "width": BAY - 1}]}, FRAME, ROOF, FRAME),
    "louvre": theme({"kind": "wallRun", "runs": [{"material": FRAME, "width": 1},
                                                 {"material": LOUVRE, "width": BAY - 1}]}, FRAME, ROOF, FRAME),
    "lintel": theme(STOREYS, FRAME, ROOF, FRAME),
    "slab": theme(FRAME, FRAME, ROOF, FRAME),
    "frame": one(FRAME),
    "skin": one(SKIN),
    "glass": one(GLASS),
    "clear": one(SOLID(20)),
    "accent": one(ACCENT),
    "steel": one(METAL),
    "bars": one(BARS),
    "lamp": one(LAMP),
    "grating": one(ANDESITE),
    "ladder": one(SOLID(65, 3)),
    "lattice": theme(MARKING, MARKING, MARKING, MARKING),
    "tank": theme(pinned((FRAME, 3), (ACCENT, 1), (FRAME, 4), (ACCENT, 1), (FRAME, 20)), FRAME, FRAME, FRAME),
    "shed": theme(CORRUGATED, ANDESITE, ANDESITE, ANDESITE),
    "vault": one(CLAY),
    "rib": one(SOLID(1, 6)),
    "log": one(SOLID(17, 0)),
    "leaves": one(SOLID(18, 0)),
    "fence": one(BARS),
}


# ── the laboratory: curtain wall, fins, a glazed lobby, a plant room and a dish ──────────────────────────
def laboratory(made):
    (x0, z0, x1, z1), top = made.mass("lab", -36, -70, 18, 5, 3)
    # The lobby is two storeys of glass with no floor between them, abutting the lab's south face.
    (lx0, lz0, lx1, lz1), lobby = made.mass("lobby", -12, z1 + 1, 6, 3, 2, facade="curtain")
    made.layers["slab-1"] = [s for s in made.layers["slab-1"] if s["id"] != "lobby-slab-1"]
    made.door("lobby-entry", "lobby", -3, lz1, -1, lz1, lobby, head=8)
    made.door("lobby-entry-2", "lobby", 1, lz1, 3, lz1, lobby, head=8)
    made.door("lab-lobby", "lab", -3, z1, -1, z1, top)
    made.door("lobby-lab", "lobby", -3, lz0, -1, lz0, lobby, head=4)
    made.door("lab-east", "lab", x1, z0 + 9, x1, z0 + 11, top)
    # A canopy over the entry, cantilevered off the lobby at its head, with a fascia in the accent.
    made.put("lobby", rect("canopy", -8, lz1 + 1, 8, lz1 + 4, floor=9, theme="frame"))
    made.put("canopy-fascia", rect("fascia", -8, lz1 + 5, 8, lz1 + 5, floor=9, theme="accent"))
    # Fins: one block proud of the wall at every pier, on a layer of their own so they do not join the
    # wall's footprint and re-number the stripe cycle the façade is painted round.
    fins = []
    for k in range(19):
        x = x0 + k * BAY
        fins.append(rect(f"fin-n-{k}", x, z0 - 1, x, z0 - 1, height=top, theme="frame"))
        if not lx0 <= x <= lx1:
            fins.append(rect(f"fin-s-{k}", x, z1 + 1, x, z1 + 1, height=top, theme="frame"))
    made.put("fins", *fins)
    # The plant room stands on the roof two bays back from every parapet, and its own slab is its own layer.
    made.mass("plant", -8, z0 + 4, 4, 3, 1, facade="louvre", floor=top - 1, slabs="plant-slab")
    # Three whip antennas at the west end, and a lamp on each.
    for k, x in enumerate((x0 + 6, x0 + 10, x0 + 14)):
        made.put("antennas", rect(f"whip-{k}", x, z0 + 4, x, z0 + 4, floor=top - 1, height=8 + 3 * k, theme="bars"))
        made.put("antenna-lamps", rect(f"whip-lamp-{k}", x, z0 + 4, x, z0 + 4, floor=top + 7 + 3 * k, theme="lamp"))
    return (x0, z0, x1, z1), top


def dish_model(cx, base_y, cz, radius=7, tilt=35):
    """A dish on a yoke on a trussed pedestal. The dish is a paraboloid shell tilted toward the south; the
    feed is a tripod meeting at the focus. Answers `{(x, y, z): material}`."""
    model = {}
    def paint(body, material):
        for cell in body.cells():
            model[cell] = material
    paint(solid.box(cx - 2, cx + 2, base_y, base_y, cz - 2, cz + 2), "grating")
    for sx, sz in ((-2, -2), (2, -2), (2, 2), (-2, 2)):
        paint(solid.beam((cx + sx + 0.5, base_y + 1, cz + sz + 0.5), (cx + 0.5, base_y + 6, cz + 0.5), 0.5), "steel")
    paint(solid.box(cx, cx, base_y + 5, base_y + 8, cz, cz), "steel")
    # The bowl: points whose depth along the tilted axis is within one block of the paraboloid.
    a = math.radians(tilt)
    hub = (cx + 0.5, base_y + 11.0, cz + 0.5)
    ax, ay, az = 0.0, math.cos(a), math.sin(a)                     # the dish's axis, leaning south
    focal = radius * radius / (4 * 3.0)
    for x in range(cx - radius - 1, cx + radius + 2):
        for y in range(base_y + 3, base_y + 20):
            for z in range(cz - radius - 2, cz + radius + 3):
                px, py, pz = x + 0.5 - hub[0], y + 0.5 - hub[1], z + 0.5 - hub[2]
                along = px * ax + py * ay + pz * az
                rx, ry, rz = px - along * ax, py - along * ay, pz - along * az
                r = math.sqrt(rx * rx + ry * ry + rz * rz)
                if r <= radius and abs(along - r * r / (4 * focal)) <= 0.6:
                    model[(x, y, z)] = "frame" if r > radius - 1 else "steel"
    focus = (hub[0] + ax * focal, hub[1] + ay * focal, hub[2] + az * focal)
    for angle in (0, 120, 240):
        t = math.radians(angle)
        # a point on the rim in the dish's own plane
        ux, uy, uz = math.cos(t), -math.sin(t) * az, math.sin(t) * ay
        rim = (hub[0] + ux * (radius - 1), hub[1] + uy * (radius - 1) + ay * 3, hub[2] + uz * (radius - 1) + az * 3)
        paint(solid.beam(rim, focus, 0.45), "bars")
    paint(solid.sphere(*focus, 0.9), "accent")
    return model


# ── the hangar: corrugated walls, a barrel vault with ribs, a door the width of three bays ────────────────
def hangar_model(x0, z0, width=37, length=41, eaves=7, rise=9):
    """A barrel vault spanning x over walls `eaves` high, its axis along z. The end walls follow the arch,
    the vault is one course of clay with a rib of andesite standing proud every four blocks, and the south
    end carries a door three bays wide. Answers the model and the door's cell range."""
    model = {}
    half = (width - 1) / 2
    cx = x0 + half
    def arch(x):
        return PLAIN + eaves + rise * math.sqrt(max(0.0, 1 - ((x - cx) / (half + 0.5)) ** 2))
    door = (int(cx) - 6, int(cx) + 6, PLAIN + 11)
    for x in range(x0, x0 + width):
        crown = int(round(arch(x)))
        for z in range(z0, z0 + length):
            end = z in (z0, z0 + length - 1)
            side = x in (x0, x0 + width - 1)
            if side or end:
                for y in range(PLAIN, crown + 1):
                    if end and z == z0 + length - 1 and door[0] <= x <= door[1] and PLAIN < y < door[2]:
                        continue
                    model[(x, y, z)] = "shed"
            else:
                model[(x, PLAIN, z)] = "grating"
                model[(x, crown, z)] = "vault"
                if (z - z0) % 4 == 0:
                    model[(x, crown + 1, z)] = "rib"
        # clerestory: the vault's glazing band, two blocks of glass either side of the crown
        if abs(x - cx) <= 2:
            for z in range(z0 + 2, z0 + length - 2):
                if (z - z0) % 4:
                    model[(x, crown, z)] = "glass"
    # a lintel over the door in the accent, the whole width of the opening
    for x in range(door[0], door[1] + 1):
        model[(x, door[2], z0 + length - 1)] = "accent"
    return model


# ── the signal tower: a lattice with platforms, a ladder, railings, a cabin, a radar and lamps ─────────────
def tower_model(cx, cz, height=56):
    model = {}
    def paint(body, material):
        for cell in body.cells():
            model[cell] = material
    base, top = PLAIN, PLAIN + height
    def half_at(y):
        return 5.5 - 3.0 * (y - base) / (top - base)
    def corner(y, sx, sz):
        h = half_at(y)
        return (cx + 0.5 + h * sx, y, cz + 0.5 + h * sz)
    corners = ((-1, -1), (1, -1), (1, 1), (-1, 1))
    for sx, sz in corners:
        paint(solid.beam(corner(base, sx, sz), corner(top, sx, sz), 0.55, square=True), "lattice")
    sections = [base + k * 8 for k in range(8)]
    for y0 in sections[:-1]:
        y1 = y0 + 8
        for (ax, az), (bx, bz) in zip(corners, corners[1:] + corners[:1]):
            paint(solid.beam(corner(y0, ax, az), corner(y1, bx, bz), 0.45), "lattice")
            paint(solid.beam(corner(y0, bx, bz), corner(y1, ax, az), 0.45), "lattice")
            paint(solid.beam(corner(y1, ax, az), corner(y1, bx, bz), 0.45), "lattice")
    # Two rest platforms and the top deck, each with a railing and a hatch the ladder comes up through.
    for y in (base + 24, base + 40, top):
        h = int(half_at(y)) + 2
        paint(solid.box(cx - h, cx + h, y, y, cz - h, cz + h), "grating")
        rail = solid.box(cx - h, cx + h, y + 1, y + 1, cz - h, cz + h) - \
            solid.box(cx - h + 1, cx + h - 1, y + 1, y + 1, cz - h + 1, cz + h - 1)
        paint(rail, "bars")
        for cell in solid.box(cx, cx, y, y + 1, cz + 1, cz + 1).cells():
            model.pop(cell, None)
    # The ladder: up the middle of the tower on the south face of a spine, from the ground to the deck.
    paint(solid.box(cx, cx, base, top - 1, cz, cz), "steel")
    paint(solid.box(cx, cx, base, top - 1, cz + 1, cz + 1), "ladder")
    # The cabin on the deck: a frame, a band of glass, a flat roof and lamps on its corners.
    y = top + 1
    cabin = solid.box(cx - 3, cx + 3, y, y + 4, cz - 3, cz + 3) - solid.box(cx - 2, cx + 2, y, y + 3, cz - 2, cz + 2)
    for (x, yy, z) in cabin.cells():
        model[(x, yy, z)] = "glass" if y + 1 <= yy <= y + 2 and abs(x - cx) < 3 or \
            y + 1 <= yy <= y + 2 and abs(z - cz) < 3 and abs(x - cx) == 3 else "skin"
    for cell in solid.box(cx, cx, y, y + 2, cz + 3, cz + 3).cells():
        model.pop(cell, None)
    paint(solid.box(cx - 3, cx + 3, y + 5, y + 5, cz - 3, cz + 3), "frame")
    for sx, sz in corners:
        model[(cx + 3 * sx, y + 6, cz + 3 * sz)] = "lamp"
    # The radar: a mast off the cabin roof and a long array across it.
    paint(solid.box(cx, cx, y + 6, y + 8, cz, cz), "steel")
    paint(solid.box(cx - 6, cx + 6, y + 9, y + 10, cz, cz), "frame")
    paint(solid.box(cx - 6, cx + 6, y + 9, y + 9, cz - 1, cz - 1), "steel")
    model[(cx, y + 11, cz)] = "lamp"
    return model


# ── the biodome: a hollow glass dome with quartz ribs, a vestibule, and three trees inside ──────────────
def biodome(made, cx, cz, radius=16):
    for r in range(radius, 0, -1):
        top = math.sqrt(max(0.0, radius * radius - r * r))
        floor = math.sqrt(max(0.0, (radius - 1.6) ** 2 - r * r))
        # every fourth ring is a rib, and the springing course is frame all the way round
        paint = "frame" if r % 4 == 0 or r == radius else "clear"
        made.put("dome", polygon(f"dome-{r}", ring(cx + 0.5, cz + 0.5, r + 0.5, max(0.0, r - 0.5)),
                                 floor=round(floor), height=max(1, round(top) - round(floor) + 1), theme=paint))
    made.put("dome", polygon("kerb", ring(cx + 0.5, cz + 0.5, radius + 1.5, radius + 0.5), theme="frame"))
    # The vestibule is a mass on the module, abutting the dome's kerb, with a door through into it.
    (vx0, vz0, vx1, vz1), top = made.mass("vestibule", cx - 4, cz - radius - 10, 2, 2, 1)
    made.door("vest-out", "vestibule", cx - 3, vz0, cx - 1, vz0, top)
    made.door("vest-in", "vestibule", cx - 3, vz1, cx - 1, vz1, top)
    made.put("dome-door", rect("dome-door", cx - 3, vz1 + 1, cx - 1, cz - radius + 2, floor=0, height=1,
                               theme="grating", override=True))


def tree_model(x, z, trunk=6, crown=3.4):
    model = {}
    for cell in solid.box(x, x, PLAIN, PLAIN + trunk, z, z).cells():
        model[cell] = "log"
    for cell in solid.ellipsoid(x + 0.5, PLAIN + trunk + 1, z + 0.5, crown, crown * 0.8, crown).cells():
        model.setdefault(cell, "leaves")
    return model


# ── the tank farm and the pipe rack ─────────────────────────────────────────────────────────────────────
def tank_farm(made, x0, z0):
    for k, (dx, dz) in enumerate(((0, 0), (12, 0), (0, 12), (12, 12))):
        tx, tz = x0 + dx, z0 + dz
        made.put("tanks", disc(f"tank-{k}", tx, tz, 4.5, height=12, theme="tank"),
                 disc(f"tank-{k}-head", tx, tz, 3.5, height=13, theme="tank"),
                 disc(f"tank-{k}-crown", tx, tz, 2, height=14, theme="tank"))
        # a walkway ring round the head, one block proud, on a layer of its own
        made.put("tank-walks", polygon(f"tank-{k}-walk", ring(tx, tz, 5.5, 4.5), floor=11, theme="grating"))
        made.put("tank-rails", polygon(f"tank-{k}-rail", ring(tx, tz, 5.5, 4.5), floor=12, theme="bars"))
    made.put("tank-bund", polygon("bund", [[x0 - 7, z0 - 7], [x0 + 19, z0 - 7], [x0 + 19, z0 + 19], [x0 - 7, z0 + 19],
                                           [x0 - 7, z0 - 7], [x0 - 6, z0 - 6], [x0 - 6, z0 + 18], [x0 + 18, z0 + 18],
                                           [x0 + 18, z0 - 6], [x0 - 6, z0 - 6]], height=2, theme="frame"))


def pipe_rack(made, x, z_from, z_to, x_to):
    """Posts every six blocks, a beam across each, and three pipes on the beams — a layer for each, because a
    post, the beam on it and the pipe on the beam are three spans in one column."""
    posts, beams, pipes = [], [], []
    for k, z in enumerate(range(z_to, z_from + 1, 6)):
        posts += [rect(f"post-{k}-w", x - 2, z, x - 2, z, height=8, theme="steel"),
                  rect(f"post-{k}-e", x + 2, z, x + 2, z, height=8, theme="steel")]
        beams.append(rect(f"beam-{k}", x - 2, z, x + 2, z, floor=8, theme="steel"))
    for k, (dx, paint) in enumerate(((-1, "frame"), (0, "accent"), (1, "steel"))):
        pipes.append(rect(f"pipe-{k}", x + dx, z_to, x + dx, z_from, floor=9, theme=paint))
    # the branch west into the lab's east wall, at the same height
    for k, (dz, paint) in enumerate(((-1, "frame"), (0, "accent"), (1, "steel"))):
        pipes.append(rect(f"branch-{k}", x_to, z_to + dz, x - 2, z_to + dz, floor=9, theme=paint))
    made.put("rack-posts", *posts)
    made.put("rack-beams", *beams)
    made.put("rack-pipes", *pipes)


# ── the perimeter: a fence, a gatehouse, a barrier ──────────────────────────────────────────────────────
def perimeter(made, x0, z0, x1, z1, gate):
    g0, g1 = gate
    outline = [[g1 + 1, z1 + 1], [x1 + 1, z1 + 1], [x1 + 1, z0], [x0, z0], [x0, z1 + 1], [g0, z1 + 1],
               [g0, z1], [x0 + 1, z1], [x0 + 1, z0 + 1], [x1, z0 + 1], [x1, z1], [g1 + 1, z1]]
    made.put("fence", polygon("fence", outline, height=2, theme="fence"))
    (hx0, hz0, hx1, hz1), top = made.mass("gatehouse", g1 + 3, z1 - 6, 2, 1, 1)
    made.door("gatehouse-door", "gatehouse", hx0, hz0 + 1, hx0, hz0 + 3, top)
    made.put("barrier", rect("barrier-post", g1 + 1, z1 - 2, g1 + 1, z1 - 2, height=3, theme="frame"))
    made.put("barrier-arm", rect("barrier-arm", g0, z1 - 2, g1, z1 - 2, floor=2, theme="accent"))


# ── the administration houses: the house stamper, a brick style forked from a shipped one ───────────────
def brick_style():
    style = json.load(open(os.path.join(os.path.dirname(HERE), "a-house-and-its-wings", "bothy.style.json")))
    shell = copy.deepcopy(style)["shell"]
    brick = {"ending": "repeat", "bands": [{"thickness": 1, "material": SOLID(45)}]}
    banded = {"ending": "repeat", "bands": [{"thickness": 4, "material": SOLID(45)},
                                            {"thickness": 1, "material": STONEBRICK}]}
    shell["wall"]["stack"] = brick
    for storey in shell["storeys"]:
        storey["wall"]["stack"] = banded
        storey["post"] = STONEBRICK
        storey["windows"].update({"block": 102, "width": 1, "height": 2, "spacing": 2})
    shell["post"] = STONEBRICK
    shell["foundation"]["plate"]["stack"]["bands"][0]["material"] = STONEBRICK
    shell["roof"].update({"form": "hip", "pitch": 1, "overhang": 1,
                          "body": SOLID(5, 5), "verge": STONEBRICK, "gable": SOLID(45)})
    shell["beams"] = {"block": -1}                      # no beams: the ends of timbers a brick house has not got
    style["shell"] = shell
    return style


def houses():
    def house(house_id, wings):
        return {"id": house_id, "kind": "house", "layer": "ground", "seed": 5, "front": "posZ", "style": "brick",
                "wings": wings}
    return [house("admin", [{"corners": [[-96, -42], [-84, -35]], "spec": {"ridge": "alongX"}},
                            {"corners": [[-92, -34], [-87, -28]], "spec": {"ridge": "alongZ", "storeysHigh": 1}}]),
            house("records", [{"corners": [[-78, -40], [-68, -34]], "spec": {"ridge": "alongX"}}])]


# ── the board ───────────────────────────────────────────────────────────────────────────────────────────
made = Made("campus")
lab, lab_top = laboratory(made)
biodome(made, -30, 30)
tank_farm(made, 58, 36)
pipe_rack(made, 44, 30, -60, lab[2] + 1)
perimeter(made, -104, -84, 104, 76, (-4, 4))
drawn = made.build()

compiled = []
def compile_model(name, model):
    built = compiler.compile_layers(model, prefix=f"{name}-", layer_prefix=f"{name}-run-", group_name=name,
                                    part_of=name, mirrors=False)
    compiled.extend(built)
    return compiler.stats(model, built)

stats = {
    "dish": compile_model("dish", dish_model(24, PLAIN + lab_top, -60)),
    "hangar": compile_model("hangar", hangar_model(52, -32)),
    "tower": compile_model("tower", tower_model(-72, 58)),
    "trees": compile_model("trees", {**tree_model(-34, 26), **tree_model(-24, 34, 7, 3.8), **tree_model(-36, 38, 5, 3)}),
}

ground = [
    rect("site", -110, -90, 110, 82, height=PLAIN, theme="moor"),
    # The roads: the spine from the gate to the plaza, a branch to the hangar door and one to the houses.
    rect("spine", -4, -36, 4, 82, height=PLAIN, theme="road"),
    rect("east-road", 5, 12, 72, 18, height=PLAIN, theme="road"),
    rect("hangar-apron", 60, 9, 82, 11, height=PLAIN, theme="road"),
    rect("west-road", -90, -24, -5, -18, height=PLAIN, theme="road"),
    rect("plaza", -20, -36, 20, -26, height=PLAIN, theme="plaza"),
    rect("tower-path", -65, 56, -5, 60, height=PLAIN, theme="road"),
    rect("dome-path", -33, -17, -29, 3, height=PLAIN, theme="road"),
    rect("house-path", -84, -27, -80, -25, height=PLAIN, theme="road"),
]
layout = {
    "setup": {"bbox": {"min_x": -114, "max_x": 114, "min_z": -94, "max_z": 86},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": THEMES,
    "mapTheme": "moor",
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": ground, "groups": [{"id": "site", "name": "site", "mirrors": False,
                                                         "shapeIds": [s["id"] for s in ground]}]}}]
              + drawn + compiled,
    "dressing": {"styles": {"brick": brick_style()}, "props": houses()},
}
out = os.path.join(HERE, "a-research-campus.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(layout['layers'])} layers, {sum(len(l['layout']['shapes']) for l in layout['layers'])} shapes -> {out}")
print(f"  drawn     {len(drawn)} layers {sum(len(l['layout']['shapes']) for l in drawn)} shapes")
for name, got in stats.items():
    print(f"  {name:9s} {got['layers']} layers {got['shapes']} shapes from {got['blocks']} blocks, "
          f"{got['materials']} materials")
