# Hushwater — decision journal

Append-only. One entry per decision that was mine rather than the studio's or the composer's.

**Entries 1–16 were written late**, in one sitting after the first world built, from the working notes
and the reads quoted in them. Everything from 17 on was written as it happened. Where a number is quoted
it is the number the read actually returned; where I cannot reconstruct what I read, the entry says so.

---

## 1. What the board is about, before any shape
**Chose:** a lead *hush* — two mine heads facing each other across the gill their own water tore out of
the fell. One sentence: *the made ground at the top is flat and stated to be flat, and everything below
it is raw ground at an angle.*
**Because:** the brief's bar is that the board is about one thing and the sentence exists before the
first shape. A hush also gives me a reason for the two grounds to meet — scoured rock at the bottom of a
fall and turf at the top are the same event seen at two ends, so the theme boundary is a fact about the
place rather than a line where two pieces met.
**Read first:** nothing, this was taste. The constraint it had to satisfy came from the warmup: a board
is two or three grounds and every join between them is chosen.
**Studio's part:** none. The studio has no opinion about what a map is of.
**Composer's part:** none — the composer emits no theme, no elevation and no name.

## 2. Which composed board to take
**Chose:** `players=18, teams=2, symmetry=rot_180, cell=4, seed=5` — ring hub, `single` frontline, two
`i` wools, score 0.000.
**Because:** I scanned 48 boards (24 seeds × two symmetries) at micro. Of the score-0 boards this one
had the cleanest lint (one complaint against three on `mirror_z` seed 6) and a **ring** hub, which comes
with a 16 × 16 enclosed yard — a hole players go round, which is the rotation device `CT8` describes and
which I could not have invented as convincingly.
**Read first:** `GET /compose?players=18&teams=2&symmetry=…&seedStart=0&count=24`, twice, then
`POST /plan/evaluate` on five pinned candidates. Seed 5: score 0, one `WL12`. `mirror_z` seed 6: score 0,
three `WL12`. `rot_180` seed 9: `SP9` (spawn door on void) and `CT12` (48-block strait).
**Studio's part:** the refusal surface narrowed the field — I picked from what evaluated clean, not from
what looked good in the SVG.
**Composer's part:** everything about the arrangement. Hub form, frontline form, the number and family of
the wool approaches, the land budget (250 cells against a 226 budget), the 32-block strait.

## 3. Micro means 14–21 players *a team*, and the board does not change inside that
**Chose:** 18.
**Because:** I asked for 14, 16, 18, 20 and 21 and got byte-identical boards at seed 0. The player count
names a size band, not a budget, so 18 is the middle of micro and carries no other meaning. The units are
the trap the brief names: `G8` says *"nano 6–13 players a team, micro 14–21"*, and `maxPlayers` is the cap
the export writes into **every team's** max — so this ships as 18 against 18, not 9 against 9, and the
board's 8864 cells are about 246 blocks² a player against the band's measured 242.
**Read first:** five `GET /compose` calls across the band — identical `unit 192/226 mid 36` on all five.
**Studio's part:** the band table (`G8`) is the studio's; the number 18 is only a label on it.
**Composer's part:** the whole of it — this is the composer's sizing law, not mine.

## 4. Push the whole unit one cell back
**Chose:** every piece +1 cell in z, taking the strait from 32 blocks to 40.
**Because:** I wanted a stone in the gill, and a mid island splits one crossing into two hops. `G5` wants
each hop 10–20 blocks. On a 32-block strait an 8-block-deep island leaves two 12-block hops but is too
thin to fight on; at 40 the island can be 8 deep in two staggered legs and still leave 12 and 20.
**Read first:** `GET /api/rules?rule=G5` — "Void gaps between individual landmasses: 10–20 for the
crossing a route depends on… Lint judges a region's minimal crossing."
**Studio's part:** `G5`'s band is the studio's; it is what made 32 too tight rather than my judgement.
**Composer's part:** the strait itself. The composer chose 32 blocks between the two fanned frontlines and
I moved its ends rather than its idea. **This changed composed geometry.**

