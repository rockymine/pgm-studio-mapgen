"""Write Loomfall's map.xml from the plan: the spawn on the top carpet, the kill height, the wool that turns white
under a player's step and falls, and the clearing of falling wool before it lands on a carpet below.

    python3 mapxml.py > map.xml
"""
import plan as P


def main():
    o = []
    a = o.append
    top = P.CARPETS[0]
    sx0, sx1 = P.SPAWN["x"]
    sz0, sz1 = P.SPAWN["z"]
    a('<map proto="1.5.0">')
    a('<name>Loomfall</name>')
    a('<version>1.0.0</version>')
    a('<objective>Keep running: the carpet falls away under every step. Be the last one flying.</objective>')
    a('<gamemode>arcade</gamemode>')
    a('<rules><rule>Wool you step on turns white and falls.</rule><rule>No fall damage, no fighting: '
      'only snowball grenades.</rule><rule>Below the last carpet you are out.</rule></rules>')
    a('<players min="2" max="40" colors="true"/>')
    a('<world><timeset>18000</timeset><timelock>on</timelock></world>')
    a('<kits>')
    a('    <kit id="flyer">')
    a('        <clear/>')
    a('        <game-mode>adventure</game-mode>')
    a('        <item slot="0" amount="5" material="snow ball" grenade="true" grenade-power="1"/>')
    a('    </kit>')
    a('    <kit id="out" force="true"><effect amplifier="100" duration="5">harm</effect></kit>')
    a('</kits>')
    a('<spawns>')
    a(f'    <spawn kit="flyer" safe="true"><region><cuboid min="{sx0},{top[5] + 1},{sz0}" max="{sx1 + 1},{top[5] + 1},{sz1 + 1}"/></region></spawn>')
    a(f'    <default pitch="60"><region><point>0.5,{top[5] + 20},-40.5</point></region></default>')
    a('</spawns>')
    a('<filters>')
    a('    <not id="only-falling-wool"><all><cause>world</cause><material>wool:0</material></all></not>')
    a('    <match-running id="running"/>')
    a('    <entity id="falling-wool">falling block</entity>')
    a('</filters>')
    a('<regions>')
    a('    <apply block="only-falling-wool"/>')
    a(f'    <apply kit="out"><region><below y="{P.KILL_Y}"/></region></apply>')
    a('</regions>')
    a('<block-drops>')
    a('    <rule trample="true"><filter><material>wool</material></filter><replacement>wool:0</replacement></rule>')
    a('</block-drops>')
    a('<falling-blocks>')
    a(f'    <rule delay="{P.WOOL_DELAY}"><filter><material>wool:0</material></filter><sticky><never/></sticky></rule>')
    a('</falling-blocks>')
    a('<actions>')
    a('    <trigger scope="match"><filter><pulse duration="0.25s" period="0.5s" filter="running"/></filter>')
    a('        <action><kill-entities filter="falling-wool"/></action></trigger>')
    a('</actions>')
    a('<damage><allow><cause>void</cause></allow><allow><cause>potion</cause></allow><not><cause>player</cause></not></damage>')
    a('<disabledamage><damage>fall</damage></disabledamage>')
    a('<hunger><depletion>off</depletion></hunger>')
    a('<blitz><lives>1</lives></blitz>')
    a('<time>10m</time>')
    a('<itemremove><item>wool</item><item>snow ball</item></itemremove>')
    a('</map>')
    print("\n".join(o))


if __name__ == "__main__":
    main()
