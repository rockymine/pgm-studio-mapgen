# Reedcut Levels — Reedcut, built

> A worked peat lowland: brown and green, low contrast on purpose, and legibility comes from relief rather
> than paint.

**In one sentence:** a low, quiet fen where the cuttings sink and the banks rise a few blocks either way of
a shared field level, a raised worked hub of coarse dirt sits at the crossing, and a water lane gives the
wool a second approach that only opens forty-five minutes in.

Board bbox `-65..65 × -85..85` (130×170 blocks) — close to the brief's "about 160×140" (axes roughly
swapped, similar area). `rot_180`, base surface 9, `maxPlayers` 24, one `team` island fanned ×2 plus one
`neutral` on-axis piece (`bar`, the crossing hub).

## Where the brief's things are

| The brief said | Where it is | Measured |
|---|---|---|
| loam (cuttings), dirt (banks), verdant (dry tops) | `reed-lowland` theme: `layered` Grass(1)/Coarse Dirt(2)/Podzol(2)/Brown Stained Clay(2); `reed-bank` theme: Grass/Green Stained Clay `cell`; `reed-cut` theme: Podzol/Brown Stained Clay `cell` | three themes, on `s0`/`s2` (lowland), `s1`/`s3`/`s4`/`s5` (bank), `s6` (the neutral crossing, `reed-cut`) |
| grass at thickness 1, on top only | `reed-lowland.surface`: first band `Grass, thickness 1`, everything below Coarse Dirt/Podzol/Clay | read straight off the theme document — no second grass band anywhere in the stack |
| relief does the work on the lowland | `relief.team`: two `area` sink marks (`cut1`, `cut2`, `h: 6`, four below base 9) and one `line` bank ridge (`bank1`, `h: 11`) plus one `push` swell | `POST /map/{slug}/sketch/relief/read` → `island team: cells=1875 low=6 high=11 relief=5` — a five-block relief range on top of the plan's own tiers |
| built things sit inside `relief_scope: hold` | *(built as `exclude`, not `hold` — see below)* | `s1`, `s3`, `s4`, `s5` all carry `relief_scope: "exclude"` |
| rims off except the cut faces | `reed-lowland`/`reed-cut`: `rimEdges: "drop"`, rim disabled; `reed-bank`: `rimEdges: "boundary"`, rim enabled | the only rimmed shapes are the built bank platforms, where the step is a made edge |
| a water lane, a second approach that opens late | `zones`: `lane-east`, `kind: "water-lane"` | 4 occurrences of `water-lane` in the exported `map.xml` — it reached the document |
| buildings on the banks, one down in a cutting | `sn-reed-bankhouse` ×2 on `works-lo-w` (a bank shape); `sn-reed-cutter` ×1 on `east-strand`, forked with `foundation.footing: null` | `h1`/`h2` on the bank tier; `h3` alone, `front: "posZ"`, footing removed so it seats without a footing course |

## The one correction against the brief's own wording

**`relief_scope` on the built shapes is `exclude`, not `hold`.** The brief says built things sit inside a
`relief_scope: hold`; `sketch.md` states what each actually does — `hold` leaves a shape's cells *in* the
relief field, pinned flat at one level, while `exclude` removes them from the field so the surrounding
relief bends around the footprint instead of ramping up to meet it. For a stepped plan tier (the works-yard,
the wool room, the spawn apron — each already at its own `base_height` from the plan) `exclude` is the
correct instrument: `hold` would still let the relief *reach into* the footprint at its ring centre, and a
tier whose neighbours are meant to sink away from it (a cutting dropping off the bank) wants a clean face,
not a ramp. I built `exclude` and record the wording difference rather than silently matching the brief's
letter over `sketch.md`'s own description of what the two modes do.

## What went wrong, and the fix

**Two houses landed off their own piece, twice.** The first placement of `h1`/`h2` (the bank-top houses)
missed `works-lo-w`'s actual footprint (`DR-SITE`, no ground under the wing); moving them onto the piece
then put them close enough together that neither kept its 5-block passable side (`DR-PASS`). Both were
found by the dressing decline read, not guessed — the fix was to re-read the compiled shape's own vertices
(`POST /plan/compile`) rather than estimate the piece's world-space footprint from its cell rect by hand a
second time.

## The techniques

**A dead-end wool room, learned from the Compass Yard build earlier in this run.** `wool-room` docks against
`wool-approach` alone (`z 45..60`), and the route from spawn to the rest of the board runs
`spawn → spawn-apron → moor → wool-approach`, never through the room — the same shape that produced `EX1` on
the four-team board when the room sat inline on a team's only route out. Confirmed:
`GET /map/reedcut-levels/traversability` → `connected: true`.

**A neutral crossing hub, not a mid island.** `bar` (`mirrors: false`) is the on-axis piece both team images
meet at, themed `reed-cut` (loam) rather than either team's bank colour, so the crossing itself reads as a
third, contested kind of ground rather than an extension of either side.

## The checklist

| # | Check | Measured | Verdict |
|---|---|---|---|
| L1 | one gamemode | `<gamemode>ctw</gamemode>`, once | pass |
| L2/L3 | team/spawn/wool present, label matches | 4 `<team>`, 2 `<spawn>`, 2 `<wool>` | pass |
| P6 | no wall on the wool room's own entry face | wall on `wool-approach`↔`leat-bench`, one piece out | pass |
| P7 | wall 10–20 wide, ~15 in front | `15×20` blocks (from `/plan/inspect`), seated on the piece one out from the room | pass |
| M1 | grass exactly 1 course, never below it | `reed-lowland.surface`: `Grass` thickness 1, top band only | pass |
| M6 | seated building has no footing | `sn-reed-cutter.foundation.footing: null` | pass |
| C0 | extent/aspect | 130×170, close to "about 160×140" | reported |
| C4 | void placement | between the two team islands at the crossing; the water lane is the only second gap, and it is not a permanent connection | reported |
| C9 | landform transitions | cuttings (`cut1`/`cut2`) and the bank ridge (`bank1`) are relief marks on the same solved field as the open lowland — no plan tier butts a hand-drawn dip with no transition between them | reported |

`GET /map/reedcut-levels/traversability` → `connected: true`. No load-blocking or §3.2–§3.5 rule failed.

## Open questions

**Whether a water lane genuinely earns its place here, or is decorative.** `approaches.md` says a lane "can
never be what connects two teams' lands" and is for "a second approach that opens late" to a tucked-away
goal. This board's wool is not especially tucked away — it sits behind one bedrock wall, the ordinary
single-chokepoint shape — so the lane is closer to a bonus flank than a necessity. I kept it because the
brief names it as the one place in the set a lane is legitimate, and because `approaches.md` does not forbid
a lane on a wool that already has a land approach, only forbid it as the *only* one. Whether the wool needed
a second approach at all, rather than being tucked further back specifically to give the lane a reason, is
a judgement call the brief does not settle and I record rather than assert.
