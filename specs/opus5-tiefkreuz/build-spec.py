#!/usr/bin/env python3
"""Write the plan and the finish for Tiefkreuz — a four-storey transit interchange.

    python3 specs/opus5-tiefkreuz/build-spec.py
    python3 tools/drive.py specs/opus5-tiefkreuz "Tiefkreuz" \
            --out maps/opus5-tiefkreuz --renders specs/opus5-tiefkreuz/renders

The board is a lane running north-south with a 32-block chasm across its middle. Each half
carries the same four storeys, one over the other:

    y 5/6   the running tracks and their ballast, in a cut-and-cover box
    y  8    the platforms — three of them, an island between two side platforms
    y 18    the concourse mezzanine, a slab over the whole box with wells cut in it
    y 29    the street, which is the box's lid where it crosses it
    y 41    the viaduct deck, a second line crossing the city on brick piers

Everything is stated absolutely: the board carries no relief at all, which is what keeps a
four-storey stack arithmetic rather than a negotiation with a solver.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "opus5-tiefkreuz"

# ── the stack, in world Y ──────────────────────────────────────────────────────────────
BALLAST_H  = 6    # span [0,6)   -> top block y5
RAIL_H     = 7    # span [0,7)   -> top block y6
PLAT_H     = 9    # span [0,9)   -> top block y8,  walk y9
CANOPY_Y   = 14   # made layer   -> [14,15)
MEZZ_Y     = 17   # span [17,19) -> top block y18, walk y19
STREET_H   = 30   # span [0,30)  -> top block y29, walk y30   (the plan's own surface)
LID_Y      = 27   # span [27,30) -> top block y29
VIA_Y      = 39   # span [39,42) -> top block y41, walk y42
PIER_H     = 39   # span [0,39)  -> top block y38, the viaduct's soffit rests on it

CELL = 4

# ── the box, in blocks (all rects are half-open [lo, hi) ) ─────────────────────────────
# Every x-rect is centred on the origin as [-a, a): a rot_180 board mirrors a half-open
# span [lo, hi) onto [-hi, -lo), so a rect is its own image only where min = -max.
BOX   = (-20, 20, 16, 58)          # x0, x1, z0, z1
PLATW = (-20, -14)                 # west platform
TRKW  = (-14, -8)                  # west track
ISL   = (-8, 8)                    # island platform
TRKE  = (8, 14)                    # east track
PLATE = (14, 20)                   # east platform
RAILS = (-13, -10, 9, 12)          # one column each, a course proud of the ballast
TRACK_Z  = (16, 54)                # tracks and platforms run to the buffer stops
ENDDECK_Z = (54, 58)               # the terminus deck, joining all three platforms
LID_MOUTH_Z = (16, 24)             # the tunnel throat, roofed
BAY_Z    = (24, 38)                # the open bay: no lid, no mezzanine, daylight
CONC_Z   = (38, 58)                # the concourse and the lid over it

STAIR_STREET = (-14, -8)           # the flight from the street to the concourse, over the
STAIR_STREET_Z = (36, 58)          #   west track: eleven treads of two, y19 -> y29
STAIR_PLAT   = (0, 8)              # the flight from the island platform to the concourse
STAIR_PLAT_Z = (16, 38)            #   eleven treads of two, y8 -> y18

WELL_W = (-20, -14, 50, 58)        # the light well over the deep goal: street to platform
WELL_E = (14, 20, 50, 58)
WELL_I = (1, 7, 42, 48)            # a drop onto the island platform

# ── the viaduct ───────────────────────────────────────────────────────────────────────
VIA_X   = (-36, 36)
VIA_Z   = (62, 74)
PARA_S  = (61, 62)
PARA_N  = (74, 75)
RAMP_S  = (-34, -26)               # the one ramp onto the deck: z 37..61, y29 -> y41,
RAMP_S_Z = (38, 62)                #   met from the south, at the end away from the goal

TRAIN_X = (9, 13)
TRAIN_Z = (26, 50)

# ── goals ─────────────────────────────────────────────────────────────────────────────
TIEF = (-16, 56)                   # on the terminus deck, under the west light well
HOCH = (22, 62)                    # on the viaduct deck, at the lip away from the ramp


# ── rectangle algebra, so a slab can be drawn round its holes ──────────────────────────
def carve(outer, holes):
    """outer minus holes, as a list of non-overlapping half-open rects.

    A layer holds one span per column, so a lid with a stairwell in it is not a rectangle
    with a hole: it is the rectangles that remain once the hole is taken out. Banding by z
    keeps the count low and the pieces long."""
    x0, x1, z0, z1 = outer
    cuts = sorted({z0, z1} | {v for h in holes for v in (h[2], h[3]) if z0 < v < z1})
    out = []
    for a, b in zip(cuts, cuts[1:]):
        spans = [(x0, x1)]
        for hx0, hx1, hz0, hz1 in holes:
            if hz1 <= a or hz0 >= b:
                continue
            nxt = []
            for sx0, sx1 in spans:
                if hx1 <= sx0 or hx0 >= sx1:
                    nxt.append((sx0, sx1))
                    continue
                if sx0 < hx0:
                    nxt.append((sx0, min(hx0, sx1)))
                if hx1 < sx1:
                    nxt.append((max(hx1, sx0), sx1))
            spans = nxt
        for sx0, sx1 in spans:
            if sx1 > sx0:
                out.append((sx0, sx1, a, b))
    # fuse vertically adjacent bands of the same x-span, so the document stays readable
    fused, out = [], sorted(out, key=lambda r: (r[0], r[1], r[2]))
    for r in out:
        if fused and fused[-1][0] == r[0] and fused[-1][1] == r[1] and fused[-1][3] == r[2]:
            fused[-1] = (r[0], r[1], fused[-1][2], r[3])
        else:
            fused.append(r)
    return fused


SHAPES = []


def rect(sid, box, floor, height, theme, override=True, layer=None, keep=False):
    x0, x1, z0, z1 = box
    s = {"id": sid, "type": "rectangle", "operation": "add",
         "min_x": x0, "max_x": x1, "min_z": z0, "max_z": z1,
         "floor": floor, "base_height": height, "theme": theme}
    if override:
        s["override"] = True
        s["height_mode"] = "level"
        s["skirt"] = 0
        s["relief_scope"] = "exclude"
    if keep:
        s["keepClear"] = True
    return s


def ground(sid, box, height, theme, floor=0, override=True, keep=False):
    SHAPES.append(rect(sid, box, floor, height, theme, override, keep=keep))


# ══ the ground layer: the street, the box cut into it, the stairs and the viaduct's feet ══
# The box. Five strips across, clamped side by side so nothing contests anything: a layer
# holds one span per column and the taller add wins it, so a hall is drawn as the shapes
# AROUND its floor rather than as a floor inside a wall.
for name, (x0, x1), h, theme in (
        ("plat-w", PLATW, PLAT_H, "bahn"),
        ("trk-w",  TRKW,  BALLAST_H, "schotter"),
        ("plat-m", ISL,   PLAT_H, "bahn"),
        ("trk-e",  TRKE,  BALLAST_H, "schotter"),
        ("plat-e", PLATE, PLAT_H, "bahn")):
    ground(f"box-{name}", (x0, x1, *TRACK_Z), h, theme, keep=True)

# the terminus deck: the tracks stop at buffer stops and the three platforms join
ground("box-kopfsteig", (BOX[0], BOX[1], *ENDDECK_Z), PLAT_H, "bahn", keep=True)

# rails — one course proud of the ballast, so a track is crossed by stepping over them
for i, x in enumerate(RAILS):
    ground(f"schiene-{i}", (x, x + 1, *TRACK_Z), RAIL_H, "gleis", keep=True)

# buffer stops at the head of each track
for i, (x0, x1) in enumerate((TRKW, TRKE)):
    ground(f"prellbock-{i}", (x0 + 1, x1 - 1, ENDDECK_Z[0] - 2, ENDDECK_Z[0]), RAIL_H + 1,
           "gleis", keep=True)

# the box lining: one column either side, at the street's own height, so the trainshed's
# lip and the box's inner face read as concrete rather than as city paving
for side, (lx0, lx1) in (("w", (BOX[0] - 1, BOX[0])), ("e", (BOX[1], BOX[1] + 1))):
    ground(f"box-wand-{side}-s", (lx0, lx1, BOX[2], BAY_Z[0]), STREET_H, "bahn", keep=True)
    ground(f"box-wand-{side}-n", (lx0, lx1, BAY_Z[1], BOX[3]), STREET_H, "bahn", keep=True)
    # one course proud where the shed is open, which is the parapet a player reads as an edge
    ground(f"box-bruestung-{side}", (lx0, lx1, *BAY_Z), STREET_H + 1, "bahn", keep=True)

# the lamps. A light is a block and a theme states blocks, so a lit floor is a one-column shape
# at the platform's own height carrying a glowstone theme — there is no lamp prop and none is
# needed. Without them the two storeys under the street are unlit and unplayable.
PLATFORM_LAMPS = [(x, z) for x in (-17, 17) for z in (20, 26, 32, 38, 44, 50)] + \
                 [(-4, z) for z in (20, 26, 32, 38, 44, 56)]
for i, (lx, lz) in enumerate(PLATFORM_LAMPS):
    ground(f"lampe-p{i}", (lx, lx + 1, lz, lz + 1), PLAT_H, "licht", keep=True)

# the flight from the island platform up to the concourse: eleven treads of two blocks,
# one course each — the run is twice the rise, which is what makes a flight walk both ways
for k in range(11):
    z0 = STAIR_PLAT_Z[0] + 2 * k
    ground(f"treppe-p{k}", (STAIR_PLAT[0], STAIR_PLAT[1], z0, z0 + 2), PLAT_H + k,
           "bahn", keep=True)

# the viaduct's piers and its two ramps
for i, x in enumerate((-36, -26, -16, -6, 4, 14, 24, 32)):
    ground(f"pfeiler-{i}", (x, x + 4, VIA_Z[0] + 2, VIA_Z[1] - 2), PIER_H, "ziegel", keep=True)

# The ramp onto the deck: twelve treads of two blocks, one course each. A tilted quad is the
# shorter statement and the column where a ramp MEETS a slab has to land on that slab's own
# top exactly, which an interpolated anchor at the last column does not promise.
for k in range(12):
    z0 = RAMP_S_Z[0] + 2 * k
    ground(f"rampe-{k}", (RAMP_S[0], RAMP_S[1], z0, z0 + 2), STREET_H + 1 + k, "ziegel",
           keep=True)

# ══ the layers over and under the street ═══════════════════════════════════════════════
def layer(lid, name, base_y, shapes, kind=None, part_of=None):
    e = {"id": lid, "name": name, "base_y": base_y, "shapes": shapes,
         "groups": [{"id": lid + "-g", "name": name, "mirrors": True,
                     "shapeIds": [s["id"] for s in shapes]}]}
    if kind:
        e["kind"] = kind
    if part_of:
        e["part_of"] = part_of
    return e


LAYERS = []

# the train, standing at the east platform. Four slices, because a colour change inside a
# run splits a layer as surely as air does; `made` keeps the stacking rules off it.
for i, (base, h, theme) in enumerate((
        (7, 2, "zug-grau"), (9, 2, "zug-rot"), (11, 1, "zug-glas"), (12, 1, "zug-grau"))):
    LAYERS.append(layer(f"zug-{i}", f"Triebzug {i}", base,
                        [rect(f"zug-{i}-a", (TRAIN_X[0], TRAIN_X[1], *TRAIN_Z), 0, h,
                              theme, override=False)],
                        kind="made", part_of="zug"))

# the platform canopies in the open bay, and the posts under them
posts = []
for px in (PLATW[0] + 1, PLATW[1] - 2, ISL[0] + 1, -2, PLATE[0] + 1, PLATE[1] - 2):
    for pz in range(BAY_Z[0] + 2, BAY_Z[1] - 1, 5):
        posts.append(rect(f"stuetze-{px}-{pz}", (px, px + 1, pz, pz + 1), 0,
                          CANOPY_Y - 9, "bahn", override=False))
LAYERS.append(layer("perron-fuss", "Bahnsteigstützen", 9, posts, kind="made",
                    part_of="perron"))
LAYERS.append(layer("perron", "Bahnsteigdach", CANOPY_Y, [
    rect("dach-w", (PLATW[0], PLATW[1], *BAY_Z), 0, 1, "bahn", override=False),
    rect("dach-m", (ISL[0], 0, *BAY_Z), 0, 1, "bahn", override=False),
    rect("dach-e", (PLATE[0], PLATE[1], *BAY_Z), 0, 1, "bahn", override=False),
], kind="made", part_of="perron"))

# the concourse mezzanine: a slab over the whole box at the north end, with the street
# flight cut out of it and three wells dropped through it
mezz = []
HALL_LAMPS = [(x, z) for z in (40, 48) for x in (-16, -4, 8, 16)] + \
             [(x, 55) for x in (-4, 8)]
lamp_rects = [(x, x + 2, z, z + 2) for x, z in HALL_LAMPS]
for x0, x1, z0, z1 in carve((BOX[0], BOX[1], *CONC_Z),
                            [(STAIR_STREET[0], STAIR_STREET[1], *CONC_Z),
                             WELL_W, WELL_E, WELL_I] + lamp_rects):
    mezz.append(rect(f"halle-{x0}-{z0}", (x0, x1, z0, z1), 0, 2, "bahn", override=False,
                     keep=True))
for i, box in enumerate(lamp_rects):
    mezz.append(rect(f"lampe-h{i}", box, 0, 2, "licht", override=False, keep=True))
for k in range(11):
    z0 = STAIR_STREET_Z[0] + 2 * k
    mezz.append(rect(f"treppe-s{k}", (STAIR_STREET[0], STAIR_STREET[1], z0, z0 + 2), 0,
                     3 + k, "bahn", override=False, keep=True))
LAYERS.append(layer("halle", "Zwischengeschoss", MEZZ_Y, mezz))

# the lid: the street where it crosses the box. Absent over the open bay, over the street
# flight and over the two light wells, which is what makes them wells rather than rooms.
lid = []
for x0, x1, z0, z1 in (carve((BOX[0], BOX[1], LID_MOUTH_Z[0], LID_MOUTH_Z[1] - 1), []) +
                       carve((BOX[0], BOX[1], CONC_Z[0] + 1, CONC_Z[1]),
                             [(STAIR_STREET[0], STAIR_STREET[1], *CONC_Z), WELL_W, WELL_E])):
    lid.append(rect(f"deckel-{x0}-{z0}", (x0, x1, z0, z1), 0, STREET_H - LID_Y, "stadt",
                    override=False))
for x0, x1, z0, z1 in (carve((BOX[0], BOX[1], BAY_Z[0] - 1, BAY_Z[0]), []) +
                       carve((BOX[0], BOX[1], BAY_Z[1], BAY_Z[1] + 1),
                             [(STAIR_STREET[0], STAIR_STREET[1], BAY_Z[1], BAY_Z[1] + 1)])):
    lid.append(rect(f"kante-{x0}-{z0}", (x0, x1, z0, z1), 0, STREET_H - LID_Y + 1, "bahn",
                    override=False))
LAYERS.append(layer("deckel", "Straßendecke", LID_Y, lid))

# the viaduct: a deck between two parapets, each notched where a ramp meets it
via = [rect("via-deck", (VIA_X[0], VIA_X[1], *VIA_Z), 0, 3, "schotter", override=False)]
for z in (64, 66, 69, 71):
    via.append(rect(f"via-schiene-{z}", (VIA_X[0], VIA_X[1], z, z + 1), 0, 4, "gleis",
                    override=False))
for name, (pz0, pz1), gap in (("sued", PARA_S, RAMP_S), ("nord", PARA_N, None)):
    for x0, x1, z0, z1 in carve((VIA_X[0], VIA_X[1], pz0, pz1),
                                [(gap[0], gap[1], pz0, pz1)] if gap else []):
        via.append(rect(f"bruestung-{name}-{x0}", (x0, x1, z0, z1), 0, 5, "ziegel",
                        override=False))
LAYERS.append(layer("viadukt", "Hochbahn", VIA_Y, via))


# ── the plan ──────────────────────────────────────────────────────────────────────────
PLAN = {
    "plan": 2,
    "meta": {"name": "Tiefkreuz"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 16,
                "surface": STREET_H, "observerY": 68},
    "pieces": [
        {"id": "kai",       "role": "piece", "rect": [-7,  4, 14, 3], "surface": STREET_H},
        {"id": "bahnhof",   "role": "piece", "rect": [-10, 7, 20, 8], "surface": STREET_H},
        {"id": "stadt",     "role": "piece", "rect": [-9, 15, 18, 7], "surface": STREET_H},
        {"id": "vorplatz",  "role": "piece", "rect": [-9, 22, 18, 3], "surface": STREET_H},
        {"id": "flanke-w",  "role": "piece", "rect": [-9, 25,  7, 3], "surface": STREET_H},
        {"id": "kopfbau",   "role": "spawn", "rect": [-2, 25,  4, 3], "surface": STREET_H},
        {"id": "flanke-e",  "role": "piece", "rect": [2,  25,  7, 3], "surface": STREET_H},
    ],
    "zones": [{"id": "uebergang", "rect": [-7, -4, 14, 8]}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "kopfbau", "at": [8, 6], "facing": "front"}],
        "destroyables": [
            {"id": "tief", "piece": "", "at": list(TIEF), "layer": "ground",
             "style": "pillar-2", "materials": "obsidian", "float": 2,
             "name": "Tiefbahnsteig"},
            {"id": "hoch", "piece": "", "at": list(HOCH), "layer": "viadukt",
             "style": "pillar-2", "materials": "obsidian", "float": 3,
             "name": "Hochbahnsteig"},
        ],
    },
}


# ── the themes: four places and four materials ────────────────────────────────────────
def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}


def noise(seed, scale, stops, octaves=2):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves,
            "stops": [solid(*s) for s in stops], "rise": 0}


def theme(surface, wall, fill, rim=None, depth=2, rim_edges="void"):
    t = {"bedrock": {"relative": False, "value": 1},
         "rimEdges": rim_edges, "wallOnTerrainFaces": True,
         "surface": {"enabled": True, "depth": depth, "material": surface},
         "wall": wall, "wallEnabled": True, "fill": fill}
    t["rim"] = ({"enabled": True, "depth": 1, "material": rim} if rim
                else {"enabled": False, "depth": 1, "material": solid(1)})
    return t


THEMES = {
    # the city: stone-brick paving drifting into andesite, kerbed at every cliff
    "stadt": theme(noise(7, 18, [(98, 0), (1, 5)]), solid(98, 0), solid(1, 5),
                   rim=solid(43, 8), depth=3, rim_edges="drop"),
    # the station's concrete: platforms, concourse, canopies, box lining
    "bahn": theme({"kind": "checker", "size": 6, "even": solid(155, 0),
                   "odd": solid(43, 8)}, solid(159, 8), solid(1, 6),
                  rim=solid(159, 7), depth=2),
    # the ballast under the rails
    "schotter": theme(noise(19, 9, [(13, 0), (1, 5)]), solid(1, 5), solid(1, 5), depth=2),
    # the viaduct's brick, banded by a string course every seventh block of its face
    "ziegel": theme(solid(45, 0),
                    {"kind": "layered", "axis": "height", "from": 0,
                     "stack": {"bands": [{"material": solid(45, 0), "thickness": 6},
                                         {"material": solid(98, 0), "thickness": 1}],
                               "ending": "repeat"},
                     "beyond": solid(45, 0)},
                    solid(45, 0), rim=solid(43, 5), depth=2),
    # the light itself, in every bucket, so a lamp lights the storey over it and the one under
    "licht": theme(solid(89, 0), solid(155, 0), solid(1, 6), depth=1),
    # four materials, for the things that are made rather than grown
    "gleis":    theme(solid(42, 0), solid(42, 0), solid(42, 0)),
    "zug-rot":  theme(solid(159, 14), solid(159, 14), solid(159, 14)),
    "zug-glas": theme(solid(95, 3), solid(95, 3), solid(95, 3)),
    "zug-grau": theme(solid(159, 7), solid(159, 7), solid(159, 7)),
}


# ── the dressing ──────────────────────────────────────────────────────────────────────
def stroke(pid, points, radius, pave, route=True, style="solid", seed=3):
    return {"id": pid, "kind": "stroke", "seed": seed, "points": points,
            "radius": radius, "style": style, "claimsGround": route, "coverage": 0.5,
            "pave": pave}


def house(pid, wings, style, front=None, seed=5):
    p = {"id": pid, "kind": "house", "seed": seed, "style": style,
         "wings": [{"corners": w} for w in wings]}
    if front:
        p["front"] = front
    return p


def tree(pid, x, z, style="platane", seed=11):
    return {"id": pid, "kind": "tree", "seed": seed, "x": x, "z": z, "style": style}


PROPS = [
    # The avenue is drawn in two runs, not one: a stroke seats on the top surface a column
    # carries, so a road drawn under the viaduct paves the viaduct's deck instead of the
    # street. The street resumes on the far side of it.
    stroke("bahnhofstrasse-nord", [[0, 104], [0, 92], [0, 82], [0, 78]], 4, solid(1, 6)),
    stroke("bahnhofstrasse-sued", [[0, 60], [0, 52], [0, 46], [0, 42]], 4, solid(1, 6),
           seed=5),
    # and round the open shed, either side of it, to the quay at the chasm
    stroke("umfahrung-west", [[-2, 59], [-14, 58], [-26, 54], [-26, 40], [-26, 24]], 4,
           solid(1, 6), seed=4),
    stroke("umfahrung-ost", [[2, 59], [14, 58], [26, 54], [26, 40], [26, 24]], 4,
           solid(1, 6), seed=6),
    # four buildings, four jobs: goods shed, signal box, substation and customs hall
    house("gueterschuppen", [[[20, 77], [32, 89]]], "@tk-schuppen", front="negX"),
    house("zollhalle", [[[-32, 77], [-21, 89]]], "@tk-schuppen", front="posX"),
    house("stellwerk", [[[31, 40], [38, 48]]], "@tk-stellwerk", front="negX"),
    house("umspannwerk", [[[-34, 93], [-26, 99]]], "@tk-schuppen", front="posX"),
]
for i, (x, z) in enumerate(((-12, 80), (12, 80), (-12, 88), (12, 88),
                            (-14, 96), (14, 96))):
    PROPS.append(tree(f"allee-{i}", x, z, seed=11 + i))

TREE_STYLE = {"kind": "tree", "form": "template", "species": "oak", "wood": "oak",
              "height": 8, "stems": 1, "leader": 0.55, "flow": 0.45, "branchAngle": 1.1,
              "levels": 2, "whorled": False, "leafSize": 0.6}

FINISH = {
    "authors": ["Opus 5"],
    "created": "2026-09-03",
    "themes": THEMES,
    "mapTheme": "stadt",
    "addShapes": SHAPES,
    "addLayers": LAYERS,
    "roomStyles": {"spawn": "@tk-kopfbau"},
    "dressing": {"props": PROPS, "styles": {"platane": TREE_STYLE}},
}

if __name__ == "__main__":
    with open(f"{HERE}/{BASE}.plan.json", "w") as fh:
        json.dump(PLAN, fh, indent=1)
    with open(f"{HERE}/{BASE}.finish.json", "w") as fh:
        json.dump(FINISH, fh, indent=1)
    print(f"{BASE}.plan.json   {len(PLAN['pieces'])} pieces, {len(PLAN['zones'])} zone")
    print(f"{BASE}.finish.json {len(SHAPES)} shapes on the ground layer, "
          f"{len(LAYERS)} added layers, {len(THEMES)} themes, {len(PROPS)} props")
    for e in LAYERS:
        print(f"   layer {e['id']:<14} base_y {e['base_y']:>3}  "
              f"{len(e['shapes']):>3} shapes  {e.get('kind','ground')}")
