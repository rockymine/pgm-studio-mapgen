# Scoriafell — one mountain between two valleys

The pass over it is the whole map. A single push builds the range, a second push cuts the defile
through it, and nothing else on the board makes a landform.

Slug `opus5-scoriafell` · 104 × 208 blocks · rot_180 · 20 a side.

## How it is meant to play

Two dale floors at y22, a mountain between them whose crest stands at y65–66, and one notch through
it whose floor is y34. The fell's ring runs from x −60 to x 60 on a board 104 wide, so the range
crosses it coast to coast: there is no way round, only over. A team leaves its lodge on the dale,
crosses its own valley floor, and climbs — 42 courses in 25 blocks, which is a scramble the whole
way — and then drops into a defile 4 blocks wide at the bottom with walls rising at 1.8 courses a
block on both hands. Whoever holds the notch holds the only crossing.

**It was briefed as a capture board and the studio cannot build one.** `controlPoints` and
`scoreLimit` are stated in the finish exactly as `tools/drive.py` documents them, and the studio
reads neither (below). Rather than ship a map nothing can win, the board carries one destroyable a
side on its own dale floor, so the thing the pass is *for* is reaching the other valley. The three
capture points stay in the finish as the authored intent and will mean something the day the field
exists.

## What the ground is made of

- **ground** — volcanic. Ash grey (gravel, light grey clay), scoria (cobble, andesite), and a
  genuinely black note on the crags (coal block, black clay). This is the run's only dark board and
  it commits: 83.9% of the ground is the `scoria` theme.
- **built** — dark oak on nether-brick footings. Timber against stone, so the lodge never reads as
  an outcrop.
- **accent** — ember, used once. The `fumarole` theme is 246 cells, 1.1% of the board, beside the
  pass; and one bed of netherrack runs through the strata everywhere.

Census: `scoria` 83.9% · `ashdale` 14.9% · `fumarole` 1.1%, with borders.

The surface of each theme is a `layered` stack on the **slope** axis, so the ash flats, the scoria
shoulders and the black crags are one material sorted by angle rather than by height. Every pattern
is two blocks, never a family, on cells 11 to 15 across.

## The techniques, and what each one bought

**A mountain is a push.** A point mark at height builds a drum — a flat disc on a sheer wall —
because a mark is a constraint honoured exactly and the relaxation has one cell to make the
transition in. The fell here is a twelve-vertex ribbon whose ring is its own rot_180 image, so the
symmetry fan lays it back over itself instead of beside itself, and `amounts` carries one lift per
vertex so the crest falls the way the ring was drawn. Vertex *i* pairs with vertex *i*+6, which is
what makes the dip at x ≈ 0 symmetric by construction rather than by luck.

**The two gradients have to agree.** Outside the ring the ground climbs at `amount / falloff`;
inside it at `crown / half`. 26 over a falloff of 16 is 1.63 courses a block; a crown of 18 over a
half-width of about 11 is 1.64. The transect proves it:

    (-40, -70) -> (-40, 0)
    23 23 23 ... 22 22 22 ... 22 23 24 26 28 30 32 34 35 38 40 42 44 45 45 46
    47 48 49 51 53 54 56 58 60 62 63 64

y22 to y64 over 25 blocks — **1.68 courses a block, continuous, with no step at the ring**. That is
the whole test the range had to pass, and it is the difference between a mountainside and a cliff
with a hill on top of it.

**The pass is a negative push.** A negative amount lowers and a negative crown dishes the ring
rather than doming it, which is a defile and not a col. Across it:

    (-52, 0) -> (51, 0)
    59 60 61 62 63 ... 66 66 66 66 | 64 63 62 60 58 56 54 52 51 50 49 48 47 46
    45 43 43 41 40 38 37 35 35 34 34 35 36 37 38 40 41 43 44 45 ... 64 65 65

Crest y66, floor y34, crest y65 — a 32-block notch, and the descent is in 1- and 2-block steps all
the way, so it walks.

