# Threap Edge — the first King of the Hill board

The studio grew capture points this week: `PUT /map/{slug}/intent` takes a `controlPoints` array, the
export stamps a clay pad per point and writes the `<king>` block with a `<score>` beside it. This is the
first board built through that, and the report is about the four things it taught — two about the
gamemode, one about the relief, and one about a read that lies.

## What the board is

A gritstone edge runs east–west across a moor. Its top is a flat, and the three hills are cut into it:
**The Edge** on the summit at dead centre, **West Nab** and **East Nab** on the shoulders where the crest
steps down. Both teams spawn on the low moor, north and south, 96 blocks apart. The board is 108 × 108.

```
            z −48   ▲ red spawn
        ┌──────────────────────────────────────┐
 z −20  │   ╱ramp                    ramp╲     │   moor, flat at y12
 z  −1  │ ▓▓ West Nab ─── The Edge ─── East Nab ▓▓  the crest: y22 · y32 · y22
 z +20  │   ╲ramp                    ramp╱     │
        └──────────────────────────────────────┘
            z +47   ▼ blue spawn
```

The arrangement is the author's rule for a capture board: one point dead centre and the rest **across**
the line between the spawns, never along it. A destroyable belongs to the team behind it and sits forward
of its own spawn; a capture point belongs to nobody, so it has to be the same walk for everyone, and the
only positions that are the same walk for everyone lie on the map's own axis of symmetry. The nabs sit at
**32 blocks from centre against a 48-block centre-to-spawn distance — 0.67**, which is the corpus median
to two decimal places.

The edge is what makes the three hills one landform instead of three pads on a field. It also decides the
routes: `acrossZ` reports **52 of 108 rows crossable on foot**, so the board cannot simply be walked
north–south. The ways across are the four ramps — one to each nab from each side, authored as two marks on
the north half and fanned — and the low ground at the east and west ends. Take a nab and the crest walks
to the summit end to end; go at the summit face directly and it is four barriers and four scrambles, which
a player with blocks can do and a player in a hurry cannot.

## Rot_180 puts the symmetry centre on a block *boundary*, and that decides the pad's size

The plan compiler images cell `c` onto `−1−c`, so with `cell: 2` block `b` images onto `−1−b` and the
board's centre is the **−0.5 boundary**, not a block. `ObjectiveFootprint.Centred(anchor, n)` puts a
structure's minimum at `anchor − (n−1)/2`, so an **odd** pad centred anywhere lands half a block off its
own mirror, and only an **even** one can sit on the line: size 8 at anchor −1 spans `[−4, 3]`, whose image
is itself. The same arithmetic settles the pair — east anchor 31 spans `[28, 35]`, whose image is
`[−36, −29]`, so the west anchor is **−33 and not −32**. I wrote −32 first, the export duly emitted a pad
one block off its own reflection, and nothing complained: the mirror render reads the *world*, and both
pads were stamped exactly where the intent said. It was the XML that showed it.

**A capture board's points are all stated, every one.** A compiled intent deliberately carries no
`symmetry` — the plan compiler has already fanned the board — so `SymmetryExpander` never runs on that
path and a centre plus one side is a two-hill board. The finish key added for this run (`controlPoints`)
states all three.

## The relief: three tries, and the first two were the same mistake

With `reach: 0` a mark decides the whole surface, so a board carrying one ridge and nothing else ramps
from the ridge to its own corners. Both of the first two builds did exactly that — **29% level, then 16%**,
`RL5` both times, "graded everywhere and left nowhere to stand", and `faces: 0`. My second attempt made it
*worse*, because I had read the skill's tread warning and taken the tread off the ridge; the tread was
never the problem.

The fix is one mark, not a setting: **pin the flat**. An `area` mark over the moor at its own height, and
the ridge's band edge then meets a stated surface on a step instead of ramping into nothing. That alone
moved the board to **48% level, 50 faces, and an incline spread of 49/15/15/7/14%** across the ten-degree
buckets. Then the tread became a real knob rather than a rescue: 5 of the 15-block reach left a narrow top
and a scrambled face; 9 left a flat top the hills stand on and six blocks of genuine barrier.

The theme is one `layered` stack on the `slope` axis, cut at 14° and 32° off that incline read: heather
moor over dirt, coarse dirt on the shoulder, gritstone on the face, and a `wallRun` of bedded stone on the
exposed risers. **One theme, no `themeByHeight`, no second piece to hang anything on.** A column at 0°
answers podzol over dirt, at 18° coarse dirt, at 52° and 68° stone — which is the whole claim, and
`GET …/column?at=` is the only read that settles it.

