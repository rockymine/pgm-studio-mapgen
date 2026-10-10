"""Tests for pgmvox: what each module promises, checked on small worlds and plans.

    cd freeform/lib && python3 -m unittest discover -s tests -v
"""
import gzip
import math
import json
import os
import sys
import tempfile
import unittest
import xml.dom.minidom

import numpy as np
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from pgmvox import B, World, audit, blocks, move, orient, plangraph, plot, render, shapes, sight, terrain, walk  # noqa: E402
from pgmvox import build as BLD  # noqa: E402
from pgmvox import facade as F  # noqa: E402
from pgmvox import pieces as P  # noqa: E402
from pgmvox import objectives as O  # noqa: E402
from pgmvox import solid as SOL  # noqa: E402
from pgmvox import forms, landform as LF, noise, route as RT  # noqa: E402
from pgmvox import props, trees as TR, under as U  # noqa: E402
from pgmvox.mapxml import Doc, E, duration, point  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402
from pgmvox.sketch import TEAM, SectionPanel, Sheet  # noqa: E402

FIXTURES = os.path.join(HERE, "fixtures")


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

    def test_jump_lands_lower(self):
        """A running jump across a gap of two lands on a pillar one lower, as well as level or one up."""
        w = World(-5, -5, 11, 11, sy=20)
        w.fill(-5, 1, -1, -2, 10, 1, B.STONE)                     # the take-off, its top at 10
        w.fill(1, 1, -1, 4, 9, 1, B.STONE)                        # the landing, its top at 9, two blocks away
        d = walk.walk(w.ids, [(-3, 11, 0)], w.x0, w.z0, walk.MoveRules(max_drop=4))
        self.assertIsNotNone(walk.nearest(d, w.x0, w.z0, 3, 10, 0, 0))

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
    def test_a_fields_image_is_every_column_at_its_image_point(self):
        xs = np.arange(-4, 4)
        X, Z = np.meshgrid(xs, xs, indexing="ij")
        a = np.random.default_rng(3).random(X.shape)
        for op in ("half", "mirror_x", "mirror_z", "cw"):
            S = Symmetry(op)
            image = S.image(a)
            for i, k in [(0, 0), (1, 5), (7, 2), (3, 3)]:
                x, z = S.point(int(X[i, k]), int(Z[i, k]))
                self.assertEqual(image[x + 4, z + 4], a[i, k], op)
            sym = S.field(a)
            self.assertTrue(np.allclose(sym, S.image(sym)), op)

    def test_a_field_completed_from_a_half_is_symmetric(self):
        half = np.random.default_rng(4).random((4, 8))
        for op in ("half", "mirror_x"):
            S = Symmetry(op)
            whole = S.whole(half)
            self.assertTrue(np.array_equal(whole, S.image(whole)), op)
            self.assertTrue(np.array_equal(whole[:4], half), op)
            keep = np.zeros((8, 8), bool)
            keep[:4] = True
            self.assertTrue(np.array_equal(S.field(np.vstack([half, np.zeros((4, 8))]), keep=keep), whole), op)

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


class Field(unittest.TestCase):
    def setUp(self):
        self.X, self.Z = np.meshgrid(np.arange(-50, 50, dtype=float), np.arange(-40, 40, dtype=float), indexing="ij")

    def test_landmarks_are_exact(self):
        from pgmvox import field as F
        X, Z = self.X, self.Z
        ramp = F.terms(X, Z, 10, F.Ramp("x", -20, 20, 6))
        self.assertTrue((ramp[X <= -20] == 10).all() and (ramp[X >= 20] == 16).all())
        falling = F.terms(X, Z, 0, F.Ramp("z", 30, -30, 4))
        self.assertTrue((falling[Z <= -30] == 4).all() and (falling[Z >= 30] == 0).all())
        mound = F.terms(X, Z, 0, F.Gauss((10, -5), 8, 5, rz=4))
        self.assertEqual(mound[60, 35], 5.0)
        self.assertEqual(np.unravel_index(mound.argmax(), mound.shape), (60, 35))
        turned = F.Gauss((0, 0), 12, 1, rz=3, angle=90).value(X, Z)
        self.assertGreater(turned[50, 40 + 9], turned[50 + 9, 40])        # turned a right angle: long along z

    def test_terms_add_and_mix_weighs(self):
        from pgmvox import field as F
        X, Z = self.X, self.Z
        a, b = F.Ramp("x", -10, 10, 3), F.Tilt(0.1, -0.2)
        self.assertTrue(np.allclose(F.terms(X, Z, 2, a, b), F.terms(X, Z, 2, a) + F.terms(X, Z, 0, b)))
        w = np.clip((X + 50) / 99, 0, 1)
        m = F.mix(np.full(X.shape, 1.0), np.full(X.shape, 5.0), w)
        self.assertEqual((m[0, 0], m[-1, 0]), (1.0, 5.0))


