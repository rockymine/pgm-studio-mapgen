# Opus 5 — Lindenkreuz: a board authored to an outside brief, with an existing map read first

## What I set out to build

The repository's author asked for a Destroy the Monument board, in German, with eight things in it:

> Erstelle eine neue Destroy the Monument Map. Die Map sollte eckig sein. Die maps von minuyo sind ein
> gutes Beispiel und liegen in CommunityMaps. Thematisch möchten wir gerne einen Parkplatz auf der Map
> haben. Die Autos sollten 5x3 sein mit Rädern aus Kohleblöcken. Die Karosserie sollte aus
> Schwammblöcken sein. Die Fenster aus Eisblöcken. Das Dach aus Stone Slabs. Also 4 Schichten: Räder,
> Karosserie, Fenster (inkl. restlicher Karosserie), Dach. Weiterhin soll eine Littfaßsäule auf der Map
> stehen die zur Skalierung der Fahrzeuge passt. Weiterhin wird ein Klavier aus Netherbrickblöcken
> gewünscht. Weiterhin wird ein S-Bahn Tunnel unterirdisch gewünscht. Die Strecke der S-Bahn sollte zur
> Oberfläche führen und schließlich über eine Brücke führen. Häuser in dem Stil von Fox Dream (eine Map
> von minuyo).

The board I set out to build from that, written down before any shape was authored: **two rectangular
city blocks either side of a twenty-block gorge, joined by one railway bridge — a car park with the
monument standing in a marked bay, a Litfaßsäule and a street piano on the station forecourt, terrace
houses on two raised garden blocks, and the S-Bahn running out of a cut-and-cover tunnel under the whole
quarter, up a ramp in an open cutting and away over the bridge.**

90 × 200, `rot_180`, cell 5, one destroyable a team at `(∓15, ∓51)`, spawns at `(0, ∓90)`.
`maps/opus5-lindenkreuz` · `specs/opus5-lindenkreuz` · `review/opus5-lindenkreuz.md`.

## Reading a map that already exists

The brief named two references that are not in this repository — minuyo's boards in
`CommunityMaps`, and *Fox Dream* in particular — so the run began by reading one rather than by
authoring anything.

**The studio's own import route could not take it.** `POST /api/map/import-folder` resolves
`<root>/<slug>/region` through `MapsRoots` and requires "a real candidate (region/*.mca, **no map.xml**,
not already a map)". The two configured roots are `CommunityMaps/ctw` and `PublicMaps/ctw`;
*Fox Dream* is `CommunityMaps/dtcm/fox_dream` and carries a `map.xml`.
`GET /api/maps/import-candidates` answers `[]`. That is the route working as specified — it exists to
open an xml-less world folder — and it is not the way to read a finished community map.

**The world tools were.** `tools/anvil.py`, landed with `REVAMP-BRIEF.md`, reads an Anvil world in the
standard library alone, and everything below came off it in about a minute:

| Read | What it said about *Fox Dream* |
|---|---|
| `anvil.py <region>` | 415 chunks, 326 459 non-air blocks, bounds `(−99, 0, −93) … (52, 106, 93)` |
| `probe.py` | body materials `clay:9, emeraldore, mossy, prismarine, stone, stone:5, stone:6`; mean run down a column **10.25** blocks — a body laid in long vertical runs, not a mixed volume |
| a surface census | **podzol 4 651 columns, grass 3 533, water 5 716** — the ground is podzol, not grass |
| a top-down ASCII off `World.columns()` | a `rot_180` board with a lake down the middle, trees everywhere, houses on both flanks |
| a section through a house at `x = 40, z −63..−49` | walls of stained clay with brick, plank floors, **jungle-stair roofs**, a clay chimney |

That is what `@lk-terrace` is a fork of: brown stained clay over two courses of brick, dark-oak log
posts, a jungle-plank gable stepped in jungle slabs with a spruce verge, glass panes. Not a copy — the
house sits on a raised garden terrace in a city rather than in a wood — but the palette is measured off
the original rather than remembered.

**One picture was worth the four reads put together.** `CommunityMaps/dtcm/mole_dream/map.png` is what
"eckig" means: terrain built out of stepped rectangular masses with sharp edges and flat tops, no
rounding anywhere. That is one screenshot, and it decided the board's single largest technical decision.