## 5. The mid the composer did not emit
**Chose:** two neutral pieces, `shoal-n` (x −16..8, z 0..8) and `shoal-s` (x −8..16, z −8..0), each the
other's `rot_180` image, meeting along z = 0 to make one Z-shaped spoil bank across the gill.
**Because:** seed 5 came with `mid 0` — a bare 40-block gap. The brief says the composer's mid is "one
lateral line at one depth"; a Z is not. The point is that the two hops off each team's own shore are
**different**: 12 blocks on one hand and 20 on the other, and under `rot_180` each team gets the short one
on the opposite hand. That is one cheap contested crossing and one long safe one per side, and it is the
same for both teams.
**Read first:** `POST /plan/inspect` after the edit — `islandGaps … "blocks": 12`, and `G5`'s band.
**Studio's part:** it refused my first arrangement outright — `G5` "gap hop 8 outside 10..20" as a *hard*
violation, score 2000. The 12 is the studio's floor, not my taste.
**Composer's part:** the mid *band* is the composer's — the `mid-band` zone rect and the fact that a
crossing belongs between the two fanned frontlines. **I added to it; I did not move it**, except to widen
it from z ±16 to z ±20 so it still docks both shores after entry 4.

## 6. A height ladder, because a flat plan cannot be painted
**Chose:** a surface per piece, falling from the spawn at the back to the shoal in the gill.
**Because:** a *flat* composed plan compiles to one merged polygon plus one subtract, and a theme is
stated on a shape — so a flat board can carry exactly one theme. Stating a surface per piece ends the
merge and gives one polygon per distinct height, which is the only way a composed board can be painted in
more than one theme.
**Read first:** `GENERATION-NOTES.md` — *"A flat composed plan compiles to one merged polygon and a
subtract"* and *"Heights first, then paint."* Confirmed by compiling: 6 plateaus came back where one had
been.
**Studio's part:** the merge rule, and `SK27`, which later complained that my six plateaus carried three
paints — see entry 18.
**Composer's part:** the composer states no elevation at all (`globals.surface` 9, no piece carries a
`surface`). **This is purely added.**

## 7. Which ground is made and which is grown
**Chose:** the made ground — the mine head, the spawn, the walled lane — is `relief_scope: "exclude"`;
everything else stays in the relief solve.
**Because:** `exclude` takes a footprint out of the solve so the two tiers meet at a **face**, and the
face is where a flight goes. `hold` lets the relief bring the lower ground up to the shape and then there
is no step and no reason for a stair. The board's sentence is that the made ground is flat *and stated to
be flat*.
**Read first:** `pgm-studio/docs/world-export/relief.md` §11 — the inherit/hold/exclude table, and
"An excluded shape is stamped back at its own height after the solve".
**Studio's part:** the three-word vocabulary, and the fact that a shape declaring a `height_mode` is not
asked the question at all.
**Composer's part:** none — there is no relief on a composed board to scope.

## 8. The west wool is open and the east wool is walled
**Chose:** `wool-a` keeps a 16-block mouth onto the ring's west arm with no wall; `wool-b` becomes a lane
leaving the ring's east nose through a 16-block mouth that carries the board's one `walls` entry.
**Because:** the composer gave both wools the same character. One wall on one interface is what the brief
allows, and putting it on one of two otherwise-alike approaches is what makes them two approaches: one
long and exposed across moor, one short and prepared behind bedrock. It also decides where the defence
spends its time.
**Read first:** `GET /api/rules?rule=ST8` — "the interface a wall bars is a 10–20 block lane mouth… and
the wall stands about 15 blocks in front of the wool room's entrance." My mouth is 16 blocks and the room
entrance is 16 blocks past it. `/plan/inspect` returned the stamped rect:
`minX 35, minZ 60, maxX 37, maxZ 76, floor 0, top 21` — two thick, 16 long, five courses above the lane.
**Studio's part:** `ST8`'s band and `PL11`/`PL13`'s refusals decided that the wall had to go on a real
land interface that is not the room's own.
**Composer's part:** `"walls": []`, always. **Purely added** — but the *interface* it stands on is the
composer's wool-b seam, moved outward (entry 9).

