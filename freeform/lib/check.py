"""Check that nothing is broken: the tests, every example rebuilt and read back against a snapshot, the docs
through the prose gate, and, where the studio is checked out, the library held to the studio's own answers.

    python3 check.py                # tests, examples against the snapshot, prose
    python3 check.py --studio       # and the studio: re-export blocks, roofs and slopes, read every map.xml
    python3 check.py --update       # accept the examples as they now are (after looking at what changed)
    python3 check.py --quick        # tests and prose only

What an example is held to is what it reads back, not how it looks: the numbers its plan check, generator and
walk print, and a fingerprint of the built world (how many of each block). A change that moves a number or a
block count fails until it is looked at and accepted with --update; the diff says which.
"""
import argparse
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
SNAPSHOT = os.path.join(HERE, "check", "snapshot.json")
# each example and the steps it runs; "write" needs the studio's toolchain and is never needed to compare
EXAMPLES = {
    "islets": ["plan_check", "sketch", "gen", "mapxml", "renders", "walk"],
    "drop": ["plan_check", "sketch"],
    "parts": ["gen", "renders"],
    "vale": ["plan_check", "gen", "renders", "walk"],
}
READS = {"plan_check": "plan-check.txt", "gen": "gen.txt", "walk": "walks.txt"}   # what each step reads back
DOCS = ["README.md", "AGENT-GUIDE.md"]
FAILED = []


def say(ok, what, detail=""):
    print(("  ok    " if ok else "  FAIL  ") + what + (f"\n{detail}" if detail and not ok else ""))
    if not ok:
        FAILED.append(what)


def tests():
    r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=HERE,
                       capture_output=True, text=True)
    tail = r.stderr.strip().splitlines()[-3:]
    say(r.returncode == 0, "unit tests: " + (tail[-1] if tail else "?"), r.stderr[-3000:])


def fingerprint(build):
    from pgmvox import World
    from pgmvox.blocks import name
    w = World.load(build)
    c = Counter(w.ids.ravel().tolist())
    return {f"{name(i, 0)} ({i})": n for i, n in sorted(c.items()) if i}


def numbers(text):
    """The lines of a read-back that carry a number, as they are: what a snapshot holds."""
    return [ln.rstrip() for ln in text.splitlines() if re.search(r"\d", ln)]


def example(name, tmp):
    from pgmvox.run import run
    board = os.path.join(HERE, "examples", name)
    build = os.path.join(tmp, name)
    steps = EXAMPLES[name]
    out = {}
    try:
        import contextlib
        import io
        with contextlib.redirect_stdout(io.StringIO()):
            for st in steps:
                run(board, build, only=st)
    except Exception as e:                                       # noqa: BLE001
        say(False, f"{name}: builds", str(e)[-2000:])
        return None
    for st in steps:
        p = os.path.join(board, "renders", READS.get(st, ""))
        if st in READS and os.path.exists(p):
            out[READS[st]] = numbers(open(p).read())
    if "gen" in steps:
        out["blocks"] = fingerprint(build)
    return out


def compare(name, got, want):
    if want is None:
        say(False, f"{name}: no snapshot yet", "run with --update to take one")
        return
    diffs = []
    for key in sorted(set(got) | set(want)):
        a, b = want.get(key), got.get(key)
        if a == b:
            continue
        if isinstance(a, dict) or isinstance(b, dict):
            a, b = a or {}, b or {}
            for blk in sorted(set(a) | set(b)):
                if a.get(blk) != b.get(blk):
                    diffs.append(f"    {key}: {blk} {a.get(blk, 0)} -> {b.get(blk, 0)}")
        else:
            diffs += ["    " + d for d in difflib.unified_diff(a or [], b or [], key, key, lineterm="", n=0)][2:]
    say(not diffs, f"{name}: reads back as the snapshot", "\n".join(diffs[:40]))


def prose():
    gate = os.path.join(REPO, "tools", "prose-check.py")
    for d in DOCS:
        p = os.path.join(HERE, d)
        if not os.path.exists(p):
            continue
        r = subprocess.run([sys.executable, gate, p], capture_output=True, text=True)
        say(r.returncode == 0, f"prose gate: {d}", r.stdout[-1500:])


def studio(tmp):
    """Re-export the studio's answers and hold the committed tables to them; read every example's map.xml."""
    if not shutil.which("dotnet"):
        say(False, "studio: dotnet is not installed")
        return
    data = os.path.join(HERE, "pgmvox", "data")

    def dotnet(script, *args):
        return subprocess.run(["dotnet", "run", os.path.join(data, script), "--", *args], cwd=tmp,
                              capture_output=True, text=True, timeout=900)
    r = dotnet("export_blocks.cs", os.path.join(tmp, "blocks.json"))
    same = r.returncode == 0 and json.load(open(os.path.join(tmp, "blocks.json"))) == \
        json.load(open(os.path.join(data, "blocks.json")))
    say(same, "studio: blocks.json is the studio's palette", r.stderr[-1500:] or "the export differs: re-export it")
    r = dotnet("export_roofs.cs", os.path.join(tmp, "roofs.json"))
    import gzip
    same = r.returncode == 0 and json.load(open(os.path.join(tmp, "roofs.json"))) == \
        json.load(gzip.open(os.path.join(data, "roofs.json.gz"), "rt"))
    say(same, "studio: roofs.json.gz is the studio's RoofField", r.stderr[-1500:] or "the export differs")
    from pgmvox.terrain import _slope_cases
    _slope_cases(os.path.join(tmp, "cases.json"))
    r = dotnet("export_slopes.cs", os.path.join(tmp, "cases.json"), os.path.join(tmp, "slopes.json"))
    same = r.returncode == 0 and json.load(open(os.path.join(tmp, "slopes.json"))) == \
        json.load(gzip.open(os.path.join(data, "slopes.json.gz"), "rt"))
    say(same, "studio: slopes.json.gz is the studio's SurfaceGradient", r.stderr[-1500:] or "the export differs")
    maps = [os.path.join(HERE, "examples", e, "scripts", "map.xml") for e in EXAMPLES]
    maps = [m for m in maps if os.path.exists(m)]
    r = dotnet("read_mapxml.cs", *maps)
    say(r.returncode == 0, f"studio: reads {len(maps)} example map.xml as valid", r.stdout[-2000:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--studio", action="store_true")
    ap.add_argument("--update", action="store_true")
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("example", nargs="*", help="only these examples")
    a = ap.parse_args()
    print("tests")
    tests()
    print("prose")
    prose()
    snap = json.load(open(SNAPSHOT)) if os.path.exists(SNAPSHOT) else {}
    with tempfile.TemporaryDirectory() as tmp:
        if not a.quick:
            print("examples")
            for name in a.example or EXAMPLES:
                got = example(name, tmp)
                if got is None:
                    continue
                if a.update:
                    snap[name] = got
                    print(f"  saved {name}")
                else:
                    compare(name, got, snap.get(name))
            if a.update:
                os.makedirs(os.path.dirname(SNAPSHOT), exist_ok=True)
                json.dump(snap, open(SNAPSHOT, "w"), indent=1, sort_keys=True)
        if a.studio:
            print("studio")
            studio(tmp)
    print(f"\n{'nothing broken' if not FAILED else str(len(FAILED)) + ' failed: ' + '; '.join(FAILED)}")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
