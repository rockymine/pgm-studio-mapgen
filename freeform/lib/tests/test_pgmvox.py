"""Tests for pgmvox: what each module promises, checked on small worlds and plans.

    cd freeform/lib && python3 -m unittest discover -s tests -v
"""
import gzip
import json
import os
import sys
import tempfile
import unittest
import xml.dom.minidom

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from pgmvox import B, World, audit, blocks, move, orient, plangraph, plot, render, sight, terrain, walk  # noqa: E402
from pgmvox import build as BLD  # noqa: E402
from pgmvox import facade as F  # noqa: E402
from pgmvox import pieces as P  # noqa: E402
from pgmvox import objectives as O  # noqa: E402
from pgmvox import solid as SOL  # noqa: E402
from pgmvox import landform as LF, noise, route as RT  # noqa: E402
from pgmvox.mapxml import Doc, E, duration, point  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402
from pgmvox.sketch import TEAM, SectionPanel, Sheet  # noqa: E402

CURIO = os.path.join(HERE, "..", "..", "opus55-freeform-curio", "plots")


class Blocks(unittest.TestCase):
    def test_the_table_comes_from_the_studio(self):
        self.assertEqual(len(blocks.TABLE), 256)
        self.assertEqual(blocks.name(B.WOOL, 14), "Red Wool")

    def test_classes(self):
        for bid in (B.AIR, B.TALLGRASS, B.TORCH, B.LADDER, B.WATER, B.CARPET, B.SNOW_LAYER):
            self.assertIn(bid, blocks.PASSABLE)
        for bid in (B.STONE, B.FENCE, B.GLASS, B.LEAVES, B.OAK_DOOR):
            self.assertNotIn(bid, blocks.PASSABLE)
        self.assertIn(B.GLASS, blocks.SIGHT_CLEAR)
        self.assertIn(B.FENCE, blocks.SIGHT_CLEAR)
        self.assertNotIn(B.LEAVES, blocks.SIGHT_CLEAR)

    def test_every_id_has_a_colour(self):
        self.assertEqual(blocks.COLOURS.shape, (256, 16, 3))
        self.assertNotEqual(blocks.colour(B.GRASS), (255, 0, 255))


class Orient(unittest.TestCase):
    def test_helpers(self):
        self.assertEqual(orient.stair("e"), 0)
        self.assertEqual(orient.stair("n", upside_down=True), 7)
        self.assertEqual(orient.ladder("s"), 2)                  # on the wall to its south: faces north
        self.assertEqual(orient.torch("w"), 1)                   # on the wall to its west: points east
        self.assertEqual(orient.yaw("e"), -90)
        self.assertEqual(orient.rotation16("n"), 8)

    def test_every_block_turns_back(self):
        for op, inverse in (("cw", "ccw"), ("half", "half"), ("mirror_x", "mirror_x"), ("mirror_z", "mirror_z")):
            a, b = orient.data_table(op), orient.data_table(inverse)
            for bid in range(256):
                for d in range(16):
                    self.assertEqual(b[bid, a[bid, d]], d, f"{bid}:{d} under {op} then {inverse}")

    def test_four_quarter_turns_are_none(self):
        t = orient.data_table("cw")
        for bid in (B.OAK_STAIRS, B.LADDER, B.TORCH, B.LOG, B.RAIL, B.RAIL_POWERED, B.OAK_DOOR, B.TRAPDOOR,
                    B.SIGN_POST, B.PUMPKIN, B.HAY, B.QUARTZ, B.VINE):
            for d in range(16):
                self.assertEqual(t[bid, t[bid, t[bid, t[bid, d]]]], d, f"{bid}:{d}")

    def test_the_families_the_studio_leaves_alone(self):
        self.assertEqual(orient.turn_data(B.OAK_DOOR, 1, "half"), 3)       # facing south -> north
        self.assertEqual(orient.turn_data(B.OAK_DOOR, 9, "mirror_x"), 8)   # a mirror swaps the hinge
        self.assertEqual(orient.turn_data(B.OAK_DOOR, 9, "half"), 9)       # a turn keeps it
        self.assertEqual(orient.turn_data(B.RAIL, 6, "half"), 8)
        self.assertEqual(orient.turn_data(B.RAIL_POWERED, 2 | 8, "cw"), 5 | 8)
        self.assertEqual(orient.turn_data(B.IRON_TRAPDOOR, 0, "half"), 1)
        self.assertEqual(orient.turn_data(B.SIGN_POST, 0, "half"), 8)

    def test_turn_world_half(self):
        w = World(-4, -4, 8, 8, sy=4)
        w.set(-3, 1, -2, B.OAK_STAIRS, orient.stair("e"))
        w.set(-2, 1, -1, B.OAK_DOOR, orient.door("s"))
        orient.turn_world(w, "half", lambda x, z: x < 0)
        self.assertEqual(w.get(2, 1, 1), (B.OAK_STAIRS, orient.stair("w")))
        self.assertEqual(w.get(1, 1, 0), (B.OAK_DOOR, orient.door("n")))


