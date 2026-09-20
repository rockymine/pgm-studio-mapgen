#!/usr/bin/env python3
"""Put everything this repository needs into a studio that has none of it.

    tools/seed-studio.py [--check] [--all] [--only <card>] [--no-trees]

**A studio seeds its own library at startup and nothing else.** `LibrarySeed` runs on every boot and is
idempotent, so the materials, the house presets and parts, the themes, the biomes, the four erratic
boulders and the six vanilla tree recipes are always there. Two things this repository depends on are
not, and this puts both in.

**The technique cards' boards.** A card says *open it in the studio as `technique-<name>`*, which is only
true on a database somebody has driven it into — thirty boards over twenty-seven cards. A card's own files
say which of two roads it takes and nothing else decides:

    <name>.layout.json [+ <name>.intent.json]     stored directly, the shape the Sketch tool writes
    <variant>.plan.json + <variant>.finish.json   driven through `tools/drive.py`, the same road a spec
                                                  takes, because a plan has to be compiled and patched

A plan with no finish beside it is not a board. `taking-over-a-composed-board/pinned.plan.json` is the
composer's own answer, committed so the card's starting point is reproducible, and it is the one plan in
`techniques/` that is not driven.

**The copied trees.** `corpus/tree-showcase` is a world of hand-built trees, and the studio's
`tools/seed-trees.cs` cuts each one out of it into the tree library as a `copied` recipe. Without them a
studio offers the six vanilla species alone, and the warmup skill tells an author to prefer a copied tree
over the vanilla stamp — so a run against an unseeded studio is told to reach for something not there.
`PGM_STUDIO_REPO` says where the studio's checkout is, and `--no-trees` skips this half.

Re-running is safe: a slug is replaced rather than added to, and a tree row is keyed by name. `--check`
says what is missing and stores nothing, which is what a pre-flight wants.
"""
import argparse, json, os, shutil, subprocess, sys, tempfile, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS = os.path.join(ROOT, "techniques")
API = os.environ.get("PGM_STUDIO_API", "").rstrip("/")
CANDIDATES = ["http://localhost:7894/api", "http://localhost:5000/api", "http://localhost:8080/api"]

# The corpus world the copied trees are cut out of, and the name every recipe from it is filed under.
CORPUS_WORLD = os.path.join(ROOT, "corpus", "tree-showcase")
CORPUS_TREES = "showcase"
# Where the studio's own checkout is. Stated as candidates rather than as a constant, because a path is
# the machine somebody happened to be on.
STUDIO_REPOS = [os.environ.get("PGM_STUDIO_REPO", ""), "/home/user/pgm-studio",
                os.path.join(os.path.dirname(ROOT), "pgm-studio")]

# The one card whose slugs are not `technique-<its folder>`: it is four boards rather than one, and its
# README names them `technique-composed-<variant>`.
SLUG_PREFIX = {"taking-over-a-composed-board": "technique-composed-"}


def endpoint():
    """The studio, asked rather than assumed — it has been a different port on every machine."""
    for base in ([API] if API else []) + CANDIDATES:
        try:
            with urllib.request.urlopen(f"{base}/health", timeout=3) as answer:
                if answer.status == 200:
                    return base
        except Exception:
            continue
    sys.exit("no studio answered /api/health — set PGM_STUDIO_API, or start one "
             "(pgm-studio/docs/cloud-setup.md)")


