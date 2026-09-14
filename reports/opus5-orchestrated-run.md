# Twelve boards from three concurrent agents — the orchestrated run

## What authored these boards, and what did not

**Twelve boards were authored by three agents running at the same time against one studio, each given four
objective kinds and one ground family.** They did not author alone. An orchestrator set the environment up,
briefed them, corrected them twice while they worked, reviewed the finished boards and sent findings back.
That involvement is the first thing a reader needs, because the boards are not a clean measurement of what
an unaided run produces and nothing here should be read as one.

The division of labour was strict in one direction: **no agent ran a `git` command.** Three agents share one
working tree and a concurrent index is a corrupted one, so every commit was made by the orchestrator. What
each commit contains is still the agents' own bytes — the orchestrator changed no board file — and the commit
boundaries below are what separates authored work from anything done to it afterwards.

| commit | holds |
|---|---|
| `d7e56b6` | a mid-flight checkpoint taken against container loss |
| `832d270` | **the three runs as authored, interrupted at 28 minutes** |
| `8977643` | dustwath's world rebuilt from its own surviving documents |
| `5cc37fc` · `6d0eec2` · `c7ffb37` | birkmire; then redmarl, potsherd, flintwick, sparholt, basaltmere; then ochrepans |
| `88af9cb` | agent B's set complete, mirkholt, and seven reviews |
| `33b15ed` | re-drives of mirkholt and ochrepans |
| `68a57e1` | agent A's set complete |
| `ca8c946` | **agent C's set complete — all twelve boards as authored** |
| `1d24531` | this document |
| `07e13e4` | the agents' responses to review — see the correction below |
| `0267870` | agent B's report taking the coverage correction |

`ca8c946` is the provenance boundary. Everything to that point is agent output with nothing of the
orchestrator's in it. Anything after it is a response to review.

**One commit message is wrong, and the record is corrected here rather than by rewriting it.** `07e13e4`
says "Agents A and C answer the review". It in fact carries **all three** agents' responses, agent B's
included: B finished writing its files before that commit was made and its completion notice arrived after,
so a `git add -A` swept its work in under a message that does not name it. Grykefell's re-sited barn, its
turf shelves and flintwick's `sward` theme are all in `07e13e4` despite what it says. Nothing was lost and
no file is misattributed — only the message is — and a commit already pushed is left standing rather than
force-rewritten, because a corrected sentence in the record costs less than a rewritten history.

## The twelve boards

Four objective kinds across three ground families, one agent to a family.

| board | mode | agent | in one line |
|---|---|---|---|
| `opus5-redmarl` | CTW | A · arid | a red marl gully, each team's dyehouse on its own bank |
| `opus5-dustwath` | DTM | A · arid | a bleached dust-flat split by the bed of a river that has gone |
| `opus5-potsherd` | DTC | A · arid | a terracotta brickfield on a baked clay terrace |
| `opus5-ochrepans` | KotH | A · arid | an ochre salt-works, three pads, every sightline broken by a pan wall |
| `opus5-flintwick` | CTW | B · pale | two chalk headlands over a sound, worked for flint |
| `opus5-grykefell` | DTM | B · pale | a limestone pavement fell — clints, grikes and a shallow gill |
| `opus5-birkmire` | DTC | B · pale | a frozen birch mire, the core on a holm in an open ice pan |
| `opus5-sparholt` | KotH | B · pale | an alabaster works on two storeys, the pads sunk rather than raised |
| `opus5-peatgarth` | DTM | C · dark | a worked peat moss where every edge is a cut somebody made |
| `opus5-basaltmere` | KotH | C · dark | a black basalt bowl with one mere, the hill a stack with no back |
| `opus5-mirkholt` | CTW | C · dark | a dark wood on a shifted diagonal, one hollow way a side |
| `opus5-slakemoss` | DTC | C · dark | a hall the moss and water took back, the nave roofless and drowned |

The capture boards are the first in this repository authored through `controlPoints` on the intent with the
studio writing the `king` block and the score beside it.

## What the agents were given, and when

Three things reached them before they authored, and two reached them while they worked. The two that arrived
mid-run are the reason "unaided" cannot be claimed.

**Before.** The ground family, to stop twelve boards coming out as twelve greys. The `techniques/` cards in
preference to `showcase/`. And, for the second run only, the author's fault catalogue with the read that
decides each fault — so the relaunched agents were measurably better briefed than the first run was.

