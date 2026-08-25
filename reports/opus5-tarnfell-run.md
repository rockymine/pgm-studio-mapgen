# Opus 5 — Tarnfell: a landscape, and the one number that decides whether ground rolls

## What I set out to build

A second brief from the same person outside this repository, and the opposite kind of board to the
first: **rolling hills, deep crevasses, a central lake with an island in the centre, a forest, some
buildings scattered around a path, a really nice sandy larger beach area around the lake, a mountain
backdrop behind the spawn with tall mountains, and one large endstone cube destroyable thirty blocks
to the right and fifty ahead of the spawn with a hundred and fifty between the enemies' pair.** A
main path about seven blocks wide meandering from the spawn over the hills, through the forest, to
the lake, with thinner paths splitting off to cabins and tents. The seams between areas textured with
brush strokes for a gentle transition, the peaks coloured **strictly with the brush**, and — the
instruction that shaped the terrain more than any other — *the relief nodes going past the actual
island itself, so the highest peaks and rolling hills are visible from the side of the map, rather
than the terrain dropping to the side and wasting the space.* No second layers.

What I built: `maps/opus5-tarnfell`, documents in `specs/opus5-tarnfell/`, the account in
`review/opus5-tarnfell.md`. 176 × 348, one landmass of 34,335 cells, y6 to y80, thirty relief marks,
sixteen strokes, 126 props, zero declines, export gate open.

## The finding this run is for

**A point mark's radius pins a flat disc, so a radius is a mesa and not a summit.**

`PointMark.Pins` yields *every* cell inside its radius at the stated height. Those cells are
constraints; the relaxation only shapes what is left between them. I gave the hills radii of 16 to 22
and the peaks 26 to 32 — reasonable-sounding numbers for a landform on a 176-wide board — and the
first build came out as **stacked plateaus with vertical faces**, because the discs nearly tiled the
board and there was almost nothing unpinned left to bend. The section along `x = 0` is unmistakable:
flat top, cliff, flat top, cliff, all the way from the mountains to the lake.

The same thirty marks at **radius 3 to 6** roll. Measured on `…/sketch/relief/read`:

| | radius 16–32 | radius 3–6 |
|---|---|---|
| walkable at one-block steps | terraced throughout | **95.1 %** |
| largest single place at that tier | — | **86.5 %** |
| walkable at two-block steps | — | 98.7 % |
| cliffs | one at every mark's edge | **6** |

The docstring says it — *"a radius of zero pins a single cell and reads as a spike; from about two up
it reads as a summit"* — and I read "from about two up" as a floor rather than as a range. It is a
range. **The rolling is the relaxation's; a radius is how much of the landform you are refusing to
let it do.** An `area` mark is the opposite instrument and is right where flat is the point: the lake
pan, the spawn terrace and the wardstone's shelf are the three level places on this board and all
three are areas.

## What I could not say

**Nothing, this time — the two hard instructions were both already in the solver.** Both are worth
writing down because neither is stated anywhere and both are the difference between the brief and a
near miss.

**A relief mark's centre may lie outside the land, and only its reach has to come back.**
`PointMark.Pins` iterates *its own* bounding box and keeps whichever cells `footprint.Inside` answers
for; `LineMark.Pins` walks `footprint.Land()` and measures each cell's distance to a polyline that
may lie anywhere at all. So a ridge traced twelve blocks out past the coast, with a radius of
fourteen, pins the coastal strip at its own heights and leaves the crest itself off the map — and the
board's edge is a mountainside cut through instead of ground decaying to `base`. Three of this
board's mountain marks are drawn entirely outside the polygon (`brow-n`, `brow-w`, `brow-e`) and a
fourth runs out through both ends of it. The heightmap shows every contour band in the mountains
closing on the frame rather than inside it, which is exactly what was asked for.

A mark placed *wholly* out of reach does nothing at all and says nothing about it — no `SK3`, no
warning. The check is the heightmap, not the document.

