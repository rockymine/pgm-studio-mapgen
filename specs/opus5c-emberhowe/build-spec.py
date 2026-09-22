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

Writes opus5c-emberhowe.plan.json and opus5c-emberhowe.finish.json.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from opus5c import (solid, cells, field, voronoi, band, stack, soil,
                    slope_stack, blob, wander_rect, arc_ring, tree_body,
                    load_cache, save_cache, write)

SLUG = "opus5c-emberhowe"
CELL = 2

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
    "team": {
        "base": 9, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1.2, "scale": 22, "seed": 5101},
        "marks": [
            {"id": "horn-w", "kind": "area", "h": 11, "bevel": 4,
             "ring": blob(-38, 40, 15, points=11, wobble=0.2, seed=5111)},
            {"id": "horn-e", "kind": "area", "h": 11, "bevel": 4,
             "ring": blob(38, 40, 15, points=11, wobble=0.2, seed=5112)},
            {"id": "crest", "kind": "area", "h": 22, "bevel": 6,
             "ring": wander_rect(-50, 82, 50, 102, wobble=2.5, seed=5113)},
            # each shelf sits at the height the arm has reached beside it, so
            # the wall's interface is a step rather than a face
            # Wide enough that the WALL's own run stands on the flat core and
            # not in the bevel: a wall's top is one level taken from the highest
            # ground it crosses, so ground that falls along its run is added to
            # its face at the low end, and past four courses ST4 says so. On the
            # first cut the seam fell 11 to 14 over sixteen blocks and the wall
            # came out six courses proud.
            {"id": "w-shelf", "kind": "area", "h": 15, "bevel": 2,
             "ring": blob(-66, 50, 20, points=11, wobble=0.14, seed=5114)},
            {"id": "e-shelf", "kind": "area", "h": 15, "bevel": 2,
             "ring": blob(66, 50, 20, points=11, wobble=0.14, seed=5115)},
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
        "pushes": [
            {"id": "spatter-cone",
             "ring": blob(-50, 92, 10, points=9, wobble=0.22, seed=5121),
             "amount": 5, "falloff": 10, "crown": 4, "roughness": 0,
             "seed": 5122},
        ],
    },
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
    "neutral": {
        "base": 9, "reach": 0, "step": 1, "landform": "plain",
        "grain": {"amplitude": 1.0, "scale": 14, "seed": 5102},
        "marks": [
            {"id": "plug-w", "kind": "area", "h": 14, "bevel": 4,
             "ring": wander_rect(-42, -8, -12, 8, wobble=1.8, seed=5116)},
            {"id": "plug-e", "kind": "area", "h": 14, "bevel": 4,
             "ring": wander_rect(12, -8, 42, 8, wobble=1.8, seed=5117)},
        ],
        "pushes": [
            {"id": "bench-w",
             "ring": wander_rect(-40, -7, -14, 7, wobble=1.2, seed=5123),
             "amount": 5, "falloff": 10, "roughness": 0, "seed": 5124},
            {"id": "bench-e",
             "ring": wander_rect(14, -7, 40, 7, wobble=1.2, seed=5125),
             "amount": 5, "falloff": 10, "roughness": 0, "seed": 5126},
        ],
    },
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

rim_theme = {
    "bedrock": {"relative": False, "value": 1},
    # a voronoi draws a diagram, so it is the body of the rock nobody sees
    # until a wall is cut, and it is made of stone
    "fill": voronoi(5134, 9, [(5, STONE), (4, ANDESITE)]),
    "wall": CRATER_FACE,
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": ANDESITE},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3,
                "material": slope_stack([
                    (SLOPE_FLAT, soil(ASH_FLAT, GRAVEL)),
                    (SLOPE_SHOULDER, soil(SCORIA_SLOPE, GRAVEL)),
                    (90, stack("depth", [band(3, CRATER_FACE)])),
                ])},
}

drift_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": voronoi(5135, 9, [(5, STONE), (4, ANDESITE)]),
    "wall": CRATER_FACE,
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": ANDESITE},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(5136, 14, 0, [ASH, ASH_PALE, STONE, GRIT]),
                                 GRAVEL)},
}

yard_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": voronoi(5137, 9, [(5, STONE), (4, ANDESITE)]),
    "wall": cells(5138, 6, 4, [COBBLE, ANDESITE]),
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": COBBLE},
    "rimEdges": "boundary",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(5139, 5, 0, [SCORIA, ANDESITE, COBBLE]),
                                 STONE)},
}

grove_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": voronoi(5147, 9, [(5, STONE), (4, ANDESITE)]),
    "wall": CRATER_FACE,
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": ANDESITE},
    "rimEdges": "void",
    # every cell of it roots a tree, which is the whole reason it exists: soil
    # scattered through an ash pattern seats a trunk and drops the crown on
    # rock, because a `cells` patch the size of one tree is not a wood's ground
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(5148, 5, 0, [GRIT, DIRT, PODZOL]), GRIT)},
}

