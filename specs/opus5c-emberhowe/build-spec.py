#!/usr/bin/env python3
"""opus5c-emberhowe — capture the wool. The approach dimension is AROUND.

A dead volcano whose crater nobody crosses. Each team holds a horseshoe of rim
open toward the middle, the two horseshoes face each other, and the pit they
enclose carries no build zone at all — so the only ways between the two lands
are the twenty-four blocks of strait at each horn. A raider picks a hand there
and cannot change it afterwards: the far room is reached by walking the whole
rim past the enemy spawn, and there is no way across.

Tone families: the ground is pale ash over black rock, what is built is warm
spruce timber on a rust plinth, and the accent is the scoria the slope bands
put on the shoulders.

Writes opus5c-emberhowe.plan.json and opus5c-emberhowe.refinement.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from studio_kit import kit

SLUG = "opus5c-emberhowe"
CELL = 2


# ---------------------------------------------------------------- materials

def solid(block, data=0):
    return kit.SolidMaterial(id=block, data=data)


def cells(seed, size, rise, palette):
    """Flat patches of `palette`, `size` blocks across at 45% jitter, their edges wandering a block."""
    return kit.CellMaterial(seed=seed, cellSize=size, jitter=45, warp=1, rise=rise, palette=palette)


def layered(axis, *bands):
    """(thickness, material) bands read along `axis`, the last carrying on."""
    return kit.LayeredMaterial(axis=axis, stack=kit.BandStack(ending="repeat", bands=[
        kit.Band(material=material, thickness=thickness) for thickness, material in bands]))


def soil(top, under):
    """One course of a surfacing block over two of soil, which is what a depth stack owes a surface that has to
    stay one course thick."""
    return layered("depth", (1, top), (2, under))


def slope_stack(bands):
    """A surface finished by the ground's angle. `bands` is (degrees, material) lowest first, each band running
    from the edge below it to its own, so one stack finishes the flat, the shoulder and the face of one hill."""
    edges = [0] + [edge for edge, _ in bands]
    return layered("slope", *[(edge - below, material) for below, (edge, material) in zip(edges, bands)])


# ---------------------------------------------------------------- the plan
#
# 168 x 200. Every gap on this board is 20 blocks, in blocks:
#
#   plug-w       x -44..-10   z -10..10    a middle island, neutral, split in two
#   plug-e       x  10..44    z -10..10
#   mid-gap      x -10..10    z -10..10    a build zone, joining the two islands
#
#   cross-w      x -44..-28   z  10..30    a build zone: the limb's face to the island
#   cross-e      x  28..44    z  10..30
#
#   arm-w        x -48..-28   z  30..80    the west limb; 12 blocks of it stand in
#   arm-e        x  28..48    z  30..80    FRONT of the spur, which is the ground
#                                          a raid is met on
#   link-w       x -28..-10   z  42..58    the causeway between a team's own rooms
#   link-e       x  10..28    z  42..58
#   rotate       x -10..10    z  42..58    a build zone, the spur band's own depth
#
#   w-mouth      x -52..-48   z  42..58    where the spur opens off the limb
#   w-approach   x -68..-52   z  42..58    the ledge the west room is entered over
#   w-room       x -84..-68   z  42..58    a shelf hung off the outside of the rim
#   e-mouth      x  48..52    z  42..58    the same spur at the same z
#   e-approach   x  52..68    z  42..58
#   e-room       x  68..84    z  42..58
#
#   cap-w        x -48..-12   z  80..100   the rim's crest, west of the hall
#   spawn        x -12..8     z  80..100   20 x 20, inside ST10's 20 x 30 cap
#   cap-e        x   8..48    z  80..100
#
# The board is symmetric twice over: `rot_180` between the teams, and each
# team's own half mirrored down x = 0, so both wool rooms sit at one z and cost
# the same walk from the hall. A 100% double-symmetric map is ordinary practice
# (author), and `WL9`'s ratio reads 1 for it since amendment 44.
#
# **There are three places to cross and they are all 20 blocks.** A team bridges
# its limb's face onto a middle island, the two islands are joined to each other
# across the axis, and a team's own two rooms are joined across its bay. Four
# build zones a team and one neutral, where one strait was: a middle worth
# holding is one with more than a single way onto it.
#
# **The limb stands 12 blocks in front of its own spur.** That ground is what a
# raid crosses before it reaches the mouth, and the board is 200 rather than 168
# long to carry it: the causeway between the two rooms was 4 blocks off the
# frontline at 168 and no fight fits in 4 blocks (author).
#
# The pit is the ground no piece covers: two bays a team, at z 30..42 and
# z 58..80, plus the void the islands stand in.
#
# Two numbers here were read rather than chosen. The rim was 176 blocks long
# and LN2 read one lane of 176 against a band topping at 110 — a lane is
# measured to its next junction, and a cap with the arms joining only at its
# ends has none. The rooms hung INTO the pit on the first cut, which put
# WL7's wool-to-wool walk at 243 against a band of [50, 227] and left the pit
# cluttered with the two things the board is played for.

SPAWN_AT = (-2, 93)
W_WOOL = (-76, 50)
E_WOOL = (76, 50)

plan = {
    "plan": 2,
    "meta": {"name": "Emberhowe"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 18,
                "surface": 9},
    "pieces": [
        {"id": "arm-w", "role": "piece", "rect": [-24, 15, 10, 25]},
        {"id": "arm-e", "role": "piece", "rect": [14, 15, 10, 25]},
        {"id": "link-w", "role": "piece", "rect": [-14, 21, 9, 8]},
        {"id": "link-e", "role": "piece", "rect": [5, 21, 9, 8]},
        {"id": "cap-w", "role": "piece", "rect": [-24, 40, 18, 10]},
        {"id": "spawn", "role": "spawn", "rect": [-6, 40, 10, 10]},
        {"id": "cap-e", "role": "piece", "rect": [4, 40, 20, 10]},
        {"id": "w-mouth", "role": "piece", "rect": [-26, 21, 2, 8]},
        {"id": "w-approach", "role": "piece", "rect": [-34, 21, 8, 8]},
        {"id": "w-room", "role": "wool-room", "rect": [-42, 21, 8, 8]},
        {"id": "e-mouth", "role": "piece", "rect": [24, 21, 2, 8]},
        {"id": "e-approach", "role": "piece", "rect": [26, 21, 8, 8]},
        {"id": "e-room", "role": "wool-room", "rect": [34, 21, 8, 8]},
        # the two middle islands: neither is fanned, so neither belongs to a
        # team and PL12's mixed-mirrors read does not see them beside the rim
        {"id": "plug-w", "role": "piece", "rect": [-22, -5, 17, 10], "mirrors": False},
        {"id": "plug-e", "role": "piece", "rect": [5, -5, 17, 10], "mirrors": False},
    ],
    "zones": [
        {"id": "mid-gap", "rect": [-5, -5, 10, 10], "holes": []},
        {"id": "cross-wa", "rect": [-22, 5, 8, 10], "holes": []},
        {"id": "cross-ea", "rect": [14, 5, 8, 10], "holes": []},
        {"id": "cross-wb", "rect": [-22, -15, 8, 10], "holes": []},
        {"id": "cross-eb", "rect": [14, -15, 8, 10], "holes": []},
        {"id": "rotate-a", "rect": [-5, 21, 10, 8], "holes": []},
        {"id": "rotate-b", "rect": [-5, -29, 10, 8], "holes": []},
    ],
    "placements": {
        # The hall is 12 x 12 inside a 20 x 24 piece. The door faces LEFT, along
        # the crest, because the piece's other three sides are the pit and the
        # outer coast: a door onto the rim's own edge is SP9's nought blocks of
        # ground. The iron cube stands in the strip between the hall's front
        # wall and the crest's lip, two blocks clear of both, which is WX8.
        "spawns": [{"id": "spawn-howe", "piece": "spawn",
                    "at": [10, 13], "facing": "left",
                    "footprint": [4, 7, 12, 12]}],
        "wools": [
            {"id": "wool-west", "piece": "w-room", "at": [8, 8],
             "footprint": [2, 2, 12, 12]},
            {"id": "wool-east", "piece": "e-room", "at": [8, 8],
             "footprint": [2, 2, 12, 12]},
        ],
        "iron": [{"id": "iron-howe", "piece": "spawn", "at": [10.0, 3.5]}],
        "destroyables": [],
        "cores": [],
    },
    # One wall a room, on the approach's outer interface — sixteen blocks in
    # front of the room's face, never the room's own edge, which PL13 refuses.
    #
    # And never on the limb's own edge either, which is what PL17 says: a wall
    # sits between two pieces of the same width, and the limb runs 50 blocks
    # past the ends of a wall on its edge. The mouth is the four blocks that put
    # the line between two pieces that line up.
    "walls": [
        {"a": "w-approach", "b": "w-mouth"},
        {"a": "e-approach", "b": "e-mouth"},
    ],
}

# ---------------------------------------------------------------- the ground
#
# The board climbs from the water line to the crest and the climb is the raid:
# a bridger lands on a horn at y11 and everything after that is uphill to the
# enemy spawn at y22. Five marks and one push.
#
# The horns are pinned low, the cap is pinned flat, and the arms between them
# are pinned by nothing — which is where the ground gets its shape. Pinning the
# arms too would leave the solver nothing to solve.

# The plug is an island nothing fans, so the compile gives it a relief group of
# its own (`neutral`) and a mark only ever pins cells of the group it is in —
# `RL4` says so, once per mark, for every mark keyed at the wrong one. So the
# two grounds are stated separately, which is what they are.
relief = {
    "team": kit.SketchReliefJson(
        base=9, reach=0, step=1, landform="rolling",
        grain=kit.ReliefGrainJson(amplitude=1.2, scale=22, seed=5101),
        marks=[
            # the west horn: a wobbled ring of radius 15 round (-38, 40)
            kit.ReliefMarkJson(id="horn-w", kind="area", h=11, bevel=4, ring=[
                [-24.2, 40.0], [-27.79, 46.56], [-31.02, 55.27], [-39.98, 53.78], [-47.49, 50.96], [-52.09, 44.14],
                [-54.24, 35.23], [-49.51, 26.71], [-40.2, 24.72], [-32.25, 27.4], [-26.1, 32.35]]),
            # the east horn: a wobbled ring of radius 15 round (38, 40)
            kit.ReliefMarkJson(id="horn-e", kind="area", h=11, bevel=4, ring=[
                [52.92, 40.0], [50.78, 48.21], [44.1, 53.37], [36.26, 52.08], [27.42, 52.21], [25.19, 43.76],
                [22.86, 35.56], [27.72, 28.13], [35.6, 23.3], [44.74, 25.25], [49.06, 32.89]]),
            # the crest: x -50..50, z 82..102 walked as a wandering ring
            kit.ReliefMarkJson(id="crest", kind="area", h=22, bevel=6, ring=[
                [-49.14, 79.7], [-27.0, 83.23], [2.34, 79.51], [24.69, 81.02], [47.75, 79.99], [47.61, 88.44],
                [49.58, 94.38], [49.05, 97.71], [51.99, 102.03], [27.04, 101.75], [-1.59, 102.8], [-25.87, 102.79],
                [-51.58, 101.92], [-51.35, 96.28], [-50.67, 93.01], [-48.37, 86.44]]),
            # each shelf sits at the height the arm has reached beside it, so
            # the wall's interface is a step rather than a face
            # Wide enough that the WALL's own run stands on the flat core and
            # not in the bevel: a wall's top is one level taken from the highest
            # ground it crosses, so ground that falls along its run is added to
            # its face at the low end, and past four courses ST4 says so. On the
            # first cut the seam fell 11 to 14 over sixteen blocks and the wall
            # came out six courses proud.
            # the west shelf: a wobbled ring of radius 20 round (-66, 50)
            kit.ReliefMarkJson(id="w-shelf", kind="area", h=15, bevel=2, ring=[
                [-43.99, 50.0], [-48.94, 60.96], [-57.11, 69.47], [-68.81, 69.57], [-78.15, 64.03], [-86.69, 56.08],
                [-83.82, 44.77], [-80.9, 32.8], [-68.68, 31.38], [-57.71, 31.84], [-47.5, 38.11]]),
            # the east shelf: a wobbled ring of radius 20 round (66, 50)
            kit.ReliefMarkJson(id="e-shelf", kind="area", h=15, bevel=2, ring=[
                [83.46, 50.0], [80.74, 59.47], [74.08, 67.69], [63.41, 67.98], [52.84, 65.19], [46.5, 55.72],
                [49.21, 45.07], [52.24, 34.12], [63.13, 30.06], [75.21, 29.83], [83.71, 38.62]]),
            # the plug stands between the horns and the crest in height as well
            # as in position: a team bridges DOWN onto it from a limb at 11 and
            # fights UP off it toward nothing, since the rim's own crest is 22
        ],
        # the spatter cone, centred over the water off the west coast so that
        # what stands on the board is its seaward flank and nothing else: a
        # bluff along the shore at z 60..84, with the flat crest west of the
        # spawn left open as the lane to the board's left side. A cone seated
        # inland fills that lane instead — the land at this z runs from the
        # coast at x -48 to the spawn's wall at x -12, so a 20-block landform
        # anywhere in it is the whole width.
        #
        # The skirt grades 5 over 10 and the crown 4 over a radius of 10 —
        # 1.14x apart, where past twice RL6 says the ground steps at the
        # push's own outline. `roughness` stays 0: it wobbles the skirt
        # against a noise field, and on a landform read as ground that is
        # damage rather than weathering.
        pushes=[
            # the cone's outline: a wobbled ring of radius 10 round (-50, 92)
            kit.ReliefPushJson(id="spatter-cone", amount=5, falloff=10, crown=4, roughness=0, seed=5122, ring=[
                [-41.47, 92.0], [-43.66, 97.32], [-48.41, 101.01], [-54.89, 100.48], [-58.03, 94.92], [-58.25, 89.0],
                [-55.89, 81.8], [-48.03, 80.84], [-40.8, 84.28]]),
        ],
    ),
    # The plug stands between the horns and the crest in height as well as in
    # position: a team bridges ACROSS to it from a limb pinned at 11 and fights
    # up a low bench, where the rim's own crest is 22.
    #
    # The push states no crown, so it grades its skirt at one rate and leaves
    # the ring's own interior flat. A crown over a patch this size grades the
    # whole of it and `RL5` reads a ramp end to end with nowhere to stand — and
    # somewhere to stand is the entire point of a middle two teams contest.
    #
    # The two islands share ONE relief group, so each is pinned in it. A mark
    # covering only the west one leaves the east to whatever the solver does
    # with an unpinned island, which was 66 barrier steps and two cliffs.
    "neutral": kit.SketchReliefJson(
        base=9, reach=0, step=1, landform="plain",
        grain=kit.ReliefGrainJson(amplitude=1.0, scale=14, seed=5102),
        marks=[
            # the west plug: x -42..-12, z -8..8 walked as a wandering ring
            kit.ReliefMarkJson(id="plug-w", kind="area", h=14, bevel=4, ring=[
                [-42.96, -7.76], [-36.11, -6.61], [-25.94, -8.59], [-18.2, -8.48], [-11.05, -8.78], [-11.93, -5.64],
                [-10.93, 1.46], [-12.5, 4.31], [-12.67, 9.24], [-20.08, 7.92], [-26.32, 8.42], [-35.16, 6.96],
                [-40.78, 6.83], [-42.35, 4.89], [-42.99, -0.27], [-42.91, -5.34]]),
            # the east plug: x 12..42, z -8..8 walked as a wandering ring
            kit.ReliefMarkJson(id="plug-e", kind="area", h=14, bevel=4, ring=[
                [11.71, -9.53], [20.23, -7.64], [25.45, -9.4], [35.11, -9.6], [40.21, -7.35], [41.47, -5.33],
                [43.53, -1.03], [40.36, 3.04], [43.03, 7.24], [35.63, 9.16], [25.89, 8.37], [20.03, 8.83],
                [12.8, 6.46], [13.05, 4.16], [13.25, -0.6], [11.6, -3.25]]),
        ],
        pushes=[
            # the west bench: x -40..-14, z -7..7 walked as a wandering ring
            kit.ReliefPushJson(id="bench-w", amount=5, falloff=10, roughness=0, seed=5124, ring=[
                [-39.9, -7.9], [-33.24, -6.09], [-26.47, -6.33], [-20.45, -7.77], [-14.16, -8.08], [-14.37, -3.16],
                [-13.55, -1.03], [-14.84, 2.59], [-13.71, 8.12], [-20.08, 7.92], [-27.71, 7.04], [-33.19, 7.81],
                [-41.12, 6.89], [-40.88, 3.09], [-39.84, 0.67], [-40.64, -4.24]]),
            # the east bench: x 14..40, z -7..7 walked as a wandering ring
            kit.ReliefPushJson(id="bench-e", amount=5, falloff=10, roughness=0, seed=5126, ring=[
                [14.99, -7.85], [21.48, -7.47], [26.45, -7.4], [32.63, -6.87], [40.98, -6.18], [38.82, -2.74],
                [41.06, 0.46], [40.04, 3.3], [40.16, 7.86], [33.81, 7.16], [26.3, 6.97], [20.0, 7.9], [14.73, 6.4],
                [14.99, 4.52], [14.74, 0.23], [14.04, -3.85]]),
        ],
    ),
}

# ---------------------------------------------------------------- the paint
#
# Three themes. The rim is the board's one ground, finished on the slope axis
# so the ash flat, the scoria shoulder and the crater face are three different
# grounds on one hillside; the drifts and the yards are the two places made of
# something else, each a shape carrying its own theme.
#
# The band edges are cut off this board's own GET .../incline.

ASH = solid(1, 3)            # diorite — the pale ash
ASH_PALE = solid(1, 4)       # polished diorite
STONE = solid(1, 0)
ANDESITE = solid(1, 5)
GRAVEL = solid(13, 0)
SCORIA = solid(172, 0)       # hardened clay — the rust the shoulders weather to
OBSIDIAN = solid(49, 0)
COAL = solid(173, 0)
COBBLE = solid(4, 0)
GRIT = solid(3, 1)           # coarse dirt
DIRT = solid(3, 0)
PODZOL = solid(3, 2)

# the crater's own face: black glass in a grey rock
CRATER_FACE = cells(5131, 7, 5, [ANDESITE, OBSIDIAN, COAL])
# The flat carries coarse dirt as well as ash, and it is what the wood stands
# in: DR-ROOT admits grass and the three dirts and nothing else, so a board
# surfaced in diorite and gravel alone has nowhere a tree belongs. Grit rather
# than grass, because a dead volcano's flat is weathered ash and not a meadow.
#
# The cell is 14 rather than 7 because soil in 7-block cells is soil a single
# trunk fits in and a crown does not: the seats mask answers 1 091 cells and
# almost none of them with four blocks of soil around it, so a tree seats and
# its canopy lands on rock. A patch a wood can stand in is what the wood needs.
ASH_FLAT = cells(5132, 14, 0, [ASH, GRAVEL, GRIT])
SCORIA_SLOPE = cells(5133, 6, 3, [SCORIA, GRAVEL])

SLOPE_FLAT, SLOPE_SHOULDER = 22, 40


def rock_fill(seed):
    """Stone and andesite in nine-block voronoi cells."""
    return kit.VoronoiMaterial(seed=seed, cellSize=9, rise=4, bands=[kit.VoronoiBand(material=STONE, depth=5),
                                                                     kit.VoronoiBand(material=ANDESITE, depth=4)])


def theme(surface, wall, fill, rim, rim_enabled=True, rim_edges="void"):
    """A theme on one block of bedrock, its wall on every face, its rim one course deep and its surface three."""
    return kit.TerrainTheme(bedrock=kit.BedrockSpec(relative=False, value=1), fill=fill, wall=wall, wallEnabled=True,
                            wallOnTerrainFaces=True, rim=kit.TopBand(enabled=rim_enabled, depth=1, material=rim),
                            rimEdges=rim_edges, surface=kit.TopBand(enabled=True, depth=3, material=surface))


rim_theme = theme(
    surface=slope_stack([
        (SLOPE_FLAT, soil(ASH_FLAT, GRAVEL)),
        (SLOPE_SHOULDER, soil(SCORIA_SLOPE, GRAVEL)),
        (90, layered("depth", (3, CRATER_FACE))),
    ]),
    wall=CRATER_FACE,
    # a voronoi draws a diagram, so it is the body of the rock nobody sees
    # until a wall is cut, and it is made of stone
    fill=rock_fill(5134),
    rim=ANDESITE)

drift_theme = theme(
    surface=soil(cells(5136, 14, 0, [ASH, ASH_PALE, STONE, GRIT]), GRAVEL),
    wall=CRATER_FACE, fill=rock_fill(5135), rim=ANDESITE, rim_enabled=False)

yard_theme = theme(
    surface=soil(cells(5139, 5, 0, [SCORIA, ANDESITE, COBBLE]), STONE),
    wall=cells(5138, 6, 4, [COBBLE, ANDESITE]), fill=rock_fill(5137), rim=COBBLE, rim_edges="boundary")

grove_theme = theme(
    # every cell of it roots a tree, which is the whole reason it exists: soil
    # scattered through an ash pattern seats a trunk and drops the crown on
    # rock, because a `cells` patch the size of one tree is not a wood's ground
    surface=soil(cells(5148, 5, 0, [GRIT, DIRT, PODZOL]), GRIT),
    wall=CRATER_FACE, fill=rock_fill(5147), rim=ANDESITE, rim_enabled=False)

# ---------------------------------------------------------------- the shapes
#
# Every piece takes globals.surface, so the compile emits one ground shape at
# base_height 9 and a patch owns a cell's paint only where its own drawn top
# equals the tallest there — which is why each states 9 rather than 10.

GROUND = 9


def patch(sid, paint, vertices):
    """A polygon of ground GROUND blocks thick, painted with the theme `paint`."""
    return kit.SketchShape(id=sid, type="polygon", operation="add", floor=0, base_height=GROUND, theme=paint,
                           vertices=vertices)


add_shapes = [
    # a wobbled ring of radius 14 round (28, 90)
    patch("drift-cap", "drift", [
        [44.92, 90.0], [38.99, 95.77], [35.22, 100.47], [29.88, 105.46], [22.57, 104.31], [16.02, 100.61],
        [17.45, 92.6], [14.04, 86.56], [16.3, 79.63], [23.9, 79.18], [29.53, 77.36], [34.65, 80.37], [43.46, 81.89]]),
    # a wobbled ring of radius 10 round (-38, 60)
    patch("drift-armw", "drift", [
        [-29.98, 60.0], [-28.41, 66.16], [-32.9, 71.17], [-39.38, 69.56], [-45.98, 69.2], [-47.84, 62.89],
        [-49.34, 56.67], [-43.73, 53.39], [-39.74, 47.9], [-33.72, 50.64], [-30.97, 55.48]]),
    # a wobbled ring of radius 9 round (38, 66)
    patch("drift-arme", "drift", [
        [46.02, 66.0], [44.84, 70.4], [41.96, 74.68], [36.94, 73.38], [32.87, 71.92], [30.07, 68.33], [28.59, 63.24],
        [30.9, 57.81], [36.9, 58.37], [42.56, 56.02], [47.35, 59.99]]),
    # x -14..10, z 82..98 walked as a wandering ring
    patch("spawn-yard", "yard", [
        [-14.16, 83.23], [-8.9, 83.42], [-1.98, 80.43], [3.98, 82.45], [9.76, 81.41], [11.29, 85.76], [9.43, 90.3],
        [10.05, 94.92], [10.16, 97.32], [4.74, 96.36], [-1.01, 96.85], [-7.73, 98.87], [-13.52, 97.18],
        [-14.68, 92.29], [-13.63, 91.37], [-15.24, 85.53]]),
    # x -83..-69, z 43..57 walked as a wandering ring
    patch("w-room-yard", "yard", [
        [-82.59, 42.49], [-78.3, 43.19], [-75.22, 44.08], [-73.05, 42.44], [-68.5, 43.69], [-68.57, 46.57],
        [-69.05, 51.08], [-69.85, 53.16], [-70.36, 57.78], [-73.44, 56.81], [-76.7, 56.16], [-78.39, 56.26],
        [-82.99, 56.13], [-82.38, 54.54], [-83.8, 50.7], [-83.47, 47.79]]),
    # x 69..83, z 43..57 walked as a wandering ring
    patch("e-room-yard", "yard", [
        [69.94, 43.91], [72.72, 42.39], [74.76, 43.46], [78.41, 44.37], [84.17, 42.0], [82.96, 46.81], [83.31, 49.14],
        [84.06, 52.17], [82.96, 56.22], [79.89, 57.77], [76.71, 56.12], [71.74, 57.71], [68.69, 55.85],
        [67.91, 53.97], [69.93, 50.44], [68.92, 46.62]]),
    # the groves: soil, authored where the wood stands rather than scattered
    # the west arm's: a wobbled ring of radius 10 round (-34, 50)
    patch("grove-armw", "grove", [
        [-24.47, 50.0], [-26.14, 55.05], [-29.79, 59.22], [-35.37, 59.56], [-41.65, 58.83], [-45.69, 53.43],
        [-43.75, 47.14], [-39.25, 43.94], [-35.51, 39.53], [-30.16, 41.59], [-23.8, 43.44]]),
    # the east arm's: a wobbled ring of radius 10 round (34, 50)
    patch("grove-arme", "grove", [
        [44.36, 50.0], [43.74, 56.26], [37.57, 57.82], [32.81, 58.31], [28.44, 56.42], [23.25, 53.16], [25.06, 47.38],
        [26.77, 41.65], [32.35, 38.49], [38.56, 40.01], [43.58, 43.84]]),
    # the cap's: a wobbled ring of radius 8 round (-42, 94)
    patch("grove-cap", "grove", [
        [-33.06, 94.0], [-35.66, 98.07], [-38.19, 102.34], [-43.31, 103.13], [-47.08, 99.87], [-49.85, 96.3],
        [-48.5, 92.09], [-47.07, 88.15], [-42.94, 87.45], [-39.23, 87.94], [-34.83, 89.39]]),
]

# The rim parapet: a revetment along the crest's own lip, where the cap meets
# the pit. Drawn as a polyline so the rasterizer splines it into a curve rather
# than a chain of chords, and kept four blocks off the hall's footprint,
# because a made thing drawn through a stamp's courses is simply absent from
# the world and only SK18's header says so.
#
# It runs the pit's own width and stops there — x -28..28, the span the cap
# actually faces void along. Carried out to the limbs it stands across the
# mouth each limb opens off the cap at, which is the lane every journey on this
# board runs along: a two-course revetment there is a step every walk out of
# the hall pays, and the walk to the west room read `barrier +6 at (-34, 62)`
# with the parapet and a tree's crown stacked over each other on the line.


def parapet(sid, vertices):
    return kit.SketchShape(id=sid, type="polyline", operation="add", floor=23, base_height=2, radius=1.0,
                           stroke_edge="solid", keepClear=True, material=cells(5151, 4, 2, [COBBLE, ANDESITE]),
                           vertices=vertices)


rim_parapet = kit.AddedLayer(
    id="rim-parapet", name="the rim parapet", base_y=0, kind="made", part_of="spawn",
    groups=[kit.SketchGroup(id="rim-parapet", name="the rim parapet", mirrors=True,
                            shapeIds=["rim-parapet-west", "rim-parapet-east"])],
    shapes=[parapet("rim-parapet-west", [[-28, 81], [-22, 82], [-14, 81]]),
            parapet("rim-parapet-east", [[14, 81], [22, 82], [28, 81]])])

# ---------------------------------------------------------------- the dressing
#
# Circulation first: the hall's door to each room, and the crest out to each
# horn, which is the way an attacker leaves and the way a defender returns.
# Everything else is placed to the outside of a piece rather than down the
# middle of it, and nothing stands where a bridger arrives.

# The copied trees, each the showcase tree it names, as the studio's tree library carries it.
from showcase import trees as studio_trees
SHOWCASE = studio_trees()
styles = {key: kit.build("TreeStyle", SHOWCASE[tree]["style"]) for key, tree in {
    "scrub": "tiny-oak-2",       # tiny oak — the pioneer scrub
    "fir": "tiny-spruce-2",      # tiny spruce — the crest
}.items()}
styles["bomb"] = kit.BoulderStyle(form="round", size=2, mossy=False, rock=kit.TurbulenceMaterial(
    seed=5161, scale=3, octaves=3, stops=[STONE, COBBLE, ANDESITE], rise=3))

# gravel, andesite and cobblestone: three blocks a reader cannot quite tell
# apart, which is what a path on hard ground is
PAVE = cells(5162, 3, 0, [GRAVEL, ANDESITE, COBBLE])


def way(pid, seed, points):
    return kit.StrokeProp(id=pid, seed=seed, radius=2, style="solid", claimsGround=True, pave=PAVE, points=points)


props = [
    way("way-west", 5171, [[-12, 90], [-26, 93], [-42, 86], [-45, 72], [-45, 60], [-50, 50]]),
    way("way-east", 5172, [[8, 90], [26, 93], [42, 86], [45, 72], [45, 60], [50, 50]]),
    way("horn-way-west", 5173, [[-45, 60], [-43, 44], [-41, 34]]),
    way("horn-way-east", 5174, [[45, 60], [43, 44], [41, 34]]),

    # One works shed, on the crest's east corner, and the board carries no
    # other free-standing building. A 20-wide limb cannot hold one and still
    # leave DR-PASS its eight blocks on the side that is not a coast; the west
    # crest is the cone's, and a building inside a push's skirt rises nine
    # blocks across its own footprint, which DR-SLOPE declines; and the spurs
    # are the wool rooms' door approaches. Bare ground chosen beats dressing
    # that was not, and the limbs are what this board is fought over.
    kit.HouseProp(id="shed-crest", seed=5177, style="works", front="negZ",
                  wings=[kit.AuthoredWing(corners=[[29, 64], [37, 70]], spec=kit.WingSpec(storeysHigh=2))]),
]

# Every position below came off POST .../sketch/seats for its own kind — a
# raster of the cells a footprint's minimum corner may sit on — rather than off
# the map in my head, which declined eleven props on the first pass. Scrub goes
# to the outside of each piece and never on the brink a bridger leaves from, so
# nothing stands within eighteen blocks of either horn's tip.
#
# A TREE's mask is the narrow one on this board, because `DR-ROOT` refuses every
# cell whose surface is not grass or one of the three dirts, and the ground here
# is ash over rock: 1 091 of the board's 12 930 cells seat a tree, against 7 659
# for a boulder. The grit in ASH_FLAT and in the drift's own cells is what those
# 1 091 are made of, and the causeway is taken out of them by hand — a lane two
# teams rotate through is not somewhere to put a wood.
props += [kit.TreeProp(id=f"scrub-{i}", seed=5200 + i, x=x, z=z, style="scrub")
          for i, (x, z) in enumerate([(-36, 56), (-32, 44), (-43, 94)])]
props += [kit.TreeProp(id=f"fir-{i}", seed=5220 + i, x=x, z=z, style="fir")
          for i, (x, z) in enumerate([(36, 56), (32, 44)])]
# volcanic bombs, each on ground the incline read calls flat — a boulder is a
# mass that was thrown, so DR-STEEP turns one away from a face
props += [kit.BoulderProp(id=f"bomb-{i}", seed=5240 + i, x=x, z=z, style="bomb")
          for i, (x, z) in enumerate([(-33, 34), (33, 34), (-38, 70),
                                      (38, 76), (-30, 74)])]

# a cinder field is bare: the coverage is low and the tall share lower, because
# two-block grass in front of a wool room is cover nobody authored
props += [
    kit.FloraProp(id="flora", seed=5180,
                  spec=kit.FloraSpec(coverage=0.11, scale=28, octaves=3, fernShare=0.16, flowerShare=0.04,
                                     flowerScale=20, tallShare=0.03),
                  # x -84..84, z 12..84 walked as a wandering ring
                  points=[
                      [-84.65, 12.63], [-42.71, 10.72], [0.98, 13.89], [41.51, 9.73], [82.8, 14.38], [84.58, 30.54],
                      [81.8, 45.66], [85.59, 67.01], [81.59, 85.66], [41.12, 85.45], [-0.87, 84.9], [-40.55, 85.92],
                      [-84.67, 83.93], [-82.65, 66.37], [-83.79, 47.64], [-84.49, 31.8]]),
]

# ---------------------------------------------------------------- the house
#
# Forked from the shipped `alpine mining` preset, whose footing is already
# null. The ground is pale ash over black rock, so what stands on it is warm
# spruce over a rust plinth — a building has to read as built from across the
# pit, which means its walls are not in the family under its feet.

SPRUCE = solid(5, 1)
DARKOAK = solid(5, 5)
SPRUCE_LOG = kit.LaidLogMaterial(id=17, data=1)

PLAIN = {"field": None, "border": None, "borderWidth": 1, "inlay": None,
         "inlayInset": 2, "isPlain": True}
NO_WINDOW = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
             "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}


def storey(clear, panel):
    """A storey `clear` blocks high, walled in a course of scoria, `panel` courses of spruce and dark oak and a
    course of laid spruce log."""
    return {
        "clear": clear,
        "wall": {"stack": {"bands": [
            {"material": SCORIA, "thickness": 1},
            {"material": cells(5191, 3, 2, [SPRUCE, DARKOAK]), "thickness": panel},
            {"material": SPRUCE_LOG, "thickness": 1}], "ending": "repeat"},
            "extent": clear},
        "post": solid(17, 1),
        "windows": {"form": "arched", "block": 134, "hostBlock": -1, "hostData": 0,
                    "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
        "surface": PLAIN, "deck": None, "headroom": clear,
    }


WORKS = kit.build("HouseStyle", {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": SCORIA, "thickness": 1}],
                            "ending": "repeat"}, "extent": 1},
        "surface": PLAIN,
        "footing": None},
    "roof": {"form": "gable", "pitch": 2, "slab": 126, "slabData": 1,
             "overhang": 1, "ridgeCap": True, "hole": False,
             "body": SPRUCE, "verge": DARKOAK, "gable": DARKOAK,
             "gableWindows": {"form": "open", "block": 102, "hostBlock": -1,
                              "hostData": 0, "data": 0, "sill": 1, "width": 1,
                              "height": 1, "spacing": 3}},
    "wall": {"stack": {"bands": [{"material": SCORIA, "thickness": 1}],
                       "ending": "repeat"}, "extent": 5},
    "post": solid(17, 1),
    "windows": NO_WINDOW,
    "storeys": [storey(5, 3)],
    "porch": None, "front": None,
    # a beam has to be the end of something, so the wall under it carries a
    # course of laid log — which is the last band of every storey above
    "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 134, "fill": "upperSlab",
                         "fillBlock": 126, "fillData": 1},
                "width": 2, "height": 3},
})

# The spawn hall and the wool rooms are the two structures a player sees from
# the inside, and a finish stating no roomStyles leaves both on the studio's
# bedrock box at 200 with no finding. Both are this board's works, hipped and
# built taller.
HALL = kit.build("HouseStyle", {
    **WORKS,
    "roof": {"form": "hip", "pitch": 2, "slab": 126, "slabData": 1,
             "overhang": 1, "ridgeCap": False, "hole": False,
             "body": SPRUCE, "verge": DARKOAK, "gable": None,
             "gableWindows": NO_WINDOW},
    "storeys": [storey(7, 5)],
})

styles["works"] = kit.HouseStyleRef(shell=WORKS)

refinement = kit.Refinement(
    authors=["Opus 5"],
    created="2026-09-21",
    themes={"rim": rim_theme, "drift": drift_theme, "yard": yard_theme,
            "grove": grove_theme},
    mapTheme="rim",
    # Extreme hills (#8ab689): there is almost no grass on a cinder field, and
    # what the flora pass does put there stays muted against the ash rather
    # than reading as a meadow. Asked of GET /api/terrain/biomes.
    biome=kit.SolidBiome(id=3),
    relief=relief,
    addShapes=add_shapes,
    addLayers=[rim_parapet],
    roomStyles=kit.SketchRoomStyles(spawn=HALL, wool=HALL),
    dressing=kit.DressingDoc(styles=styles, props=props),
)

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(refinement, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
print("wrote", SLUG)
