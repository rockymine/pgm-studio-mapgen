"""Does the ground vary down a column, or is each column one material? The read a render cannot give.

    python3 tools/probe.py <region> [--body 1:0,1:5,1:6,48:0,129:0,159:9,168:0] [--earth 3:1,5:1,3:0]
                           [--every 3] [--face z=60,x=-100..-88,y=30..1] [--floating]

A fill pattern that samples the plane resolves every column to one material, and on a cut face that reads
as vertical stripes; a pattern with a rise reads as blobs. The difference is invisible from above and hard
to see in a small render, and this is the number for it: the run lengths of one material down a column
through the stone body, their mean, and how many of the earth's courses are one material. `--body` and
`--earth` name the materials counted, as `id:data`; the defaults are the six-stone body and the earth mix
the Millrace revamp uses, and the read says which sets it used. `--face` prints one vertical slice as a
character per block so a face can be looked at in a terminal. `--floating` lists the columns whose lowest
block is above the world's floor, bucketed by what stands at their top, which is how a bridge over a strait
or a cloud is told from a hole in the bottom of the world.
"""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anvil import World, name  # noqa: E402

BODY = {(1, 0), (1, 5), (1, 6), (48, 0), (129, 0), (159, 9), (168, 0)}
EARTH = {(3, 1), (5, 1), (3, 0)}
FACE_CHARS = {(1, 0): "s", (1, 5): "a", (1, 6): "p", (48, 0): "m", (129, 0): "e", (159, 9): "c", (168, 0): "r",
              (3, 1): "C", (5, 1): "P", (3, 0): "D", (2, 0): "G", (4, 0): "k", (98, 0): "b", (43, 0): "S",
              (8, 0): "≈", (9, 0): "≈", (7, 0): "X", (43, 8): "S", (35, 8): "w", (98, 0): "b", (98, 1): "b",
              (98, 2): "b"}


def option(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def parse_set(text):
    out = set()
    for item in text.split(","):
        block_id, _, data = item.partition(":")
        out.add((int(block_id), int(data or 0)))
    return out


def span(text):
    lo, _, hi = text.partition("..")
    return int(lo), int(hi or lo)


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    world = World(sys.argv[1])
    columns = world.columns()
    body = parse_set(option("--body")) if option("--body") else BODY
    earth = parse_set(option("--earth")) if option("--earth") else EARTH
    every = int(option("--every", 3))
    print(f"body materials: {', '.join(sorted(name(b) for b in body))}")
    print(f"earth materials: {', '.join(sorted(name(b) for b in earth))}")

    runs, earth_kinds = Counter(), Counter()
    for (x, z), column in columns.items():
        if x % every or z % every:
            continue
        blocks = [(i, d) for _y, i, d in column]
        stone = [b for b in blocks if b in body]
        if len(stone) >= 8:
            run = 1
            for a, b in zip(stone, stone[1:]):
                if a == b:
                    run += 1
                else:
                    runs[run] += 1
                    run = 1
            runs[run] += 1
        soil = [b for b in blocks if b in earth]
        if len(soil) == 3:
            earth_kinds[len(set(soil))] += 1
    total = sum(runs.values())
    if total:
        print("body: runs of one material down a column, share by length: "
              + ", ".join(f"{k}: {v * 100 / total:.0f}%" for k, v in sorted(runs.items())[:10]))
        print(f"body: mean run {sum(k * v for k, v in runs.items()) / total:.2f} blocks over {total} runs")
    else:
        print("body: no column carries eight of the body materials — state --body for this board's palette")
    soils = sum(earth_kinds.values())
    if soils:
        print("earth: distinct materials in the three courses: "
              + ", ".join(f"{k}: {v * 100 / soils:.0f}%" for k, v in sorted(earth_kinds.items())))
    else:
        print("earth: no column carries exactly three courses of the earth materials — state --earth")

    if face := option("--face"):
        fields = dict(part.split("=") for part in face.split(","))
        x0, x1 = span(fields["x"])
        y0, y1 = span(fields["y"])
        z = int(fields["z"])
        print(f"\nface at z={z}, x {x0}..{x1}, y {y0} down to {y1}"
              " (s stone, a andesite, p polished, m mossy, e emerald, c cyan clay, r prismarine, C coarse, P planks, D dirt, G grass,"
              " b stone brick, S slab, w wool, X bedrock, . air, # other)")
        for y in range(max(y0, y1), min(y0, y1) - 1, -1):
            print(f"  y{y:3} " + "".join(FACE_CHARS.get(world.get(x, y, z), "." if world.get(x, y, z)[0] == 0 else "#")
                                        for x in range(x0, x1 + 1)))

    if "--floating" in sys.argv:
        floating = []
        for (x, z), column in columns.items():
            lowest = column[0][0]
            if lowest > 1:
                floating.append((x, z, lowest, column[-1]))
        buckets = Counter((lowest >= 20, top[1]) for _x, _z, lowest, top in floating)
        print(f"\nfloating: {len(floating)} columns whose lowest block is above y1")
        for (high, top_id), count in buckets.most_common(12):
            print(f"  {count:7}  {'from y20 or higher' if high else 'low'}, topped by {name((top_id, 0))}")
        for x, z, lowest, top in sorted(floating)[:8]:
            print(f"  e.g. ({x},{z}) lowest y{lowest}, top {name(top[1:])} at y{top[0]}")


if __name__ == "__main__":
    main()
