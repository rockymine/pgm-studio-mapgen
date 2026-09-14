# Birkmire — the last twenty blocks are across open ice

> A destroy-the-core board on a frozen birch mire. White bark on white ground, and one place on it
> with nothing standing at all: the frozen pan the core's holm sits in.

**In one sentence:** everything on this board is cover except the pan, so a raid is a walk through
hummocks and birch that ends with twenty blocks of flat ice nobody can cross unseen.

80 × 200 blocks, `rot_180`, cell 5, `maxPlayers` 20, ground y16–y31, observer y54. Two plan pieces,
eight relief marks, two pushes, five authored shapes, four themes, 44 props. `score 0`, `valid true`,
nothing refused, **nothing declined**.

## The arrangement

`mire` (16 × 15 cells) and `holt` (the spawn row, 6 × 3), with a 20-block void lead down the middle —
`CT12`'s strait, which a raider bridges in the open. Everything else is authored: the pan, the holm,
the bank, the garth, four hummocks, two pushes.

## What the ground is made of

| theme | share | what it is |
|---|---|---|
| `mire` | 61.0% | snow lying on the mire's turf, coarse dirt on the drier flanks, a cut peat hag over 26° |
| `ice` | 34.2% | the pan and the shore of the lead — packed ice under clear ice |
| `holm` | 3.0% | the shingle knuckle the core stands on |
| `garth` | 1.9% | the pad cut into the north-west shoulder that the bothy stands on |

The mire's surface is a `layered` stack on the **slope** axis — under 10° the mire itself, 10–26° a
hummock's drier flank, over 26° a cut peat face — so the one dark material on the board (podzol) can
only land where the ground has an angle. That is the whole of the board's contrast and it sits on a
break of slope by construction.

`PT1` refused the first stack twice over: podzol is a surfacing block, exactly one course thick with
soil under it, and it was stated as the whole four courses of the surface bucket *and* as the theme's
fill. A `cell` is a pick and not a stack, so a surfacing block cannot go in one at any depth over one.
The hag is now one course of podzol over three of coarse dirt, and the fill is coarse over dirt.

Angle distribution over 12 930 cells:

```
00-09° 51.4%   10-19° 24.3%   20-29° 10.6%   30-39° 8.5%
40-49° 3.2%    50-59° 1.1%    60-69° 0.7%    70-79° 0.1%
5.2% at 40° or steeper
```

No spike. `03-slopes.txt`: **12 330 walked, 448 scrambled, 152 barrier, 4 faces**, the largest 48
cells at x 21..35 z −75..−63.

## The marks that had to change, and the one that did not work

`POST …/sketch/relief/read` raised three `RL3` seams on the first build:

| pair | step | worst at | cells |
|---|---|---|---|
| `hum-w` · `pan` | 7 | (−28, 34) | 16 |
| `bank` · `hum-w` | 4 | (−28, 30) | 1 |
| `bank` · `hum-s` | 3 | (6, 27) | 32 |

**A `tread` did not fix them, and it is worth writing down why.** `RL3`'s fix is a tread on the later
of the two marks, narrower than its `r`, so the band past the tread grades into whatever the earlier
mark put there. Applied to `hum-w` at `r 9, tread 3` the seam did not move at all — step still 7 —
and the boundary got **longer**, 16 cells to 21, because the wider radius reached further into the
pan. The same on `hum-s`: step 3 held and the seam went 32 cells to 64. A fourth complaint appeared,
`RL2`, on the extra barrier the wider marks made.

What did fix it was the arrangement rather than the grading: `hum-w` was standing **inside** an area
mark's pinned band, seven courses over it, and no shoulder width closes seven courses against a band
that is pinned exactly. It was deleted — the pan is the one place on this board meant to have nothing
on it, so a hummock in it was off the board's own subject as well as being a wall — and `hum-s` came
down from three courses over the bank to two, which is a scramble and not a seam.

After: `level 0.543`, `largestField 0.250`, `faceCount 6`, **no `RL2`, no `RL3`, no silent marks**, and
two seams both of 2 blocks — `bank | hum-s` over 40 cells and `holm | pan` over 68. The second is the
design: the holm stands two courses over the ice so that stepping onto it costs a placed block
anywhere but the spit.

