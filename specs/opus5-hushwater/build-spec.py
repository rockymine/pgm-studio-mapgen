#!/usr/bin/env python3
"""Hushwater — a composed micro CTW board adapted into a place.

The board is a lead hush: two mine heads facing each other across the gill their own
water tore out of the fell, where the dressing floors at the top are flat and made and
everything below them is raw, angled ground.

The arrangement is the composer's. `GET /api/compose?players=18&teams=2&symmetry=rot_180
&seedStart=5` is pinned, read back as a PlanModel, and then adapted: the unit is pushed a
cell back so a shoal fits in the gill, the board is given a height ladder from the gill to
the mine head, the east wool is turned into a walled lane and the west one into an open
spur, a bing is cut off the team's own ground and bridged back, and the flat crossing
is given a spoil bank to fight over.

    PGM_STUDIO_API=... python3 specs/opus5-hushwater/build-spec.py
    tools/drive.py specs/opus5-hushwater "Hushwater" --out maps/opus5-hushwater
"""
import json, os, urllib.request

API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api")
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-hushwater"
NAME = "Hushwater"

DESCRIPTOR = {"players": 18, "teams": 2, "symmetry": "rot_180", "cell": 4, "seed": 5,
              "composerVersion": "body-first-1", "schema": 1}

CELL = 4

# ── the studio ────────────────────────────────────────────────────────────────────────────

def get(path):
    with urllib.request.urlopen(API + path, timeout=180) as response:
        return json.load(response)


