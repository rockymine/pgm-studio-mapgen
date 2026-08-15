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

## The house styles do stamp

`specs/grok-ridge/style-previews/` holds the studio's own plan, section, isometric and cutaway of all three
of Grok's styles, taken through `POST /api/room-styles/preview-snapshot` from his JSON. `ridge-hall` builds
the building `authored-by-grok/THEME.md` describes — stone-brick base, andesite body, spruce-log posts,
arched door head and windows, grey stained-clay roof with a ridge cap — and `ridge-cottage` and
`wool-shelter` come out as the hip and the shed the same document claims. Nothing here needed
approximating; the styles are complete, and the reason no building stands on the map is the props file's
footprint, not the styles.

`wool-shelter` states `"gableWindows": null` and `"doorHead": null` to mean "neither of those parts". Both
are non-nullable properties with an initializer, so the stated null bypasses it and `HouseStamper` throws
`NullReferenceException` — a 500, not a named refusal. Previewed with `{"form": "none"}` in their place,
which is what the document meant.

## The paint is an approximation, and it is grey

`specs/grok-ridge/approximated-theme.json` writes THEME.md's palette table as two real terrain themes —
`ridge-stone` for the terraces, `ridge-crest` for the two top rows — and `renders/10-topdown-material-painted.png`
is the board under them. The block ids are Grok's; which block is rim, which is surface, which is the
exposed riser and how deep each band runs are not stated anywhere and are mine.

What the painted board shows is that his stated ground palette is three greys — andesite, stone brick,
cobblestone — so the terraces read as one flat field from above and the tiers are legible only by their
risers. The colour in his palette is all on the buildings: spruce posts, grey stained-clay roofs, glass
panes. Nothing named a terrain theme, so the committed world paints with the built-in default.

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
