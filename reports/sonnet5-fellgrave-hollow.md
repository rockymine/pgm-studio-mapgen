# Report — `sonnet5-fellgrave-hollow`

## What I set out to build

A destroy board, `Fellgrave Hollow`: two highland mining camps dig for the same frost-locked relic in
a snowbound valley, each holding their find in a hollow cut into the hillside at the head of its own
dig. One destroyable a team (obsidian, `pillar-2`), a snow-capped valley finished by slope angle
(snow meadow → rocky shoulder → bare stone), a cold biome bound over it, one small taiga/podzol stand
kept off the grass, a single timber-and-stone spawn hut, and the mandatory team-to-team void dressed
as a frozen tarn that has cracked through at its centre. Deliberately one of the plainer, quieter
boards of the five: one plan piece worth of shape decisions (plus a junction stub), everything else in
the relief and three themes.

## What I could not say

Checked against `GET /api/openapi/v1.json` and the live API before writing any of this down, per the
brief's own warning that an agent's account of what it could not do is evidence about the surface, not
the system.

- **Why `EX6` fires on every drive despite the map carrying its authors correctly.** I wanted
  `intent.meta.authors` to read populated the way `GET /map/{slug}/xml` actually shows it
  (`<authors><author>Sonnet 5</author></authors>`, confirmed) and the way `GET /map/{slug}` shows it
  (`"authors": [{"name": "Sonnet 5", ...}]`, confirmed). `tools/drive.py`'s `patch_intent` only ever
  writes `intent.meta.created`; the `authors` value is passed as a **separate top-level field** to
  `POST /map/from-documents`, which the flow document says "applies the authors" as its own step after
  the intent projection. `EX6`'s own read (`POST …/sketch/columns`, called right after the store)
  reports the field empty anyway. This is **out of reach from where I was standing**, not missing: the
  finish schema documented in `tools/README.md` has no key that patches `intent.meta.authors` directly,
  and I could not find one in `GET /api/openapi/v1.json` either — every author-facing field lives on
  the outer `authors` list I already used. Since the actually-exported document is correct, I read this
  as a same-request ordering artifact in the observer-platform check rather than a real gap, and did
  not spend further budget chasing it.
- **Whether a `line`/`area` relief mark can state a per-cell paint scope of its own**, so a bowl's paint
  could be authored alongside its height in one place instead of a separate `addShapes` polygon
  tracing the same ring. Checked `ReliefMarkJson` in the openapi document: it carries no `theme` field.
  This is **missing from the system** rather than out of reach — paint is a shape concept only
  (`SketchShape.theme`), and a relief mark is a height-only primitive by design (`docs/world-export/
  relief.md`), so tracing the ring twice (once for the mark, once for the paint shape) is the current
  answer, not an oversight I could route around.

## What I got wrong, and why it looked right

**A `base_height: 1` paint patch drawn exactly to `GENERATION-NOTES.md`'s own documented safe form
painted nothing.** The note's worked recipe for scoping a theme to a patch of solved ground is
`operation: "add"`, `base_height: 1`, no `override` — "the ground, repainted." I drew the dig floor,
the shore band and the taiga patch that way. It looked right because everything downstream said so:
the compile printed the correct theme tally per shape, the store answered 200 with no `RQ3` and no
`SK*` complaint naming any of the three shapes, and the export gate opened. The built world painted
100% `frost-valley` regardless — confirmed by `GET …/themes/census` and by a direct `GET …/column` read
inside the hollow, which showed Gravel, a `frost-valley` band member, not the packed-ice mix I had
painted the hollow with.

