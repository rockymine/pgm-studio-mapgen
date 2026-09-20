# Portway — a breached rampart, and a stone pier in the gap

**In one sentence:** the front is a built rampart with a hole punched through it that nobody can
close, and the crossing is made at a stone pier standing in the middle of the gap.

Composed from `GET /api/compose?players=30&symmetry=mirror_z&seed=2` — hub `bar` (one 9 × 6 piece),
frontline `twin` with an eight-cell hole between its prongs, wools `i`/`i`, card score 0.000, 123
land cells, 85 × 170 blocks. The adapted plan is 95 × 180 and evaluates at **score 0, valid**.

## What the composer gave, and what was done with it

The `twin` frontline's own hole is the board's subject. The composer draws it and does nothing with
it; here the two prongs are raised four courses into stone bastions with a crenellated battlement
along each lip and a return down each cheek of the gap, and the notch between them is void from the
mid band right through to the apron. The middle of the rampart is a breach.

| the composer's | what shipped |
|---|---|
| a flat plan at surface 9 | heath 12, pier 14, bastions 16 |
| one zone, twenty blocks of build flush against both fronts | **four zones** and a `pier` piece seated in the hole they leave — ten blocks of water either side of it |
| no middle island on any board it makes | a neutral stone stump, 15 × 10, with a drum-tower beacon on it |
| `"walls": []` | two bedrock approach walls, one per ward, each on a twenty-block seam |
| a 10-block frontline prong (`FR9` complains) | three equal thirds across the front: bastion, breach, bastion, fifteen blocks each |
| the spawn on the east flank | ten blocks west, which is what squares the two raids |

## The two wools

The composed board walks 159 blocks to one wool and 144 to the other, and the defender 63 and 49. The
two wools here sit at different depths on purpose — the west one behind the hub, the east one forward
of it — so the journeys differ, and the distances were tuned until the difference stopped mattering:

| | composed (mirror_z seed 2) | Portway |
|---|---|---|
| attacker's walk | 159 / 144 | **160 / 158** |
| attack ratio | 1.10 | **1.01** |
| defender's walk | 63 / 49 | **51 / 55** |
| defence ratio | 1.29 | **1.08** |

## How it is meant to play

Both crossings are ten blocks, not twenty: the pier halves the gap at the centre and the flanks keep
their full span, so the cheap crossing is the one directly under the breach and everybody knows it.
A player on the pier is under fire from two bastions and from the beacon nobody owns.

Behind the breach the apron is flat — stated flat, with an `area` mark, because the gatehouse stands
on it and a made thing states an absolute floor. The gatehouse is two drum towers, an arch and two
crenellated curtains closing the hub's whole front except for two-block slips at either end. A wall
with one gate is a gate; a wall with no way round it is a board that cannot be walked, and those
slips are why `preflight` has something to say yes to.

Each wool ward hangs off the hub on exactly one twenty-block seam and both seams carry bedrock. That
is the device the composer emits empty on every board it makes, and it is the whole of what makes the
two raids cost anything once the breach is crossed.

## The techniques, and what each one bought

**Four zones instead of one.** `zones` takes more than one entry, and a middle island is a `piece`
with build zone round it rather than a gap in the band. The straits come out at 30 blocks team to
team and 15 team to pier, both inside `CT12`'s band.

**`relief_scope: "exclude"` on three shapes** — both bastions and the pier. The bastions meet the
heath at a face, and the pier stands on vertical sides, which is the one thing only `exclude` does.

**Eighteen made layers**: a whole `props.gatehouse` (two drum towers, an arch, a gate parapet and two
curtain runs), two battlements, two cheek returns, two bastion towers and the pier's beacon.

**Vertex edits, not a second shape.** The heath's ring carries a bay eaten into its west flank and
four chamfered ward corners; the two bastions carry a battered outer angle and a notch cut into each
breach cheek, so the breach reads as something knocked through rather than as the gap left between
two boxes. Every move is inward: a corner pushed out hangs over sea and builds a stub at the shape's
own floor, and nothing declines that. The pier is the one ring whose every edge is over water, so it
is the one that carries a `bend`.

**The portway is a `polyline` shape, not a chain of rectangles.** The rasterizer splines its four
points — centripetal Catmull-Rom, eight samples a segment — before offsetting the band, so what
lands is a causey that flows: out of the gate's arch, one course proud of the heath, down to the lip
of the breach. The `stroke` prop that runs from the spawn to meet it is the other thing entirely —
it repaints the top course and adds no cell.

**The ground is finished by its angle** — a `layered` stack on the `slope` axis, red sand and
hardened clay under 14°, coarse dirt to 28°, red sandstone above. The board is a Mesa biome because
the palette is hardened clay and red sand and the biome is a palette decision, not a line added at
the end.

**Numbers.** `preflight` ends `export gate OPEN`. `coverage`: 7400 reached, **0.0% dead**.
`03-slopes.txt`: 6496 walked, 68 scrambled, 92 barrier, 8 faces, largest 19. Relief: `level` 0.541,
`largestField` 0.286, range 7 over 3047 cells, `faceCount` 0, `symmetryError` 0, one seam of step 2.
Themes: heath 91.6%, works 6.6%, pier 1.8%.

## What went wrong

**`RL2` on the first build**: twelve steps taller than a scramble, "the elevation is there and was
never graded". The cause was one flat `area` mark 27 blocks across pinning most of the hub, with the
marks outside it meeting the pin on a wall. Shrinking the flat to the gatehouse's own footprint and
putting a `tread` on every point mark outside it cleared it.

**The flat was the other fault too.** With the big pin the heath read `level` 0.745 — a table. It now
reads 0.541, which is still flat for a board of this size; the shape budget went into structure
rather than terrain, which is what this board is for, and it is stated rather than accidental.

**Five props declined on the first pass** — `DR-SITE` on two the bay had taken the ground from under,
`DR-KEEP` on two inside a door's approach, `DR-STEEP` on one pinned to a 35° face. Every placement on
the board now comes from `POST …/sketch/seats` or `loop.py --candidates` rather than from a guess.

## Standing complaints

- **`EL1` ×2** on the two bastion seams, four blocks. Answered by the two flights, each ten blocks of
  run for four courses, cut into the apron behind the bastion rather than leaning on its face.
- **`SK27`**: three plateaus of one component stating two paints. Same reading as on Revetment — the
  riser here is the rampart and the rampart is the board.

## Coordinates

| thing | at |
|---|---|
| the breach | x −5..10, z 15..25, void |
| west bastion | x −20..−5, z 15..25, surface 16 |
| east bastion | x 10..25, z 15..25, surface 16 |
| the pier | x −5..10, z −5..5, surface 14 |
| the beacon | (2, 0), drum tower, outer 4, 12 tall |
| the gatehouse | centred (2.5, 42), span 20, curtains to x −17.5 and 21.5 |
| bedrock walls | x = −20, z 45..65 and x = 25, z 40..60 |
| the causey | polyline (2,46)→(1,38)→(3,31)→(2,26), one course |
| west stair | x −18..−12, z 25..35, 12 → 16 |
| east stair | x 14..20, z 25..35, 12 → 16 |
| wools | (−35, 55) and (40, 45) |
