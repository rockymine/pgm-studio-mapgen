# Opus 5 — four composed boards, adapted at the ground plan

Four CTW boards, each pulled off `GET /api/compose` and then reshaped. The emphasis this run was given
is **the ground plan, deformed**: what the composer's rectangles become once they stop being
rectangles — widening what is too tight to fight in, cutting away what is dead, re-hanging a wool that
is in the wrong place, and putting into the mid the things the composer never puts there.

## What I set out to build

Written before the first shape, all four together, so the second board is not the first board's
arrangement in different blocks.

| Board | The sentence |
|---|---|
| **Gallowsholt** | A limestone moor whose only made ground is a flagged causey island in the middle of the crossing and the two walled garths the wools sit in, with a broken ring of fell between them that both teams have to come over. |
| **Kettleshulme** | A coal-measure clough of dark grit and podzol where each team's near wool is cut off the hub entirely and reached only over a bridge that team owns, and a mill launder is carried over the hub's east slot on a deck a raider can run. |
| **Longstrand** | A sand spit — flat, pale and open nearly everywhere — with one ring of dune on it that you have to walk round, two tide-worn stones in the middle at a ten-block grain, and a water lane down the west flank that opens forty-five minutes in. |
| **Medlock Drift** | A drift mine in red shale where the only two flat places are the pit floor at the front and the mine yard at the back, everything between is a spoil bank benched two blocks at a time, and the spawn has a second exit that goes nowhere an attacker can follow. |

Tone families, checked **across** the set and not within it, because five boards can each be
internally coherent and still be five greys:

| Board | ground | built | accent | biome |
|---|---|---|---|---|
| Gallowsholt | pale limestone, bleached turf | dark spruce over stone brick | pink granite (the erratics) | Extreme hills `#8ab689` |
| Kettleshulme | dark millstone grit, podzol, coal | red brick | pale oak (the launder) | Swampland `#6a7039` |
| Longstrand | pale warm sand, sandstone, marram | dark oak over stone brick | prismarine (the stones) | Savanna `#bfb755` |
| Medlock Drift | red shale, hardened clay, red sand | pale birch over cobblestone | grey andesite (the portal) | Mesa `#90814d` |

---

## The one finding that is about the composer and not about a board

**§2's lopsided wool is caused by where the composer hangs the spawn, and fixing it moves the spawn.**

The brief measures the fault as *the two wools are not equidistant from the spawn that has to attack
them*. The geometry that follows from wanting to fix it is forced, and I found it by failing at it
three times:

- Equal distance from the **enemy** spawn, which is at the far end of the board, means the two wools
  must sit at **comparable depth**. Any depth difference of *d* shows up almost undiminished in the
  enemy walk, because the enemy leg is nearly parallel to the board's long axis.
- Equal distance from the **own** spawn, *given* equal depth, means the two wools must be symmetric in
  **x** about the spawn's own x.
- So a spawn on a flank — which is where the composer puts it on every board I pulled, `rot_180` and
  `mirror_z` alike — cannot carry two balanced wools at all. On a board 90–110 blocks wide with the
  spawn at `x ≈ ±45`, any wool on the far flank is ~85 blocks from its own door and any wool on the
  near flank is ~40.

All four boards therefore move the spawn off the flank, and each moves it differently so that the four
do not come out as one arrangement:

| Board | where the spawn went | where the wools went |
|---|---|---|
| Gallowsholt | hub's back, centre | the two back shoulders, behind the spawn's own line |
| Kettleshulme | hub's back, offset east | the two flanks at mid-depth, one of them on an island |
| Longstrand | the far back, down a 40-block lonning | the two flanks at mid-depth, one inside a dune ring and one on open strand |
| Medlock Drift | hub's back, centre | the two flanks at mid-depth, one inside a clamp |

And the results, straight-line to the enemy's door and by the walk `GET …/plan/flow` measures:

| Board | composed, straight | mine, straight | composed, by walk | mine, by walk |
|---|---|---|---|---|
| Gallowsholt (`rot_180` s0) | 138 / 94 — **1.47×** | 174 / 178 — **1.02×** | 144 / 116 — **1.24×** | 183 / 200 — **1.09×** |
| Kettleshulme (`rot_180` s23) | 123 / 83 — **1.48×** | 138 / 144 — **1.04×** | 139 / 120 — **1.16×** | 158 / 167 — **1.06×** |
| Longstrand (`mirror_z` s12) | 157 / 108 — **1.44×** | 200 / 192 — **1.05×** | 200 / 148 — **1.35×** | 234 / 206 — **1.14×** |
| Medlock Drift (`mirror_z` s34) | 134 / 104 — **1.28×** | 167 / 164 — **1.02×** | 150 / 151 — **1.01×** | 182 / 185 — **1.02×** |

Two things worth saying about that table. **Medlock's composed board was already balanced by walk** —
1.01× — while its straight line read 1.28×, so the straight-line measure in the brief's own §2 table
and the walk the flow read takes are not the same fault and do not always co-occur. And **Longstrand's
walk ratio is the worst of my four at 1.14×**, because a wool inside a donut costs more to walk to
than one on open ground at the same distance; the ring is the point of that board and I took the trade.

---

## The method I settled on

After the first board, the loop that worked was:

1. **Browse, then pin.** `GET /api/compose?players=20&symmetry=…&seedStart=&count=20` over ten windows
   of twenty seeds gives the hub/frontline/wool vocabulary and the scores in one sweep;
   `POST /api/compose/pin` (which needs `composerVersion` and `schema`, not just the seed) returns the
   `PlanModel`. `GET /api/plans/{id}/ascii` is the board.
2. **Measure the composed board before touching it.** Store it under the slug you are going to use —
   `POST /plan/compile` then `POST /map/from-documents` — and read `GET …/plan/flow`. That is the only
   way to get the "before" number, and the map row is replaced by the real drive later.
3. **Edit the plan, and iterate at the plan tier only.** `POST /plan/evaluate` (score, violations),
   `POST /plan/inspect` (the hop table), `GET …/plan/flow` (the walks and, crucially, *what no journey
   reaches*). This costs seconds; a drive costs four minutes. Every board's arrangement was settled
   here, and Longstrand took six iterations.
4. **`tools/board.py` before every post.** It is the only view that puts two rectangles on the same
   rows. It caught the enemy team having no bridge on Kettleshulme — ten cells of enclosed void where
   a zone should have been.
5. **Compile, read the shape ids, write the finish against them.** `POST /plan/compile` and print the
   `groups`/`shapes`. A composed board at one surface compiles to **one** merged polygon plus one
   subtract per hole, which turns out to be exactly what this emphasis wants: one long ring to reshape
   and a negative space to redraw.
6. **Simulate the `editShapes` replay locally before driving.** Insert/move/remove, then a shoelace
   area and an all-pairs segment-intersection check. A folded ring refuses nothing — the store answers
   200, the export answers 200, pre-flight answers OPEN — so this is the only thing that catches it
   before a build. ~120 ops across four boards, zero folds.
7. **`tools/loop.py` for the relief**, which is twenty seconds and answers `RL2`/`RL5`/`RL6` and the
   step histogram without building a world.
8. **Drive, then read `03-slopes.txt`, `06-claims.txt` and the transects before opening a picture.**
9. **`POST …/sketch/seats` with the driven layout for every prop**, and only then re-drive.

### What I would tell the next agent

- **The plan tier is cheap and the world is not.** Nine of every ten decisions on these boards were
  made by `evaluate` + `inspect` + `flow` in under a second each. Do not build to find out.
- **`plan/flow`'s *WHAT NO JOURNEY REACHES* is a design instrument, not a report.** It names the dead
  ground by piece and by block count. Longstrand went **25% → 5%** dead on one change it suggested:
  the donut's wool room moved from the ring's near corner to its far one, so both arms of the ring
  are on a route. Nothing else on the board moved.
- **Reach for `POST …/sketch/seats` before placing anything.** It answers forwards. On Gallowsholt a
  12 × 8 house seats in **zero** cells of the whole board, 9 × 7 in zero, and 7 × 5 in seventy — which
  is a fact about a composed board (it is corridors) that no amount of looking at a render tells you.
  It cannot answer `DR-WAY`, `DR-CROSS` or `DR-SLOPE`, which read the built world. And **it answers
  for the exact cell**: the dressing pass seats a prop a block or three off the position stated and
  judges it at every image of its orbit, so a cell the mask marks legal at the edge of a run can be
  nudged out of one — measured on Kettleshulme, where `(−45, 40)` and its image `(45, −40)` both read
  1 in the mask and the tree was declined at `(43, −43)`, which reads 0. Pick cells several blocks
  inside a run, in both axes.