**During.** The container's database was empty, so `tree_style` carried only the six vanilla templates; the
74 copied trees were seeded out of `showcase/tree-showcase` after the agents had started and messaged to them
mid-run. And a correction on contrast: **boulders are stone**, and a sharp change of material needs a change
of ground under it — a face, a bench, a break of slope, a watercourse or a built edge — with a red ramp on
yellow sand as the named fault. The arid brief was the one most exposed to it and was corrected first.

**A run was lost and restarted.** The first three agents were killed at 28 minutes by an interrupt. Each had
finished its DTM and nothing else. Agents A and B had written their four identity sentences into their reports
before authoring and those survived; **agent C had not, and its three remaining identities were lost with it**
and had to be invented again. Writing the identities down first is a durability property and not only a design
one, which is not what the rule was put there for.

## What the review found

Every finding below is a read with coordinates, taken against the stored world rather than off a render.
Three boards were re-driven between the first reading and the second; each finding was re-taken afterwards,
because a re-drive moves the very coordinates a finding cites.

**Half the run's goals sit straight out of the door, and all three agents arrived there independently.**

| board | spawn separation | goal from own spawn | GO1 | lateral offset |
|---|---|---|---|---|
| dustwath | 184 | 43.3 / 44.0 | 3.32 / 3.24 | 14 / 13 |
| grykefell | 184 | 42.9 / 42.5 | 3.43 / 3.49 | 20 / 21 |
| peatgarth | 184 | 41.8 / 40.5 | 3.46 / 3.59 | 12 / 11 |

Three agents, three families, no contact, and the same arrangement to within a few blocks — because `GO1`'s
band of [3.0, 4.0] on a lane-shaped board puts the goal between `L/5` and `L/4` from its own spawn, and the
centre line is the cheapest way to satisfy it. This is the failure `AUTHORING-BRIEF.md` names when it says a
solved arrangement is what gets reused. The goals were authored as `pillar-2` and `pillar-3` — two or three
blocks of obsidian, forty blocks from a spawn. The author's ruling is `cube-3`, at 27 blocks, because the
break has to cost something when the walk does not.

**Thirty-five of ninety-eight trees are not seated on soil.** Reading a tree's seat means finding the lowest
log in its column and taking the block beneath it; taking the topmost non-leaf block instead counts a tree's
own canopy carpentry — a copied body carries wooden slabs, stairs and fences — and reports fourteen trees
that are correctly planted. The real set runs from trees on ice (`birkmire/birk-0` at −38,40 on Packed Ice)
through trees on ore (`basaltmere/scrub-8` at −22,70 on Coal Ore) to six trees standing on the masonry of
slakemoss' ruin, and one, `birkmire/birk-4` at 26,58, planted in another tree's leaves.

**One house in twelve boards has terrain through it.** `grykefell`'s barn: a transect across its small wing
(x 16–21, z 26–31) reads `BARRIER +5 at (18, 28)`, ground at y22 on the west half and y27 on the east.
Seventeen of eighteen houses are seated cleanly, so this is a singleton rather than a pattern — unlike the
trees, which are a pattern.

**Eleven of twelve build zones end on a straight line.** A single rectangle spanning the board's full width,
with the land running past it, so the boundary between building anywhere and building only on land has no
counterpart in the terrain. `opus5-flintwick` is the exception and the model: **three rectangles, stepped to
follow the coast.** The fix is to move the zone rather than the ground — `build.areas` takes a list.

## What the studio could not do

Four findings about the tool rather than the boards. Each cost an agent a build.

**`GET /coverage` cannot see a control point**, and two agents found it independently on two different capture
boards. `controlPoints` reach the intent while the coverage walk reads the plan, so a pad counts as ground
nobody goes to: `ochrepans` reports 51.3% dead **with its two largest dead patches lying exactly on its two
flank pads**, and `sparholt` 72.1%. The dead-ground calibration is meaningless on a KotH board until this is
closed, and it belongs beside `PG6`–`PG8` and `TC7`–`TC8` in `pgm-studio/docs/pgm/control-points.md` §9.

