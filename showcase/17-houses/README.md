# 17 — several buildings, one settlement

**The technique: six houses stamped from six forked presets — one genuinely applied fork, one L-wing joint,
five of the six roof forms, and a sealed shell used as a boundary rather than a room — placed so the result
reads as a village built by one culture rather than a swatch of everything the stamper can do.**

The plan is `02-theme`'s, untouched. The finish gains a `dressing.props` list of six `house` props and nothing
else; the meadow, the buildings and the two bound room styles (`@showcase-hall`, `@showcase-cage`) are
untouched.

## The document

```json
"dressing": { "props": [
  { "kind": "house", "id": "croft",   "seed": 101, "points": [[-39,17],[-33,25]], "front": "posX", "style": "@17h-croft" },
  { "kind": "house", "id": "hall",    "seed": 102, "points": [[27,17],[35,29]],   "front": "negX", "style": "@17h-hall" },
  { "kind": "house", "id": "barn",    "seed": 103,
    "wings": [
      { "corners": [[-39,38],[-32,50]] },
      { "corners": [[-31,42],[-27,45]], "spec": { "form": "shed" } }
    ], "front": "negZ", "style": "@17h-barn" },
  { "kind": "house", "id": "granary", "seed": 104, "points": [[27,39],[35,47]],   "front": "negX", "style": "@17h-granary" },
  { "kind": "house", "id": "vault",   "seed": 105, "points": [[34,62],[39,67]],   "front": "negX", "style": "@17h-vault" },
  { "kind": "house", "id": "coop",    "seed": 106, "points": [[-40,62],[-35,68]], "front": "posX", "style": "@17h-coop" }
] }
```

Six new style files sit in `tools/styles/`, each a fork of one shipped preset (`GET /api/room-styles`):
`17h-croft.json` (from `cottage`), `17h-hall.json` (from `townside`), `17h-barn.json` (from `workshop`),
`17h-granary.json` (from `alpine mining`), `17h-vault.json` (from `terrace`), `17h-coop.json` (from
`diorite pyramid`).

## How the mechanism works

A `house` prop is a footprint and a `HouseStyle` snapshot, nothing else. The footprint is `wings`, a list of
`AuthoredWing` — each one two opposite corners plus an optional per-wing `WingSpec` — and a bare `points` pair
is upgraded on read into a one-entry `wings` list, which is the shorthand every single-rectangle house in this
map uses. `front` names the wall the door opens in, stated once because a prop has no room frame to derive an
entry from the way a spawn or a wool room does. `style` is either an inline `HouseStyle` object or an
`"@name"` string that loads `tools/styles/<name>.json` at read time — the mechanism that keeps this finish
seven lines long instead of carrying six full shells inline.

**A wing composes into one building, not several.** `barn`'s two wings share the edge at `x = -32/-31` whole —
the lean-to's four-block depth (`z 42..45`) lies entirely inside the hall's thirteen-block one (`z 38..50`) —
so `WingJoints` reads them as a single junction rather than two buildings standing near each other, and the
stamper paints one continuous outline, one set of corner posts, one door. The lean-to's own `spec.form:
"shed"` overrides only its own roof; every other field — wall, windows, post — is the building's, because a
wing states only what it needs to and wears the rest of the style it belongs to. Whether the wing's roof
*marches* into the hall's (each course stepping up until it meets the hall's own slope, drawing a valley) or
*projects* through it is `WingSpec.Projects`, and it defaults to marching — which is what every corpus L is,
and what `barn` is here.

**Five of the six roof forms carry a reason, not a rotation through the enum.** `RoofForm.Flat` is the one
form that can carry a hole and the one that reads as a lid rather than a peak, which is exactly what `vault`
wants. `RoofForm.Shed` is a single falling plane — the lean-to's own form, because a lean-to that shared the
hall's gable would just be a smaller version of the same building rather than a wing added onto it.
`RoofForm.Gambrel` climbs at two rates (`RoofField.Gambrel`: steep for the first course off the eave, `pitch`
per block after) — the barn-roof profile a granary wants for the loft space a plain gable would waste.
`RoofForm.Hip` has no gable end at all, which is what keeps a five-by-six shed from reading as a doll's-house
version of a bigger building. `RoofForm.Gable` is what is left when nothing else is asked for, and it is what
`croft`, `hall` and the hall-wing of `barn` wear, because a village of six roof forms and no repeats reads as
a demo board rather than a place.

**Every roof in Ganton is laid in Bricks (`45:0`).** Six different wall recipes — grey stone and dark oak for
`croft`/`hall`/`barn`, sandstone and oak for `granary`/`vault`/`coop` — under one unchanging roof material is
what makes six different footprints read as one settlement rather than six unrelated stamps: the walls are
each house's own answer, the roofline is the whole village's.

## The fork that repainted nothing, measured

The first `hall` fork changed exactly one field: `wall.stack.bands` at the top of the style, from `townside`'s
plain plank band to a stone-brick recipe. `HouseStyle.Levels` resolves a storey's wall as `storey.Wall ??
Wall` — and `townside`'s own two storeys **both name their own `Wall`**, so the top-level field is never asked
for on this building. Rendered against `POST /api/room-styles/preview-snapshot?format=png&view=section`, the
naive fork and the unmodified `townside` preset are **byte-identical**:

```
sha256(naive-hall-section.png) == sha256(preset-4-section.png)   →  True   (1807 bytes, both)
```

The fix touches `storeys[0].wall` and `storeys[1].wall` as well as the top-level field. The corrected section
(`renders/house-hall-section.png`) shows two visibly different bands — Stone Bricks/Andesite below, Dark Oak
Planks/Log above — and the column read below confirms it landed in the built world, not only in the preview.

## The L that was two ranges side by side, once

Before `barn`'s lean-to was given its own proportions, an earlier draft stated `"ridge": "alongZ"` on it —
forcing its ridge to run parallel to the hall's rather than into it. `POST /api/terrain/prop-preview` refused
it outright:

```
HJ3  both ridges run along the edge they share, which is two ranges side by side meeting in a gutter
     rather than a valley; turn one of them across the other
