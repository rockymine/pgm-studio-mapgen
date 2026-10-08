"""Write Curio Square's map.xml from the plan, after the community's Hide n' Seek maps: hiders and seekers, the
seekers blinded in a glass cage over the fountain for twenty-five seconds, six plots vanishing every minute in one
of four random orders, the hiders winning if any is alive at seven minutes.

    python3 mapxml.py > map.xml
"""
import random
from xml.sax.saxutils import escape

import plan as P
import sketch
from gen import CAGE, Y

ORDERS = 4


def plot_regions():
    out = []
    for (i, j), (builder, row) in sorted(sketch.layout().items()):
        x0, z0 = P.origin(i, j)
        out.append((f"plot-{i}-{j}", row["name"] if row else "a plot", x0, z0, builder))
    return out


def main():
    o = []
    a = o.append
    plots = plot_regions()
    orders = []
    for k in range(ORDERS):
        ids = [p[0] for p in plots]
        random.Random(100 + k).shuffle(ids)
        orders.append(ids)
    names = {p[0]: p[1] for p in plots}
    cx0, cy0, cz0, cx1, cy1, cz1 = CAGE
    a('<map proto="1.5.0">')
    a('<name>Curio Square</name>')
    a('<version>1.0.0</version>')
    a('<objective>Hide from the seekers until the time runs out!</objective>')
    a('<gamemode>arcade</gamemode>')
    a('<rules><rule>Fall damage is disabled.</rule><rule>Hiders\' name tags are hidden.</rule>'
      '<rule>Every minute six of the fair\'s curiosities vanish.</rule></rules>')
    a('<teams>')
    a('    <team id="hiders" color="green" show-name-tags="false" max="50" plural="true">Hiders</team>')
    a('    <team id="seekers" color="dark aqua" max="3" max-overfill="3" plural="true">Seekers</team>')
    a('</teams>')
    a(f'<time result="hiders">{P.TIME}</time>')
    a('<blitz filter="only-hiders"/>')
    a('<kits>')
    a('    <kit id="seeker-blind"><effect>blindness</effect><game-mode>adventure</game-mode></kit>')
    a('    <kit id="seeker" force="true">')
    a('        <clear effects="true"/>')
    a('        <game-mode>adventure</game-mode>')
    a('        <item slot="0" material="iron sword" unbreakable="true" locked="true"/>')
    a('        <helmet material="diamond helmet" unbreakable="true" locked="true"/>')
    a('        <chestplate material="diamond chestplate" unbreakable="true" locked="true"/>')
    a('        <leggings material="diamond leggings" unbreakable="true" locked="true"/>')
    a('        <boots material="diamond boots" unbreakable="true" locked="true"/>')
    a('        <effect>speed</effect>')
    a('    </kit>')
    a('    <kit id="hider">')
    a('        <game-mode>adventure</game-mode>')
    a('        <item slot="0" material="compass" locked="true"/>')
    a('        <item material="potion" name="`rPotion of Invisibility `7(15s)"><effect duration="15s">invisibility</effect></item>')
    a('    </kit>')
    a('    <kit id="hider-potion" deduct-items="false">')
    a('        <item material="potion" name="`rPotion of Invisibility `7(15s)"><effect duration="15s">invisibility</effect></item>')
    a('    </kit>')
    for r in (1, 3, 5):
        a(f'    <give kit="hider-potion" filter="potion-{r}"/>')
    a('    <give kit="seeker" filter="seekers-out"/>')
    a('</kits>')
    a('<spawns>')
    a('    <spawn team="hiders" kit="hider" safe="true">')
    a('        <regions>')
    for x0, z0, x1, z1 in ((-8, -8, 8, -7), (-8, 7, 8, 8), (-8, -6, -7, 6), (7, -6, 8, 6)):
        a(f'            <cuboid min="{x0},{Y},{z0}" max="{x1 + 1},{Y + 1},{z1 + 1}"/>')
    a('        </regions>')
    a('    </spawn>')
    a(f'    <spawn team="seekers" kit="seeker-blind" filter="not(seekers-released)"><region><point>{P.CENTRE_X + 0.5},{cy0 + 1},{P.CENTRE_Z + 0.5}</point></region></spawn>')
    a(f'    <spawn team="seekers" kit="seeker" filter="seekers-released"><region><point>{P.CENTRE_X + 0.5},{Y},{P.CENTRE_Z + 7.5}</point></region></spawn>')
    a(f'    <default yaw="180" pitch="35"><region><point>{P.CENTRE_X + 0.5},{Y + 30},{P.CENTRE_Z + 60.5}</point></region></default>')
    a('</spawns>')
    a('<filters>')
    a('    <team id="only-hiders">hiders</team>')
    a('    <team id="only-seekers">seekers</team>')
    a(f'    <after id="seekers-released" duration="{P.RELEASE}s" filter="match-started" message="`3`lSeekers`r will be released in {{0}}"/>')
    a('    <all id="seekers-out"><filter id="seekers-released"/><team>seekers</team></all>')
    for k, t in enumerate(P.ROUNDS):
        a(f'    <time id="round-{k + 1}">{t}s</time>')
    for r in (1, 3, 5):
        a(f'    <all id="potion-{r}"><time>{P.ROUNDS[r - 1]}s</time><team>hiders</team></all>')
    a('    <deny id="not-players"><any><cause>player</cause><cause>explosion</cause></any></deny>')
    a('</filters>')
    a('<regions>')
    a(f'    <cuboid id="seeker-cage" min="{cx0},{cy0},{cz0}" max="{cx1 + 1},{cy1 + 1},{cz1 + 1}"/>')
    for rid, name, x0, z0, builder in plots:
        a(f'    <cuboid id="{rid}" min="{x0},{Y},{z0}" max="{x0 + P.PLOT},{Y + 24},{z0 + P.PLOT}"/>  <!-- {escape(name)}, {builder} -->')
    a(f'    <negative id="outside"><cuboid min="{-P.HALF},0,{-P.HALF}" max="{P.HALF + 1},256,{P.HALF + 1}"/></negative>')
    a('    <apply enter="never" region="outside" message="The fair is inside the walls!"/>')
    a('    <apply block="not-players"/>')
    a('</regions>')
    a('<variables>')
    a('    <variable id="order" scope="match" default="0"/>')
    a('</variables>')
    a('<actions>')
    a('    <action id="cage-clearer" scope="match"><fill region="seeker-cage" material="air"/></action>')
    a('    <trigger filter="seekers-released" action="cage-clearer" scope="match"/>')
    a('    <trigger scope="match" filter="always">')
    a(f'        <action><set var="order" value="floor(random() * {ORDERS})"/></action>')
    a('    </trigger>')
    for k, t in enumerate(P.ROUNDS):
        a(f'    <trigger scope="match" filter="round-{k + 1}">')
        a(f'        <action id="vanish-{k + 1}" scope="match">')
        a(f'            <message text="`6`l{P.PER_ROUND} curiosities have vanished!"/>')
        for n, ids in enumerate(orders):
            a(f'            <action filter="order={n}">')
            for rid in ids[k * P.PER_ROUND:(k + 1) * P.PER_ROUND]:
                a(f'                <fill region="{rid}" material="air"/>')
                a(f'                <message text="`7- {escape(names[rid])}"/>')
            a('            </action>')
        a('        </action>')
        a('    </trigger>')
    a('</actions>')
    a('<compass show-distance="true"><player filter="only-seekers" name="`3Closest Seeker"/></compass>')
    a('<broadcasts>')
    a(f'    <alert after="{P.RELEASE}s">Seekers have been released!</alert>')
    a(f'    <tip after="{P.RELEASE + 10}s">Every minute, six of the curiosities will vanish!</tip>')
    for t in P.ROUNDS:
        a(f'    <alert after="{t - 10}s">Six curiosities vanish in 10 seconds!</alert>')
    a('    <tip filter="only-hiders" after="5s">Your name tag is hidden from the seekers.</tip>')
    a('</broadcasts>')
    a('<disabledamage><damage>fall</damage></disabledamage>')
    a('<gamerules><doTileDrops>false</doTileDrops></gamerules>')
    a('<hunger><depletion>off</depletion></hunger>')
    a('<world><timeset>6000</timeset><timelock>on</timelock></world>')
    a('<itemremove><item>potion</item><item>glass bottle</item></itemremove>')
    a('</map>')
    print("\n".join(o))


if __name__ == "__main__":
    main()