- **Author the relief as pushes and nothing else.** A mark is a constraint honoured exactly and a push
  is added to the surface the marks solved, so a board that states both gets the mark's height *with*
  the push's on top. Every flat this run needs is stated as made ground with `relief_scope: "exclude"`,
  where it can be walked on and painted.
- **Read `pushes[].skirt` and `pushes[].crown` back.** The half-width a crown is divided by is the
  ring's own medial distance and no arithmetic in a spec predicts it: I computed 0.62 for a crown that
  read 0.30.
- **Cut the slope bands against the push's gradients, not only against the incline histogram.** The
  histogram says how much ground stands in each ten degrees; it does not say *which* ground. A push
  that reads `skirt 0.67 · crown 0.55` is a hillside at 34° and 29°, so a first cut at 24 puts the
  entire hill on the worn-shoulder band and the board comes out grey with green only at its edges —
  measured on Gallowsholt, whose first cut was 24 and whose second is 32. **`arctan(skirt)` and
  `arctan(crown)` are where a landform actually sits on that axis**, and the cut goes above them or
  below them on purpose.

---

## What I could not say

Three verdicts, kept apart: **missing** (no mechanism), **unreachable** (exists, the surface hid it),
**mistaken** (exists, documented, I did not find it).

### Missing

- **`stairs` on a relief.** `GENERATION-NOTES.md` describes `step` *with* `stairs: true` as the quarry
  instrument — *"`stairs: true` then cuts a way up out of every place the terracing stranded"*. It is
  not on the wire on this branch: `SketchReliefJson` carries `base`, `reach`, `step`, `landform`,
  `grain`, `marks` and `pushes`, and nothing else, checked in `GET /api/openapi/v1.json`. `step` alone
  works — Medlock's tip is benched at 2 and reads 1 854 scrambles against 126 barriers — but a board
  that wants stated ways up the benching has to author them as flights. **Verdict: missing from the
  wire, and the note describing it is stale.**
- **A `POST /plan/flow` to match `POST /plan/ascii`.** The endpoint's own summary says the derivation
  reads the plan alone and costs no build, and `ascii`, `evaluate`, `inspect`, `compile` and `columns`
  all have a body-taking twin. `flow` and `coverage` do not: both require a stored map. Measuring a
  *composed* board's flow — which is the whole of §2's "run it before and after" — therefore means
  storing somebody's plan under a slug first. I did that four times; it works, and it is not what the
  surface suggests.

### Unreachable

- **`POST …/sketch/seats` is not in the loop.** `drive.py` writes `06-claims.txt` (the backwards
  raster: what claims each cell) and `loop.py --candidates` tries a named prop at stated positions,
  but nothing runs the forwards mask, and it takes the **layout** in the body — which means the driven
  `*.layout.json`, which only exists after a build. It is the most useful read in this run and I wrote
  a four-line script to reach it.
- **A `made` layer's theme is invisible to `themes/census`.** Kettleshulme's launder deck paints oak
  planks and oak-log kerbs — `column (6, 52)` answers `y17 Oak Log · y16 Oak Planks` — and
  `05-themes.txt` lists two themes, not three. The census projects one height per column off the
  ground, which `GENERATION-NOTES` already says of every 2-D read. The consequence for an author is
  specific: **on a stacked board, "no theme registered that painted nothing" cannot be checked with
  the census.** `column` is the check.
- **The pairwise hop table.** `POST /plan/inspect`'s `islandGaps` reports the pairs it considers
  straits; `G5`'s hard failure reports the pair and the distance in `evaluate`'s lint. Both are there.
  What is not there is the table *before* you have failed — so the fact that three stepping stones in
  a row cannot satisfy `G5` (see below) is something you find by evaluating, not by reading.

### Mistaken

- **`type: "polyline"`, not `"path"`.** Four shapes on the first Gallowsholt build drew no ground at
  all and said so as `SK3`, listing the five kinds. And a polyline states its bounds rather than the
  points a height is stated at, so `anchor_heights` on one is `SK22` and lands nowhere.
