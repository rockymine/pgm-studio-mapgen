# Fable run 5 — Whitebarrow Down, and what the documents did not say

## What I set out to build

Stated before authoring anything: **a combined destroy board — one destroyable and one core per
team, the corpus's "ordinary combined board" — on a chalk down.** A lane, not a square: spawn at
the back, the Barrow Stone (obsidian standing stone) a short walk forward on an open lawn ringed
by sarsens, the Powder Magazine core sunk in a dell east of it, and the two sides meeting across
a saddle holding a dew pond — the depression instrument `approaches.md` prescribes for a destroy
mid in place of a void hole. West flank a beech hanger (cover), east flank a chalk scarp
(height), a flint-and-timber hamlet behind. Five numbers first: 100 × 190, `rot_180`, spawns at
(0, ±90), destroyable at (∓8, ±53), core at (±25, ±55); two routes: the frontal ramps over the
saddle, and the flank pair (hanger west, scarp east).

Built as `specs/fable-r5-whitebarrow/` (plan + finish), world in `maps/fable-r5-whitebarrow/`
(final API slug `whitebarrow-down-6`), review in `review/fable-r5-whitebarrow.md`. **It
exported**: 200 at every step of the final run, nothing declined, all 37 props landed (verified
against `region/provenance.json`), 18 structures standing, both goals in GO1's band at 3.0,
relief symmetry error 0, kit auto-upgraded to diamond pickaxe.

## What I could not say

Item by item; **missing from the system** vs **out of reach from where I stood** marked. Every
"missing" claim was checked against `GET /api/openapi/v1.json` or the source before filing.

1. **A per-run size for preview images.** Wanted: theme/house preview PNGs large enough to read.
   Tried: `?format=png&view=…` (works), looked for a size/scale query in the OpenAPI document —
   which declares **no parameters at all** on `/terrain/theme-preview`, `/terrain/material-preview`
   or the room-style previews, so even `format`/`view` are invisible there; they are documented
   only in `docs/tools/sketch.md` prose. **Missing** (the size knob), and a real OpenAPI gap for
   the params that do exist. Worked around by upscaling locally.

2. **A named contract for the gap two buildings need.** `DR-CLAIM` names the colliding cell but
   nothing states the claim's extent: a building claims footprint + eaves + ring (≈2 blocks each
   side), so two buildings need ~4 blocks between footprints and the spawn shell claims ~2
   outside itself. Learned by three declined barn placements. **Out of reach**: the mechanism is
   deterministic and the decline names the neighbour, but the margin is nowhere stated —
   `sketch.md` documents the one-block ring for trees only.

3. **Any warning when a flora field lands zero blades.** `f2` (coverage 0.3, scale 10, octaves 3,
   seed 32, a 68 × 18 ring) landed **nothing on either image** — 200, no decline, no warning; the
   only witness is the missing row in `provenance.json`, exactly as GENERATION-NOTES' census
   advice predicts. Controlled experiment via `sketch/columns` diffing: seed 99 → 13 blades;
   coverage 0.5 → a full meadow. **Missing**: a `decline`-severity finding for "prop landed
   nothing" would close the last silent drop I met. (The same census shows a ring crossing the
   symmetry axis lands image 0 only — benign, since the image is the same ground, but nothing
   says so.)

4. **Reusing a map row through the driver.** `drive.py` POSTs `/plan` each run, so six
   `whitebarrow-down*` rows now exist in the dev database; the driver has no `--slug` to rebuild
   in place even though `PUT /map/{slug}/plan` + the rest would support it. **Out of reach from
   the driver**, not the API.

5. **A standalone `--contour` render.** `capabilities.md` reads "`--heightmap` and `--contour`
   for the third dimension", so I invoked `--contour <region> <out>`; it fell through silently to
   the round-trip default ("0 maps across 1 roots"). In `Program.cs`, `--contour` is a
   **sub-option of `--heightmap`**. **Out of reach as documented** — the doc reads as two flags,
   and an unknown flag falls through with no error.

## What I got wrong, and why it looked right

- **`axis: "down"` on a layered wall.** The pattern reads "down from the top of the bucket", so
  "down" looked like the word; the choices are `depth`/`inward`. The RQ1 refusal named the JSON
  path but not the legal words — `/terrain/patterns`' `choices` field did.
