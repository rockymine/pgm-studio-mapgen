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
moving that anybody can see; and each wool stands sixty blocks down a bare lane of its own, so reaching
one is a commitment rather than a step sideways out of the door.*

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
| `opus5-peatgarth` | DTM | 80 × 200 | 91.4 / 5.7 / 2.9 | 11 790 · 74 · 296, 4 faces | 30 placed, **0 declined** | 25.3 % |
| `opus5-basaltmere` | KotH | 90 × 190 | 64.2 / 27.0 / 5.8 / 3.0 | 12 781 · 234 · 720, 8 faces | 38 placed, 1 declined | 49.3 %* |
| `opus5-mirkholt` | CTW | 110 × 230 | 47.1 / 40.4 / 12.4 | 11 160 · 42 · 48, 4 faces | 34 placed, 1 declined | 0.0 % |
| `opus5-slakemoss` | DTC | 90 × 200 | 40.4 / 31.5 / 28.1 | 14 292 · 182 · 326, 4 faces | 40 placed, 1 declined | 27.8 % |

\* not a coverage figure that means anything: `GET /coverage` cannot see a control point, so on a KotH
board the walk has two spawns and no objective to travel to. See *Author feedback* below.

Relief reads, all four with symmetry error 0 and no silent marks:

| slug | level | largestField | faces / cliffs | landform | seams |
|---|---|---|---|---|---|
| peatgarth | 0.431 | 0.167 | 0 / 0 | rolling | none |
| basaltmere | 0.649 | 0.477 | 4 / 1 | rolling | none |
| mirkholt | 0.458 | 0.326 | 0 / 0 | rolling | none |
| slakemoss | 0.713 | 0.486 | 1 / 1 | plain | none |

Incline distributions, which is where each board's slope bands were cut:

| slug | <10° | 10s | 20s | 30s | 40°+ | bands cut at |
|---|---|---|---|---|---|---|
| peatgarth | 41.3 | 30.0 | 17.3 | 6.7 | 4.7 | 22 / 34 |
| basaltmere | 47.2 | 22.9 | 16.5 | 5.3 | 8.1 | 18 / 32 |
| mirkholt | 45.4 | 30.0 | 17.1 | 7.1 | 0.4 | 16 / 30 |
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
  slakemoss 5°, mirkholt 13° and 11° (its two target rooms, both well inside the 90° the fault wants).
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

1. **Is open water dead ground?** The coverage figure itself turned out not to be evidence — the walk
   cannot see a capture point — but the question under it stands on any board with a lake in it: more
   than half of what that read calls dead on basaltmere is the mere, and a player crosses water rather
   than standing on it. **Does water in the middle of a board count as ground nobody goes to, or as a
   route?** If it counts as dead, every board in this set with a pool in it is being marked down for
   having one.
2. **Slakemoss's cores stand on dry plinths above a flooded nave, and I moved them there to avoid a
   guess.** A core leaks when its lava reaches `y ≤ B − leak`; lava meeting water turns to stone. **Does
   a core over standing water leak at all in PGM?** I did not find out and did not build on the
   assumption either way — the plinth is four courses of dry ground with the water below and beside
   it, so the question is moot on this board but not on the next one.

5. **The goal material follows the goal's size, and that takes it out of the board's palette.** A
   `cube-3` may not be obsidian (`DC3`), so peatgarth's Peat Store is now 26 blocks of ender stone —
   a pale sandy block, the one thing on a black-and-olive board that is not dark, wet or green. On the
   studio's own reading that is correct (`OB26`: a goal reads as a goal). **Is a pale goal on a dark
   board right, or should the board make room for it — a paler works stage under it, say?**
3. **Mirkholt's two wool rooms of a side sit two courses apart** (y15 and y17), because the east room
   stands outside the `court-flat` mark's ring and takes the grain instead. `WL9` measures spawn↔wool
   *distance* balance and says nothing about height. **Is a height difference between a team's two wool
   rooms a fairness problem, or is it the kind of difference that makes two rooms worth having?**
