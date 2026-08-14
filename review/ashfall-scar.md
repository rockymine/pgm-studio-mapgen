# Ashfall Scar — Map 3, DTC + DTM

`rot_180`, 16 players, 250×190. My own design, deliberately not a variation on Map 1: two goals of
different kinds set against each other, a crossable ford instead of a permanent moat, relief marks
instead of erected shapes for the elevation.

## What it is

A volcanic ash field. Spawn and a village sit at the rear on ashen/ember ground; forward of them, the
yard carries both goals **against each other**, per `approaches.md`'s "several goals placed against each
other rather than scattered": a destroyable stands forward and exposed on a low relief-pushed mound near
the mid line, a core sits back in a shallow relief-carved crater closer to the village — one goal costs an
attacker more distance, the other costs more digging (`digDepth: 3`, `leak 9 − float 6`). West of the yard
a cinderwood forest closes that flank with cover; east of it a ford — a genuine void cut, twenty blocks
across, that this map declares **buildable** rather than permanent — forces a bridge before it can be
crossed at all, the "river or a drop" approach `approaches.md` names as its own thing from a void hole.

## How it plays

- **A crossable void is a different decision from a permanent one, and this map makes the other choice
  from Map 1's.** `approaches.md`: "the same gap with a build region covering it is crossable from the
  first minute, at the price of the time and material a bridge costs and the visibility of building one."
  The ford is exactly that price — an attacker can commit to it from tick one, but building a bridge in
  the open, next to a flank with sparse cover, is a visible act a defender can watch for.
- **Two goals of different depth read as two different tasks, not one goal twice.** The forward
  destroyable is the cheap, fast target; the back core costs an actual dig. `match-flow.md`'s corpus
  reading (one destroyable + one core is the ordinary combined destroy board) is the shape here, and the
  two are close enough — both inside the yard — that a defender holding the yard defends both, while an
  attacker has to choose which fight to start.
- **Forest and ford are both flank features, and they differ in kind rather than degree**, matching
  Map 1's forest/hill pair with a different second half: cover on one side, a hard chokepoint on the
  other, instead of cover against elevation.

## Techniques used

- **Relief marks instead of erected shapes for the goals' own ground**, the third way of shaping elevation
  this run used (Map 1: `height_mode`/`anchor_heights`; Map 2: a subtract ring plus a push; this map: an
  `area` mark and a `push` on ordinary ground). The core's crater is an `area` mark held at `h: 7` against
  a `base` of 9; the destroyable's mound is a `push` of `amount: 2` over the same field. Both are
  constraints/lifts on the same island relief rather than shapes standing apart from it, which is the
  right tool when the landform is meant to read as *grown into* the yard rather than *placed on* it.
- **A build zone declared over a void is what makes it a ford rather than a moat.** `ford-void` (a
  `subtract` rectangle, 20×20) sits inside the plan's `ford` zone (`build.areas` after compile), so
  `BuildGenerator` wires `not-build-area` around everything *except* it — the void is permanent everywhere
  on the board but there. I first also added a standalone `build.voidEnforcement` with no exclusions,
  copying Map 1's pattern without checking whether it applied here — see *What I got wrong*.
- **Per-shape theming, five themes**: `ashfield` (yard, a `noise` field of dirt/stone/andesite/gravel —
  scorched ground, deliberately grassless), `cinderwood` (forest, a `cell` fabric in the same burnt
  palette), `quench-flat` (the ford's banks), `ember-row` (village, `cell`-in-`layered` again), `cinder-hold`
  (spawn, team-tinted nether brick). Rim is `boundary` on the three built tiers and `void` on the two grown
  ones, the same rule as the other two maps.
- **A Bézier curve on the forest's own outer edge**, the closing edge of the loop (`vertex[3]`'s `out`
  paired with `vertex[0]`'s `in`) — the edge-pair convention fixed after Map 1's mistake, applied correctly
  here without a second round of column-probing needed to catch it.
- **One house style, `cottage`, in ember-brick and dark planks**, ten instances on a shared street
  frontage — deliberately simpler than the other two maps' multi-style villages, because this map's second
  point of visual interest is the crater/mound pair at its centre rather than the settlement.

## What I got wrong, once I found out

**I copied Map 1's `voidEnforcement` fix onto a map where it was actively wrong, without re-deriving
whether it applied.** Map 1 has no declared `build.areas` at all, so `voidEnforcement` was the only way to
make its moat permanent. Ashfall Scar already declares a `build.areas` rectangle over the ford, and
`BuildGenerator.ApplyBuildAreas` already wires `block=no-void` over everything *outside* that rectangle —
which is exactly the permanent-except-the-ford behaviour the design wants. Adding `voidEnforcement` with
empty `exclusions` on top of that stamps a **second**, unconditional `block-place=deny(void)` over
`everywhere`, with no carve-out for the declared build area, so the ford would have been just as
unbridgeable as the rest of the void — the opposite of the design. Caught by reading the exported
`map.xml` directly rather than trusting the intent JSON: `<everywhere id="void-enforcement-area"/>` with
no child exclusions, feeding an `apply block-place="deny(void)"` with nothing scoping it away from the
ford. Removing the standalone `voidEnforcement` and relying on `build.areas` alone gave the correct
document — one `no-void` rule, scoped to `not-build-area`, exactly as `BuildGenerator`'s own docstring
describes the two knobs as *independent* rather than *additive-safe by default*. This is the sharpest
instance in the whole run of a fix helping on one map and having to be actively un-applied on the next
rather than becoming a reflex.

## Findings, with coordinates

| # | What | Where | Verdict |
|---|---|---|---|
| 1 | `build.voidEnforcement` and `build.areas` are independent and do not compose safely when both are set with empty exclusions — the standalone rule has no knowledge of the area rectangle | first export's `map.xml`: `<everywhere id="void-enforcement-area"/>` with no exclusions, denying block-place over the whole map including the declared `build-area` rectangles | mistaken — the docstring on `BuildIntent.VoidEnforcement` states the two are independent, which I read as "safe to combine" rather than "must be reconciled by the author" |
| 2 | A core's `digDepth` (`leak − float`) is computed and carried on the compiled intent, not left for the author to derive | `as-compile.json` → `intent.cores[0].digDepth: 3` for `float: 6, leak: 9` | confirmed working, not previously verified in this run |
| 3 | The ford reads as bridged rather than isolated once the standalone enforcement is removed | `renders/06-traversability.png`: 4/4 markers connected, "800 bridged over void" | confirmed working as designed |

## Open gameplay question

**Should a core and a destroyable on one board be roughly equal in cost to break, or is a cheap forward
goal and an expensive back one the better shape?** This is the same question `opus-run1.md` recorded on
Quillon Foundry, and I made the same choice for the same reason — a forward destroyable that falls fast
and a back core that costs real digging reads as two different fights rather than one fight twice — but
`approaches.md` does not settle which is correct, only that goals should be placed against each other
rather than scattered. Recorded as a decision, not a derivation.

## Reproducing

```
POST   /api/plan                          {"name": "Ashfall Scar"}
PUT    /api/map/ashfall-scar/plan         specs/ashfall-scar/ashfall-scar.plan.json
PUT    /api/map/ashfall-scar/sketch       specs/ashfall-scar/ashfall-scar.layout.json
POST   /api/map/ashfall-scar/sketch/finish
PUT    /api/map/ashfall-scar/intent/from-plan   specs/ashfall-scar/ashfall-scar.intent.json
GET    /api/map/ashfall-scar/export
```
