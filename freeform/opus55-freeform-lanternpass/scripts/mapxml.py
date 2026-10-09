"""Write Lantern Pass's map.xml from the plan and the generator: the bell's region, the shrine, the side-swap rows,
the warm-up gate and the spawns are the plan's own numbers.

    python3 mapxml.py > map.xml
"""
import gen as G
import plan as P


def main():
    o = []
    a = o.append
    lx0, lx1 = P.LANE
    bx0, bx1, bz0, bz1 = P.BELL["box"]
    hx0, hx1, hz0, hz1 = P.HEAL["box"]
    L, Rw = P.WALKS["left"], P.WALKS["right"]
    a('<map proto="1.5.0">')
    a('<name>Lantern Pass</name>')
    a('<version>1.0.0</version>')
    a('<objective>Runners: reach the temple and hold the bell for two seconds. Shooters: stop every runner before the clock runs out.</objective>')
    a('<gamemode>arcade</gamemode>')
    a('<gamemode>blitz</gamemode>')
    a('<rules><rule>Fall damage is off. Runners have one life.</rule><rule>Shooters: step on the yellow row to cross to the other walkway.</rule></rules>')
    a(f'<time result="shooters">{P.TIME}</time>')
    a('<teams>')
    a('    <team id="runners" color="light purple" max="25" max-overfill="30" plural="true">Runners</team>')
    a('    <team id="shooters" color="dark blue" max="4" plural="true">Shooters</team>')
    a('</teams>')
    a('<kits>')
    a('    <kit id="fed"><saturation>20</saturation><foodlevel>20</foodlevel></kit>')
    a('    <kit id="runner-kit" parents="fed">')
    a('        <clear/>')
    a('        <helmet color="E07AAE" material="leather helmet"/><chestplate color="E07AAE" material="leather chestplate"/>')
    a('        <leggings color="E07AAE" material="leather leggings"/><boots color="FFFFFF" material="leather boots"/>')
    a('        <effect duration="oo">speed</effect>')
    a('    </kit>')
    a('    <kit id="shooter-kit" parents="fed">')
    a('        <clear/>')
    a('        <helmet color="1D2A5C" material="leather helmet"/><chestplate color="1D2A5C" material="leather chestplate"/>')
    a('        <leggings color="1D2A5C" material="leather leggings"/><boots color="111111" material="leather boots"/>')
    a('        <item slot="0" unbreakable="true" enchantment="ARROW_DAMAGE:3;ARROW_KNOCKBACK:1;ARROW_INFINITE" material="bow"/>')
    a('        <item slot="28" material="arrow"/>')
    a('        <effect duration="oo" amplifier="1">speed</effect>')
    a('    </kit>')
    a('    <kit id="heal"><health>20</health></kit>')
    a('</kits>')
    a('<spawns>')
    a('    <default><region yaw="0"><point>0.5,70,-20.5</point></region></default>')
    a(f'    <spawn team="runners" kit="runner-kit"><region yaw="0"><cuboid min="{lx0 + 4},21,-8" max="{lx1 - 3},21,3"/></region></spawn>')
    hw = int(G.HW[P.iz(-6)]) + 1
    # two ledges, two point providers: PGM draws a spawn from one of a spawn's regions at random, and cannot draw a
    # random point inside a union
    a(f'    <spawn team="shooters" kit="shooter-kit">'
      f'<region yaw="0"><cuboid min="{L[0] + 1},{hw},-8" max="{L[1] + 1},{hw},-4"/></region>'
      f'<region yaw="0"><cuboid min="{Rw[0]},{hw},-8" max="{Rw[1]},{hw},-4"/></region></spawn>')
    a('</spawns>')
    a('<filters>')
    a('    <team id="only-runners">runners</team>')
    a(f'    <after id="warmup-over" duration="{P.WARMUP}"><match-started/></after>')
    a('</filters>')
    a('<blitz filter="only-runners"><lives>1</lives><broadcastLives>true</broadcastLives></blitz>')
    a('<control-points>')
    a(f'    <control-point id="the-bell" name="The Bell" capture-time="2s" capture-filter="only-runners" '
      f'capture="bell" progress="bell" captured="bell"/>')
    a('</control-points>')
    a('<regions>')
    a(f'    <cuboid id="bell" min="{bx0},{P.BELL["y"]},{bz0}" max="{bx1 + 1},{P.BELL["y"] + 3},{bz1 + 1}"/>')
    a(f'    <cuboid id="shrine" min="{hx0},33,{hz0}" max="{hx1 + 1},36,{hz1 + 1}"/>')
    a(f'    <cuboid id="boathouse" min="{lx0 + 3},20,-9" max="{lx1 - 2},28,4"/>')
    for stage, boxes in G.GATE_REGIONS.items():
        x0, y0, z0, x1, y1, z1 = boxes[0]
        a(f'    <cuboid id="gate-{stage}" min="{x0},{y0},{z0}" max="{x1 + 1},{y1 + 1},{z1 + 1}"/>')
    a(f'    <cuboid id="swap-left" min="{L[0]},0,{P.Z_MIN + 2}" max="{L[0] + 1},oo,{P.Z_MAX - 1}"/>')
    a(f'    <cuboid id="swap-right" min="{Rw[1]},0,{P.Z_MIN + 2}" max="{Rw[1] + 1},oo,{P.Z_MAX - 1}"/>')
    a('    <apply block="never" use="never"/>')
    a('    <apply region="shrine" kit="heal"/>')
    a('    <apply region="boathouse" enter="never" message="You may not go back into the boathouse!"/>')
    a('</regions>')
    a('<actions>')
    a('    <trigger scope="match" filter="warmup-over"><action><fill region="gate-warmup" material="air"/></action></trigger>')
    a('</actions>')
    a('<portals>')
    a(f'    <portal x="{P.SWAP_DX["left"]}" y="0" z="0" region="swap-left"/>')
    a(f'    <portal x="{P.SWAP_DX["right"]}" y="0" z="0" region="swap-right"/>')
    a('</portals>')
    a('<disabledamage><damage>fall</damage></disabledamage>')
    a('<hunger><depletion>off</depletion></hunger>')
    a('<itemremove><item>arrow</item><item>bow</item><item>leather helmet</item><item>leather chestplate</item>'
      '<item>leather leggings</item><item>leather boots</item></itemremove>')
    a('</map>')
    print("\n".join(o))


if __name__ == "__main__":
    main()
