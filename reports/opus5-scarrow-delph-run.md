# Opus 5 — Scarrow Delph: what a relief can say about carved ground

## What I set out to build

A worked hillside quarry where the terrain *is* the board, announced before anything was authored:

> Two hillsides facing each other across a valley, a quarry cut into each and **benched** so the face
> steps down in worked terraces; **haul roads** switchbacking down each face, wide enough to fight on and
> graded so a player can walk them; a **flooded pit** at the bottom of the valley with the water at one
> level; **spoil heaps** and an overburden lip that read as material moved. Objectives placed so that
> **height** is the defence rather than distance — one goal at the bottom of a pit and one on a bench.

Slug `opus5-scarrow-delph`. 108 × 220 blocks, `rot_180`, cell 2, two destroyables a team, four buildings,
one lake. `maps/opus5-scarrow-delph`, `specs/opus5-scarrow-delph`, `review/opus5-scarrow-delph.md`.

Everything vertical is a relief mark. The plan is **five rectangles**: the moor split into three by the
spawn piece, one big `works` piece for the whole hillside, and a neutral island for the flooded pit. The
relief carries **seventeen marks and three pushes** on the team group and three marks on the pit.

## The three numbers, and the one that is the board

```
03-slopes.txt   cells: 16656 walked, 1824 scrambled, 2480 barrier; faces: 20, largest 755 at x -54..0 z -82..-28
06-claims.txt   placed 56, declined 0
04-routes.txt   spawn-blue -> dt-pit-0: barrier +4 at (-44,-22); barrier +20 at (-44,-36); drop -11 at (-42,-46)
```

The relief read, per group, `POST /map/{slug}/sketch/relief/read`:

| group | cells | low | high | relief | landform stated / measured | scramble : barrier | cliffs | symmetry error |
|---|---|---|---|---|---|---|---|---|
| `team` | 9072 | 13 | 57 | 44 | `hills` / `hills` | 566 : 641 = **0.88** | 15 | 0 |
| `neutral` | 2816 | 4 | 10 | 6 | `plain` / `plain` | 0 : 160 | 0 | 0 |

At the walk tier (max step 1) the team group is **93.3% crossable, one place holding 99.8%, 11 ledges**,
over **143 faces** of which 15 qualify as cliffs — the four biggest 24 wide × 12 down, 21 × 22, 20 × 6
and 20 × 13.

**And the number that says the board works.** `GET …/walk` from the shore an attacker lands on to each
of the enemy's two goals, at both aims:

| from the enemy's brink to | shortest route (`aim=travel`) | fewest blocks (`aim=reach`) |
|---|---|---|
| **The Sump** (−28, −60), the delph floor at y24 | 33 blocks, **19 placed** | 109 blocks, **0 placed** |
| **The Gallery** (22, −58), the shelf at y32 | 31 blocks, 5 placed | 38 blocks, 0 placed |

That is the whole design in one table. The gallery is a 1.2× detour or five blocks; the pit is a **3.3×
detour or nineteen placed blocks** — the straight line into it meets `barrier +18 at (−30, −35)`, the
delph's own face over the valley. Since only the middle band of the board is buildable, in play it is
always the detour. Neither goal is far away and both are expensive, which is what "height is the defence
rather than distance" was supposed to mean.

Plan tier, first read and never moved: `score 0, valid True`, no lint. `GO1` 3.41 and 3.35 against the
authored band [3.0, 4.0]; own-spawn walk 49 for both goals (`GO4` [40, 90]); the team's own pair 50
apart (`GO2` [35, 65]); opposing pairs 132 / 124 / 118 (`GO3` [85, 150]). `coverage`: reached 13244,
decorated 3364, **dead 4352 of 20960 = 20.8%**.

---

## What the surface let me say, and what it did not

### 1. A block step per group, when a quarry needs one per feature

**Wanted:** the delph's faces terraced at a 6-block quantum and the haul road left at 1, so the benches
step and the road is walked.

