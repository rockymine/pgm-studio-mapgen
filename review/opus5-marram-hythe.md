# Marram Hythe — three grounds, and two different ways of meeting

> A destroy board on a shore. The monument stands on a built quay, so an attack crosses an
> open strand, climbs a dune field it can hide in, and has to get up a made face at the end —
> three grounds, and none of them costs what the last one did.

**In one sentence:** the board is the business of getting between its own grounds, and the
point of it is that the beach meets the dunes **two different ways** — by relaxation on the
west, where there is no mark between them at all, and along a cut bank on the east.

88 × 224 blocks, `rot_180`, one ground piece at base 16, a bar in the channel at 10, a quay
at 20. `GO1` own 52 · enemy 186 · **ratio 3.58**. Export gate OPEN, **no complaint, no
refusal, no decline**, 30 props placed.

## The two meetings, measured

This is the whole board, and it is one transect each.

| where | what is stated between beach and dune | measured |
|---|---|---|
| x **−34** (west) | **nothing but a berm** — the tide line at h9, a hummock, the dune toe at h13, relaxation between them | z −26 → −48: rises 4, **worst step 1**, walked |
| x **−20** (west) | the same | z −26 → −48: rises 3, **worst step 1**, walked |
| x **10** (east) | a `scarp`, `high 17 low 9`, `face 3`, six points | z −26 → −78: **BARRIER +3** at z −50, 2 scramble |
| x **30** (east) | the same scarp, further along its curve | worst step 2, 1 scramble, walked |
| x **40** (east) | the same | **BARRIER +3** at z −48, 2 scramble |

Not everything on a board meets the same way. The cut bank is six points, not two, so the
edge curves; and it runs the **east half only**, so the west half is a shore that rises into
its own dunes with no line in it anywhere.

## What made the flow possible was giving up a piece

An early draft had the strand as a plan piece at surface 9 against a links piece at 14 — a
straight five-block step the full 88-block width of the board, which is the straight meeting
this board exists to avoid. `fable-saltwharf` is the answer and it is one piece: `base` is the
**high** ground (there 22, here 16), `reach` is **0** so the marks decide the whole surface,
and the beach is a small `area` mark scooped out of it. What lies between the mark and the
dunes is the solver, and that is the flow.

`grain` is **0.7**. Saltwharf runs 0.7 and Ashcombe Delph 0.6; a larger amplitude is noise
laid over the answer, and it is the first thing that stops a solved surface reading as one
place.

**No pushes.** Six of the eight reference boards carry none, and this one does not need any:
four `point` marks at r5–8 with the relaxation between them are a dune field, where a push
would be a hill somebody stamped.

## The two grounds

| | base | reach | landform | marks |
|---|---|---|---|---|
| `team` — the shore | 16 | **0** | rolling | strand, apron, 4 dunes, a slack, the cut bank |
| `neutral` — the bar | 10 | **8** | plain | a flat landing, a knap |

Two reliefs, not one: the bar in the channel has its own base, its own reach and its own
landform, so the crossing reads as a different place rather than as more of the shore's field.
The composer emits no island in the middle, which is exactly why one is here.

The hop is **16** either side and the whole crossing **48** — `G5` wants 10–20 for the hop a
route depends on and 40–60 in total — and the build zone is exactly the bar's width, because
a mid-board stepping stone is used only across the width of the zone that reaches it.

## The made ground

The quay is `relief_scope: "exclude"` with a `base_height` of 20 and **no** `height_mode`:
`exclude` takes the footprint out of the solve, so the two tiers meet at a face. `hold` would
have brought the lower tier up to it and left no step and no reason for a stair.

Its outline is a plain quadrilateral and **nothing is cut into it**: a stair set into a made
face is a hole in the thing it is supposed to be, and a shed standing in that hole is inside
the stair. The way up runs **against** the west face instead, on the strip of ground between
the platform and the coast — 22 blocks of ramp for a 10-block rise, then six blocks of
landing level with the deck, so a player arriving has somewhere to stand and turn rather than
stepping off a slope straight onto a platform. It reads 9 → 20 station by station with a flat
top: `9 9 10 10 … 19 20 20 20 20 20 20`. The dune ramp climbs the east flank away from the
quay entirely, so the board is not one way in.

Both sheds stand **on the deck**, at ground 20 for every station of both transects, with the
road running to a door.

The face is where the quay's paint goes: a `wallDiagonal` at slope 2, four runs, one of them a
**`teamTint`**, so a player reads whose quay they are looking at from the far bank.

