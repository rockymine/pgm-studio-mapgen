# Sallowfen — two stones in a fen

**A fen of willows and reed pools, where each team keeps two monuments on peat hummocks north and south of a
dry causeway running out from its spawn.** A stream winds across the fen in front of both hummocks, crossed dry
only on two plank boardwalks. Pools lie in the flank hollows, a hamlet of stilt houses stands on the causeway by
the spawn, and a watch platform on four legs stands near the lip.

Slug `opus55-sallowfen`, map name **Sallowfen**, built on the deployed studio. The author's questions on it are
notes 11–13 (`reports/opus55-notes-run.md`).

## How it is meant to play

**Two goals a team, placed against each other north and south rather than scattered.** The Willow Stone stands
at (−78, −30) and the Reed Stone at (−76, 30), each on a hummock at y17, 60 blocks apart. The defence walks 65
and 67 from its spawn and the attack 219 and 217, ratios of 3.4 and 3.2 against `GO1`'s 3.0–4.0.

**The causeway is the dry way and the fen either side of it is the slow one.** The stream is six wide and two
deep, so it is swum anywhere or crossed on a boardwalk. The flank hollows hold pools that turn a walk into a
wade. The halves meet across a 32-block build zone over void the whole width.

**The watch platform is height at the front.** Its deck is at y18, six over the fen and eight back from the
lip, and it has no ladder.

## What the ground is made of

**Fen grass with podzol and worn earth, over peat beds, over rock.** Swampland tints grass the olive that meets
podzol as one leaf-littered floor, so the podzol sits at one end of the stop list and worn dirt at the other.
The hummocks' tops lean more to podzol; a bank of dirt, coarse dirt and gravel lines the water.

**The built family is spruce timber on stilts, with stone gables and a stone-brick spawn.** Twelve willows and
dark oaks a team stand at the water, on the hummocks' outer sides and along the back coasts, and ground cover
runs over the whole fen with little tall grass in it.

**The relief is low on purpose, with raised carr banks off both coasts.** The fen floor is at 12, the hummocks
at 17, the hollows four down, and the banks lift the coasts to about 22.

## What went wrong

**Every sketch write answered 200 and was dropped while the stilt style carried an `HS10` complaint.** Vertex
inserts, a vertex move and a map-theme write all left the stored sketch at revision 1. Stating the stilt house's
plate as air, as `HS10` asks, made the same writes land.

**The stream was cut nowhere under the boardwalks, for two reasons found one after the other.** The causeway
path's stroke repainted the stream's top course with paving, so it was split at the boardwalk. The sculpt
builder marks every shape `keepClear`, and the water keeps off a kept-clear column, so the decks state
`keepClear: false`.

## Coordinates

| Feature | Team 0 (red) | Read |
|---|---|---|
| spawn | (−132, 0), knoll y16 | — |
| Willow Stone | (−78, −30), hummock y17 | — |
| Reed Stone | (−76, 30), hummock y17 | — |
| causeway boardwalk | x −56…−38, z −3…4, planks y13, water y11–12 under it | `column` (−44, 1) |
| north boardwalk | x −50…−34, z 36…41, planks y13 | `column` (−42, 38) |
| watch platform | legs at (−34, 12) to (−29, 17), deck y18 | — |
| dead ground | 29.8%: the coasts behind the hummocks | coverage |

Blue's features are the rot_180 images: block `(x, z)` maps to `(−x−1, −z−1)`.