**Two flat marks butted against each other build as two terraces with a step at the seam.** The first
beach put a `shore-lo` band at y8 and a `shore-hi` band at y14 with their radii touching, and the
transect read `…7 7 7 7 [+5] 12 13 13…` — a five-course wall right round the lake, which is the
opposite of the gentle transition the brief asked for. Pulling them seven blocks apart and letting
the relaxation own the gap gives `7 7 7 7 9 11 12 13 13` — steps of one and two. **Unpinned ground
between two marks is not a gap in the design; it is where the design happens.**

**A crevasse is a `subtract` and cannot be anything else.** No relief mark of any kind cuts a hole:
the marks move a surface. `docs/tools/capabilities.md` says this and it is worth repeating because
"deep crevasse" sounds like a relief word. The four here are subtract polygons open at the coast and
closing inland, so the ground goes round and the board stays one component.

## What I got wrong

**I keyed the relief to an island that did not exist.** I named the island `fell` in a dict the
driver never reads — `addShapes` appends onto the island the *compile* emitted, which is called
`team` — and the first build answered `SK3: a relief is stated for island 'fell', which the layout
does not carry`, then `relief/read` with no islands at all, and the driver stopped. `"*"` is the key
for a board of one island. The finding named the fault exactly and the driver's own guard caught it
before a world was built.

**I gave the plan one piece and lost every plan-tier read.** With only the spawn on the board,
`SP9` complained that the spawn's door faced void zero blocks out and `GO1` answered `None` — both
true of the plan and both false of the world, where the door opens onto a polygon that reaches 170
blocks past it. Seven `piece` rectangles inset *inside* the drawn coast fixed it without squaring the
coastline off: the outline the board builds is still the polygon's, because the rectangles are a
subset of it. This is the second run in a row where a sketch-authored landform made the plan tier
measure a board that is not there, and the fix is the same both times — put ground under the plan
even when the plan is not what draws it.

**I read `world-material.png` and concluded the lake was missing.** The material top-down draws the
top *solid* block, so over water it shows the bed and the tarn reads as sand. The category top-down
has a `WATER` class and draws it cyan, and `…/column?at=0,22` answers `y5 Water · y4 Water · y3 Water
· y2 Sand`. One picture disagreeing with another is a question for `column`, and it took me a
render's worth of doubt to remember that.

## What worked first time

- **`rot_180` over a polygon authored on one half.** The coast is drawn on three sides and the
  fourth is the `z = 0` seam the mirror closes; the two halves fuse into one island and the relief
  folds across it. Symmetry error **0**, first build and every build after.
- **The lake.** One `water` prop traced as a wobbled ring at radius 25 with a band of 12, cut three
  courses into an `area` mark holding the pan flat at y6 — so the water line is level by construction
  rather than by luck, and the islet inside the ring stands ten blocks clear of it.
- **The two authored distances.** 30 right and 50 ahead came out exact; the pair measures 150.5
  because 30 and 50 fix it and 68.74 is not a block.
- **The brush on the peaks.** Six `rough` strokes along the crest and its shoulders, and the snow runs
  off the north, west and east edges with the ridge, which is what makes the frame read as a cut
  rather than a border.
- **`cube-4` in ender stone.** `<cuboid min="29,31,68" max="33,35,72"/>`, hollow on a bedrock core,
  four blocks over a shelf an `area` mark holds flat — no adjustment to `float` and no `OB17`.

## Open gameplay questions

**Is 60 % dead ground acceptable on a scenic single-goal board?** `…/coverage` answers 34,889 of
58,083 cells off every route, in two patches centred at `(±21, ±93)` — which is everything except the
corridor the one journey takes. The brief asked for a mountain backdrop, a forest, a lake and a beach,
and a board with one objective has one route; scenery is what the rest is *for*. I built it and
report the number rather than trimming the landscape to flatter it. Bringing it down means more
objectives, not less map.

**Should an island in a lake cost blocks to reach?** Getting onto the islet is 132 blocks and two
placed blocks — you wade and then climb its bank. I kept it, because an island that is free to stand
on is not an island; but nothing on it is worth the trip, so in practice nobody will make it.

**Should the crevasses be bridgeable?** `build.voidEnforcement` is left null, so they are. A DTM
board over natural terrain wants players able to cross what they can see across, and the crevasses
are flank scenery rather than a line anyone defends. Setting it would make them permanent walls,
which is a different map.