class Shapes(unittest.TestCase):
    def test_a_rectangle_is_taken_by_its_corners_in_either_order(self):
        cells = shapes.rect_cells(3, 9, 1, 7)
        self.assertEqual(cells, shapes.rect_cells(1, 7, 3, 9))
        self.assertEqual(len(cells), 3 * 3)
        self.assertEqual(min(cells), (1, 7))
        self.assertEqual(max(cells), (3, 9))

    def test_a_polygons_cells_are_the_centres_inside_it(self):
        self.assertEqual(shapes.poly_cells([(0, 0), (4, 0), (4, 3), (0, 3)]),
                         {(x, z) for x in range(4) for z in range(3)})

    def test_a_polyline_says_which_side_of_it_a_point_lies(self):
        X, Z = np.meshgrid(np.arange(-3, 4), np.arange(-3, 4), indexing="ij")
        d, along, side = shapes.polyline(X, Z, [(-3, 0), (3, 0)], side=True)
        self.assertTrue((side[Z > 0] == 1).all())                 # walking east, south is the right hand
        self.assertTrue((side[Z < 0] == -1).all())
        self.assertTrue(np.array_equal((d, along), shapes.polyline(X, Z, [(-3, 0), (3, 0)])))

    def test_the_nearest_point_on_a_polyline_is_measured_along_it(self):
        bend = [(0, 0), (10, 0), (10, 10)]
        self.assertEqual(shapes.nearest_on(bend, 4, -2), (2.0, 4.0))
        self.assertEqual(shapes.nearest_on(bend, 13, 6), (3.0, 16.0))
        self.assertEqual(shapes.nearest_on(bend, -5, 0), (5.0, 0.0))

    def test_an_island_keeps_to_its_box_its_insets_and_its_cuts(self):
        from pgmvox.noise import ragged
        X, Z = np.meshgrid(np.arange(-40, 0), np.arange(-30, 30), indexing="ij")
        west = 2 + ragged(X.shape, "z", 12, 5, seed=1)
        corner = [(-40, 20), (-25, 20), (-25, 29), (-40, 29)]
        land = shapes.island(X, Z, (-40, -30, -1, 29), west=west, east=4, north=3, cuts=[(corner, 1.0)])
        self.assertTrue((X[land] <= -5).all() and (Z[land] >= -27).all())
        self.assertTrue((west >= 2).all() and (west <= 7).all())
        self.assertTrue(all(X[:, k][land[:, k]].min() == -40 + west[0, k] for k in range(3, 48)))   # rows clear of the cut corner
        self.assertFalse(land[(X < -26) & (Z > 21)].any())
        self.assertEqual(ndimage.label(land)[1], 1)

    def test_depth_inside_a_mask_by_each_metric(self):
        m = np.zeros((7, 7), bool)
        m[1:6, 1:6] = True
        self.assertEqual(shapes.distance_in(m)[3, 3], 3)
        self.assertEqual(shapes.distance_in(m, "chessboard")[3, 3], 3)
        self.assertAlmostEqual(float(shapes.distance_in(m, "euclid")[3, 3]), 3.0)
        self.assertEqual(shapes.distance_in(m)[0, 0], 0)
        e = shapes.edge_depth(m)
        self.assertEqual((e[1, 1], e[3, 3], e[0, 0]), (0, 2, -1))

    def test_a_line_wanders_along_one_axis_only(self):
        from pgmvox.noise import fbm, line
        f = line((30, 50), "z", 12, seed=7, amp=4, base=-10)
        self.assertEqual(f.shape, (1, 50))
        self.assertTrue(np.array_equal(f[0], -10 + 4 * fbm((50,), 12, 2, seed=7)))
        self.assertEqual(line((30, 50), "x", 12, seed=7).shape, (30, 1))
        clipped = line((30, 50), "z", 12, seed=7, amp=40, clip=(-1, 2))
        self.assertTrue(clipped.min() >= -1 and clipped.max() <= 2)
        self.assertTrue(np.array_equal(f, line((30, 50), "z", 12, seed=7, amp=4, base=-10)))

    def test_smoothstep_rises_falls_and_steps(self):
        from pgmvox.noise import smoothstep
        self.assertEqual((float(smoothstep(0, 10, -1)), float(smoothstep(0, 10, 5)), float(smoothstep(0, 10, 11))),
                         (0.0, 0.5, 1.0))
        self.assertEqual((float(smoothstep(-14, -64, -70)), float(smoothstep(-14, -64, 0))), (1.0, 0.0))
        self.assertEqual(smoothstep(3, 3, np.array([2, 3, 4])).tolist(), [0.0, 1.0, 1.0])

    def test_no_public_function_takes_a_rectangle_by_ranges_but_the_two_named(self):
        import inspect
        import pkgutil
        import pgmvox
        ranges = []
        for info in pkgutil.iter_modules(pgmvox.__path__):
            module = __import__(f"pgmvox.{info.name}", fromlist=["_"])
            found = [(f"{info.name}.{n}", f) for n, f in vars(module).items()
                     if inspect.isfunction(f) and f.__module__ == module.__name__ and not n.startswith("_")]
            for n, cls in vars(module).items():
                if inspect.isclass(cls) and cls.__module__ == module.__name__:
                    found += [(f"{info.name}.{n}.{m}", f) for m, f in vars(cls).items()
                              if inspect.isfunction(f) and not m.startswith("_")]
            for name, f in found:
                params = [p for p in inspect.signature(f).parameters if p != "self"]
                if params[:4] == ["x0", "x1", "z0", "z1"]:
                    ranges.append(name)
        self.assertEqual(sorted(ranges), ["pieces.box", "plan.Raster.rect"])


