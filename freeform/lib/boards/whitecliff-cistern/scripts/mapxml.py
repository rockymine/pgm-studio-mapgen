"""Write Whitecliff Cistern's map.xml, a king of the hill: the teams, spawns and observer from the plan's objectives, the
three hills (the Cistern at two a second, the Garden and the Boatyard at one), a score limit, a twenty-minute clock won
by the higher score, the kit, the fall past the stack, building only over the stack and no higher than the build height.

    python3 mapxml.py > map.xml
"""
import plan as P
from pgmvox.play.rules import Build, Item, KillHeight, Kit, Map, Match

M = Map("Whitecliff Cistern", "0.1.0", "Hold the hills: the Cistern pays two a second, the Garden and the Boatyard one.", "koth",
        authors=["Claude (freeform generator, on pgmvox)"],
        objectives=P.objectives(),
        kit=Kit(
            Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
            Item("iron pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True),
            Item("wood", 4, 64, 0), Item("stained clay", 5, 32, team_color=True), Item("golden apple", 6, 4),
            Item("cooked beef", 8, 16), Item("arrow", 28),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("iron chestplate", unbreakable=True, wear="chestplate"),
            Item("chainmail leggings", unbreakable=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=P.MAX_BUILD),
        kill=KillHeight(P.KILL_Y),
        match=Match(score=300, time=20 * 60, result="score"))
print(M.xml())
