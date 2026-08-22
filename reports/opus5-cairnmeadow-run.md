# Opus 5 — Cairnmeadow: erected shapes used as terrain rather than as monuments

## What I set out to build

The third board, and the one that takes the second board's correction. Hoarstone's monoliths clashed
with the ground they stood in and its terrain was flat; the brief for this one was:

- **two destroyables a team**, on three islands — one a side and one in the middle;
- **terrain, not houses**: one house on the whole board, and it is the spawn's;
- an **open green meadow** with dirt patches and stone, textured deliberately;
- the erected-shape idiom used the other way — **angled into the terrain** rather than standing out
  of it: at most a seven-block cliff, walkable, irregular, in a **plain material**, then **painted
  back over with grass** so the stones merge into the ground and the terrain is pulled up under them;
- one destroyable **on** such a stone, and one **inside** a negative one — a cut, where the stone was
  taken out;
- a small oak wood and a small birch wood, and paths.

`maps/opus5-cairnmeadow`, `specs/opus5-cairnmeadow/`, `review/opus5-cairnmeadow.md`.

## What worked first time

- **`skirt` is the walkability knob, and the rule is one line.** Probed on flat ground before anything
  was authored: at `skirt 0` an erected shape is a sheer face of its whole lift; at about half the
  lift it steps two blocks at a time; at **`skirt ≥ lift` it steps one block at a time all the way
  round**. That single measurement is what the whole board is drawn from — every outcrop but the cut
  is in the third case, and the transects come back +1 +1 +1.
- **`height_mode: sink` with `skirt: 1` is a quarry, exactly.** Sheer faces, a flat floor, and the
  depth stated per vertex so it can be tilted or notched.
- **A notch beats a slope for a way in.** Setting five of a seven-vertex ring to depth 5 and the two
  southernmost to 1 gives a pit that is sheer nearly all the way round with one shallow ramp; a
  linear tilt across the same ring turned the whole south half into a bowl and lost the cut.
- **Grass painted back over stone is free and it works.** Twenty path props with a grass pave, drawn
  as tongues over each crag's shoulders — a path replaces the surface and adds no cell, so a crag can
  be plain rock in the theme and still read as belonging to the meadow. In section the Tor is green
  up its flanks and grey across its crown.
- **A small spawn piece gives a small house.** 10 × 10 → an 8 × 8 shell. The room's building is sized
  by its piece and nothing else, so this was the whole fix.

## What I got wrong

**A push is applied to the solved surface, so it fills a hollow back in.** `meadow-swell`, a
twenty-radius push meant to give the west meadow some swell, lay across the quarry's own hollow and
lifted it by six — so the pit was cut from ground that was six blocks higher than drawn and came out
shallow. Nothing complained. One column transect down the pit showed 8, 8, 9 where 3 was intended.

**A later mark wins a contested cell, and I wrote a knoll over a bench.** `west-brow` — a point mark
at h 19 — was written after `delve-hollow` and overlapped it, so it overrode the bench and left a
**21-block face** into the quarry that no one authored and no gate mentions. Both of these are the
same lesson from opposite directions: the relief document is ordered and layered, and two landforms
that share ground need to be checked in a transect, not in the JSON.

**I put eight crags on an island meant to read as open meadow.** The first cut had the woods placing
five trees between them, and the diagnosis was not the trees — it was that the board had no meadow
left. Cutting two crags gave the woods room and gave the brief its "open" back.

**The pit floor was a stranded place.** Before the notch, `relief/read` reported three walkable
places with the largest at 95% — the missing 5% was the bottom of the cut, which could be dropped
into and not walked out of. The readback says this and the top-down does not.

## What I could not say

**Which of the three walkable places a readback is counting.** `relief/read` gives the count, the
largest share and the ledge count, which is enough to know something is stranded and not enough to
know *what*. I found the pit floor by guessing and checking with a transect. A per-place centroid and
size would have answered it in one call. **Missing from the surface** — the flood already computes
the places.

**A way to make one side of an erected shape steeper than another.** `skirt` is one number for the
whole outline, so an outcrop is uniformly walkable or uniformly a lip; the only asymmetry available
is `anchor_heights`, which tilts the *top* rather than the edge. The notch trick gets there for a
sink because a sink's anchors are its depth, so a shallow corner is a ramp. For a raise there is no
equivalent: a per-vertex skirt would be the field, and it does not exist. **Missing from the design**,
and arguably rightly — one more number per vertex is a lot for one gesture.

**A house whose size is not its piece's size.** `WX1` derives the shell from the piece inset one, so
the only way to a smaller building is a smaller piece — which also shrinks the protection region and
the spawn's own ground. On this board that was what I wanted; a big protected apron with a small
cottage on it is not expressible. **In the design**, and worth knowing before drawing a spawn piece.

**Whether a crag overlaps another crag.** Same gap Hoarstone reported for buildings: an authored
shape is terrain, so nothing checks two of them against each other, and two erected shapes sharing
ground resolve by "the taller add wins" without saying so. I kept them apart by hand.

## Open gameplay questions

1. **Is a goal on a fully walkable outcrop too easy?** The Tor is climbed from every side in
   one-block steps, so the Tor Stone has no approach that costs anything — it is defended by
   sightlines rather than by ground. The brief asked for walkable and I built walkable; whether a
   destroy goal wants at least one face is not something I can settle.
2. **Is the quarry goal reachable enough?** One ramp in, a 4-to-11-block face everywhere else. A
   defender at the rim looks down on everything in the hole. That may be the best fight on the board
   or a killbox.
3. **The middle of the front is void and the two crossings are on the flanks.** No route goes down
   the centre at all. It splits every attack, which I think is the point, and it also means a team
   that holds one flank never has to worry about the other.
4. **49.7% dead by `coverage`.** Recorded, not treated as a verdict — the repository's author has
   said the reading is imperfect and that a board of this kind can carry it.
