# Sixes and Sevens — report

**A Destroy the Monument board for two teams of twenty, built with pgmvox in the author's Bunker style.** The
board is `freeform/lib/boards/sixes-and-sevens` and its world is `maps/dtcm/sixes_and_sevens`. `PLAN.md` is the
plan, and `renders/00-plan-sketch.png` is the sketch the author reviewed before the build.

    cd freeform/lib
    MINECRAFT_JAR=/path/to/1.8.9.jar python3 -m pgmvox.run boards/sixes-and-sevens --build <build-dir>

## What it is built from

**The grammar the bunker is spoken in became library code for this board.** `pgmvox.built.segments` holds the
segment grammar: peels, fades, rows, walls with the corner rule, openings, the crown, staggered panels, floors and
lofts. `pgmvox.grammar.bunker` holds the author's style. Both came out of `studies/bunker-walls`, which now builds
from them; this board is their second user.

**The ground is the winter study's snowfield, written as one pattern with its strength as a field.** `land.snowfield`
takes the outcrops' height and the drifts' strength as arrays. The field between the bunkers runs it calm, and calmer
still near the paths, the front and the Spine. The mountains over the bunkers rise gently over about 60 blocks
measured in from the front, and carry it in the study's own blocks: wool rock, packed ice and a snow cap.

**The bunker is walled by one call over every room.** The wall cells are every column within two of a room, and
each is as tall as the room it faces. Tunnels pass through 2-block walls at openings, so a room's segments stand
either side of a mouth and over it.

## The reads

**Every walk the goal rules measure is in its band, on the plan and in the built world.** Built, on foot and
placing nothing: Reactor 53 from its spawn, enemy over own 3.09; Pump 49, enemy over own 3.51. Blue's numbers are
the same. The objectives read back clean.

**The textured renders are in `renders/`.**

- `01` is the whole board.
- `02` and `03` are Red's front and its door.
- `04` is the yard.
- `05` is the field.
- `06` is the mountain over Red's bunker.
- `07` is the seam.
- `08` is the north spur's lofted wall.
- `09` to `11` are the tall hall, the spawn hall and the dark room, cut open.
- `12` is the shelf and its wall.

## Open decisions

- **The roof.** Every room has a cobblestone ceiling with polished-andesite beams on the segments' six and a
  glowstone in each bay. It stands in for a roof design the author has not decided yet.
- **The gallery from the ground.** It is reached only by the spawn hall's stair. A second switchback inside the
  tall hall would let attackers take it.
- **The Reactor sits close to the line between the spawns.** The front's geometry pins it there.
- **A blast wall's falling top is steps** a player can climb onto.
