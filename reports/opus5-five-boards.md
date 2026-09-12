# Five boards, one run

## What I set out to build

Five maps, each with **one idea**, written down before anything was authored:

| # | slug | mode | the story, in one sentence |
|---|---|---|---|
| 1 | `opus5-blackden-sough` | DTM | a gritstone edge with a drainage sough driven under it: over the crest, through the one nick, or under it in the dark |
| 2 | `opus5-heftfold` | CTW | two hill farms either side of a pass, with a drystone sheepfold on the saddle as the only ground in the middle that is nobody's |
| 3 | `opus5-glassmere` | DTC | two snowbound shores of a mere whose middle never freezes — nothing hides you on the way over |
| 4 | `opus5-burgage-terrace` | DTM | a market terrace over a water meadow: made ground meets grown ground along one notched edge |
| 5 | `opus5-lingbeck` | CTW | a heather moss split by its own beck, with a wool on each bank and three ways across |

Every one built, every one `export gate OPEN`, every one `placed N, declined 0`.

| board | evaluate | coverage dead | walked / scrambled / barrier | props |
|---|---|---|---|---|
| Blackden Sough | 0, valid | 17.9% | 11 297 / 265 / 629 | 26, 0 declined |
| Heftfold | 0, valid | **0.0%** | 8 683 / 52 / 492 | 20, 0 declined |
| Glassmere | 0, valid | 39.1% | 12 473 / 200 / 36 | 32, 0 declined |
| Burgage Terrace | 0, valid | 35.6% | 12 733 / 79 / 377 | 20, 0 declined |
| Lingbeck | 0, valid | **0.0%** | 10 381 / 40 / 328 | 18, 0 declined |

---

## What I could not say

Three items. The first is **missing**; the second is a **defect**; the third is **mistaken
documentation** and cost the most.

### 1. `intent.meta.authors` is out of reach from a finish — `EX6` on every board

`EX6` fires on every one of the five: *"the map names no author, so the observer platform's authors
board is left off — state meta.authors."* The map **does** name an author: `map.xml` carries
`<authors><author>Opus 5</author></authors>` on all five, because `POST /map/from-documents` takes
`authors` in the request body and applies it to the map row.

What the export's observer board reads is `intent.meta.authors`, which stays `[]`. `drive.py` patches
`created` into `intent.meta` and does not patch `authors`; the finish has no key that reaches it, and
a spec carrying a finish has its intent regenerated from the compile on every run, so it cannot be
stated there either.

**Verdict: out of reach** rather than missing — `PUT /map/{slug}/intent` exists and would take it. It is
a one-line gap between where the authors are applied and where the observer platform looks for them.
Reported rather than worked around, since working around it would mean a curl after every drive that
the next re-drive throws away.

### 2. A house style in `dressing.styles` without its discriminator is a 500, not a 400

```
POST /map/from-documents   500
RQ2  the studio failed to answer this request, and the fault is its own rather than the document's
```
and in the server log:
```
System.NotSupportedException: The JSON payload for polymorphic interface or abstract type
'PgmStudio.Minecraft.Dressing.PropStyle' must specify a type discriminator.
  at DressingJson.ParseStyles … at SketchMaterialGate.Buildings … at MapFromDocuments.LoadAsync
```

The correct shape is `{"kind": "house", "shell": <HouseStyle>}`. A bare `HouseStyle` — which is exactly
what `roomStyles` takes, two keys away in the same finish — throws. Every other malformed field in this
repository's vocabulary answers with a rule id and a JSON path; this one answers with the studio's own
fault and a sentence that says to read a log the author does not have.

**Verdict: a defect.** The parse is the gate's, so a 400 naming `dressing.styles.<id>.kind` is
reachable from where the exception is thrown.

### 3. `roomStyles`' wool half is documented as `cage` and the schema calls it `wool`

`SketchRoomStyles` carries exactly two members, `wool` and `spawn`. `tools/README.md` documents the
finish key as `{"cage": …, "spawn": …}`; `drive.py`'s own docstring says the same; `showcase/16-forest`
— one of the four showcases that keeps the capture board *because* its technique is about a wool
board's furniture — states `cage`.

A key `SketchRoomStyles` does not know is dropped in silence. A snapshot draws no `RQ3`. So Heftfold
stored at 200, pre-flighted OPEN, exported at 200 and built **both its wool rooms as bedrock boxes**:

```
GET …/column?at=-45,75      y24 Bedrock · y16 Bedrock        (cage)
GET …/column?at=-45,75      y26 Bricks  · y16 Gravel         (wool)
```

**Verdict: mistaken** — the mechanism exists and is documented under the wrong name in two places, and
nothing in the pipeline says so. It is the most expensive kind of fault this repository has a rule
about: the world builds, every gate passes, and the thing you asked for is not there.

---

## What I got wrong

**A plan piece at a lower surface, enclosed by pieces at a higher one, is not a cut.** Lingbeck's gill
was stated as a `beck` piece at surface 7 with the hub at 12 either side. The compiler traces one
outline per component, the taller add wins every column, and the gill was simply not in the world — a
transect read `11 11 12 12 13 13 14` straight across it, the water prop sat on the surface like a
puddle, and the export gate was OPEN. `override: true` is what cuts it, because override moves a shape
into the second pass where it overwrites the column it lands on.

