# Run B — four boards, combining relief modes

Agent B of a two-agent run of eight. Four boards, each about one thing, each built by combining a
push for the landform, marks for the ground that has to agree with something, and `height_mode`
shapes for what people built. Written down together before a shape was authored, because the
failure mode is four internally-coherent boards that are all grey:

> **`opus5-goldbank-quarry`** — Ground that people cut away: the whole board is one worked quarry,
> and both destroyables stand on the floor of it, under everybody.
>
> **`opus5-lynchet-brow`** — A hillside farmed into terraces, where every fight is about getting up
> or down exactly one retaining wall.
>
> **`opus5-scoriafell`** — One mountain between two valleys, and the pass over it is the whole map.
>
> **`opus5-braidwater-ford`** — A wide braided river, and the two sides meet at three fords and
> nowhere else.

Checked across the four rather than within each: **warm pale** limestone · **green** pasture over
drystone · **black** volcanic ash and scoria · **ochre-brown** floodplain silt. Every board's ground
theme is finished on the **slope** axis, so a board's tone is its rock and its angle rather than its
plan pieces.

## The drill

Predictions written down before any check, with the caveat that Agent A's brief had already
disclosed `opus5-millrace`'s two numbers, so only its face count was a genuine prediction.

| board | scramble% pred/act | barrier% pred/act | faces pred/act |
|---|---|---|---|
| `opus5-alderfen` | 9.0 / **14.1** (−5.1) | 2.5 / **5.1** (−2.6) | 40 / **20** |
| `fable-mossgill` | 7.0 / **3.6** (+3.4) | 7.0 / **7.1** (−0.1) | 55 / **14** |
| `opus5-millrace` | *disclosed* | *disclosed* | 30 / **20** |

Two of four inside the 3-point band, both outside 8. The errors are informative in three ways.

**I over-corrected on scramble because I had read Agent A's errors first.** They were 3.9–7.1 points
high on all three; I shaded down and went 5.1 points *low* on Alderfen. Reading another agent's bias
is not the same as having a model, and the right answer would have been to read the heightmap again
rather than to apply a correction.

**A gradual lettered rim scrambles more than it looks.** Alderfen's rims descend one band per
two-block character, which reads gentle and accumulates to 14.1%.

**Faces are few, and I was 2–4× high on all three — the same error as Agent A.** A board carries
14–20 faces, not 40–60, because barrier clumps into a handful of large walls (largest 114, 243 and
694 cells) rather than scattering. That is the single most useful thing the drill taught me, and it
held on all four of my own boards: 12 to 20 faces each.

**Scramble and barrier are near-independent.** Millrace is 0.9% scramble with 8.0% barrier because a
water/land wall has no intermediate angle. That prediction transferred directly — my quarry's first
build came out 0.55% scramble with 7.47% barrier for exactly the same reason, and I recognised it as
too sheer from the numbers rather than from a picture.

## The four boards, measured

All four export with the gate OPEN and `symErr 0`. `03-slopes` percentages are of that board's
ground cells; `coverage` is the read nothing refuses on and nobody takes.

| | `goldbank-quarry` | `lynchet-brow` | `scoriafell` | `braidwater-ford` |
|---|---|---|---|---|
| mode | destroy | core | capture → destroy | destroy |
| size (blocks) | 104 × 224 | 104 × 208 | 104 × 208 | 104 × 224 |
| walked | 21,136 | 19,051 | 17,505 | 21,467 |
| scrambled | 828 (3.6%) | 558 (2.6%) | **2,923 (13.5%)** | 807 (3.5%) |
| barrier | 1,332 (5.7%) | **2,023 (9.4%)** | 1,204 (5.6%) | 1,022 (4.4%) |
| faces | 20 | 17 | 20 | 20 |
| relief low–high | 26–32 | 19–36 | **8–66** | 13–41 |
| themes | 48.7 / 37.6 / 13.8 | 56.0 / 32.8 / 11.2 | 83.9 / 14.9 / 1.1 | 80.2 / 16.3 / 3.4 |
| `GO1` ratio | 3.37 | 3.13 | 3.74 | 3.34 |
| declined props | 0 | 0 | 0 | 4 (`DR-BANK`, below) |
| `symErr` | 0 | 0 | 0 | 0 |
| gate | OPEN | OPEN | OPEN | OPEN |

