"""Tests for pgmvox: what each module promises, checked on small worlds and plans.

    cd freeform/lib && python3 -m unittest discover -s tests -v
"""
import os
import sys
import tempfile
import unittest
import xml.dom.minidom

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from pgmvox import B, World, audit, blocks, move, orient, plangraph, plot, render, sight, terrain, walk  # noqa: E402
from pgmvox.mapxml import Doc, E, duration, point  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402

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


class Terrain(unittest.TestCase):
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
