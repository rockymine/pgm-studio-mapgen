# Revamp brief

The studio builds a board. A person finishes it in game, with WorldEdit and Arceon, over hours. This brief is
the loop that turns the finish back into documents: read the two worlds against each other, name what every
command did, find which of it the studio can state, state it, build a new board with it, and write down
what could not be stated. It was run once, on Millrace, and every step below cites where that run's result
is, so a step can be checked against a worked example before it is run again.

It is read after [AUTHORING-BRIEF.md](AUTHORING-BRIEF.md), which is how a board is authored from nothing;
this is what happens after a person has touched one. The tools are in `tools/` and documented in
[tools/README.md](tools/README.md).

---

## 1. Before the hand work: the board has to be reproducible

The whole read rests on one property: the studio rebuilds its own board the same way twice. Only then is a
difference between the studio's world and the person's a statement about the person's work.

- The board is a spec in `specs/<slug>/` driven to `maps/<slug>/`, with `specs/<slug>/provenance.json`
  beside it. The sidecar records which pass claimed each column (ground, structure, made thing, prop) and
  which prop; it is what the diff keys on. Commit all of it before the world is handed over.
- The person edits **a copy** of `maps/<slug>/` and commits it as `maps/<author>-<slug>/` — `region/`,
  `level.dat`, `map.xml`, nothing else — with their own account of the work as
  `review/<author>-<slug>.md`, carrying **every command in the order it was run**. The command list is the
  half of the read a diff cannot recover: a diff says what the blocks became, and the list says what was
  asked. `review/rockymine-ruediger-millrace.md` is the shape.
- Trees, statues, boats: anything pasted in from elsewhere is committed as the world it was pasted from,
  under `showcase/` (`showcase/tree-showcase` is 74 trees on platforms), so the paste can be matched back
  to its original rather than guessed.

## 2. The control: rebuild the original and diff it against itself

```bash
python3 tools/drive.py specs/<slug> "<Name>" --out /tmp/rebuild
python3 tools/world-diff.py maps/<slug>/region /tmp/rebuild/region --things 20
```

The drift this reports is what the studio itself moves between two builds. On `opus5-millrace` it was
**0.4%** of cells, every one a grown tree, a spawn hall's shell or a croft under a building programme that
changed since — not one column of ground, water, wall, bridge, boulder or cairn. Write the number and what
it is made of into the review before anything else; the diff against the hand work is trustworthy exactly
where the control moved nothing. A control that moves terrain means the studio changed under the board,
and the read has to be taken against a rebuild rather than the committed world.

## 3. The diff: two worlds, one provenance

```bash
python3 tools/world-diff.py maps/<slug>/region maps/<author>-<slug>/region \
        --provenance specs/<slug>/provenance.json --json specs/<new-slug>/diff.json
```

Read the sections in the order they print.

**The surface.** How many columns kept their exact height, trees ignored. On Millrace 29,954 of 35,610
did, and that one number is why the rest could be read as substitution: the person themed the studio's
ground rather than reshaping it. A revamp that moved the ground is a different read — the things section
carries it, the substitution table does not.

**Substitution by pass and depth.** For every unmoved column, what each block became, grouped by the pass
that laid it and its depth under the surface. This is where the patterns fall out as numbers: the surface
mix, how many courses of earth and of what, the body's stones and their shares, which masonry changed and
which did not. Each row is one command in the person's list; put them side by side. Millrace's table and
the command each row came from are in `review/fable-millrace-revamp.md` § *What the hand work did*.

**Things added and removed.** Every body one world has and the other lacks, 26-connected, with a bounding
box and a census, largest first. Builds, fills, removed structures and replaced trees all land here with the
coordinates a lift needs. Read the largest ones first and ask what each *is*; on Millrace the four largest
were not decoration but 25,000 blocks of fill under walls the studio had left standing on void, which was a
studio bug (`TS77`) and not a design decision.

**The four targeted reads** — the bed under the water, the plants and what they stand on, the biomes, and
the exposure of each material — are the reads that turned out to be asked of every revamp, so the tool
takes them without being asked.

## 4. The commands, and the studio's word for each

For every command in the person's list, find its row in the diff and the studio's way of stating it. The
correspondences found so far, so they are not derived twice:

| WorldEdit / Arceon | the studio's word |
|---|---|
| `#vor[n][…]` of `#turb[m][…]` through wool placeholders | one `cell` material whose palette is `turbulence` materials, each with a `rise` — the placeholders were how WorldEdit nests, and the studio's materials nest natively |
| `//replace #below[2,3][3] #frac[4][…]` | a `layered` surface, the top mix one course over the earth mix three |
| `//gmask 2&#below[air][1]` · `#frac[4][…]` | a theme's top band as a `noise` at scale 4 |
| `#cell[4][…]` on a wall | a theme scoped to the wall's shapes, and nothing else |
| `//brush boulder` | a boulder recipe whose `rock` is a `noise` of the materials |
| paths brushed in blobs | `stroke` props with the mix as `pave`, `rough` edge, `route: true` |
| `//s #frac[4][0,31:1,31:2,175:3]` over grass | `flora` props, coverage and fern share from the diff's plant read |
| biomes as `#vor[8][#biome…]` | the layout's `biome` as a `cell` field over a palette — one level of nesting where the command has two |
| pasted trees | `copied` tree recipes (§5) |
| pasted or built structures | made things on layers (§6) |

**A pattern is a plane until it states a `rise`, and a cell as tall as it is wide is a column.** WorldEdit's
patterns are volumes by nature; the studio's sample the plane by default (`TP15`), so a body stated without
a rise builds as vertical stripes on every cut face. State the body's cells wider than tall — nine across
and five tall over turbulences seven across and four tall is measured — and the earth the other way, three
courses deep with a tall rise so its mix shows across the ground. `probe.py` is the number for it (§8).

## 5. The trees

```bash
python3 tools/trees.py catalogue showcase/<trees>/region
python3 tools/trees.py match showcase/<trees>/region maps/<author>-<slug>/region --against maps/<slug>/region
python3 tools/trees.py bodies showcase/<trees>/region --row <z>=<prefix> [--row …] --out specs/<new-slug>/trees.json
```

`match` finds, for every tree body the person's world has and the studio's lacks, which catalogue tree it is
on leaf shape alone under the eight symmetries of the square, so a paste with a rotation is still found; a
score of 0.99 or better is the same tree, and a lower score with a body two or three trees large is a grove
that grew into one. `bodies` cuts the rows used into the `trees.json` a spec reads; the studio side is
`pgm-studio/tools/seed-trees.cs`, which cuts the same trees straight into the library. A `copied` recipe
carries the body block for block and is placed like any tree: seated on its foot's column, turned round the
symmetry with its logs and stairs turned, every leaf written no-decay, its footprint claimed.

Two facts from Millrace: the person extended each oak's trunk by four to thirteen logs to reach the ground
where a paste at fixed height left it short, which a copied tree does not need because it seats on its
foot; and the only per-block difference between a paste and its original is the game's leaf check bit,
which `match` ignores.

## 6. The builds

```bash
python3 tools/lift.py maps/<author>-<slug>/region <name> --box x0 y0 z0 x1 y1 z1 \
        --against maps/<slug>/region [--ground-below <y>] --out specs/<new-slug>/models --cost --plan
```

Take the box from the diff's things table. `--against` keeps what the person added; `--ground-below` drops
the terrain a footing stands in; `--cost` says what the thing costs as layers and shapes, which is the
number that decides whether to carry it: a colour change in a column is a run and every run is a layer, so
a statue is 8 layers and 402 shapes and a tug 11 and 405, while a beacon frame is 7 and 63. In a spec's
`build.py` the model becomes `addLayers` through `tools/sculpt/layers.py`'s `compile_layers`;
`specs/fable-millrace-revamp/build.py`'s `model()` and `made()` are the worked example, including a
recolour for a team-coloured thing stated twice (`WE74`), a turn to move a thing, and the six-by-six cut
out of the balloon's basket for the observer platform the studio stamps at the centre.

## 7. The restatement, and the new board

Two boards come out of a revamp. The **restatement** is the original's own layout and intent, re-themed and
dressed with what the diff found: `specs/fable-millrace-revamp/build.py` reads `specs/opus5-millrace`'s
documents, re-themes the ground shapes, drops what the person removed, appends the made things and states
the props. The **new board** is the same techniques stated from the first drive on a layout of its own:
`specs/fable-mossgill/build.py` is five plan rectangles and a finish. Write the new board's `build.py` from
Mossgill's rather than from nothing; it carries every correction the two Millrace builds taught, and the
list is short enough to check:

- the body as cells wider than tall with a rise, the earth as a depth stack with a tall rise (§4);
- a `scarp`'s shelf is on the +z hand of the direction its lip is traced — south of a line traced west to
  east, north of one traced east to west;
- an override add standing in ground keeps the ground under its floor (`TS77`), so a wall states a floor a
  few courses under the ground it stands in and leaves no shaft;
- a theme is scoped by shape and the smaller shape wins a contested cell, so a bed under water is a polygon
  at the bank's own height carrying the bed theme and no geometry;
- every prop keeps 21 blocks off a goal (`OB19`) and off a spawn's ground, out of the lane in front of a door,
  clear of a water prop's bed, three blocks beyond a road's band, and a block beyond a house's footprint;
- a house at a bench's edge raises `WX11` for the face its foundation fills; give it a bench of its own with
  an `area` mark held flat;
- on half a box the three goal bands cannot all hold at the plan tier (`GENERATION-NOTES.md` has the
  arithmetic); take the ratio and let the built board decide the walk.

## 8. The loop, the drive, and the reads that check it

```bash
python3 tools/drive.py specs/<new-slug> "<Name>" --out maps/<new-slug>     # once, so the intent is stored
python3 tools/loop.py specs/<new-slug> --candidates <propId> x,z x,z x,z    # twenty seconds a pass
python3 tools/loop.py specs/<new-slug> --profile x=30,z=-30..30 --column 0,0
python3 tools/drive.py specs/<new-slug> "<Name>" --out maps/<new-slug>     # the real drive
python3 tools/probe.py maps/<new-slug>/region --floating
python3 tools/trees.py verify maps/<new-slug>/region specs/<new-slug>/trees.json
```

Drive once so the map exists, then iterate through `loop.py`: it posts the compiled, patched layout to the
relief read and the dressing preview without storing anything, and `--candidates` answers a placement
question for eight positions in one pass. Drive again when the loop is clean. Then read the world back:
`probe.py` for the body's run lengths (a mean under three blocks is a blob; the first Millrace build was
stripes) and the floating columns classified by what stands on them; `trees.py verify` for every copied
tree block for block and every leaf no-decay; `world-diff.py` of the restatement against the person's world
if the question is how close the restatement came.

## 9. What the review says

One `review/<agent>-<slug>.md` per board, in the shape of `review/fable-millrace-revamp.md`: the control;
the substitution table with the command beside each row; the things added and removed with coordinates;
the trees matched; the commands and the studio's word for each; **what the studio cannot state, each one
tried on the build and named by what happened**; what the build says (declines, complaints, coverage, the
export gate); and what to look at, as `column?at=` and render URLs. A finding that became a rule goes into
`GENERATION-NOTES.md`; a gap goes into `pgm-studio`'s `BACKLOG.md` under an id whose prefix names the
document it obliges; a README row per board. What could not be stated on Millrace is the numbered list in
its review, and three of those are filed (`WE73` rocks in water, `WE74` team-coloured made things, `TS79`
`SK18` per course); the largest gap is unfiled because it is a capability rather than a defect: the grain
of a block on a block — chimneys, pots, slabs at every rise — that a person places in a second and that
reads, from the ground, as care.

## 10. Operational notes

- **In a cloud container neither MariaDB nor the API survives the session idling.** Start both at the
  beginning of a turn's work — `sudo service mariadb start`, then `bash tools/dev.sh restart` in
  `pgm-studio` with `ConnectionStrings__PgmStudio` exported as `docs/cloud-setup.md` says — and expect to
  start them again after a pause. A drive against a dead API is a connection refused on the first call,
  not a partial build, and an API started without the connection string aborts at once.
- The API must be restarted after a change to `Export`, and a drive gives no hint that it was not.
- `dotnet run <script>.cs` caches the built script against old `src/`; `rm -rf ~/.local/share/dotnet/runfile/<script>-*`
  before measuring a studio change.
- `GET /map/{slug}/column?at=x,z` answers text, not JSON. `loop.py --column` is the JSON read of the same
  thing off the preview.
- A drive is about ten minutes on a 260 × 250 board, five on 130 × 120; a loop pass is twenty seconds; the
  world tools read a million-block world in seconds and diff two in a minute.
