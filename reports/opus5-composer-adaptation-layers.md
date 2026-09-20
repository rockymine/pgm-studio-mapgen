# Four composed boards, adapted — the second storey

**Run:** four CTW boards authored by driving pgm-studio's HTTP API, each adapted from a board
pulled off `GET /api/compose`, under `COMPOSER-ADAPTATION-BRIEF.md`. The emphasis is
**layers**, and the four differ in what the storey is.

## What I set out to build

Written before the first shape, one sentence each:

| Slug | The board | The storey |
|---|---|---|
| `opus5-crossdyke` | a limestone reef in the middle of the board with a masonry causeway standing over it, so the crossing is two crossings | **a deck over a contested crossing** — the high road and the reef under it, both reached from the bank, joined only by two flights that come up behind whoever holds the deck |
| `opus5-burrowgate` | two wools on cut shelves below a flat-topped hill, with a gallery running the hill's length between them | **an undercroft that is a second route between a team's own two wools** — forty-eight blocks of covered defensive rotation under the ground being fought over |
| `opus5-eaveswick` | a three-tier river terrace whose frontline is a quay seven blocks down, with the hub's ground carried out over it on a timber gallery | **an upper deck over a lower lane** — the defence holds the deck, the attack lands on the lane, and the only ways between are two flank ramps the deck overlooks |
| `opus5-drystone-ring` | a drystone ring round a thirty-by-fifteen hole, with a causeway walked out above its north bar | **a raider's bridge above the ground** — forty blocks of open deck with a ramp at each end and no way off between them |