The scramble/barrier spread is the run's own evidence that the four boards are different ground: a
mountain is 13.5% scramble, a board of retaining walls is 9.4% barrier with almost no scramble, and
a floodplain is nearly flat with its barrier concentrated in two river banks.

**Coverage**, taken on all four because nothing refuses on it and so nobody runs it:

| | reached | decorated | dead | route |
|---|---|---|---|---|
| `goldbank-quarry` | 55.7% | 11.5% | **30.6%** | 2.2% |
| `lynchet-brow` | 56.1% | 15.3% | **26.2%** | 2.5% |
| `scoriafell` | 63.8% | 11.8% | **22.1%** | 2.4% |
| `braidwater-ford` | 58.9% | 9.8% | **28.8%** | 2.5% |

For scale, the skill's worked example is 62% dead for a monument on the centre line and 17.9% after
moving it twelve blocks off; a board with two objectives a side and a spawn between them reads 0.0%.
All four of mine carry one objective and one spawn a side — two journeys — and 22–31% is what that
arrangement costs. The dead ground is consistent across them: the ground behind each spawn, and the
two far flanks of whatever the middle feature is. It is the first thing I would attack on a second
pass, and the fix is a second objective a side rather than any amount of dressing.

Scoriafell is the best of the four at 22.1%, which is worth noting against
`reports/opus5-threap-edge-run.md`'s capture board reading **71.8% dead** — coverage cannot see a
capture point, so a board whose only objectives are hills reads as though nobody goes anywhere.
Giving Scoriafell a destroyable did not only make it winnable; it made it legible to the one read
that asks whether ground is *used*.


**Braidwater's four remaining declines are all one thing.** Three `DR-BANK` and one `DR-DRY`, every
one on a water channel: *"braid-a is 3 deep and its carve cut 8 course(s) of ground away above its
own line — a straight-sided wall from y13 to y20."* Raising the haugh to 22 to make the bank a
barrier also raised the ground the braids run through where they pass near a ford's band, so those
reaches carve a vertical-sided trench instead of a channel in a bed. The water itself is in the
world — `column` reads `y12 Water` at four sampled points across the braids, and the census carries
`9:0 Water` in two of three themes — so this is the shape of the banks and not a missing river. The
fix is to move the braids' x ranges clear of the ford bands, and I stopped at six drives on this
board rather than take a seventh.

## What I could not say

Checked against `openapi.json`, `GET /api/rules` and `GET /api/rules/terms` before writing either
verdict, and by function as well as by name.

**Capture points — MISSING FROM THE SYSTEM.** `tools/drive.py` documents `controlPoints` and
`scoreLimit` as "the capture board's hills and the score the match ends at", prints them on the run,
and patches them onto the compiled intent. The studio reads neither:

    RQ3  field 'intent.controlPoints' was not read
    RQ3  field 'intent.scoreLimit' was not read

and the exported `map.xml` carries no capture element of any kind. Three searches: by **name** —
`controlPoints`, `scoreLimit`, `capturePoint`, `hill` and `koth` return nothing anywhere in
`openapi.json`, there is no `ControlPoint*` schema, and `MapIntent` has `additionalProperties:
false`; by **what it would do to a board** — no rule in the 172-rule catalogue mentions a control
point, a capture or a score limit, and no route under `/paths` answers one; by the **term
catalogue** — no capture, point, score or hill term.

**And it is a regression rather than a gap that was always there.**
`reports/opus5-threap-edge-run.md` opens *"The studio grew capture points this week:
`PUT /map/{slug}/intent` takes a `controlPoints` array"* — a different route from the one a
spec-driven build takes. So I asked that route directly, on this studio, against a real stored map:

    PUT /api/map/opus5-scoriafell/intent    200
    RQ3  field 'controlPoints' was not read
    RQ3  field 'scoreLimit' was not read

Both keys, on the route that used to carry them, on a 200. `GET …/intent` returns fifteen fields and
neither is among them. A whole board type that shipped once is no longer reachable by any route, and
nothing refuses — the board stores, pre-flights OPEN, and exports a `map.xml` with no way to win in
it. That is the most serious thing I found on this run, and it wants checking against the studio's
own history rather than taken from me.

