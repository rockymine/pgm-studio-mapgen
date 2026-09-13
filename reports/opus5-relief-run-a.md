# Run A — four boards, a demonstration board, and what combining relief modes cost

Two Opus 5 agents authored eight boards in one run. This is Agent A's four; Agent B's are in
`reports/opus5-relief-run-b.md`. The organising idea was **combining relief modes** — a push
for the landform, marks for the ground that has to agree with something, `height_mode` shapes
for what people built — and one board with a tunnel network.

## What I set out to build

Eight identities, written down together before any shape was authored, and checked across the
set rather than within it so the run would not come out as eight greys.

| slug | one sentence | mode | ground tone | whose |
|---|---|---|---|---|
| `opus5-swallet-dale` | Played on two floors: a limestone dale above, worked galleries below, the monument in the dark. | destroy | pale limestone / dark wet rock | A |
| `opus5-ruddle-brink` | One continuous red scarp; the face is climbed in exactly three places. | core | **red sandstone (warm)** | A |
| `opus5-blindtarn` | A ring of fell round one frozen tarn; the corrie is the no-man's-land. | destroy | cold pale, snow | A |
| `opus5-skerry-wick` | Wool carried between islands; every route is a crossing somebody pays for. | wool | dark basalt / sea green | A |
| `opus5-goldbank-quarry` | Ground people cut away; both goals on the floor, under everybody. | destroy | pale gold oolite | B |
| `opus5-lynchet-brow` | A hillside farmed into terraces; every fight is one retaining wall. | core | green pasture | B |
| `opus5-scoriafell` | One mountain between two valleys; the pass is the whole map. | destroy | dark volcanic | B |
| `opus5-braidwater-ford` | A braided river; the two sides meet at three fords and nowhere else. | destroy | ochre floodplain | B |

`opus5-blindtarn` and `opus5-scoriafell` were both drawn as capture boards. Neither could be
one — see *What I could not say*.

## The four, measured

| | GO1 | slopes: walked / scramble / barrier / faces | claims | dead | gate |
|---|---|---|---|---|---|
| `opus5-ruddle-brink` | 3.24 | 12 536 / 792 / 724 / 16 | 14, **0 declined** | 19.2% | OPEN |
| `opus5-swallet-dale` | 3.47 | 13 248 / 1 342 / 706 / 20 | 9, **0 declined** | 23.2% | OPEN |
| `opus5-blindtarn` | 3.28 | 12 945 / 1 657 / 758 / 20 | 8, **0 declined** | 13.6% | OPEN |
| `opus5-skerry-wick` | — (wool) | 5 553 / 54 / 150 / 4 | 10, **0 declined** | **9.9%** | OPEN |

`symErr 0` on all four. Standing complaints, each answered by measurement rather than
redesign: `EL1`×2 and `RL2` on Ruddle Brink (the plan tier walks pieces flat and cannot see
an authored flight; the barrier *is* the cliff), `RL5` on Blind Tarn (26% level — a corrie is
a bowl), `LN1` on Skerry Wick (lane-width 0 on a board whose pieces are islands). Swallet
Dale finished with **no complaint of any kind**.

## The drill

Predicted before checking, scored before authoring.

| board | scramble% pred/actual | barrier% pred/actual | faces pred/actual |
|---|---|---|---|
| `opus5-alderfen` | 18 / **14.1** | 4 / **5.1** | 60 / **20** |
| `fable-mossgill` | 10 / **3.6** | 12 / **7.1** | 25 / **14** |
| `opus5-millrace` | 8 / **0.9** | 2 / **8.0** | 35 / **20** |

### The drill did not transfer, and it propagated a bias

The scores are in the 3–8 band, and none of them changed an authoring decision. Nothing
downstream consumes a predicted `scramble%`: a cliff is settled with `face`, a push with the
arithmetic `RL6` measures, a flight with a transect. A figure read out of a built world is a
diagnostic, and predicting it calibrates nothing.

It also did measurable harm. I predicted high, wrote the bias into this report as the drill
instructs, and Agent B reported: *"I over-corrected scramble downward after reading Agent A's
upward bias."* Two agents, two wrong directions, the second caused by the first's report. Both
of us were 2–4× high on faces, which the drill measured and neither of us learned from.

One fact in it is worth keeping and is now a sentence in the warmup rather than an exercise:
**barrier is not the tail of the scramble distribution.** The prediction exercise is replaced
by reading two `showcase/` diffs against `02-theme`, which is one technique per map and
therefore transfers to the next board directly.

Three biases, recorded for the next reader. I over-predicted scramble on all three — I was reading visual steepness on a heightmap where
1 char is 2–3 blocks and calling it scramble. I picked **mossgill** as the quiet-underfoot,
most-impassable board; it is **millrace**, at 0.9% scramble and 8.0% barrier. Barrier is not
the tail of the scramble distribution: it comes from vertical walls and shoreline, and the
gentlest board on the shelf can be the least climbable. And a "face" is a large coherent
slope region, not a local facet — I guessed 2–3× high, and so did Agent B.

## What I could not say

