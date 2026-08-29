"""Four sculptures, modelled as solids and compiled to layers.

Nothing here is a special case in the layer system — each is a set of spheres, cylinders, capsules and
extruded outlines, unioned and cut, then handed to `layers.compile_layers`. The point of the four is the
range: a figure with limbs, a vehicle whose body is a profile crossed with a plan, a ring station that is
mostly hollow, and a monument that has to read as a silhouette from the ground. What each costs in layers
and shapes is what `stats` reports, and that number is the whole argument.

Coordinates are the studio's — `x` and `z` in plan, `y` up — and every model is written about its own origin
so a caller places it with one `translate`. Each faces **north**, along `-z`."""
import math

from solid import (Solid, beam, box, cylinder, cylinder_z, difference, ellipsoid, extrude_x,
                   sheet, tube,
                   extrude_z, frustum, half_space, intersect, mirror_x, prism, revolve, revolve_z,
                   rotate_y, shell, sphere, torus, translate, union)


def paint(model, *parts):
    """Lay solids into a `{(x, y, z): material}` model in order, later parts claiming what they cover."""
    for solid, material in parts:
        for cell in solid.cells():
            model[cell] = material
    return model


def _eroded(solid, depth):
    from solid import cells_solid
    cells = solid.cells()
    for _ in range(depth):
        cells = {c for c in cells
                 if (c[0] + 1, c[1], c[2]) in cells and (c[0] - 1, c[1], c[2]) in cells
                 and (c[0], c[1] + 1, c[2]) in cells and (c[0], c[1] - 1, c[2]) in cells
                 and (c[0], c[1], c[2] + 1) in cells and (c[0], c[1], c[2] - 1) in cells}
    return cells_solid(cells)


# ── the robot ─────────────────────────────────────────────────────────────────────────────────────────────

def robot():
    """A cheerful bipedal robot, 34 blocks from sole to antenna tip.

    Proportioned the way a toy is rather than the way a person is: the head is a third of the height, the
    body a barrel under it, and every hinge is a ball, so the limbs read as jointed instead of as sticks. The
    face is a recessed plate — an ellipsoid a shade larger than the head, knifed to the front and cut back
    into it — which is the trick that stops a voxel face reading as paint on a sphere."""
    model = {}

    boot = union(ellipsoid(-5.5, 2.0, -1.5, 3.6, 2.2, 4.4), ellipsoid(-5.5, 3.2, 0.0, 3.2, 2.2, 3.2))
    shin = union(beam((-5.5, 4, 0), (-5.0, 9, 0), 2.5), sphere(-5.0, 9.4, 0, 2.9))
    thigh = beam((-5.0, 9.5, 0), (-4.2, 13.5, 0), 2.7)
    leg = union(boot, shin, thigh)

    pelvis = ellipsoid(0, 15.0, 0, 6.4, 3.2, 4.6)
    torso = ellipsoid(0, 20.0, 0, 7.2, 5.4, 5.2)
    yoke = ellipsoid(0, 23.6, 0, 8.6, 2.6, 5.2)
    belt = intersect(ellipsoid(0, 16.4, 0, 6.8, 1.4, 4.9), box(-9, 9, 15, 18, -9, 9))

    # A panel is a shape *proud* of the body it sits on: its z radius is the larger, so it wins the front
    # face outright. Cut level with the body it would speckle, since two curved surfaces that close cross.
    chest = intersect(ellipsoid(0, 20.2, 0, 4.6, 3.4, 6.0), half_space(0, 0, 1, -2.0))
    vent = union(*[intersect(ellipsoid(0, 20.2, 0, 3.6, 2.8, 6.3), box(-4, 4, y, y, -9, -2))
                   for y in (19, 21)])

    arm = union(
        sphere(8.6, 23.0, 0, 3.0),
        beam((8.8, 22.0, 0), (10.4, 17.0, -0.6), 2.3),
        sphere(10.4, 16.6, -0.6, 2.6),
        beam((10.4, 16.0, -0.6), (10.0, 12.0, -2.4), 2.1),
        ellipsoid(9.8, 10.2, -2.8, 2.9, 2.5, 2.9),
    )

    neck = cylinder(0, 0, 2.8, 24, 26)
    head = ellipsoid(0, 32.0, 0, 7.6, 6.6, 7.0)
    crown = intersect(ellipsoid(0, 32.0, 0, 7.8, 6.8, 7.2), box(-9, 9, 36, 39, -9, 9))

    # A marking on a curved body is that body's own surface grown by a hair and clipped by a box. Any other
    # shape crosses the surface it sits on somewhere and speckles along the crossing, which is what a
    # separately-centred ellipsoid does the moment it leaves the middle of the face.
    def decal(x0, x1, y0, y1, grow=0.35):
        return intersect(ellipsoid(0, 32.0, 0, 7.6 + grow, 6.6 + grow, 7.0 + grow),
                         box(x0, x1, y0, y1, -9, -2))

    visor = decal(-6, 6, 31, 35)
    brow = decal(-6, 6, 36, 36, 0.55)
    eye = decal(2, 5, 32, 34, 0.75)
    grille = union(decal(-4, 4, 28, 28, 0.55), decal(-3, 3, 27, 27, 0.55))

    ear = union(beam((7.2, 32.0, 0), (9.6, 32.0, 0), 2.2), sphere(9.9, 32.0, 0, 1.4))
    antenna = union(beam((0, 38, 0), (0, 42, 0), 1.1), sphere(0, 43.0, 0, 2.0))

    paint(model,
          (union(leg, mirror_x(leg, 0)), "shell"),
          (pelvis, "trim"),
          (union(torso, yoke), "shell"),
          (belt, "trim"),
          (union(arm, mirror_x(arm, 0)), "shell"),
          (union(ear, mirror_x(ear, 0)), "trim"),
          (neck, "joint"),
          (union(head, crown), "shell"),
          (chest, "panel"),
          (vent, "joint"),
          (visor, "visor"),
          (brow, "trim"),
          (union(eye, mirror_x(eye, -0.5)), "eye"),
          (grille, "visor"),
          (antenna, "trim"),
          (sphere(0, 43.0, 0, 2.0), "eye"))
    return model


# ── the space station ─────────────────────────────────────────────────────────────────────────────────────

