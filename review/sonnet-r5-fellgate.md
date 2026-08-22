# Fellgate Moor — a two-wool moorland lane

> A CTW lane rather than a square: each side's bothy sits off the main track behind a bedrock wall, the
> two flanks climb onto raised peat banks around a ringed hollow, and the mid is crossed by a ford or,
> forty-five minutes in, by a second flooded lane out to the side.

**In one sentence:** a highland sheep-moor whose two hamlets face each other down a heather lane, each
guarding a stone bothy behind a bedrock wall, the two banks either side of the mid hollow topped by
granite tors, crossed by a ford at the centre and a flooded lane out on the flank.

70 × 350 blocks framed (`min_x -35, max_x 35, min_z -175, max_z 175`), `rot_180` about the origin, base
surface 9, 16 players a team. One connected island — the whole authored half is one landmass, fanned
whole onto the mirror image.

## Where the design ideas are

| The identity says | Where it is | Measured |
|---|---|---|
| two-wool CTW | one `<wool>` a team, red and blue | `<gamemode>ctw</gamemode>`; red room `x 10..30, z -130..-110`, blue room mirrored |
| bothy off the main track, behind a wall | `bothy` is a piece branching **east** off `wall-mouth`, not inline on the spine | wall on the `wall-mouth`–`fork` interface, `x -10..10, z -111..-109`, `topY 11` |
| raised banks either side of a ringed hollow | `moor-w`/`moor-e`, two 10-block pieces at surface 11, a 10×32-cell (180-cell) enclosed void between them | column `(-20,-50)`: 13 solid blocks (top ~y11); the void is `PlanVoids`-declared automatically |
| ford at the centre | a build zone straight across the mid | void `z -15..14` at `x=0` (30 columns), `build.areas = [{-10,-15,10,15}]` |
| second lane out on the flank, opens late | a `water-lane` zone east of the ford | `waterLanes.rects = [{20,-15,40,15}, {-40,-15,-20,15}]` |
| granite tors on the banks and the hollow rim | 4 boulders, `outcrop`/`cairn`, mossy stone | `(-20,-50)`, `(20,-50)` on the banks; `(-19,-19)`, `(19,-19)` on the hollow rim |
| a hamlet behind each spawn | 2 small houses south of red's spawn (mirrored north of blue's) | `x -13..-6, z -188..-181` and `x 6..13, z -181..-174` |

## The mistake the loop caught, and what it was

This is the one design decision the board is actually built on, because it was wrong twice before it was
right. The first cut put the wool room **inline** on the spine — `spawn → lane-out → bothy → wall-mouth →
…` — the same shape a plan piece naturally falls into when a room is drawn where the lane happens to be.
It compiled clean, evaluated clean, and refused only at `GET /export`, 409, `EX1`: *"2 objective(s) sit
behind ground an enter rule bars the attacking team from."*

