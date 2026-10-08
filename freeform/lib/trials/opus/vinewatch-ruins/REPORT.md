# Vinewatch Ruins — team deathmatch

**A white temple ruin in a jungle bowl, fought over in three lanes with a cistern under the middle that joins
them.** The lanes are a causeway over a marsh, a plaza round a low lidded ziggurat, and a sunken court. Each team
spawns in a walled gate-court that nothing in the middle can see into. The board is 96 by 112 blocks, mirrored
north and south, teams of twelve; a kill scores a point and fifty win, or the most kills in ten minutes.

```
cd freeform/lib && python3 -m pgmvox.run trials/opus/vinewatch-ruins --build <scratch>/vinewatch-ruins --skip write
```

The run takes about 15 seconds.

## How it plays

**A deathmatch board is a control board without a point, so it is built to `match-flow.md` §10.** The ground is
built, the middle is entered from decided directions, cover is placed in two sizes, height is kept small, and
nothing in the middle looks into a spawn. Building is off: the board is fought as it was made.

**The gate-court is the spawn, at 44, walled five high, with three ways out.** The south gate leads down three
steps behind a screen eight high, which turns the way out so that no line runs from the plaza into the court. The
west and east gates stand in the court's back corners and open into a corridor behind a baffle wall. So a side
gate is seen only from behind its own baffle. The jungle either side of the court is thicket, planted and not
walked.

**The three lanes run north to south, and the cistern crosses under them from west to east.**

| Lane | What it is | Spawn to the middle, plan (octile) | Built world (moves) |
|---|---|---|---|
| the Causeway | a pale stone walk at 42 over the marsh at 39, quartz pillars along it | 58.4 | 70 |
| the Plaza and the Ziggurat | the plaza at 40 round a ziggurat of three tiers to 46, under a lid at 51 on four pillars | 51.0 | 57 |
| the Sunken Court | a court four under the jungle, walled in pale stone, stairs at its head and through its parapet | 56.9 | 70 |
| the Cistern | a stone-brick tunnel at 34, six wide, with a hall and a pool under the ziggurat, stairwells up into the marsh and the court | 52.4 | 78 |

**Every lane is a choice.** The slowest lane in the plan is 1.14 times the quickest, and both teams' walks are
equal to the decimal. The built world counts four-way moves, which stretches the diagonal plaza walk least and
the cistern's stair-and-corridor walk most (1.37 times the plaza).

**The cistern is the stacked route §10.3 asks for.** It joins the marsh to the court under the plaza, so two
players heading for the same ground are on different storeys until one comes up. Three pairs of stone-brick
pillars stand in its run and the hall under the ziggurat holds a pool, so its 62 blocks are not one firing line.

**Height is a trap, so the centre is six over the plaza and roofed.** The ziggurat's top tier stands at 46 under
a lid of quartz slab and gold at 51. It overlooks the plaza; it does not overlook a spawn.

## The check, plan and built

| Measured | Plan | Built | Target |
|---|---|---|---|
| The spawn court seen from the middle (every walkable cell with \|z\| at most 12) | 0% | 0 of 74 sampled cells, from 559 reachable eyes | 0 |
| The spawn court seen from the ziggurat's top | 0% | — | 0 |
| The ziggurat's top over the plaza | 6 | 6 | at most 6 |
| The cistern's width, its cover columns | 6, 6 | — | 5-6, at least 4 |
| The farthest a floor cell stands from anything that breaks a line | 6.1 | — | at most 9 |
| Playing floor on no way between the spawns within 1.35 of the shortest | 7% | — | at most 20% |
| The cistern walked from the marsh's stairwell: to the hall, to the court's stairwell | — | 49, 71 | reached |
| Rim columns a player reaches (out of bounds) | — | 0 | 0 |

## Renders

| File | What it shows |
|---|---|
| `renders/00-plan-sketch.png` | the plan: the board with the cistern over it, the four lanes' walks, two cuts, the check |
| `renders/05-topdown-annotated.png` | the built top-down with the plan's names |
| `renders/30-iso-board-se.png`, `31-iso-board-nw.png` | the bowl from two corners |
| `renders/32-iso-gate-court-se.png` | red's gate-court, its canopy, the baffles and the screen |
| `renders/33-iso-ziggurat-sw.png` | the ziggurat, its lid and the plaza's cover |
| `renders/34-iso-causeway-and-marsh-se.png`, `35-iso-sunken-court-sw.png` | the west and east lanes |
| `renders/40-xray-cistern.png` | the cistern with the ground above lifted off |
| `renders/10-section-middle-x0.png`, `11-section-lanes-z-10.png`, `12-section-cistern-z0.png` | cuts down the middle, across the lanes, along the cistern |

## Read-back

- **`Objectives.check`:** no problems; both spawns stand.
- **`audit.footing`:** 0 problems.
- **Out of bounds:** no rim column is reached; the rim rises 11 to 17 blocks sheer.
- **Standing places nobody reaches:** 5,244 (the tops of walls, pillars, cover and the lid). Building is off, so
  they stay out of play.
- **The studio's reader:** valid, 2 teams, 2 spawns, 1 kit, 5 apply rules, no issues. Its counts carry no row for
  `<score>`, so it says nothing about the kill scoring.
- **The build:** 467,134 blocks, 13 trees, 6 tile entities (the banners).

## The plan

