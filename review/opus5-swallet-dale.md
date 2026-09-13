# Swallet Dale — the monument is inside the rock

> A destroy board on a limestone dale. Each team's monument stands in a chamber inside a
> crag, and the crag has three ways into it: a drift, an adit, and a hole in its roof.

**In one sentence:** crossing the strait is only the first half of an attack; the second
half is getting inside a rock with three doors, and the crag's roof is ground you can hold
without it helping you reach anything.

80 × 240 blocks, `rot_180`, dale surface 12, crag top 21. Strait 32 blocks of void.

## The stack, bottom-up

| layer | span | kind | is |
|---|---|---|---|
| `ground` | y0..y12 | ground | the dale. **Its surface is the gallery floor.** |
| `workings` | y13..y18 | **made** | the crag's rock — the complement of the corridors |
| `roof` | y18..y21 | **made** | the lid, drawn as rectangles *around* the chamber |
| `crown` | y21..y23 | **made** | the taller lid over the chamber, with the swallet cut in it |

Written bottom-up: the painter walks layers in document order and each pass paints its
layer's whole column from the bedrock course, so a storey listed after one that stands over
it finds no stone left.

## The gallery, and how it is stated

The corridors are stated **once**, as air, and the rock is derived from them by a grid sweep
(`complement()` in `build-spec.py`). Nothing is cut with a `subtract`: `SK13` reads one as
the board's negative space and refuses any add that fills it, on any layer. The rock is
what was not drawn, and the holes are the rectangles left out of it.

That matters for a reason the studio states plainly: **among the shapes of one layer the
taller override-add wins the column, not the later one.** A wall drawn across a corridor
would seal it whatever the document order, and the export gate would stay open.

Five corridors, 35 rock rectangles derived, 8 roof, 8 crown.

| way in | where | measured |
|---|---|---|
| west drift | opens on the crag's west face, x −28 | walk to monument: **walked end to end, 0 steps** |
| east adit | opens on the east face, x 20 | **walked end to end, 0 steps** |
| south adit | opens toward the strait, z −42 | **walked end to end, 0 steps** |
| the swallet | a 6×6 hole in the crown, drop ~9 into the chamber | reached over the roof: worst step 2, both scrambles |

The void scan reads **5 692 cells of open gallery, 0 of them sealed**.

## Why the layers say `kind: "made"`

The first build raised two `SK10`s and five `SK11`s — 7 332 and 2 208 places of "standable
ground with no route onto it". Every one was true and none was a fault: a crag sinking into
a dale has no gap to lose, and its roof is not a storey somebody forgot a stair to.
`SketchLayer.kind: "made"` is the word that keeps the stacking rules off it, and setting it
on all three cleared **both rules at once**. `part_of: "crag"` names the one thing the three
slices belong to.

(`SCULPTING-WITH-LAYERS.md` §6 still lists `kind: "made"` among the things that *could*
become a tool. It shipped; the document is stale on it.)

## Numbers

`GO1` own 55 · enemy 191 · **ratio 3.47** · slopes **13 248 walked, 1 342 scramble, 706
barrier**, faces 20 · claims **placed 9, declined 0** · coverage **23.2% dead** · export
gate OPEN, and after the last four fixes **no complaint of any kind**.

## What it is made of

`dale` (grass over limestone, slope-banded at 20°/40° against a measured 62.7% under 10°),
`crag` (strata in `wall` and `fill`), `gallery` (gravel and cobble over coal-bearing stone).

**The gallery floor is a covered column**, so it resolves one band stack and falls inside
`fill`: no turf, no rim, no wall, whatever its theme says about a surface. The gallery
patches are therefore there for their *fill*, which is what puts stone and coal in a mine
floor instead of the dale's own rock. This is also why `themes/census` reports one theme at
100% on this board — it is a surface projection and does not attribute a `made` layer.
`column` at (10, −50) shows the crag's own stone, andesite and diorite, so the paint landed.

## What went wrong

- `workings` and `roof` were driven **4 blocks into each other over 3 576 columns**: the rock
  span was y13..y21 and the roof y18..y21. Two layers may share exactly one course.
- The roof ramp stopped at the crag's face and **eased back into the ground over its last
  column**, leaving a 5-block barrier onto a roof it was drawn to reach. Overlapping the two
  footprints by two blocks and setting `skirt: 0` fixed it.
- The crown was three courses and stood a **barrier +3** over the roof — and the swallet is cut
  in the crown, so the third way in was unreachable. Two courses is a scramble.
- `SK23`: the first crown left 2-wide strips round the hole, where no column has ground on all
  eight sides, so only the rim and wall buckets paint them and the theme's surface appears
  nowhere. Every strip is now at least four wide.
- `DC3`: a `cube-3` is 27 blocks and obsidian is worth at most three of them. It is a `pillar-3`.
