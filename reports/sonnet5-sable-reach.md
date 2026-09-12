# Report — sonnet5-sable-reach

## What I set out to build

A capture-the-wool board, `sonnet5-sable-reach`: two rival trading posts facing each other across a
tidal river mouth, each holding its wool in a dockside warehouse behind a seawall, with the mudflats
and a single low bridge deciding who controls the crossing. Specifically, past the composer's three
known gaps: each team's site is **two landmasses** (a main settlement island and a flanking mudbank/dock
skerry) joined by a **short build zone**; a **build zone sits inside the team's own site** (a plaza among
the warehouses, not just at the mid interface); the crossing is a **real route** — one permanent, `made`,
`keepClear` bridge as the primary chokepoint, and a pair of shallow sand fords as the secondary route,
per WL8. Three themes only (shore/water, settlement, the skerry's own), an estuary shore graded sand-
then-mud, a dockside seawall with a diagonal pattern and a team-colour rim accent, two timber house
styles forked from one recipe, and the two path triads the brief names.

Driven end to end with `tools/drive.py`: `POST /plan/evaluate` → `valid: true`, `POST /map/from-
documents` → 200, export gate **OPEN**, dressing pass **0 declines** on the final build (41 props
placed). `maps/sonnet5-sable-reach/`, `specs/sonnet5-sable-reach/` (plan, finish, layout, intent,
`build-spec.py`, 49 renders), `review/sonnet5-sable-reach.md` and this report are all in place.

## What I could not say

**`roomStyles.cage` — mistaken, not missing.** `tools/README.md`'s table states `roomStyles` as
`{"cage": …, "spawn": …}`. Posting that key built the wool room in the studio's default shell rather than
mine, with a silent `RQ3` (`layout.roomStyles.cage` unread) as the only sign. `GET
/api/openapi/v1.json`'s `SketchRoomStylesDto` names the field `wool`, not `cage`, and that fixed it. The
capability (a house style for the wool room) is fully present; the doc's own key name is stale. I did
not check whether other specs in this repo carry the same stale key.

**`meta.authors` via `POST /map/from-documents` — out of reach from where `drive.py` stands, not
missing.** The endpoint's own schema (`MapFromDocumentsRequest.authors`) documents the field, applied
*after* the intent projection "for the reason projection exists" — and posting `authors: [{"name": "Sonnet
5"}]` drew no `RQ3`. The stored intent's `meta.authors` still read back `[]`, and `EX6` kept complaining
that the observer's authors board was blank. `PATCH /api/map/{slug}/metadata` with the same value fixed
it immediately and a re-export shows `<author>Sonnet 5</author>` in `map.xml`. So the capability exists
and is reachable — just not through the one call `drive.py` documents as sufficient. I did not read the
server source to say *why* the `from-documents` path drops it; I only confirmed the second path works and
used it.

**Whether `SK24` (theme XOR material) is stated anywhere before the refusal — checked and it is not,
quite.** I looked for it in `docs/generator/model.md`'s theme section before hitting the refusal and
found only "a `material` is one material over the shape's whole span," which reads as an addition to a
theme rather than a replacement of one. The refusal itself is unambiguous once raised (`SK24`'s message
says the material is what paints and the theme is read by nothing), so this is a documentation gap I
found by hitting it rather than a missing capability.

## What I got wrong, and why it looked right

**I keyed `themeById` by plan piece id, and none of them existed.** Eight of my nine `themeById` keys
(`quay`, `warehouse`, `back-w`, …) drew `!` warnings naming a shape list I had not seen —
`back-e-12`, `back-e-9`, `skerry-7`, `spawn-red`, `wool-red-red`, and their `-building` twins. It looked
right because the plan's own piece ids are meaningful names I chose; it was wrong because abutting
equal-height pieces fuse into one polygon at compile, named for the fused component rather than for any
one piece, and a spawn or wool piece compiles to its own separate shape entirely. `AUTHORING-BRIEF.md`
says outright to "read the SHAPE IDS here and key the finish on them" — I wrote the finish before reading
that compile output, and paid for it in a rebuild.

**I made the mid-band zone span the whole width of both teams' quays, and `FR6` refused it.** A CTW
frontline is capped at 16 cells (80 blocks); a destroy board's is not, and I had just been reading
`basalt-reach`'s destroy board (no cap at all) when I sized this one's zone at the full 20-cell quay
width. Narrowing the zone to dock only the centre of the quay — leaving its outer flanks facing plain,
un-zoned void — fixed `FR6` and, as a second effect I had not planned for, also brought the channel's
`CT12` strait reading down from 50 blocks (outside the 15–40 band) to 30 (inside it), because a narrower
zone let me pull the quay pieces closer to the axis without widening the docking face past the cap.

**I nearly designed a ford that could never connect anything.** My first ford spanned the full channel
depth at a fixed x range near the skerries — but under `rot_180` a team's own flank sits at *positive* x
for one side and *negative* x for the other, so a single straight shape spanning the whole depth at one
x band dead-ends into open water on its mirrored half rather than reaching the other team's landmass.
Caught before posting anything, by tracing where the auto-fanned copy would actually land rather than
assuming symmetry made the geometry sort itself out. The fix — ford within the shared quay's own
symmetric x-range, so both the authored shape and its fan independently span the full depth — is in the
finish now.

## What worked first time

The plan's piece/zone arrangement, once `tools/board.py`'s grid caught two one-cell gaps between spawn
and wool (`GENERATION-NOTES.md`'s whole point about relations between rectangles, not the rectangles
themselves) — after that the compile, store and export ran clean apart from the issues above. The timber
house fork (`timber_style(wall_extent, roof_form, ...)` producing both the warehouse and the cottage from
one function) built and stamped both styles correctly first time, including the `laidLog` verge and the
two-species checker course. `POST /plan/inspect`'s `CT12`/frontline readout was exactly the tool the
skill said it would be — the numbers it prints are what I fixed against, not a render.

## Open gameplay questions, decided without an oracle

**Two secondary fords instead of one.** The `rot_180` fan turns one authored ford shape into two —
one near each team's own skerry flank. I judged that a fair pair of crossings beats an asymmetric single
one and kept it, rather than fighting the fan to produce exactly one. `docs/gameplay/approaches.md` does
not say how many alternative routes a wool wants beyond "more than one" (WL8); I read the fan's own
consequence as the design rather than a defect.

**37.2% dead ground.** The flanking filler pieces that keep the rectangle contiguous around the wool
room and the back band read as mostly unused ground per `GET /coverage`. I added two short path spurs
into the worst of it rather than narrowing the pieces themselves, on the judgement that some backdrop
land around a defended wool room is normal rather than a fault — but I did not have a number to check
that judgement against, and a further pass would likely narrow the fillers instead.

**The un-ramped seawall.** Only a 12-block-wide stair grades the quay's 3-block rise to the town; the
rest of the 100-block frontage is a plain retaining wall. I read this as the point of a seawall — a
built town has one stair, not a beach — rather than a defect the relief solver should have smoothed. No
oracle confirms that reading; it is the shape a real dockside town has.
