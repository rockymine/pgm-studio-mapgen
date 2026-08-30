# The map-experiment brief — three boards off one base

`rockymine-map-experiment` is a board the author drew **in the browser**, in the Sketch tool, rather than
through the API. Its spec folder therefore holds a `plan`, a `layout` and an `intent`, and its `finish.json`
carries nothing but authorship: the geometry *is* the layout, hand-drawn and not derivable from the plan.

**Every board goes through `tools/drive.py`, and a board that has not been driven is not finished.** The
driver takes a drawn spec as it takes a compiled one — it skips `/plan/compile` where a `layout` and an
`intent` are already on disk and drives those instead:

    python3 tools/drive.py specs/<slug> "<Map Name>" --out <worlddir>

That one call is the ascii grid, the flow read, `sketch/relief/read` (the only place `RL2` is heard), the
dressing declines, the preflight, the coverage read, the world export and **23 renders** into
`specs/<slug>/renders`. Taking a picture is not the same as looking at one: read `world-iso.png`,
`world-heightmap.png` and `world-traversability.png` before claiming a board is done. The driver **sweeps**
its own render directory, so a closeup that should survive the next run goes in `specs/<slug>/closeups/`.

Three boards are authored off it, one per agent, each on its **own slug** — the base is a starting composition
and is never overwritten. What follows is what the author asked all three for, then what separates them.

## The base, as drawn

260 × 250 blocks, `rot_180` about `(0, 0)`, 12 players, `cell: 5`.

| layer | `base_y` | holds |
|---|---|---|
| `ground` | 0 | `s0` the basin (11 vertices, height 25) · `s1` north mass (30) · `s2` south mass (30) · `s3` the island (25, floor 0) · the two spawn annotations |
| `Layer 2` | 30 | three polygons, height 5 |
| `Layer 3` | 25 | one polygon, height 5 |
| `Layer 4` | 35 | one polygon, height 5 |
| `Layer 5` | 35 | two polygons, height 5 |

**The four upper layers are a hint, not the terrain.** They are flat 5-block slabs stacked to say *a hill goes
about here*, and the author wants them replaced by relief — real hills and cliffs, with vertical in them —
rather than kept as steps. Nothing above `ground` is sacred.

**`s0` is the whole idea of the board.** It is the sunken basin between the two 30-high masses, drawn so its
vertex chains are shared with `s1` above it and `s2` below it — the ground either side fits it exactly. It is
also the shape that was disappearing from the mirror, which is what `pgm-studio`'s `TS66`/`C61` fixed and what
`SK17` now names.

Spawns sit at `(−90, 105)` and `(90, −105)`. There are **two destroyables a team**, at `(−90, 18)` and
`(−15, 98)` with their `rot_180` images, `float: 4`, and the build zone is the middle band `x −65..65`.

## What every board here must do

**The dip is water.** `s0` becomes a canal or river — filled, and free to cut deeper than the 5 blocks it
sits below its neighbours.

**The canal is walled, and the wall is drawn rather than sampled.** The author's own construction: trace the
canal's edge with a **thin, open sketch shape** — a `path`, or a polygon two blocks thick — laid exactly along
the boundary, so an actual wall separates the terrain from the water instead of a bank shading into it. The
outside face is straight; the **inside** carries a small relief that curves the bed down. Straight wall, dished
floor.

**A bridge crosses it,** with a pathway running to and from — the crossing is a route, not scenery.

**Three themes and no more, and each is a place.** One ground either side of the water, and the island its own.
Everything else — the hills included — takes the main ground. `TP10` scopes a theme on a shape, so the brush is
a polygon with a theme of its own, not a pattern turned up.

**No premade theme is used.** Every theme on these boards is authored for them. The author's own `grass clay`
theme is named specifically: do not bind it.

**One house style per theme area, two at the most, and the second is a variation of the first** — a repaint or
a roof change, not a second design. Fork a shipped preset (`GET /api/room-styles/{id}/json`) rather than
writing one from nothing. The island holds very few buildings; it has no room for a settlement.

