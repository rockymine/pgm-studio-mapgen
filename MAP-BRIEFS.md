# Map briefs — what to author, and what each board is a test of

"A map of your own design" was asked three times and answered three times with the same map: a roughly square
board, one street of houses behind the spawn, a palette nobody checked, and the objectives placed where the
plan rectangles happened to be. That is not three models failing independently — it is what an open brief
produces, because the fastest defensible answer is always the generic one.

So the briefs are named now. Each one states **what the board is, what it is made of, how it is composed, and
the one thing it is a test of**. What it does not state is geometry: no coordinates, no shape list, no piece
names. The brief is the commission; the board is yours.

## How a run uses this file

**A run authors three maps: the control, plus two named briefs — one CTW and one destroy.**

The **control** (§0) is identical for every run and every model and carries **no art direction at all**. It is
the same brief `docs/tools/mapgen-review.md` has always used, kept verbatim so that boards from different
models and different runs stay directly comparable, and so the effect of everything in `ART-DIRECTION.md` can
be seen by comparing an art-directed board against it. **Do not apply this file's art direction to the
control.** Author it exactly as the brief reads, the way earlier runs did.

The **two named briefs** are yours to pick from §1–§6, one of each mode. Prefer a brief no run has answered
yet; a second answer to an already-answered brief is worth having only if you say in the review what you did
differently. Announce your two choices at the top of your run report before you author anything, so the
reviewer can check the board against the brief it claims.

**Naming.** The folder slug is `<your-run-prefix>-<brief-key>` — `wren-chancel`, `wren-wharf`. The map's own
name, which is what a server shows and what `meta.name` carries, is **yours to invent**: the brief gives the
subject, not the title, and a name that reuses an existing map's is never acceptable.

**Every brief below is subject to `ART-DIRECTION.md`**, which is law rather than suggestion, and every board
is reviewed by a different agent working from `REVIEWER-BRIEF.md`. Where a brief and the art direction seem to
disagree, the art direction wins and the disagreement goes in your report.

---

## §0 — The control (every run, no art direction)

> A destroy board, one connected island, the monument in the open with a forest closing the west flank, a hill
> east that attackers can bridge from, a village behind, a void channel twenty blocks in front.

That is the whole brief and it stays the whole brief. One caveat that is not art direction but law: the
channel is on a destroy board and `approaches.md` has been **amended** — a void hole cut in the middle of a
team's own terrain is withdrawn for `dtm`/`dtc` and replaced by a depression or a pond. The brief says "void
channel twenty blocks in front", so author a channel; what has changed is that it must sit where it separates
the two sides rather than across your own approach, and if you conclude the brief's channel cannot be made to
do that, **build your best reading of it and record the conflict as an open question**. Do not silently
substitute a pond and call it the control.

**Key:** `canonical`.

---

## §1 — Sunk Chancel · DTM

**Key:** `chancel` · **about 100 × 170** — a lane, not a square.

**What it is.** A flooded churchyard on a limestone shelf: pale stone above the waterline, dark waterlogged
stone below it, and one accent of weathered copper-green that appears in three places and nowhere else. The
monument stands in a **drained basin** — ground that has been cut down and left, not cut away — so an attacker
who wants cover comes at it from *below*, over a lip, into a bowl a defender is standing on the rim of.

**The ground.** The identity is a horizontal band: everything above a stated height is bleached and dry,
everything below is dark and wet, and the transition is a real line in the paint rather than a gradient. That
line is what makes the basin read as a basin from any direction. The shelf itself is grown ground with the rim
**off**; the chancel platform and its steps are built ground with the rim **on**.

**The settlement.** Not a village. Three separate structures at three heights and three sizes: a gatehouse on
the shelf edge, a low hall on the flat, and one small isolated building on the far rise with nothing near it.
They may not share a frontage line and they may not all face the same way.