class Move(unittest.TestCase):
    def test_knockback_matches_the_boards(self):
        self.assertAlmostEqual(move.knockback(1), 7.2, places=1)
        self.assertAlmostEqual(move.knockback(10), 42.9, places=1)
        self.assertAlmostEqual(move.knockback(1, slip=move.SLIP["ice"]), 9.4, places=1)

    def test_falls(self):
        t, out = move.fall(22, "run off")
        self.assertAlmostEqual(out, 7.3, places=1)
        self.assertEqual(move.fall_damage(3), 0)
        self.assertEqual(move.fall_damage(22), 19)

    def test_jump_reach(self):
        self.assertTrue(walk.gap_cleared(3))
        self.assertFalse(walk.gap_cleared(4))

    def test_solve_launch(self):
        best = move.solve_launch((0, 10, 0), (20, 0), move.land_at(10))
        self.assertIsNotNone(best)
        self.assertLess(abs(best[2]["x"] - 20), 1.0)


class Walk(unittest.TestCase):
    def setUp(self):
        self.w = World(-5, -5, 11, 11, sy=20)
        self.w.fill(-5, 0, -5, 5, 3, 5, B.STONE)

    def test_ladder_climb(self):
        w = self.w
        w.fill(0, 4, 0, 2, 8, 2, B.STONE)
        for y in range(4, 9):
            w.set(-1, y, 1, B.LADDER, orient.ladder("e"))
        d = walk.walk(w.ids, [(-5, 4, -5)], w.x0, w.z0)
        self.assertIsNotNone(walk.nearest(d, w.x0, w.z0, 1, 9, 1, 0))

    def test_no_step_up_under_a_ceiling(self):
        """Generation 1's headroom test could never fire; here a step up with a block over the player is refused."""
        w = self.w
        w.set(1, 4, 0, B.STONE)                                  # a one-block step
        w.fill(-5, 6, -5, 5, 6, 5, B.STONE)                      # a ceiling over everyone's head as they jump
        w.set(1, 6, 0, B.AIR)                                    # but room to stand on the step itself
        d = walk.walk(w.ids, [(0, 4, 0)], w.x0, w.z0, walk.MoveRules(jumps=False))
        self.assertEqual(d[1 - w.x0, 5, 0 - w.z0], -1)

    def test_no_stand_above(self):
        w = self.w
        w.set(3, 10, 3, B.STONE)
        bad = walk.no_stand_above(w, 6, np.ones((w.sx, w.sz), bool))
        self.assertEqual(bad, [(3, 3)])


class Audit(unittest.TestCase):
    def test_footing(self):
        w = World(-3, -3, 6, 6, sy=8)
        w.fill(-3, 0, -3, 2, 0, 2, B.STONE)
        w.set(0, 3, 0, B.SAND)
        w.set(1, 1, 1, B.TORCH, orient.torch("w"))
        w.set(-2, 1, -2, B.TORCH, orient.torch())
        why = sorted(r[3].split(":")[0] for r in audit.footing(w))
        self.assertEqual(len(why), 2)


