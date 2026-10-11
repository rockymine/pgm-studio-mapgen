"""Write Overgrowth's map.xml, a team deathmatch: the teams of sixteen, their spawns and the observer from the plan's
objectives; the kit; a score of one a kill to a limit of 75; a forty-minute clock won by the higher score; a fall
off the terraces' bridges hurts; building anywhere up to the build height.

    python3 mapxml.py > map.xml
"""
import plan as P
from pgmvox.play.rules import Build, Item, Kit, Map, Match

M = Map("Overgrowth", "0.1.0", "Kill the other team: seventy-five points, or the higher score at forty minutes.", "tdm",
        authors=["Claude (freeform generator, on pgmvox)"],
        objectives=P.objectives(),
        kit=Kit(
            Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
            Item("iron pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True),
            Item("wood", 4, 64, 3), Item("stained clay", 5, 32, team_color=True), Item("golden apple", 6, 4),
            Item("water bucket", 7), Item("cooked beef", 8, 16), Item("arrow", 28),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("iron chestplate", unbreakable=True, wear="chestplate"),
            Item("chainmail leggings", unbreakable=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=P.MAX_BUILD, void=False),
        match=Match(score=75, kills=1, deaths=0, time=40 * 60, result="score"))
print(M.xml())