## 9. The ring grows an east nose so the wall cannot be walked round
**Chose:** `hub-t1` and `hub-t2` shortened to x −16..24; `hub-t4` pushed out to x 16..36, so the east arm
protrudes 12 blocks past its neighbours and the wool-b lane leaves from the end of a nose.
**Because:** in the composed ring all four arms present a flush face at the same x. A wall across a spur
leaving a flush face is bypassed by a 2–3 block diagonal bridge from the arm beside it — the wall is then
only in the way of someone who chooses to walk into it. With the nose, the shortest bypass is about 15
blocks of open bridging beside a wall the defence is standing on.
**Read first:** the composed grid from `tools/board.py` — hub-t1, hub-t2 and hub-t4 all ending at cell
x 8. `GENERATION-NOTES.md`: "Count the ways round the thing before counting the walls."
**Studio's part:** nothing. No gate measures a way round a wall; this is the `PC-C` corner case read by
eye off the grid.
**Composer's part:** the ring, its four arms and its enclosed yard are the composer's `ring` hub.
**I changed two of the four arms' extents.** The yard survived at 16 × 16 and I did not touch it.

## 10. Both wool rooms get an apron
**Chose:** `wool-a-apron` and `wool-b-apron`, one cell each, against the far face of each room.
**Because:** a stamped wool room fills its piece and fills *downward in bedrock to y 0*, so every side of
it that faces void is a bedrock cliff as tall as the ground is high. Composed, each room had three such
sides. An apron takes it to two — and two faces on void is what the author's ruling says a wool room
wants anyway: it sits in a corner, the defence holds two lines, the attack picks between two.
**Read first:** `GENERATION-NOTES.md`, *"A wool room's foundation is bedrock to y 0, so it needs land on
all four sides"* — the measured column under `opus5-thornfell`'s room: floor y25, bedrock y24 to y0.
**Studio's part:** nothing warns about this at any tier. It is visible in the world and nowhere else.
**Composer's part:** the rooms' positions and sizes are the composer's `i` wool family. **I added ground
beside them and did not move them relative to their spurs.**

## 11. The intra-team build zone: the bing
**Chose:** a 16 × 12 pad (`bing`) off the mine head's east side, joined to team ground by two build zones
and to nothing by land — one onto the mine head, one onto the walled lane *behind* the wall.
**Because:** a bedrock approach wall bars the defence as well as the attack, so the team that owns the
wool behind it needs a way in that is not the gate. That is `BZ5`'s defender-egress bridge and `CT4`'s
team transient-link in one object: every zone touching it touches only one team's islands. It also gives
wool-b a second approach, which is the `WL8` variant `CT8` calls hole-mediated.
**Read first:** `GET /api/rules?rule=CT4` — "a stone whose every interfacing zone component touches only
one team's islands is a **team transient-link**, not a mid stone", measured as `team-stepping-count`,
band [0, 2].
**Studio's part:** it refused my first two placements. `G2` "zone 'staithe-link-e' corridor width 8 < 10"
and `G5` "gap hop 8 outside 10..20" were both **hard** violations at score 2000 — the 12-block minimum
plank and the 12-block minimum hop are the studio's numbers, not mine.
**Composer's part:** none. The composer models exactly one zone, the mid band. **Purely added.**

## 12. Where the bing did *not* go
**Chose:** not on the west flank between the frontline and the west spur, which is where I first drew it.
**Because:** a pad there is reachable through its own zones by *anyone*, and zones are not team-restricted.
The route frontline → pad → west spur → wool-a skips the hub entirely, which is the strongest defensive
ground on the board. A transient link has to be behind the defence or it is a shortcut for the attack.
**Read first:** nothing — I walked the route on the grid and saw it. This was reasoning, not a read.
**Studio's part:** nothing would have caught it. `CT4`'s definition is about which islands the zones
touch, not about who may cross.
**Composer's part:** none.

## 13. Three themes, and what each one is
**Chose:** `moor` (the fell, map default, finished on the **slope** axis), `floor` (the made ground: laid
cobble and stone brick with a `wallRun` retaining face), `hush` (the scour: washed gravel and bare rock).
**Because:** three is what the brief says a map has, and each of mine is a *place* rather than a piece.
The third one is the board's subject: the same washed ground appears at the top of the fall as a scar on
the bank and at the bottom as the shore the crossing lands on and the spoil bank standing in the gill, so
the eye joins the two ends of one event.
**Read first:** the `AUTHORING-BRIEF.md` painting section — "Three themes is a map"; "A voronoi is never
ground… it belongs in the fill, and it is made of stone"; "A pattern takes two blocks, not a family."
Every pattern I wrote carries two members, and the only sampled body is in the `fill`.
**Studio's part:** `PT4` refused four of my shapes outright — a `cell` material used as a shape's fill
samples the plane only and reads as vertical stripes unless it states a `rise`. That is the studio
deciding the shape of my patterns, not me.
**Composer's part:** none.

