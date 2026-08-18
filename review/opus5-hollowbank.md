# Hollowbank — one board, two things to do at once

**In one sentence:** a chalk ring-fort where each team's wool sits in a keep off the inner enclosure and each
team's beacon stands on the inner rampart, so a side must break out and dig in at the same time, across a
ditch with two causeways and one sally port.

100 × 190 blocks, `rot_180`, base surface 9, build ceiling 35, ground y5..25. One island, 5 466 cells,
y7..15, relief 8, symmetry error 0.

**`<gamemode>ctw</gamemode>` and `<gamemode>dtm</gamemode>`, as two elements.** This is the board the run
carried the two-objective case on, and the thing worth stating plainly: the writer emits the element
**repeated**, one id each, which is what PGM's closed 25-value enum requires. `tallow-kilnrow`, `ashfall-scar`
and `basalt-reach` shipped `<gamemode>dtm dtc</gamemode>` and did not parse; `B155`'s fix is confirmed
working on a live board. The objective line reads *"Capture the wool and destroy the enemy's monument!"* —
both kinds, counted per team.

## Where each thing is, measured

| Thing | Where | Read at |
|---|---|---|
| spawn | `x −10..10, z 75..90`, door −Z | h15, the highest ground on the board |
| wool room | `x 25..40, z 75..90`, entry seam `z = 75` | `(32, 82)` shell courses y17, y21, y28 |
| wool sky marker | above the shell and above the cap | `(32, 82)` red wool y40..42, cap 35 |
| beacon | `pillar-3` in **gold block**, anchored `(0, 45)` on the inner rampart | `(0, 45)` gold y16..18 over stem y11 |
| beacon sky marker | | `(0, 45)` red wool y40..42 |
| goal-to-own-spawn walk | 40 blocks | `POST /plan/inspect` |
| goal-to-enemy-spawn walk | 140 blocks | ratio **3.5** — dead centre of `GO1`'s 3.0–4.0 |
| approach wall | `x 25..40, z 64..66`, 15 wide, 15 in front of the entry | inspect structures feed |
| the ditch | `x −45..45, z 30..40` at h8, floor falling to its middle | `line` mark `h [8, 7, 7, 8]`, width 6 |
| west causeway | `x −30..−20`, tilted `11 → 12` over the ditch | `(−25, 35)` diorite y10..11 |
| east causeway | `x 16..28`, same | carries the flank road `p3` |
| sally port | a rectangle subtract, `x −22..−15, z 40..50` | `(−18, 45)` = **0 solid** — cut clean through the inner bank |
| team strait | team front `z = 15` to its own image at `z = −15` | 30 blocks — `CT12` wants 15–40 |

## Three ways through the ditch, and one of them is a hole

The ditch is continuous from `x −45` to `x 45`, so the fort's interior is only reachable three ways: the two
causeways, which are tilted `level` shapes at the banks' own height and are the walked routes, and the **sally
port**, a seven-block notch cut clean through the inner rampart with a ramp from the enclosure down into it.
The port is narrow enough that one defender holds it and it comes out *inside* the ditch rather than over it,
so a side using it has committed to the ditch floor.

That is what makes the board's two jobs interfere. The wool a team wants is behind the enemy's wall at the
back of their enclosure; the beacon a team defends is on their own inner rampart, forward of the enclosure.
A side that sends everyone out has left its rampart, and the rampart is where the enemy is going.

## What the ground is made of

Five themes. **Ground** is `verdant`+`dirt` — the turf, which is on the **outer** bank because that is the one
the fort did not strip; **built** is `pale stone`, the chalk of the ditch, the inner bank and the enclosure;
the **accent** is `gold`, spent on the enclosure's rim, the hay roofs of all three buildings, and nowhere
else.

| Theme | On | Says |
|---|---|---|
| `hb-down` | the outer bank, and the map default | grown: rim off, grass exactly one course (a `cell` of grass/grass/green clay) over two of coarse dirt |
| `hb-ditch` | the ditch floor | rim off, a `noise` of gravel, cobble and mossy cobble — wet chalk rubble |
| `hb-bank` | the inner bank and both causeways | rim **on**: a bank crest is a made edge. A `cell` of stem, diorite and polished diorite |
| `hb-ring` | the enclosure floor | the board's identity, painted: a `layered` stack on the **inward** axis, five deep, so the floor draws concentric bands in from its own boundary, with a hay rim round the outside |
| `hb-yard` | the two rooms' ground | built: a 4-block `checker` of spruce and oak, with a **`wallFrame`** revetment — a log edge inked wherever the wall turns, panels filled between |