Beyond the storeys, the run was held to: a real mid island (Crossdyke), an intra-team build
zone (Burrowgate's `b-link`), a plan wall (Eaveswick), relief used selectively with structural
ground stated out of it (all four), a `layered` material on the `slope` axis (all four), and
`plan/flow` read before and after every adaptation.

All four: **`export gate OPEN`**, **0 dressing declines**, dead ground **0.0 %** / 0.2 % /
0.0 % / 0.0 %, three themes each, every theme on the ground.

---

## What I could not say

Each of these was checked against `GET /api/openapi/v1.json`, `GET /api/rules` and
`GET /api/rules/terms` before being written down, and each carries the verdict the brief asks
for: **missing** (no mechanism) · **unreachable** (exists, the surface hid it) · **mistaken**
(exists, documented, I did not find it).

### 1. There is no per-storey theme census — **missing (the number), not the picture**

`GET …/themes/census` counts the **surface**, which on a stacked board means the topmost
storey and nothing else. On `opus5-burrowgate` the board carries three themes and the census
reports two: the whole of `rock` — the gallery's floor, its walls and the hill's body — is
under a roof, so it reads as a theme that painted nothing, which is the exact shape of a fault
the brief tells you to look for.

What I searched: `census`, `layer`, `storey`, and the parameter lists of every route in
`openapi.json` whose name contains `theme`. `themes/census` declares `slug` and `format` and
nothing else; posting `?layer=under` answers 200 and ignores it (measured). The **picture**
per storey does exist — `render/topdown`, `render/heightmap`, `render/surface` and
`render/structures` all declare `layer`, and `?layer=under` answered 200 with a PNG — and
`GET …/column?at=12,52` answered the cell (cobblestone at y10, the gallery floor, painted
correctly). So the mechanism to *see* a storey is there and the mechanism to *count* it is
not. A `?layer=` on `themes/census` would close it.

### 2. `GET …/coverage` and `GET …/plan/flow` are single-storey, and `flow` is pre-layer — **by design, and worth a word**

Neither declares a `layer`. `coverage` walks the surface; `flow` reads the stored **plan**,
which has no storeys at all. The consequence is that the read the brief's §7 makes a bar —
"`/plan/flow` says something you meant it to say" — cannot see the thing three of these four
boards are about. `opus5-eaveswick` reports *"One way in, end to end: nothing forks and
nothing merges"* for each wool while the board's whole design is a deck and a lane over the
same ground; `opus5-drystone-ring` reports *2 ways in* when there are three.

This is **not** a gap in the system: the plan tier is defined as the arrangement, and the reads
that do see a storey exist and were used — `render/section`, the driver's void scan, and
`GET …/walk` with a `y` in its `from` (`from=-12,52,11&to=36,52,11` answered *walked end to
end* through Burrowgate's gallery). It is a gap in the **bar**: a stacked board cannot be
judged by `flow` alone, and no read says so at the point where flow is printed.

### 3. `reach` reports a whole team's ground as unreachable — **unreachable (the wording), not the system**

`04-reach.txt` on every one of the four lists the two teams' own ground as
`no-build-zone — nothing the map opens to bridging reaches it, and it is not walked to`, in
patches of 950–1 150 cells. On `opus5-crossdyke` that is literally both banks, including the
spawn a player arrives on. The same board's `preflight` answers *"traversability: spawn ↔
objective chain connected"* and `coverage` answers 0.0 % dead, so nothing is actually wrong.
The read's own header says *"None of this is a fault"*, but a reader who takes the patch list
at face value will redesign a correct board — which is the failure `opus5-run4` already made
once against the traversability map. The classification is about **bridging reach from the
build zones**, not about whether a player can get there, and the label does not say so.

### 4. A compiled shape's `floor` can only be set per height class — **mistaken on my part, and the workaround is the right shape anyway**

Burrowgate needs the hub's ground to be a slab from `y15` so the gallery fits under it.
`shapePropsByHeight {"16": {"floor": 15}}` does that, and `shapePropsById` would do it per
shape — but the compile emits **one shape per (component, surface)**, so there is no id that
names the hub bar without also naming its two prongs. I wanted to floor the bar and leave the
prongs solid, and could not. Reading it back: flooring all three and filling under all three
with the same rock layer is the *correct* construction — a hill whose body is one mass — and
the thing I wanted was an optimisation rather than a capability. Not a gap.

### 5. `GET /api/compose` takes two symmetries, and one of them is not in any document I read

Measured: `rot_180` → 200, `mirror_z` → 200, `mirror_x` → **400**, `rot_90` → **400**,
`none` → 400, `translate` → 400. `GENERATION-NOTES.md`'s composer section and the brief both
name `rot_180` and the vocabulary of hubs, frontlines and wools, and neither says which
symmetries the endpoint accepts. Not a gap — the answer is one `curl` — but it is the first
thing a run pointed at "both symmetries" has to find out.

---

## What I got wrong

**`voidEnforcement: true` closes a CTW board.** It writes
`<apply block-place="deny(void)" region="void-enforcement-area"/>` over an `<everywhere/>`
region, which denies placing a block in the void *everywhere* — including the crossings the
board is played across. It was in `opus5-crossdyke`'s first build, copied from a destroy board
where a permanent ditch is the point. Nothing refused it; the map stored, pre-flighted OPEN and
exported. The build zones already generate exactly the right rule
(`<apply … region="not-build-area">`), so the field simply comes off a wool board unless a
named exclusion list goes with it. It is off on all four.

**§2's 1.3×–1.5× is a straight-line measure at 20 and 30 players, and the walked ratio at 8
and 12 is much tighter.** I sieved 32 two-wool boards at 12 players through
`POST /plan/compile` → `POST /map/from-documents` → `GET …/plan/flow` and read the attacker's
**walked** distance to each wool:

| | attacker-distance ratio |
|---|---|
| median over 32 boards | **1.10** |
| range | 1.00 – 1.36 |
| boards at or over 1.30 | 2 of 32 (`rot_180` seed 65 at 1.36, `mirror_z` seed 72 at 1.31) |

What *is* routinely lopsided at 12 players is the **defence**: the same 32 boards run the
defender's two walks from 1.0× to **2.03×** apart (`mirror_z` seed 61: 29 and 59 blocks), and
that is `WL9`'s `spawn-wool-ratio`, whose band is **[1.031, 1.220]** — a band the composer's
own output falls outside without the evaluator refusing, because the term is soft. So the
brief's fault is real and my first reading of where to look for it was wrong. Both of the
boards I picked for it were sieved on the walked numbers rather than assumed, and both were
fixed: Burrowgate 1.36 → **1.07**, Eaveswick 2.03 (defence) → **1.05**.

**Eleven `SK9` declines from one layer, and the store answered 200.** Crossdyke's piers, deck
and kerb were drawn on one layer; a layer holds one span per column, so every pier under the
deck and every kerb on it was not in the world. The status code was 200 and the export gate was
open. Three layers fixed it. This is the fault the pre-warmup says a stacked board can carry
invisibly, and the read that named it was the drive's own `warnings`.

**A ramp with absolute anchors needs the ground it lands on stated too.** Twice. Burrowgate's
two flights ended at `y16` while the relief solved the hill around them to `y26`
(`BARRIER +12 at (5, 44)`); Drystone Ring's far ramp landed at `y12` against a push that had
raised the stub to `y19` (`BARRIER +7 at (−65, 30)`). In both cases the fix is an `area` mark
pinning the landing at exactly the anchor's height. Neither was visible in any render; both
were one transect.

**A one-course paint patch paints nothing, in silence.** Crossdyke's `scald` was an ordinary
`add` of `base_height: 1` under twenty courses of terrain. `SK23` caught it — *"not one of
their 4 columns has ground on all eight sides"* — but only because the patch was small enough
to be entirely edge; a larger one would have gone unmentioned. A brush must declare a
`height_mode`.

**Widening a corridor made the dead ground worse.** Drystone Ring's north bar was widened from
ten blocks to fifteen so the causeway over it would not cover the whole lane. `plan/flow`'s
*"what no journey reaches"* went from 4 % to **9 %**: the extra width at the ring's corner is a
cul-de-sac the route turns before reaching. Widening only the bar's middle third took it to
**0.0 %**.

**Three sites for one building, then none.** On both eight-player boards I placed a house by
eye, read the decline, moved it, read the next decline. The instrument is
`POST …/sketch/seats`, it is new on this branch, and it answers the question forwards. Used
properly it also gives the honest answer: see below.

---

## The measured answer nobody asked for: composed boards have almost nowhere to put a building

`POST …/sketch/seats?kind=house` over all four finished boards, footprint 11 × 9 unless stated:

| Board | Players | Seats | Largest refusal |
|---|---|---|---|
| `opus5-crossdyke` | 8 | **16** at 9 × 7, **4** at 7 × 7 — every one on the mid island | 1 904 cells `DR-KEEP` |
| `opus5-drystone-ring` | 8 | **8**, none on the team's own ground; 8 × 8 on the hub refuses `DR-PASS` | 2 785 cells `DR-KEEP` |
| `opus5-burrowgate` | 12 | **116** | 2 466 cells `DR-KEEP` |
| `opus5-eaveswick` | 12 | **40**, all on the quay | 3 905 cells `DR-KEEP` |

So the two twelve-player boards carry buildings (two and one) and the two eight-player boards
carry none, and that is not a failure of siting: between a spawn march, one or two wool
approaches and a road, an eight-player composed team side has no eight-block-passable
footprint left. The boards say so in their reviews rather than shipping a building squeezed
into a lane.

---

## What worked first time

- **`opus5-eaveswick` went in on the first build.** Score 0 on the first `--dry`, `SK27` the
  only complaint at the store, zero dressing declines, export gate open. Every number in it —
  the seven-block cut, the fourteen-block flank ramps, the six courses under the deck — was
  arithmetic done against `GET /api/rules` and `GET /api/rules/terms` before the first shape.
- **The complement idiom for a tunnel.** Burrowgate's gallery is four rock rectangles with a
  hole between them and no `subtract` anywhere; it built correctly the first time it was
  posted, and the section at `z = 52` reads exactly what was drawn.
- **Three made layers for one structure.** Once the `SK9` lesson was paid for on Crossdyke, the
  same pattern — one layer for the posts, one for the deck, one for the rail — went in first
  time on Eaveswick and Drystone Ring.
- **`plan/flow` as a design instrument rather than a check.** Both balance fixes were done
  entirely at the plan tier, before a world existed, by moving a spawn and re-hanging two wools
  and re-reading. It costs one `POST /plan/compile` and one `POST /map/from-documents`.
- **`walk` with a `y`.** `from=-12,52,11` answered *walked end to end* through a gallery that no
  projection read can see. It is the only read that confirmed the second storey is a route
  rather than a hole.
- **The `slope` band axis.** All four grounds are finished with a `layered` material on it, cut
  against each board's own `GET …/incline?format=text` distribution. None of the four reads as
  a flat sheet from above.

---

## Open gameplay questions, decided without an oracle

1. **Is a build zone that only one team can reach fair?** Burrowgate's `b-link` is a crossing
   whose every interface touches one team's own islands, so the wool island behind it is
   unreachable except across a bridge the defence stands on. `CT4` and `BZ5` both name the
   motif, but neither says whether the *objective* may sit on the far side of one. I built it:
   the attacker can cross the same bridge, they just cannot flank it. **Decided:** a wool behind
   a team transient-link is a chokepoint, not a lock, because the zone is open to both sides —
   but it is the strongest single defensive position in the run and it may be too strong.

2. **Should a raider's route be one-way?** Drystone Ring's causeway has a ramp at each end and
   nothing in between: forty blocks with no turning and no cover, in full view of the board's
   west half. **Decided:** yes — an alternative route that is also safe is not a decision. The
   question I cannot answer is whether forty blocks is too long to commit to at eight players.

3. **Where does an approach wall belong when the wool has two lanes?** Eaveswick walls the
   quay→spur interface and leaves the hub→spur interface open, so the attack must come the long
   way and the defence walks straight in. `ST8` sizes the wall and `PL13` says where it may not
   go; nothing says which of two lanes to bar. **Decided:** bar the one the attack would
   otherwise take *first*, which is the short one off the frontline.

4. **How much of a board may be stated flat?** Burrowgate is 0.606 level and 0.508
   largest-field, which the warmup calls a table with edges; the alternative attempt rolled the
   hill and produced `RL5` at 29 % level, which is the opposite fault. On a board where a
   quarter of the ground is a gallery roof and another fifth is a cut shelf, neither number
   describes the board honestly. **Decided:** state the roof and the shelves flat, put the
   relief on the frontline, and record both numbers rather than tuning to one.

5. **Is a building on the crossing's landing apron cover for the attack or for the defence?**
   Eaveswick's wharf shed is the only seat `seats` offers and it sits where the bridges arrive.
   **Decided:** it is symmetric, so it is cover for whoever is holding it, and on a board whose
   whole design is that the attack must cross open ground I would rather the attack had one
   thing to stand behind.

---

## Where the boards are

| Slug | World | Spec | Review | Isometric |
|---|---|---|---|---|
| `opus5-crossdyke` | `maps/opus5-crossdyke/` | `specs/opus5-crossdyke/` | `review/opus5-crossdyke.md` | `specs/opus5-crossdyke/renders/world-iso.png` |
| `opus5-burrowgate` | `maps/opus5-burrowgate/` | `specs/opus5-burrowgate/` | `review/opus5-burrowgate.md` | `specs/opus5-burrowgate/renders/world-iso.png` |
| `opus5-eaveswick` | `maps/opus5-eaveswick/` | `specs/opus5-eaveswick/` | `review/opus5-eaveswick.md` | `specs/opus5-eaveswick/renders/world-iso.png` |
| `opus5-drystone-ring` | `maps/opus5-drystone-ring/` | `specs/opus5-drystone-ring/` | `review/opus5-drystone-ring.md` | `specs/opus5-drystone-ring/renders/world-iso.png` |
