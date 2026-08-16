# The mapgen API, reviewed after driving it — and the fast-track

Written after authoring four boards end to end (see `fable-run3.md`), then reading the code the way the
CLAUDE.md duplication rules ask: one concept, one shape, and the tell is prose. Three sweeps fed this — a
distance-measurement inventory, an API-layer survey, and a task-board read — and every claim below carries
its file. The board ids cited are the existing ones; nothing here invents a parallel plan.

## 1. The distance question, settled by inventory

The worry was that "distance between objectives" is computed many ways. The inventory says: **the canon
already exists and the core is healthy; the duplication is at the edges.**

- The canonical primitive is `Geom.Cells.ShortestPath` / `PathLength` (`Geom/Cells.cs:48,77`) — 4-connected
  rectilinear walk, exactly what `rules.md` amendment 13 declares. It lives in the one leaf every project
  reaches. All three spawn↔wool evaluator terms already route through it via `SurfaceNav`.
- **Nine implementations answer "how far is a spawn from its objective"** across five metrics and four
  grids — but most are legitimately different questions (boolean reachability, bridge cost in blocks
  placed, piece-hop counts). The genuine duplications are small and precise:
  1. `Triangle.FrontDistances` hand-rolls a multi-target BFS (`TriangleTerms.cs:174`) because `Cells` has
     no multi-target overload — a fifth copy of BFS logic in the one file that also mixes an un-fanned
     walkable surface with fanned targets.
  2. **Snap-to-walkable exists four ways**: Manhattan ring r≤2 (`SurfaceNav.cs:44`), square ring r=3
     (`Traversability.cs:191`), r=4 (`KitReach.cs:190`), r=6 (`TraversabilityRender.cs:242`). Four radii,
     two ring metrics, three endpoint-resolution fallback chains, one operation.
  3. `ContactGraph.VoidSpan` is the one Euclidean `Math.Sqrt` feeding a rule (G5's hop band) — arguably
     right for a jump, but unmarked as an exemption under a preamble that says all distances are walks.
  4. "Is this rect too close to that one" exists as four independent Chebyshev tests (`SeatGeometry`,
     `BandWoolClearance`, `DressingScope.GoalClearance`, `IslandRolesEndpoint.ClusterAnchors`).
- **Nothing anywhere measures a distance to a destroyable or a core.** The traversability gate reports
  them as points and deliberately does not gate on them; every evaluator distance term reads spawns and
  wools only. A destroy board can ship an unreachable monument today and nothing says so. B188's own
  2.9-median table is straight-line off XML centroids — the retired unit — and the sweep is not in the
  repo, so the number cannot be reused as a band; per amendment 13 the band is the author's to state.

## 2. The API layer, in one paragraph

146 endpoint classes in 40 files over a `Services/` bag of four unrelated populations; the composition
root is bigger than its own structure doc believes (two stale, mutually inconsistent counts at
`project-structure.md:92,197`). The healthiest corner is compose→evaluate→pin→author: genuinely one path,
no second evaluation wiring. The unhealthiest: **the refusal envelope exists in seven shapes** (16 proper
`Refusals.Of` sites against 29 anonymous `{error}` objects, a hand-rolled `{error, islands, hint}`, and
`MapExportComposer` re-implementing the envelope as a `Dict` because `Export` cannot see `Api` — two wire
projections of `Finding`, one per consumer); **six hand-rolled artifact stores** whose own docstrings say
"mirrors X"; the same six-line plan-body prologue five times; and — the structural one — **`tools/mapgen`
re-implements the export leg and drops three of its four gates** (OB17 via its own `GoalsOverVoid`, OB19
and OB20 absent), directly contradicting `project-structure.md`'s "through the real export path".

## 3. The silences, which the run paid for twice

Every expensive failure this run hit was a **silent decline**, and the board already knows the family:
`B146` (path band drops a building), `B142` (prop over void), `B187` (house over void), `B166` (buildings
colliding) — bucket 6, all waiting on **`B37`'s placement report the export can refuse on**. The run added
two: an unplaceable iron cube (`WX9`) that no evaluate term and no compile warning carries, and the
lint-reach fact behind it — `B177`'s corrected premise says `LintSp2` exists and *nothing runs the lint on
a posted plan* (`B109`). The preview-side halves were closed this session (prop-preview now refuses
`HJ*`/`HP*`; `PL12`; compile 400s carry the message), but claim-collision drops are only visible in
`provenance.json` after a build.

## 4. The fast-track — seven moves, in order

Ranked by what they buy per unit of change; the first four are each a day or less.

1. **Two helpers in `Geom.Cells`** — a multi-target `PathLength(from, targets, within)` and one canonical
   `SnapToWalkable(cell, within, radius)`. Delete the hand-rolled BFS in `TriangleTerms` and converge the
   four snaps on it (each caller keeps its radius; the *metric* becomes one). Zero boundary moves; this is
   the whole "one distance" consolidation the codebase actually needs.
2. **Goal distance terms + goal gating** (the B188 fast half). `GoalTerms.cs` beside `ObjectiveTerms.cs`:
   per-team spawn→goal walk and the enemy/own ratio, `LearnsFromTraced: false` like `SpawnWoolRatio`.
   Plumbing it needs: a goal accessor on `SurfaceNav`, an absolute-`at` branch in `MarkerCell` (B128
   goals name no piece), and the fanned board for the cross-team leg — `Triangle.FrontDistances` is the
   precedent to fix in the same motion. **The band is the author's to state in walk blocks** (amendment
   13 retired the 2.9 table); ship the term, ask for the number. In the same change: let destroyables and
   cores gate `Traversability.Connected` — an unreachable monument should refuse export like an
   unreachable wool does.