Every riser on the board takes the same `layered` chalk-over-flint stack, so a ditch face, a rampart face and
the enclosure's lip are one rock at three scales.

## The buildings

Three, and they are three ideas rather than a street.

| Prop | At | Is | Forks |
|---|---|---|---|
| `h1` moot hall | `x −30..−19, z 54..61` | the fort's one real building, in the enclosure, with a **porch** | `Longhouse` |
| `h2` granary | `x 15..21, z 53..59` | half the plan, a storey taller, same timber | `Cottage` |
| `h3` byre | `x −33..−25, z 18..24` | **alone out past the ditch** on the outer bank, chalk-walled, with bare ground round it | `Workshop` |
| `cage` | the wool keep | chalk and timber, so the keep reads as the fort's own | `Counting` |
| `spawn` | the spawn shell | a parapet deck | `Terrace` |

Six trees on the outer bank's crest and in the enclosure — the hedge a rampart carries — and three sarsens on
the inner bank in chalk-country stone rather than in the turf they lie on.

## The isolated-marker read is the renderer, not the board

`--traversability-map` reports **6 components and 2 isolated markers**, and both isolated markers are the two
wool rooms. It is the known `B99` artifact and not a defect: `TraversabilityRender.Scan` steps past decoration
when it searches for ground and then tests headroom with strict air, so the **cobweb course** capping every
approach wall reads as impassable. `B99` measures it on a plain 60 × 20 plateau — 1 component plain, 2 with
the wall, 1 again with the web removed. The export gate navigates on `WorldColumns.Membership`, which has no
headroom test, and passed the board.

`wheal-hazel` reads *0 isolated* on the same studio because its wool lane carries a second land seam the wall
does not cover; here the wall spans the lane's only seam, which is what a wall does. **The difference between
the two boards is a renderer, not a design.** A wall is meant to be crossed over the top, cutting the web
with the shears every kit ships.

## What went wrong

**The sally port cut the ground out from under the beacon.** The plan put the destroyable at the centre of the
inner rampart for its `GO1` ratio, and the layout then cut the port through that same rampart. `/plan/compile`
answered 200 — a compile judges the plan's rectangles and cannot see a layout `subtract` — and
`GET …/export` answered **409, `OB17` — is 1×1 and overhangs the void**. The port moved 18 blocks west. Cut
the holes before placing the goal.

**`OB19` twice more.** Both enclosure buildings stood inside the beacon's ten-block ring; with the goal at
`(0, 45)` the box is `x −10..10, z 35..55` and it is tested against a footprint *plus its eaves*. Both moved
outside `|x| > 10`.

**The map default painted nothing.** Every compiled shape named a theme, so `hb-down` — the downland turf the
board is named for — covered zero cells, and the whole board came out chalk and timber with no green on it.
Caught by counting the themes actually bound to shapes rather than by looking, which is the one check in this
run a picture would not have given.

## Where it is weak

The `--surface` read shows a magenta outline round the enclosure and both yards: *unnamed material, no family
claims*. It is the spruce **log** in the `wallFrame` revetment's edge and the yard's rim — logs belong to no
tone family, which is `B147`'s reading of stained clay one material over. It is a read-back artifact rather
than something a player sees, and it does mean the surface census cannot name a third of the fort's edges.

The `layered` inward rings read as elongated bands rather than as a bullseye, because the enclosure is
70 × 15 rather than square. That is what an inward stack does on a long shape, and it reads as terracing —
correct for a fort's interior, but it is not what the swatch preview showed and the difference should be
expected.

## Open questions

**Should a board carrying both objectives split a team's attention, or give it two jobs in one place?**
This one splits it on purpose — the wool is at the back of the enemy's fort and the beacon is in front of your
own — so holding and raiding compete for the same players. `approaches.md` says nothing about combined boards
at all. Built as a split; it may simply play as two half-maps.

**Is 30 blocks the right strait for a board where the crossing is also the beacon's approach?** `CT12` bands
15–40 and this sits at the top of it, because a shorter strait would put the two beacons within sight of each
other across the middle. Chosen by eye.