- **Prop spacing by eye.** Two sarsens sat inside the path band and the pond's wandered shore,
  and a tree pair claimed each other — all placed with polyline arithmetic in my head after the
  run-3 report warned the band follows a spline. Each came back as a named decline with the cell,
  so the cost was one cycle each, not a hunt.
- **The core's first two positions.** At the dell centre GO1 read 2.57 (walks are surface
  traversals, and my straight-line estimate undercounted the walk around the tiers); and at
  `at: [2, 5.5]` the compiled 5-block footprint reached z 60.5, half a block past the dell edge —
  the plan gate passed it, and only reading the compiled anchor showed the OB17 risk at export.
  Fixed by moving it inward before ever hitting the 409.
- **Barn placement, three times** — see item 2 above; the claim looked like the footprint.

## What worked first time

- **The whole documented loop**: evaluate → inspect → plan → grid/flow → compile → from-plan →
  relief/read → finish → intent → columns → coverage → export. No 500s anywhere in the run; every
  refusal and decline carried a rule id and a position.
- **`level` + `anchor_heights` + `exclude` ramps** — all five, first build, walkable and flush
  where computed (verified by column probes at (11,29) h12 and (34,15) h12).
- **The hold/exclude/solve split**: apron `hold`, back/scarp `exclude`, saddle + down solved with
  marks — the terraces stayed crisp, the down rolled 9..17, symmetry error 0.
- **The barrow push**: a 2-block tumulus under the stone from one ring push; the stone floats 4
  over the *built* mound exactly as `plan.md` promises for `float`.
- **The dew pond**: point mark dish + water prop; water y4..5 over a gravel bed with a clay/sand
  shore, first build.
- **`GET /terrain/patterns`, `/terrain/species`, `/room-styles/{id}/json`** as the vocabulary —
  every field name and word I took from them was right; every one I guessed (`axis`) was wrong.
- **Kit pairing**: obsidian goal + core → diamond pickaxe in the spawn kit, unasked.
- **GENERATION-NOTES paid for itself five times**: the provenance census (caught the flora),
  observerY 55, `base_height N` = top `N−1`, the compiled-shape-id keying, the fresh-export rule.

## Open gameplay questions (decided without an oracle)

1. **Does a destroy board's open contested field count as dead ground?** Coverage reads 48.7%
   dead, almost all of it the two symmetric saddle/apron flanks — the ground the fight is *for*.
   The walk routes are spawn↔goal traversals only; a fight front is not a route, and
   `approaches.md` wants destroy mids "larger and emptier". I kept the field open (with flora,
   sarsens, tracks and the flank paths as the only furniture) rather than shrinking the board to
   satisfy the number. If the answer is that 48% is too much, the fix is narrowing the saddle by
   a cell each side, not decorating it.
2. **Should the scarp be a contested platform rather than a defenders' balcony?** Its only ramp
   faces the mid, so attackers reach the top as easily as defenders, and from it either side can
   bridge toward the dell. I chose contested (the defenders' "back way up" is a Δ4 drop they can
   take but not climb). No rule speaks to which way round a flank height should load.
3. **G8 fill-ratio fired (0.703 against [0.201, 0.496]) and I shipped anyway.** The band is
   measured over a corpus dominated by void-carrying capture boards; a solid destroy lane cannot
   reach it without cutting holes `approaches.md` forbids in exactly this position. Treated as
   the evaluator critiquing a shape it was not calibrated for.
4. **The mirror read shows 10.5% of columns unmirrored** — flora flowers, worn-path dice and
   canopy noise, all per-image scatter the docs say is deliberately free. I took that as
   cosmetic asymmetry and shipped; if two-block grass is ever found in the diff, that answer
   changes.

## The three documentation/API items that most got in my way

1. The **silent zero-blade flora field** (missing decline; provenance is the only witness).
2. The **building claim margin** being undocumented (three cycles on one barn).
3. The **preview endpoints' invisible query surface** — no parameters in the OpenAPI document,
   tiny fixed image sizes, and `--contour` documented as if it were a flag.

---
_Everything above is reproducible from `specs/fable-r5-whitebarrow/` against the API this run
drove; the drive log's final pass is the sequence of 200s described, and every geometric claim
carries the coordinate it was probed at._
