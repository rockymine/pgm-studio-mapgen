"""Write the spec for Slipway — a harbour DTM with a ship on the water, a balloon over each headland and a
crane on each quay — for `drive.py` to build.

The board exists to put the made-thing machinery on a map that is actually played rather than on a gallery
deck. Three things are stated three different ways, and the difference is the point:

- the **ship** floats, so it states an absolute floor at the load line and no seat;
- the **balloons** fly, so they state an absolute floor and no seat either;
- the **cranes** stand on a quay that rolls, so they state `seat: "ground"` and settle onto whatever the
  relief left under their feet, one drop for all four of a crane's layers.

The water is the other half. A harbour is an area rather than a stroke and it is dug *down*, so it is a
`pool` — a filled ring — at a stated `level`: the lowest surface a channel crosses would be the basin floor,
and filling to that puts no water in the hole. It names `layer: "ground"` so its bed is the seabed and not
the hull of the ship floating in it.

**The board's size is the four goal rules, not a preference.** `GO4` holds a destroy goal 40–90 blocks from
its own spawn by walk and `GO1` holds the enemy walk at 3–4 times that, which together put the two spawns
roughly 4x the own-walk apart; `GO3` then holds opposing goals to 85–150 and `GO2` a team's own pair to
35–65. Solved together on this shape they give a board 256 x 240 blocks with the goals 60 blocks out from
their spawn and 40 apart.

    python3 tools/sculpt/make_slipway.py specs/opus5-slipway
    python3 tools/drive.py specs/opus5-slipway "Slipway" --out /tmp/slipway
"""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import board
import models
from layers import compile_layers, stats

API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api")

CELL = 4
# Surfaces, in blocks. Every step between neighbouring pieces is a multiple of two (`EL1`).
BASIN, WATER, MARKET, QUAY, TOWN, HEAD, RIDGE = 6, 16, 22, 22, 24, 26, 28

PLAN = {
    "plan": 1,
    "meta": {"name": "Slipway"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 28, "surface": QUAY,
                "observerY": 96},
    # A waterfront in segments rather than one ruled line. `LN2` caps a lane at 110 blocks and rects sharing
    # a cross-axis interval merge into one lane however many pieces they are written as, so the basins sit
    # either side of a slipway, the quays either side of that, and the town is three blocks around a market
    # set forward into it — 80 blocks the longest run, and terrain the relief has something to work with.
    "pieces": [
        {"id": "basin-w",  "role": "piece", "rect": [-24, -6, 20, 12], "surface": BASIN},
        {"id": "slip",     "role": "piece", "rect": [ -4, -6,  8, 13], "surface": BASIN},
        {"id": "basin-e",  "role": "piece", "rect": [  4, -6, 20, 12], "surface": BASIN},
        {"id": "quay-w",   "role": "piece", "rect": [-24,  6, 20,  4], "surface": QUAY},
        {"id": "quay-e",   "role": "piece", "rect": [  4,  6, 20,  4], "surface": QUAY},
        {"id": "town-w",   "role": "piece", "rect": [-22, 10, 14,  8], "surface": TOWN},
        {"id": "market",   "role": "piece", "rect": [ -8,  7, 16, 11], "surface": MARKET},
        {"id": "town-e",   "role": "piece", "rect": [  8, 10, 14,  8], "surface": TOWN},
        {"id": "ridge-w",  "role": "piece", "rect": [-18, 18, 13,  5], "surface": RIDGE},
        {"id": "crest",    "role": "piece", "rect": [ -5, 18, 10,  7], "surface": RIDGE},
        {"id": "ridge-e",  "role": "piece", "rect": [  5, 18, 13,  5], "surface": RIDGE},
        {"id": "spawn",    "role": "spawn", "rect": [ -2, 25,  5,  5], "surface": RIDGE},
        # One arm of the bay; its orbit image closes the other end.
        {"id": "headland", "role": "piece", "rect": [-32, -8,  8, 18], "surface": HEAD},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [2.5, 2.5], "facing": "down"}],
        # Ahead of the spawn rather than behind it (`SP7`): a player leaving for the front passes it.
        "iron":   [{"id": "iron-1", "piece": "spawn", "at": [2.5, 1.0]}],
        # Two a team, in the town. Solved against all four goal bands at once: 56 blocks from their own
        # spawn by walk (`GO4` wants 40-90), 3.2x that from the enemy's (`GO1` wants 3-4), 40 apart from
        # each other (`GO2` wants 35-65) and 126-142 from the pair across the axis (`GO3` wants 85-150).
        "destroyables": [
            {"id": "destroyable-1", "style": "pillar-2", "at": [-5.0, 15.0], "materials": "obsidian",
             "float": 2, "name": "The Sail Loft"},
            {"id": "destroyable-2", "style": "pillar-2", "at": [ 5.0, 15.0], "materials": "obsidian",
             "float": 2, "name": "The Ropewalk"},
        ],
    },
}


