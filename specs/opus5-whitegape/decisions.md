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
