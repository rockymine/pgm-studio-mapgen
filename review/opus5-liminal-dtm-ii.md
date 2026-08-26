# Liminal DTM II — a desert town on a plateau, and three floors of it

> Built to a brief from outside this repository. A destroy map for 24 v 24 on a point-symmetric
> desert: a walled village is the battlefield, an oval river rings it, a Desert Pyramid spawn and a
> Snowy Taiga sit on each long edge, and the whole of it is played on three floors — an undercroft
> under the sand, the desert itself, and eight islands hanging over the water.

**In one sentence:** a vanilla Overworld village walled against a moat, with a swimming pool and a
Backrooms maze under it and its own sky above it, and one monument a team on each of the three.

248 × 160 blocks, `rot_180` about the origin, **five sketch layers** (`under` · `lid` · `ground` ·
`bridge` · `sky`), the desert standing at y36 and the highest island's grass at y53. Six
`<destroyable>`s, obsidian, two blocks each.

## The three monuments, and where each stands

| Monument | Storey | Where | Blocks | Own walk | Enemy walk |
|---|---|---|---|---|---|
| **The Desert Well** | `ground`, y36 | `(56, 32)` — on the road in from the Pyramid, inside a well's rim | 2 | 71 | 215 |
| **The Deep End** | `under`, y12 | `(80, 8)` — in the Liminal Poolroom, directly under the river | 2 | 73 | 229 |
| **The Floating Garden** | `sky`, y54 | `(74, 22)` — on the island nearest that team's spawn | 2 | 64 | 226 |

Walks are `POST /plan/inspect`'s, which is the plan's own read. `GO1` wants an enemy-to-own ratio
between 3.0 and 4.0 and these measure **3.03 · 3.14 · 3.53** — the first board of this run to sit
inside that band on every goal, and it took moving the two the brief places near their own spawn.

Both teams' monuments carry the same three names, because PGM prints a stated name verbatim on every
orbit image.

## The five storeys

A layer is a slab: one span per column, one theme, and its height carried by each shape's own
`floor` rather than by the layer's `base_y`, so a course is never counted twice.

| Layer | Blocks | Stood on at | Is |
|---|---|---|---|
| `under` | 6..11, walls to 17 · the Stronghold 1..3, walls to 17 | y12 · y4 | the Liminal Poolroom and its water, the corridor east out of it, the Backroom Space, and the Stronghold's End Portal Room on the origin |
| `lid` | 16..17 | — | the Backrooms' own ceiling, which is what gives that corridor four courses of headroom where the landmass over it would leave six |
| `ground` | 18..35, the river 18..27, the Town Wall to 44 | y36 · y28 · y45 | the desert: the village, the river region, the Pyramid and the Snowy Taiga |
| `bridge` | 34..35 | y36 | four oak decks over the water, one at each gate |
| `sky` | 50..53 | y54 | eight L-shaped islands, obsidian under two of dirt under grass |

One column says the whole thing. At `(80, 32)`, on a bridge over the moat over the Poolroom:

```
y 35  Oak Planks        the deck
y 34  Oak Planks
y 27  Water             the river, four courses of it
y 24  Water
y 23  Sand              its bed
y 22  Sandstone         five courses of rock
y 18  Sandstone
y 11  Light Blue Clay   the Poolroom's floor
y  6  Prismarine Bricks
```

**The stack is written bottom-up**, which is not a preference: the painter walks the layers in
document order and each pass paints its whole column, so a storey listed after one that stands over
it finds no stone left to paint. `under` and `lid` are inserted before the compiled ground; `bridge`
and `sky` are appended after it.

## The Stronghold, and why its floor is eleven courses lower

The End Portal Room stands **directly under the Village Well** and is the one room on the board with
height. It gets it by standing lower rather than by reaching higher: its floor is y1..3 where the
Poolroom's is y6..11, and because every underground ceiling is the landmass's own underside at y18,
that leaves **fourteen courses of air** where the Poolroom has six. The frame is a ring of end stone
one course off the floor, and it is decoration — the brief's golden-apple spawner has no prop in the
studio's vocabulary.

The room is 32 × 32 and its ring is centred on the origin, which is a trap `rot_180` sets: a ring on
the symmetry centre maps onto itself, so a door authored on one side is **filled in by its own
image**. Both doors are stated, and each is the other's image. A stair of eight one-block treads
falls from the Backroom corridor at y12 into it.

**Where it departs from the brief:** four times the vanilla End Portal Room's area, not twice its
height. Fourteen courses is a little over twice a vanilla stronghold corridor and a little under
twice the vanilla portal room, and going higher would mean cutting into the village floor overhead.

## The Liminal Poolroom's water

**A pool is not a basin drawn and then filled.** Water in this studio cuts its own bed below the
surface it crosses and fills that bed to one level line, so a *flat* Poolroom floor and a channel
four courses deep **is** the pool, and the deck is simply where the channel is not. One channel
traced as a rounded rectangle makes the Main Pool; two short ones two courses deep make the Sub
Pools. Measured at `(72, 12)`: water y9–y11 over a prismarine bed at y6–y8, ten courses of sandstone
over it, and the river's own bed at y23.

The bands stop clear of the room's walls, because a channel **cuts anything above its water line
inside its band back to air** — which on a wall is the wall.

## How the board is got round

**Four crossings, and they are the only ones.** The Town Wall stands nine courses over the village
and is open at exactly four places, each where a bridge lands: `x ±72`, `z ±28..36`. A player leaving
a Pyramid or a Snowy Taiga walks the outer strip, crosses an oak deck over the moat, and is inside
the town. There is no other way in on foot.

