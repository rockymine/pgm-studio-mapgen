"""Writes opus55-clasp's plan and finish.

The arrangement is composed board p20 rot_180 seed 4 (`composed-seed4.plan.json`, the composer's raw answer),
taken over: the hub is widened two cells toward the clamp so its hole is three cells by four, the clamp wool
moves with it unchanged, the spawn is brought level with the hub's middle piece, the spawn and the back wool
room are deepened, and each wool approach carries one bedrock wall behind a neck.
"""
import copy
import json
from pathlib import Path

HERE = Path(__file__).parent

composed = json.loads((HERE / "composed-seed4.plan.json").read_text())

BASE = 9

# Cell rects [x, z, w, h]. The hub's front and back bars reach two cells further east and its east side moves
# with them, so the hole between the two sides is three cells by four. The clamp keeps its shape with arms a cell
# longer, so its room stands sixteen blocks off the hub's side, the least a gap beside a goal may be; its front
# arm is split two cells from the hub so the wall on it has void past both ends, where a wall at the hub's own
# side is rounded off the bars that run on past it. The back wool leaves the hub through a neck two cells long,
# and its room stands sixteen blocks behind that neck's wall. That depth is what balances the two wools: a cell
# shorter and the clamp is the further walk from the spawn (WL9); the clamp a cell nearer the hub and the back
# wool is the further walk from the front (WL10). The spawn stands level with the hub's middle piece rather than
# its front bar.
RECT = {
    "hub-t1": [-4, 20, 11, 4],
    "hub-t2": [-4, 12, 11, 4],
    "hub-t4": [3, 16, 4, 4],
    "wool-b-t1": [7, 20, 6, 3],
    "wool-b-t2": [9, 14, 4, 3],
    "wool-b-room": [11, 17, 2, 3],
    "wool-a-t1": [-2, 26, 3, 4],
    "wool-a-room": [-2, 30, 3, 4],
    "spawn-t1": [-5, 16, 1, 4],
    "spawn-room": [-9, 16, 4, 4],
}
NECKS = [{"id": "wool-b-neck", "role": "piece", "rect": [7, 14, 2, 3]},
         {"id": "wool-a-neck", "role": "piece", "rect": [-2, 24, 3, 2]}]
BOXES = {"hub": [-4, 12, 11, 12], "spawn": [-9, 16, 5, 4], "wool-a": [-2, 24, 3, 10], "wool-b": [7, 14, 6, 9]}

# The clamp is walled at its front arm only; the back wool is walled across its arm.
WALLS = [{"a": "wool-b-t2", "b": "wool-b-neck"}, {"a": "wool-a-t1", "b": "wool-a-neck"}]

# The two rooms that were deepened hold a building seven deep at the back, with a yard nine deep in front of the
# door and the marker inside the building. A footprint is [x, z, w, h] in blocks from the piece's minimum
# corner. The back wool's room opens south onto its arm and the spawn's east onto the hub, which is the way
# a player arriving there faces. The clamp's room
# keeps the studio's default.
ROOMS = {
    "wool-a-room": {"footprint": [1, 8, 10, 7], "at": [6, 11]},
    "spawn-room": {"footprint": [1, 1, 7, 14], "at": [4, 8], "facing": "right"},
}

# The spawn's iron stands in its yard, where the studio's room read seats a cube clear of the building. Inside a
# spawn piece it renews itself.
IRON = [{"id": "iron-1", "piece": "spawn-room", "at": [11.5, 11.5]}]


def plan():
    doc = copy.deepcopy(composed)
    doc["meta"] = {"name": "Clasp"}
    doc["pieces"] += copy.deepcopy(NECKS)
    for piece in doc["pieces"]:
        piece["rect"] = RECT.get(piece["id"], piece["rect"])
        piece["surface"] = BASE
    doc["walls"] = WALLS
    for marker in doc["placements"]["spawns"] + doc["placements"]["wools"]:
        marker.update(ROOMS.get(marker["piece"], {}))
    doc["placements"]["iron"] = copy.deepcopy(IRON)
    for box in doc.get("boxes", []):
        box["rect"] = BOXES.get(box["id"], box["rect"])
        if box["id"] == "wool-a":
            box["members"] = ["wool-a-neck", "wool-a-t1", "wool-a-room"]
        if box["id"] == "wool-b":
            box["members"] = ["wool-b-neck", "wool-b-t1", "wool-b-t2", "wool-b-room"]
    return doc


def finish():
    return {"authors": ["Opus 5.5"], "created": "2026-09-22"}


if __name__ == "__main__":
    for name, doc in (("plan", plan()), ("finish", finish())):
        (HERE / f"{HERE.name}.{name}.json").write_text(json.dumps(doc, indent=1) + "\n")
