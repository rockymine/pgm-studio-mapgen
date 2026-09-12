# Glassmere — the one black thing on a white board

> A destroy-the-core board on two snowbound shores of a mere whose middle never freezes. The whole of
> an attack is the decision to start bridging where everybody can see you do it.

**In one sentence:** everything on this board is white, low and legible except the gulf across the
middle of it, so there is nothing to hide behind on the way over and the only question is *where* you
cross — twenty-four blocks at a headland, forty in a bay.

80 × 220 blocks, `rot_180`, one terrain shape, maxPlayers 12, ground y14..y34, build ceiling y54.

## The board is two pieces and a relief

`shore` and `bield`, both at surface 14, so they fuse into **one** shape and the board's shape is the
relief's rather than the piece list's. There is no theme per piece here because there is no piece to
hang one on.

The relief is four `point` marks at radius 4–5, three `area` marks where flat is actually the point —
the apron a bridge lands on, the shelf the Beacon stands on, the floor the bield opens onto — and a
one-block grain. 12 473 cells walk, 200 scramble, and **36 are barrier**, in two faces.

## The coast is drawn, and that is the gameplay

The compiled ring is a rectangle. Nine vertex inserts turn its seaward edge into three headlands and
two bays:

```
(-40,20) (-30,13) (-16,21) (0,12) (15,20) (29,14) (40,20) …
```

Under `rot_180` the image sits opposite, so the crossing is **24 blocks at x 0 and at x ±30**, and
**40 in the bays between them**. An attacker who wants the short bridge has to build it at a headland,
which is the one place a defender already knows to watch. That is the whole design, and it cost nine
calls to `POST …/sketch/shapes/{id}/vertices`.

## What the ground is made of

**One theme.** Its surface is a `layered` stack on the **slope** axis, which is what tells lying snow
from a scoured shoulder from a crag face:

| under 14° | lying snow over two dirt |
| 14–30° | a cell of snow and grass over two dirt — scoured in patches |
| over 30° | bare rock (stone / andesite / cobble, cells nine across with a rise of five) |

The green showing through the white is not decoration: it is where the ground is steep enough for the
wind to have taken the snow off, and the top-down shows it as a map of the board's own angle.

`PT1` refused the first stack: it read snow over **grass** over dirt, and a surfacing block is exactly
one course thick with soil under it — grass may only ever be a stack's top band. Snow over dirt is the
legal form, and the grass moved up into its own band on the shoulder, which is where the cold biome
(`Ice plains`, 12) tints it to sit beside the ice rather than fight it.

## The shore, painted solid first and freckled afterwards

Where two grounds meet, the edge is **drawn** and never sampled: a fractal field between snow and ice
reads as static. So the ice is one **solid** stroke laid right at the water — a `layered` band of ice
over packed ice, radius 5 — and the transition is a **second, wider, worn** stroke over it at
coverage 0.34, carrying snow and ice and nothing else. `worn` is the one path style that spends its
coverage; `rough` fills its band solid, which is how sixteen seam strokes once turned every boundary on
a board into a stripe of a third material.

Two strokes, two materials, and the join reads as a shore.

## Three families, and the one thing that reads from across the mere

Ground is **bright** (snow) over **grey stone**. So what is built is grey stone laid in courses — and
its roof is **dark timber**, which on a white board is the only accent that carries. Every bothy is a
stone hall on a cobble plinth with a dark oak gable at pitch 2, spruce log posts, spruce beams and a
course of laid spruce log in the upper wall for the beams to end on. No footing. No shed roof.

## The dressing, and why each of it is where it is

| | where | why |
|---|---|---|
| the bothy | on the shelf's west end, `x -26..-7` | somebody lit the Beacon; it is outside `OB19`'s box, which is ten blocks about the marker and four round the structure |
| five firs | the crag's lee and the back of the fell | trees grow out of the wind, and none of them stands between the shore and the Beacon |
| five outcrops | the crag, and two on the apron | the apron pair are the only cover a bridging party has |
| three ways | door → Beacon → apron, and a second round the crag | the circulation diagram, drawn. Both ends of every line are attached to something |

32 props placed, **0 declined**.

## Numbers

| read | answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` |
| `GET /rules/terms` | core ratio **3.49** (GO1 wants 3–4); own-spawn walk 47 (GO4 wants 40–90) |
| `GET …/preflight` | **export gate OPEN** |
| `GET …/coverage` | reached 6 319 · decorated 1 531 · dead 5 050 of 12 900 = **39.1% dead** |
| `03-slopes.txt` | 12 473 walked · 200 scrambled · **36 barrier**; 2 faces |
| `…/sketch/relief/read` | 6 450 cells, y14..y34, range 20, 9 barrier steps |
| `06-claims.txt` | placed 32, declined 0 |

## What is left standing

**39% of the ground is dead.** The four patches are the board's own corners, each one block from used
ground. On a board with one objective a side and one spawn a side there are only two journeys to
measure, and the flanks are not on either of them — a path does not make ground used, only a route
does. The honest fix is a second objective or a narrower board, and both would be a different map.
Recorded rather than dressed over.

## What went wrong on the way

- **`PT1`**, above: the first surface stack buried grass under snow.
- **A boulder on a step is half buried.** `scar-1` landed on the crag's own shoulder and `DR-CUT`
  answered that 68 of its 118 blocks were inside something already standing — *"a prop seats on the
  lowest column its feet cover, which on stepped ground is the bottom of a step, so move it onto one
  step or the other."* Moving it onto flat ground was the whole fix.
- **A drawn coast moves the ground out from under the props already placed on it.** Two outcrops at
  `x -38` were `DR-SITE` after the west flank was pulled in to `x -37`; the vertex edits run after the
  store and before the dressing reads back, so the props have to be re-sited against the ring that was
  drawn rather than the one the plan compiled.

## Open, and not the author's to settle here

The crossing is 24 blocks at three headlands and 40 in the two bays between them. Whether that spread
is enough to make *where* a real choice, or whether everyone simply always bridges at a headland, is a
question about how a map plays. Built as stated.
