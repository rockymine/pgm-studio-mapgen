# Wheal Hazel — a tin-streaming valley, and a leat that is not an aqueduct

**In one sentence:** a granite moor cut by a tin works, where each team's wool sits at the head of a walled
lane above the works floor, a flooded shaft is spanned by a raised leat, and the only ground between the two
valleys is a shingle bar nobody owns.

130 × 170 blocks, `rot_180` about the origin, base surface 9, build ceiling 33, ground y 5..25.
Two islands: `team` (4 101 cells, y7..13, symmetry error 0) and `neutral`, the bar (828 cells, y9..11).

## What the board is for

The topology is capture's: the wool a team wants is at the back of the *enemy's* valley, up a lane a bedrock
wall is built across. The run out crosses the bar; the run back is the same walk carrying the wool.

**The three ways across are three different prices.** The build zone at `x −15..15, z 5..20` is a bridged
crossing open from the first tick — the short way and the watched one. The **water lane** at `x 30..50,
z 10..25` is void for forty-five minutes and then becomes a second crossing on the flank, so the endgame is
not the shape the opening was; under `rot_180` it lands east for red and west for blue, which pinwheels the
late route rather than mirroring it. And the **inlet** cut into the works floor at `x −20..−10, z 20..30`
(probed: `(−15, 25)` = 0 solid) makes the front coast a pair of headlands rather than a wall, so the walk to
the crossing is a choice of two.

## Where each thing is, measured

| Thing | Where | Read at |
|---|---|---|
| spawn | `x −10..10, z 70..80`, door facing −Z | `(−10, 77)` stone brick top y12 |
| wool room | `x 20..35, z 60..75`, entry seam `z = 60` | `(27, 67)` red wool y11 on bedrock to y10 |
| wool sky marker | above the built shell **and** above the cap | `(27, 67)` red wool y38..40, cap 33 |
| approach wall | `x 20..35, z 44..46`, 15 wide, 15 in front of the entry | `POST /plan/inspect` structures feed |
| the shaft | circle r6 at `(−28, 43)` | `(−28, 48)` = 0 solid — cut to the void |
| the leat | path shape, r 2.5, `x 22..−44` along `z ≈ 43` | `(−28, 43)` polished diorite y9..11 |
| the bar | `x −40..40, z −5..5`, `mirrors: false` | `(0, 0)` cobblestone top y10 |
| strait | team front `z = 20` to bar `z = 5` | 15 blocks — `CT12` wants 15–40 |

Traversability: **10 037 navigable columns, 466 bridged over void, 2 components, 0 isolated.**

## The leat is a causeway, and calling it an aqueduct would have been wrong

It was authored as a `path` **shape** — a shape type the Draw dock cannot draw and no board here had ever
carried — laid as an `override: true` add so it would survive the shaft it crosses. It does survive, and it
is a raised walk two blocks over the yard reachable only from the bench at its east end, which is what was
wanted. It is **not** a span: an override-add fills its column from its own `floor`, so `(−28, 43)` reads
solid stone from y1 to y8 under the diorite. The shaft is a real hole everywhere the leat does not cross it
and a plugged one where it does. A genuine bridge over a hole needs a second `layers[]` slab, which this run
was not authoring at.

## What the ground is made of

Six themes, one per kind of ground. **Ground** is `verdant`+`dirt` (the moor) and `cobble`+`dirt` (the
streamed floor); **built** is `grey stone` (the yard, the lane, the spawn); the **accent** is `pale stone`
diorite, spent in exactly three places — the leat bench's rings, the bar's rim, and the paving of all three
roads.

| Theme | On | Says |
|---|---|---|
| `hazel-moor` | the moor, the spur turf | grown: rim **off**, grass exactly one course (mottled `cell` of grass/grass/green clay) over two of coarse dirt |
| `hazel-floor` | the streamed valley floor | worked: rim off, a `noise` of gravel, coarse dirt and mossy cobble |
| `hazel-yard` | the works yard, strand and spur | rim off, a `cell` of stone, andesite and polished andesite at works scale |
| `hazel-vein` | the leat and its bench | the accent: a `layered` stack on the **inward** axis, so the bench draws concentric rings from its own boundary — rim **on**, because a bench lip is a made edge |
| `hazel-lane` | the wool lane, the apron, the spawn | built: a 5-block `checker` of stone brick and andesite |
| `hazel-bar` | the shingle bar | neutral: a `voronoi` ramp of gravel, cobble and sand, rim on **void edges only** — a coast |

Rims are **off on the four grown surfaces and on for the two made edges**, which is the whole of AD-R1/R2 and
the single most visible decision on the board.

## The four placement ideas, and the four idioms

