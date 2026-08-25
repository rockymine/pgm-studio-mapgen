# Thornfell — a capture board with void down the middle and a wool on each spur

`maps/opus5-thornfell` · `specs/opus5-thornfell` · **192 × 294 blocks** · capture, **two wools a team** ·
`rot_180` · 24 players · single layer

Ravensmere's technique on the other kind of board. Where a destroy map wants one open landmass, a capture
map wants a **strait** — ground that stops, void, and ground again — and somewhere for a wool to be that a
raider has to walk out to. So the land branches: two spurs off the back of each half, a wool room at the end
of each, and a range standing behind every one of them.

## The shape, and what states it

Sixteen rectangles a side. The board's z runs 15…145, so the two halves are 30 blocks apart before anything
is drawn — that gap is the strait, and `CT12` measures it. The pieces after the front narrow to a `neck`,
and three things hang off that neck at the same z-band with **void between them**: a spur west, the apron
and the spawn in the middle, a spur east. Each spur carries a `wool-room` piece with a `ledge` either side
of it, and the whole band backs onto a piece that carries a range.

| Interface | Blocks |
|---|---|
| `strand` → `moor` | 140 |
| `moor` → `neck` | 120 |
| `neck` → `spur-w` · `spur-e` | **10 each** |
| `neck` → `apron` | 60 |
| `spur-*` → `room-*` | 20 |
| `ledge-*` → `room-*` | 15 each side |
| `room-*` → `crag-*` | 20 |
| `spawn` → `backdrop` | 20 |

The ten-block interfaces are the whole design: the wools hang off the board on a neck two players wide,
and everything else is 60 or more.

**The ledges are not decoration.** A stamped wool room fills its whole piece and fills downward in bedrock,
so a room piece that is the full width of its spur has a 25-course bedrock cliff for two of its four sides.
A ten-block piece of ordinary ground either side of it, and the pad mark drawn wide enough to cover both,
puts that foundation under the land instead. The same reasoning gives the spawn a `backdrop` piece it shares
an edge with, so the range behind it stands on ground the spawn piece touches.

**The frontline is split rather than spanned.** One zone across the whole 140-block face measured
`frontline-width 28` against a band of `[1, 16]` — `FR6`'s reading of a board a team can cross anywhere.
Two ford zones of 7 cells each give two crossings of 35 blocks with 50 blocks of unbridgeable coast between
them, which is what the rule is asking for.

## The coast is drawn from the compiled outline, not restated

The compiler emits the union of the plan's rectangles: on this board a 36-vertex staircase, which is the
board's *shape* and not its *coast*. Ravensmere redrew its ring by hand, which states the coast twice — once
in the plan and once in the finish, free to disagree. This one is bent instead, by a driver key:

```json
"bendShapes": { "s0": { "k": 0.22, "wander": 3.0, "step": 9, "seed": 5 } }
```

`tools/drive.py` resamples the compiled ring every 9 blocks along its long edges, pulls each **inserted**
point inward by a deterministic wander, and lays Catmull-Rom handles over the result: 36 compiled vertices
became 99 drawn ones. Two rules make it safe on a board like this one. **The plan's own vertices never
move** — a corner that moved would narrow the ten-block neck a spur hangs off, which is the one width the
board cannot spare. And **nothing ever moves outward** — a point that did could close the strait the board
is measured on. Measured after the bend over 23 transects, the strait runs **26 to 28 blocks** and wanders,
against a plan that stated a flat 30.

## The landforms

Constraints state the plan of the board, pushes state its relief.

| | |
|---|---|
| `coast` rim, `shore` | a `line` mark at `h 20` across the head of the strait, so the ground *falls* to the void rather than ending at it |
| `moor`, `neck`, `apron`, `spurpad-w`, `spurpad-e` | the flats a player walks, held at 26 |
| `spawnpad`, `roompad-0`, `roompad-1`, `yard-*` | written **last** — the ground a stamped building stands on wins its cells whatever else wants them |
| 8 hill pushes | `amount` 5–7, `crown` 3–4, `falloff` **20** |
| 3 range pushes | `amounts` 13–17 per ring vertex, `crown` 12, `falloff` 10 |

Read back: `low 20 · high 52 · relief 32 · symErr 0`.

