# Map briefs — what to author, and what each board is a test of

"A map of your own design" was asked three times and answered three times with the same map: a roughly square
board, one street of houses behind the spawn, a palette nobody checked, no path anywhere, and the objectives
placed where the plan rectangles happened to be. That is not three models failing independently — it is what an
open brief produces, because the fastest defensible answer is always the generic one.

So the briefs are named, and they are **literal**. Each states the tone families to build from, the house style
to start from, the routes to draw as paths, how its landforms meet, and the one thing it is a test of. What
none of them states is geometry: no coordinates, no shape list, no piece names. The brief is the commission;
the board is yours.

**Two of the eight exist because they have never been attempted at all.** There has never been a desert map in
this repository, and never a four-team board — and both are fully expressible: `HousePresets.Desert` is a
worked desert style, and `rot_90` fans an orbit to order 4 with `PlanCompiler` carrying a red/blue/yellow/green
slot palette and three four-team seeds already in `seed-stats.md`.

## How a run uses this file

**A run authors three maps: the control, plus two named briefs — one CTW and one destroy.**

The **control** (§0) is identical for every run and every model and carries **no art direction at all**. It is
the brief `docs/tools/mapgen-review.md` has always used, kept verbatim so boards from different models stay
directly comparable and so the effect of everything in `ART-DIRECTION.md` can be seen against it. **Do not
apply this file's art direction to the control.**

The **two named briefs** are yours to pick from §1–§8. Prefer one no run has answered; a second answer is worth
having only if you say what you did differently. Announce both at the top of your run report before you author
anything, so the reviewer can check the board against the brief it claims.

**Naming.** The folder slug is `<your-run-prefix>-<brief-key>`. The map's own name — what a server shows, what
`meta.name` carries — is **yours to invent**: the brief gives the subject, not the title, and a name that
reuses an existing map's is never acceptable.

**Every brief is subject to `ART-DIRECTION.md`**, which is law, and every board is reviewed by a different
agent working from `REVIEWER-BRIEF.md`. Where a brief and the art direction seem to disagree, the art direction
wins and the disagreement goes in your report.

---

## §0 — The control (every run, no art direction)

> A destroy board, one connected island, the monument in the open with a forest closing the west flank, a hill
> east that attackers can bridge from, a village behind, a void channel twenty blocks in front.

That is the whole brief and it stays the whole brief. One caveat that is law rather than art direction:
`approaches.md` has been **amended**, and a void hole cut in the middle of a team's own terrain is withdrawn
for `dtm`/`dtc` in favour of a depression or a pond. The brief says "void channel twenty blocks in front", so
author a channel — what has changed is that it must sit where it separates the two sides rather than across
your own approach. If you conclude the brief's channel cannot be made to do that, **build your best reading and
record the conflict as an open question.** Do not silently substitute a pond and call it the control.

**Key:** `canonical`.

---

## §1 — Caravanserai · DTM · *never attempted*

**Key:** `caravanserai` · **about 90 × 190** — a lane.

**What it is.** A waterless canyon in red rock, with a walled caravan stop at the head of it. There has never
been a desert map here and the system has a worked desert style waiting.

**The palette, literally.** Ground from **`rust`** — Red Sand and Red Sandstone, two members, no more — with
**`sand`** for the canyon floor where the rock gives out: Sand and Smooth Sandstone. Four blocks across two
families and that is the whole terrain. The accent is **End Stone**, which lives in `sand` and reads almost
white against red: use it for the caravanserai's own courses and for nothing else on the board.

**The buildings.** Start from **`HousePresets.Desert`** and read it before you change anything: end stone over
sandstone in a two-band `RoomPart`, a Brick gable, a birch stair lattice, **`Sill = Air`** — a building with no
footing, which is the one preset that models the rule twelve boards broke. Fork it by **proportion**: the
caravanserai is one long low block, the outbuildings are small and square, and none of them changes material.

**The ground.** The canyon is a `sink` with `anchor_heights` so its floor **tilts** along its length — a wadi
runs downhill or it is a trench. Its walls are a `layered` riser through Red Sandstone, Smooth Red Sandstone and
Sandstone, so the face reads as strata. **The rim is off** on the open desert and **on** at the canyon lip,
because that lip is an edge somebody's eye should catch.