- **`BoulderStyle` is `form` / `size` / `rock` / `mossy`.** I wrote `reach` / `materials` / `moss` from
  memory and got a 400 naming `BoulderForm`. `GET /api/openapi/v1.json` has the four fields.
- **A lifted tree body is not a `PropStyle`.** `tools/trees.py bodies` writes `{foot, body}`;
  `dressing.styles` wants `{"kind": "tree", "form": "copied", "body": …}`. Without the discriminator
  the answer is **500 / `RQ2`**, which reads as the studio's fault and is the document's.
  `specs/opus5-dustwath/trees.json` and `specs/opus5-potsherd/trees.json` are in the style shape;
  `specs/archive/opus5-marram-hythe/trees.json` is in the reader's.

---

## What I got wrong

**A relief mark and a push add.** Gallowsholt's first build put a **twelve-block bedrock wall in front
of the spawn door** and reached `high 32` on a base of 11. The relief stated an `area` mark at 18 and a
`point` at 21 *and* a push of 6 with a crown of 5 — and a push is applied to the solved surface. This
is written down in `GENERATION-NOTES.md` and I read it and authored against it anyway, because the
mark and the push were in different parts of the document. The fix: **no marks at all** on three of the
four boards; the fourth has one mark, added because `WX11` asked for it by name.

**`relief_scope: "hold"` is a plate, not a flush join.** I read *"`hold` lets the relief bring the lower
tier up to the shape"* as "the join comes out flush". It comes out flush only where the solver's answer
would have been lower; where the ground around is higher, a `hold` pad is *a plate punched through the
hill* — which is the other half of the same note, in a table I skipped. Gallowsholt's garths read
`drop −9` on the route before I moved the push's skirt off them.

**Zones are not fanned by the plan's symmetry.** Every piece is; `zones[]` is written back exactly as
stated. Kettleshulme's enemy team had **no bridge to its own island**, and nothing refused: the
evaluator scored 0, the compile answered 200. `tools/board.py`'s grid is what showed it, as ten cells
of enclosed void where a zone should have been.

**Three stepping stones in a row cannot satisfy `G5`.** The band is 10–20 blocks and it is a **hard**
term — a violation scores 1 000 and `valid: false`. The failing pair is not a neighbouring hop but the
**diagonal from a front's inner corner to the far stone**: with the fronts 10 blocks off the stones
and the middle stone 15 wide, that diagonal is 22. Two builds at 1002 before I read the pair names in
the lint rather than the distances. Two stones twenty apart put every pair inside the band.

**The crown divisor.** Computed twice, wrong twice. `RL6` reads it back.

**Props placed by eye are props declined.** Gallowsholt: seven declines, then four, then two, then
zero — and the only pass that moved the number was the one where every position came off the seats
mask. `DR-ROAD` measures to a stroke's *paved cells*, `DR-CLAIM` between props is footprint overlap,
`DR-TONE` refuses a rock cut from the ground's own tones, and `DR-STEEP` refuses one pinned to a face
the theme already calls a face.

**`solid(162)` is acacia log.** Dark oak is `162:1`. `HS4` refuses a frame whose beams and posts are
two woods, which is the right rule and a confusing way to learn a block id.

**Podzol may not lie under turf** (`PT1`), and a `cell` field in a `wall` or a `fill` with no `rise`
samples the plane only (`PT4`). Both refused a store; both are one line.

**A wool room needs two cells of interface with its approach, not one** (`WX6`).

**`SK13` is exactly as strict as it says.** Medlock's east incline reached four columns into the hub's
slot and the store refused. But a shape **raised above the ground** over a subtract is a bridge and not
a filling: Kettleshulme's launder deck at `base_y 16` over the same kind of slot stores at 200.

---

## What worked first time

Not padding — this is what the next reader can trust.

- **The composed arrangement itself.** All four boards evaluate at **score 0** with the composer's hub,
  frontline and proportions kept. Nothing about the arrangement needed rethinking; what needed moving
  was the spawn, the wools and the mid.
- **`editShapes`, per vertex.** About 120 ops over four boards: **zero** self-intersections, zero
  folded rings, and every corner the compile drew still exactly where the plan put it. `{"after": n}`
  inserting at `n+1` and shifting everything above it is the whole of the arithmetic, and running the
  list back-to-front is the whole of the discipline.
