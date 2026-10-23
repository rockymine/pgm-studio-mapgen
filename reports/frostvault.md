# Frostvault: a composed board read as a bunker

**The author judged the transfer a miss, and the lessons are in §6.** The board stands as the record of the attempt.

**Frostvault is the bunker concept carried onto a layout the studio's generator composed: 24 players a team,
mirrored, seed 11.** It is the second half of the author's request: learn the concept on the quarter they sent
(`reports/coldstore.md`), then transfer it to a generator layout. The board is in `freeform/lib/boards/frostvault`,
its world in `maps/ctw/frostvault`. No studio was driven and nothing was written to the deployed studio.

## 1. How a composed board reaches pgmvox

**The generator runs offline.** `freeform/lib/pgmvox/data/compose_board.cs` calls the studio's composer and its board
deriver directly, as `read_mapxml.cs` calls its parser, and writes the plan with the fanned board in cells: every
standing cell and its piece, the build cells and what they link, the islands and their roles, the enclosed voids and
their classes, and every wool room. With a range of seeds it prints one line a board instead.

## 2. The island question

**A generated board has one island a team; the concept has no floor that is not an island.** The author named this
the question to answer. The generator's land is joined from the spawn to every wool, and its void is the crossing
and a few holes; the concept's quarter is two islands among three pillars, every way off one a bridge of ten to twelve
blocks.

**The answer taken is the generator's own isolation cut, applied where the boxes meet.** A wool's approach and the
frontline are each cut from the rest of their team's land by two cells of void, ten blocks, unless that leaves the
box under twelve cells. In front of each wool room the land is cut back the same two cells, so every seal faces
void as the concept's does. The hub stays one island; cutting it too is the `cut` parameter.

**The other exchanges follow the concept's signs.** Land is islands, build regions are void, every enclosed void
is a pillar from the floor to the roof, the world outside is rock with a moat along every shore, and each defence
wall the generator seated is a seam of rock to the roof.

## 3. What was measured

| Reading | Value |
|---|---|
| islands, each team | 147 (the hub), 54, 49, 28 cells |
| pillars | 104 cells, from the hub's two holes and the frontline's notches |
| spawn to its own monuments, on foot | 11, 10 |
| spawn to its own seals / the enemy's, bridging | 121 and 136 / 226 and 331 |
| seals blown: to the enemy's wools and home | 244 and 234, 349 and 336 |
| the phases, seal standing / blown | not reached / the same in bridged, sky and dug; the seal holds in all three |

The studio reads the map.xml as valid: four wools, four seals, two spawns.

## 4. pgmvox

| Added | What it is |
|---|---|
| `pgmvox/data/compose_board.cs` | a board composed by the studio's generator, and what its deriver reads off it, as JSON |
| `plan.bunker` | `load` that JSON; `draw` it as a bunker plan of rock, island, void and pillar, cut into islands |
| `built.bunker` | `lay` a bunker plan in blocks, rooms sealed and spawns cut into the rock; `dress` it |

Each has a test and a section in `freeform/lib/README.md`. `built.chambers`, the chain of chambers the author ruled
out, is kept for the approach study and marked so.

## 5. Open

- The board is large, as the generator draws 24 a team. The far wool is 331 blocks of bridging from the enemy.
- Whether the hub should be cut into islands too is the author's call; the parameter is there.

## 6. The author's verdict, and what it teaches

**A defence wall to the roof is not wanted.** Under a roof a §5.14 wall is raised to the ceiling, and a wall from
the floor to the roof across an approach is ugly and does nothing the void cannot.

**A pillar never touches an island.** In the concept every pillar stands alone in the void, a gap all round it.
Turning a hole inside the land into a pillar puts the pillar on the land, which is the opposite of the concept: the
pillar there replaced a void and took away the gap the board lives from.

**The generator's layout is the wrong ground for the concept.** It is built of land joined into a mass with holes in
it; the concept is built of void with islands and pillars standing in it. A board in the concept wants a layout of
its own, drawn from the void outward, and it may be as small as one wool a team.

**A wool room need not be sealed.** The seal is Ender Blast's, one way to do it; a plain wool room at the end of an
approach, tied to nothing else, is as good. And beside a spawn there is a place its own team may not build in.
