# Grok Ridge — the measured record

> A CTW board of three terraces and a crest, cut by a mid build band, with one wool room per side reached
> off the terrace it stands beside. Authored by Grok with no live studio; built here from its plan with one
> rect corrected.

140 × 220 blocks, `rot_180` about the origin, base surface 12, build ceiling 42, y 13..53. Seventeen
pieces at eight surfaces — 14, 15, 16, 18, 19, 22, 23, 24, 27, 28 — compiled to 19 shapes on one island.

## What was corrected, and nothing else was

`low-gate` was written `[-5, 2, 5, 4]` where its own row (`low-west`, `low-east`) is five cells deep. That
left a one-cell notch between it and `mid-gate`, and the plan's single `walls` entry names exactly that
pair, so the compile refused: *wall 'low-gate'–'mid-gate' is not a shared land interface*. Built as
`[-5, 2, 5, 5]`. Grok's README describes the wall as intended ("wall link between the low and mid gates"),
so the deeper gate is what the document meant.

The wall is visible in `renders/02-topdown.png` as the orange bar across the gate seam, one per team image.

## Measured

| | |
|---|---|
| gamemode | `ctw`, "Capture the enemies' wools!" |
| teams / spawns | 2 / 2, `rot_180` |
| wools | 4 — `red` at `(−60, 23, 95)` and `orange` at `(60, 15, 25)` for blue; `blue` and `light_blue` at the rot_180 images for red |
| build ceiling | `maxbuildheight` 42 (surface 12 + headroom 30) |
| traversability | 20 982 navigable columns, 2 364 bridged over void, 6 components, **4 of 4 markers isolated** |
| evaluator | score 7.1, `valid: true` — fill-ratio 0.609 (band .201–.496), frontline-width 17 (1–16), spawn-wool-ratio 1.588, wool-front-ratio 2.364 |

**The four isolated markers are the four wool cages**, and this is the documented reading rather than a
fault in the board: a stamped wool room is a walled shell, `--traversability-map` models ground-level
walking with headroom, and a cage therefore reads as its own component. The precedent is `FINDINGS.md`
(ClayClay Redux) and `review/sable-marsh.md`. The compile gate's own reachability rule — a wool reachable
from every capturing team's spawn without passing through a spawn piece — passed on this plan.

## What is not here

Grok's own `grok-ridge.layout.json` was not used: all thirteen of its shapes carry `x`/`z`/`w`/`h`, which
the rasterizer does not read, so the document builds no ground at all (`reports/grok-run1.md` §2). Its
geometry is the plan's geometry, so the compiled layout is the same board.

The dressing is in `specs/grok-ridge/grok-ridge.dressing.json`, translated from Grok's props into the
real prop model at ×5 (cells → blocks). Only the four spruce landed: all seven houses are over the
192-block² footprint cap once scaled — `spawn-hall` covers 1 500 — and a house past the cap is dropped in
silence. `renders/06-topdown-dressed.png` is that build; the paths are stone-paved and so read as ground
in the category colouring.

No terrain theme was authored. Grok's layout names `stone-terrace` / `stone-crest` / `stone-strand` on its
shapes but no `themes` registry defines them, so the board paints with the built-in default.
