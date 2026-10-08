"""Write Copperline's map.xml from the plan and the generator, so no coordinate in it is typed twice: the payloads'
locations are the legs' first rails, the gates are the generator's barred doorways, the spawns and their rooms
are the plan's.

    python3 mapxml.py > map.xml

The payload module is an experiment in PGM: a server loads this map only with `experiments.payload: true`.
"""
import gen as G
import plan as P

ROOMS = {"attackers": ["engine-shed", "station", "depot"], "defenders": ["office", "bunkhouse", "lamp-room"]}
YAW = {"attackers": {"1": 90, "2": -90, "3": 90}, "defenders": {"1": 90, "2": 90, "3": 0}}
FILTER = {"1": "first-leg", "2": "second-leg", "3": "third-leg"}


def spawn_region(name):
    x0, x1, z0, z1 = P.BUILDINGS[name]["box"]
    y = P.BUILDINGS[name]["floor"] + 1
    if name == "engine-shed":                                        # the north half: the engine stands in the south
        z1 = (z0 + z1) // 2 + 1
    return f'<cuboid min="{x0 + 2},{y},{z0 + 2}" max="{x1 - 1},{y + 1},{z1 - 1}"/>'


def main():
    o = []
    a = o.append
    a('<map proto="1.5.0">')
    a('<name>Copperline</name>')
    a('<version>1.0.0</version>')
    a('<objective>Attackers push the ore cart up the line to the mine in three legs; defenders stop it until the clock runs out.</objective>')
    a('<gamemode>payload</gamemode>')
    a('<!-- needs experiments.payload: true in the PGM config -->')
    a(f'<time result="defenders">{P.TIME}</time>')
    a('<teams>')
    a('    <team id="attackers" color="dark red" max="12">Attackers</team>')
    a('    <team id="defenders" color="blue" max="12">Defenders</team>')
    a('</teams>')
    a('<broadcasts>')
    a(f'    <alert after="2s" filter="attackers">Push the ore cart up the line to the mine. The shed opens in {P.WARMUP}.</alert>')
    a('    <alert after="2s" filter="defenders">Stop the ore cart before it reaches the mine. Stand by it to hold it still.</alert>')
    a('</broadcasts>')
    a('<kits>')
    a('    <kit id="spawn-kit">')
    a('        <clear/>')
    a('        <item slot="0" unbreakable="true" material="stone sword"/>')
    a('        <item slot="1" unbreakable="true" material="bow"/>')
    a('        <item slot="2" material="golden apple"/>')
    a('        <helmet unbreakable="true" team-color="true" material="leather helmet"/>')
    a('        <chestplate unbreakable="true" team-color="true" material="leather chestplate"/>')
    a('        <leggings unbreakable="true" material="chainmail leggings"/>')
    a('        <boots unbreakable="true" material="iron boots"/>')
    a('        <effect duration="3s" amplifier="255">resistance</effect>')
    a('        <game-mode>adventure</game-mode>')
    a('    </kit>')
    a('    <kit id="attacker-kit" parent="spawn-kit"><item slot="8" amount="20" material="arrow"/></kit>')
    a('    <kit id="defender-kit" parent="spawn-kit"><item slot="8" amount="16" material="arrow"/></kit>')
    a('</kits>')
    a('<spawns>')
    a('    <default><region yaw="180"><point>0.5,70,20.5</point></region></default>')
    for team in ("attackers", "defenders"):
        kit = "attacker-kit" if team == "attackers" else "defender-kit"
        a(f'    <spawns team="{team}" kit="{kit}">')
        for stage, room in zip(("1", "2", "3"), ROOMS[team]):
            a(f'        <spawn filter="{FILTER[stage]}"><region yaw="{YAW[team][stage]}">{spawn_region(room)}</region></spawn>')
        a('    </spawns>')
    a('</spawns>')
    ids = [leg["id"] for leg in P.LEGS]
    a('<filters>')
    a(f'    <after id="warmup-over" duration="{P.WARMUP}"><match-started/></after>')
    a(f'    <not id="first-leg"><completed>{ids[0]}</completed></not>')
    a(f'    <all id="second-leg"><completed id="a-done">{ids[0]}</completed><not><completed>{ids[1]}</completed></not></all>')
    a(f'    <all id="third-leg"><completed>{ids[0]}</completed><completed id="b-done">{ids[1]}</completed></all>')
    a('</filters>')
    a('<actions>')
    a('    <message id="a-message" text="`6The cart is at the station. `fSpawns move up the line."/>')
    a('    <message id="b-message" text="`6The cart is over the gorge. `fSpawns move up the line."/>')
    a('    <trigger filter="a-done" trigger="a-message" scope="match"/>')
    a('    <trigger filter="b-done" trigger="b-message" scope="match"/>')
    for stage, filt in (("warmup", "warmup-over"), ("A", "a-done"), ("B", "b-done")):
        a(f'    <trigger scope="match" filter="{filt}"><action><fill region="gate-{stage.lower()}" material="air"/></action></trigger>')
    a('</actions>')
    radius = P.RADIUS
    a(f'<payloads permanent="true" radius="{radius}" capture-filter="attackers" capture-time="{P.CAPTURE}" decay-rate="0.1" '
      f'recovery-rate="0.5" contested-rate="0" time-multiplier="0.1">')
    for n, leg in enumerate(P.LEGS):
        x, z, hh = leg["pts"][0]
        pf = '' if n == 0 else f' player-filter="{["a-done", "b-done"][n - 1]}"'
        a(f'    <payload id="{leg["id"]}" name="{leg["name"]}" location="{x},{hh + 1},{z}"{pf} display-filter="{FILTER[str(n + 1)]}"/>')
    a('</payloads>')
    a('<regions>')
    for stage, boxes in G.GATE_REGIONS.items():
        a(f'    <union id="gate-{stage.lower()}">')
        for x0, y0, z0, x1, y1, z1 in boxes:
            a(f'        <cuboid min="{x0},{y0},{z0}" max="{x1 + 1},{y1 + 1},{z1 + 1}"/>')
        a('    </union>')
    for team, rooms in ROOMS.items():
        a(f'    <union id="{team}-rooms">')
        for name in rooms:
            x0, x1, z0, z1 = P.BUILDINGS[name]["box"]
            a(f'        <cuboid min="{x0},0,{z0}" max="{x1 + 1},oo,{z1 + 1}"/>')
        a('    </union>')
    a('    <apply block="never" use="never"/>')
    a('    <apply enter="attackers" region="defenders-rooms" message="You may not enter the defenders\' spawn!"/>')
    a('    <apply enter="defenders" region="attackers-rooms" message="You may not enter the attackers\' spawn!"/>')
    a('</regions>')
    a('<itemremove><item>leather helmet</item><item>leather chestplate</item><item>chainmail leggings</item>'
      '<item>iron boots</item></itemremove>')
    a('<itemkeep><item>stone sword</item><item>bow</item></itemkeep>')
    a('<kill-rewards><kill-reward><item amount="4" material="arrow"/></kill-reward></kill-rewards>')
    a('<respawns><respawn delay="5s" filter="attackers"/><respawn delay="7s" filter="defenders"/></respawns>')
    a('<hunger><depletion>off</depletion></hunger>')
    a('</map>')
    print("\n".join(o))


if __name__ == "__main__":
    main()
