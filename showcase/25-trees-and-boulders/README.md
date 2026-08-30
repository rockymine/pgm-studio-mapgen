# 25 — the grown tree, and the rock a glacier left

**The technique: the two props that are shapes rather than materials — the `grown` tree beside the
`template` tree that is its control, and the glacial erratic in all four of its forms from 3 blocks of reach
to 10 — on a board that holds nothing else, so what separates them is the only thing in the picture.**

The plan is `02-theme`'s with one change: the field is **28 × 20 cells rather than 20 × 20**, so the board is
140 × 100. That is the change the technique needs and the only one. On the square, once the two
destroyables' 21-block clearance is taken out, the free ground is two strips 28 blocks wide down the east
and west edges — one column of trees fits in one, and a size-10 erratic beside it does not. Widening x gives
each family its own column with a gap between them and moves nothing else: the goals, the spawns and the
theme are `02-theme`'s.

The finish adds a `dressing` block of eleven props, all on the **west half**. `rot_180` fans each to the
east, so eleven statements build twenty-two props and the two halves are the same board read twice.

## The document

A grown tree names a **wood** and is shaped by knobs; a template tree names a **species** and is scaled by
height. They are two trees, not two settings of one, and the pair below is the control:

```json
{ "kind": "tree", "id": "oak-grown",    "x": -50, "z": -22, "seed": 12,
  "form": "Grown",    "wood": "oak",    "height": 20, "stems": 1 },
{ "kind": "tree", "id": "oak-template", "x": -50, "z":   0, "seed": 13,
  "form": "Template", "species": "oak", "height": 20 }
```

Same height, same wood, twenty-two blocks apart. Everything that differs between them in the world is the
difference between the two forms.

An erratic is a form, a size and a stone:

```json
{ "kind": "boulder", "id": "erratic-10", "x": -24, "z": -9, "seed": 23,
  "form": "round", "size": 10, "mossy": true,
  "rock": { "kind": "solid", "id": 1, "data": 0 } }
```

Every rock on the board is that same `solid` stone, so the only thing that varies down the column is the
form and the size. `size` is reach from the middle and runs **2 to 10**; the six here are `round` at 3, 6 and
10, `angular` at 7, `outcrop` at 8 and `cairn` at 6.

## What separates the two trees

**A template tree is a trunk under a canopy profile.** Its crown is a radius per course, so it comes out as a
solid ball on a straight pole — `world-foliage.png` shows it as a perfect violet **circle**, third down the
west column, and nothing else on the board is round like that.

**A grown tree is a skeleton with foliage gathered at the tips.** `TreeSkeleton.Grow` wanders a central axis
up through the crown and staggers laterals along it at about 60° off vertical; `SweptVolume` fills each limb
as a capsule along its spline; `TreeCrown` hangs one small perforated cluster on each outer tip and keeps a
seam of air between neighbours. In plan that is a spidery irregular crown with the branches showing through
it, and in `world-iso.png` it is a tree with visible timber inside its foliage rather than a green ball.

The grown crown is **lace and reads thinner** than the template's beside it. That is the corpus's own
finding rather than a defect: 75 hand-built trees carry **6.2 occupied neighbours per leaf** and **24% block
over the crown's own volume**, with no interior at all, and the grower now sits at 7.5 against a solid's
12.5. A crown you cannot see the branches through is the tell of a generated tree.

`stems` is the other knob worth a slot: `triple-grown` is the same height and wood with three stems off one
base, which is the shape a coppiced tree has and the template form cannot make at all.

## What an erratic is