def style(name):
    """One of the author's own ground patterns, by the name it was saved under. Fetched rather than
    transcribed: a copy here would be free to disagree with the library the studio paints from."""
    with urllib.request.urlopen(f"{API}/styles?limit=400") as answer:
        rows = json.load(answer)
    for row in rows:
        if row.get("name") == name:
            return json.loads(row["params"])
    raise SystemExit(f"no style named {name!r} in the library")


def ground(surface, wall, rim, fill=None):
    """A terrain theme over four full materials rather than four blocks — which is what the author's styles
    are, so binding one to a bucket is the whole of using them. The surface is one course: `all green` and
    `all sand` are picks, and a pick two courses deep is soil surfaced twice over, which `PT1` refuses."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "boundary",
        "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": rim},
        "surface": {"enabled": True, "depth": 1, "material": surface},
        "wall": wall,
        "wallEnabled": True,
        "fill": fill or wall,
    }


def turn(model, quarter):
    """A model rotated a quarter turn at a time about its own origin, in the plan axes."""
    def spun(x, y, z):
        for _ in range(quarter % 4):
            x, z = -z, x
        return x, y, z
    return {spun(x, y, z): material for (x, y, z), material in model.items()}


def place(model, at, quarter=0):
    dx, dy, dz = at
    return {(x + dx, y + dy, z + dz): material for (x, y, z), material in turn(model, quarter).items()}


def made(name, voxels, seat=None):
    """A model compiled to layers, in the shape `addLayers` takes. `kind`, `prop` and `seat` ride with it."""
    layers = compile_layers(voxels, prefix=f"{name}-", layer_prefix=f"{name}-L", group_name=name,
                            prop=name, seat=seat)
    return [{"id": layer["id"], "name": layer["name"], "base_y": 0, "kind": layer["kind"],
             "prop": layer["prop"], **({"seat": layer["seat"]} if "seat" in layer else {}),
             "shapes": layer["layout"]["shapes"], "groups": layer["layout"]["groups"]}
            for layer in layers], stats(voxels, layers)


def sculpted():
    add_layers, table = [], []

    # The ship lies athwart the basin so both quays see the same broadside, and floats: her load strake sits
    # at the water line and her keel clears the basin floor.
    ship = place(models.ship(), (-5, WATER - 8, 0), quarter=1)
    layers, row = made("ship", ship)
    add_layers += layers
    table.append(("ship", row))

    # A balloon over each headland, just risen off it. Two rather than one because a single one on a rot_180
    # board is the one thing on it that is not answered across the axis. What a made thing costs a played
    # board is build ceiling — the highest column plus twenty — so height here is spent, not free.
    for name, at in [("balloon-w", (-112, HEAD + 2, -8)), ("balloon-e", (112, HEAD + 2, 8))]:
        layers, row = made(name, place(models.balloon(), at))
        add_layers += layers
        table.append((name, row))

    # A crane on each quay, seated. Wholly on the quay rather than overhanging the water, since a seat takes
    # the LOWEST column under the whole footprint and a jib over a sixteen-block drop would settle to the
    # harbour floor.
    for name, at, quarter in [("crane-w", (-56, QUAY, 34), 1), ("crane-e", (56, QUAY, -34), 3)]:
        layers, row = made(name, place(models.crane(), at, quarter), seat="ground")
        add_layers += layers
        table.append((name, row))

    return add_layers, table


def houses():
    """The dockside town, one house per plot. `@name` loads a style out of `tools/styles/`.

    Each is stated once: the dressing pass fans every prop across the symmetry orbit, so a hand-placed image
    lands on the ground the automatic one already claimed and is declined as `DR-CLAIM`. A plot's footprint
    is inclusive of both corners and is capped at 192 blocks — `HP3`'s limit on what one placed building may
    take — so the town is many small sheds rather than a few halls, which is what a working dock is."""
    plots = [
        ("chandler",       "@wh-shed",  (-84, 44), (-72, 56), "negZ"),
        ("workshop",       "@workshop", (-68, 44), (-56, 56), "negZ"),
        ("counting",       "@counting", (-52, 44), (-40, 56), "negZ"),
        ("sailmaker",      "@terrace",  (-84, 60), (-72, 70), "negZ"),
        ("granary",        "@17h-barn", ( 40, 44), ( 52, 56), "negZ"),
        ("cooper",         "@wh-shed",  ( 58, 44), ( 70, 56), "negZ"),
        ("harbour-office", "@17h-hall", ( 74, 44), ( 86, 56), "negZ"),
        ("ropehouse",      "@terrace",  ( 46, 60), ( 58, 70), "negZ"),
    ]
    return [{"id": name, "kind": "house", "seed": 40 + index, "front": front,
             "points": [list(low), list(high)], "style": style_name}
            for index, (name, style_name, low, high, front) in enumerate(plots)]


def trees():
    """Two stands on the ridge behind the town and a scatter along its edges. Stated once each, for the same
    reason a house is: the pass fans them. Every position is on ground the plan actually states, since a tree
    over the void is `DR-SITE`, and a tree keeps its own stand-off from a route, so the roads through the
    town decide where one can go."""
    stands = [(-66, 78), (-58, 86), (-46, 76), (-34, 84), (-24, 78), (24, 80), (34, 86), (46, 76),
              (58, 84), (66, 78), (-14, 88), (14, 90), (-52, 90), (52, 90),
              (-64, 66), (64, 66), (-38, 68), (38, 68), (-14, 76), (14, 76)]
    species = ["oak", "birch", "spruce", "oak", "birch"]
    return [{"id": f"tree-{index}", "kind": "tree", "seed": 200 + index, "x": x, "z": z,
             "form": "template", "species": species[index % len(species)], "height": 9 + (index % 4)}
            for index, (x, z) in enumerate(stands)]


THEMES = {
    "quay":   ground(style("white stone cells"), style("stone dark voronoi"),
                     {"kind": "solid", "id": 98, "data": 0}),
    # Clay turf rather than `all green`: `all green` mixes wool into its palette, the dressing pass reads
    # wool as a stamp's own block, and a tree on it is declined as built ground rather than terrain.
    "town":   ground(style("grass clay surface"), style("dirt clay fill"),
                     {"kind": "solid", "id": 5, "data": 1}),
    "ridge":  ground(style("grass clay surface"), style("stone fractal"),
                     {"kind": "solid", "id": 4, "data": 0}),
    "head":   ground(style("terracotta with dirt"), style("stone fractal"),
                     {"kind": "solid", "id": 98, "data": 3}),
    "seabed": ground(style("all sand"), style("dirt fractal"),
                     {"kind": "solid", "id": 24, "data": 0}),

    # A made thing is painted in solids: the painter's buckets are a model of ground — a rim capping every
    # plateau boundary, a wall down every riser — and a curved form is nothing but boundaries, so a shaded
    # theme speckles it.
    "hull": board.solid(5, 1), "strake": board.solid(35, 14), "rail": board.solid(5, 0),
    "deck": board.solid(5, 2), "spar": board.solid(17, 1), "rig": board.solid(35, 15),
    "canvas": board.solid(155, 0), "glass": board.solid(95, 3), "lamp": board.solid(89, 0),

    "envelope-a": board.solid(35, 14), "envelope-b": board.solid(35, 0),
    "envelope-band": board.solid(35, 11), "wicker": board.solid(5, 4), "flame": board.solid(89, 0),

    "stone": board.solid(98, 0), "iron": board.solid(35, 15), "chain": board.solid(1, 6),
    "timber": board.solid(5, 1),
}


def finish(add_layers):
    return {
        "authors": ["Opus 5"],
        "created": "2026-08-29",
        "themeByHeight": {str(BASIN): "seabed", str(QUAY): "quay", str(TOWN): "town",
                          str(HEAD): "head", str(RIDGE): "ridge"},
        "mapTheme": "quay",
        "themes": THEMES,
        "addLayers": add_layers,
        # The ground the plan states is a set of plateaus; the relief is what makes it terrain. `reach` 26 is
        # what shelves the quay into the basin over a beach rather than dropping it down a sixteen-block
        # wall, and the marks behind it roll the town so the cranes have something to seat onto.
        "relief": {"team": {"base": TOWN, "reach": 26, "step": 1, "stairs": True, "marks": [
            {"id": "harbour-floor", "kind": "area", "h": BASIN,
             "ring": [[-90, -22], [90, -22], [90, 22], [-90, 22]]},
            {"id": "quay-line", "kind": "line", "h": QUAY,
             "points": [[-92, 30], [-40, 29], [0, 30], [40, 29], [92, 30]]},
            {"id": "town-roll", "kind": "area", "h": TOWN + 2,
             "ring": [[-84, 52], [-30, 50], [-24, 70], [-80, 72]]},
            {"id": "market-dip", "kind": "point", "at": [0, 62], "h": TOWN - 1, "r": 14},
            {"id": "town-rise", "kind": "area", "h": TOWN + 3,
             "ring": [[30, 52], [84, 54], [80, 72], [26, 70]]},
            {"id": "ridge-crown", "kind": "line", "h": RIDGE + 4,
             "points": [[-70, 92], [-20, 96], [20, 94], [70, 92]]},
            {"id": "head-crown", "kind": "point", "at": [-112, 0], "h": HEAD + 5, "r": 18},
        ]}},
        "dressing": {"props": [
            # The harbour: a filled ring at a stated level, on the ground layer so its bed is the seabed and
            # not the hull of the ship floating in it. `radius` on a pool is the shelf — how far in from the
            # shore the bed reaches full depth — so the water shallows against the quays.
            {"id": "harbour", "kind": "water", "seed": 7, "layer": "ground", "shape": "pool",
             "points": [[-92, -26], [92, -26], [92, 26], [-92, 26]],
             "radius": 14, "depth": 6, "shore": 3, "shoreWander": True, "edge": 1.2, "level": WATER,
             "bank": {"kind": "voronoi", "seed": 3, "cellSize": 6, "bands": [
                 {"material": {"kind": "solid", "id": 13, "data": 0}, "thickness": 2},
                 {"material": {"kind": "solid", "id": 3, "data": 1}, "thickness": 1},
                 {"material": {"kind": "solid", "id": 12, "data": 0}, "thickness": 1}]}},
            # The quay road, and the two lanes out of the town onto the ridge.
            {"id": "quay-road", "kind": "path", "seed": 3, "route": True, "radius": 3, "coverage": 0.95,
             "points": [[-88, 36], [-40, 35], [0, 36], [40, 35], [88, 36]],
             "pave": {"kind": "solid", "id": 98, "data": 0}},
            {"id": "town-road", "kind": "path", "seed": 4, "route": True, "radius": 3, "coverage": 0.9,
             "points": [[-34, 40], [-18, 52], [0, 64], [18, 52], [34, 40]],
             "pave": {"kind": "solid", "id": 4, "data": 0}},
            {"id": "spawn-road", "kind": "path", "seed": 5, "route": True, "radius": 3, "coverage": 0.9,
             "points": [[0, 64], [0, 88], [0, 108]],
             "pave": {"kind": "solid", "id": 4, "data": 0}},
        ] + houses() + trees()},
        "voidEnforcement": True,
    }


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "specs/opus5-slipway"
    slug = os.path.basename(os.path.abspath(out))
    os.makedirs(out, exist_ok=True)

    add_layers, table = sculpted()
    json.dump(PLAN, open(f"{out}/{slug}.plan.json", "w"), indent=2)
    json.dump(finish(add_layers), open(f"{out}/{slug}.finish.json", "w"), indent=2)

    width = max(len(name) for name, _ in table)
    print(f"{'model':<{width}}  {'blocks':>7} {'layers':>7} {'shapes':>7} {'b/shape':>8}")
    for name, row in table:
        print(f"{name:<{width}}  {row['blocks']:>7} {row['layers']:>7} {row['shapes']:>7} "
              f"{row['blocks_per_shape']:>8}")
    print(f"\nspec written to {out}/ ({len(add_layers)} added layers)")


if __name__ == "__main__":
    main()
