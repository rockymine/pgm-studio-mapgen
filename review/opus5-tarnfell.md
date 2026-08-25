# Tarnfell — a mountain tarn with one stone in the hills above it

> A landscape DTM board, built to a brief from outside this repository: rolling hills, deep
> crevasses, a central lake with an island in it, a forest, buildings scattered along a path, a
> sandy beach round the water, a mountain backdrop behind the spawn, and one large endstone cube
> thirty blocks right and fifty ahead of the spawn with a hundred and fifty between the pair.

**In one sentence:** a drowned corrie — a tarn with a green islet in the middle of it, ringed by a
wide sand shore, held in rolling fell above which the mountains rise and run off all four edges of
the map, with one endstone wardstone standing on a shelf in the hills and a track down to the water
past three cabins and a lakeside camp.

176 × 348 blocks drawn (the coast reaches z ±173), `rot_180` about the origin, one landmass of
**33,942 cells**, ground from **y6 to y80**, build ceiling 100, symmetry error **0**.

## The two distances the board is authored to

| Asked | Built | How |
|---|---|---|
| the goal 30 right and 50 ahead of spawn | spawn `(0, 32, 119)`, goal `(30, 69)` — **+30 x, −50 z** | the spawn faces `front` (−z), so its right hand is +x |
| 150 blocks between the two goals | **150.5** — `(30, 69)` and `(−30, −69)`, `2·√(30² + 69²)` | 30 and 50 are exact, so the pair is whatever they make it; 68.74 would have been exactly 150 and is not a block |

`<cuboid id="the-wardstone-region" min="29,31,68" max="33,35,72"/>` — a **4 × 4 × 4 endstone cube**
(`cube-4`, hollow on a bedrock core, which is what that style builds), floating four over a shelf the
relief holds flat at y27.

**The walk, placing nothing:** its own team reaches it in **62** blocks, the enemy in **209**. Ratio
**3.37**, inside `GO1`'s 3.0–4.0 band, and neither route asks for a placed block or a drop.

## The terrain, and the one thing that decides whether it rolls

Every height on this board is a relief mark: the plan states seven flat rectangles and a spawn, and
the ground is one 19-vertex polygon. Thirty marks and two pushes over one island, `base 20`,
`reach 36`, `step 1`, grain 1.9 at scale 9.

**A point mark's radius pins a flat disc, so a radius is a mesa and not a summit.** The first build
gave every hill a radius of 16 to 22 and every peak 26 to 32, and it came out as **stacked plateaus
with vertical faces** — the discs nearly tiled the board, so there was almost no unpinned ground left
for the relaxation to bend through. The same marks at **radius 3 to 6** roll:

| Read | First build | Now |
|---|---|---|
| ground walkable at one-block steps | terraced | **95.1 %**, largest place 86.5 % |
| at two-block steps | — | 98.7 %, largest place 98.0 % |
| cliffs | a wall at every mark's edge | **6** |

An `area` mark still pins its interior flat, and that is what an area mark is *for* — the lake pan,
the spawn's terrace and the wardstone's shelf are the three places on this board that are meant to be
level, and all three are areas.

## The mountains run off the edge, which is the whole point of where the marks are

The brief asked for the relief to reach past the island so the peaks are visible from the side rather
than the ground tapering to base and wasting the margin. It is a fact about the solver that makes it
possible: **a mark's centre may lie outside the land.** `PointMark.Pins` iterates its own bounding
box and keeps whichever cells the footprint has; `LineMark.Pins` walks the land and measures its
distance to a polyline that may lie anywhere. So a ridge traced eight to twelve blocks out to sea
pins the coastal strip at its own heights and puts the crest itself off the map.

| Mark | Runs | Heights | Reaches back |
|---|---|---|---|
| `brow-n` | `(-46,180) → (50,177)`, past the north coast at z ≈ 170 | 70 · 80 · 78 · 72 | 15 |
| `brow-w` | `(-98,104) → (-70,166)`, past the west coast at x ≈ −85 | 58 · 72 · 70 · 62 | 14 |
| `brow-e` | `(100,96) → (70,164)` | 56 · 70 · 68 · 60 | 14 |
| `ridge` | `(-96,148) → (100,140)`, across the board and out both ends | 58 · 67 · 73 · 69 · 62 · 56 | 10 |

The heightmap is the proof: every contour band in the mountains is cut by the frame rather than
closing inside it, and the four summits `peak-a`…`peak-d` (radius 3–4) put crests on the crest.

## The tarn is not a circle, and it did not have to be

**`rot_180` maps a shape centred on the origin onto itself**, so the only thing a lake at the centre
of the board has to be is symmetric about its own centre. A circle satisfies that and so does
anything else with a half-turn in it, which is the whole freedom the constraint leaves.

So every ring on this board is drawn from one profile of twelve radii covering half a turn, repeated
at θ+180° — an outline that maps onto itself by construction, and reads as a tilted oval with a
shoulder on one side and a pinch on the other rather than as a compass arc. The profile runs
0.86 · 0.93 · 1.03 · 1.13 · 1.17 · 1.10 · 0.97 · 0.86 · 0.90 · 0.83 · 0.78 · 0.80, smoothstepped
between entries so the outline has no corners, and a `swell` scales how far each ring departs from a
circle so an outer one can be gentler without stopping being the same shape.

The pan, the two shore lines, the waterline, the beach's paint scope, the islet and its bank and the
four shore seams are all traced from it, which is what keeps the beach an even band round a shore
that is nowhere an arc: the long axis reaches 47 blocks and the pinch 35.

