"""Write Spark's map.xml from the plan, after Knockout Stick Fight's: a knockback stick that steps up on a clock,
three seconds' protection at the start, nothing that hurts but the void, one life each.

    python3 mapxml.py > map.xml
"""
import math

import plan as P

NAMES = {1: "`r`lKnockback 1 Stick", 2: "`r`a`lKnockback 2 Stick", 3: "`r`e`lKnockback 3 Stick",
         10: "`r`c`lKnockback 10 Stick"}


def spawn_points():
    """One point at the foot of every ray, facing out along it, on the ring round the hub's eye."""
    pts = []
    for a, length, w0, w1 in P.RAYS:
        t = math.radians(a)
        x, z = P.SPAWN_R * math.cos(t), P.SPAWN_R * math.sin(t)
        bx, bz = math.floor(x), math.floor(z)
        if P.crate_at(bx, bz) or not P.is_floor(bx, bz):
            continue
        yaw = (a - 90) % 360                                     # Minecraft yaw: 0 faces south, 90 west
        pts.append((bx + 0.5, bz + 0.5, round(yaw - 360 if yaw > 180 else yaw)))
    return pts


def main():
    o = []
    a = o.append
    y = P.FLOOR_Y + 1
    a('<map proto="1.5.0">')
    a('<name>Spark</name>')
    a('<version>1.0.0</version>')
    a('<objective>Knock the other players off the spark and be the last one standing!</objective>')
    a('<gamemode>blitz</gamemode>')
    a('<rules><rule>Players can only die to the void.</rule>'
      '<rule>Your stick gets stronger at one, two and four minutes.</rule></rules>')
    a('<players min="2" max="64" colors="true"/>')
    a('<broadcasts>')
    for t, level in P.LEVELS[1:]:
        a(f'    <alert after="{t // 60}m">Your sticks are now knockback {level}!</alert>')
    a('</broadcasts>')
    a('<kits>')
    a('    <kit id="stick">')
    a(f'        <item slot="0" material="stick" name="{NAMES[1]}"><enchantment>knockback</enchantment></item>')
    a('        <effect amplifier="255" duration="3s">damage resistance</effect>')
    a('        <effect amplifier="255" duration="1s">slowness</effect>')
    a('        <effect>regeneration</effect>')
    a('        <knockback-reduction>0.9</knockback-reduction>')
    a('        <game-mode>adventure</game-mode>')
    a('    </kit>')
    for t, level in P.LEVELS[1:]:
        a(f'    <kit id="stick{level}" force="true">')
        a(f'        <item slot="0" material="stick" name="{NAMES[level]}"><enchantment level="{level}">knockback</enchantment></item>')
        a('    </kit>')
    a('    <give><kit force="true"><knockback-reduction>0</knockback-reduction></kit><filter><time>3s</time></filter></give>')
    for t, level in P.LEVELS[1:]:
        a(f'    <give kit="stick{level}" filter="from-{t}"/>')
    a('</kits>')
    a('<spawns>')
    a('    <spawn kit="stick" spread="true" safe="true">')
    a('        <regions>')
    for x, z, yaw in spawn_points():
        a(f'            <point yaw="{yaw}">{x},{y},{z}</point>')
    a('        </regions>')
    a('    </spawn>')
    a(f'    <default yaw="0" pitch="40"><region><point>0.5,{y + 24},-40.5</point></region></default>')
    a('</spawns>')
    a('<filters>')
    for t, level in P.LEVELS[1:]:
        a(f'    <all id="from-{t}"><time>{t}s</time><participating/></all>')
    a('</filters>')
    a('<regions>')
    a('    <apply block="never"/>')
    a('</regions>')
    a('<portals>')
    a(f'    <portal y="@-64" sound="false" observers="never"><region><below y="{P.KILL_Y}"/></region></portal>')
    a('</portals>')
    a(f'<time>{P.TIME}</time>')
    a('<blitz><lives>1</lives><broadcastLives>true</broadcastLives></blitz>')
    a('<itemremove><item>stick</item></itemremove>')
    a('<disabledamage><damage>fall</damage></disabledamage>')
    a('<hunger><depletion>off</depletion></hunger>')
    a('<world><timeset>6000</timeset><timelock>on</timelock></world>')
    a('</map>')
    print("\n".join(o))


if __name__ == "__main__":
    main()
