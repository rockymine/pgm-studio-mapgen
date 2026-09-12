# Grok Ridge — map model

A simple Capture-the-Wool board authored by following the `pgm-studio` / `pgm-studio-mapgen` pipeline.

## Intent

- **Mode**: CTW (two teams, rot_180 symmetry)
- **Players**: 24 max
- **Board**: three main terraces + crest, cut by two narrow void ravines
- **Objectives**: one wool room per team (west high, east low) + central mid band
- **Spawn**: on the crest platform

## Documents produced (the four levels)

| Level | File | Notes |
|-------|------|-------|
| Plan (board + meaning) | `grok-ridge.plan.json` | Hand-authored rectangles, roles, placements, walls. Ready for `POST /api/plan/compile` or `PUT /api/map/{slug}/plan`. |
| Layout / Sketch (geometry) | `grok-ridge.layout.json` | Minimal but valid shapes carrying the required `type` / `operation` / `floor` fields (the silent-failure trap from GENERATION-NOTES §1). Themes are placeholders. |
| Intent | (would be produced by compile + Configure) | Teams, spawns, wool colours, protections. |
| Built map | (requires running studio) | `map.xml` + Anvil world + provenance. |

## How to continue (on a machine with the studio)

```powershell
# From pgm-studio-mapgen/tools
. .\drive.ps1
$slug = New-PlanMap -Name "Grok Ridge"
Set-MapPlan -Slug $slug -File ../artifacts/grok-ridge/grok-ridge.plan.json
# then compile, push layout, finish sketch, set intent, Export-Map ...
```

Or open the Blazor UI at the map's plan/sketch stages and refine.

## Design notes

- Cell size 5, surfaces step 12 → 16 → 20 → 24 → 28 (classic terrace language used by marlstone-steps).
- Two ravines declared as zones so the compiler keeps them as voids.
- Wall link between the low and mid gates.
- All shapes have explicit `type` so rasterization cannot silently produce empty islands.
- Themes are deliberately generic (`stone-*`); a real run would pull concrete block palettes from the library or inject them post-compile as the ClayClay recreation did.

This is the exact grain an agent or human authors *before* the studio turns it into voxels.
