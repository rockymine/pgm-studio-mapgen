# QUALITY-LEAP.md, cross-checked

`freeform/QUALITY-LEAP.md` on `opus55-freeform-riftwater` (commit `ba932271`) is a second analysis of the same
question, written by a Sonnet agent in another session from the run reports, the library and the studio's docs. This
note checks it against this folder's report, and against the code where the two disagree.

## Where the two agree

**The mechanisms are the same list.** Per-block control through a voxel world written by the studio's own writer;
ground painted by slope and rock in tilted beds; undersides, skirts and root vines on floating islands; houses at any
heading through `Frame` with the studio's `RoofField`; a grammar beside the theme; props as small code objects; and
a plan that is drawn, sketched and walked before it is built and read back after. Both rank the floating objective
marker first among what to adopt, and both name the lost stamps (defence chest and wall, wool-room gear, build-zone
outline) and the coarser build regions.

## What it says that this folder under-weighted

- **The studio's paint adds no geometry.** `terrain-painting.md` says the painter reads the terrain the world builder
  placed and "rewrites its surface — no new geometry, only materials". So every look the studio has is a finish over
  a shape already decided by plan pieces and relief marks. This folder made the same point through the closed prop
  vocabulary; the painter's contract is the cleaner statement of it.
- **Rooms are held inside their plan pieces.** `WX12` refuses a room whose footprint leaves its room piece, which
  ties where a wool room or spawn can stand to the plan's rectangles. It is one reason the studio's Slatefold put its
  wool rooms where the plan's pieces were rather than where a place would have them.
- **Rules a board does not re-state are not enforced.** Each freeform checker re-measures the rules it remembers
  (about 120 lines a board); whatever it forgets is unchecked. This folder counted the lines; QUALITY-LEAP names the
  consequence.

## Where it is wrong, or overtaken

- **"Add a slope axis to `TerrainTheme`" (its item 4).** The studio already has it: `BandAxis.Slope` (TP24), Horn's
  gradient over a window of two, an angle mask on any band stack, which `CLAUDE.md` names. And for beds the studio is
  ahead: TP26 lets a height stack follow the ground averaged over `reach` cells, which carries strata along the land's
  tilt where pgmvox's beds are either level or locked to the surface (this folder's report, *Strata that follow the
  land*). What pgmvox has that the studio lacks is soil depth by slope and beds that dip and fold.
- **"Few gameplay trades" / "gameplay barely changed".** The objectives' XML is valid, but validity is not
  correctness. Of the thirty faults in the author's playtest notes of 10 October, nine are ones the studio would have
  caught by itself (`playtest-feedback-2026-10-10.md`): an obsidian monument with no diamond pickaxe, hills with nothing
  that changes colour, a defence wall facing away, thin wool-room loot, a team boxed in at its spawn, and four
  objectives hidden underground or atop a tower. The experiment's pgmvox Abbeymoor added another the studio refuses:
  a 3 × 3 × 3 obsidian cube, 27 blocks, where `DC3` caps obsidian at three.
- **"Nothing here is a controlled comparison."** It was true when written. The experiment in `experiment/` built two
  briefs both ways with the model, the brief, the lessons and the time held equal, and the boards came out comparable
  (`experiment/RESULTS.md`). That moves weight off the tool alone and onto what was spent on it: Opus, hours per
  board, the author's review rounds and bespoke code. Its ranking of mechanisms stands; its implied size of each
  does not.
- **The window beside the door** is not in it, and has since been fixed on its branch: pgmvox 0.20.0 keeps a block of
  wall either side of every door (`c7f16729`), and Riftwater's doors with a pane beside them went from 36 of 58 to 0.

## What it does not cover

The noise (why the studio's grain reads grainy: its settings, not its algorithm), the renderers (framing is the
difference, not the ability to see), house styles (taste in code against taste in 146 values of data), the studio's
closed set of doorway materials, the footing, vegetation density and micro-geometry as the new class of fault, and
how a person would inspect and diff a pgmvox board (the recipe). Those are this folder's report and
`STUDIO-2-DESIGN.md`.