# ---------------------------------------------------------------- the shapes
#
# Every piece takes globals.surface, so the compile emits one ground shape at
# base_height 9 and a patch owns a cell's paint only where its own drawn top
# equals the tallest there — which is why each states 9 rather than 10.

GROUND = 9

add_shapes = [
    {"id": "drift-cap", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "theme": "drift",
     "vertices": blob(28, 90, 14, points=13, wobble=0.26, seed=5141)},
    {"id": "drift-armw", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "theme": "drift",
     "vertices": blob(-38, 60, 10, points=11, wobble=0.24, seed=5142)},
    {"id": "drift-arme", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "theme": "drift",
     "vertices": blob(38, 66, 9, points=11, wobble=0.24, seed=5143)},
    {"id": "spawn-yard", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "theme": "yard",
     "vertices": wander_rect(-14, 82, 10, 98, wobble=2.0, seed=5144)},
    {"id": "w-room-yard", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "theme": "yard",
     "vertices": wander_rect(-83, 43, -69, 57, wobble=1.4, seed=5145)},
    {"id": "e-room-yard", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "theme": "yard",
     "vertices": wander_rect(69, 43, 83, 57, wobble=1.4, seed=5146)},
    # the groves: soil, authored where the wood stands rather than scattered
    {"id": "grove-armw", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "theme": "grove",
     "vertices": blob(-34, 50, 10, points=11, wobble=0.22, seed=5149)},
    {"id": "grove-arme", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "theme": "grove",
     "vertices": blob(34, 50, 10, points=11, wobble=0.22, seed=5150)},
    {"id": "grove-cap", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "theme": "grove",
     "vertices": blob(-42, 94, 8, points=11, wobble=0.22, seed=5151)},
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
rim_parapet = {
    "id": "rim-parapet", "name": "the rim parapet", "base_y": 0,
    "kind": "made", "part_of": "spawn",
    "groups": [{"id": "rim-parapet", "name": "the rim parapet", "mirrors": True,
                "shapeIds": ["rim-parapet-west", "rim-parapet-east"]}],
    "shapes": [
        {"id": "rim-parapet-west", "type": "polyline", "operation": "add",
         "floor": 23, "base_height": 2, "radius": 1.0,
         "stroke_edge": "solid", "keepClear": True,
         "material": cells(5151, 4, 2, [COBBLE, ANDESITE]),
         "vertices": [[-28, 81], [-22, 82], [-14, 81]]},
        {"id": "rim-parapet-east", "type": "polyline", "operation": "add",
         "floor": 23, "base_height": 2, "radius": 1.0,
         "stroke_edge": "solid", "keepClear": True,
         "material": cells(5151, 4, 2, [COBBLE, ANDESITE]),
         "vertices": [[14, 81], [22, 82], [28, 81]]},
    ],
}

# ---------------------------------------------------------------- the dressing
#
# Circulation first: the hall's door to each room, and the crest out to each
# horn, which is the way an attacker leaves and the way a defender returns.
# Everything else is placed to the outside of a piece rather than down the
# middle of it, and nothing stands where a bridger arrives.

cache_path = os.path.join(HERE, "trees.json")
cache = load_cache(cache_path)
SCRUB = tree_body("showcase-r6-2", cache)       # tiny oak — the pioneer scrub
FIR = tree_body("showcase-r4-2", cache)         # tiny spruce — the crest
save_cache(cache_path, cache)

styles = {
    "scrub": SCRUB,
    "fir": FIR,
    "bomb": {"kind": "boulder", "form": "round", "size": 2, "mossy": False,
             "rock": field(5161, 3, 3, [STONE, COBBLE, ANDESITE], rise=3,
                           kind="turbulence")},
    "works": {"kind": "house", "shell": None},   # filled below
}

# gravel, andesite and cobblestone: three blocks a reader cannot quite tell
# apart, which is what a path on hard ground is
PAVE = cells(5162, 3, 0, [GRAVEL, ANDESITE, COBBLE])

props = [
    {"id": "way-west", "kind": "stroke", "seed": 5171, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[-12, 90], [-26, 93], [-42, 86], [-45, 72], [-45, 60],
                [-50, 50]]},
    {"id": "way-east", "kind": "stroke", "seed": 5172, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[8, 90], [26, 93], [42, 86], [45, 72], [45, 60], [50, 50]]},
    {"id": "horn-way-west", "kind": "stroke", "seed": 5173, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[-45, 60], [-43, 44], [-41, 34]]},
    {"id": "horn-way-east", "kind": "stroke", "seed": 5174, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[45, 60], [43, 44], [41, 34]]},

    # One works shed, on the crest's east corner, and the board carries no
    # other free-standing building. A 20-wide limb cannot hold one and still
    # leave DR-PASS its eight blocks on the side that is not a coast; the west
    # crest is the cone's, and a building inside a push's skirt rises nine
    # blocks across its own footprint, which DR-SLOPE declines; and the spurs
    # are the wool rooms' door approaches. Bare ground chosen beats dressing
    # that was not, and the limbs are what this board is fought over.
    {"id": "shed-crest", "kind": "house", "seed": 5177, "style": "works",
     "front": "negZ",
     "wings": [{"corners": [[29, 64], [37, 70]], "spec": {"storeysHigh": 2}}]},
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
props += [{"id": f"scrub-{i}", "kind": "tree", "seed": 5200 + i,
           "x": x, "z": z, "style": "scrub"}
          for i, (x, z) in enumerate([(-36, 56), (-32, 44), (-43, 94)])]