**`relief.stairs` — MISSING FROM THE SYSTEM.** `SketchReliefJson` carries `base`, `reach`, `step`,
`landform`, `grain`, `marks` and `pushes`. `stairs` answers `RQ3`. `GENERATION-NOTES`' entry *"`step`
with `stairs` is the instrument for a quarry"* is half stale — `step` is real and does the terracing;
`stairs: true`, described there as what "cuts a way up out of every place the terracing stranded",
is not read. My first quarry build depended on it for its ways out of the pit and got nothing.

**A third ford character — OUT OF REACH from where I was standing**, and it is symmetry rather than
the surface. Under `rot_180`, crossings of an on-axis river are either self-image (one, on the centre
line) or image pairs, so three fords are at most two authored characters. `mirror_x` would give three
self-mirrored crossings, but a mirror reverses handedness and a `scarp`'s high side is decided by its
trace direction, so the mirrored lip would put its shelf in the river. I took `rot_180` and the
documented scarp behaviour and wrote the limitation down rather than claiming three.

**The red-wool cross over one destroyable — UNEXPLAINED, and I did not invent a cause.** Three blocks
of red wool at (−32, 70..72, −49) with four more at y71 around it, directly over red's goal on
`opus5-goldbank-quarry`. Blue's goal at (31, 48) has none, so it is asymmetric. It stands above the
y65 build ceiling, it is in no region in `map.xml`, the compiled intent is symmetric and states
nothing of the kind, and the section renderer classes it as `destroyable/core`. I could not find the
rule that puts it there. Reported with coordinates so someone who knows can check it in one look.

## What I got wrong, and why it looked right

**A theme patch that painted nothing, at 200, with the gate open.** The quarry's first build stored
at 200, pre-flighted OPEN and exported — with one of its three themes entirely absent from the world.
An `add` with no `height_mode` is "the flat one-block behaviour at y=0", so it never wins a cell
whose ground is twelve blocks tall, and a shape that wins no cell owns no theme scope. Nothing warns.
`05-themes.txt` is the only read on the board that reports it, and I now open it on every build.
Agent A reached the same conclusion from the source; two routes, one answer.

**Then the fix flattened the thing it was painting.** A standing shape reads the **median** ground
under its own footprint, so one patch across the whole bench band came out a flat plate: a transect
down x −20 read `29 29 29 29 28 28 … 26 25 25` where three 3-block benches had been. One patch per
flat tread fixed it. The general rule is that a theme patch is a statement about *one* piece of
ground, and a piece of ground with a slope in it is more than one.

**Two flights that were not in the world, on a board whose whole subject is flights.** The plan tier
passed, the gate opened, and the transect read `BARRIER +6 at (6, −69); DROP −7 at (6, −70)`. Reading
the profile out showed the grown hillside climbing gently where the stair should have been: the top
terrace was stated at y36 where the relaxation arrived at ~37.5, so the shelf was a hollow and its
flight lost every column to the taller ground. The fix is arithmetic — a made shelf has to stand
above the line the relief solves under it, *everywhere its flight's footprint reaches* — and it is
why the brow came down from 40 to 36 and the runs from 12 to 8. All eight flights now read
`rises 4, worst step 2, 0 barrier, walked end to end`.

**A rule pulling against a board's identity, and the rule winning.** `GO1` asks a destroy goal to sit
three to four times as far from the enemy's spawn as from its own. Goals in the middle of a shared
pit cannot: the first Goldbank measured **1.13**. The board's sentence says both goals stand on the
quarry floor, and it survives — lengthening the board to 224 and moving each goal to its own end of
the pit reached **3.37** with both still on the floor. What it cost is that the pit's deepest ground
is now the contested middle rather than where the goals stand, because a sink's depth interpolates
inward to its medial axis and notching two opposite sides makes a bowl.

