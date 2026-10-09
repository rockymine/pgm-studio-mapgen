# Five trial boards on pgmvox — summary

**Five boards were planned, checked, sketched, built, read back and written up on pgmvox 0.10.0, one for each mode
asked.** Each folder holds the port layout (`scripts/plan.py`, `plan_check.py`, `sketch.py`, `gen.py`,
`mapxml.py`, `walk.py`, `renders.py`), its renders and a `REPORT.md` with its friction log. `common.py` holds what
the boards shared and the library lacked. The studio's own reader (`data/read_mapxml.cs`) reads every map.xml as
valid with no issues.

```
cd freeform/lib && python3 -m pgmvox.run trials/opus/<slug> --build <scratch>/<slug> --skip write
```

## The boards

| Mode | Slug | Size | Symmetry | Theme | Walk numbers, plan (octile) / built (moves) | Time |
|---|---|---|---|---|---|---|
| Destroy the core | `cinder-reach` | 208 x 144 | half turn | two ash shelves across a fissure, each core over the vent of a breached cinder cone | own core 41.2 / 52; enemy spawn to the core 137.6 / 139, 20 bridged; GO1 3.34 / 2.67 | 29 min |
| Destroy the monument | `redwash-mesa` | 192 x 128 | mirror in x | badlands mesas crossed at three heights, a cliff house between a table monument and a canyon-town monument | own table / wash 48.2 / 56, 40.3 / 48; enemy 148.5 / 162, 131.2 / 141; GO1 3.08 and 3.26 / 2.89 and 2.94 | 12 min |
| Capture the wool | `brassmoor-works` | 176 x 224 | half turn | an ironworks over smog: a gatehouse over a yard, a boiler house and a water tower behind bedrock lines | spawn to band 88; spawn to own rooms 72.3, 68.9; band to each room 81, 76 (by the flats) and 96, 92 (over the wall); building, spawn to the enemy's wool 232, 227 | 14 min |
| Team deathmatch | `vinewatch-ruins` | 96 x 112 | mirror in z | a white temple ruin in a jungle bowl, three lanes and a cistern under the middle | spawn to the middle by each lane 51.0 to 58.4 / 57 to 78, equal for both teams | 10 min |
| King of the hill (chosen) | `tidewell-canals` | 160 x 128 | half turn and mirror in z | a canal quarter: a Campo worth two under a gallery, two fish markets worth one | spawn to the Campo 70.3 / 76; to each market 92.1 and 93.1 / 106 and 107, the same for both teams | 9 min |

**The times are from the commit stamps.** The first board's 29 minutes include writing `common.py`; the reading
before it (the guide, the README, `match-flow.md`, `approaches.md`, both ports and the house rules) is not
counted.

**King of the hill was chosen because its law is the most detailed and its corner of the library the least
tried.** `approaches.md` and `match-flow.md` §10 say where points go and what surrounds them. The studio reads a
`Hill` as valid where it refuses a flag or a score box. And a hill board exercises arrivals at a shared target,
sight from a pad and a walkable upper storey, which the other four did not.

**The five are different in kind, not only in paint.** The ground families are grey ash, orange badlands, grey
decks under red brick, a pale temple on jungle green, and pale plaster over grey paving. The arrangements are two
floating shelves, two banded mesas, a works of decks over void, an enclosed arena, and a walled town on water.
Each board uses a different symmetry from its neighbours in the list.

## The library's gaps and bugs, ranked

**Ranked by how much play they can decide without anybody noticing, then by how many boards met them.**

1. **The plan walk and the built walk measure different blocks, and the goal rules do not say which they mean.**
   The plan walks octile, `walk.walk` counts four-way moves, and an open diagonal is 28.3 in one and 40 in the
   other (reproduction in `cinder-reach/REPORT.md`). GO1 passed in the plan on both destroy boards (3.34, 3.08 and
   3.26) and fell under 3 in the built walk (2.67, 2.89 and 2.94); one GO3 rose to 162 against 150. All five boards
   met it.
