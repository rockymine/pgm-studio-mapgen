# techniques/ — small boards, one mechanism each

A `showcase/` folder is a whole map: it compiles, it exports, a server would load it, and its README names
the one thing it demonstrates. A technique card is smaller than that. It is a **sketch board and nothing
else** — no plan, no intent, no objectives, no symmetry — so what a reader looks at is the mechanism itself
with no map around it, and what the card ships is the layout, the reads that check it, and two isometrics.

Each card holds several **plots** side by side, one per variation, because a mechanism is easiest to read
against the same mechanism arranged differently. Every plot is its own group with `mirrors: false`, on a
board whose `setup.mirror_mode` is `none`.

```
<concept>/
  README.md                what it shows, the document that says it, the one mistake it guards against
  <concept>.layout.json    the authored board — open it in the studio as `technique-<concept>`
  *.txt                    the reads: columns, sections, walks, whatever the card is checked by
  iso.png · iso-turned.png the board from the south-east and the south-west
```

| Card | Shows |
|---|---|
| `flat-ground` | one island reshaped a vertex at a time, then tilted — and the three routes that move one point |
| `curved-outlines` | a circle, a lasso, a bowed edge and rounded corners |
| `combined-shapes` | four shapes as one island, flat and at four heights, and how an overlap decides its paint |
| `polylines` | edge styles, a land bridge, a rising line and a thin wall |
| `ramp-and-stair` | five ways up the same eight blocks, and why a flight needs half-block anchors |
| `relief-on-shapes` | a relief over a group, and the three ways a shape stays out of it |
| `tunnels` | a bore is a flat base, two walls and a top layer — with a corner, a change of level, a crossing and two storeys |
| `tunnel-mouths` | where a bore meets the sky: a cut, a terrace portal, a skylight, a stairwell |

Read `tunnels` before `tunnel-mouths`: the second assumes the stack the first sets out.

## Reads a technique card is checked by

None of them is a picture. A card claims something about a column, and only these answer about one.

| Read | Answers |
|---|---|
| `GET /api/map/{slug}/column?at=x,z&format=text` | what is actually there, block by block. Every other read is a projection |
| `GET …/render/section?axis=&at=&from=&to=&format=text` | one cut as characters. `axis` names the direction the cut *runs*, so `at` is the other coordinate |
| `GET …/walk?from=x,z,y&to=x,z&aim=reach&format=text` | whether a flight or a bore is walked, and the worst step in it. On a stacked board the `y` picks the storey |
| `POST …/sketch/columns` | the built world as per-column runs — what `tools/render/iso.py` draws every picture here from, and what its `cavities` scan reads to report covered space |
| `GET …/themes/census?format=text` | cells and share per theme, where the card paints with themes rather than materials |
