"""Lantern Karst's plan, drawn before anything is built, in three panels:

1. THE BOARD — every piece as its polygon, filled by kind and numbered with its floor height; the build
   zones hatched over the void; the defence wall; the wools, the monuments and the spawn; both halves.
2. THE ROUTES — red's two wools and the ways blue attacks them, with the measured lengths from
   plan_check.py, and red's own lanes from its spawn to its wools.
3. TWO SECTIONS — across the Pillar's pit at z -75 (the two Arms, the pit, the Pillar, the bedrock course under
   each island, the kill height, the mist), and along the Store Road at x 52 (the joins, the climb, the wall, the room).

    python3 sketch.py <out.png>
"""
import sys

from PIL import Image, ImageDraw

import plan as P
import plan_check as C

S = 3
W, H = (P.X_MAX - P.X_MIN + 1) * S, (P.Z_MAX - P.Z_MIN + 1) * S
FILL = {"frontline": (190, 175, 140), "hub": (150, 185, 110), "spawn": (220, 200, 150), "lane": (170, 200, 120), "ledge": (90, 120, 170),
        "approach": (150, 175, 110), "wool": (240, 240, 240), "islet": (140, 150, 130)}


def px(x, z, ox=0, oy=0):
    return (ox + (x - P.X_MIN + 0.5) * S, oy + (z - P.Z_MIN + 0.5) * S)


def both(poly):
    return [(poly, "red"), ([P.rot(x, z) for x, z in poly], "blue")]


def label(d, x, z, t, oy, ox=0, fill=(0, 0, 0)):
    a, b = px(x, z, ox, oy)
    d.text((a + 1, b + 1), t, fill=(255, 255, 255))
    d.text((a, b), t, fill=fill)


def hatch(d, poly, oy, col):
    xs = [p[0] for p in poly]; zs = [p[1] for p in poly]
    import geometry as G
    import numpy as np
    for x in range(int(min(xs)), int(max(xs)) + 1):
        for z in range(int(min(zs)), int(max(zs)) + 1):
            if (x + z) % 4 == 0 and G.inside(np.array([[x + 0.0]]), np.array([[z + 0.0]]), poly)[0, 0]:
                a, b = px(x, z, 0, oy)
                d.point((a, b), fill=col)


