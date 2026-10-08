"""Write Islets' map.xml: two teams, their spawns and the hill from the plan's objectives, and a kill height."""
from plan import KILL_Y, objectives
from pgmvox.mapxml import Doc

d = Doc("Islets", "0.2.0", "Hold the middle hill.", "koth")
objectives().write(d, limit=300)
d.kill_below(KILL_Y)
d.time(600)
d.no_fall_damage()
print(d.tostring())