class Plan(unittest.TestCase):
    def raster(self):
        R = Raster((-20, 19), (-10, 9), ["wall", "floor", "stair", "gap"], base_h=6, base_kind="gap",
                   symmetry=Symmetry("half"))
        R.rect(-18, -10, -5, 4, 10)
        R.rect(-6, -1, -5, 4, 12)
        R.flight((-9, 0), "e", width=(-1, 1), h0=11, n=1)
        return R

    def test_symmetry_is_drawn_in_the_plan(self):
        R = self.raster()
        self.assertEqual(R.h(17, -5), 10)
        self.assertEqual(R.stair[(8, -1)], "w")

    def test_arrivals_are_fair(self):
        R = self.raster()
        G = plangraph.graph(R, {"floor", "stair"}, {"wall"})
        a = plangraph.arrivals(G, {"red": [(-15, 0)], "blue": [(14, -1)]},
                               {"middle": [(x, z) for x in range(-6, 6) for z in range(-5, 5)]})
        self.assertEqual(a["middle"]["red"], a["middle"]["blue"])

    def test_sight(self):
        R = self.raster()
        op = sight.plan_opaque(R)
        self.assertFalse(sight.line_clear(sight.eye(-15, 11, 0), sight.target(15, 11, 0), op))
        self.assertTrue(sight.line_clear(sight.eye(-2, 13, 0), sight.target(15, 11, 0), op))


class Landforms(unittest.TestCase):
    def setUp(self):
        self.X, self.Z = np.meshgrid(np.arange(-60, 60), np.arange(-60, 60), indexing="ij")
        self.H = 40 + 12 * noise.fbm(self.X.shape, 30, 3, seed=3) - 0.05 * self.Z

    def test_a_river_never_climbs_and_only_cuts(self):
        X, Z, H = self.X, self.Z, self.H
        path = [(-50, -55), (0, 0), (40, 55)]
        H2, river = LF.watercourse(H, X, Z, path, width=5, depth=2, lowest=20)
        self.assertTrue((H2 <= H + 1e-9).all())
        s, bed, _ = LF._sample(H2, X, Z, path)
        self.assertTrue((np.diff(bed) <= 1e-9).all())
        self.assertGreaterEqual(bed.min(), 20)
        self.assertTrue(river.mask.any())

    def test_a_spire_leaves_the_rest_alone(self):
        X, Z, H = self.X, self.Z, self.H
        H2 = LF.spire(H, X, Z, (0, 0), r=6, top=90, jag=0)
        far = np.hypot(X, Z) >= 6
        self.assertTrue((H2[far] == H[far]).all())                         # it once lifted the whole world
        self.assertEqual(H2.max(), 90)
        jagged = LF.spire(H, X, Z, (0, 0), r=6, top=90, jag=0.15)
        self.assertTrue((jagged[np.hypot(X, Z) >= 12] == H[np.hypot(X, Z) >= 12]).all())

    def test_butte_canyon_grade_coast_terraces(self):
        X, Z, H = self.X, self.Z, self.H
        self.assertEqual(set(LF.butte(H, X, Z, (10, 10), 6, 80)[np.hypot(X - 10, Z - 10) < 4]), {80})
        self.assertTrue((LF.canyon(H, X, Z, [(-50, 0), (50, 0)], width=16, depth=8) <= H + 1e-9).all())
        _, (s, p) = LF.grade(H, X, Z, [(-50, -40), (50, 40)], width=4, max_grade=0.2)
        self.assertLessEqual(np.max(np.abs(np.diff(p)) / np.diff(s)), 0.2 + 1e-9)
        outline = [(-40, -40), (40, -40), (40, 40), (-40, 40)]
        H2, sea = LF.coast(H, X, Z, 45, outline=outline)
        self.assertFalse((sea.mask & (np.abs(X) < 38) & (np.abs(Z) < 38)).any())
        T = LF.terraces(H, np.ones(H.shape, bool), step=4, base=0)
        self.assertTrue((T % 4 == 0).all())