def station():
    """A ring station, 118 blocks across the solar wings and 56 tall.

    The one model here that is mostly *hollow* — the habitation torus is a tube and the hub a shelled sphere
    — which is what makes it the fair test: a hollow ring is a column with two runs wherever the eye looks
    through it, and every one of those runs has to find a layer."""
    model = {}

    ring = torus(0, 30, 0, 27, 6)
    ring_deck = intersect(torus(0, 30, 0, 27, 6), box(-40, 40, 28, 30, -40, 40))
    windows = difference(intersect(torus(0, 30, 0, 27, 6.4), box(-40, 40, 31, 33, -40, 40)),
                         torus(0, 30, 0, 27, 5.4))

    spokes = union(*[rotate_y(beam((7, 30, 0), (25, 30, 0), 2.6), turn) for turn in (0, 90, 180, 270)])
    pods = union(*[rotate_y(union(ellipsoid(30, 30, 0, 4.6, 4.2, 4.2), beam((25, 30, 0), (30, 30, 0), 1.5)),
                            turn) for turn in (45, 135, 225, 315)])

    hub = shell(sphere(0, 32, 0, 10), 2)
    hub_band = intersect(sphere(0, 32, 0, 10.4), box(-11, 11, 31, 33, -11, 11))
    spine = union(cylinder(0, 0, 3.4, 8, 24), cylinder(0, 0, 5.2, 4, 9), cylinder(0, 0, 4.0, 40, 46))
    collar = union(cylinder(0, 0, 5.6, 46, 49), cylinder(0, 0, 7.6, 49, 51))

    mast = beam((0, 51, 0), (0, 60, 0), 1.2)
    dish = difference(revolve([(9, 0), (8.4, 1), (5, 4), (0, 5)], 0, 0, 60),
                      translate(revolve([(8, 0), (7.4, 1), (4, 4), (0, 5)], 0, 0, 60), 0, 1, 0))

    wing = box(30, 58, 28, 29, -13, 13)
    arm = beam((26, 29, 0), (32, 29, 0), 1.6)
    panels = union(wing, mirror_x(wing, 0), arm, mirror_x(arm, 0))
    struts = union(*[box(30, 58, 27, 30, z, z) for z in (-13, -6, 0, 6, 13)])
    struts = union(struts, mirror_x(struts, 0))

    paint(model,
          (ring, "hull"),
          (ring_deck, "deck"),
          (windows, "glass"),
          (spokes, "hull"),
          (pods, "hull"),
          (spine, "deck"),
          (hub, "hull"),
          (hub_band, "glass"),
          (collar, "deck"),
          (mast, "deck"),
          (dish, "hull"),
          (struts, "deck"),
          (panels, "solar"))
    return model


# ── the car ───────────────────────────────────────────────────────────────────────────────────────────────

def car():
    """A fastback coupe, 36 blocks long, 18 wide and 15 tall, standing on four wheels.

    A car is a **side profile crossed with a plan**, and that is exactly how it is written: one silhouette in
    `(z, y)` extruded across the width, one outline in `(x, z)` extruded up, and the intersection is the
    body. The greenhouse is the same pair narrowed, and the glass is the skin of it rather than the volume,
    so the cabin is a cabin and not a solid block of blue."""
    model = {}

    #        nose            bonnet          cowl        screen       roof         fastback      tail
    profile = [(-18, 3), (-18, 7.6), (-13, 8.6), (-5, 9.6), (-1.5, 13.4), (4, 13.8), (11, 11.6),
               (16, 10.0), (18, 9.2), (18, 3)]
    plan = [(-7.6, -18), (-8.6, -12), (-9.2, -4), (-9.2, 6), (-8.6, 13), (-6.8, 18),
            (6.8, 18), (8.6, 13), (9.2, 6), (9.2, -4), (8.6, -12), (7.6, -18)]

    wells = [(-8, -10), (8, -10), (-8, 10), (8, 10)]
    body = intersect(extrude_x(profile, -10, 10), prism(plan, 3, 15))
    body = difference(body, *[translate(rotate_y(cylinder(0, 0, 4.7, -11, 11), 90), x, 4.2, z)
                              for x, z in wells])
    sill = intersect(extrude_x([(-18, 3), (-18, 6.4), (18, 6.4), (18, 3)], -10, 10), prism(plan, 3, 7))
    body = union(body, sill)

    # The cabin is glazed rather than hollowed. At this scale a hollow cabin reads as a hole in the roof —
    # the glass has to be the body's own skin over the window band, which is the same decal rule the robot's
    # face is drawn with, taken round all four sides.
    skin = difference(body, _eroded(body, 1))
    glass = intersect(skin, extrude_x([(-5.0, 9.4), (-1.5, 13.4), (4, 13.8), (10.5, 11.4), (10.5, 9.4)],
                                      -10, 10))
    pillar = union(box(-10, 10, 3, 16, -2, -1), box(-10, 10, 3, 16, 9, 10))
    glass = difference(glass, pillar, box(-10, 10, 13, 16, -20, 20))

    def wheel(x, z):
        return translate(torus(0, 4.2, 0, 2.9, 1.5, axis="x"), x, 0, z)

    def hub(x, z):
        return translate(rotate_y(cylinder(0, 0, 2.0, -2, 2), 90), x, 4.2, z)

    seats = wells
    tyres = union(*[wheel(x, z) for x, z in seats])
    hubs = union(*[hub(x + (1.1 if x > 0 else -1.1), z) for x, z in seats])
    stripe = intersect(skin, box(-1, 1, 9, 16, -20, 20))
    grille = intersect(skin, box(-5, 5, 6, 6, -19, -16))
    lamps = union(ellipsoid(-6.6, 7.8, -17.6, 1.8, 1.3, 1.6), ellipsoid(6.6, 7.8, -17.6, 1.8, 1.3, 1.6))
    tails = union(box(-8, -3, 7, 9, 17, 18), box(3, 8, 7, 9, 17, 18))

    paint(model,
          (body, "paint"),
          (stripe, "stripe"),
          (grille, "chrome"),
          (glass, "glass"),
          (lamps, "lamp"),
          (tails, "tail"),
          (tyres, "tyre"),
          (hubs, "chrome"))
    return model


# ── the statue ────────────────────────────────────────────────────────────────────────────────────────────