## 14. Extreme hills, chosen before the patterns
**Chose:** biome 3.
**Because:** grass, leaves and water take their colour from the chunk's biome byte and nothing else does,
so the biome is a palette decision. `Extreme hills` tints grass `#8ab689`, a grey-green that agrees with
the stone beside it; `Plains` at `#91bd59` reads as a lawn on a moor.
**Read first:** `GET /api/terrain/biomes` — the full hex table.
**Studio's part:** the table. The studio answers what each biome tints and refuses nothing here.
**Composer's part:** none.

## 15. No iron
**Chose:** dropped the iron marker I had added.
**Because:** `ST2` wants an iron marker's whole cube inside a **spawn-role** piece; `WX8` wants it outside
the room shell with two blocks of clear air; `WX1` makes the shell that piece inset one block on every
side. On a plan-compiled spawn those three cannot all hold — there is a one-block ring and the cube needs
three. Rather than grow the spawn region past `ST10`'s cap to chase it, I left it out.
**Read first:** `POST /plan/evaluate` → `ST2` "the iron cube at (0,96) does not stand inside a spawn
piece"; then after moving it, `WX8` "the cube needs its 3×3 footprint inside the piece and 2 blocks of
clear air to the shell, and the room keeps the footprint it was given".
**Studio's part:** all of it — two refusals in series narrowed this to "not on this kind of board".
**Composer's part:** the composer emitted `"iron": []`. It was right and I was wrong to add one.

## 16. The spawn moves to the centre line
**Chose:** `spawn-room` from cells x 2..6 to x −2..2, so the spawn point sits at x 0.
**Because:** the composed spawn sits east of centre, which makes the east wool the near one for the
defence and the west wool the near one for the *attack*. With two wools on opposite flanks a centred
spawn makes the defence's two rotations equal and the attacker's two raids equal. The usual warning
against a centred objective — a board reading dead on the flanks — does not apply, because the two wools
are the journeys and they fan.
**Read first:** straight-line distances computed off the cell rects before the move (enemy spawn → wool-a
174, → wool-b 188, ratio 1.08) and after (179 / 184, ratio 1.03).
**Studio's part:** `WL9` (spawn↔wool balance) and `WL2` are the terms this is measured by; both were
silent before and after, so this was mine to improve rather than the studio's to demand.
**Composer's part:** the spawn's *piece* and its position on the hub's back arm are the composer's.
**I moved it 16 blocks west along its own arm.**

---

## 17. The first built board reads grey, and the cause is the split rather than the band cuts
**Chose:** put the hub ring's three lower arms **back into the relief solve** and paint them `moor`,
leaving only the mine head, the spawn, the walled lane and the bing as made `floor`.
**Because:** `05-themes.txt` on build 1 read **floor 50.5% · moor 35.6% · hush 13.8%**. Half the board
was stated as made stone *by me* — the whole hub ring was excluded from the solve and themed `floor`.
No band cut can make a board green when 64% of it is stated to be grey ground. The ring around a shaft
is worked ground, not a paved floor; the mine head is the paved part and it is one piece.
**Read first:** `renders/05-themes.txt` (the three shares above) and
`GET …/incline?format=text` → `00-09° 71% · 10-19° 20.5% · 20-29° 4.6% · 30-39° 2.3% · 40-49° 1% ·
50-59° 0.5%`, 2216 sampled cells. My bands cut at 14° and 26°, which put ~79% of the *moor* into the turf
band — so the moor that existed was already green, and there simply was not enough of it.
**Studio's part:** `SK27` said the same thing from the other side — "component 'frontline-t1' compiles to
6 plateaus from surface 13 to 19 and they state 3 different paints… one landform with a hard line at
every riser, where a theme is a place."
**Composer's part:** none of this is the composer's. The composer's board is flat and unpainted; the grey
was entirely mine.

