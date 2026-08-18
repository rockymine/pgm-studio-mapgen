# Alabaster Rake — a gypsum badland, and the wall that raises its own ceiling

**In one sentence:** a bone-white gypsum pan under a mesa, where each team's monument stands on a made brow
above the pan, and the two ways at it are a weave through a picket of banded hoodoos or a drop into a sunk
hollow and up under the brow.

100 × 190 blocks — a **lane**, one dimension meaningfully shorter, which `AD-B2` asks of a destroy board and
which no generated board here has ever been. `rot_180`, base surface 9, build ceiling 42, ground y6..22.
One island, 4 703 cells, y8..14, symmetry error 0.

## Where each thing is, measured

| Thing | Where | Read at |
|---|---|---|
| spawn | `x −10..10, z 75..90`, door −Z | mesa behind it at h12 |
| monument | `column-plus` in **end stone**, anchored `(5, 47)` on the brow | `(5, 47)` end stone y15..17 |
| sky marker | above the built cap | `(5, 47)` red wool y48, cap 42 |
| goal-to-own-spawn walk | 45 blocks | `POST /plan/inspect` |
| goal-to-enemy-spawn walk | 145 blocks | ratio **3.22** — `GO1` wants 3.0–4.0 |
| the hoodoo picket | five circles r 2.5–3.5 at `x −40..−12`, `z 30..37`, top y21 | `(−40, 31)` 22 solid, banded |
| the sunk hollow | a `sink` polygon, skirt 3, `x 2..24, z 28..42` | visible in `11-section-z33.png` |
| the east shelf | tilted `11 → 9` from the brow down to the pan | `anchor_heights [9, 10, 11, 11]` |
| the seam | pieces stop at `z = 10`; the gap is `z −10..10` | 20 blocks of void, one build zone across it |

Traversability: **10 190 navigable columns, 764 bridged over void, 2 components, 0 isolated.**
`<gamemode>dtm</gamemode>`, `<objective>Destroy the enemy's monument!</objective>` — the label per team, not
per fanned list.

## The three approaches are three dimensions

`approaches.md` asks that the ways at a goal differ in kind rather than in flavour, and this board's three do:

- **through** — the west half of the pan is crossed by the hoodoo picket. Nothing walks over a 13-block
  pillar, so the west approach is a weave whose gaps a defender on the brow can watch one at a time.
- **below** — the east half carries a `sink` depression with a half-buried shed in it. A player drops in out
  of sight of the brow and comes up under it. This is the instrument `approaches.md` names as the
  replacement for the withdrawn mid-terrain void hole, and it is what the brief for this board was built to
  test.
- **above** — the east shelf tilts from the pan up to the brow's own level, so an attacker who takes it
  arrives level with the goal rather than under it, and pays for that with the longest walk of the three.

The void is at the **seam**, twenty blocks across between the two teams' lands, and nowhere else on the
board's own approaches — which is the amended rule, and the one `tallow-kilnrow` broke.

## The hoodoos do not do what the capability document says they do

They were authored to be **un-bridgeable**: `capabilities.md` describes "an erected cube as a blocker … a
shape given a `height_mode` of `level` at an absolute height above the cap … a wall made of terrain", and a
picket over `max_build_height` would have been exactly that.

It cannot work. The ceiling is `BuildCeiling.Of(highestGround)` where `highestGround` is the tallest
**terrain** column the world builds (`SketchWorldBuilder.cs:114`), and an erected shape is a terrain column.
The first build of this board put the picket at `base_height: 44` and wrote
`<maxbuildheight>64</maxbuildheight>` — **twenty-one blocks of clear air over the wall that was meant to be
unbuildable-over**, and a 64-block ceiling on a board whose real terrain tops at y14.

The picket now stands at `base_height: 22` and the ceiling is 42. It is honestly what it is: an obstacle
nobody climbs, which players may bridge over at the cost of the material and the visible time it takes.
That is still a real device. It is not the one the document promises.

## What the ground is made of

Six themes. **Ground** is `sand` (the pan, the mesa); **built** is `pale stone` (the brow, the hoodoos);
the **accent** is `rust`, spent on the wash at the front, on the strata band that runs through every riser
and every hoodoo, and on the paving of the east road.

