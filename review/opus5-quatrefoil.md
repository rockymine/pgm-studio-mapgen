# Quatrefoil — four teams, four quarters, one keep

> A four-team capture board on one `rot_90` island: four wooded corner quarters, four pale sand spits on
> the axes, and a high angular keep in the middle that every route crosses and nobody owns.

**In one sentence:** a mossy grey-green moor cut into four quarters that touch nothing, each with a spawn
compound in its corner and a wool room in its middle, joined only by build zones over void — twice out to
the sand spit on either axis, and once down from the keep into the next team's shelf.

196 × 196 blocks, `rot_90` about the origin, cell 2, base surface 9, y 6..55, twelve players a team.
Thirteen pieces in the authored quarter, fanned four ways: nine landmasses, none of them touching.

## The layout is the one that was handed over, at twice the scale

The plan came in drawn at `cell: 1` — a 98 × 98 board. Every gap in it was 6 to 8 blocks, which
`/plan/evaluate` refuses twice over (`G2` corridor width, `G5` gap hop, both hard) and which builds a
board whose crossings cost four blocks of wood. The arrangement is the design and the cell is the scale,
so the cell was doubled and nothing was moved: the same rectangles at `cell: 2` put every hop at 12 to 16
blocks, every lane at 20 wide, and the board comes back `valid`.

Two rectangles could not double with the rest, because their size is a fact in blocks rather than in
cells. A 20 × 20-cell spawn piece is a 40 × 40-block **protection region**, and `ST10` caps one at
20 × 30 — *"past 30 it stops being a room's ground and becomes a field of immunity a team cannot be fought
out of"*. So the corner block stayed 40 × 40 and the spawn region shrank to the 20 × 20 blocks in its
outer corner, with the rest of the block re-tiled as two yard pieces on the two ways out. That is also
what fixed the board's dead ground: with the room in the middle of its yard, `plan/flow` read **12%** of
the board as ground no journey passes, almost all of it the four yards. With the room in the corner and
the yard on the road out, `coverage` reads **1.1%**.

| Piece | Surface | Is |
|---|---|---|
| `spawn` · `yard-e` · `yard-s` | 8 | the corner compound — a 20 × 20 protection region in the outer corner, its yard on the two ways out |
| `march-s` · `march-e` | 9 | the two marches, one to each spit |
| `wool-app-w/n` · `wool-ledge-e/s` | 10 | the shelf, on all four sides of the room |
| `wool` | 11 | the room |
| `arm-outer` · `arm-mid` · `arm-inner` | 7 · 8 · 9 | the spit, on the axis |
| `keep-apron` | 13 | the keep's landing, one per spit |
| `keep` | 18 | the keep |

Every **land** seam on the board steps by one block, so nothing wants a ramp it has not got. The one
stated step is the keep's own wall — 13 to 18 — and that is a carved flight rather than a seam
(`EL1` says so and the flight is what answers it).

## The wool room has ground on all four sides, and that was not optional

A stamped wool room fills its piece and fills **downward in bedrock** to y 0. Where the cell beside it is
void, that reads in the world as a bedrock cliff as tall as the room's floor — here eleven courses, on
two of four sides, looking into the quarter's own bay. The fix is the one `opus5-thornfell` paid for:
a shelf on every side at one riser below the room, four pieces tiling round it (`wool-app-w`,
`wool-app-n`, `wool-ledge-e`, `wool-ledge-s`), all `relief_scope: hold` at 10 with the room held at 11.
Two pads side by side cannot be ramped between, so each one climbs exactly one block over the pad it is
reached from.

The shelf costs the room two more doors — the cage cuts one on every entry seam — and buys back the
raid: the ledge on the room's south side is what the keep's apron bridges down onto.

## The three ways in, and what each costs

Measured with `GET …/walk?aim=reach` from red's spawn point:

| Route | Blocks | Placed | Worst drop |
|---|---|---|---|
| red → its **own** wool | 66 | 0 | 0 |
| red → blue's wool (the quarter clockwise) | 153 | 19 | 10 |
| red → green's wool (anti-clockwise) | 149 | 19 | 10 |
| red → yellow's wool (opposite) | 207 | 25 | 11 |

A team's own wool is 66 blocks of walking and costs nothing. Every other team's costs nineteen placed
blocks at least, because there is no land route anywhere on this board: each quarter is its own island
and the three build regions are the whole of the connection.

