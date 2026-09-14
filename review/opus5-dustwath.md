# Dustwath — the crossing is the map

> A destroy-the-monument board on a bleached dust-flat split by the bed of a river that has gone.
> Each team's monument stands in the open on a low sand bench a short walk forward of its camp, and
> the wath that named the place is now a gap that has to be built across.

**In one sentence:** the palest board of the warm set, where the only decision an attacker makes is
where to cross a 24-block void — at the causeway head somebody already built, or fifty blocks out on
a flank where nobody is watching.

88 × 208 blocks, `rot_180`, five plan pieces, maxPlayers 12, ground y16..y26, observer y52.

## Rebuilt rather than re-authored

The world under `maps/opus5-dustwath/` was lost to a re-export that wrote over a region directory it
never cleared (`B102`). The spec — plan, layout, intent, finish, provenance — survived intact, so the
rebuild is a re-drive of the committed documents into a fresh empty directory and nothing else. One
thing did move: the stored intent had `style: "cube-3"` on the destroyable where the plan says
`pillar-3`, so the re-drive corrected a stale document rather than the board.

## The board is four grounds and a gap

`head` (21) · `apron` (20) · `bench` (23) · `flats` (19), and between the two teams' `flats` a
**zone** rather than a piece: the wath is void, 48 blocks of it, spanned by a brick causeway head
reaching in from each bank so the crossing is 23 blocks at the centre and about 50 at the flanks.

The relief is seven marks — four `area` pans, a hollow, and two braided `line` scours carrying a
one-block `tread` so the band either side of each lofts back to the flat instead of walling itself —
plus three pushes for the back dunes and one swell on the apron. `symErr=0`, range 10 blocks over
5 930 cells.

## What the reads say

| fault | the read | what it says |
|---|---|---|
| objective hidden | `column?at=-14,-51` | ground 22, monument obsidian **y27–29**, nothing over it but its own sky marker at y54–56. Open |
| spawn faces away | intent yaw 0 vs bearing to (-14,-51) | 18.8° off. Within the 90° bar |
| spawn faces a wall | `04-routes.txt`, first 17 blocks out of the door | y21 flat, worst step 0 |
| stairs that end nowhere | `column?at=0,-14` | the causeway head is brick at y14–15 on smooth sandstone — it is there, and it is where it was drawn |
| flat, one theme, empty | `coverage` · `incline` | 18.7% dead, largest patch 441 cells **1 block** from used ground; angles 43.6 / 37.9 / 13.7 / 3.2 / 1.6 % — no spike |
| straight frontline | the wath's edge | the `flats-pan` mark ring wanders, and `apron-21`/`apron-20` are bent coasts |
| stark contrast, no separation | `05-themes.txt` | dust 91.1%, scour 6.3%, works 2.6%; borders dust·scour 294 cells, dust·works 104. Every scour patch lies in a braid's own hollow and every works cell is the causeway |

`03-slopes.txt`: **12 246 walked, 100 scrambled, 146 barrier; 4 faces, largest 39** at x 6..11
z -26..-17 — the causeway's revetments, which is where a face is supposed to be.

## The one number that looks like a fault and is not

`04-routes.txt` reports `spawn-red -> destroyable-1-1: 54 placed, 1 drop, worst drop 37`. That is the
route walker crossing the wath: 54 blocks it would have to place, and a 37-block fall into void if it
does not. On a board whose stated premise is a gap that has to be built across, that is the design
being measured rather than a defect — the build zone spans the whole width and the causeway heads cut
the shortest crossing to 23 blocks.

## Limits

- The monument's sky marker is a five-block team-coloured cross at y54–56, written by the export path
  and not by this spec. It is in the world and not in `map.xml`.
- Nothing here was re-authored, so the board's own faults — if the human oracle finds any in how it
  plays — are the previous run's and are recorded rather than corrected.
