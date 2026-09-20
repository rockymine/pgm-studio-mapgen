# Whitegape — decision journal

Append-only. One entry per decision that was actually mine.

## 1. What the board is about
**Chose:** One sentence — *a limestone gorge quarried from both rims; each team's monument stands on the
floor of its own pit, and the only way across is a bridge the attackers build.* Everything else on the board
has to be a consequence of that: the pit, the haul ramp, the tramway incline, the loading dock at the lip and
the lime kiln standing on it.
**Because:** The warmup is blunt that a board needs one thing it is about, written down before anything is
made. A gorge gives me the author's ruling for a destroy board for free — "air between the two sides, joined
by a build zone over void" — and a quarry gives me a reason for every height change on the map, so the relief
has a story instead of being noise with a gradient in it.
**Read first:** `AUTHORING-BRIEF.md` §3 — "One objective, and air between the two sides… the two teams'
ground is joined by a build zone over void spanning the board's whole width, never by a land connection"
(marked as the author's ruling, and that both halves of it were wrong in the brief's own first test board).
**Studio's part:** Nothing yet. This was mine, inside the ruling.

## 2. Two teams, 14 a side
**Chose:** `maxPlayers: 14`, two teams, 28 players total.
**Because:** I wanted the gorge lip defensible but not sealed. 64 blocks of lip against 14 defenders is
~4.5 blocks a player — too thin to wall, which is the point of a bridging board: you react to where the
bridge goes rather than holding a line.
**Read first:** `openapi.json` → `PlanGlobals.maxPlayers`: *"How many players the board is sized for **per
team** — the cap the export writes into every team's max, so a board's total is this times the n…"*. Two
prior runs shipped a 48 v 48 map by reading it as the board's cap; I read the field description before
picking a number.
**Studio's part:** Team count is not mine at all — destroyables take two teams, the task states it as the
author's ruling, and the intent fans one authored unit under `rot_180`.

## 3. The board's five numbers, solved from the goal rules before any shape existed
**Chose:** lane 176 blocks spawn-to-spawn along z; board 64 wide (x −32..31) × 200 long (z −100..99);
void gap 23 blocks (z −12..10); monument 42 blocks from its own spawn, 10 blocks off the centre line.
**Because:** `GO1` (ratio 3–4), `GO3` (goals ≥85 apart) and `GO4` (goal ≥40 from its own spawn) have a common
solution only above a certain lane length, so I solved for it rather than drawing a board and hoping.
With `d` the goal's distance from its own spawn and `L` the spawn separation: `GO4` gives `d ≥ 40`,
`GO1` gives `d ≤ L/4`, so `L ≥ 160`; `GO3` gives `L − 2d ≥ 85`. `L = 176, d = 42` satisfies all three with
room (ratio ≈ 3.2, goals ≈ 99 apart).
**Read first:** `AUTHORING-BRIEF.md` §3 — "`GO1` is solvable before a shape exists… the ratio is about
`(L − d) / d`" — and `GENERATION-NOTES.md` "On half a box the three goal bands cannot all hold at the plan
tier", which is the same arithmetic failing on a 130 × 120 board.
**Studio's part:** The bands themselves, and `/plan/inspect` will be the judge — my arithmetic is Euclidean
and the plan tier walks a piece graph.

## 4. The monument 10 blocks off the centre line, and the spawn on the same side
**Chose:** monument at (−10, −50); spawn hall centred near (−12, −92) — both west of centre.
**Because:** Coverage. Putting spawn and goal on the *same* side keeps the own-side defensive walk short
(so `GO1` survives) while pushing both off the centre line; the attack walk is then the long diagonal from
one side's west to the other side's east, and under `rot_180` the two teams use opposite flanks. A board with
both on the centre line uses a 20-block strip and lets the flanks rot.
**Read first:** `pgm-board` §4 — a destroy board with its monument on the centre line read **62.0% dead**;
moving it twelve blocks off and taking ten off the width took it to **17.9%** with nothing else changed.
**Studio's part:** `GET …/coverage` will say whether this worked; nothing refuses on it.

## 5. The quarry cut with `height_mode: sink`, not with relief marks
**Chose:** The pit is one `addShapes` polygon, `height_mode: "sink"`, `skirt: 1`, uniform depth, sitting on a
flat pad the relief pins at 23. Two authored ramps in, each `height_mode: "level"` with `anchor_heights`.
**Because:** My first plan was nested `area` marks at 18 and 12. That builds a *funnel*, not a quarry: with
`reach: 0` every unpinned cell is the relaxation between the marks, so the moor grades smoothly down into the
pit over tens of blocks and the cut stops reading as a cut. A `sink` leaves the field alone and cuts sheer.
**Read first:** `GENERATION-NOTES.md` — "`height_mode: sink` is a quarry, and its anchors are its depth…
`sink` with `skirt: 1` cuts sheer faces and a flat floor — measured, a lift of 6 on flat y11 ground gives a
clean 6-block drop to y5 and back", plus the warning that a *tilted* ring "turns the whole shallow half into
a bowl and the cut stops reading as a cut".
**Studio's part:** It refuses to let me have both — the note also says that without a way in the floor is a
**stranded walkable place** that only `relief/read`'s `places` share reports. That is why both ramps are
authored rather than notched into the ring.

