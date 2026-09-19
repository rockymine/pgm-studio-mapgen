--- name: pgm-board-warmup description: The first ten minutes of an authoring run — what this
repository costs to read, what must never be opened, what a board is made of, and how its
grounds are made to meet. Load once, at the start of a run, before pgm-board. ---

# Before the first board

Two things, in order: what reading costs here, and what a board is made of. Together they run
about 12k tokens and ten minutes, and both are done before a plan is written.

## 1. The budget, because this repository is larger than any context window

The documents a run is pointed at come to **~241k tokens** — more than a 200k window holds,
before a single map is opened. `AUTHORING-BRIEF.md` §4's reading list is 187k of that on its own,
and the four briefs and two skills here are the other 54k. Nothing below assumes it can all be
read: open a tool document at the question that needs it, not at the start.

| Read | ~tokens | When |
|---|---|---|
| `00-board.txt` | 0.4–3k | freely |
| one named `renders/*.txt` | ~1.1k median | freely, **named individually** |
| `02-heightmap.txt` · `03-slopes.txt` | 1.3–10k | one board at a time |
| every text render of one board | **30–57k** | never — name the file wanted |
| median `*.layout.json` | ~12k | only through `jq`, never whole |
| `fable-millrace-revamp`, `opus5-slipway` layouts | **397k · 367k** | **never open. Either one ends the run.** |

**Never `cat` a `*.layout.json`.** Two of them exceed a whole window and 27 exceed 20k. A
layout is queried: `jq '.shapes | length'`, `jq '.shapes[] | select(.id=="…")'`. Same for a
large `*.finish.json`.

**A one-line answer is a `grep`, not a file read.** `03-slopes.txt` runs to 10k tokens and its
verdict is one line: `grep 'cells:' …/03-slopes.txt`.

**`specs/` is split, and the split is the reading rule.** Eighteen boards sit flat and are worth
reading; the other 118 are under `specs/archive/` — probes, experiments run to find the limit
of one mechanism, early runs, superseded boards.

**Nothing under `specs/archive/` is a model for anything.**

When a *number* is wanted rather than an example, `GET /api/rules` and `GET /api/rules/terms`
answer in one fetch and are greppable. That is cheaper than any board.

## 2. A board is grounds that meet, and the meetings are the craft

**Decide what the board is about before deciding what it is made of, and keep it to one
thing.** Write the sentence down. If it cannot be written, the board is not ready.

Then: a board is two or three or four *grounds*, each stated by the one instrument that can
state it, and **every join between them is chosen rather than left over**. That is the whole
technique, and it is what separates a board that reads as a place from a board that reads as
one field with a gradient in it.

A shore board, worked all the way through, as the pattern to copy:

| the ground | stated by | why that instrument |
|---|---|---|
| the beach | a relief with flow — marks pinning only the waterline, `grain`, a low `step` | it has to read as deposited, so nothing is pinned that does not have to be |
| the dunes behind it | **a second relief, on its own layer**, held a little higher | relief solves per layer and `ReliefFields` shifts each into world Y, so two reliefs can meet. One relief across both is one field, and no join at all |
| the yard the houses stand on | a shape carrying `relief_scope: "exclude"` | `exclude` takes the footprint out of the solve, so the two tiers meet at a **face**. `hold` lets the relief bring the lower tier *up* to the shape, and then there is no step and no reason for a stair |
| beach → dune | the two reliefs' own meeting, across the layer seam | the join has a shape because two fields made it |
| dune → yard | an authored flight: `height_mode: "level"`, `anchor_heights`, `skirt: 0`, `keepClear: true`, a **`material`** rather than a theme, run **at least twice the rise** | a relief graded across the seam deletes the boundary; a flight states it |
| yard → quay | a ramp of the same kind, or a **polyline** where the join is a wall | |
| the sand ON the beach, the gravel ON the tide line | an add shape carrying a **`theme`**, `base_height` **equal to the ground it lies on**, and **no `relief_scope` at all** | a shape owns the paint only on a cell it *forms the surface of*: one stated lower runs under the ground, paints nothing, and says so on a 200. And a `relief_scope` is a statement about **height** — `follow` seats the shape on the solved field and then pins its whole ring there **rigid**, which over a terrain patch is a floor: the strand solves level to the block and every mark inside it is overwritten in silence |

**One map needn't be one ground.** Plains everywhere is not simplicity, it is one instrument.

### The plan phase is small, and stays small

**The plan states the arrangement and nothing else.** Two shapes it may take:

- **three or four distinct height zones** as pieces, which the sketch then pulls into shape; or
- **one rectangle**, with every landform authored downstream.

A plan that grows a piece per landform is a plan whose paint will grow a theme per piece, and
the board's look ends up decided by how it happened to be cut up. `firnline` is the worked
failure: 13 pieces at 6 surface heights, then a theme per height.

### What makes an area read as what it is

The relief says where the ground goes. These say what the place is, and each one is placed
because there is an answer to *why here*:

- **a landmark sculpted out of layers** — `tools/sculpt/props.py` emits `dome`, `spire`,
  `ring_wall`, `ellipse_wall`, `tapered_tower`, `arch`, `colonnade`, `ziggurat`, `bowl`,
  `crenellated_wall`, `drum_tower` and a composite `gatehouse` as ordinary sketch shapes —
  circles and polygons with a floor and a height, not stamped block soup. A lighthouse is a
  `tapered_tower` under a `dome`; eight of the nine single forms cost one layer. Give the layer **`kind: "made"`** and
  `part_of`, which keeps `SK10`'s pair walk and `SK11`'s reachability walk off it — a solid
  standing in a hill has no gap to lose, and its roof is not a stair somebody forgot.
- **tunnels, walls and undercrofts out of the same layers**, drawn as the complement of the
  space rather than cut with a `subtract`: `SK13` reads a subtract as the board's negative
  space and refuses any add that fills it, on any layer.
- **copied trees rather than the vanilla stamp.** A `copied` recipe carries a `body` block for
  block; `pgm-studio/tools/seed-trees.cs` files bodies out of a world into the library, and
  `showcase/tree-showcase` is the world they come from. State them under names in
  `dressing.styles` and let the placements name those — `specs/fable-millrace-revamp/trees.json`
  is 22 of them, keyed the way its placements name them.
- **boulders, which are stone** — stone, cobblestone, andesite, and nothing else.
- **polylines for anything that flows.** The rasterizer splines a polyline's points before
  offsetting the band, so four points draw as a curve: a wall, a lane, a watercourse.
- **paths that are `solid`**, three blocks a reader cannot quite tell apart, running to a door.

## 3. The ten minutes: read one showcase diff

`showcase/` is one technique per map, and every one of them forks `02-theme` — a plain
100 × 100 destroy board scoring 0 with no violation and no lint — changing **only** what its
technique needs. The diff is therefore the lesson, with nothing else in it.

Read `02-theme`'s finish, then the finish of the two showcases nearest the board about to be
built. `06-ramp-and-slant`, `07-hill`, `08-cliff`, `09-mesa-and-hollow`, `10-landform-shapes`,
`12-underpass`, `19-mountain-range`, `20-undercroft`, `21-wall-and-stair` are the ones that
carry joins. Say what each diff changed before authoring anything.

**Numbers off a finished board are a diagnostic, not a control.** `scramble%`, `barrier%` and
the face count are read out of a built world, and no authoring decision is made against them:
a cliff is settled with `face`, a push with the arithmetic `RL6` measures, a flight with a
transect. Predicting them calibrates nothing, and a predicted figure written into a report
becomes the next reader's bias.

One fact about them is worth carrying anyway, because it is not what it looks like: **barrier
is not the tail of the scramble distribution.** Scramble is ground a player climbs and barrier
is ground a player cannot, and barrier comes from vertical walls and shoreline rather than from
steepness — `opus5-millrace` is the quietest board on the shelf underfoot, at 0.9% scramble,
and carries the most impassable ground in the set at 8.0% barrier.

## 4. Before a board is called done, count its own instruments

Run this over the spec that was just written. A zero is not a fault; **four zeros is a board
that used one instrument and called it terrain.**

```python
# python3 - specs/<slug>/<slug>.finish.json
import json, sys
d = json.load(open(sys.argv[1]))
shapes = list(d.get("addShapes") or [])
layers = d.get("addLayers") or []
for L in layers:
    shapes += (L.get("shapes") or [])
hm = [s.get("height_mode") for s in shapes]
rel = d.get("relief") or {}
marks = [m for g in rel.values() for m in g.get("marks", [])]
styles = (d.get("dressing") or {}).get("styles") or {}
print("reliefs", len(rel), "— two or more is two grounds meeting")
print("marks", len(marks), sorted({m["kind"] for m in marks}))
print("pushes", sum(len(g.get("pushes", [])) for g in rel.values()))
print("level", hm.count("level"), "raise", hm.count("raise"), "sink", hm.count("sink"))
print("made ground", sum(1 for s in shapes if s.get("relief_scope")))
print("polyline", sum(1 for s in shapes if s.get("type") == "polyline"))
print("made layers", sum(1 for L in layers if L.get("kind") == "made"))
print("copied trees", sum(1 for v in styles.values()
                          if isinstance(v, dict) and v.get("form") == "copied"))
```

It reads the **finish the spec generated**, not the script that generated it. A
`build-spec.py` that states a flight through a helper writes `height_mode` once and
uses it four times, and a grep over the source counts one.

And read `05-themes.txt`. A theme registered and not on the ground is a theme that painted
nothing, and nothing anywhere raises a finding for it. A theme at a fraction of a percent is
the same fault: the shape is under the ground rather than on it, or another shape of equal
area is taking the cell.

And `POST /sketch/relief/read` with the stored layout, which is the only read that says what
the marks did to **each other**: `silentMarks` is every mark that landed nowhere, `seams`
names the pairs that meet on a step.

And a seam naming a **shape** rather than a mark is a `relief_scope` pinning ground you meant
the marks to shape.

`level` and `largestField` are the two numbers that say whether the ground has a shape at all;
over about 0.45 and 0.13 it is a table with edges.

## 5. Stop

Load `pgm-board` and begin.