## What is where

| Band | Ground | Carries |
|---|---|---|
| the islet | y16 | one mossy cairn, ground cover at 0.45 |
| its own sand | y9 | — |
| **the tarn**, 21–28 out on the profile | water at y5 over a bed at y2 | a `stream`-banked water ring 20 wide, cut 3 deep, banks of sand over gravel |
| **the beach**, out to 33–47 | y7 | four courses of sand deep, so a shore dug into is still a shore |
| the beach shelving up, to 43–61 | y7 → 13 → 16 | the two shore seams |
| \|z\| 58..104 | **the forest**, y13..30 | 56 trees — oak, spruce, birch — over podzol, ground cover at 0.5 |
| the flanks at \|z\| < 58 | **open fell**, y12..24 | 32 trees and 12 boulders over the band the beach and the wood both leave bare, with ground cover at 0.34 |
| \|z\| 58..126 | **the rolling fell** | 14 hill and hollow marks, two pushes, three cabins, the wardstone's shelf |
| \|z\| 126..173 | **the mountains**, to y80 | bare rock, brushed |
| the flanks | **four crevasses**, void to y0 | `subtract` polygons ~8 wide, open at the coast, closing inland |

**A crevasse is a subtract and could not be anything else.** No relief mark of any kind cuts a hole:
the marks move a surface and a subtract removes the column. Each slot is open at the coast so the
ground goes round rather than being cut in two, and the board stays one component. Beside them the
**gully** is the other kind of deep — a `line` mark at y9–16 with the fell at 26–34 either side, so it
is a twenty-course ravine a player can walk down into and out of.

## The brush does three jobs

Twenty-eight strokes, and none of them is a road except the five that are.

**The path.** `path-main` is **seven blocks across** (`radius 3.5`, `solid`, `coverage 1.0`), the only
stroke on the board that claims its cells as a `route`, and it meanders `(0,116) → (-13,106) →
(2,95) → (-11,84) → (5,72) → (-4,62) → (7,54) → (0,47)` — off the spawn terrace, over the fell,
through the wood, to the water. Four thinner ones split off it at `radius 1.4–1.6` and `coverage
0.8–0.85`, to the three cabins and the lakeside camp.

**The peaks, strictly.** The `crag` theme lays bare rock and stops there; every band above it is a
stroke traced along a ridge, because a stroke is the only instrument that follows a *line of ground*
rather than a footprint. Six of them: `peak-rock` at radius 13 in andesite and diorite over the whole
crest, `peak-pale` at 8 in diorite, `peak-snow` at 5 in snow, and three more on the shoulders that
run off the north, west and east edges so the frame cuts snow and not bare stone. All `rough`, so the
band's width wanders and no snowline is a drawn curve.

**The seams.** Seventeen `worn` strokes, and the style is the whole of it: **only `worn` spends
`coverage`.** It rolls a die per cell against it, which is what makes a band read as scattered
ground; `rough` wanders the band's *edge* and fills what is inside it solid, so a seam drawn with one
is a belt of a third material laid over the join — which is what a three-material voronoi at
`rough` had made of every boundary on this board.

Each seam is now **two grounds freckling into each other, one material to a stroke**: a wide thin
stroke at the far edge and a narrow dense one over it, so the density ramps from a scatter to about
half cover and no boundary is a drawn curve. Grass out to radius 8 at 0.24 and in to 4 at 0.34;
its opposite number in the same two sizes at 0.22 and 0.30 — sand round the shore, podzol along
both edges of the wood, andesite and coarse dirt at the mountains' foot, and one sand stroke round
the islet. Never a third material in a seam: a voronoi of three laid across a join is a new ground
over the top of it, which is what reads as noise wherever the two it stands between already differed.

## What it costs

`GET …/preflight`: **export gate OPEN**. Round-trip, mirror and buildability clean, traversability
connected for both teams.

The dressing pass takes **100 prop documents — 44 trees, 15 boulders, 6 buildings, 6 flora fields,
one water and 28 strokes — and declines none**.

`GET …/coverage`: **54.5 % dead** — 31,661 of 58,083 ground cells sit off every route. Both dead
patches are one block from used ground and centred at `(±17, ±103)`, which is to say: *everything
except the corridor the one journey on this board takes.* A single-goal map has one route, and a
mountain backdrop is scenery on purpose — but 54 % is the number, and it is the honest cost of the
brief rather than something the board hides. Bringing it down means more objectives, not less
landscape.

## Where it departs, and why

**The islet costs two placed blocks to get onto.** `…/walk?aim=reach` from the spawn to `(0, 10)`
answers 132 blocks and `blocks 2`: you wade the tarn and then climb its bank. That is a decision
rather than a defect — an island in a lake should cost something — but nothing on the islet is worth
going for, so nobody will.

**The plan tier is a stand-in.** The seven `piece` rectangles are inset inside the drawn coast and
exist so the reads that walk a plan have ground to walk; the outline the board actually builds is the
polygon's. Without them the spawn's door opened onto void at the plan tier (`SP9`) and `GO1` answered
nothing at all. `G8`'s fill-ratio reads 0.961 against a band of 0.201–0.542 and `LN2`'s chain 128
against 25–110 — both are the critic measuring a solid natural landmass against a composed wool
board, and neither gates anything.

**The build ceiling is 100**, because it is twenty over the highest ground and the highest ground is
a mountain at y80. Players may build eighty blocks over the lake. That is what a tall backdrop costs
and there is no second knob for it.
