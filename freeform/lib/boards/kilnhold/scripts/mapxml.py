"""Write Kilnhold's map.xml: destroy both of the enemy's monuments and carry the enemy's flag home. Teams of sixteen,
two monuments and a flag each, the spawn in the muster hall, a net on each team's gate-hall dais, the kit the
genre uses, no building over the void, a build height over the Crown, a kill height under the caldera.

    python3 mapxml.py > map.xml
"""
import plan as P
from pgmvox.play.mapxml import E
from pgmvox.play.rules import Build, Effect, Item, KillHeight, Kit, Map, Match, Respawn, terrain_of


class CtfRules:
    """The parts of capture the flag the library's Flag does not write: each flag may be picked up by everyone but
    its own team, and each team has a net, a box over its dais, that takes the other team's flag."""

    def __init__(self, nets):
        self.nets = nets

    def write(self, doc):
        flags = doc.child("flags")
        for flag in flags.findall("flag"):
            owner = flag.get("owner")
            if owner:
                flag.set("pickup-filter", "not-" + P.TEAMS.short(owner))
        for team, flag_id, box in self.nets:
            short = P.TEAMS.short(team)
            rid = doc.region(f"{short}-net-region", box.cuboid())
            flags.append(E("net", id=f"{short}-net", owner=team, points=1, flags=flag_id, region=rid))


M = Map("Kilnhold", "0.1.0",
        "Destroy the monuments of the enemy bunker, and carry its flag back to your own gate hall.",
        ["dtm", "ctf"],
        terrain=terrain_of(__file__),
        authors=["Claude Sonnet 5.5 (freeform generator, on pgmvox)"],
        objectives=P.objectives(),
        kit=Kit(
            Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
            Item("diamond pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True),
            Item("wood", 4, 64), Item("stained clay", 5, 32, team_color=True), Item("golden apple", 6, 2),
            Item("water bucket", 7), Item("cooked beef", 8, 16), Item("arrow", 28),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("iron chestplate", unbreakable=True, wear="chestplate"),
            Item("chainmail leggings", unbreakable=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        kits=[Kit(id="carrier", force=True, effects=[Effect("absorption", "3s", 2)])],
        build=Build(max_height=96, message="You cannot build there!"),
        kill=KillHeight(y=16),
        match=Match(score=3, time=2400, result="objectives", time_of_day=12000,
                    respawn=Respawn("3s", auto=True, spectate=True)),
        parts=[CtfRules(P.net_boxes())])
print(M.xml())
