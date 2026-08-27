# 22 — an indoor pool: water as a shape, not as a channel

**The technique: water in the *surface bucket of a theme*, on a rectangle cut into a room's floor. The
pool is exactly the rectangle drawn — straight sides, one depth, flush with the deck — because nothing
swept it.**

This forks `20-undercroft`: the rock, the hall and the flight down are unchanged. The finish gains one
room, one theme, and nothing else.

## The document

```json
"themes": {
  "pool": { "surface": { "enabled": true, "depth": 4,
                         "material": { "kind": "solid", "id": 9, "data": 0 } },
            "wall": { "kind": "solid", "id": 159, "data": 9 },
            "fill": { "kind": "solid", "id": 168, "data": 1 }, … }
}
```

and the pool is a room like any other — a hole in the rock with a floor put back under it:

```json
{ "id": "rf5", "type": "rectangle", "operation": "add", "theme": "pool",
  "floor": 0, "base_height": 8,
  "min_x": -36, "min_z": 26, "max_x": -30, "max_z": 54 }
```

Same span as the hall around it, `floor 0` for eight courses. What makes it water is the theme: the
**surface bucket claims the top four courses** and paints them block 9, and the fill takes everything
under. Read back:

```
GET …/column?at=-34,40     y7..y4  Water
                           y3..y1  Prismarine Bricks
                           y0      Bedrock
GET …/column?at=-37,40     y7      Quartz Block   — the deck, one block away
```

Four courses of water whose surface is at y7, level with the deck it is cut into, and a hard edge at
`x -37/-36`.

## Why not the water prop

A `WaterProp` sweeps a disc along a polyline and **carves its own bed**, then fills it to one level
line — the lowest surface its band crosses. That is exactly right for a river: the bank follows the
sweep, the depth follows the terrain, the outline is organic because a river's is.

It is exactly wrong for a pool. A room's pool is a made thing with straight sides and one depth, and a
swept disc gives it neither: the outline comes out lobed where the discs overlap, the corners round
off, and a pool wider than the sweep needs a second prop down the middle to fill the part the first
one missed. `maps/opus5-liminal-dtm-ii` shipped four props to make two pools that way and they still
read as ponds indoors.

The rule, stated once: **a channel is for water that found its shape; a themed rectangle is for water
somebody built.** `13-pond` and `14-river` are the other half of this pair and use the prop, rightly.

## The one thing to get right

A room nested inside another room is **two floors in the same columns** unless the outer one is banded
round it — a column carries one span a layer, and stating it twice is stating it twice. The generator
bands the hall round the pool for the same reason it bands the rock round its rooms, and the tiling
check says so: over the board's **8,250 columns, none bare and none doubly covered**.

The pool's own depth is its theme's `surface.depth`, so changing four to two is the whole of a shallow
pool. It is not the shape's height: the shape spans the room's own eight courses either way, and a
shorter shape would be a *hole* in the floor rather than water in it.

## What to look at

| | |
|---|---|
| `renders/section-pool-z40.png` | the pool in section: four of water, three of prismarine, deck level |
| `GET …/column?at=-34,40` · `?at=-37,40` | water and deck, one block apart |

```bash
python3 tools/drive.py showcase/22-indoor-pool "Indoor Pool" --out showcase/22-indoor-pool/world
```