def statue():
    """A hooded sentinel on a stepped plinth, 44 blocks to the crown of the hood.

    A monument is read from the ground and from a distance, so it is written as a silhouette first: a robe
    that flares at the hem and tapers to the shoulders, a deep hood with a shadowed face inside it, and one
    arm raised holding a lantern — the outline that has to survive being a hundred blocks away. The robe is a
    revolve, which is what keeps its fall smooth over twenty-four courses with no hand-placed step in it."""
    model = {}

    plinth = union(box(-11, 11, 0, 2, -11, 11), box(-9, 9, 2, 5, -9, 9), box(-10, 10, 5, 6, -10, 10))

    robe = revolve([(6.9, 0), (6.4, 2), (5.4, 6), (4.9, 12), (4.7, 18), (4.7, 22), (4.4, 25)], 0, 0, 6)
    hem = intersect(revolve([(7.4, 0), (6.9, 2), (5.9, 6)], 0, 0, 6), box(-9, 9, 6, 9, -9, 9))
    folds = intersect(
        revolve([(7.4, 0), (6.9, 2), (5.9, 6), (5.4, 12), (5.2, 18), (5.2, 22)], 0, 0, 6),
        union(*[rotate_y(box(-1, 0, 6, 28, -9, -3), turn) for turn in (0, 55, 130, 180, 235, 305)]))

    shoulders = ellipsoid(0, 32.0, 0, 6.6, 3.2, 4.4)
    chest = intersect(ellipsoid(0, 29.5, -0.6, 5.2, 4.4, 4.2), half_space(0, 0, 1, -1.4))

    hood = difference(
        union(ellipsoid(0, 36.4, 0.8, 5.2, 5.0, 5.2), ellipsoid(0, 33.4, 1.0, 6.0, 3.0, 5.0)),
        intersect(ellipsoid(0, 35.6, -1.4, 3.2, 3.4, 4.0), half_space(0, 0, 1, -1.0)))
    face = intersect(ellipsoid(0, 35.6, -0.2, 2.9, 3.1, 3.8), half_space(0, 0, 1, -1.0))

    arm_up = union(
        beam((5.6, 31.4, 0), (9.4, 27.4, -2.6), 2.2),
        beam((9.4, 27.4, -2.6), (10.4, 33.6, -4.6), 2.0),
        ellipsoid(10.4, 34.8, -4.8, 2.1, 1.7, 2.1))
    arm_down = union(
        beam((-5.6, 31.4, 0), (-7.4, 25.0, -2.4), 2.2),
        beam((-7.4, 25.0, -2.4), (-6.6, 20.0, -3.4), 2.0),
        ellipsoid(-6.4, 18.6, -3.6, 2.2, 1.9, 2.2))

    hanger = beam((10.4, 35.4, -4.8), (10.4, 38.4, -4.8), 0.9)
    lamp_shell = difference(box(9, 12, 39, 43, -6, -3), box(10, 11, 40, 42, -5, -4))
    lamp_cap = union(box(8, 13, 43, 44, -7, -2), box(9, 12, 44, 44, -6, -3))
    flame = box(10, 11, 40, 42, -5, -4)

    paint(model,
          (plinth, "stone"),
          (robe, "robe"),
          (hem, "fold"),
          (folds, "fold"),
          (union(arm_up, arm_down), "robe"),
          (shoulders, "robe"),
          (chest, "fold"),
          (hood, "hood"),
          (face, "dark"),
          (union(hanger, lamp_shell, lamp_cap), "metal"),
          (flame, "flame"))
    return model


# ── the starship ──────────────────────────────────────────────────────────────────────────────────────────

def starship():
    """A one-seat interceptor, 76 blocks nose to exhaust and 62 across the wings, flying north.

    Everything long about it is a **body of revolution laid down** — `revolve_z` spins a radius profile about
    the north-south axis, so the fuselage, the two nacelles and their bells are each one statement rather than
    a stack of rings. What is left is flat: the wings are swept polygons three blocks thick, the fins are
    silhouettes in the side plane, and the livery is decals — the hull's own surface grown by a hair and
    clipped by a box, because any other shape crosses the hull somewhere and speckles along the crossing."""
    model = {}

    #        tip      nose        cockpit        waist        engine deck      tail
    fuselage = revolve_z([(0.6, 0), (3.4, 5), (5.6, 13), (6.6, 24), (6.4, 40), (7.2, 54), (6.8, 62),
                          (5.0, 66), (5.2, 68)], 0, 10, -38)
    spine = intersect(revolve_z([(0.6, 0), (4.4, 5), (7.0, 13), (8.2, 24), (8.0, 40), (8.6, 54),
                                 (8.0, 62), (6.0, 68)], 0, 8.0, -38),
                      box(-5, 5, 13, 22, -38, 30))
    hull = union(fuselage, spine)

    # A swept delta: root chord long, tip short, leading edge raked back. One polygon and a thickness.
    wing = prism([(5, -8), (14, -2), (26, 10), (31, 20), (30, 24), (16, 18), (8, 12), (5, 6)], 9, 12)
    wing = union(wing, mirror_x(wing, 0))
    wing_edge = prism([(5, -8), (14, -2), (26, 10), (31, 20), (30, 21), (25, 11), (13, 0), (5, -6)], 9, 12)
    wing_edge = union(wing_edge, mirror_x(wing_edge, 0))
    tips = union(*[intersect(cylinder_z(x, 10.5, 2.2, 8, 26), box(-33, 33, 8, 13, 8, 26))
                   for x in (-30.5, 30.5)])

    canards = prism([(5, -26), (13, -22), (15, -16), (6, -18)], 10, 12)
    canards = union(canards, mirror_x(canards, 0))

    fin = intersect(extrude_x([(18, 16), (26, 31), (32, 31), (32, 16)], -1, 1),
                    box(-2, 2, 15, 32, 16, 33))

    def nacelle(x):
        tube = revolve_z([(2.0, 0), (3.8, 3), (4.2, 22), (3.8, 30), (4.6, 33), (4.0, 35)], x, 8.0, -6)
        return tube
    nacelles = union(nacelle(-15), nacelle(15))
    bells = union(*[intersect(revolve_z([(4.6, 0), (5.0, 2), (3.6, 4)], x, 8.0, 27), box(-40, 40, 0, 20, 27, 31))
                    for x in (-15, 15)])
    glow = union(*[cylinder_z(x, 8.0, 3.4, 29, 30) for x in (-15, 15)])
    pylons = union(*[box(x - 2, x + 2, 9, 13, -4, 12) for x in (-15, 15)])

    def decal(x0, x1, y0, y1, z0, z1, grow=0.45):
        return intersect(union(
            revolve_z([(0.6 + grow, 0), (3.4 + grow, 5), (5.6 + grow, 13), (6.6 + grow, 24),
                       (6.4 + grow, 40), (7.2 + grow, 54), (6.8 + grow, 62), (5.0 + grow, 66),
                       (5.2 + grow, 68)], 0, 10, -38),
            intersect(revolve_z([(0.6 + grow, 0), (4.4 + grow, 5), (7.0 + grow, 13), (8.2 + grow, 24),
                                 (8.0 + grow, 40), (8.6 + grow, 54), (8.0 + grow, 62), (6.0 + grow, 68)],
                                0, 8.0, -38),
                      box(-6, 6, 13, 22, -38, 30))),
            box(x0, x1, y0, y1, z0, z1))

    canopy = intersect(hull, extrude_x([(-20, 14), (-14, 18.4), (-1, 19.0), (4, 15.5)], -5, 5))
    canopy = difference(canopy, _eroded(canopy, 1))
    nose = intersect(hull, box(-9, 9, 0, 24, -38, -33))
    stripe = union(decal(-2, 2, 14, 26, -38, 30), decal(-10, 10, 2, 26, -20, -19))
    intakes = union(*[intersect(hull, box(-9, 9, 11, 14, z, z + 1)) for z in (-4, 6)])
    wing_flash = intersect(union(wing, tips), box(-33, 33, 9, 12, 16, 26))

    paint(model,
          (union(hull, wing, tips, canards), "ship-hull"),
          (wing_edge, "ship-red"),
          (wing_flash, "ship-red"),
          (pylons, "ship-grey"),
          (fin, "ship-red"),
          (stripe, "ship-red"),
          (intakes, "ship-dark"),
          (nose, "ship-dark"),
          (nacelles, "ship-grey"),
          (bells, "ship-dark"),
          (glow, "ship-glow"),
          (canopy, "ship-glass"))
    return model


