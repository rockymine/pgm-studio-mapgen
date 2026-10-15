#!/usr/bin/env python3
"""Gate BOARDS-BUILT.md against what is on disk.

    tools/boards-check.py [--fix-report]

A board lands in `specs/` and its world in `maps/<mode>/<name>/` the moment it is driven, and its entry in the log
is written by hand because the column that matters — what the board turned out to be — is not derivable from a
folder. That is exactly the shape of thing that goes unwritten, so this counts.

Every world folder under `maps/` has to have its row in `maps/INDEX.md`, and every row a folder. Every board the
index names by slug, and every folder under `specs/` and `specs/archive/`, has to be accounted for in one of three
ways:

  written up      named in the log or in `README.md`
  not a board     named under `## Not boards` — a probe suite, a test world, a generated library map
  not yet         named under `## Not yet written up`, which is a debt the log carries in the open

Anything else fails. So does a slug in either list that has left the disk, and a slug that is in the debt
list and written up as well — a list nobody prunes is a list nobody reads.
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worlds  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "BOARDS-BUILT.md")
# The log is where a board is written up; the README describes the few boards it is the index of.
INDEXES = ["README.md"]
NOT_BOARDS = "## Not boards"
NOT_YET = "## Not yet written up"


def world_faults():
    """World folders the index does not name, and index rows with no folder."""
    on_disk = {f"{mode}/{name}" for mode in sorted(os.listdir(worlds.WORLDS))
               if os.path.isdir(os.path.join(worlds.WORLDS, mode))
               for name in os.listdir(os.path.join(worlds.WORLDS, mode))
               if os.path.isdir(os.path.join(worlds.WORLDS, mode, name))}
    indexed = {world for world, _, _ in worlds.rows()}
    return sorted(on_disk - indexed), sorted(indexed - on_disk)


def folders():
    """Every board, as {slug: where it lives}: the boards the index names by slug, and the spec folders."""
    found = {board: "world" for _, board, _ in worlds.rows() if "/" not in board}
    for where, path in (("spec", "specs"), ("archived spec", "specs/archive")):
        directory = os.path.join(ROOT, path)
        if not os.path.isdir(directory):
            continue
        for name in os.listdir(directory):
            if name == "archive" or not os.path.isdir(os.path.join(directory, name)):
                continue
            found.setdefault(name, where)
    return found


def sections(text):
    """The log's body, and the slugs named under each of its two accounting headings."""
    body, listed = text, {NOT_BOARDS: set(), NOT_YET: set()}
    for heading in (NOT_BOARDS, NOT_YET):
        if heading not in text:
            continue
        after = text[text.index(heading) + len(heading):]
        end = after.index("\n## ") if "\n## " in after else len(after)
        named = re.findall(r"`([^`\s]+)`", after[:end])
        # A slug is a folder name: a backticked path or filename in the prose is not one.
        listed[heading] = {name for name in named if "/" not in name and "." not in name}
        body = body.replace(heading + after[:end], "")
    return body, listed[NOT_BOARDS], listed[NOT_YET]


def main():
    fix_report = "--fix-report" in sys.argv
    text = open(LOG, encoding="utf-8").read()
    body, not_boards, not_yet = sections(text)
    on_disk = folders()
    for name in INDEXES:
        path = os.path.join(ROOT, name)
        if os.path.isfile(path):
            body += "\n" + open(path, encoding="utf-8").read()
    named_in_body = {slug for slug in on_disk if re.search(rf"\b{re.escape(slug)}\b", body)}

    unlisted = sorted(set(on_disk) - named_in_body - not_boards - not_yet)
    gone = sorted((not_boards | not_yet) - set(on_disk))
    both = sorted(not_yet & named_in_body)

    stray, missing = world_faults()
    for world in stray:
        print(f"  no row      maps/{world:33s} (a world folder maps/INDEX.md does not name)")
    for world in missing:
        print(f"  no folder   maps/{world:33s} (named in maps/INDEX.md, not on disk)")

    for slug in unlisted:
        print(f"  unlisted    {slug:38s} ({on_disk[slug]})")
    for slug in gone:
        print(f"  not on disk {slug:38s} (named in the log, no folder)")
    for slug in both:
        print(f"  both        {slug:38s} (written up and still in the debt list)")

    written = len(named_in_body)
    print(f"\n{written} written up · {len(not_yet)} not yet · {len(not_boards)} not boards · "
          f"{len(on_disk)} folders on disk")
    faults = len(unlisted) + len(gone) + len(both) + len(stray) + len(missing)
    if faults:
        print(f"{faults} unaccounted for")
        if not fix_report:
            print("run with --fix-report for the list alone")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
