# 02 — one theme, five buckets

**The technique: what a `TerrainTheme` actually paints, bucket by bucket, and how to check it.**

This is the folder's **base board**: a plain 100 × 100 square with a theme on it, and nothing else. Two
pieces, two spawns, one destroyable a side, `rot_180`. It scores **0** against the evaluator with no
violation and no lint, so anything a showcase's evaluation says is about the technique rather than about the
board — **and it is the fork parent for `03` onward**, since a showcase about a cliff should not also be a
showcase about a board.

## The whole document

```json
{ "authors": ["Opus 5"],
  "roomStyles": { "spawn": "@showcase-hall" },
  "themes": { "meadow": { … } } }
```

**Nothing here ships a default room shell.** A spawn with no bound style stamps a bedrock box, so the board
binds `tools/styles/showcase-hall.json` — a shipped preset forked into the library's three tone families:
ground **verdant + dirt**, built **grey stone + loam**, accent **brick**. Everything below is the third key.

## The board under it

```json
"globals": { "cell": 5, "symmetry": "rot_180", "maxPlayers": 8, "surface": 9, "observerY": 40 },
"pieces": [ { "id": "field", "role": "piece",  "rect": [-10, -10, 20, 20] },
            { "id": "camp",  "role": "spawn",  "rect": [ -2,   6,  4,  4] } ],
"placements": {
  "spawns":       [ { "id": "spawn-1", "piece": "camp", "at": [2, 2], "facing": "front" } ],
  "destroyables": [ { "id": "destroyable-1", "style": "pillar-2", "at": [0, 4.4],
                      "materials": "obsidian", "float": 2, "name": "The Cairn" } ] }
```

Twenty cells square at five blocks a cell is 100 × 100 blocks, `x −50..50` and `z −50..50`. `rot_180` fans
the one spawn and the one destroyable onto the far half, so the document states half a board and the compile
produces both: spawns at `(0, ±40)`, cairns at `(0, 22)` and `(−1, −23)`. `/plan/inspect` reads the pair at
**own 20 · enemy 67 · ratio 3.35**, inside `GO1`'s 3.0–4.0 band, which is the one number that pins where a
destroyable may sit on a board this shape.

A destroy board is deliberately the mode here rather than capture-the-wool: it needs no lane, no technical
void and no strait, so the square can be **empty**, and an empty square is what makes a technique the only
thing in the picture.

No `themeById`, no `mapTheme`: the driver makes the registry's first key the map default, and a shape naming
no theme paints with the default. A board that wants one theme therefore says one theme, once.

## The five buckets, and where each one lands

A theme is not a colour. It is five statements about a *column*, and each is visible at a different place on
the board:

| Bucket | Is | Lands |
|---|---|---|
| `surface` | a `TopBand` — material plus its own `depth` | the top `depth` courses of every ordinary column |
| `fill` | a bare material | everything under the surface band, down to the bedrock |
| `rim` | a `TopBand` — its own material and depth | the **top course of the outermost ring**, where the ground meets what `rimEdges` names |
| `wall` | a bare material | the **face** under the rim: the exposed side of the ground |
| `bedrock` | a height | the courses at the bottom |

Two column reads prove all five, and they are the check to take rather than a picture:

```
GET /map/02-theme/column?at=-50,0      the outermost column — rim and wall
  y 8   Cobblestone     ← rim, depth 1
  y 7   Coarse Dirt     ┐
  y 6   Dirt            │ wall: a layered stack read downward
  y 5   Dirt            │
  y 4   Andesite        │
  y 3   Andesite        ┘
  y 2   Stone           ← fill, once the stack has handed over
  y 1   Stone
  y 0   Bedrock

GET /map/02-theme/column?at=-49,0      one block in — surface and fill
  y 8   Grass Block     ← surface, depth 3, its first course a voronoi
  y 7   Dirt
  y 6   Dirt
  y 5   Stone           ← fill
  …
  y 0   Bedrock
```