**The paths.** Two, drawn before anything else: the caravan road from the spawn along the canyon floor to the
caravanserai, and a goat track climbing the canyon wall to the rim. `tapered` edges, and the road wider than
the track. Everything the road crosses stays clear of props.

**What it is a test of.** **A desert, and a preset used as a starting point rather than reinvented.** Report
which fields of `Desert` you changed and why, and whether the two-family ground reads as one desert or as two.

---

## §2 — Compass Yard · CTW · four teams · *never attempted*

**Key:** `compass` · **about 170 × 170**, square on purpose — this is the one brief where square is correct.

**What it is.** Four teams under `rot_90`, each owning one quadrant of a walled yard, with a shared centre none
of them owns. No four-team board has been authored here and the machinery is all present: `rot_90` fans an
orbit to order 4, `PlanCompiler` carries the red/blue/yellow/green slot palette, and `seed-stats.md` records
three four-team seeds.

**The palette, literally.** The ground is deliberately neutral so four team colours can sit on it: **`ash`** —
Clay and Smooth Stone — with **`cobble`** — Gravel and Cobblestone — for the worked ground. Four blocks, low
contrast, no accent in the terrain at all. **The accent is the teams**, and it is the only place a shade row
belongs: each quadrant carries its team's Stained Clay on the built ground of its own approach, and nowhere
else. A player should be able to tell whose quarter they are standing in without looking up.

**The composition.** One quadrant is authored and `rot_90` fans it — so **every decision you make is made four
times**, which is what makes this brief hard. Get the wool approach right once. The centre is the contested
ground and belongs to nobody; the four gaps between quadrants are the separation, and each wants the 15-to-40
rule applied to it independently.

**The buildings.** One structure per quadrant, identical under the rotation — this is the one board where
identical buildings are correct, because the symmetry is the point. Make that one building good.

**The paths.** One route per quadrant, spawn → its own wool → the centre, fanned by the rotation. Because the
board is square and symmetric, a path is the only thing that will tell a player which way is out.

**What it is a test of.** **Whether four teams work at all**, end to end: the orbit, the team palette, the
separation on four gaps instead of one, and whether the export writes four teams correctly. Report anything the
pipeline does at order 4 that it does not do at order 2 — that is the whole value of this board.

---

## §3 — Sunk Chancel · DTM

**Key:** `chancel` · **about 100 × 170**.

**What it is.** A flooded churchyard on a limestone shelf. The monument stands in a **drained basin** — ground
cut down and left, not cut away — so an attacker wanting cover comes at it from *below*, over a lip, into a
bowl a defender stands on the rim of.

**The palette, literally.** **`pale stone`** above the waterline — Diorite and Mushroom Stem — and **`slate`**
below it — Cyan Stained Clay and Grey Wool. The identity is a **horizontal band**: everything above a stated
height is bleached, everything below is dark, and the transition is a real line in the paint rather than a
gradient, which is what makes the basin read as a basin from any direction. One accent of **Prismarine** from
`turquoise`, in three places and nowhere else.

**The ground.** The shelf is grown ground, **rim off**. The chancel platform and its steps are built ground,
**rim on**. The basin is a `sink` with a `skirt` so its lip ramps into the shelf instead of stepping off it —
and its floor tilts, so the far rim sits above the near one and you look *into* it.

**The buildings.** Three structures at three heights and three sizes, and **not a village**: a gatehouse on the
shelf edge, a low hall on the flat, and one small building alone on the far rise with bare ground around it.
They may not share a frontage line and may not all face the same way. Start from `HousePresets.Counting` for
the gatehouse and fork by proportion.

**The paths.** Spawn → the basin rim, and the rim → the hall. The second one should visibly stop at the lip:
a path that ends where the ground drops is a decision a player can read.

**What it is a test of.** **Whether a depression does the work the withdrawn void hole used to do.** Report the
two ways in, what each costs a player, and whether a defender on the rim can watch both.

---

## §4 — Ochre Ladder · DTC

**Key:** `ladder` · **about 80 × 190** — the narrowest board in the set.

**What it is.** A terraced clay hillside in five steps, warm the whole way, with exactly one cold material —
reserved for the ways up. Because the only cold thing on the board is the route, the routes are legible from
anywhere without a marker.

**The palette, literally.** **`rust`** and **`brick`**, two members each: Orange Stained Clay and Red Sandstone
for the terraces, Granite and Hardened Clay for the worked faces. The cold accent is **Polished Andesite** from
`grey stone`, used **only** on stairs, ramps and the treads between terraces.