## 6. Two ways into the pit, not one
**Chose:** a haul ramp from the spawn side (defenders') and a tramway incline from the gorge side
(attackers'), both at least 2:1 run-to-rise.
**Because:** A goal with one entrance is a choke the defence holds for free, and a goal with one entrance on
the *attacker's* side is a goal the defence cannot hold at all. Two entrances on opposite sides is the
decision I wanted the match to have. The 2:1 is not taste.
**Read first:** `GENERATION-NOTES.md` "Three things nothing checks about a placed building" — the measured
table: 1:1 gives a worst step of 2 blocks and does not walk; 2:1 and 3:1 give worst step 1 and do.
**Studio's part:** Nothing yet — `EL1`/`WL11` walk the plan's pieces flat and cannot see an authored flight
at all, so this is mine to prove with a transect.

## 7. PL4 — the spawn piece cannot sit inside the fell piece
**Chose:** tiled the fell into three rectangles around the spawn piece (`fell`, `fell-w`, `fell-e`) instead
of one big rectangle with the spawn drawn on top of it.
**Because:** I had copied the overlap from `opus5-millrace`, where the spawn piece sits inside the main
piece — but there both are at the same surface, and mine were 4 apart.
**Read first:** the refusal itself, then `GET /api/rules?rule=PL4`: *"Two pieces claim the same ground at
incompatible heights… a step between them wants two pieces that meet at an edge, not two that overlap."*
**Studio's part:** entirely the studio's. `PL4` is a hard violation and it named both pieces and the delta.
**Refusal log:** `PL4` (refusal, hard) — fixed by tiling.

## 8. SP8/SP9 — the spawn shelf came down from 4 steps to 1, and the door turned round
**Chose:** `head` surface 25 against the fell's 24, a single step; `facing: "back"` so the player arrives
looking down the board rather than off its back edge.
**Because:** I wanted a spawn on a shelf and the lint said the shelf was a wall. Rather than argue with it I
moved the drama: the board now *falls* from the spawn (25) through the pad (22) to the lip (21) and the dock
(17), so the spawn is still the high ground and the fall is the relief's rather than the plan's.
**Read first:** `GET /api/rules?rule=SP8` — *"A spawn's egress steps by 1 level or takes a ramp: a seam at
Δ≥2 ahead of the door is un-walkable bare"* — and `SP9`, *"A spawn door stands ≥15 blocks from bare void,
measured along the door's own line."* With `facing: "front"` (−z) the door looked at the board's back edge:
`spawn door on 'head' faces void 0 blocks out`.
**Studio's part:** both. `facing` is a direction only — the doors themselves come from what the piece
touches, which is not something I get to state.
**Refusal log:** `SP8` (complaint), `SP9` (complaint) — both cleared.

## 9. dead-share 0.198 — accepted, with the measurement I will hold it to
**Chose:** narrowed the board from 64 to 56 wide and raised `maxPlayers` from 14 to 20, then **accepted**
`G8 dead-share 0.198` against its band of [0, 0.12].
**Because:** I first read this as a refusal and went looking for the shape that would clear it. It is a
*soft* term, and when I evaluated the eight shipped destroy boards in `specs/` against the same endpoint,
**every one of them** was outside the band: braidwater-ford 0.366, mossgill 0.417, dustwath 0.411,
blackden-sough 0.279, millrace 0.249, grykefell 0.217, brackenfold 0.179. Mine at 0.198 is second best of
the nine and scores 1.29 where the others score 1.6 to 5.4. A board with one objective and one spawn a side
has two journeys, and the flanks are on neither — that is structural, not a defect I can draw out.
The width change was not wasted: 64 → 56 took it 0.219 → 0.198, and 56 × 88 = 4,928 blocks a team is
**246 a player at 20**, which is `G8`'s own measured law (~250 blocks² a player, 331 corpus maps).
**Read first:** `POST /plan/evaluate` on my plan and on eight others; `GET /api/rules/terms` —
`dead-share`, rule `G8`, **kind `soft`**, band [0, 0.120438], source `envelope`; and `G8`'s own prose for
the land-per-player law.
**Studio's part:** it set the player count for me, in effect. I picked 14 by feel; the land budget says 20.
**Open question:** whether a bridging DTM *should* be held to a wool board's dead-share envelope at all.
I decided it should not, and I will check the real answer with `GET …/coverage` on the built world rather
than argue from the plan-tier proxy.

## 10. The ground finished by angle, and where the bands cut
**Chose:** the ground theme's surface is a `layered` stack on the **slope** axis, cut at 16° and 34°:
meadow (grass over coarse dirt over dirt), worn shoulder (a cell of coarse dirt and gravel over dirt),
bare rock (a cell of stone and andesite). One `layered` depth stack — stone, diorite, stone, andesite,
stone, diorite, repeating — is the `wall` bucket of every theme on the board, so the gorge walls, the
quarry faces and the cut banks are the same limestone beds in the same order.
**Read first:** `GET …/incline?format=text`. My first cuts were 20°/36° and the distribution said that
made the board two thirds meadow: 36.2% of the ground under 10°, 27% from 10 to 19, 15% from 20 to 29,
11.2% from 30 to 39, 10.6% at 40 or steeper. Cutting at 16 and 34 splits it about half meadow, a quarter
shoulder, a fifth rock. Verified in the world: `column (-20, -13)` on the gorge lip reads grass / coarse
dirt / dirt and then stone·2, diorite, stone·3, andesite, stone·4, diorite — the beds, on the cliff.
**Studio's part:** the 34° band edge became the studio's own threshold for `DR-STEEP` — its refusals
quote "the theme painting that cell calls the ground a face from 36°", reading *my* band edge back at me.
The theme decides what counts as a face, and then the dressing pass enforces it.

## 11. The east knott was a wall, and the boulders are what said so
**Chose:** softened the push from amount 8 / falloff 9 / crown 8 to amount 5 / falloff 14 / crown 4.
**Because:** three of five boulders were declined `DR-STEEP` at 56°, 53° and 37°. I had checked the two
gradients agreed with each other (8/9 outside against 8/8 inside) and never checked what the number *was*:
0.89 courses a block is 42°, and a 42° hillside is a cliff with grass on it. The fixed pair is 5/14 = 20°
outside against 4/8 = 27° inside. Board-wide: scramble 712 → 304 cells, barrier 1061 → 969, and the share
of ground at 40° or steeper fell from 16.5% to 10.6%.
**Read first:** the three `DR-STEEP` declines with their measured angles, then `GET …/incline?format=text`
before and after.
**Studio's part:** all of it. `GENERATION-NOTES.md`'s range rule made me check that the gradients agreed;
the studio's own declines made me check what they agreed *on*.
**Refusal log:** `DR-STEEP` ×3 (decline) — fixed by softening the landform, not by moving the rocks.

## 12. Sixteen dressing declines, and the instrument that ended them
**Chose:** placed every prop by reading `06-claims.txt` and then testing sites with
`loop.py --candidates`, eight to twelve at a time, instead of choosing coordinates by eye.
**Because:** my first pass put every prop where the map looked empty to me, and the pass declined 16 of
them — door approaches, a keep-out round the ramps, a road standoff, one boulder claiming eight blocks in
every direction, one tree with 64 of its 424 blocks inside a hillside. The claims raster shows the whole
board as one character per block; the candidate loop says whether a given prop actually seats there.
Four passes took it from 16 declines to 0, and none of them cost a build.
**Read first:** `06-claims.txt`, then `loop.py --candidates` — ten sites a pass, twenty seconds a pass.
**Studio's part:** every decline was the studio telling me something I could not see, with coordinates.
**Refusal log:** `DR-PASS` ×1, `DR-STEEP` ×3, `DR-KEEP` ×6, `DR-CLAIM` ×4, `DR-ROAD` ×2, `DR-SITE` ×2,
`DR-CUT` ×2 (complaint) — all cleared.

## 13. PT4 — a cell pattern used as a shape's whole material needs a rise
**Chose:** gave `HARDCORE` (the ramps' and flights' material) `rise: 4` and the drystone wall `rise: 2`.
**Because:** a shape's `material` stands in for every bucket including `fill`, and a field sampled in the
plane alone makes every block of a column resolve alike.
**Read first:** the refusal: five `PT4`s at 400, one per shape, each naming its own JSON path
(`layers.ground.shapes.haul-ramp.material.fill.rise`).
**Studio's part:** the studio's, and it refused the whole store rather than building striped ramps.
**Refusal log:** `PT4` ×5 (refusal, 400) — fixed.

## 14. This pass was directed by the repository's author, not by my own reading
**Chose:** to stop and rework the board against six rulings handed down after the first complete build:
(1) the outline is a literal square and must be deformed; (2) there is no separation between natural and
structural ground, which is the biggest miss; (3) too much relief piled in one place; (4) the houses are
far too small and use none of the multi-wing model; (5) stone boulders are seated on stone; (6) use the
seats read and the candidate loop rather than my eye.
**Because:** these are rulings from the human oracle, not suggestions, and four of the six are things no
gate in the studio raises. The board had passed every gate it has — `valid: true`, export gate OPEN, zero
dressing declines, coverage inside its band — and was still wrong in ways only a person could say. That is
the whole point of the oracle: the studio can tell me a boulder has no ground under it, and cannot tell me
that a boulder on stone reads as nothing.
**Read first:** nothing — this arrived as a judgement on the built board. The one item I *could* have
caught myself is (5): `DR-SITE` asks whether there is ground under a prop, not what that ground is made
of, so a `column` read per boulder was always available to me and I never took it.
**Studio's part:** none, and that is the finding. The studio raises no rule for any of the six.

## 15. The natural half and the made half, and the line between them
**Chose:** the back of the board (z -100..-64) is grown ground — relief only, no authored shape on it
except two roads — and the front (z -64..-12) is made ground: one level stone yard with the quarry pit
sunk into it, a loading dock cut five courses lower at the lip, and the works shed and kiln on them. The
boundary is the yard's own retaining face, with two flights let into it.
**Because:** the author's ruling. The board's first build treated the whole map as one undifferentiated
terrain with a pit in it; the split makes the two halves look like different kinds of place and gives the
journey from spawn to objective a line to cross.
**Read first:** nothing of mine — this was a ruling. What I read afterwards was `sketch/relief/read` and the
`incline` distribution, to see what taking the front half out of the solve did to the rest.
**Studio's part:** `relief_scope: "exclude"` is the whole mechanism — it takes the yard's footprint out of
the solve so the two tiers meet at a face instead of being graded into each other, and it is the difference
between a terrace and a ramp.

## 16. The outline was a literal square
**Chose:** fourteen `editShapes` ops on the compiled ring `fell-24` — four inserted points on each flank,
six along the lip, and three corners moved — then one `bendShapes` pass at `wander 2.5, step 11, side: out`.
**Because:** the author's first words about the board. The compiler emits the plan's rectangles, which is
the board's shape and not its coast.
**Read first:** the compiled ring itself, out of `opus5-whitegape.layout.json` — eight vertices, three of
them long straight runs. That is what a bend needs to know: an edge with room for fewer than two cuts is
left straight, so the spawn notch (16 blocks at step 11) comes out as the plan drew it.
**Studio's part:** the choice of `side`. `out` only bloats, which is what lets the yard and the dock keep
their ground: a coast that moved inward would have left the dock's front edge hanging over void. The lip is
cut only outside the dock's own span, so the made edge is straight and the grown edge is not — which turned
out to be the cheapest way to say the two halves are different kinds of place.

## 17. Boulders on stone, which nothing in the studio refuses
**Chose:** `column`-read every boulder site before using it, and moved all four onto grass or coarse dirt.
**Because:** the author's ruling, and the one item of the six I could have caught myself. The measured
answer: (18,-70) andesite, (2,-66) stone, (20,-58) gravel, (24,-86) andesite — all legal seats, all of them
a stone boulder standing on stone. The four that shipped read `Grass Block` or `Coarse Dirt`.
**Read first:** `GET …/column?at=x,z`, once per candidate, beside `POST …/sketch/seats?kind=boulder`.
**Studio's part:** `DR-SITE` asks whether there is ground under a prop, not what that ground is, and
`DR-STEEP` asks the angle rather than the block. Nothing in the studio reads what a prop stands on.

## 18. `sketch/seats` — the read that answers forwards
**Chose:** placed both buildings and every prop from `POST …/sketch/seats`, asked of a board with no props
on it at all, instead of guessing and reading the declines.
**Because:** the author's ruling, and it immediately found something I would never have found by guessing:
**a 15x14 house seated nowhere on the board**, and neither did an 8x8 except in one small patch. The cause
was mine — I had marked the entire yard `keepClear: true`, which makes the whole made half a dressing
keep-out, so no building could stand on the ground I built for it. With that off, a 15x14 seats in exactly
one place on this half (minimum corner x 2..5, z -58..-52) and that is where the works shed stands.
**Read first:** `POST …/sketch/seats?kind=house&width=15&depth=14&format=text` — one raster, the whole
board, the answer read as coordinates rather than eyeballed.
**Studio's part:** all of it. The five declines only ever answer backwards; this one runs the same
predicates forwards. It is the single most useful call I made on this board.