**An insert names the edge LEAVING that vertex.** Burgage Terrace's meadow ring got `{"after": 8}` when
the west flank was at index 9, which put the point on the board's back edge and folded the polygon. The
world then carried ten blocks of void **inside** the meadow at `x -30, z 40..49`. Nothing refused it.
After a run of inserts the index is not the one it started as, and the fix is to count.

**A push is applied to the solved surface, so a push over a pan lowers the pan.** Blackden's `slack`
push reached the sough's tail and the south flight came out landing two blocks proud of the ground it
was supposed to arrive on. Visible in the walk and in nothing else. Both pushes became `point` marks —
marks negotiate with each other, pushes are added afterwards.

**A ramp's top anchor is an absolute height.** Lingbeck's ford ramps state `MOSS`, and where the relief
left the bank two blocks above that the crossing arrived at `BARRIER +3`. Two `area` marks pinning the
banks flat at the ford and at the brig were the fix — which is what an `area` is *for*, and I had been
treating it as the thing to avoid after Blackden's first relief came out a table.

**I painted a terrace like a car park.** Heftfold's intake took the setts over its whole 50 × 40, and
the top-down showed two farms standing on a grey slab. An intake is walled *grassland*: what is built
about it is its **edge**. Grass on top, a stone-brick coping on the rim, a `wallRun` on the wall, and
the paving as two splotches round the buildings.

**I bound a theme to the map and forgot to bind it to the shape.** Burgage Terrace's first painted build
left `themeById` unset, so the terrace took the map default: a green field with a grey cliff, and the
diagonal team-tinted retaining wall — the reason the board exists — simply absent. One look at the
isometric; no finding at all.

**Two boards' worth of relief were tables before they were landscapes.** Blackden's first pass pinned
70 × 64 of dale flat with one `area` mark and read as two green slabs. An area pins a flat disc and is
right only where flat is the point — the ground a bridge lands on, the pan a sough discharges into, the
shelf a goal stands on, a crossing. Everything else is a `point` at radius 4–6 with the relaxation
between them.

---

## What worked first time

- **The slope band axis.** All five boards finish their ground on one `layered` stack on `slope`, with
  the cuts read off `GET …/incline?format=text`. Blackden's incline answered 43% under 10°, 16% in the
  teens, 22% in the twenties and 9.6% at 40° or steeper; cuts at 28° and 42° put three quarters under
  turf, a sixth on the worn shoulder and a tenth on bare rock, and the worn ground appears exactly where
  the ground is worn. It worked on the first build on every board and is the single technique that did
  most for how they look.
- **The stacked sough.** Rock banded round the corridor as adds only, clipped out of the moor's own
  drawn outline, a ground layer with `floor: 24`, and six courses of air between. It built correctly on
  the first attempt and `walk?from=-21,45,18&to=-21,80` answered **35 blocks, 0 placed, 0 drops, walked
  end to end**.
- **Anchored flights.** Eleven of them across five boards, every one a single polygon with two anchors
  at the foot and two at the head, `height_mode: level`, `skirt: 0`, `keepClear: true`, a `material`
  rather than a theme. Every one measured at **worst step 1** or better on its first build.
- **Solid first, freckled afterwards.** Glassmere's ice: one `solid` stroke at the water and one wider
  `worn` stroke at coverage 0.34 over it. First try, and it is the best-looking thing in the five.
- **`tools/loop.py`.** Twenty seconds against ten minutes. Every prop position on every board after the
  first drive was settled with `--candidates`, eight at a time, and the boards finished at 0 declines
  because of it.

---

## Open gameplay questions, decided without an oracle

1. **Blackden Sough** — the edge is a twelve-block face with one eighteen-block gully and one six-wide
   tunnel through it. Is that the right ratio of open route to chokepoint for twelve a side? Built as
   stated; `RL2` is left complaining about 178 barrier steps, which are the scarp and are the board.
2. **Heftfold** — both wools sit on the same terrace, 25 and 32 blocks from the door, and differ in
   their *approach* rather than their distance. Do two wools that are equally far but unequally
   defensible read as balanced?
3. **Glassmere** — the crossing is 24 blocks at three headlands and 40 in the two bays. Is that spread
   enough to make *where* a real choice, or does everyone simply always bridge at a headland?
4. **Burgage Terrace** — the monument stands four blocks back from a six-course wall with two stair
   chokepoints and a bridged void in front. Breakable, or a stalemate with a good view?
5. **Lingbeck** — the gill runs the full depth of a team's ground, so an attacker who drops into it is
   in cover the whole way to the spawn's apron and cannot get out except at the ford. A route or a trap?

---

## One measurement worth keeping

**`coverage` is the read that separates a board with a shape from a board with a middle.** Blackden's
first build read **62.0% dead** with four 2 000-cell patches, all of them one block from used ground:
one objective and one spawn a side make two journeys, and the flanks are on neither. Moving the
monument twelve blocks off the centre line and narrowing the board ten blocks took it to **17.9%** with
no other change. The two wool boards read **0.0%**, because a board with two objectives a side and a
spawn between them has journeys everywhere by construction.

Nothing refuses on coverage. It is the cheapest read in the pipeline and the one that says whether the
ground you authored is ground anybody walks on.
