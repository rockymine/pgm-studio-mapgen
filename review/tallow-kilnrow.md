# Tallow Kilnrow — a destroy board on a lime works

**In one sentence:** a lime works cut into a red-clay hillside, with a core sunk in a slake pot at the
west end of the kiln row and a destroyable standing on a leaning stack of burnt lime at the east, and a
flue cut across the burnt floor between them that is meant to be bridged.

134 × 190 blocks, `rot_180` about the origin, base surface 10, build ceiling 32, y 0..45. One core and
one destroyable a team — the ordinary combined destroy board `capabilities.md` measures (16 of the 17
corpus maps carrying both have exactly one core a team). `<gamemode>dtm dtc</gamemode>`,
`<objective>Destroy the enemy's monuments and leak the enemy's cores!</objective>`.

## Two goals, placed against each other, and unlike on two axes

`approaches.md`: where a board carries more than one goal they are placed **against each other rather
than scattered** — a west and an east, or two forward with one back — and their spacing decides whether
the defence is one line or three. These are a west and an east, both 55 blocks forward of the spawn and
70 apart, so the defence is two lines and the attacker chooses which to make the defenders split for.

They are deliberately not the same problem twice, and the difference runs on two axes rather than one:

| | Slake Pit (core) | Lime Kiln (destroyable) |
|---|---|---|
| where | `(-37..-32, 17..22, -57..-52)` | `(34..38, 27..31, -56..-52)` |
| stands on | a `sink` pot cut into the works' west face, floor y10 | a `raise` stack leaning out of the burnt floor, top y20 |
| reaching it | **cheap** — the pot's south lip is two blocks below the floor around it; walk in | **expensive** — nineteen blocks above the floor; climb the stack's south face or bridge |
| breaking it | **expensive** — `float 6` against `leak 10`, so four blocks of ground come out under the casing before it runs | **cheap** — end stone, against the diamond pickaxe the core has already forced into the kit |

The kit is one kit, and that is what makes the pairing readable: `DestroyKitPairing` upgrades to a
diamond pickaxe because the board carries a core, and the destroyable's end stone is then soft against
it. A defender cannot spend the same attention on both.

## The flue is bridgeable, and that is the opposite call from Tallow Mirefast

The flue is a curved `subtract` across the burnt floor, `x −44..44`, about fourteen blocks across, with
its ends stopping short so the two ways round it are the flanks. A build zone `min="-45,-40"
max="45,-15"` covers it, so it is crossable from the first minute at the price of the time a bridge costs
and the visibility of building one. `approaches.md` says both are legitimate and that a channel cut
without deciding which it is has had half of it decided by accident; Mirefast's ditch is permanent and
this one is not, on purpose, so the two boards ask different things of an attack.

The measured effect is in the traversability read: **1 656 navigable columns are bridged over void**,
against 0 on Mirefast, and the board reports 2 components with 0 isolated objectives.

## What the ground is made of

Five themes. The identity is *red clay and quicklime*: everything cut is banded clay, everything built is
white.

| Theme | On | Says |
|---|---|---|
| `kiln-yard` | the crest the spawn stands on | white-clay rim, a red-sandstone/sandstone `checker`, a `wallFrame` inking quartz round the riser's corners |
| `kiln-works` | the kiln terrace and both haul roads | quartz rim, a quartz/white-clay `checker` over two sandstone, a `wallRun` of red sandstone → smooth sandstone → quartz pillar → orange clay |
| `kiln-floor` | the burnt floor and the mid | **rim off**, a `noise` ramp black clay → gravel → grey clay → coarse dirt → hardened clay, and **the strata riser** below |
| `kiln-pit` | the slake pot and the old clay pit | orange-clay rim, a `voronoi` of orange / red / hardened clay / clay, clay fill |
| `kiln-stack` | the kiln stack and the two slag heaps | quartz-pillar rim, a `cell` of quartz / chiselled quartz / white clay / smooth red sandstone / light-grey clay, a `wallDiagonal` of the same |

The strata riser is the piece worth naming. Every face the works cut into the hillside is painted with
one `layered` stack — red clay ×1, orange ×2, hardened ×1, brown ×3, white ×1, grey ×2, stone ×6 — so a
cut bank shows bands the way badlands clay does, and the same stack appears on every drop on the board
because it is bound to the floor's theme rather than to a shape.