# ── the cube ──────────────────────────────────────────────────────────────────────────────────────────────

def rubik(cubie=7, gap=1, scramble=None):
    """A 3x3 twisty cube, 23 blocks on a side at the default seven-block cubie.

    Geometrically it is the simplest thing here — one solid box, one run per column — and it is the most
    expensive to compile, which is the whole reason it is in the set. A layer holds one span per column and a
    span carries one theme, so a colour change splits a run as surely as air does. A column down the east
    face crosses white, black, red, black, red, black, red, black, yellow: nine bands, nine layers, through a
    solid cube with no hole in it anywhere.

    `scramble` is a `{face: [[colour x 3] x 3]}` override; the default is the solved cube."""
    model = {}
    side = 3 * cubie + 2 * gap
    body = box(0, side - 1, 0, side - 1, 0, side - 1)
    faces = scramble or {
        "up": [["white"] * 3] * 3, "down": [["yellow"] * 3] * 3,
        "north": [["green"] * 3] * 3, "south": [["blue"] * 3] * 3,
        "east": [["red"] * 3] * 3, "west": [["orange"] * 3] * 3,
    }

    stickers = []
    for face, grid in faces.items():
        for row in range(3):
            for col in range(3):
                low = lambda i: i * (cubie + gap) + 1
                high = lambda i: i * (cubie + gap) + cubie - 2
                a0, a1 = low(col), high(col)
                b0, b1 = low(row), high(row)
                edge = side - 1
                if face == "up":
                    tile = box(a0, a1, edge, edge, b0, b1)
                elif face == "down":
                    tile = box(a0, a1, 0, 0, b0, b1)
                elif face == "north":
                    tile = box(a0, a1, b0, b1, 0, 0)
                elif face == "south":
                    tile = box(a0, a1, b0, b1, edge, edge)
                elif face == "east":
                    tile = box(edge, edge, b0, b1, a0, a1)
                else:
                    tile = box(0, 0, b0, b1, a0, a1)
                stickers.append((tile, grid[row][col]))

    paint(model, (body, "frame"), *stickers)
    return model


# ── the droid ─────────────────────────────────────────────────────────────────────────────────────────────

def droid():
    """A barrel droid, 21 blocks tall — the robot's small cousin, and the one to reach for as a map prop.

    Everything about it is a body of revolution: a domed head on a ring collar, a barrel with a service
    hatch and a row of ports, two outboard legs on shoulder pivots and a centre caster. Cheap enough to
    stand four of them along a road."""
    model = {}

    foot = union(ellipsoid(-6.5, 1.4, 0, 2.6, 1.6, 4.2), box(-9, -4, 0, 1, -4, 4))
    leg = union(beam((-6.5, 2, 0), (-5.2, 11, 0), 2.2), sphere(-5.2, 11.4, 0, 2.6))
    caster = union(sphere(0, 2.0, 5.6, 2.2), beam((0, 3, 5.4), (0, 8, 3.4), 1.6))

    barrel = union(cylinder(0, 0, 4.6, 4, 15), ellipsoid(0, 15.2, 0, 4.6, 1.6, 4.6),
                   ellipsoid(0, 4.2, 0, 4.6, 1.4, 4.6))
    collar = cylinder(0, 0, 4.2, 15, 16)
    dome = union(ellipsoid(0, 15.6, 0, 4.5, 5.4, 4.5), cylinder(0, 0, 4.5, 16, 17))
    dome = intersect(dome, box(-6, 6, 16, 22, -6, 6))

    def skin(x0, x1, y0, y1, z0, z1, grow=0.4):
        return intersect(cylinder(0, 0, 4.6 + grow, 4, 15), box(x0, x1, y0, y1, z0, z1))

    hatch = skin(-2, 2, 8, 12, -6, -3)
    ports = union(*[skin(-2, 2, y, y, -6, -3, 0.55) for y in (6, 13)])
    band = union(intersect(cylinder(0, 0, 5.0, 4, 15), box(-6, 6, 13, 13, -6, 6)),
                 intersect(cylinder(0, 0, 5.0, 4, 15), box(-6, 6, 6, 6, -6, 6)))

    def head_skin(x0, x1, y0, y1, z0, z1, grow=0.4):
        return intersect(union(ellipsoid(0, 16.0, 0, 4.4 + grow, 4.6 + grow, 4.4 + grow),
                               cylinder(0, 0, 4.4 + grow, 16, 17)),
                         box(x0, x1, y0, y1, z0, z1))

    lens = head_skin(-2, 2, 17, 19, -6, -2, 0.7)
    lamp = head_skin(-4, -3, 18, 19, -6, -3, 0.7)
    rim = head_skin(-6, 6, 16, 16, -6, 6, 0.55)

    paint(model,
          (union(leg, mirror_x(leg, 0), foot, mirror_x(foot, 0), caster), "joint"),
          (barrel, "shell"),
          (band, "trim"),
          (hatch, "panel"),
          (ports, "joint"),
          (collar, "trim"),
          (dome, "shell"),
          (rim, "trim"),
          (lens, "visor"),
          (union(lamp, mirror_x(lamp, 0)), "eye"))
    return model


# ── the dragon ────────────────────────────────────────────────────────────────────────────────────────────

