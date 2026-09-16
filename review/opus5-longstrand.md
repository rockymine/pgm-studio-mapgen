# Longstrand — two stones, a blowout and a tide that opens late

> Adapted from `GET /api/compose?players=20&symmetry=mirror_z`, **seed 12**, composer
> `markers-in-blocks-1`, cell 5. Composed score 4.173; structure **hub `twin` · frontline `bar` ·
> wools `l`, `donut`**.

**In one sentence:** a sand spit — flat, pale and open nearly everywhere — with one ring of dune on it
that you have to walk round, two tide-worn stones in the middle at a ten-block grain, and a water lane
down the west flank that opens forty-five minutes in.

115 × 230 blocks, `mirror_z`, base surface 10, observer y 42. Two groups: `team` (5 192 solved cells)
and `neutral` (the two stones, 464).

## What the composer gave and what it became

| The composed board | This board |
|---|---|
| the near wool level with the frontline, 108 blocks from the enemy's door; the deep wool 157 — **1.44×** straight-line, 200/148 by walk | 192 and 200 — **1.05×** straight-line, 206/234 — **1.14×** by walk |
| one plain 20-block mid band across the middle | **two stepping stones** at 15 × 10 blocks each, ten blocks off each front and twenty apart, five build zones, and a **water lane** |
| a five-piece donut wool at the board's far end, its room on the ring's near corner so one arm of the ring is on no route | the ring pulled forward and shrunk to 35 × 35 round a 15 × 15 blowout, with the room on its **far** corner so **both arms are somebody's road** |
| a 55 × 25 frontline bar, its outer thirty blocks on no route at all | trimmed at both ends to the ground the crossings land on, with a scalloped bay cut into its face **in the layout**, where `G5`'s hop band cannot see it |
| no storeys, no curves, no holes but the donut's | the blowout redrawn as an octagon; 41 vertices of hand-drawn coast; both stones drawn as tide-worn rock |

## The mid, which is the board

Three crossings that are open at the first tick and one that is not.

- `stone-w` at `x −25..−10` and `stone-e` at `x 10..25`, both `z −5..5`, each a plan piece stated once
  with `mirrors: False` — under `mirror_z` a rect centred on `z = 0` is its own image. Each is four
  vertex inserts away from a rectangle and is bent `in`, so the hops off them read 12–14 blocks rather
  than the plan's 10.
- `hop-w`, `hop-e` and `hop-mid`: the first two join each stone to the two fronts, the third runs the
  twenty blocks **between** the stones, so a player who takes one can work along the chain instead of
  going back.
- `tide` is a `water-lane` zone, `x −35..−25, z −15..15`. It is closed at the first tick and opens
  forty-five minutes in, and it is not in the navigable set — which is why the five build zones exist
  and why the ten blocks of front bar it docks read as **dead** on the plan-tier flow. That is the
  documented cost of a late crossing and I paid it deliberately: 175 blocks a side.

**Three stones did not work and the reason is arithmetic.** With three stones in a row, the diagonal
from a front's inner corner to the *far* stone is 22 blocks, and `G5`'s hop band tops out at 20 — a
hard term, so the plan evaluates at 1002 and invalid. Two stones twenty apart put every pair on the
board inside 10–20. The notch that would have split the front into two headlands has the same problem,
so it is cut into the compiled outline instead of stated as two pieces.

## The donut, made to be a donut

The composer's five-piece wool body encircles a hole, and the hole is what the body is for. On the
composed board the room hangs off the ring's near corner, so the flow read named **525 blocks** of the
ring — `dune-w` 250, `dune-s` 150, `dune-e` 125 — as ground no journey passes. Moving the room to the
ring's **far** corner puts both arms on a route and takes the board's dead share from **25% to 5%**.

The blowout itself is `void-1-cut`, the subtract the compile emits for the hole. It is rounded off and
opened a block on every side through `shapePropsById` — a subtract may be redrawn, never filled.

## Where the made ground meets the grown ground

`staithe` is a four-vertex polygon at `base_height` 12 with `relief_scope: "exclude"` — a plank-and-
stone landing at the head of the lonning with the spawn hall on it — and `staithe-ramp` is a twelve-
block flight up onto it from the strand.

The one relief **mark** on this board is there because `WX11` asked for it by name: *spawn spawn-1
stands 2 blocks above the ground beside it at (4, 104). Its foundation fills that face in bedrock,
which is a wall a player cannot climb and nobody drew.* The read even hands back the edit. An `area`
mark at 12 round the staithe brings the strand up to the landing's floor, and neither push reaches
that corner of the board, so the mark is not lifted by one.

## The relief

Two pushes and one mark.

- `dune`, a six-point ring over the donut's own arms: `amount` 7, `crown` 6, `falloff` 10,
  `roughness` 3. Its two gradients agree by construction — 0.70 outside the ring against 0.67 inside
  — so the blowout is a hole in a hill rather than a hole in a table.
