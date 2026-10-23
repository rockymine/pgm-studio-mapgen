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

pgmvox is an installed package (`pip install -e freeform/lib`, once per machine): a board's scripts import it as one,
not by path, and `run` stops at once, saying so, where it is not installed or is installed from another checkout.
"""
import argparse
import datetime
import os
import subprocess
import sys
import tempfile

from . import VERSION
from pgmvox.core.world import studio_root, write

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
    key = os.path.relpath(os.path.abspath(board), worlds.ROOT)
    if any(held == place for held, _, _ in worlds.rows()):
        place += "_pgmvox"
    worlds.register(place, os.path.abspath(board), key)          # the index makes the board relative itself
    return os.path.join(worlds.WORLDS, place)

def require_installed():
    """Stop with the command that fixes it unless this Python imports pgmvox, from anywhere, as this checkout's
    copy: a board's scripts run in their own folder and find the library only as an installed package."""
    here = os.path.dirname(os.path.abspath(__file__))
    r = subprocess.run([sys.executable, "-c", "import os, pgmvox; print(os.path.dirname(os.path.abspath(pgmvox.__file__)))"],
                       cwd=tempfile.gettempdir(), capture_output=True, text=True)
    found = r.stdout.strip() if r.returncode == 0 else None
    if found != here:
        lib = os.path.dirname(here)
        where = "is not installed" if found is None else f"is installed from {found}"
        sys.exit(f"pgmvox {where} for {sys.executable}: run  {sys.executable} -m pip install -e {lib}")


STEPS = ["plan_check", "sketch", "gen", "write", "mapxml", "renders", "walk"]


def run(board, build=None, start=None, only=None, skip=(), out=None):
    board = os.path.abspath(board)
    home = os.path.abspath(out) if out else board
    scripts = os.path.join(board, "scripts")
    renders = os.path.join(home, "renders")
    os.makedirs(renders, exist_ok=True)
    slug = os.path.basename(board.rstrip("/"))
    build = build or f"/tmp/{slug}-build"
    require_installed()
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
        r = subprocess.run([sys.executable, path, *args], cwd=scripts, capture_output=True, text=True)
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