**The composition.** The basin is the *below* approach. Give it exactly one other, and make it a different
dimension — a stand of trees for *through*, or the shelf edge for *above*, not both. A destroy board's spare
space is real and the temptation is to fill it; leave it and put a level change in it instead.

**What it is a test of.** Whether a **depression** does the work the withdrawn void hole used to do. Report
the two ways in, what each costs a player, and whether a defender standing on the rim can watch both.

---

## §2 — Ochre Ladder · DTC

**Key:** `ladder` · **about 80 × 190** — deliberately the narrowest board in the set.

**What it is.** A terraced clay hillside in five steps, warm the whole way — ochre, orange, red-brown, each
terrace a different clay so the steps read as steps from above — with exactly one cold material, a weathered
grey stone, reserved for the stairs and ramps between terraces. Because the only cold thing on the board is
the way up, the routes are legible from anywhere without a single sign or marker.

**The ground.** Elevation is **tiers, not relief**: the five terraces are stated as `base_height` steps with
authored outlines, the way `ruediger.plan.json` does it, and relief is used only for the rough ground at the
foot of the hill. Each terrace's riser is a `layered` wall stack so the face reads as strata rather than as a
painted cliff.

**The objectives.** The core sits in a **sunk yard at the top** of the ladder and the destroyable stands on a
**shelf half way down** — so a team's two goals are at different heights, on different terraces, and 70 or
more blocks apart. That is the shape `basalt-reach` got right and `haiku-dtm-tower` got wrong by 62 blocks.

**The settlement.** Buildings on more than one terrace, and the ones on the upper terrace are visibly smaller
than the ones below — the eye reads that as distance and height at once. No more than four buildings total;
this board's variety is in its ground.

**What it is a test of.** **Goal spacing and board proportion.** Report your own-spawn and enemy-spawn
distances to both goals and the ratio, against the corpus median of 2.9, and the same-team separation against
the 70–75 band.

---

## §3 — Kelp Wharf · CTW

**Key:** `wharf` · **about 150 × 150** — two islands and the water between them.

**What it is.** Two timber wharves facing each other across open water. The built ground is dark: tarred
timber, green-black stone, iron. The natural ground is pale: sand, gravel, dry reed. The split is hard and
deliberate, so on this board *built* and *grown* are two different colours before they are two different
shapes, and a player can tell from a distance which ground someone made.

**The ground.** The two islands sit **15 to 40 blocks apart** and neither touches the other. Each team owns
its island outright, which is the right shape for CTW and is not a defect. If you want a contested middle,
make it a **third** landform in the gap — and it needs the 15-to-40 separation on *both* of its sides, which
is precisely what Weirgate's merged middle did not have.

**The wool approach.** The dock a wool room sits on **attaches to the hub**, not to some piece two joints
away. Read the shapes endpoint for the valid base shapes and how each attaches, and author from that — **do
not run the generator**. Getting the attachment right is also what makes the defence wall possible, because a
dock seated against the hub has a face to wall that is not its own door.

**The defence wall.** Bedrock, spanning the full piece intersection it bars, **10 to 20 blocks wide**, about
**15 blocks in front of** the wool room's entrance, and never on the room's own entry face. Its supply chest
opens the way the room's door faces, so a defender arriving at the door meets it — not into the room it seals.

**What it is a test of.** **The wool approach as a composition**: separation, attachment, the wall, and the
chest. Four things, each of which a shipped board got wrong, and all four are stated above rather than left to
be inferred.

---

## §4 — Winterfold · DTM

**Key:** `winterfold` · **about 90 × 200** — one long lane.

**What it is. A deliberate walk up to the edge of the failure mode.** A snowfield over dark rock, near
monochrome — white, pale grey, near-black — and the *only* colour anywhere on the board is the objective, the
team wool, and one thing you choose. On a white board a red monument reads from anywhere, which is the whole
argument for the restriction.

**The ground.** Because there is no colour to carry legibility, **height has to carry it**. Fold the snowfield
— long, low, tilted surfaces using per-vertex `anchor_heights`, not a bumpy relief — so that what a player
reads as terrain is the shape of the ground rather than its paint. A `layered` riser down every drop is the
one place you may spend a fourth material.

