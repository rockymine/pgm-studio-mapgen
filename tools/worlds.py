#!/usr/bin/env python3
"""Where a board's world is: `maps/<mode>/<name>/`, named in `maps/INDEX.md`.

    tools/worlds.py of <board>          the world folder a board writes to (a slug, or a board folder)
    tools/worlds.py place <map.xml>     the folder a new world would take, from its name and game modes

Every world in this repository is one folder holding `map.xml`, `level.dat` and `region/` (and `map.png` where the
studio draws one), under the game-mode folder `OvercastCommunity/CommunityMaps` files it in (`bucket` says which:
`ctw`, `dtcm`, `koth`, `kotf`, `ctf`, `tdm`, `ffa`, `blitz`, `arcade`, `mixed` for two objective modes at once, and the
rest of `MODES`). The folder is the map's name in lower case with underscores, so it can be copied out to a server as
it stands. `maps/INDEX.md` says which board builds each one; a board finds its
world there, and a board building its first world adds its row.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORLDS = os.path.join(ROOT, "maps")
INDEX = os.path.join(WORLDS, "INDEX.md")
HEADER = """# Maps

Every world built in this repository: one folder per world holding `map.xml`, `level.dat` and `region/`, under the
game-mode folder `OvercastCommunity/CommunityMaps` files it in (`ctw`, `dtcm`, `koth`, `tdm`, `arcade`, `mixed` and the
rest), named for the map. Copy a folder out and a server
loads it. **Board** is the studio slug or the freeform board folder that builds the world, and **source** is where
its spec or scripts are. `tools/worlds.py` reads and extends this table; `tools/boards-check.py` gates it.

| World | Board | Source |
|---|---|---|
"""


def snake(name):
    """A map's name as a folder name: lower case, every run of other characters one underscore."""
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


MODES = ("ctw", "dtcm", "ctf", "kotf", "koth", "tdm", "ffa", "blitz", "scorebox", "arcade", "touchdown", "bridge",
         "5cp", "mixed", "other")
MODIFIERS = {"rage", "ad"}                                  # a tag that changes how a mode plays, not which mode
TAGGED = {"ctw": "ctw", "dtm": "dtcm", "dtc": "dtcm", "ctf": "ctf", "kotf": "kotf", "koth": "koth"}
NEEDS = {"ctw": r"<wools", "dtcm": r"<destroyables|<cores", "ctf": r"<flags", "kotf": r"<flags",
         "koth": r"<hills|<control-points"}


def bucket(map_xml):
    """The game-mode folder `OvercastCommunity/CommunityMaps` would file a map.xml under.

    `arcade` and `blitz` are the author's word and win. Otherwise the objective modes decide: those the
    `<gamemode>` tags name and the map holds the objective of, or, where no tag holds, those its objectives
    show (wool `ctw`, monuments and cores `dtcm`, hills `koth`, flags `ctf` with a score and `kotf` without),
    or, where it holds no objective at all, those its tags name. Two objective modes make `mixed`. A map with none is filed by its tag (`tdm`, `ffa`, `scorebox` and the
    rest), then by what it scores, and `other` where nothing says."""
    tags = {t.lower() for t in re.findall(r"<gamemode>\s*([^<\s]+)\s*</gamemode>", map_xml)} - MODIFIERS
    if "arcade" in tags:
        return "arcade"
    if tags & {"blitz", "br"}:
        return "blitz"
    claimed = {TAGGED[t] for t in tags if t in TAGGED and re.search(NEEDS[TAGGED[t]], map_xml)}
    shown = {m for m in ("ctw", "dtcm", "koth") if re.search(NEEDS[m], map_xml)}
    if re.search(NEEDS["ctf"], map_xml):
        shown.add("ctf" if "<score" in map_xml else "kotf")
    objective = claimed or shown or {TAGGED[t] for t in tags if t in TAGGED}
    if len(objective) > 1:
        return "mixed"
    if objective:
        return objective.pop()
    for mode in ("tdm", "scorebox", "ffa", "touchdown", "bridge", "5cp"):
        if mode in tags:
            return mode
    if tags:
        return "other"
    if "<blitz" in map_xml:
        return "blitz"
    if "<players" in map_xml:
        return "ffa"
    return "tdm" if "<score" in map_xml else "other"


def rows():
    """The index as (world, board, source) triples, world relative to `maps/`."""
    if not os.path.isfile(INDEX):
        return []
    found = []
    for line in open(INDEX, encoding="utf-8"):
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) == 3 and "/" in cells[0] and not cells[0].startswith("-"):
            found.append((cells[0], cells[1], "" if cells[2] == "—" else cells[2]))
    return found


def _board_key(board):
    """A board as the index names it: a slug stays a slug, a folder is made relative to the repository."""
    if os.path.isabs(board) or os.sep in board.rstrip(os.sep):
        return os.path.relpath(os.path.abspath(board), ROOT)
    return board


def of(board):
    """The absolute world folder `board` writes to, or None where the index names none."""
    key = _board_key(board)
    for world, named, _ in rows():
        if named == key:
            return os.path.join(WORLDS, world)
    return None


def place(map_xml):
    """`<mode>/<name>` for a world with this map.xml text, or None where the map states no name."""
    name = re.search(r"<name>([^<]+)</name>", map_xml)
    return f"{bucket(map_xml)}/{snake(name.group(1))}" if name else None


def register(world, board, source):
    """Add a world to the index, refusing a folder another board holds."""
    key = _board_key(board)
    taken = {named: held for held, named, _ in rows()}
    for held, named, _ in rows():
        if held == world and named != key:
            raise SystemExit(f"maps/{world} is {named}'s world; name this one another way (--world <name>)")
    if taken.get(key) == world:
        return
    entries = [row for row in rows() if row[1] != key] + [(world, key, source)]
    write(entries)


def write(entries):
    with open(INDEX, "w", encoding="utf-8") as handle:
        handle.write(HEADER)
        for world, board, source in sorted(entries):
            handle.write(f"| `{world}` | `{board}` | {f'`{source}`' if source else '—'} |\n")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "of":
        found = of(sys.argv[2])
        if found is None:
            raise SystemExit(f"no world in maps/INDEX.md for {sys.argv[2]}")
        print(found)
    elif len(sys.argv) == 3 and sys.argv[1] == "place":
        print(place(open(sys.argv[2], encoding="utf-8").read()) or "")
    else:
        raise SystemExit(__doc__)
