# showcase/ — one technique per map

Every map in `maps/` is a board: a whole design, with a dozen decisions in it at once. That makes them poor
things to learn from. A reader who wants to know *how a cliff is stated* has to find the cliff inside a
thousand-line finish and work out which of its fields are the cliff and which are the map around it.

A showcase is the other thing. It is **one technique, on a board that does nothing else**, so the document
that states it is short enough to read in full and small enough to paste into an example. Each folder here is
a complete map — it compiles, it builds, it exports, a server would load it — and the only reason it exists is
the one line in its README saying what it demonstrates.

## The rule that makes them readable

**Every showcase forks `02-theme` and changes only what its technique needs**, and `02-theme` is
`01-base-board` with paint on it. The base board is the smallest legal capture board there is: two teams, one
wool each behind the spawn line, `rot_180`, a 30-block strait crossed by building, and a hole in each island
that puts the fill ratio in band. It scores **0** against the evaluator with no violation and no lint, so
anything a showcase's evaluation says is about the technique rather than about the board.

That makes the **diff the lesson**. A reader comparing `08-cliff`'s finish against `02-theme`'s sees the
technique and nothing else, and a reader comparing two showcases against each other sees exactly what
separates two ways of moving ground.

**Nothing here ships a default room shell.** A spawn or a wool room with no bound style stamps a bedrock box,
so the base board binds `tools/styles/showcase-hall.json` and `showcase-cage.json` — two shipped presets
forked into the library's three tone families: ground **verdant + dirt**, built **grey stone + loam**, accent
**brick**. Every board in this folder wears them.

## What a folder holds

```
<nn>-<concept>/
  README.md                    what the technique is, the document that says it, what to look at
  <nn>-<concept>.plan.json     the board            — authored
  <nn>-<concept>.finish.json   the technique        — authored
  <nn>-<concept>.layout.json   what was posted      — written by the driver
  <nn>-<concept>.intent.json   what was posted      — written by the driver
  renders/                     the pictures it was reviewed from, including the board grid and the flow
  world/                       region/, level.dat, map.xml — what a server loads
```

The two authored files are the whole of the input. Everything else is derived from them and committed so a
reader can see the result without a running studio.

## Running one

```bash
python3 tools/drive.py showcase/<nn>-<concept> "<Map Name>" --out showcase/<nn>-<concept>/world
```

The driver posts the two documents through the whole pipeline and prints every finding at every place one can
appear. `tools/README.md` documents it; `AUTHORING-BRIEF.md` is the authoring account these were written
against.

## The showcases

Read them in order the first time — each assumes the one before it. `01` is the board; `02` is the board
with paint on it and is what `03` onward fork.

| | Folder | The technique | Stated in |
|---|---|---|---|
| 01 | `01-base-board` | the smallest legal capture board, and what "legal" is measured by | the plan |
| 02 | `02-theme` | one `TerrainTheme` — surface, fill, rim, wall, bedrock, read off two columns | `themes` |
| 03 | `03-paving` | scoping a theme to a patch, picking a pattern legible where it lands, and why an edge is geometry rather than paint | `addShapes` + `themes` |
| 04 | `04-organic-outline` | replacing a compiled ring with a drawn one, bent by Bézier controls — the `elderwold` / `cairnmeadow` coast | `shapePropsById` |
| 05 | `05-steps` | a stair as one plan piece per tread, a theme per tread — and the export gate that will not tell you a step is too tall | the plan |
| 06 | `06-ramp-and-slant` | `anchor_heights`: a ramp below the build cap, a leaning slab above the ground, and the ceiling a tall shape raises for everyone | `addShapes` |
| 07 | `07-hill` | a relief: a `point` mark against a `push`, side by side, and why paint cannot follow elevation | `relief` |
| 08 | `08-cliff` | a `scarp` — two bands with the face left free, so what is authored is a grade — and the two ways up it | `relief` |
| 09 | `09-mesa-and-hollow` | the `area` mark, stacked rings, and the measurement of a push laid over a hollow | `relief` |
| 10 | `10-landform-shapes` | a landform as its own shape — `height_mode`, `skirt`, `anchor_heights` — so it can carry its own paint | `addShapes` |
| 11 | `11-channel` | a `subtract`: relief moves a surface, a subtract removes it, and its height is not read | `addShapes` |
| 12 | `12-underpass` | putting ground back over a cut with an override-add — a bridge with headroom, and the floor it cannot have | `addShapes` |
| 13 | `13-pond` | a basin cut with a negative `crown`, and the water prop that fills it | `relief` + `dressing` |
| 14 | `14-river` | a valley `line` mark and the water course laid in it, one prop per fall | `relief` + `dressing` |
| 15 | `15-boulder-outcrop` | rock at three scales — a prop, a crowned push, an erected slab — and the block that silently gates every prop near it | `dressing` + `relief` + `addShapes` |
| 16 | `16-forest` | a wood is a list of trees somebody placed: an edge, two species, a flora floor, and what a canopy claims | `dressing` |
| 17 | `17-houses` | several buildings in one world — forked presets, roof forms, an L-wing, and a shell used as a boundary | `dressing` + `roomStyles` |
| 18 | `18-wall-and-iron` | the two structures the composer never asks for: a defence wall and a renewable iron cube | the plan |

## The map they add up to

`maps/opus5-whinnymoor` is a whole board built out of them — a slate quarry cut into a moor, at score 0 with
0.0% dead ground. `review/opus5-whinnymoor.md` says which showcase every part of it came from, and records
the one pair that fought: a push and a ramp cannot be matched to each other, because a push is applied after
every constraint the ramp was drawn against.