class Landforms(unittest.TestCase):
    def setUp(self):
        self.X, self.Z = np.meshgrid(np.arange(-60, 60), np.arange(-60, 60), indexing="ij")
        self.H = 40 + 12 * noise.fbm(self.X.shape, 30, 3, seed=3) - 0.05 * self.Z

    def test_a_river_never_climbs_and_only_cuts_but_its_banks(self):
        X, Z, H = self.X, self.Z, self.H
        path = [(-50, -55), (0, 0), (40, 55)]
        H2, river = LF.watercourse(H, X, Z, path, width=5, depth=2, lowest=20)
        beside = ndimage.binary_dilation(river.mask, np.ones((3, 3))) & ~river.mask
        self.assertTrue((H2[~beside] <= H[~beside] + 1e-9).all())          # a bank may rise to hold the water
        s, bed, _ = LF._sample(H2, X, Z, path)
        self.assertTrue((np.diff(bed) <= 1e-9).all())
        self.assertGreaterEqual(bed.min(), 20)
        self.assertTrue(river.mask.any())

    def test_a_profile_holds_its_levels_and_its_mode(self):
        X, Z = self.X.astype(float), self.Z.astype(float)
        d = np.abs(X)
        steps = [LF.Step(20, 28, 57), LF.Step(38, 55, 74)]
        h = LF.profile(np.zeros(X.shape), d, 41, steps)
        self.assertTrue((h[d < 20] == 41).all() and (h[(d >= 28) & (d < 38)] == 57).all() and (h[d >= 55] == 74).all())
        row = h[:, 60]
        self.assertTrue((np.diff(row[60:]) >= 0).all())                          # it climbs outward, never back
        talus = LF.profile(np.zeros(X.shape), d, 41, steps, talus=(3, 5))
        self.assertTrue((talus[(d >= 15) & (d < 20)] > 41).any() and (talus >= h).all())
        low = np.full(X.shape, 50.0)
        self.assertTrue((LF.profile(low, d, 41, steps, mode="lift") >= low).all())
        self.assertTrue((LF.profile(low, d, 41, steps, mode="cut") <= low).all())
        bank = LF.profile(self.H, d, 30, [LF.Step(5, 12, "ground")], mode="cut")
        self.assertTrue((bank[d >= 12] == self.H[d >= 12]).all())

    def test_a_profile_is_the_hollow_mesa_canyon_it_was_written_from(self):
        X = self.X.astype(float)
        d = 5.0 - X
        line = lambda seed: noise.fbm((120,), 9, 2, seed=seed)[None, :]          # noqa: E731
        fe = 12 + 2.6 * line(1)
        b0, small, jag = fe + 4, noise.fbm(X.shape, 8, 2, seed=4), 1.2 * noise.fbm(X.shape, 3, 2, seed=7)
        b1 = b0 + 9 + 2.0 * line(2)
        rim = b1 + 6 + 1.5 * line(3)
        floor = 41 + 0.5 * small + 3.0 * noise.smoothstep(fe - 5, fe, d)
        bench, plateau = 57 + 0.4 * small, 74 + 1.6 * noise.fbm(X.shape, 40, 2, seed=5)
        h = floor                                                                 # the board's own formula
        h = np.where(d >= fe + jag, np.maximum(h, 41 + 16 * noise.smoothstep(fe + jag, b0 + jag, d)), h)
        h = np.where(d >= b0 + jag, bench, h)
        h = np.where(d >= b1 + jag, 57 + 17 * noise.smoothstep(b1 + jag, rim + jag, d), h)
        h = np.where(d >= rim + jag, plateau, h)
        op = LF.profile(np.zeros(X.shape), d, 41, [LF.Step(fe, b0, 57, bench), LF.Step(b1, rim, 74, plateau)],
                        floor_ground=floor, jag=jag)
        self.assertTrue(np.array_equal(op, h))

    def test_level_ground_is_level_inside_and_left_alone_outside(self):
        X, Z, H = self.X.astype(float), self.Z.astype(float), self.H
        dd = np.hypot(X - 10, Z + 5)
        flat = LF.level(H, dd, 50, inner=8, outer=14)
        self.assertTrue((flat[dd < 8] == 50).all() and (flat[dd >= 14] == H[dd >= 14]).all())
        k = noise.smoothstep(8, 14, dd)                                     # Hollow Mesa's pads, as written there
        self.assertTrue(np.array_equal(flat, np.where(dd < 14, 50 * (1 - k) + H * k, H)))
        lifted = LF.level(H, dd, 50, inner=8, outer=14, mode="lift")
        self.assertTrue((lifted >= np.where(dd < 8, -np.inf, H)).all())
        median = LF.level(H, dd, "median", inner=8, outer=14)
        self.assertEqual(median[70, 55], float(np.median(H[dd < 8])))            # at the centre, (10, -5)
        e = shapes.ellipse_distance(X, Z, (0, 0), 20, 5, angle=90)
        self.assertAlmostEqual(float(e[60, 80]), 1.0)                       # turned: 20 along z, 5 along x
        self.assertAlmostEqual(float(e[65, 60]), 1.0)

    def test_a_mound_peaks_at_its_rise_and_a_crater_is_walked_out_of(self):
        X, Z, H = self.X.astype(float), self.Z.astype(float), np.full(self.X.shape, 40.0)
        e = shapes.ellipse_distance(X, Z, (5, 5), 10, 6)
        heap = LF.mound(H, e, 7)
        self.assertEqual(heap[65, 65], 47.0)
        self.assertTrue((heap[e >= 1] == 40).all() and (heap >= H).all())
        d = np.hypot(X + 20, Z - 10)
        bowl = LF.crater(H, d, 30, 12, flat=1.5)
        self.assertEqual(bowl[40, 70], 30)
        self.assertTrue((bowl[d > 12] == 40).all() and (bowl <= 40).all())
        inside = d <= 12
        steps = np.abs(np.diff(bowl, axis=0))[inside[1:] & inside[:-1]].max()
        self.assertLessEqual(steps, 1 + 1e-9)                             # one block a block: climbable

    def test_an_elliptical_spire_is_a_round_one_stretched(self):
        X, Z = self.X.astype(float), self.Z.astype(float)
        H = np.full(X.shape, 30.0)
        oval = LF.spire(H, X, Z, (0, 0), r=8, rz=16, top=50, jag=0.0)
        round_ = LF.spire(H, X, Z / 2, (0, 0), r=8, top=50, jag=0.0)
        self.assertTrue(np.allclose(oval, round_))
        self.assertGreater(oval[60, 72], 30)                               # 12 out along z: still on its foot
        self.assertEqual(oval[72, 60], 30)                                 # 12 out along x: past it

    def test_a_ridge_climbs_from_its_foot_lifts_only_and_is_terraced(self):
        X, Z, H = self.X.astype(float), self.Z.astype(float), self.H
        foot = noise.line(X.shape, "z", 20, seed=4, amp=4, base=-20)
        r = LF.ridge(H, X, foot, 15, 80.0, terrace=(3, 1.0, 0.25))
        east = X >= foot + 0 * X
        self.assertTrue((r >= H).all() and (r[east] == H[east]).all())      # only lifts; nothing past its foot
        cut = (noise.smoothstep(foot, foot - 15, X) > 0.25) & (r > H)
        self.assertTrue(cut.any() and np.allclose((r[cut] - r[cut].min()) % 3, 0))   # three-block terraces
        spur = LF.ridge(H, X, foot, 15, 50.0, spurs=[(np.abs(Z), np.full(X.shape, 70.0), (10, 2))])
        self.assertTrue((spur[(np.abs(Z) < 2) & (X > 0)] >= 70).all())       # the arm holds its top out east

    def water_world(self, H, *waters):
        w = World(-60, -60, 120, 120, sy=96)
        top = np.round(H).astype(int)
        terrain.lay(w, top)
        level = np.zeros(H.shape)
        for wat in waters:
            level = np.maximum(level, np.where(wat.mask, wat.surface, 0))
        terrain.fill_water(w, top, level, bed=(B.GRAVEL, 0))
        self.assertTrue(all(w.id(int(x), int(top[i, k]), int(z)) == B.GRAVEL
                            for (i, k), x, z in zip(np.argwhere(level > 0), self.X[level > 0], self.Z[level > 0])))
        return w

    def test_a_river_into_a_lake_leaves_no_water_against_air(self):
        X, Z, H = self.X, self.Z, self.H
        H1, lake = LF.lake(H, X, Z, (30, 40), 12, 30, depth=4, seed=1)
        H2, river = LF.watercourse(H1, X, Z, [(-50, -50), (0, 0), (30, 40)], width=5, depth=3, water=2,
                                   lowest=28, into=lake)
        self.assertTrue(river.falls)
        self.assertEqual(audit.loose_water(self.water_world(H2, lake, river)), [])

    def test_a_river_meets_the_sea_at_its_level_with_no_bank_in_it(self):
        X, Z, H = self.X, self.Z, self.H
        H1, sea = LF.coast(H - 12, X, Z, 30, shelf=10)                       # the sea runs on to the world's edge
        H2, river = LF.watercourse(H1, X, Z, [(0, -40), (0, 0), (0, 59)], width=5, depth=2, lowest=29, into=sea)
        self.assertTrue((H2[sea.mask] <= H1[sea.mask] + 1e-9).all())        # nothing raised inside the sea
        mouth = river.mask & sea.mask
        self.assertTrue((river.surface[mouth] == 30).all())
        self.assertEqual(audit.loose_water(self.water_world(H2, sea, river)), [])

    def test_loose_water_allows_a_fall_and_a_waterfall_only(self):
        w = World(0, 0, 8, 3, sy=12)
        w.ids[:, :4, :] = B.STONE
        w.ids[1:7, 4, 1] = B.WATER                      # a water block standing on stone in open air
        self.assertTrue(audit.loose_water(w))
        w.ids[:, 4, :] = B.STONE
        w.ids[3, 5, 1] = B.WATER                        # a step: air beside it, lower water under that air
        w.ids[4, 4, 1] = B.WATER
        w.ids[2, 5, 1] = B.STONE
        w.ids[3, 5, 0] = w.ids[3, 5, 2] = B.STONE
        self.assertEqual([r for r in audit.loose_water(w) if r[:3] == (3, 5, 1)], [])
        w.set(6, 8, 1, B.WATER_FLOW, 8)                 # falling water over the void is a waterfall
        self.assertEqual([r for r in audit.loose_water(w) if r[:3] == (6, 8, 1)], [])

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


