# Sonnet 5 — run 4

## The four briefs, announced

1. **§2 Compass Yard** — CTW, four teams under `rot_90`. Key `compass`. Never attempted before this run.
2. **§1 Caravanserai** — DTM, desert canyon. Key `caravanserai`. Never attempted before this run.
3. **§7 Gantry Quarter** — DTC, industrial yard, hand-authored building grid. Key `gantry`.
4. **§8 Reedcut** — CTW, worked peat lowland, legibility by height not colour. Key `reedcut`.

All four built, exported and rendered. `maps/sonnet-<key>/`, `specs/sonnet-<key>/` and
`review/sonnet-<key>.md` exist for all four. Every board's `traversability` endpoint reports
`connected: true` on the exported world.

| Board | Slug | `<gamemode>` | Extent (blocks) | Brief said |
|---|---|---|---|---|
| Compass Yard | `four-winds-compound` | `ctw` | 200×200 | "about 170×170" |
| Caravanserai | `redsand-caravanserai` | `dtm` | 100×190 | "about 90×190" |
| Gantry Quarter | `gantry-quarter-works` | `dtc` | 120×230 | "about 120×160" |
| Reedcut | `reedcut-levels` | `ctw` | 130×170 | "about 160×140" |

---

## What I could not say

Each item: what I wanted, the exact endpoint or field I looked for, and whether it is **missing from the
system** or **out of reach from where I was standing**.

**1. Whether `LN1`'s "lane width" measures the piece I think it measures — out of reach.** Building
Compass Yard's wool bay, `LN1` (`lane-width`) refused at a fixed **25 blocks** across five different
edits of `wool-room`'s and `wool-approach`'s own width, depth and offset — none of which moved the
reported number by even one block, including edits that should have changed a raw rectangle's own
dimension. `PgmStudio.Pgm/Derive/BoardDeriver.cs` (`ShapeClassifier.ClassifyOpen`, called once per wool
against the **whole team-0 unit's filled cell set**, not the wool piece alone) is the code, and I read it,
but a flood-fill classifier that walks the entire authored terrain from the room outward to "the first
junction" is not something I could hand-trace to the exact 25 in the time this run had. I worked around it
by removing the geometry that triggered it (a narrower wool room, matching the piece's own width to its
neighbours) rather than understanding the number, which is exactly the "workaround, not an answer" this
brief warns against. **Out of reach**, not missing — the term computes something, I just could not read
off what.

**2. `POST /room-styles/preview-snapshot?format=png&view=plan` answers a blank grey swatch — likely
missing/broken, not out of reach.** `GENERATION-NOTES` §17 says this route was fixed this session and
"now answers raw PNG." It does — 2 colours, 72×72, no building drawn — on **every** style I tried,
including an unmodified shipped preset (`HousePresets.Desert`, id 2) pulled straight from
`GET /room-styles/2/json` with nothing edited. The `section` view on the same endpoint, same body, works
correctly and shows a real cross-section. I could not find a wrapper shape that changed this (tried the
bare style and `{"style": ...}`), and `isometric`/`cutaway` correctly refuse by name on the same route, so
the endpoint is alive and reads `view` — only `plan` specifically renders nothing. I used `section` and the
non-PNG SVG-in-JSON default (`GET`, no query) as substitutes throughout this run; AD-S6 and reviewer C14 ask
for a plan view specifically and I could not produce one that shows anything.

**3. A live, per-team traversability read exists and is not named in `plan.md`'s or `sketch.md`'s API
tables — likely a documentation gap, not a missing capability.** `GET /map/{slug}/traversability`
(`AnalysisEndpoints.cs`) answers the exact `Traversability.Check` the export gate runs, including the
per-team `isolated[].for` breakdown `EX1`'s message summarises into one sentence — and it answers on a map
that has **not yet passed export**, which is precisely the situation an author needs it in. Neither tool
document's endpoint table lists it (`configure.md` names `GET /map/{slug}/xml`'s and `/export`'s refusal
codes but not this route as a way to get the same information pre-emptively). Finding it was `grep -rln
Isolated src/PgmStudio.Api` after `EX1` sent me looking for the export gate's own logic; an agent without
source access would only ever see the 409's summary sentence and the twelve names it lists, never the
per-team cause table this endpoint answers directly.