class Routes(unittest.TestCase):
    def slope(self):
        X, Z = np.meshgrid(np.arange(0, 60), np.arange(0, 60), indexing="ij")
        return X, Z, (0.5 * Z).astype(float)                                # 1 in 2, straight up the z axis

    def test_switchbacks_come_out_of_the_cost(self):
        X, Z, H = self.slope()
        pts = RT.find(H, X, Z, (30, 2), (30, 56), max_grade=1 / 8)
        legs = RT.simplify(pts)
        self.assertGreaterEqual(len(legs) - 1, 3)                           # it turns about at least twice
        self.assertLessEqual(len(legs) - 1, 9)                              # in long legs, not a zig-zag
        _, (s, p) = LF.grade(H, X, Z, RT.smooth(legs), width=3, max_grade=1 / 8)
        self.assertLessEqual(np.max(np.abs(np.diff(p)) / np.diff(s)), 1 / 8 + 1e-9)

    def test_avoid_and_water(self):
        X, Z = np.meshgrid(np.arange(0, 40), np.arange(0, 40), indexing="ij")
        H = np.zeros(X.shape)
        wall = (X == 20) & (Z < 35)
        pts = RT.find(H, X, Z, (5, 5), (35, 5), avoid=wall)
        self.assertTrue(all(not wall[int(round(x)), int(round(z))] for x, z in pts))
        self.assertGreater(max(z for _, z in pts), 30)                      # round the end of the wall
        river = (X >= 18) & (X <= 22)
        self.assertIsNone(RT.find(H, X, Z, (5, 5), (35, 5), water=river, bridge=None))
        self.assertIsNotNone(RT.find(H, X, Z, (5, 5), (35, 5), water=river, bridge=6))

    def test_a_network_shares_its_trunk(self):
        X, Z = np.meshgrid(np.arange(0, 60), np.arange(0, 60), indexing="ij")
        H = np.zeros(X.shape)
        branches, roads = RT.network(H, X, Z, {"a": (5, 30), "b": (55, 25), "c": (55, 35)})
        separate = sum(len(RT.find(H, X, Z, (5, 30), p)) for p in ((55, 25), (55, 35)))
        self.assertLess(sum(len(b) for b in branches.values()), separate)

    def test_grade_keeps_water_and_earlier_roads(self):
        X, Z, H = self.slope()
        river = (Z >= 28) & (Z <= 30)
        earlier = (X >= 28) & (X <= 32) & (Z >= 40)
        H2, _ = LF.grade(H, X, Z, [(30, 2), (30, 56)], width=4, max_grade=0.1, water=river, keep=earlier)
        self.assertTrue((H2[river] == H[river]).all() and (H2[earlier] == H[earlier]).all())
        _, (s, p) = LF.grade(H, X, Z, [(30, 2), (30, 56)], width=4, max_grade=0.6)
        self.assertEqual((round(p[0]), round(p[-1])), (1, 28))                 # the ends hold their ground


class Sketch(unittest.TestCase):
    def test_a_sheet_with_every_panel(self):
        R = Plan.raster(None)
        J = plangraph.jumps(R, {"floor", "stair"})
        S = Sheet("t")
        m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="BOARD", legend="a legend")
        m.raster(R, {"floor": (150, 175, 110), "stair": (170, 160, 130), "wall": (90, 90, 90)})
        m.heights(R)
        m.jumps(J, R=R)
        m.marker(-15, 0, "S", TEAM["red"], both=True)
        m.route([(-15, 0), (-6, 0), (0, 0)], TEAM["red"], both=True)
        m.callout(0, 0, "the middle")
        m.zone([(-6, -5), (0, -5), (0, 0), (-6, 0)], both=True)
        a = SectionPanel(R.x_min, R.x_max, 0, 20, scale=3, title="ACROSS")
        a.raster(R, "x", 0)
        a.level(6, "kill")
        b = SectionPanel(0, 20, 0, 20, scale=3, title="ALONG")
        b.along(R, [(-15.5, 0.5), (4.5, 0.5)])
        S.row(a, b)
        S.table([("1", "a number", "at most 2", True), ("3", "another", "at most 2", False), "a note"])
        with tempfile.TemporaryDirectory() as d:
            p = S.save(os.path.join(d, "s.png"))
            self.assertTrue(os.path.getsize(p) > 0)


