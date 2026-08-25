# Ravensmere — a mere with an island in it, and a range behind the spawn

`maps/opus5-ravensmere` · `specs/opus5-ravensmere` · **152 × 302 blocks**, one open landmass ·
destroy, one destroyable a team · `rot_180` · 24 players · **single layer**

The brief, in the author's own order: rolling hills, ravines, a central lake with an island in the
centre, a forest, buildings scattered around a path, one large end-stone cube destroyable about 30 blocks
right and 50 ahead of spawn, 150 blocks between the two of them, a large sandy beach round the lake, the
seams between areas textured with brush strokes, a mountain backdrop behind the spawn, and a path seven
blocks wide of brick, granite and smooth granite. No second layer.

## The numbers the brief named

```
red spawn point      1, 26, 119
red goal centre     31, 33,  70        30 blocks right · 49 blocks ahead
blue goal centre   -30, 33, -69
goal separation                        151.8 blocks
```

The two are a straight consequence of each other: with the goal 30 right and 50 ahead of a spawn on the
board's own axis, the separation under `rot_180` is `2 · √(30² + 50²) = 116` — too short. Holding 30 to the
right and solving for 150 apart puts the goal 68.7 ahead of the spawn, and putting the *spawn* at
`z = 119` puts the goal at `z = 69`: 30 right, 50 ahead, 150.4 apart, all three at once. The spawn tier was
then placed to land the exported spawn point there, which it does at `z = 119`.

The by-product is that `GO1` passes without being aimed at — own 62, enemy 199, **ratio 3.21** against a
band of 3.0–4.0.

## What states what

**Constraints state the plan of the board; pushes state its relief.** A relief mark is honoured exactly and
has no falloff, so it can pin a lake bed at 15 or a yard at 26, and it can never be a
mountain. A push lifts the solved surface inside a drawn ring and its `crown` is what makes a landform of
it. Eleven marks and eleven pushes:

| | |
|---|---|
| `coast` rim, `mere`, `isle` | the water's own ground, and the island standing out of it |
| `downs`, `wood`, `apron`, `spawnpad` | the flats a player stands on |
| `goalpad`, three `yard-*` | written **last**, after everything else — marks resolve in order and the last wins, so the ground under the Wardstone and under each building is the ground stated for it |
| 6 hill pushes | `amount` 5–6, `crown` 3–4, **`falloff` 20**, `roughness` 0.55 |
| 2 ravine pushes | `amount` 0, **`crown` −14**, `falloff` 10 — a dished ring, not a cut |
| 2 range pushes | `amounts` 20–36 per ring vertex, `crown` 16, `falloff` 12 — the technique `showcase/19-mountain-range` is the worked example of |

Read back: `low 10 · high 75 · relief 65 · symErr 0`. The goal's flat reads 26 across its whole width, and
the ground round every building's footprint reads **1–2 blocks of spread**.

**A ravine is a push, not a mark.** The first pair of these were `line` marks at `h 12` — a height pinned
exactly, cut into ground the `wood` and `downs` areas hold level, which comes out as a slot with two
vertical walls. Two of them ran through the beach, where a sheer face has no business at all: a section
across the board read *sand, wall, sand*, which is quarrying rather than terrain. A push with a **negative
crown** dishes the ring it is drawn on toward its own medial axis and skirts the result out over `falloff`,
so the sides slope and the lip is a lip. Both are now in the wood and on the downs, and neither is in sand.

## The mere, and why the island is a hole in a ring

A `water` prop is a band round a **centreline**, not a filled outline, and `showcase/13-pond` records what a
closed ring does: *the loop itself came up water, and its centre came up dry* — a donut, filed there as the
mistake that turns a pond into a moat. It is the whole shape here. The mere is one closed ring of twelve
points on a 25 × 19 ellipse with `radius 12`, so the water runs from the island's edge out to about `r 37`,
and the ground inside `r 13` — pinned by the `isle` mark at `h 22`, six courses above the water — never
floods. The ring's own `shore` band gives the island a beach without a second prop.

The bed is the `mere` mark at `h 15` out to `40 × 30`. Beyond it nothing is pinned until the coast, so the
relaxation climbs from 15 to 24 over thirty-odd blocks: **that slope is the beach**, and it is large because
nothing was drawn to stop it being.

## Where a building may stand, and why it is searched rather than typed

A building seats on the **lowest** column of its own footprint and the terrain standing over that floor is
carved out of it. That is what lets a house dig into a bank instead of standing on a plinth, and it has no
opinion about how much bank there is: hand-sited on rolling downs, four of the first five houses landed on
footprints spanning 8 to 13 courses, and one of them sat **inside a ravine** — its own ground reading 11
against a 31-block wall three blocks away. Nothing declined any of it, because every cell had ground under
it. A house you cannot see is not a house.

So the sites are computed. `yards()` walks a two-block grid over the three flats and keeps a cell where

- the **whole footprint** is inside one of the flats — the same rings the `area` marks are written from, so
  "level ground" cannot mean one thing to the terrain and another to the search;
