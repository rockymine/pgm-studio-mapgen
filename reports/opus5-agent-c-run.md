# Opus 5 · agent C — the dark, wet, green set

Four boards in one family: basalt, dark spruce, moss, peat, deep water, slate, wet leaf litter.
`opus5-peatgarth` was built by the previous agent C before it was interrupted; its identity sentence
below is recovered from the spec and the built world rather than from a report, because it never
wrote one. The other three were authored against it so that they answer to it instead of repeating it.

## The four identity sentences, written together before anything was authored

**opus5-peatgarth — DTM.** *Every edge on this board is a cut somebody made: each team's Peat Store
stands on a stripped peat bench with a face on three sides and a tramway ramp up the fourth, so
attacking it is choosing which of four ways onto a cut you take — the open moor, the ramp, a flooded
cutting that arrives below it, or the knott that arrives above.*

**opus5-basaltmere — KotH.** *There is exactly one piece of commanding ground on this board, it is an
island in a black mere, and the four ways onto it arrive from four different quadrants — so holding
the hill is holding a place with no back to it.*

**opus5-mirkholt — CTW.** *A wood dark enough that the only things you can see across are the two
clearings the wools stand in, cut by one hollow way that is roofed and blind both ways — so a wool run
is a choice between the lane you cannot see out of and the brow above it, where you are the one thing
moving that anybody can see.*

**opus5-slakemoss — DTC.** *A hall the moss and the water took back: each core stands on a dry plinth
in a ruined chapter house, and the middle is a roofless nave already under water — so the short way to
the enemy's core is the one where you are wading in the open with nothing overhead.*

The four differ by **arrangement** first and by palette second, which is what writing them together
was for. Peatgarth is a flat moss with geometric cuts in it; basaltmere is a bowl with a hole in the
middle of it; mirkholt is a diagonal band of wood with a void quarter either side; slakemoss is built
ground standing in water. Value and hue run peat-black/olive → blue-black/grey → dark-green/brown →
grey-green/murk, and none of the four is grey stone in shadow: the darkness is coal block, black
stained clay, dark oak, podzol and mossy cobble under swamp, deep-ocean and roofed-forest tints.

## What was built

| slug | mode | size | themes | slopes (walked / scramble / barrier) | claims | dead |
|---|---|---|---|---|---|---|
| `opus5-peatgarth` | DTM | 80 × 200 | 94.2 / 2.9 / 2.9 | 11 790 · 74 · 296, 4 faces | 30 placed, 0 declined | 25.0 % |
| `opus5-basaltmere` | KotH | 90 × 190 | 67.3 / 29.7 / 3.0 | 12 628 · 152 · 720, 8 faces | 42 placed, 1 declined | 47.2 % |
| `opus5-mirkholt` | CTW | 100 × 200 | 51.4 / 37.1 / 11.4 | 9 980 · 220 · 300, 8 faces | 30 placed, 3 declined | 0.0 % |
| `opus5-slakemoss` | DTC | 90 × 200 | 40.4 / 31.5 / 28.1 | 14 292 · 182 · 326, 4 faces | 38 placed, 3 declined | 27.2 % |

Relief reads, all four with symmetry error 0 and no silent marks:

| slug | level | largestField | faces / cliffs | landform | seams |
|---|---|---|---|---|---|
| peatgarth | 0.426 | 0.151 | 0 / 0 | rolling | none |
| basaltmere | 0.651 | 0.461 | 4 / 1 | rolling | none |
| mirkholt | 0.459 | 0.166 | 2 / 0 | rolling | none |
| slakemoss | 0.713 | 0.486 | 1 / 1 | plain | none |

Incline distributions, which is where each board's slope bands were cut:

| slug | <10° | 10s | 20s | 30s | 40°+ | bands cut at |
|---|---|---|---|---|---|---|
| peatgarth | 41.3 | 30.0 | 17.3 | 6.7 | 4.7 | 22 / 34 |
| basaltmere | 47.2 | 22.9 | 16.5 | 5.3 | 8.1 | 18 / 32 |
| mirkholt | 46.9 | 28.5 | 11.1 | 8.0 | 5.4 | 16 / 30 |
| slakemoss | 62.8 | 21.6 | 9.0 | 2.5 | 4.0 | 16 / 30 |

No distribution has a spike in it, which is the read that says the board is reporting its own shape
rather than its `step` quantum.