**The surface:** `SketchReliefJson` carries `step` once, and it is keyed by **group**, which is a whole
landmass. `ReliefMarkJson` has no step field (`id`, `kind`, `at`, `r`, `width`, `points`, `ring`, `h`,
`depth`, `high`, `low`, `face`, `band` and nothing else) and `SketchShape` has none either — it carries
`height_mode`, `skirt`, `relief_scope`, `base_height`, `anchor_heights` and `floor`, none of which is a
quantum.

**What I did instead:** dropped `step` to 1 and wrote the four bench levels as **nested `area` marks,
outward-in**. A later mark wins a contested cell, so `q-lip` 42 → `q-bench3` 36 → `q-bench2` 30 →
`q-floor` 24 terraces itself, and the roads keep a one-block quantum. Cost: four marks instead of one
number, and four `loop.py` passes to find out.

**Measured, on this board's own marks, changing only `step`** — four `loop.py` passes at one point in
the build, so the four rows compare with each other rather than with the shipped board's final numbers
above:

| `step` | scramble | barrier | ratio | cliffs | rows crossable on foot, x | rows on foot, z | `RL2` |
|---|---|---|---|---|---|---|---|
| 1 | 559 | 603 | 0.9 | 15 | 4 / 84 | 1 / 108 | fires |
| 2 | 1881 | 482 | **3.9** | 15 | 0 / 84 | 0 / 108 | **silent** |
| 3 | 12 | 1785 | 0.0 | 17 | 0 / 84 | 0 / 108 | fires |
| 6 | 2 | 1086 | 0.0 | 31 | 12 / 84 | 0 / 108 | fires |

Two things in that table are worth carrying away. **`step 2` is the only setting `RL2` accepts**, because
every riser becomes exactly a two-block scramble and the rule reads a board of two-block walls as graded
ground — and it is the setting that leaves *no* row crossable on foot in either direction. And **`step`
at the bench height destroys the roads**: at 3 and 6 the surface has essentially no scrambles at all, the
road's own grade having been snapped away with everything else.

**Verdict: missing.** There is no per-mark or per-shape quantum in `openapi.json`. The workaround is
complete, so it is a convenience gap rather than a capability one — but the documented instrument for a
quarry (`GENERATION-NOTES`: *"`step` with `stairs` is the instrument for a quarry"*) is incompatible with
the other half of the same brief, and nothing says so.

### 2. Protecting a flat mark from a push

**Wanted:** a level platform for the winding house inside a spoil heap's falloff.

**The surface:** `relief.md` §2.1 states it plainly — a push is applied to the solved surface and steps
over a *room* floor only, because a room floor is rigid; an author's own area mark is a statement about
the ground and a push crossing one sculpts it. There is no field for it: `ReliefMarkJson` has no
rigidity flag and `ReliefPushJson` has no exclusion list.

**What it cost:** two builds. `WX11 — house winder 0 stands 6 blocks above the cell beside it at
(−48, −92)` and `house smithy 0 stands 8 blocks above the cell beside it at (28, −91)`, with the studio
offering the fix as a mechanical `edit` (an area mark at 56, which would simply have flattened the heap).
The fix was to move both heaps into the back corners and both platforms out of every falloff: four edited
rectangles, one drive.

**Verdict: missing** for a mark — but see the next item, because a *shape* can do it.

### 3. A level floor inside a relief — and a thing I cannot explain

The loading stage at the water's edge stands on a quay. Two ways to state it, same rectangle, same run:

| stated | result at (7, −33) |
|---|---|
| `relief_scope: "hold"`, `base_height: 18` | flat **y17** from z −41 to −30, then 12 — and the surface either side solved *up to meet it*, reading 17 at x −6 as well |
| `relief_scope: "exclude"`, `height_mode: "level"`, `base_height: 18`, `skirt: 3` | **y15** — the relief's own value. No plate at all |

