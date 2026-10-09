"""Write Ocotillo's map.xml: four teams, their spawns and the five hills from the plan's objectives; the kit, with
sixteen leaves to bridge with; a leaf and a golden apple for every kill; the golden apples on the inner islands and
the arrows on the landings; building only over the board; the score and the time.
"""
import plan as P
from pgmvox.mapxml import Doc, E, item

O = P.objectives()
d = Doc("Ocotillo", "1.0.0", "Hold the hills: the Dais in the middle, and the islands between the spawns.", "koth")
d.add(E("authors", E("author", text="Claude (freeform generator, pgmvox)")))
O.write(d)                                    # teams, spawns, the hills (the Dais worth two), the observers' point

d.kit("spawn-kit",
      item("stone sword", 0, unbreakable=True), item("bow", 1, unbreakable=True),
      item("iron pickaxe", 2, unbreakable=True), item("leaves", 3, 16),
      item("cooked beef", 4, 8), item("arrow", 8, 16),
      item("leather helmet", unbreakable=True, team_color=True, tag="helmet"),
      item("leather chestplate", unbreakable=True, team_color=True, tag="chestplate"),
      item("leather leggings", unbreakable=True, team_color=True, tag="leggings"),
      item("leather boots", unbreakable=True, team_color=True, tag="boots"))

# building: only over a column carrying block 36 at y 0, which lies under the board and its gaps
d.filter("not-void", E("not", E("void")))
d.apply(block_place="not-void", message="You may not build in the void!")
d.add(E("itemkeep", [E("item", text=m) for m in ("stone sword", "bow", "iron pickaxe")]))
d.add(E("kill-rewards", E("kill-reward", E("item", material="leaves", amount=1), E("item", material="golden apple"))))


def spawner(rid, x, z, y, material, amount, delay, most):
    """A spawner over (x, z) on the floor at y - 1: its items drop in the block over the spot, and it runs only
    while a player stands within four blocks of it."""
    d.region(rid, E("cuboid", min=f"{x - 0.5},{y},{z - 0.5}", max=f"{x + 1.5},{y + 2},{z + 1.5}"))
    d.region(f"{rid}-near", E("cuboid", min=f"{x - 4},{y},{z - 4}", max=f"{x + 5},{y + 4},{z + 5}"))
    return E("spawner", E("item", material=material, amount=amount), spawn_region=rid,
             player_region=f"{rid}-near", delay=delay, max_entities=most)


spawners = [spawner(f"apples-{k}", x, z, P.LEVEL[2] + 1, "golden apple", 1, "30s", 1)
            for k, (x, z) in enumerate(P.APPLES)]
spawners += [spawner(f"arrows-{k}", x, z, P.LEVEL[1] + 1, "arrow", 4, "10s", 8)
             for k, (x, z) in enumerate(P.ARROWS)]
d.add(E("spawners", *spawners))
d.child("score").append(E("limit", text=400))
d.add(E("time", text="15m"))
d.add(E("maxbuildheight", text=P.MAX_BUILD))
print(d.tostring())