**A board that did not do the one thing it is for, with every gate green.** Braidwater Ford's
sentence is that the two sides meet at three fords *and nowhere else*. It stored at 200, pre-flighted
OPEN, exported, declined nothing and carried three themes — and three transects across the river said
this:

    across the centre ford (x 0)   rises 4, falls 4, worst step 2: 0 barrier, walked end to end
    between fords     (x -18)      rises 5, falls 5, worst step 2: 0 barrier, walked end to end
    between fords     (x  20)      rises 6, falls 5, worst step 2: 0 barrier, walked end to end

The river was crossable everywhere. A cut bank of five courses over a `face` of 2 is two steps of
two — a scramble, not a wall — and I had been reasoning about `face` as though it alone decided
whether a bank was passable, when what decides it is `(high − low) / face`. The bars could not go
lower because they have to stand above the water line, so the haugh went up from 18 to 22 and the
terrace behind it to 26. Nothing else on the board would ever have said so: the plan tier passes, the
gate opens, the heightmap shades a bank either way, and only a transect across the thing the board
claims can answer whether the claim is true.

**Believing a route read that was standing on a roof.** Every route on Goldbank reports `barrier +11`
and a matching drop. That is `drive.py`'s sweep starting from the spawn point's x,z, which resolves
to the top of the column — the hut's roof — and the shell is 11 courses. `04-reach.txt` names the
same 49 cells at y43 as unreachable standing ground and they are the shell's footprint exactly. The
real walks, taken from outside the door, are 41 blocks own and 139 enemy, both `0 placed, 0 drops`.

## What worked first time

- **The plan tier, once the numbers were read rather than guessed.** Three of four boards evaluated
  `score 0, valid True` with no findings on the first try, after `GO1`/`LN2` had been worked out on
  the first.
- **The push gradient rule, stated as arithmetic before authoring.** Setting `amount/falloff` and
  `crown/half` equal on paper produced a mountainside that measured **1.68 courses a block,
  continuous, with no step at the ring** on its first build. Where I did not do the arithmetic — the
  pass's negative push — `RL6` caught it at 1.2 against 0.6 and printed both numbers.
- **The self-symmetric ring idiom.** A ring authored as half its points plus their negations, so the
  fan lays it back over itself, worked for the quarry's notched sink and the fell's ribbon alike, and
  made the two notches and the saddle symmetric by construction rather than by luck.
- **`relief_scope: "exclude"`, measured rather than asserted.** Lynchet Brow's relief reports 6,054
  cells on a board of 21,632 — the grown ground alone, with the four terraces outside the model.
- **Reading `incline` before choosing where the slope bands cut.** 61.9% under 10° and 7.5% at 40°+
  set the quarry's cuts at 18° and 42° instead of the 20/38 I had guessed.

## Open gameplay questions I had to decide without an oracle

1. **Does `GO1`'s band apply to a board whose goals share one pit?** The rule's stated risk is that
   an under-band goal "falls to a rush before a defence can form". On Goldbank the defence is
   *vertical* — an attacker must descend 16 courses into a sheer pit through one of two notches — and
   the plan tier, which walks pieces flat, cannot see any of that. I obeyed the band rather than
   argue with it, at the cost described above. Whether a pit board should be judged by it is the
   author's call, not mine.
2. **How tall may a bench riser be before a quarry stops being playable?** I used 3, which is a
   scramble, with one walked haul road. I do not know whether the intended feel is "everything is
   climbable slowly" or "there is one road and the rest is a fall".
3. **Is a 4-block retaining wall the right unit for Lynchet Brow?** It makes the wall a genuine
   barrier and the flights the only ways up — 9.35% barrier, the highest of the four — but it also
   means a player who misses a flight is committed to walking the headland. 3 would be a scramble
   everywhere and might dissolve the board's whole idea.
4. **Should a capture board's points be the objective at all, or should the pass simply be the route
   between two destroy goals?** Forced by the missing mechanism, I gave Scoriafell a destroyable a
   side and left the three control points in the finish as stated intent. That is a different match
   from the one briefed.

## For `GENERATION-NOTES.md`

Each of these cost at least one build here.

1. **A theme patch must declare a `height_mode`, or it paints nothing and says nothing.** Only a
   standing shape (`level`/`raise`/`sink`) is a candidate for a cell it does not out-top. `05-themes.txt`
   is the only witness. Corroborated independently by Agent A from `SketchRasterizer.ShapeScopeOwners`.
