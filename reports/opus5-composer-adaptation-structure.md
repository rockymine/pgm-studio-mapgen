# Composer adaptation, structure emphasis — Opus 5

Four CTW boards, each adapted from a board pulled off `GET /api/compose`, with one thing in common:
**built ground doing the gameplay work, and relief used where it is wanted rather than everywhere.**

| slug | source descriptor | composed structure | card score → shipped | what the structure is |
|---|---|---|---|---|
| `opus5-revetment` | `players=30 symmetry=rot_180 seed=2` | hub `double-hole`, front `bar`, wools `i`/`i`, 118 land cells | 0.278 → **0** | a hillfort: 70 blocks of six-course revetment, two stairs cut into it, a bastion, two walled wards |
| `opus5-portway` | `players=30 symmetry=mirror_z seed=2` | hub `bar`, front `twin` (8-cell hole), wools `i`/`i`, 123 | 0.000 → **0** | a breached rampart, a gatehouse closing the hub's front, a stone pier in the gap |
| `opus5-sallyport` | `players=30 symmetry=rot_180 seed=66` | hub `bar`, front `single`, wools `i`/`l`, 138 | 1.392 (WL10 refused) → **0** | a rampart with a postern, and a wool on an outwork you have to bridge to |
| `opus5-quadrangle` | `players=30 symmetry=rot_180 seed=7`, **flipped to `rot_90`** | hub `ring`, front `none`, wools `i`/`i`, 56 | 1.881 → **0** | four walled quadrangles round a crossed court, each with a cloistered yard |

All four end `export gate OPEN`; all four read **0.0% dead** on `GET …/coverage`.

---

## 1. What I set out to build

The author's ruling is that relief should be used and that overdoing it is a danger — solid
structural areas are likewise important. So on every one of these four the *shape* budget was spent
on made ground and the relief was confined, deliberately and by name:

- every board states its made ground as its own compiled shape and takes it out of the solve with
  `relief_scope: "exclude"`, so the grown ground arrives at a **face** rather than being graded into
  it, and every face has an authored flight or a gate;
- every board's relief is one group, five to seven marks and exactly **one** push, and the push's
  ring plus its falloff is checked against the nearest flight's foot before it is written;
- the structures are **47 made layers** across the four, all of them circles, polygons and
  rectangles with `kind: "made"` and a `part_of` — four crenellated curtain systems, **twelve** drum
  towers, a full `props.gatehouse`, a tapered turret, a three-tier ziggurat barrow, a twelve-pillar
  colonnade, eight bars of well rail, and two bastion battlements with returns.

Each board was written down in one sentence before a shape was authored; the four sentences are at
the head of the four files in `review/`.

## 2. The four boards, in numbers

| | revetment | portway | sallyport | quadrangle |
|---|---|---|---|---|
| size | 100 × 170 | 95 × 180 | 120 × 180 | 170 × 170 |
| teams | 2 | 2 | 2 | **4** |
| `plan/evaluate` | 0, valid | 0, valid | 0, valid | 0, valid |
| preflight | OPEN | OPEN | OPEN | OPEN (per team) |
| coverage dead | 0.0% | 0.0% | 0.0% (1% off-route) | 0.0% (1% off-route) |
| attack ratio before → after | 1.11 → **1.02** | 1.10 → **1.01** | 1.28 → **1.02** | n/a → 1.22 |
| defence ratio before → after | 1.27 → 1.04 | 1.29 → 1.08 | 1.08 → 1.22 | — |
| relief `level` | 0.325 | 0.541 | 0.551 | 0.589 |
| relief `largestField` | 0.055 | 0.286 | 0.185 | 0.334 |
| relief range / cells | 4 / 1030 | 7 / 3047 | 8 / 2777 | 9 / 2316 |
| `symmetryError` | 0 | 0 | 0 | 0 |
| seams (all step 2) | 3 | 1 | 1 | 0 |
| slopes: walked / scramble / barrier | 7052 / 94 / 172 | 6496 / 68 / 92 | 6788 / 232 / 272 | 12684 / 264 / 200 |
| faces, largest | 8, 61 | 8, 19 | 4, 76 | 12, 28 |
| themes | 54 / 28 / 18 % | 92 / 7 / 2 % | 76 / 12 / 12 % | 60 / 29 / 11 % |
| made layers | 15 | 18 | 9 | 5 |
| props placed / declined | 22 / 0 | 14 / 0 | 16 / 0 | 26 / 0 |

Every "before" flow number is `GET /api/map/{slug}/plan/flow` run against the **composed plan itself**,
stored under one probe slug (`composed-p30-t2-2`) and re-`PUT` for each source. That row is the
brief's §2 measured on the actual sources rather than quoted from its table.

