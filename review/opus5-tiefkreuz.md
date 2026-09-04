# Tiefkreuz — a destroy board on the two railways that cross under a city

> Two lines cross at right angles over the same block of city and the board is played on both. The deep
> line runs north–south in cut-and-cover under the street and goes on through a tunnel into the back of
> the map; the elevated line crosses it east–west on a brick viaduct with a platform, a canopy and a
> train of its own. One monument stands on each line, in the four-foot between its rails.

**In one sentence:** two halves of a city are cut apart by a thirty-two-block chasm, and in each half a
through station is buried under the street — tracks and platforms at y8, a concourse slab at y18, the
street at y29 and a viaduct at y41 — with one monument on the deep track and one on the elevated track,
so both objectives stand on the line and a raid on either has to be climbed or descended before it can
be fought.

80 × 224 blocks, `rot_180` about the origin, base surface 30, build ceiling 69, ground y0..y48.
`maps/opus5-tiefkreuz` · `specs/opus5-tiefkreuz` · `reports/opus5-tiefkreuz-run.md`.

## The stack, in world Y

| Storey | Ground top | A player walks at | Drawn by |
|---|---|---|---|
| ballast of the deep tracks | y5 | y6 | ground layer, override adds |
| rails, one course proud of the bed | y6 | y7 | ground layer, a height band stack |
| cess — one column of concrete at each track edge | y7 | y8 | ground layer |
| platforms — an island between two side platforms | y8 | y9 | ground layer |
| platform canopies over the open bay | y15 | — | `perron`, a **made** layer on posts from y9 |
| tunnel vault over the two northern bores | y29 | — | `tunnel`, base_y 12 |
| concourse mezzanine | y18 | y19 | `halle`, base_y 17 |
| street — and the box's lid where it crosses it | y29 | y30 | the compiled ground layer, and `deckel` at base_y 27 |
| girders and soffit under the viaduct | y38 | — | `traeger`, base_y 37 |
| viaduct deck · elevated platform (parapets y44) | y41 · y42 | y42 · y43 | `viadukt`, base_y 39 |

Eighteen layers in all: the compiled `ground` carrying 188 authored shapes, five ground layers over it
(`tunnel`, `halle`, `deckel`, `traeger`, `viadukt`) and twelve **made** layers — four bands of each of
the two trains, and the posts and the roof of each of the two canopies.

**The board carries no relief at all.** Every height on it is stated: a shape's `floor` and
`base_height`, or a tread's own course. That is what makes a four-storey stack arithmetic rather than a
negotiation with a solver — a relief moves the ground under a slab and a slab does not move with it, and
on a board where a soffit has to clear a platform by exactly eight blocks that is not a trade worth
making. The cost is that every landform on the board is a rectangle, which is right for a city and would
be wrong for anywhere else.

## Ground and made: the two words a shape is painted with

A shape that is **ground** carries a `theme`, whose five buckets are resolved per column: the platforms,
the concourse, the elevated platform, the ballast, the street, the tunnel vault, the planted verges. A
shape that is a **thing made of something** carries a `material` instead, which paints its whole span
with no rim, no wall and no surface depth: every rail, kerb, parapet, stair tread, balustrade, canopy
post, canopy roof, road course, lamp and carriage side. Thirty-eight shapes on this board carry a theme
and three hundred and sixty-seven state one material.

The division is not stylistic. A shape with no interior column can never show a theme's surface, because
which bucket a block takes is decided per column by whether that column is an edge, and on a one-block
kerb or a one-tread stair every column is an edge. `SK23` names exactly that, and the board raises none:
the four groups it named before this pass — eighteen canopy stilts, three street kerbs, three viaduct
parapets and one concourse threshold — are materials now.

Two things a material buys that a theme cannot. A **height band stack** (`layered`, `axis: height`,
`from: 0`) lets one shape say *ballast to y5, iron at y6*, which is how a rail sits **on** its bed
instead of being an iron pillar sunk six courses into it; and *stone plinth, brick shaft, stone impost*,
which is how a pier reads as masonry rather than as thirty-eight courses of brick. And a **road** is a
shape rather than a stroke, so it lands where it is drawn — a stroke seats on whatever surface a column
carries and a stroke under the viaduct paves the viaduct — and `keepClear` on it keeps props off it
exactly, with no margin.

