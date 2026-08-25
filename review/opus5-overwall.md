# Overwall — a labyrinth with a country standing on top of it

> Built to a brief from outside this repository: a labyrinth of pillars with walls in between, one
> destroyable inside one of its areas and a wool room in another, **every passageway twelve blocks
> wide**, relief on the floor the players walk *and* relief on the tops of the walls, trees inside
> it, and most of the boulders, trees and a couple of houses — houses on stilts — up on the walls
> out of the player's reach. A river inside the labyrinth. Smooth terrain, not many hills but some
> elevation. A bridge of sorts over the walls, on a third layer. And walls of an ordinary stone with
> a pattern in it, without too many colours.

**In one sentence:** a stone maze on a twenty-two block grid where every pillar is ten square and
every gap is twelve, with a river down the one corridor no wall crosses, a keystone in one court and
a wool room in another — and, fifteen to thirty blocks over your head, a second landscape of wooded
ridges, boulders, four houses on stilts and two brick bridges that nobody in the match will ever
stand on.

184 × 264 blocks, `rot_180` about the origin, **two islands** — 24,516 cells of floor from y10 to
y17, and 9,992 cells of wall from y32 to y42 — plus a third slab carrying the bridges. Symmetry
error **0** on both.

## Twelve, and everything else follows from it

The grid is **22 blocks node to node**; a pillar is **10 square**; a wall between two pillars is
**10 thick and 12 long**. So the gap between any two solids on the board is 22 − 10 = **12**, and it
is twelve between two pillars, between two walls, and between a pillar and a wall — there is no
second measurement anywhere in the labyrinth.

Seven node columns at x = 0, ±22, ±44, ±66 and eight cell columns between and beside them; four node
rows per half at z = 11, 33, 55, 77, with the seam row of cells straddling z = 0. **Forty open cells
of 12 × 12 on the authored half**, every one of them reachable from every other — the build script
floods the grid and refuses to write a document that has sealed a court off.

## The maze is a picture, and everything geometric is read off it

```
#######.#.#######     the spawn court's wall, open at two doors
#.......#.......#     z 88
###.###.#.#...###     z 77   ← the pillar at (44, 77) is out: the goal's court
#.........#...#.#     z 66
###.#.###.#.###.#     z 55
#.........#.....#     z 44
#.#...#.#.###.#.#     z 33   ← the pillar at (-44, 33) is out: the wool's court
#.....#.#.......#     z 22
###.#.#.#.###.###     z 11
#.....#...#.....#     z 0    — the seam, and a palindrome
```

Odd columns are cell columns and even ones are nodes; odd lines are cell rows and even ones are node
rows. `#` is solid and `.` is open — **including at a node**, where a `.` takes the pillar out and
merges the four cells round it into one **34 × 34 court**. Two of those are the objectives'.

The last line is the seam the mirror closes, so it is drawn once and stands once, and the two halves
of the board meet along the twelve-wide gallery it opens. It is a palindrome for that reason: what
is authored there and what the fan lays over it have to agree.

## Three slabs, and why none of them is driven into another

| Layer | `base_y` | Holds |
|---|---|---|
| `ground` | 0 | the floor, y10–y17, under its own relief |
| `walls` | 12 | the labyrinth, tops y32–y42, under a **second** relief |
| `span` | 38 | two bridges, deck at y44, parapets to y47 |

**Relief is keyed by island id across the whole stack.** `SketchRasterizer.ReliefFields` walks every
layer and looks each of its islands up in the one `relief` dictionary, adding that layer's `base_y`
to whatever it solves — so `{"team": …, "walls": …}` gives the floor and the wall tops separate
landscapes, and a layer's marks are stated in **its own frame**.

**The ground under every wall is a `hold` shape at y12.** The labyrinth's footprint is drawn a second
time on the ground layer with `relief_scope: "hold"` and a stated top of 12; a held shape pins its
whole interior and is applied after every other mark, so the floor is exactly 12 under every wall and
rolls freely between them. That is what lets the walls layer be founded at 12 sharing **one course**
with what it stands on, which is the seam `SK10` allows — and the board reports no `SK10` at all.

The same trick seats the bridges: four `area` marks hold the four pillar tops they land on flat at
y38, and the `span` layer's `base_y` is 38.

## The two courts

| | Stands in | Reached in | Room |
|---|---|---|---|
| **The Keystone** | the court at (44, 77) | own team **60**, enemy **211** — ratio **3.52** | a 3 × 3 × 3 ender-stone cube floating 3 over ground an `area` mark holds flat |
| **the wool** | the court at (−44, 33) | — | a 16 × 16 `wool-room` piece, walled in the labyrinth's own masonry |

