# Hollowstack: the plan

Capture the wool, two teams of sixteen, two wools a team. Two walls of rock riddled like cheese face each other
across a void chasm, and every storey of each wall opens onto it. `scripts/layout.py` holds every number below as
data, and `assets/` holds the segment sheet the passages were designed on.

## 1. The identity

**Two walls of honeycombed rock face each other across a chasm, each a stack of worlds: a wood on top, a mine
under it, a forest in a cavern under that, a dungeon under the forest and fire at the bottom; every storey looks
out over the chasm at its twin, and a wool is kept in the forest and in the dungeon.**

The board is read like a side-scrolling game's cross-section. Standing at any mouth, a player sees the other team's
storeys stacked opposite, lit and open, the way a cut through an ant's nest shows its chambers.

## 2. The layout

Blue holds the east (x > 0); red is blue's image under the half turn, (x, z) -> (-1 - x, -1 - z). The board is 192
long, 56 deep and 108 high. Each wall runs from the chasm's face at x 12 to the back at x 95.

| Storey | Heights | What it is |
|---|---|---|
| **The Tops** | ground at y 94 to 104 | a wood of oak and birch on rolling ground, the keep at the back on a levelled hill at y 100, a broken watch tower at the brink |
| **The Workings** | floor at y 82 | a mine laid from the timber kit: galleries with rails, the keep well passing through, two galleries out to the chasm on timber stages |
| **The Underwood** | floors at y 53 to 61 | a cavern 50 long and 38 deep, its forest on three terraces, a pond under a light well from the Tops, glowstone in its roof and vines down its walls; its whole front is open to the chasm |
| **The Undercroft** | floors at y 34 and 40 | a dungeon laid from the stone kit on two levels: corridors, stairs, a library, a prison, a crypt, the gallery at its front with its arcades open on the chasm, and the vault at its back by the keep well |
| **The Deep** | floors at y 13 to 20 | a cavern with a lava lake held in obsidian, a pool under the Root Well and a grotto of huge mushrooms |
| **The Chasm** | x -12 to 11, all heights | the void between the walls, 24 across, the whole of it the build zone |

## 3. The wools

Each team keeps two wools on its own side and carries the enemy's two home to its keep.

| Wool kept | Where | Its room |
|---|---|---|
| **The Grove Shrine** | a ruined round of pillars on a spur of rock in the Underwood's mouth, y 57 | open to the chasm in front, the Root Well's drop beside it, held from the terraces behind: the front wool, the one fought over across the chasm |
| **The Vault** | the Undercroft's back room, two storeys high, by the foot of the keep well, y 34 | three cells by three, its doors on the corridors; the deep wool, reached across the chasm and through the enemy's whole dungeon |

The monuments stand in the keep's yard at y 100, beside the well house, where a carrier comes up the ladder.

## 4. The ways

**Down your own wall.** The keep well is one ladder from the yard down through the Workings to the Undercroft, with
a door at every storey it passes and the postern at the Underwood's height. The Workings run to the chasm and down a
winding cave into the Underwood's back; the Underwood's gatehouse is a ladder down into the Undercroft; the
Undercroft drops by a third well into the Deep's grotto.

**The fast ways down are falls into water.** The light well drops from the Tops into the Underwood's pond, the
plunge from the keep's hillside into a pool at its back, and the Root Well from the Underwood's mouth into the
Deep's pool.

**Across the chasm.** Every storey opens onto it: the Workings by timber stages, the Underwood by its whole mouth,
the Undercroft by the gallery's two arcades and two balconies, the Deep by a cave mouth. At the brink the stumps of
a broken bridge reach out from both walls and leave eight blocks between them, the shortest crossing on the board.

**Back up with the wool.** A carrier goes back across the chasm and up their own wall: the segment stairs, the
ladder wells and the winding caves are the only ways up, so the defence knows where to wait.

## 5. As built

**The board is read back from the built world after every build.** `scripts/walk.py` writes `renders/walks.txt`:
no block over air, no water against air, and every place a player reaches inside the laid passages has at least
three blocks of air over it (all but eight, on the crypt's tombs, have four).

| Walk | Blocks |
|---|---|
| spawn to the Shrine it keeps, on foot / taking the drops into water | 128 / 79 |
| spawn to the Vault it keeps, on foot / taking the drops into water | 127 / 75 |
| spawn to the enemy's Shrine, bridging the chasm | 158 |
| spawn to the enemy's Vault, bridging the chasm | 231 |
| the Shrine's wool carried home | 118 to 120 |
| the Vault's wool carried home | 210 to 212 |
| the keep well, the yard to the Workings / to the Undercroft | 25 / 53 |
| the postern, the keep well into the Underwood | 20 |
| the gallery on the chasm to the Vault's wool | 67 |

**The passages come from pgmvox's segment kit.** `assets/segments_sheet.py` lays every piece in both kits and walks
them; the Undercroft has 53 passage cells, six rooms, two stairs and three wells, the Workings 31 cells and a room.
The network between the fixed pieces is drawn by `segments.network`, the shortest ways between them, so the rock
between the corridors stays solid.

## Open

- The Shrine is close to even: 128 on foot for its keepers against 158 for its takers. It is the front wool by
  design, but the defence leans on the drops into water to get there first.
- The Vault's carry home is long, 210; a carrier has the whole enemy wall and the chasm to cross.