def dragon():
    """A wyrm rearing off a crag, 80 blocks across the wings and 46 tall.

    The one model whose body is a **path**: `tube` sweeps a radius profile along a 3-D polyline, so the tail,
    the spine and the neck are one statement each and every joint between them is round. Nothing else here can
    say that — a plan crossed with a profile gives a body that is a function of one axis, and a creature
    doubling back over itself is not. The wings are the other new primitive: a plan outline lifted onto a
    surface (`sheet`), which is how a membrane arcs over its own spars.

    It is also the model with the deepest columns on the board. A wing held over the shoulders puts tail,
    body, wing and spar in one column, and every one of them has to find a layer."""
    model = {}

    # tail tip on the rock, up through the haunches and the chest, then the neck curling forward
    spine = [(0, 3, 36), (0, 5, 28), (-1, 8, 20), (-1, 13, 12), (0, 19, 4), (1, 24, -2),
             (1, 29, -8), (0, 33, -13), (-2, 35, -17), (-4, 35, -21)]
    girth = [1.2, 2.2, 3.6, 5.2, 5.8, 5.2, 4.2, 3.4, 3.0, 2.8]
    body = tube(spine, girth)

    # The underside is a second tube run below the first, so the pale scales follow the curve rather than
    # being knifed off by a plane the body has already bent past.
    under = tube([(x, y - g * 0.60, z) for (x, y, z), g in zip(spine, girth)],
                 [g * 0.80 for g in girth])
    belly = intersect(body, under)

    skull = union(
        ellipsoid(-4.8, 35.4, -23.5, 3.6, 3.4, 5.0),
        ellipsoid(-5.6, 34.0, -28.0, 2.6, 2.2, 4.0),
        ellipsoid(-6.0, 33.2, -31.0, 1.9, 1.5, 2.2))
    jaw = union(ellipsoid(-5.4, 32.6, -27.6, 2.6, 1.3, 4.2),
                ellipsoid(-5.9, 32.2, -30.8, 1.8, 1.0, 2.2))
    teeth = union(*[ellipsoid(-5.4 + dx, 33.2, z, 0.6, 0.9, 0.6)
                    for dx in (-1.8, 0, 1.8) for z in (-26.0, -29.0, -31.6)])
    horn = tube([(-2.8, 37.4, -21.5), (-0.4, 40.2, -16.5), (2.4, 40.6, -10.5)], [1.2, 0.8, 0.3])
    horn = union(horn, translate(horn, -4.0, -0.8, -0.4))
    brow = union(ellipsoid(-3.1, 36.6, -24.6, 1.2, 0.9, 1.5), ellipsoid(-6.5, 36.6, -24.6, 1.2, 0.9, 1.5))
    nostril = union(ellipsoid(-5.2, 33.8, -31.4, 0.7, 0.7, 0.8), ellipsoid(-6.8, 33.8, -31.4, 0.7, 0.7, 0.8))
    eye = union(ellipsoid(-2.7, 36.2, -25.9, 1.0, 1.0, 1.3), ellipsoid(-6.9, 36.2, -25.9, 1.0, 1.0, 1.3))

    # The membrane's surface: it climbs away from the shoulder and falls again past the wrist, so the wing
    # arcs over the body instead of lying flat, and it slopes down toward the trailing edge.
    def lift(x, z):
        t = min(1.0, abs(x) / 42.0)
        return 26.0 + 34.0 * t - 20.0 * t * t - (z + 6.0) * 0.24

    def wing_outline(sign):
        return [(sign * 4, -6), (sign * 18, -18), (sign * 32, -18), (sign * 42, -6),
                (sign * 36, 6), (sign * 24, 13), (sign * 12, 14), (sign * 4, 8)]

    def membrane(sign):
        return sheet(wing_outline(sign), lift, 1.7)

    def spars(sign):
        root = (sign * 4, lift(sign * 4, -4) - 1, -4)
        wrist = (sign * 20, lift(sign * 20, -16) + 1, -16)
        fingers = [(sign * 32, -18), (sign * 42, -6), (sign * 36, 6), (sign * 24, 13)]
        out = [tube([root, wrist], [2.6, 1.8])]
        for fx, fz in fingers:
            out.append(tube([wrist, (fx, lift(fx, fz), fz)], [1.5, 0.5]))
        out.append(tube([root, (sign * 12, lift(sign * 12, 14), 14)], [1.8, 0.6]))
        return union(*out)

    wings = union(membrane(1), membrane(-1))
    bones = union(spars(1), spars(-1))

    def leg(sign, hip, knee, ankle, foot, thick):
        return union(tube([hip, knee, ankle, foot], [thick, thick * 0.60, thick * 0.50, thick * 0.45]),
                     ellipsoid(foot[0], foot[1] - 0.4, foot[2] - 1.8, thick * 0.95, thick * 0.5, thick * 1.5),
                     sphere(hip[0], hip[1], hip[2], thick * 1.05))
    fore = union(leg(1, (4.0, 22, 0), (8.4, 15, -4), (8.0, 8, -8), (7.6, 4, -10), 2.5),
                 leg(-1, (-4.0, 22, 0), (-8.4, 15, -4), (-8.0, 8, -8), (-7.6, 4, -10), 2.5))
    hind = union(leg(1, (4.4, 13, 16), (9.6, 8, 20), (9.0, 4, 15), (8.4, 3, 11), 3.2),
                 leg(-1, (-4.4, 13, 16), (-9.6, 8, 20), (-9.0, 4, 15), (-8.4, 3, 11), 3.2))
    claws = union(*[ellipsoid(x, 3.4, z, 0.9, 0.7, 1.5)
                    for x, z in ((6.3, -12), (8.9, -12), (-6.3, -12), (-8.9, -12),
                                 (7.1, 9), (9.7, 9), (-7.1, 9), (-9.7, 9))])

    # A crest of plates along the spine: each is the body's own section grown upward and clipped to one course
    # of thickness, so the ridge follows the curve instead of standing off it.
    ridge = union(*[intersect(ellipsoid(spine[i][0], spine[i][1], spine[i][2],
                                        1.1, girth[i] + 2.6, 1.1),
                              box(-9, 9, int(spine[i][1]), int(spine[i][1] + girth[i] + 4), -44, 44))
                    for i in range(1, len(spine) - 1)])

    crag = union(box(-14, 14, 0, 2, -8, 32), box(-12, 12, 2, 4, -6, 30), box(-13, 13, 4, 5, -7, 31))

    paint(model,
          (crag, "rock"),
          (union(body, skull), "scale"),
          (belly, "belly"),
          (union(fore, hind), "scale"),
          (claws, "bone"),
          (jaw, "belly"),
          (teeth, "bone"),
          (wings, "membrane"),
          (bones, "scale"),
          (ridge, "spine"),
          (union(horn, brow), "bone"),
          (nostril, "spine"),
          (eye, "ember"))
    return model


# ── the walker ────────────────────────────────────────────────────────────────────────────────────────────

