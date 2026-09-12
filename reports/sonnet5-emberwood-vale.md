# Report — sonnet5-emberwood-vale

## What I set out to build

A CTW board, `sonnet5-emberwood-vale`: two hamlets at opposite ends of an autumn forest clearing, each
keeping its wool at a shrine behind the village, with the wood between them the only way across. The
concrete plan, decided before any API call: a timber hamlet (spawn hall + one hand-placed cottage) split
by a village-green void; a small garden island cut off from the main approach and rejoined by a hand-built
footbridge; a shared forest clearing at the board's centre, itself split by a ten-block brook (void) that
every crossing must ford; and a rougher, west-flank trail as the wool's second, harder route. Three
themes only — forest floor, hamlet dooryard, shrine accent — and two timber house styles differing by a
roof swap and a repaint.

## What I could not say

Nothing in this build turned out to be a genuine capability gap. Two things looked at first like they
might be, and both were checked against `GET /api/openapi/v1.json` and the live schema before being
treated as anything:

- **"Can a shape state its own accent material without a fourth theme?"** — not missing. `SketchShape.material`
  (confirmed on the live schema, `TerrainMaterial`-shaped) does exactly this, which is how the leaf-litter
  patch and the garden footbridge are painted without adding a theme to the registry.
- **"Does a spawn/wool room's own paint reach the board?"** — not a gap either, but a documented,
  measured limitation: `GENERATION-NOTES.md`'s "a spawn shape's interior is never painted by its theme"
  is real (confirmed by reading the compiled layout — `spawn-red` and `wool-red-red` both carry a `role`
  field, and the theming pass explicitly skips any shape with one). The fix the same document implies —
  an ordinary `add` patch at the ground's own height, themed, laid over and around the pad — is what
  `dooryard-w`/`dooryard-e` and `shrine-yard` are.

One thing I did not test and cannot report either way: whether a `wools[]` marker can ride a plain
`role: "piece"` piece (a true freestanding shrine stamp, no auto-room) rather than a `wool-room` piece.
`approaches.md` says this is legitimate design ("a shrine on the concourse... is authoring something
legitimate"), but I built the shrine as a `wool-room` piece styled to look like a shrine hut rather than
trying the freestanding form, so I can only say it is untested from here — not missing, not confirmed.

## What I got wrong, and why it looked right

- **I assumed a window's `hostBlock` had to name the wall it sits in.** `WINDOW_TIMBER` first stated
  `hostBlock: 5, hostData: 1` (the wall's own Spruce Planks band), on the reasoning that a window frame
  should be cut from its host wall. `HS4` refused it: *"a window whose block and whose host disagree"* —
  the rule is that a window's own **two** blocks (its pane and whatever else it states) must agree with
  each other, not with the wall. It looked right because "cut a pane into a plank wall" is a completely
  ordinary sentence about a real window; the document's field just doesn't mean that. Fixed by leaving
  `hostBlock: -1` (cut wherever one fits).
- **I wrote the wall/fill `cell` patterns before giving them a `rise`, on the same call signature I'd
  already used correctly for the surface bucket.** `PT4` caught it (a plane-sampled field on a
  wall/fill bucket paints one block up the whole column). It looked right because the *surface* bucket
  genuinely doesn't need one — only a few blocks deep, a vertical-stripe artifact never becomes visible —
  so the working code for one bucket was a false model for the other two.
- **I painted the leaf-litter patch with a bare `cell` pick as the shape's whole `material`.** `PT1`
  named it exactly: podzol surfaces one course and this is a full-depth "fill"-shaped field. It looked
  right because the patch is visually thin (`base_height: 1`) and I read that as making the "surfacing
  block buried" concern moot; the validator reads the *bucket role* a plain `material` plays, not the
  shape's own stated depth.
- **I discovered the spawn/wool doors by decline, several drive cycles in, when the compiled document
  had already said them on the first compile.** `POST /plan/compile`'s own output carries a `doors` field
  on every role-tagged spawn/wool shape (`spawn-red: ["+x","+z"]`, `wool-red-red: ["+z"]`) — I only
  checked it after already having placed dressing that DR-KEEP declined, and moved props by re-reading
  the decline coordinates rather than the field that would have told me outright. Worth stating plainly:
  the answer was in the first `plan/compile` response the whole time.

## What worked first time

- The plan tier's own refusals were exact and actionable every time something was wrong: `PL12` when the
  shared clearing was first drawn as a non-fanned on-axis piece touching mirrored land (fixed by
  splitting it into a normal fanned piece either side of the axis instead); `WX3`'s marker-parity check;
  `ST9`/`ST10`'s footprint and protection-region caps, both of which named the exact offending rectangle.
- `POST /plan/room` handed back the precise `at`/`footprint`/`iron` numbers for both the spawn hall and
  the shrine on the first ask once the pieces were sized to fit `ST10` — no disagreement between the
  seeded rectangle and what the export would have defaulted to.
- The timber house recipe itself — the laid-log course under a two-species checker under a plank
  infill, corner posts in log, beams enabled, footing left unset — built and stamped correctly the
  moment the two material refusals (`HS4`, `PT4`) were fixed. Nothing about the recipe's own shape needed
  a second pass.
- `plan/evaluate`'s `G8` fill-ratio band caught a genuinely too-solid first draft (0.67 against a
  [0.201, 0.542] band) and the fix that brought it in band — cutting the shared clearing down to a
  ten-block-wide brook rather than a solid lawn — is also the fix that gave the board its central void
  instrument. The gate and the design were pointing at the same thing.
- The export gate opened clean on the first fully-dressed drive once the plan-tier refusals were
  resolved; every later iteration was dressing declines (`DR-KEEP`, `DR-ROAD`, `DR-CLAIM`), never a
  reopened plan or layout refusal.

## Open gameplay questions decided without an oracle

- **The own-spawn-to-own-wool ratio reads 0.17** (defender 33 blocks, attacker 193). `approaches.md`
  states this shape — spawn remote, the defended goal a short walk forward — as correct for a *destroy*
  board's monument, on the reasoning that a team defends what stands close to it. There is no equivalent
  stated ruling for a *capture* board's own wool specifically. I decided to keep the same shape (wool
  deep and close to its own spawn) rather than pull it forward toward parity with the enemy's approach
  distance, on the reading that "a wool has to be fetched and brought home, so it belongs behind"
  (`approaches.md`, stated of the core/wool distinction generally) argues the same way. Recorded here as
  a decision an author should confirm rather than a settled rule.
- **Whether the flank trail is actually used as a second route, or ignored because the main street is
  wide and direct enough** (`match-flow.md` §6.9's own finding, that an alternative is taken only when it
  costs little) is not answerable from the plan alone — it is exactly the kind of claim that document
  says needs recorded play. The plan makes the route genuinely available (its own share of the crossing
  frontage, its own denser wood, its own worn path) without being able to say whether it will be chosen.
