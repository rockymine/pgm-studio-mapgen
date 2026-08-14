# Sable Marsh — Map 2, CTW

`rot_180`, 20 players, 200×192. My own design, read against `match-flow.md` before drawing anything.

## What it is

A reed marsh around a ring-shaped hub with an open pool at its centre. Spawn sits at the back on a
fortified platform (`marsh-hold`); a **two-legged frontline** (`leg-w`/`leg-e`) runs forward from it with
an enclosed void between the legs, so the crossing into the hub forks before either team has touched the
other's land — the single largest source of routing options `match-flow.md` §3.2 measures (97% of
objectives behind a two-legged frontline carry more than one attack route). The hub itself is a true ring:
a subtract cut through its centre gives it two ways across, with a reed pool sitting in the hole. Each
team defends **two wools in its own forward territory** — a walled one (`west-lane`, `stockade` theme,
timber-stockade wall pattern, an authored defence wall on the `approach-a`/`wool-a` interface) and an open
one (`east-lane`, `sable-reeds` theme, scrub and birch/spruce cover, no wall) — so the two objectives on
one team's own side read as genuinely different problems for the attacker rather than the same room twice.

## How it plays

- **The entrance void forks the rush before it starts.** A player leaving spawn down either leg is already
  committed to a side; the void between the legs (`entrance-void`) cannot be crossed on foot, only walked
  around, matching §3.2's "the band crossing forks before the attacker has touched the defender's land."
- **The hub's ring gives a second choice at the middle**, per §3.2's "ways across the hub" — a solid hub
  never offers this, a ring one does on 163 of 224 spawn-to-wool crossings in the corpus. Whoever holds the
  pool at the centre watches both doors.
- **The two wools differ in kind, not just in position.** The walled lane is the prepared line
  `match-flow.md` §6.2 measures — a raider has to get over or through the `stockade` wall, which stands on
  the `approach-a`/`wool-a` interface exactly where `PlanWall` puts it. The open lane has no such line: its
  defence is the cover the reeds and scrub give an ambusher, not a barrier. `approaches.md`'s claim that
  "the approaches should differ" is answered twice on one board rather than once.
- **The captured-room dynamic (§4.8) has somewhere to go on this board**, because both of a team's own
  wools sit forward of their spawn rather than deep behind it — a captured room is a genuine forward base,
  not a dead end at the map's edge.

## Techniques used

- **A ring hub is a sketch-level subtract, not a plan buffer**, and this is the fix from Map 1's mistake
  applied correctly the first time here: I first tried declaring `hub-hole` as a plan `buffer` sitting
  entirely inside the `hub-ring` piece — which compiles fine and does *nothing*, because "a buffer over a
  generating piece is inert" (`plan.md`). The hole never appeared. I moved the cut to the sketch layer, a
  `subtract` polygon over the same footprint, the same way `corvid-hollow`'s moat works — see *What I got
  wrong*.
- **A declared build zone is what makes a piece "frontline."** My first plan had no `zones` entry at all,
  and the compile refused every wool as "only reachable through a spawn piece (SP1)" — not because no path
  existed (the interface graph was fine), but because `PlanValidator`'s reachability check starts its walk
  from pieces the plan marks `frontline`, and that set is derived from `plan.BuildZones`, not from role or
  adjacency. A CTW map needs a declared mid band for the SP1 check alone, independent of whether the
  ground actually needs bridging — see *What I got wrong*.
- **The two mirrored halves have to physically touch at the axis.** My first `hub-ring` stopped nine cells
  short of `z=0`; its mirror image stopped the same nine cells short on the other side, leaving a drawn gap
  neither half's outline covered and no buffer to declare it, so the two teams' territories were never
  connected at all. Extending `hub-ring` to the axis fixed it — recorded because it is the same class of
  mistake as `corvid-hollow`'s bezier bug: a boundary two shapes are each responsible for half of, drawn
  without checking that the halves actually meet.
- **Per-shape theming, five themes**: `reed-hub` (a `voronoi` fabric of dirt/grass), `stockade` (a
  `wallRun` of log posts and dark-oak planks), `sable-reeds` (a `cell` fabric of grass/dirt/gravel, rim and
  wall both switched off — the open lane reads as unbuilt scrub, not as a plateau with an edge),
  `silt-flat` (the frontline legs, held level), `marsh-hold` (spawn, team-tinted clay wall). Rim is `void`
  on every grown surface and `boundary` only on the two built platforms (spawn, stockade), following the
  same rule Map 1 used.
- **A `water` prop cut into the hub's own hole**, a natural-form pool with a Voronoi gravel/dirt bank,
  authored once and fanned to both teams — the one prop type Map 1 didn't use.
- **Two room styles**: `reed-cage` (the wool shell — a gambrel roof, log posts, open unglaze windows) and
  `spawn-hold` (a hipped, deeper-eaved fortress hall). Both written for this map; neither is `corvid-hollow`'s.