4. **Slakemoss's arcade.** Sixteen piers three blocks across and ten apart, standing in and beside
   the water down the nave's banks. It is meant to be cover a raider weaves through. **Is a colonnade
   on the main crossing of a destroy board cover or a nuisance?** The transect across the nave reads
   zero barrier, so it does not block; whether it *plays* is not derivable from here.

## Author feedback, applied and re-driven

All six items were applied and all four boards were re-driven. Mirkholt needed no change.

**1 · peatgarth's bench now reads as built.** The `bench` shape carried no theme at all and inherited
`mapTheme: "moss"`, so a raised disk of moor sat under an andesite ramp that said "built". It now
carries the **`works`** theme — the same stone the ramp is cut from — so the surface, the face and the
ramp agree. `column (−24, 48)` reads andesite over stone, `column (−6, 60)` polished andesite over
stone over cobble. Only the scald on top of it is soil, and that is the cut peat drying on the stage.
Stone on the ground went 2.9 % → **5.7 %**, and it is now where a player fights rather than behind the
spawn.

**2 · the slab and the second house style are gone.** `works-pad` is deleted; the ground under it was
already flat under `back-flat`, and `column (−22, 86)` now reads podzol over dirt. The store is rebuilt
in the **spawn's own shell** (`sb-spawn`, clear 5 then 4 under a gable) at x −30..−20, z 70..82, so the
two buildings at the head of the tramway are one family. The first attempt at x −30..−20, z 80..92 was
declined `DR-KEEP` at (−26, 86) for standing in the spawn door's approach; moved south, the board
declines **nothing at all**.

**3 · the goal is a `cube-3` in ender stone.** 3 × 3 × 3 with the studio's own 1 × 1 × 1 bedrock centre
(`ObjectiveStamper`), so **26 breakable blocks** against a `pillar-3`'s three, at 40–42 blocks from its
own door. The material follows the size rather than the palette: `DC3` reads obsidian as worth at most
three blocks and names ender stone, gold or emerald for a cube — and a cube declared obsidian is built
in ender stone anyway, with a complaint attached, so declaring it is the honest form. `column` at the
cube's corners reads solid end stone y23–25; at its middle, end stone, bedrock, end stone.

**Slakemoss's cores were checked and left alone.** `lava: 3` leaves the corpus's 5 × 5 × 5 casing round
a 3 × 3 × 3 interior — **98 obsidian blocks** — confirmed by `column` at (−16, 54) and (−12, 58) reading
solid obsidian y23–27. At 41 blocks of walk from its own spawn that is a raid, not a grind.

**4 · nothing is growing out of masonry any more.**

- *slakemoss*, ten trees, each seat read back: **eight on soil** — grass (38, 40); coarse dirt
  (−42, 40), (−10, 36), (34, 48), (40, 56); gravel (−42, 54), (10, 36); podzol (24, 44) — and **two kept
  deliberately in the ruin** on mossy stone bricks at (2, 62) and (−26, 62), which is the note worth
  having. One exception is a sapling in a broken floor; six is a mistake.
- *basaltmere* needed soil before it could seat anything: the bowl's flat band now carries **coarse
  dirt and podzol** among its grit, and two **greaves** — peat pans stated as `exclude` shapes so they
  are flat to their own lip — carry a fourth theme (`peat`, 5.8 % of the ground) and hold the scrub.
  The count came down ten → **eight**: the two that still seated on coal ore were removed rather than
  moved, because the pans were full and a basalt strand with nothing on it is the honest answer. Every
  remaining trunk read back: coarse dirt (32, 41), (26, 62); podzol (−8, 56); grass (34, 50), (34, 68),
  (26, 73); gravel (−38, 54), (40, 38).

