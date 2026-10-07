# Sonnet 5.5 — Ember Reach, an autumn river valley

One half of a model comparison, driven on the deployed studio (`https://pgmstudio.de/api`) with the proxy's
credential. Branch `claude/sonnet55-ember-reach`, board `sonnet55-ember-reach`, map name *Ember Reach*.

## What I set out to build

**A destroy-the-monument board, 16 a side, that reads as an autumn river valley.** One monument a team, a
slow river across the middle, a watermill on each bank, real relief with valley sides, three or more
buildings a team and one place below ground, on an authored plan rather than a composed one.

The board's identity, written before the first request: *a russet valley where a river runs across the
middle, each team's monument stands in an open yard about fifty blocks from its spawn, the valley sides rise
over the lane on both flanks, and a dugout beside the yard is the way in from below.*

The numbers decided first, from `ORDER-OF-WORK.md`: 104 × 224 blocks, `rot_180`, spawns at (0, −102) and its
image, monuments at (−14, −60) and its image, a 32-block gap between the banks (`z = −16..16`) holding the
river and a build zone the whole width. The goal band is `L/5..L/4` of a 204-block lane, 41 to 51 blocks.

The gameplay reading that shaped it is `match-flow.md` §4 and §6 and `approaches.md`. Void belongs between
the teams and not across an approach, and an objective sits exposed with approaches that differ.

Those four are around, above, below and through. The lane is the *around*, the valley sides the *above*, the
cellar the *below* and the houses the *through*, and the gap is the join because the sky is built over it.

## What was built

| Thing | Where (team 0; the image is `(−x−1, −z−1)`) | Measured |
|---|---|---|
| Spawn | `(0, −102)`, hall piece `x −12..12, z −112..−92`, facing +z | ground y20, flat |
| Monument | `(−14, −60)`, `pillar-3` obsidian, float 4 | own walk 51, enemy 165, `GO1` 3.24 |
| Watermill | wings `(8..23, −33..−26)` and `(8..15, −25..−20)`, door +z to the river, `dark-oak-quay-warehouse` | mill pad y14 |
| Miller's house | `(−29..−17, −44..−35)`, door +x, `hay-roofed-stone-and-dark-oak-house` | house pad y17 |
| Granary | `(6..15, −76..−66)`, door −x, the same style, a storey taller | y20 |
| Dugout cellar | floor `x −30..−20, z −86..−74` at y14, roof deck y21..22, stair `x −20..−11, z −82..−78` | six blocks of headroom |
| West valley side | push `x −52..−38, z −88..−30`, +9, falloff 14 | crest y30..33 |
| East valley side | push `x 38..52, z −86..−32`, +8, falloff 14 | crest y29 |
| River | bed `x −44..44, z −16..16` top y3, water to y8 | bank edge y13..14, six above the water |

The relief read says `team: low 14, high 33, level 0.41, largestField 0.144, seams [], silentMarks []`,
symmetry error 0. Three themes, one biome (Mesa, id 37), one flora pass, three gravel-and-andesite roads.

## What could not be said

**A waterwheel on the mill.** I wanted a vertical wheel in the water beside each mill. I searched
`openapi/v1.json` for *wheel*, *waterwheel*, *sluice* and *millrace*: no hits in any of them, which proves
nothing about a structure, because a wheel is a made thing and `techniques/designing-a-structure` is how one
is built. Verdict: **out of reach from where I stood** — not tried, for time. The mills are quay warehouses
on the water's edge.

**Water over void.** I wanted the river to be water with air under it. A fluid prop is a carved bed under a
level fill (`techniques/water`), so the river has ground under it, four blocks of sandstone and sand, and
the plan has to leave a gap for it. Verdict: **mistaken**, in that I looked for an instrument the card says
does not exist. The consequence is real and listed under the open questions.

**A wrong field in `biome` is silent.** I stored `{"kind":"solid","biome":37}` and the store answered 200; the
exported world's chunks read biome 1 (Plains), which I found only by reading them with `tools/anvil.py`.
Re-driving the same document as a dry run answers no `warnings` and no `Pgm-Warnings` header. The field is
`id`. Verdict: **unreachable** — `RQ3` is documented not to reach themes and house styles, and the biome is a
third place it does not reach, not yet in the brief's list.

**Whether the water counts as ground anyone uses.** `GET …/coverage` reads 39.6% dead, and 6 608 of the
6 759 dead cells are the two river patches. I did not look for a way to exclude water, so I cannot say it is
missing. Verdict: **unchecked**; the figure is reported as measured.

## What I got wrong, and why it looked right

