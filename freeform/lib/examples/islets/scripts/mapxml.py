"""Write Islets' map.xml: two teams, their spawns and the hill from the plan's objectives, and a kill height."""
from plan import KILL_Y, objectives
from pgmvox.play.rules import KillHeight, Map, Match, terrain_of

M = Map("Islets", "0.2.0", "Hold the middle hill.", "koth",
        terrain=terrain_of(__file__),
        objectives=objectives(),
        kill=KillHeight(KILL_Y),
        match=Match(score=300, time=600, fall_damage=False))
print(M.xml())