**Two flights to the wall-walk on each side face.** The gate cuts each face in two, so one stair a
face left fifty-six blocks of rampart with no way up — `SK11` said so by name, at 224 places. Every
flight on this board is stated as **one rectangle per course** rather than as a ramp, because a ramp
at one course a cell rasterizes into treads of two and a two-block rise costs a placed block to
climb. Nothing here costs a block.

**Down to the undercroft, once a side.** A switchback of twenty-four one-block treads falls from the
Pyramid's floor into the corridor that runs west to the Poolroom: 81 blocks of walking, no placed
blocks, no drops. The well it falls through is not a hole — see below.

**Across, underneath.** The Backroom Space joins the two Poolrooms round the origin, so a raider can
reach the enemy's Deep End without ever surfacing: **311 blocks, no placed blocks.** It is the long
way and it is the only way that does not cross the town.

**Out of the water.** The river sits eight courses below everything around it. Stepped slipways are
cut into the two outer banks beside each crossing; the village's own bank has none, because that is
where the wall stands and a flight cut into it is a pit against a wall rather than a way out.

**Up to the sky, only by building.** `…/walk?aim=reach` prices the nearest island at **20 placed
blocks**. Nothing on the board walks to one.

**Out of a Pyramid.** The spawn is a `role: "spawn"` piece 20 × 20, so the compiler sizes the
stamped room to it and `roomStyles.spawn` decides what it looks like: a **hip roof over a square
footprint is a pyramid** — the form's own docstring says so — with sandstone banded in orange clay
the way the vanilla structure's front is, and a floor of `teamTint` wool, which is the brief's red
under Red and blue under Blue without either being stated. Two strokes leave its door: **orange
wool** toward the bridge, and a worn line of **gravel and stone** along the outer strip to the
Snowy Taiga, which is the guideline the brief asks for rather than a road.

## The stairwell, and why it is an override rather than a hole

The obvious way to state a well is a `subtract` on the ground layer with the stair climbing through
it from the storey below. **`SK13` refuses that** — *"a subtract reaches only the layer it is on"* —
and it refuses the same shape when the hole is left by arrangement instead, because the compiler
declares an enclosed gap a `void-N` and emits the subtract itself.

What states it is the **override add**: a shape that overwrites whatever column it lands on, floor
and all. Each of the twenty-four treads is a rectangle at `floor 6` with a thickness one course
shorter than the last, so it replaces the desert's `floor 18` column outright and the shaft is
simply the air left over the treads. The Town Wall, the wall stairs, the slipways, the Small Hills
and the Village Well's rim are all the same instrument.

## What the board is made of

Ten themes, one per place rather than one per piece.

| Place | Surface | Wall | Fill |
|---|---|---|---|
| the desert | sand over sandstone | sandstone | sandstone |
| the Snowy Taiga | snow lying in patches over grass, over dirt | stone | stone |
| the river region | sand | sandstone | sandstone |
| the Town Wall | stone brick grained with cobble | the same | stone brick |
| a Small Hill | grass over two of dirt | dirt | sandstone |
| a stair, and the Village Well's rim | smooth sandstone | smooth sandstone | sandstone |
| a bridge | oak planks | oak log | oak planks |
| the Liminal Poolroom | light blue clay over cyan | cyan clay | prismarine brick |
| the Backroom Space | double smooth stone slab | smooth sandstone | smooth sandstone |
| its ceiling | smooth sandstone | smooth sandstone | smooth sandstone |
| a skyblock | grass over two of dirt | dirt | obsidian |
| the Stronghold | stone brick grained with cracked and mossy | the same | stone brick |
| the portal frame | end stone | end stone | end stone |

**The river is one ground and not two.** Its first draft was a fractal field of gravel into sand,
which is the fault the authoring brief measures on fifty boards: a noise between two *different*
grounds reads as static rather than as texture. The bed is sand, and what says "river" is the water
and the eight-course drop.

**A desert village is sandstone standing on sand**, which is the one case where the "a building is
never the ground it stands on" rule has to give: the brief asks for the vanilla Desert Village
variant by name. What separates a house from its ground instead is the course of **orange stained
clay** under its eaves and the **sandstone-slab** flat roof over them — the two things the vanilla
variant has that the sand does not.

## What the reads say

`GET …/preflight`: **export gate OPEN**. Round-trip clean, mirror clean, buildability clean,
traversability connected for both teams.

Eight `SK11` complaints ride on every stage and all eight are the floating islands: standable ground
with open sky over it and no route onto it, which is what a floating island is.

## Where it departs from the brief, and why

**The Skyblock Monument is bridged to.** The brief puts an island 25–35 blocks over the river and a
monument on the one nearest each spawn, and says nothing about how a player gets up. Nothing on the
board is a walk to one. Stated so it can be overruled.

**Nothing places a light source.** The studio has no lamp, torch or sea lantern prop, so the
Poolroom, the corridor and the Backroom Space are unlit and the brief's sea lanterns and lamp posts
are not in the world. The brief's spawn-kit torches are the same gap at the other end.

**What the prop vocabulary has no word for.** Cacti and dead bushes: `FloraSpec` states coverage, a
period, a fern share, a flower share and a tall share, and nothing else grows from it. Lamp posts,
sea lanterns and the spawn kit's torches: nothing in the studio places a light source. A spawner. An
end portal. The Town Wall's chests of `Power I` bows — a chest is authored on a `PlanWall`, and this
wall is terrain rather than one.

**Still to build.** The Farm, the Backrooms' maze proper (what stands is one corridor a side joining
the two halves through the portal room), the village's gentle four-block relief, and the map-level
settings the brief names — `timelock` off, the build ceiling, the Plains biome.
