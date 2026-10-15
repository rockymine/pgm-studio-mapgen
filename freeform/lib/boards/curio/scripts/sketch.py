"""Curio Square's plan, drawn before anything is built: the square from above, every plot coloured by its builder
and its kind, with its name and the height of its highest standing place, read from each builder's IDEAS.md.

    python3 sketch.py <out.png>
"""
import os
import random
import sys

from PIL import Image, ImageDraw

import plan as P

HERE = os.path.dirname(os.path.abspath(__file__))
COLOUR = {"opus": (196, 120, 70), "haiku": (90, 150, 110), "sonnet": (100, 120, 190)}
KIND_MARK = {"house": "H", "structure": "S", "sculpture": "*"}
S = 9


def ideas(builder):
    rows = []
    for line in open(os.path.join(HERE, "..", "plots", builder, "IDEAS.md")):
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) == 7 and cells[0].endswith(".py"):
            rows.append(dict(file=cells[0], name=cells[1], kind=cells[2], height=cells[6]))
    return rows


def layout():
    """Each builder's plots, shuffled with a fixed seed so the kinds mix across the square, over the builder's places
    in the grid."""
    queue = {b: ideas(b) for b in P.BUILDERS}
    for k, b in enumerate(P.BUILDERS):
        random.Random(P.SEED + k).shuffle(queue[b])
    out = {}
    for i, j in P.plots():
        b = P.builder(i, j)
        out[(i, j)] = (b, queue[b].pop(0) if queue[b] else None)
    return out


def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + [cur]


def main(out):
    W = (2 * P.WALL + 1) * S
    img = Image.new("RGB", (W + 40, W + 120), (30, 32, 40))
    d = ImageDraw.Draw(img)
    ox = oy = 20
    px = lambda v: (v + P.WALL) * S
    d.rectangle([ox, oy, ox + W, oy + W], fill=(120, 110, 100))                  # the wall
    d.rectangle([ox + px(-P.HALF), oy + px(-P.HALF), ox + px(P.HALF + 1), oy + px(P.HALF + 1)], fill=(176, 170, 160))
    lay = layout()
    for i in range(P.N):
        for j in range(P.N):
            x0, z0 = P.origin(i, j)
            a, b = ox + px(x0), oy + px(z0)
            box = [a, b, a + P.PLOT * S - 1, b + P.PLOT * S - 1]
            if (i, j) == P.CENTRE:
                d.rectangle(box, fill=(150, 190, 220))
                d.text((a + 6, b + 6), "the fountain\nseekers' cage\nover it", fill=(20, 30, 50))
                continue
            builder, row = lay[(i, j)]
            d.rectangle(box, fill=COLOUR[builder])
            if row:
                lines = wrap(row["name"].replace("The ", ""), 14)
                d.multiline_text((a + 4, b + 4), "\n".join(lines[:3]), fill=(255, 255, 255), spacing=2)
                d.text((a + 4, b + P.PLOT * S - 16), f"{KIND_MARK.get(row['kind'], '?')}  {row['height']} up", fill=(240, 240, 220))
    y = oy + W + 14
    for k, bld in enumerate(P.BUILDERS):
        d.rectangle([ox + 160 * k, y, ox + 160 * k + 14, y + 14], fill=COLOUR[bld])
        d.text((ox + 160 * k + 20, y + 1), bld, fill=(255, 255, 255))
    d.text((ox, y + 26), "H a house   S a structure   * a sculpture   the number: the highest standing place over the street",
           fill=(220, 220, 220))
    d.text((ox, y + 46), f"forty-eight plots of {P.PLOT} by {P.PLOT}, streets of {P.STREET}; six plots vanish every minute "
           f"from {P.ROUNDS[0] // 60}m{P.ROUNDS[0] % 60:02d}s", fill=(220, 220, 220))
    img.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