2. **A standing patch reads the median ground under its footprint, so a patch across a slope
   flattens it.** Measured: 3-block quarry benches → 1-block steps. One patch per flat tread.
3. **`relief.stairs` is not a field** — `RQ3`. The `GENERATION-NOTES` quarry entry needs its second
   half removed.
4. **`controlPoints`/`scoreLimit` are not read** — `RQ3`, and nothing reaches `map.xml`. `drive.py`'s
   docstring and its `intent_from_finish` both need the caveat, or the studio needs the field.
5. **`placements[*].at` is in blocks**, for spawns and goals alike, despite the openapi description
   saying "half-blocks" for destroyables and cores. Settled in one call without building:
   `POST /plan/compile` returns the compiled intent, and `at: [10,10]` on a piece whose minimum
   corner is (−32,−64) came back as `anchor {x:−22, z:−54}`.
6. **A goal with no `piece` still yields `GO1`/`GO3`/`GO4`.** Agent A reports the ratio coming back
   `None` with `piece: ""`; omitting the key entirely gave `own/enemy/ratio` on all three of my
   destroy boards. The difference may be empty-string versus absent, and is worth one probe.
7. **`drive.py`'s route sweep starts on the spawn hut's roof.** It walks from the spawn point's x,z,
   which resolves to the top of the column, so on any board whose spawn is a building every route
   reports the shell's wall height as a barrier and its far side as a drop. Walk from outside the
   door for the real cost. `04-reach.txt`'s unreachable patch is the same cells.
8. **`RL6` exists and names the push-gradient mismatch with both numbers.** It is the enforcement of
   *"a range is a wall unless its two gradients agree"* and it prints skirt and crown in courses a
   block. Reach for it rather than deriving the ratio by hand.
9. **A `sink`'s depth interpolates inward to its medial axis.** A ring notched on two opposite sides
   builds a bowl — deepest in the middle — not a flat floor with two ramps. Stated depth 10; centre
   measured 11 down, ends 5 down.
10. **`WX11` prints the exact area mark to add.** A stamped shell levels the column under its whole
    footprint at the footprint's highest, so give every spawn a rectangular room pad wider than the
    shell on all four sides *from the start*. A lobed apron ring will leave a corner outside it.
11. **A push skirt grades whatever it reaches, in both directions.** Held 20 and 5 blocks clear of a
    scarp it leaves the bank sharp; allowed to reach a spawn it lifts the ground the shell stands on
    and `RL3` reports a 10-course step between the room pad and the compiler's own spawn mark.
12. **The house-style refusal chain, in the order it fires**: `HS3` (a roof's verge may not be a bare
    log — use a `laidLog`; and the half-course slab must be the roof body's own material), `HS9`
    (beams only come out of a wall course that is itself a laid log), `HS4` (the door head's stair
    block and the slab that fills it are one material). Four separate round trips if met one at a
    time.
13. **`PT1`: a surfacing block is exactly one course and must be at the top of a stack.** Podzol
    under grass is a refusal, not a warning. Two surfacing blocks share one course as a pattern.
14. **`DR-DRY`: a channel's bed can be carved wider than its water fills**, leaving a dry trench
    beside every braid. A wandering 3-block shore did it; a narrow even shore digs only what the
    pool covers.
15. **`DC3` substitutes silently enough to miss**: `materials: "hardened clay"` is not buildable and
    the goal was built in ender stone, which no render distinguishes.
16. **A scarp's passability is `(high − low) / face`, not `face` alone.** A `face` of 2 is quoted as
    a cliff and a 6 as a walk-up, but 5 courses over a face of 2 measured `0 barrier, walked end to
    end` while 9 over the same 2 is a drop that cannot be climbed. State the drop you want and then
    pick the face, and prove it with a transect *across the thing the board claims*, not along it.
17. **`DR-DRY` is usually the ground's fault, not the shore's.** Its coordinates carry the y — a
    complaint at `(-27, 15, -17)` on a water line of 15 is telling you the bed around the channel
    sits below the water, and no amount of shore tuning fixes that. Read the y.
18. **`column` and the other reads answer text, not JSON.**