## The board's own reads do not know what a capture point is

Three of them, and all three are quiet rather than wrong-looking:

| read | what it says on this board | what is true |
|---|---|---|
| `POST /plan/evaluate` | `PL3` — "this plan has no objective — no wool, destroyable or core, so nothing wins the match" | three hills and a 750 score limit |
| `GET …/coverage` | 71.8% dead, the two largest patches dead centre on the nabs | the nabs are the board |
| `04-routes.txt` | "no route between a spawn and a goal" | every spawn walks to every nab end to end |

None of them is a defect in the board, and the export gate opens regardless. But a board whose goals are
invisible to the plan tier, to the coverage read and to the walk read is a board an agent cannot check the
way it checks a destroy board, and `PL3` in particular reads as a refusal to anyone who has not been told.
The routes had to be walked by hand — `GET …/walk?from=0,-48&to=-33,-1` — to establish that the board is
connected at all.

## The spawn is a building, not the shell

The default spawn shell is a plain box with a flat roof and a hole in it, and on a board finished as
gritstone it reads as the one thing nobody drew. The style this board states is a **shooting box** — the
field house a Pennine moor carries — and it is stated in the same finish as everything else, under
`roomStyles.spawn`:

```
y 21  stone bricks                the ridge, two over the eave
y 20  stone bricks                gable, slab-stepped roof over it
y 19  spruce log (laid)           the wall plate
y 18  chiselled stone bricks      the loft band
y 17  mossy stone bricks
y 16  spruce planks               the loft deck
y 13  stone bricks                the room's wall, four courses
y 12  cobblestone                 the plinth
y 10  stone bricks                the plate the whole thing stands on
```

*(`GET …/column?at=0,-53`, the north wall of the red spawn.)*

Two storeys, so the building stands high enough on the low moor to be seen from the crest; spruce corner
posts and glass panes so it reads as framed masonry rather than a block of one material; a **gable** roof
stepped in stone-brick slabs, which is how a flagged roof lies, at pitch 1 over an eleven-deep footprint —
`GET …/render/section?axis=z&at=0` shows the ridge two courses over the eave with the overhang either side,
and that cut is the only read that shows it: from above a gable and a flat roof are the same grey rectangle.

`HS9` caught the one thing I had wrong and was right to. I gave the building projecting beam ends over a
wall of stone brick — *"eight logs sticking out of masonry with nothing behind them, which is not a detail
but a mistake about how the building is put together."* The fix is the detail the building wanted anyway: a
**laid spruce log** as the loft's top course, a wall plate the beam ends actually come out of. A rule that
teaches the building rather than just refusing it.

## What went in the other direction

Two things the studio got right that I would have got wrong by hand. `06-claims.txt` plus
`loop.py --candidates` placed the last two props in **one pass each** after two guesses had been declined
— `DR-KEEP` in the door approach, then `DR-CLAIM` on the peat track I had just drawn — and the claims
raster had both answers in it before I asked. And a **studio bug surfaced through a board**:
`POST /map/from-documents` took `authors` as `[{"name": "Opus 5"}]`, answered 200, and credited nobody,
because the entries arrive as `JsonElement` and both readers took only CLR strings. The only symptom was
`EX6` and a blank observer board. The bare-string form worked, which is why the existing test had never
caught it.

## The hills, as built

| hill | pad (8×8, y) | capture volume | sky marker | distance from centre |
|---|---|---|---|---|
| The Edge | `[−4, 3] × [−4, 3]`, y31 | y31–33 | `[−2, 0] × [−2, 0]`, y57–59 | 0 |
| West Nab | `[−36, −29] × [−4, 3]`, y20 | y20–22 | `[−34, −32] × [−2, 0]`, y57–59 | 32 |
| East Nab | `[28, 35] × [−4, 3]`, y20 | y20–22 | `[30, 32] × [−2, 0]`, y57–59 | 32 |

Every pad is 64 blocks of white stained clay and nothing else; every marker is 7 blocks of white wool and
nothing else. Both are regions the point displays through — the pad as `progress-display-region`, the
marker as `owner-display-region` — so both go the holder's colour on capture and back to white when the
point goes neutral. The marker is the change worth watching from a spawn: a wool room's and a
destroyable's marker name a team for the whole match, and a hill's is the one that moves.

Final reads: **8420 walked · 908 scrambled · 224 barrier · 8 faces**, 40 props placed and none declined,
9614 columns mirrored and none not, export gate OPEN.
