# 22 — an indoor pool: water as a shape, not as a channel

**The technique: water in the *surface bucket of a theme*, on a rectangle cut into a room's floor. The
pool is exactly the rectangle drawn — straight sides, one depth, flush with the deck — because nothing
swept it.**

This forks `20-undercroft`: the rock, the hall and the flight down are unchanged. The finish gains one
shape, one theme, and nothing else.

## The document

```json
"themes": {
  "pool": { "surface": { "enabled": true, "depth": 4,
                         "material": { "kind": "solid", "id": 9, "data": 0 } },
            "wall": { "kind": "solid", "id": 159, "data": 9 },
            "fill": { "kind": "solid", "id": 168, "data": 1 }, … }
}
```

and the pool is a patch of the hall's own floor, painted:

```json
{ "id": "basin", "type": "rectangle", "operation": "add", "theme": "pool",
  "floor": 0, "base_height": 8,
  "min_x": -12, "min_z": -8, "max_x": 12, "max_z": 8 }
```

**Same span as the hall around it** — `floor 0` for eight courses, exactly the hall's own column. What
makes it water is the theme, and what makes the theme land only here is that **paint resolves
smallest-area-wins**, which is `03-paving`'s mechanism applied one storey down. Read back:

```
GET …/column?at=0,0       y7..y4  Water
                          y3..y1  Prismarine Bricks
                          y0      Bedrock
GET …/column?at=-13,0     y7      Quartz Block   — the deck, one block away
```

Four courses of water whose surface is at y7, level with the deck it is cut into, and a hard edge
between `x −13` and `x −12`.

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

**The basin is not banded out of the hall, and it must not be.** The rock is banded round the hall
because the two differ in *height* — fourteen courses against eight — and on one layer the taller add
wins the column outright. The basin and the hall are the same eight courses in the same columns, so
neither wins anything: the geometry is identical either way and only the paint differs, which is
resolved by area. That is why a pool is one extra shape and a room is a set of bands.

The rule falls out of the two together: **band where the heights differ, overlay where they do not.**
Getting it the wrong way round is silent in both directions — a banded-out basin is the same world, and
a shorter add inside a taller one is no room at all.

The pool's own depth is its theme's `surface.depth`, so changing four to two is the whole of a shallow
pool. It is not the shape's height: the shape spans the hall's own eight courses either way, and a
shorter shape would be a *hole* in the floor rather than water in it.

## What to look at

| | |
|---|---|
| `renders/world-section-z0.png` | the pool in section: four of water, three of prismarine, deck level, the landmass over it |
| `GET …/column?at=0,0` · `?at=-13,0` | water and deck, one block apart |

```bash
python3 tools/drive.py showcase/22-indoor-pool "Indoor Pool" --out showcase/22-indoor-pool/world
```
