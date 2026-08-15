# Grok run 1 — three maps authored with no running studio

Grok was given the two repositories and the app, cloned them, read `docs/tools/`, `GENERATION-NOTES.md`
and the committed specs, and wrote three maps as documents. It never had a live API: no .NET, no MariaDB,
so nothing it wrote was ever posted to an endpoint, compiled, rasterized or exported. Its own account of
that is `grok-experience.md` beside this file.

This report is what happened when those documents were driven through the real endpoints for the first
time. The three boards are `grok-ridge` (CTW), `sandscar` (DTM) and `sandscar-complex` (DTM); each is
committed whole under `maps/`, its documents under `specs/`, and Grok's originals verbatim under
`specs/<slug>/authored-by-grok/`.

The headline: **the plans were nearly right and two of three were refused for arithmetic; the layouts
were wrong in a way that builds nothing and says nothing; the dressing was authored in the wrong unit.**

## What each document did

| Document | Verdict | Why |
|---|---|---|
| `*.plan.json` × 3 | 1 compiled clean, 2 refused with 422 | overlapping pieces at different surfaces; a wall on a pair that shares no interface. Four rect edits in total fixed all of it |
| `*.layout.json` × 3 | all three rasterize to **no ground** | rectangles carry `x/z/w/h`, the model reads `min_x/min_z/max_x/max_z`; and `relief` sits inside `layout` where the model reads it at the root |
| `*.props.json` × 3 | parse-refused, then partly dropped | positions in **plan cells**, the document is in **blocks**; houses are `points`, the model reads `wings`; `style` is a registry name, the model takes the style inline |
| `*.styles.json` × 3 | **all six styles stamp** | two field faults — one material wrapped in a second `material` object, one invented enum value — and past those, six complete buildings (§3.1) |

## 1. The plans

Posted verbatim to `POST /api/plan/compile`:

```
grok-ridge        422  wall 'low-gate'–'mid-gate' is not a shared land interface
sandscar          200  no warnings, 4 shapes, 1 island
sandscar-complex  422  overlapping pieces 'pit-floor' and 'savanna-gate' have different surfaces (delta 10)
                       overlapping pieces 'pit-rim-e' and 'savanna-gate' have different surfaces (delta 5)
                       overlapping pieces 'hill-top' and 'upper-east' have different surfaces (delta -5)
                       overlapping pieces 'upper-east' and 'crest-east' have different surfaces (delta 3)
```

Both refusals are cell arithmetic, not design. **Grok Ridge**: every terrace row is five cells deep and
`low-gate` was written four (`[-5, 2, 5, 4]`), so it stopped one cell short of `mid-gate` and the wall
Grok's own README describes — "wall link between the low and mid gates" — had no seam to stand on. The
`low-west`/`low-east` pieces either side of it are `[…, 5]`, which is what the gate was meant to match.
**Sandscar Complex**: `savanna-gate` started two cells inside the pit column, and `upper-east` reached two
cells into `hill-top` and one into `crest-east`.

The fix was four numbers, and nothing else in the three documents was touched:

| Piece | Grok wrote | Built as | Effect |
|---|---|---|---|
| `low-gate` | `[-5, 2, 5, 4]` | `[-5, 2, 5, 5]` | one cell deeper, so the gate abuts `mid-gate` and the wall exists |
| `savanna-gate` | `[-8, 18, 6, 5]` | `[-8, 20, 6, 5]` | two cells south, off the pit, aligned with `savanna-west`/`savanna-east` |
| `upper-east` | `[4, 28, 8, 4]` | `[4, 28, 6, 3]` | trimmed off `hill-top` and `crest-east` |

Everything else — every surface, every zone, every marker, both monuments per team, the 50-block
monument spacing, the spawn facings — is Grok's, unchanged.

With those four numbers all three compile with **no warnings**, and all three build a world and export.

The evaluator (advice, not a gate) reads them as dense and wide against the corpus bands:

| Map | score | valid | fired |
|---|---|---|---|
| `grok-ridge` | 7.1 | true | fill-ratio 0.609 (band .201–.496), frontline-width 17 (1–16), spawn-wool-ratio 1.588, wool-front-ratio 2.364 |
| `sandscar` | 2.1 | true | fill-ratio 0.611, frontline-width 24, max-chain-length 120 (25–110) |
| `sandscar-complex` | 1005.3 | **false** | gap hop 21 outside 10..20 between `low-desert-e` and `mid-bridge` (hard), plus fill-ratio 0.647, frontline-width 36, max-chain 180 |

## 2. The layouts build nothing, and say so only at the last call