- **`bendShapes` with an explicit `side`.** `out` where a coast should read as land, `in` where the
  shape is one end of a measured hop. Both behave exactly as the magnitude table in
  `GENERATION-NOTES` says.
- **The excluded-pad-plus-flight idiom.** Gallowsholt's quarry wall came out as designed on the first
  build that had it: `z 34..44` flat at y10, `BARRIER +4` at `z 45`, then the fell; two rakes of
  fourteen blocks' run for six of rise cut through it, and the transect down the back of the fell reads
  worst step 1, walked end to end.
- **`kind: "made"` on a layer.** No `SK13`, the deck painted over its own span, and the ground four
  courses below kept its own grass and dirt.
- **A `layered` material on the `slope` axis**, on all four boards, cut against `GET …/incline`. Every
  board's three bands carry real ground: 43/34/23 on Gallowsholt, 50/27/23 on Kettleshulme,
  66/22/12 on Medlock.
- **`POST /plan/ascii`** over a posted plan, which `tools/board.py` does not cover for `mirror_z` —
  the local renderer draws the stated unit and not its image, so a `mirror_z` board reads as half a
  board there and whole through the API.

---

## Open gameplay questions

Decided without an oracle, built, and recorded here rather than filed as facts.

1. **How high may a mid island stand over the fronts?** Gallowsholt's causey is four blocks proud, so
   a player bridging out of his own front has to place a block to get onto it. That makes it a prize
   and makes the first team there hard to shift. Decided: four.
2. **Is a one-way high route good?** Kettleshulme's launder is a one-block step up from the mill yard
   and a five-block drop off its far end. Decided one-way, because it costs the raider his retreat and
   gives the defender the ground above it.
3. **Is ten blocks of void enough to make an attacker pay for an island wool?** Kettleshulme's near
   wool is the closest objective on the board to the crossing and is reachable by the defence over a
   bridge no attacker can stand on. Decided ten.
4. **Is a two-block bench across most of a board playable?** Medlock reads 1 854 scrambles and 126
   barriers — every step crossable with a placed block, nothing impassable. Right for a worked tip;
   possibly wrong for a board somebody has to sprint a wool across. This is the decision I am least
   sure of.
5. **What is a water lane worth in dead ground?** Longstrand's tide docks 175 blocks a side that no
   walked route reaches, because a lane sits outside the navigable set by design. Decided: worth it
   for a fourth crossing that arrives late.
6. **May two wools be the same distance and completely different to raid?** Longstrand's are 200 and
   192 blocks from the enemy's door; one is inside a ring of dune you must go round and one is on open
   strand. Decided yes, and it is the thing I would most like judged.

---

## The four boards

| | Gallowsholt | Kettleshulme | Longstrand | Medlock Drift |
|---|---|---|---|---|
| source | `rot_180` s0 | `rot_180` s23 | `mirror_z` s12 | `mirror_z` s34 |
| composed score | 0.302 | 0.0 | 4.173 | 1.548 |
| composed structure | ring · twin · i,i | double-hole · twin · i,i | twin · bar · l,donut | double-hole · twin · l,clamp |
| size | 90 × 200 | 110 × 180 | 115 × 230 | 105 × 190 |
| my score | 0 | 0 | 0 | 0 |
| pre-flight | OPEN | OPEN | OPEN | OPEN |
| coverage dead | 0.0% | 0.0% | 0.0% | 1.5% |
| mid | a flagged island, 15-block hop each side | two 15-block lanes, a declared buffer between | two stones + a water lane | two 25-block lanes, 20 of void between |
| intra-team zone | — | the island's own bridge (`CT4`) | — | the defender-egress bridge (`BZ5`) |
| layer | — | the launder deck, `kind: "made"` | — | — |
| relief | 1 push, 0 ground marks | 1 push, 0 marks | 2 pushes, 1 ground mark | 1 push, 0 marks, `step: 2` |

Every board's world, spec, renders and review are under `maps/`, `specs/` and `review/` at the slugs
`opus5-gallowsholt`, `opus5-kettleshulme`, `opus5-longstrand`, `opus5-medlock-drift`.
