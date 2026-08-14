# Tallow Weirgate — a capture board on a drained reservoir

**In one sentence:** a brick mill town on a hub cut through by a sluice, two wool docks standing out at
the board's edges, and one gap between the halves that is walked at one end, bridged in the middle and —
as authored — meant to open late at the other.

142 × 190 blocks, `rot_180` about the origin, base surface 9, build ceiling 24, y 5..41. Two wools a
team, at `(-60, 13, -30)` and `(60, 13, -30)` on the red side and their images on the blue: 120 blocks
apart, inside the corpus band `WL7` measures (46–143).

## The shape, in the order a match uses it

The spawn gatehouse stands on a yard at `z −95..−75`. South of it the **hub** runs the full width of the
board at height 13, and a curved **sluice** is cut clean through its middle — `x −11..11, z −72..−58`,
void to the bottom. A team leaving its spawn therefore chooses east or west at the door rather than
pouring down one middle, and an attacker inside the hub has a long way round that stays out of the
defenders' reinforcement lane. That is the one use `match-flow.md` §4.9 measures for a hub void: the far
side covers 37% of the defender's lane against the near side's 76%.

Below the hub the board splits three ways. Two **mill lanes** at height 14 run down the flanks to the two
**wool docks**; between them an **apron** at 12 steps down to the **front** at 11, which is the only
relief-solved ground on the board and carries the old channel as a `line` mark with a stream in it. Below
that, one gap at `z −20..−10` runs the whole width, and it is crossed three different ways:

| Where | What | When |
|---|---|---|
| `x −45..−25` | the **causeway** — a `level` shape tilting `[12, 11, 9, 10]` from the front's lip down to the mid | walked, from the first tick |
| `x −25..45` | the **millrace** — void under a build zone | bridged, from the first tick, at the price of building it |
| `x 45..70` | a **water lane** — void, authored to open 45 minutes in | **not in the shipped `map.xml`; see below** |

The mid is a 20-block flat with a drawn shoreline and four **sluice piers** standing in it — leaning
slabs, `raise` with `anchor_heights [8, 8, 3, 3]` and `skirt 0`, sheer on their north face and low enough
on the south to be run up. They are the cover the mid would otherwise not have and the anchors the sky
gets built between.

## The two wools are not the same objective twice

The **west** dock's inner face at `x = −50, z −40..−20` carries a pre-built bedrock wall — the plan's
`walls: [{"a": "dock-w", "b": "front", "side": "a"}]`, stamped two thick with a cobweb course on top
(probed at `(-50, -30)`: bedrock y0..13, cobweb y14). That is `match-flow.md` §4.3's prepared line: the
face an attacker who has crossed the race and walked west arrives at, with the lane behind the dock left
open as the defenders' lateral route. The **east** dock has no wall and a single door from its own lane,
and the second way at it was to be the water lane opening late.

That asymmetry is deliberate and it is recorded as an open question in the run report: I do not know
whether asymmetry between a team's *own* two objectives reads as design or as an unfair wool, and
`approaches.md` settles the frame ("the approaches should differ") without settling this.

## The water lane is authored and does not reach the map

`specs/tallow-weirgate/tallow-weirgate.intent.json` carries
`waterLanes.rects = [{45,-20,70,-10}, {-70,10,-45,20}]`. The exported `maps/tallow-weirgate/map.xml`
carries **no `water-lanes` region and no `<include id="water-lanes"/>`**. The cause is in
`SketchWorldBuilder`, which builds its resolved intent with a field-by-field `new MapIntent { … }` that
copies eleven fields and omits `WaterLanes`; the export then re-projects from that resolved copy, and
`WaterLaneGenerator.Apply` clears the region it was about to rewrite. The run report carries the full
entry.

The consequence for this board, stated plainly: the east gap is **permanent void with no crossing at
all**, so the east wool keeps one door for the whole match. That is `WL8`'s default and 79% of the
corpus, so the map is playable; it is simply not the map the documents describe.

## What the ground is made of

Six themes. The board's identity is one sentence — *red brick over drained silt* — and every bucket is
chosen against it.