## 18. Cut the slope bands where the histogram is, not where they look right
**Chose:** bands at **0–10°**, **10–20°**, **20°+**, after re-reading `incline` on the revised relief.
**Because:** the histogram's own boundaries are at ten-degree steps and the population falls off a cliff
after 19°. A first cut at 14° puts the whole 10–19° population — a fifth of the ground — into the turf
band with the flat, so the shoulder never appears and the board reads as two materials. Cutting at 10
makes the shoulder the fifth of the ground it actually is.
**Read first:** `GET …/incline?format=text`, before and after the relief change; the numbers are in
`composed-vs-adapted.md`.
**Studio's part:** the `slope` band axis itself, and the fact that a thickness on it is a span of degrees.
**Composer's part:** none.

## 19. More fall on the bank, so there is ground at an angle at all
**Chose:** the wash pinned at 11 and the ring's yard at 17 — a six-block fall over the bank's sixteen
blocks, where build 1 had three.
**Because:** 71% of build 1's ground stood under 10°. A board whose ground is three-quarters flat has
nothing for a slope axis to say. Six over sixteen is about 21°, which puts the bank in the shoulder and
rock bands and gives the gully sides something to cut into.
**Read first:** the incline histogram above, and `03-slopes.txt` — `8598 walked, 134 scrambled, 132
barrier`, which says the board was walkable everywhere and therefore shapeless.
**Studio's part:** `RL5` is the gate on the other side of this (level share under 30% is a board with
nowhere to stand); I have to keep the flat ground the yard and the made floors give.
**Composer's part:** none.

## 20. The bing's hop to the mine head goes to sixteen blocks
**Chose:** moved the bing from x 36..52 to x 40..56, taking the mine-head hop from 12 blocks to 16 and
leaving the lane hop at 12.
**Because:** the sixteen-block floor is for a bay touching a goal or a spawn, and `/plan/inspect` listed
`wool-b-room` and `spawn-room` among that space's walls. `WL12` does not *ask* a space a build zone
covers, and both of my hops are stated crossings under their own planks — but the one that could be
widened without breaking `G5`'s 10–20 band or `G2`'s corridor width should be.
**Read first:** `POST /plan/inspect` → `{"kind": "bay", "cells": 76, "narrowestBlocks": 12, "between":
["bing", "hub-t1"], "walls": ["wool-b-room", "bing", "wool-b-t1", "hub-t4", "hub-t1", "spawn-room",
"spawn-t1"]}`, and `GET /api/rules?rule=WL12`.
**Studio's part:** the geometry refuses the other half — the lane's north edge and the mine head's north
edge are sixteen blocks apart, so a pad sixteen from the lane has only four blocks of facing left for the
mine head, which `G2` then refuses at corridor width. Twelve on that plank is the studio's floor, not a
compromise I chose.
**Composer's part:** none.

## 21. The rooms stop being made of the ground they stand on
**Chose:** forked `showcase-hall` and `showcase-cage` into `tools/styles/hw-minehouse.json` and
`hw-assay.json` — spruce boarding over a course of laid spruce log, spruce posts and beams, a brick
roof with dark-oak verges, and the footing set back to null.
**Because:** both presets are walled in cobblestone, stone brick and andesite, which is the ground's own
family on this board — a stone building on stone, which the brief names as the hard thing to get right
and not the one to attempt. Timber is the other family, and a mine's buildings are timber anyway.
**Read first:** `POST /room-styles/preview-snapshot?format=png&view=section` on the fork — a two-storey
spruce shell with a brick roof and a dark beam course, warm against grey. And the two presets' own JSON:
`wall` bands of `98:0`, `4:0`, `1:5`.
**Studio's part:** `HS4` refused the first fork outright — *"beams are dark oak and post is spruce. A
post, the beam ends docking against it and the course they are the ends of are one frame, so they are cut
from one wood."* The studio decided the beams' material for me. `HS7` is why the footing went to null.
**Composer's part:** none — the composer emits no room style.

