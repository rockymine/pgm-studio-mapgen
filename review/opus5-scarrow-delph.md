# Scarrow Delph — a worked hillside quarry, where the terrain is the board

> Two hillsides face each other across a drowned valley. A benched delph is cut into each, a haul road
> spirals down it, a two-level gallery is cut into the other shoulder, and the bottom of the valley is a
> flooded pit standing in void that both sides have to bridge to.

**In one sentence:** a gritstone delph on a Pennine moor, worked in four benches down to a dry sump where
one monument stands, with a second monument on a cut gallery across the spine, and the abandoned deepest
working flooded and marooned in the middle of the board.

108 × 220 blocks, `rot_180` about the origin, cell 2, base surface 30, observer y74. Ground runs y4 (the
drowned pan) to y57 (the spoil heaps). Three landmasses: one per team and the flooded pit, joined by
nothing but a build zone spanning the board's whole width.

**Almost nothing here is a shape.** The plan is five rectangles; every landform on the board is a relief
mark. Seventeen marks and three pushes make the team's ground and three marks make the pit.

## What the ground says, level by level

| Level | y | Stated as | Measured |
|---|---|---|---|
| spoil heaps | 51–57 | `push` ×2, amount 7/6, falloff 7, roughness 3, crown 3 | high 57 |
| moor crest | 46 | `line` mark along z −106..−103, r 7 | — |
| the camp's flat | 44 | `area` mark x −18..18, z −108..−88 | ground 42 under the spawn, walked end to end down the spine |
| works platforms | 44 | two `area` marks, x ±14..34, z −102..−86 | no `WX11` on either building |
| delph lip (overburden) | 42 | `area` x −52..−4, z −86..−36 | — |
| delph bench 3 | 36 | `area` x −47..−9, z −81..−41 | — |
| delph bench 2 | 30 | `area` x −42..−14, z −76..−46 | — |
| delph floor (the sump) | 24 | `area` x −37..−19, z −71..−51 | 6-block wall on all four sides, both axes |
| upper gallery | 38 | `area` x 34..54, z −82..−56 | — |
| lower gallery | 32 | `area` x 8..36, z −74..−46 | — |
| valley shoulder | 15 | `line` along z −31 | — |
| brink | 13 | `line` along z −27, r 2 | last land before the void |
| the quay | 17 | an `addShapes` rectangle at `relief_scope: "hold"` | flat 17 over z −41..−30, then 12 |
| pit strand | 10 | `area` mark on the neutral group | — |
| pit beach | 9 | `area` mark | — |
| the water | 8 | one `water` pool prop, `level: 7` | water top y8 across x −41..41 at z 0 |
| the drowned pan | 4 | `area` mark x −32..32, z −8..8 | 5 blocks under the beach |

The four rings of the delph are written **outward-in**, and that is the whole trick: a later mark wins a
contested cell, so four nested `area` marks at 42 / 36 / 30 / 24 terrace themselves without a block step
being asked for. `step` stays at 1, which is what leaves the roads walkable.

## The three roads, and why they exist

Every graded way down the board is a `line` mark with a height per vertex, written **after** the benches
so that it cuts their faces rather than being buried by them.

| Road | From | To | Run | Fall | Grade |
|---|---|---|---|---|---|
| `spine` | the spawn door at (0, −88), y43 | the shoulder at (−3, −29), y16 | 59 blocks | 27 | 0.46 |
| `haul` | the brow at (−2, −84), y41 | the sump at (−28, −54), y24 | ~250 blocks, one full spiral of the lip and a doubling back along bench 3 | 17 | 0.07 |
| `incline` | the lower gallery at (30, −48), y32 | the shoulder at (51, −28), y14 | ~30 blocks | 18 | 0.6 |
| `gallery-ramp` | the spine at (4, −60), y31 | the gallery at (15, −58), y32 | 11 blocks | +1 | — |

