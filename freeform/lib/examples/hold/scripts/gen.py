"""Knuckle Hold: a valley board on three floors, built from `hold.layers.json`.

    the valley        a river down the middle; on its east bank a hamlet of seven houses round a green and a keep,
                      the inn on the road to the arch; woods beyond the ridges
    the Shelf         a second ground at 68 resting on the Knuckle and hanging out over the meadow, its stream
                      falling into the river
    the arch          a stone deck over the river between two ridges, the road from the keep crossing it
    the cave          a mouth in the Knuckle's cliff, under the Shelf, down to a cavern under the hill; the miners'
                      shed in the meadow below it
    the hold          an undercroft under the keep reached by its roofed well, a crypt, cells and a cistern, a hall to each,
                      and the miners' tunnel from the cavern that broke into the crypt

The generator prints every layer as it ran and what each floor reads back: where the Shelf rests and how much air
is under it where it does not, the arch's span and the clearance under it, the cave's mouth, and every room's floor
and the steepest step on its halls.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import B  # noqa: E402
from pgmvox.document import layers  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
doc = json.load(open(os.path.join(HERE, "..", "hold.layers.json")))
built = layers.build(doc)
w, X, Z = built.world, built.X, built.Z
x0, z0 = int(X[0, 0]), int(Z[0, 0])

for s in built.steps:
    print(f"{s.stage:10} {s.level or '-':6} {s.id:20} {s.op:11} {int(np.asarray(s.changed).sum()):6} columns")
print()
for sf in built.surfaces:
    on = sf.top >= 0
    print(f"surface {sf.id:14} {sf.kind:6} {int(on.sum()):6} columns, y {int(sf.top[on].min())} to {int(sf.top[on].max())}")
print()

ground, shelf = built.surface("ground"), built.surface("shelf")
over = shelf.top >= 0
rests = over & (ground.top < 0)
hangs = over & (ground.top >= 0)
gap = (ground.ceiling - ground.top - 1)[hangs]
kept = sum(int(w.ids[i, int(ground.top[i, k]), k] != 0) for i, k in np.argwhere(hangs))
print(f"the Shelf: rests on {int(rests.sum())} columns, hangs over {int(hangs.sum())}; under it the ground stands in "
      f"{kept} of {int(hangs.sum())}, with {int(np.median(gap))} blocks of air (least {int(gap.min())})")

arch = built.surface("arch")
span = arch.top >= 0
water = ground.water
under = []
for i, k in np.argwhere(span & (water > 0)):
    rock = next(y for y in range(int(water[i, k]) + 1, int(arch.top[i, k]) + 1) if w.ids[i, y, k] != 0)
    under.append(rock - int(water[i, k]) - 1)
print(f"the arch: {int(span.sum())} columns of deck, y {int(arch.top[span].min())} to {int(arch.top[span].max())}, "
      f"{min(under)} to {max(under)} blocks of air over the river")

mouth = doc["carve"][[L["id"] for L in doc["carve"]].index("cave-mouth")]["pts"][0]
mx, my, mz = int(mouth[0]), int(mouth[1]), int(mouth[2])
face = next(x for x in range(mx, mx - 12, -1) if w.ids[x - x0, my + 3, mz - z0] != 0)
roof = next(y for y in range(my, w.sy) if w.ids[face - x0, y, mz - z0] != 0)
print(f"the cave mouth: at x {face} z {mz} the face opens from y {my} to {roof - 1}, rock over it to y "
      f"{w.top(face - 1, mz)}")
cavern = built.surface("cavern")
print(f"the cavern: {int((cavern.top >= 0).sum())} columns of floor at y {int(cavern.top.max()) + 1}")

dungeon = next(L for L in doc["carve"] if L["op"] == "rooms")
floor = built.surface("dungeon").top
for r in dungeon["rooms"]:
    a0, b0, a1, b1 = r["rect"]
    room = floor[a0 - x0:a1 - x0 + 1, b0 - z0:b1 - z0 + 1]
    print(f"room {r['id']:10} floor y {r['floor']}: {int((room == r['floor'] - 1).sum())} of {room.size} columns")
step = 0
for a in (0, 1):
    pair = (np.take(floor, range(1, floor.shape[a]), a) >= 0) & (np.take(floor, range(floor.shape[a] - 1), a) >= 0)
    step = max(step, int(np.abs(np.diff(floor, axis=a))[pair].max()))
print(f"halls: the steepest step between neighbouring floor columns is {step}, "
      f"{int((w.ids == B.STONEBRICK_STAIRS).sum())} stairs")
print(f"the well: {int((w.ids == B.LADDER).sum())} ladders from y {dungeon['rooms'][0]['floor']}")
w.save(sys.argv[1], "knuckle-hold", (118.5, 41, 92.5))
print("generated")
