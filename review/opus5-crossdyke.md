# Crossdyke — two storeys over one crossing

> A CTW board adapted from the composed board `players=8 symmetry=rot_180 seed=10`
> (hub `bar`, frontline `none`, wool `i`, score 0). The composer's twenty-block mid band
> becomes a fifty-block crossing with a real island in it, and the island carries a
> masonry causeway seven blocks over its own ground.

**In one sentence:** a limestone reef sits five blocks below the banks in the middle of the
board with a causeway standing over it, so the crossing is two crossings — the deck, which
is twelve blocks wide and visible from both banks, and the reef under it, which is covered,
slower, and comes up on the far half of the deck by one of two flights.

80 × 130 blocks, `rot_180` about the origin, team ground at surface 14, the reef at 9, the
deck at y15. Two landmasses: the two teams' banks (one fanned polygon, `bank-e-14`) and the
reef, which lies on the symmetry centre and is stamped once (`reef-9`, group `neutral`,
`mirrors: false`).

## What the composed board said and what was changed

| Composed | Here |
|---|---|
| hub `bar` at `x −15..10, z 10..30`, one piece | split into `bank-w` (`x −25..−5, z 25..40`) and `bank-e` (`x −5..15, z 25..45`), widened ten blocks west, with a 20 × 5 bite out of the north-west flank |
| spawn room 10 × 10 at `x −30..−20` | 15 × 10 at `x −45..−30`, which is what leaves the ring an iron cube fits in (`WX8`) |
| wool spur off the hub's east end at `z 30..50` | re-hung fifteen blocks further back, `x 5..15, z 45..65`, off `bank-e`'s north face |
| one mid band, `x −15..15, z −10..10`, 20 blocks of void | every piece pushed three cells further out and the band split into **two** crossings of fifteen blocks each with a **mid island** between them, `reef`, `x −25..24, z −10..9` at surface 9 |
| no elevation anywhere | five tiers: the reef at 9, the quay at 14, the moor to 23, the deck at 15, the spawn apron at 17 |
| no layers | three: `piers`, `deck`, `kerb` |

## The second storey, and what the storey is

The causeway is three made layers, bottom-up as the painter walks them:

| Layer | `base_y` | Holds |
|---|---|---|
| `piers` | 9 | eight 2 × 2 trestles, `y9..y14`, standing on the reef |
| `deck` | 15 | one slab `x −6..5, z −10..9`, the course at `y15` |
| `kerb` | 16 | two parapets at `y16` along the deck's long edges, **broken** where each flight arrives |

Measured at `(0, 0)`: reef top `y9` (cobblestone), air `y10..y14`, `y15` chiselled stone
bricks. Five clear courses under the deck.

In gameplay terms the storey is a **choice made at the bank, not at the island**. The deck's
two ends are at `z = ±10`, fifteen blocks of void from each bank, so a bridge onto the deck
and a bridge down onto the reef cost the same. The deck is twelve wide, walled by its kerb,
overlooked by both banks and is the fast way. The reef is a covered lane six blocks high,
with two erratic-free flanks, and it only rejoins the deck by one of two flights — 
`reef-stair-e` (`x 6..12, z −8..9`) and its `rot_180` image `reef-stair-w`. Each is eighteen
blocks of run for seven of rise, and each comes up on the *far* half of the deck from the
bank it faces, which is the whole point: the low road arrives behind whoever is holding the
high one.

Transect up the east flight, `(10, 12) → (10, −12)`:
`rises 5, worst step 1: 0 barrier, 0 scramble, walked end to end`, with a single `DROP −4`
at `(10, −9)` where it leaves the flight back onto the reef.

## Relief: what carries it and what is stated out of it

Two reliefs, one per group, and they never meet — the moor is grown, the reef is a shelf.

- **`team`** (the moor): base 14, reach 16, grain 1.5/17. Two point knolls (`r` 5 and 4) and
  one push. Two `area` marks carry a `tread` because each would otherwise meet the moor on a
  wall — the spawn flat at 17 and the wool flat at 16. The front apron at 14, where the
  bridges land, carries **no** tread: it is meant to be flat to its edge.