**The river as a neutral piece.** I authored it as a lowered piece between the banks, because a river is
ground and a piece is what the plan has. `PL12` refused: an island with pieces the symmetry copies and one it
does not. The refusal was the author's ruling on land connections, stated by the studio.

**The goal at 53 blocks.** I put the monument by the arithmetic `L/4` along the straight lane. `GO1` read
2.66 because the walk goes round the spawn hall; moving it nine blocks forward made 51 against 165 (3.24).
The arithmetic is for a straight lane and this one was not.

**End levees to keep the water in.** `DR-DRY` named 156 open columns and the first was at `(−39, 8, −16)`, a
corner, so I took it for the ends. It was the row `z = −16`, where the pool's ring stopped one column short
of the bank. The levees I built for the ends then joined the banks by land: the walk from spawn-0 to the
enemy monument read *2 placed, scramble +2 at (39, 16)*. I removed them and drew the ring past the edge.

**Five props in the wrong place.** Two trees stood at `x = ±46` on a board that ends at ±44 (`DR-SITE`), one on
andesite (`DR-ROOT`), and two houses on the valley sides' skirts, which dug 6 and 10 blocks (`DR-DIG`). The
skirt of a push reaches `falloff` past its ring, and I had read the ring. I moved all five.

**The watermill's footprint.** Two wings of 15 × 9 and 8 × 6 cells came to 224 blocks over `HP3`'s cap of
192, and the building was not made. A second try overlapped its two wings by a row (`HJ1`).

## What worked first time

**The plan evaluated clean once `PL12` was met.** It read `valid True` with no complaint but `LN5` (47% of
ground off every route, 38% once I narrowed the board from 26 to 22 cells), and `GO1` was in band once the
monument moved.

**The store never refused.** Eight `PUT /source` calls, and the export gate read OPEN after every one.

**The cellar stamped as asked the first time it was stored.** The sunk floor, five sunk steps and the turf
roof came out as drawn, and the transect from the road down the stair reads `rises 5, falls 5, worst step 7`,
the one drop being the roof's edge and not the floor.

**The relief read was clean where it counted.** Symmetry error 0 on every store, and at the final one no seam
and no silent mark. The first stores drew two `RL6` complaints on the hills, which a wider `falloff` and a
`crown` of 4 cleared.

## Open gameplay questions

1. **Is a swimmable river the right air between the sides?** I built water with a bed under it, so an
   attacker can drop in from the bank and swim, and climb out only over a six-block wall. The walk reads
   that as four blocks placed. I decided to keep the bank six above the water on both sides and the bed a
   dead end at the board's ends. A defender who watches the bank can kill a swimmer, a bridge is faster, and
   whether that is a crossing at the right price is the author's to say.
2. **Is the cellar's one entrance in the right place?** It opens on the road from the spawn, east of the
   dugout, not under the monument. A dugout that comes up under the goal is an approach from below; this
   one is a place to hold. I chose the conservative one.
3. **Are the valley sides a hill in the wrong place?** They stand on both flanks, nine and eight over the
   yard, 24 to 40 blocks from the monument. They are neither the frontline nor ground in front of a wall,
   which is the rule I read, but a defender on the east side sees the whole yard.
4. **One monument a team on a 104-block-wide board.** I read the ruling (one a team at 100 or less) and the
   corpus (55% of boards carry one), and followed both.

## What the run cost

| | |
|---|---|
| Wall time, first request to final store | about 11 minutes (the clock read 719 s from the first plan evaluation to a check made just after the last store) |
| Plan stored | 8 times, as part of each `PUT /source`; one version after the first dry runs, the document unchanged between stores |
| Relief stored | 8 times; four distinct documents (hills and cellar added in store 2, house and mill pads in 4, grain in 8) |
| Finish stored | 8 times; four distinct documents (grass band widened in stores 3 and 4, the biome corrected in 7) |
| Stores refused | none. Refused before a store: `PL12` once (the plan evaluation and the dry run, one document), `PT4` once on a dry run (a `cell` on the wall with `rise` 0), and `RQ1` once on a probe after the last store (`origin`) |
| Declines at the export | 8, then 5, 2, 1, 0, 0, 0, 0 across the eight builds |

The three numbers `drive.py` printed on the final store:

```
ground   16496 walked, 108 scrambled, 548 barrier — 3.8% steps further than a player walks
props    42 placed, 0 declined
routes   worst step 5, on route spawn-0 to destroyable-1
```

The worst step is the river: `drop −5 at (1, −16)`, `barrier +5 at (1, 16)`. The barrier cells are the two
river walls and the two cellars' faces.