def walker():
    """A four-legged walker, 42 blocks across the stance and 34 tall.

    A hull slung between two shoulder yokes, four jointed legs, a turret with a pair of barrels and a
    sensor mast. Every limb is a `tube` along three points, which is what makes a knee read as a knee: the
    capsule's own round cap is the joint, so nothing has to be stamped there."""
    model = {}

    hull = union(
        intersect(extrude_x([(-13, 16), (-9, 22), (9, 23), (14, 18), (14, 13), (-13, 13)], -9, 9),
                  prism([(-9, -14), (-11, -4), (-11, 8), (-8, 15), (8, 15), (11, 8), (11, -4), (9, -14)],
                        12, 24)),
        box(-11, 11, 15, 20, -6, 8))
    skirt = intersect(prism([(-12, -12), (-13, 6), (-10, 14), (10, 14), (13, 6), (12, -12)], 12, 15),
                      extrude_x([(-13, 12), (-13, 15), (15, 15), (15, 12)], -14, 14))

    yoke = union(*[tube([(-13, 18, z), (13, 18, z)], 2.6) for z in (-7, 9)])

    def limb(sx, sz, out, forward):
        hip = (sx * 13, 18, sz)
        knee = (sx * 20, 11, sz + forward * 3)
        ankle = (sx * 18, 5, sz + forward * 8)
        foot = (sx * 18, 1, sz + forward * 11)
        return union(tube([hip, knee, ankle, foot], [3.0, 2.2, 1.8, 1.4]),
                     ellipsoid(sx * 18, 1.4, sz + forward * 11, 3.2, 1.6, 4.0),
                     sphere(sx * 13, 18, sz, 3.2))
    legs = union(limb(1, -7, 1, -1), limb(-1, -7, 1, -1), limb(1, 9, 1, 1), limb(-1, 9, 1, 1))

    turret = union(ellipsoid(0, 25, 1, 7.4, 3.6, 6.4), cylinder(0, 1, 6.0, 21, 25))
    barrels = union(*[union(cylinder_z(x, 25, 1.5, -16, 2), cylinder_z(x, 25, 2.2, -10, -6))
                      for x in (-4, 4)])
    mast = union(tube([(6, 28, 4), (8, 34, 6)], [0.9, 0.6]), sphere(8, 34.6, 6, 1.6))

    def decal(x0, x1, y0, y1, z0, z1, grow=0.5):
        return intersect(union(
            intersect(extrude_x([(-13 - grow, 16), (-9 - grow, 22), (9 + grow, 23), (14 + grow, 18),
                                 (14 + grow, 13), (-13 - grow, 13)], -10, 10),
                      prism([(-9 - grow, -14), (-11 - grow, -4), (-11 - grow, 8), (-8 - grow, 15),
                             (8 + grow, 15), (11 + grow, 8), (11 + grow, -4), (9 + grow, -14)], 12, 24)),
            box(-12, 12, 15, 21, -7, 9)), box(x0, x1, y0, y1, z0, z1))

    visor = decal(-6, 6, 18, 20, -20, -10)
    flank = union(decal(-14, -12, 14, 21, -6, 8, 0.9), decal(12, 14, 14, 21, -6, 8, 0.9))
    lamps = union(ellipsoid(-5, 16.4, -14.6, 1.2, 1.0, 1.4), ellipsoid(5, 16.4, -14.6, 1.2, 1.0, 1.4))

    paint(model,
          (union(legs, yoke), "joint"),
          (hull, "shell"),
          (skirt, "trim"),
          (flank, "trim"),
          (visor, "visor"),
          (turret, "shell"),
          (barrels, "joint"),
          (mast, "trim"),
          (lamps, "eye"))
    return model


# ── the ship ──────────────────────────────────────────────────────────────────────────────────────────────

def ship():
    """A two-masted brigantine, 54 blocks stem to stern and 42 to the mainmast truck.

    A hull is the car's trick taken seriously: one **sheer profile** in `(z, y)` extruded across the beam and
    one **waterplane** in `(x, z)` extruded up, intersected. What that pair alone cannot give is tumblehome —
    a hull is narrower at the keel than at the rail — so the plan is applied twice, a narrow one low and the
    full one high, and the volume between them is the turn of the bilge.

    Above the deck nothing is a volume. The bulwark is the hull's own skin over a height band, the sails are
    `sheet` surfaces bowed by a height function, and the rigging is a set of tubes: a ship read as solids
    would be a barge with poles in it."""
    model = {}

    #          stem          forefoot      midships       quarter        transom
    sheer = [(-27, 4.0), (-25, 1.6), (-16, 0.0), (0, 0.0), (14, 0.4), (23, 2.0), (26, 3.4), (26, 15.0),
             (14, 12.4), (0, 11.6), (-16, 12.4), (-25, 14.4), (-27, 14.0)]
    waterplane = [(-1.2, -27), (-4.6, -20), (-7.0, -10), (-7.6, 2), (-6.8, 13), (-4.6, 22), (-3.0, 26),
                  (3.0, 26), (4.6, 22), (6.8, 13), (7.6, 2), (7.0, -10), (4.6, -20), (1.2, -27)]
    keelplane = [(x * 0.42, z) for x, z in waterplane]

    body = intersect(extrude_x(sheer, -8, 8), prism(waterplane, 0, 16))
    bilge = intersect(extrude_x(sheer, -8, 8), prism(keelplane, 0, 16))
    # The turn of the bilge: below the waterline the hull narrows to the keel, so the low band takes the
    # narrow plan and the high band the full one, and the two meet at the load line.
    hull = union(difference(body, box(-9, 9, 0, 5, -28, 27)),
                 intersect(bilge, box(-9, 9, 0, 5, -28, 27)))
    keel = intersect(extrude_x([(-26, -0.4), (-24, -1.2), (20, -1.2), (24, -0.4)], -1, 1),
                     box(-1, 1, -2, 1, -28, 27))
    hull = union(hull, keel)

    # The deck is a lid rather than a fill: the hull below it is never seen and would cost a run per column.
    deck = intersect(prism([(x * 0.94, z) for x, z in waterplane], 11, 13), difference(hull, _eroded(hull, 1)))
    deck = union(deck, intersect(prism([(x * 0.90, z) for x, z in waterplane], 11, 12),
                                 box(-9, 9, 11, 12, -25, 25)))

    skin = difference(hull, _eroded(hull, 1))
    rail = intersect(skin, box(-9, 9, 12, 16, -28, 27))          # bulwark: the skin above the deck
    strake = intersect(skin, box(-9, 9, 8, 9, -28, 27))          # the load-line stripe, one course of it

    quarterdeck = intersect(prism([(-6.0, 8), (-6.0, 24), (6.0, 24), (6.0, 8)], 13, 17),
                            difference(hull, box(-5, 5, 13, 17, 9, 23)))
    quarterdeck = union(quarterdeck, prism([(-6.0, 8), (-6.0, 24), (6.0, 24), (6.0, 8)], 16, 17))

    def mast(z, height, top_radius=0.7):
        return union(tube([(0, 10, z), (0, height, z)], [1.5, top_radius]),
                     sphere(0, height + 0.6, z, 1.2))

    fore, main = mast(-11, 33), mast(7, 41)

    def yard(z, y, half, radius=0.8):
        return tube([(-half, y, z), (half, y, z)], radius)

    yards = union(yard(-11, 30, 13), yard(-11, 22, 15), yard(7, 37, 11), yard(7, 28, 16))
    bowsprit = tube([(0, 14, -24), (0, 19, -36)], [1.4, 0.7])

    def square_sail(z, y_top, y_foot, half_top, half_foot, belly, thickness=1.3):
        """A square sail, bowed downwind: a **near-vertical** cloth whose depth in z is a function of where
        on it you are, deepest at the middle of the head-to-foot and slack at both. It cannot be a `sheet` —
        a sheet's height is a function of the plan, and a sail's plan is a line. So it is written as its own
        membership test over `(x, y)`, which is the plane a sail actually lives in."""
        span = max(y_top - y_foot, 1)

        def inside(x, y, zz):
            if not (y_foot <= y <= y_top):
                return False
            down = (y_top - y) / span                      # 0 at the head, 1 at the foot
            half = half_top + (half_foot - half_top) * down
            if abs(x) > half:
                return False
            across = 1 - (x / max(half, 1e-6)) ** 2        # slack in the middle, taut at the leeches
            # The bow is across the width and the lean is down the drop, and they are kept separate on
            # purpose: a curve in both puts a step in every course and the cloth reads as slats. Curved one
            # way and raked the other, every course has the same profile and the steps fall along the curve.
            bow = belly * across + 0.35 * span * down
            return abs(zz - (z + bow)) <= thickness / 2
        reach = max(half_top, half_foot) + 1
        return Solid(inside, (-reach, reach, y_foot, y_top, z - 2, z + belly + 2))

    def furled(z, y, half):
        """A sail rolled onto its yard: a fat bolt of cloth along the spar, tapering to the yardarms. A ship
        at anchor carries her topsails this way, and it is what keeps the deck of a moored one visible."""
        return tube([(-half, y, z), (-half * 0.7, y - 0.4, z), (half * 0.7, y - 0.4, z), (half, y, z)],
                    [1.1, 2.0, 2.0, 1.1])

    # Courses set, topsails furled: a ship lying to her anchor, which is what one in a harbour is doing, and
    # what leaves her deck open rather than roofed in cloth.
    sails = union(square_sail(-11, 21.5, 15.5, 14, 15, 2.6), square_sail(7, 27.5, 19.0, 15, 16, 2.8),
                  furled(-11, 30, 13), furled(7, 37, 11))

    # A fore-and-aft jib on the bowsprit: a triangle standing between the stay and the stem, so it is a
    # sheet in the (z, y) plane rather than a bowed square.
    jib = intersect(extrude_x([(-34, 17.5), (-11, 31), (-13, 15)], -1, 1), box(-1, 1, 14, 32, -36, -10))

    def stay(a, b, radius=0.5):
        return tube([a, b], radius)

    rigging = union(
        stay((0, 33, -11), (0, 19, -35)), stay((0, 41, 7), (0, 33.5, -10.5)),
        stay((0, 41, 7), (0, 16, 25)), stay((0, 33, -11), (0, 15.5, -1)),
        *[stay((x, 12.5, -11 + s), (0, 29, -11), 0.4) for x in (-7.4, 7.4) for s in (-1, 1)],
        *[stay((x, 12.5, 7 + s), (0, 36, 7), 0.4) for x in (-7.4, 7.4) for s in (-1, 1)])

    rudder = intersect(extrude_x([(24, 0), (27, 1), (27, 12), (24, 12)], -1, 1), box(-1, 1, 0, 12, 22, 28))
    cabin = difference(box(-5, 5, 17, 21, 11, 22), box(-4, 4, 18, 21, 12, 21))
    windows = union(*[box(-5, 5, 18, 19, z, z + 1) for z in (13, 16, 19)])
    lantern = union(cylinder(0, 24, 1.0, 21, 23), sphere(0, 23.6, 24, 1.3))

    paint(model,
          (hull, "hull"),
          (strake, "strake"),
          (rail, "rail"),
          (deck, "deck"),
          (quarterdeck, "deck"),
          (union(fore, main, yards, bowsprit), "spar"),
          (rigging, "rig"),
          (union(sails, jib), "canvas"),
          (rudder, "hull"),
          (cabin, "rail"),
          (windows, "glass"),
          (lantern, "lamp"))
    return model


