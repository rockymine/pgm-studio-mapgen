# Report — sonnet5-kilnholt-cut

## What I set out to build

A destroy board, `dtm` only: two rival stonework guilds have driven their excavation into opposite
flanks of the same worked-out quarry, each guarding two buried obsidian monuments at the bottom of their
own cut, and a played-out mine adit under the west flank still connects the two sides for whoever is
bold enough to use it. One landmass a side (spawn fused to its excavation), `rot_180`, joined on the
surface only by a permanent void gap spanned by a build zone, ground finished by slope angle rather than
height (flat reclaimed floor, worked-stone shoulder, bare cut face), and an honest attempt at a bottom-up
stacked tunnel under the gap with a stair back to the surface at each end.

## What I could not say

**Nothing in this build turned out to be missing from the system.** Every capability the board needed —
per-shape override cavities, a new layer with its own unmirrored group, the slope-axis material, absolute
destroyable placement — is documented in `docs/tools/sketch.md`, `docs/world-export/relief.md` and
`tools/README.md`, and every refusal I hit named the exact field or the exact rule to fix. The two things
that cost real time were **unreachable from where I was standing**, not gaps in the studio:

- **A brand-new, unmirrored relief group for a layer `addShapes` adds to the compiled ground.** The
  compiled "team" group is always the fanned one on a two-team board with no on-axis piece, and any
  `addShapes` entry naming a group id that doesn't exist yet is created with `mirrors: True` hard-coded
  (`drive.py` line 590). I needed the tunnel's floor cavity to sit on that same fanned ground layer *and*
  not double under both flanks, and the only way to get that was to make the cavity's own footprint
  self-symmetric under `rot_180` (its two ends already `rot_180` images of each other), so fanning it
  reproduces the identical shape rather than a second one. `addLayers`, by contrast, does let me state a
  layer's own `groups` with `mirrors: false` directly — I used that for the tunnel's three new layers and
  it worked first time. So: reachable, by putting the self-symmetric trick on the one shape that had no
  other way out, and reachable cleanly everywhere else.
- **`intent.meta.authors` on the one-call `/map/from-documents` path.** Checked in `GET
  /api/openapi/v1.json`: `MapFromDocumentsRequest` carries `authors` as a top-level field, and it is
  applied — the exported `map.xml` correctly carries `<authors><author>Sonnet 5</author></authors>`. But
  `EX6` still fires on every drive (*"the map names no author, so the observer platform's authors board
  is left off"*), and `docs/tools/sketch.md`'s Info section says the sync is meant to run the other way:
  a name written through `PATCH /api/map/{slug}/metadata` is supposed to be patched into the stored
  intent's own `meta.authors` too, so the export's in-world sign has something to read. The one-call path
  `drive.py` uses evidently does not do that second write. This is real and reproducible, not a
  misunderstanding on my part — I checked the schema, checked the XML, and checked the doc's own
  description of where the sync is supposed to happen — but I did not chase a workaround beyond what a
  spec can state, since patching it would mean a second call outside the documented one-call flow, which
  the run rules ask me not to invent.

## What I got wrong, once I found out

**I assumed a `subtract` on one layer could only ever be judged against shapes on that same layer, because
the finding's own sentence says so** ("a subtract reaches only the layer it is on"). My first cut at the
tunnel's walkway was a full-width `add` plus a `subtract` cutting the walkway gap, both on `tunnel-walls`,
four blocks below the compiled excavation's own surface — geometrically nowhere near it. The store still
refused it with `SK13`, naming the excavation shape (`cut-16`, on `ground`) and my subtract (on
`tunnel-walls`) as disagreeing about whether that ground is void. The check is over the **document's**
shapes, not the resolved world, so a subtract anywhere is compared against every `add` in the whole
layout regardless of layer or height. Two plain `add` strips either side of the walkway, no subtract at
all, sidesteps it and builds the identical hollow corridor. I had read the rule's own sentence too
literally instead of testing it.

**I got a quad's `anchor_heights` order backwards on the first attempt at the surface stair**, assigning
`[near, near, far, far]` to a rectangle a shared `strip()` helper actually returns as
`[near-lo, far-lo, far-hi, near-hi]`. The result was a twisted ramp — one near corner at the tunnel floor,
the other at the surface — that only showed up once I probed the column at the portal and it read a flat
tunnel roof where a rising stair should have been. Reading the helper's own return order before writing
the anchor list would have caught it without a probe.

**I moved the two destroyables to fix `GO2` and broke `GO1` in the process** (own-walk went from 43 to
50, ratio from 3.07 to 2.6), then over-corrected along the wrong axis and broke `GO4` (own-distance one
block under 40) before landing on a position that satisfies all three at once. `/plan/inspect` after
every move is what caught each one; none of the three failures was visible from `board.py`'s grid, since
they are all walk-distance numbers rather than rectangle relations.

## What worked first time

The plan — two pieces a side stated at one surface, fused into a single landmass, with the descent's
`tread` keeping the pit floor flat and grading only the outer shoulder into the rim — compiled and
exported clean on the very first full drive once the JSON errors above were fixed; no `SK1`, `SK7`, or
seam complaint ever showed up on the terrain proper. The slope-axis theme (`SLOPE_MASK`, following
`opus5-scarp-mask`'s pattern almost exactly) produced a graded three-band split of 67.9% / 6.3% / 25.7%
on the real board without a single retune — `incline?format=text` matched what I had guessed from the
mark heights closely enough that I never had to move a cut point. The self-symmetric tunnel line (both
portals stated as `rot_180` images of each other) fanned correctly the first time it was tried, with no
double corridor anywhere on the board. And narrowing the excavation from 104 to 80 blocks wide dropped
`coverage`'s dead share from 30.3% to 9.4% in one edit, exactly the size of the flank that was cut away.

## Open gameplay questions decided without an oracle

**Should the tunnel cost something, the way bridging the surface gap does?** The walk endpoint confirms
a genuinely free crossing through it — `rises 0, falls 0, worst step 0` from either spawn to the far
side's destroyables — where bridging the void costs placed blocks and exposure. I built the cheap version
because the brief called it a reward "for whoever is bold enough to use it" rather than asking it to be
priced against the bridge, but whether a free flanking route is right for this board rather than merely
convenient to build is a question about play, not geometry, and I have recorded it in `review.md` rather
than decided it.

**`SK11` still names 350 cells of standable ground near the western portal with no route onto them.**
I believe it is the stair's own risen shoulder or the tunnel-cover's edge — a ledge nothing currently
walks up to — but I did not trace the exact cells before running out of time, and I would rather say so
than guess at a fix I have not verified. The export gate is open regardless: this is a complaint, and
the spawn-to-objective chain is connected on both sides.
