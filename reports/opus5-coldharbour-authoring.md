# Authoring Coldharbour — how the system was actually driven

One map, authored end to end, with the process recorded rather than the result. Every request, every file
written by hand versus by script, every preview looked at before committing to it, every render and what it
showed. The map matters less than the method; where the two conflict this document keeps the method.

**Measured against `pgm-studio` at `14fb4a653f164dfc9a884ec1baa1cf646cae34ab`** — *"Which rectangle is the
hall is derivable, and the size rule is about height (G186)"*, branch `claude/grok-mapgen-renders-7rchd2`,
working tree clean before and after. **Nothing in `pgm-studio` was edited.** The map, its documents and this
report are the only output, and they live here.

The short version of the answer: **the documents were hand-written, the API was driven with `curl` while a
call took one document and with Python once a call needed two joined together, and every gate was asked
before it was crossed.** The source was read exactly twice in the whole build, and §9 says when and why.

---

## 1. Environment

The API had died between sessions — `curl` to `/api/objectives/vocabulary` answered `000` — so:

```
sudo service mariadb start
ConnectionStrings__PgmStudio="Server=localhost;Database=pgm_studio;Uid=pgm;Pwd=pgm_dev_pw;" \
  dotnet run --project src/PgmStudio.Api --no-build          # backgrounded
```

`docs/cloud-setup.md` supplies the connection-string variable and the "no systemd, use `service`" rule. It
does **not** supply the port: that came off the API's own startup line, `Now listening on:
http://localhost:5189`, because `launchSettings.json` overrides the 7894 `tools/dev.sh` uses. Every call
below is `http://localhost:5189/api`.

## 2. What was read before anything was written

In order, and all of it documentation rather than source:

| Read | For |
|---|---|
| `docs/tools/flow.md` | the four levels, which tool owns which, and the five hand-offs. The one paragraph that shaped the whole session: *"Plan → layout and intent … `POST /api/plan/compile` turns the document into both halves at once"* |
| `docs/gameplay/approaches.md` | the design law. Every `[author]` claim is settled, so this is what the board is composed *for* rather than advice |
| `docs/tools/plan.md` | the plan document field by field, the refusal list, the six-call loop |
| `docs/tools/library.md` §endpoints | that a theme can be composed, previewed and pulled back as painter-ready JSON |
| `docs/world-export/decoration.md` §3, §5 | what flora and boulders are, and the four-block goal clearance |

`approaches.md` did the most work, and three of its claims are visible in the finished board: **void is the
instrument on a capture map**, **an objective's approaches must differ** rather than being one lane repeated,
and **a water lane can never be what connects two teams' lands**, so it has to be a second route inside one
team's own ground.

## 3. The plan — hand-written, then argued with by three endpoints

The document was typed into a file. Not generated, not templated: `coldharbour.plan.json`, nineteen pieces
written out by hand in aligned columns so the rows read as a board. That formatting turns out to matter, and
§6 records what happened to it.

The design, before any call: two teams `rot_180`; a spawn at the back; two wool rooms per unit placed
**against each other** — one low in a walled yard reached down a sunken lane, one on a chalk shelf reached
over open ground; a mid the build zone crosses; two permanent 20-block channels in the frontline that cannot
be bridged; a water lane inside the east flank that opens at 45 minutes; one approach wall.

Then, before a map row existed anywhere, the three reads `plan.md` says are the cheapest way to find out
whether a board is well-formed:

```
POST /api/plan/inspect      -> 200
POST /api/plan/evaluate     -> 200
POST /api/plan/feasibility  -> 200
```

**`/plan/inspect` replaced a script I would otherwise have written.** On the earlier Grok maps I wrote a
Python overlap-and-abutment checker to find out which pieces actually touched. That was wasted work: inspect
answers it directly, in block coordinates, and classifies every interface as `land`, `corner` or `narrow`.
It found something I had got wrong and could not see:

```
{'a': 'hub', 'b': 'yard', 'kind': 'narrow', 'x1': -40, 'z1': 65, 'x2': -35, 'z2': 65, 'length': 5, …}
```

A five-block seam between the hub and the yard — a scramble I never intended, on a board whose west route is
supposed to be the sunken lane. Fixed by pulling the yard off the hub and widening the holloway to carry the
seam instead. After the fix the shortest land seam on the board is 10 blocks and the only non-`land`
interfaces are corners I meant.