The spine is the board's lane. **Unstated, it is not a lane at all.** With the delph lip pinned at 42 on
one side and the gallery at 32 on the other, the relaxation holds the strip between them near its
neighbours' height for fifty blocks and then lets go; and the haul road's first vertex, left at 40 where
the ground under it was 24, pinned a plug across it. Measured down x = 2 before the spine was stated:
`z −50: 30 · z −48: 24 · z −46: 39 · z −42: 39 · z −40: 39 · z −38: 19 · z −30: 15` — a fifteen-block
step up into the plug and a twenty-block fall off its far side in two blocks. Stating the spine as its
own falling line mark, and moving the haul road's entry to the brow where the lip and the moor are level,
turned that into `walked end to end, worst step 1` out of the spawn door.

## What the goals cost an attacker

`GET …/walk` from the shore an attacker lands on, at both aims:

| from the enemy's brink to | shortest (`aim=travel`) | fewest blocks (`aim=reach`) |
|---|---|---|
| **The Sump** (−28, −60), y24 | 33 blocks, **19 placed** | 109 blocks, **0 placed** |
| **The Gallery** (22, −58), y32 | 31 blocks, 5 placed | 38 blocks, 0 placed |

Only the middle band of the board is buildable (`build.areas = [{−54, −30, 54, 30}]`), so the sump's
nineteen-block climb is not available in play and the pit is always the 109-block walk round by the spine
and the haul road — a 3.3× detour. The gallery is 1.2×.

## How height defends each goal

