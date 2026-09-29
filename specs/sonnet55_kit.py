"""What the 2026-09-29 run's two boards share beyond the shared authoring kit beside it: block ids by name and a house style forked by
repainting. Like the kit it builds on, nothing here reads a built world or computes a
placement — it writes pieces of a finish document and nothing else.
"""
import copy, json, os
from opus55_kit import S, cell, noise, depth, by_slope, beds, theme, one, ROCK, ROOT  # noqa: F401  (re-exported)

# block ids the two boards paint with
GRASS, DIRT, STONE, COBBLE, GRAVEL, SAND, CLAY, BRICKS, HAY = 2, 3, 1, 4, 13, 12, 82, 98, 170
COARSE, PODZOL = (DIRT, 1), (DIRT, 2)
ANDESITE, POL_ANDESITE = (STONE, 5), (STONE, 6)
JUNGLE_PLANK, DARKOAK_PLANK, SPRUCE_PLANK = (5, 3), (5, 5), (5, 1)
JUNGLE_LOG, DARKOAK_LOG = (17, 3), (162, 1)


def repaint(style, solids=None, blocks=None, roof_body=None, slabs=None, beams=None):
    """A shipped house style forked by repainting: `solids` maps (id, data) to (id, data) wherever a material
    of kind solid, laidLog or checker names it; `blocks` maps a stair/window block id to another; `roof_body`
    replaces the roof's body material outright, and `beams` the block the beam ends are cut from (one wood with the posts, `HS4`). Returns a new style and leaves the shipped one alone."""
    style = copy.deepcopy(style)
    solids, blocks, slabs = solids or {}, blocks or {}, slabs or {}

    def walk(o):
        if isinstance(o, dict):
            if o.get("kind") in ("solid", "laidLog") and "id" in o:
                new = solids.get((o["id"], o.get("data", 0)))
                if new:
                    o["id"], o["data"] = new
            for k in ("block", "fillBlock", "hostBlock"):
                if isinstance(o.get(k), int) and o[k] in blocks:
                    o[k] = blocks[o[k]]
            if isinstance(o.get("slab"), int) and (o["slab"], o.get("slabData", 0)) in slabs:
                o["slab"], o["slabData"] = slabs[(o["slab"], o.get("slabData", 0))]
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(style)
    if beams is not None and style.get("beams"):
        style["beams"]["block"], style["beams"]["data"] = beams
    if roof_body is not None:
        style["roof"]["body"] = roof_body
        if style["roof"].get("verge"):
            style["roof"]["verge"] = roof_body
    return style


def shipped(name):
    return json.load(open(os.path.join(ROOT, "tools", "styles", f"{name}.json")))