**Only ground a player walks is pinned.** Four marks: the two dale floors, the pass floor, the spawn
apron (and its room pad). The flanks carry no mark at all, and `reach: 0` goes with that — a finite
reach pulls the flanks back toward base and the range falls apart into separate hills. Every ring is
a nine- or eleven-point lobed outline; a four-vertex rectangle builds a literal square mesa.

**And the pass is the pass, measured rather than asserted.** The board's sentence needs the crossing
to be easier at the notch than anywhere else, which is a comparison and not a picture:

    over the ridge, off the pass (x -46)   rises 27, falls 23, worst step 4: 4 barrier, 6 scramble
    through the pass            (x   0)    rises 21, falls 21, worst step 2: 0 barrier, 5 scramble

Four barriers on the flank against none in the notch, and a raider's whole journey from spawn to the
far dale's goal is 152 blocks, 3 placed, worst drop 7.

## What went wrong

**Capture points are missing from the system.** `drive.py` documents `controlPoints` and
`scoreLimit`, prints them on the run (`3 capture point(s): The Scoria Pass, North Dale, South
Dale` · `score limit 750`), and patches them onto the intent. The studio answers:

    RQ3  field 'intent.controlPoints' was not read
    RQ3  field 'intent.scoreLimit' was not read

and the exported `map.xml` contains no capture element of any kind. `PUT /map/{slug}/intent` — the
route `reports/opus5-threap-edge-run.md` says grew the feature — answers the same two `RQ3`
complaints on a 200 when asked directly, so no route carries it now. I checked three ways before
writing this down, as the skill requires: by **name** — `controlPoints`, `scoreLimit`,
`capturePoint`, `hill`, `koth` return nothing anywhere in `openapi.json`, and `MapIntent` carries
`additionalProperties: false` with no such property; by **what it would do** — no rule in
`GET /api/rules` mentions a control point, a capture or a score limit, and no route under `/paths`
answers one; by the **term catalogue** — `GET /api/rules/terms` has no capture, point, score or
hill term. The gap is real, and it is in `drive.py`'s documentation rather than in the studio's:
the driver describes a key the studio has no field for.

**`RL6` caught the pass stepping off its own outline.** The first notch was `amount −13, falloff 11`
against `crown −6`, and the rule named it exactly: *"climbs its skirt at 1.2 and its crown at 0.6
blocks a block — 2.1× apart, the skirt the steeper — so the ground steps where the two meet, at the
push's own outline."* A crown of −12 brought them to 1.18 and 1.20 and the step went.

**`relief.stairs` is not a field.** Stated on the first build and answered with `RQ3`.

**`OB19`'s keep-out is bigger than it sounds.** Adding the destroyable put the watch hut and a
spruce inside the goal's clearance at ranges that looked generous — the hut's near corner was 10
blocks from the anchor. Both were declined; both moved.

## Numbers

    03-slopes   17,505 walked · 2,923 scrambled (13.5%) · 1,204 barrier (5.6%) · 20 faces, largest 241
                13.5% scramble, 5.6% barrier — the scramble share of a mountain, which is what it is
    relief      group team  cells 10,816  low 8  high 66  relief 58  symErr 0
    06-claims   placed 48, declined 0
    coverage    63.8% reached · 11.8% decorated · 22.1% dead · 2.4% route — the best of the four
    04-routes   no route between a spawn and a goal on the capture draft, which is what that read
                says on any board whose goals are not destroyables; the destroy goal answers it
    preflight   round-trip · mirror · buildability · traversability all pass — gate OPEN

## Coordinates to check in game

| what | where |
|---|---|
| the crest, west massif | (−40, 0) reads y64; the ridge line runs y65–66 either side of the notch |
| the pass floor | (−3, 0) to (3, 0) reads y34–35 |
| the climb that must not step | transect (−40,−70) → (−40,0): 1.68 courses a block, no step |
| the ember patch, used once | the `fumarole` ring about (−9, −9), 246 cells |
| the dale floor and its goal | (−30, −58), floating 4 over y22 |