def board(d, oy):
    d.rectangle([0, oy, W, oy + H], fill=(28, 30, 40))
    for z in P.BUILD_ZONES:
        for q, team in both(z["poly"]):
            hatch(d, q, oy, (230, 200, 90))
    for p in P.PIECES + [P.BELL_ROCK]:
        for q, team in both(p["poly"]):
            col = FILL.get(p.get("kind"), (200, 200, 200))
            d.polygon([px(x, z, 0, oy) for x, z in q], fill=col, outline=(20, 20, 20))
            if "hole" in p:
                h = p["hole"] if team == "red" else [P.rot(x, z) for x, z in p["hole"]]
                d.polygon([px(x, z, 0, oy) for x, z in h], fill=(28, 30, 40), outline=(20, 20, 20))
    for p in P.PIECES + [P.BELL_ROCK]:
        cx = sum(q[0] for q in p["poly"]) / 4; cz = sum(q[1] for q in p["poly"]) / 4
        label(d, cx - 2, cz - 1, str(p["y"]), oy, fill=(60, 30, 0))
    for w in P.WALLS:
        for (a, b), team in both([(w["x0"], w["z"]), (w["x1"], w["z"])]):
            pass
        for q, team in both([(w["x0"] - 0.5, w["z"]), (w["x1"] + 0.5, w["z"])]):
            d.line([px(x, z, 0, oy) for x, z in q], fill=(20, 20, 20), width=S + 1)
    for wl in P.WOOLS:
        for (x, z), team in ((wl["at"], "red"), (P.rot(*wl["at"]), "blue")):
            col = {"lime": (120, 220, 40), "yellow": (250, 220, 40)}[wl["colour"]]
            d.rectangle([px(x - 1.5, z - 1.5, 0, oy), px(x + 1.5, z + 1.5, 0, oy)], fill=col, outline=(200, 30, 30) if team == "red" else (40, 70, 220), width=2)
    for m in P.MONUMENTS:
        for (x, z), team in ((m["at"], "red"), (P.rot(*m["at"]), "blue")):
            col = {"lime": (120, 220, 40), "yellow": (250, 220, 40)}[m["colour"]]
            d.ellipse([px(x - 1.5, z - 1.5, 0, oy), px(x + 1.5, z + 1.5, 0, oy)], fill=col, outline=(255, 255, 255))
    for (x, z), col in (((P.SPAWN_POINT[0], P.SPAWN_POINT[2]), (200, 30, 30)), (P.rot(P.SPAWN_POINT[0], P.SPAWN_POINT[2]), (40, 70, 220))):
        d.ellipse([px(x - 3, z - 3, 0, oy), px(x + 3, z + 3, 0, oy)], fill=col, outline=(255, 255, 255), width=2)
    names = {"leg-w": "West Stair", "bar": "Gate Terrace", "hub": "Tea Court", "sp-mid": "Pavilion (spawn)",
             "f-stem": "Long Terrace", "f-west": "Far Arm", "f-east": "Near Arm", "pillar": "PILLAR", "rows": "Tea Rows",
             "drying": "Drying Floor", "road": "Store Road", "store": "TEA STORE", "w-2": "Mist Steps",
             "e-1": "Tea Steps", "ledge-w": "Ledges (46)", "leg-e": "East Stair"}
    for p in P.PIECES:
        if p["key"] in names:
            x0 = min(q[0] for q in p["poly"]); z1 = max(q[1] for q in p["poly"])
            if p["key"] == "rows":
                z1 = min(q[1] for q in p["poly"]) - 6
            if p["key"] in ("store", "sp-mid"):
                x0, z1 = (x0 - 4, min(q[1] for q in p["poly"]) - 6) if p["key"] == "store" else (x0 + 30, z1 - 8)
            label(d, x0, z1 + 1, names[p["key"]], oy, fill=(255, 255, 255) if p["key"] not in ("pillar", "store") else (255, 240, 120))
    for what, q, top in P.SPAWN_DETAIL:
        for qq, team in both(q):
            d.rectangle([px(min(x for x, z in qq), min(z for x, z in qq), 0, oy), px(max(x for x, z in qq) - 1, max(z for x, z in qq) - 1, 0, oy)],
                        outline=(120, 70, 30), width=1)
    label(d, -46, -2, "the band (build) and the Bell Rock", oy, fill=(255, 230, 140))
    d.text((6, oy + 4), "1. THE BOARD - the number on each piece is its floor height (y); yellow dots: build zones over void;"
           " black bar: bedrock wall;\n   squares: wools (rim = owner); dots: monuments; discs: spawns; brown boxes: the spawn's relief (pavilion, pool, outcrop, towers)", fill=(255, 255, 255))


