"""Build a freeform board from nothing, in the order every board's build.sh ran it:

    plan_check.py  > renders/plan-check.txt      (if the board has one)
    sketch.py        renders/00-plan-sketch.png
    gen.py           <build-dir>                 (saves volume.bin, tiles.json, level.json)
    write            world/region, world/level.dat, through the studio's Anvil writer
    mapxml.py      > scripts/map.xml and world/map.xml
    renders.py       <build-dir> <board-dir>      (if the board has one)
    walk.py        > renders/walks.txt            (if the board has one)

and writes renders/build-info.txt with the library version, so a board records what it was built with.

    python3 -m pgmvox.run <board-dir> [--build <build-dir>] [--from STEP] [--only STEP] [--skip STEP ...]

Run from freeform/lib (or with it on PYTHONPATH). A board's scripts find the library on their own sys.path.
"""
import argparse
import datetime
import os
import subprocess
import sys

from . import VERSION
from .world import studio_root, write

STEPS = ["plan_check", "sketch", "gen", "write", "mapxml", "renders", "walk"]


def run(board, build=None, start=None, only=None, skip=()):
    board = os.path.abspath(board)
    scripts = os.path.join(board, "scripts")
    renders = os.path.join(board, "renders")
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
    for step in steps:
        if step == "plan_check":
            py("plan_check", out=os.path.join(renders, "plan-check.txt"))
        elif step == "sketch":
            py("sketch", os.path.join(renders, "00-plan-sketch.png"))
        elif step == "gen":
            out = py("gen", build) or ""
            print(out, end="")
            with open(os.path.join(renders, "gen.txt"), "w") as f:
                f.write(out)
        elif step == "write":
            print(write(build, os.path.join(board, "world")))
            log.append("write: ok")
        elif step == "mapxml":
            xml = py("mapxml")
            if xml is not None:
                for p in (os.path.join(scripts, "map.xml"), os.path.join(board, "world", "map.xml")):
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    with open(p, "w") as f:
                        f.write(xml)
        elif step == "renders":
            py("renders", build, board)
        elif step == "walk":
            out = py("walk", build, out=os.path.join(renders, "walks.txt"))
            if out:
                print(out, end="")
    with open(os.path.join(renders, "build-info.txt"), "w") as f:
        f.write(f"pgmvox {VERSION}\nbuilt {datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}\n"
                f"studio {studio_root()}\n" + "\n".join(log) + "\n")
    return log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("--build")
    ap.add_argument("--from", dest="start", choices=STEPS)
    ap.add_argument("--only", choices=STEPS)
    ap.add_argument("--skip", choices=STEPS, action="append", default=[])
    a = ap.parse_args()
    for line in run(a.board, a.build, a.start, a.only, a.skip):
        print(line)


if __name__ == "__main__":
    main()