## What is on it

Four themes, and the census agrees: `links` 62.8%, `quay` 19.0%, `strand` 12.5%, `foreshore`
5.7%, with 776 cells of drawn border between them. The front of each island is a beach over
its whole extent and in two bands: `strand`, gravel over sand, from the water back to the dune
toe; and `foreshore` inside it along the tide line, a cell field of gravel, sand and clay, which
is the one thing on the board that says where the water is. The ground behind them is finished
**by angle** — marram on the flat and the shoulder, blown sand on a dune's steep face, which
nothing but the `slope` axis can tell apart.
Biome **Savanna**, whose grass tints `#bfb755`: Plains' `#91bd59` beside blown sand is a lawn.

**Sixteen hand-built trees**, cut out of `showcase/tree-showcase` with `tools/trees.py bodies`
as eight `copied` recipes — three squat `scrub` for the crests, five `pine` for the slacks.
`tools/trees.py verify` matches every one back to its recipe: four exact, twelve at 0.94–0.97
where a crown clipped a neighbour or the ground, which is what a hand-built tree does.

**A lighthouse**, on the bar at dead centre — the thing both teams cross toward and the one
landmark neither owns. It is **built**, not assembled out of two presets: a splayed plinth of
two nested discs, eight stilts, a shaft of six bands alternating quartz and red stained clay
and tapering 6 to 4, a colonnade of eight posts carrying an overhanging gallery, a parapet
ring, a glazed lantern with a glowstone lamp standing in it, and a dome cap. **Fourteen
layers**, every one `kind: "made"` and `part_of: "lighthouse"`.

Each colour band is its own layer because a layer holds one span per column and a colour change
splits a run as surely as air does. The hollow forms — shaft, rail, lantern — are single
even-odd polygons (`props.annulus`), because an outer circle minus an inner one is a `subtract`
and `SK13` reads a subtract as the board's negative space and refuses any add that fills it.

`props.py`'s emitters are **primitives**, not a lighthouse. Only the cap is one of them.

## What went wrong, third pass

The board was reviewed again with the platform, the ramps and the front named as the faults.
What that cost:

- **A `follow` shape is a floor, not a patch — and that is what flattened the whole front.**
  `relief_scope: "follow"` is answered outside the solver's three-way participation: the group
  is solved once, the shape is *seated* at the height the field settled on under it, and that
  one height is then pinned back over its **entire ring as a rigid area mark** and the group
  re-solved. Over a spawn plot that is the point — a door opens onto ground, not into rock.
  Over an eighty-block beach it is a slab: the strand came out level to the block for fifteen
  courses and every mark drawn inside it — three hummocks, a dune toe — was overwritten in
  silence. The reading names it plainly: `relief/read` reported a seam between `beach` and
  `dune-toe`, and `beach` is a shape, not a mark. A themed terrain patch states **no**
  `relief_scope` at all. It is then ordinary ground of the group: the marks shape it and the
  theme says what it is made of.
- **A theme only lands on a cell the shape FORMS the surface of.** `ShapeScopeOwners` gives a
  cell to a non-standing shape only where its top equals the ground already claimed there, so
  a patch stated at `base_height: 1` over an island stated at 16 runs nine courses under the
  sand, forms nothing, and paints nothing — on a 200, with the shape in the layout and the
  theme in the registry. It took 34 cells out of 15 178. Flush with the island at 16 and
  smaller in area, the same polygon takes 12.5%.
- **An `area` mark holds its height over everything inside its ring, the grain included.** The
  beach was one `area` at h9 drawn over the whole front, which is why the front was a table.
  The tide line is a `line` now, r3: it pins the water's edge and nothing else.
- **`bevel` is measured inward from the ring, so a strip narrower than twice it never reaches
  `h`.** A five-cell wet flat with `bevel: 4` is all shoulder — it solved two courses above the
  height it stated.
- **A push is a lift, not a texture.** `amount: 3` over a ring covering the whole strand raised
  the whole strand by three and inverted the tide line with it. What puts shape into relaxed
  ground is marks inside it, at small radii.
- **The front was grass because nothing painted it.** It is a beach now in two bands: `strand`
  (1 890 cells, gravel over sand) over the whole front, and `foreshore` (870) — a cell field of
  gravel, sand and clay — along the water's edge inside it. 18.2% of the board, against 0.2%.
- **The ground now has a shape.** `level` fell from 0.47 to 0.426 and `largestField` from 0.14
  to 0.082: the strand climbs from y9 at the tide line over three hummocks to a dune toe at
  y13, and the quay stands seven courses over it.

