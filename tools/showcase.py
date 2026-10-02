"""The showcase's copied trees, asked of the studio a board is driven against.

    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import showcase

    SHOWCASE = showcase.trees()
    SHOWCASE["tall-spruce-4"]["style"]   # the recipe, as `GET /api/tree-styles/{id}/json` answers it
    SHOWCASE["tall-spruce-4"]["foot"]    # where it stands in corpus/tree-showcase

**The trees are the studio's, and this repository keeps no copy of them.** The studio's seed folder holds the one
cut of `corpus/tree-showcase` (`pgm-studio/src/PgmStudio.Minecraft/Library/trees.json`, written by
`pgm-studio/tools/seed-trees.cs`), every start files it into the tree library, and a row filed so is the folder's:
the studio refuses to edit it (`LB6`). So a tree read here by its name is the cut, on whichever studio answers.

**A tree is fetched when it is named.** The library is listed once and a recipe asked for the first time a board
names it, so a board planting five trees makes eleven requests rather than nearly two hundred. A name the library
does not hold stops the run, naming the nearest ones it does.
"""
import collections.abc
import difflib
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drive  # noqa: E402


def _get(path):
    request = urllib.request.Request(drive.endpoint() + path, headers=drive.signed({}))
    with urllib.request.urlopen(request, timeout=120) as answer:
        return json.load(answer)


class Trees(collections.abc.Mapping):
    """The tree library by name, each entry `{"style": recipe, "foot": [x, y, z]}`, the foot being where a copied
    tree was cut and None for a template."""

    def __init__(self):
        self._ids = None
        self._held = {}

    def _rows(self):
        if self._ids is None:
            self._ids = {row["name"]: row["id"] for row in _get("/tree-styles")}
        return self._ids

    def __getitem__(self, name):
        if name in self._held:
            return self._held[name]
        rows = self._rows()
        if name not in rows:
            near = difflib.get_close_matches(name, list(rows), n=3)
            raise SystemExit(f"the studio's tree library holds no `{name}`"
                             + (f"; nearest: {', '.join(near)}" if near else ""))
        cut = _get(f"/tree-styles/{rows[name]}").get("cut")
        self._held[name] = {
            "style": json.loads(_get(f"/tree-styles/{rows[name]}/json")["styleJson"]),
            "foot": [cut["x"], cut["y"], cut["z"]] if cut else None,
        }
        return self._held[name]

    def __iter__(self):
        return iter(self._rows())

    def __len__(self):
        return len(self._rows())


_library = None


def trees():
    """The tree library of the studio `drive.endpoint()` resolves, one per run however often it is asked for."""
    global _library
    if _library is None:
        _library = Trees()
    return _library