class Capture(unittest.TestCase):
    def test_a_wool_places_itself_its_spawner_and_its_room(self):
        o = O.Objectives(O.Teams(("red-team", "Red", "red"), ("blue-team", "Blue", "blue")), Symmetry("half"))
        o.add(O.Wool("blue-team", "lime", slot=(3, 11, 6), found=(-8, 11, -6), room=O.Box(-10, 11, -8, -6, 14, -4)),
              color="magenta")
        o.add(O.Spawn("red-team", (-2, 11, -10), area=O.Box(-4, 11, -12, 0, 14, -8), protect=("iron block",)))
        w = World(-12, -12, 24, 24, sy=20)
        w.fill(-12, 0, -12, 11, 10, 11, B.STONE)
        o.stamp(w)
        self.assertEqual(w.get(-8, 11, -6), (B.WOOL, 5))
        self.assertEqual(o.check(w), [])
        w.set(-8, 11, -6, B.AIR)
        self.assertEqual(len(o.check(w)), 1)                                # the wool is missed
        x = xml.dom.minidom.parseString(o.write(Doc("T", "1", "t")).tostring())
        self.assertEqual(len(x.getElementsByTagName("spawner")), 2)
        self.assertEqual({r.getAttribute("id") for r in x.getElementsByTagName("union")},
                         {"reds-woolrooms", "blues-woolrooms"})
        self.assertEqual(len(x.getElementsByTagName("renewable")), 2)
        self.assertEqual([m[2] for m in o.markers()].count("w"), 2)          # each room marked

    def test_a_walk_over_build_zones(self):
        R = Raster((0, 19), (0, 4), ["void", "floor"], base_h=0, base_kind="void")
        R.rect(0, 5, 0, 4, 10, "floor", both=False)
        R.rect(14, 19, 0, 4, 10, "floor", both=False)
        zone = R.mask("void")
        E = plangraph.graph(R, {"floor"}, rules=plangraph.PlanRules(jumps=False, diagonals=True), bridge=zone)
        D, prev = plangraph.dijkstra(E, [(0, 2)])
        cost, by, _ = plangraph.measure(D, prev, E, [(19, 2)])
        self.assertAlmostEqual(by["bridge"], 9.0)                           # the gap, built over
        self.assertLess(cost, 20)
        Ed = plangraph.graph(R, {"floor"}, rules=plangraph.PlanRules(jumps=False, diagonals=True))
        Dd, _ = plangraph.dijkstra(Ed, [(0, 0)])
        self.assertAlmostEqual(Dd[(4, 4)], 4 * math.sqrt(2))                # octile, not four-way

    def test_the_voxel_walk_builds_and_dies(self):
        w = World(-1, -1, 24, 3, sy=40)
        w.fill(0, 20, 0, 4, 20, 0, B.STONE)
        w.fill(15, 20, 0, 19, 20, 0, B.STONE)
        zone = np.zeros((w.sx, w.sz), bool)
        zone[6:16, :] = True
        d = walk.walk(w.ids, [(0, 21, 0)], w.x0, w.z0, walk.MoveRules(jumps=False, build=(zone, (21, 21))))
        self.assertGreater(d[19 - w.x0, 21, 0 - w.z0], 0)
        w.fill(0, 5, 0, 19, 5, 0, B.STONE)                                  # a floor below the kill height
        d = walk.walk(w.ids, [(0, 21, 0)], w.x0, w.z0, walk.MoveRules(jumps=False, kill_y=10))
        self.assertEqual(d[8 - w.x0, 6, 0 - w.z0], -1)

    def test_a_kit(self):
        from pgmvox.mapxml import item
        d = Doc("T", "1", "t")
        d.kit("k", item("bow", 1, enchant=[("infinity", 1)], unbreakable=True), item("leather boots", tag="boots"))
        d.kill_below(40, how="kit")
        x = xml.dom.minidom.parseString(d.tostring())
        self.assertEqual(len(x.getElementsByTagName("kit")), 2)
        self.assertEqual(x.getElementsByTagName("enchantment")[0].getAttribute("level"), "1")