## The decision the rest of the board follows from

**The board carries no `relief` at all.** Every height on it is stated: the plan's per-piece `surface`,
an authored shape's `base_height`, a ramp's `anchor_heights`. Four surfaces on the whole map — y8
trackbed, y10 platform, y19 city, y23 terrace — and every face between them sheer.

Two things follow, and the second is the one that mattered:

1. It is what makes the board angular. A relief is a solver and a solver rounds; `AUTHORING-BRIEF.md`'s
   ruling that "a landscape board is a small plan and a large relief" is right for a landscape and is
   exactly what this board must not be.
2. **Every surface height is known at authoring time**, so a made thing can state an absolute floor.
   `SCULPTING-WITH-LAYERS.md` §5 and `tools/sculpt/make_board.py` both record the opposite problem — a
   prop states an absolute floor and a relief moves the ground under it, so `opus5-automaton` had to be
   built on a flat board for its sculptures to seat. Here flatness is the brief rather than the price of
   it, and thirty cars, two Litfaßsäulen, two pianos and eighteen lamp posts all state `floor = 20` and
   land on the tarmac.

The cost is `EL1` six times: the plan tier walks its pieces flat, so the six seams where a terrace at 24
meets ground at 20 read as four-block steps, and the evaluator asks for relief line marks. The layout
answers all six with an authored tilted quad at better than 2:1. The complaint is correct at the tier it
reads and wrong about the world, and nothing can tell it so.

## What I could not say

### `import-folder` cannot read a finished community map

- **Wanted**: to put `CommunityMaps/dtcm/fox_dream` through the studio's own reads — `render/section`,
  `themes/census`, `transect` — rather than through a hand-written ASCII dump.
- **Tried**: `GET /api/maps/import-candidates` → `[]`. `POST /api/map/import-folder` requires a slug
  under a configured `MapsRoots` entry with **no `map.xml`**.
- **Checked**: `openapi.json`, `POST /api/map/import-folder`'s own summary — *"The slug must be a real
  candidate (region/\*.mca, no map.xml, not already a map)"* — and
  `src/PgmStudio.Api/appsettings.Development.json`, whose `MapsRoots` are `…/CommunityMaps/ctw` and
  `…/PublicMaps/ctw`.
- **Verdict**: **not missing and not unreachable.** `import-folder` is the "open a local folder" source
  for a world that is not yet a map; a finished map with an xml is the *other* half of the pipeline
  (`import-url`, or the xml importer). What is genuinely absent is a route that takes a **complete**
  PGM map folder and makes it readable through the studio's own analysis reads. That is worth filing as
  a studio task, and it is a feature request rather than a defect: the world tools do the reading, and
  they did it in a minute.

### A goal name reaches a player verbatim, and there is no way to check that from the API

`AUTHORING-BRIEF.md` says so; nothing in `GET /api/rules` does. "Parking Meter" is a name that reads on
both teams, but the only oracle for that is reading the brief.

## How I looked at it, and what that cost

**I looked at pictures, and where I wanted a number I wrote my own reader instead of opening the one the
drive had already written.** Over seven builds I opened `world-topdown.png`, `world-ground.png`,
`world-surface.png`, `world-iso.png`, `world-xray.png` and the house previews; of the twenty-five text
reads the driver writes beside them I opened exactly one, `05-themes.txt`. Everything else I wanted in
numbers I got out of a scratchpad script — an ASCII section renderer over the Anvil world, a surface
census, a column probe — every one of which is a worse copy of something `?format=text` already answers
at any extent. The board was **built, exported and written up** before I read `03-slopes.txt`.

It cost a fault that shipped in five consecutive builds. `03-slopes.txt` flags it in one line:

```
 -27 ..................................##:..:...:..:........##.................................
```

Four `:` — scramble, rise 2 — inside the cutting at `x −9, −6, −2, 1`, which are the four rails, and the
same four again at `z −21..−20`. `transect?points=-9,-36;-9,-10` says it in prose:

```
x -9  (the rail line)  rises 8,  worst step 10: 2 scramble — scramble +2 at (-9, -26); +2 at (-9, -20)
x -8  (the ballast)    rises 11, worst step 11: 0 scramble
```