Grok's layout documents are the plan geometry re-expressed in blocks, with themes named and (for the two
Sandscars) a relief. Posted as-is:

```
PUT  /api/map/{slug}/sketch/from-plan   200 {"ok": true, "orphaned": []}
POST /api/map/{slug}/sketch/finish      422 Nothing is drawn: the layout rasterizes to no ground.
```

Three faults, each silent on its own:

**Rectangles carry the wrong four fields.** `SketchShape` reads a rectangle as `min_x`/`min_z`/`max_x`/
`max_z`; every rectangle Grok wrote carries `x`/`z`/`w`/`h`. The unknown keys are dropped and the known
ones default to zero, so `RingOf` returns a degenerate ring at the origin and the shape covers nothing.
Twelve of the thirteen Grok Ridge shapes and both Sandscar shapes are rectangles, so the boards
rasterize to nothing at all. This is exactly the failure mode `GENERATION-NOTES.md` §1 warns about —
Grok read that note, cited it in its own README ("the silent-failure trap from GENERATION-NOTES §1"),
and then hit a different instance of it.

**`relief` is nested one level too deep.** It is written inside `layout` beside `shapes` and `islands`;
`SketchLayout` reads it at the document root, keyed by island id. Nested, it is dropped without a word.

**The relief body is an invented vocabulary.** Grok wrote `{base, noise:{scale, amp, octaves},
features:[{type: "depression"|"hill"|"flat"|"river", x, z, radius, depth|height}]}`. The model reads
`{base, step, reach, stairs, grain:{amplitude, scale, seed}, marks:[{kind, at, r, h, …}]}`. Only `base`
survives the crossing, so even at the right nesting the relief would have flattened the island to its
base level and placed no landform.

The one that would have cost the most cycles is the ordering: `from-plan` answers `200 {"ok": true}` for
a layout that draws nothing, and the refusal arrives one call later from `sketch/finish`. The store
step accepts geometry it never reads.

**What was built instead.** The layouts were not repaired — the compiled layout from each plan is the
same geometry, so repairing them would have been transcription. The compiled layout was used, and for
`sandscar` Grok's relief was translated mark-for-mark into the real vocabulary (`specs/sandscar/sandscar.relief.json`):
its depression at `(−25, 75)` r18 d8 → a `point` mark `h: 32`, its hill at `(25, 75)` r16 h10 → `h: 50`,
the rise at `(0, 100)` → `h: 44`, the flat at `(0, 45)` → `h: 40`, and `noise{scale: 0.04, amp: 2.5}` →
`grain{amplitude: 2.5, scale: 25}` (the stated scale is a frequency; the model's is a feature size in
blocks, and 1/0.04 = 25). `maps/sandscar/renders/03-heightmap.png` is that relief solved: a hollow and a
hill either side of the plateau, one under each monument, exactly where the document's own notes say
they belong.

`sandscar-complex`'s relief was **not** carried, and the reason is worth stating. Its pieces stand at ten
surfaces from 32 to 52; its relief states `base: 40`. A relief governs its whole island — a shape only
keeps its own top if it declares `relief_scope: "hold"` — so carrying it would have levelled every terrace,
the pit and the hill to 40 and then dug three landforms into the flat. The terraces are the board, so the
board was built from the plan's surfaces and the relief left out. Two documents that each make sense
alone contradict each other, and nothing in the pipeline would have said so.

## 3. The dressing is authored in plan cells

Props are placed in **world blocks**. Grok's props are in **plan cells** — `spawn-hall` at
`[[-6, 23], [6, 28]]` against a spawn piece that lives at blocks `x −15..15, z 110..135`. Multiply by
`cell = 5` and the positions are right, which is the proof of the unit rather than a guess.

That leaves houses unbuildable either way, and the two readings fail differently:

| Reading | Houses | Trees | Paths |
|---|---|---|---|
| literal (blocks) | one lands, in the wrong place — `renders/07-topdown-dressed-literal-units.png` shows the spawn hall standing at the plateau's front lip instead of on the spawn pad | off the ground, dropped | in the wrong place |
| × 5 (cells → blocks) | all dropped: `spawn-hall` covers 60 × 25 = 1 500 blocks², and `HouseProp.MaxFootprint` is 192 | all four land — `renders/06-topdown-dressed.png` | land, and the "river" runs |

Every house in both prop files is over the cap at × 5 — 400 to 1 500 blocks² against 192 — because each
was dimensioned as a room in cells (12 × 5 cells reads as a hall; 60 × 25 blocks is a stadium). **A house
past the cap is dropped in silence**: no warning, no finding, a 200 and an export with nothing in it.
That is the same class of silent loss as the empty rectangle, one pass further down.