class Forms(unittest.TestCase):
    def test_a_tower_carries_its_ledge_rings(self):
        w = World(-16, -16, 32, 32, sy=80)
        rng = np.random.default_rng(1)
        n = forms.tower(w, 0, 0, 10, 60, 5, lambda y, b: (B.STONE, 0), rng, bulge=0.0, vines=0)
        self.assertGreater(n, 0)

        def area(y):
            return int((w.ids[:, y, :] == B.STONE).sum())
        self.assertGreater(area(18), area(17))                              # a ledge every nine courses
        self.assertGreater(area(18), area(19))
        self.assertGreater(area(11), area(58))                              # tapering up the stack
        self.assertEqual(w.id(0, 60, 0), B.GRASS)                           # the crown

    def test_a_skirt_never_rises_into_the_floor(self):
        w = World(-10, -10, 20, 20, sy=40)
        land = np.zeros((20, 20), bool)
        land[5:15, 5:15] = True
        floor = np.where(land, 30, 0)
        T = __import__("pgmvox.terrain", fromlist=["lay"])
        T.lay(w, floor, mask=land, from_y=20)
        forms.skirt(w, land, floor, lambda y: (B.STONE, 0), np.random.default_rng(2), bulge=np.ones((20, 20)))
        cols = w.ids.transpose(0, 2, 1)[~land]                              # every column off the floor, by y
        self.assertFalse((cols[:, 29:] != 0).any())                         # nothing at floor - 1 or above
        self.assertTrue((cols[:, 20:28] != 0).any())                        # but ledges below it


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
        self.assertEqual(facing, "s")
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
        F.extrude(w, shapes.rect_cells(0, 0, 20, 5), 0, 8, faces_=[F.word(2, "LT", F.DARK)])
        south = ["".join("#" if w.id(x, y, 5) == B.AIR else "." for x in range(0, 21)) for y in range(6, 1, -1)]
        north = ["".join("#" if w.id(x, y, 0) == B.AIR else "." for x in range(20, -1, -1)) for y in range(6, 1, -1)]
        self.assertEqual(south[0].strip("."), "#...###")
        self.assertEqual(south, north)                           # the same word, read from its own side
        self.assertEqual(w.get(7, 6, 4), F.DARK)                 # set back, in the inset block

    def test_corners_stay_flush(self):
        w = World(-2, -2, 12, 12, sy=8)
        F.extrude(w, shapes.rect_cells(0, 0, 5, 5), 0, 5, faces_=[F.band(0, 5, F.DARK)])
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

    def test_a_plan_read_off_terrain(self):
        H = np.zeros((20, 10), int)
        H[10:, :] = 3                                                       # a three-block step across x = 10
        water = np.zeros(H.shape, bool)
        water[2:4, :] = True
        R = Raster.from_heights(H, -10, 0, water=water)
        self.assertEqual((R.at(-10, 0), R.at(-7, 5)), ((0, "ground"), (0, "water")))
        E = plangraph.graph(R, {"ground"}, rules=plangraph.PlanRules(jumps=False))
        up, _ = plangraph.dijkstra(E, [(-5, 5)])
        down, _ = plangraph.dijkstra(E, [(5, 5)])
        self.assertNotIn((5, 5), up)                                        # three up is a wall
        self.assertIn((-5, 5), down)                                        # three down is a drop
        self.assertNotIn((-7, 5), down)                                     # water is not walked

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
        o.add(O.Destroyable("red-dtm", "Red's", "red-team", O.Box(-16, 14, -8, -15, 15, -7)))      # three over
        o.add(O.Core("red-core", "Red's Core", "red-team", O.Box(-12, 14, 4, -10, 16, 6)))        # the floor
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
    def test_paint_layers_choose_the_top_by_slope_and_place_first_match_first(self):
        w = World(0, 0, 20, 4, sy=80)
        H = np.tile((np.arange(20) * np.where(np.arange(20) < 10, 0, 3))[:, None] + 10, (1, 4))
        east = np.zeros((20, 4), bool)
        east[15:] = True
        deg = terrain.lay(w, H, top=lambda d, h: (B.GRASS, 0), ledges=False, paint=[
            terrain.Paint((B.SAND, 0), slope=(30, None), where=east),
            terrain.Paint((B.STONE, 0), slope=(30, None)),
            terrain.Paint((B.CLAY, 0), values=[(np.full((20, 4), 0.9), 0.5, None)], where=~east)])
        for i in range(20):
            top = w.id(i, int(H[i, 1]), 1)
            want = (B.SAND if i >= 15 else B.STONE) if deg[i, 1] > 30 else (B.CLAY if i < 15 else B.GRASS)
            self.assertEqual(top, want, i)

    def test_an_island_hangs_sheer_under_its_rift_and_tapers_elsewhere(self):
        X, Z = np.meshgrid(np.arange(-60, 0), np.arange(-30, 30), indexing="ij")
        land = (X >= -50) & (X <= -11) & (Z >= -29)
        top = np.full(X.shape, 60)
        bottom = terrain.island_bottom(top, land, X > -11, taper=(4, 0.9), sheer_taper=(26, 1.2), floor=5)
        self.assertEqual(bottom[49, 30], round(60 - (26 + 1.2)))            # at the rift's lip: 26 deep already
        self.assertEqual(bottom[10, 30], round(60 - (4 + 0.9)))             # at the far edge: the taper's start
        self.assertTrue((bottom[land] >= 5).all())
        inward = bottom[(X >= -50) & (X <= -32) & (Z == 0)]
        self.assertTrue((np.diff(inward) <= 0).all())                      # deeper the further from the void

    def test_nothing_is_left_under_a_columns_bottom(self):
        H = np.full((6, 6), 30)
        bottom = np.arange(36).reshape(6, 6) % 9 + 5
        w = World(0, 0, 6, 6, sy=40)
        terrain.lay(w, H, from_y=1, bottom=bottom)
        for i in range(6):
            for k in range(6):
                self.assertTrue((w.ids[i, :bottom[i, k], k] == 0).all())
                self.assertTrue((w.ids[i, bottom[i, k]:31, k] != 0).all())

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
    def test_a_columns_top_is_the_heightmaps(self):
        w = World(0, 0, 3, 3, sy=10)
        w.set(0, 4, 0, B.STONE)
        w.set(1, 2, 1, B.STONE)
        w.set(1, 6, 1, B.LEAVES)
        H = w.heightmap()
        self.assertEqual([w.top(x, z) for x in range(3) for z in range(3)], H.ravel().tolist())
        self.assertEqual((w.top(0, 0), w.top(1, 1), w.top(2, 2), w.top(9, 9)), (4, 2, -1, -1))

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


class Underground(unittest.TestCase):
    def rock(self):
        w = World(0, 0, 60, 30, sy=64)
        w.ids[:, :41, :] = B.STONE
        return w, np.full((60, 30), 40)

    def test_a_tunnel_has_a_level_floor_and_keeps_its_cover(self):
        w, H = self.rock()
        n, floor = U.tunnel(w, [(5, 20, 15, 2.5), (30, 22, 15, 3), (50, 24, 10, 2.5)], ground=H)
        self.assertGreater(n, 500)
        self.assertEqual(w.id(30, floor(30, 15) - 1, 15), B.STONE)       # nothing carved under the floor
        self.assertFalse((w.ids[:, 38:41, :] == B.AIR).any())             # nor within three of the surface
        d = walk.walk(w.ids, [(5, 20, 15)], w.x0, w.z0)
        self.assertIsNotNone(walk.nearest(d, 0, 0, 50, 24, 10, r=2))

    def test_a_gallery_climbs_by_stairs_and_its_shaft_reaches_the_top(self):
        w, _ = self.rock()
        line = U.gallery_line([(5, 10, 5), (40, 14, 5), (40, 14, 25)])
        self.assertTrue(all(abs(b[1] - a[1]) <= 1 for a, b in zip(line, line[1:])))
        U.gallery(w, line, np.random.default_rng(2))
        U.shaft(w, 5, 5, 10, 40)
        self.assertIn(B.COBBLE_STAIRS, w.ids)
        d = walk.walk(w.ids, [line[3]], w.x0, w.z0)
        self.assertIsNotNone(walk.nearest(d, 0, 0, *line[-1]))
        self.assertIsNotNone(walk.nearest(d, 0, 0, 5, 41, 5, r=2))         # into the well and up its ladder


class Trees(unittest.TestCase):
    def tree(self):
        logs = [(0, y, 0, B.LOG, 0) for y in range(4)] + [(1, 2, 0, B.LOG, 4)]
        leaves = [(dx, 4, dz, B.LEAVES, 0) for dx in (-1, 0, 1) for dz in (-1, 0, 1)]
        return TR._tree("t-1", "t", logs + leaves)

    def ground(self):
        w = World(0, 0, 30, 30, sy=30)
        w.ids[:, :11, :] = B.DIRT
        w.ids[:, 10, :] = B.GRASS
        return w

    def test_a_tree_is_planted_whole_and_turned(self):
        w, t = self.ground(), self.tree()
        self.assertEqual((t.crown, t.height), (1, 5))
        self.assertTrue(TR.plant(w, 10, 10, t, turn=1))
        self.assertEqual(w.id(10, 11, 10), B.LOG)
        self.assertEqual(w.id(10, 10, 10), B.DIRT)                        # no grass under the trunk
        self.assertEqual(w.get(10, 13, 11), (B.LOG, 8))                   # the branch along x now lies along z
        self.assertEqual(w.get(10, 15, 10), (B.LEAVES, 4))                # leaves do not decay

    def test_a_tree_is_refused_whole(self):
        w, t = self.ground(), self.tree()
        w.set(11, 15, 11, B.PLANKS)
        before = w.ids.copy()
        self.assertFalse(TR.plant(w, 10, 10, t))
        self.assertTrue((w.ids == before).all())
        self.assertFalse(TR.plant(w, 20, 20, t, allowed=lambda x, z: x < 20))

    def test_a_wood_keeps_its_crowns_apart(self):
        w, t = self.ground(), self.tree()
        placed = []
        n = TR.scatter(w, np.ones((30, 30), bool), {"t": [t]}, {"t": 1}, np.random.default_rng(3), spacing=2,
                       planted=placed)
        self.assertEqual(n, len(placed))
        for i, (ax, az, _) in enumerate(placed):
            for bx, bz, _ in placed[i + 1:]:
                self.assertGreaterEqual(math.hypot(ax - bx, az - bz), 2)

    @unittest.skipUnless(os.path.exists(os.path.join(TR.studio_root(), "src", "PgmStudio.Minecraft", "Library",
                                                     "trees.json")), "the studio is not checked out")
    def test_the_studio_library_reads(self):
        by = TR.kinds(TR.library())
        self.assertIn("birch", by)
        self.assertTrue(all(t.blocks and t.crown > 0 for t in by["oak"]))