**Capture points — missing from the system.** I wanted a King-of-the-Hill board and
`tools/README.md` documents the finish key for one: `controlPoints`, with `scoreLimit`, onto
`intent.controlPoints`. It reaches nothing. Checked three ways before writing this down:
by **name** — `controlPoint` has 0 occurrences in `openapi.json`; by **function** — no rule
in `GET /api/rules`, no term in `/rules/terms`, no route; and in the **model** — `MapIntent`
carries `teams, maxPlayers, spawns, observer, build, waterLanes, wools, destroyables, cores,
modes, meta, symmetry, islandTeams, structures`, and no control point of any kind.
`MapParser.cs:57` lists `control-points` as `"CP/KOTH"` among the elements the studio
*refuses to read*. `drive.py` writes the key, `RQ3` names it unread, and the board exports at
200 with the gate open and nothing to win. Agent B took it further and asked
`PUT /map/{slug}/intent` directly — same two `RQ3` on a 200 — and found
`reports/opus5-threap-edge-run.md` claiming the feature had shipped, which makes this a
**regression** rather than a gap that was always there. Both boards became destroy boards.

**A covered floor cannot take a surface finish — out of reach rather than missing.** A cell
under a slab resolves one band stack and falls inside `fill`: no turf, no rim, no wall. The
gallery floors in Swallet Dale are themed for their *fill* for that reason. The mechanism is
documented and behaving; what is out of reach is a *different* surface treatment for the
covered storey, and nothing in the API offers one.

**Ground cover on a snowfield — not a gap, a consequence.** `FloraProp` seats on grass. Blind
Tarn's flat band is snow, so a flora pass over the whole board claimed 22 cells of 15 000. It
states no ground cover now. Worth knowing before authoring a cold board that wants dressing.

## What I got wrong

**I attributed a fix to the wrong change, and Agent B caught it.** I reported that a goal
with `piece: ""` loses its GO1 ratio — `/plan/inspect` had answered `own None enemy None
ratio None`. It does not. Re-measured at the end of the run on the same plan:

| goal states | own | enemy | ratio |
|---|---|---|---|
| `piece: "fell"`, `at: [38,42]` | 49 | 159 | 3.24 |
| `piece: ""`, `at: [-22,-62]` | 49 | 159 | **3.24** |
| `piece: ""`, `at: [-44,-124]` | null | null | null |

The `null`s were never about the piece. They were the **half-blocks** reading putting the
goal off the board. I changed two things in one edit — added the piece *and* halved the
number — and credited the wrong one. The unit itself is settled twice over, by both agents
independently: **`placements[*].at` is in blocks**, whatever the openapi description says.

**"A paint patch is `add` + `base_height: 1`, no override" is wrong**, and it is the recipe
in `GENERATION-NOTES.md`. On a board whose ground is more than one course high it paints
nothing, raises no warning, and `05-themes.txt` is the only witness — mine read "1 theme,
100%" for three consecutive builds. `override: true` does not help either. Reading
`SketchRasterizer.ShapeScopeOwners`: a scoping shape owns a cell only where its own top
**equals** the tallest top there, and a one-course add at bedrock under twelve blocks of
terrain never is. The exception is a *standing* shape — `IsErected()`, true only when the
shape declares `height_mode` of `level|raise|sink` — which is always a candidate whatever its
height. The working form is `height_mode: "raise", base_height: 0, skirt: 0`, and it took the
census to 87.3 / 6.8 / 6.0 with drawn borders. Agent B hit the same wall independently and
added the caveat: a `raise` reads the **median** ground under its footprint, so a patch drawn
across a slope flattens it.

**I built a cliff that was a ramp and did not notice for two builds.** Ruddle Brink's scarp
stated `high 23, low 12, face 6`, and the transect read *walked end to end, worst step 2* —
eleven blocks over six is a 45° slope a player strolls up anywhere, which made the board's
identity sentence false while every gate stayed green. Two causes: `face: 2` is what makes a
brink, and the `backridge` push's skirt reached the lip and **graded it**, because a push is
added to the surface the marks solved.

**I wrote "one theme is fine" when four themes were registered and three were inert.** Three
themes is a map; three themes in the registry and one on the ground is a swatch nobody
painted. `05-themes.txt` on every build, before the pictures.

## What worked first time

- **The plan grid caught the board before the world did**, both times it mattered. `board.py`
  showed Ruddle Brink's build zone spanning the full width of the bench — the wheal-hazel v2
  fix built in rather than discovered at coverage — and Skerry Wick's hub ring declaring its
  32-cell enclosed void by arrangement.
- **`kind: "made"` on a layer cleared `SK10` and `SK11` at once**, on a board that had raised
  seven of them. `SCULPTING-WITH-LAYERS.md` §6 still lists it among the things that *could*
  become a tool; it has shipped, with `part_of` beside it.
- **Deriving the rock from the corridors.** Swallet Dale states five corridors and computes 35
  rock rectangles as their complement, so a corridor moved can never leave a wall behind —
  which matters because the taller add wins a column outright and a wall crossing a drift
  seals it with the export gate still open.
- **Asking the composer for the wool board's proportions instead of deriving them.** 105 land
  cells a team; mine came out at 104, and `fill-ratio` never complained.