Both readings are `POST …/sketch/columns` on the compiled-and-patched layout, taken through
`tools/loop.py --column 7,-33`, thirty seconds apart with one word changed. The stored version — the
`hold` one — goes through `POST /map/from-documents` with **no `RQ3` on any of the three documents**, so
the field is read rather than dropped; the `exclude` variant was never stored, and `sketch/columns` does
not answer `RQ3`, so I cannot say from here whether that word was read. I reached for `exclude` because
`GENERATION-NOTES` says it is what makes a vertical-sided shape, and `hold` is what makes a floor —
**that part was mine to get wrong**. The `exclude` result is an observation with a coordinate on it, not
a defect I am filing.

**Verdict: mistaken** about which word I wanted. The mechanism exists and is `hold`.

### 4. Painting a patch on a group that is not group 0

**Wanted:** an `addShapes` polygon with its own theme on the flooded pit's beach — the same brush the
brief calls for ("splotches beat patterns, and a splotch is a shape").

**The surface:** `tools/drive.py`'s `patch_layout` appends every `addShapes` entry to
`groups[0]["shapeIds"]`, which on a compiled board is always `team`; the finish's vocabulary has no way
to name a group. The API underneath does not have this limit — `SketchLayout` carries `groups[]`, each
with its own `shapeIds`, and `POST /map/from-documents` takes the whole layout.

**What I did instead:** themed the whole island by its compiled shape id,
`themeById: {"s1": "spoil"}`. One line, and one landform's worth of paint I could not state.

**Verdict: unreachable.** The mechanism is in the document; the driver's finish hides it.

### 5. Saying that ground is *cut* rather than ungraded

`RL2` reads the team group at 0.9 two-block scrambles per taller barrier and says *the elevation is there
and was never graded*. On a quarry that is a description, not a fault: the benches are cut and the roads
are graded, and the rule measures the island rather than the feature. There is no word for it —
`landform` takes four, and the four are kinds of ground, not kinds of working.

While checking this I nearly filed a second claim and the schema corrected me. I had written that
`openapi.json` describes the field as *"one of Landform's four words"* without naming them. It names
them: `SketchReliefJson.landform` carries `"enum": ["plain", "rolling", "hills", "mountain"]`, and I
missed it because my first pass over the schema printed each property's `type` and `$ref` and not its
`enum`. **Mistaken, and the check the brief asks for is what caught it.**

What is left after that check is smaller and real. The endpoint does **not enforce the enum**: a word
outside it is accepted silently and behaves exactly like stating nothing. Measured on this board's own
layout through `POST …/sketch/relief/read`, which stores nothing:

| stated `landform` | warnings |
|---|---|
| `plain` | `RL1`, `RL2` |
| `rolling` | `RL1`, `RL2` |
| `mountain` | `RL1`, `RL2` |
| `quarry` | `RL2` |
| `Hills` | `RL2` |
| `HILLS` | `RL2` |
| absent | `RL2` |

`hills` is this board's true measure, so the three rows that answer `RL2` alone are the ones where the
claim was thrown away. **A typo in `landform`, or the wrong case, turns `RL1` off and nothing says so** —
no refusal, no `RQ3`, no complaint. The studio's own `RQ3` discipline is exactly the thing that would
have caught it, and this is a field value rather than a field name, so it does not.

`landform` is also the only closed set in the relief vocabulary that is published as an `enum` at all:
`ReliefMarkJson.kind` (the five mark shapes), `SketchShape.height_mode` and `SketchShape.relief_scope`
carry their words in prose only, so those three have to be read out of a description rather than out of
the schema.

**Verdict on the missing word for "worked ground": missing**, and arguably correctly so; the alternative
is a word an author uses to switch a measurement off. **Verdict on the unenforced enum: a real gap.**

### 6. Two correct readings that look contradictory

`acrossZ` reports **0 of 108 rows** crossable on foot north–south, while the walk tier reports **one place
holding 99.8%** of the same group. Both are right: the fords count straight rows and the tier floods.
Reading the first alone would say the board is cut in half; it is not. Naming this here because
`opus5-run4` nearly redesigned a correct board off a similar mismatch.

### 7. Where I looked before writing any of the above