**The ground.** Elevation is **tiers, not relief** — five `base_height` steps with authored outlines, the way
`ruediger.plan.json` does it — and relief is used only on the rough ground at the foot of the hill. Each riser
is a `layered` wall stack so the face reads as strata. Where a terrace meets the rough ground, it meets it
along a **skirt**: this brief has five chances to leave a flat pad butted against a slope, and it is the fault
being tested for.

**The objectives.** The core sits in a **sunk yard at the top** of the ladder; the destroyable stands on a
**shelf half way down**. Different heights, different terraces, **70 or more blocks apart** — the shape
`basalt-reach` got right and `haiku-dtm-tower` missed by 62.

**The buildings.** Four at most, on more than one terrace, and the ones above visibly smaller than the ones
below — the eye reads that as height and distance at once. This board's variety is in its ground.

**The paths.** The zigzag up the ladder, drawn as one path with `tapered` edges that narrow where it climbs.

**What it is a test of.** **Goal spacing, board proportion, and whether terraces flow.** Report both distances
and the ratio against `GO1`'s authored band of 3.0–4.0 (scored by `goal-spawn-ratio`), the same-team separation against the 70–75 band, and a section
through two terrace joins.

---

## §5 — Kelp Wharf · CTW

**Key:** `wharf` · **about 150 × 150** — two islands and the water between them.

**What it is.** Two timber wharves facing each other across open water. Built ground is dark, natural ground is
pale, and the split is hard: on this board *built* and *grown* are two different colours before they are two
different shapes.

**The palette, literally.** Built from **`dark`** — Nether Brick and Dark Oak-dark tones — and **`loam`** —
Dark Oak Planks and Podzol. Natural from **`sand`** — Sand and Birch Planks — and **`cobble`** — Gravel and
Mossy Cobblestone. Four blocks a side, and the two sides never mix.

**The ground.** The islands sit **15 to 40 blocks apart** and neither touches the other. Each team owns its
island outright, which is right for CTW and is not a defect. A contested middle is welcome as a **third**
landform in the gap, with the 15-to-40 gap on *both* its sides — precisely what Weirgate's merged middle did
not have.

**The wool approach, stated because four boards got it wrong.** The dock a wool room sits on **attaches to the
hub**, not to a piece two joints away — read the shapes endpoint for the valid base shapes and how each
attaches, and author from that. **Do not run the generator.** The defence wall is bedrock, spans the full piece
intersection it bars, is **10 to 20 wide**, stands about **15 blocks in front of** the room's entrance, and is
never on the room's own entry face. Its supply chest opens the way the door faces, so a defender arriving at the
door meets it — not into the room it seals.

**The paths.** Along each wharf, from the spawn to the dock head. A jetty is a path over ground; draw it.

**What it is a test of.** **The wool approach as a composition** — separation, attachment, wall, chest. Four
things, each of which a shipped board got wrong, all four stated here rather than left to be inferred.

---

## §6 — Winterfold · DTM

**Key:** `winterfold` · **about 90 × 200**.

**What it is. A deliberate walk up to the edge of the failure mode.** A snowfield over dark rock, and the
*only* colour anywhere is the objective, the team wool, and one thing you choose. On a white board a red
monument reads from anywhere, which is the whole argument for the restriction.

**The palette, literally.** **`bright`** — Snow Block and Quartz Block — over **`ice`** — Ice and Packed Ice —
with **`dark`** for the rock beneath: Black Stained Clay and Coal Block. Six blocks, three families, no accent
in the terrain.

**The ground.** With no colour to carry legibility, **height carries it.** Fold the snowfield with long, low
tilted surfaces using per-vertex `anchor_heights` — not a bumpy relief — so what a player reads as terrain is
its shape. **The rim is off everywhere**; a rim on a relief-solved snowfield terraces it into contour lines,
and on this palette that would be the only thing anyone saw. A `layered` riser down each drop is the one place
to spend a fourth material.

**The buildings.** A run along one board edge acting as a boundary, plus **one structure alone in the field**.
Note the limit honestly: a building whose interior is *filled* — a mass rather than a place — is **`B92` and is
not built**, so the edge run is enterable buildings and your review says so. Do not work around it with props.

**The paths.** One, from the spawn to the monument, in the dark rock showing through the snow. On this board a
path is the only ground that is not white, which makes it the strongest single mark available.