class Roofs(unittest.TestCase):
    def test_the_roof_is_the_studios(self):
        """Every cell of 300 roofs answered by the studio's own RoofField (data/export_roofs.cs)."""
        with gzip.open(os.path.join(os.path.dirname(HERE), "pgmvox", "data", "roofs.json.gz"), "rt") as f:
            cases = json.load(f)
        for c in cases:
            r = BLD.RoofField(c["form"], tuple(c["box"]), c["overhang"], 70, c["pitch"], c["front"], c["halves"])
            self.assertEqual((r.peak, r.trough), (c["peak"], c["trough"]))
            for x, z, crown, riser, half, up, ridge, verge in c["cells"]:
                self.assertEqual((r.crown(x, z), r.riser(x, z), r.half(x, z), r.upslope(x, z) or "",
                                  r.on_ridge(x, z), r.past_verge(x, z)), (crown, riser, half, up, ridge, verge),
                                 f"{c['form']} {c['box']} at {x},{z}")

    def test_a_framed_roof_square_to_the_board_is_the_studios(self):
        for form in BLD.FORMS:
            for L, W, cx, cz in ((10, 6, 3, 2), (9, 5, 0.5, -1.5), (6, 12, 0, 0)):
                a = BLD.RoofField.framed(form, BLD.Frame(cx, cz, 0), L, W, 1, 70)
                x0, z0 = round(cx - L / 2), round(cz - W / 2)
                b = BLD.RoofField(form, (x0, z0, x0 + L - 1, z0 + W - 1), 1, 70)
                self.assertEqual(sorted(a.cells()), sorted(b.cells()))
                for x, z in b.cells():
                    self.assertEqual((a.crown(x, z), a.upslope(x, z)), (b.crown(x, z), b.upslope(x, z)))

    def test_frame_covers_its_length(self):
        self.assertEqual(len(BLD.Frame(0, 0, 0).cells(8, 6)), 48)
        self.assertEqual(len(BLD.Frame(0, 0.5, 90).cells(7, 6)), 42)          # u runs along z here


class Houses(unittest.TestCase):
    def test_a_house_at_45_degrees_is_closed(self):
        """Walls from eight neighbours: nothing outside reaches inside but through the door."""
        w = World(-16, -16, 32, 32, sy=30)
        w.fill(-16, 0, -16, 15, 4, 15, B.STONE)
        r = BLD.house(w, BLD.House(0, 0, 45, L=10, W=7, floor=4, storeys=1, door=1))
        dx, dz, _ = r["door"]
        w.set(dx, 5, dz, B.STONE)                                # shut the door for the test
        w.set(dx, 6, dz, B.STONE)
        seen, todo = {(-16, -16)}, [(-16, -16)]
        while todo:
            x, z = todo.pop()
            for ex, ez in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + ex, z + ez)
                if -16 <= n[0] < 16 and -16 <= n[1] < 16 and n not in seen and w.id(n[0], 6, n[1]) == B.AIR:
                    seen.add(n)
                    todo.append(n)
        self.assertNotIn((0, 0), seen)
        self.assertEqual(w.id(0, 6, 0), B.AIR)

    def test_square_house_has_its_door_and_roof(self):
        w = World(-12, -12, 24, 24, sy=30)
        r = BLD.house(w, BLD.House(0, 0, 0, L=9, W=6, floor=2, storeys=2))
        x, z, facing = r["door"]
        self.assertEqual(facing, (0, 1))
        self.assertIn(w.id(x, 3, z), blocks.DOORS)
        self.assertEqual(r["roof"].peak, r["eave"] + 1 + 2)     # a pitch-1 gable over six: two courses up

    def test_claims(self):
        c = BLD.Claims()
        c.claim("a", {(0, 0), (1, 0)})
        c.claim("b", {(1, 0)})
        c.claim("c", {(1, 0)}, layer="sky")
        self.assertEqual(c.overlaps(), [("ground", "a", "b", 1)])