**The relief solves the `z ≤ 0` half and rotates it.** `ochrepans` drew its pan banks centred on `z 0` and each
built as a half bank with a seven-block fall through it, putting a control point on ground 61° from level.
`preflight` opened the gate, `relief/read` reported `seams 0`, and no render showed it; one transect found it.
Splitting the ring in two changes nothing, because the second ring lies in the half that is never solved. The
fix is arrangement — move the feature off the centre line.

**A `sink` cannot open a hole.** It writes ground to its floor, and it sealed `sparholt`'s undercroft.
`subtract` over exactly the courses to remove is the instrument.

**Three shapes that store at 200 and draw nothing or draw wrong.** A `polyline` takes `radius` and `vertices`,
not `width` and `points` — stated wrongly it pre-flights OPEN and builds nothing (`SK4`). An override add
cannot put its top below its own layer's floor. A polygon's `x1` is exclusive when it rasterizes, which stood
one column of deck as a six-block wall across the only way into `sparholt`'s lower storey. `beams: null` on a
house style answers 500; the documented "none" is `beams.block = -1`.

## Open questions for the author

Recorded as questions rather than filed as facts, because a rule about the map as it is played is not
derivable from this repository.

Whether open water should count as dead ground on a capture board. Whether a core standing over water can
leak in PGM at all. Whether a height difference between a team's two wool rooms is a fairness problem or a
convention. Whether a colonnade on a destroy board's main crossing is cover or nuisance. And whether
`fill-ratio`'s band of [0.201, 0.542] can be met by a CTW board authored as a landscape rather than as a
composer's board — `flintwick` ships at 0.794 and `mirkholt` was redrawn as a shifted diagonal to get near it,
which is why it is the only board of its set with void quarters.

## What the review round found that no gate does

The round after the review produced three findings about the pipeline, each invisible to every read except a
transect or a column, and each caught only because an agent took one.

**Nothing in the pipeline asks what block a prop is seated on.** `DR-SITE` asks whether there is ground under
a prop, not what that ground is, so a birch on packed ice, a tree on coal ore and six trees on a ruin's
masonry all placed cleanly and reported nothing. Thirty-five of ninety-eight trees across the run were seated
on something that is not soil, and the only read that says so is one `column` per prop.

**A paint patch drawn after a flight deletes it.** A `raise 0` shape drawn later in the document sets its
columns back to median ground, which took out `flintwick`'s west stair — at 200, gate OPEN, no rule, no
warning. Paint goes down before flights.

**A wall drawn along one line stands across whatever flight arrives at it.** `flintwick`'s east ramp read
`BARRIER +3` because the board's own cliff-top wall crossed the head of the flight. The answer is a gateway
in the wall where the way comes up, not a change to the flight.

The first of these is the one worth a task: it is the cause of the run's largest single fault class, and a
`column` per prop is the whole of the check.

## What the fixes came to

| board | props | dead | trees on soil | gate |
|---|---|---|---|---|
| `opus5-flintwick` | 42, 0 declined | **0.0%** | 9 / 9 | OPEN |
| `opus5-grykefell` | 36, 0 declined | 13.1% | 6 / 6 | OPEN |
| `opus5-birkmire` | 44, 0 declined | 14.7% | 11 / 11 | OPEN |
| `opus5-sparholt` | 8, 0 declined | artefact | — | OPEN |
| `opus5-dustwath` | 0 declined | 18.7% | seated | OPEN |
| `opus5-redmarl` | 0 declined | **0.0%** | seated | OPEN |
| `opus5-potsherd` | 2 declined | 9.4% | seated | OPEN |
| `opus5-ochrepans` | 1 declined | artefact | seated | OPEN |
| `opus5-peatgarth` | 30, **0 declined** | 25.3% | seated | OPEN |
| `opus5-basaltmere` | 38, 1 declined | artefact | 8 / 8 | OPEN |
| `opus5-mirkholt` | 30, 3 declined | **0.0%** | seated | OPEN |
| `opus5-slakemoss` | 40, 1 declined | 27.8% | 8 on soil, 2 kept in the ruin | OPEN |

Grykefell's barn moved onto a `relief_scope: "exclude"` pad on the level shelf east of its spawn and its
footprint now reads worst step 0. Every goal that was a pillar is a `cube-3`, which `DC3` builds in ender
stone because obsidian is worth at most three blocks — and that substitution is the run's one open question
for the author, since a 26-block cube of a soft material may break faster than the three obsidian blocks it
replaced.