**6 · the coverage correction is taken, and it changes what one of my questions was about.**
`controlPoints` reach the intent and not the plan the coverage walk reads, so basaltmere's dead figure
is the read declining to answer rather than the empty-board fault — its `journeys: 3` against
slakemoss's 10 and mirkholt's 21 is the tell, and it is now footnoted in the table and rewritten in
`review/opus5-basaltmere.md`. The oracle question below is kept, because the part of it that is about
water is still open and is not a question about the tool.

## Second round of author feedback: mirkholt's wool rooms

**The finding was right and no read would have caught it.** All three back pieces shared edges —
`west-cage` | `lodge` | `east-cage` — so each room's footprint stood **9 blocks** from the spawn's with
no lane anywhere between them. `WL2` states *"on a different lane than the spawn; wool↔spawn ≥ 20"* and
**only the distance clause is implemented**; it passes comfortably, because a room wide enough puts its
wool block far away while the rooms still touch. `WL6` — each wool on a distinct lane — has **no term at
all**. Score 0, no refusal, wrong board.

**Rebuilt to the composer's own shape**, which is why it reports every wool unit as `boxes: 2` (room
plus lane) against `boxes: 1` for a spawn or a hub, and which `opus5-coinfall` shows as `camp` → `run`
→ `plinth`:

- **west spur** — `lodge` (x −5..20) → `west-lane` (x −30..−5, **25 blocks**) → `west-cage` (x −50..−30),
  all in the z 80..95 band.
- **east spur** — off the garth's east side, running south into the quarter the shift left empty:
  `east-lane` (x 20..35, z 55..80, **25 blocks**) → `east-cage` (x 20..35, z 35..55).

Read back: wools at (−44, 15, 87) and (27, 15, 45), spawn at (7, 90), and the walk to each is **53
blocks with 0 drops** — balanced to the block, which is `WL9` satisfied by construction. 82 blocks
apart, inside `WL7`'s 46–143.

**Both lanes are bare.** `column` at (−12, 87), (−20, 87), (−28, 87), (27, 60), (27, 68) and (27, 76)
reads grass block with nothing standing. The tree lattice excludes the two lane rectangles outright,
the understorey flora stops at z 80, and the four remaining boulders are in the wood and on the brow.

**`fill-ratio` was re-read rather than assumed,** as instructed — two spurs are land. It came back
**0.55**, outside `G8`'s band, and the plan was trimmed (toe 6 cells → 5, brow 10 → 8, garth 11 → 10)
until the evaluate scored **0** again.

**What else moved, and why it is better.** The stair off the brow is gone: a push whose skirt and crown
climb at the same rate has no face, and a flight is for a face — its keep-out had also blanketed a
20-block swathe of a 40-block wood. With it gone, the hollow way moved to hug the wood's east edge and
its reach came down 12 → 9, so the plantable mass is one strip rather than two slivers. The wood went
from **8 trunks a side to 17**, barrier from **300 to 90** in 4 faces instead of 8, `largestField` from
0.166 to **0.343**, and the board now declines **one** prop out of 46.

## Third round: mirkholt's fronts made to face, and the spawn pulled back

**The two fronts were staggered by 35 blocks** — red's land met the strait over x −50..15 and blue's
over x −15..50, sharing 30 blocks of a 65-block width, so most of each team's front looked across at
void. Under `rot_180` a front spanning `[a, b]` is faced by one spanning `[−b, −a]`; they are equal
only when `a = −b`, so the edge has to be symmetric about x = 0 and there is no way round it.

**The fix was to make the front band alone symmetric and leave the rest of the unit offset.** A new
`toe` piece runs x −35..35 at z 10..30 as one wet flat across the whole front; the wood, the brow, the
garth, the lanes, the cages and the spawn stay where the diagonal put them. `GET /rules?rule=CT12` now
reports both teams' frontline runs as **`x1: −35 … x2: 35`, 70 blocks**, facing over 69 of them.