The cause: the rails up the ramp were drawn in **three-block segments at a rounded height**, and the ramp
under them steps once every two blocks, so a rail stood a course proud wherever a step fell inside a
segment — and a rail one course proud beside ground one course lower is a two-block rise a player has to
place a block to cross. `02-heightmap.txt` shows the same thing as a different digit under each rail:
`c010010001001000000000c`.

The fix is to draw one rail block per z column at the ramp's own height, floored rather than rounded —
`int(TRACK + t·(CITY − TRACK)) − 1`, checked against all 25 stations of that transect. Rebuilt, the
trackbed reads `000000000000000000000` / `111111111111111111111` straight across, the rail line transects
**11 rises, 0 scramble**, and the board's scramble count falls from **152 cells to 120**.

**Nothing in any picture shows this.** A one-block bump under a rail is one shaded pixel in a heightmap
and invisible in an isometric, a top-down and an x-ray alike. It is a number, and there were three files
sitting in `renders/` with the number in them.

Two more things the text reads gave me that no picture had:

- **`06-claims.txt`** — the goal's clearance is a literal 21 × 21 block of `9` at `x −25..−5`, with no
  `3`, `4` or `b` anywhere inside it: the nearest car is 24 blocks out, and the pass placed 60 props and
  declined 0. That is the `OB19` question answered by lookup rather than by a build.
- **`world-section-z0.txt`** — the gorge and the bridge in one cut: 21 columns of void from bedrock to
  y16 with a three-course deck over them, and the ramp's wedge climbing into it. Its ruler is **z**,
  not x, which is worth knowing before reading it: `axis=z` names the direction the cut runs, so `at` is
  the x.

## What I got wrong

**`plan: 1` was the version I copied.** Every spec in `specs/` that I looked at first —
`opus5-slipway`, `opus5-undercroft` — states `"plan": 1`, and I wrote the destroyable's `at` in cells to
match, because `opus5-slipway`'s `at: [10.75, 11.5]` × cell 4 lands exactly on its built
`car-park-region min="43,26,46"`. The compile refused: *"this plan states version 1; this build reads
version 2 — marker offsets are blocks from the piece corner, and version 1 stated them in cells."* The
wrong claim looked right because **a version-1 spec in this repository is evidence about the day it was
written, not about the API today**, and the two disagree by a factor of the cell size. The refusal is a
model of what a refusal should be: it names the units both ways.

`DestroyablePlacement.at`'s own description still says *"an \[x, z\] offset in **half-blocks**"* and
`PlanPlacements`' says *"Positions are piece-relative cells"*. Neither is version 2's answer, which the
refusal gives correctly. Worth a docs fix.

**I stated a whole theme for a painted line.** `line`, `warnline`, `coping`, `stage` and `steel` were
written with one block in all five buckets — which is right for a made thing, since a car is sponge all
the way through, and wrong for paint. A theme owns a **column**, so the bay markings painted their
columns white from bedrock: measured at `x = 19, z −64..−60`, fifteen courses of white stained clay from
y5 to y19. The fix is one line — the marking in `surface`, stone in `wall` and `fill` — and the fault is
invisible from above and obvious in a section.

**I put a railing on the wrong layer, twice.** The light well's rail as an override add on the *ground*
layer at `floor: 20` re-filled the tunnel it stands over: an override add keeps "the ground under its
floor" where the ground's own span reaches that floor, and the span it reads is the **plain** add — the
city polygon at top 20 — not the trench override that cut the column. 36 columns of solid rock where the
platform should have had a ceiling, `SK10` naming it exactly. Moved onto the lid as a shape at `floor:
3` it then stacked on the deck, and a layer holds **one span per column**: `SK9` declined the deck out of
the world under it. The answer is that a rail on a deck is the deck **plus a course** — one shape,
`floor 0`, `base_height 4` — and the taller shape simply keeps the column.

**I marked the tunnel mouth and made the fall worse.** A coping course across the portal at `z −36`
stands on the lid, so it hit the same override rule (42 columns, `SK10`), collided with the rails on the
theme scope (`SK15` × 4), and deepened the drop it was drawn to mark from 11 courses to 12. Taken out
again. The mouth of a tunnel is meant to be a hole.

