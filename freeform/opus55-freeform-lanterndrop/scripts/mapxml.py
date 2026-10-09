"""Write Lantern Drop's map.xml from the plan and the generator: the hills' boxes, the bell court, the slipway, the
board's own water that nobody may scoop up, and the void that kills, all from the plan's own numbers.

    python3 mapxml.py > map.xml
"""
import gen as G
import plan as P


def hill_boxes():
    out = []
    n = 0
    for p in P.pieces():
        if not p[8].get("hill"):
            continue
        n += 1
        hx0, hx1, hz0, hz1 = G.hill_box(p)
        y = p[7]
        pts = P.POINTS["last" if p[8].get("last") else "hill"]
        label = p[1].replace("the ", "").title() + ("" if p[9] == "middle" else f" ({p[9]})")
        out.append((f"hill-{n}", label, pts, (hx0, y - 2, hz0, hx1 + 1, y + 4, hz1 + 1)))
    return out


def kill_boxes():
    """Under each group of pieces: the course's width, from the previous group's far edge (the court's own near
    edge for the first) to this group's far edge, from the world's floor to five under the group's top; the
    harbour's under its floor."""
    groups = {}
    for p in P.pieces():
        groups.setdefault(p[0], []).append(p)
    out, z_from = [], None
    for i in sorted(groups):
        g = groups[i]
        z0, z1, y = min(p[5] for p in g), max(p[6] for p in g), g[0][7]
        top = y - 5
        if g[0][8].get("harbour"):
            z1, top = P.HARBOUR["z"][1], min(top, P.HARBOUR["y"] - 8)
        out.append((-40, 0, (z0 - 10) if z_from is None else z_from, 40, top, z1))
        z_from = z1 + 1
    return out


def built_water():
    out = []
    for p in P.pieces():
        if "water" in p[8]:
            a0, a1, b0, b1 = p[8]["water"]
            out.append((a0, p[7] - 3, b0, a1 + 1, p[7] + 1, b1 + 1))
    h = P.HARBOUR
    out.append((h["x"][0], h["y"] - 6, h["z"][0], h["x"][1] + 1, h["y"] + 1, h["z"][1] + 1))
    return out


def main():
    o = []
    a = o.append
    court = [p for p in P.pieces() if p[8].get("spawn")][0]
    cx0, cx1, cz0, cz1, cy = court[3], court[4], court[5], court[6], court[7]
    a('<map proto="1.5.0">')
    a('<name>Lantern Drop</name>')
    a('<version>1.0.0</version>')
    a('<objective>Drop down the broken pass and hold the most hills when the clock runs out.</objective>')
    a('<gamemode>arcade</gamemode>')
    a('<rules><rule>A drop of nineteen kills unless it ends in water: a cistern, the paddies, the harbour or your bucket.</rule>'
      '<rule>Touch a hill to take it; it scores for you until someone else touches it, even after you die.</rule>'
      '<rule>The slipway in the harbour takes you back to the bell court.</rule></rules>')
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
    a(f'    <spawn kit="players" yaw="0"><region><cuboid min="{cx0 + 3},{cy + 1},{cz0 + 7}" max="{cx1 - 2},{cy + 1},{cz1 - 2}"/></region></spawn>')
    # observers come in where the players do, on the bell court
    a(f'    <default yaw="0"><region><cuboid min="{cx0 + 3},{cy + 1},{cz0 + 7}" max="{cx1 - 2},{cy + 1},{cz1 - 2}"/></region></default>')
    a('</spawns>')
    a('<filters>')
    a('    <any id="water"><material>water</material><material>stationary water</material></any>')
    # a bucket places a source, data 0; water spreading is a placement too, of data 1 to 8, and is refused
    a('    <any id="water-source"><material>water:0</material><material>stationary water:0</material></any>')
    for hid, name, pts, box in hill_boxes():
        a(f'    <not id="holding-{hid}"><objective>{hid}</objective></not>')
    a('</filters>')
    a('<regions>')
    a(f'    <cuboid id="bell-court" min="{cx0 - 2},{cy - 4},{cz0 - 4}" max="{cx1 + 3},{cy + 12},{cz1 + 2}"/>')
    a(f'    <cuboid id="court-floor" min="{cx0 + 3},{cy + 1},{cz0 + 7}" max="{cx1 - 2},{cy + 1},{cz1 - 2}"/>')
    a('    <union id="built-water">')
    for x0, y0, z0, x1, y1, z1 in built_water():
        a(f'        <cuboid min="{x0},{y0},{z0}" max="{x1},{y1},{z1}"/>')
    a('    </union>')
    s = P.SLIPWAY
    hy = P.HARBOUR["y"]
    a(f'    <cuboid id="slipway" min="{s["x"][0]},{hy - 3},{s["z"][0]}" max="{s["x"][1] + 1},{hy + 4},{s["z"][1] + 2}"/>')
    for hid, name, pts, (bx0, by0, bz0, bx1, by1, bz1) in hill_boxes():
        a(f'    <cuboid id="{hid}-box" min="{bx0},{by0},{bz0}" max="{bx1},{by1},{bz1}"/>')
    a('    <apply region="built-water" block-break="never" block-place="never" message="This water belongs to the pass."/>')
    a('    <apply region="bell-court" block-place="never"/>')
    a('    <apply block-place="water-source" block-break="water" block-physics="never"/>')
    a('</regions>')
    a('<damage><deny><region id="bell-court"/></deny></damage>')
    a('<score/>')
    a('<control-points required="false" neutral-state="false" capture-time="0.1s" capture-rule="lead" show="false">')
    for hid, name, pts, box in hill_boxes():
        a(f'    <control-point id="{hid}" name="{name}" points="{pts}" capture="{hid}-box" captured="{hid}-box" '
          f'player-filter="holding-{hid}"/>')
    a('</control-points>')
    a(f'<time>{P.TIME}</time>')
    a('<portals sound="true">')
    a('    <portal region="slipway" destination="court-floor" yaw="@0"/>')
    # a box under every landing, from the last group's far edge to this one's, five under its top: a player who
    # misses the landing falls into it and is put under the world, where the void kills within a few ticks. A
    # landing, even in a cistern three deep, stays above it; the drop onward leaves past the group's far edge
    a('    <portal y="-70"><region><union>')
    for x0, y0, z0, x1, y1, z1 in kill_boxes():
        a(f'        <cuboid min="{x0},{y0},{z0}" max="{x1},{y1},{z1}"/>')
    a('    </union></region></portal>')
    a('    <portal y="-64"><region><below y="-5"/></region></portal>')
    a('</portals>')
    a('<itemremove><item>bucket</item><item>water bucket</item></itemremove>')
    a('<hunger><depletion>off</depletion></hunger>')
    a('</map>')
    print("\n".join(o))


if __name__ == "__main__":
    main()