**Both tree forms are usable.** The grown tree's severed trunks and floating limbs are fixed, and the four
boulder forms are fixed with them — `showcase/25` is the world that demonstrates both. A grown tree names a
`wood` and is shaped by its own knobs; `whorled: true` is the conifer against the broadleaf. Put the conifer
on earth ground and the broadleaf on grass, and give the erratics more than one form and more than one size.

**A pit under one of the destroyables,** and one goal sitting down inside a dip rather than on open ground.

**Props are wanted, and placed for a reason.** The hot-air balloon, clouds, a ship or boat in the canal; an
**airplane** and a **statue** are both asked for as new things to try. `showcase/` and `review/opus5-slipway.md`
say how a made thing is built out of layers and how it meets the ground — `seat: ground`, or an absolute floor
for anything that flies or floats.

**No sky-writing.** It was tried and the author has ruled it out. Spend the layers on the props instead.

## The outline stays edgy

**No Bézier handles on the coast.** The author drew the landmasses as straight-edged polygons and wants that
faceted silhouette kept — it is the board's look. `controls` may be used **inland**, where a curve is a
riverbank or a path rather than the shape of the map, and nowhere on the outer boundary.

## What separates the three

| board | brief |
|---|---|
| **Opus** (this session) | the full reading above — canal, walls, bridge, boat, pit, sky-writing, the lot |
| **Sonnet A** | the same base and the same constraints, its own composition |
| **Sonnet B** | the same base, **more open**: fewer things, more ground, a board that breathes |

**`opus5-slipway` is the warning as much as the reference.** It is the most recent authored board here and it
works, but the author's verdict is that it is **too full**. Its history is where two rules above come from:
four house styles was too many, its pattern count was too high, and a steep drop had to have a staircase
retro-fitted. Read `review/opus5-slipway.md` for what a finished board looks like, and take the fullness as
the thing to avoid.

## What the base already fails, measured

Driven against the live API before any of the three boards was authored. `POST /plan/evaluate` answers
`valid: false`, and **exactly one of the four terms is what makes it false**: `gap-hop-band` comes back
`kind: "hard"` and the three goal terms come back `kind: "soft"`. A soft term costs score and does not
refuse; fixing `G5` alone turns the plan valid.

| rule | term | kind | says | reading |
|---|---|---|---|---|
| `G5` | `gap-hop-band` | **hard** | `gap hop 25 outside 10..20 between 'piece' and 'piece-4'` | the two are too far apart to jump between. Move one, widen one, or put ground between them |
| `GO1` | `goal-spawn-ratio` | soft | `2.511 outside [3, 4]` | each goal sits 2.5× as far from the enemy spawn as from its own, against a band of 3–4 |
| `GO2` | `own-goal-distance` | soft | `111 outside [35, 65]` | the **two goals one team owns** stand 111 blocks apart by walk. Not a goal-to-spawn measure |
| `GO3` | `opposing-goal-distance` | soft | `205 outside [85, 150]` | the same walk read across the axis |

**The two goals per team are the author's, and they stay.** They were placed where they are on purpose, and
`GO2`'s band is what a pair of goals covered from one defensive position measures — a statement about a
convention, not about this board. `G5` is the one term a board must answer; the three `GO` terms are read,
weighed and left alone unless moving something else happens to improve them.

`POST /map/from-documents` answers **200** with `5 SK11 SK8`:

- **`SK11` ×4** — the four stacked hill layers are standable ground with open sky and **no route onto them**:
  990 places at `(42, 41) @31`, 990 at `(−65, −70) @31`, 360 at `(−46, −60) @41`, 358 at `(42, 41) @41`. This
  is the same fault `opus5-slipway` had to retro-fit a staircase for. Turning the slabs into relief-solved
  hills answers it at the root; leaving them as slabs means drawing the way up.
- **`SK8`** — the board carries no theme registry, no relief and no props. That is the whole of what these
  three builds are for.
