# Report — sonnet5-talltimber-yard

## What I set out to build

A destroy board, one obsidian core per team, called the ledger. Two rival logging outfits each run a small
timber yard around a tall counting-house that holds their ledger-core, and the two yards face each other
across the felled ground between them. At most three house styles, all forks of shipped presets, varied by
wings and storeys rather than by unrelated designs; one tall multi-wing counting-house per team; one or two
small human-scale buildings; solid three-colour paths drawn before scenery; sparse street trees; a
build-zone-spanned void between the two yards, never solid land.

Slug `sonnet5-talltimber-yard`, built end to end with `tools/drive.py` from a `build-spec.py`, `--dry`-checked
against `GO1`/`GO3`/`GO4` before the first store, then driven, re-driven and inspected through the text
reads and renders until `06-claims.txt` read "declined 0" and every warning cleared.

## What I could not say

**A core literally inside a building's walls.** I checked `GET /api/openapi/v1.json` and
`docs/pgm/destroyables-and-cores.md`/`decoration.md` §3.1 before filing this: the mechanism exists (a core
takes no plan piece, and `float`/`leak` are ordinary knobs), but `OB19`'s dressing rule holds a building at
least ten blocks from a goal's own marker, unconditionally, and a building breaching that ring is declined
outright rather than shrunk. No footprint under the 192-block wing cap (`HP3`) can keep every wall of itself
ten blocks from its own centre. This is **not missing from the system** — cores and buildings are both fully
supported — it is a real geometric conflict between two rules that are each working as documented, and I
could not find a way to satisfy both. I resolved it by seating the ledger in a small clearing beside the
counting-house (twelve blocks off its nearest wall) rather than inside it, and I am recording the tension
rather than the workaround as the finding, since the brief itself anticipated this might not resolve
cleanly ("read the rule rather than guessing").

**Whether a paint-only `addShapes` patch should have needed `relief_scope: exclude`.** This one I got wrong
before I got it right, and it is worth separating the two. `GENERATION-NOTES.md`'s own table ("A paint patch
on solved ground is an ordinary one-course add, not an override") states that a plain `add`, `base_height: 1`
shape repaints solved ground without disturbing its height, and separately that `override: true` does the
same "only where a relief covers the cell." I tried both, at multiple sizes and with an unmistakable single
block, on my one relief-carrying group, and both painted zero cells — the census read 100% of the ground as
the map default regardless. `relief_scope: "exclude"` (which the notes describe as a way to make a shape's
*column* survive the solve untouched, not as a paint fix) is what actually worked, once I also matched its
`base_height` to the group's own solved height so it met the surrounding ground flush. I do not know whether
this is the current, correct behaviour and the notes are stale for this build (the pgm-board skill warns
`GENERATION-NOTES.md` is measured against a specific commit and can disagree with a running studio), or
whether I made an error the SK14 warning's own wording papered over. I am reporting the measurement rather
than a diagnosis of the C#.

## What I got wrong, and why it looked right

- **A road drawn straight from spawn to the ledger.** It looked right on the plan grid — one line, shortest
  path — and `DR-CROSS` named the actual fault at the dressing pass: the line ran through the counting-house
  and out the far side, which is "two dead ends at a building" rather than a road reaching a door. It looked
  right because nothing before the dressing pass reads a stroke against a building's footprint at all; the
  plan and the compile have no opinion about it.
- **Oak beams on a spruce-post hall.** I set the hall's decorative beams to oak for a visual accent before
  reading `HS4` closely, on the assumption a beam was independent of the wall studs. It refused at the store
  with the actual reason — a post and its beam ends are one timber frame — which is the same discipline the
  brief's own log-checker rule states for a different part of the wall.
- **A default 28×14 spawn footprint.** I assumed `WX1`'s inset default would simply fit inside `ST9`'s 20×20
  cap on a 30×20 piece; it does not, because the inset is one block per side, not enough to bring a 30-wide
  piece under 20. `POST /plan/evaluate`'s own `ST9` complaint caught it before a single block was built.

## What worked first time

- The three `GO` bands (`GO1` 3.76, `GO4` 46, `GO3` 139) all landed inside their authored ranges on the
  first `/plan/inspect`, because I solved the spawn/hall/core distances algebraically before drawing
  anything rather than placing them by eye and measuring after.
- The wing joint (hall + gambrel lean-to) previewed clean at `POST /terrain/prop-preview` on the first try —
  no `HJ*` refusal — because I sized the lean-to's own proportions (wider along the shared edge's
  perpendicular than along it) to tie its ridge into the hall rather than stating an explicit `ridge`
  override to force it.
- The void gap: stopping both team pieces six cells short of the axis and adding one `zones` rectangle over
  the gap produced exactly the intended `CT12` 30-block build-zone-spanned strait, with `voidEnforcement:
  true` correctly denying the rest of the board's edges to bridging, on the first drive.
- `06-claims.txt` read "placed 20, declined 0" on the drive that shipped — every house, both roads' spurs
  and all three trees seated without a single `DR-*` decline, which followed from checking each prop's
  distance to the core marker and to the road/building footprints by hand before authoring positions rather
  than placing by eye and fixing declines afterward.

## Open gameplay questions I decided without an oracle

- **The ledger's exact standing** (§ above): held beside the counting-house rather than inside it. I do not
  know whether the author would rather see the goal moved further from the building entirely (reading as
  "guarded by" rather than "kept at") or would accept the twelve-block clearance as close enough to satisfy
  the brief's intent.
- **`float: 5`, `leak: 6`** — a two-block dig requirement rather than the zero-dig default pairing
  (`float 6`, `leak 5`). I chose it so capturing the ledger costs a small excavation as well as breaking the
  casing; the corpus centre and the studio's own default both point at zero dig, so this is a deliberate
  departure rather than an oversight.
- **27.7% of the ground reads "dead"** in `GET …/coverage` — the open flanks of each yard, west and east of
  the buildings and the road, that no authored route crosses. I judged this as legitimate open yard rather
  than a fault to pave over, since GENERATION-NOTES' own worked example of a dead-ground fault (Wheal Hazel)
  is about a stepping-stone bottleneck rather than open flanking ground beside a settlement, and paving
  every corner would have contradicted the brief's "nothing is scattered" / clean-space-around-objectives
  guidance. I would want the author's read on whether this share is too high for a board this size.
- **`maxPlayers: 10`** — a modest-board guess with no stated corpus figure to check it against for a
  single-core two-team board this size.