## 3. What I could not say — three verdicts, kept apart

### Missing from the system

**Nothing.** Every instrument the brief names was found and used. The three items I was closest to
filing as gaps all turned out to be *mistaken* and are below.

### Unreachable from where I was standing

- **`tools/board.py` cannot draw a `rot_90` board.** It renders the stated unit and its `rot_180`
  image and labels the legend "lower = its rot_180 image". For the four-team board it is still the
  right read for the unit's own relations — which is what it is for — but it cannot show the fan, and
  the fan is where a quadrant unit fails. What I used instead was arithmetic: under `rot_90` the
  images of a point are `(−z, x)`, `(−x, −z)` and `(z, −x)`, so a unit strictly inside one quadrant
  cannot meet them. The verdict is *out of reach from where I was standing*, not missing: the check
  is three lines and the render is not the only way to make it.

- **The composer's own vocabulary stops at two teams.** `GET /api/compose` answers 400 for both
  `rot_90` and `teams=4`, so there is no way to ask it for the *arrangement* of a four-team board —
  where a quadrant's frontline sits relative to a crossed court, how big a quadrant unit should be
  for a given player count, what a four-team land budget is. All of that had to be invented. See §6.

### Mistaken — it exists, it is documented, and I nearly filed it anyway

- **"A wool room reached only over a build zone is unreachable."** I expected `preflight` to refuse
  Sallyport's outwork. `WL11`'s own text says a room reached only over a build zone "states no land
  seam and is not this rule's business but `BZ5`'s", and `Traversability.Check` connects "across the
  build geometry". It passes, and the log says so in those words.
- **"An approach wall seals its interface and will block traversability."** `StructureStamper.StampWall`
  raises solid bedrock from y 0 with a cobweb course on top, which reads as impassable in
  `render/traversability` (`B99`). But the gate reads `WorldWalk.Ground` off the map document, and a
  wall is a stamp: nine bedrock curtains across these four boards and the gate opens on all of them.
- **A `teamTint` on terrain.** I expected `PT5` — one colour for the whole board. It is one colour per
  **canonical island**, and on a CTW board whose halves are joined only by a build zone each team's
  land is its own island. Three of these four boards carry a tint course in a `wallDiagonal` and each
  fort wears its own garrison's colour; on `opus5-quadrangle` that is four colours on four quadrants.

## 4. What I got wrong

**I predicted Sallyport's lopsided wool could not be closed, and it closed.** The argument was sound
as far as it went — with the spawn in a corner of its own half, the locus of points equidistant from
both spawns is the perpendicular bisector of the spawn-to-spawn line, and for a corner spawn it runs
outside the half — and I wrote it into the spec's docstring as a reason to compensate with cost
rather than distance. Then the walk read 169 / 165. Moving the near wool twenty blocks west onto an
outwork across a strait moved the *walk* by thirty-five, because the walk has to come back round the
water. **Straight-line arithmetic is not a walk**, and `plan/flow` costs nothing to ask.

**A push on a narrow field puts a pit at a stair's foot.** A push is applied after every constraint,
so Revetment's first `knowe` lifted the meadow beside the west stair to 15 while the flight's own
anchor held its first tread at 11. The transect read `DROP −4` at (−13, 27). Nothing else reported
it: the flight walked end to end, the relief read had no seam, the gate was open. The rule is
arithmetic — ring radius + falloff must clear the foot — and it was applied to the other three
boards before their first build.

**I gave a terrace one flight instead of two.** Sallyport's rampart stands on a terrace three courses
over the moor. The sally port climbs it from the *attackers'* side; the garrison's own side had no
ramp, so a defender could drop off their own rampart and not get back up. `EL1` named the seam at the
plan tier and I had read that as answered by the flight I had already cut. A transect out of the
spawn read `−3` at z 45. Both re-entrants are now cut and both flights walk.

**Made layers were stamped through bedrock, nine times over four builds.** `SK18` — a made thing and a stamped structure
sharing courses — fired five times on Revetment and once each on three other builds. Neither pass
reads the other. Parapets now stop short of the wall columns, which is also the honest reading: the
bedrock *is* the parapet where it stands.

**Two room styles and one house style refuse with `HS9`.** `@hb-cage`, `@sb-assay` and `@lk-terrace`
lay beams over walls with no laid-log course. The tell is `beams.any: true` with no `laidLog` band
anywhere in the style, including its storeys. Forking one with `"beams": null` is a **500**, not a
400 — dropping the key outright parses.

