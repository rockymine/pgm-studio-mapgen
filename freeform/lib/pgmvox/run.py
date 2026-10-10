"""Build a freeform board from nothing, in the order every board's build.sh ran it:

    plan_check.py  > renders/plan-check.txt      (if the board has one)
    sketch.py        renders/00-plan-sketch.png
    gen.py           <build-dir>                 (saves volume.bin, tiles.json, level.json)
    write            region/ and level.dat in the board's world folder, through the studio's Anvil writer
    mapxml.py      > scripts/map.xml and the world folder's map.xml
    renders.py       <build-dir> <board-dir>      (if the board has one)
    walk.py        > renders/walks.txt            (if the board has one)

and writes renders/build-info.txt with the library version, so a board records what it was built with.

The world folder is the one `maps/INDEX.md` names for the board when the library runs inside pgm-studio-mapgen
(`maps/<mode>/<name>/`, see `tools/worlds.py`); a board the index does not name yet is added under its map's name,
or `<name>_pgmvox` where another board already holds that name.
Outside that repository a board's world is `<board>/world`.

With `--out <dir>` nothing is written into the board or the repository: the renders go to `<dir>/renders`, the map.xml
to `<dir>/map.xml` and the world to `<dir>/world`. That is how `check.py` rebuilds a board to compare it.

    python3 -m pgmvox.run <board-dir> [--build <build-dir>] [--out <dir>] [--from STEP] [--only STEP] [--skip STEP ...]

Run from freeform/lib (or with it on PYTHONPATH). A board's scripts find the library on their own sys.path.
"""
import argparse
import datetime
import os
import subprocess
import sys

from . import VERSION
from .world import studio_root, write

REPOSITORY_TOOLS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tools"))


def world_folder(board, map_xml):
    """Where `board`'s world is written: the folder the repository's maps index names for it, a new row there under
    the map's own name where it names none (`<name>_pgmvox` where another board holds that name), and
    `<board>/world` where the library runs outside the repository."""
    if not os.path.isfile(os.path.join(REPOSITORY_TOOLS, "worlds.py")):
        return os.path.join(board, "world")
    sys.path.insert(0, REPOSITORY_TOOLS)
    import worlds
    if (known := worlds.of(board)) is not None:
        return known
    xml = map_xml()
    place = worlds.place(xml) if xml else None
    if place is None:
        return os.path.join(board, "world")
    key = os.path.relpath(board, worlds.ROOT)
    if any(held == place for held, _, _ in worlds.rows()):
        place += "_pgmvox"
    worlds.register(place, key, key)
    return os.path.join(worlds.WORLDS, place)

STEPS = ["plan_check", "sketch", "gen", "write", "mapxml", "renders", "walk"]


def run(board, build=None, start=None, only=None, skip=(), out=None):
    board = os.path.abspath(board)
    home = os.path.abspath(out) if out else board
    scripts = os.path.join(board, "scripts")
    renders = os.path.join(home, "renders")
    os.makedirs(renders, exist_ok=True)
    slug = os.path.basename(board.rstrip("/"))
    build = build or f"/tmp/{slug}-build"
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                       os.environ.get("PYTHONPATH", "")]))
    steps = STEPS[STEPS.index(start):] if start else STEPS
    if only:
        steps = [only]
    steps = [st for st in steps if st not in skip]
    log = []

    def py(name, *args, out=None):
        path = os.path.join(scripts, f"{name}.py")
        if not os.path.exists(path):
            log.append(f"{name}: none")
            return None
        r = subprocess.run([sys.executable, path, *args], cwd=scripts, env=env, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"{name}.py failed:\n{r.stderr[-3000:]}")
        if out:
            with open(out, "w") as f:
                f.write(r.stdout)
        log.append(f"{name}: ok")
        return r.stdout
    found = []

    def world():
        if not found and out:
            found.append(os.path.join(home, "world"))
        if not found:
            stated = os.path.join(scripts, "map.xml")
            found.append(world_folder(board, lambda: py("mapxml") if os.path.isfile(os.path.join(scripts, "mapxml.py"))
                                      else (open(stated).read() if os.path.isfile(stated) else None)))
        return found[0]

    for step in steps:
        if step == "plan_check":
            py("plan_check", out=os.path.join(renders, "plan-check.txt"))
        elif step == "sketch":
            py("sketch", os.path.join(renders, "00-plan-sketch.png"))
        elif step == "gen":
            said = py("gen", build) or ""
            print(said, end="")
            with open(os.path.join(renders, "gen.txt"), "w") as f:
                f.write(said)
        elif step == "write":
            print(write(build, world()))
            log.append("write: ok")
        elif step == "mapxml":
            xml = py("mapxml")
            if xml is not None:
                stated = os.path.join(home, "map.xml") if out else os.path.join(scripts, "map.xml")
                for p in (stated, os.path.join(world(), "map.xml")):
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    with open(p, "w") as f:
                        f.write(xml)
        elif step == "renders":
            py("renders", build, home)
        elif step == "walk":
            said = py("walk", build, out=os.path.join(renders, "walks.txt"))
            if said:
                print(said, end="")
    with open(os.path.join(renders, "build-info.txt"), "w") as f:
        f.write(f"pgmvox {VERSION}\nbuilt {datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}\n"
                f"studio {studio_root()}\n" + "\n".join(log) + "\n")
    return log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("--build")
    ap.add_argument("--out")
    ap.add_argument("--from", dest="start", choices=STEPS)
    ap.add_argument("--only", choices=STEPS)
    ap.add_argument("--skip", choices=STEPS, action="append", default=[])
    a = ap.parse_args()
    for line in run(a.board, a.build, a.start, a.only, a.skip, a.out):
        print(line)


if __name__ == "__main__":
    main()
