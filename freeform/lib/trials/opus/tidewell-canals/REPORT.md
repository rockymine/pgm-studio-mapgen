# Tidewell Canals — king of the hill

**A canal quarter on a lagoon, with a customs house at each end and three markets fought over between them.** The
Campo in the middle is a square ringed by arcades with a gallery over them, and it pays two points a second. A fish
market under an open loggia on each side pays one. Every way between them crosses a canal by a bridge. The board is
160 by 128 blocks, symmetric by a half turn and by a mirror in z, three hills, teams of sixteen, building off.

```
cd freeform/lib && python3 -m pgmvox.run trials/opus/tidewell-canals --build <scratch>/tidewell-canals --skip write
```

The run takes about 20 seconds.

## Why king of the hill

**It is the mode whose author's law is the most detailed and the least tried here.** `approaches.md` says where
points go (square pads, a centre and two flanks across the spawn line, at two-thirds or more of the way out).
`match-flow.md` §10 says what surrounds them: built ground, cover in two sizes, stacked routes, no dead space,
height a trap, the centre paying double. The studio reads the library's `Hill` as valid, unlike a flag or a score
box. And a hill board exercises what the other four did not: arrivals at a shared target, sight from a pad, and a
walkable upper storey.

## How it plays

**The quarter is three bands between two canals.** Each team's district (the Sestiere) runs from its customs
house to its Grand Canal: three streets east to three bridges, blocks of houses between them as large cover, and
a campiello with a wellhead. Between the two Grand Canals lies the middle band. The Campo is its centre, and two
cross canals (the Rii) cut it off from the fish markets at the north and south edges.

**The hills sit on the centre line, level with the ground round them.** The Campo's pad is 8 by 8 at the centre
of rotation. The flank pads stand under the loggias at z -54 to -47 and 46 to 53, which puts them 0.72 of the
centre-to-spawn distance out, inside the corpus' 0.66 to 0.88. No pad stands over its ground, so none is owned
from above.

**Every hill is the same walk for both teams.** Red's half is drawn mirrored in z and the board turns by a half,
so the board is symmetric both ways, and each flank is as near to red as to blue.

| Walk | Plan (octile) | Built world (moves) |
|---|---|---|
| Spawn to the Campo's pad, red / blue | 70.3 / 70.3 | 76 / 76 |
| Spawn to the north market's pad, red / blue | 92.1 / 93.1 | 106 / 107 |
| Spawn to the south market's pad, red / blue | 93.1 / 92.1 | 107 / 106 |
| Spawn onto the gallery | — | 89 / 89 |
| A swimmer in the Grand Canal: out by the steps, to the Campo's pad | — | 6, 46 |

**The one-block difference between the flanks is the spawn's.** A spawn is one block, and the mirror line in z
lies between blocks -1 and 0, so red stands a block nearer the north market; blue, by the turn, a block nearer
the south.

**Each market is entered four ways, decided.** The fishmongers' fronts wall each market's sides, so a market is
entered by a gate on the line of each team's Grand Canal bridge, and by the two bridges over its Rio from the
Campo. The loggia's back wall stands on the sea wall. So a market is held from its corner, and its four ways in
come from two teams' sides and from the middle.

**The Campo is watched from the gallery.** The gallery runs over the arcade on the Campo's north and south sides
at 45, five over the pad and twenty off it, and its eyes see the whole pad. That is the height a holder has to
watch, small enough to be shot back at, reached by a stair at each end.

**Nothing on a pad sees a spawn.** A column on an Istrian-stone plinth stands in each central street, so the
straight line from the Campo down the street into the customs house's court is broken.

## The check

| Measured | Plan | Built | Target |
|---|---|---|---|
| Points a second: centre, north, south | 2 / 1 / 1 | the map.xml | the centre double |
| A flank from the centre over a spawn from the centre | 0.72 | — | 0.66 to 0.88 |
| The centre's walk over a flank's | 0.76 | — | the centre the nearer |
| Each pad over the ground round it | 0 | 0 | 0 |
| Spawn courts seen from each pad | 0%, 0%, 0% | 0 of 108, each pad | 0 |
| The centre pad seen from the gallery | 100% | 64 of 64 | most |
| Ways into a fish market | 4 | — | 3 to 4 |
| The farthest a floor cell stands from a wall, cover or canal | 9.8 | — | at most 10 |
| Floor on no way from a spawn to a hill within 1.35 of it | 3% | — | at most 20% |
| Lagoon columns a player reaches | — | 0 | 0 |

