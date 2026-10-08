"""Write Lantern Karst's map.xml. The teams, their spawns, the observer point, the four wools with their
monuments and the rule that keeps a team out of its own rooms come from the plan's objectives; the rest of a
capture board's rules are written here with mapxml.E, since the library does not carry them: the kit, the wool
spawners, the rooms' block protection, the spawn's iron, the void filter, the build height.
"""
import plan  # noqa: F401  (puts the library on the path)
from plan import KILL_Y, MAX_BUILD, objectives
from pgmvox.mapxml import Doc, E, point
from pgmvox.objectives import DYES, Spawn, Wool

O = objectives()
d = Doc("Lantern Karst", "0.2.0", "Capture the enemy's two wools: the Pillar Shrine's and the Tea Store's.", "ctw")
d.add(E("authors", E("author", text="Claude (freeform generator, ported onto pgmvox)")))
O.write(d)                                       # teams, team filters, spawns, monuments, wools, rooms' entry rule

# the kit every spawn names, and the fall
d.add(E("kits", E("kit",
                  E("item", slot=0, material="iron sword", unbreakable=True),
                  E("item", E("enchantment", text="infinity", level=1), slot=1, material="bow", unbreakable=True),
                  E("item", E("enchantment", text="efficiency", level=1), slot=2, material="iron pickaxe",
                    unbreakable=True),
                  E("item", E("enchantment", text="efficiency", level=1), slot=3, material="iron axe",
                    unbreakable=True),
                  E("item", slot=4, material="wood", damage=1, amount=64),
                  E("item", slot=5, material="stained clay", amount=48, team_color=True),
                  E("item", slot=6, material="golden apple"),
                  E("item", slot=7, material="water bucket"),
                  E("item", slot=8, material="cooked beef", amount=16),
                  E("item", slot=28, material="arrow"),
                  E("item", slot=29, material="shears", unbreakable=True),
                  E("item", slot=31, material="wood", damage=1, amount=64),
                  E("helmet", material="leather helmet", unbreakable=True, team_color=True),
                  E("chestplate", material="leather chestplate", unbreakable=True, team_color=True),
                  E("leggings", material="chainmail leggings", unbreakable=True),
                  E("boots", material="leather boots", unbreakable=True, team_color=True),
                  id="spawn-kit")))
d.kill_below(KILL_Y)

# the spawns: kept to their team, and nothing edited in them but the iron, which grows back
spawns = [o for o in O.of(Spawn)]
d.region("spawns", E("union", *[E("region", id=f"{O.teams.short(s.team)}-spawn") for s in spawns]))
for s in spawns:
    t = O.teams.short(s.team)
    d.apply(enter=f"only-{t}", region=f"{t}-spawn", message="You may not enter the enemy's spawn!")
d.filter("only-iron", E("material", text="iron block"))
d.filter("only-iron-cause-world", E("all", E("material", text="iron block"), E("cause", text="world")))
d.apply(block_place="only-iron-cause-world", block_break="only-iron", region="spawns",
        message="You may not edit the spawn!")
d.add(E("renewables", E("renewable", region="spawns", renew_filter="only-iron")))

# the rooms: each team's two in one union, their blocks kept but for what an attacker brings in
d.filter("woolroom-materials", E("any", E("material", text="wood"), E("material", text="stained clay"),
                                 E("material", text="web"),
                                 E("all", E("cause", text="player"),
                                   E("any", E("material", text="water"), E("material", text="stationary water")))))
spawners = []
for keeper in ("red-team", "blue-team"):
    t = O.teams.short(keeper)
    rooms = [o for o in O.of(Wool) if o.team != keeper]           # the wools the other team captures
    d.region(f"{t}s-woolrooms", E("union", *[E("region", id=f"{o.color}-room") for o in rooms]))
    d.filter(f"{t}s-woolrooms-filter", E("all", E("filter", id=f"not-{t}"), E("filter", id="woolroom-materials")))
    d.apply(block=f"{t}s-woolrooms-filter", region=f"{t}s-woolrooms", message="You may not edit the wool room!")
    for o in rooms:
        x, y, z = o.found
        d.region(f"{o.color}-wool-spawn", point(x + 0.5, y + 1, z + 2.5))
        spawners.append(E("spawner", E("item", material="wool", damage=DYES[o.color]),
                          spawn_region=f"{o.color}-wool-spawn", player_region=f"{o.color}-room", delay="1.5s"))
d.add(E("spawners", spawners))

# building: only over a column carrying block 36 at y 0, and no higher than the build height
d.filter("not-void", E("not", E("void")))
d.apply(block_place="not-void", message="You may not build in the void!")
d.add(E("itemkeep", [E("item", text=m) for m in ("iron sword", "bow", "iron pickaxe", "iron axe", "water bucket",
                                                  "shears")]))
d.add(E("kill-rewards", E("kill-reward", E("item", material="wood", damage=1, amount=16),
                          E("item", material="golden apple"))))
d.add(E("maxbuildheight", text=MAX_BUILD))
print(d.tostring())
