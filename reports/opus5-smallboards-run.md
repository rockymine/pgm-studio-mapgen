# Opus 5 — three small boards, and the band that takes the rest of the cell

## What I set out to build

Three boards to one brief and two of my own choosing, all deliberately **small — 72 × 128 blocks**,
where the last three had been 176 × 348 and 184 × 264. One capture-the-wool, one destroy-the-monument,
one mixed. The briefed one was to be **desert and mesa**, with houses from the studio's own template
stock — *a brick roof and some clay, like an apartment building* — which is `HousePresets.Desert`,
end stone and sandstone under a roof laid entirely in brick.

- **`opus5-kiln-row`** — ctw. A dry wadi between two banded bluffs, a terrace of flats on each shelf.
- **`opus5-deepcut`** — dtm. A chalk quarry worked down in benches, the monument on a spire of
  unquarried rock.
- **`opus5-aerie`** — ctw · dtc. Six crags in open sky and a twenty-four block strait; every crossing
  is a bridge somebody builds.

All three: export gate open, zero declines, symmetry error 0.

## The finding this run is for

**A voronoi's bands are depths inward from a cell boundary, and the last one takes the whole rest of
the cell.**

`VoronoiMaterial.Resolve` walks `Bands` and stops **one short**:

```csharp
for (var i = 0; i < Bands.Count - 1; i++)
{
    edge += Math.Max(1, Bands[i].Depth);
    if (depth < edge) return Bands[i].Material.Resolve(in ctx);
}
return Bands[^1].Material.Resolve(in ctx);
```

`depth` is the Worley `F2 − F1` gap — small near a cell boundary and largest at a cell's centre — so
the bands are **rings measured inward from the boundary**, not weights over an area, and the final
band's stated thickness is read by nothing at all. It takes every interior the earlier bands did not
reach, which on a cell size of seven is most of the ground.

Every voronoi I had written was ordered the other way round. `kiln-row`'s wadi was

```python
voronoi(11, 7, [(SAND, 4), (RED_SAND, 2), (GRAVEL, 1)])
```

intended as *sand with a seventh of gravel*, and it built as a **gravel bed with sand along the
cracks** — the board's whole midfield came out grey, and the two braided strokes I first blamed and
thinned made no difference, because they were never the cause.

Stated correctly, a voronoi is a **diagram, not a mixture**: write the ground it is made of *last*,
and the bands before it are the veining along the boundaries. `[(GRAVEL, 1), (RED_SAND, 2),
(SAND, 1)]` is a sand wadi with gravel in the cracks and a red-sand margin round each patch, which is
what a dry riverbed looks like. All fourteen voronoi materials across the three boards and their
seven house styles were re-ordered on that reading.

## Four instruments, and what each is actually for

**A cliff's strata live in the `wall` bucket, because a cliff is what a wall bucket paints.** There is
no material that bands by world height and `kiln-row` did not need one: a `layered` stack read on the
wall is read *by depth from the top of the face*, so on a board whose drops all start from one shelf,
banding by depth **is** banding by altitude. One stack of white, orange, terracotta, red, brown,
orange, red sandstone and sandstone is the rock of the whole board and appears nowhere else on it —
look down and it is sand, stand under the bluff and it is a mesa.

**`step` with `stairs` is the quarry, and it is the terracing that ruined `tarnfell`.** That board
came out as stacked plateaus with vertical faces and had to be rebuilt at radius 3–6. `deepcut`
*wants* those plateaus: it states four heights — the plateau, two lobes of working floor, the sump —
lets the relaxation solve a smooth bowl between them, and then snaps the finished surface to a
four-block quantum. Six benches, four-course risers, and `stairs: true` cuts a way up out of every
place that stranded. Thirty marks the last time; four marks and a number this time. Every stated
level is a multiple of the step, or the knob that shapes everything between them rounds them away.

**`relief_scope: "exclude"` is the only way to a vertical-sided spire.** Every mark is a *constraint*
the relaxation then smooths through, so a mark makes a cone; an excluded shape leaves the field
entirely — the solver bends round it as it bends round the void — and keeps the column it was drawn
with. `deepcut`'s two witness pillars are radius-4 circles at a stated 28 standing in a floor at 16,
joined to nothing.

**`wallRun` is a cut face and `layered` is a weathered one.** `wallRun`'s stripes wrap the perimeter
and are constant up a column, so they stand vertical: saw scars. `layered` on the same bucket bands
horizontally: bedding planes. `deepcut` and `kiln-row` were built the same week and say the
difference with two materials in one bucket, which is a nicer answer than two palettes.

## What I got wrong

**I put the wool at the front of a capture board.** `aerie`'s first draft had the wool on the crag
nearest the strait and the core behind it, and `WL10` read a wool-front-distance of **8**. A core is
the objective that wants to be contested — it cannot be carried anywhere, only breached — and a wool
has to be fetched and brought home. Swapping them moved the number to 14 and made the board read the
way it plays.

**I drew nine crags and eight running jumps.** Six-block gaps, and the critic answered `G2`, `G5` and
`CT12` on every pair of them. **On a bridging board the gaps are the design**, so the second draft
stated the four numbers first — 10, 16, 16 and a 24-block strait — and fitted the crags round them.

**I put four flats across a shelf in front of two doorways.** All four declined `DR-KEEP`. The ground
in front of a door is kept clear, so on `kiln-row` the two rooms went to the ends of the shelf and
the terrace went in the forty blocks between them, which is a better composition than the one I lost.

**I built the flats three storeys tall** on a board whose highest natural ground is y27. A 9 × 9
building fifteen courses high is a tower. Two.

**I flooded a quarry by making its pan the size of the pit.** Water fills whatever is level, and an
`area` mark 34 × 30 at the sump's height is a 34 × 30 lake. The pan is the size of the pool.

## What worked first time

- **`scarp`.** A mark that pins `high` one side of a drawn line and `low` the other and leaves `face`
  blocks between them, so the grade is chosen and the cliff goes where the line goes. It is the
  instrument `tarnfell`'s beach wanted and did not have.
- **A core.** 5 × 5 × 5 of obsidian over lava, floating six over a crag in open sky. Nothing to adjust
  and nothing refused.
- **`teamTint`.** One course of stained clay in the fold's surface stack and one in the pen's top
  wall course; the material resolves to the owning team's colour where a cell has a team and to a
  stated neutral where it does not. Each wool crag is quietly its own colour, from one material and
  no per-team theme.
- **Small.** 1.2 % dead ground on `kiln-row`, 6.1 % on `aerie`. On a 128-long board with a wool
  carried out and back, nearly every block is on somebody's way somewhere — which the 54 % of
  `tarnfell` says as loudly from the other end.

## Open gameplay questions

**Is a forward core the right shape?** `aerie`'s `GO1` reads 2.02 because the core sits one strait
from the enemy on purpose. A ratio band written for a goal a team sits on may simply be the wrong
measure for an objective meant to be fought over in the middle — but that is a claim about how a map
plays, and it is the author's.

**Should a spire be bridgeable only?** Nothing joins `deepcut`'s witness pillars to a bench. A
causeway would meet a bench four courses off, which the step turns into a wall. Crossing the floor in
the open and then building upward is the approach the board has; whether a DTM monument should cost a
bridge is not something the corpus settles.

**Is 24 blocks the right strait?** `CT12` wants 15–40 and it is at the low end. Wider is a longer
bridge and a longer time in the open; narrower stops being a crossing at all.
