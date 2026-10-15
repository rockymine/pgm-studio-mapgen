# The experiment: one brief, two pipelines

Two map descriptions, each built twice, once through pgm-studio's HTTP API and once with pgmvox. Every build is
by Sonnet 5.5, from the same brief, the same reading list and the same playtest lessons, so what differs between
the two boards of a pair is the tool.

| Brief | Studio board | pgmvox board |
|---|---|---|
| Slatefold, capture the wool | `exp-slatefold-studio` (`maps/`, `specs/`, `reports/`) | `freeform/lib/boards/exp-slatefold-pgmvox/` |
| Abbeymoor, destroy the monument | `exp-abbeymoor-studio` (`maps/`, `specs/`, `reports/`) | `freeform/lib/boards/exp-abbeymoor-pgmvox/` |

## Brief 1: Slatefold, capture the wool

**A capture-the-wool board for two teams of twelve: a slate-quarrying hamlet on two terraced hillsides that face
each other across the void.** The middle is crossed by building. Each team has two wools to defend.

- **Each side** is one hillside in terraces. The spawn stands on the upper terrace. One wool room is a kiln house
  down by the quarry floor; the other is a winding house or watchtower on the high bench, reached by its own path.
- **The places** are the builder's to decide, at least five a side, each with a reason a player goes there: the
  quarry pit, spoil heaps, a cart track, kilns, cottages and whatever else a slate hamlet has.
- **The look**: grey slate and stone, timber, red brick for the kilns; grass and moss on the benches.
- **Size**: about 150 to 220 blocks along the axis between the spawns.

## Brief 2: Abbeymoor, destroy the monument

**A destroy-the-monument board for two teams of sixteen, two monuments a team: a high moor where each team holds
the hill of a ruined abbey, with an orchard village below it, and a peat bog with standing stones between the
two sides.**

- **The two sides are joined by land** across the bog; there is no void between them.
- **Each team's monuments**: one at the abbey and one in or by the village. Both are visible from the ground an
  attacker approaches over.
- **Under each abbey is a crypt**, and a passage from it comes up near one of that team's monuments, so a monument
  can be reached from below as well as over the surface.
- **The places** are the builder's to decide, at least six a side, each with a reason.
- **The look**: moorland heather and grass, grey stone ruins, an orchard's greens, the bog dark and wet.
- **Size**: about 200 to 260 blocks along the axis between the spawns.

## The playtest lessons, given to both builders

The author played the boards built so far and found the same faults recur. They apply to both pipelines equally.

1. **An objective is found without a map.** It stands in the open, or is plainly signposted, and defenders can
   stand round it. It is never only underground, and never only at the top of a tower. A monument or core floats
   a few blocks over the ground by design.
2. **An objective is made of what the mode needs.** A monument breaks with the kit's tools (obsidian needs a
   diamond pickaxe). A capture point carries wool or clay that can change colour.
3. **A wool room holds the standard wool-runner loot.** In the studio's wool room that is four inner corners with
   two chests each: one with planks, Speed I potions and golden apples, the other with diamond leggings, a Power I
   and Infinity bow and planks. A defence wall's chests sit in its front face, visible from the approach.
4. **Vegetation leaves the floor visible and fightable.** No dense trees on lanes, on small islands or in narrow
   corridors a player navigates.
5. **Every stair is attached and walkable.** Its sides meet land or carry a rail; a stair approach is at most four
   blocks tall; a diagonal ramp is slabs and full blocks rather than turned stairs; two stairways never collide;
   each stair has room to step onto it.
6. **A spawn's exit is open.** Nothing must be walked round on every spawn, and a team can always leave its spawn.
7. **A floating platform cannot be mined away.** Bedrock lies under its last layer, and a platform is thick.
8. **Ladders stand only where players need them, and never in water.** 1.8 does not waterlog.
9. **Every join is open.** A shaft or well reaches the tunnel it is meant to meet.
10. **Things are at a player's scale.** A feature is neither a speck nor a field; outer walls are no thicker than
    their job.
11. **Ground varies in patches, not only in noise,** and bare stone undersides and edges carry detail.
12. **A build zone shows where to build.** A player can see where the bridge goes.

## The rules of the experiment

- **Same reading for both:** `ORDER-OF-WORK.md`, `WHAT-A-BOARD-IS-MADE-OF.md`,
  `pgm-studio/docs/gameplay/approaches.md`, and `pgm-studio/docs/gameplay/match-flow.md` §4, §6 and §10. Then the
  pipeline's own guide: `AUTHORING-BRIEF.md` and the `pgm-board` skill for the studio; `freeform/lib/AGENT-GUIDE.md`
  and `freeform/lib/README.md` for pgmvox.
- **No author review is available.** Each builder reviews its own plan or sketch once against the brief and the
  lessons before building, and writes that review down.
- **The studio is a local one**, at `http://localhost:7894/api`; pgmstudio.de is not touched.
- **Wall-clock is recorded per phase**, from `date` at each phase's start and end.
- **Each report ends with the same three sections:** the times, what the brief asked for that the tool could not
  express (and what was done instead), and the lessons above one by one, met or not.