The missing half is in a different document: `docs/world-export/terrain-painting.md`'s account of
`ShapeThemeOwners` — *"among the shapes covering a column, only those reaching its visible top may own
its paint; among those the smallest area wins."* A relief group solves ground far taller than a
`base_height: 1` patch (mine ran to 30–52 blocks), so the patch never "reaches the top" in that
ownership test, independent of the later height repair (`RasterizeLayout`'s `Max(floor+1, field)`) that
`GENERATION-NOTES.md`'s passage is actually about. The two mechanisms are evaluated at different
points and the note that documents one does not mention the other. The fix, once found, was one
number: stating `base_height: 60` (above the relief's own high of 52) on all three patches made every
one paint correctly, with **no change to the built geometry** — the height repair still clamps every
cell to the solved surface regardless of the stated height, so nothing floats or steps. I did not file
this as a task (out of scope for a single map's report), but it belongs beside the passage in
`terrain-painting.md` that names the mechanism, and as a correction to `GENERATION-NOTES.md`'s own
worked recipe, which is only safe when the covering shape's *own* stated height is comparably short —
true of the `07-hill` example it was measured on, not of a shape sitting on a tall relief-solved group.

**I read `SP2`'s complaint as something to fix before reading the rule's own text.** `POST
/plan/evaluate` flagged the spawn as "not near the back of its lane." `GET /rules?rule=SP2` names the
exact failure mode: *"the current lint approximates 'back' per-piece and misreads spawns placed
mid-chain."* My spawn piece is the literal furthest-back rectangle on the board (`z = -140`, the
board's own edge, nothing behind it) — a textbook case of the false positive the rule's own text
predicts, once the lane was split into several same-height pieces to satisfy `LN2`. Left as a known
complaint rather than a fault.

## What worked first time

- The `GO1`/`GO3`/`GO4` ratio arithmetic from `AUTHORING-BRIEF.md` §3 (`d ≈ L/5..L/4`) put the goal in
  band on the very first `--dry` evaluate: ratio 3.57 (band 3.0–4.0), own-spawn distance 54 (band
  40–90), opposing-goal distance 140 (band 85–150) — no iteration needed on any of the three.
- The "state the rim and the floor as two `area` marks" bowl idiom for the hollow, and the "two long
  push rings" idiom for the flanking ridges, both built clean and legible on the first drive that had
  the right numbers; only the push's own two gradients (`RL6`) needed a second pass.
- The house-style fork (cobble base, one laid-log beam course, spruce infill, snow-capped gable, no
  footing) built and previewed correctly on the first store — no `HS*` refusal beyond the one windows-
  block mistake (`102`, a glass pane, where `stairLattice` wants a stair id; fixed to `134`, spruce
  stairs).
- The cold biome bound as a flat `solid` field with zero interaction with the theme's own slope bands —
  picked, stated, and never touched again.
- Dressing placed all 28 props (9 trees, 4 boulders, 1 path stroke, plus spawn/goal structures) with
  zero declines on every drive once the relief itself stabilised — no `DR-*` complaint was ever raised
  against a tree, a boulder or the path.

## Open gameplay questions decided without an oracle

**The void's finish: dressed void, or a walkable basin.** `docs/gameplay/approaches.md` requires the
seam between the two teams to be a real void spanned by a build zone, never solid land at any depth —
that half is law. The brief separately offered "paint it as ice … if you don't want it walkable, or as
a real water prop … if you do." I read these as two answers to the **same** question (how the void's
edge and near ground should be dressed) rather than a choice about whether the seam is void at all, and
decided the void stays void — a true gap, not a shallow walkable ice floor — with both banks themed as
the dig's own worked stone-and-packed-ice mix so the crossing reads as a frozen lake that has cracked
through at its centre rather than an arbitrary ditch. I did not add a literal `WaterProp` pool, because
a water body needs solid ground under it and the ground here is deliberately absent. A human oracle
might prefer the walkable-basin reading instead — a shallow ice-capped pan a player can cross on foot,
with the "hole" moved elsewhere — which would trade the destroy-topology law's letter for its spirit;
I judged the letter binding given how explicitly the brief and `approaches.md` state it, and recorded
the choice here rather than filing it as settled.

**Whether the flanking ridges' large "dead" share is a fault or a feature.** `coverage` reports 61.7%
of the board's ground as reachable but on no route between any two named features — almost entirely
the two flanking ridges (both teams). The brief explicitly asked for a "snow-capped highland valley"
with hills finished by slope angle, which reads as scenic, mostly unplayed backdrop by design rather
than graded flank routes a defender would actually use — `docs/gameplay/approaches.md`'s "a hill …
attackers climb to its ledge and bridge from there" describes a *tactical* hill, which this board does
not attempt, on the instruction to keep this one of the plainer boards. I narrowed the board from 140
to 100 blocks wide once (cutting dead ground from 71.7% to 61.7%) and judged further narrowing would
shrink the mountains into insignificance rather than into a route. A human oracle may want the ridges
cut back further, or a single graded shoulder route added on one flank; I left the valley wide and the
peaks decorative, and say so here rather than assuming it plays the way I intended.

## Deliverables

- `specs/sonnet5-fellgrave-hollow/` — `build-spec.py`, the plan/finish/layout/intent JSON, `renders/`
  (27 images + 16 text reads taken at every stage), `provenance.json`.
- `maps/sonnet5-fellgrave-hollow/` — `region/`, `level.dat`, `map.xml`. Export gate **OPEN**. The
  export wrote a `region/dressing-report.json` alongside the `.mca` files that `tools/drive.py` does
  not move out the way it does `provenance.json`; removed by hand to keep the folder to what a server
  is handed.
- `review/sonnet5-fellgrave-hollow.md` — the board, the void decision, the themes, the techniques, what
  went wrong, coordinates.
- This report.