**Every prop I placed by eye was declined.** Across the four boards the first dressing pass declined
5, 5, 5 and 6 of them — `DR-SITE` on ground a vertex edit had taken away, `DR-KEEP` inside a door's
approach or a goal's ring, `DR-STEEP` on a face the theme already calls a face. Everything that
shipped came from `POST …/sketch/seats` or `loop.py --candidates`. Final tally: 78 placed, 0 declined.

## 5. What worked first time

- **Per-piece `surface` on a composed plan.** One line per piece ends the merge, gives one polygon
  per height and makes a composed board paintable. Every one of the four did this and none of them
  needed a second try.
- **`editShapes` as an ordered op list, simulated before posting.** Each spec carries a `simulate()`
  that replays its own ops and prints the ring. Every fold I would have shipped — an insert after the
  wrong index, a chamfer that crossed itself, a bay that took the ground from under a stair — was
  caught on the console instead of in a build. Eight rings reshaped across four boards; two folds
  caught; zero shipped.
- **`relief_scope: "exclude"` and an authored flight.** **Eight** crossings across the four boards, each
  one `height_mode: "level"` with `skirt: 0`, anchors at both ends, a `material` rather than a theme
  and at least twice the run as rise. Every one transected `walked end to end` on its first build.
- **`props.py` as written.** Forty-seven made layers, and the only geometric failures were where two
  of them or one of them and a stamp shared columns. `crenellated_wall` states each merlon from the
  wall's own floor, so `SK9` never fired.
- **A `polyline` for anything that flows.** Sallyport's drystone dyke and Portway's causey are four
  points each and come out as curves.
- **`plan/evaluate` as the iteration loop.** One curl, sub-second, and it answers the two things that
  actually constrain a CTW plan (`WL9` and `WL10`). The quadrangle's plan went through seven
  arrangements in the time one build would have taken.

## 6. The four-team board

**It works, end to end, and the composer is the only thing in the way.**

```
POST /api/plan/evaluate   → score 0, valid true, no violations, no lint
POST /api/plan/compile    → 4 teams: red, blue, yellow, green
GET  …/preflight          → 4 teams · 8 wools · 37 regions · 40 filters · 20 apply-rules
                            buildability: all 12 spawn / wool / monument placements on solid ground
                            traversability: spawn ↔ objective chain connected across the build geometry
                            export gate OPEN
GET  …/coverage           → 14000 reached, 0.0% dead
```

### What it took

1. **Reshape the unit into a quadrant, before flipping the symmetry.** Seed 7's unit spans
   `x −35..30` by `z 10..60` about the origin and walks through its own images when fanned four ways.
   Redrawn strictly inside `x 10..80`, `z 10..90` — the open `+x/+z` quadrant — the four images tile
   and never touch. The arrangement survives the redraw: ring hub with a yard, spawn hung off it, two
   wool spurs, frontline facing the mid. What changes is that a quadrant unit has **two** fronts.
2. **One zone, because `rot_90` maps a cross onto itself.** A single arm, `x −10..10` by `z −60..60`,
   fans into the crossed court. Each team meets it along two faces and has two neighbours across 20
   blocks of void with the third diagonally opposite.
3. **No destroyable and no core** — destroy objectives are order-2 only. CTW, two wools a team,
   eight wools on the board.
4. **`WL9` is the binding constraint, not the symmetry.** The band is [1.031, 1.22] and both wools
   have to sit in a wedge with the spawn in its outer corner. Seven arrangements were evaluated. What
   finally cleared it was a five-block slip beside the walled wool approach: it gives `SP9`'s door
   its fifteen blocks of ground ahead without shortening the walk to the wool behind it.

### What refused, and with which id

| | |
|---|---|
| `GET /api/compose?symmetry=rot_90` | **400** |
| `GET /api/compose?teams=4` | **400** |
| everything downstream | nothing refused |

The only rule that ever fought the four-team plan was `WL9` (`spawn-wool-ratio`, band [1.031, 1.22]),
which refused six of the seven arrangements at 1.227 to 2.933 and is a **soft** term throughout —
`valid` stayed true even at 2.933. `WL2`'s `spawn-wool-distance` fired twice at 15 and 20 blocks when
an arrangement let the spawn lane touch a wool approach directly. Nothing in `SP`, `FR`, `LN`, `CT`,
`BZ`, `G` or `EL` ever complained about the symmetry itself.

### What a four-team composed board would need from the composer

Three things, in the order they bite:

1. **A quadrant body vocabulary.** The composer's boxes — hub, frontline, wool approach, spawn, mid —
   assume one front facing one image. A quadrant has two fronts meeting at an angle, and the corner
   between them is a piece with a role no current kind names. Without that the composer cannot place
   a frontline at all: `FR9` reads a 10-block prong as a funnel, and the natural corner piece on a
   quadrant is exactly 10 × 10 until something tells it to be 15.
