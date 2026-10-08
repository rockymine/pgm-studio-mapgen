"""Write Sunwell's map.xml from the plan: every hill's box, the spawn shelf, the spring, the water the board is built
with (which nobody may scoop up), all from the plan's own numbers.

    python3 mapxml.py > map.xml
"""
import gen as G
import plan as P


def hill_boxes():
    """(id, name, points, (x0, y0, z0, x1, y1, z1)) for every hill: five by five, from two under the shelf's top to
    three over it, so a swimmer in its pool and a runner over it both touch it."""
    out = []
    n = 0
    for k, d in enumerate(P.DROPS):
        y = P.ISLET["y"] if d.get("lake") else P.shelf_y(k + 1)
        for name, x0, x1, s0, s1, sd in P.hills(k):
            n += 1
            za, zb = sorted((P.z_of(k, s0), P.z_of(k, s1)))
            pts = P.POINTS["last" if d.get("lake") else "hill"]
            label = f"{name.replace('the ', '').title()}" + ("" if sd == "middle" else f" ({sd})")
            out.append((f"hill-{n}", f"{k + 1}. {label}", pts, (x0, y - 2, za, x1 + 1, y + 4, zb + 1)))
    return out


def built_water():
    """Boxes over the water the board is built with: pools, basins, falls, streams, the lake."""
    out = []
    for k, d in enumerate(P.DROPS):
        if d.get("lake"):
            continue
        y = P.shelf_y(k + 1)
        for name, x0, x1, s0, s1, sd in P.pools(k) + P.falls(k):
            za, zb = sorted((P.z_of(k, s0), P.z_of(k, s1)))
            out.append((x0, y - 3, za, x1 + 1, y + 1, zb + 1))
        for name, x0, x1, s0, s1, sd in P.falls(k):
            za, zb = sorted((P.z_of(k, 1), P.z_of(k, 2)))
            out.append((x0, y, za, x1 + 1, P.shelf_y(k) + 1, zb + 1))
            ze = P.EDGE if P.side(k) == "N" else -P.EDGE
            zs = sorted((ze, ze + (-5 if P.side(k) == "N" else 5)))
            out.append((x0, P.shelf_y(k) - 1, zs[0], x1 + 1, P.shelf_y(k) + 1, zs[1] + 1))
    out.append((-G.R - 4, G.LAKE_FLOOR, -G.R - 4, G.R + 5, P.LAKE_Y + 1, G.R + 9))
    return out


def main():
    o = []
    a = o.append
    sx0, sx1 = P.SPAWN["x"]
    sz0, sz1 = P.SPAWN["z"]
    top = P.TOP + 1
    a('<map proto="1.5.0">')
    a('<name>Sunwell</name>')
    a('<version>1.0.0</version>')
    a('<objective>Drop down the sinkhole and hold the most hills when the clock runs out.</objective>')
    a('<gamemode>arcade</gamemode>')
    a('<rules><rule>Every drop kills unless it ends in water: hit a pool, place a bucket, or ride the falls.</rule>'
      '<rule>Touch a hill to take it; it scores for you until someone else touches it, even after you die.</rule>'
      '<rule>The spring in the lake takes you back to the top.</rule></rules>')
    a('<players min="1" max="40" colors="true"/>')
    a('<kits>')
    a('    <kit id="players">')
    a('        <clear/>')
    for slot in range(3):
        a(f'        <item slot="{slot}" locked="true" name="`b`lWater Drop" material="water bucket"/>')
    a('        <effect duration="3s" amplifier="5">resistance</effect>')
    a('        <effect duration="oo" amplifier="-2">health boost</effect>')
    a('        <game-mode>survival</game-mode>')
    a('    </kit>')
    a('</kits>')
    a('<spawns>')
    a(f'    <spawn kit="players" yaw="0"><region><cuboid min="{sx0},{top},{sz0}" max="{sx1 + 1},{top},{sz1 + 1}"/></region></spawn>')
    a(f'    <default yaw="0"><region><point>0.5,{P.TOP + 12},-14.5</point></region></default>')
    a('</spawns>')
    a('<filters>')
    a('    <any id="water"><material>water</material><material>stationary water</material></any>')
    for hid, name, pts, box in hill_boxes():
        a(f'    <not id="holding-{hid}"><objective>{hid}</objective></not>')
    a('</filters>')
    a('<regions>')
    a(f'    <cuboid id="spawn-shelf" min="-32,{P.TOP - P.THICK},-32" max="32,256,32"/>')
    a(f'    <cuboid id="top-shelf" min="{sx0},{top},{sz0}" max="{sx1 + 1},{top},{sz1 + 1}"/>')
    a('    <union id="built-water">')
    for x0, y0, z0, x1, y1, z1 in built_water():
        a(f'        <cuboid min="{x0},{y0},{z0}" max="{x1},{y1},{z1}"/>')
    a('    </union>')
    x0, x1 = P.SPRING["x"]
    z0, z1 = P.SPRING["z"]
    a(f'    <cuboid id="spring" min="{x0},{P.LAKE_Y - 2},{z0 + 1}" max="{x1 + 1},{P.LAKE_Y + 4},{z1 + 5}"/>')
    for hid, name, pts, (bx0, by0, bz0, bx1, by1, bz1) in hill_boxes():
        a(f'    <cuboid id="{hid}-box" min="{bx0},{by0},{bz0}" max="{bx1},{by1},{bz1}"/>')
    a('    <apply region="built-water" block-break="never" block-place="never" message="This water belongs to the well."/>')
    a('    <apply region="spawn-shelf" block-place="never"/>')
    a('    <apply block-place="water" block-break="water" block-physics="never"/>')
    a('</regions>')
    a('<damage><deny><region id="spawn-shelf"/></deny></damage>')
    a('<score/>')
    a('<control-points required="false" neutral-state="false" capture-time="0.1s" capture-rule="lead" show="false">')
    for hid, name, pts, box in hill_boxes():
        a(f'    <control-point id="{hid}" name="{name}" points="{pts}" capture="{hid}-box" captured="{hid}-box" '
          f'player-filter="holding-{hid}"/>')
    a('</control-points>')
    a(f'<time>{P.TIME}</time>')
    a('<portals sound="true">')
    a('    <portal region="spring" destination="top-shelf" yaw="@0"/>')
    a('</portals>')
    a('<itemremove><item>bucket</item><item>water bucket</item></itemremove>')
    a('<hunger><depletion>off</depletion></hunger>')
    a('</map>')
    print("\n".join(o))


if __name__ == "__main__":
    main()