## The fault-catalogue reads, taken per board

Every row of the catalogue was decided by its own read rather than by looking at a picture.
Per-board detail is in `review/<slug>.md`; the summary:

- **Objective hidden.** `column` at every goal. Peatgarth: ground y18, obsidian y23–25, clear sky
  above. Basaltmere: pad at y15, nothing over it to the observer platform. Slakemoss: ground y16,
  casing y23–27 with lava between, clear above, and the chapter wall has three breaches so the core is
  visible from the nave, the west bank and the head of the stair. Mirkholt: both wool blocks inside
  their own rooms with no terrain over them.
- **Spawn faces away.** Yaw against the bearing to the target objective: peatgarth 4°, basaltmere 0°,
  slakemoss 5°, mirkholt 1° and 17° (its two target rooms, both well inside the 90° the fault wants).
- **Spawn faces a wall.** Door transects: every board reads worst step 1, 0 barrier, 0 scramble over
  the first fifteen blocks out of the door.
- **Stairs that end nowhere.** Walked per flight rather than assumed. Basaltmere's east spit:
  `walk from=40,4 to=0,0` — 47 blocks, **0 placed, 0 drops**; the west spit 46 blocks, 1 placed, 0
  drops. Every authored flight on all four boards is `height_mode: "level"` with `anchor_heights`,
  `skirt: 0`, `keepClear: true` and a **material** rather than a theme, and runs at two to five times
  its rise.
- **Flat, one theme, empty.** `relief/read`, `coverage` and `incline` per board, tabled above.
- **A straight frontline.** None of the four has a boundary that is a plan rectangle's own edge:
  peatgarth bends its `fore-13` ring, basaltmere's rim is a relief mark wandering between z 18 and 34,
  mirkholt's front is an `offset` strait 41 blocks wide across a 20-block gap, and slakemoss's nave
  crosses the centre as one sheet with the waterline for a boundary.
- **Stark contrast with no area separation.** `05-themes.txt` border census plus `column` at the
  boundary: every theme border on all four boards is a face, a bench or a waterline.

## What I got wrong

- **I gave a house style `beams: null` and the studio answered 500 rather than a refusal.** `HS9`'s
  own fix text says "drop the beams"; the house style's word for a building with none is
  `beams.block = -1`, and `null` is not a shape it reads. Bisecting a 500 down through the finish cost
  about twenty minutes on basaltmere. All three of my specs now carry a `style(name, beams=False)`
  helper that states `-1`.
- **I drew a water pool over the island it was supposed to surround.** A pool empties every column
  inside its outline down to its own line, so the first basaltmere build had a stack that was in the
  height field at y16 and *not in the world* — the section showed water where the island should be.
  `SketchShape.keepClear` is the answer and says so in its own docstring: "a channel cuts it down to
  the water line. Marking it keeps every prop off its columns exactly." The causeways and spits had it
  and survived; the stack did not and was carved. `column` is what showed it; the store's 200 and the
  export gate's OPEN did not.
- **I stated `kind: "channel"` on a prop.** The prop kinds are stroke, water, tree, boulder, flora,
  house; a channel is `kind: "water"` with `shape: "channel"`. `DR-DOC` said so exactly.
- **I designed mirkholt as a solid rectangle of wood and had to redraw the whole plan.** `G8`'s
  `fill-ratio` measures **a wool board and no other kind** — filled land over the bounding box of the
  land, band [0.201, 0.542] — and my first plan read 0.92. This is why basaltmere (KotH) and
  peatgarth (DTM) were silent on the same term at similar densities. The fix was heftfold's trick, a
  side shifted off the axis so two quarters of the board are void; it made the board better and cost
  an hour.
- **I over-defended mirkholt's wood with keep-out margins; eight trunks a side stand where I wanted
  thirty.** The first pass gave a building an 11-block margin and every boulder 8, which blanketed a
  40-block-wide wood. Measured cause, not guessed: wood 40 wide, lane plus `DR-ROAD`'s three-block
  trunk standoff takes 14, a copied canopy tree is 15–17 across. The board ships with a thinner wood
  than its own sentence claims.
- **I put a relief push over a spawn's own pad on slakemoss** and `RL3` named the three-block step at
  (−15, 79) along 30 cells. Moving the push east of the court cleared it.

## What the system could not do, and what it could after all

