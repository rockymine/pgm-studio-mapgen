# Fable run 3 — four maps through the live API, and the fixes made along the way

Four boards — two capture-the-wool, two destroy-the-monument — authored end to end through the studio's
HTTP API in a cloud container, against `pgm-studio` at `claude/mapgen-map-design-api-78du90` (16 Aug 2026).
This run differs from the earlier ones in one respect: where a defect was found and was small enough to fix
without leaving the task, it was **fixed in the studio in the same session** rather than only filed. Five
landed; each is marked below.

The four maps: `firnline` (DTM, snow and mountains, a lane board), `kerbstone` (DTM, cityscape, a street
canyon), `sunspit` (CTW, summer beach, sea-split halves), `tanglewold` (CTW, woodlands, a forest board with
a causeway mid). Specs in `specs/<slug>/`, worlds in `maps/<slug>/`, measured records in `review/<slug>.md`.

## What was used deliberately, because the last runs could not

- **`GET /terrain/patterns` + `POST /terrain/material-preview`** as the design loop for paint: every theme
  on these boards was previewed as SVG and *looked at* before it was bound — the snow/ice `cell` mix and the
  city flagstone `voronoi` each went through two iterations at preview cost instead of build cost. The
  `reads` field is what made the choices legible: `laidLog` (reads `bend`) went on the pier deck where a
  colour pattern would have been invisible in plan.
- **Multi-wing, multi-storey buildings** (`G177`/`G172`): kerbstone carries an L-house with a **marching**
  wing under a forced crossing `ridge`, and a three-storey counting-house hall with a **projecting**
  two-storey wing; firnline carries an alpine L and a two-storey alpine variant with a porch. All verified
  standing via `region/provenance.json` owners.
- **The box model**: tanglewold's south wool is annotated as a `wool` box and the producibility read answers
  its identity as **`Donut (w 2)`** — the shape was recognized, not just accepted.
- **`POST /plan/evaluate` before anything**: every board went through the evaluator first; firnline went
  1001 → 0.89 across three edits, sunspit reached **score 0**.
- **Water lanes**: sunspit's tidal lane ships in its `map.xml` (4 region references) — the run-2 report's
  export-drop bug is confirmed **fixed** (`SketchWorldBuilder` now rebuilds the intent with `with`).

## Faults found, and their verdicts

