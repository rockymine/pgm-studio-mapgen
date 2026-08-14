# Sonnet Briarlock — a CTW map of my own design

Two wools a team, symmetric `rot_180`, 24 players. Built to test the arrangement
`docs/gameplay/match-flow.md` §3.3/§9.1 names as canonical and rare at once: **spawn at the back,
wools flanking left and right** (27% of the corpus, the lower-imbalance shape) rather than the lopsided
73% majority, with the defending spawn already interposed between its own two wools by construction
rather than by a rule someone remembered to apply.

## The board

264×340. Spawn (raised platform, surface 11) sits on the centre axis at the back of each team's
territory. A shared "home" field connects it to two wool arms, one east one west, each a short
corridor into a walled room. In front of home, two frontline legs flank a **40-block enclosed void** —
`docs/gameplay/match-flow.md` §3.2: a two-legged frontline with a void between its legs is the single
largest source of routing options in the corpus (97% of objectives behind one have more than one
attack route, against 38% behind a plain bar). Past the legs, a 140×100 mid gap separates the two
teams' land entirely; a build zone covers it edge to edge, so the sky-bridge fight described in
match-flow §4.4–§4.6 has one clear place to start from.

| Piece | How |
|---|---|
| Spawn | surface 11, raised 2 over the field, two iron markers |
| Wool arms | a 4-cell corridor into an 8×6 wool room, one each side |
| Defence wall | `walls` on the home/corridor interface, both arms — bedrock, 2 thick, 3 courses (y9–11) |
| Frontline void | two 6×8 legs either side of a 40-block gap, undrawn so it declares itself | 
| Hub | a gentle relief `push` (+3, crown 2) under home, so the centre reads as a low rise rather than dead flat |
| Mid | one build zone, x −70..70 by z −50..50, the map's only crossable void |

## Techniques used

**A defence wall on the sole approach, and reading its own traversability refusal correctly.**
`--traversability-map` reports 4 isolated points — the four wool markers. `FINDINGS.md` (this
repository, ClayClay Redux) already diagnosed the identical reading: a full-width wall only three
courses tall is not a barrier the ground-connectivity model understands as "step over," and the
corpus's own walls stand exactly this way — built over rather than walked around
(`docs/gameplay/match-flow.md` §4.3: "the pre-placed wall stops ground rushers and tunnellers, who
must surface to cross it"). I read this as the traversability check doing what it says it does — modelling
ground-level, headroom-limited walking — rather than as a fault in the board, and left the wall as
designed rather than widening or lowering it to clear a warning that a real CTW wall is supposed to
trip.

**A void that declares itself.** The 40-block gap between the two frontline legs was never drawn as a
`buffer` or a `subtract` — `PlanVoids.Declare` runs on every compile and adds one automatically over
any enclosed space no piece covers, so leaving that rectangle empty in the plan was the whole of
authoring it.

**Team-tinted stone in the wall bucket.** `briarlock`'s wall is a `wallRun` of a `teamTint` band over
mossy cobblestone, so the riser at every drop — the frontline void, the true void edge behind each wool
— reads in the standing team's own colour without a second theme.

**A `roomStyles.cage` bound explicitly, so the wool cages are not the built-in bedrock lid.**
`library.md`: an unbound room stamps "a bedrock lid"; I bound one storey of mossy cobble under a
team-tinted band, `Flat` roof, no pitch, so a wool room reads as a low bunker rather than a slab.

## What went wrong

Nothing new — map 1's two findings (`kind` must be a prop's first JSON key; every enum field needs its
literal PascalCase C# name, not the camelCase the docs show) applied here identically and were fixed on
the first attempt once known. The one map-specific miss: an early `hub-rise` push (amount 3) inside the
`home-bench` area mark's own footprint solved to only +2 rather than the expected +3–5, for a reason I
did not chase down given the time this run had left — accepted as a gentler central rise than planned,
which is not a wrong shape for a combat hub, just a smaller one than authored.

## Open gameplay question, decided without an oracle

**Where exactly should a defence wall stand relative to its wool room?** `match-flow.md` §6.2 measures
real maps' walls at a median 13 blocks out from the room face, standing on a bedrock line the map
itself supplies; the corpus-derived convention is "out from the room," not "at the room's mouth."
`approaches.md` does not give a rule for the distance, only that the wall exists to give the defence "a
prepared line to hold." I placed both walls at the home/corridor interface — the corridor's outer
mouth, roughly 20 blocks out from the room's own face — rather than flush against the room, which reads
closer to the corpus convention than the alternative. I recorded this as a judgement call rather than
a derived fact, since nothing in the read documents settles the exact number.

## Coordinates, for checking in-game

| What | World position | Note |
|---|---|---|
| Red spawn | (0, 11, −165) | facing +Z |
| Red wool "red" (east) | room 90..130 × −130..−100 | defence wall at x 69..71, topY 11 |
| Red wool "orange" (west) | room −130..−90 × −130..−100 | defence wall at x −71..−69, topY 11 |
| Frontline void | x −40..40, z −90..−50 | no ground, no build zone — permanent |
| Mid build zone | x −70..70, z −50..50 | the map's only crossing |
| Traversability isolation | all four wool markers | expected — see above |
