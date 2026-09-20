# Gallowsholt — a composed ring hub, re-hung

> Adapted from `GET /api/compose?players=20&symmetry=rot_180`, **seed 0**, composer
> `markers-in-blocks-1`, cell 5. Composed score 0.302; structure **hub `ring` · frontline `twin` ·
> wools `i`, `i`**. This is the board §2 of `COMPOSER-ADAPTATION-BRIEF.md` measures at 1.47×.

**In one sentence:** a limestone moor whose only made ground is a flagged causey island in the middle
of the crossing and the two walled garths the wools sit in, with a broken ring of fell between them
that both teams have to come over.

90 × 200 blocks, `rot_180` about the origin, base surface 11, observer y 40. Two groups: `team` (the
fanned landmass, 4 246 solved cells) and `neutral` (the causey, 390).

## What the composer gave and what it became

| The composed board | This board |
|---|---|
| wool-a 138 blocks from the enemy's door, wool-b 94 — **1.47×** straight-line, 144/116 by walk | 174 and 178 — **1.02×** straight-line, 183/200 — **1.09×** by walk |
| spawn hung off the hub's **west flank**, both wools east of it | spawn moved to the hub's **back**, one wool on each back shoulder |
| frontline tips 10 blocks wide (`FR9`: *a funnel rather than somewhere to cross*) | 15 blocks each, noses pushed out and broken |
| mid: 20 blocks of build zone flush against both fronts, nothing in it | the team unit shifted +2 cells of z, the gap opened to 40, and a **causey island** seated in it with a 15-block crossing on each side |
| ring hub with a 10 × 10 hole | the hole redrawn as a rounded 12 × 12 **shakehole** and a bite cut out of the hub's west flank, so the west way round it narrows from 20 blocks to 12 |
| every piece an axis-aligned rectangle | one 24-vertex compiled ring taken to 30 by hand, then bent |

## The mid the composer does not place

`causey` is a plan piece stated once with `mirrors: False` — its rect is centred on the origin, so it
is its own `rot_180` image — at `surface` 15 against the board's 11. It compiles as its own shape in
its own group, which is what lets it carry its own theme and its own relief. Four vertex inserts turn
the rectangle into a lens 36 × 14, and two `polyline` walls run along its two long sides, authored as
an explicit pair about the origin because **nothing on a non-mirroring group is mirrored for you**.

Either side of it: `crossing-s` and `crossing-n`, 40 × 15 blocks each. `POST /plan/inspect` measures
the front-to-causey gap at **15 blocks**; that is the hop at the fronts' two noses. Into the **gate** —
the bay cut into the frontline's notch — it is 17 blocks to the bay's mouth and **27** to its back
wall. So a team can cross short and land on ground somebody is already standing on, or cross long and
land inside a bay with land on three sides of it.

## Where the made ground meets the grown ground

One face, and it is on the line everybody walks.

`apron` is a ten-vertex polygon over the whole frontline at `base_height` 11 with
`relief_scope: "exclude"` — a quarried floor, flat to its own edge and out of the relief solve. Behind
it the `fell` push lifts the hub. Measured down `x = 0`:

```
z 34..44   y10 y10 y11 … y11        the apron
z 45       y15                      BARRIER +4      <- the quarry's back wall
z 46..58   y16 y16 y17 … y22        the fell
```

Two `rake` flights cut through that wall at `x −20..−10` and `x 10..20`: fourteen blocks of run for six
of rise, `height_mode: "level"`, `skirt: 0`, `relief_scope: "exclude"`, a `material` rather than a
theme. The back of the fell falls to the garths at about a block a block and needs no stair —
`transect (−5, 55)..(−5, 90)` reads `21 22 22 21 20 20 19 18 18 17 17 16 16 15 15 14 13 12 11 10 …`,
worst step 1, walked end to end.

The three rooms' aprons — `garth-a`, `garth-b`, `stell` — are `relief_scope: "hold"` pads at the base
height, which is also what buries each room's **bedrock plinth**: a stamped room fills its piece and
fills downward in bedrock, so the composed rooms, whose pieces are exactly their own footprint, stand
on a 25-course cliff on three sides. Ten vertex moves put ground round all three.

## The relief: two pushes' worth of nothing, and one push

`relief.team` states **no marks at all**. A mark is a constraint honoured exactly and a push is added to
the surface the marks solved, so a board that states both gets the mark's height *with* the push's on
top of it — which is what put this board's first build at `high 32` against a base of 11 and a
twelve-block wall in front of the spawn door. The flat this board needs is stated as made ground, where
it can be walked on.

`fell`: a seven-point ring over the hub, `amount` 6, `amounts` 6/7/6/5/6/7/6, `crown` 6, `falloff` 9,
`roughness` 2. The read answers `skirt 0.67 · crown 0.55` — the two gradients within 1.2× of each other,
which is what keeps a range from being a wall with a hill on it. `seams []`, `silentMarks []`,
`level 0.596`, `largestField 0.139`, `faces 0`, `cliffs 0`, `symmetryError 0`.

