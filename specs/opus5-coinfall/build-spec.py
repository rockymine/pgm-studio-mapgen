#!/usr/bin/env python3
"""Coinfall — a two-team CTW board whose blocks are bought.

The board is deliberately small and plain: two spawn camps, an apron in front of each, a vault holding the
wool, and one crossing between them. What it is *for* is the shop. Each camp carries a villager trading the kit's own wood
for the things a wool run needs — a gapple to get a carrier home, arrows, ladders, iron bars to cut a bridge
— so what a player carries at minute ten is bought rather than handed out.

The finish states the menu and nothing about where the villager stands: a shop is a catalogue rather than a
place, and pgm-studio puts one keeper per shop at every team's spawn, beside the point players arrive on and
turned to face them (`pgm-studio/docs/pgm/shops.md` §9).

    python3 specs/opus5-coinfall/build-spec.py
    tools/drive.py specs/opus5-coinfall "Coinfall" --out maps/opus5-coinfall --renders specs/opus5-coinfall/renders
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "opus5-coinfall"
CELL = 5


def solid(block_id, data=0):
    return {"kind": "solid", "id": block_id, "data": data}


def cells(size, *palette, rise=0):
    """A cell field. `rise` is its vertical period in blocks, and a bucket a player reads edge-on — the wall,
    the fill — must state one or every block of a column resolves alike and the face comes out striped (PT4)."""
    out = {"kind": "cell", "cellSize": size, "palette": list(palette)}
    if rise:
        out["rise"] = rise
    return out


def depth(*bands):
    """A vertical stack: the top course first, each band a material and how many courses of it."""
    return {"kind": "layered", "stack": {"ending": "repeat",
                                         "bands": [{"material": m, "thickness": t} for m, t in bands]}}


def by_slope(*bands):
    """A stack on the slope axis: a thickness here is a span of DEGREES, so one stack finishes the flat,
    the shoulder and the face of the same hill. Read `GET …/incline?format=text` before moving a cut."""
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}


GRASS, DIRT, COARSE_DIRT, STONE, COBBLE, ANDESITE, GRAVEL = \
    solid(2), solid(3), solid(3, 1), solid(1), solid(4), solid(1, 5), solid(13)

# The ground, finished by its angle: meadow to 30 degrees, a worn shoulder to 45, bare rock above it.
COIN_THEME = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "drop",
    "wallOnTerrainFaces": True,
    "rim": {"material": solid(1, 5), "depth": 1, "enabled": False},
    "surface": {
        "material": by_slope(
            (depth((GRASS, 1), (DIRT, 2)), 30),
            (depth((COARSE_DIRT, 1), (DIRT, 2)), 15),
            (cells(9, STONE, COBBLE), 45)),
        "depth": 3,
    },
    # `wall` and `fill` are bare materials rather than bands: the riser is however tall the ground makes it
    # and the fill is everything no bucket claimed, so neither takes a depth.
    "wall": cells(11, ANDESITE, COBBLE, GRAVEL, rise=3),
    "wallEnabled": True,
    "fill": STONE,
    "edgesFromGround": True,
}


def piece(piece_id, role, x, z, w, h, surface=None):
    """A rectangle of ground, in signed proxy cells about the symmetry centre. Team 0's unit only — rot_180
    fans the rest, so everything authored here sits at z < 0."""
    out = {"id": piece_id, "role": role, "rect": [x, z, w, h]}
    if surface is not None:
        out["surface"] = surface
    return out


PLAN = {
    "plan": 2,
    "meta": {"name": "Coinfall"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 12, "surface": 14},
    "pieces": [
        piece("camp", "spawn", -2, -12, 4, 4, surface=16),
        piece("vault", "wool-room", -12, -8, 4, 3, surface=15),
        piece("apron", "piece", -8, -8, 16, 3, surface=15),
        piece("crossing", "piece", -6, -5, 12, 3, surface=14),
    ],
    # The middle is void, and the shop is what bridges it: ten blocks of nothing between the two crossings,
    # buildable from the first tick, which a stack of bought wood spans and nothing else on the board does.
    "zones": [{"id": "ford", "rect": [-6, -2, 12, 4]}],
    "walls": [],
    "placements": {
        # Piece-relative offsets in BLOCKS from the piece's minimum corner: a 4-cell piece is 20 blocks, so
        # 10,10 is its centre. `back` is +z, which is the way the crossing lies.
        "spawns": [{"id": "spawn-1", "piece": "camp", "at": [10, 10], "facing": "back"}],
        "wools": [{"id": "wool-1", "piece": "vault", "at": [10, 8]}],
    },
}

# The menu. **The currency is the kit's own wood**, which is the one thing on this board a player both
# starts with (64) and earns more of (16 a kill, from the studio's default kill reward): pgm-studio has no way
# to state a currency source yet, so a shop priced in anything else is a shop nobody can buy from. Trading the
# neutral blocks for the things a wool run actually needs is a real economy rather than a workaround — the
# corpus prices a third of its upgrade ladders in the tool they replace.
SHOP = {
    "id": "quartermaster",
    "name": "Quartermaster",
    "keeper": {"name": "`6`lQuartermaster", "mob": "Villager"},
    "categories": [{
        "id": "kit",
        "material": "gold ingot",
        "name": "`6Supplies",
        "items": [
            {"material": "golden apple", "name": "`6Runner's Apple", "price": 16, "currency": "wood"},
            {"material": "arrow", "amount": 16, "price": 8, "currency": "wood"},
            {"material": "ladder", "amount": 8, "price": 8, "currency": "wood"},
            {"material": "stained clay", "amount": 16, "price": 12, "currency": "wood",
             "teamColor": True},
            {"material": "iron fence", "amount": 8, "price": 24, "currency": "wood"},
        ],
    }],
}

FINISH = {
    "authors": ["Opus 5"],
    "created": "2026-09-12",
    "themes": {"coin": COIN_THEME},
    "mapTheme": "coin",
    "shops": [SHOP],
}


def write(name, document):
    path = os.path.join(HERE, name)
    with open(path, "w") as handle:
        json.dump(document, handle, indent=1)
        handle.write("\n")
    print(f"wrote {path}")


write(f"{BASE}.plan.json", PLAN)
write(f"{BASE}.finish.json", FINISH)