**The settlement.** A run of buildings along one board edge, acting as a boundary rather than as a place, plus
one structure standing alone in the field. **Note a limit honestly:** a building whose interior is filled — a
mass rather than somewhere to walk into — is `B92` and **is not built**, so your edge run is enterable
buildings and your review says so. Do not work around it by stacking props.

**What it is a test of.** **Whether a restricted palette can stay legible**, which is the question
`basalt-reach` failed by accident and this brief asks on purpose. Your review must argue it either way with
`--surface`, `--heightmap` and column probes, and if the board vanishes, **say it vanished** — a run that
proves a restriction does not work is a more useful result than one that quietly adds a fifth colour.

---

## §5 — Gantry Quarter · DTC

**Key:** `gantry` · **about 120 × 160**.

**What it is.** An industrial yard in three material registers that never mix: **brick** for the buildings,
**iron and dark stone** for the machinery and the retaining walls, **pale sand and gravel** for the open yard
between them. Anything built of brick is somewhere a player goes; anything built of iron is something in the
way. That rule holds across the whole board and it is the board's identity.

**The settlement.** This is the one brief that asks for a **grid, and asks for it to be authored by hand.**
Buildings around a square, on shared frontage lines you gave them the same coordinate for, all differing in
**footprint and storey count** while sharing a material — because aspect ratio and height are what the eye
reads first, and six identical footprints in six materials read as a swatch. At least six buildings and no two
of the same size.

**The objectives.** Both goals inside the works, at different heights — one on a raised gantry deck, one in a
sunk pit — and the ground beneath each stated as a shape rather than dressed on afterwards. Keep the 35-block
minimum between them and aim at 70.

**What it is a test of.** **Deliberate placement.** Every one of the twenty-one boards in this repository
placed its buildings by feel; this one is a claim that a grid authored one prop at a time reads better than a
row that happened. Report the coordinates of every building and the line each shares.

---

## §6 — Reedcut · CTW

**Key:** `reedcut` · **about 160 × 140**.

**What it is.** A worked peat lowland: brown and green, low contrast on purpose, and **the legibility comes
from relief rather than from paint**. The cuttings are sunk and wet, the banks between them are raised and
dry, and the difference a player navigates by is where the ground is, not what colour it is. It is the inverse
argument to Winterfold, on a capture board.

**The ground.** Relief does the work on the lowland — this is the one brief where a rolling relief pass is the
right instrument — and every built thing sits inside a `relief_scope: hold` so it stays flat while the ground
moves around it. Without that the relief solves straight through your platform and the wool docks arrive
covered in contour rings. Rims **off** everywhere except the cut faces.

**The water.** A **water lane** is legitimate here and is the one place in this set where it is: a lane is a
gap that becomes bridgeable at 45 minutes, so it can never be what joins two teams' lands, but it can be a
**second approach to a wool that opens late**. If you use one, verify it reaches `map.xml` — a lane authored
on the sketch was silently dropped until `10e031d4`, and `tallow-weirgate` shipped as a different map from its
own specs because of it.

**The settlement.** Buildings on the banks, at bank height, so the settlement is legible as a line of high
ground rather than as a block of houses. One structure down in a cutting, which will read as half-buried, and
that is the point.

**What it is a test of.** **A board that reads by height instead of by colour**, and `relief_scope: hold` used
across a whole board rather than on one shape.

---

## What a brief does not give you, and must not be invented

None of these briefs says how the map **plays**. Where a question about play comes up that
`docs/gameplay/approaches.md` does not settle — whether a team's two goals should differ in difficulty,
whether a channel should be bridgeable, how unequal two ways round may be — **make your best judgement, build
it, and record the question in your report as an open question.** Four boards were built on the same
unexamined answer to the first of those, by three models, none of whom asked. If it is wrong, four boards are
wrong the same way.