**`GENERATION-NOTES.md` is wrong about cross-layer paint, and it cost me a wrong design.** It says *"Theme
scope is 2-D. `ShapeThemeOwners` gives a cell to the smallest-area themed shape covering it across every
layer, so an upper shape's theme owns the ground beneath it too."* I designed the trench's paint around
that, splitting it into twelve-block segments so it would stay smaller than the lid over it.
`SketchRasterizer.ShapeScopeOwners` keys `owner` on `(layer, x, z)` and says so in a comment: *"a cell
covered on two layers is not contested at all, because each layer shows its own surface."* The note is
out of date. The consequence runs the other way and is the real fact: **a marking drawn on the ground
layer does not appear on the lid**, and every bay line that crosses the tunnel roof has to be drawn
twice.

## What worked first time

- **The trench.** An override add with `height_mode: "level"`, `skirt: 0` and `relief_scope: "exclude"`
  cut 21 × 45 blocks eleven courses into ground a plain add had already claimed, first try, exactly as
  `GENERATION-NOTES.md` describes it.
- **The ramp out of the cutting.** One tilted quad, `anchor_heights` `[9, 9, 20, 20]` over 24 blocks for
  11 courses. The section down `x = 0` reads a clean diagonal from y8 to y19 and the walk climbs it for
  nothing.
- **The switchback stair.** Nine per-course rectangles in two flights, the break placed where the lid's
  soffit leaves less than three blocks of headroom. Right the first time it was built, off arithmetic
  alone.
- **The bridge.** A plain add with `floor: 17` over void; the column is the deck and the air under it,
  and over the land at either end the taller add keeps the column so the deck runs into the cutting's
  shoulder rather than standing on it. No bedrock plate, because it is a shape on the ground layer
  rather than a layer of its own.
- **The car.** `tools/sculpt/layers.py` compiled a 42-block model into **exactly four layers**, one per
  course, because it decomposes by run index and a car's worst column passes through a wheel, the body,
  a window and the roof. The brief asked for four layers and the compiler produced four without being
  told to.
- **`GO1` at 3.51 on the first plan that stated its `at` in blocks**, from arithmetic done before any
  shape existed: with the doors `L` apart and the goal `d` along the lane, the ratio is about
  `(L − d)/d`, so `L = 180` and `d = 41` is 3.4 before the pieces are drawn.

## Open gameplay questions

**The viaduct is a land connection, and the brief rules against one.** `AUTHORING-BRIEF.md` §3: *"the
two teams' ground is joined by a build zone over void spanning the board's whole width, never by a land
connection: a corridor is a place a defender stands."* This board has a bridge, because a railway that
stops at a chasm is not a railway and the brief also asked for one. What I built instead of obeying is a
*choice*: the deck is 19 blocks wide against a 90-block frontline, it is on the line to neither monument,
and it is the only place on the board where both teams stand in the open at the same height. Everything
else is still a bridge somebody builds — the plan's one build zone spans the whole width. **Decided,
built, and recorded here rather than filed as a fact.** It wants a match.

**An eleven-course fall at the tunnel mouth is on the shortest route.** `spawn-red → destroyable-1-1`
drops 11 blocks at `(0, −35)` straight off the car park into the trackbed, because the walk prices a fall
at nothing. In game it is a choice between damage and a detour round the cutting, which is the kind of
decision the cutting exists to create — but the walk read makes it look like the intended route, and it
is not.

**15.9% of the ground is dead, and it is the frontline's two flanks.** Four patches of 238 cells at
`(±37, ∓18)` and `(±36, ±16)`. Every computed route crosses at the bridge, so a 90-block frontline is
used over the 20 in the middle. Coverage cannot see a bridge nobody has built yet; whether that means the
number is wrong or the board is, a match decides.

## The order this board has to be built in

For anyone rebuilding it: `specs/opus5-lindenkreuz/build-spec.py` writes both documents and
`tools/drive.py` does the rest.

```bash
python3 specs/opus5-lindenkreuz/build-spec.py
python3 tools/drive.py specs/opus5-lindenkreuz "Lindenkreuz" --out maps/opus5-lindenkreuz
```

The one ordering that is not obvious: **`addLayers` puts the lid after the compiled ground and before
the made things**, and the painter now orders layers by the lowest surface each carries rather than by
document order, so the bottom-up rule `GENERATION-NOTES.md` states is enforced by the studio rather than
by the author. What still has to be right by hand is that the lid is a *layer* and the trench is an
*override add on the ground layer* — swap either and the tunnel is solid rock.