## 22. The east flight was cutting a trench, so it moved to where the ground actually steps
**Chose:** deleted the flight at x 14..22 and put one at x 3..11 running from the shore at 11 up to 17,
fourteen of run for six of rise.
**Because:** I authored two flights up the bank before the ground existed to measure, and a flight's
anchor is an absolute height the relief knows nothing about. The transect at x 18 read
`(18,32) 20 · (18,33) 15 DROP -5` — the east bank is higher than the yard it was supposed to climb to,
because the `knowe` mark and the `brow` push put it there, so the flight was a five-block trench cut
across a knoll. The west bank does step: `(8,21) scramble +2` and `(8,31) scramble +2` on the main
landing route, which is exactly what a flight is for.
**Read first:** `GET …/transect?points=18,26;18,52` and `points=8,19;8,40`, quoted above. Board-wide, the
move took `03-slopes` from `132 barrier, 8 faces, largest 44` to **`54 barrier, 6 faces, largest 16`**.
**Studio's part:** nothing refused the trench. `EL1` and `WL11` walk the plan flat and cannot see an
authored flight at all; the transect is the only thing that saw it.
**Composer's part:** none.

## 23. The wall bars the defence too, and the bing is the answer to that
**Chose:** left the bedrock wall across the only land way into wool-b, and let the bing's south plank
land *behind* it.
**Because:** a `walls` entry is bedrock with no door, so it costs the team that owns the wool as much as
the team raiding it. Measured, the defence pays 3 placed blocks to reach its own east wool against 4 to
reach the west one — the wall is a real cost to both sides and the plank is how the defence pays it
cheaply if it has thought ahead. That is what makes the wall a prepared line rather than damage.
**Read first:** `04-routes.txt` — `spawn-red -> orange-0: 73 blocks, 3 placed` against
`spawn-red -> red-0: 68 blocks, 4 placed`, and `barrier +4 at (35, 74)`, which is the wall.
**Studio's part:** `ST8`'s 10–20 block lane mouth and ~15 blocks in front of the room decided where the
wall could stand; `PL11` and `PL13` decided which pair it could name.
**Composer's part:** `"walls": []`. The wall is added; the *interface* it stands on is the composer's
wool-b seam, moved 12 blocks east so the ring's east nose protrudes past its neighbours.

## 24. The sky wool over each room is the studio's, and I checked before filing it
**Chose:** nothing — left it alone.
**Because:** the column at the wool read `y 58/57/56 Red Wool` with 30 courses of air under it, which
looks exactly like a stray write. It is `GoalMarkerStamper`: a 3³ wool cube stamped
`BuildCeiling.MarkerOver` = 5 blocks over the build cap, deliberately out of reach so nobody can bury or
grief it, one per fanned goal. The board's cap is y51, so the marker is y56–58.
**Read first:** `GET …/column?at=-46,68`, then `GET …/render/section?axis=z&at=-46`, then
`pgm-studio/src/PgmStudio.Minecraft/Stamping/GoalMarkerStamper.cs`. Three boards in `specs/` read
`top 21..23` at their wools, which is what made it look anomalous — their build caps are lower.
**Studio's part:** the whole of it. This is a feature, and a gap filed against it would have been the
third wrong capability claim in this repository's history.
**Composer's part:** none.

## 25. The bing is dead ground on the flow read and it stays
**Chose:** kept the bing, knowing `plan/flow` calls 144 of its 192 blocks "off every route".
**Because:** the flow read walks *land* routes between the places the board has. A team transient-link is
by definition not on one — it is a pad reached only over its own team's build zones, which is what makes
it a lane an attacker cannot flank. Reading it as dead ground is reading the instrument as damage. The
built read agrees the board is fine: `coverage` says 1.6% dead, 146 cells of 8864.
**Read first:** `01-flow.txt` — *"144 blocks at (-48, -96) — bing (144)"* — against
`GET …/coverage` — `reached 8718 · dead 146 · 1.6%`.
**Studio's part:** neither read refuses on this; both are measurements. The disagreement between them is
the honest answer and I am recording it rather than choosing one.
**Composer's part:** none — the composer models no intra-team zone at all.

