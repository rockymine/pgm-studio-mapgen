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
| `under` | the rock 1..17 · a room's floor 1..11 · the Stronghold's 1..3 | y12 · y4 | solid rock over every column of the board, with the Liminal Poolroom and its water, the corridor and stairwell east out of it, the Backroom maze and the Stronghold's End Portal Room cut out of it |
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

## The rock, and what is cut out of it

**A layer is one span a column, so a room drawn on it is a room drawn in vacuum.** State the
Poolroom's floor and its walls and nothing else, and every column that is not the Poolroom carries no
span at all: the board's lower half is air, the landmass above it stands on nothing, and the sandy
places read as slabs hanging over a hole. That is the whole of the fault, and the answer is not more
rooms — it is to state the **rock** and cut the rooms out of it.

`under` therefore carries a mass: rectangles at `floor 1`, **seventeen courses thick**, tiling every
column of the 248 × 160 board that no room, corridor, shaft or maze run occupies, and meeting the
landmass's own underside at y18. The rooms are the holes, each a shorter span in the same column with
air over it, and each cut is stated in **both** halves before the rock is drawn round it. The layer
is 373 rectangles: 355 in the rock and 18 in the rooms.

**The rock does not mirror; its holes do.** A shape covering the whole board has its own `rot_180`
image lying over it, so every column would carry the same span twice — which is `SK9`. The mass and
the maze therefore sit in an island stated `mirrors: false` and are stamped once, while the rooms sit
in a mirrored island beside them and their cuts are named for both teams. The tiling is checked
rather than believed: over the board's 39,680 columns, **bare 0, doubly covered 0**.

## The Backroom Space, which is a maze and not a corridor

Thirteen north–south runs on a **20-block pitch**, each **4 blocks wide**, spanning the board end to
end; seven rows of east–west links between neighbouring runs, of which **one in three is left out**.
The omission is what makes it a maze rather than a lattice: what is left is long runs, short links,
loops that return, and legs that end at rock.

The rule that drops a link is `(2k + 1 + 2m) % 3 == 0`, indexed off the origin — and it is stated
that way because the maze has to be **its own `rot_180` image**. A link is indexed by the run on its
low side, so negating both indices shifts a naive `(k + m) % 3` by one and the two teams get
different mazes; doubling the indices and centring the link's own coordinate is what makes the test
even under negation. Both teams walk the same maze.

Each run is then **carved round what it may not open into** — the Poolroom's and the Portal Room's
liners, the east corridor, the stairwells — which leaves 72 segments. Where two segments meet, they
join; where one meets a lined room, it stops at the liner. Floor at y11 in double smooth stone slab,
ceiling at y16 in smooth sandstone, and **four courses of headroom** the whole way, uniform by
construction because the lid is a slab of its own rather than the landmass's underside.

It joins the two Poolrooms and the Stronghold, and it is the one route that crosses the board without
surfacing: **Deep End to Deep End is 188 blocks, no placed blocks, no drops.**

## The Farm

A 12 × 8 plot on the road east of the village centre — `(47, 18)` to `(59, 26)` — dug **one course
below the road** and rimmed one course above it, with a water furrow down its middle. The bed is an
override add themed in a **two-block chequer of dirt and coarse dirt**, so the plot reads as tilled
rather than as a patch of dirt; the rim is the same smooth sandstone every other cut edge on the
board is. Measured across at z=22: gravel road at y36, rim at y36, bed at y34, furrow water at
y34 over dirt at y33.

The furrow is a one-block channel one course deep, which is exactly how the pools are stated — water
in this studio cuts its own bed and fills to a level line, so a furrow is a very small river.

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

**Down to the undercroft, once a side.** A flight of twenty-four one-block treads falls from beside
the Pyramid's door into the corridor that runs west to the Poolroom, and out of that into the maze.
The well it falls through is a hole in the rock but not a hole in the ground layer — see below.

**Across, underneath.** The Backroom maze joins the two Poolrooms round the origin, so a raider can
reach the enemy's Deep End without ever surfacing: **188 blocks, no placed blocks, no drops.** It is
the only way that does not cross the town, and it is dark.

**Out of the water.** The river sits eight courses below everything around it. Stepped slipways are
cut into the two outer banks beside each crossing; the village's own bank has none, because that is
where the wall stands and a flight cut into it is a pit against a wall rather than a way out.