- **`bz-arm`** — one region lapping a spit and both quarter gaps either side of it, 16-block hops. This
  is the flank: out of the compound, down the march, across onto the sand, and up into the next team's
  march. It is the long way and it is the one an attacker is seen on.
- **`bz-cross`** — the spit's inner hop onto the keep apron, 12 blocks.
- **`bz-raid`** — the apron down onto the next quarter's wool shelf, 14 blocks and three blocks of fall.
  This is the short way, it is one bridge a defender can watch, and it lands beside the room rather than
  at the far end of the quarter.

The keep is therefore not scenery: it is the junction all four spits meet at and the only place a raid
can start from. It is also 5 blocks above its own aprons and 9 above the sand, so standing on it is
standing over everything.

**The mid build region never touches a wool piece** (`BZ6`) — `bz-raid` docks the shelf, four blocks
clear of the room's own edge.

## What the ground is made of

Four themes, and the palette is five colours the author named, resolved through `GET /api/terrain/blocks`
to the nearest block that is *ground* rather than a stated shade — no stained clay, no wool, no glass.

| Asked for | Hex | Built with |
|---|---|---|
| Muted teal | `#ABC4AB` | mossy cobblestone `#6e7b62`, mossy stone brick `#74796a`, prismarine brick `#63a08f` |
| Camel | `#A39171` | coarse dirt `#7e5a3c`, sandstone `#d9cfa1` |
| Pale oak | `#DCC9B6` | smooth sandstone `#d8cea0`, sand `#dbd3a0` |
| Grey | `#727D71` | mossy cobblestone, cobblestone `#7a7a7a`, stone brick, andesite |
| Coffee bean | `#6D4C3D` | podzol `#5d421f`, spruce planks `#725430`, dark oak `#422b14` |

| Theme | Share | On | Says |
|---|---|---|---|
| `moor` | 63.1% | the quarters | a **cell of two blocks** — moss against bare earth — over dirt over coarse dirt; rim **off**, because a rim caps every fall a relief solved and turns a hill into contour lines |
| `brake` | 12.9% | ten authored splotches | podzol and coarse dirt: bare ground worn under the trees, and the beds cut into the keep |
| `strand` | 13.1% | the four spits | sandstone, sand and gravel — a mottle, because two blocks on a bar that size read as a deck |
| `keep` | 10.9% | the keep and its four aprons | **made**: a 4-block checker of smooth sandstone and sandstone for the deck, a chiselled kerb on every drop (`rimEdges: drop`), and a `layered` face of cornice · smooth sandstone · **prismarine band** · stone brick · andesite |

The borders are drawn rather than sampled: `brake | moor` 956 cells, `moor | strand` 432, `brake | keep`
204, and nothing else meets anything — the moor and the sand are on different islands.

Three families were named out loud before anything was painted. **Ground** is the mossy moor and the pale
sand. **Built by a team** is pale — polished diorite and mushroom stem, in the spawn hall and the wool
cage alike, so a team's own architecture reads as one thing from across the board. **Built long ago** is
the keep's sandstone masonry. The lookout on each swell is the fourth and is deliberately none of them: a
timber shed, coffee-dark against grey-green ground, because a building is never the ground it stands on.

## The terraforming is pushes, and the marks are one

A relief mark is a constraint honoured exactly, so the only mark on this board is the `area` that holds
the ground outside the spawn door level whatever else happens to it. Every landform is a **push**:

| Push | Is | Gradients |
|---|---|---|
| `bank-w` · `bank-n` | the bank along the map's own rim, behind each compound | 5 over a 7-block skirt · crown 2 |
| `swell-south` | a hill in the south march | 5 over 11 = 0.45 a block · crown 3 over ~8 = 0.37 |
| `dell-east` | the same shape dished — a **negative crown** makes a corrie | 3 over 10 · crown −4 |
| `spit-crown` | the sand bar crowned down its middle | 4–5 over 8 · crown 2 |
| `shelf-knap` | a knap on the shelf's outer shoulder, overlooking the raid landing | 3–4 over 8 · crown 3 |

The swell and the dell are the same idea taken both ways, and they are **not** each other's mirror: a
team's two ways out of its own compound are a high road and a low one. Both rings are 13-vertex lobes,
because an `area` or a push ring written as a rectangle builds a mesa with sheer sides that reads in the
heightmap as a literal square.