class Props(unittest.TestCase):
    def test_scattered_points_keep_apart_and_off_the_taken(self):
        X, Z = np.meshgrid(np.arange(40), np.arange(40), indexing="ij")
        pts = shapes.scatter_points(np.ones((40, 40), bool), 30, 5.0, np.random.default_rng(2), X, Z, taken=[(20, 20)])
        every = pts + [(20, 20)]
        self.assertTrue(len(pts) > 10)
        self.assertTrue(all(math.hypot(a[0] - b[0], a[1] - b[1]) >= 5.0 for i, a in enumerate(every) for b in every[i + 1:]))

    def test_rubble_hangs_over_nothing_unless_told(self):
        for supported in (True, False):
            w = World(0, 0, 12, 12, sy=12)
            w.fill(0, 0, 0, 11, 2, 11, B.STONE)
            w.fill(6, 2, 0, 11, 2, 11, B.AIR)                       # half the floor is a step down
            props.rubble(w, 6, 2, 6, np.random.default_rng(1), r=2.6, supported=supported)
            hanging = [(x, y, z) for x in range(12) for z in range(12) for y in range(3, 12)
                       if w.id(x, y, z) != B.AIR and w.id(x, y - 1, z) == B.AIR]
            self.assertEqual(hanging == [], supported)

    def test_a_masonry_tower_is_climbed_inside_and_entered_at_its_foot(self):
        w = World(0, 0, 9, 9, sy=40)
        px, pz = forms.masonry_tower(w, 1, 1, 7, 7, 10, 14, ladder_on="n", door_side="s")
        self.assertEqual((px, pz), (4, 2))
        self.assertTrue(all(w.id(4, y, 2) == B.LADDER for y in range(11, 25)))
        self.assertEqual((w.id(4, 11, 7), w.id(4, 12, 7)), (B.DARK_OAK_DOOR, B.DARK_OAK_DOOR))
        self.assertEqual(w.id(4, 26, 4), B.GLOWSTONE)

    def test_lamps_stand_beside_the_route_on_alternate_sides(self):
        w = World(0, 0, 60, 20, sy=20)
        X, Z = w.grid()
        H = np.full((60, 20), 5)
        posts = props.lamps(w, [(0, 10), (59, 10)], H, X, Z, every=10, side=3)
        self.assertEqual([z for _, z in posts], [13, 7, 13, 7, 13, 7][:len(posts)])
        self.assertTrue(all(w.id(x, 8, z) == B.GLOWSTONE for x, z in posts))

    def test_a_row_of_stalls_faces_one_way(self):
        w = World(0, 0, 30, 30, sy=20)
        w.ids[:, :6, :] = B.STONE
        cells = props.stalls(w, [(5, z) for z in range(2, 26)], 5, "e")
        self.assertEqual(len(cells) % 9, 0)
        self.assertGreater(len(cells), 9)
        self.assertEqual(w.id(6, 6, 3), B.WOOD_SLAB)                      # the counter on the east side

    def test_a_chest_laid_out_as_a_pattern(self):
        items = props.laid(props.DEFENCE)
        self.assertEqual(len(items), 27)
        picks = [it for it in items if it[1] == "minecraft:iron_pickaxe"]
        self.assertEqual([it[0] for it in picks], [12, 14])               # either side of the middle slot
        self.assertEqual(picks[0][4], [(32, 2)])                          # Efficiency II
        with self.assertRaises(ValueError):
            props.laid((["P........", "", ""], {"P": ("minecraft:planks", 1, 0)}))
        w = World(0, 0, 4, 4, sy=8)
        w.chest(1, 1, 1, items)
        self.assertEqual(w.tiles[-1]["items"][12]["ench"], [[32, 2]])


class Plots(unittest.TestCase):
    def test_a_curio_plot_passes(self):
        m = plot.load(os.path.join(FIXTURES, "bandstand.py"))
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


class DestroyableHeart(unittest.TestCase):
    def test_heart_at_the_middle(self):
        d = O.Destroyable("m", "M", "red-team", O.Box(2, 5, 2, 4, 7, 4), material=(B.EMERALD_BLOCK, 0),
                          materials="emerald block", heart=(B.BEDROCK, 0))
        w = World(0, 0, 8, 8, sy=10)
        d.stamp(w)
        self.assertEqual(w.id(3, 6, 3), B.BEDROCK)
        self.assertEqual(w.id(2, 5, 2), B.EMERALD_BLOCK)
        self.assertEqual(d.check(w), [])

    def test_two_gamemodes(self):
        self.assertEqual(Doc("x", "1", "o", ["ctw", "dtm"]).tostring().count("<gamemode>"), 2)


class HouseDoor(unittest.TestCase):
    def test_no_window_beside_the_door(self):
        for L in (5, 6, 7, 8, 9, 10, 11):
            w = World(-20, -20, 40, 40, sy=80)
            d = BLD.house(w, BLD.House(0, 0, 0, L=L, W=6, floor=64, windows=BLD.window_rhythm(period=2)))
            x, z = d["door"][0], d["door"][1]
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for y in range(65, 68):
                        self.assertNotEqual(w.id(x + dx, y, z + dz), B.PANE, (L, dx, dz, y))


class FloatRule(unittest.TestCase):
    def test_on_the_floor_is_a_problem(self):
        w = World(0, 0, 8, 8, sy=16)
        w.fill(0, 0, 0, 7, 3, 7, B.STONE)
        on = O.Destroyable("m", "M", "red-team", O.Box(2, 4, 2, 3, 5, 3))
        on.stamp(w)
        self.assertTrue(any("float" in p for p in on.check(w)))
        w2 = World(0, 0, 8, 8, sy=16)
        w2.fill(0, 0, 0, 7, 3, 7, B.STONE)
        up = O.Destroyable("m", "M", "red-team", O.Box(2, 7, 2, 3, 8, 3))
        up.stamp(w2)
        self.assertEqual(up.check(w2), [])