class Facades(unittest.TestCase):
    def test_a_word_reads_left_to_right_from_outside(self):
        w = World(-2, -2, 30, 10, sy=12)
        F.extrude(w, F.rect_cells(0, 0, 20, 5), 0, 8, faces_=[F.word(2, "LT", F.DARK)])
        south = ["".join("#" if w.id(x, y, 5) == B.AIR else "." for x in range(0, 21)) for y in range(6, 1, -1)]
        north = ["".join("#" if w.id(x, y, 0) == B.AIR else "." for x in range(20, -1, -1)) for y in range(6, 1, -1)]
        self.assertEqual(south[0].strip("."), "#...###")
        self.assertEqual(south, north)                           # the same word, read from its own side
        self.assertEqual(w.get(7, 6, 4), F.DARK)                 # set back, in the inset block

    def test_corners_stay_flush(self):
        w = World(-2, -2, 12, 12, sy=8)
        F.extrude(w, F.rect_cells(0, 0, 5, 5), 0, 5, faces_=[F.band(0, 5, F.DARK)])
        self.assertEqual(w.get(0, 2, 0), F.CONCRETE)
        self.assertEqual(w.id(2, 2, 0), B.AIR)

    def test_carpet(self):
        w = World(0, 0, 12, 12, sy=2)
        n = F.carpet(w, 0, 0, 10, 10, 0, F.first_of(F.border(1, (B.WOOL, 15)), F.star(2, (B.WOOL, 4)),
                                                    default=(B.WOOL, 11)))
        self.assertEqual(w.get(0, 0, 5), (B.WOOL, 15))
        self.assertEqual(w.get(5, 0, 5), (B.WOOL, 4))
        self.assertEqual(sum(n.values()), 121)


class Courses(unittest.TestCase):
    def course(self, pool=True):
        C = P.Course(Symmetry("mirror_x"))
        C.add("start", P.box(-4, 3, 0, 4), 60)
        C.add("ledge", P.box(-9, -6, 8, 12), 52)
        C.add("pool", P.box(-6, 5, 16, 24), 30, **({"water": P.box(-6, 5, 16, 24)} if pool else {}))
        return C

    def test_images_and_the_middle(self):
        C = self.course()
        self.assertEqual([p.side for p in C.pieces], ["middle", "main", "image", "middle"])
        self.assertEqual(min(x for x, _ in C.pieces[2].cells), 5)            # -9..-6 mirrored about -0.5
        self.assertEqual(len(C.links()), 4)

    def test_the_audit(self):
        rows = self.course().audit()
        self.assertTrue(all(r["how"] for r in rows))
        self.assertEqual(rows[0]["damage"], move.fall_damage(8))
        self.assertEqual(rows[1]["lands"], (-1 - rows[0]["lands"][0], rows[0]["lands"][1]))   # mirrored exactly
        self.assertTrue(rows[2]["water"] and rows[2]["damage"] == 0)
        dry = self.course(pool=False).audit()
        self.assertEqual(dry[2]["damage"], move.fall_damage(22))

    def test_a_gap_is_judged_as_the_walk_judges_it(self):
        for g in range(0, 6):
            how, _ = P.clears(g, 0)
            self.assertEqual(how is not None, walk.gap_cleared(g), g)
        self.assertEqual(move.jump_reach(1.3), 0.0)                         # higher than any jump

    def test_a_course_is_a_raster(self):
        R = self.course().raster()
        self.assertEqual(R.at(-7, 10), (52, "floor"))
        self.assertEqual(R.at(6, 10), (52, "floor"))
        self.assertEqual(R.at(0, 6)[1], "void")


class Storeys(unittest.TestCase):
    def raster(self, roof=14):
        R = Raster((0, 19), (0, 9), ["floor", "stair", "roof"], base_h=10, base_kind="floor")
        R.storey(1).rect(10, 15, 2, 7, roof, "roof", both=False)
        R.flight((6, 4), "e", h0=11, n=3, both=False)
        R.rect(9, 9, 4, 4, 13, "stair", both=False)
        return R

    def test_a_roof_is_walked_and_so_is_the_ground_under_it(self):
        E = plangraph.graph(self.raster(), {"floor", "stair", "roof"})
        D, _ = plangraph.dijkstra(E, [(0, 4)])
        self.assertIn((12, 4, 1), D)
        self.assertIn((12, 4), D)
        self.assertIn((16, 4), [v for v, _, _ in E[(15, 4, 1)]])          # off the far edge to the ground

    def test_a_low_storey_closes_the_ground_under_it(self):
        E = plangraph.graph(self.raster(roof=12), {"floor", "stair", "roof"})
        self.assertNotIn((12, 4), E)

    def test_one_storey_is_unchanged(self):
        R = Plan.raster(None)
        self.assertEqual(R.storeys, [R])
        self.assertTrue(R.has().all())