| Place | What it is | Why a player goes there |
|---|---|---|
| The Gate-court | the spawn at 44, walled, a canopy over its back, three gates | the spawn |
| The Screen and the baffles | walls in front of each gate | they keep the middle's eyes out of the spawn |
| The Plaza | pale floor at 40, ruined plinths three high, a broken wall on its west side with two breaches | the middle lane and the main fight |
| The Ziggurat | three tiers to 46, stairs on the north and south faces, a lid | the middle's height, kept small |
| The Causeway and the Marsh | a raised walk with pillars, a strip of mud and pools | the west lane, and the cistern's west stairwell |
| The Sunken Court | four under the jungle, plinths and pillars | the east lane, and the cistern's east stairwell |
| The Cistern | the tunnel and its hall | the stacked route under the middle |

**The look.** The biome is jungle, and the built family is a pale temple: polished diorite, diorite and quartz in
cells of three, quartz pillars, chiselled quartz on the ziggurat's risers, mossy brick only faintly in the walls.
The ground is jungle grass with worn dirt, the marsh mud and pools, the rim stone with grass on top. Green comes
from jungle and oak trees in the thicket and on the rim, vines on the walls and a few low ferns, and no
two-high grass. The accent is the lid's gold, the cistern's glowstone and the banners.

## Decisions, and why

- **Deathmatch built as a control board.** §10 is the author's law for a board fought for ground, and a
  deathmatch is fought for nothing else.
- **Building off.** A deathmatch on a made board plays as made; building would let a team tower out of its spawn
  over the screen.
- **Mirror north and south.** The other four boards turn by a half or mirror across x; a mirror across z gives
  each lane to the same side for both teams, so a lane is a known place.
- **The side gates in the court's back corners.** It was the only placement the sight check passed with a
  baffle wall of reasonable length.

## What went wrong, and how it was found

- **Every first stair climbed the wrong way or overwrote its own gate.** A flight's first cell is its lowest, and
  the gates had been drawn on the court's last row instead of on its wall line. Printing the plan's heights
  round the gate-court found all four.
- **The cistern ran two blocks under the sunken court.** The plan walk would not stand in it there, because a
  floor over a storey needs three blocks of air. The cistern now ends under the jungle and comes up by
  stairwells cut into the ground storey.
- **The middle saw 54% of the spawn court.** The plan's sight check found it, through the side gates from the
  causeway and over the screen from the ziggurat. Baffles went in, the screen went up to eight, and the side
  gates moved to the back corners.
- **The dead-space measure was wrong first.** "More than six from a lane's walk" called 60% of the floor dead,
  because a walk is a line and the plaza is 42 wide. The measure that matches §10.3 asks whether a reasonable way
  between the spawns passes a cell.
- **The built world's sight check first read 59 of 74.** Its eyes stood on wall, pillar and lid tops that nobody
  reaches with building off; restricted to reached places it reads 0.
- **The spawn's canopy came out black and white.** Slab data 6 is nether brick; the render showed it.

## What the plan missed

- **The lid as a place.** The plan held the lid as a roof for sight and not as a floor someone might stand on; a
  board that allowed building would need it in the plan.
- **The walks in the built world's units.** The plan's lanes are within 1.14 of each other; the built world's
  are within 1.37, past the plan's own target.

## Friction log

### What the library lacked, written locally

- **A storey's stairwell up into the ground.** The cistern's ends are stairs cut into the ground storey by hand;
  the plan raster has no idea of an opening in a floor.
- **A sight check against what a player reaches.** `sight` takes eyes; `walk` finds reached places; the built
  check joins them by hand.
- **Dead space by the routes between spawns.** `plangraph` gives the costs; the "within 1.35 of the shortest"
  share is three lines, and it is the measure `match-flow.md` §10.3 means.
- **A deathmatch's scoring.** `mapxml` has `kill_below`, `time`, `blitz` and the rest, but no `score(kills=...)`;
  it is one `E` call.

### Bugs and surprises, with reproductions

**`plangraph.walkable` drops a storey's cell when the ground over it is within three, which is right, and the
message is silence.** A tunnel two under a floor simply is not walked; nothing reports the cells lost:

```python
from pgmvox.plan import Raster
from pgmvox import plangraph as G
R = Raster((0, 9), (0, 9), ["floor", "tunnel"]); R.H[:] = 36
U = R.storey(1); U.box(0, 4, 9, 5, 34, "tunnel")
print(int(G.walkable(R, {"floor", "tunnel"})[1].sum()))      # 0 of 20
```

**The studio's reader accepts a deathmatch without reading its score.** Its counts list teams, spawns and kits,
and nothing for `<score>`, so a mistake in the scoring would pass.

### Wanted, how hard, what it would take

| What I wanted | How hard it was | What a library or studio feature would need |
|---|---|---|
| A tunnel that comes up through the floor | 12 lines in the plan and gen | `Raster.opening(storey, cells, stairs=...)` cutting the floor over a storey and drawing its stair |
| Sight against reached places | 6 lines | `walk.reached(w, starts)` and `sight.seen_from(w, reached, targets)` |
| Dead space by route | 5 lines | `plangraph.live(edges, a, b, slack)` |
| A deathmatch's score | 1 line | `Doc.score(kills=1, limit=50)` and the reader counting it |
| A warning for a storey with no headroom | found by a walk that said nothing | `walkable(..., report=True)` naming the cells it drops |
