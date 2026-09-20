# Walls and iron

**A defence wall and an iron cube are the two structures nothing generated ever asks for.** `Composer`
writes neither list, so both exist only where an author states them — and both are stated on a **plan**,
not on a layout, which makes this the one card that is a plan first. It is deliberately non-symmetric: every
station is authored once and stands on its own, so nothing here is an orbit image of anything else. Open it
in the studio as `technique-walls-and-iron`, or run `build.py`.

Three approaches and a spawn. The wall is the same wall at all three stations; what changes is where it
stands and what ground is beside it.

| Station | Pieces, north to south | Walls | What the walk says |
|---|---|---|---|
| `line` | room · approach · field | one, on the approach's outer interface | `barrier +4`, and no ground either side of it |
| `shoulder` | room · approach with a piece each side · field | the same one | the same `barrier +4` — and two clean legs round its end |
| `sealed` | room · inner · middle · outer | two, in series | `barrier +4` twice on one approach |
| the spawn | spawn piece · yard | — | one cube of the two markers authored |

## A wall is two piece ids, and everything else is derived

**`PlanWall` carries `a` and `b` and nothing else.** No side, no length, no thickness, no height. The wall
is stamped along the interval the two named pieces share, and `compiled.txt` reads what came out: four
`WallStructure` entries, each **16 blocks long and 2 thick**, `topY` 11 from the ground they stand on, and a
`chestOnMinFace` the compiler decided rather than the author.

**A wall is bedrock.** `walls.txt` reads the column at (8, 32) as six courses of it. Nothing breaks it and
nothing is placed over it, which is the whole of the device — it is a prepared line the defence holds, not
scenery and not damage.

**It may not stand on the wool room's own interface.** `PL13` refuses that outright — *"the wall and the
room stand through each other and the room can barely be entered"* — and names where it belongs instead:
about fifteen blocks out, on the approach's outer interface, where the approach meets the board. Every
station here is three pieces deep for exactly that reason.

## What separates a line from an obstacle is the ground beside it

**The wall at `line` and the wall at `shoulder` are the same 16 blocks, and only one of them is a
decision.** `shoulder` has a piece of ground pulled out past each of the wall's ends, and two walk legs
reach the approach *behind* the wall with **nothing placed** — north off the field into the piece beside the
approach, then east into the approach itself. At `line` the same two columns answer `0 solid block(s)`.

**A wall with a walk around it has stopped being a decision.** That is the author's ruling, and the reads
are what make it checkable: the wall's own `barrier +4` is identical at both stations, so a walk *at* the
wall cannot tell them apart. What tells them apart is whether there is ground at the wall's ends.

**A walk travels its aim line and reports what it meets.** It is not a pathfinder, so it will not discover
the way round for you — the legs above were authored, one per piece the route crosses. A single walk
through a wall proves the wall is there and proves nothing about whether it can be avoided.

**Two walls in series is the other bound.** `sealed` answers `barrier +4` twice on one approach, which
`docs/gameplay/approaches.md` settles as a sealed room rather than a prepared line: one wall, on one
interface, is what a wool wants behind it.

**The `barrier +7` at the end of every line is not a defence wall.** It is the wool room's own wall, which
every station has and no `walls` entry put there.

## A team is an orbit image, so a non-symmetric plan has one

**`globals.symmetry: "none"` compiles to one team however many spawn markers the plan carries.** Two of
them land on the same team, and `POST /map/from-documents` refuses the result — **`RQ5 — id
'red-spawn-point' already in use`**. A two-team board comes from symmetry; a second spawn marker does not
make one.

**A plan's `meta.authors` does not survive the compile.** The intent comes back with an empty list and the
export answers `EX6`, which is a complaint about the observer platform's authors board. The names go back
onto the intent before it is stored.

## An iron cube needs a yard, and the default shell leaves none

**`at` is the cube's centre, in blocks from the piece's minimum corner, on a half-block lattice.** Not
cells, and not a corner. The cube is 3 × 3, and `WX8` wants that footprint inside the piece with **2 blocks
of clear air to the shell**.

**So the spawn's building has to be smaller than its piece.** `WX1`'s default shell is the piece inset one
block on every side, which leaves a one-block ring — no yard, and no cube anywhere on the piece. This card
states `footprint: [4, 1, 12, 12]` on a 20 × 20 piece, and the cube stands in the strip that leaves.

**Two markers were authored and one cube stands.** `iron.txt` reads three iron blocks at (194, 32) and
nothing but the spawn floor at (194, 26). The compile kept **both** points; the stamper placed one.

**`WX9` is why nothing said so at the export.** An unplaceable marker is not an error — it stamps nothing
and the room takes its full clearance. A cube missing from a built world is a **plan** finding to go back
and read, never an export one, and `POST /api/plan/evaluate` is where the `WX8` complaint was waiting.

## The recipe

- **state a wall as the two pieces it stands between.** Everything else — its length, its thickness, its
  height, which face carries the chests — is derived, and none of it is yours to write.
- **never on the room's own interface.** `PL13` refuses it; put it about fifteen blocks out, where the
  approach meets the board.
- **one wall, on one interface.** Two in series is a sealed room, and the walk will say `barrier` twice.
- **check the ground at the wall's ends, not the wall.** A walk through it reads the same whether or not
  there is a way round; a column beside it is what answers.
- **a walk is not a pathfinder.** To show a route exists, author its legs.
- **symmetry is what makes a second team.** A non-symmetric plan is a one-team board, and a second spawn
  marker is an id collision rather than an opponent.
- **give a spawn a `footprint` smaller than its piece before authoring an iron cube.** The default shell
  leaves a one-block ring, which is not a yard.
- **read `POST /plan/evaluate` before the export.** `WX8` complains there; `WX9` means the export will
  build the board without the cube and without a word.

## Limits

**This is not a playable board.** One team, three wool rooms, no destroy goal, and `G8` reads
`dead-share 0.131` against a band of `[0, 0.12]` — a demonstration board earns that and a real one does
not.

**Where a wall belongs on a real approach is not derivable here.** What an objective needs around it, and
what a wall is for, is `docs/gameplay/approaches.md`, whose claims are the author's.

**The wall's chest face is not worked.** `chestOnMinFace` comes back false at every station on this board;
what decides it, and what the chests hold, is the compiler's and is not read here.

## What checks it

- `compiled.txt` — the four `walls` entries in and the four `WallStructure` out, with every derived number;
  and the two things a non-symmetric plan does not carry.
- `walls.txt` — a walk straight at each wall, the three legs round the `shoulder` wall's end, the columns
  that are void beside `line`, and what a wall is made of.
- `iron.txt` — the two markers, the `WX8` complaint on one of them, and the column where each landed.
- `walls-and-iron.plan.json` — 14 pieces, 4 walls, 2 iron markers, `symmetry: "none"`.

Renders, off the **built** world: `board.png`, the four stations from above, where the `shoulder` wall is
visibly shorter than the ground it crosses; `structures.png`, the same read by what the build claimed;
`line.png`, `shoulder.png` and `sealed.png`, each approach cut north to south the way it is walked; and
`iron.png`, the spawn and its cube.
