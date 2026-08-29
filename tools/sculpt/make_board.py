"""Write the spec for a board furnished with sculpted props, for `drive.py` to build.

The finish's `addLayers` takes the storeys a plan cannot state, and that is exactly what a prop is: a set of
layers with a floor at the board's surface. So nothing about the studio has to change for a sculpture to
stand on a compiled plan — the props are generated here, written into `<slug>.finish.json`, and the ordinary
driver does the rest.

    python3 tools/sculpt/make_board.py specs/opus5-automaton
    python3 tools/drive.py specs/opus5-automaton "Automaton" --out /tmp/automaton
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import board
import models
import props
from layers import compile_layers, stats

SURFACE = 9                                               # the plan's own surface, and every prop's floor
CELL = 5

PLAN = {
    "plan": 1,
    "meta": {"name": "Automaton"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 12, "surface": SURFACE,
                "observerY": 60},
    "pieces": [
        {"id": "field", "role": "piece", "rect": [-11, -11, 22, 22]},
        {"id": "camp", "role": "spawn", "rect": [-4, 6, 8, 5]},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "camp", "at": [2, 2], "facing": "front"}],
        "destroyables": [{"id": "destroyable-1", "style": "pillar-2", "at": [0, 5],
                          "materials": "obsidian", "float": 2, "name": "The Governor"}],
    },
}

THEMES = {
    "meadow": board.shaded(surface=(2, 0), wall=(3, 0), rim=(3, 1)),
    # The props state one block a material. A three-tone theme is a model of ground — a rim capping every
    # plateau boundary, a wall down every riser — and a curved form is nothing but boundaries, so it speckles.
    "brass": board.solid(155, 0),
    "brass-trim": board.solid(35, 1),
    "brass-joint": board.solid(1, 6),
    "brass-panel": board.solid(35, 3),
    "brass-visor": board.solid(168, 2),
    "brass-eye": board.solid(35, 4),
    "granite": board.shaded(surface=(1, 4), wall=(24, 2), rim=(24, 0)),
    "robe": board.solid(159, 8),
    "fold": board.solid(159, 7),
    "hood": board.solid(159, 9),
    "shadow": board.solid(49, 0),
    "iron": board.solid(42, 0),
    "flame": board.solid(89, 0),
    "tile": board.shaded(surface=(24, 2), wall=(24, 0), rim=(172, 0)),
    "slate": board.shaded(surface=(1, 6), wall=(98, 0), rim=(98, 3)),
    "clay-roof": board.shaded(surface=(159, 1), wall=(179, 0), rim=(159, 14)),
}

ROBOT_THEME = {"shell": "brass", "trim": "brass-trim", "joint": "brass-joint",
               "panel": "brass-panel", "visor": "brass-visor", "eye": "brass-eye"}
STATUE_THEME = {"stone": "granite", "robe": "robe", "fold": "fold", "hood": "hood",
                "dark": "shadow", "metal": "iron", "flame": "flame"}


def turn(model, quarter):
    """A voxel model spun about its own origin in quarter turns, so a prop can face where it is put."""
    out = {}
    for (x, y, z), material in model.items():
        for _ in range(quarter % 4):
            x, z = -z - 1, x
        out[(x, y, z)] = material
    return out


def place(model, at, palette, quarter=0):
    """One model, turned, moved onto the board and repainted into the board's theme registry."""
    dx, dy, dz = at
    return {(x + dx, y + dy, z + dz): palette[material]
            for (x, y, z), material in turn(model, quarter).items()}


def sculpted(name, voxels, mirrors):
    made = compile_layers(voxels, prefix=f"{name}-", layer_prefix=f"{name}-L",
                          mirrors=mirrors, island_name=name)
    return [{"id": layer["id"], "name": layer["name"], "base_y": 0,
             "shapes": layer["layout"]["shapes"], "islands": layer["layout"]["islands"]}
            for layer in made], stats(voxels, made)


def native(made, mirrors):
    """A prop already written in sketch shapes only needs its island's mirror flag set."""
    out = []
    for layer in (made if isinstance(made, list) else [made]):
        for island in layer["layout"]["islands"]:
            island["mirrors"] = mirrors
        out.append({"id": layer["id"], "name": layer["name"], "base_y": layer["base_y"],
                    "shapes": layer["layout"]["shapes"], "islands": layer["layout"]["islands"]})
    return out


def build():
    add_layers, table = [], []

    # The colossus stands on the symmetry centre, so it is its own image and is drawn once.
    colossus = place(models.robot(), (0, SURFACE + 3, 0), ROBOT_THEME)
    made, row = sculpted("colossus", colossus, mirrors=False)
    add_layers += made
    table.append(("colossus", row))
    add_layers += native(props.ziggurat("colossus-plinth", 0, 0, 15, SURFACE, 3, 1, 4, "granite",
                                        mirrors=False, name="Colossus plinth"), mirrors=False)

    # Two sentinels flank each spawn approach, facing the middle of the board. Authored on the north half
    # and fanned, which is what the mirror is for.
    sentinels = {}
    for x in (-30, 30):
        sentinels.update(place(models.statue(), (x, SURFACE, -18), STATUE_THEME, quarter=2))
    made, row = sculpted("sentinel", sentinels, mirrors=True)
    add_layers += made
    table.append(("sentinels (x2, fanned to x4)", row))

    # Everything below is written in sketch shapes rather than compiled, so it stays editable in Draw.
    # Everything is authored on the north half and fanned. A square-ish board centred on the mirror is where
    # `rot_180` bites: a shape has to clear every *other* shape's image as well as the shapes themselves.
    add_layers += native(props.ring_wall("rotunda", -42, -42, 11, 2, SURFACE, 13, "tile",
                                         doors=[(135, 6), (315, 5)], inner_floor="slate",
                                         name="Rotunda wall"), mirrors=True)
    add_layers += native(props.spire("rotunda-roof", -42, -42, 13, SURFACE + 13, 9, "clay-roof",
                                     steps=9, name="Rotunda roof"), mirrors=True)

    add_layers += native(props.tapered_tower("watchtower", 40, -42, 9, 6, 2, SURFACE, 26, "slate",
                                             courses=6, name="Watchtower"), mirrors=True)



    return add_layers, table


FINISH_HEAD = {
    "authors": ["Opus 5"],
    "created": "2026-08-28",
    "themes": THEMES,
    "mapTheme": "meadow",
    "roomStyles": {"spawn": "@showcase-hall"},
    # The board is flat, and that is a finding rather than a taste. A prop states an absolute floor, and a
    # relief moves the ground under it — so on rolling ground a prop either floats or is buried, and SK10
    # names every one of them. Seating a prop needs the *solved* surface, which nothing in the document can
    # state; the two-pass fix is written up in docs/sculpting-with-layers.md.
}


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "specs/opus5-automaton"
    slug = os.path.basename(out)
    os.makedirs(out, exist_ok=True)

    add_layers, table = build()
    finish = dict(FINISH_HEAD)
    finish["addLayers"] = add_layers

    json.dump(PLAN, open(f"{out}/{slug}.plan.json", "w"), indent=1)
    json.dump(finish, open(f"{out}/{slug}.finish.json", "w"), indent=1)

    shapes = sum(len(layer["shapes"]) for layer in add_layers)
    print(f"{len(add_layers)} prop layers, {shapes} shapes")
    for name, row in table:
        print(f"  {name:<30} {row['blocks']:>7} blocks  {row['layers']:>3} layers  "
              f"{row['shapes']:>5} shapes")
    print("wrote", f"{out}/{slug}.plan.json", "and", f"{out}/{slug}.finish.json")