**4. `GET /map/{slug}/coverage`, `wool-availability`, `kit-reach`, `monument-obstruction` and
`wool-sources-in-region` all exist in `AnalysisEndpoints.cs` and none is documented in `sketch.md`,
`configure.md` or `capabilities.md` — likely a documentation gap.** I used `traversability` (above) and
did not have time to drive the rest; I list them because they answer questions this run asked by hand
(`coverage` is exactly `AD-L6`'s "dead ground" read, `docs/tools/sketch.md` cites it by name without an
endpoint) and a future run would save a build cycle knowing they are live.

**5. Whether `CT12`'s 15–40 gap applies to Compass Yard's arm-to-arm pairing or its arm-to-plaza
pairing — genuinely out of reach, not a defect.** `POST /plan/inspect`'s `islandGaps` only ever reports
one pair for a four-team `rot_90` board: `{"piecesA": ["plaza"], "piecesB": [...team pieces...]}`. The four
rotated images of the team unit are **one mirrored island**, not four separate ones, so there is no
`islandGaps` entry for "one arm vs. its rotational neighbour" — that distance exists only as geometry I
computed by hand from the piece rects (30 blocks, direct). I could not get the deriver to answer that
specific question and did not invent a passing number for it; see the review's open question.

---

## What I got wrong, and found out