| Theme | On | Says |
|---|---|---|
| `rake-pan` | the gypsum pan | rim off, a `cell` of sand, end stone and white clay at pan scale |
| `rake-wash` | the front strand | rim off, a `noise` of red sand and orange clay — the one warm ground |
| `rake-mesa` | the mesa | rim off, a `noise` of end stone and mushroom stem, plainly whiter than the pan |
| `rake-brow` | the brow the monument stands on | rim **on**: a made lip, over a `voronoi` of polished diorite, diorite and stem |
| `rake-hoodoo` | the five pillars | a `layered` depth stack in **both `surface` and `fill`**, so the bands run the whole column rather than its top four courses |
| `rake-works` | the spawn terrace and its ramp | rim on, a 4-block `checker` of sandstone and white clay |

The wall bucket of every one of them is the same `layered` strata stack, which is `AD-P7`'s rule — one
material system per role, everywhere the role recurs — so a mesa face, a brow lip and a hoodoo's flank are
the same rock read at three scales.

## The buildings

Four, forking two presets by proportion. `Desert` was read before it was changed, exactly as the desert brief
asks of it: end stone over sandstone in a two-band wall, a brick gable, and **`Sill = Air`**, the one preset
that models the rule twelve earlier boards broke.

| Prop | At | Is |
|---|---|---|
| `h1` kiln | `x −30..−18, z 54..61` | an **L** on the mesa's west end, hall ridge `AlongZ`, wing `AlongX` |
| `h2`·`h3` sheds | `x 18..27` and `x 28..34`, `z 52..57` | a **run as a boundary**, sharing a frontage line, differing in footprint |
| `h4` sunk shed | `x 8..14, z 29..34` | down in the hollow, so it reads half buried — which is the point |

Three trees, all acacia, all on the mesa, because `AD-M9` says a tree stands on soil and the pan is stone.
The pan's only cover is three gypsum boulders in the hoodoos' own banded rock.

## What went wrong

**`HJ4`, then `HJ5`.** The kiln's hall is roughly square, which ties its ridge `AlongX`; the wing then also
ran into the shared vertical edge, and both-into-it is `HJ4`. Stating the **hall's** ridge along the shared
edge fixed it. `POST /terrain/prop-preview` answers this before a build — its body is `{propJson, themeJson}`
with the documents as strings and the style resolved, which is not what `capabilities.md`'s "each takes the
document it previews as the body, unwrapped" implies.

**`OB19` twice, both times at export.** The shed run and then the kiln stood inside the goal's clearance —
a 10-block square about the anchor, tested against a footprint **plus its eaves** and against every orbit
image. Neither appeared in the pre-build decline read, because `OB19` is a refusal raised by
`MapExportComposer` rather than a dressing complaint. Two whole build cycles.

**Three themes were silently wrong.** `noise` takes `stops` and not `palette`; `voronoi` takes `bands` of
`{material, depth}` and not `palette`; `layered`'s axis is `depth` or `inward` and there is no `inset`. Each
answered **200 with a flat swatch**. `GET /terrain/patterns` names every field and was the fix.

**A 44-block hoodoo was banded in its top four courses.** `surface` claims a stated depth and `fill` takes
the rest, so the strata stopped at y40 and everything below was plain sandstone. Putting the same `layered`
stack in `fill` carries the bands the whole way down — `(−40, 31)` now reads stem/stem/sandstone/sandstone/
stem/stem/sandstone×3/orange clay/red sandstone from y21 down.

## Where it is weak

The pan is large and its only relief is one `line` mark, one `point` and a `push` dune. `AD-L6` says a large
open area wants level changes rather than more props; the hoodoos and the hollow are those changes on two
thirds of it, and the strip between the wash and the picket is still flat.

Three trees is the whole of the board's foliage, which is correct for a desert and means the canopy share is
near zero — a legitimate answer rather than an omission, but it should be read as chosen.

## Open questions

**Should a picket of pillars be bridgeable?** Built at a height that can be bridged, because it cannot be
built at one that cannot. If erected terrain *should* be excluded from the ceiling derivation, this board
wants rebuilding at 44 and the studio wants changing; the decision is the author's and is filed as such.

**Is a depression a fair replacement for a void hole in front of a goal?** The hollow here is 22 × 14 and
about 4 deep, and a player in it is out of sight of the brow but not of the mesa behind it. `approaches.md`
withdraws the hole and names the depression; it does not say how deep or how close. Chosen by eye.
