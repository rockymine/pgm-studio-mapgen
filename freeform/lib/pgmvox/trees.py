"""Trees: hand-built trees planted whole, from the studio's tree library or a board's own cut.

    lib = library()                                  # the studio's copied trees, by name ("oak-3", "birch-7")
    by = kinds(lib)                                  # {"oak": [...], "birch": [...], "tiny-oak": [...]}
    plant(w, x, z, by["birch"][2], turn=1)           # one tree, its foot on the ground at (x, z)
    scatter(w, zone, by, {"oak": 0.3, "birch": 0.7}, rng, planted=placed)   # a wood, crowns spaced

**A tree is planted whole, as its author built it, or not at all.** Its blocks are offsets from its foot, the
lowest wood block, and every block on that lowest row rests on the ground: the tree stands on the lowest ground
under that row, as the studio's own stamp seats it. A block that would land in anything but air or plants refuses
the whole tree, except ground and rock, which a crown meeting a hillside gives way to. Leaves are written with the
no-decay bit, so a crown never rots.

**A turned tree turns its blocks with it.** A quarter turn moves every offset and turns each block's data with
`orient.turn_data`, so a lying log's axis and a stair's facing follow the body rather than staying as cut.

**A wood is scattered with its crowns apart.** Two trees stand no nearer than `spacing` times the sum of their
crown radii, so a wood reads as trees and not one mass of leaves; a spacing under one lets crowns touch.
"""
import json
import os
import re
from dataclasses import dataclass

import numpy as np

from .blocks import B
from .orient import turn_data
from .world import studio_root

LEAVES = (B.LEAVES, B.LEAVES2)
WOOD = (B.LOG, B.LOG2)
PLANTS = {B.AIR, B.TALLGRASS, B.FLOWER, B.DANDELION, B.DOUBLE_PLANT, B.LEAVES, B.LEAVES2, B.VINE}
GIVES_WAY = {B.GRASS, B.DIRT, B.STONE, B.COBBLE, B.GRAVEL}      # a crown meeting a hillside: the hill wins
NO_DECAY = 4


@dataclass(frozen=True)
class Tree:
    name: str
    kind: str                     # the name without its number: "oak", "tiny-spruce"
    blocks: tuple                 # ((dx, dy, dz, id, data), ...) from the foot
    crown: int                    # the leaves' reach from the foot, in blocks
    height: int
    builder: str | None = None


def _tree(name, kind, rows, builder=None):
    rows = tuple(tuple(int(v) for v in r[:5]) for r in rows if len(r) >= 5 and r[3] != B.AIR)
    leaves = [max(abs(r[0]), abs(r[2])) for r in rows if r[3] in LEAVES]
    ys = [r[1] for r in rows]
    return Tree(name, kind, rows, max(leaves) if leaves else 0, max(ys) - min(ys) + 1 if ys else 0, builder)


def library(path=None):
    """The studio's copied trees, {name: Tree}, from its Library/trees.json (path overrides where)."""
    path = path or os.path.join(studio_root(), "src", "PgmStudio.Minecraft", "Library", "trees.json")
    with open(path) as f:
        doc = json.load(f)
    out = {}
    for name, entry in doc["trees"].items():
        style = entry["style"]
        if style.get("body"):
            out[name] = _tree(name, re.sub(r"-\d+$", "", name), style["body"], style.get("builder"))
    return out


def load(path):
    """A board's own cut, {kind: [{"blocks": [...]}, ...]}, as {name: Tree} named kind-1, kind-2, ..."""
    with open(path) as f:
        doc = json.load(f)
    return {f"{kind}-{i + 1}": _tree(f"{kind}-{i + 1}", kind, t["blocks"])
            for kind, ts in doc.items() for i, t in enumerate(ts)}


def kinds(lib):
    """{kind: [Tree, ...]} in name order."""
    out = {}
    for name in sorted(lib, key=lambda n: (lib[n].kind, int(re.findall(r"\d+$", n)[0]) if re.findall(r"\d+$", n) else 0)):
        out.setdefault(lib[name].kind, []).append(lib[name])
    return out


def turned(tree, turn):
    """The tree's blocks after `turn` quarter turns clockwise seen from above (x, z) -> (-z, x)."""
    out = []
    for dx, dy, dz, i, d in tree.blocks:
        for _ in range(turn % 4):
            dx, dz = -dz, dx
            d = turn_data(i, d, "cw")
        out.append((dx, dy, dz, i, d))
    return out