`GET /api/openapi/v1.json` (161 routes, 363 schemas) for `SketchReliefJson`, `ReliefMarkJson`,
`ReliefPushJson`, `ReliefGrainJson`, `SketchShape`, `ReliefReadDto` and the four relief routes;
`GET /api/rules` (150 rows) and `?family=RL`, `?rule=` for `EL1`, `GO1`–`GO4`, `CT12`, `G2`, `G5`, `G8`,
`LN1`, `LN2`, `SP8`, `SP9`, `ST9`, `ST10`, `FR9`, `OB17`, `OB19`, `PT1`, `PT2`; `GET /api/terrain/patterns`
for the fourteen pattern kinds and their exact field names.

---

## How I edited the layout while iterating

**I never edited a stored layout. Every iteration regenerated both documents from
`specs/opus5-scarrow-delph/build-spec.py` and re-posted the whole map** through
`POST /map/from-documents`, which replaces the map at the slug outright.

That was not a considered choice between two surfaces so much as the shape the tooling has. A spec here
is a plan plus a *finish*, and the finish is a **patch language over a fresh compile** rather than a
stored document: `drive.py` compiles the plan on every run, applies `themeById`, `addShapes`, `relief`,
`themes`, `roomStyles` and `dressing` onto the result, and overwrites `<slug>.layout.json` as **output,
never input**. There is nothing incremental to edit, because the layout is derived on every run. Writing
one back and patching it again would append `addShapes` twice.

The partial-edit surface does exist and I read it before deciding:
`PUT /api/map/{slug}/sketch/relief/{groupId}` replaces one group's relief in place, `DELETE` takes it
off, `GET` reads it back, and `PUT /api/map/{slug}/sketch` replaces the whole blob verbatim. On a board
whose relief is emitted by a Python file, a partial write has to be reconciled with the generator on the
next run, and `GENERATION-NOTES` records the trap on the neighbouring route — a relief posted to
`sketch/from-plan` answers 200 and builds the terrain that was already there, so the read-back and the
render disagree and both are correct. I did use `PUT`-shaped thinking exactly once, and read-only: I
posted nine *modified copies* of the stored layout to `POST …/sketch/relief/read` to probe the
`landform` word set, which stores nothing.

**What actually made iteration cheap was not partial writes. It was not storing at all.**
`tools/loop.py` compiles the spec the same way the driver does and posts the result to
`sketch/relief/read`, `sketch/dressing` and `sketch/columns` without writing a map row.

| | count | each |
|---|---|---|
| full drives | 5 (4 stored; one refused at `HS3` before storing) | 12–18 minutes |
| `loop.py` passes | 17 | 20–70 seconds |
| `--dry` runs, and plan variants posted straight to `/plan/evaluate` | 2 + 9 | 2–4 seconds |

Every number in this report that decided something came out of a loop pass or an evaluate probe. The
drives confirmed and exported. The board's whole shape — the width, the goal positions, the four bench
rings, the block step, the road grades, the prop positions — was settled before the second stored build.

---

## What I got wrong

**I read the evaluator's score upside down.** The first plan was 144 blocks wide and answered
`score 0.8, valid True` with one soft violation, `max-chain-length 144 outside authored band [25, 110]`.
I narrowed the board to 108 to see what happened and got `score 0` — and read that as *worse*. The score
is a distance: 0 is a board with no term outside its band. Two minutes, three plan variants posted to
`/plan/evaluate`, and the narrower board was right for the design anyway.

**The board's main lane was a twenty-block cliff and no picture showed it.** The spine between the delph
and the gallery is unpinned ground between two tall marks, and the relaxation holds it near its
neighbours' height and then lets go. Measured down x = 2 before the spine was stated:
`z −50: 30 · z −48: 24 · z −46: 39 · z −42: 39 · z −40: 39 · z −38: 19 · z −30: 15` — a fifteen-block step
up into a plug the haul road's first vertex had pinned at 40, and a twenty-block fall off its far side in
two blocks. It came out of `loop.py --profile x=2,z=-110..-26`; it is one shade in a heightmap and
nothing at all in the isometric.

