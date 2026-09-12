# Coinfall — the first board with a shop in it

The studio grew shops this run: `PUT /map/{slug}/intent` takes a `shops` array, the export writes the
`<shops>` menu and a `<shopkeeper>` at every team's spawn, and a map that carries either now parses, stores
and re-emits instead of losing it. Coinfall is the first board built through that. The report is about the
four things it taught — one about where a keeper goes, one about what a shop board needs that this one cannot
state, one about why a path drawn on the ground painted nothing, and one about a room that is a block out of
true.

## What the board is

Each team's ground falls in three steps and faces a neutral holm across a void. The camp and the long run sit
at **y20**; the wool's plinth is raised to **y25** at the far east end of the run and is climbed rather than
walked onto; the bank against the void drops to **y17**, and the only ways back up from it are the two flights
cut into the seam. The middle is a third island at **y18** with a crown at **y23**, four brick stumps standing
where the crown gives out, and a birch on the grass at each end of it.

```
       z −80  ┌──────────┐                          camp (spawn hall), y20
              │   camp   │
       z −65  ├──────────┴──────────────┬────────┐  run y20 · plinth (wool) y25
              │           run           │ plinth │
       z −50  └──┬──────────────────────┴──┬─────┘
                 │         bank            │        y17 — the frontline is its far edge
       z −30     └─────────────────────────┘
                 ─ ─ ─ ─ ─ void ─ ─ ─ ─ ─ ─         the ford: 20 blocks, buildable from the first tick
       z −10     ┌───────────────────┐
                 │   holm  (crown)   │              y18, crown y23
```

`rot_180` fans the lot. 28 × 32 cells = **140 × 160 blocks**, 12 a side, `cell: 5`. The frontline stands
**20 blocks** off the holm by the plan, and 21–22 as built once the coast is bent inward — every cut of a
`side: "in"` bend takes ground away from the island, so the stated number is the closest the two ever come.

The run is deliberately lopsided: it reaches 25 blocks west of the camp's centreline and 50 east, so the wool
sits at the end of a walk rather than beside the spawn. The plinth's flight is **the whole of its front** —
fifteen wide, five courses over twelve blocks — because a narrower one stands proud of the run on both cheeks
and puts a four-block step beside itself (`RL3`). The two down onto the bank are narrower and drop three.

Every cut face is read in **registers** rather than in one pattern. A board that drops twenty courses in one
go and paints all of them the same way reads as a texture rather than as a wall, so the face is banded by
depth from the top of its own wall bucket: **seven courses of the diagonal** under the rim, where a player
standing above the drop actually meets it; a **two-course string** — a cobble cornice and a course of polished
stone — closing that register; and below it a **vertical run** whose stripes stand as pilasters and wrap the
whole perimeter, holding everything down to bedrock. The team's colour appears in both, as one narrow stripe
in the shear and as the run's pilasters, so which ground stands above you is readable from either register.
The holm is the same construction with the shear leaning the other way, gravel where a camp has clay and no
tint anywhere — which is the whole of what says the middle is nobody's.

Read down the frontline face at `column?at=0,-31`: cobble rim at `y 16`, the diagonal `y 15…9`, the cornice
at `y 8`, polished andesite at `y 7`, and the run from `y 6` to bedrock — which across the face at
`x −8…12` cycles stone, red clay, cobble, red clay, six and two and three and two wide.

## The keeper carries no position, and that is the whole placement rule

The finish states the menu and says nothing at all about where the villager stands:

