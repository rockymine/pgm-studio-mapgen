"""Lantern Karst's plan, drawn before anything is built, in three panels:

1. THE BOARD — every piece as its polygon, filled by kind and numbered with its floor height; the build
   zones hatched over the void; the defence wall; the wools, the monuments and the spawn; both halves.
2. THE ROUTES — red's two wools and the ways blue attacks them, with the measured lengths from
   plan_check.py, and red's own lanes from its spawn to its wools.
3. TWO SECTIONS — across the Pillar's pit at z -90 (the Horseshoe, the pit, the Pillar, the kill height, the
   mist), and along the Store Road at x 45 (the climb, the wall, the room).

    python3 sketch.py <out.png>
"""
import sys

from PIL import Image, ImageDraw

import plan_v1 as P
import plan_check_v1 as C

S = 3
W, H = (P.X_MAX - P.X_MIN + 1) * S, (P.Z_MAX - P.Z_MIN + 1) * S
FILL = {"frontline": (190, 175, 140), "hub": (150, 185, 110), "spawn": (220, 200, 150), "lane": (170, 200, 120),
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
    names = {"leg-w": "West Stair", "bar": "Gate Terrace", "hub": "Tea Court", "spawn": "Pavilion (spawn)",
             "lane-w": "Long Terrace", "shoe-s": "Horseshoe", "pillar": "PILLAR", "lane-e": "Tea Rows",
             "lane-e2": "Store Road", "store": "TEA STORE", "islet-2": "Mist Steps", "leg-e": "East Stair"}
    for p in P.PIECES:
        if p["key"] in names:
            x0 = min(q[0] for q in p["poly"]); z1 = max(q[1] for q in p["poly"])
            label(d, x0, z1 + 1, names[p["key"]], oy, fill=(255, 255, 255) if p["key"] not in ("pillar", "store") else (255, 240, 120))
    label(d, -38, -2, "the band (build) and the Bell Rock", oy, fill=(255, 230, 140))
    d.text((6, oy + 4), "1. THE BOARD - pieces by kind, numbered with their floor y; yellow dots: build zones over void;"
           " black bar: bedrock wall; squares: wools (rim = owner); dots: monuments; discs: spawns", fill=(255, 255, 255))


def routes(d, oy, table):
    d.rectangle([0, oy, W, oy + H], fill=(28, 30, 40))
    for p in P.PIECES + [P.BELL_ROCK]:
        for q, team in both(p["poly"]):
            d.polygon([px(x, z, 0, oy) for x, z in q], fill=(70, 75, 70), outline=(40, 40, 40))
    blue_store = [(-30, -6), (18, -12), (18, -32), (16, -38), (16, -45), (24, -46), (24, -52), (38, -52), (46, -58),
                  (46, -82), (46, -95)]
    blue_store_far = [(18, -40), (-14, -46), (-24, -60), (-14, -70), (14, -70), (24, -66), (26, -52)]
    blue_pillar = [(-30, 6), (-18, -12), (-18, -36), (-18, -46), (-24, -52), (-27, -58), (-50, -58), (-60, -66),
                   (-62, -70), (-57, -86)]
    blue_flank = [(-36, -9), (-58, -19), (-71, -33), (-81, -47), (-82, -58), (-76, -70), (-70, -84), (-60, -90)]
    red_store = [(0, -90), (0, -76), (20, -70), (24, -52), (46, -52), (46, -95)]
    red_pillar = [(0, -90), (0, -76), (-20, -70), (-27, -58), (-58, -58), (-58, -70), (-55, -86)]
    for pts, col, w_ in ((blue_store, (90, 140, 255), 4), (blue_store_far, (90, 140, 255), 2), (blue_pillar, (90, 140, 255), 4),
                         (blue_flank, (150, 190, 255), 3), (red_store, (240, 90, 80), 2), (red_pillar, (240, 90, 80), 2)):
        d.line([px(x, z, 0, oy) for x, z in pts], fill=col, width=w_)
    for wl in P.WOOLS:
        x, z = wl["at"]
        col = {"lime": (120, 220, 40), "yellow": (250, 220, 40)}[wl["colour"]]
        d.rectangle([px(x - 2, z - 2, 0, oy), px(x + 2, z + 2, 0, oy)], fill=col)
    label(d, 30, -64, "attack on the Store: one road, one wall", oy, fill=(170, 200, 255))
    label(d, 4, -48, "far side of the sinkhole", oy, fill=(170, 200, 255))
    label(d, -54, -52, "attack on the Pillar: lane, then bridge", oy, fill=(170, 200, 255))
    label(d, -94, -40, "the flank: Mist Steps", oy, fill=(190, 215, 255))
    label(d, -6, -96, "red's own lanes (red)", oy, fill=(255, 160, 150))
    y = int(H * 0.60)
    d.rectangle([4, oy + y - 6, W - 4, oy + y + 12 * len(table) + 4], fill=(20, 22, 30), outline=(90, 90, 90))
    for a, b in table:
        d.text((10, oy + y), f"{b:>22}   {a}", fill=(230, 230, 230))
        y += 12
    d.text((6, oy + 4), "2. THE ROUTES onto red's two wools (blue attacking, blue lines; red defending, red lines),"
           " and the plan's measured numbers", fill=(255, 255, 255))


def sections(d, oy, hgt):
    d.rectangle([0, oy, W, oy + hgt], fill=(205, 222, 240))
    half = W // 2

    def py(y):
        return oy + hgt - (y - 20) * hgt / 90.0
    # left: across the Pillar's pit at z -90, x -90..-20
    sx = lambda x: (x + 92) * (half - 20) / 72.0 + 10
    d.rectangle([0, py(P.MIST_Y[1]), half, py(P.MIST_Y[0])], fill=(245, 248, 252))
    d.line([(0, py(P.KILL_Y)), (half, py(P.KILL_Y))], fill=(200, 30, 30), width=2)
    for (x0, x1, top, bot) in ((-79, -73, 66, 48), (-39, -33, 66, 48), (-59, -52, 74, 44)):
        d.polygon([(sx(x0), py(top)), (sx(x1 + 1), py(top)), (sx(x1 + 1) - 4, py(bot)), (sx(x0) + 4, py(bot))],
                  fill=(150, 145, 130), outline=(60, 60, 60))
    d.rectangle([sx(-59), py(78), sx(-51), py(74)], outline=(60, 40, 20), width=2)
    d.rectangle([sx(-56), py(76), sx(-55), py(75)], fill=(120, 220, 40))
    d.line([(sx(-72), py(66)), (sx(-60), py(66))], fill=(230, 200, 90), width=1)
    d.text((sx(-80), py(70)), "Horseshoe 66", fill=(0, 0, 0))
    d.text((sx(-60), py(81)), "Pillar Shrine 74", fill=(0, 0, 0))
    d.text((sx(-72), py(63)), "12 to bridge, 8 to climb", fill=(120, 80, 0))
    d.text((sx(-90), py(P.KILL_Y) - 12), f"kill below y {P.KILL_Y}", fill=(200, 30, 30))
    d.text((sx(-90), py(P.MIST_Y[1]) + 2), "mist", fill=(90, 90, 90))
    d.text((6, oy + 4), "3a. ACROSS THE PILLAR'S PIT, z -90", fill=(0, 0, 0))
    # right: along the Store Road at x 45, z -45..-105
    sz = lambda z: half + 10 + (-z - 40) * (half - 30) / 68.0
    prof = [(-47, 66), (-52, 66), (-57, 68), (-65, 68), (-73, 69), (-81, 69), (-83, 70), (-91, 70), (-103, 70)]
    pts = [(sz(z), py(y)) for z, y in prof]
    d.polygon(pts + [(sz(-103), py(48)), (sz(-47), py(48))], fill=(150, 145, 130), outline=(60, 60, 60))
    d.rectangle([sz(-83), py(74), sz(-84), py(69)], fill=(20, 20, 20))
    d.rectangle([sz(-91), py(76), sz(-103), py(70)], outline=(60, 40, 20), width=2)
    d.rectangle([sz(-99), py(72), sz(-100), py(71)], fill=(250, 220, 40))
    d.text((sz(-50), py(72)), "Tea Rows 66", fill=(0, 0, 0))
    d.text((sz(-66), py(73)), "Store Road 68-70", fill=(0, 0, 0))
    d.text((sz(-84), py(78)), "bedrock wall", fill=(0, 0, 0))
    d.text((sz(-96), py(80)), "Tea Store 70", fill=(0, 0, 0))
    d.text((half + 6, oy + 4), "3b. ALONG THE STORE ROAD, x 45: a block a step, the wall, the room", fill=(0, 0, 0))
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