The cause is a real PGM convention neither the plan gate nor the evaluator checks: `WoolGenerator` writes
`enter = not-<owner>` over the wool room's own region, which bars the **defending** team from its own
room (so a defence can never camp inside what it is meant to hold — match-flow.md §4.7's "defenders hold
the wall, attackers get in" is the room's own rule, not a convention). Put the room inline on the
defenders' only road home and that same rule cuts the defenders off from their own frontline. The fix is
topological, not numeric: `bothy` now branches **off** `wall-mouth` rather than sitting on it, so the
defenders' own walk (`spawn → lane-out → wall-mouth → fork → …`) never enters the room at all, while an
attacker crossing the wall can still turn into it. `GET …/traversability` went from `isolated: [wool blue
for red-team, wool red for blue-team]` to `connected: true` with the same wall, the same rooms, the same
theme — only the one piece's position changed.

## What the ground is made of

One theme, `fellgate`, on every shape — a deliberate single-material moor rather than a swatch, since the
board's variety is in height and dressing rather than in paint:

| Bucket | Says |
|---|---|
| rim | cobblestone, depth 1, capped wherever ground drops (`rimEdges: drop`) |
| surface | a two-family noise mix, grass block over coarse dirt, scale 9 — a mottle, not a stripe |
| wall | team-tinted stained clay over a mossy-cobblestone neutral — the one place a "stated colour" belongs |
| fill | stone |

The bothy itself is a light fork of the shipped `alpine mining` preset (cobblestone/stone noise wall,
spruce log-checker banding, gable roof, stair-lattice windows) with its second wall stop swapped from
plain stone to mossy cobblestone, so the byre reads weathered rather than freshly quarried.

## The techniques, and what each one bought

**A ring hub instead of one wide lane.** The first cut of the frontline was a single 20-block-wide piece
from the wall to the mid, and `POST /plan/evaluate` flagged it on both axes at once: `G8` fill-ratio 0.912
(band 0.201–0.496, i.e. almost no void inside the board's own frame) and `LN2` max-chain-length 155 (band
25–110, i.e. one uninterrupted lane with no junction). Splitting it into `fork → {moor-w, moor-e} → hub`
around a 180-cell enclosed void put both back in band (score 0, no violations) and gave the crossing two
legs that part and merge, which `GET …/plan/flow` confirms in prose: *"2 ways in. They part at (0,-160)
and meet again at (-20,75), 45 blocks short of the objective… the defence arrives from behind the
objective while the attack arrives at its front."*

**Coverage read at each redraft, not just at the end.** The first full-length single-lane cut read 46%
dead ground on `plan/flow` before anything was even compiled — almost every block of two side pieces I'd
drawn for flavour was never on any shortest walk between a spawn and a wool. Narrowing the lane to the
corridor's own width and folding the leftover variety into the ring hub (which *is* on a route, in both
directions) brought it to 11% dead at `GET …/coverage`, all of it accounted for by the hollow's unused
corners and the hamlet's own dead-end tail — not by an oversized landform nobody had a reason to walk.

**`observerY` is not a default worth trusting.** The first export placed the spectator platform — a bare
bedrock block — at `(0, 24, 0)`, which is `surface + 15` and sits **inside the ford**, the one crossing
every match uses. `GENERATION-NOTES.md` names the fix; `globals.observerY: 58` moves it clear of the
build ceiling and the traffic both.

## What went wrong

Three things, in the order they were found:

1. **The wool room inline on the spine** — the traversability failure above. Caught by `GET …/export`'s
   409, not by anything upstream; nothing before it reads an `enter` apply-rule.
2. **A flank piece and a knoll that were pure decoration.** The first-drafted board had a west "peat-cut"
   bypass and an east "tor-knoll" vantage, neither of which sat on any shortest route the flow/coverage
   reads compute — 46% of the board's ground was dead by that measure. Cut, and folded into the ring hub
   instead, which the reads do credit.
3. **`iron` beside the wall clearance.** A first iron marker at `[2,1]` on a 20×20 spawn room triggered
   `WX8` — no room size leaves the marker a clear block on every side once the shell and its own clearance
   are taken off a room already at the size cap. Dropped rather than repositioned; a 20×20 room has no
   slack left to give it.

## Coordinates

| Thing | Position | Reading |
|---|---|---|
| red spawn | `(0, 9, -160)` | protection `x -10..10, z -170..-150` |
| red bothy (wool room) | `x 10..30, z -130..-110` | source `(20, 9, -120)`, branches east off `wall-mouth` |
| approach wall, red side | `x -10..10, z -111..-109` | `topY 11`, chests on the min face (facing the attack) |
| red-side bank tors | `(-20, -50)`, `(20, -50)` | outcrop, mossy stone, on `moor-w`/`moor-e` |
| hollow-rim tors | `(-19, -19)`, `(19, -19)` | cairn, mossy cobblestone, either side of the ring void |
| ring void | `x -15..15, z -90..-25` minus the two 10-block banks | 180 enclosed cells, `PlanVoids`-declared |
| mid void, at `x = 0` | `z -15..14` | 30 columns; ford (build zone) `x -10..10, z -15..15` |
| flooded lane, east | `x 20..40, z -15..15` | opens 45 minutes in, mirrored west at `x -40..-20` |
| hamlet houses (red side) | `x -13..-6, z -188..-181`, `x 6..13, z -181..-174` | small footprints south of red's spawn |
| observer | `(0, 58, 0)` | over the mid, clear of the ford and the build cap |
