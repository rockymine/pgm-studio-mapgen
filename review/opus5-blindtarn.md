# Blind Tarn — the corrie is the no-man's-land

> A destroy board whose middle is a corrie: a bowl with a frozen tarn in the bottom. Every
> attack goes down into the open, across or round the ice, and up the far side under
> everything on the rim.

**In one sentence:** the board's whole middle is a hole, and the two monuments stand on the
outer slope beyond it, so an attack is a descent and a climb with no cover in between.

80 × 192 blocks, `rot_180`, fell surface 24, rim 30, tarn floor ~10.

## What makes the bowl

A **`push` with a negative crown**. Nothing else in the studio makes a corrie: a mark is a
constraint honoured exactly, so an `area` mark is a flat disc and a `point` mark at radius
is a drum on a sheer wall. A push takes a drawn ring and moves the solved surface inside it,
and a *negative* crown dishes the ring instead of doming it.

    {"id": "corrie", "amount": 6, "falloff": 14, "crown": -20, "ring": r32}

`amount/falloff` = 0.43 a block against `crown/half` = 20/32 = 0.63 — 1.45× apart, inside
what `RL6` calls a step. A range whose two gradients disagree is a cliff with a hill on it.

Four instruments, each doing only what it can:

| | |
|---|---|
| push, negative crown | the corrie — the one thing no mark can be |
| push, positive crown | the headwall behind it, so the rim is not level |
| `area` marks | the four flats a player stands on, **all outside the corrie push** — a push is added to the surface the marks solved, so a mark under one moves with it |
| `height_mode: raise` | the moraine bar and the ice pan, applied *after* the pushes, which is the only way to state a height inside a push and keep it |

## Numbers

`GO1` own 47 · enemy 154 · **ratio 3.28** · slopes **12 945 walked, 1 657 scramble, 758
barrier**, faces 20 · claims **placed 8, declined 0** · coverage **13.6% dead** — the best of
my four · export gate OPEN.

Incline: 45.9% under 10°, 25.7% at 40°+. Crossing rim to rim measures 14 rises, 14 falls,
worst step 4, walked; dropping onto the ice is a −6 bank you can walk back out of.

Four themes and the census agrees: `fell` 65.2%, `crag` 18.5%, `tarn` 10.8%, `ice` 5.5%.

Biome **Ice plains**. Snow and ice are *blocks*, so a snowfield on `Plains` has a summer
meadow running through it; Ice plains tints grass `#80b497`, which is what makes the two
agree. The snow sits straight on the soil — `PT1` refuses a surfacing block that is not the
top of its stack, so grass under snow is a 400.

## What went wrong, and the one that changed the board

**It was drawn as a capture board and cannot be one.** `MapIntent` carries wools,
destroyables, cores and modes and no control point of any kind; `controlPoint` has no
occurrence anywhere in `openapi.json`; and `MapParser` lists `control-points` among the
elements the studio *refuses to read*. `drive.py` documents a `controlPoints` finish key and
writes it to `intent.controlPoints`, which nothing consumes — `RQ3` naming it unread is the
only report of it. The board became a destroy board with the corrie as its subject.

- **Coverage started at 58.9% dead** with both monuments near the centre line: every journey
  ran down the same corridor and the corrie's two flanks were 9 000 dead cells. Moving the
  monuments out to the flanks so the two roads diverge took it to **13.6%** with nothing else
  changed. This was the single largest coverage move of the run.
- The tarn was a **water prop** for three builds and never worked. A pool takes the lowest
  surface its body crosses as its line and empties every column above it, so water drawn on a
  dish digs a shaft: `DR-BANK` measured a straight-sided wall from y15 to y30 at a stated
  depth of 1. The tarn is now **frozen** — ice is a block, the pan is level, and players
  fight on it.
- The pan was first a `sink` with `skirt: 1`, which cuts sheer faces: a **13-block pit** you
  drop into and cannot climb out of. A flush `raise` with a wide skirt is the same flat floor
  with an edge that eases (−6).
- `RL4`: both goal shelves were stated, west and east. The `team` group is **fanned**, so one
  mark of a pair is the pair, and the image pins nothing.
- A `flora` pass claimed **22 cells of 15 000**: ground cover seats on grass and this board's
  flat band is snow. A snowfield carries no ground cover, so it states none.

## Standing complaint

`RL5` — 26% level ground against a bar of 30%. A corrie is a bowl; the flats are the ice, the
two goal shelves and the spawn aprons, and grading more of it would delete the subject.