**A boulder is a mass a glacier carried and left** (the author's ruling), so it stands on the ground and is
bedded into it: `BoulderShapes.Bed` is **0.30** of the rock's height under the surface, and the rest of it is
over. `BoulderShapes.Of(form, size, seed)` answers three lobes — a main mass, a haunch at its foot and a
shoulder over it, the latter two thrown out on bearings hashed from the rock's own seed — so the plan
outline is a rounded irregular blob, the elevation leans, and two rocks of one form and size are two
different rocks. `Geom.Blob` erodes the quadric with a field sampled at a **three-block scale**, which
weathers a surface into facets.

The lift puts the widest course a little above the ground, so a rock overhangs its own foot the way a
perched erratic does while the foot stays nearly its full width — which is what reads as weight rather than
as balance. `outcrop` is the one form that still emerges from the surface, because an outcrop is bedrock
showing through rather than something carried here; on the board it is the flat wide slab in the middle of
the rock column.

## What to look at

| Picture | What it says |
|---|---|
| `renders/world-foliage.png` | the template's circle against the grown trees' spidery crowns — the whole lesson in one plan |
| `renders/world-iso.png`, `world-iso-turned.png` | whether a tree has bulk and whether a rock reads as a rock. It is the only view that answers either |
| `renders/world-topdown.png` | the six rocks in plan, size 3 → 10 down the column, with the flat outcrop among them |
| `renders/world-section-x0.png` | a rock in section: how much of it is over the ground and how much is bedded |

## The numbers

**On this board.** Every prop's blocks, read out of the built world and filed by what a player sees — a body
is a set of blocks joined face to face, because a block joined only at a corner has air on all six of its own
faces and is seen straight past:

| | blocks | bodies | blocks with air on all six faces | bodies resting on nothing |
|---|---|---|---|---|
| the ten trees | 6,052 | 8 | **0** | **0** |
| the twelve rocks | 13,674 | 12 | **0** | **0** |

Twelve rocks are twelve bodies. The ten trees are eight because two pairs of crowns touch, which is what
trees twenty-two blocks apart do. The dressing pass declined nothing.

**Against what these props built before the fix that this board exists to show.** Measured over 32 grown
trees on a flat probe board — every height from 6 to 40, one to three stems, staggered and whorled:

| | before | after |
|---|---|---|
| blocks placed | 27,228 | 21,638 |
| face-connected bodies | **3,106** | **32** — one per tree |
| blocks with air on all six faces | **1,912** | **0** |
| pieces resting on nothing | **3,069** | **0** |
| worst single tree | 394 bodies, 235 floating blocks | 1 body, 0 |
| trunks severed, of 768 grown | **396** | 0 |
| branches severed, of 10,362 | **5,472** | 0 |

and the rock, at the six forms and sizes this board states, measured in the rock's own frame at the seed the
board gives it — blocks, courses standing over the ground, blocks across:

| form | size | before | after |
|---|---|---|---|
| round | 3 | 89 / 3 / 7 | 99 / **5** / 5 |
| round | 6 | 763 / 6 / 13 | 845 / **8** / 11 |
| round | 10 | *clamped to 7* — 1,207 / 6 / 15 | **3,932 / 14 / 20** |
| angular | 7 | 1,199 / 7 / 15, **10 bodies, 9 blocks in mid-air** | 1,385 / **10** / 15, **1 body, 0** |
| outcrop | 8 | *clamped to 7* — 1,130 / 4 / 21, **3 bodies, 2 in mid-air** | 2,123 / 5 / 25, **1 body, 0** |
| cairn | 6 | 595 / 10 / 11 | 607 / **12** / 11 |

Two things run through that table. The rock **stands taller for its width** at every size, because its middle
is lifted clear of the surface instead of sunk to it — `round 3` goes from a 3-course lump 7 across to a
5-course rock 5 across. And the **angular form stopped shedding chips**: its erosion field used to turn over
every block, which at that amplitude cut nine blocks loose into the air and left the rock in ten pieces; at a
three-block scale it weathers the surface instead of chewing it.

`reports/opus5-trees-and-boulders.md` is the full account with the coordinates each figure was taken at.

## Limits

**Two crowns twenty-two blocks apart touch**, so the tree column reads as eight bodies rather than ten. On a
board whose point is the comparison that is a cost of putting the pair close enough to compare; a wood wants
them touching anyway (`16-forest`).

**The whorled conifer is not on this board.** It is a third silhouette and it still misses the measure that
separates a hand-built conifer from a broadleaf — its widest tenth sits at mid-height rather than in the
bottom third (`G173`) — so putting it beside a template spruce here would state a comparison that is not
finished.

**63% of the ground is dead**, against `02-theme`'s 75%. A square destroy board with two objectives and two
spawns has no route through its edges, and props do not make one: the coverage read counts a decorated
column as decorated and still dead, which is the honest answer.