**The Sump**, at (−28, −60) on the delph floor, is read on both axes as *one barrier in, one drop out*:
`DROP −6 at (−37, −60); BARRIER +6 at (−19, −60)` along x and `DROP −6 at (−28, −71); BARRIER +6 at
(−28, −48)` along z. A player drops into the sump for free from any side and climbs out only by the haul
road, which passes within two blocks of the monument. The defenders' own walk in is `rises 0, falls 3,
worst step 7` — they arrive by falling, and they leave by the road they would rather hold.

**The Gallery**, at (22, −58) on the lower shelf, is the other problem. Its own team reaches it at
`worst step 5` (a drop off the spine). An attacker coming up from the water lands on the shoulder at y15
and must take the incline, or come along the spine and step two onto the shelf; the upper gallery at y38
looks down on all of it. Height above, height below, and two ways in that a single defender cannot both
watch.

## What the ground is made of

Three themes, and one bedded stone stack shared as the `wall` and the `fill` of all three, so every cut on
the board shows the same rock in the same order, read down from the top of each face.

| Theme | On | Says |
|---|---|---|
| `gritstone` (35.4%) | the moor, the spine, the unworked hillside | grown: a `layered` skin whose top course is a `cell` of grass / grass / grass / coarse dirt at cellSize 17 over two of dirt — turf with bare patches worn in it, and **rim off** |
| `workings` (41.4%) | the delph's four rings, both galleries, the delph's face over the valley, the quay | stripped: a `cell` of stone and cobble at cellSize 12, depth 2 |
| `spoil` (23.2%) | the two heaps, and the whole flooded pit | moved: a `cell` of gravel and coarse dirt at cellSize 11 |

The shared stack is stone 3 · diorite 1 · stone 3 · gravel 1 · andesite 3 · cobble 2 · stone 4 · coarse
dirt 1 · stone 5 · andesite 2, on repeat. The pale diorite bed, the gravel parting and the coarse-dirt
parting are there because the first stack — stone, andesite and diorite alone — is three shades of one
grey and every cut on the board came out flat. `gritstone` borders `workings` over 808 cells and `spoil`
over 386.

The rim is off on every theme. This board is one long argument for that: a rim caps every fall with a
band, and a board with fifteen cliffs and a hundred and forty-three faces would have come out as contour
lines.

Four buildings, three ideas. Two works sheds on the moor above the delph — the winding house and the smithy,
each on an `area`-mark platform at the moor's own level — a crusher on the upper gallery, and a loading
stage on a quay at the water's edge. All four are timber and sandstone; the ground under all four is grey
stone, so nothing is walled in the family it stands on.

## The techniques, and what each one bought

**Nested `area` rings terrace without `step`.** Four rings written outward-in give four benches with
6-block faces and leave the roads at a one-block quantum. Setting `step` to the bench height instead is
the documented instrument for a quarry and it costs the roads: measured on this board's own marks,
`step 3` gives 12 scrambles against 1785 barriers and no row crossable on foot in either direction.

**A road is a line mark with a height per vertex, written last.** The haul road's 250 blocks of run for
17 of fall is a grade of 0.07, which is why a spiral through three bench faces reads as a road rather than
as a stair.

**`relief_scope: "hold"` is how a built floor is stated inside a relief.** The loading stage stands on a
rectangle held at `base_height 18`; the surface either side of it is solved knowing where it has to
arrive, so the quay is flat at y17 for eleven blocks and the ground runs up to meet it rather than
stepping. The same rectangle at `relief_scope: "exclude"` built no plate at all — the column read y15,
the relief's own value.

**A push sculpts an area mark; only a room floor is rigid.** The first two builds put the works sheds
inside a spoil heap's falloff, and the platform marks under them were lifted and domed along with
everything else: `WX11 — house winder 0 stands 6 blocks above the cell beside it`. There is no way to
protect a mark from a push, so the heaps moved into the back corners instead.

**The flooded pit is a `pool`, not a channel.** `shape: "pool"` with a twelve-point ring, `level: 7` and
`depth: 4` fills a stated basin whatever the column under it is doing — which is the only way to flood
ground the sketch dug out, since there is no surface up at the line for a derived level to find.

## What went wrong

**The main lane was a cliff and no picture showed it.** The nineteen-block drop across the spine at
z −38 is one shade in a heightmap and nothing at all in the isometric. It came out of `loop.py --profile
x=2,z=-110..-26`, which is the read that answers a lane.

**The first haul road started at the wrong end.** Its first vertex sat at the delph's mouth at y40 while
the ground the spine gave there was y24, so the road pinned a 15-block plug across the lane. Moving its
entry to the brow, where the lip and the moor are at the same height, is the fix; the general shape of it
is that a road mark must start where the ground it leaves is already at the road's stated height.

**Three passes of dressing declines.** Six the first time, five the second, three the third, and none the
fourth — every one of them a boulder or a tree standing in a building's claim, a road's standoff, a
spawn's keep-out or a goal's clearance. `tools/loop.py` answers all of them in fifty seconds without
building anything, which is what made four passes affordable.

**`RL2` is on this board and is staying.** The team group carries 0.9 two-block scrambles for every
barrier taller than one, and the rule reads that as elevation that was never graded. That is what a
quarry is: the benches are cut and the roads are graded, and the rule cannot see the difference because
it measures the whole island. The complaint is read and left.

**20.8% of the ground is dead.** `coverage` reports 4352 of 20960 blocks off every journey, the two
largest patches of about a thousand cells each at (−45, −67) and (44, 65) — the bench interiors between
the passes of the haul road. A benched quarry has that shape by construction, but it is a real number and
a bigger board would have made it worse rather than better.

## Coordinates

| Thing | At | Ground |
|---|---|---|
| red spawn | (0, −98) | y42, door on +z, spine road from the door |
| The Sump (red) | (−28, −60) | y24, delph floor, 6-block wall all round |
| The Gallery (red) | (22, −58) | y32, lower gallery |
| blue spawn / goals | the `rot_180` images | symmetry error 0 |
| the tarn | ring x −41..41, z −7..7 | water top y8, bed y4 |
| the quay | x 0..16, z −41..−29 | y17 |
| winding house | x −30..−18, z −98..−90 | on a platform at y44 |
| smithy | x 18..30, z −98..−90 | on a platform at y44 |
| crusher | x 40..50, z −76..−68 | upper gallery, y38 |
| loading stage | x 3..13, z −38..−32 | the quay, y17 |
