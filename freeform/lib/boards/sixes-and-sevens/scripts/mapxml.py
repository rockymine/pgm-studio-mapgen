"""Write Sixes and Sevens' map.xml: two teams, their spawns and their two monuments each from the plan's objectives,
the kit, the play area, the mountains over the bunkers closed, the build height, and no fire from the lava."""
import plan as P
from plan import objectives
from pgmvox.play.logic import Gamerules
from pgmvox.play.objectives import Box
from pgmvox.play.rules import Build, Item, Kit, Map, Match, terrain_of, Bounds, Zone

TOP = 159
O = objectives()
O.add(Bounds(Box(P.X[0], 0, P.Z[0], P.X[1], TOP, P.Z[1]), build=False), mirror=False)
# over each bunker the mountain is scenery: closed above the facade's crown, and the wall's crest a block under it
O.add(Zone("red-mountain", [Box(P.X[0], 75, P.Z[0], P.FACADE_X - 4, TOP, P.Z[1])], enter="never",
           enter_message="The mountain is out of bounds"), mirror=False)
O.add(Zone("blue-mountain", [Box(-1 - P.X[0], 75, -1 - P.Z[0], -1 - P.FACADE_X + 4, TOP, -1 - P.Z[1])],
           enter="never", enter_message="The mountain is out of bounds"), mirror=False)

M = Map("Sixes and Sevens", "1.0.0", "Break the enemy's Reactor and Pump; keep your own.", "dtm",
        authors=["Claude (on pgmvox)"], contributors=[("rockymine", "the Bunker style and the brief")],
        terrain=terrain_of(__file__),
        objectives=O,
        kit=Kit(
            Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
            Item("iron pickaxe", 2, enchant=[("efficiency", 1)], unbreakable=True),
            Item("iron axe", 3, enchant=[("efficiency", 1)], unbreakable=True), Item("wood", 4, 64, 1),
            Item("glass", 5, 32), Item("golden apple", 6), Item("water bucket", 7), Item("cooked beef", 8, 16),
            Item("arrow", 28), Item("wood", 31, 64, 1),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("iron chestplate", unbreakable=True, wear="chestplate"),
            Item("chainmail leggings", unbreakable=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(void=False, max_height=74),
        match=Match(time="30m", result="objectives"),
        rules=["Each team defends its Reactor, in the tall hall behind its door, and its Pump, in the yard beside it.",
               "The crevasses run down to lava. The mountains over the bunkers are out of bounds."],
        parts=[Gamerules({"doFireTick": False})])

if __name__ == "__main__":
    print(M.xml())