## What I got wrong, once I found out

**A buffer drawn inside a generating piece's own rectangle is inert, and I designed the hub's hole that
way on the first pass.** `plan.md` states this outright — "A buffer over a generating piece is inert, so
it can declare a void but never destroy ground" — and I had read it before drawing the plan, then drew
`hub-hole` fully inside `hub-ring`'s rect anyway, because a plan piece can only be a rectangle and I was
thinking of "draw the ring" as "draw the square, then poke a hole in it" rather than "a plan can't draw a
ring at all; the ring is a sketch-level fact." The compile gave no error and no warning — the buffer is
legal, it simply does nothing — so the first sketch came back with a solid hub and no second route across
it. Caught by comparing the compiled shape list against what I'd drawn (the hub's outline had no notch in
it) before ever building a world. Fixed by cutting the hole as an explicit `subtract` shape in the layout,
the same mechanism `corvid-hollow`'s moat already used.

**A CTW plan with no declared build zone refuses every wool, for a reason that has nothing to do with
whether the wool is reachable.** I read the SP1 refusal message — "only reachable through a spawn piece" —
and first suspected my interface graph, since that is what the sentence describes. `/plan/inspect`'s
interface list showed every connection I expected; the actual cause was that `PlanValidator`'s frontline
set is computed from `plan.BuildZones` alone (`ComputeFrontline`, `ContactGraph.cs`), and I had declared
none. A `zones` entry with no `kind` was the fix, and it does double duty — it is also the buildable mid
band the late-game sky bridge needs (`match-flow.md` §4.4–4.6), which I would have had to add anyway. I
record this as **mistaken** rather than **missing**: the mechanism is documented (`plan.md`'s zones section
states a build zone "is what the gap-connectivity derivation reads"), I had simply not connected that a
zone's second, unstated job is answering the SP1 walk.

**The board's two mirrored halves did not actually touch, and nothing caught it until I asked why every
wool was unreachable from the opposing spawn.** Before extending `hub-ring` to `z=0`, `plan/evaluate`
answered `wool on 'wool-a' (team 1) is unreachable from team 0's spawn` for all four wools — a real,
correct refusal, not a false one like the two above. I had drawn the hub short of the axis out of habit
(most of my other pieces stop a cell or two shy of the true edge for margin) without checking that *this*
edge was the one piece whose whole job was to be the seam.

## Findings, with coordinates

| # | What | Where | Verdict |
|---|---|---|---|
| 1 | A `buffer` piece drawn inside a generating piece's own rect compiles clean and produces no void | first `hub-hole` attempt, compiled shape list showed no notch in `hub`'s outline | mistaken — documented in `plan.md`'s Pieces section, I mis-applied it |
| 2 | `PlanValidator`'s SP1 frontline set comes from declared build zones, not from role or adjacency | `sable-marsh.plan.json` first draft, no `zones` key, refused all 4 wools with SP1 | mistaken — the zones section of `plan.md` documents what a zone is for; the SP1 dependency specifically wasn't stated anywhere I found, so this sits at the boundary between mistaken and unreachable |
| 3 | Two mirrored piece edges must be drawn to the symmetry axis or the board is two unconnected halves | `hub-ring` first draft, `z` stopping at `-2` instead of `0`; evaluator answered "unreachable from team 1/0's spawn" for every wool | mistaken — my own authoring error, correctly refused by the compiler |
| 4 | A walled wool room reads as an isolated traversability marker (foot-level), an open one does not | `renders/06-traversability.png`: 2 isolated of 4 markers, both the `stockade`-walled lane's images | confirmed, matches the documented `FINDINGS.md`/`sonnet-run1` precedent — a wall meant to be built over, not a fault |

## Open gameplay question

**Is giving one team's own two wools different defensive character (one walled, one open) a good CTW
shape, or does it just make one wool the "real" objective and the other a formality?** `approaches.md`
says approaches should differ from each other; it says nothing about whether a team's *own* pair of
objectives should differ in defensibility. I built it this way because a single repeated wool room reads
as one objective twice rather than two, and the corpus number `capabilities.md` cites (55% of destroy
maps carry exactly one goal a team, most CTW boards carry one or two wools) doesn't settle whether two
wools *of the same kind* is the norm. Decided as a design choice, not derived.

## Reproducing

```
POST   /api/plan                        {"name": "Sable Marsh"}
PUT    /api/map/sable-marsh/plan        specs/sable-marsh/sable-marsh.plan.json
PUT    /api/map/sable-marsh/sketch      specs/sable-marsh/sable-marsh.layout.json
POST   /api/map/sable-marsh/sketch/finish
PUT    /api/map/sable-marsh/intent/from-plan   specs/sable-marsh/sable-marsh.intent.json
GET    /api/map/sable-marsh/export
```