def routes(d, oy, table):
    d.rectangle([0, oy, W, oy + H], fill=(28, 30, 40))
    for p in P.PIECES + [P.BELL_ROCK]:
        for q, team in both(p["poly"]):
            d.polygon([px(x, z, 0, oy) for x, z in q], fill=(70, 75, 70), outline=(40, 40, 40))
    blue_store = [(18, -12), (20, -32), (26, -44), (56, -44), (56, -80), (56, -90)]
    blue_store_far = [(20, -32), (24, -48), (20, -70), (40, -72), (56, -76)]
    blue_store_flank = [(46, -10), (46, -24), (46, -40)]
    blue_store_flank2 = [(46, -24), (64, -24), (60, -40)]
    blue_pillar = [(-20, -12), (-24, -32), (-30, -48), (-37, -70), (-37, -94), (-59, -94)]
    blue_pillar_far = [(-30, -48), (-37, -66), (-87, -66), (-87, -94), (-67, -94)]
    blue_flank = [(-48, -10), (-48, -26), (-48, -44), (-56, -62), (-62, -89)]
    red_store = [(0, -104), (0, -92), (13, -88), (13, -78), (40, -72), (56, -74), (56, -88)]
    red_pillar = [(0, -104), (0, -92), (-14, -88), (-14, -78), (-30, -74), (-37, -80), (-37, -90)]
    for pts, col, w_ in ((blue_store, (90, 140, 255), 4), (blue_store_far, (90, 140, 255), 2), (blue_pillar, (90, 140, 255), 4),
                         (blue_flank, (150, 190, 255), 3), (blue_store_flank, (150, 190, 255), 3), (blue_store_flank2, (150, 190, 255), 2),
                         (blue_pillar_far, (90, 140, 255), 2), (red_store, (240, 90, 80), 2), (red_pillar, (240, 90, 80), 2)):
        d.line([px(x, z, 0, oy) for x, z in pts], fill=col, width=w_)
    for wl in P.WOOLS:
        x, z = wl["at"]
        col = {"lime": (120, 220, 40), "yellow": (250, 220, 40)}[wl["colour"]]
        d.rectangle([px(x - 2, z - 2, 0, oy), px(x + 2, z + 2, 0, oy)], fill=col)
    label(d, 24, -118, "the Store: three ways onto a short road,", oy, fill=(170, 200, 255))
    label(d, 24, -113, "one wall where they meet", oy, fill=(170, 200, 255))
    label(d, -108, -112, "the Pillar: bridge from", oy, fill=(170, 200, 255))
    label(d, -108, -107, "either Arm or the Terrace", oy, fill=(170, 200, 255))
    label(d, -108, -36, "the Mist Steps", oy, fill=(190, 215, 255))
    label(d, 72, -26, "the Tea Steps", oy, fill=(190, 215, 255))
    label(d, 18, -107, "red's own lanes (red)", oy, fill=(255, 160, 150))
    y = int(H * 0.55)
    d.rectangle([4, oy + y - 6, W - 4, oy + y + 12 * len(table) + 4], fill=(20, 22, 30), outline=(90, 90, 90))
    for a, b in table:
        d.text((10, oy + y), f"{b:>22}   {a}", fill=(230, 230, 230))
        y += 12
    d.text((6, oy + 4), "2. THE ROUTES onto red's two wools (blue attacking, blue lines; red defending, red lines),"
           " and the plan's measured numbers", fill=(255, 255, 255))