2. **The library writes over the void without being asked.** `build.site` fills its eased ring in void columns
   (52 blocks in a twelve-block reproduction, in `redwash-mesa/REPORT.md`). `trees.scatter` hangs crowns over the
   void unless `allowed` is passed. Both were found only by the read-back's count of standable columns over the
   void (boards 1 and 2).
3. **A plan cannot state a join.** A tunnel meeting a sinkhole, a cistern coming up through a floor, a shaft's
   ladder, a bridge reaching a tunnel mouth in a cliff, a lane meeting a room at its corner: each was drawn by
   hand, and four of them were wrong in the first plan (boards 1, 2, 3, 4). `plangraph.walkable` drops a storey's
   cells that lack headroom and says nothing (reproduction in `vinewatch-ruins/REPORT.md`).
4. **`facade.extrude` patterns nothing on a wall one block thick.** Every cell of a one-block ring is open on two
   sides, so it is a corner and gets no face (reproduction in `brassmoor-works/REPORT.md`). The Lantern Karst port
   met the same thing; every room and hall here was walled by a local loop.
5. **Each mode's rules are measured by hand in each checker.** GO1, GO3 and GO4; SP10, WL7, WL9 and WL10e; a hill's
   arrivals and what it sees: about 120 lines a board, the same rows the ports wrote. `common.via`, `common.gaps`
   and the "within 1.35 of the shortest" live-ground measure were each needed by more than one board.
6. **One symmetry at a time, and the axis is copied over.** `Symmetry` is one operation, so a board symmetric two
   ways is drawn through a local `quad`; `turn_world` copies one half whole, so whatever straddles the axis is laid
   after the turn (boards 4 and 5).
7. **Two conventions for one flight of stairs.** `Raster.flight` widens either side of its line; `build.stairs`
   widens to the right of the climb. A north stair came out a column off on board 2, caught only by reading the
   library's code.
8. **A house's door is known only after it is built.** The plan re-derives it (`door_cell`) and the generator
   raises if they disagree, as in the Riftwater port (boards 1 and 2).
9. **Paint by place, and floors in cells.** `terrain.lay` paints the top by slope alone and `route.pave` picks a
   block per column at random. Every board used `common.cell_pick` for floors and most used `common.set_paint` for
   inset patches, which is what the look ruling asks for.
10. **A deathmatch's scoring is unread.** `mapxml` has no `score(kills=...)`, and the studio's reader counts
    nothing for `<score>`, so a mistake in it passes as valid (board 4).

**One environment fault cost a run.** A build folder in the shared scratch space held a different world (another
origin, another size) between the generator and the renders; something else had written to the same path. The
default `/tmp/<slug>-build` that `pgmvox.run` uses has the same exposure, and a folder named for the session as
well as the slug would remove it.

## What I would change in AGENT-GUIDE.md

- **Say which walk the goal rules are against, and require both in the check.** One sentence: GO1, GO3 and GO4 are
  stated in the studio's units, the plan's octile walk reads short of the built walk by up to a third, so a plan
  should hold its ratios with a margin and the read-back should report them again.
- **Add "the plan states its joins" to the five things a plan is complete with.** Every place one piece or storey
  meets another (a stair, a ladder, a stairwell, a bridge onto a mouth) as data, each with a check that it is an
  edge join of at least a lane's width and that both sides are walked.
- **Make sight a standard row for every mode.** What each objective or pad sees of each spawn, against zero; and in
  the read-back, eyes only on places the walk reaches, or every wall top counts.
- **Add a row to the per-mode table for team deathmatch,** and add to the capture row that each build zone must
  touch the floor its bridges start from.
- **Recommend printing the plan's heights as a grid round each piece before the sketch.** On these five boards it
  found more faults than any other single step: stairs climbing the wrong way, gates on the wrong row, houses on a
  wall, pieces meeting at a corner.
- **Say that a half turn alone gives each team a nearer flank.** A capture-point board that wants every point the
  same walk for both teams needs a second symmetry inside the half, or measured equal walks.
- **Keep the first sketch before the first change, by the tool rather than by memory.** The guide says to keep it;
  board 1 did not. `run` could write each sketch with a version suffix and never overwrite one.
