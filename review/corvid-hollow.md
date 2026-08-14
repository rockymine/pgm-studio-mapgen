# Corvid Hollow — the canonical brief

DTM, `rot_180`, 16 players, 142×180. This is Map 1 of the run: the fixed brief every model built —
*"A destroy board, one connected island, the monument in the open with a forest closing the west flank,
a hill east that attackers can bridge from, a village behind, a void channel twenty blocks in front."*

## What it is

One authored half (team 0) fanned by `rot_180` into the whole board. Along the spawn-to-monument axis:
a fortified spawn platform (`corvid-keep`, y12) behind a village (`roost-timber`, y10) behind an open
plaza (`hollow-turf`, y9) carrying the monument, with a forest (`rookwood`) closing the plaza's west
flank and a hill (`briar-crest`, an erected `raise` shape tilted 10→18) closing the east. A 20-block-deep
central void (`moat`) sits immediately in front of the plaza, spanning its full width; the forest and hill
corridors run past it unbroken on either side, so the board is **one connected landmass** — the void forces
a detour, it does not cut the island in two.

Under `rot_180` the two teams' pieces land on opposite diagonal corners (red's forest top-left mirrors to
blue's forest bottom-right, and the same for the hill), which is the symmetry working correctly rather
than a fault — see `renders/01-topdown.png`.

## How it plays

- **Around**: the moat is enforced void (`build.voidEnforcement`, no exclusions — see *What landed*
  below) from the first tick, so a straight rush at the monument is not an option. An attacker must commit
  to one flank or the other before reaching the plaza.
- **Through**: the forest (west) reaches to within a few blocks of the plaza's edge, cover the whole way,
  cheapest early when the moat is unwatched.
- **Above**: the hill (east) climbs from y9 at its own rear (near the village, the easy walk-up) to y18 at
  its southwest corner — the point directly overlooking the plaza and the moat. An attacker who takes the
  hill gets a bridging launch point with height on the defenders; the peak sits at y16–18, two to four
  blocks under the y20 build cap, so a player standing there can still place blocks — the whole point of a
  ledge that is *climbed to and bridged from*, not a wall that ends the approach.
- **Room by room**: the village sits behind the plaza on the walk back to spawn, nine houses (two styles)
  fronting a worn-gravel street on a shared building line — the deliberate grid the brief asks for, not
  scattered lots.
- **Exposed**: the plaza itself is flat, undecorated `hollow-turf`, held flat (`relief_scope: hold`)
  against the island's own grain so it never picks up incidental cover near the goal.

## Techniques used

- **A tier that recedes is overlapped by the piece above it, not the other way round.** Spawn (y12) and
  village (y10) step down toward the plaza (y9) exactly as `ruediger.plan.json` does it — three plan
  pieces at three surfaces, no relief needed for the built stair.
- **A subtract over the mid, drawn as one buffer piece.** The moat is `role: buffer` at the plan layer,
  not a hand-carved sketch subtract — `PlanCompiler` turns it into the notch directly (`corvid-hollow.plan.json`,
  piece `moat`), and it shows up as both the fused plaza/forest/hill outline's own concave notch (`s0`
  before I split it) and a second, explicit `subtract` shape (`PlanVoids.Declare`). Both read the same
  channel; I kept the explicit one and gave *it* the Bézier curve.
- **Three Bézier curves, all edge-vertex pairs done correctly the second time.** The moat's plaza-facing
  edge scallops inward at the centre (`controls` on vertices 0 and 1 of the same edge); the forest's and
  the hill's outer (map-edge) sides round outward the same way. The first attempt at the hill and forest
  curves put an `out` **and** an `in` handle on the *same* vertex, which bends both edges meeting that
  vertex rather than one — see *What I got wrong*.