class WoolChests(unittest.TestCase):
    def test_studio_loot_in_each_corner(self):
        w = World(0, 0, 12, 12, sy=16)
        corners = props.wool_chests(w, (2, 3, 8, 9), 4, door="s")
        self.assertEqual(len(corners), 4)
        self.assertEqual(len(w.tiles), 8)
        low = [t for t in w.tiles if t["y"] == 5]
        high = [t for t in w.tiles if t["y"] == 6]
        self.assertTrue(all(len(t["items"]) == 27 for t in w.tiles))
        self.assertEqual({i["id"] for i in low[0]["items"]},
                         {"minecraft:planks", "minecraft:potion", "minecraft:golden_apple"})
        bow = [i for i in high[0]["items"] if i["id"] == "minecraft:bow"][0]
        self.assertEqual(bow["ench"], [[48, 1], [51, 1]])
        self.assertEqual(w.get(2, 5, 3), (B.CHEST, 3))
        self.assertEqual(w.get(2, 5, 9), (B.CHEST, 2))

    def test_defence_chest_is_the_studios(self):
        items = props.studio_defence()
        self.assertEqual(len(items), 27)
        self.assertEqual(sorted(i[0] for i in items), list(range(27)))
        self.assertEqual(sum(1 for i in items if i[1] == "minecraft:planks" and i[3] == 5), 12)
        w = World(0, 0, 8, 8, sy=8)
        for y in range(1, 5):
            w.set(3, y, 3, B.BEDROCK)
        props.defence_chests(w, [(3, 3)], 2, "s")
        self.assertEqual(w.get(3, 2, 3), (B.CHEST, 3))
        self.assertEqual(w.id(3, 3, 3), B.AIR)
        self.assertEqual(w.id(3, 4, 3), B.BEDROCK)


if __name__ == "__main__":
    unittest.main()


class QuarterTurns(unittest.TestCase):
    def test_a_world_turns_a_quarter(self):
        w = World(-4, -4, 8, 8, sy=4)
        w.set(-3, 1, -2, B.STONEBRICK_STAIRS, orient.stair("n"))
        keep = np.zeros((8, 8), bool)
        keep[:4, :4] = True                                               # the north-west quarter
        orient.turn_world(w, "cw", keep)
        self.assertEqual(w.get(1, 1, -3), (B.STONEBRICK_STAIRS, orient.stair("e")))   # north turns to east

    def test_four_teams_fan_from_one(self):
        teams = O.Teams(("red-team", "Red", "red"), ("blue-team", "Blue", "blue"), ("green-team", "Green", "green"),
                        ("yellow-team", "Yellow", "yellow"))
        objs = O.Objectives(teams, Symmetry("rot_90"))
        objs.add(O.Spawn("red-team", (-58, 20, -58), yaw=315))
        objs.add(O.Wool("red-team", "lime", slot=(-60, 20, -55), found=(5, 19, -90), keeper="green-team",
                        room=O.Box(1, 19, -94, 8, 24, -87)), color=["orange", "pink", "light_blue"])
        spawns = objs.of(O.Spawn)
        self.assertEqual([s.at for s in spawns], [(-58, 20, -58), (57, 20, -58), (57, 20, 57), (-58, 20, 57)])
        self.assertEqual([s.yaw for s in spawns], [315, 45, 135, 225])
        self.assertEqual([(o.team, o.keeper, o.color) for o in objs.of(O.Wool)][1],
                         ("blue-team", "yellow-team", "orange"))
        d = Doc("t", "1.0.0", "x", "ctw")
        objs.write(d)                                                     # four rooms, each written once
        rooms = [ln for ln in d.tostring().splitlines() if "<cuboid" in ln and 'id="lime-room"' in ln]
        self.assertEqual(len(rooms), 1)


class Brittle(unittest.TestCase):
    def test_a_blueprint_builds_in_the_style(self):
        from pgmvox import brittle as BR
        unit = {(a, b): BR.Cell("flat", 13) for a in range(-4, -1) for b in range(-4, -1)}
        unit[(-1, -3)] = BR.Cell("stair", 10, rises="w")
        unit[(-1, -2)] = BR.Cell("stair", 10, rises="w")
        cells, team = BR.fan(unit)
        w = World(-30, -30, 60, 60, sy=32)
        BR.build(w, cells, only=[c for c in cells if team[c] == 0])
        self.assertEqual(audit.footing(w), [])
        self.assertEqual(w.id(-20, 13, -20), B.SPRUCE_STAIRS)            # the rim on the piece's corner
        self.assertEqual(w.get(-20, 9, -16), (B.STAINED_CLAY, 15))       # the black band at the foot of the cap
        self.assertEqual(w.get(-20, 12, -20), (B.STAINED_CLAY, 15))      # a panel's side, black all the way down
        self.assertEqual(w.id(-19, 13, -18), B.SANDSTONE_STAIRS)         # the bed's outer ring, inside the rim
        self.assertEqual(w.id(-13, 14, -13), B.LOG)                      # its birch, at its middle
        self.assertEqual(w.id(-5, 0, -15), 36)                           # building allowed over the board

    def test_an_under_section_is_hollow_with_its_pillar(self):
        from pgmvox import brittle as BR
        unit = {(a, b): BR.Cell("stacked", 16, under=(b == -3)) for a in (-4, -3) for b in (-4, -3)}
        cells, team = BR.fan(unit)
        w = World(-30, -30, 60, 60, sy=32)
        BR.build(w, cells, only=[c for c in cells if team[c] == 0])
        self.assertEqual(audit.footing(w), [])
        self.assertEqual([w.id(-18, y, -11) for y in (16, 15, 14, 13)],             # the deck's edge, no black band
                         [B.SPRUCE_STAIRS, B.BRICK, B.WOOD_SLAB, B.DARK_OAK_STAIRS])
        self.assertEqual([w.id(-18, y, -13) for y in range(10, 13)], [B.AIR] * 3)   # open under the deck
        self.assertEqual(w.get(-18, 12, -16), (B.STAINED_CLAY, 15))                 # black on the wall behind
        self.assertEqual(w.get(-18, 8, -15), BR.SPRUCE_PLANKS)                      # planks along that wall
        with self.assertRaises(ValueError):                                         # a lower floor at y 0
            BR.build(World(-30, -30, 60, 60, sy=32), {(0, 0): BR.Cell("stacked", 8, under=True)})
        self.assertEqual({w.get(x, 12, -11) for x in (-16, -15)}, {(B.PLANKS, 5)})   # the pillar, two wide
        self.assertEqual([w.id(-18, y, -11) for y in (8, 7, 6, 5, 0)],                # the short cap into the floor
                         [B.SPRUCE_STAIRS, B.BRICK, B.STAINED_CLAY, B.BEDROCK, 36])

    def test_a_studio_plan_tells_water_from_bare_zones(self):
        from pgmvox import studioplan as SP
        plan = {"globals": {"cell": 5, "surface": 9}, "pieces": [{"id": "a", "rect": [-3, -3, 2, 2]}],
                "zones": [{"id": "water", "rect": [-1, -3, 1, 1]}, {"id": "zone", "rect": [-3, -1, 2, 1]}]}
        u = SP.unit(plan, lift=6)
        self.assertEqual((u[(-1, -3)].kind, u[(-3, -1)].kind, u[(-3, -3)].y), ("water", "gap", 15))

    def test_a_house_stacks_whole_cells(self):
        from pgmvox import brittle as BR
        w = World(-5, -5, 20, 20, sy=48)
        BR.house(w, [[(0, 0), (1, 0), (0, 1), (1, 1)], [(0, 0), (1, 0), (1, 1)], [(0, 0)]], 10, 4,
                 door=((0, 1), "s"))
        self.assertEqual(audit.footing(w), [])
        self.assertEqual([w.id(0, y, 7) for y in (11, 12, 13, 14, 15)],                # a plain face, the terrace over it
                         [B.STAINED_CLAY, B.DARK_OAK_STAIRS, B.DARK_OAK_STAIRS, B.BRICK, B.SPRUCE_STAIRS])
        self.assertEqual(w.get(-1, 14, 2), (B.WOOL, 4))                              # the wool's colour under an eave
        self.assertEqual(w.id(2, 15, 7), B.SAND)                                     # the terrace the L leaves
        self.assertEqual((w.id(7, 20, 7), w.id(7, 25, 7)), (B.SAND, B.AIR))         # the L's own terrace, nothing over it
        self.assertEqual((w.id(2, 24, 2), w.get(2, 25, 2)), (B.BEACON, (B.STAINED_GLASS, 4)))
        self.assertEqual((w.id(2, 11, 9), w.id(2, 11, 8)), (B.AIR, B.COBWEB))        # the door, cobwebs inside

    def test_sections_outline_each_other_and_panels_need_a_full_drop(self):
        from pgmvox import brittle as BR
        unit = {(a, b): BR.Cell("flat", 16, section="a" if b < -2 else "b") for a in (-4, -3) for b in (-4, -3, -2, -1)}
        unit[(-2, -4)] = BR.Cell("flat", 13)                                      # three under: no room for a panel
        cells, team = BR.fan(unit)
        w = World(-30, -30, 60, 60, sy=32)
        BR.build(w, cells, only=[c for c in cells if team[c] == 0],
                 fill=lambda piece, cs: "grass" if cs[piece[0]].section == "b" else None)
        self.assertEqual(audit.footing(w), [])
        self.assertEqual({w.get(-17, 16, z) for z in (-11, -10)}, {BR.SPRUCE_PLANKS})  # two sections meet in planks
        self.assertNotIn(B.LOG, {w.id(x, 17, z) for x in range(-20, -10) for z in range(-10, 0)})   # grass, no tree
        self.assertIn(B.LOG, {w.id(x, 17, z) for x in range(-20, -10) for z in range(-20, -10)})    # a bed's birch
        self.assertEqual([w.id(-11, y, -18) for y in (16, 15, 14)],                  # over three: brick and dark oak
                         [B.SPRUCE_STAIRS, B.BRICK, B.WOOD_SLAB])