class Solids(unittest.TestCase):
    def test_the_image_is_the_plans_turn(self):
        v = SOL.revolve([(3, 0), (4, 3), (2, 6)], -5.5, -3.5, 10)
        for op in ("half", "mirror_x", "mirror_z"):
            sym = Symmetry(op)
            want = {(*sym.point(x, z), y) for x, y, z in v.cells()}
            got = {(x, z, y) for x, y, z in SOL.image(v, sym).cells()}
            self.assertEqual(got, want, op)

    def test_fill(self):
        w = World(-8, -8, 16, 16, sy=12)
        n = SOL.fill(w, SOL.box(0, 1, 2, 3, 0, 1), (B.QUARTZ, 0))
        self.assertEqual(n, 8)
        self.assertEqual(w.get(1, 3, 1), (B.QUARTZ, 0))


class Objectives(unittest.TestCase):
    def objectives(self):
        o = O.Objectives(O.Teams(("red-team", "Red", "red"), ("blue-team", "Blue", "blue")), Symmetry("half"))
        o.add(O.Spawn("red-team", (-20, 11, 0), yaw=-90, area=O.Box(-21, 11, -1, -19, 13, 1)))
        o.add(O.Hill("mid", "the Middle", O.Box(-2, 10, -2, 1, 10, 1)), mirror=False)
        o.add(O.Wool("blue-team", "lime", slot=(-15, 12, 6)), color="pink")
        o.add(O.Destroyable("red-dtm", "Red's", "red-team", O.Box(-16, 11, -8, -15, 12, -7)))
        o.add(O.Core("red-core", "Red's Core", "red-team", O.Box(-12, 11, 4, -10, 13, 6)))
        return o

    def world(self, o):
        w = World(-24, -12, 48, 24, sy=24)
        w.fill(-24, 0, -12, 23, 10, 11, B.STONE)
        o.stamp(w)
        return w

    def test_the_other_half(self):
        o = self.objectives()
        spawns = o.of(O.Spawn)
        self.assertEqual([s.team for s in spawns], ["red-team", "blue-team"])
        self.assertEqual(spawns[1].at, (19, 11, -1))
        self.assertEqual(spawns[1].yaw, 90)
        self.assertEqual(o.of(O.Destroyable)[1].id, "blue-dtm")
        self.assertEqual(o.of(O.Wool)[1].color, "pink")
        self.assertEqual(len(o.of(O.Hill)), 1)

    def test_the_xml(self):
        o = self.objectives()
        d = o.write(Doc("T", "1.0.0", "t"), limit=100)
        x = xml.dom.minidom.parseString(d.tostring())
        cub = [c for c in x.getElementsByTagName("cuboid") if c.getAttribute("id") == "mid-capture"][0]
        self.assertEqual((cub.getAttribute("min"), cub.getAttribute("max")), ("-2,10,-2", "2,15,2"))   # max exclusive
        hill = x.getElementsByTagName("hill")[0]
        self.assertEqual(hill.getAttribute("capture-region"), "mid-capture")
        self.assertEqual(len(x.getElementsByTagName("wool")), 2)
        self.assertEqual(x.getElementsByTagName("point")[0].firstChild.data, "-19.5,11,0.5")
        with self.assertRaises(ValueError):
            d.region("mid-capture", O.Box(0, 0, 0, 1, 1, 1).cuboid())

    def test_stamped_and_read_back(self):
        o = self.objectives()
        w = self.world(o)
        self.assertEqual(o.check(w), [])
        w.set(-15, 12, 6, B.STONE)                                # the wool slot filled in
        w.set(-20, 12, 0, B.STONE)                                # a block in the spawn's head
        self.assertEqual(len(o.check(w)), 2)