def call(base, method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(base + path, data=data, method=method,
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request) as answer:
            raw = answer.read().decode("utf-8", "replace")
            return answer.status, (json.loads(raw) if raw.strip()[:1] in "{[" else raw)
    except urllib.error.HTTPError as refused:
        raw = refused.read().decode("utf-8", "replace")
        return refused.code, (json.loads(raw) if raw.strip()[:1] in "{[" else raw)


def boards():
    """Every board a card carries, as (card, slug, kind, files). One card can carry several."""
    found = []
    for card in sorted(os.listdir(CARDS)):
        folder = os.path.join(CARDS, card)
        if not os.path.isdir(folder) or card.startswith("__"):
            continue
        here = set(os.listdir(folder))
        prefix = SLUG_PREFIX.get(card, "technique-")
        if f"{card}.layout.json" in here:
            found.append((card, f"technique-{card}", "layout",
                          {"layout": os.path.join(folder, f"{card}.layout.json"),
                           "intent": os.path.join(folder, f"{card}.intent.json")
                           if f"{card}.intent.json" in here else None}))
            continue
        for name in sorted(here):
            if not name.endswith(".plan.json"):
                continue
            base = name[: -len(".plan.json")]
            if f"{base}.finish.json" not in here:
                continue                       # a plan with no finish is not a board — see the docstring
            found.append((card, f"{prefix}{base}", "spec",
                          {"plan": os.path.join(folder, name),
                           "finish": os.path.join(folder, f"{base}.finish.json"), "base": base}))
    return found


def store_layout(base, slug, files):
    """The three calls a drawn board takes, and the two more a board with objectives takes."""
    layout = json.load(open(files["layout"], encoding="utf-8"))
    call(base, "POST", "/sketch", {"name": slug, "slug": slug, "layout": layout})
    status, body = call(base, "PUT", f"/map/{slug}/sketch", layout)
    said = [f"{finding.get('rule')} {finding.get('severity')}"
            for key in ("refusals", "warnings", "errors", "findings")
            for finding in (body.get(key) or []) if isinstance(body, dict)]
    finish, _ = call(base, "POST", f"/map/{slug}/sketch/finish", {})
    note = f"store {status} finish {finish}"
    if files["intent"]:
        intent = json.load(open(files["intent"], encoding="utf-8"))
        put, _ = call(base, "PUT", f"/map/{slug}/intent", intent)
        export, _ = call(base, "GET", f"/map/{slug}/export")
        note += f" intent {put} export {export}"
    return note + (f"  [{' '.join(sorted(set(said)))}]" if said else "")


def drive(slug, files):
    """A spec goes down the road every spec goes down, in a directory named as `drive.py` wants."""
    with tempfile.TemporaryDirectory() as scratch:
        spec = os.path.join(scratch, files["base"])
        os.makedirs(spec)
        for key in ("plan", "finish"):
            shutil.copy(files[key], spec)
        done = subprocess.run(
            [sys.executable, os.path.join(ROOT, "tools", "drive.py"), spec, slug,
             "--out", os.path.join(scratch, "world")],
            capture_output=True, text=True)
    if done.returncode != 0:
        tail = (done.stderr or done.stdout).strip().splitlines()[-1:] or ["no output"]
        return f"FAILED — {tail[0][:110]}"
    return "driven"


def copied_trees(base):
    """How many recipes in the tree library came out of the corpus world."""
    status, body = call(base, "GET", "/tree-styles")
    rows = body if isinstance(body, list) else (body.get("items") or []) if isinstance(body, dict) else []
    return sum(1 for row in rows if str(row.get("name", "")).startswith(f"{CORPUS_TREES}-"))


def seed_trees():
    """The studio's own `seed-trees.cs`, over this repository's corpus world. It is a dotnet build and a
    scan of every region file, so it takes minutes rather than seconds and says so."""
    studio = next((path for path in STUDIO_REPOS
                   if path and os.path.isfile(os.path.join(path, "tools", "seed-trees.cs"))), None)
    if studio is None:
        return "SKIPPED — no pgm-studio checkout found; set PGM_STUDIO_REPO"
    if not os.path.isdir(os.path.join(CORPUS_WORLD, "region")):
        return f"SKIPPED — no world at {CORPUS_WORLD}"
    began = time.time()
    done = subprocess.run(
        ["dotnet", "run", os.path.join("tools", "seed-trees.cs"), CORPUS_WORLD, CORPUS_TREES],
        cwd=studio, capture_output=True, text=True)
    if done.returncode != 0:
        tail = (done.stderr or done.stdout).strip().splitlines()[-1:] or ["no output"]
        return f"FAILED — {tail[0][:110]}"
    said = [line for line in done.stdout.splitlines() if "added" in line and "updated" in line]
    return f"{said[-1].strip() if said else 'done'}  ({time.time() - began:.0f}s)"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="say which are missing and store nothing")
    parser.add_argument("--all", action="store_true", help="re-seed every board, not only the missing")
    parser.add_argument("--only", help="one card folder")
    parser.add_argument("--no-trees", action="store_true", help="the boards only, not the corpus trees")
    args = parser.parse_args()

    base = endpoint()
    print(f"studio at {base}")
    missing, seeded = 0, 0
    for card, slug, kind, files in boards():
        if args.only and card != args.only:
            continue
        status, _ = call(base, "GET", f"/map/{slug}/sketch")
        there = status == 200
        if there and not args.all:
            if args.check:
                print(f"  ok       {slug}")
            continue
        missing += 1
        if args.check:
            print(f"  MISSING  {slug}  ({card}, {kind})")
            continue
        note = store_layout(base, slug, files) if kind == "layout" else drive(slug, files)
        seeded += 1
        print(f"  {'reseeded' if there else 'seeded  '} {slug:44s} {note}")
    trees = copied_trees(base)
    wants_trees = not (args.no_trees or args.only)
    if args.check:
        print(f"  {'ok      ' if trees else 'MISSING '} {trees} copied tree(s) from `{CORPUS_TREES}`")
        print(f"\n{missing} board(s) missing of {len(boards())}"
              f"{'' if trees else ', and the copied trees'}")
        return 1 if (missing or not trees) else 0
    if wants_trees and (args.all or not trees):
        print(f"  {'reseeding' if trees else 'seeding  '} the copied trees — this is a build and a world "
              f"scan, give it minutes")
        print(f"  trees: {seed_trees()}")
    elif wants_trees:
        print(f"  ok       {trees} copied tree(s) already filed under `{CORPUS_TREES}`")
    print(f"\n{seeded} board(s) stored of {len(boards())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
