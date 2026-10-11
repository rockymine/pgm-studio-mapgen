"""Write Islets' map.xml: two teams, their spawns and the hill from the plan's objectives, and a kill height."""
from plan import KILL_Y, objectives
from pgmvox.play.rules import KillHeight, Map, Match

M = Map("Islets", "0.2.0", "Hold the middle hill.", "koth",
        objectives=objectives(),
        kill=KillHeight(KILL_Y, "portal"),
        match=Match(score=300, time=600, fall_damage=False))
print(M.xml())