| # | Found | Checked | Verdict |
|---|---|---|---|
| 1 | `POST /plan/compile` answered a bare `{"error":"Invalid plan structure"}` (no rule, no message) for a plan `/plan/evaluate` called `valid: true` — a `mirrors: false` piece touching mirrored land | `PlanCompiler.BuildLayout` throws `InvalidOperationException` with a good sentence; all four catch sites in `PlanInspectEndpoints` discarded it; nothing in `PlanValidator.Check` refuses the case, so evaluate and compile disagreed | **missing** — **fixed this run**: `PL12` added to `PlanValidator` (named refusal, subjects = the component), the catch sites now carry the message |
| 2 | `POST /terrain/prop-preview` rendered a two-wing house whose wings share a row — the same plan the dressing pass then silently dropped (`HJ1`) | `PropPreviewEndpoint` never called `HouseProp.Check()`; the preview certified exactly the prop most in need of the warning | **missing** — **fixed this run**: the preview refuses with the same `HJ*`/`HP*` findings the build acts on |
| 3 | A symmetric one-monument-per-team board ships `<objective>Destroy the enemy's monuments!</objective>` (opus5 run-2 finding 8, still live) | `MetaGenerator.Objective` counted the fanned list | **missing** — **fixed this run**: counts are per team; one wool per team now also reads "Capture the wool!" |
| 4 | A path's claimed band swings outside the drawn polyline at corners and silently dropped four houses whose clearance to every drawn segment was ≥1.5 blocks | `PathBand.Centerline` runs the points through **`CatmullRom.Spline`** — the band follows the smoothed curve, which overshoots outside corners by several blocks on long segments. Membership is cell-centre within radius (`Polyline.Hits`), so the polyline-margin arithmetic every earlier report suggests is measured against the wrong line | **mistaken** (mine, then diagnosed) — the working rule is in GENERATION-NOTES §12; the underlying silence is the same `B*` path-claim silence already on the board |
| 5 | An L-wing sharing its hall's edge **row** is `HJ1` (overlap), because `corners` are inclusive cell coordinates — "touching" means adjacent rows | `AuthoredWing.Corners` floored inclusive; the worked example in `sketch.md` shows touching-by-adjacency but never says the corners are inclusive | **mistaken** — cost one build cycle; GENERATION-NOTES §13 |
| 6 | A square-ish hall with a wide shallow wing dropped silently: both ridges tie AlongX → `HJ3` gutter | `sketch.md` documents the tie rule; the failure is that the *build* is silent — but with fix #2, `prop-preview` now answers `HJ3` before building | **mistaken**, and the silence is closed by fix #2 |
| 7 | `porch.edge: "front"` refuses on a snapshot (`RQ1`, enum convert error) though the porch table documents `front` | The **save request** maps `front`→null; the **snapshot's** `RoomEdge?` has no `front` member — null is the snapshot's word for "door wall". Two layers, two words for one thing | **unreachable** (documented word not readable at the layer an agent actually posts) — worth a converter or a doc line |
| 8 | The donut/staple wool sanction is a **naming convention**: a hole's ring is "own" only if the leg pieces share the wool room's id prefix (`ClosureAnalysis.AnyHoleRingedBy`); legs named `south-rim` fired hard `wool-ringed-hole`, renamed `wool-south-rim` passed | Read at `Compose/ClosureAnalysis.cs` — nothing in `rules.md` WL8 or any tool doc says the sanction keys on piece ids | **unreachable** — the mechanism exists, the contract is invisible to a hand author |
| 9 | `POST .../sketch/relief/read` answers `{"islands": []}` for a valid layout that simply declares no relief — same symptom as the type-less-shape trap in GENERATION-NOTES §1 | The read reports islands that carry a relief; a no-relief board legitimately answers empty | **mistaken** (mine) — but the overload of one symptom for two causes is real; the §1 diagnostic should say "or the layout declares no relief" |
| 10 | A spawn's iron marker produced iron-cube provenance on firnline and none on tanglewold with identical markers | `IronResolution` (WX8/WX9): beside tanglewold's 10-block-wide spawn room the `[0.5, 0.5]` marker has no legal strip, degrades to `Placeable: false`, and stamps nothing — and no evaluate term and no compile warning carries WX8/WX9, so the API loop never says so. `POST /plan/inspect`'s structures feed is the one surface that answers (a placeable iron draws a box); sweeping offsets there found `[1, 0.5]` | **unreachable** — the flag exists (`WX9`) and reaches no response an agent reads; tanglewold rebuilt with the seated cube |

## What worked without a fight

- The **plan → evaluate → compile → from-plan → finish → intent → export** loop is solid; nothing 500d,
  and every refusal that fired carried the field or rule after the fixes above.
- `anchor_heights` ramps (knoll ramps on firnline) — right first time, again.
- The `walls` one-liner: every wall arrived where the corpus puts one (bluff wool 20/13 blocks; both
  tanglewold wools).
- Per-shape themes at six-to-seven registry entries per board, several patterns deep (`cell`, `voronoi`,
  `noise`, `turbulence`, `checker`, `layered`, `laidLog`), previewed before binding.
- `relief_scope: exclude` per tier + one solved tier + `stairs: true` gives crisp built terraces against
  rolling ground exactly as designed.
- B188 discipline on the two destroy boards: both are lanes (90×200, 95×201), goal-to-own-spawn ≈ 35–40,
  ratio to enemy spawn ≈ 3.5–4.6 — inside the corpus envelope (median 2.9, p90 5.0).

## The one design rule this run would add to the errata

**Margins are measured to the spline, not the polyline** (fault 4). A street grid with corners wants chamfer
points (two extra points bracketing each 90° turn); a frontage line wants 3+ blocks beyond the *claimed
band*, and the band's centreline is the Catmull-Rom through your points. When in doubt, drop the corner
radius by one and add a control point — the cost is nothing and the failure it prevents is the silent one.

**Addendum, same day (fault 4 retired for buildings).** The author's ruling landed after this report: a
path's band no longer claims against a building at all — paths are laid first, a house drawn across the
pavement stands and the road ends at its wall, so a route can run to a porch. The frontage-margin arithmetic
above is obsolete for houses; it still governs the road's own course and the scatter (a tree or boulder on
the real curve is refused, now with a `dressing-report.json` entry naming the cell). GENERATION-NOTES §7/§12
carry the current rule.

---
_Generated with the studio's own endpoints; every claim above is reproducible from `specs/` against the
branch named in the header._