**`/plan/evaluate` argued about the shape and half-won.** First pass: `score 3.54, valid: true`, two soft
terms — `fill-ratio 0.724` against an authored band of `[0.201, 0.496]`, and `lane-width 30`. The fill-ratio
is the evaluator agreeing with `approaches.md`: a board that is 72% ground has no void to design with. So the
hub was split into two arms around a 15-block hole, the four corners were trimmed, and a 15×20 pit was cut
into the yard directly in front of the west wool room — which is `approaches.md`'s central capture
instrument, *"a hole in front of the objective … forces every attacker to pass around it"*, and which turns
that room's approach into two narrow ways round a drop.

Fill went 0.724 → 0.706 → **0.680**, and there it stayed, because closing the rest of the gap meant deleting
a third of a board whose shape I wanted. That is a decision rather than an oversight: `plan.md` is explicit
that *"an agent should read the score as advice about a board's shape and the compile's 422 as the only
refusal"*, and the reference map `ruediger.plan.json` ships with sixteen findings. The number is recorded
here so it is a stated choice and not a silent one.

**`/plan/feasibility` was the one read that told me nothing usable**, and correctly so. All three boxes came
back `producible: false` with `no-parameters-reproduce`, one citing `G105`. The feasibility read is a critic
for *generated* boards — it asks whether a composer's parameter tuple could have emitted this box — so on a
hand-drawn board the honest answer is always no. `plan.md` says as much (*"a hand-authored plan does not need
them"*). Worth calling once to see; not worth calling twice.

### 3.1 One field settled by experiment rather than by reading

`walls[].side` did not behave as I read it. The document says *"`side` names which of the wall's two faces
carries its defence chests, as the piece id that face looks out at"*, and naming the piece put the chests on
the other face. Rather than open the source I ran six `POST /api/plan/inspect` calls over the same board with
only that field changed, and read the `wallChest` back:

| `walls[0]` | `wallChest` |
|---|---|
| `{a: holloway, b: yard-sill, side: "yard-sill"}` | `holloway` |
| `{a: holloway, b: yard-sill, side: "holloway"}` | `holloway` |
| `{a: holloway, b: yard-sill}` | `holloway` |
| `{a: yard-sill, b: holloway, side: "yard-sill"}` | `yard-sill` |
| `{a: yard-sill, b: holloway, side: "b"}` | `holloway` |
| `{a: holloway, b: yard-sill, side: "b"}` | `yard-sill` |

So: **the literals `"a"` and `"b"` work; a piece id works only when it happens to be `a`.** Naming the `b`
piece by its id is silently ignored and falls back to `a` — which is exactly the case the documented sentence
describes. Six calls, no source, and the map uses `"side": "b"`.

The wall also moved because of this. Its first position — between the holloway and the yard — was a divider
between two approach routes rather than a defence line, which is not what a wall is for. It is now on
`holloway`–`back-west`, the centre route into the wool's own ground, so the two ways to that wool differ:
one walled and direct, one around the pit and open.

## 4. Compile, and the fact that forced a redesign

```
POST /api/plan/compile -> 200, warnings []
```

The compiled layout is 12 terrain polygons plus 6 structural rectangles. Reading their fields is what
produced the session's one genuine geometry change:

```
s0  base_height 10   s2 s3 s4  base_height 12   s5..s8 base_height 14
s9  base_height 16   s10       base_height 18   s11    base_height 20
```

**A compile fuses abutting pieces of equal height into one shape, so a compiled shape's only handle is the
height it stands at.** Every surface-12 piece — the whole frontline *and* the yard *and* the holloway —
arrived as one shape, and one shape takes one theme. Painting the yard differently from the frontline was
therefore impossible while they shared a height.

The fix was a design improvement rather than a workaround: the holloway and the yard were dropped two blocks
to surface 10. A holloway *is* a sunken lane, the drop gives the west approach a real character, and it hands
those pieces a shape of their own to paint. This is the sort of constraint worth knowing before drawing a
board — **plan surfaces are the theming granularity, not the pieces.**

## 5. The finish — and the preview that was right when I thought it was broken

### 5.1 Picking blocks from the API rather than from memory

```
GET /api/terrain/blocks -> 200   (105 blocks, each {id, data, name, group, hex})
```

This is the call I did not make on the earlier maps and should have. It answers with names, semantic groups
(`pale stone`, `cobble`, `bright`, `grey stone`, `sand`, `loam`) and a **hex colour** per block, so a palette
can be composed by looking at it instead of by recalling numeric ids. The chalk palette — quartz `155:0`
`#ece9e2`, mushroom stem `99:15` `#cbc4ab`, diorite `1:3` `#acacae`, cobble/gravel/mossy cobble for the yard
— came straight out of that list.

### 5.2 The import shape, found by mirroring the documented GET

`POST /api/themes/import` with the theme JSON as the body answers **500** with a raw .NET stack trace
(`ArgumentNullException … Parameter 'json'`), against a documented promise of "400, never 500, on bad JSON".
The working shape is the mirror of the documented `GET /themes/{id}/json` response — the document as a
**string** in a field:

```
POST /api/themes/import  {"name": "Chalk down", "themeJson": "<the whole theme, stringified>"}  -> 200 {"id": 1}
```

### 5.3 The finding that mattered: `palette` is not a field

The theme's section preview came back **flat green** where I had asked for a three-material voronoi turf. My
first reading was that the preview cannot draw patterns. That reading was wrong, and proving it wrong is the
most useful thing that happened all session.

The chain: `GET /api/themes/1/json` — the painter-ready form of what I had just imported — came back with my
`"palette": [grass, coarse dirt, grass]` replaced by `"bands": [{material: grass, depth: 1}]`. **Two of my
three entries were gone and the field had a different name.** A control test settled it:

```
POST /themes/import with "bands":[3 entries] ; GET /themes/{id}/json
  -> kind voronoi | bands kept: 3 -> [(2,0,1), (3,1,1), (99,15,1)]
```

`bands` keeps everything; `palette` is dropped. Rewritten with `bands`, the section preview immediately showed
green turf broken by brown at the cell edges — the thing I had drawn. **The preview had been telling the truth
the whole time**: a flat swatch means the pattern did not parse, not that the previewer cannot draw one. That
is the rule to carry: read a flat preview as a parse failure.

Two consequences worth recording. `tools/seeds/ruediger.layout.json` — the file `plan.md` names as *"the one
to read first"* — writes `palette` on its voronoi, so its surface is not the three-material mix it appears to
ask for. And a voronoi is **not** a palette to pick from: §9 records what it actually is.

### 5.4 What was previewed before being built, and what could not be

| Previewed | Call | What it showed |
|---|---|---|
| all three terrain themes | `POST /api/themes/preview` | a sample plateau cut open. Caught the collapsed voronoi; confirmed the fix; showed the band depths |
| both room shells | `POST /api/room-styles/preview-snapshot` | plan, section, isometric and cutaway of the actual buildings, from the same JSON the map binds |
| a single material | `POST /api/terrain/material-preview` | **one column** — a plan swatch of the top block and a section of the stack. Useless for judging a pattern; it is a column read, not an area read |

The room previews are the strongest surface in the studio: the shell that comes back is stamped by the same
`HouseStamper` the export uses, so what the picture shows is what the map gets. The cage was accepted on
sight — cobble plinth, stone-brick body, quartz top course, oak posts, arched openings; the spawn barn the
same in hardened clay under a hipped roof.

**Nothing previews the terrain paint in plan.** The bucket swatches are literally one `<rect>` of one colour
each, so a voronoi surface is a flat square in all of them. The first sight of the actual ground is the built
world's `--topdown --material`.

### 5.5 Relief, and the trap that was avoided by having hit it before

A relief governs its **whole island**: a shape keeps its own top only under `relief_scope: "hold"`. This board
stands at six surfaces from 10 to 20, so an unguarded relief would have levelled all of it — the exact fault
diagnosed on `sandscar-complex` in `grok-run1.md`. So the played surfaces (the yard and holloway at 10, the
hub band at 14, the shelf at 16, the spawn at 20 — eight shapes) were pinned `hold`, and only the two open
bands, the frontline at 12 and the downland at 18, were left to the field. Marks then state what those two
do: point marks holding the frontline at its own level, a summit at `h 21` on the knoll, a plateau at `h 18`
behind, and a `rim` mark at `h 11` so the coast falls a block into the void. `stairs: true`, because a block
step is what turns a riser into a wall.

The heightmap render is where that was checked, and the knoll's summit reads as a clean dome.

## 6. What was hand-edited and what was scripted

The distinction the whole session turned on:

- **Hand-written, in an editor**: the plan, all three terrain themes, both room styles, the relief, the
  dressing. Six documents, none generated.
- **`curl`, one call at a time**: everything that takes one document and answers about it — `inspect`,
  `evaluate`, `feasibility`, `compile`, `terrain/blocks`, `themes/import`, `themes/preview`,
  `room-styles/preview-snapshot`, `plans` + `plans/{id}/png`. Twenty-odd calls, each one line, each status
  read before the next.
- **Python, and only where a call needs two documents joined**: `build.py`, which attaches the themes
  registry, the per-shape theme and `relief_scope`, the relief, the room styles and the dressing onto the
  compiled layout and posts the six-call chain. That assembly is data-joining a shell cannot do cleanly. It
  is 90 lines and it prints every call with its status.

**One process lesson, learned the hard way.** Two early edits were made with a Python script — `json.load`,
mutate, `json.dump(indent=2)`. It worked and it destroyed the document: nineteen aligned one-line piece rows
exploded into 200 lines of one-number-per-line, which is unreadable as a board. The plan was **re-typed by
hand** to restore it, and every edit after that used a text edit on the file. A plan document is a drawing;
a formatter is not a neutral operation on it.

## 7. The build

Six calls, exactly as `plan.md` documents them, all first-time:

```
POST /api/plan                            -> 200  {"slug": "coldharbour"}
PUT  /api/map/coldharbour/plan            -> 200
GET  /api/map/coldharbour/layers          -> 200   (origination or rebuild? — origination)
POST /api/plan/compile                    -> 200   warnings []
PUT  /api/map/coldharbour/sketch/from-plan?force=true -> 200
POST /api/map/coldharbour/sketch/finish   -> 200
PUT  /api/map/coldharbour/intent/from-plan-> 200
GET  /api/map/coldharbour/export          -> 200
```

No refusal fired at any gate. That is the payoff for having asked `inspect`, `evaluate` and `compile` before
storing anything.

## 8. Reading the world back — which render answered which question

Every render was run for a question, not for a gallery.

| Question | Read | Answer |
|---|---|---|
| did the board come out as drawn? | `--topdown … --scale 3` | yes — the mid band, both 20-block frontline channels and the yard pit are all void, structures where they were placed |
| did the paint come out? | `--topdown --material` | yes — grass cells rimmed with coarse dirt over the downland, grey cobble-and-gravel over the sunken yard, the two themes clearly different ground |
| did the relief solve? | `--heightmap --contour 2` | yes — the knoll reads as a dome, the terraces as terraces, ground y 9..46 |
| did the trees land? | `--topdown --layer foliage --dressing <layout>` | **16 tree(s)**, drawn from the document — 8 per team image |
| is the board connected? | `--traversability-map` | 30 133 navigable columns, 4 164 bridged, 3 components, **0 of 4 markers isolated** |
| what is actually in a column? | `--column x z …` | the only honest read, and the one that caught the flora |
| what does a cut look like? | `--section --x -75 40 --z 80` | the yard at y10, the step up, the knoll's turf and a tree over it |

**`--column` is what caught the silent failure.** The topdown showed nothing wrong; the export answered 200;
the provenance sidecar lists structures only, never flora — so the only way to know whether ground cover
existed was to look at a column inside the ring I had drawn:

```
(0, 30)  -> y11 Grass Block          # nothing above it — no flora
(8, 22)  -> y11 Grass Block
```

Bare. After the fix in §9, the same columns:

```
(0, 30)  -> y12 Grass (31:1) over y11 Grass Block
(8, 22)  -> y13 Double Plant, y12 Large Fern
```

The boulders were verified the same way and had landed first time — `(-12, 26)` reads Diorite at y13 over a
y11 ground, two blocks proud — and they are visible in the heightmap as two small domes on the frontline,
which is a second, cheaper check for anything that adds height.

## 9. When the source was the only oracle

Twice in the whole build. Both times the API had been exhausted first, and both times the answer was a field
name the documents do not print.

**CODE-1 — `VoronoiMaterial`, after the API gave two contradictory answers.** The library round trip said the
field is `bands`; a committed seed file that the plan document points at says `palette`. Both are "the API"
in the sense that matters, and they disagree, so only the type settles which the *painter* reads.
`src/PgmStudio.Minecraft/TerrainPatterns.cs:44`:

```csharp
public sealed record VoronoiMaterial(uint Seed, int CellSize, IReadOnlyList<VoronoiBand> Bands, int Rise = 0)
```

`Bands`, and no `palette` anywhere. The read paid for itself twice over, because the surrounding `Resolve`
also says what a voronoi *is*: bands measured **inward from the cell edge** by the Worley F2−F1 gap — band 0
is the rim of each cell, the last band its middle. Not a palette to pick from at random, which is what the
name `palette` had led me to write. The chalk turf was re-authored on that understanding: coarse dirt on the
cell edges, grass in the middles, so the ground reads as scuffed turf rather than as confetti.

**CODE-2 — `FloraProp`, after a silent drop with no diagnostic left to try.** Two flora props landed nothing.
The export answered 200, no `DR-DOC` refusal fired, the provenance sidecar does not record flora at all, and
`decoration.md` names the `FloraSpec` knobs but never the field that carries the outline. Every API surface
was out. `src/PgmStudio.Minecraft/Dressing/PlacedProp.cs:223` and `Dressing/DressingModel.cs:36`:

```csharp
public sealed record FloraProp : PlacedProp {
    public IReadOnlyList<double[]> Points { get; init; } = [];
    public FloraSpec Spec { get; init; } = new();
}
```

The outline is `points`, not `ring`, and the seven knobs live in a nested `spec` object rather than flattened
onto the prop. I had guessed `ring` (from the relief model's area mark, which does use `ring`) and flattened
the knobs. Both wrong, both silent.

**What did not need the source, and nearly did.** The wall's `side` field (six inspect calls, §3.1). The
theme import's body shape (mirror the documented GET). The whole prop model except flora — `path`, `tree`,
`house` and `boulder` were written from `decoration.md`'s prose and verified by render and column probe.
Every question about the plan document. Every question about what the compile produces — the shape list is
in the compile's own response.

**The pattern in both code reads is the same, and it is a documentation gap rather than an API gap.** In each
case the *behaviour* was reachable — I could see that something had not parsed — and the *name* was not. A
document that printed one worked example of every prop kind and every material kind, the way `plan.md` prints
one plan carrying every element, would have removed both. `decoration.md` describes flora for eleven
paragraphs and never shows the object.

## 10. What the finished map measures

`ctw`, `rot_180`, 24 players, 144 × 280 blocks, ground y 9..46, build ceiling 32.

| | |
|---|---|
| pieces / compiled shapes | 19 pieces at six surfaces → 12 terrain polygons + 6 structural rectangles, one island |
| wools | 4 — `red` at `(-58, 9, 102)` and `orange` at `(57, 15, 102)` for blue, mirrored for red |
| spawns | 2, one per team, with an iron cube beside each |
| zones | one mid build zone; one water lane, which the `map.xml` carries as a `water-lanes` region |
| walls | one approach wall, `holloway`–`back-west`, chests on the defence side |
| dressing | 4 paths, 16 trees, 4 boulders, 4 flora rings, 4 houses (2 per team image) |
| evaluator | `score 3.243`, `valid: true`; `fill-ratio 0.68` and `lane-width 30` outside their bands |
| traversability | 30 133 navigable columns, 4 164 bridged, 3 components, **0 isolated** |

**Zero isolated markers is worth one line.** Grok Ridge reported 4 of 4 isolated because a stamped wool cage
reads as its own component. Coldharbour's cages report 0, and the difference is that both of its wool rooms
carry a land seam onto ground a player can walk from — the yard room to `back-west`, the shelf room to both
the shelf and `back-east`. The cage is the same building; the seam is what changed.

## 11. What I would tell the next agent

1. **Call `/plan/inspect` before writing a geometry checker.** It answers abutment, seam width and interface
   kind in block coordinates, and it found a five-block seam I could not see in my own document.
2. **Call `/plan/evaluate` twice — once to hear the complaint, once to see whether the fix helped.** Then
   decide, and write the decision down. It is advice; the 422 is the refusal.
3. **`GET /terrain/blocks` before choosing any block.** Names, groups and hex colours, 105 rows.
4. **Read a flat preview as a parse failure.** The previews do not simplify; if the picture is one colour, the
   pattern did not survive being read.
5. **Plan surfaces are the theming granularity.** Two pieces at one height are one shape and take one theme.
   Give a piece its own height when you want its own paint — and prefer a height that is also a design idea.
6. **Pin the played surfaces with `relief_scope: "hold"` before attaching any relief**, or the field will
   level the board you drew.
7. **`--column` is the only read that can prove a prop landed.** The topdown will not show it, the export
   will not refuse it, and the provenance sidecar does not record flora, boulders or trees.
8. **Do not run a plan document through a JSON formatter.** It is a drawing.