# ── the hot air balloon ───────────────────────────────────────────────────────────────────────────────────

def balloon():
    """A hot air balloon, 30 blocks across the shoulder and 52 from basket floor to crown.

    The envelope is one `revolve` of a teardrop profile and then a **shell**, because a balloon is a skin and
    a solid one would cost a hundred thousand blocks to say nothing. The gores are the reason it is worth
    building at all: a wedge test on the angle about the axis cuts the skin into twelve panels, and painting
    the alternate ones is one line rather than twelve solids. Below it the mouth is a frustum, the cables are
    tubes drawn to the four corners of the basket, and the basket is a shelled box with a burner in it."""
    model = {}

    #        mouth      shoulder                        crown
    profile = [(4.5, 0), (9.0, 4), (13.0, 9), (15.0, 15), (14.6, 21), (12.4, 27), (8.4, 32), (0.0, 35)]
    envelope = shell(revolve(profile, 0, 0, 20), thickness=1, keep_bottom=True)

    def gore(index, count=12):
        """One wedge of the envelope, by the angle about its axis. `index` is which of `count` panels."""
        step = 2 * math.pi / count

        def inside(x, y, z):
            angle = math.atan2(z, x) % (2 * math.pi)
            return int(angle / step) % count == index
        return Solid(inside, (-20, 20, 0, 128, -20, 20))

    band = intersect(envelope, box(-20, 20, 41, 44, -20, 20))
    panels = [intersect(envelope, gore(i)) for i in range(12)]

    mouth = shell(revolve([(4.6, 0), (4.0, 3), (5.2, 6)], 0, 0, 14), thickness=1, keep_bottom=True)
    ring = torus(0, 14, 0, 4.8, 0.8)

    basket = difference(box(-4, 4, 0, 6, -4, 4), box(-3, 3, 2, 7, -3, 3))
    coaming = box(-4, 4, 6, 6, -4, 4)
    burner = union(cylinder(0, 0, 1.6, 8, 11), cylinder(0, 0, 2.4, 11, 12))
    flame = cylinder(0, 0, 1.2, 12, 13)

    # The rigging is two runs per corner: the basket's own lines drawing in to the load ring at y14, and the
    # load tapes carrying on from the ring to the envelope. **A tape ends ON the skin.** The profile passes
    # radius 13 at y29, so that is where the second run stops — 2.55 times the corner's own offset, which
    # lands it within a fifth of a block of the fabric. Aimed anywhere else it is a black stick in the air:
    # ending at y20.5 put its tip eight blocks outside a skin that is only 5 wide there, and the run came out
    # at 51 degrees off the vertical because that is what reaching that far in six blocks of climb costs. At
    # 28 degrees it runs a block clear of the fabric the whole way up and meets it at the shoulder.
    cables = union(*[tube([(x, 6.5, z), (x * 0.9, 14, z * 0.9)], 0.5)
                     for x in (-3.6, 3.6) for z in (-3.6, 3.6)],
                   *[tube([(x, 14, z), (x * 2.55, 29, z * 2.55)], 0.5)
                     for x in (-3.6, 3.6) for z in (-3.6, 3.6)])
    sandbags = union(*[ellipsoid(x, 1.4, z, 1.4, 1.2, 1.4) for x, z in ((-5.0, 0), (5.0, 0))])

    paint(model,
          *[(panel, "envelope-a" if i % 2 == 0 else "envelope-b") for i, panel in enumerate(panels)],
          (band, "envelope-band"),
          (mouth, "envelope-band"),
          (ring, "rig"),
          (cables, "rig"),
          (basket, "wicker"),
          (coaming, "rail"),
          (sandbags, "wicker"),
          (burner, "rig"),
          (flame, "flame"))
    return model


