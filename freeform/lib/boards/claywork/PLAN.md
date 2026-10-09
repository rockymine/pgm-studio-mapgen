# Claywork — the layout

**Claywork is a standard capture-the-wool board, grounded, built on pgmvox.** Two teams of sixteen, two wools a
team, mirrored north and south. It is flat ground at four levels joined by broad steps, laid in pale clay and
stone. A player remembers the Clay Court with its well, the arches over the Walks, and the two Kilns in the back
corners.

This is the layout only, for review. Nothing is built yet. The sketch is `renders/00-plan-sketch.png`, the
checker's table is `renders/plan-check.txt`, and both are drawn from `scripts/plan.py`.

## The arrangement

**Every piece stands on the world's floor.** Under each surface lie twelve blocks of ground, and under those,
bedrock down to y 1. The void between pieces runs to the bottom of the world, so a fall between them is a death.
Nothing floats.

**The board is mirrored north and south, and each half is mirrored west and east.** Red holds the north. The two
wools of a team are walked the same, and so are the two teams.

**The levels rise from the front to the back in broad steps, one block up and three deep.** No rise between two
floors anywhere is more than one block.

| Level | Floor | Pieces |
|---|---|---|
| The front | 20 | the Forecourt, the West and East Aprons, build zones between them |
| The Undercroft | 19 | the well, a passage under the Court, a balcony under each Arcade |
| The hub | 23 | the Clay Court, the Arcades, the Walks' long stretch |
| The wools | 26 | the West and East Kilns |
| The spawn | 27 | the Gatehouse and its two Statue Terraces |

**The routes meet at the wall.** An attacker crosses the band onto the Forecourt, or builds across a flank zone
onto an Apron, and climbs the Walk to the Kiln. A defender comes down the Spawn Steps, or drops four off
a Statue Terrace, into the Court and out along an Arcade onto the Walk. Both pass the bedrock wall across the Walk
before it climbs into the Kiln.

**The band stops at the Aprons, and the flanks are built over too.** The band runs from one Apron's inner edge
to the other's, so nothing is built out in front of an Apron and the board's edge is no crossing. Between the
Forecourt and each Apron lies a build zone the front's full depth, so the front line is joined only by building:
less land, and more risk, on the way to a Walk.

**The Undercroft is a second layer under the hub.** A player drops four into the well onto its floor at 19, and
the well is a way down only: nothing climbs out of it but the ladders at the Walks. A
passage three wide runs from the well under the Court and out under each Arcade as a balcony, open on the side
facing the spawn, to a ladder up onto the Walk short of the wall. It is a quiet way from one wool to the other.

## The numbers

**Every row of the check passes.** The full table is on the sketch; these are the ones that decide play.

| Measure | Value | Target |
|---|---|---|
| The band, front to front | 24 | 20 to 30 |
| Spawn to the band | 83 | at least 55 |
| Spawn to its own monuments | 12 | under 15 |
| Band to a Kiln, the attacker's shortest | 75, 7 of it built | at least 59 |
| Spawn to the two Kilns | 97 and 96 | ratio at most 1.25 |
| Walk to Walk, through the Undercroft / the shortest way | 129 / 123 | a way round under the Court |
| The drop into the well | 4 | at most 4 |
| Band cells in front of an Apron | 0 | none |
| Rises between neighbouring floors | 1, 3 and 4 | 1 a step, 3 or more a wall, never 2 |
| Kiln to Kiln | 131 | 46 to 143 |
| The Walk's narrowest, arch legs included | 10 | 10, the corpus's usual funnel |
| A Kiln's faces on the void | 3 | at least 2 |
| Void from a Kiln to the Gatehouse, Arcade and Court | 42, 17, 29 | at least 16 |
| The wall across the Walk | 12 wide, ends on the void | at most 20, no way round |

**A defender reaches the wall line later than an attacker, 84 against 63.** The recorded matches put the ratio at
a median of 1.0 and a mean of 1.75, with the defender farther on 44 percent of objectives, so this is ordinary.
The Statue Terraces brought it from 90 against 58: a defender drops off a terrace's front into the Court.

## The places

- **The Gatehouse** (27): the spawn, 32 by 20, its two monuments at the head of the Spawn Steps.
- **The Statue Terraces** (27): the Gatehouse carried out to the Court either side of the Spawn Steps, 10 by 12,
  a statue on each. Their front stands four over the Court, and a parapet two high runs along their edge over the
  steps.
- **The Spawn Steps** (23 to 27): twelve wide, four broad steps cut down between the terraces into the Court.
- **The Clay Court** (23): the hub, 64 by 29, with **the well** in its middle, a pit 14 by 12 down to 19.
- **The Undercroft** (19): the well's floor, a passage three wide under the Court, and a balcony under each
  Arcade open toward the spawn, ending at a ladder up the Walk's face.