## The buildings

Four styles, and the first thing an eye reads is that they are three different proportions on one
frontage line. The **draw kiln** is long and low, red sandstone banded with orange clay under a quartz
course, an arched window and an arched door head. The **hoist tower** is narrow and two storeys, red
sandstone under quartz, with beams reaching two blocks past every corner where the storeys meet. The
**lime store** is squat with a shed roof and a two-block overhang, hardened clay under white. The
**office** is the spawn: red sandstone under a quartz cornice, hipped, no timber.

Seven of them stand on one line at `z −67..−62`, squared to the tramway that runs along `z = −70`, with
the two hoist towers breaking the line's height at its middle rather than at its ends. `--structures`
reports **20** structures — 7 × 2 buildings, 2 spawn cubes, 2 goal markers, the core and the destroyable
— so every building stamped on both orbit images.

Six quicklime blocks are stacked in a line along the tramway's north kerb at `z = −74`, twenty blocks
apart, alternating `cairn` and `angular` in quartz and chiselled quartz. Spoil is stacked where a cart
could reach it; that is the answer to *why here*, and it is why they are on a line and not scattered.

Nine acacia stand on the two pieces of ground the works never burnt: the west bank above the spoil line,
inside the scrub the flora ring already covers, and the contested mid. Nowhere else on the board has a
tree, because everywhere else was fired.

## What went wrong

**The `k-pan` area mark and the pot overlap, and the pot won by less than intended.** `sink` measures
from the **median** of the ground under its own footprint, and the pot's footprint straddles the works
terrace (15) and the burnt floor (11), so the median is about 13 and a `base_height` of 4 puts the floor
at 9–10 — two below the floor around it rather than four. The section at `x = −35` shows it: the pot
reads as a shallow bay cut into the terrace's face rather than as a pit. It is the shape I wanted for
"cheap to reach" and it is not the depth I asked for, and the difference is only visible in a vertical
cut.

**`--surface` cannot read this board.** Most of it paints magenta — "unnamed material" — because
`TerrainPalette`'s nineteen tone families cover only eight of the sixteen stained-clay data values and
none of the four this board leans on (159:0 white, 159:7 grey, 159:8 light grey, 159:14 red). The board's
blocks are exactly what was asked for; the read-back simply has no family to sort them into.
`--topdown --material` reads it correctly and is in `renders/04-material.png` beside the broken one,
which is kept because the failure is the finding.

**The destroyable's own column is unpainted stone under its bedrock plate.** Probed at `(35, -55)`: stone
y1..20, bedrock y21, end stone y27..30. Painting runs after every stamp and skips a column whose top is
not terrain, which is correct and documented; the consequence is a six-wide grey patch visible only in
section.

## Coordinates

| Thing | Position | Reading |
|---|---|---|
| red Slake Pit | `(-37..-32, 17..22, -57..-52)` | obsidian casing y17 and y21, lava y18..20; pot floor y10 |
| red Lime Kiln | `(34..38, 27..31, -56..-52)` | end stone, `cube-4`; bedrock plate y21, stack top y20 |
| sky markers | `(-35, 36..38, -55)` and `(35, 36..38, -55)` | red wool, above the cap |
| the flue | `x -44..44, z ≈ -37..-16` | void; probed at `(0, -25)` — no block at any height |
| build zone over it | `min="-45,-40" max="45,-15"` | 1 656 columns bridged over void |
| the kiln row | `z -67..-62`, `x -58..48` | seven buildings, one frontage |
| the tramway | `z = -70` | solid voronoi paving, radius 2 |
| the spoil line | `z = -74`, `x ±26, ±36, ±46` | quartz cairns and angular blocks |
| the settling pond | `(14..32, -38..-33)` | in the old clay pit, natural form, 2 deep |
| west spoil ridge | `(-60,-50) → (-52,-28)` | a `line` mark falling 14 → 10 |
| traversability | — | 22 167 navigable columns, 2 components, **0 isolated** |
| observer | `(-58, 44, -60)` | over the works' west end |