- **`loop.py --candidates`.** Twenty seconds a pass, eight positions at a time, and it turned
  five declined props into ten placed with zero declines across two boards.
- **`height_mode: level` ramps worked first time on every board**, at worst step 1, every time
  the run was at least twice the rise.

## Open gameplay questions — decided without an oracle

1. **Is a one-way entrance fair?** Swallet Dale's swallet is a hole in the crag's crown: you
   drop about nine blocks into the chamber and cannot climb back out that way. I built it,
   because an attacker choosing a committed route is a decision and a defender knowing where
   it lands is an answer. It may simply be a trap.
2. **How much of a cliff may be broken before it stops being a cliff?** I ruled three ways up
   in 104 blocks, leaving 63% of Ruddle Brink's brink unbroken, and shaped the ways up as
   embankments specifically to keep that share high. The number is mine and nothing checks it.
3. **Should the two wools be near-and-far or side-by-side?** Skerry Wick wanted one deep wool
   and one forward. `WL9` holds the pair to 1.232× of each other's walk and a near/far pair
   cannot be that, so the idea survives as separation — two flanks, 55 blocks apart — rather
   than depth. Whether `WL9`'s band is right for an island board is the author's call.
4. **Is a corrie floor that is 26% level enough to fight in?** `RL5` says 30%. I chose the
   bowl over the bar.


---

## The demonstration board

`opus5-marram-hythe` was built after the four above, against the standard the four did not
meet. It is a shore: a strand, a dune field and a built quay, with the monument on the quay.

**What it demonstrates that the four did not.** The audit the warmup now asks for, run on the
generated finish rather than on the script that wrote it:

| | `marram-hythe` | `ruddle-brink` |
|---|---|---|
| reliefs — two is two grounds meeting | **2** | 1 |
| marks / kinds | **10**, four kinds | 4, two kinds |
| pushes | **0** | 2 |
| `level` flights | **4** | 2 |
| `exclude` made ground | **1** | 0 |
| polyline shapes | **1** | 0 |
| `made` layers | **2** | 0 |
| copied tree recipes | **8** | 0 |

It exports with the gate OPEN and **no complaint, no refusal and no decline**.

**The thing it is actually about** is that the beach meets the dunes two different ways, and
both are one transect: at x −42, where nothing is stated between them, the shore rises at
**worst step 1, walked end to end**; at x 10 and x 40, along a six-point `scarp`, it carries
**BARRIER +3**. Not everything on a board meets the same way, and a board where everything
meets the same way has one idea in it.

**The move that made the flow possible was giving up a plan piece.** The first draft stated the
strand as a full-width piece at surface 9 against one at 14 — a straight five-block step the
width of the board. `fable-saltwharf` is one piece with `base` at the *high* value, `reach: 0`,
and the beach as a small `area` mark scooped out of it; what lies between the mark and the
brow is the solver. That is the flow, and it cannot be had from two pieces.

**Two reference boards, read rather than remembered.** `fable-saltwharf` is the only one of the
eight carrying both a core and an ender-stone pillar, and it is the beach-meets-grass-meets-made
-ground board: one relief group, `reach 0`, two area marks thirteen blocks apart, grain 0.7.
`fable-ashcombe-delph` is the fable board with the `under` layer and the most tunnel language:
a six-point curving `scarp`, a ten-point `area` ring, grain 0.6, **zero pushes**, and its
tunnels as a plain layer of rock rectangles at `base_height` 16 with the gallery at 12.

Six of the eight reference boards carry **no push at all**. All four of mine carried two. A
push is a landform somebody stamped; four `point` marks with the relaxation between them are
a dune field.

**New findings, measured on this board:**

- A parapet stated from the surface it stands on **deletes that surface**. Among the shapes of
  one layer the taller add wins the column *floor included*, so a sea wall at `floor 20,
  base_height 2` over a quay topping at 20 left the world holding only the wall (`SK9`). From
  `floor 0, base_height 22` it is simply the taller shape and the quay survives.
- **`SketchShape.type` accepts `polyline`, and its own openapi description says `path`.** A
  `path` draws no ground; `SK3` names it, on a 200.
- **`radius` on a water pool is the shelf**, not a width — how far in from the outline the bed
  is held up. A shelf on ground already at the water line is dug and holds nothing, which is
  what `DR-DRY` reports.
- `teamTint.neutral` is a **material**, not a block id.
- `props.py` emits a `SketchLayer` — `{id, name, base_y, layout:{shapes, groups}}` — and
  `drive.py`'s `addLayers` takes the same fields **flat**. The nesting has to be unwrapped.
- A hollow sculpted tower with no door is a **SEALED void** the void scan reports and nothing
  can enter. A landmark seen only from outside is stated solid.

**Coverage calibration, which the four boards lacked.** The shipped boards read 17.9%
(`blackden-sough`) and 35.6% (`burgage-terrace`) dead on a single-objective board;
`heftfold` reads 0.0% and is a wool board. 24.7% here is mid-range, and the dead ground is the
defender's rear. Chasing the number past that point reshapes a board for a measurement.
