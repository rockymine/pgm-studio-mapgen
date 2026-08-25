# Thornfell — a capture board with void down the middle and a wool on each spur

`maps/opus5-thornfell` · `specs/opus5-thornfell` · **204 × 292 blocks** · capture, **two wools a team** ·
`rot_180` · 24 players · single layer

Ravensmere's technique on the other kind of board. Where a destroy map wants one open landmass, a capture
map wants a **strait** — ground that stops, void, and ground again — and somewhere for a wool to be that a
raider has to walk out to. So the land branches: two spurs off the back of each half, a wool room at the end
of each, and a range standing behind every one of them.

## The shape, and what states it

Twelve rectangles a side. The board's z runs 15…145, so the two halves are 30 blocks apart before anything
is drawn — that gap is the strait, and `CT12` measures it. The pieces after the front narrow to a `neck`,
and three things hang off that neck at the same z-band with **void between them**: a spur west, the apron
and the spawn in the middle, a spur east. Each spur ends in a `wool-room` piece and each room backs onto a
`piece` that carries a range.

| Interface | Blocks |
|---|---|
| `strand` → `moor` | 140 |
| `moor` → `neck` | 120 |
| `neck` → `spur-w` · `spur-e` | **10 each** |
| `neck` → `apron` | 60 |
| `spur-*` → `room-*` | 20 |
| `room-*` → `crag-*` | 25 |

The ten-block interfaces are the whole design: the wools hang off the board on a neck two players wide,
and everything else is 60 or more.

**The frontline is split rather than spanned.** One zone across the whole 140-block face measured
`frontline-width 28` against a band of `[1, 16]` — `FR6`'s reading of a board a team can cross anywhere.
Two ford zones of 7 cells each give two crossings of 35 blocks with 50 blocks of unbridgeable coast between
them, which is what the rule is asking for. Score went from 3.129 to **1.202** on that change alone.

## The coast is drawn from the compiled outline, not restated

The compiler emits the union of the plan's rectangles: on this board a 44-vertex staircase, which is the
board's *shape* and not its *coast*. Ravensmere redrew its ring by hand, which states the coast twice — once
in the plan and once in the finish, free to disagree. This one is bent instead, by a new driver key:

```json
"bendShapes": { "s0": { "k": 0.22, "wander": 3.0, "step": 9, "seed": 5 } }
```

`tools/drive.py` resamples the compiled ring every 9 blocks along its long edges, pulls each **inserted**
point inward by a deterministic wander, and lays Catmull-Rom handles over the result: 44 compiled vertices
became 103 drawn ones. Two rules make it safe on a board like this one. **The plan's own vertices never
move** — a corner that moved would narrow the ten-block neck a spur hangs off, which is the one width the
board cannot spare. And **nothing ever moves outward** — a point that did could close the strait the board
is measured on. Measured after the bend, the strait runs **26 to 32 blocks** and wanders, against a plan
that stated a flat 30.

## The landforms

Constraints state the plan of the board, pushes state its relief.

| | |
|---|---|
| `coast` rim, `shore` | a `line` mark at `h 20` across the head of the strait, so the ground *falls* to the void rather than ending at it |
| `moor`, `neck`, `apron`, `spurpad-w`, `spurpad-e` | the flats a player walks, held at 26 |
| `roompad-0`, `roompad-1`, `yard-*` | written **last** — the ground a stamped building stands on wins its cells whatever else wants them |
| 8 hill pushes | `amount` 5–7, `crown` 3–4, `falloff` **20** |
| 3 range pushes | `amounts` 22–36 per ring vertex, `crown` 16, `falloff` 12 |

Read back: `low 20 · high 80 · relief 60 · symErr 0`.

**The two ranges behind the wools are what make a spur read as a headland.** A spur with flat ground behind
it is a shelf; one that ends in rock is somewhere the board stops. They are the same push
`showcase/19-mountain-range` is the worked example of, at two thirds the size.

## The rest

Sixteen themes on one cold axis — peat and heather against wet grey rock, with the pale scoured stone of the
tops as the only light in it — and **five seam themes**, each one step off the two grounds it stands
between. The spurs carry a ground of their own (`spur`: coarse dirt, gravel and andesite over the moor's
green) so a raider standing on one knows it.

Four tracks, five blocks across, paved with a `cell` of cobble, andesite and gravel: one out of the spawn to
each wool room, and one down to each ford. A way worn over a fell rather than a street, which is what
separates this board's path from Ravensmere's brick. Measured per block over all **284 cells** of track, no
step is greater than one.

The two steadings are sited by the same search Ravensmere's are — the whole footprint inside a flat, outside
every push's own exclusion, twelve blocks off every track — and each gets a `yard` area mark so the plateau
is stated rather than hoped for.

## What it measures

```
score 1.202 · valid true · symErr 0
intent → generate: 2 teams · 4 wools · 22 regions · 20 filters · 11 apply-rules
mirror check: spawn/protection ✓ wool/room ✓ build ✓
buildability: all 6 spawn / wool / monument placements on solid ground
traversability: spawn ↔ objective chain connected across the build geometry
island team: cells 18008 · low 20 · high 80 · relief 60
export gate OPEN · <maxbuildheight> 100 · 4 region files
strait: 26–32 blocks   (CT12 wants 15–40)
coverage: reached 28164 · dead 7852 of 36016 = 21.8%
provenance: tree 40 · flora 9 · redstoneline 8 · stroke 8 · boulder 8 · roomfloor 4 · wool 4 ·
            house 4 · spawn 2 · ironcube 2
dressing: nothing declined
```

`render/traversability` answers **one component** across both halves, with the two fords showing as bridged
by a build region — which is what a strait is: not a gap in the board but the part of it players make.

Two soft violations, both the shape of the board. **`G8`, fill-ratio 0.586** — the band was learned from
boards with holes in them, and this one's holes are the strait and the void round the spurs, which is less
than the band expects. **`LN2`, 150** measures the longest run of collinear land-joined pieces, which here
is the widest single piece: the `moor` is 150 blocks across, and a board that has to hold two spurs reaching
to x ±90 cannot be 110 wide.

**21.8% dead ground**, against Ravensmere's 36.7% — a capture board spends less of itself on scenery because
the routes go to four places rather than one. The largest patches are the ranges: 1780 cells behind each
spawn and 888 behind each wool. That is what a backdrop is.
