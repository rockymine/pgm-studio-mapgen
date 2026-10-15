"""Every study as a world to walk round and take parts from: one world a subject, its forms laid out side by side.

    python3 studies/worlds.py                  # every world
    python3 studies/worlds.py volcanoes        # one of them

Each form is built the way its own study builds it, by its own functions, so the world is the study's renders in
blocks. A subject's forms stand on a grid 40 blocks apart, six to a row, each round of a study in its own band of
rows, round one first; a sign at each form's spawn names its study and form. The world is written through the
studio's Anvil writer to `maps/other/studies_<subject>/` as a `level.dat` and `region/`, with no map.xml, and its row
added to `maps/INDEX.md`. A visitor arrives at the first form; a dungeon's spot is a floor inside it.
"""
import importlib
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(LIB))
sys.path[:0] = [LIB, os.path.join(REPO, "tools")]
from pgmvox import World  # noqa: E402
from pgmvox.core.blocks import NOT_GROUND, LIQUID  # noqa: E402
from pgmvox.core.world import write  # noqa: E402
import worlds as INDEX  # noqa: E402


def module(folder, name):
    """A study's script, imported from its own folder."""
    path = os.path.join(HERE, folder, "scripts")
    if path not in sys.path:
        sys.path.insert(0, path)
    return importlib.import_module(name)


# Each study as (folder, the forms it draws, and how one form becomes a World), mirroring the study's own main().
def volcanoes(round_name):
    V = module("volcanoes", "volcanoes")
    forms = V.STUDIES if round_name == "volcanoes" else module("volcanoes", "round2").STUDIES

    def built(f):
        X, Z = V.grid()[1:]
        got = f(X, Z)
        H, bottom = got if isinstance(got, tuple) else (got, None)
        return V.build(H, bottom)[0]
    return forms, built


def winter(_):
    W = module("winter", "winter")
    return W.STUDIES, lambda f: W.build(f(*W.grid()[1:]))[0]


def combinations(_):
    C = module("combinations", "combos")
    return C.STUDIES, lambda f: C.build(f(*C.grid()))


def water(round_name):
    W = module("water", "water")
    forms = W.STUDIES if round_name == "water" else module("water", "water2").STUDIES
    return forms, lambda f: W.build(f(*W.grid()))


def dungeon_layouts(_):
    D = module("dungeons", "dungeons")
    return D.STUDIES, lambda f: D.build(*f())


def dungeon_deep(_):
    P = module("dungeons", "deep")
    rng = np.random.default_rng(1)

    def built(f):
        dp, key = f()
        w, _ = P.carve(dp, P.PACKS[key])
        P.finish(w, dp, P.PACKS[key], rng)
        return w
    return [P.dungeon, P.crypt, P.bunker], built


# The subjects, each its studies in the order their rounds stand in the world.
SUBJECTS = {
    "volcanoes": [("volcanoes round 1", lambda: volcanoes("volcanoes"), False),
                  ("volcanoes round 2", lambda: volcanoes("round2"), False)],
    "winter": [("winter", lambda: winter(None), False)],
    "combinations": [("combinations", lambda: combinations(None), False)],
    "water": [("water round 1", lambda: water("water"), False), ("water round 2", lambda: water("water2"), False)],
    "dungeons": [("dungeon layouts", lambda: dungeon_layouts(None), True),
                 ("dungeons deep", lambda: dungeon_deep(None), True)],
}
SOURCE = {"volcanoes": "volcanoes", "winter": "winter", "combinations": "combinations", "water": "water",
          "dungeons": "dungeons"}
GAP, COLUMNS = 40, 6

def standable(w, x, y, z):
    """Solid ground at y that is not liquid or loose, and two blocks of air over it."""
    ground = w.get(x, y, z)[0]
    return (ground not in NOT_GROUND and ground not in LIQUID
            and w.get(x, y + 1, z)[0] == 0 and w.get(x, y + 2, z)[0] == 0)


def spawn(w, inside):
    """Where a visitor arrives: on the surface nearest the south middle of the form, or for a dungeon the lowest
    floor with a roof over it."""
    xs = np.arange(w.x0 + 2, w.x0 + w.sx - 2, 2)
    zs = np.arange(w.z0 + 2, w.z0 + w.sz - 2, 2)
    target = (w.x0 + w.sx // 2, w.z0 + w.sz - 20)
    for x, z in sorted(((x, z) for x in xs for z in zs), key=lambda c: (c[0] - target[0]) ** 2 + (c[1] - target[1]) ** 2):
        column = w.ids[x - w.x0, :, z - w.z0]
        solid = np.nonzero(column)[0]
        if not len(solid):
            continue
        if inside:
            for y in solid:
                if standable(w, x, y, z) and column[y + 3:].any():
                    return int(x), int(y) + 1, int(z)
            continue
        y = int(solid.max())
        if standable(w, x, y, z):
            return int(x), y + 1, int(z)
    raise SystemExit("no ground to stand on")


def index(world, source):
    """The world's row in `maps/INDEX.md`, the subject's study folder as its board and its source, keyed by the
    world."""
    rows = [row for row in INDEX.rows() if row[0] != world] + [(world, source, source)]
    INDEX.write(rows)


def export(subject):
    """Build every form of a subject, lay them out on one grid, and write the world."""
    placed, row = [], 0
    for study, forms_of, inside in SUBJECTS[subject]:
        forms, built = forms_of()
        for k, f in enumerate(forms):
            w = built(f)
            placed.append((study, f.__name__, w, inside, k % COLUMNS, row + k // COLUMNS))
            print(f"  built {study}: {f.__name__}", flush=True)
        row += (len(forms) + COLUMNS - 1) // COLUMNS
    cell_x = max(w.sx for _, _, w, *_ in placed) + GAP
    cell_z = max(w.sz for _, _, w, *_ in placed) + GAP
    columns = max(c for *_, c, _ in placed) + 1
    first = placed[0][2]
    world = World(first.x0, first.z0, columns * cell_x - GAP, row * cell_z - GAP, sy=max(w.sy for _, _, w, *_ in placed))
    arrival = None
    for study, name, w, inside, col, r in placed:
        dx, dz = col * cell_x + first.x0 - w.x0, r * cell_z + first.z0 - w.z0
        i, k = w.x0 + dx - world.x0, w.z0 + dz - world.z0
        world.ids[i:i + w.sx, :w.sy, k:k + w.sz] = w.ids
        world.dat[i:i + w.sx, :w.sy, k:k + w.sz] = w.dat
        world.biome[i:i + w.sx, k:k + w.sz] = w.biome
        world.tiles += [{**t, "x": t["x"] + dx, "z": t["z"] + dz} for t in w.tiles]
        x, y, z = spawn(w, inside)
        x, z = x + dx, z + dz
        if world.get(x + 1, y, z)[0] == 0 and world.get(x + 1, y - 1, z)[0] != 0:
            world.sign(x + 1, y, z, [study, name.replace("_", " "), f"at {x} {z}", "pgmvox study"], rot=4)
        arrival = arrival or (x, y, z)
        print(f"  {study:18s} {name:16s} spawn {x:5d} {y:4d} {z:5d}")
        del w
    folder = f"other/studies_{subject}"
    with tempfile.TemporaryDirectory() as build:
        world.save(build, f"Studies: {subject}", arrival)
        said = write(build, os.path.join(INDEX.WORLDS, folder))
    index(folder, f"freeform/lib/studies/{SOURCE[subject]}")
    print(f"{folder}: {said}")


if __name__ == "__main__":
    for subject in sys.argv[1:] or list(SUBJECTS):
        export(subject)