`AD-S1` asks for three distinct placement ideas; this board carries four, and each building forks a different
shipped preset by material and proportion rather than by palette.

| Prop | At | Is | Forks | Idiom |
|---|---|---|---|---|
| `h1` stamps mill | `x −16..−2, z 38..46` | an **L** on the works yard: a hall with a marching wing | `Workshop` | multi-wing under one style |
| `h2` picking shed | `x −22..−16, z 48..53` | on the shaft's lip | `Stilts` | a ground storey of **air over a beam course** |
| `h3` count house | `x −41..−33, z 52..58` | alone on the moor, bare ground round it | `Counting` | a porch and a storey stack |
| `h4` wheelhouse | `x −59..−53, z 41..47` | on the far spur, across the flank road | `Cottage` | seated into the turf, **sill = air** |
| `cage` | the wool room shell | the works' strongroom | `Counting` | stone brick over cracked, diorite roof |
| `spawn` | the spawn shell | | `Terrace` | a **parapet deck** — a storey of one wall course over air |

Every one was looked at in section as a PNG before a world was built, and two rule breaks were caught there
that no top-down would have shown: the fork was repainting `wall` and leaving `storeys[*].wall` in the
preset's own material (the cage came out timber over stone brick), and every verge was a spruce **log**,
which `AD-M4` forbids.

## Circulation, drawn before the scenery

Three paths, authored first, everything else placed clear of them.

| Path | Route | Style |
|---|---|---|
| `p1` | spawn door → apron → moor → yard → the crossing at `(0, 22)` | `worn`, r 2.5, corners chamfered |
| `p2` | yard → leat bench → **stops at the wall's face** at `(27, 42)` | `tapered`, r 2 |
| `p3` | yard → the west spur, under the leat's ramp | `rough`, r 2 |

The stream (`w1`, a `stream`-form water prop) runs down the gravel floor from `(−33, 34)` to `(−30, 22)` and
is what the works is named for. `--surface` reads 112 columns under liquid at waterline y8.

## What went wrong, and what it cost

**Three buffers did nothing.** The first plan shaped its coast with `buffer` pieces drawn over `works-lo`.
A buffer over a generating piece is inert; the fill ratio did not move and no hole appeared. The coast had to
be redrawn out of the *pieces*, which is the only way a plan states one.

**`LN1` cannot be satisfied on this board.** The wool lane reads 30 blocks against the authored band 10–20.
Shortening the approach to two cells fixes `LN1` and fires a hard term instead (score 2 → 1000). The wall has
to seat about 15 blocks in front of the room's entrance (`ST8`), which is three cells of approach on its own,
so a plan-authored wool lane at `cell: 5` cannot be under 25. Shipped at score **2.0, `valid: true`**.

**The observer platform was standing on the contested bar.** A compiled intent puts the observer at
`(0, observerY, 0)` and `observerY` defaults to `surface + 15` — a bedrock pad at y24 over the exact centre of
the neutral bar, found by probing `(0, 0)` and reading bedrock at y24 among the cobble. `globals.observerY:
55` moves it out of play; `(0, 0)` now reads bedrock at y55 alone.

**Six declines, over four builds**, each fixed rather than shipped: a tree in the spawn door's approach
(`DR-KEEP`), two boulders on a path's claimed band (`DR-CLAIM`), a tree a block off the road's *spline*
(`DR-ROAD`, and the polyline was 4 blocks clear — §12's lesson again), a tree over void where the coast had
been bowed away from it (`DR-SITE`), and one tree the spur simply had no room for, which was dropped rather
than moved a fourth time. Final build: **nothing declined**.

## Where it is weak

The middle of the board reads grey. The moor's green is a band at the back of each half and the yard, floor,
lane and bar are all some stone; the works floor's brown is what separates yard from floor and it does the job
alone. A fifth family in the mid would have helped and there was no obvious one that is still a granite moor.

The works yard is a large flat field. Two spoil tips (`raise` shapes with a 3-block skirt) were added after
the first render precisely because the coverage read like a car park, and it is better rather than solved.

## Open questions

**Should a late-opening water lane be the same crossing as the early one, or a different one?** This board
puts them 40 blocks apart on purpose, so the endgame is fought on ground the opening never used.
`approaches.md` says a lane is "a **second** approach that opens late" and does not say whether it should
share the frontline. Built as a separate flank; unverified.

**Is a hole inside a team's own land legitimate on a capture board?** `approaches.md` withdraws the
mid-terrain hole for `dtm`/`dtc` and leaves capture alone, and the shaft here is a rotation device inside the
works rather than a barrier across an approach. Built; if the withdrawal is meant to generalise, this shaft
is wrong.
