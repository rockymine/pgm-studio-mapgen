# Fellgrave Hollow — two digs, one frozen tarn

> A snow-capped highland valley: two mining camps follow the same frost-locked seam up opposite
> flanks, each holding its find in a hollow cut into the hillside at the head of its own dig. The
> valley narrows between them to a frozen tarn whose centre has calved into the void every destroy
> board needs at the seam between two teams.

**In one sentence:** two highland mining camps dig for the same frost-locked relic in a snowbound
valley, each holding their find in a sheltered hollow at the head of their own dig.

124 × 280 blocks (62 × 140 cells, cell 2), `rot_180` about the origin, base surface 10, build
ceiling 72 (`y 0..72`). One fused landmass a side — the spawn hut's piece and the three ground
pieces share the plan's implicit surface, so they compile to a single polygon, and the whole climb,
the hollow and the flanking ridges are stated in the relief rather than in a second plan piece.

## Where the brief's things are

| The brief asked for | Where it is | Measured |
|---|---|---|
| destroy, one goal a team, kept simple | one `<destroyable>` a team, `pillar-2`, obsidian | `<cuboid id="frozen-relic-region" min="0,9,-70" max="1,11,-69"/>`; `<gamemode>dtm</gamemode>` |
| remote spawn, short walk to the goal | spawn hut at `(0,-124)`, goal at `(0,-70)` | `goal-spawn-distance` 54 blocks (GO4 band 40–90) |
| goal 3–4× closer to its own spawn than the enemy's | plan geometry only, no hand tuning beyond it | `goal-spawn-ratio` 3.57 (GO1 band 3.0–4.0) |
| two goals "against each other" | both goals on the shared `z = ±70` line | `GO3` (opposing-goal walk) 140 blocks (band 85–150) |
| snow-capped valley, slope-banded hills | one `frost-valley` theme, `axis: slope`, three bands | `incline`: 56.6% under 20°, 39.5% at 40°+ — flat valley floor against bare ridge faces |
| cold biome bound as well as painted | `biome: {kind: solid, id: 12}` (Ice Plains) | `GET /terrain/biomes` confirms id 12 = Ice plains |
| void between the teams, not across an approach | no plan piece covers `z −14..14`; a `tarn-crossing` build zone spans it | `CT12` strait 28 blocks (band 15–40), full board width |
| taiga/podzol patch kept off the grass | `old-firs` theme on its own polygon, no grass anywhere on the map | census: `old-firs` 3.1%, borders `frost-valley\|old-firs` 168 cells only |
| one small timber-and-stone hut, no footing | the spawn hut itself: cobble base, one laid-log course, spruce infill, gable, snow roof | `roomStyles.spawn`; `foundation.footing: null` |
| trees/boulders clear of the goal | 9 spruce, 4 boulders, none inside the clearance box | nearest is `boulder-3` at `(13,-50)`, 13 blocks off-axis from the goal's `x ±10` box |

## The one call with no oracle: the void is a real gap, dressed as a frozen lake

`approaches.md` requires a real void seam between the two teams, joined only by a build zone — never
solid land, never a "hole" cut across a team's own approach. That is mechanically a real `subtract`
(here, an absence: no piece covers `z −14..14`), which is a chasm, not a pond. The brief offered two
finishes for it and left the choice to the author.

I chose **the void stays void, dressed as the thing that would actually be there**: the last 6 blocks
of solid ground on each bank (`shore-band`, `z −20..-14`) carry the `worked-hollow` theme — the same
stone-and-packed-ice mix as the dig floor — so the two shores read as a lake's frost-heaved edge
rather than a raw cliff, and the gap between them reads as the place the ice has cracked through
rather than an arbitrary rule-drawn ditch. I did **not** add a literal `WaterProp` pool: a real water
body needs a floor to hold it, and the floor here is the mandatory void, which a water prop cannot be
drawn over. The alternative — a shallow, walkable ice-capped basin with no true void at all — would
have satisfied the "frozen pond" reading better but broken the destroy-topology law that the seam
between two teams is void, not land at any depth. I judged the topology law binding and the pond a
matter of finish; a human oracle may disagree and would say so by asking for the walkable-basin
reading instead.

## What the ground is made of

Three themes, each a place rather than a swatch:

| Theme | On | Says | Share |
|---|---|---|---|
| `frost-valley` | the whole valley and both flanking ridges (map default) | `layered` on the `slope` axis: snow over dirt under 22°, a stone/andesite/gravel shoulder to 40°, bare stone/cobble/andesite beyond | 78.2% |
| `worked-hollow` | the dig floor, its rim, and the 6-block shore band at the void | a `cell` mix of stone/andesite/cobble with a packed-ice fleck (~1 in 6 cells); a thin cobblestone rim at the dig's lip | 18.7% |
| `old-firs` | one taiga stand on the west flank, its own polygon | podzol over coarse dirt over gravel, never touching a grass cell | 3.1% |

The hollow itself is the "state the rim and the floor as two `area` marks and let the relaxation
solve a bowl between them" idiom: `hollow-rim` (h 12, a 22×18 ring) and `hollow-floor` (h 5, a 5×4
ring) 14–18 blocks apart, wide enough that the fall between them grades at run ≥ 2× rise — no built
stair was needed, and none is authored, because there is no abrupt structural/natural seam on this
board to bridge: the hut sits on ordinary relief-solved ground and the hollow is a graded natural
bowl, not a stamped platform.

## The techniques, and what each one bought

**One relief, two pushes, three marks.** The whole board's shape — the valley floor, both ridges and
the hollow — comes from a `lane` line mark (the walking spine, base ~10 tilting gently to 7 near the
tarn), the rim/floor mark pair, and two `push` rings hugging the outer edge (`amount 26, crown 16,
falloff 12`). No plan piece states a height; `globals.surface` is the only number every piece shares.

