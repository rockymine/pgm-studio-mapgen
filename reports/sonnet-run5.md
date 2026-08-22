# Sonnet run 5 — Fellgate Moor

## What I set out to build

A CTW moorland lane, deliberately elongated rather than square (a lane, per the brief, not a square board
where every goal is equidistant from both spawns). Each side: a spawn at the back with a small hamlet
behind it, a bothy (the wool room) tucked off the main track and guarded by a bedrock approach wall, a
frontline that splits around a raised-bank ring hollow rather than running as one wide corridor, a mid
crossed by a ford at the centre and, out on the flank, a second lane that floods open forty-five minutes
in. One theme across the whole board — a heather-and-peat moor in grass, coarse dirt and cobblestone — so
the board's variety comes from height and dressing rather than from a swatch of materials. Full account
and coordinates are in `review/sonnet-r5-fellgate.md`; this document is the account of the run itself.

## What I could not say

**Nothing in this run turned out to be a genuine capability gap.** Everything I set out to build, the
studio could build; every obstacle I hit was either something the pipeline told me about directly (and I
fixed), or something I found by reading the code the documentation pointed at. I looked, before writing
anything below, and found no case where a wanted capability was simply absent.

The nearest thing to a gap is a documentation-precision issue rather than a missing feature:

- **Wanted:** to set which face of an approach wall carries the defence chests.
- **Tried:** `tools/plan.md`'s own prose — *"`side` names which of the wall's two faces carries its
  defence chests, as the piece id that face looks out at"* — reads as "pass the piece's own id string," so
  I posted `"side": "moor-gate"` (naming the piece I wanted the chests to face).
- **Checked:** `PlanWall.ChestPiece` in `src/PgmStudio.Pgm/Plan/PlanModel.cs` resolves `Side` against the
  literal string `"b"` (case-insensitive) and falls back to `A` otherwise — so any value other than
  literally `"a"` or `"b"` silently defaults to `A`. `GET /api/openapi/v1.json`'s `PlanWall` schema states
  this precisely: *"named by the piece that face looks out at: `\"a\"` or `\"b\"`."*
