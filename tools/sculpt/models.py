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