**A junction piece purely to satisfy `LN2`.** The single 96-block lane from spawn to the tarn read as
one uninterrupted 140-block chain (`LN2`, band 25–110). Splitting the lane into three same-height
pieces did not break the chain — same-width consecutive rectangles do not create a graph junction —
but a small branching stub (`east-adit`, an 8×16 alcove into the east ridge's foot) did. It reads as a
second, shorter working into the hillside, which the mining-camp premise wants anyway.

**Narrowing the board fixed two complaints for the price of one edit.** The first drive was 140
blocks wide with the ridges at the very edge; `LN2` still refused (140 > 110) and 71.7% of the ground
was "reachable, on the way to nothing" (coverage). Pulling the ridges in to `x 38..50` (a 100-wide
board) put the whole lane under `LN2`'s band on its own and cut dead ground to 61.7% — still high,
because the two flanking ranges are deliberately scenic backdrop for a "snow-capped valley" rather
than graded flank routes, which I judged the right trade for one of the plainer boards of the five
rather than one to engineer away entirely.

**Matching the two gradients of a push.** The first ridges climbed their skirt at 2.2 blocks a block
and their crown at 0.8 — `RL6`, a visible kink at the push's own outline. Raising `crown` from 9 to 16
(closer to the skirt's own grade) cleared the complaint and dropped the board's barrier-step count
from 2,778 to 1,146 cells.

## What went wrong

**A themed patch drawn `base_height: 1` painted nothing, and the documented safe form was the trap.**
`GENERATION-NOTES.md`'s own worked recipe for a paint patch on solved ground is `operation: "add"`,
`base_height: 1`, no override — "the ground, repainted." I drew the dig floor, the shore band and the
taiga patch exactly that way and the store, the compile and the export all answered clean; the export
even printed the right theme tally at compile time (`themes on shapes: {'worked-hollow': 2, 'old-firs':
1, ...}`). The built world painted **100% `frost-valley`** anyway — `themes/census` listed one theme,
and a column inside the hollow read Gravel (a `frost-valley` band member), not the packed-ice cell mix
I had painted it with.

`docs/world-export/terrain-painting.md` names the missing half: *"Among the shapes covering a column,
only those reaching its visible top may own its paint; among those the smallest area wins."* A
`base_height: 1` shape never reaches the visible top of a column the relief has already solved to
30–50 blocks, so it loses the *ownership* contest even though `RasterizeLayout`'s later height repair
(`Max(floor+1, field)`) would have put it at the right *height* regardless. The two mechanisms — height
repair and paint ownership — are evaluated at different points, and the note that documents the first
does not mention the second. Setting `base_height: 60` (comfortably above the relief's own high of 52,
so the patch plausibly "reaches the top" before repair) fixed all three patches at once, with no change
to the built geometry — the repair still clamps every cell to the solved surface, so nothing floats.
I could not find this stated anywhere in `docs/` and have not filed it as a task; it belongs in
`docs/world-export/terrain-painting.md` beside the passage that names the mechanism, and possibly as a
correction to `GENERATION-NOTES.md`'s own worked recipe, which is incomplete for a shape sitting on
relief-governed ground rather than on a `07-hill`-style shape with a comparably short stated height.

**`SP2` names a false positive the rule itself predicts.** The lint complains the spawn is "not near
the back of its lane," and its own `means` text says the per-piece approximation misreads a spawn split
across multiple chained pieces — exactly this board's shape. The spawn piece is the literal furthest-
back rectangle on the board (`z −140`, the board's own edge); nothing is behind it.

## What worked first time

The GO1/GO3/GO4/CT12 numbers all landed in band on the first `--dry` read, from the ratio arithmetic in
`AUTHORING-BRIEF.md` §3 alone (`d = L/5..L/4` for the band). The house-style fork (cobble base, one
laid-log course, spruce infill, snow gable roof, no footing) built and previewed clean on the first
store. The biome bound cleanly as a flat `solid` field with no interaction with the theme's own slope
bands. Dressing placed all 28 props with zero declines on every drive once the relief stabilised.

## Coordinates

| Thing | Position | Reading |
|---|---|---|
| red goal (Frozen Relic) | `(0, 9..11, -70)` region, marker `(0,-70)` | obsidian, `pillar-2`, float 4, ground top y5 |
| blue goal (mirror) | `(-1..0, 9..11, 69..70)` | mirror of the above |
| red spawn hut | `(-8..8, -132..-118)` footprint, door facing `+z` | timber-and-stone, gable, snow roof |
| the hollow | rim ring 22×18 about `(0,-70)`, floor 5×4 | rim h12, floor h5, graded bowl, no stair needed |
| the tarn crossing | void `z -14..14`, full 100-block width | `tarn-crossing` build zone; CT12 gap 28 blocks |
| west ridge | push ring `x -50..-38, z -140..-14` | amount 26, crown 16, falloff 12; peak ~y45-52 |
| east ridge | push ring `x 38..50, z -140..-14` | mirror of the above |
| old-firs stand | polygon `x -44..-22, z -102..-82` | 6 spruce (`fir-1..6`), podzol/coarse-dirt/gravel |
| scattered spruce | `(22,-108)`, `(22,-55)`, `(-24,-45)` | `spar-1..3`, singles clear of the lane's centre |
| boulders | `(16,-85)`, `(-18,-55)`, `(13,-50)`, `(-30,-108)` | grey outcrop/round, Stone/Andesite/Cobble |
| east adit | `x 50..62, z -82..-66` | the `LN2` junction stub, doubles as a second working |
| observer | `(0, 58, 0)` | over the tarn crossing, not the bedrock default |