def sections(d, oy, hgt):
    d.rectangle([0, oy, W, oy + hgt], fill=(205, 222, 240))
    half = W // 2
    fd = P.FOUNDATION_DEPTH

    def py(y):
        return oy + hgt - (y - 20) * hgt / 90.0

    def column(x0, x1, top, bot, sx):
        """A karst island in section: stone to its bedrock course, then rock tapering on below it, out of play."""
        d.polygon([(sx(x0), py(top)), (sx(x1 + 1), py(top)), (sx(x1 + 1), py(top - fd)), (sx(x0), py(top - fd))],
                  fill=(150, 145, 130), outline=(60, 60, 60))
        d.rectangle([sx(x0), py(top - fd), sx(x1 + 1), py(top - fd - 1)], fill=(25, 25, 25))
        d.polygon([(sx(x0), py(top - fd - 1)), (sx(x1 + 1), py(top - fd - 1)), (sx(x1 + 1) - 3, py(bot)), (sx(x0) + 3, py(bot))],
                  fill=(175, 170, 160), outline=(120, 120, 120))
    # left: the Pillar's pit seen from the Long Terrace, looking north, x -96..-28
    sx = lambda x: (x + 96) * (half - 20) / 68.0 + 10
    d.rectangle([0, py(P.MIST_Y[1]), half, py(P.MIST_Y[0])], fill=(245, 248, 252))
    d.line([(0, py(P.KILL_Y)), (half, py(P.KILL_Y))], fill=(200, 30, 30), width=2)
    for (x0, x1, top, bot) in ((-92, -83, 67, 46), (-42, -33, 67, 46), (-66, -59, 74, 42), (-75, -70, 46, 30), (-55, -50, 46, 30)):
        column(x0, x1, top, bot, sx)
    d.rectangle([sx(-66), py(78), sx(-58), py(74)], outline=(60, 40, 20), width=2)
    d.rectangle([sx(-63), py(76), sx(-62), py(75)], fill=(120, 220, 40))
    for a, b in ((-82, -67), (-58, -43)):
        d.line([(sx(a), py(67)), (sx(b + 1), py(67))], fill=(200, 160, 40), width=1)
    d.line([(sx(-52), py(47)), (sx(-52), py(74)), (sx(-59), py(74))], fill=(40, 70, 220), width=1)
    d.text((sx(-95), py(71)), "Far Arm 67", fill=(0, 0, 0))
    d.text((sx(-44), py(71)), "Near Arm 67", fill=(0, 0, 0))
    d.text((sx(-70), py(81)), "Pillar Shrine 74", fill=(0, 0, 0))
    d.text((sx(-82), py(64)), "16 to bridge", fill=(120, 80, 0))
    d.text((sx(-57), py(64)), "16 to bridge", fill=(120, 80, 0))
    d.text((sx(-80), py(50)), "Ledges 46: drop 20 onto a bucket,", fill=(40, 70, 220))
    d.text((sx(-80), py(47) + 2), "pillar up 28 beside the pillar", fill=(40, 70, 220))
    d.text((sx(-95), py(P.KILL_Y) - 12), f"kill below y {P.KILL_Y}", fill=(200, 30, 30))
    d.text((sx(-95), py(P.MIST_Y[1]) + 2), "mist", fill=(90, 90, 90))
    d.text((sx(-95), py(26)), f"black: bedrock {fd} under every floor; block 36 at y 0 under every buildable column", fill=(20, 20, 20))
    d.text((6, oy + 4), "3a. THE PILLAR'S PIT, seen from the Long Terrace", fill=(0, 0, 0))
    # right: along the Store Road at x 56, z -24..-101
    sz = lambda z: half + 10 + (-z - 24) * (half - 30) / 78.0
    prof = [(-39, 66), (-50, 66), (-59, 67), (-68, 68), (-77, 69), (-86, 70), (-100, 70)]
    pts = [(sz(z), py(y)) for z, y in prof]
    d.polygon(pts + [(sz(-100), py(70 - fd)), (sz(-39), py(66 - fd))], fill=(150, 145, 130), outline=(60, 60, 60))
    d.line([(sz(-39), py(66 - fd)), (sz(-100), py(70 - fd))], fill=(25, 25, 25), width=3)
    d.polygon([(sz(-39), py(66 - fd - 1)), (sz(-100), py(70 - fd - 1)), (sz(-94), py(44)), (sz(-45), py(44))],
              fill=(175, 170, 160), outline=(120, 120, 120))
    d.rectangle([sz(-22), py(65), sz(-27), py(59)], fill=(150, 145, 130), outline=(60, 60, 60))
    d.rectangle([sz(-82), py(74), sz(-83), py(70)], fill=(20, 20, 20))
    d.rectangle([sz(-87), py(76), sz(-100), py(70)], outline=(60, 40, 20), width=2)
    d.rectangle([sz(-95), py(72), sz(-96), py(71)], fill=(250, 220, 40))
    for z0, z1, t in ((-39, -50, "Tea Rows join"), (-67, -78, "Drying Floor joins")):
        d.rectangle([sz(z0), py(83), sz(z1), py(82)], fill=(90, 140, 255))
        d.text((sz(z0), py(88)), t, fill=(0, 0, 0))
    d.text((sz(-24), py(70)), "Tea Step II", fill=(0, 0, 0))
    d.text((sz(-80), py(78)), "wall", fill=(0, 0, 0))
    d.text((sz(-88), py(80)), "Tea Store 70", fill=(0, 0, 0))
    d.text((sz(-50), py(72)), "Store Road, 14 wide, 66 -> 70", fill=(0, 0, 0))
    d.text((half + 6, oy + 4), "3b. ALONG THE STORE ROAD, x 56", fill=(0, 0, 0))
    d.line([(half, oy), (half, oy + hgt)], fill=(0, 0, 0), width=1)


def main(out):
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        table = C.main()
    hs = 300
    im = Image.new("RGB", (W, 2 * H + hs + 8), (255, 255, 255))
    d = ImageDraw.Draw(im)
    board(d, 0)
    routes(d, H + 4, table)
    sections(d, 2 * H + 8, hs)
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