class Terrain(unittest.TestCase):
    def test_slope_is_the_studios(self):
        """Every cell of sixteen grounds at windows 1 to 3, answered by the studio's SurfaceGradient."""
        with gzip.open(os.path.join(os.path.dirname(HERE), "pgmvox", "data", "slopes.json.gz"), "rt") as f:
            cases = json.load(f)
        for c in cases:
            m = np.array([[v is not None for v in r] for r in c["grid"]])
            H = np.array([[v if v is not None else 0 for v in r] for r in c["grid"]])
            for window, want in c["degrees"].items():
                got = terrain.slope_deg(H, m, int(window))
                self.assertTrue(((got == np.array(want)) | ~m).all(), f"window {window}")

    def test_a_gentle_grade_reads_as_a_grade(self):
        X = np.arange(30)[:, None] + np.zeros((1, 10), int)
        self.assertEqual(set(terrain.slope_deg(X // 4)[6:24, 5]), {14})        # not 0 and 27 by turns
        self.assertEqual(set(terrain.slope_deg(X // 4, window=1)[6:24, 5]), {0, 27})

    def test_strata(self):
        S = terrain.Strata([((B.STONE, 0), 0.5, 4), ((B.WOOL, 14), 0.2, 1), ((B.STONE, 5), 0.3, 3)], seed=3, start=10)
        beds = S.thicknesses()
        self.assertTrue(all(n == 1 for b, n in beds if b == (B.WOOL, 14)))
        self.assertTrue(all(a[0] != b[0] for a, b in zip(beds, beds[1:])))
        self.assertEqual(S(5), (B.STONE, 0))

    def test_root_depth(self):
        m = np.zeros((20, 20), bool)
        m[4:16, 4:16] = True
        d = terrain.root_depth(m, flutes=3, spires=8)
        self.assertTrue((d[~m] == 0).all() and (d[m] >= 1).all())
        self.assertGreater(d[10, 10], d[4, 10])                             # deeper inland

    def test_slope_does_not_wrap(self):
        H = np.zeros((10, 10))
        H[0, :] = 0
        H[-1, :] = 30                                            # a cliff on the east edge only
        self.assertEqual(terrain.slope_deg(H)[0, 5], 0.0)

    def test_mountain_ring_keeps_the_middle_clear(self):
        X, Z = np.meshgrid(np.arange(-100, 100), np.arange(-100, 100), indexing="ij")
        h = terrain.mountain_ring(X, Z, clear=60)
        self.assertLess(h[np.hypot(X, Z) < 50].max(), 4)


class WorldAndOutput(unittest.TestCase):
    def test_save_and_load(self):
        w = World(-2, -2, 4, 4, sy=6)
        w.set(0, 1, 0, B.WOOL, 14)
        w.chest(1, 1, 1, [(0, "minecraft:apple", 1, 0)])
        with tempfile.TemporaryDirectory() as d:
            w.save(d, "t", (0, 2, 0))
            w2 = World.load(d)
        self.assertEqual(w2.get(0, 1, 0), (B.WOOL, 14))
        self.assertEqual(len(w2.tiles), 1)

    def test_render(self):
        w = World(-4, -4, 8, 8, sy=8)
        w.fill(-4, 0, -4, 3, 2, 3, B.STONE)
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "a.png")
            render.iso(w.ids, w.dat, w.x0, w.z0, p, 2)
            self.assertTrue(os.path.getsize(p) > 0)

    def test_mapxml(self):
        d = Doc("T", "1.0.0", "Win", "blitz")
        d.spawns(E("spawn", E("regions", point(0.5, 65, 0.5, yaw=90))), default=point(0, 90, 0))
        d.kill_below(40)
        d.time(90)
        xml.dom.minidom.parseString(d.tostring())
        self.assertEqual(duration(90), "1m30s")


class Plots(unittest.TestCase):
    @unittest.skipUnless(os.path.isdir(CURIO), "Curio Square's plots are not here")
    def test_a_curio_plot_passes(self):
        m = plot.load(os.path.join(CURIO, "opus", "bandstand.py"))
        r = plot.check_alone(m)
        self.assertEqual(plot.verdict(r), [])
        self.assertEqual(r["top"], 11)

    def test_the_canvas_refuses(self):
        class Bad:
            NAME, KIND = "bad", "sculpture"

            @staticmethod
            def build(c):
                c.set(2, 0, 2, B.OAK_DOOR)
                c.set(11, 0, 0, B.STONE)
        r = plot.check_alone(Bad)
        self.assertTrue(any("forbidden" in e for e in r["errors"]))
        self.assertTrue(any("outside" in e for e in r["errors"]))


if __name__ == "__main__":
    unittest.main()