```

Dropping the `ridge` override let the wing's own proportions (5 wide × 4 deep) pick `RidgeAlongX = true` on
their own — perpendicular to the hall's — and the pair joined clean, no fault. The lesson `WingJoints` is
built to teach: a cross-wing is legal exactly when its own shape, not an author's stated preference, points
its ridge into the shared edge.

## Two buildings that corked their own passage, twice

The first `barn` placement ran the full width of its own corridor — flush against the map's void edge on one
side and one column short of the pond on the other. `DressingRules.PassAround` grows a five-block band off
*every* side of a building's bounding box, corner steps included, and needs **one whole side** clear:

```
DR-PASS  building 'barn' leaves no way past it: fewer than 5 blocks of passable ground beside every side
```

Every side failed at once: west met the void five blocks out, east met the pond, and north/south both ran
past the void corner on their way round. The fix was not to move `barn` — there was nowhere in that corridor
to move it to — but to **narrow** it: the hall wing dropped from 9 to 8 blocks and the lean-to from 6 to 5,
freeing one column of real ground on the void side for the pass-around band to stand on. The same fault, for
the same reason, hit a first, wider `granary` (13 × 9): its own north flank needed ground one column past the
island's actual edge. Shrinking it to 9 × 9 — which is also what gave the gambrel roof enough span for its
kink to read as two rates rather than one — cleared it.

## What the dressing pass declined, provoked and honoured

A decoy boulder dropped on `barn`'s own footprint and a decoy tree dropped in `hall`'s door lane, each
declined on contact and neither built:

```
DR-CLAIM  boulder 'decoy-claim' rests on (-36, 40), claimed by the building 'barn'
DR-KEEP   tree 'decoy-keep' rests on (-20, 62), which is kept clear as the approach in front of a door
```

Both were authored purely to provoke the finding and removed once quoted; neither appears in the shipped
`dressing.props` above, and the final run declines nothing.

## The vault: a building used as something other than a place

`vault` is `RoofForm.Flat` with `overhang: 0` and `hole: false` — a lid, not a light well — over four courses
of Sandstone banded with White Stained Clay. It reads as a sealed block rather than a house, and the column
read confirms it is exactly that: a shell, not a filled mass.

```
column (34, 64)  the wall              column (36, 64)  one step inside
  y 14  Sandstone                        y 14  Bricks           ← the lid, directly over the floor
  y 13  White Stained Clay               (y 9–13 air)           ← nothing between floor and lid
  y 12  White Stained Clay
  y 11  Sandstone
  y  8  Stone Bricks   ← the floor       y  8  Stone Bricks     ← the same floor
```

The wall stands from floor to lid; one column in, there is nothing between them. Filling a stamped shell is
`B92`'s open half — the pass raises the box, not what is inside it.

## What to look at

| Picture | Says |
|---|---|
| `renders/world-ground.png` | the whole settlement: six roofs ringing the pond on both sides of the strait, three tone families apart from the meadow |
| `renders/world-topdown.png` | the same board by material class — `barn`'s L-shaped bite is visible as a single structure, not two |
| `renders/section-croft-hall.png` | `croft` and `hall` in one cut — one storey against two, gable against gable, and both hollow inside |
| `renders/section-barn.png` | the L's own joint: the hall's gable and the lean-to's shed meeting in a marched valley |
| `renders/section-granary.png` | the gambrel's two-rate climb, read in one cut through the ridge |
| `renders/section-vault.png` | the sealed lid, and the empty column beneath it |
| `renders/section-coop.png` | the hip roof's four-sided pyramid, no gable end anywhere |
| `renders/house-hall-section.png` | the fork actually applied: grey stone below, dark oak above |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` — the plan is untouched |
| provenance census | `house` × **12** (six authored × two team images) · `roomfloor` × 2 · `wool` × 2 · `redstoneline` × 2 · `spawn` × 2 — every authored building has a row |
| `GET …/coverage` | reached 7 979 · decorated **26** · dead **245** of 8 250 = **3.0%** — down from `02-theme`'s 3.3% (271 dead): the six houses' own footprints are exactly the 26 cells that moved from dead to decorated |
| `GET …/preflight` | round-trip, mirror, buildability and traversability all ✓ — export gate **OPEN** |
| `column (27,19)` — `hall`'s wall, plinth to ridge | Bedrock → Stone ×5 → Dirt ×2 → Oak Planks (floor, y8) → **Stone Bricks ×4** (y9–12) → **Andesite ×2** (y13–14) → **Dark Oak Planks ×3** (y15–17) → **Dark Oak Log** (y18) → Bricks (roof, y19) |
| `column (34,64)` vs `(36,64)` — `vault` | wall solid floor-to-lid; one step inside, air from y9 to y13 under the same lid — confirmed hollow |
| roofline rise, `granary` ridge cut, `z 39→43` | +2, +1, +1, +1 blocks per step off the eave — the gambrel's steep-then-shallow climb, measured rather than eyeballed |
