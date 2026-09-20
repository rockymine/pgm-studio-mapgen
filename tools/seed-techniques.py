#!/usr/bin/env python3
"""Store every technique card's board in the studio, from the card's own committed documents.

    tools/seed-techniques.py [--check] [--all] [--only <card>]

A card says *open it in the studio as `technique-<name>`*, and that is only true on a database somebody
has already driven the card into. A fresh container has none of them. This puts them all back, so the
sentence holds and an agent can look at the thing the card describes rather than only read about it.

A card's own files say which of two roads it takes, and nothing else decides:

    <name>.layout.json [+ <name>.intent.json]     stored directly, the shape the Sketch tool writes
    <variant>.plan.json + <variant>.finish.json   driven through `tools/drive.py`, the same road a spec
                                                  takes, because a plan has to be compiled and patched

**A plan with no finish beside it is not a board.** `taking-over-a-composed-board/pinned.plan.json` is
the composer's own answer, committed so the card's starting point is reproducible, and it is the one plan
here that is not driven.

Re-running is safe: a slug is replaced rather than added to. `--check` says which are missing and stores
nothing, which is what a pre-flight wants.
"""
import argparse, json, os, shutil, subprocess, sys, tempfile, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS = os.path.join(ROOT, "techniques")
API = os.environ.get("PGM_STUDIO_API", "").rstrip("/")
CANDIDATES = ["http://localhost:7894/api", "http://localhost:5000/api", "http://localhost:8080/api"]

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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="say which are missing and store nothing")
    parser.add_argument("--all", action="store_true", help="re-seed every board, not only the missing")
    parser.add_argument("--only", help="one card folder")
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
    if args.check:
        print(f"\n{missing} missing of {len(boards())}")
        return 1 if missing else 0
    print(f"\n{seeded} board(s) stored of {len(boards())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
