"""Write Islets' map.xml: two teams, one hill, a kill height."""
from plan import KILL_Y
from pgmvox.mapxml import Doc, E, cuboid, point

d = Doc("Islets", "0.1.0", "Hold the middle hill.", "koth")
d.teams(("red", "red", 8, "Red"), ("blue", "blue", 8, "Blue"))
d.spawns(E("spawn", E("region", point(-23, 31, 0, yaw=-90)), team="red"),
         E("spawn", E("region", point(23, 31, 0, yaw=90)), team="blue"), default=point(0.5, 50, 20.5))
d.add(E("control-points", E("control-point", id="hill", name="the Hill", capture=None,
                            **{"capture-region": None}), capture_time="5s"))
d.root[-1][0].append(E("captured", cuboid((-2, 33, -4), (2, 36, 4))))
d.kill_below(KILL_Y)
d.time(600)
d.no_fall_damage()
print(d.tostring())