```json
"shops": [{
  "id": "quartermaster",
  "keeper": {"name": "`6`lQuartermaster", "mob": "Villager"},
  "categories": [{"id": "kit", "material": "gold ingot", "name": "`6Supplies", "items": [ … ]}]
}]
```

A shop is a catalogue rather than a place. The studio puts one keeper per shop at **every team's spawn**, on
the spawn's own floor, beside the point players arrive on and turned to face them, with blocks counted from
the block the spawn point stands in. The two it emitted:

| keeper | spawn point | stands at | faces |
|---|---|---|---|
| red | `0,20,-72`, yaw 0 (+z) | `2.5,20,-71.5` | yaw 90 (−x) |
| blue | `0,20,72`, yaw 180 (−z) | `-1.5,20,72.5` | yaw −90 (+x) |

Both are two blocks across the way the team faces, on a block centre, at the spawn's own height, and
`column?at=2,-72` and `column?at=-2,72` both answer a stone-brick floor at `y 19` with the hall's storeys
above it — each keeper stands inside its team's hall. Nothing is stamped for either: PGM spawns the entity
itself at match load and freezes it, so a shop board exports the moment its intent is stored, with no world
build to wait for.

## The board mints no currency, so the shop is priced in wood

Everything a player holds on a generated board comes from two places — the spawn kit `TeamsGenerator` writes,
and the kill reward `MapStandards` derives from that kit's own blocks — and **neither pays in anything a shop
would normally charge**. Of the corpus's 907 shop icons, 764 are priced in a material no spawn kit carries:
emerald 225, nether star 126, gold ingot 118, gold nugget 86. A first draft of this board priced its menu in
gold nuggets and would have shipped a villager nobody could open an account with.

So Coinfall prices everything in **wood**: 64 in the kit, 16 more a kill, and the menu trades it for the
things a wool run actually needs — a gapple at 16, arrows at 8, ladders at 8, the team's own stained clay at
12, iron bars at 24. That is a real economy rather than a workaround (the corpus prices a third of its upgrade
ladders in the tool they replace), but it is a narrow one, and the reason it is narrow is filed as `PG14`:
the intent has no way to say what a kill pays or what a block drops.

## A path paints where it reaches the ground the *shapes* draw

The two brown ways out of each camp — one east along the run and up the plinth's flight to the wool, one south
down onto the bank and out to the frontline — were first authored the obvious way: a `polyline` with a
`theme` and a radius, and nothing else. They painted **nothing**, in silence, and the coarse dirt that looked
like a path in the render was the holt theme's own 10–20° slope band on the ramp beside it.

A cell's theme goes to the smallest-area shape that **reaches the ground stated there**, and the reading is
taken against the ground the shapes draw rather than the one the relief later carves. A stroke with no `floor`
and no `base_height` is one block thick, so its top is 1 against a terrace stated at 17, 20 or 25, and it
never wins a cell it covers. Stating the terrace's own height is the whole fix:

```python
"floor": 0, "base_height": RUN_Y,   # 20 — the run's own surface
```

Its own height changes nothing about where the way ends up, because the relief owns the ground once a group
carries one: both ways follow their flights down exactly as the ground does, and the one that crosses the
bank at y17 is painted there too, because 20 is *at least* the 17 the bank states. The ways now hold **660
cells, 9.8% of the board**, with a 412-cell border against the meadow.

## A room's stamp is a block out of true on its mirror image

Read while checking the keepers were under cover. The two camp pieces are exact mirror rectangles and the
mirror gate passes on them, but the halls stamped inside them are not images of one another:
`column?at=2,-72` tops out at `y 38` where its image `column?at=-2,72` tops at `y 40`, and `column?at=0,-68`
is open grass where `column?at=0,68` carries roof at `y 32`. The frame is measured from the piece's own
minimum corner and `rot_180` maps that corner onto the image's maximum, so everything the stamp does not
centre lands a block off on the far team's copy. Filed against the studio as `WE121`.

The mirror check does not see it: it compares regions, and both rooms' regions are exact images. Only the
blocks disagree.

## The reads

```
03-slopes.txt   6646 walked, 0 scrambled, 80 barrier; faces 4, largest 20 at x −9..−5 z −8..−4
05-themes.txt   4 themes over 6726 cells: holt 68.8% · holm 12.5% · track 9.8% · plinth 8.9%
06-claims.txt   placed 26, declined 0
04-routes.txt   all four spawn → wool walks read "walked end to end", worst step 0
coverage        reached 6674 of 6850, dead 176 = 2.6%, in two 88-cell patches at (±18, ∓43)
01-flow.txt     attacker 160 blocks to the wool, defender 66 — ratio 0.41, one way in
preflight       2 teams · 2 wools · 16 regions · 34 filters · 11 apply-rules — export gate OPEN
```

The 80 barrier cells are the four stumps of the ruin on the holm, which are cover and meant to be climbed
round. The two dead patches are the far corners of each bank, past the last flight; at 2.6% they are not worth
cutting the board down for.

## Rebuilding it

```bash
python3 specs/opus5-coinfall/build-spec.py
tools/drive.py specs/opus5-coinfall "Coinfall" --out maps/opus5-coinfall --renders specs/opus5-coinfall/renders
```
