# firnline — measured record

DTM, snow and mountains. `rot_180`, cell 5, 16 players, board **90 × 200** (frame −50..50 × −105..105).
A lane per B188: valley floor at 9 down the middle, built terraces excluded from the relief, one obsidian
`pillar-3` monument per team on a checker forecourt shelf.

## The numbers that were designed to, and what was measured

| Measure | Designed | Measured |
|---|---|---|
| Board | lane, one dimension < ~90 | 90 wide × 200 long |
| Spawn → own monument (straight) | 25–50 band | **43.2** — spawn (−2.5, 97.5), monument (22.5, 62.5) |
| Enemy spawn → that monument | ~3× own | **161.2**, ratio **3.7** (corpus median 2.9, p90 5.0) |
| Monument approaches | ≥ 2 angles | 3 — village terrace (Δ1), steps chain Δ1×3 from valley, moraine flank overlooks it |
| Heights | Δ1 walk chains, Δ2–3 defended ledges | tiers 8/9/10/11/12/13/15; steps-lo→hi→shelf all Δ1; moraine Δ3 face over valley |

## Provenance census (`region/provenance.json`)

`spawn 4` (two halls + two iron cubes) · `house 6` (h1 L-wing alpine ×2, h2 two-storey porch alpine ×2,
h3 alpine ×2) · `destroyable 2`.

## What it exercises

- Six themes over ten shapes: `cell` snow/ice on the frozen tarn basin, `layered` snow-over-coarse-dirt on
  the valley, `turbulence` scree on the moraine, timber-rimmed village terraces, `checker` forecourt.
  Rim **off** on grown ground, **on** for the built tiers only.
- Relief on the valley tier alone (everything built is `relief_scope: exclude`): two point mounds, grain
  1.3/11, `stairs: true`. Read-back: 1741 solved cells, low 8, high 11, symmetry error 0.
- Two `anchor_heights` ramps onto the mid knoll (fanned rotationally — the access pinwheels).
- The enclosed void pocket (30×10) between village brow and steps is the CT8 rotation device, fanned to
  both halves; no build zones and no void enforcement, so crevasse bridging is a deliberate build-around.

## What went wrong first, in order

1. `mirrors: false` mid pieces touching team land — evaluate said valid, compile said an anonymous 400.
   Now `PL12` (fixed in the studio this run). Authored fix: the mid is half-pieces the fan completes.
2. Marker parity refusal (`at: [1.5, 1]`) — the pad is square; both offsets must share parity.
3. h2 dropped by the street's *spline* (the drawn polyline cleared it; the Catmull-Rom didn't).
4. h1's wing shared its hall's edge row (`HJ1` — corners are inclusive), then tied ridges (`HJ3`) until the
   wing stated `ridge: AlongZ`; preview said nothing at the time — it refuses now (fixed this run).

Soft evaluator terms accepted: `fill-ratio` 0.628 over band [0.201, 0.496] — a snow lane is dense by
design; the crevasse pockets are the concession.
