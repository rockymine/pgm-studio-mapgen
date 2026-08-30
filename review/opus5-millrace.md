# Millrace — a walled water course cut down the author's basin

**What I set out to build:** the author's sunken basin as a millrace — a walled channel with water in it,
a sluice, a dry mill yard east of the sluice with the monument standing in a pit, a viaduct over the water
and a causeway out to the island.

`specs/opus5-millrace`, driven 2026-08-30 off `specs/rockymine-map-experiment`. 260 × 250 blocks,
`rot_180`, 12 players, **one destroyable a team**. Plan `valid: true` at score **1.18**, export gate
**OPEN**, and **nothing the dressing pass declined**.

## What the base could not keep

The author's board carries **two** destroyables a team. It cannot: I searched every land cell on a 5-block
lattice and no pair satisfies `GO1`, `GO2` and `GO3` together with the spawns where they are drawn. The
spawns are 277 blocks apart, so `GO1`'s band [3.0, 4.0] puts a goal **55–69** blocks from its own spawn;
the base stands them at **111**. Of 319 well-inside land cells, the ones inside `GO1`'s band on `s1` are a
patch at `x −40..−15, z 75..115` and on `s2` a strip of four at `z 30` — and no cross-pair of those is
`GO2`'s 35–65 apart.

**613 configurations do work, and every one of them moves the spawn.** They put red on `s2` at about
`(−110, 20)` with goals at `(−60, 10)` and `(−60, 45)`. That keeps two objectives and strands the north
mass, which nothing would then walk. So this board takes the other branch: **one goal a team**, and the
spawns stay where the author drew them.

**With one goal there is exactly one place it can stand.** Requiring `GO1` ∈ [3, 4] and `GO3` ∈ [85, 150]
leaves a 22-cell patch at `x −60..−44, z 45..55` — all of it inside `s0`, the basin. The board's objective
was therefore always going to be *in the dip*, which is what the author asked for from the other direction.
It stands at **(−52, 52)**, `ownSpawnBlocks 69`, `enemySpawnBlocks 217`, ratio **3.14**.

`G5` took a second change: the island sat 25 blocks off the team mass against a band of 10–20, and the
short alternative lay outside the build zone so it did not excuse the long one. `piece` reaches one cell
further east and `piece-4` west to the race mouth, which is the causeway made honest in the plan.

## What it carries

| thing | how it is stated |
|---|---|
| race walls | two thin **open** `path` shapes traced along `s0`'s own south and north lips, radius 1 — two blocks thick — `height_mode: level`, `skirt: 0`, `relief_scope: exclude`, standing sheer `y15..31` |
| sluice | the same, across the basin at `x −70`: water west of it, dry yard east |
| viaduct | a deck at `y30..31` on its own layer, on three piers down to `y17`, spanning bank to bank at `x −100` |
| causeway | a deck at `y24..25` out of the race mouth to the island |
| yard ramp · wharf steps | tilted quads through two gates cut in the north wall — `(−64..−52)` down to the yard at `y19`, `(−86..−74)` down to the water at `y20` |
| water | one `pool` prop on the race's west arm, `level: 23` |
| monument | `(−52, 52)`, floating 4 over a pit floor at `y18` |

**The walls are the author's own construction and they work as described.** A `path` shape with `radius 1`
lays a two-block band; `height_mode: level` with `skirt: 0` holds its top flat and sheer; `relief_scope:
exclude` keeps the relief from solving through it. Read at `(−70, 54)` the sluice is stone brick from
`y20` to `y30`, unbroken.

**The four hint slabs are gone and the relief does their work.** `moor-brow` reaches `y39` at `(−40, 118)`,
`fell-head` `y43`, `wold-brow` `y38`, and the island knoll `y38` at `(47, 50)`.

## Three grounds, and the two mistakes it took to get them

`moor` (grass ↔ podzol, noise scale 26) is the north bank, `wold` (coarse dirt ↔ dirt, 24) the south, `holm`
(mossy cobble ↔ gravel, 15) the island. Each is **two blocks of one family**, so the noise is grain rather
than static, and each is stated on a shape rather than sampled across a border. `masonry` is a fourth and
is not a place: it is the one stone every built thing on the board is made of — both walls, the sluice, both
spans, both ramps.

**The race mark sank the moor behind its own wall.** A `line` mark with `r: 19` down a basin 35 blocks wide
reaches 2 blocks past the north lip, so a strip of `s1` came out at `y19..21` — walled off from the moor
above and the race below, and unreachable from either. Marks are read in order, so the fix is to state the
line at `r: 15` and then state each bank as an `area` at `h: 30` **after** it. Measured at `(−58, 72)`:
`y21` before, `y29` after.

**A deck written on the ground layer takes the ground out from under itself.** The first viaduct was an
override add on `ground`, and a layer keeps one span per column: at `(−100, 57)` the column held the two
deck blocks and nothing else, all the way to bedrock. Spans belong on their own layer.

## What it still complains about

| rule | count | what |
|---|---|---|
| `SK10` | 1 | the viaduct shares 2 courses with the bank over 94 columns where it lands — a bridge has to meet its bank, and one course is the seam the rule allows |
| `SK11` | 1 | 12,520 places of race bed at `y20`, walled on both sides. The wharf steps are the way in; the rule's own answer is *leave it if a detached group is what this is*, and a canal is one |

**The number I am least happy with is coverage: `reached 7,075 · decorated 5,391 · dead 17,485` — 57.7%
dead against `opus5-slipway`'s 19.3%.** One objective a team on a board this size leaves most of the ground
off every spawn↔goal journey, and adding two more paved routes moved it by nothing, because coverage walks
the journeys and not the lanes. The honest reading is that this board is **too big for one objective**: it
wants either the second goal (which needs the spawn moved, above) or a smaller board.

## What I could not get to work

- **A `path` prop will not pave a `keepClear` shape**, so `holm-way` stops at the causeway rather than
  running over it. That is `KeepOut.Structure` behaving exactly as documented; it just means a bridge deck
  cannot carry a road's paint.
- **Two studio faults, both unhandled 500s rather than named refusals**, filed in `BACKLOG.md`: a prop
  whose enum field will not parse (`form: "rounded"` against `BoulderForm`) is accepted by
  `POST /map/from-documents` and then throws `DressingParseException` out of every later read as `RQ2`; and
  a house style whose `wall` is replaced by a bare material instead of a band stack throws a
  `NullReferenceException` out of `HouseStyleValidation.CheckOres`.
- **The grown tree is untouched here** — every tree on this board is `form: "template"`, as the author asked.

## What to look at

`maps/opus5-millrace/` is the world. The reads worth taking are `GET /map/opus5-millrace/column?at=-70,54`
(the sluice, floor to parapet), `at=-80,68&at=-80,64` (the wharf step into the water), `at=-58,68..56`
(the yard ramp's courses), and `at=-70,-3` (the sign's letters at `y84..86`).