## What the ground is painted with

Three themes and three tone families, named before a block was chosen: the **ground** is pale
limestone and bleached turf, what is **built** is dark spruce over stone brick, and the **accent** is
pink granite — the erratics, and nowhere else.

`moor`'s surface is a `layered` material on the **`slope`** axis, cut at **32° and 44°**: turf, then
the worn shoulder the sheep keep bare, then the rock. The cuts come off `GET …/incline`, which reads
43.2% of this board under 10°, 19.5% at 10–19°, 14% at 20–29°, 17.2% at 30–39° and 6.1% at 40° or
steeper — **and off the push's own gradients**, which the relief read answers as `skirt 0.67` and
`crown 0.55`, or 34° and 29°. Cutting at 24, which the incline distribution alone suggests, put the
whole fell on the worn-shoulder band and the board came out grey in the isometric; at 32 the fell is
turf, its brow is worn and only the cut faces are rock. **The distribution tells you where the ground
is; the push's gradients tell you which of it is the hillside.** Read back off the built world:

```
column (0, 66)   ground 27°  y17 Grass Block · y16 Dirt · y15 Dirt          the fell's crown — turf
column (-8, 52)  ground 30°  y17 Grass Block · y16 Dirt · y15 Dirt         its shoulder — turf
column (20, 60)  ground 35°  y18 Coarse Dirt · y17 Gravel · y16 Dirt       its skirt — worn
```

`themes/census`: `moor` 5 370 cells (60.5%), `works` 3 216 (36.2%), `causey` 288 (3.2%); 887 cells of
drawn border between the moor and the workings, 122 between the causey and the moor. Nothing
registered painted nothing.

## The numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, valid, one `SP2` complaint (the lint's own approximation — the spawn *is* at the back of its lane) |
| `GET …/preflight` | **export gate OPEN**, per team |
| `GET …/coverage` | reached 7 469, dead **0**, **0.0% dead** |
| `03-slopes.txt` | 7 934 walked, 134 scrambled, 806 barrier; 12 faces, largest 123 |
| `06-claims.txt` | placed **26**, declined **0** |
| relief `team` | `level 0.596 · largestField 0.139 · faces 0 · seams 0 · symErr 0` |
| flow, attacker | 183 blocks to one wool, 200 to the other — **1.09×** (composed: 144/116, **1.24×**) |
| flow, defender | 49 and 50 — 1.02× |

## What went wrong

**The first build put a twelve-block wall in front of the spawn door.** `relief.team` carried an
`area` mark at 18 and a `point` at 21 *and* a push of 6 with a crown of 5, and the push is applied to
the solved surface: the ground reached `high 32` over pads excluded at 15. The fix was to delete every
mark and let the push be the only thing that decides a height.

**Four props were declined twice before I stopped guessing.** `POST …/sketch/seats?kind=&width=&depth=`
answers the question forwards — where a footprint of that kind *may* stand, over the whole board — and
the answer for a 12 × 8 house on this board is **zero cells**, for 9 × 7 zero, and for 7 × 5 seventy. The
one building on the board stands at `(16, 48)` because that is one of the seventy.

**`type: "path"` is not a shape kind** — the word is `polyline`, and a polyline states its bounds rather
than the points a height is stated at, so `anchor_heights` on one is `SK22` and is nowhere in the world.

**The erratics were the ground.** `DR-TONE` on three boulders cut from cobble and grey stone standing on
cobble and grey stone. They are granite and diorite now, which is also what an erratic is: rock a
glacier carried from somewhere else.

## Open gameplay questions

- **The causey stands four blocks over the frontline.** A player bridging out of his own front arrives
  at y10 and has to place a block to get onto y14. That makes the island a real prize and it makes the
  first team there hard to shift. I judged that right for an island nobody owns; the author's ruling is
  what settles it.
- **The gate is a 25-block bridge and the two shoulders are 15.** Three ways across at two prices, and
  the long one lands in a bay with land on three sides of it. Whether that reads as a trap or as a
  flank is a question about how it plays.

## Coordinates

| Thing | Where |
|---|---|
| spawn (red) | `(−5, 11, 92)`, door `−z` |
| wools (red) | `red` at `(30, 11, 80)`, `orange` at `(−40, 11, 80)` |
| the causey | `x −18..18, z −7..7`, top y14 |
| the quarry's back wall | `z 44 → 45` across `x −28..28`, +4 |
| the rakes | `x −20..−10` and `x 10..20`, `z 34..48`, 11 → 17 |
| the shakehole | `x 4..16, z 54..66` |
| the neck | the hub's west flank pinched to `x −8` at `z 57` |