- **`height_mode: raise` with per-vertex `anchor_heights` and `skirt: 0`** on the hill: four corners at
  `[4, 1, 1, 9]`, which — because `raise` reads the datum as the **median of the ground already under the
  shape** and adds the anchor as an offset to it, not as an absolute height — resolves to nine feet high at
  the low corner and eighteen at the high one. `skirt` is zero rather than the softer value I first tried,
  because a nonzero skirt blends toward "the ground just outside the outline," and the hill's outline
  meets **void** on its western face; blending toward nothing pulled that whole edge down to y7. A sheer
  hill face reads as a rock scarp here, which the `briar-crest` wall pattern (`wallDiagonal`, stone over
  cobble) was already themed for.
- **`relief_scope`, three ways on one island.** `plaza: hold` (flat, exposed, no incidental cover),
  `village`/`spawn-ground: exclude` (built tiers, no grain), `forest` left in the solve (grown ground, a
  gentle line-mark ridge plus 0.8-amplitude grain). `hill` needs neither, since a `height_mode` shape is
  never read against the relief at all.
- **`build.voidEnforcement` with no `build.areas`.** This map declares no buildable rectangles — nothing
  should be bridgeable — and the fix this run tests for is exactly this case: enforcement used to require a
  declared build area to fire at all, so a map with none got an unenforced, freely bridgeable void by
  default. I set `voidEnforcement: { exclusions: [] }` explicitly rather than relying on the old
  accidental behaviour.
- **A goal riding a `raise: false` ordinary shape via an absolute marker, and a default `obsidian`
  destroyable.** `{"piece": "", "at": [0, -6]}` on the plan, no `materials` field. This tests the second
  fix this run is measured against: an obsidian destroyable used to be refused against the standard iron
  pickaxe as "unwinnable," which was false (an iron pickaxe breaks obsidian, it only fails to drop it).
  The export succeeded with the default; see *What worked first time*.
- **Per-shape theming, five themes on one board**: `hollow-turf` (plaza/default), `rookwood` (forest, a
  `cell` fabric of grass/dirt/mossy-cobble patches nested in the surface band), `briar-crest` (hill,
  `wallDiagonal` rock strata), `roost-timber` (village, a `cell` pattern nested inside the top course of a
  `layered` surface — the single most useful technique the run-1 reports found), `corvid-keep` (spawn).
  Rim is `void`-only on the two grown themes (forest, plaza) and `boundary` on the three built ones — off
  wherever the ground is meant to read as grown, on wherever a tier is meant to read as built.

## What went wrong, and what I caught before it shipped

**The `bedrock` field's `relative` flag inverts what it sounds like it does, and I had it backwards on
every one of the five themes at first.** `TerrainTheme.cs`: `BedrockSpec.TerrainRelative(int
terrainDepth)` — "bedrock takes everything **under** the top `terrainDepth` painted blocks." I read
`{"relative": true, "value": 1}` as "one block of bedrock, placed relative to the floor" (a thin bedrock
floor); it actually means "keep one block of *terrain*, and bedrock swallows everything below it." Every
column on the first build was a single painted block sitting on a solid pillar of bedrock down to y0 — a
tunnel-proof map by accident, and invisible from directly above, because a top-down render only ever shows
the topmost block. I caught it with `--column`, not with any plan-view render, which is exactly the
brief's point about the vertical read-backs: four separate findings tonight were settled by them and
nothing else, and this is a fifth. Fixed by setting `relative: false` everywhere (a true one-block bedrock
floor at the map's own y0).

**A `controls` entry with both an `out` and an `in` handle on one vertex bends *two* edges, not one.**
`sketch.md`'s own worked example puts both handles on the same vertex index to *round a corner* — which
is correct when that is the intent. I copied the shape of that example to bulge a single *edge* (the
hill's and the forest's outer sides) and it silently warped the **neighbouring** edge as well (the north
edge shared with the village), far enough to self-intersect the polygon and cut a real hole in the ground —
two void columns, `(40, -40)` and `(60, -40)`, with nothing above them at all. Caught with `--column`
again, on a routine sweep of the hill's four corners rather than because anything upstream complained: the
plan compiled clean, the sketch saved clean, and the export succeeded both times. Fixed by putting the
`out` handle on the edge's start vertex and the matching `in` handle on the edge's *end* vertex instead of
doubling up on one.

**The hill's first anchor values put its peak at y27, seven blocks over the y20 build cap.** I had assumed
`anchor_heights` under `raise` states the *final* height per vertex, the way it reads under `level`. It
does not — `raise`'s datum is the median of the ground already under the shape (here, the plain terrain
before erection, ≈9), and the anchor is added to that datum rather than replacing it. `[12, 9, 9, 18]`
therefore built a hill fourteen to eighteen blocks *taller* than I'd drawn, defeating the whole point of a
bridging ledge — a player standing above the build cap cannot place a block at all, so nothing can be
bridged from up there. Re-tuned to `[4, 1, 1, 9]`, which reads back at y10–18 exactly where the design
wants it. Caught by column-probing the hill's own corners before calling it finished, not by any refusal —
nothing in the pipeline checks a shape's erected height against the build cap.