The first pass of this board had `swell-south` at crown 4 over a falloff of 8 on a 9-vertex ring with
wobble 0.2, and a transect down `x = −72` read **8 · 8 · 8 · 14** — a six-block wall where a hillside was
meant to be. A range is a wall unless its two gradients agree; widening the skirt to 11, dropping the
crown to 3 and rounding the ring took the board from 221 scrambled and 18 barrier steps to **36 and 10**
in the relief read.

Read back on the built world: **22,936 cells walked, 524 scrambled, 248 barrier**, 16 barrier faces, and
the largest of them (21 blocks at `x −10..−5, z −26..−20`) is the keep's own wall, which is the one face
on the board that is supposed to be one.

## The keep is drawn, not solved

`keep-apron` and `keep` carry `relief_scope: exclude`, which takes them out of the elevation model
entirely: flat where they are stated, sheer where they end. On top of that, five authored shapes:

- **`keep-ramp`**, one per apron — a `height_mode: level` polygon with `anchor_heights` running 13 → 18
  over sixteen blocks. That is a course every third block; a rise wants at least twice its run before it
  starts building treads of two, and this has three times.
- **`keep-t1` · `keep-t2` · `keep-t3`** at 19, 20 and 21 — three concentric terraces, each a single
  walkable riser over the one below.
- **`keep-bastion`** at 20, on the deck's corner, fanned four ways — cover on a platform that would
  otherwise be a table, and the shape that makes the keep read as built from across the board.

Everything on it is a right angle, and the `keep` theme's kerb runs round every drop, which is the
contrast the board is built on: the four quarters are rolled by pushes and have no rim at all.

## What lets the keep go green

Eight beds are cut into the deck — `brush` shapes in the ordinary form a paint patch takes
(`operation: add`, `base_height: 1`, no override), themed `brake`, so the deck is opened to podzol and
coarse dirt. Over each, a `flora` outline at coverage 0.55 with a third of it flowers; in two of them a
six-block birch. Mossy angular boulders stand at the foot of each ramp where the made thing meets the
ground it stands on. The keep is 40 × 40 blocks of pale masonry with plants growing out of its edges.

## The coast is bitten, not bent

`bendShapes` is the driver's instrument for an organic outline and it is wrong for this board: it bends a
whole compiled ring, and every ring here shares an edge with a neighbour it must keep touching. Bowing a
seam a player walks stops the two pieces touching. So the coast is irregular where it can be — five
`subtract` bays, each on an outer edge, none across a seam and none across a face a build zone docks:
two in the compound's rim, two in the marches' outer coasts, one at the tip of each spit.

## What is left, and what it is

- **`G8` fill-ratio 0.637 against an authored band of [0.201, 0.542]** — soft, and knowingly out of band.
  `G8` measures the plan's rectangles, which know nothing about a layout `subtract`; the built board is
  smaller than the plan by five bays. Meeting it would mean cutting the handed-over arrangement rather
  than scaling it.
- **`SP2` — "spawn not near the back of its lane"** on all four. The spawn sits in the outer corner of
  its own compound, which is as far back as this board has; the rule's own text says the lint
  approximates "back" per piece and misreads a spawn placed mid-chain.
- **`EL1` — the keep's 5-block step.** Answered by `keep-ramp` rather than by flattening the keep.
- **`FR9` ×2 — a 14-block and a 12-block crossing face** where 15 is wanted. Both are the raid bridge,
  and it is meant to be the narrow one.
- **`WX11` ×4 — the lookout stands 4 blocks above the cell beside it**, so its foundation fills that
  face in bedrock. It is a shed on a hill crown and 4 courses is a plinth rather than a wall; benching it
  would put a flat pad in the middle of the one landform the quarter has.
- **`06-claims.txt`: placed 132, declined 0.** Every prop on the board is in the world.

## The open question

**Twelve players a team is the number the handed-over plan carried, and it is kept.** `maxPlayers` is
documented as *"how many players the board is sized for, across all teams"* and the export writes it as
each team's `max`, so this board loads as 12 v 12 v 12 v 12 — forty-eight players on 23,708 cells of
ground. For a four-team rush board this reads high, and the number is a gameplay call rather than a
measurement, so it is recorded here rather than changed.