The ratio is inside `GO1`'s 3.0–4.0 band, which took moving the goal's court one row north: at
(44, 55) it read 2.42, because a maze lengthens the enemy's walk and the defender's about equally
and what fixes the ratio is depth.

A **cube-3 is 27 blocks and obsidian is worth at most 3 of them** (`DC3`), so the keystone is ender
stone and the document says so rather than asking for obsidian and getting told.

## The river

One `stream` water prop, 4 blocks across and cut 2 deep, down **cell column x = 11 — the one column
no wall crosses** — from z 92 to the seam, then west to the origin, where it meets its own image and
the two halves make one river. A `line` relief mark at y10–11 with radius 3 cuts the channel a course
under the corridor either side of it, so the water lies level in a trench rather than as blue paint
on a slope, and there are four blocks of gravel bank to walk on each side.

Nothing else is planted in that column: a tree standing in the channel is declined `DR-CLAIM`, and
the east route is walked with the whole column excluded so no stroke repaints the riverbed.

## What is up there

The walls' own relief has twelve point marks on nodes at heights 20–30 and four `line` marks running
level along the two side walls and the two court walls, so a wall's crest **rises and falls along its
run** rather than capping flat. Ten courses of variation over a ten-wide network, and grain at
amplitude 1.3.

Standing on it, and reachable by nobody: **32 trees** — oak, birch and spruce, on pillar tops and
every third wall segment — **14 boulders** in cairns, outcrops and rounds, and **four houses on
stilts**, each a masonry storey carried on four spruce posts over six blocks of open air with a
ladder climbing through it. The lowest wall top is 15 blocks over the floor beside it and the highest
is 32.

The floor gets what is left: trees in the middle of the cells no route and no objective claims, one
per cell, so each is a thing to walk round in a twelve-wide corridor rather than a blockage.

## What the walls are made of

One stone family, and the pattern is a shape cut in it rather than a second palette.

**`wallFrame`** inks an edge material wherever the wall turns sharply enough — angle 38, so a corner
and a fillet both count — and along its **top and bottom two courses**, panelling a fill inside it.
The frame is a voronoi of stone brick, mossy brick and cracked brick at cell size 6; the panel is
stone and andesite as a noise field, with an `inward` band of a 2-block chequer under it so the
deeper courses of a thick wall differ from the face. Three faces of one brick and two greys: that is
the whole colour scheme of the labyrinth.

The crests are thin soil over rock — a noise of grass, coarse dirt and stone, one course, over coarse
dirt and stone. It is what a rampart's top looks like, and it is also what makes the board legible
from above: with grass on the walls as well as the floor the whole maze reads as one lawn.

The two bridges are the one thing built rather than grown, so they are dressed brick throughout with
a chiselled frame.

## What it costs

`GET …/preflight`: **export gate OPEN**. Round-trip, mirror (spawn, wool room and build all), and
buildability clean; traversability connected for both teams.

The dressing pass takes 55 prop documents and **declines none**.

`GET …/coverage`: **40.5 % dead** — 19,693 of 48,576 ground cells sit off every route, in one patch
centred on the origin and one block from used ground. On a maze that is the honest number: three
routes cross forty cells and the other thirty-odd are the alternatives a labyrinth is *for*.

**Twelve `SK11` complaints, all of them the bridges.** 272 places at y47 and 24 at y50, four times
over: standable ground with open sky and no route onto it. That is the brief — a bridge over the
labyrinth that nobody reaches — and the finding is the studio correctly noticing it rather than
something to fix. The wall tops raise none, because they are founded in the floor and share its mass.

## Where it departs, and why

**The bridges cannot be walked.** The brief said "a bridge of sorts over the labyrinth walls using a
third layer", and a bridge you can reach needs a stair up the outside of a pillar, which is a way
onto the whole wall-top world and would put the trees, the boulders and the houses in play. The
houses are the ones that were asked to be out of reach, so the bridges are scenery with them.

**`G8` reads a fill-ratio of 1 and `LN2` a chain of 128.** Both are the critic measuring a solid
board against a composed wool map; a labyrinth is one landmass with holes in it, and neither gates
anything.

**The mid band is a build zone.** The plan carries one across the seam gallery, because
`FannedGraph.Build` sets the frontline to the pieces a build zone touches and `SP1` reads *every*
wool on a zoneless plan as reachable only through a spawn. It is also the right zone to have: the
seam gallery is where the two halves meet.