- `bank`, a low swell over the west strand at `amount` 4, `crown` 3, `falloff` 7, so the open wool is
  not approached across a plate.

Read back: `dune` climbs `skirt 0.70 · crown 0.48`, `bank` `skirt 0.57 · crown 0.36`. `seams []`,
`silentMarks []`, `level 0.606`, `largestField 0.302`, `faces 2`, `cliffs 0`, `symmetryError 0`.

## What the ground is painted with

Three families: the **ground** is pale and warm — sand, sandstone, marram turf; what is **built** is
dark oak over stone brick, the only dark thing on the board; the **accent** is prismarine, on the two
stones and nowhere else.

`strand`'s surface is a `layered` material on the **`slope`** axis cut at 20° and 38°, because a
dune's own angle of repose is about 34 and the cut has to fall either side of it: marram-bound flat,
then the blown face, then the eroded scarp. `GET …/incline` reads 58.5% of this board under 10°,
16.5% at 10–19°, 13.3% at 20–29°, 9% at 30–39° and 2.7% at 40° or steeper — the gentlest of the four,
which is what a spit is.

`themes/census`: `strand` 9 476 cells (87.8%), `staithe` 892 (8.3%), `skear` 424 (3.9%), with 82 cells
of drawn border to the staithe and 46 to the stones. Nothing registered painted nothing.

`themeById` binds `skear` to both stones. Without it the stones took the map default and the theme
registry carried a theme that painted nothing — which `05-themes.txt` is the only witness to.

## The numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, valid, one `SP2` complaint |
| `GET …/preflight` | **export gate OPEN**, per team |
| `GET …/coverage` | reached 10 108, dead **2**, **0.0% dead** |
| `03-slopes.txt` | 10 560 walked, 168 scrambled, **64 barrier**; 4 faces, largest 21 |
| `06-claims.txt` | placed **18**, declined **0** |
| `plan/flow`, dead | 525 of 9 700 blocks (5%) — 175 a side under the tide's dock, 175 a side on the front bar's west end |
| relief `team` | `low 12 · high 28 · level 0.606 · largestField 0.302 · faces 2 · seams 0 · symErr 0` |
| flow, attacker | 234 and 206 — **1.14×** (composed: 200/148, **1.35×**; straight-line 1.44× → 1.05×) |
| flow, defender | 118 and 102 — 1.16× |
| hops | front → stone 10 blocks each (12–14 after the bend), stone → stone 20 |

## What went wrong

- **`G5` is a hard term and three stones cannot satisfy it.** Two builds at score 1002 before I
  worked out that the failing pair was a *diagonal* between a front and the far stone, not a
  neighbouring hop.
- **The wool room needs two cells of interface, not one.** `WX6` — *no land seam and no abutting build
  zone* — on a room that shared exactly one cell edge with its approach. It answers at two.
- **The lifted tree bodies in `specs/archive/opus5-marram-hythe/trees.json` are in the reader's own
  `{foot, body}` shape**, not a `PropStyle`. A bare body in `dressing.styles` is a **500 / `RQ2`**,
  because `DressingJson.ParseStyles` throws before any gate reads it.
- **`solid(162)` is acacia log.** Dark oak is `162:1`, and `HS4` refuses a frame whose beams and posts
  are cut from two woods.
- **The first seat the net-house took was declined `DR-WAY`** — 23 blocks further round the board. The
  seats mask answers `DR-CLAIM`, `DR-KEEP`, `DR-ROAD`, `DR-SITE` and `OB19` forwards; `DR-WAY`,
  `DR-CROSS` and `DR-SLOPE` read the built world and it cannot.

## Open gameplay questions

- **The two stones are five blocks off each other's diagonal and twenty apart in line.** I built them
  to be run between rather than bridged between, and I do not know whether that makes the middle too
  easy to hold.
- **A water lane costs ground.** The 175 blocks a side that only the tide reaches are dead by the
  coverage measure and alive at forty-five minutes. I judged that worth it for a fourth crossing that
  arrives late; whether a match lasts long enough to use it is the author's to say.

## Coordinates

| Thing | Where |
|---|---|
| spawn (red) | `(0, 12, 107)`, door `−z` |
| wools (red) | `red` at `(55, 10, 85)` — the ring's far corner — and `orange` at `(−50, 10, 77)` |
| the blowout | `x 24..41, z 64..81` |
| the two stones | `x −25..−10` and `x 10..25`, both `z −5..5` |
| the tide | `x −35..−25, z −15..15`, a `water-lane` zone |
| the bay | cut into the front bar's face, `x −12..10, z 16..24` |
| the staithe | `x −13..3, z 83..117`, top y11, ramp at `x −8..−2, z 76..88` |