| Theme | On | Says |
|---|---|---|
| `weir-yard` | the spawn yard | a brick rim, a stone-brick `checker`, and a `wallFrame` that inks brick round every corner of the riser |
| `weir-plaza` | the hub and the apron | polished-andesite rim, a `voronoi` of stone brick / mossy cobble / gravel that reads as laid paving, a `wallRun` of brick → mossy cobble → stone brick |
| `weir-mill` | the lanes, the necks and both docks | brick rim, a `cell` of brick / mossy cobble / dark oak / mossy brick over two gravel, a `layered` riser brick → mossy cobble → cracked brick → stone |
| `weir-silt` | the front and the mid | **rim off**, a `cell` of grass / clay / gravel / coarse dirt / sand with a four-block warp |
| `weir-bank` | the causeway | mossy-cobble rim, a `noise` ramp gravel → cobble → clay → sand, and a `wallDiagonal` leaning the *other* way (`slope: -1`) so the slipway's face reads against the piers' |
| `weir-pier` | the four piers | polished-andesite rim, solid brick top, a `wallDiagonal` of brick / stone brick / mossy cobble, stone-brick fill |

## The buildings

Four styles, written for this board. The **mill house** is the wool cage: brick to a mossy-brick sill
band, dark oak above, laid-log posts, a **gambrel** roof — the one roof form with usable volume under it —
and the shipped `stainedGlassPane` door so an attacker can break in. The **gatehouse** is the spawn: all
masonry, hipped, no timber anywhere, a slab-banded window. The town carries two: a two-storey brick
**counting house** with a pitch-2 gable and no overhang, and a low dark-oak **store** with a shed roof
and a stair-lattice window. Fourteen of them stand on two frontage lines either side of a street at
`z = −67`, with the sluice in the gap between the lines. `--structures` reports **47** structures over
the terrain — 14 × 2 town buildings, 2 × 2 wool cages, 2 spawn cubes, the iron cubes and the goal markers
— which is every one asked for, on both orbit images.

Eight birches stand on one line at `z = −58`, twelve blocks apart. It is an avenue, not a wood: the hub
is a built tier and the only trees on it are planted in a row.

## What went wrong

**The first plan fired a hard `WL8` term.** `POST /plan/evaluate` answered
`wool-ringed-hole … a closure hole is ringed by a wool plateau (two approaches, WL8)` — the void moat I
had drawn between each dock and the front was an enclosed hole with the wool plateau in its ring, which
`ClosureTerms.WoolRingedHole` forbids by name. The compile accepted the plan regardless (the evaluator's
`valid` is not the compile's), but the board was genuinely over-open: three approaches to one wool.
Redrawn so every band spans a contiguous x range and the notches are filled; the term went quiet and the
west dock now has two approaches, one of them walled.

**The wool dock is bedrock all the way down.** `WoolStructureStamper` calls `StampFoundation`
unconditionally, so the whole 20 × 20 dock piece is bedrock from y0 to its surface — probed at
`(-60, -30)`: bedrock y0..11, bricks y12, red wool y13. The `weir-mill` theme is therefore painted on
nothing there. Not a fault; worth knowing before spending a theme on a wool room.

**The mid's shoreline was a ruled line on the first build** and read as a bathtub. Given a Bézier north
and south edge on the second; the heightmap shows a wavy shore with four piers standing in it.

## Coordinates

| Thing | Position | Reading |
|---|---|---|
| red-team's two wools | `(-60, 13, -30)` and `(60, 13, -30)` | blue captures them; monuments in blue's spawn at `z = 77` |
| west defence wall | `x = -50..-49, z -40..-20` | bedrock y0..13, cobweb y14 |
| the sluice | `x -11..11, z -72..-58` | void; the hub's own hole |
| the causeway | `x -45..-25, z -20..-10` | `level`, tilting 12 → 9; probed y9 at `(-35,-15)` |
| the millrace | `x -25..45, z -20..-10` | void under `build-area-1 min="-25,-20" max="45,-10"` |
| the east gap | `x 45..70, z -20..-10` | void, **no lane region in `map.xml`** |
| pier A | `x -56..-42, z -8..2` | stone brick to y15 over a mid at y9 |
| the town street | `z = -67`, two segments either side of the sluice | solid voronoi paving, radius 2 |
| traversability | — | 21 316 navigable columns, 1 258 bridged over void, 8 components, **0 isolated** |
| observer | `(-60, 41, -50)` | over the west lane |