The props also need three mechanical translations, none of which change what was authored: the document
is `{"props": [...]}` and not a bare array; a house's footprint is `wings` (a list of rectangles) and not
`points`; and `style` is the style **inline**, not a name looked up in a registry — there is no prop style
registry, deliberately, so that editing a library row can never rebuild a shipped map's scenery.

Two faults inside the styles themselves, out of three styles per file, each of which the export gate
names precisely (`DR-DOC`):

```
prop 'spawn-hall' (#0): field 'style.sill.kind' does not name a kind — expected one of solid, layered,
teamTint, voronoi, cell, noise, turbulence, electric, wallRun, wallDiagonal, checker, logChecker,
laidLog, wallFrame.
prop 'crest-cottage-w' (#1): field 'style.doorHead.form' could not be read — expected DoorHeadForm.
```

The first is `desert-hall`'s `sill` written as `{"material": {…}}` — one wrapper too many, and Grok's own
`ridge-hall` in the other file writes the same field correctly. The second is `doorHead.form: "flat"`,
which is not one of the two members (`none`, `arched`); it was read as `none` here, the member that means
a plain rectangular head. Beside those two, several hundred lines of wall courses, posts, sills, gables,
verges, window forms, beams and door heads across six styles parse without complaint.

### 3.1 The house styles are not approximations — they stamp

The styles were the part of the run most likely to be hand-waving, and they are the opposite. All six —
three per map — go through `POST /api/room-styles/preview-snapshot` and come back as buildings:
`specs/grok-ridge/style-previews/` and `specs/sandscar/style-previews/` are the studio's own plan, section,
isometric and cutaway of each, stamped from Grok's JSON with no field of it rewritten except the two faults
named above.

They also match the prose. `specs/grok-ridge/authored-by-grok/THEME.md` states the palette as a table of
block ids and calls the result "cool gray ridge stone with dark spruce timber framing and a slate-like
roof", and that is what `ridge-hall` stamps: a stone-brick base course, an andesite body, spruce-log corner
posts, an arched door head and arched side windows under a grey stained-clay roof with a ridge cap.
`desert-hall` is the same building in sandstone, end stone and brick. The three roof forms the documents
claim — gable on each hall, hip on each cottage, shed on each shelter — are the three that come out.

So the answer to "could the styles be approximated" is that no approximation was needed: the styles are
complete `HouseStyle` documents, `HouseStamper` builds them today, and the only reason no building stands
on either map is the **footprint**, which is a property of the props file rather than of the styles.

### 3.2 The unit error was a stated belief, not a slip

`THEME.md` closes with the sentence that explains the whole of §3:

> All coordinates are in the same cell space as the plan. The studio scales and seats them on real ground
> when the layout is finished / exported.

Nothing does that. A plan is the one document in cells; every other document — layout, relief, dressing —
is in blocks, and no pass rescales a prop. The belief is reasonable from the outside, which is what makes
it worth recording: an author who thinks the studio will scale will write cells everywhere and get no
diagnostic anywhere.

### 3.3 Two style fields crash the stamper when they are stated as `null`

Found by both shelters, and it is the studio's defect rather than Grok's. `HouseStyle.GableWindows` and
`HouseStyle.DoorHead` are non-nullable properties with an initializer; a JSON `null` bypasses the
initializer, and `HouseStamper.Stamp` dereferences it:

```
POST /api/room-styles/preview-snapshot   {"gableWindows": null}   500
System.NullReferenceException at HouseStamper.<Stamp>g__StampGableWindows|4 (HouseStamper.cs:361)
POST /api/room-styles/preview-snapshot   {"doorHead": null}       500
```

`"porch": null` and `"doorEdge": null` are fine — both are declared nullable — so the document reads as
though stating `null` is how a style says "not this part", and for two fields out of the four it is a 500.
Grok wrote `"gableWindows": null` and `"doorHead": null` on `wool-shelter` and `monument-shelter` to say
"no gable windows, no door head", which is exactly what `{"form": "none"}` says safely. Previewed here with
that substitution; the fix belongs in the studio, which should either read a stated null as the default or
refuse it by name the way `DR-DOC` refuses a bad material.

**The river is the run's one genuinely clever move.** Sandscar's `river-meander` is not a `water` prop —
it is a `path` prop paved with a `cell` material whose palette is blocks 8 and 9, still water and flowing
water. It reads as a river in the top-down (`renders/06-topdown-dressed.png`) and it never touches the
ground, which is what a path does.

## 3.4 The terrain themes are the one part that had to be invented