- it is outside every push's own exclusion. This is not the same as outside the push: what decides whether
  a building can stand is the **gradient** where it stands, and a push's is its lift over its falloff. A
  hill's ring interior is domed toward the medial axis and steep, so a building keeps out of the ring; its
  skirt at `falloff 20` is one course every four blocks — two across a footprint — and a building may stand
  on that. A ravine's side and a massif's flank are steep on any reading and are kept out of whole;
- it is 12 blocks off every road, 22 from the goal, and 24 from the last site taken.

Three sites survive on this board, which is six buildings across the orbit, and each one gets a `yard-*`
`area` mark written after everything else so the plateau is stated rather than hoped for. Measured on the
built world, the ground round each footprint reads **1–2 blocks of spread**.

**The hills changed to make room, and they are better for it.** At `falloff 12` a lift of 5 is a knoll at
one course every two blocks: a house standing anywhere on it has five courses of relief across its own
footprint, which is what its walls are. At `falloff 20` the same lift is one course every four. *Rolling* is
a statement about the gradient, not about the height.

The general fault is now a gate rather than a habit: `DR-SLOPE` declines a building whose footprint rises by
as much as the building itself stands — its wall courses plus the rise of its roof — shipped in pgm-studio
as `WE29`. It reports what this board found, on any board.

## The path, and the one thing it may not have

Four `stroke` props, `radius 3` — seven blocks across — paved with a `cell` material of brick, granite and
polished granite at `jitter 100, warp 0`, so the three read as laid stone rather than as a blend. A spine
from the spawn to the mere, a branch to the Wardstone, and a loop round each side of the water. All four are
`route: true`, which is what the standoff every other prop is filtered against is measured to.

**A path with a two-block riser in it is not a path**, and the first three builds had five of them. A push
crosses whatever it covers and its skirt is where its gradient lives, so the cause was hills sited where the
roads run — two of them on the beach, which is the last place a hill belongs. The hills moved onto the downs
and into the wood, the grain came down from 1.6 to 1.0, and the shore loops moved eight blocks inland off
the low ground. Measured per block over all **236 cells** of road:

```
spine    74 cells   steps > 1: 0
ward     26 cells   steps > 1: 0
shore-w  65 cells   steps > 1: 0
shore-e  71 cells   steps > 1: 0
```

## The seams

Eleven grounds and **five seam themes**, and a seam theme is not a twelfth ground: it is one step off each
of the two it stands between, so a stroke of it reads as the two mixing rather than as a third material
arriving. `seam-mere` (gravel and sand, the wet edge) rings the water; `seam-strand` (sand and grass) runs
round the back of the beach; `seam-scar` is a wide ribbon along each ravine with the narrower `scar`
ribbon inside it, so what is left of the wider one is exactly the shoulder; `seam-holt` is more podzol and less
grass along the wood's edge; `seam-crag` is the foot of the range. Paint scopes to the smallest shape
covering a cell, which is what lets one stroke carry a whole ground and a dozen sit inside it.

Every block in every palette is claimed by a paint family. Smooth sandstone (`24:2`) and the mushroom block
(`99:0`) are not, and the first build put them through the beach and the island: they read as magenta on
`render/surface` and say nothing about the ground they are on.

## What it measures

```
score 2.548 · valid true · symErr 0
goal destroyable-1 (The Wardstone): own 62 · enemy 199 · ratio 3.21
island team: cells 21353 · low 10 · high 75 · relief 65
export gate OPEN · <maxbuildheight> 95 · 4 region files
coverage: reached 19369 · decorated 3510 · dead 13239 of 36118 = 36.7%
provenance: tree 52 · boulder 20 · flora 12 · house 6 · stroke 8 · destroyable 2 · spawn 2 · ironcube 2
dressing: nothing declined
```

Two soft violations, both the shape of the board rather than a defect in it. **`G8`, fill-ratio 0.816**
against a band of `[0.201, 0.542]`: a landmass with no holes in it fills its bounding box, and the band was
learned from boards that have holes. **`LN2`, max-chain-length 150** against `[25, 110]`: that term measures
the longest run of *collinear, land-joined* pieces, and with every tier a different width the longest chain
here is the widest single piece — the board's own 150-block width. A lake with an island, a beach round it
and a road either side does not fit in 110.

**36.7% dead ground** is the beach, the water and the backdrop. Every dead patch is one block from used
ground; the two large ones are the quadrants of sand between the four roads. Four routes were drawn rather
than one partly to answer it. Whether a beach that players cross rather than
fight over should count against a board is the author's call, not a derivable one.

## Two readings

**The observer platform stands over the island.** `observer-spawn` seats a 6 × 6 bedrock pad at the board's
centre, which on this board is directly above the mere's island. `observerY` is 130 rather than the 90 it
was authored at, which puts it 108 courses up instead of 68; it is what the magenta square at the centre of
`render/surface` is, since the render draws the topmost block and no paint family claims bedrock.

**The 3-D preview drew this board flat, and the cause was a studio bug this board found.** Two brush strokes
drawn wholly on the mirrored half fell outside the compiled ground's own polygon — the compiler emits one
half and mirrors it — so the canvas read them as islands of their own, and `restoreIslandMeta` gave all
three the one saved id. A relief is keyed by island id. Fixed in pgm-studio as `C50`, with `SK12` added to
report a layout that carries one id twice; the strokes here are now folded onto the authored half, which is
where they belonged.