def post(path, body):
    request = urllib.request.Request(
        API + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.load(response)


def delete(path):
    request = urllib.request.Request(API + path, method="DELETE")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            response.read()
    except Exception:
        pass


def composed():
    """The composer's own plan for this descriptor, pinned and read back. The pinned row is
    dropped again — the spec is what the map is, and the descriptor is what reproduces it."""
    page = get(f"/compose?players={DESCRIPTOR['players']}&teams={DESCRIPTOR['teams']}"
               f"&symmetry={DESCRIPTOR['symmetry']}&seedStart={DESCRIPTOR['seed']}&count=1")
    card = page["cards"][0]
    pinned = post("/compose/pin", {**card["descriptor"], "index": 0})
    plan = json.loads(pinned["planJson"])
    delete(f"/plans/{pinned['id']}")
    return plan, card


# ── the adaptation ────────────────────────────────────────────────────────────────────────

# Every rect is [x, z, w, h] in cells; a block is four of them. The composed unit is kept
# where it recognisably is — ring hub with its yard, a bar frontline fronting it, a spawn
# hung off the back, one wool approach a side — and re-cut piece by piece.
#
#  surface   what stands there
#     12     the shoals in the gill, and the gill's own floor level
#     13     the wash — the lowest bank, at the water
#     14     the bank the frontline is fought on, and the west spur out to the powder house
#     15     the dressing floors: the hub ring's three lower arms, the east lane, both rooms
#     16     the mine head's own floor, and the bing hung off its east side
#     17     the spawn

PIECES = [
    # the gill and the bank up out of it
    ("frontline-t2", "piece",     [-4,  5,  8, 2], 13),
    ("frontline-t1", "piece",     [-4,  7, 12, 4], 14),
    # the ring: three arms at the floor level, the back arm a course higher at the head
    ("hub-t2",       "piece",     [-4, 11, 10, 4], 15),
    ("hub-t3",       "piece",     [-4, 15,  4, 4], 15),
    ("hub-t4",       "piece",     [ 4, 15,  5, 4], 15),   # the east nose the lane leaves from
    ("hub-t1",       "piece",     [-4, 19, 10, 4], 16),
    ("spawn-t1",     "piece",     [-2, 23,  4, 2], 17),
    ("spawn-room",   "spawn",     [-2, 25,  4, 2], 17),
    # west: the open spur out to the powder house, on moor rather than on made ground
    ("wool-a-t1",    "piece",     [-10, 15, 6, 4], 14),
    ("wool-a-room",  "wool-room", [-13, 16, 3, 2], 14),
    ("wool-a-apron", "piece",     [-13, 18, 3, 1], 14),
    # east: the walled lane out to the assay house
    ("wool-b-t1",    "piece",     [ 9, 15, 4, 4], 15),
    ("wool-b-room",  "wool-room", [13, 16, 2, 3], 15),
    ("wool-b-apron", "piece",     [13, 15, 2, 1], 15),
    # the bing: a team's own ground, cut off and bridged back — the spoil heap the
    # defence drops onto to get in behind its own wall
    ("bing",         "piece",     [ 9, 22, 4, 3], 16),
    # the gill's spoil bank — two legs, each the other's rot_180 image, so the short hop is
    # on the west hand for one team and the east for the other
    ("shoal-n",      "piece",     [-4,  0,  6, 2], 12, False),
    ("shoal-s",      "piece",     [-2, -2,  6, 2], 12, False),
]

ZONES = [
    # the crossing: one region, docking both frontlines, with the shoal standing in it
    ("mid-band",        [-4, -5, 8, 10]),
    # the two planks onto the bing — team ground on both ends of each, which is what makes
    # the bing a team transient-link (CT4) rather than a mid stone
    ("bing-plank-s",    [ 9, 19, 4, 3]),
    ("bing-plank-w",    [ 6, 20, 3, 5]),
]

WALLS = [("hub-t4", "wool-b-t1")]

PLACEMENTS = {
    "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [8, 4], "facing": "front"}],
    "wools": [{"id": "wool-1", "piece": "wool-a-room", "at": [6, 4]},
              {"id": "wool-2", "piece": "wool-b-room", "at": [4, 6]}],
    # no iron: WX8 wants the cube inside the spawn piece and clear of the shell, and WX1
    # makes the shell that piece inset one block, so a plan-compiled spawn has no room for one
    "iron": [],
    "destroyables": [], "cores": [],
}

BOXES = [
    ("hub",       "hub",       [-4, 11, 13, 12],
     ["hub-t1", "hub-t2", "hub-t3", "hub-t4"]),
    ("spawn",     "spawn",     [-2, 23, 4, 4], ["spawn-t1", "spawn-room"]),
    ("wool-a",    "wool",      [-13, 15, 9, 4], ["wool-a-t1", "wool-a-room", "wool-a-apron"]),
    ("wool-b",    "wool",      [9, 15, 6, 4], ["wool-b-t1", "wool-b-room", "wool-b-apron"]),
    ("frontline", "frontline", [-4, 5, 12, 6], ["frontline-t1", "frontline-t2"]),
    ("mid",       "mid",       [-4, -2, 8, 4], ["shoal-n", "shoal-s"]),
]


def adapt(plan):
    plan["meta"] = {"name": NAME}
    plan["globals"]["surface"] = 12
    pieces = []
    for entry in PIECES:
        piece = {"id": entry[0], "role": entry[1], "rect": entry[2], "surface": entry[3]}
        if len(entry) > 4:
            piece["mirrors"] = entry[4]
        pieces.append(piece)
    plan["pieces"] = pieces
    plan["zones"] = [{"id": i, "rect": r, "holes": []} for i, r in ZONES]
    plan["walls"] = [{"a": a, "b": b} for a, b in WALLS]
    plan["placements"] = PLACEMENTS
    plan["boxes"] = [{"id": i, "kind": k, "rect": r, "members": m} for i, k, r, m in BOXES]
    return plan


def main():
    print(f"studio at {API}")
    plan, card = composed()
    before = {"score": card["score"], "structure": card["structure"], "spend": card["spend"],
              "topSoft": card["topSoft"], "descriptor": card["descriptor"],
              "pieces": len(plan["pieces"]), "zones": len(plan["zones"]),
              "walls": len(plan["walls"])}
    print(f"  composed  score {card['score']:.3f}  hub {card['structure']['hub']}  "
          f"front {card['structure']['frontline']}  wools {','.join(card['structure']['wools'])}  "
          f"land {card['spend']['unit']['cells']}/{card['spend']['unit']['budgetCells']:.0f}  "
          f"mid {card['spend']['mid']['cells']}")
    json.dump(before, open(os.path.join(HERE, "composed.json"), "w"), indent=1)

    plan = adapt(plan)
    json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
    print(f"  adapted   pieces {len(plan['pieces'])}  zones {len(plan['zones'])}  "
          f"walls {len(plan['walls'])}")


if __name__ == "__main__":
    main()