**The four-team `EX1` refusal looked like an order-4 bug and was my own topology.** Three complete builds
of Compass Yard refused at export with *"12 objective(s) sit behind ground an enter rule bars the attacking
team from,"* naming every cross-team wool for every team — which reads exactly like "four teams broke
something two teams never trip." I spent real time suspecting `WoolGenerator`'s per-team `not-<owner>`
filter, a team-id string mismatch, and a `RegionMask` resolution failure on `union`-typed regions, checking
each against the live DB (`apply_rule`, `region`, `filter` tables) before finding the actual cause: my
first three drafts routed a team's own spawn to the rest of the board **through** its own wool room,
which the map correctly, by design, bars every team from entering. The fix (`wool-room-flank-w`/`-e`,
named with the room's own id prefix per `GENERATION-NOTES` §15) is two renamed ground pieces, not a
studio change. I record this at length in the review because the failure mode is worth knowing before it
costs someone else the same three build cycles: **a wool room can never be the only way through a team's
own land**, on any team count, and nothing before `GET /map/{slug}/traversability` or the export's `EX1`
says so.

**I initially wrote `relief_scope: "hold"` where the geometry wanted `"exclude"`, on both Caravanserai and
Reedcut.** `sketch.md` is unambiguous that `hold` pins a shape's cells flat at one level while `exclude`
removes them from the field entirely, and I had read it — but under time pressure I defaulted to `hold`
for "keep this built thing flat" without checking whether the shape's *neighbours* were meant to ramp up to
meet it (which `hold` invites) or fall cleanly away from it (which `exclude` gives). The Reedcut brief
literally names `hold` for its built shapes; I built `exclude` on purpose once I re-read the mechanism
against what a stepped plan tier actually wants, and I say so in that review rather than silently matching
the brief's word over the tool's own documented behaviour.

**I guessed `theme.wall` could hold a `wallRun`/pattern object as easily as a bare material and then did
not use one anywhere**, out of time rather than a finding — `capabilities.md`'s "the wall bucket takes a
pattern tied to what the wall is" (AD-R3) went unanswered on all four boards; every wall bucket in this
run is a bare `solid` or `layered` material. Recorded as scope cut under time pressure, not as something
the system refused.

---

## What worked first time

- **`tools/drive.py`'s ordering** — evaluate/inspect before a map row, compile, patch, `sketch/from-plan`,
  `relief/read`, finish, intent, dressing declines, export — never needed correcting once understood; every
  refusal it printed was real and each one's fix was in the document it named.
- **Forking a shipped preset by proportion, not by material.** `HousePresets.Desert` copied verbatim for
  Caravanserai's two buildings, `Workshop` and `Counting House` repainted only in wall/roof material for
  Compass Yard and Gantry Quarter — every fork built and rendered correctly the first time it was tried,
  including the `foundation.footing: null` (`Sill = Air`) idiom, which needed no correction anywhere it was
  carried across.
- **`teamTint` for the per-quadrant accent on Compass Yard.** One theme, `{"kind": "teamTint", "blockId":
  159, "neutral": <clay>}`, painted all four wool approaches in their own dye with no per-team authoring —
  confirmed directly in `--surface`.
- **The `rot_90` pipeline itself.** Four teams, four spawns, four wool rooms, twelve `<wool>` elements (one
  per attacker/defender pair), the red/blue/yellow/green palette — all correct on the first successful
  compile, once the topology (not the symmetry machinery) was fixed. Nothing about order 4 needed different
  handling from order 2 anywhere except the `EX1` case above, which was my own geometry.
- **`GET /map/{slug}/traversability`**, once found, answered every "is this actually connected" question
  in one call, on a map that had not yet built successfully — the single most useful instrument this run
  used that is not named in a tool document.

---

## Open gameplay questions, and what I decided

**Compass Yard — is a "pinwheel" (each arm centred on its own axis, widening outward) a faithful reading
of "each owning one quadrant of a walled yard"?** A literal square quadrant sharing a straight edge with
its two neighbours is not reachable with rectangle-based pieces without either the quadrants touching
directly (which fuses them into one island and removes the four separate gaps the brief explicitly asks
for) or a cut the plan-piece system does not offer at cell resolution. I built the pinwheel — each arm
provably non-overlapping with its own 90°-rotated image because its half-width never exceeds its near-edge
distance from the origin — and recorded the reasoning in the review rather than asserting it is the only
correct shape.

**Gantry Quarter — does "one on a raised gantry deck, one in a sunk pit" mean two cores per team, or one
core's two faces?** I read it as two cores, because the brief's own separation numbers ("keep 35 minimum
between the goals and aim at 70") are `O1`'s same-team spacing language verbatim, and a single goal has no
second goal to be 70 blocks from. `approaches.md` does not address multi-core boards. Built two per team,
75 blocks apart, `GO1` in band on both (3.46, 3.83); recorded as an open question rather than asserted as
the only reading.

**Reedcut — does a wool that already has a walled land approach need a water lane at all, or does adding
one risk being decorative rather than earned?** `approaches.md`'s rule is negative (a lane can never be the
*only* connection) rather than positive (when one is warranted), and this wool is not especially remote.
Built the lane because the brief names Reedcut as the one board in the set where it is legitimate, and
recorded the softer judgement — whether the wool should have been tucked further back specifically to give
the lane a reason — as open rather than settled.

---

## Coordinates for the geometric claims above

| Claim | Board | Coordinate | What is there |
|---|---|---|---|
| `EX1` root cause: wool room inline on the only route out | Compass Yard (pre-fix draft) | red spawn `(0, y13, 90)`; red wool room `x -5..5, z 55..65` | the room's footprint sat directly between the spawn and the hub with no other route |
| The fix: dead-end room, bypass flanks | Compass Yard (shipped) | `wool-room-flank-w`/`-e`, `x -40..-10` / `x 10..40`, `z 55..80` | ground pieces carrying the spine's width past the room |
| `LN1`'s fixed 25-block reading | Compass Yard (dry-run only, not shipped) | wool-room piece varied `[2,10,1,1]` through `[2,10,4,4]` | reported lane-width stayed 25 across every variant tested |
| End Stone confined to the caravanserai | Caravanserai | `--column (10, 47)` | `End Stone y14..16`; no End Stone elsewhere in a spot-check off the yard |
| Core separation | Gantry Quarter | markers `(-37.5, y?, 80)` and `(37.5, y?, 80)` | 75 blocks apart, straight-line |
| Grass confined to the top course | Reedcut | `reed-lowland.surface` stack | `Grass` thickness 1 (band 1 of 4), Coarse Dirt/Podzol/Brown Clay beneath |

## Defects believed to be in the studio, not this run's authoring

1. `POST /room-styles/preview-snapshot?format=png&view=plan` answers a blank grey PNG for every style
   tried, shipped presets included, while `view=section` on the same route/body works. (Item 2 above.)
2. `docs/tools/sketch.md`/`configure.md` do not list `GET /map/{slug}/traversability`,
   `/coverage`, `/wool-availability`, `/kit-reach`, `/monument-obstruction` or
   `/wool-sources-in-region`, all of which are live, anonymous, and answer real authoring questions before
   export. (Items 3–4 above.)
