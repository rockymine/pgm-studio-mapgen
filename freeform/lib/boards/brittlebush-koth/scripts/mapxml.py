"""Write Brittlebush KotH's map.xml: four teams, their spawns and the five hills from the plan's objectives; the kit, with
sixteen leaves to bridge with, from which the kill reward follows; the golden apples on the inner islands and
the arrows on the landings; building only over the board; the score and the time.
"""
import plan as P
from pgmvox.play.rules import Build, Item, Kit, Map, Match, Spawner, terrain_of

O = P.objectives()

for k, (x, z) in enumerate(P.APPLES):                # golden apples on the inner islands
    O.add(Spawner(f"apples-{k}", (x, P.LEVEL[2] + 1, z), [("golden apple", 1)], delay="30s", max_entities=1),
          mirror=False)
for k, (x, z) in enumerate(P.ARROWS):                # arrows on the landings
    O.add(Spawner(f"arrows-{k}", (x, P.LEVEL[0] + 1, z), [("arrow", 4)], delay="10s", max_entities=8), mirror=False)
M = Map("Brittlebush KotH", "1.0.0", "Hold the hills: the Dais in the middle, and the islands between the spawns.", "koth",
        terrain=terrain_of(__file__),
        authors=["Claude (freeform generator, pgmvox)"],
        objectives=O,
        kit=Kit(
            Item("stone sword", 0, unbreakable=True), Item("bow", 1, unbreakable=True),
            Item("iron pickaxe", 2, unbreakable=True), Item("leaves", 3, 16),
            Item("cooked beef", 4, 8), Item("arrow", 8, 16),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
            Item("leather leggings", unbreakable=True, team_color=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=P.MAX_BUILD),
        match=Match(score=400, time=15 * 60))
print(M.xml())