**A range is a wall unless its two gradients agree.** A push climbs at `amount / falloff` over its skirt and
at `crown / half` from the ring's edge to its medial axis, and where those disagree the landform has a step
at its own outline. Both are ~1.7 courses a block here, and each spine is set back far enough that ring plus
skirt stops at `z 125` — the edge of the piece in front of it. That is what decides the height: 20 blocks
between the spawn's back wall and the coast, at 1.7 a block, is `high 52` over ground at 26. The spines
themselves sit past the coast, so the medial axis is off the board and what is on it is one climb from the
wall to the back edge.

**The two ranges behind the wools are what make a spur read as a headland.** A spur with flat ground behind
it is a shelf; one that ends in rock is somewhere the board stops. They are the same push
`showcase/19-mountain-range` is the worked example of, at half the size.

## The rest

Sixteen themes on one cold axis — peat and heather against wet grey rock, with the pale scoured stone of the
tops as the only light in it — and **five seam themes**, each one step off the two grounds it stands
between. The spurs carry a ground of their own (`spur`: coarse dirt, gravel and andesite over the moor's
green) so a raider standing on one knows it.

Four tracks, five blocks across, paved with a `cell` of cobble, andesite and gravel: one out of the spawn to
each wool room, and one down to each ford. A way worn over a fell rather than a street, which is what
separates this board's path from Ravensmere's brick. Measured per block over all **308 cells** of track, no
step is greater than one.

The two steadings are sited by the same search Ravensmere's are — the whole footprint inside a flat, outside
every push's own exclusion, twelve blocks off every track — and each gets a `yard` area mark so the plateau
is stated rather than hoped for.

## What it measures

```
score 1.607 · valid true · symErr 0
intent → generate: 2 teams · 4 wools · 22 regions · 20 filters · 11 apply-rules
mirror check: spawn/protection ✓ wool/room ✓ build ✓
buildability: all 6 spawn / wool / monument placements on solid ground
traversability: spawn ↔ objective chain connected across the build geometry
island team: cells 19093 · low 20 · high 52 · relief 32
export gate OPEN · <maxbuildheight> 72 · 4 region files
strait: 26–28 blocks   (CT12 wants 15–40)
coverage: reached 28392 · decorated 486 · dead 9308 of 38186 = 24.4%
provenance: tree 40 · redstoneline 16 · boulder 14 · flora 9 · stroke 8 · wool 4 · house 4 ·
            spawn 2 · ironcube 2
dressing: nothing declined
```

`render/traversability` answers **one component** across both halves, with the two fords showing as bridged
by a build region — which is what a strait is: not a gap in the board but the part of it players make.

Two soft violations, both the shape of the board. **`G8`, fill-ratio 0.655** — the band was learned from
boards with holes in them, and this one's holes are the strait and the void round the spurs, which is less
than the band expects; the ledges either side of each room fill in more of it again. **`LN2`, 150** measures
the longest run of collinear land-joined pieces, which here is the widest single piece: the `moor` is 150
blocks across, and a board that has to hold two spurs reaching to x ±95 cannot be 110 wide.

**24.4% dead ground**, against Ravensmere's 36.7% — a capture board spends less of itself on scenery because
the routes go to four places rather than one. The largest patches are the ranges: 1625 cells behind each
spawn and 1353 behind each wool. That is what a backdrop is.

## What the two rounds of correction cost

Three faults, all of them invisible above the terrain and all of them measured with a column read.

**The ranges were walls.** `amounts 22–36 · crown 16 · falloff 12` gave `high 80` on ground at 26, with the
climb concentrated at the ring: 26 courses over the eight blocks of skirt, then a shallower dome. Section
`axis=z at=0` shows it as a vertical face. The fix is the gradient, not the height — see the note above.

**The wool room stood on a 42-course bedrock plinth with void either side.** The room piece was the full
width of its spur, so `x −93` and `x −69` at `z 117` were void against room blocks from `x −90` to `x −70`;
and the range's skirt crossed the room, which — pushes being applied after every constraint — lifted the
`roompad` from 26 to 43 and grew the plinth by the difference. The ledges fix the sides, and setting the
spine back fixes the height: the room's floor is `y 25` and the ground either side of it is `y 25`.

**The spawn was buried in its own backdrop.** At `x 0` the building read `y 36–39` with the ground at
`z 120` already at `y 47`, because the range's ring reached `z 119` and the spawn piece ends at `z 125`.
The `backdrop` piece and the set-back spine put the foot of the climb at the building's back wall, which is
where the author asked for it.