class Grammar(unittest.TestCase):
    def test_split_and_tile_cut_a_box_into_rectangles(self):
        from pgmvox import grammar as G
        secs = G.split((0, 0, 9, 6), 2, 2, y=10)
        self.assertEqual([s.boxes[0] for s in secs], [(0, 0, 4, 2), (0, 3, 4, 6), (5, 0, 9, 2), (5, 3, 9, 6)])
        self.assertEqual(len(G.tile((0, 0, 19, 9), 5, y=10)), 8)

    def test_a_style_lays_faces_seams_and_fills_by_rule(self):
        from pgmvox import grammar as G
        courses = [(B.STONEBRICK, 0), (B.BRICK, 0), (B.STONE, 0)]
        face = G.Face(courses, G.Accent(4, frame=[(B.STONEBRICK, 0)] * 3, inner=[(B.STONEBRICK, 0), (B.GLASS, 0),
                                                                                 (B.GLASS, 0)], every=2, min_air=3))
        laid = []

        def checker(w, lot, rng):
            for x, z in lot.cols:
                w.set(x, lot.y, z, B.WOOL, (x + z) % 2)
            laid.append(lot.section.name)
            return True
        style = G.Style("test", body=lambda w, x, z, h: [w.set(x, y, z, B.STONE) for y in range(h)],
                        faces={"edge": face}, seam=(B.PLANKS, 0), fills={"checker": checker},
                        choose=lambda sec, lot: ["checker"])
        secs = G.split((0, 0, 7, 3), 2, 1, y=10, name="a") + [G.Section(((0, 4, 7, 7),), 7, "low")]
        g = G.Ground(secs)
        w = World(-2, -2, 12, 12, sy=16)
        G.lay(w, g, style)
        self.assertEqual(g.depth(3, 1), 0)                                   # the seam between two sections
        self.assertEqual(w.get(3, 10, 1), (B.PLANKS, 0))
        self.assertEqual(w.id(1, 9, 3), B.GLASS)                             # an accent bay over a drop of three
        self.assertEqual(w.id(5, 6, 7), B.BRICK)                             # the next bay along is plain
        self.assertEqual(sorted(laid), ["a-0-0", "a-1-0", "low"])

    def test_the_claywork_style_inlays_its_bays_and_lays_its_arrows(self):
        from pgmvox import clay
        from pgmvox import grammar as G
        secs = [G.Section(((0, 0, 8, 8),), 20, "front-0-0", "plate", motifs=(("arrow", (("d", "n"),)),)),
                G.Section(((9, 0, 17, 8),), 20, "front-1-0", "inlay")]
        w = World(-2, -2, 22, 12, sy=32)
        G.lay(w, G.Ground(secs), clay.style(dye=14))
        self.assertEqual(w.get(4, 20, 2), (B.WOOL, 14))                           # the arrow's tip, one in
        self.assertEqual((w.get(4, 20, 1), w.get(3, 20, 2)), (clay.BRICK, clay.DIORITE))   # its frame, its plate
        self.assertEqual(w.get(9, 20, 4), clay.ANDESITE)                          # the seam between sections
        self.assertEqual((w.id(4, 15, 8), w.get(4, 15, 7), w.get(4, 17, 7)), (B.AIR, (B.QUARTZ, 1), (B.STAINED_CLAY, 14)))
        self.assertEqual(w.id(0, 0, 0), 36)

    def test_made_ground_reads_the_grown_ground_beside_it(self):
        from pgmvox import brittle as BR
        unit = {(a, b): BR.Cell("flat", 16, section="a") for a in (-4, -3) for b in (-4, -3)}
        cells, team = BR.fan(unit)
        grown = {(x, z): 13 for x in range(-10, -5) for z in range(-20, -12)}     # a meadow three under its east
        grown.update({(x, z): 16 for x in range(-10, -5) for z in range(-12, -10)})  # and one level with it
        w = World(-30, -30, 60, 60, sy=32)
        BR.build(w, cells, only=[c for c in cells if team[c] == 0], grown=grown)
        self.assertEqual([w.id(-11, y, -18) for y in (16, 15, 14)],                  # a face as deep as the drop,
                         [B.SPRUCE_STAIRS, B.BRICK, B.WOOD_SLAB])                     # no panel
        self.assertEqual(w.get(-11, 16, -12), BR.SPRUCE_PLANKS)                      # level with it: a seam