3. **Route `tools/mapgen` through `MapExportComposer.Compose`** by splitting the gate chain from the
   doc-assembly. Deletes `GoalsOverVoid` (one of four goal-over-void copies) and puts OB17/OB19/OB20 in
   front of every mapgen world. Until this lands, the tool ships maps the HTTP export would refuse.
4. **Push the refusal envelope down to `Domain`** beside `Finding.Wire()`, delete one of the two `Finding`
   projections, and let `MapExportComposer.Refuse` use it. The 29 anonymous `{error}` sites then convert
   mechanically (each needs its rule id from `docs/refusals.md`).
5. **B37's report, thinnest slice first**: the export response (and `tools/mapgen`'s summary) carries the
   decorator's own census — asked / placed / dropped-with-reason per prop. `Decorator` knows the reason at
   every early return; today the same `[]` means five different things. This closes B146/B142/B187/B166's
   *silence* without yet building the refusal semantics.
6. **Lint reach (B109/B177)**: `/plan/evaluate` (or a `?lint=true` on it) carries the validator's lint
   table — `SP2`, `WX4`, `WX8`/`WX9` — so an unplaceable iron or a mid-lane spawn is visible on the loop
   agents actually drive. `SP7` still needs its first implementation.
7. **Board hygiene, twenty minutes**: BACKLOG's heading collapse makes ~50 tasks (all of G158–G168, B37,
   B58…) structural children of "Bucket 13"; there is no `## Layout generation (G)` section though
   CLAUDE.md rule 5 names it; the bucket-set count is stated as 48, 40 and 44 in three places. Cheap to
   fix, and it is exactly the kind of drift that makes the *next* agent misread the board.

Deliberately **not** on the fast-track: the destroy-native composer (MG32/B106 — moves 1–2 are its
prerequisites, not substitutes), the `LibraryCrud` generic and `Services/` foldering (real but cosmetic
next to the above), and any corpus re-sweep of the distance bands (amendment 13 forbids exactly that).

## 5. Two small doc debts from this run's findings

- The donut sanction's id-prefix contract (`ClosureAnalysis.AnyHoleRingedBy`) belongs in `rules.md` WL8's
  text — today it is discoverable only by tripping the hard term.
- `HJ5` fired on a configuration that appears to satisfy its stated clauses (kerbstone review, east-wing
  case); `WingJointRules`' height clause wants a read and either a fix or a sharper sentence.

## Postscript — what landed, same day

The fast-track was executed the session it was proposed, under the author's four rulings (terms ship
unbanded; an unreachable goal hard-refuses; B37 report-first; mixed orchestration — two moves by the
proposing model, the mechanical five by Sonnet subagents under written briefs, every diff reviewed and
every suite run serialized between merges).

| Move | Landed as |
|---|---|
| 1 — Geom helpers | `Cells.PathLengthToAny` + `Cells.SnapToWalkable`; the evaluator's hand-rolled BFS deleted; four snaps converged at their own radii |
| 2 — goal distance + gating | destroyables/cores gate `EX1` like wools; `POST /plan/inspect` answers `goalDistances` (own walk, enemy walk, ratio — firnline reads 3.0, kerbstone 3.9, both walk-based) |
| 3 — one gate chain | `MapExportComposer.ComposeSketch`; `tools/mapgen` routes through it, OB17/OB19/playability included, wool monuments folded into OB17 |
| 4 — one envelope | `Finding.Envelope` in `Domain`; `MapExportComposer.Refuse` a one-liner; the orphaned-relief 409 speaks `SK1` findings |
| 5 — the census | `Decorator` reports every whole-prop decline with a reason: `region/dressing-report.json` beside the provenance sidecar + one mapgen stderr line per drop (B37 report-first over B146/B142/B187) |
| 6 — lint reach | `POST /plan/evaluate` carries the whole lint table as `lint[]` — `WX9`'s silent iron and `SP2`'s mid-lane spawn are visible on the loop (B109/B177) |
| 7 — board hygiene | bucket 13 closed, the G section exists, counts agree at forty-four, B107/CV16 refiled, project-structure's Api counts true |

Not done, deliberately: the ratio **band** (the author calibrates from the new measurement before it
scores), the destroy-native composer (moves 1–2 are its prerequisites), and the `LibraryCrud`/`Services/`
foldering (real, cosmetic, filed in §4's own not-now list).

Closed outright the same day, past the report-first slice: **B146** — by the author's ruling a path's band
no longer claims against a building at all (paths are laid first, the road runs to the porch, the house
wins the ground), so the family's worst member is not "reported now" but gone; the band still refuses the
scatter, with the census naming each refusal. And two rulings became pinned semantics: a water lane under
`deny(void)` is not a route pre-timer while an open build zone over void is (a test holds both halves), and
intended walls/climbs are recorded as relief-design concerns, never traversability faults
(`docs/design-decisions.md`).