- **Verdict: mistaken**, not unreachable. The openapi schema — which the brief names as the first thing to
  check — already says the right thing; I read the tool document's prose first, which is genuinely more
  ambiguous than the generated schema on this one field, and did not cross-check openapi until the
  behaviour surprised me. Worth a documentation note (`tools/plan.md` could say "the literal string `a` or
  `b`" instead of "the piece id"), but the capability was never in question.

## What I got wrong, once I found out

**The wool room, drawn inline on the spine.** The first cut of the plan put `bothy` directly between
`lane-out` and `wall-mouth` — the natural place to draw a room when the lane is what you drew first. It
compiled clean (`POST /plan/compile`: no warnings), evaluated clean (`score 0, valid: true`), and refused
only at `GET /map/{slug}/export`, 409, with `EX1`: *"2 objective(s) sit behind ground an enter rule bars
the attacking team from — check the protection regions."* Nothing upstream of the export gate reads an
`enter` apply-rule, so nothing said this earlier.

The claim that looked right and wasn't: I assumed a wool room's own topology (which pieces touch it, in
what order) was purely a geometry question the connectivity gates (`CT12`, the traversability read on a
half-built board) would have already exercised. It isn't — `WoolGenerator` writes `enter =
not-<owner>` over the room's own region, barring the *defending* team from entering its own wool room by
design (`match-flow.md` §4.7's "defenders hold the wall, attackers get in" is this rule, not a convention
layered on top of it). Putting the room on the defenders' only road home meant the same rule that keeps
defenders out of the room also cut them off from their own frontline, and nothing before the export gate
computes a navigable set *per team* — every earlier read (`plan/inspect`'s `islandGaps`, the plan
evaluator, `GET .../traversability` itself, before I read its `isolated` field's `for` closely) answers a
single team-blind connectivity question. `GET /map/{slug}/traversability` does carry the per-team read
(`isolated: [{kind, name, for}]`), and reading it — rather than just the top-level `connected: false` —
is what named the actual cause. Fixed by making `bothy` branch off `wall-mouth` rather than sit on it, so
the defenders' own walk never enters the room. `review/sonnet-r5-fellgate.md` has the full account and the
`GET .../traversability` before/after.

**Two pieces that were pure decoration.** An early draft carried a west "peat-cut" bypass and an east
"tor-knoll" vantage, both added for variety before checking whether either was on any route. `GET
/map/{slug}/plan/flow` (asked, as `tools/README.md` and the brief both say to, before compiling) answered
46% of the board's ground dead — reachable, on the way to nothing. I had read the exact same lesson in
`GENERATION-NOTES.md` (`opus5-wheal-hazel`'s 27.2%) before drawing a single piece and still reproduced a
worse version of it, because the mistake isn't "forgetting the rule" — it's drawing width and shape for
how a board *looks* on paper before asking whether a route needs it. Cut both, folded the same variety
into a ring-hub split (`fork → {moor-w, moor-e} → hub` around an enclosed void) that the flow/coverage
reads do credit because both legs sit on the shortest walk from one side or the other; final dead share
10.8%.

**An iron marker beside the spawn's own wall clearance.** `[2,1]` on a 4×4-cell (20×20-block) spawn piece
answered `WX8`, *"no room size leaves 1 block clear of the shell for even the smallest cube."* I read the
rule text (`GET /api/rules?rule=WX8`) rather than guess again: the shell already claims a 1-block inset
(`WX1`) off a piece already at `ST9`'s 20×20 cap, and an iron cube needs its own 1-block clearance off
whatever the shell's outer face still is — there is no ring left wide enough for both, at the size cap,
whatever roomStyle Sketch later binds. This held even though I'd bound `roomStyles.spawn: null` (no
stamped building) — `WX1`/`WX8` run at the plan/compile level, before Sketch's binding exists to say a
shell won't be stamped, so the room-frame math is conservative about a shell that might still be there.
Dropped the iron marker rather than grow the spawn piece past the cap; a legitimate trade, not a bug.

**`observerY` left at its default.** Didn't get caught by any gate — `GET /export` succeeded with the
observer at `(0, 24, 0)`, which is `surface + 15`, sitting inside the ford every match crosses. Caught
only by column-probing `(0, 0)` after the first successful export and comparing against
`GENERATION-NOTES.md`'s own note about this exact default. Fixed by stating `globals.observerY: 58`
explicitly; nothing else about the board changed.

## What worked first time

- The plan → layout → intent compile chain, on every iteration: `POST /plan/compile` never once answered
  a structural refusal across five plan revisions, because `POST /plan/evaluate` and `POST /plan/inspect`
  (asked before every store, per `tools/drive.py`'s own order) caught the shape questions before the
  compile ever saw them.
- The finish's `addShapes`, `roomStyles` (an inline forked style, not a library `@name`, since
  `tools/styles/` was off limits for this run), and `dressing` all landed exactly as authored on the first
  full build after the topology fix — `POST .../sketch/columns` answered `nothing declined` and
  `region/provenance.json`'s owner census matched every prop 1:1 (accounting for the orbit fan).
- The theme (`GET /terrain/patterns`'s field names, taken directly rather than guessed) painted correctly
  first try — no `RQ3` on any theme field, confirmed visually with `--topdown --material`.
- `tools/board.py` and `plan/ascii` caught every rectangle-adjacency mistake (a corner touch, a piece that
  didn't actually share an edge with its neighbour) before a single API call was made to store anything.
- `dotnet run tools/seed-library.cs` seeded the room-style library cleanly on the first run, with an
  honest report of which presets round-trip whole and which lose fields to the library's own schema
  (`cottage`, `longhouse`, etc. — not the preset I used).

## Open gameplay questions

No rule in `docs/gameplay/approaches.md` or `match-flow.md` settled these; each is a judgment call made
without the author, recorded here rather than filed as fact.

- **Should the bothy have a second entrance?** `WL8` (in `GET /api/rules`) says a wool's default is a
  single chokepoint route and that real maps sometimes add alternatives. I kept it single — one wall, one
  way in — rather than adding a second branch, mostly because a second branch is exactly the mistake this
  run made once already (ground that isn't clearly on a route). Whether this board wants the alternative
  WL8 describes is the author's call.
- **Is a 180-cell ring hollow the right size for a 16-a-side board?** I sized it to bring the plan
  evaluator's `G8` fill-ratio back into its authored corpus band (0.201–0.496) rather than from any
  player-count-driven formula. The evaluator says the *shape* reads like real boards at this scale; whether
  it plays right for 32 players on a 350-block lane is not something any read answers.
- **Is the hamlet worth its dead ground?** Two small houses south of each spawn cost roughly 4 of the
  final 10.8% dead-ground share (the plot's own dead-end tail). I judged the "village behind" idea from
  `docs/tools/plan.md`'s design notes worth that cost; a stricter reading of the coverage lesson would cut
  it to zero.
- **Should the wool's own approach lane (`wall-mouth`) be shared with the main frontline lane, or
  separate?** In the final shape, attackers reach the bothy by turning off the same lane defenders use to
  reach their own frontline. I did not try a version where the two are fully separate corridors; whether
  that reads as a cleaner defence or a redundant one is exactly the kind of question `approaches.md` says
  is the author's rather than the tool's.

## Where things ended up

`maps/sonnet-r5-fellgate/` — world, `map.xml`, ten renders across the plan/theme/build/export stages.
`specs/sonnet-r5-fellgate/` — the authored plan and finish, plus the two documents `tools/drive.py` wrote
back (`.layout.json`, `.intent.json`). `review/sonnet-r5-fellgate.md` — the measured record. The final
`GET /export` is a clean 200 with no `Pgm-Warnings`; `POST /plan/evaluate` on the stored plan still carries
one soft term (`LN1` lane-width 30, band 10–20 — the wall-mouth/bothy/fork cluster reads as one wide
junction to the lane-width measure) and one lint complaint (`ST8`, the wall sits 0 blocks from the room's
entrance rather than ST8's ~15 target, because the room branches sideways off the same piece the wall
guards rather than sitting downstream of it) — both left as known, minor, and explained in the review
rather than chased further.
