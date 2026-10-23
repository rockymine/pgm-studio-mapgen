"""Write Saltgate's map.xml from the plan: attack and defence in three stages for two teams of sixteen. The attackers
take the Sea Gate, blow both powder stores and carry the city's banner down to the Sea Gate; the defenders hold for
fifteen minutes. Each stage that falls opens its gates and moves both teams' spawns up; only the stores' obsidian
and the banner may be broken, and nothing placed but the banner in its slot.

    python3 mapxml.py > map.xml
"""


import plan as P  # noqa: E402
from pgmvox.play.logic import (After, All, Completed, ControlPoint, Fill, MatchStarted, Message, Named,  # noqa: E402
                               Not, Ref, Trigger)
from pgmvox.play.objectives import Box, Destroyable, Objectives, Observer, Spawn, Teams, Wool  # noqa: E402
from pgmvox.play.rules import Build, Effect, Item, Kit, Map, Match, Respawn, Zone, terrain_of  # noqa: E402

KITS = {"attackers": "attacker-kit", "defenders": "defender-kit"}
STAGE_FILTER = {"1": "stage-1", "2": "stage-2", "3": "stage-3"}
COLOURS = {10: "purple"}

O = Objectives(Teams(("attackers", "Attackers", "red", 16), ("defenders", "Defenders", "blue", 16)))
O.add(Observer((0, 50, -41)))
for team, stages in P.SPAWNS.items():
    for stage, (x, y, z, yaw) in stages.items():
        O.add(Spawn(team, (int(x - 0.5), y, int(z - 0.5)), yaw=yaw, kit=KITS[team], filter=STAGE_FILTER[stage]))
c = P.CONTROL
x0, x1, z0, z1 = c["box"]
O.add(ControlPoint(c["key"], c["name"], Box(x0, c["y"], z0, x1, c["y"] + 5, z1),
                   progress=Box(x0, c["y"], z0, x1, c["y"], z1), capture_time="15s", capture_filter="only-attackers",
                   initial_owner="defenders", permanent=True, show_progress=True))
for m in P.MAGAZINES:
    O.add(Destroyable(f"{m['key']}-store", m["name"].replace("the ", "").title(), "defenders",
                      Box(*m["monument"], m["monument"][0], m["monument"][1] + 1, m["monument"][2])))
O.add(Wool("attackers", COLOURS[P.WOOL["colour"]], P.WOOL["monument"], found=P.WOOL["at"], spawner=False,
           open_slot=True, renew=True))
O.add(Zone("posterns", [Box(x, 30, 23, x + 1, 35, 25) for x in (36, -38)], enter="defenders",
           enter_message="Only the defenders know the postern's key."))
O.add(Zone("flagship", [Box(-6, 24, -66, 5, 39, -56)], enter="attackers",
           enter_message="You may not board the enemy's flagship!"))

GATES = {stage: [Box(*b) for b in boxes] for stage, boxes in P.GATE_REGIONS.items()}
LOGIC = [
    Named("warmup-over", After(P.WARMUP, MatchStarted())),
    Named("sea-gate-taken", Completed(c["key"])),
    Named("stores-blown", All(*[Completed(f"{m['key']}-store") for m in P.MAGAZINES])),
    Named("stage-1", Not(Ref("sea-gate-taken"))),
    Named("stage-2", All(Ref("sea-gate-taken"), Not(Ref("stores-blown")))),
    Named("stage-3", All(Ref("sea-gate-taken"), Ref("stores-blown"))),
    Trigger("warmup-over", [Fill(GATES["warmup"])]),
    Trigger("sea-gate-taken", [Fill(GATES["A"]), Message(
        "`c`lThe Sea Gate has fallen! `7The powder stores' doors are open and the spawns move up.")]),
    Trigger("stores-blown", [Fill(GATES["B"]), Message(
        "`c`lBoth powder stores are blown! `7The citadel's gate and the keep's doors are open.")]),
]

BASE = Kit(Item("iron sword", 0, unbreakable=True), Item("bow", 1, unbreakable=True), Item("golden apple", 2, 2),
           Item("cooked beef", 3, 16),
           Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
           Item("chainmail chestplate", unbreakable=True, wear="chestplate"),
           Item("iron leggings", unbreakable=True, wear="leggings"),
           Item("iron boots", unbreakable=True, enchant=[("feather_falling", 2)], wear="boots"),
           id="base-kit", clear=True, effects=[Effect("resistance", "3s", 255)], game_mode="survival",
           reward=[Item("arrow", amount=4)])
ATTACKER = Kit(Item("diamond pickaxe", 4, unbreakable=True, enchant=[("efficiency", 2)]), Item("arrow", 8, 24),
               id="attacker-kit", parents=[BASE])
DEFENDER = Kit(Item("arrow", 8, 40), id="defender-kit", parents=[BASE])

M = Map("Saltgate", "0.1.0", "Attackers: take the Sea Gate, blow both powder stores, and carry the city's banner down "
        "to the Sea Gate. Defenders: hold out for 15 minutes.", "ad",
        terrain=terrain_of(__file__),
        authors=["Claude (freeform generator)"], includes=[],
        objectives=O, kit=BASE, kits=[ATTACKER, DEFENDER], parts=LOGIC,
        build=Build(breakable=("obsidian", f"wool:{P.WOOL['colour']}"), message="The town's stones will not move."),
        match=Match(time=P.TIME, result="defenders", respawn=Respawn("4s"), time_of_day=3000,
                    broadcasts=[("tip", 2, f"Your gangplanks open after {P.WARMUP[:-1]} seconds. Take the Sea Gate!",
                                 "only-attackers"),
                                ("tip", 2, f"Man the sea wall. The attackers land in {P.WARMUP[:-1]} seconds.",
                                 "only-defenders")]))
print(M.xml())