def plant(w, x, z, tree, turn=0, allowed=None, through=PLANTS, gives_way=GIVES_WAY):
    """Plant `tree` with its foot at (x, z), turned `turn` quarter turns. allowed(x, z) may refuse a column any
    block of it would stand in. Returns True if it stood, False (and nothing written) if it was refused."""
    body = turned(tree, turn)
    if not body:
        return False
    rest = min(b[1] for b in body)
    tops = [w.top(x + dx, z + dz) for dx, dy, dz, _, _ in body if dy == rest]
    if min(tops) < 0:
        return False
    base = min(tops) + 1 - rest
    cells = []
    for dx, dy, dz, i, d in body:
        X, Y, Z = x + dx, base + dy, z + dz
        if not w.inside(X, Y, Z) or (allowed is not None and not allowed(X, Z)):
            return False
        cur = w.id(X, Y, Z)
        if cur in gives_way:
            continue
        if cur not in through:
            return False
        cells.append((X, Y, Z, i, (d & 3) | NO_DECAY if i in LEAVES else d))
    for X, Y, Z, i, d in cells:
        if i in LEAVES and w.id(X, Y, Z) in LEAVES:
            continue                                            # a crown meeting a crown keeps the first
        w.set(X, Y, Z, i, d)
    for dx, dy, dz, i, _ in body:
        if dy == rest and i in WOOD and w.id(x + dx, base - 1 + rest, z + dz) == B.GRASS:
            w.set(x + dx, base - 1 + rest, z + dz, B.DIRT)        # no grass under a trunk
    return True


def scatter(w, zone, by_kind, weights, rng, spacing=0.85, tries=4000, planted=None, ok=None, allowed=None):
    """Plant a wood over zone (a mask over the world's columns): up to `tries` shuffled cells, each a tree of a
    kind drawn by `weights` ({kind: share}), a random one of that kind and a random quarter turn, kept only if its
    crown is `spacing` of the crown radii clear of every tree in `planted` [(x, z, radius), ...] (which it adds
    to) and ok(x, z, tree) allows it. Returns how many stood."""
    planted = [] if planted is None else planted
    X, Z = w.grid()
    names = list(weights)
    p = np.array([weights[k] for k in names], float)
    p /= p.sum()
    cells = np.argwhere(zone)
    rng.shuffle(cells)
    n = 0
    for i, k in cells[:tries]:
        x, z = int(X[i, k]), int(Z[i, k])
        group = by_kind[names[int(rng.choice(len(names), p=p))]]
        t = group[int(rng.integers(len(group)))]
        c = t.crown * 0.5
        if any((x - px) ** 2 + (z - pz) ** 2 < ((c + pc) * spacing) ** 2 for px, pz, pc in planted):
            continue
        if ok is not None and not ok(x, z, t):
            continue
        if plant(w, x, z, t, int(rng.integers(4)), allowed):
            planted.append((x, z, c))
            n += 1
    return n


def dead_tree(w, x, y, z, rng, h, log=B.LOG2, kind=1):
    """A bare tree on the floor at y: a trunk h high, three to five arms leaning out of its upper half, each ending
    in a stub. No leaves. An arm fills only air and low plants."""
    import math
    for k in range(1, h + 1):
        w.set(x, y + k, z, log, kind)
    n = int(rng.integers(3, 6))
    for _ in range(n):
        a = rng.uniform(0, 2 * math.pi)
        dx, dz = round(math.cos(a)), round(math.sin(a))
        if (dx, dz) == (0, 0):
            dx = 1
        y0 = y + int(rng.integers(max(2, h // 2), h))
        reach = int(rng.integers(2, 4))
        for s in range(1, reach + 1):
            bx, bz, by = x + dx * s, z + dz * s, y0 + (s // 2)
            if w.id(bx, by, bz) in (B.AIR, B.TALLGRASS, B.DEADBUSH):
                w.set(bx, by, bz, log, (kind | (4 if abs(dx) >= abs(dz) else 8)) if s < reach else kind)
        if rng.random() < 0.5:
            w.set(x + dx * reach, y0 + reach // 2 + 1, z + dz * reach, log, kind)
