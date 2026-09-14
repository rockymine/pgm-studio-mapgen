# Dustwath — the crossing is the map

> A destroy-the-monument board on a bleached dust-flat split by the bed of a river that has gone.
> Each team's monument stands in the open on a low sand bench a short walk forward of its camp, and
> the wath that named the place is now a gap that has to be built across.

**In one sentence:** the palest board of the warm set, where the only decision an attacker makes is
where to cross a 24-block void — at the causeway head somebody already built, or fifty blocks out on
a flank where nobody is watching.

88 × 208 blocks, `rot_180`, five plan pieces, maxPlayers 12, ground y16..y26, observer y52.

## Rebuilt, then revised on the author's reading

The world was lost to a re-export that wrote over a region directory it never cleared (`B102`); the
spec survived, so the first pass was a re-drive of the committed documents into a fresh directory. Six
things changed after the author read it, and each is below where it belongs.

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
| objective hidden | `column?at=-14,-51` | ground 22, end stone at y27 and y29 over bedrock at y28, nothing above it but its own sky marker at y54–56. Open |
| spawn faces away | intent yaw 0 vs bearing to (-14,-51) | 18.8° off. Within the 90° bar |
| spawn faces a wall | `04-routes.txt`, first 17 blocks out of the door | y21 flat, worst step 0 |
| stairs that end nowhere | `column?at=0,-14` | the causeway head is brick at y14–15 on smooth sandstone — it is there, and it is where it was drawn |
| flat, one theme, empty | `coverage` · `05-themes.txt` | 18.7% dead, largest patch 441 cells **1 block** from used ground; four themes — dust 80.3%, sward **10.9%**, scour 6.2%, works 2.6% |
| straight frontline | the wath's edge | the `flats-pan` mark ring wanders, and `apron-21`/`apron-20` are bent coasts |
| straight **build-zone** edge | the `build-area` union in `map.xml` | six rectangles stepping from z ±28 at the flanks to z ±36 over the middle — no longer one ruled line across all 87 columns |
| stark contrast, no separation | `05-themes.txt` | dust 91.1%, scour 6.3%, works 2.6%; borders dust·scour 294 cells, dust·works 104. Every scour patch lies in a braid's own hollow and every works cell is the causeway |

`03-slopes.txt`: **12 072 walked, 307 scrambled, 158 barrier; 8 faces, largest 39** at x 6..11
z -26..-17 — the causeway's revetments, which is where a face is supposed to be.

## The one number that looks like a fault and is not

`04-routes.txt` reports `spawn-red -> destroyable-1-1: 54 placed, 1 drop, worst drop 37`. That is the
route walker crossing the wath: 54 blocks it would have to place, and a 37-block fall into void if it
does not. On a board whose stated premise is a gap that has to be built across, that is the design
being measured rather than a defect — the build zone spans the whole width and the causeway heads cut
the shortest crossing to 23 blocks.

## The goal is a cube, and the cube decides the material

`pillar-3` is three blocks of obsidian on a goal that stands forty blocks out of its own camp door
(`GO1 3.09`, eleven blocks of lateral offset). It is **`cube-3`** now — twenty-seven blocks, which is
what gives a defender time to arrive.

The material then follows from the count rather than from the palette. `DC3`:

> *cube-3 is 27 blocks and obsidian is worth at most 3 of them — built in ender stone*

So the goal is **ender stone**, one of the four the stamper builds (obsidian · emerald block · gold
block · ender stone). Twenty-seven blocks of obsidian is a grind rather than a raid, and the studio
names the substitute itself; leaving `materials: "obsidian"` in the plan would have written obsidian
into `map.xml` while the world came out ender stone, which is `OB3` — a goal at zero health.

`render/section?axis=x&at=-51` draws it: a 3 × 3 × 3 of end stone at y27–29 with one bedrock at its
centre — **26 breakable blocks** — floating five above ground at y22. `DC3` is silent on the re-drive.

## The path, the trees and the grass

**The track was dirt on sand.** Three strokes paving `dirt · coarse dirt · spruce planks` across a
bleached board is a dark band with nothing to say where it changes. They pave **sand, granite and
polished granite** now: the sand breaks the run up, the two granites are a lighter hue that sits with it.

**Two of the copied trees were conifers.** `spar-1` and `spar-2` are acacia log under **birch leaves**
(`162:12` under `18:14`) at fourteen blocks — a pine silhouette on a desert. `thorn-1/2/3` are acacia
under acacia (`161:12`) at eight or nine. The library names rows and not species, so the leaf id is what
has to be read; both spars are dropped and their five placements are thorns.

**It was all sand.** Nine `sward` patches now — grass over two dirt over sandstone, laid as seven-point
rings with the radius wobbled per point, six of them under trees standing on open flat. The cell carries
the flat's own sand beside the grass so the patch feathers rather than ending on a line, and Savanna puts
grass at #bfb755, which is the olive of dry grass rather than a lawn. `05-themes.txt`: sward **10.9%**,
`dust | sward` 632 cells of border.

## Limits

- The monument's sky marker is a five-block team-coloured cross at y54–56, written by the export path
  and not by this spec. It is in the world and not in `map.xml`.
- Nothing here was re-authored, so the board's own faults — if the human oracle finds any in how it
  plays — are the previous run's and are recorded rather than corrected.
