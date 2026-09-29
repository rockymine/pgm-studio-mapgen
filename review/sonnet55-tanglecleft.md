# Tanglecleft — a monument on a temple terrace in a jungle cleft

**A jungle where each team's monument stands on a stone-walled terrace with a temple behind it, above a lagoon dell on one side and under a jungle hill on the other.** A dry cleft crosses the south wood under a plank bridge, and dark jungle wood fills the ground between. The four ways in are from below through the lagoon, from above off the hill, round through the wood and through the temple's pillars.

Slug `sonnet55-tanglecleft`, map name **Tanglecleft**, built on the deployed studio. The author's questions on it are notes 23–27 (`reports/sonnet55-jungle-swamp.md`).

## How it is meant to play

**A monument is broken where it stands, so it stands forward, in the open, on the ground the fight comes to.** It is 58 blocks from its own spawn and 183 from the enemy's on the plan tier, a ratio of 3.16 against `GO1`'s 3.0–4.0. The halves meet across a 24-block build zone over void the whole 80-block width.

**The terrace is flat ground at 18 where the monument stands, with the ways in arranged round it.** Below it the lagoon dell lies at 8 and the ground rises ten blocks to the shelf in one-block steps, so the way from below is a long open climb. Above it a hill crowns at 34, 24 blocks east and 16 over the stone, and a player on it shoots down and bridges across.

**The way through is the temple, and the way round is the wood.** The ziggurat's near face is 13 blocks behind the stone with a three-wide stair up it, and four broken pillars stand between them. The south wood runs from the spawn bench to a dry cleft crossed by a plank bridge, which puts a defender's flank behind the cleft.

## What the ground is made of

**Turf over dirt over rock, finished by angle.** Turf holds to 44 degrees, dirt and coarse dirt with a little podzol to 52, and stone and andesite beyond, so the hill wears a green coat with rock showing where it is steep. The rock under the paint is strata that follow the ground, dirt over stone and andesite beds written out bed by bed.

**The built family is pale stone brick with a faint mossy vein, and the accent is jungle wood.** The ziggurat, pillars and terrace lip are stone brick, polished andesite and andesite. The bridge, the trails and the spawn hall's timbers and cabin are jungle plank and log, a warm tone against the green.

**Two species of tree, both on soil.** Six jungle giants and four dark oaks stand on each side, the giants 14 to 21 blocks apart because their crowns are 12 to 16 blocks wide and cannot overlap. Every site was read off the seats mask after the trails were in.

## How the relief was decided

**Four reliefs were sketched and driven unpainted before one was kept.** The table is what each read back; the ground that shipped is the fourth, the first with the dry cleft added.

| Sketch | What it states | relief | level | largest field | at 40° or more |
|---|---|---|---|---|---|
| a | dell, north hill, three hummocks | 26 | 0.40 | 0.149 | 10.8% |
| b | a ravine from the south coast to z 6, the hill moved | 27 | 0.42 | 0.123 | 13.4% |
| c | two long spurs and a knoll, no cut | 21 | 0.46 | 0.162 | 7.1% |
| d, shipped | a, plus a cleft from the south coast to the dell | 30 | 0.36 | 0.097 | 11.5% |

**The ravine became the whole board and the spurs left it a table.** Sketch b put 13.4% of the ground at 40 degrees or more and made the crossing the one thing to look at, and c came out at 0.46 with `RL6` raised on a spur whose crown was steeper than its skirt. Sketch d keeps a's dell and hill and lets a shorter cleft cross only the south wood, so the flank has something to cross and the middle does not.

## What went wrong

**The cleft's bed patch first added land outside the coast.** It stated a height of 4, the height the cleft floor solves to, and the patch only owns paint where it states the plan's own 12; at 4 it painted 74 cells that were ground it had itself added past the outline. At 12 and drawn inside the coast it owns 171 cells.

**The bridge's posts took the deck's columns and I found it a stage late.** They stood on the deck's own layer, which holds one span a column, so `SK9` declined the deck under all eight posts and a picture from the bridge's end did not show the holes. Posts now stand on a layer of their own and `column` reads planks from y10 to y13 at (−54, −34).

**The grass band was cut too low twice.** At 34 degrees the slopes striped brown, and at 46 with a fourteen-degree dirt band the hill was still a brown mound; 44 with an eight-degree band leaves a green hill with rock showing.

**Half-integer rectangle corners gave a two-wide bridge.** A deck stated from −35.5 to −32.5 took only the blocks whose centres fall inside, and the deck built two blocks wide until it was stated in whole blocks.

## Coordinates

| Feature | Team 0 (red) | Read |
|---|---|---|
| spawn | (−112, 0) on the bench at 21, in a jungle-timber hall | `column` (−112, 0) |
| monument | (−64, 24) on the terrace at 18, obsidian pillar y22–24 | `column` (−64, 24) |
| lagoon dell | floor 8, water at y6–7, x −66…−33, z −15…−1 | `column` (−54, −8) |
| north hill | crown 34 at (−42, 34), 24 from the stone | hill grid, z 28–36 |
| ziggurat | x −95…−77, z 17…35, top y23; stair z 25…28 at y18, y20, y22 | `column` (−86, 26), (−76, 26), (−80, 26) |
| pillars | x −74 at z 17, 22, 30, 35, tops y24, y21, y23, y20 | `column` (−74, 22) |
| cleft | floor 4 at x −44…−38, bed of gravel and andesite | `column` (−41, −30), (−41, −34) |
| cleft bridge | x −56…−32, z −36…−34, deck y10, posts y11–13 | `column` (−44, −34), (−54, −34) |
| dead ground | 9.7%: behind the temple (−72, 36) and the wood's south-west corner | coverage |

Blue's features are the rot_180 images: block `(x, z)` maps to `(−x−1, −z−1)`, and the deck, the ziggurat and the pillars were each read at their image.