**Up to the sky, only by building.** `…/walk?aim=reach` prices the nearest island at **11 placed
blocks** from a Pyramid's floor and the next at **25**. Nothing on the board walks to one, which is
what an island is.

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
and all. Each of the twenty-four treads is a rectangle at `floor 12` with a thickness one course
shorter than the last, so it replaces the desert's `floor 18` column outright and the shaft is
simply the air left over the treads. The Town Wall, the wall stairs, the slipways, the Small Hills,
the Farm and the Village Well's rim are all the same instrument.

**The shaft is a hole in the rock and the flight rests on it.** A shaft the mass fills is a stair
that descends twenty-three courses onto solid stone six above the corridor it is for, and both spawns
leave the objective chain at `EX1`. So the shaft is one of the mass's holes — the rock stops at its
wall — and the treads start at `floor 12`, which is the room floor's own top, so the two storeys meet
rather than drive through each other (`SK10`). From a Pyramid's floor to its own Deep End is **95
blocks, no placed blocks, no drops.**

## What the board is made of

Ten themes, one per place rather than one per piece.

| Place | Surface | Wall | Fill |
|---|---|---|---|
| the desert | sand over sandstone | sandstone | sandstone |
| the Snowy Taiga | snow lying in patches over grass, over dirt | stone | stone |
| the river region | sand | sandstone | sandstone |
| the Town Wall | stone brick grained with cobble | the same | stone brick |
| a Small Hill | grass over two of dirt | dirt | sandstone |
| the Farm's beds | dirt in a two-block chequer of two shades | dirt | sandstone |
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
traversability connected for both teams. **The dressing pass declines nothing** — every road, house,
tree, pool and channel authored is standing in the world.

Eight `SK11` complaints ride on every stage and all eight are the floating islands: standable ground
with open sky over it and no route onto it, which is what a floating island is.

`GET …/coverage` walks the routes between the places the map is played between and calls the rest
dead: **36.5% of 39,680 columns**, the two largest patches being the outer strip and the moat on
either long edge. A board with a corner spawn, a ring moat and an outer strip nobody has to cross has
dead ground by design; it is a number to watch rather than a fault.

Two plan-level refusals stand and are structural: `G8` (fill-ratio 1, outside the authored band) and
`LN2` (max chain 176, band 25–110). Both are what a board tiled edge to edge with no void in it
measures; neither gates the export.

## Where it departs from the brief, and why

**Nothing places a light source.** The studio has no lamp, torch or sea lantern prop, so the
Poolroom, the corridor and the Backroom Space are unlit and the brief's sea lanterns and lamp posts
are not in the world. The brief's spawn-kit torches are the same gap at the other end.

**The monument's island is bare, by the author's ruling.** The brief puts one oak on each island and
the Skyblock Monument beside the oak on the island nearest the Pyramid. A goal holds a **21-block
square** against every placed prop (`OB19`, `DressingScope.GoalStandoff` = 10) and the widest island
here is **eight blocks across**, so no cell of the monument's own island is far enough from it to
plant on. The monument keeps its island without an oak. Six oaks are authored and six stand.

**An island is reached by building up to it, by the same ruling.** `…/walk?aim=reach` prices the
nearest at **11 placed blocks** from a Pyramid's floor and the next at **25**. An island is not
connected to the board and is not meant to be.

**A chest on each island is not authorable, and the monument's island already has one.** The studio
places a chest at exactly two places, both in `Minecraft/Stamping`: `WoolChests` fills a wool room
(this map has none), and `DefenseChest.Embed` sets one into a bedrock approach wall or **on the
ground beside a monument**, from `StructureStamper.StampPlatform`. Read back at `(74, 22)`: obsidian
at y56–57, **a chest at y54**, grass at y53 — the Floating Garden's island has its supply already.
There is no prop, no document field and no endpoint that places a standalone chest, so the other
seven islands cannot have one without a new prop kind.

**What the prop vocabulary has no word for.** Cacti and dead bushes: `FloraSpec` states coverage, a
period, a fern share, a flower share and a tall share, and nothing else grows from it. Lamp posts,
sea lanterns and the spawn kit's torches: nothing in the studio places a light source, so the
Poolrooms, the corridors and the whole maze are unlit. A spawner. An end portal. The Town Wall's
chests of `Power I` bows — a chest is authored on a `PlanWall`, and this wall is terrain rather than
one.

**Still to build.** The village's gentle four-block relief; the Stronghold's Straight, Prison Hall,
Room Crossing and Library components beside the End Portal Room; and the map-level settings the brief
names — `timelock` off, the build ceiling, the Plains biome.