2. **A land budget calibrated for four.** `fill-ratio`'s band [0.201, 0.542] is measured over
   two-team boards where each unit's own `rot_180` image interlocks with it. Four quadrant units and
   a crossed court do not interlock — they tile — and the cross itself is a large share of the
   bounding box. This board lands at about 0.43 by land, and I could not tell from outside whether
   that is the right number or a coincidence.
3. **A mid shape that is not a band.** Everything in the composer's mid vocabulary is a band between
   two images. Four teams need a shape that `rot_90` maps onto itself — a cross, a square ring, a
   pinwheel — and whether the stones in it are *mid* stones or *team* transient-links (`CT4`) is a
   different question when there are four teams rather than two.

A fourth, smaller: `tools/board.py` should know `rot_90`, because a quadrant unit's one real failure
mode is colliding with its own images and the grid is where every other relation of that kind is
caught.

## 7. Open gameplay questions I had to decide without an oracle

1. **Is a wool ward with one gate and bedrock on its other two seams fair, or is it a vault?**
   Revetment's two wards each face the fort along three seams; two carry bedrock and the middle one
   is open. Both teams reach the wool through one 10-block gate. I decided that is a gate and not a
   vault, because `PL13`'s own fix text describes the canonical use as a wall on the approach's outer
   interface with both teams meeting at it. But a ward with *no* unwalled seam — which the plan tier
   accepts and `preflight` opens — would be a wool nobody can reach without building, and I do not
   know whether that is a legitimate device or a broken board.
2. **Should a wool a team must bridge to be one of its two, or is that a whole board's idea?**
   Sallyport puts the near wool on an outwork over a 20-block strait reached only by a team-only
   build zone. It makes the two raids genuinely different and it closed the lopsidedness. It also
   means the defence has to bridge to its own objective at the first tick. `CT4` measures the device
   and bands it [0, 2], so one is clearly allowed; whether one should hold an *objective* is not
   something the corpus or the code answers.
3. **How much of a board may be built ground before it stops being a map?** Revetment is 54% made
   ground by theme census and Quadrangle 40%. The brief says solid structural areas are important and
   does not say where the ceiling is. I took 50–60% as the top of the range and gave Portway the
   opposite balance (92% heath, 7% works) so the set spans it.
4. **On a four-team board, whose walk is "the attacker's"?** `plan/flow` reads one attacker against
   one wool. With three enemies the number it prints is one of three pairings and I do not know which.
   Quadrangle's 1.22 is reported as measured and should be read with that caveat.
5. **Is a two-block rail at the head of a stair cover or a hazard?** Revetment's well rails stand
   three blocks from where both flights arrive. A player can scramble over a two-block rail — and
   then falls into the shaft. I kept it, because the rail is what marks the hazard and a player who
   climbs a parapet at a stair head has chosen to; but it is a decision about how a board should
   punish carelessness, which is the author's.

## 8. The method, for the next agent

1. **Pull twelve cards, not one.** `GET /api/compose?seedStart=&count=24` with the SVG discarded is
   one call and gives structure, score and land budget for twenty-four boards. Pick for the *shape*
   you want to work with — a `double-hole` hub is two wells, a `twin` frontline is a breach, a `ring`
   hub is a cloister — rather than for the score.
2. **Pin it, `board.py` it, then throw the rectangles away and keep the arrangement.** The
   composer's contribution is where the hub, the spawn, the wools and the front sit relative to one
   another. Its rectangles are a staircase.
3. **Give every piece a `surface` in the first draft.** Everything downstream — themes, exclusion,
   flights, faces — depends on it, and it costs one line per piece.
4. **Iterate on `POST /plan/evaluate` alone until the score is 0.** It is a sub-second curl and it
   answers `WL9`, `WL10`, `FR9`, `SP9`, `EL1` and `ST8`. Do not build to find out.
5. **Compile once and read the shape ids and the rings off the response.** Write the ring into the
   spec as a constant, write the `editShapes` ops against it, and simulate them in the build script.
   A folded ring costs a build; a printed ring costs nothing.
6. **Check every push against every flight's foot before the first build.** Ring radius plus falloff
   against the distance to the nearest anchored tread. This is the one number that nothing downstream
   reports.
7. **Place nothing by eye.** `POST …/sketch/seats?kind=&width=&depth=` for buildings, `loop.py
   --candidates` for everything else, eight positions a pass.
8. **Expect `level` to land between 0.30 and 0.45 and steer with the push, not the marks.** Under
   0.30 `RL5` fires; over about 0.45 the ground is a table. Marks with treads set the places; the
   push sets the number.