## Renders

| File | What it shows |
|---|---|
| `renders/00-plan-sketch.png` | the plan: the board with the gallery over it, red's walks to the three hills, two cuts, the check |
| `renders/05-topdown-annotated.png` | the built top-down with the plan's names and hills |
| `renders/30-iso-board-se.png`, `31-iso-board-nw.png` | the quarter from two corners |
| `renders/32-iso-campo-se.png` | the Campo, its pad, its wellheads and the gallery |
| `renders/33-iso-north-market-sw.png` | the north fish market under its loggia, the Rio and its bridges |
| `renders/34-iso-customs-and-sestiere-se.png` | red's customs house, its district, the column and the gondolas |
| `renders/10-section-spawn-to-spawn-z-1.png`, `11-section-flank-to-flank-x-8.png` | cuts spawn to spawn and flank to flank |
| `renders/50-elev-campo-from-the-west.png` | the Campo seen from red's bridge |

## Read-back

- **`Objectives.check`:** no problems; every pad has a floor and both spawns stand.
- **`audit.footing`:** 0 problems.
- **The studio's reader:** valid, 2 teams, 2 spawns, 3 control points, 1 kit, 5 apply rules, no issues.
- **The build:** 842,164 blocks (most of it the lagoon and the made ground under the streets), 10 houses, 10
  tile entities (the banners and the stalls' chests).

## The plan

| Place | What it is | Why a player goes there |
|---|---|---|
| The Customs House | the spawn's court, walled on three sides, a portico east | the spawn |
| The Sestiere | three streets, five blocks of houses, a campiello and a wellhead | the ways to the three bridges |
| The column | a quartz column on a plinth in the central street | breaks the line from the Campo to the spawn |
| The Grand Canal | water at 38, three arched bridges, steps out at three places | the line every route crosses |
| The Campo | brick paving, the centre pad, four wellheads as large cover, small cover | the centre hill |
| The gallery and the arcade | a walk at 45 over pillars on the Campo's north and south sides | the stacked route and the watch over the pad |
| The Rii | the cross canals, two bridges each | the markets' south ways in |
| The Fish Markets | the flank pads under loggias, stalls, the fishmongers' fronts with a gate | the flank hills |

**The look.** The streets are grey: stone brick, polished andesite, andesite and stone in cells of three. The
campi are warm brick bordered in polished diorite as Istrian stone. The houses are one style, a brick ground
storey under pale or ochre plaster with brick-tiled roofs, and the stone buildings are quartz and diorite. Water
is the canals and the lagoon, with gondolas moored; the accent is the pads' carpets, lamps on the quays and the
banners.

## Decisions, and why

- **Three hills, the centre worth two.** Two teams get two or three points, three is the ordinary board, and a
  centre paying double puts a reason to leave a held flank back into the match (`match-flow.md` §10.6).
- **Symmetric both ways.** With the half turn alone, each team has a nearer flank; the corpus' rule is that a point
  is the same walk for everyone, and the mirror within red's half gives that exactly.
- **Canals and bridges as the decided directions.** A canal is a line nobody crosses except at a bridge, so every
  way into a market or the Campo is a choke the author chose. A player in the water climbs out only at the steps.
- **Building off.** A built quarter plays as built; building would let a team bridge the canals anywhere and tower
  onto the loggias.
- **The flanks at 0.72, not higher.** The board's 128 blocks in z leave room for a market band and a sea wall; a
  flank at 0.85 would have put the pad against the wall with no way in from behind.

## What went wrong, and how it was found

- **The street ran out past the sea wall and the customs house's wings stood in the lagoon.** Printing the plan's
  heights showed both; a box was drawn from the board's edge rather than the wall's.
- **The Campo's pad saw 22% of the spawn courts.** The check found it: the central street runs straight from the
  Campo to the customs house's portico. A column went in, and at three wide it still let two lines past
  (11%); at six wide it reads 0.
- **A market had one way in, then six.** The first count merged the market's open sides into one run, and once
  walled, the market's corner row was still open to the quay. Both the plan and the count were fixed.
- **The gallery's link pointed at the wrong cell.** The walk graph steps from the stair's top onto the gallery by
  itself, so the link was dropped.
- **The plaster read as brick.** The orange and rose clays render the same red-brown as the roofs; the render
  showed it, and the houses are pale and ochre now.
- **Two targets were mine and wrong.** "The centre's walk over a flank's, about 1" asked for something the corpus
  arrangement does not do, and "equal" for the flank walks asked for what a one-block spawn beside a mirror line
  cannot give. Both were restated with a reason.

## What the plan missed

- **Lines down straight streets.** The plan placed the streets before it asked what a pad sees along them; a row
  "the longest unbroken line from each pad" would have caught the central street at once.

## Friction log

### What the library lacked, written locally

- **Two symmetries at once.** `Symmetry` is one operation. A board symmetric by a half turn and a mirror is drawn
  through `quad`, which draws each box and its mirror in z and lets the raster add the turn.
- **Pieces on the axis after a turn.** `orient.turn_world` copies red's half onto blue's whole, so anything that
  straddles the axis (the Campo's pad, the loggia's roof) is laid after the turn or laid twice.
- **Ways into a place.** Counting the entries into a market is a labelled boundary, written in the checker.
- **Arched bridges.** The plan's bridge is three heights; the stairs onto each arch are chosen per cell in `gen.py`.

### What fitted with no friction

**The capture-point half of the library worked as designed.** `Hill(points=...)` wrote the 2/1/1 rates the studio
reads, `plangraph.arrivals` with targets both teams share gave the fairness rows directly, `sight.plan_opaque`
with `roofs` held the loggia and the gallery solid, and the canal behaved the same in the plan walk and the built
walk (a swimmer climbs out only at the steps).

### What in the guide was unclear

- **The guide's king-of-the-hill row asks "what a holder sees from the hill and who can see them".** It does not
  say what the targets are; this board used the spawn courts (must be none) and the overlooking gallery (must be
  some, and close enough to be shot back at).

### Wanted, how hard, what it would take

| What I wanted | How hard it was | What a library or studio feature would need |
|---|---|---|
| A board symmetric two ways | 5 lines and a convention | `Symmetry("half", also="mirror_z")`, a group of operations applied in the plan |
| The axis built once | ordering in gen | `turn_world(..., keep=...)` that leaves the axis's own pieces alone, or a `mirror=False` stamp list |
| The longest line from a pad | not measured | `sight.longest_line(R, cells, opaque)` |
| Entries into a region | 12 lines | `plangraph.entries(R, region, walk_kinds)` |

## After the playtest

**A hill needs wool or stained clay under it for PGM to recolour, and the pads had neither.** PGM's default visual-materials filter takes wool, carpet, stained clay, stained glass and its panes, banners and ink sacks, and nothing else. The pads were an Istrian stone border over a quartz and andesite checker, so a hill could be captured and never change colour.

**Each pad is now a stone border, a ring of white stained clay, a ring of white wool and a quartz heart.** The eight-by-eight pad reads back as 28 Istrian stone, 20 white stained clay, 12 white wool and 4 quartz on all three hills. The clay ring is where the capture's progress shows, and the wool ring inside it shows the owner. The pad stays level with the Campo, so the capture region and the walk to each pad are unchanged.

**The map.xml names the ring as the progress display.** The library's hill wrote one pad region as both the progress and the owner display, and PGM takes the progress blocks out of the owner display, so the owner would have shown nothing. `mapxml.py` now defines `campo-progress`, `north-market-progress` and `south-market-progress`, each a union of four one-block-thick cuboids over the clay ring, and points each hill's `progress-display-region` at it. The owner display stays the pad, which leaves the wool ring.

**The studio reads it as valid, and the walks do not move.** The checker reports the map valid with no issues and three control points. Spawn to each pad reads 76, 103 and 104 for red and 76, 104 and 103 for blue, the same as before the change, and the gallery 86.

## After the second playtest

**Houses keep a block of wall either side of the door.** The library's house builder no longer puts a window against a door, and the board was rebuilt with it. A scan of every door block finds no pane or glass beside any. The walks are unchanged but for their timings.