**What it is a test of.** **Whether a restricted palette stays legible** — the question `basalt-reach` failed
by accident and this asks on purpose. Argue it either way with `--surface`, `--heightmap` and column probes,
and **if the board vanishes, say it vanished.** A run proving a restriction does not work is more useful than
one quietly adding a fifth colour.

---

## §7 — Gantry Quarter · DTC

**Key:** `gantry` · **about 120 × 160**.

**What it is.** An industrial yard in three registers that never mix: **brick** for the buildings, **iron and
dark stone** for the machinery and retaining walls, **pale gravel** for the open yard. Anything brick is
somewhere a player goes; anything iron is something in the way. That rule holds across the whole board and it
is the board's identity.

**The palette, literally.** **`brick`** — Bricks and Hardened Clay — for the buildings. **`grey stone`** —
Stone Bricks and Iron Ore — for the works. **`ash`** — Clay and Smooth Stone — for the yard. Two members each.

**The buildings.** The one brief that asks for a **grid, authored by hand.** Buildings around a square, on
shared frontage lines you gave them the same coordinate for, all differing in **footprint and storey count**
while sharing a material — because aspect ratio and height are what the eye reads first. At least six, no two
the same size. Start from `HousePresets.Workshop` and `Counting` and fork by proportion, not by palette.

**The ground.** Both goals inside the works, at different heights — one on a raised gantry deck, one in a sunk
pit — each stated as a shape rather than dressed on afterwards, and each meeting the yard along a skirt or a
built retaining wall with the rim **on**. Keep 35 minimum between the goals and aim at 70.

**The paths.** The yard's own circulation: spawn → square → each goal. This is the board where paths are most
obviously right, because a works has roads.

**What it is a test of.** **Deliberate placement.** Twenty-one boards placed buildings by feel; this one claims
a grid authored one prop at a time reads better than a row that happened. Report every building's coordinates
and the line each shares.

---

## §8 — Reedcut · CTW

**Key:** `reedcut` · **about 160 × 140**.

**What it is.** A worked peat lowland: brown and green, low contrast on purpose, and **legibility comes from
relief rather than paint.** The cuttings are sunk and wet, the banks between them raised and dry, and the
difference a player navigates by is where the ground is, not what colour it is. The inverse argument to
Winterfold, on a capture board.

**The palette, literally.** **`loam`** — Podzol and Brown Stained Clay — for the cuttings, **`dirt`** — Coarse
Dirt and Spruce Planks — for the banks, and **`verdant`** — Grass Block and Green Stained Clay — for the dry
tops. Grass goes at `thickness: 1` on top of a `layered` stack and **nowhere below it**; this brief walks
straight past the rule four boards broke, so it is the one to get right.

**The ground.** Relief does the work on the lowland — the one brief where a rolling relief pass is the right
instrument — and every built thing sits inside a `relief_scope: hold` so it stays flat while the ground moves.
Without it the relief solves through your platform and the docks arrive covered in contour rings. **Rims off
everywhere except the cut faces**, which are edges somebody made.

**The water.** A **water lane** is legitimate here and this is the one place in the set where it is: a lane
becomes bridgeable at 45 minutes, so it can never join two teams' lands, but it can be a **second approach to a
wool that opens late.** If you use one, **verify it reaches `map.xml`** — a lane authored on the sketch was
silently dropped until `10e031d4`, and `tallow-weirgate` shipped as a different map from its own specs.

**The buildings.** On the banks, at bank height, so the settlement reads as a line of high ground rather than a
block of houses. One structure down in a cutting, which will read as half-buried — that is the point.

**The paths.** Along the bank tops, between cuttings. On rolling ground a path is also the flattest thing on
the board, which is a navigational fact a player will use.

**What it is a test of.** **A board that reads by height instead of by colour**, and `relief_scope: hold` used
across a whole board rather than on one shape.

---

## What a brief does not give you, and must not be invented

None of these says how the map **plays**. Where a question about play comes up that
`docs/gameplay/approaches.md` does not settle — whether a team's two goals should differ in difficulty, whether
a channel should be bridgeable, how unequal two ways round may be — **make your best judgement, build it, and
record the question in your report as an open question.** Four boards were built on the same unexamined answer
to the first of those, by three models, none of whom asked. If it is wrong, four boards are wrong the same way.