**`fill-ratio` was re-read rather than assumed, as instructed, and it holds: the evaluate scores 0.**
`AUTHORING-BRIEF.md`'s warning is about a *whole unit* drawn symmetric, and only the front is symmetric
here. It was not free — land added at the front came off the back, and the wood went from 45 blocks of
depth to 25. The first cut of the new plan read 0.55 and outside the band; trimming the toe, brow and
garth brought it back inside, and the longer board (z ±110 rather than ±100) then left headroom the
wood took 5 blocks of width from.

**The spawn is pulled back 15 blocks**, to z 95..110, standing on its own piece behind a new `apron` at
z 80..95. It shares an edge with the apron and with nothing else — two pieces from either lane root,
no edge with a wool room, and joined along an edge rather than at a corner, which `PC-C` reads as no
connection at all. The walks are now **63 and 68 blocks, 0 placed, 0 drops**.

**What it cost, stated as a number.** The wood stands **11 trunks a side** where it stood 17: the
symmetric front takes 20 blocks of depth across the full width, and the width bought back with the
headroom lies inside the hollow way's own exclusion. The fronts facing is worth more than the trees,
but it is a real trade. Everything else improved or held — 36 props placed and **nothing declined**,
barrier still 90 in 4 faces, `level` up to 0.526, `largestField` 0.357, no seams, no silent marks,
symmetry error 0, both lanes still bare on six `column` reads.

## Fourth round: the strait, the east spur, and a soft band shipped outside

**The build zone was wrong in both directions and is now exact.** It ran x −50..50, z −20..20 — ten
blocks of it over each team's own land, and a hundred blocks wide against a seventy-block front.
`intent.build.areas` now reads `minX −35, minZ −15, maxX 35, maxZ 15`: the width of the fronts and the
gap between them, nothing over land, nothing over void. The fronts moved to z ±15, so `CT12` reads the
strait as **30 blocks**, inside the 25–30 the author wanted, and both frontline runs come back
`x1 −35 … x2 35`, 70 blocks, **`profile: "straight"`**.

**The east spur was backwards and is rotated.** Its room had sat five blocks behind the front band with
its lane *behind* it, so a raider reached it straight off the front and the lane did nothing. The whole
back row now reads `west-cage | west-lane | apron | east-lane | east-cage`, all at z 85..100, with the
spawn behind the apron at z 100..115. Wools at (−50, 92) and (45, 92); walks from the spawn **58 and 59
blocks, 0 placed, 0 drops** — one block of `WL9` spread. Both lanes still bare on four `column` reads.

**The wood is back to 45 blocks deep, and the board grew rather than the wood shrinking.** The trade I
made last round was wrong and the ruling is taken: a soft term off a corpus envelope does not get to
delete the thing a board is named for. The remedies were worked in the order given — **bigger** first
(110 × 230), which took `fill-ratio` off the board entirely and kept it off at every later step; then
**move**, which cleared `max-chain-length` (115 → 105, band max 110) by narrowing the cages from 20 to
15 and paring the brow to one cell and the garth to two.

**Two soft terms remain outside their bands, and the numbers are here rather than hidden.**

| term | reads | band | kind |
|---|---|---|---|
| `WL10` `wool-front-remoteness` | **128** | [22, 118] | soft, envelope |
| `WL10` `wool-front-ratio` | **1.488** | [1, 1.474] | soft, envelope |

Both are distances from the frontline to the rooms, and the only lever left that would move them is
shortening the wood — which is what this round forbade. Shifting the back row a cell east was measured
rather than reasoned and read **worse** on both (1.583 and 133), so it sits a cell west of centre.
128 against 118 is a long raid rather than a stalemate, and `wool-front-remoteness` is described as
catching exactly that stalemate, so it is the author's call and not mine: the board ships at 128 with
the wood intact.

The board otherwise improved: barrier **48** in 4 faces (from 90), scrambles 42, **0.0 % dead**, no
seams, no silent marks, symmetry error 0, one prop declined of 34.

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