## Findings, with coordinates

| # | What | Where | Verdict |
|---|---|---|---|
| 1 | `bedrock.relative: true` reserves only the *top* `value` blocks as terrain and fills everything below with bedrock — the opposite of a thin bedrock floor | any column before the fix, e.g. `(45, -30)`, y1–19 solid bedrock under one grass block | mistaken — documented in `TerrainTheme.cs`'s own docstring, I misread it |
| 2 | A `controls` entry combining `out` and `in` on one vertex bends both adjacent edges; using it to bulge a single edge self-intersects the polygon | `(40, -40)` and `(60, -40)`, void before the fix | mistaken — my own authoring error, not a system fault |
| 3 | `raise`/`sink` add `anchor_heights` to the **median pre-erection ground**, not to an absolute datum | hill peak measured y27 with `anchor_heights` `[…,18]` before re-tuning, y16–18 after | mistaken — the mechanism is documented in `SketchRasterizer.Erect`'s comments, I hadn't read the source before authoring |
| 4 | Skirt blends toward "the ground just outside the outline"; where that outline meets void the blend has nothing to ease into and drags the edge down | `(32, -2)` read y7 with `skirt: 3` against the moat, y16 with `skirt: 0` | mistaken — not documented as a caveat anywhere I found, but the mechanism (`InwardDepth`) explains it once read |
| 5 | `build.voidEnforcement` fires independently of `build.areas`, so a map with no build area can still declare the void permanent | `corvid-hollow.intent.json` `build.voidEnforcement.exclusions: []`; `map.xml` carries `block-place=deny(void)` over `everywhere` | confirmed fixed — this is the capability the brief named as newly landed |
| 6 | A default-obsidian destroyable exports clean against the standard kit | `destroyables[0].materials` omitted (defaults to `obsidian`); export `200`, `map.xml`'s spawn kit carries a diamond pickaxe (`DestroyKitPairing`) | confirmed fixed — the brief names this as the false premise from run 1 |

## Open gameplay question

**How far "twenty blocks in front" should be measured from.** I read it as the width of the void itself
(the plan piece `moat` is 20 blocks deep in z, from the plaza's edge to the symmetry axis) rather than as
the monument's distance to the void's near lip (which is 10 blocks, since the monument sits mid-plaza).
`approaches.md` gives "roughly twenty blocks" for the gap's own width and does not separately state a
setback, so I made the channel's width the exact number and left the setback as a design choice. Recorded
as a decision, not a derivation.

## Reproducing

```
POST   /api/plan                          {"name": "Corvid Hollow"}
PUT    /api/map/corvid-hollow/plan        specs/corvid-hollow/corvid-hollow.plan.json
PUT    /api/map/corvid-hollow/sketch      specs/corvid-hollow/corvid-hollow.layout.json
POST   /api/map/corvid-hollow/sketch/finish
PUT    /api/map/corvid-hollow/intent/from-plan   specs/corvid-hollow/corvid-hollow.intent.json
GET    /api/map/corvid-hollow/export
```