Eight theme names are written on the shapes of the two Sandscars and four on Grok Ridge —
`stone-terrace`, `stone-crest`, `desert`, `desert-pit`, `river-bank`, `savanna`, `savanna-mid`,
`savanna-hill`, `savanna-peak`, `savanna-crest` — and nothing defines any of them. A theme name is a key
into a `themes` registry plus a `mapTheme` default; neither was written, so every one resolves to nothing
and all three boards paint with the built-in default. That is the fourth instance of the run's recurring
shape: a field that reads correctly and refers to nothing.

Unlike the styles, this **could not** be recovered from the documents, because a terrain theme is not a
palette — it is which block is the rim, which is the surface, which is the exposed riser, how deep each
band runs and where the bedrock floor sits, and none of that is stated anywhere. What Grok did state is
the palette: a block-id table in `grok-ridge/THEME.md` ("andesite 1:5 body, stone brick 98:0/98:1/98:3
base and trim, spruce log 17:1 posts, path mix stone brick + andesite + cobble … cool gray ridge stone")
and one line per Sandscar README ("sandstone + endstone + birch + brick roofs", "desert → savanna
progression").

`specs/<slug>/approximated-theme.json` is those palettes written as real themes, and
`specs/approximated-themes.py` is how they were derived. **The block ids are Grok's; the bucket structure
and the band depths are not stated anywhere and are this report's.** They are kept out of `maps/<slug>/`
for that reason: the committed world is what Grok's documents produce, and the painted board is
`renders/10-topdown-material-painted.png` beside it.

Two things the painted boards show that the plain ones cannot:

**Sandscar Complex's desert→savanna progression is real, and it is in the plan rather than in the theme.**
Grok's per-shape theme names track his own shape ids, which a compile does not produce, so the assignment
here is by the one property both documents share — the height a piece stands at, with the bands his own
names describe: pit at 37 and below, desert to 41, savanna above. Sand at the river front, green on the
high ground behind, end stone in the cut pit, exactly as his README describes it, off nothing but the
surfaces he authored.

**Grok Ridge's stated palette is almost monochrome**, and the board reads flat from above because of it:
andesite, stone brick and cobble are three greys. The colour in his palette — spruce timber, grey stained
clay roofs, glass — lives entirely on the buildings, which are the one thing that did not build.

## 4. What the built boards measure

| | `grok-ridge` | `sandscar` | `sandscar-complex` |
|---|---|---|---|
| gamemode | ctw | dtm | dtm |
| extent | 140 × 220 blocks, y 13..53 | 144 × 270, y 30..82 | 204 × 360, y 31..82 |
| teams / spawns | 2 / 2 | 2 / 2 | 2 / 2 |
| objectives | 4 wools | 4 destroyables, obsidian | 4 destroyables, obsidian |
| build ceiling | 42 | 76 | 76 |
| navigable columns | 20 982 (2 364 bridged) | 28 692 (5 564 bridged) | 50 892 (4 264 bridged) |
| components | 6 | 2 | 2 |
| isolated markers | **4 of 4** | 0 of 4 | 0 of 4 |

Grok Ridge's four isolated markers are its four wool rooms, and this is the reading `FINDINGS.md` and
`review/sable-marsh.md` already record: a stamped wool cage is a walled room, and the traversability read
models ground-level walking with headroom and nothing else, so a cage reads as its own component. The
compile gate's own reachability rule — a wool must be reachable from every capturing team's spawn without
passing through a spawn piece — passed on this board. It is the documented measurement, not a fault in
what Grok drew.

## 5. What this run says about the system

**The refusals that fired were good ones.** Four bad rectangles produced four sentences naming the pieces
and the height deltas, and the wall refusal named the pair. Nothing had to be guessed.

**The silences are still where the cost is, and they compound down the pipeline.** A rectangle with the
wrong four keys covers nothing; a relief at the wrong depth is dropped; a relief in the wrong vocabulary
keeps only its base; a house over the footprint cap vanishes. None of these says anything, three of the
four are accepted with a `200`, and the one refusal that does arrive (`sketch/finish`) points at the
whole layout rather than at the shape that was empty. An author with no live API cannot find any of them,
which is precisely the situation this run was in.

**Cell-versus-block is the single biggest source of error in the run**, and it hit two different
documents in two different ways: the plan is in cells and got them right, the layout is in blocks and got
those right too, and then the props — the third document — went back to cells. A dressing document that
carried its own unit, or a gate that refused a prop whose position lies outside the map's own extent,
would have caught every one.

**Nothing about the three boards' design needed changing.** Two hundred-odd numbers were authored, four
were wrong, and all four were arithmetic. The terraces, the pit, the hill, the monument spacing, the
spawn placement, the wall, the build bands and the river are all Grok's, and they built.