- **The Grand Steps** (20 to 23): two flights at the Forecourt's two ends, each ten wide with three broad steps
  and an arch over it. Two ways up spread the traffic between the front and the Court.
- **The Rostrum** (23): the Court carried out between the flights, 36 by 9, for a statue or a feature, a
  parapet on each side over the steps.
- **The Forecourt** (20): the middle of the front, 56 by 18, on the band.
- **The flank zones**: 24 by 18 of void between the Forecourt and each Apron, built over.
- **The stepping stones**: four in the void in front of each Arcade, two wide and three deep, at 22, 21, 20 and
  19, following the Walk down toward the front. Every gap is two, the most a running jump one block up clears, so
  they are crossed both ways. The last stands two short of the flank zone, a jump from a block placed at its edge:
  mostly an attacker's way back.
- **The West and East Aprons** (20): the front's flanks, 20 by 18, each the foot of a Walk, with no band before
  them.
- **The West and East Arcades** (23): from the Court to the Walks, 28 by 12, an arch across each.
- **The West and East Walks** (20 to 26): twelve wide along the board's edge, two arches across each, the
  bedrock wall where they climb to the Kiln.
- **The West and East Kilns** (26): the wool rooms, 14 by 17, walled and roofed six high, the door eight wide.
  Red's hold yellow and lime; blue's hold orange and light blue.
- **The band**: twenty-four blocks of void between the two front lines, 104 wide, built over.

## The look, decided now

**The surface is a checker of clay, stone and double stone slab.** Each pace is three by three, and each level
has its own mix, so a player reads their height from the floor. The steps are stone with slab nosings.

**Arrows are set into the surface pointing the way forward.** They are laid in stone in the clay, from the
Gatehouse to the Grand Steps, from the Court along each Arcade, and up each Walk to its Kiln.

**Arches span each flight of the Grand Steps, each Arcade and each Walk twice.** They are stone brick, five clear of the floor,
with legs a block wide on the way's edges. The legs are what narrow a Walk from twelve to ten.

**The faces of every piece are layered, so tall bedrock does not show as one slab.** Under the twelve blocks of
ground lie two of bedrock, then a one-block stripe of the team's stained clay set one block in, then bedrock to
the floor. Black wool and obsidian break that bedrock into a pattern on the faces. Block 36 lies at y 0 under the
band and under every piece: building is allowed only over it, up to y 44.

**The team accent is stained clay, red or blue.** It appears in the face stripe, the Gatehouse and the Kilns'
door frames.

## What the build adds that the plan does not show

- The checker, the arrows and the arch tops, which change no floor height.
- The Kilns' interiors: the wool on a pedestal, two chests of gear, light.
- The Gatehouse's walls, its iron, and cover on the Forecourt and the Court (low walls and boxes two high).
- The face patterns under each piece.

**Cover is the one thing that changes play, so its places are fixed before the build.** It goes on the Forecourt
and the Court only, two blocks high, never on a Walk or an Arcade.

## What changed after the first review

**The first layout is kept as `renders/00-plan-sketch-v1.png`.** Three changes came from the review.

- **The band was narrowed to stop at the Aprons, and the front line joined up.** The Parades join the Forecourt to
  each Apron. Players can no longer cross along the board's edge, so they come in toward the middle and the flanks
  can be held.
- **The Grand Steps became two flights with a hole between.** Two ways up spread the traffic between the front and
  the Court.
- **The Gatehouse was carried out to the Court as two Statue Terraces.** The Spawn Steps are now cut down between
  them, with room for a statue on each. A parapet along each edge keeps a terrace from standing two over the
  stair's middle, a ledge that would look climbable.

## What changed after the second review

**The second layout is kept as `renders/00-plan-sketch-v2.png`.** Three more changes came from the review.

- **The Parades became build zones,** the front's full depth, meeting the Forecourt and the Aprons edge to edge.
  There was too much land and not enough risk on the way to a Walk.
- **The Grand Steps moved out to the Forecourt's ends,** and the Rostrum took the middle where the flights were.
- **The well became the way into the Undercroft,** a second layer under the Court and the Arcades: a rotation
  from one wool to the other that is hidden but not sealed, open toward the spawn under each Arcade.

## What changed after the third review

**The third layout is kept as `renders/00-plan-sketch-v3.png`.** The well stays a way down only. Four stepping
stones now cross the void in front of each Arcade, stepping down toward the flank zone, every gap two so a
running jump clears it upward.