# ── weather ───────────────────────────────────────────────────────────────────────────────────────────────

def cloud(lobes):
    """A cumulus puff: overlapping domes on one flat base, from `(x, z, span, rise)` a lobe.

    **A cloud is the one made thing seen from underneath**, so what has to read is the flat base every
    cumulus has and the lumpiness of the silhouette above it. Both come free from the primitive: an
    ellipsoid centred ON the base plane is a dome once everything below the plane is cut away, and a handful
    of them at different spans and rises is a cumulus without a single hand-placed block. `rise` is the
    dome's own height and `span` its radius in plan; a lobe wider than it is tall is what keeps the thing
    from reading as a heap of spheres.

    Written about `y = 0` at its base, like every model here is written about its own origin, so a caller
    states one altitude and gets the underside there."""
    domes = union(*[ellipsoid(x, 0, z, span, rise, span * 0.86) for x, z, span, rise in lobes])
    floor = max(rise for _x, _z, _span, rise in lobes)
    return intersect(domes, half_space(0, -1, 0, 0), box(-4096, 4096, 0, int(floor) + 1, -4096, 4096))


def cumulus(seed=0):
    """One of four puffs, so a sky is not one shape repeated. Each is five or six lobes about a wide low
    one, and none is symmetric about either axis — a cloud that answers itself across a mirror reads as a
    logo rather than as weather."""
    return paint({}, (cloud([
        [(0, 0, 11, 5), (-6, -3, 7, 8), (5, 2, 8, 7), (10, -2, 5, 4), (-11, 3, 5, 4), (2, -7, 5, 5)],
        [(0, 0, 13, 4), (-4, 4, 8, 8), (7, -3, 7, 6), (-12, -2, 6, 4), (13, 3, 5, 4)],
        [(0, 0, 9, 6), (-7, 2, 8, 5), (6, -4, 6, 8), (12, 2, 5, 4), (-13, -3, 4, 4), (0, 8, 5, 4)],
        [(0, 0, 12, 5), (-8, -4, 6, 7), (6, 5, 7, 8), (-14, 3, 5, 4), (11, -5, 4, 4)],
    ][seed % 4]), "cloud"))


# ── the quay crane ────────────────────────────────────────────────────────────────────────────────────────

def crane():
    """A shear-legs crane on a quay: two raking legs meeting at a head 22 blocks up, a back stay holding them
    off the vertical, and a load swinging on a chain over the water.

    It is here because it is the smallest thing worth **seating**. A ship floats and a balloon flies, so
    neither reads the ground under it; a crane stands on a wharf that rolls, and its four feet have to find
    that ground or it is a model hanging in the air. Everything above the feet is tubes: a lattice read as
    solids would be a wall."""
    model = {}

    head = (0, 22, -3)
    feet = [(-6, 0, 4), (6, 0, 4)]
    legs = union(*[tube([foot, head], [1.5, 0.9]) for foot in feet])
    brace = union(tube([(-5, 8, 3.4), (5, 8, 3.4)], 0.6), tube([(-4, 15, 1.6), (4, 15, 1.6)], 0.6),
                  tube([(-5, 8, 3.4), (4, 15, 1.6)], 0.5), tube([(5, 8, 3.4), (-4, 15, 1.6)], 0.5))
    stay = union(tube([head, (0, 3, 14)], [0.9, 1.2]), tube([(0, 12, 5.5), (0, 3, 14)], 0.5))

    sill = union(*[box(x - 2, x + 2, -1, 1, 2, 6) for x in (-6, 6)], box(-2, 2, -1, 1, 12, 16))
    drum = union(rotate_y(cylinder(0, 0, 2.0, -3, 3), 90), rotate_y(cylinder(0, 0, 1.2, -4, 4), 90))
    drum = translate(drum, 0, 3, 11)

    chain = tube([(0, 21.4, -3.6), (0, 9, -3.6)], 0.4)
    hook = union(tube([(0, 9.4, -3.6), (0, 8, -3.6)], 0.8), torus(0, 7.2, -3.6, 1.2, 0.5))
    crate = difference(box(-3, 3, 2, 7, -7, -1), box(-2, 2, 3, 7, -6, -2))
    load = union(tube([(0, 8.6, -3.6), (0, 7.2, -3.6)], 0.5), crate)

    cap = union(sphere(0, 22.4, -3, 1.6), tube([(-2.4, 22, -3), (2.4, 22, -3)], 0.7))
    lamp = sphere(0, 20.4, -4.6, 1.0)

    paint(model,
          (sill, "stone"),
          (union(legs, brace, stay, cap), "iron"),
          (drum, "iron"),
          (union(chain, hook, load), "chain"),
          (crate, "timber"),
          (lamp, "lamp"))
    return model


# ── the mini car ──────────────────────────────────────────────────────────────────────────────────────────

def minicar(cabin_back=True):
    """A car at the scale a board can carry a row of: 9 blocks long, 5 wide, 5 tall, one block a wheel.

    Everything larger in this file is a form written as solids and then hollowed. This is the other end: at
    nine blocks there is no room for a profile crossed with a plan, so the whole model is **four boxes and
    four cubes** — a chassis course, a two-course body, a cabin set back or forward on it, and the wheels.
    What makes it read as a car at all is the setback and the glass band, not the outline."""
    model = {}

    body = box(-2, 2, 1, 3, -4, 4)
    chassis = box(-2, 2, 1, 1, -4, 4)
    nose = box(-2, 2, 2, 2, -5, -4)
    tail = box(-2, 2, 2, 3, 4, 5)

    cabin = box(-2, 2, 4, 5, -1, 3) if cabin_back else box(-2, 2, 4, 5, -3, 1)
    glass = difference(cabin, box(-1, 1, 4, 5, -2 if cabin_back else -4, 4 if cabin_back else 2))
    roof = box(-2, 2, 5, 5, *( (-1, 3) if cabin_back else (-3, 1) ))

    wheels = union(*[box(sx * 2, sx * 2, 0, 1, sz, sz + 1) for sx in (-1, 1) for sz in (-4, 2)])
    lamps = union(box(-2, -1, 2, 2, -5, -5), box(1, 2, 2, 2, -5, -5))
    lights = union(box(-2, -1, 3, 3, 5, 5), box(1, 2, 3, 3, 5, 5))

    paint(model,
          (union(body, nose, tail), "car-paint"),
          (chassis, "car-trim"),
          (cabin, "car-glass"),
          (roof, "car-paint"),
          (wheels, "car-trim"),
          (lamps, "lamp"),
          (lights, "car-tail"))
    return model