## What went wrong, second pass

The first build of this board was reviewed and most of it was wrong. What that cost:

- **The lighthouse built entirely out of grass and dirt.** The layer helper took a `material`
  argument and never applied it, so every shape fell to the map default. A made thing carrying
  neither a theme nor a material is terrain.
- **`cell` takes `palette`, and `jitter` and `warp` are required.** I used `entries`, which the
  studio does not read: inside a snapshot it is dropped in silence and the pattern renders as a
  flat swatch, and in a surface bucket the theme gate throws on the null and answers `RQ2` — a
  500 — rather than naming the field. Every path on every board of this run was a flat swatch
  because of it; all five are rebuilt.
- **The wall bucket painted every natural riser.** `wallOnTerrainFaces: True` over a grained
  dune field lays a brown web of sandstone across the marram, because a dune with grain in it
  is nothing but small risers. Off, and a dune's face is the surface stack's steep band, which
  is what the slope axis is for.
- **`17:5` is spruce on its side, not dark oak.** Dark oak log is `162:1`. Every post and beam
  on the board was the wrong wood.
- **Sand to bedrock.** Every surface band handed over to sandstone and the fill was a sandstone
  voronoi, so the board was sand all the way down. Sand is a surface fact: it lies on the steep
  faces and blows a course over the flats, and what is under it is soil and then rock.
- **A `raise` of zero is not flush — it stands one course proud.** The gravel freckles were
  plates somebody laid. `relief_scope: "follow"` takes the height the field settles on under
  the shape and holds it there, so the patch's top equals the ground it paints.
- **The board was a rectangle.** Seven of the eight reference boards reshape their compiled
  outline per vertex with `editShapes`; none bends. Two corner moves and two inserts cut the
  back corners off as triangles, and three more give the frontline a shape instead of a line.
- **The quay was 4.3% of the board and empty.** It is 19.0% now and carries two sheds — one
  style, two plots, differing in height and footprint and in nothing else — with the road
  running to a door.
- **There was no water at all.** Setting the pool's `radius` to 0 to silence `DR-DRY` deleted
  it: `radius` on a pool is the **shelf**, not a width. The lagoon it was dug for is gone from
  the board — the front is a beach against the void now, and what says where the water is on a
  board whose water is the crossing is the foreshore band, not a pool.

## What went wrong, first pass

- **`SK9`**: the sea-wall was stated as `floor 20, base_height 2` over a quay topping at 20.
  Among the shapes of one layer the taller add wins the column **floor included**, so the
  parapet deleted the quay beneath every cell it covered and the world kept only the wall.
  Stated from the quay's own floor — `floor 0, base_height 22` — it is simply the taller shape
  and the quay survives. This is the battlement case from `SCULPTING-WITH-LAYERS.md`.
- **`CT9`**, the frontline rotation hole, band [0, 0]: two bars facing each other across a gap,
  with a build zone either side, enclose a void between them. One wide bar has no hole in it.
- **`SK3`**: the sea-wall was `"type": "path"`. The studio draws five kinds and the fifth is
  **`polyline`** — the openapi description for `SketchShape.type` says "path", and a `path`
  draws no ground and says so on a 200.
- **`RQ1`**: `teamTint.neutral` is a **material**, not a block id.
- **`HS4`** twice: a window in a dark-oak wall must be cut from dark oak, and a door head's
  fill likewise. Forking a preset carries its spruce in.
- **`DR-DRY`**: `radius` on a **pool** is not a width — it is the *shelf*, how far in from the
  outline the bed is held up. A shelf on ground already at the water line is dug and holds
  nothing; that was all 56 dry columns.
- **`RL3`** twice: two marks that touch pin their bands exactly and the whole difference lands
  in one cell. The dunes were moved clear of the spawn apron.

## Coverage, and why it stands at 24.7%

Four dead patches of about 1 000 cells each, at (±36, ±80) — the back corners of the dune
field beside the spawn, one block from used ground. A board with one objective a side has two
journeys and the rear flanks are on neither.

The shipped boards this was measured against read **17.9%** (`opus5-blackden-sough`) and
**35.6%** (`opus5-burgage-terrace`) on the same kind of board; `opus5-heftfold` reads 0.0% and
is a wool board, which has more journeys by construction. 24.7% is mid-range for a single
destroyable, and the ground in question is a defender's rear. I stopped reshaping the board
for the number.