**The rim is one column wide and the wall is what is under it.** That pairing is the thing most easily got
wrong: a rim with no wall behind it is a coloured line floating on a face made of fill, and a wall with the
rim disabled is a face with no lip. `rimEdges` decides which edges get one at all — `void`, `drop` or
`boundary` — and this board says `void`, because its edges are a coast over nothing.

## What the surface is made of

```json
"surface": { "enabled": true, "depth": 3, "material": {
    "kind": "layered", "axis": "depth", "beyond": { "kind": "solid", "id": 1 },
    "stack": { "ending": "handOver", "bands": [
      { "thickness": 1, "material": { "kind": "voronoi", "seed": 7, "cellSize": 16, "bands": [
          { "depth": 1, "material": { "kind": "solid", "id": 3, "data": 1 } },
          { "depth": 1, "material": { "kind": "solid", "id": 2 } } ] } },
      { "thickness": 2, "material": { "kind": "solid", "id": 3 } } ] } } }
```

Read outward-in. A `layered` stack claims courses downward from the top of the bucket, so the first band is
the turf and the second is the two courses of soil under it; `handOver` means the fill takes over once the
stack runs out, which is why the fifth bucket needs no mention here.

The turf itself is a `voronoi`, and **its bands read from the edge of a cell inward** — `bands[0]` is the
1-block seam between patches and `bands[1]` is the patch. Written the other way round the board comes out
brown with green veins, which is what the first attempt here did.

**Two families, not one.** Grass Block is `verdant` and Coarse Dirt is `dirt`; the ground reads as one thing
with a texture rather than as five near-identical blocks. `GET /terrain/blocks` names all nineteen families
and which blocks are in each. `cellSize` is the dial that decides whether the pattern reads at map scale: 9
gives a mottle, 16 gives patches a player walks across.

## Grey on grey does not work, and the preview says so

The wall started as a `wallRun` of Stone stripes against Cobblestone stripes. `POST /terrain/theme-preview
?format=png&view=wall` answered a **flat grey square**: `#7e7e7e` against `#7a7a7a` is not a stripe, it is one
colour. Stone, Andesite, Stone Bricks and Cobblestone are all some shade of grey, and a pattern built out of
one tone family is a pattern nobody sees.

What replaced it is the reason the face reads at all: the wall is the *section through the ground above it*,
so it is a soil profile — turf-line, two courses of dirt, andesite beneath — and it agrees with the surface
instead of ignoring it.

## What to look at

| Picture | Says |
|---|---|
| `renders/theme-meadow-surface.png` · `-section.png` | the theme as it will paint, before a world exists |
| `renders/world-ground.png` | the built board in **real material colour** — this is the render that shows paint |
| `renders/world-topdown.png` | the category reading, which paints all ground one hue and shows nothing about paint |
| `renders/world-heightmap.png` | one flat plate at y8 — the ground a technique will move |

`world-topdown.png` and `world-ground.png` are the same board and answer different questions. The top-down
sorts each column into void / water / foliage / structure / ground and paints five deliberate hues; the
ground layer with `material=1` paints the block that is actually there. **Checking a theme against the
top-down proves nothing** — it is not drawing materials.

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true`, no violation and no lint |
| `POST /plan/inspect` | `GO1` **3.35** — own 20, enemy 67 |
| build | 10 000 cells, 1 island; no `SK8` — the board is finished carrying a finish |
| `GET …/coverage` | 2 451 reached · **7 549 dead** of 10 000 = 75.5% |
| extent | 100 × 100 blocks, ground top y8, bedrock y0 |

**75% dead is the board working, not failing.** Coverage measures ground a journey passes, and a destroy
board has no wool to carry back — the only journeys are spawn to cairn and back. An empty square is mostly
ground nobody crosses, which is exactly what a showcase wants: room to put a technique in.
