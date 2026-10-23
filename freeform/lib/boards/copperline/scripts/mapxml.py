"""Write Copperline's map.xml from the plan, so no coordinate in it is typed twice: the payloads' locations are the
legs' first rails, the gates are the plan's barred doorways, the spawns and their rooms are the plan's buildings.
Attackers push the ore cart up the line in three legs; each leg pushed opens its gates and moves both teams' spawns
up; the defenders win at the clock.

    python3 mapxml.py > map.xml

The payload module is an experiment in PGM: a server loads this map only with `experiments.payload: true`.
"""


import plan as P  # noqa: E402
from pgmvox.play.logic import (After, All, Completed, Fill, MatchStarted, Message, Named, Not, Payload,  # noqa: E402
                               Payloads, Ref, Trigger)
from pgmvox.play.objectives import Box, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.play.rules import Build, Effect, Item, Kit, Map, Match, Respawn, Zone, terrain_of  # noqa: E402

ROOMS = {"attackers": ["engine-shed", "station", "depot"], "defenders": ["office", "bunkhouse", "lamp-room"]}
YAW = {"attackers": [90, -90, 90], "defenders": [90, 90, 0]}
KITS = {"attackers": "attacker-kit", "defenders": "defender-kit"}
LEG_FILTER = ["first-leg", "second-leg", "third-leg"]
DONE = ["a-done", "b-done"]


def spawn_box(name):
    """The room's floor less a two-block margin; the engine shed's north half, the engine standing in the south."""
    b = P.BUILDINGS[name]
    x0, x1, z0, z1 = b["box"]
    if name == "engine-shed":
        z1 = (z0 + z1) // 2 + 1
    return Box(x0 + 2, b["floor"] + 1, z0 + 2, x1 - 2, b["floor"] + 1, z1 - 2)


O = Objectives(Teams(("attackers", "Attackers", "dark red", 12), ("defenders", "Defenders", "blue", 12)))
O.add(Observer((0, 70, 20), yaw=180))
for team, rooms in ROOMS.items():
    for k, room in enumerate(rooms):
        O.add(Spawn(team, yaw=YAW[team][k], kit=KITS[team], filter=LEG_FILTER[k], spread=spawn_box(room)))
    who = "defenders'" if team == "defenders" else "attackers'"
    O.add(Zone(f"{team}-rooms", [Box(x0, 0, z0, x1, 255, z1) for x0, x1, z0, z1 in
                                 (P.BUILDINGS[r]["box"] for r in rooms)],
               enter=team, enter_message=f"You may not enter the {who} spawn!"))
for n, leg in enumerate(P.LEGS):
    x, z, h = leg["pts"][0]
    O.add(Payload(leg["id"], leg["name"], (x, h + 1, z), player_filter=DONE[n - 1] if n else None,
                  display_filter=LEG_FILTER[n]))

ids = [leg["id"] for leg in P.LEGS]
GATES = {stage: [Box(*b) for b in boxes] for stage, boxes in P.GATE_REGIONS.items()}
LOGIC = [
    Payloads("only-attackers", capture_time=P.CAPTURE, radius=P.RADIUS),
    Named("warmup-over", After(P.WARMUP, MatchStarted())),
    Named("a-done", Completed(ids[0])),
    Named("b-done", Completed(ids[1])),
    Named("first-leg", Not(Ref("a-done"))),
    Named("second-leg", All(Ref("a-done"), Not(Ref("b-done")))),
    Named("third-leg", All(Ref("a-done"), Ref("b-done"))),
    Trigger("warmup-over", [Fill(GATES["warmup"])]),
    Trigger("a-done", [Fill(GATES["A"]), Message("`6The cart is at the station. `fSpawns move up the line.")]),
    Trigger("b-done", [Fill(GATES["B"]), Message("`6The cart is over the gorge. `fSpawns move up the line.")]),
]

SPAWN_KIT = Kit(Item("stone sword", 0, unbreakable=True), Item("bow", 1, unbreakable=True), Item("golden apple", 2),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, wear="leggings"),
                Item("iron boots", unbreakable=True, wear="boots"),
                clear=True, effects=[Effect("resistance", "3s", 255)], game_mode="adventure",
                reward=[Item("arrow", amount=4)])

M = Map("Copperline", "1.0.0", "Attackers push the ore cart up the line to the mine in three legs; defenders stop it "
        "until the clock runs out.", "payload",
        terrain=terrain_of(__file__), authors=["Claude (freeform generator)"], includes=[],
        objectives=O, kit=SPAWN_KIT, parts=LOGIC,
        kits=[Kit(Item("arrow", 8, 20), id="attacker-kit", parents=[SPAWN_KIT]),
              Kit(Item("arrow", 8, 16), id="defender-kit", parents=[SPAWN_KIT])],
        build=Build(never=True, use=False),
        match=Match(time=P.TIME, result="defenders",
                    respawn=[Respawn("5s", filter="only-attackers"), Respawn("7s", filter="only-defenders")],
                    broadcasts=[("alert", 2, "Push the ore cart up the line to the mine. The shed opens in "
                                 f"{P.WARMUP}.", "only-attackers"),
                                ("alert", 2, "Stop the ore cart before it reaches the mine. Stand by it to hold it "
                                 "still.", "only-defenders")]))
print(M.xml())