*This is one board's reading and not a claim about the rule. The tread may well behave as documented
between two `line` or `scarp` marks; what it did not do here was grade a `point` mark's band against
an `area` mark's.*

## The bothy, and the ground it stands on

The first build declined the whole building: `DR-SITE`, no ground under (−37, 85) — the footprint ran
five blocks past the mire's own edge. The fix added an instrument the board did not have: a
**`relief_scope: "exclude"` pad**, x −37..−25 by z 73..83, level at y26. Exclude takes the footprint
out of the relief solve, so the north-west shoulder — which the `swell` push carries to y30 over the
crown and drops to y25 at the track — meets the pad at a **face** instead of being graded into it.
The back of the garth is that face; the track comes in over the low east side, where the two are
within a block. Measured across the shoulder at z 76 before the pad: y26 → y30 → y21 over 20 blocks,
`worst step 2, 0 barrier`.

`HP2` then refused the cross wing at 3 × 5 — a wing holds two walls and an inside, so four each way is
the least any building footprint may be — and it went to 4 × 5.

## The fault-catalogue reads

**Objective hidden — no.** `GET …/column?at=-18,52`:

```
y 64..62   35:14 Red Wool     the studio's marker
y 28       49:0  Obsidian     the core's lid
y 27..25   11:0  Lava
y 24       49:0  Obsidian     its floor
y 17       13:0  Gravel       the holm
```

Six courses of air between the holm and the core, which is `float: 6` doing what it is for: the lava
free-falls six to the holm and has to fall five to count, so a breach over open ground ends it.
Nothing at all between y29 and y61.

**Spawn faces away — no.** Red at (0, 92), `yaw 180`, bearing to the enemy core at (17.5, −52.5) is
**186.9°** — 6.9° off. Blue at (0, −92), `yaw 0`, bearing **6.9°**. Both far inside 90°.

**Spawn faces a wall — no.** (0,92) → (0,78), the first fourteen blocks out of the door:
`rises 0, falls 0, worst step 0: 0 barrier, 0 scramble, 0 drop | walked end to end`.

**Spawn to objective — walked.** (0,92) → (17,−52): `rises 6, falls 8, worst step 2: 0 barrier, 1
scramble, 0 drop | walked end to end`, the scramble a +2 at (7, 36). Passing within two blocks of it:
the spawn, the track, `erratic-1` at (4,61), two birches at (8,43) and (4,41), and the shore track —
which is the board's claim about itself, that there is cover the whole way until there is not.

**Stairs that end nowhere — one authored flight, and it walks.** `spit`, the six-block run onto the
holm for two courses of rise — three times the rise — stated `height_mode: "level"`, `skirt: 0`,
`keepClear`, with a material rather than a theme. The spawn→core transect walks over it end to end.

**Stark contrast with no area separation — no.** `ice | mire` is 690 cells and every one of them is
the pan's own rim, which is an area mark's edge and therefore a bench. `garth | mire` is 74 cells and
that boundary is the excluded pad's face. `holm | ice` is 128 and that is the two-course step the
board is played on.

**Empty board — 16.0% dead.** 12 930 ground cells, 9 371 reached, 1 496 decorated, **2 063 dead**.
The five patches:

| area | centroid | distance to used ground |
|---|---|---|
| 529 | (−35, −49) | 1 |
| 495 | (33, 47) | 1 |
| 472 | (−35, 40) | 1 |
| 460 | (34, −42) | 1 |
| 33 | (−14, −98) | 1 |

All four corners and one sliver behind a spawn, every one of them a block off used ground.

## The gate

```
round-trip       pass
mirror check     pass   spawn/protection ✓  build ✓
buildability     pass
traversability   pass   spawn ↔ objective chain connected across the build geometry
export gate      OPEN
06-claims.txt    placed 44, declined 0
04-routes.txt    spawn-blue → core-1-1: walked end to end
```

## What is open

- **A question for the author, not a claim:** the holm stands two courses over the pan, so the last
  step onto the core's island costs a placed block from every direction except the six-block spit.
  Is that the right price? It makes the spit the obvious approach and therefore the obvious place to
  defend, which may be exactly right for a core board — or may mean the other three quarters of the
  pan are decoration. Nothing in the corpus or in the rules answers it.
- **`largestField` 0.250** on a board whose subject is a flat pan. Worth watching rather than fixing.