## 26. Where the buildings went was the studio's answer, not mine
**Chose:** the store at the mine head's north-east corner, `[[17, 85], [23, 91]]`, and the powder house
on the west spur, `[[-31, 60], [-25, 64]]`.
**Because:** I picked the head's *centre* first, which is where a whim house belongs over a shaft, and it
was refused twice — once for standing in the spawn door's approach and once for leaving under eight
blocks of way past it on two sides. A 16-deep strip cannot hold a 5-deep building anywhere but against
its own edge, which is arithmetic rather than taste.
**Read first:** `POST …/sketch/seats?kind=house&width=7&depth=5` — 396 seats over the whole board, as a
raster — then `loop.py`, three passes: `DR-KEEP building 'whim' stands on (-7,-81), which is kept clear
as the approach in front of a door`; `DR-PASS … a side has fewer than 8 blocks of passable ground`;
`DR-SITE … has no ground under (18, 92)`, which is how I learned the head's last land row is z 91.
**Studio's part:** all of it. Every one of the seven first-pass declines carried a rule and a coordinate,
and `--candidates` answered eight alternative rock positions in one pass.
**Composer's part:** none.

## 27. A dam on the mine head, because the board is called Hushwater
**Chose:** a `pool` water prop on the head's flat made ground, with the launder polyline leaving its east
edge — and then moved it eight blocks west when it turned out to sit in the spawn's own door lane.
**Because:** a hush is water let go down a fellside, and the board had no water in it at all. The head is
`exclude`d flat ground at a known height, which is the one place on this board a prop that *carves* its
own bed can be given a level with confidence.
**Read first:** the first placement preview said `placed 14, declined 0` — and then `04-routes.txt` read
`ROUTE (0,104) -> (46,-68): 206 blocks, 55 placed, 3 drops, worst drop 10` against **30 placed** on its
own mirror. A pond is an obstacle a walk routes round, and only the walk read saw it. Moved west, all four
raids read `206 / 211 / 204 / 211 blocks, 30 placed` — symmetric again.
**Studio's part:** the water prop carves its own band rather than finding a level, so the pan *is* the
pool and `radius`/`depth`/`level` are the whole of it. The dressing pass placed it without complaint; the
route read is what refused it, and nothing refuses on a route read.
**Composer's part:** none.

## 28. The observer platform was sitting on the one piece of ground both teams fight over
**Chose:** `globals.observerY: 32`, up from the derived 27.
**Because:** a board whose ground crosses the origin gets a bedrock observer platform in its middle, and
this board's middle is the crown of the spoil bank in the gill — the contested stone. At the derived
height it caps the island thirteen blocks up. At 32 it is eighteen clear of the crown and still a sensible
place to watch from.
**Read first:** `GET …/column?at=0,0` — `y 32 Bedrock` over `y 14 Coarse Dirt`, and the long section
`world-section-x0.txt`, which draws the platform directly over the shoal's mound.
**Studio's part:** the default, `surface + 15`, and the fact that the platform exists at all.
**Composer's part:** none.

## 29. The chimney went on the bing, because a made layer is ground to everything downstream
**Chose:** a `tapered_tower` off `tools/sculpt/props.py` at `(48, 94)` on the bing, `kind: "made"`,
`part_of: "chimney"`, `mirrors: true`, five polygons on one layer, in brick and stone brick rather than
in the dressing floor's own material.
**Because:** the board had no vertical landmark, and on a board whose two halves are rotations of each
other a stack is what tells a player which end they are looking at. I put it beside the engine house at
the mine head first, and the defence's own walk to its east wool went from **3 placed** to **30 placed,
worst drop 13** — everything downstream of a stacked cell reads one number, the surface top, so the walk
climbed the chimney and fell off it. The bing is the one piece of ground no land route passes, which is
what makes it the right plinth.
**Read first:** `04-routes.txt` before and after — `ROUTE (0,104) -> (56,70): 73 blocks, 30 placed,
worst drop 13` against `73 blocks, 3 placed, 0 drops`. Nothing else saw it: the store answered 200, the
export gate stayed OPEN, and `03-slopes` did not move.
**Studio's part:** `kind: "made"` is what keeps `SK10`'s pair walk and `SK11`'s reachability walk off a
solid, and `GENERATION-NOTES.md` is what told me the builder defaults `mirrors` to **False** — right for a
landmark on the symmetry centre, and on a team's own ground it means one side simply has no chimney, with
nothing anywhere reporting it.
**Composer's part:** none. The composer has no storeys at all.