**The haul road started at the wrong end.** Its first vertex was at the delph's mouth at y40 while the
spine there solved to y24, so the road pinned a fifteen-block plug across the lane. A road mark has to
start where the ground it leaves is already at the road's stated height — which for a quarry means the
brow, not the mouth.

**Two buildings inside a push's falloff, twice.** Item 2 above.

**The strata read as one flat grey until I opened a section at scale 4.** The first stone stack was
stone / andesite / stone / diorite / stone / andesite, which is six bands and, in 1.8, three shades of
the same grey. `POST /api/terrain/theme-preview?format=png&view=section&scale=4` shows it instantly and
the thumbnail the driver takes by default does not — the three at `scale=4` are in
`specs/opus5-scarrow-delph/renders/close/`, which is a subdirectory so the driver's sweep leaves it. The fix was contrast inside the same family: a
gravel parting, a cobble bed and a coarse-dirt parting between the stone beds. On a board with fifteen
cliffs and a hundred and forty-three faces this was the largest visual miss on it.

**I wrote that `openapi.json` does not name the four `landform` words.** It does, in an `enum` on
`SketchReliefJson.landform`; my schema dump printed types and `$ref`s and skipped enums, so I read a
prose sentence and believed it over the schema three rows below. Corrected above, before the claim was
filed.

**Dressing by eye, three times.** Six declines, then five, then three, then none — every one a boulder or
a tree in a building's claim, a road's standoff, a spawn keep-out or a goal's clearance. `loop.py`'s
dressing preview answers all of them in under a minute, which is what made four passes affordable.

---

## What worked first time

- **The goal bands, from arithmetic off the rule text.** `GO1` says the ratio is about `(L − d) / d`, so
  with the spawns 196 apart the goals want `d ≈ 44`; placed there, `/plan/inspect` answered 3.41 and 3.35
  on the first read and the four bands have not been touched since.
- **Nested `area` rings terracing outward-in.** Four rings, four benches, 6-block faces, no `step`.
- **A road as a `line` mark with a height per vertex, written last.** The haul road's 250 blocks of run
  for 17 of fall is a grade of 0.07 and the spiral cuts three bench faces without being buried by them.
- **`relief_scope: "hold"` for a built floor.** Flat at y17 and the ground solved up to meet it.
- **The water.** `shape: "pool"` with a twelve-point ring and a stated `level` filled a basin the sketch
  had dug out: `transect-tarn.txt` reads water top y8 continuously from x −41 to x 41 at z 0 over a bed
  at y4.
- **`rot_180` symmetry error 0** on both groups on every build.
- **`preflight` OPEN** on the first stored build and every one after.
- **`tools/board.py`** before the first post — five rectangles and their relations on one screen.

---

## Open gameplay questions

No oracle was available for these; I built my judgement and am recording the question.

**Only the middle band of the board is buildable.** The plan's single build zone becomes
`build.areas = [{−54, −30, 54, 30}]`, so a player can bridge to the flooded pit and nowhere else — no
towering up a bench, no shortcutting a face. That makes the terrain an absolute gate and it is why the
attacker's route to The Sump is always the 109-block walk rather than the 19-block climb. I took it
because every board in `specs/` here does, and because it is the strongest possible reading of "height is
the defence". A quarry may want the opposite.

**A goal at the bottom of a pit with one walkable way out commits its defender too.** The Sump's own team
reaches it at `rises 0, falls 3, worst step 7` — they arrive by falling — and leaves by the haul road.
Is a pit whose defenders are as stuck as its attackers a good objective or a trap for both sides?

**Two goals a team on a 108 × 220 board.** The brief's ruling is one destroyable a team on a board a
hundred blocks or less across. This board is 220 along the lane, `GO2` and `GO3` both hold, and the two
goals are genuinely different problems — but the ruling is stated on a size and I read it as scaling.

**20.8% dead ground on a benched board.** The two largest patches are about a thousand cells each at
(−45, −67) and (44, 65) — the bench interiors between the passes of the haul road. On a corridor board
that would be a fault; on a quarry the bench *is* where the fight happens even though no journey needs to
cross it. `coverage` cannot tell the difference and neither can I.
