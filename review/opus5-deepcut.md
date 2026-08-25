# Deepcut — a chalk quarry, and the terracing that ruined a hillside

> A small destroy-the-monument board. Chosen rather than briefed, to answer a question the last
> landscape raised: `tarnfell` came out as stacked plateaus with vertical faces and had to be
> rebuilt. **What is that terracing actually good for?**

**In one sentence:** one chalk pit worked down in six benches, its floor a Z of two working faces
joined by a flooded neck, and standing in each face under its own team's rim a spire of unquarried
chalk with the monument four blocks over its crown.

**72 × 128 blocks**, `rot_180` about the origin, one landmass of **4,736 cells**, ground from **y12
to y40**, symmetry error **0**.

## Four marks, one knob

Every bench on this board is the **step quantum**, not a mark. The relief states four heights and
nothing else:

| Mark | Kind | Says |
|---|---|---|
| `downs` | area | the plateau, z ≥ 41, at **y40** |
| `lobe` | area | this team's working face, `(-25, 14) → (1, 36)`, at **y16** |
| `neck` | area | the floor through the seam, `(-9, -14) → (9, 14)`, at **y16** |
| `sump` | area | the pool in it, `(-7, -6) → (7, 6)`, at **y12** |

The relaxation solves a smooth bowl between them. Then:

```
"step": 4, "stairs": true
```

`step` snaps the finished surface to a four-block quantum, which turns the bowl into concentric
benches with a four-course riser between each — **six of them**, from y16 to y40. `stairs` then cuts
a way up out of every place that terracing stranded, so the pit is walkable without stopping being
terraced. `RIM_Y`, `FLOOR_Y` and `SUMP_Y` are all multiples of four, so none of the three is rounded
away by the knob that shapes everything between them.

`tarnfell` needed thirty marks and got plateaus it did not want. This board wanted the plateaus and
took four marks and a number.

## The floor is a dumbbell, because both monuments were the same distance from both spawns

A pit whose floor is a disc in the middle of the board is symmetric in a way that ruins it: the first
build read `GO1` at **2.08**, because each monument sat as far from the team defending it as from the
team attacking it. Two lobes, each worked back under its own team's rim and joined by a neck through
the seam, is how a two-faced quarry actually reads *and* where a defended goal belongs. The lobe is
authored once and the fan draws the other, so the floor comes out as a Z through the board.

| | Built |
|---|---|
| own team's walk to its monument | **34** |
| the enemy's | **99** |
| ratio | **2.91** |

## Twelve blocks of plateau before the lip

The spawn first sat at z 42 — one block of flat ground outside its own door, and then the pit. That
put `GO1` at 3.35, inside its band, and it was the wrong thing to spend a spawn's frontage on: a
player walked out and fell in.

The room is now at **z 52–62**, which is twelve blocks of level plateau between the door and the
break. It is ten deep rather than sixteen, because twenty-three blocks of plateau will not hold both
a sixteen-deep room and an apron worth having. The haul road's head was brought up to meet it, so the
way down starts where the players do.

The cost is the ratio: **2.91** against a band of 3.0–4.0, which is what moving a spawn seven blocks
away from its own objective does on a board 128 long. The apron is worth more than the 0.09.

## The spire is an `exclude` shape, because no mark can make one

Every relief mark is a *constraint* the relaxation then smooths through, so a mark cannot make a
vertical-sided column — it makes a cone. `relief_scope: "exclude"` does something else: it takes the
shape's cells **out of the field entirely**, so the bowl is solved as if there were a hole there and
the shape keeps the column it was drawn with.

`(-13, 32)`, radius 4, crown at **y28** over a floor at y16 — twelve courses of unquarried chalk with
nothing joining it to anything. The monument is a `pillar-3` in obsidian floating four over the
crown, and the only way onto it is a bridge somebody builds off the bench. The pit floor either side
of the neck is a build zone for exactly that reason.

Obsidian, because it is the only black on the board.

## The faces are `wallRun`, because a cut face is scored and a weathered one is banded

`wallRun` lays stripes that wrap the outer perimeter and are **constant up a column**, so on a face
they stand vertical. Seven runs of widths 3, 5, 2, 4, 1, 7, 2 in quartz, white clay, light grey clay
and diorite — widths that do not divide into one another, so the cycle round a face never falls back
into step with the corners.

This is the deliberate opposite of `kiln-row`, built the same week, whose mesa is a `layered` stack
read by depth so it bands *horizontally*. Weather lays a cliff down in beds; a saw scores it up and
down; and the two boards say so with two materials in the same bucket.

## What is where

| Band | Ground | Carries |
|---|---|---|
| \|z\| 41..64 | **the downs**, y40 | turf, four thorn trees, the spawn, and the head of the haul road |
| \|z\| 34..41 | the lip | the top bench, and the turf falling into it |
| the bowl | **six benches**, y36 → y16 | spoil, a wash of grit along the second bench |
| the lobes | **the working faces**, y16 | the two spires |
| the neck | y16, and **the sump** at y12 | water two courses deep over gravel |

The **haul road** comes down the west wall into this team's own face — `(-30,44) → (-29,36) →
(-25,28) → (-22,22)` — so the stone had a way out and the team that defends a face has the short way
onto it. It is stated twice: as a `line` mark, which the step terraces like everything else and
`stairs` gives back, and as the one `route` stroke on the board.

## What it costs

`GET …/preflight`: **export gate OPEN**. Round-trip, mirror, buildability and traversability clean.
The dressing pass takes 16 prop documents and **declines none**.

`GET …/coverage`: **27.8 % dead** — 2,563 of 9,216 cells. Most of it is the plateau behind each
spawn, which on this board is the ground the pit was cut *out of* and is there to be looked at from
below.

## Where it departs, and why

**`G8` reads a fill-ratio of 1.** One solid landmass with nothing cut out of it, measured against a
composed wool board. It gates nothing.

**`GO1` reads 2.91 against a band of 3.0.** Bought deliberately, for the apron above.

**Nothing joins a spire to a bench.** A causeway would have to stand at the spire's own height and
meet a bench at a different one, and the step would put a four-block wall at the junction. Bridging
to a monument is what the pit-floor build zone is for, and it is the shape of the approach: you cross
the floor in the open and then you build upward while being shot at.
