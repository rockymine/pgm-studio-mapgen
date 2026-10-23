# Hollowstack: the plan

Destroy the monument, two teams of sixteen, two monuments a team. Two walls of rock riddled like cheese face each other
across a void chasm, and every storey of each wall opens onto it. `scripts/layout.py` holds every number below as
data, and `assets/` holds the segment sheet the passages were designed on.

## 1. The identity

**Two walls of honeycombed rock face each other across a chasm, each a stack of worlds: a wood on top, a mine
under it, a forest in a cavern under that, a dungeon under the forest and fire at the bottom; every storey looks
out over the chasm at its twin, and a monument stands in the forest and in the dungeon.**

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

## 3. The monuments

**Each team defends two obsidian monuments on its own side.** The board was built for capture the wool and the
author's review turned it: a wool must always be defensible, and the Shrine's, at the very edge of the chasm, was
not. A monument is broken where it stands, so the map asks to be held rather than raided.

| Monument | Where | What holds it |
|---|---|---|
| **The Shrine** | floating over the altar of a ruined round of pillars on a spur in the Underwood's mouth, y 57 | the terraces behind it; the front monument, fought over across the chasm |
| **The Vault** | floating over the dais at the back of the Undercroft, two storeys high, by the foot of the keep well, y 34 | its doors on the corridors; the deep monument, reached through the enemy's dungeon |

**Only what a player builds may be broken, and the monuments.** The map writes `Build(break_only=("wood", "glass",
"ladder", "obsidian"))` and disables the crafting table, so the rock holds: no route to a monument goes round its
doors, and no fence or fence gate is crafted for the late game's sky (`analysis/late-game/README.md`).

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

**The ways in are few.** The segment stairs, the ladder wells and the winding caves are the only ways between the
storeys, and with the rock unbreakable they stay the only ways, so the defence knows where to wait.

## 5. As built

**The board is read back from the built world after every build.** `scripts/walk.py` writes `renders/walks.txt`:
no block over air, no water against air, and every place a player reaches inside the laid passages has at least
three blocks of air over it (all but eight, on the crypt's tombs, have four).

| Walk | Blocks |
|---|---|
| spawn to its own Shrine monument, on foot / taking the drops into water | 128 / 79 |
| spawn to its own Vault monument, on foot / taking the drops into water | 127 / 75 |
| spawn to the enemy's Shrine monument, bridging the chasm | 158 |
| spawn to the enemy's Vault monument, bridging the chasm | 231 |
| the keep well, the yard to the Workings / to the Undercroft | 25 / 53 |
| the postern, the keep well into the Underwood | 20 |
| the gallery on the chasm to the Vault's monument | 67 |

**In a long match's phases the Vault's doors hold.** `scripts/late.py` walks red's spawn to the Vault with its
doors walled: under the usual rules a route dug round them is 176 blocks; under this board's rules there is none.

**The passages come from pgmvox's segment kit.** `assets/segments_sheet.py` lays every piece in both kits and walks
them; the Undercroft has 53 passage cells, six rooms, two stairs and three wells, the Workings 31 cells and a room.
The network between the fixed pieces is drawn by `segments.network`, the shortest ways between them, so the rock
between the corridors stays solid.

## Open

- The Shrine is close to even: 128 on foot for its keepers against 158 for its takers. It is the front monument by
  design, but the defence leans on the drops into water to get there first.
- The board is a fun map, not one to play many times; a board composed from `plan.approach` under one roof is the
  serious form of it.
