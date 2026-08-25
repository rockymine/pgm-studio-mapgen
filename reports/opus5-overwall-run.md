# Opus 5 — Overwall: a wall is a second slab, and the ground under it is one flat statement

## What I set out to build

A third brief from the same person outside this repository, and the first that is a *structure*
rather than a landscape: **a labyrinth of pillars with walls in between, every passageway twelve
blocks wide**, one destroyable inside one of its areas and a wool room in another, relief on the
floor players walk **and** relief on the tops of the walls, trees inside it, and most of the
boulders, trees and a couple of houses — houses on stilts — up on the walls **out of the player's
reach**. A river inside the labyrinth. Terrain smooth, not many hills but some elevation. A bridge of
sorts over the walls on a third layer. Walls of an ordinary stone with a pattern in it, and — the
correction on the last board of this kind — not too many colours.

What I built: `maps/opus5-overwall`, documents in `specs/opus5-overwall/`, the account in
`review/opus5-overwall.md`. 184 × 264, three slabs, two islands, 40 open cells all reachable,
55 props, zero declines, export gate open, `GO1` 3.52.

## The finding this run is for

**A wall is not a shape on a floor. It is a second slab, founded on ground the floor was told to hold
flat.**

The naive build — wall shapes on the same layer as the floor — cannot work: a layer holds one span
per column and the taller add takes the shorter's ground outright (`SK9`), and the one relief solved
over that island would smooth the walls and the corridors into a single surface. The next attempt —
a `walls` layer starting below the floor's lowest point so nothing floats — builds correctly and
reports `SK10` over every wall footprint on the board, because the two slabs are then driven nine
courses into each other.

The answer is one shape drawn twice. The labyrinth's footprint goes on the **ground** layer as
`relief_scope: "hold"` shapes with a stated top of 12, and on the **walls** layer as ordinary adds
with `base_y` 12. A held shape becomes an `AreaMark` at its stated top and is appended **after** every
other mark, so it wins its cells outright: the floor is exactly y12 under every wall and rolls freely
in the corridors between them. The upper slab then starts exactly where the lower one ends, the two
share one course, and that is the seam `SK10` is written to allow.

The board reports **no `SK10` anywhere**, and the same trick seats the bridges: four `area` marks on
the *walls* island hold the four pillar tops they land on flat at 26 in that layer's frame, and the
`span` layer's `base_y` is 12 + 26.

Two facts make it possible and neither is written down anywhere:

**Relief is keyed by island id across the whole stack.** `SketchRasterizer.ReliefFields` walks every
layer and looks each of its islands up in the one `relief` dictionary, then adds that layer's
`base_y` to the field it solved. So a stacked board can give every storey its own landscape, and a
layer's marks are stated in **its own frame** rather than the board's. `drive.py`'s `"*"` only ever
meant the islands the *compile* emitted, so it now keeps any key stated beside it instead of
replacing the dictionary.

**A prop with no `layer` seats on `SurfaceTop`.** `Decorator.GroundFor` takes the top surface across
the stack unless the prop names a storey, so a tree at a pillar's centre lands on the wall top and a
tree in a corridor lands on the floor, from the same list, with no field to set. Thirty-two trees,
fourteen boulders and four houses were placed by picking grid positions off the maze picture and
letting the seater work out which world they were in.

## What I could not say

**Nothing about the geometry, and one thing about the plan.**

The plan tier's **frontline is the set of pieces a build zone touches** — `FannedGraph.Build` sets
`Frontline` to exactly that, and `SP1` asks whether a wool is reachable from a frontline node without
crossing a spawn. A plan with `zones: []` therefore has no frontline at all and refuses *every* wool
on it with "only reachable through a spawn piece", however open the board is. Nothing in the message
says the word *zone*. The canonical two-wool seed carries a `mid-band` for this reason, and so does
this board — which is the right zone to have anyway, since the seam gallery is where the two halves
meet.

## What I got wrong

**I nested the wool room inside a piece.** A `wool-room` rectangle drawn inside a larger `piece`
shares no edge with it, and the plan tier answered `WX6 — wool room is unreachable: no land seam and
no abutting build zone to enter by`. Pieces tile; a room is one of the tiles. The maze floor is four
rectangles that surround the room rather than one that contains it.

**I put the goal's court one row too deep.** At (44, 55) `GO1` read 2.42 against a band of 3.0–4.0:
a maze lengthens the attacker's walk and the defender's about equally, so what actually sets the
ratio is how far into its own half the objective sits. One row north — (44, 77) — reads 3.52, and the
only edit was three characters in the maze picture.

**I wrote a route down the river.** The east loop's shortest way through the maze is the one corridor
with no cross-walls, which is the corridor the river runs down; a stroke repaints the surface it
crosses, and the surface there is water. The walk now takes an `avoid` set and the river's whole
column is in it. The same column is out of the running for trees, which is what `DR-CLAIM tree
'in-16' … claimed by the channel` had already said.

**I planted the seam row on both sides.** That row is its own mirror image, so a tree at (−33, 0) and
the image of a tree at (33, 0) land a block apart and one of them is declined. Only the east half of
the seam row is planted now.

**I asked for obsidian and got told.** `DC3`: a `cube-3` is 27 blocks and obsidian is worth at most
three of them, so the studio built ender stone and said so. The document now says ender stone.

## What worked first time

- **The picture as the source of geometry.** Ten lines of `#` and `.` produce the 48 wall rectangles,
  the 49 ground shapes, the two courts, the three routes and every prop position; a flood over the
  same grid refuses to write a document that has sealed a court off, and a BFS over it produces
  routes that cannot cross a wall. Nothing on this board is a coordinate typed by hand, which on the
  last two boards was where every decline came from.
- **Twelve everywhere.** 22 pitch − 10 thickness, and the gap between any two solids is 12 by
  construction: between two pillars, between two walls, and between a pillar and a wall.
- **The river across the seam.** Authored from z 92 down the corridor and west to the origin, it
  meets its own image there and the two make one water — the same trick the coast used on `tarnfell`,
  applied to a line instead of a ring.
- **The house on stilts.** Two storeys, the lower one's wall a five-course band of **air** with the
  beam course kept: what is left standing is four spruce posts, the deck they carry and the ladder
  climbing through open air, which is what a stilt house is. The section render shows it exactly.

## Open gameplay questions

**Should the bridges be reachable?** They are not, and that is a decision: a stair up a pillar is a
way onto the whole wall-top world, and the wood, the rock and the houses up there were asked to be
out of reach. But a bridge nobody crosses is scenery, and a labyrinth with two high crossings that
*could* be taken would be a different and possibly better map. Twelve `SK11` complaints are the
studio noticing exactly this and asking the same question.

**Is 12 wide too wide to be a labyrinth?** The brief said so itself — "you can't really make a
full-on labyrinth with that" — and the board is a colonnade of courts rather than a warren. Forty
cells, three routes, and 40.5 % of the ground off every one of them: the dead share *is* the maze,
and cutting it would mean fewer alternatives, not less map.

**Should the wall tops be walled?** Nothing stops a player pillaring up onto one, only the 15-block
minimum rise. If the wall-top world is meant to be strictly out of play, that is a build-height or a
region question rather than a geometry one, and it is the author's call.