- **`neutral`** (the reef): base 9, two `point` marks at `r` 4 and `h` 11, grain 0.7.
- **Excluded from the solve** (`relief_scope: "exclude"`): the `quay` — the masonry landing
  along the moor's front edge — and the four flights. The quay meets the moor behind it at a
  **face**, and two flights are set into re-entrants cut into that face rather than leaning
  on it.

Read back: `team` level **0.396**, largestField **0.129**, 0 seams, 0 silent marks;
`neutral` level 0.648, largestField 0.520. Incline: 45.6 % under 10°, 20.9 % in the teens,
9.8 % in the twenties, 12.1 % in the thirties, 11.7 % at 40° or steeper — which is where the
moor's slope bands cut, at 20 and 34.

## What it is painted with

Three themes, all on the ground and none at a fraction of a percent:
`moor` 48.7 %, `reef` 35.0 %, `quay` 16.3 %; borders moor|reef 172 cells, moor|quay 70,
quay|reef 26.

The ground family is a green limestone moor (grass, coarse dirt, dirt, gravel) on a `Plains`
tint; the built family is pale grey masonry (stone brick, polished andesite, chiselled); the
reef is wet grey shingle, which is neither. The moor's surface is a `layered` material on the
**`slope`** axis — flat to 20°, shoulder to 34°, face beyond — so the same stack finishes the
knoll's top, its shoulder and its face. Every ground theme's `fill` is a cell of andesite and
diorite rather than plain stone, so nothing drawn above it can repaint the column.

## What is not here, and why

**No building.** `POST …/sketch/seats` answers **four** house seats on the whole board at
7 × 7 and **sixteen** at 9 × 7, and every one of them is on the mid island. Between the spawn
march, the wool approach and the two roads, an eight-player team side has no room for one.
What this board is built out of is the quay, its two flights, the causeway and its trestles.

**No boulders.** The only ground with room for one is the reef, and a rock on a reef of
gravel, cobble and andesite is that ground standing up (`DR-TONE`) whatever stone it is cut
from — stone, cobble and andesite being the whole rock palette.

## The numbers

| Read | Answer |
|---|---|
| `/plan/evaluate` | score **0**, valid, no violations |
| `/preflight` | **export gate OPEN** |
| `/coverage` | reached 3 224, dead **0**, **0.0 %** |
| `03-slopes.txt` | 2 613 walked, 128 scrambled, 198 barrier; 8 faces, largest 63 |
| `06-claims.txt` | placed 14, declined **0** |
| `/plan/flow` | attacker 113, defender 64 — one wool, so §2's two-wool ratio does not apply |
| relief read | level 0.396 / 0.129, 0 seams, 0 silent |

## What went wrong

**`voidEnforcement: true` closes the crossing.** It writes
`<apply block-place="deny(void)" region="void-enforcement-area"/>` over an `<everywhere/>`
region, which denies placing a block in the void *anywhere* — including the two crossings
this board is played across. It was in the first build, copied from a destroy board where a
permanent ditch is the point. It is off; the `not-build-area` filter the build zones already
generate is exactly the right rule and nothing else was needed.

**Eleven `SK9` declines from one layer.** The piers, the deck and the kerb were all on one
layer, and a layer holds one span per column, so every pier under the deck and every kerb on
it was simply not in the world. Three layers, no declines.

**A one-course paint patch paints nothing.** `scald` was an ordinary `add` of
`base_height: 1` under twenty courses of terrain; `SK23` said its four columns were all edge.
A brush has to declare a `height_mode` — `raise`, `base_height: 0`, `skirt: 0` — to be a
scope candidate at all.

**A one-column gap between a ramp and a slab is a jump.** The two flights were drawn
`x 7..13` beside a deck drawn to `x 6`, which left column `x = 6` at reef level: a two-block
horizontal jump with a one-block rise. Both flights were widened one column toward the deck.