| Theme | On | Says |
|---|---|---|
| `stadt` | the street, the lid, the tunnel vault, the chasm walls, and every column a material paints | **one** block — stone brick — kerbed with a smooth-stone rim wherever the ground drops |
| `bahn` | platforms, concourse, the elevated platform | a **one-block** `checker` of quartz and smooth stone: a tiled floor, light against the city |
| `schotter` | the trackbed and the viaduct's own ballast | gravel, over an andesite body |
| `gruen` | the avenue's two planted verges | turf over two courses of soil, which is what a street tree stands in |

**No field is sampled anywhere on the board.** An octave-2 noise between two blocks of nearly one shade
runs eight blocks of a material at a stated scale of 4 and forty at 18, so on a board 80 across it draws
blotches of two pavements rather than grain in one, and it reads worse than either block on its own
(the author's ruling). Every variation the city has is *drawn*: the black carriageways with their yellow
dashes, the smooth-stone pavements, the two green verges, the station's own checker, the brick of the
buildings and the piers. The census reads the surface block, so `stadt`'s share includes every column a
`material` painted — brick, iron, glowstone, asphalt and the trains are all inside it.

## What the four storeys are for

**The deep level is a through station.** Two tracks run from the tunnel mouths at `z = ±16` — the chasm
face — north past a west platform, an island and an east platform, and on at `z = ±58` through a portal
into a bore eighteen blocks long, roofed at y12, that carries the rails into the back of the map. The
deep monument stands in the four-foot of the west track at `(−12, 8, 56)` and `(11, 8, −57)`, on the
ballast, a few blocks short of the portal.

**A track is a trough a player walks through, not a ditch to be climbed out of.** One column of concrete
at each track edge stands a course over the rail head, so crossing a track from a platform is
`y8 → y7 → y6 → y5` and back — four one-block steps. Before that step existed the trackway was three
hundred cells of two-block scramble and the only free way between platforms was the concourse; it is now
the shortest way to the monument and the reason a goal may stand on the line at all.

**The concourse is a slab over the whole box** from `z ±43` to `z ±57`, with a two-course parapet along
its open south lip, ten glowstone panels cut into it and put back at the same span so their light
reaches the platform beneath, and two openings: the street stair's own well and a shaft over the deep
monument. That shaft runs the whole way up — street to track, twenty-four blocks — so the monument is
visible from the pavement and can be dropped onto.

**The street is the lid over the station** for `z ±16..±23` and `z ±43..±57`, and is missing between
them: the open bay, 41 × 18, where the trainshed is open to the sky and daylight reaches the platforms.
Its edges are kerbed two courses proud, which is what makes the hole read as an edge rather than as a
flush twenty-one-block drop.

**The viaduct is an elevated station.** `z ±57..±69`, 72 blocks of deck on six brick piers with a
thirty-two-block clear span over the box, a two-course masonry soffit and edge girders under the whole
of it, a side platform on the south edge under a canopy, one track with two rails, and a two-car train
standing at it. The high monument stands in that track's four-foot at `(24, 44, 63)` and
`(−25, 44, −64)`. Two masonry stair towers climb to it from the street — twelve treads and a landing,
one rise to one tread — one either side of the avenue.

**Behind the crossing is the quarter the two stations serve.** An avenue sixteen blocks wide runs from
the station forecourt to the spawn: a black carriageway with a dashed centre line, two smooth-stone
pavements and two planted verges with six oaks in them. An arterial road crosses it east–west. Six
flat-roofed brick blocks stand on the grid the two roads make, and the spawn is the seventh and tallest
— a four-storey block at the head of the avenue, not a station head house standing where no station is.

## Where the two teams meet

The chasm is `z −16..+16`, 32 blocks, full-depth: void from the sky to y0. It is `CT12`'s strait
measured at **32** and the plan's one build zone (`x −28..28`) covers it exactly, so a stepping stone no
wider than the window that reaches it is not possible here — the window *is* the ground. The export
writes `<apply block-place="…" region="not-build-area" message="You may not edit the void!"/>`, so a
crossing may be built only inside that window.

| Crossing | Height | Gap | What it arrives at |
|---|---|---|---|
| the tunnel mouths | y9 | 32 | straight onto the enemy platform, at the far end from their monument |
| the quays | y30 | 32 | the enemy street, in the open |
| — | up to y69 | 32 | legal anywhere inside the window, up to the build ceiling |

The viaduct does **not** reach the chasm: each team's is a stub over its own half.

## What the walks cost

Measured on the built world with the storey named — `GET …/walk?from=0,106,30&to=x,z,y`. Naming the `y`
matters: without it the walk targets a column, and on a stacked board a route to a goal on the viaduct
ends on the street twelve blocks beneath it.

| From the red spawn point (0, 106, 30) | `aim=reach` | `aim=travel` |
|---|---|---|
| own deep monument `(−12, 56, 10)` | 101 blocks, 0 placed, one 35-block drop | 55 blocks, 3 placed |
| own high monument `(24, 63, 43)` | 94 blocks, 2 placed | 53 blocks, 17 placed |
| enemy deep monument `(11, −57, 10)` | 260 blocks, 25 placed | 168 blocks, 97 placed |
| enemy high monument `(−25, −64, 43)` | 232 blocks, 27 placed | 180 blocks, 36 placed |

The two placed blocks on the way to the high monument are the climb onto the monument itself, which
floats three courses over the deck by design.

Every leg of the vertical chain walks for nothing, in both directions:

| Leg | `aim=reach` |
|---|---|
| island platform → concourse (stair A) | 22 blocks, 0 placed |
| concourse → street (stair B) | 36 blocks, 0 placed |
| tunnel bore → island platform | 48 blocks, 0 placed |
| deep track → own spawn, the whole climb | 111 blocks, 0 placed, 0 drops |

Plan tier, off `POST /plan/inspect`: `GO1` **3.15** and **3.31** (band 3–4), `GO4` **53** and **54**
(band 40–90), `GO2` **37**, `GO3` **124 / 131 / 145** (band 85–150), `CT12` **32** (band 15–40). The
evaluator scores the plan **0** with no violations and no lint.

## The techniques, and what each one bought

**The clamp, five ways across.** The box is not a floor drawn inside a wall — a layer holds one span per
column and the taller add wins it, so a hall drawn that way builds as its roof alone. The five strips
across the box (platform, track, island, track, platform) are drawn side by side at their own heights,
and the street either side of them *is* the box wall.

**Every flight is 45°, and every flight has a rail.** A tread is one block deep for one course of rise,
drawn as a rectangle per course, and a balustrade stands beside each tread **two** courses above it. Two
is the number that matters: a rail one course proud is a step, and the walk climbs it — measured, the
route from the platform to the spawn ran up the balustrade rather than the stair. At two it is a wall.
Stair A is ten treads from the island platform to the concourse, stair B eleven from the concourse to
the street, and each stair tower twelve treads and a landing from the street to the elevated platform.

**A height band stack is how one shape says two materials.** `layered` on `axis: height` reads world Y,
so a rail is `gravel ×6, iron ×1` from y0 and a pier is `stone ×3, brick ×30, stone ×4`. One shape, one
span, no two override adds contesting a column.

**A rectangle algebra for the slabs.** `carve(outer, holes)` in `build-spec.py` turns a slab and its
openings into the rectangles that remain, banded by z. The lid, the concourse, the parapets, the
girders, the two parapet notches where a stair tower lands, and every carriage side with its doors and
its cab cut out of it are all one routine.

**Made layers for the things that are not ground.** Each train is four layers — underframe with two
bogies a car, body with its doors and cab ends, a window band with pillars between the windows, and a
roof — with an eleven-block car and a two-block gap between the cars. `kind: "made"` keeps `SK10`'s pair
walk and `SK11`'s reachability walk off all of them.

**A goal states its storey.** `DestroyablePlacement` carries `layer`, and it is carried through the
compile onto every orbit image: `{"at": [-12, 56], "layer": "ground"}` resolves against the ballast at
y5 and `{"layer": "viadukt"}` against the deck's own at y41.

## What is wrong with it

**`03-slopes.txt`: 11 672 walked, 648 scrambled, 1 632 barrier, 10 faces, the largest 348 cells at
`x −21..20, z −53..−24`.** That face is the trainshed's own lip — the drop from the street into the open
bay — and every other face is either the chasm wall, the box wall or the viaduct's edge. The 648
scrambled cells are almost all **parapets**: the bay's kerbs, the concourse's lip, the viaduct's two
parapets and every stair balustrade stand two courses over the floor beside them, which is what a
parapet is and what a one-course one is not. The trackway, which was 300 of the old board's scrambles,
is now walked end to end.

**8.3% of the ground goes unused** (`GET …/coverage`: reached 12 006, decorated 791, dead 1 155). The
patches are the corners behind each spawn and the flank west of the viaduct's ramp-less end. Bare ground
beside a spawn is not a fault worth dressing over, and the spawn's own door approach is a keep-out wide
enough that a building cannot be put there — three were declined for it before they were moved.

**`SK11` names 9 209 places of standable ground around `(−14, −76)` as unreached, and the board is
connected.** Every leg of the chain measures 0 placed in both directions (the table above), pre-flight
reports *traversability: spawn ↔ objective chain connected across the build geometry*, and the export
gate is OPEN. The complaint is not reconciled and is recorded rather than worked around; the two
72-place complaints beside it are the two viaduct parapets, whose tops stand two over the platform on
purpose and which nothing is meant to walk onto.

**`SK18` reports the elevated canopy and the deep monument in ten shared columns, and no block of either
is in the other.** The test is two-dimensional. Read at `(−14, 58)`, the first column it names, the
world holds the tunnel vault `y12..y29`, the girder `y37..y38`, the deck `y39..y42` and the canopy
`y48` — and no obsidian, because the monument is at `(−12, 56)` and stands at `y8..y9`. Left as it is.

**`WX11` reports the deep monument thirty-nine blocks above the cell beside it, and the world says
three.** `GET …/column?at=-12,56` reads obsidian at y8–y9 over ballast topping at y5, and `?at=-12,53`
reads that neighbour's own surface at y5. Thirty-nine is the distance from the viaduct's parapet, which
crosses fifteen blocks north of the goal and thirty-six above it. The same complaint on the old board
reported twenty-one against a measured three.

## What a match would decide

Four things were settled without an oracle and are recorded here rather than filed as facts.

**Is a goal on the track the right place for it?** It is the author's own suggestion and it reads well —
the monument stands between the rails with the train behind it — but it puts the objective in the
narrowest part of the station, four blocks wide between two rails, reached along a trough. That is a
place two defenders hold. The alternative was the terminus deck the old board had, which is open and
which the through station removed.

**Is a one-way drop a route?** The shaft over the deep monument falls twenty-four blocks straight onto
the track — no way back except the stairs, and `aim=reach` prefers it because the walk prices a fall at
nothing. It is kept, kerbed on both storeys so it reads as an edge, and it is the only way in that is
not a stair.

**Is a seventeen-block pillar a route?** The free way onto the viaduct is a stair tower, 94 blocks; the
fast one is straight up off the street, 53 blocks and seventeen placed. That is the decision the deck is
for.

**Is the inside of a station a corridor the brief rules out?** `AUTHORING-BRIEF.md` §3 says the two
teams' ground is joined by a build zone over void and never by a land connection. This board obeys that
at every height. But the *inside* of each half's station is an enclosed hall an attacker walks end to
end, and the through tunnel behind it is a dead-end bore eighteen blocks long. A match decides whether
the shaft, the open bay and two stairs give an attacker enough ways in.
