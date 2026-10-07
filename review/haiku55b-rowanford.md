# Rowan Ford — the canonical brief, built (Haiku 5.5)

> An autumn river valley: a slow river runs across the board between the two sides, a watermill on each
> team's bank, one monument a team, real relief, at least three buildings a team and one place below ground.

**In one sentence:** a golden valley on a dry Savanna ground, a team's spawn set on a flat back crest, a
monument on the near bank in front of it, and a sixteen-block river between the two banks crossed by a
build zone that runs the length of the board.

**What it does not yet deliver:** the relief is almost flat, and the below-ground place was not built. Both
are stated in the sections below and in the report, not hidden.

## Measured

Plan cells are four blocks; the world is in blocks. Board 160 × 88 blocks, `mirror_x` about the origin,
base surface 9, 16 players a side.

| The brief said | Where it is | Measured |
|---|---|---|
| destroy board, one monument a team | `monument` on `bank`, at (−61, −38); its mirror at (60, −38) | pillar-3, team-tinted red and blue wool; GO1 ratio 3.33 (own 48, enemy 160 by the plan), walk 46 vs 156 |
| a slow river between the two sides | the void gap x −8..8, the full depth of the board; a build zone `river-crossing` over it | 16 blocks wide; spawn-to-enemy routes place 16 blocks to bridge it |
| a watermill on each bank | `mill-west` / `mill-east`, library style `oak-framed-rubble-house` | at (−26..−18, 8..16), ten blocks off the bank's river face after the DR-PASS fix; 6 props placed, 0 declined |
| real relief, the valley has sides | `highland-crest` h 13 flat, `bank-flat` h 9, `monument-pad` h 9; no pushes | **weak.** One 4-block step from the crest to the bank, walked end to end; 0 scrambled, 0 barrier |
| at least three buildings a team | `mill`, `store`, `lookout` per team | 3 each, all placed; the mirror is the symmetry's own fan |
| one place below ground | none | **not built.** See *What did not get built* |
| autumn | Savanna biome, `{"kind": "solid", "id": 35}`, grass tint #bfb755 | golden-olive ground in the picture |

## The spawn's seat

Measured in the built world, from the report's transect through spawn-0 along x:

- the spawn stands on a flat crest at y13, which runs from x −84 to x −65 — two blocks of land behind the
  spawn before the board's edge, and 17 blocks of flat ground in front of it before the fall to the bank;
- nothing stands higher than the spawn within 20 blocks, so the rise beside it is 0;
- the spawn room is 20 × 16 blocks, the longer side along x, with the spawn in its outer half (SP2) and a
  block clear of both walls (WX4);
- the spawn room carries its own house, `spruce-roofed-oak-cottage` (WX14).

The approaches law puts the spawn "in the land at its back, up to ten blocks into the land". Here it is
two blocks in. The reason is GO1: a spawn further into the land takes the monument's enemy walk below three
times its own. That trade is recorded as an open question in the report.

## The layout

Two grounds meet at the river: the team's own crest and bank, and the void. The crest is the back; the bank
is the front, where the monument, the mill and the store stand. The river is a void gap, not a bed of water,
because an on-axis neutral piece joined the mirrored pieces into one island and refused as PL12. The build
zone over the gap is what lets a team cross it.

Buildings: the mill sits on the bank ten blocks back from the river, the store (`rubble-and-spruce-house`)
to its south-west on the bank, and the lookout (`spruce-roofed-oak-cottage`) on the bank's inner side,
north of the mill, clear of the walk from the spawn to the monument. Each building is placed by declaration
and fanned by the symmetry.

## Techniques used

- **plan**: four pieces a side (the highland in three parts so the spawn room is its own piece, and the
  bank) and one build zone over the void. The on-axis river is not a piece.
- **relief**: three area marks, pinned flat on the crest, the bank and the monument pad. No pushes. No
  `relief_scope` on any shape.
- **themes**: one theme, `valley`. Its surface is a slope-axis band stack: grass over two dirt to 30°,
  dirt and coarse dirt to 45°, then stone, andesite and cobblestone. A depth stack under the grass.
- **dressing**: three house styles by library name, declared in `dressing.styles`; the spawn room style in
  `roomStyles`. The team-1 copies are the symmetry's fan, not authored.
- **biome**: Savanna (id 35), because its grass tint is the nearest of the stated biomes to a dry gold.

## What went wrong

- **The river as a bed piece.** The first plan had the bed on the axis as a neutral piece. It joined the
  mirrored pieces into one island and refused as PL12. The river is now the void gap.
- **Spawn too close to the enemy.** Spawns 104 blocks apart put the monument's GO1 ratio at 2.2 to 2.98.
  Widening the highland to 150 blocks apart brought it to 3.3.
- **Houses with four corners.** A wing takes exactly two opposite corners. Four corners built a 9×1 wing,
  and six buildings declined as HP2.
- **Explicit mirrored houses.** The symmetry already fans a building. The authored copy collided with its
  own fan (DR-CLAIM), so the copies were removed.
- **The lookout's door.** Every `front` value I tried was refused as not a value the field takes. The
  door is left to the building.
- **The below-ground place, twice.** A made storey below the ground is painted as stone and carves nothing
  (the first try, no hole, no room). A subtract carved the room and the shaft: it cut every column down to
  the void, bedrock included. The column at (−45, −28) read `0 solid block(s)` for a whole column. Found
  by `column`, after the store had accepted it at 200. The final build removes both, and the three columns
  that read void now read ground.

## What did not get built

**The place below ground.** The brief asks for one place players can use below ground. The studio's
`techniques/cutting-a-hole` card says a room needs a floor layer under a stated void and a ceiling layer
over it, and that the shaft is the complement of both.

I tried the subtract alone, which carves to the void, and a below-ground storey, which paints stone.
Neither gave a room, and the room is not in the world.

## Decisions and open questions

- **Relief.** I chose three flat marks and no pushes. I reasoned that a higher, sloped crest would cliff the
  monument's pad, and did not test it. The brief asks for sides. The board has a four-block step. A second relief
  sketch, as `ORDER-OF-WORK.md` §3 advises, was not run.
- **The river is a void, not water.** A fluid needs a bed to carve; a void gap has none. The river reads as
  a gap a player must bridge, which matches `approaches.md`'s "a river or a drop forces a bridge". It does
  not read as a river.
- **Dead flanks.** `coverage` reads 30% dead, almost all of it the two south corners behind the stores,
  z 28 to 44. The approaches law says a dead flank is a note on a destroy board, so it is kept.
- **LN5.** A third of the ground is off every route between waypoints (33%). The board is a wide plate
  with a river and two monuments; most of its outer ground is not on a route. Kept.
