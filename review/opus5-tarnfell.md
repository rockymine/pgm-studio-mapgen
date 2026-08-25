# Tarnfell — a mountain tarn with one stone in the hills above it

> A landscape DTM board, built to a brief from outside this repository: rolling hills, deep
> crevasses, a central lake with an island in it, a forest, buildings scattered along a path, a
> sandy beach round the water, a mountain backdrop behind the spawn, and one large endstone cube
> thirty blocks right and fifty ahead of the spawn with a hundred and fifty between the pair.

**In one sentence:** a drowned corrie — a tarn with a green islet in the middle of it, ringed by a
wide sand shore, held in rolling fell above which the mountains rise and run off all four edges of
the map, with one endstone wardstone standing on a shelf in the hills and a track down to the water
past three cabins and a lakeside camp.

176 × 248 blocks drawn (the coast reaches z ±173), `rot_180` about the origin, one landmass of
**34,335 cells**, ground from **y6 to y80**, build ceiling 100, symmetry error **0**.

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

## What is where

| Band | Ground | Carries |
|---|---|---|
| r < 8 | y16, an islet | one mossy cairn, ground cover at 0.45 |
| r 8..13 | y9, the islet's own sand | — |
| r 13..37 | **the tarn**, water at y5 over a bed at y2 | a `natural` water ring, 24 wide, cut 3 deep, banks of sand over gravel |
| r 37..49 | **the beach**, y7 | four courses of sand deep, so a shore dug into is still a shore |
| r 49..64 | the beach shelving up, y7 → 13 → 16 | the shore seam brush |
| \|z\| 58..104 | **the forest**, y13..30 | 56 trees — oak, spruce, birch — over podzol, ground cover at 0.5 |
| \|z\| 58..126 | **the rolling fell** | 14 hill and hollow marks, two pushes, three cabins, the wardstone's shelf |
| \|z\| 126..173 | **the mountains**, to y80 | bare rock, brushed |
| the flanks | **four crevasses**, void to y0 | `subtract` polygons ~8 wide, open at the coast, closing inland |

**A crevasse is a subtract and could not be anything else.** No relief mark of any kind cuts a hole:
the marks move a surface and a subtract removes the column. Each slot is open at the coast so the
ground goes round rather than being cut in two, and the board stays one component. Beside them the
**gully** is the other kind of deep — a `line` mark at y9–16 with the fell at 26–34 either side, so it
is a twenty-course ravine a player can walk down into and out of.

## The brush does three jobs

Sixteen strokes, and none of them is a road except the five that are.

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

**The seams.** Five `rough` strokes at **coverage 0.26 to 0.45**, each laid in the material of the
area on the *far* side of it, so most of the ground it crosses still shows and the join reads as a
gradient: sand-and-grass round the shore at radius 11, podzol-and-grass along both edges of the wood
at 9, andesite-and-coarse-dirt along the mountains' foot at 8, sand round the islet at 3.

## What it costs

`GET …/preflight`: **export gate OPEN**. Round-trip, mirror and buildability clean, traversability
connected for both teams.

The dressing pass places **126 props and declines none**.

`GET …/coverage`: **60.1 % dead** — 34,889 of 58,083 ground cells sit off every route. Both dead
patches are one block from used ground and centred at `(±21, ±93)`, which is to say: *everything
except the corridor the one journey on this board takes.* A single-goal map has one route, and a
mountain backdrop is scenery on purpose — but 60 % is the number, and it is the honest cost of the
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
