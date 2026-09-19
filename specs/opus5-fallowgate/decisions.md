# Fallowgate — what was mine and what was the studio's

One entry per decision the studio did not make for me. The studio's own answers are named
where they overrode or corrected mine.

## The idea

**A hillside sheep pasture with one stone-walled fold at the top of it; the fold's flagged
yard is cut into the hill and held out of the relief, and the monument stands on the wet flat
below both, so an attacker who starts on the fold has to come down off the hill to reach it.**

Written before any geometry. Three areas at three heights, which is the shape
`techniques/relief-on-shapes/README.md` builds: a made yard held out of the solve, an upland
beside it, a lowland below both, and the band between the two pinned areas left for the solve
to grade.

## The massing

**48 × 80 blocks, `cell: 4`, `rot_180`, `maxPlayers: 20`.** Mine. The brief capped the board
at 80 × 80 and a destroy board is a lane rather than a square, so the width came down to 48.

**Three pieces, not more.** Mine, and the thing the last board got wrong. `fold` (spawn,
24 × 12, y24), `flat` (48 × 12, y13), `pasture` (48 × 8, y20). A fourth piece was available
under the budget and there was nothing for it to say.

**The fold is 24 × 12 and not 40 × 12.** The studio's: `ST10` caps a protection region at
20 × 30 in either orientation, and 40 × 12 was refused.

**The crossing is 16 blocks of void, not 8.** The studio's: `G2` is a hard term and refused a
corridor under 10 blocks wide. That the two teams' ground is joined by a build zone over void
rather than by land is the repository author's ruling, in `AUTHORING-BRIEF.md` §3.

**The monument sits at (−15, −22), off the centre line.** Mine, then tuned against the
evaluator. Swept `/plan/evaluate` over spawn-z × monument-(x, z) and took the cell where
`GO1`'s ratio and `G8`'s dead-share both land in band; the residual score of 1.763 is `GO3`
and `GO4` and nothing else.

**`GO3` and `GO4` stand refused and the board did not grow.** Mine. `GO1` in [3, 4] and `GO4`
at 40+ blocks by walk together need a spawn separation of 160 blocks; the brief's board is 80.
Both are soft terms and the plan is `valid: True`.

## The relief

**Two marks, no push, `step: 1`, `base: 16`.** Mine. The two `area` marks pin the two benches
and the band between them is pinned by nothing, which is what grades the hillside — the
technique card's own arrangement.

**Both rings are drawn past the ground they pin.** The studio's correction. Drawn on each
area's own outline the bevel ate both floors and `RL5` came back: *"17 % level ground … it is
a ramp end to end"*. Run past the excluded fold, over the crossing's void and past the board
edge, the read is `level 0.308, largestField 0.221`, `seams []`, `silentMarks []`,
`symmetryError 0`.

**The two rings' facing edges are wavy.** Mine. It makes the free band 7 blocks wide at x −10
and 11 at x +10, so the hillside is 45° at one end and 32° at the other and a slope-banded
paint has something to cut on.

**`relief.grain`, amplitude 1, scale 9.** Mine, and forced by looking. Without it the relief
solves the free band as an even ramp, every cell of a row sits at one angle, and the slope
bands paint as unbroken contour ribbons. With it the bands interleave along their edges and
`03-slopes.txt` still reads 0 scrambled.

## The paint

**Cuts at 20° and 34°, off `GET …/incline?format=text`.** Read on the built relief before the
stack was written: `00-09 38.5% · 10-19 13.1% · 20-29 22.3% · 30-39 17.5% · 40-49 1% ·
60-79 7.7%`. Turf to 20, worn soil to 34, rock above.

**Two themes, not three.** Mine. `fell` is the map default over both grown areas; `yard` is
the fold and the flight. A third for the hollow was in budget and the slope bands were already
saying what the hollow is.

**No rim on `fell`, a rim on `yard`.** The brief's rule, applied: a rim caps every fall with a
band and turns a solved hillside into contour lines, and it belongs where an edge was *made*.

**`fill` is a voronoi of stone and andesite with `rise: 7`.** Mine for the material; the
`rise` is the studio's — `PT4` refused a fill sampled in the plane only, because every block
of a column would resolve alike and read as vertical stripes.

**Biome `Extreme hills` (#8ab689).** Mine, chosen off `GET /api/terrain/biomes` before any
pattern was written, because grass takes its colour from the chunk and `Plains`' #91bd59 reads
as a lawn beside stone and coarse dirt.

## What is built

**One flight, and it is the only added shape.** Mine. The fold is excluded, so it meets the
hollow at an 11-block face — the only face on the board — and nothing walked up it. 25 blocks
of run for 11 of rise, `height_mode: "level"`, `skirt: 0`, `keepClear: true`,
`relief_scope: "exclude"`, carrying the yard's theme rather than a third one.

**Its head sits on the fold's own south-west corner column.** Mine, after measuring. Headed
one column further east the transect read `BARRIER +10 at (-9, -27)` — a free-standing
ten-block buttress in the middle of the hollow.

**No second building.** Mine. The yard is the built thing and it already carries the hall; the
hollow is a wet bottom nobody builds in; the pasture is grazing. The budget allowed a house
and nowhere on the board answered *why here*.

## The dressing

**The yard takes nothing.** The brief's rule: a worked floor is swept.

**One erratic, on the shelf, not on the hillside.** The studio's, twice over. `DR-STEEP`
declined every seat on the slope — *"the slope is already the feature there and a rock pinned
to it reads as [pinned]"*, measured against the same 34° cut the paint uses — and `DR-KEEP`
declined the middle of the hillside as the spawn door's approach. The pair I first wanted
became one, because the seats near enough to read as a pair were declined `OB19`, whose real
clearance measures about 11 blocks.

**It moved from (−12, −11) to (20, −13) and from `size 3.5` to `size 3`.** Mine, after
`column (-12, -8)` read three blocks of mossy cobble standing over the crossing's void.
`size` is a radius: 3.5 comes out 7 blocks across.

**Three birch, one species, in the hollow's north-east.** Mine. Out of the wind under the
yard's east end, where the water off the hill collects and stock cannot get at seedlings.

**One flora pass over the whole board, `coverage 0.18`, `tallShare 0.03`.** The shape is the
whole board because the density field does the patchiness better than a hand-drawn polygon;
the two numbers stay low because tall grass is cover nobody authored in front of an objective
nobody chose.

**The spawn hall is `@hw-minehouse`, a shipped preset, unforked.** Mine. The default room is a
bedrock box. This one is timber-framed with a gable roof and no footing, so the building is not
the stone family of the yard under it.

**Its footprint moved from `[5,2,19,9]` to `[4,1,20,6]`.** Mine, after measuring. At the first
footprint the transect along z at x 6 read the hall's structure to z −30 with the fold's last
ground row at z −29 and `DROP −9 at (6, −28)`: one block of yard between a wall and a
nine-block fall. The stamp reaches about two blocks past the stated footprint.
