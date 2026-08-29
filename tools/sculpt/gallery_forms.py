"""The form gallery — eight structures written in the sketch's own shapes, on one board.

Each is a candidate for a stamper the way the house already is one: a footprint, a few numbers, and the
shapes come out editable in the Draw phase. What the board is for is the shape count under each — a dome of
radius 11 is twelve circles on one layer, and that is the number that decides whether a form belongs in the
tool or in a compiler.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "render"))

import board
import props

THEMES = {
    "ground": board.shaded(surface=(2, 0), wall=(3, 0), rim=(4, 0)),
    "pale": board.shaded(surface=(155, 0), wall=(1, 3), rim=(1, 4)),
    "grey": board.shaded(surface=(1, 6), wall=(98, 0), rim=(98, 3)),
    "warm": board.shaded(surface=(24, 2), wall=(24, 0), rim=(172, 0)),
    "rust": board.shaded(surface=(159, 1), wall=(179, 0), rim=(159, 14)),
    "dark": board.shaded(surface=(1, 5), wall=(159, 7), rim=(49, 0)),
    "moss": board.shaded(surface=(48, 0), wall=(98, 1), rim=(98, 2)),
}

PLINTH = 6                                                # every form stands on the same six-block plinth
SPAWN = (0, PLINTH + 1, 58)


def deck():
    """The board itself: one wide plate for everything to stand on, and the visitors' pad at the south edge —
    `EX2` refuses to export a map no player can enter."""
    ground = props.LayerBuilder("deck", name="Deck")
    ground.rect(-70, -46, 70, 66, 0, PLINTH, "ground")
    ground.rect(SPAWN[0] - 9, SPAWN[2] - 5, SPAWN[0] + 9, SPAWN[2] + 5, 0, PLINTH + 1, "pale")
    return ground.done()


def build():
    layers = [deck()]
    notes = []

    def take(made, label):
        added = made if isinstance(made, list) else [made]
        layers.extend(added)
        shapes = sum(len(entry["layout"]["shapes"]) for entry in added)
        notes.append((label, len(added), shapes))

    take(props.ring_wall("roundhouse", -52, -26, 11, 2, PLINTH, 12, "warm",
                         doors=[(180, 5), (0, 4)], inner_floor="dark",
                         name="Roundhouse wall"), "roundhouse wall")
    take(props.spire("roundhouse-roof", -52, -26, 13, PLINTH + 12, 9, "rust", steps=9),
         "roundhouse roof")

    take(props.dome("dome", -18, -26, 13, PLINTH, "pale", thickness=3, steps=13), "hollow dome")

    take(props.ellipse_wall("oval", 18, -26, 15, 9, 2, PLINTH, 11, "grey", rotate=20,
                            inner_floor="warm", name="Hollow ellipse"), "hollow ellipse")

    take(props.tapered_tower("tower", 52, -26, 10, 6, 2, PLINTH, 30, "grey", courses=6), "tapered tower")

    take(props.ziggurat("zigg", -52, 24, 14, PLINTH, 5, 4, 3, "warm"), "ziggurat")

    take(props.arch("arch", -26, -4, 24, 4, PLINTH, 12, 8, "pale", steps=9), "arch")

    take(props.colonnade("peristyle", 22, 24, 12, 12, 1.6, PLINTH, 13, "pale"), "colonnade")
    take(props.dome("peristyle-roof", 22, 24, 15, PLINTH + 13, "warm", squash=0.42, steps=12),
         "colonnade roof")

    take(props.bowl("bowl", 56, 24, 14, PLINTH + 14, 11, "moss", steps=6, seat=2), "amphitheatre")

    return layers, notes


if __name__ == "__main__":
    layers, notes = build()
    document = board.layout(layers, THEMES, map_theme="ground", mirror="none", room_styles=None)

    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/forms"
    world = sys.argv[2] if len(sys.argv) > 2 else None
    os.makedirs(out, exist_ok=True)
    json.dump(document, open(f"{out}/forms.layout.json", "w"), indent=1)

    print(f"{'form':<22} {'layers':>7} {'shapes':>7}")
    for label, layer_count, shape_count in notes:
        print(f"{label:<22} {layer_count:>7} {shape_count:>7}")
    print(f"{'TOTAL':<22} {len(layers):>7} "
          f"{sum(len(l['layout']['shapes']) for l in layers):>7}")

    board.store("form-gallery", "Form Gallery", document, spawn=SPAWN,
                observer=(0, PLINTH + 60, 90))
    payload = board.columns("form-gallery", document)
    json.dump(payload, open(f"{out}/forms.columns.json", "w"))
    if world:
        board.export("form-gallery", world)

    import iso
    print(iso.isometric(payload, f"{out}/forms-iso.png", scale=4, quarter=2,
                        title="forms drawn in sketch shapes",
                        caption="every structure here is circles, polygons and rectangles on a layer"))
    for label, x, z, reach in (("roundhouse", -52, -26, 20), ("dome", -18, -26, 18),
                               ("ellipse", 18, -26, 20), ("tower", 52, -26, 16),
                               ("ziggurat", -52, 24, 20), ("arch", -15, 24, 26),
                               ("peristyle", 22, 24, 20), ("amphitheatre", 56, 24, 20)):
        iso.isometric(payload, f"{out}/form-{label}.png", scale=7, quarter=2,
                      clip=(x - reach, x + reach, PLINTH - 1, None, z - reach, z + reach), title=label)
