"""Three teacups stacked on saucers and leaning like a tower: a ledge winds up each cup, doors lead into the cups."""
import math
from mc import B

NAME = "The Teetering Teacups"
KIND = "sculpture"

# (centre x, saucer y, scale, ledge direction): cup occupies y = saucer + 1 .. saucer + 5
P = math.pi
CUPS = [(4, 0, 1.0, 4.4, P / 2, 1.5 * P), (6, 6, 0.95, 4.0, -P / 2, P / 2), (4, 12, 0.85, 3.9, P / 2, 1.5 * P)]


def ro(h, s):
    return s * (2.6 + 0.25 * h)


def build(c):
    for k, (cx, sy, s, sr, a0, a1) in enumerate(CUPS):
        cz = 5
        # saucer: a disc with a blue edge band
        for x in range(0, 11):
            for z in range(0, 11):
                d = math.hypot(x - cx, z - cz)
                if d <= sr:
                    c.set(x, sy, z, B.STAINED_CLAY, 3 if d > sr - 0.7 else 0)
                    c.set(x, sy, z, B.QUARTZ) if d <= sr - 0.7 else None
        # the cup: a closed foot, a flaring wall, hollow
        for h in range(0, 5):
            y = sy + 1 + h
            r = ro(h, s)
            for x in range(0, 11):
                for z in range(0, 11):
                    d = math.hypot(x - cx, z - cz)
                    if d <= r:
                        solid = h == 0 or d > r - 1.0
                        if solid:
                            band = h in (2,) and (x + z) % 2 == 0
                            c.set(x, y, z, B.STAINED_CLAY, 3) if band else c.set(x, y, z, B.QUARTZ)
                            if h == 4 and d > r - 0.6:
                                c.set(x, y, z, B.STAINED_CLAY, 3)
                        else:
                            c.set(x, y, z, B.AIR)
        # the ledge round the outside of the cup
        n = 36
        prev = None
        for i in range(0, n + 1):
            t = i / n
            a = a0 + (a1 - a0) * t
            y = sy + 1 + int(4 * t + 0.5)
            h = y - (sy + 1)
            rr = ro(h, s) + 0.9
            x = int(round(cx + rr * math.cos(a)))
            z = int(round(cz + rr * math.sin(a)))
            if not (0 <= x <= 10 and 0 <= z <= 10):
                continue
            cell = (x, y, z)
            if prev and prev != cell:
                if prev[0] != x and prev[2] != z:
                    c.set(prev[0], prev[1], z, B.WOOL, 3)
                    for kk in (1, 2, 3):
                        c.set(prev[0], prev[1] + kk, z, B.AIR)
                c.set(x, y, z, B.WOOL, 3 if i % 2 else 0)
                for kk in (1, 2, 3):
                    if c.get(x, y + kk, z)[0] not in (B.AIR,):
                        c.set(x, y + kk, z, B.AIR)
            elif prev is None:
                c.set(x, y, z, B.WOOL, 3)
                for kk in (1, 2, 3):
                    c.set(x, y + kk, z, B.AIR)
            prev = cell
        # a door into the cup from the ledge, halfway round
        t = 0.5
        a = a0 + (a1 - a0) * t
        y = sy + 1 + int(4 * t + 0.5)
        h = y - (sy + 1)
        for rr10 in range(int((ro(h, s) + 0.9) * 10), 5, -5):
            x = int(round(cx + rr10 / 10 * math.cos(a)))
            z = int(round(cz + rr10 / 10 * math.sin(a)))
            if 0 <= x <= 10 and 0 <= z <= 10:
                if math.hypot(x - cx, z - cz) < ro(h, s) - 1.0:
                    break
                for kk in (1, 2):
                    c.set(x, y + kk, z, B.AIR)
        # inside: a step up to the door and a lantern
    # spoon and sugar on the top cup, a wisp of steam
    for i in range(0, 4):
        c.set(2 + i, 18 + i if 18 + i <= 22 else 22, 7, B.FENCE)
    c.set(5, 18, 4, B.QUARTZ)
    c.set(6, 18, 4, B.QUARTZ)
