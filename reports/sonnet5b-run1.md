# Sonnet 5b — run 1: four boards, one of each objective shape

## What I set out to build

Four boards, decided together before any JSON was written: one destroy-the-monument
(`sonnet5b-white-scarp`, a chalk down), one destroy-the-core (`sonnet5b-turbary-cut`, a peat moor), one
capture-the-wool (`sonnet5b-ropeworks-quay`, a fishing harbour) and one played for a wool and a monument
at once (`sonnet5b-highgarth-fell`, a red-earth hill-fort).

The two destroy boards share a flat-lane skeleton (landscape boards, per
`WHAT-A-BOARD-IS-MADE-OF.md`'s "every destroy board is a landscape board"); the two wool boards share a
hub-and-spur skeleton with a corner room and a prepared wall (`match-flow.md` §10.1's "ground is built,
not landscape").

Four different ground tone families — pale chalk, warm peat, grey stone, red earth — checked across the
run rather than within any one board.

All four exported at **0 props declined** and **export gate OPEN** on the drive that shipped them.
`GET .../coverage` dead-share: 27.4%, 43.0%, 3.3%, 1.2% — reported per the brief's own instruction rather
than contorted toward, since the two landscape boards' dead ground is the flank scenery (a quarry, a
cutting, a knoll, a mound) the approach diversity asks for, off the spawn↔goal line but not off the
board's own approaches.

## What I could not say

**Where the biome lives for a driven board.** `SketchLayout.biome`/`biomeSource` is a real field, readable
and writable at `GET`/`PUT /map/{slug}/sketch/biome`, and I found it in `openapi.json` before writing
anything — this is **not** a missing capability. What is missing is a route from `drive.py`'s own loop:
`tools/README.md`'s finish-document key table (`themeById`, `roomStyles`, `dressing`, `relief`, …) does
not list `biome`, so a `finish.json` cannot state it and have the driver patch it in.

I set it with one extra `PUT` after driving `sonnet5b-turbary-cut` and re-exported by hand (curl, unzip,
move the provenance sidecar out of `region/`) rather than through a second `drive.py` pass, because a
second pass calls `POST /map/from-documents` again and that call writes a whole new layout document from
the plan and finish — which would have overwritten the biome just set. This is **unreachable from where
I was standing** (the documented driver loop), not absent from the surface.

**Whether `HouseProp.wings` takes `corners` or `{minX,minZ,maxX,maxZ}`.** The schema in
`openapi.json` states `corners: [[x,z],[x,z]]` plainly (`AuthoredWing`), so this was a **mistaken** claim
I made once and corrected against the schema, not a gap — I had written the wrong shape into
`sonnet5b-ropeworks-quay`'s first `ropewalk` prop without re-checking the schema after drafting it from
memory of `Rect`'s own min/max convention used elsewhere in the same document. The wrong shape did not
refuse; see *What I got wrong*.

## What I got wrong, and why it looked right

**The wrong wing shape did not refuse, and it should have looked more alarming than it did.** Posting
`wings: [{"minX": …, "minZ": …, "maxX": …, "maxZ": …}]` against a schema whose `additionalProperties` is
`false` and whose real field is `corners` answered **200** at `plan/compile` and at
`POST /map/from-documents`, and `preflight` answered `export gate OPEN`. The fault only surfaced three
calls later, as a 500 on `sketch/columns`, `coverage` and `export` — the three calls that actually walk
the dressing pass rather than only the plan and the intent.

I initially read the 500's own body (`RQ2`, "the fault is its own") as meaning the fault was unfindable
from here; it was not — the running studio's own stdout, redirected to a log file its process still held
open (`/proc/<pid>/fd/1`), carried the full .NET stack trace naming `HouseProp.Check()`, and reading that
rather than guessing from the refusal text is what actually found it in one step instead of several.

**A combined board's numeric bands are not the union of its two gamemodes' bands.** I built
`sonnet5b-highgarth-fell` by taking `sonnet5b-ropeworks-quay`'s plan geometry (sized so `CT12`'s strait
comes out 15–40 blocks) and adding a destroyable at the offset that had worked on the *short* landscape
lane. `GO1` came out 7.32 against a 3.0–4.0 band and `GO3` 278 against 85–150 — a CTW-length approach
chain is far longer than a destroy lane wants, and no amount of sliding the beacon within that chain
closes both gaps at once, because moving it toward the enemy to fix `GO3` moves it away from `GO4`'s own
floor. The actual fix was shrinking the whole spawn-to-strait depth, not retuning the goal.

## What worked first time

The two landscape boards' core geometry — spawn piece, field piece, an 8-cell build-zone strait — cleared
`GO1`, `GO3`, `GO4` and `CT12`-equivalent island-gap numbers on the *second* attempt at
`sonnet5b-white-scarp` (one correction, from a hand-guessed monument offset to one read off
`plan/inspect`'s own `goalDistances`), and the identical skeleton with a core in place of a destroyable
cleared the same four bands on `sonnet5b-turbary-cut`'s **first** attempt, because the geometry, not the
goal kind, is what the bands are about.

The wool-room-and-wall arrangement on `sonnet5b-ropeworks-quay` cleared `PL13` (wall not on the room's
own interface), `ST8` (lane-mouth width and wall-to-door distance) and `CT12` together once the room was
sized against `plan/evaluate`'s own complaints rather than guessed — zero iterations were spent on trial
geometry that had to be thrown away; every correction was read off a named finding and applied once.

The `slope`-axis `layered` material (turf → coarse dirt/gravel → sandstone/stone) painted a legible
flat-shoulder-face gradient on every board's first export, calibrated against each board's own
`GET .../incline?format=text` rather than copied from another board's cut points.

## Open gameplay questions

**Whether a combined wool-and-monument board should shorten its strait or lengthen its approach chain.**
`approaches.md` settles that a wool belongs behind its spawn and that a CTW strait is 15–40 blocks; it
does not settle what a board does when satisfying the second (which wants a long hub-and-spur chain to
give the wall and the room's clearances room to sit right) pulls against the first two destroy bands
(which want a short lane).

`sonnet5b-highgarth-fell` resolved it by shortening the whole approach depth until all three numeric
bands landed together, which reads as a smaller, more compact fort than either gamemode's own worked
examples — I do not know whether a real map of this kind is expected to read compact that way, or
whether the correct answer is a board large enough that the wool sits properly deep while the monument
sits on a spur of its own rather than in the shared yard. Built it the compact way and recorded the
question rather than filing it as a rule.

**Whether 27–43% dead share is an acceptable cost for flank scenery on a small destroy board.** The brief
is explicit that `coverage`'s dead-share carries no gate and should be reported rather than chased, and I
took that at face value for the two landscape boards — narrowing `sonnet5b-white-scarp` once (208×80 to
208×64) cut it from 53% to 27% at no cost to the goal-distance bands, and I stopped there rather than
narrowing further, because narrowing again would have started crowding the quarry and the knoll against
the monument's own clearance box.

Whether a real destroy board this small should carry two flank features at all, or one, is a composition
question `WHAT-A-BOARD-IS-MADE-OF.md` leaves to the author.