- **KotH is supported and a committed spec says it is not.** `specs/archive/opus5-blindtarn/build-spec.py`
  states in its docstring that `MapIntent` carries no control point of any kind and that
  `controlPoint` has no occurrence in the API surface. That is **stale**: `ControlPointIntent` is in
  `openapi.json`, `drive.py` carries the `controlPoints` and `scoreLimit` finish keys, and
  `ControlPointGenerator` emits a `<king><hills><hill …>` element with a `<score><limit>`. Basaltmere's
  `map.xml` carries both. Order of authority held: the API's answer beat the committed spec.
- **Control points are stated already fanned.** They ride on the finish rather than the plan, and a
  compiled intent carries no `symmetry`, so one entry is one hill — a point at the centre of symmetry
  does not need any special handling and a second point would have to be written out.
- **A pool cannot be drawn as a ring.** There is no way to state a lake with a hole in it, so an
  island inside a pool depends entirely on `keepClear` on the shape that makes it. That is
  *unreachable* rather than *missing* — the mechanism exists and the field that makes it work is
  documented on `SketchShape` — but nothing in the water prop's own schema points at it.
- **`04-reach.txt` and `preflight` disagreed on mirkholt** and I could not settle it from here. Reach
  reports the whole opposite half (4 971 cells) as `no-build-zone` unreachable and `bridgeable 0`;
  `preflight` reports one traversable component containing all six spawn and wool points; `coverage`
  reports 0 % dead over 21 journeys. The strait is 21 blocks of void inside a build zone spanning
  z −20..20.

## Questions for the human oracle — recorded as questions, not as facts

1. **Basaltmere's coverage.** 47.2 % of the ground is dead and all of it is the mere's two flank
   lobes, each a block from used ground. The documented calibration says *where* the dead ground is
   decides it, and water in the middle of a board is not ground anybody walks. **Is open water on a
   KotH board dead ground at all, or is the coverage read counting a thing it should not?** If it is
   dead, the fix is a second hill or an off-centre one, and both change what the board is.
2. **Slakemoss's cores stand on dry plinths above a flooded nave, and I moved them there to avoid a
   guess.** A core leaks when its lava reaches `y ≤ B − leak`; lava meeting water turns to stone. **Does
   a core over standing water leak at all in PGM?** I did not find out and did not build on the
   assumption either way — the plinth is four courses of dry ground with the water below and beside
   it, so the question is moot on this board but not on the next one.
3. **Mirkholt's two wool rooms of a side sit two courses apart** (y15 and y17), because the east room
   stands outside the `court-flat` mark's ring and takes the grain instead. `WL9` measures spawn↔wool
   *distance* balance and says nothing about height. **Is a height difference between a team's two wool
   rooms a fairness problem, or is it the kind of difference that makes two rooms worth having?**
4. **Slakemoss's arcade.** Sixteen piers three blocks across and ten apart, standing in and beside
   the water down the nave's banks. It is meant to be cover a raider weaves through. **Is a colonnade
   on the main crossing of a destroy board cover or a nuisance?** The transect across the nave reads
   zero barrier, so it does not block; whether it *plays* is not derivable from here.

## Where things are

```
specs/opus5-peatgarth/   build-spec.py · plan · finish · layout · intent · renders/   (previous agent C)
specs/opus5-basaltmere/  build-spec.py · trees.json · plan · finish · layout · intent · renders/
specs/opus5-mirkholt/    build-spec.py · trees.json · plan · finish · layout · intent · renders/
specs/opus5-slakemoss/   build-spec.py · trees.json · plan · finish · layout · intent · renders/
maps/opus5-peatgarth/    maps/opus5-basaltmere/    maps/opus5-mirkholt/    maps/opus5-slakemoss/
review/opus5-peatgarth.md · opus5-basaltmere.md · opus5-mirkholt.md · opus5-slakemoss.md
```

Each of the three new specs carries its own `trees.json` — two to seven **copied** bodies pulled out of
the `tree_style` library (`tree-showcase-r2-*`, `r3-1`, `r10-*`, `r11-*`) and chosen by measuring the
leaf and log ids in each body rather than by name: `r10-*` are dark-oak leaves on dark-oak logs, nine
courses, the scrub of all three boards; `r2-*` and `r3-1` are spruce, birch and jungle crowns on
dark-oak trunks at 20 to 25 courses, the canopy of mirkholt. Every world was exported into a freshly
emptied directory.