props += [{"id": f"fir-{i}", "kind": "tree", "seed": 5220 + i,
           "x": x, "z": z, "style": "fir"}
          for i, (x, z) in enumerate([(36, 56), (32, 44)])]
# volcanic bombs, each on ground the incline read calls flat — a boulder is a
# mass that was thrown, so DR-STEEP turns one away from a face
props += [{"id": f"bomb-{i}", "kind": "boulder", "seed": 5240 + i,
           "x": x, "z": z, "style": "bomb"}
          for i, (x, z) in enumerate([(-33, 34), (33, 34), (-38, 70),
                                      (38, 76), (-30, 74)])]

# a cinder field is bare: the coverage is low and the tall share lower, because
# two-block grass in front of a wool room is cover nobody authored
props += [
    {"id": "flora", "kind": "flora", "seed": 5180,
     "points": wander_rect(-84, 12, 84, 84, wobble=2.5, seed=5181),
     "spec": {"coverage": 0.11, "scale": 28, "octaves": 3, "fernShare": 0.16,
              "flowerShare": 0.04, "flowerScale": 20, "tallShare": 0.03}},
]

# ---------------------------------------------------------------- the house
#
# Forked from the shipped `alpine mining` preset, whose footing is already
# null. The ground is pale ash over black rock, so what stands on it is warm
# spruce over a rust plinth — a building has to read as built from across the
# pit, which means its walls are not in the family under its feet.

SPRUCE = solid(5, 1)
DARKOAK = solid(5, 5)
SPRUCE_LOG = {"kind": "laidLog", "id": 17, "data": 1}

PLAIN = {"field": None, "border": None, "borderWidth": 1, "inlay": None,
         "inlayInset": 2, "isPlain": True}
NO_WINDOW = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
             "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}

WORKS_STOREY = {
    "clear": 5,
    "wall": {"stack": {"bands": [
        {"material": SCORIA, "thickness": 1},
        {"material": cells(5191, 3, 2, [SPRUCE, DARKOAK]), "thickness": 3},
        {"material": SPRUCE_LOG, "thickness": 1}], "ending": "repeat"},
        "extent": 5},
    "post": solid(17, 1),
    "windows": {"form": "arched", "block": 134, "hostBlock": -1, "hostData": 0,
                "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
    "surface": PLAIN, "deck": None, "headroom": 5,
}

WORKS = {
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
    "storeys": [WORKS_STOREY],
    "porch": None, "front": None,
    # a beam has to be the end of something, so the wall under it carries a
    # course of laid log — which is the last band of every storey above
    "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 134, "fill": "upperSlab",
                         "fillBlock": 126, "fillData": 1},
                "width": 2, "height": 3},
}

# The spawn hall and the wool rooms are the two structures a player sees from
# the inside, and a finish stating no roomStyles leaves both on the studio's
# bedrock box at 200 with no finding. Both are this board's works, hipped and
# built taller.
HALL = json.loads(json.dumps(WORKS))
HALL["roof"] = {"form": "hip", "pitch": 2, "slab": 126, "slabData": 1,
                "overhang": 1, "ridgeCap": False, "hole": False,
                "body": SPRUCE, "verge": DARKOAK, "gable": None,
                "gableWindows": NO_WINDOW}
HALL["storeys"][0] = json.loads(json.dumps(WORKS_STOREY))
HALL["storeys"][0]["clear"] = 7
HALL["storeys"][0]["headroom"] = 7
HALL["storeys"][0]["wall"]["extent"] = 7
HALL["storeys"][0]["wall"]["stack"]["bands"][1]["thickness"] = 5

styles["works"] = {"kind": "house", "shell": WORKS}

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-21",
    "themes": {"rim": rim_theme, "drift": drift_theme, "yard": yard_theme,
               "grove": grove_theme},
    "mapTheme": "rim",
    # Extreme hills (#8ab689): there is almost no grass on a cinder field, and
    # what the flora pass does put there stays muted against the ash rather
    # than reading as a meadow. Asked of GET /api/terrain/biomes.
    "biome": {"kind": "solid", "id": 3},
    "relief": relief,
    "addShapes": add_shapes,
    "addLayers": [rim_parapet],
    "roomStyles": {"spawn": HALL, "wool": HALL},
    "dressing": {"styles": styles, "props": props},
}

write(os.path.join(HERE, f"{SLUG}.plan.json"), plan)
write(os.path.join(HERE, f"{SLUG}.finish.json"), finish)
