# sonnet55b-rustwater — an autumn river valley (Sonnet 5.5, run b)

## What I set out to build

**Rustwater Vale: a destroy-the-monument board for two teams of sixteen on an autumn river valley.** Two
hillsides face each other across a slow river; each team holds one bank and the slope above it. A dark-oak
watermill stands at each bank, a gold Millstone stands on a terrace below each spawn hall, and a roofed
cellar lies beside a cottage on the lower shelf.

The plan is authored by hand, not composed: three overlapping ranges of one height stepping eastward to the
river, so the two banks overlap only in the middle and the valley bends. Every landform is in the relief. The
board is credited to Sonnet 5.5, the slug is `sonnet55b-rustwater`, and the studio driven was the deployed one.

## How the layout was chosen

**I took the corpus's "box cut by water" and its "long lane of rolling ground" and departed from both.** From the
box I took a spawn seated high on its own massif with the goal on lower ground and a body of water below; from
the lane, a spawn in the land with ground to its back and a goal off to one side. I did not take the
side-islands, basin, tour, islands-in-a-box or rings layouts: each puts the spawn on a platform of its own or
makes the objective a station on an island chain, and the brief asked for one valley.

**`ORDER-OF-WORK.md` §1 decided three things.** A monument never ends a lane, so the Millstone stands on a
terrace to the side of the line. A destroy spawn stands in the land at its back, so the spawn hall stands on a
shelf with a ridge behind it. And the walk gates (`GO1` 3 to 4, `GO4` 40 to 90, `GO3` 85 to 150) fixed the
length: a goal 50 blocks from its own spawn and at least 150 from the enemy's wants spawns about 190 apart.

**The same gates put the goal on the slope and not on the bank.** The bank is about 95 blocks of walk from the
spawn, so a monument there reads a ratio near 1.7. The watermill therefore stands on the bank and the
Millstone on the terrace above it, which is the brief's watermill and not its monument.

**The spawn's seat, measured with `transect` from `(−20, −92)`.** It stands on ground y32 with **21 blocks of
its own land behind it** along the line to the enemy spawn, and the highest ground within 20 blocks above it is
y40 at `(−22, −110)`, **8 above**. The barn at `(−6..3, −102..−95)` stands beside it, 14 blocks off. No tree
stands within 20 blocks.

**Each goal's distance from its spawn, as measured.** The Millstone at `(16, −66)` is 44 blocks from the spawn
`(−20, −92)` by line: **33 ahead and 30 aside, 42° off the line to the enemy spawn.** The walk is 50 to its own
spawn and 172 from the enemy's, a ratio of 3.4, and 155 to the enemy goal at `(−17, 65)`. Team 1's goal at
`(−17, 65)` is the same figures mirrored.

## What the run cost

**Wall time was 14 minutes, from the first request at 20:44 to the final store at 20:58.** Reading the documents
and cloning the second repository took the first four of them.

**Seven stores, none refused.** Every `PUT /source` carries plan, relief and finish together, so by what changed:
the plan changed in the first two stores and was resent unchanged in five; the relief changed in the first five;
the finish (themes, dressing, layers, room styles) was first stated in the second store and changed in each of
the next five. Two dry runs were refused, which stored nothing: `PL7` (spawn offset outside its piece) and
`DR-DOC` (a boulder recipe naming a `form` the field does not take).

**The three numbers `drive.py` printed on the final store.**

```
ground   12232 walked, 390 scrambled, 118 barrier — 4.0% steps further than a player walks
props    24 placed, 0 declined
routes   worst step 4, on route spawn-0 to destroyable-1
```

Findings were empty, pre-flight read `export gate OPEN`, and coverage read 27.5% dead.

## What you could not say

**A river across the board, as water over the void.** *Wanted:* water between the banks. *Tried:* a `channel`
fluid on each bank. *Looked for:* a fluid that stands over void; `water/README.md` says water is "a shape taken
out of the ground".

*Verdict:* **missing from the system as a fact of how a fluid is cut, and not hidden**. The
river is two half-rivers a bank each with the 24-block build zone between them, and the zone kind `water-lane`
opens late and was not used.

**A water wheel on the mill.** *Wanted:* a wheel standing in the stream. *Looked for:* "wheel" in
`openapi/v1.json` (0 hits), in the glossary and the rules (0), and for a vertical form in `tools/sculpt/props.py`
(`dome`, `spire`, `arch`, `ring_wall` and the others stand in horizontal layers). *Verdict:* **missing**, as far
as three searches by name and by function go, and no deeper than that.

**A tree within 20 blocks of the spawn.** *Wanted:* canopy beside the spawn hall. *Tried:* `t8` at `(7, −79)` and
`t9` at `(−25, −78)`, both declined `DR-KEEP`. *Found:* the spawn's whole piece and the door approach are kept
clear, so the nearest legal ground is about 12 blocks off and outside the corridor I had. *Verdict:* **out of
reach from where I stood**; I did not find the keep-out's own number.

## What I got wrong

**I read the spawn's offset as board blocks and it is piece-relative.** `PL7` refused `(32, 52)` on a piece 92 by
28 blocks. The plan's rectangles are cells and the markers are blocks from the piece's corner, which the schema
says and I had not read.

**I let a spawn hall fill its whole piece.** The first store gave a 66 by 30 block grey hall (`WX13`) because I
stated no `footprint`. The fix was one field, and the picture is what showed it.

**I stated a sink's `base_height` as a floor and it is a depth.** The cellar pit came out at y4 with `SK11` naming
an island of 6,313 places. Seven blocks deep put the floor at y11, as `hollows/README.md` says in its table.

**I trusted the first tree mask.** A mask drawn before the board had its final outline sent three trees onto void
(`DR-SITE`), and a second mask read with the wrong x origin cost one more round.

**I did not sketch the relief more than one way.** `ORDER-OF-WORK.md` §3 asks for three or four unpainted reliefs
side by side; I built one and tuned it by `level` (0.27 to 0.41). The decision it was meant to inform is
therefore untested, and `incline` on the final board reads 38% under 10° and 9.5% at 40° or steeper.

**I never looked from a player's eye.** The paths, the cellar lid and the mill were judged from the overview
picture only; `render/eye` and `material-preview` were not used.

## What worked first time

**The dry run named every plan fault before a store.** `GO1`, `GO4`, `CT12`, `SP8` and `EL1` all came back from
`--dry` with edits attached, and two of them led to the layout above.

**One shape, reshaped by its vertices.** The three same-height pieces fused into one `bank-20` and a single
`shapePropsById` vertex list drew the whole coast, with no bend and no second shape.

**The Mesa biome.** Brown-olive grass, podzol and dirt read as one leaf-littered floor under it, which is the
autumn the brief asked for, with no extra block.

**Library styles for the buildings.** `hay-roofed-stone-and-dark-oak-house` served the hall, cottage and barn as
one row and `dark-oak-quay-warehouse` the mill; none was declined and there were no `HS*` complaints.

## Open gameplay questions

**Is a wadeable river between the bank and the build zone right?** I made the river two blocks deep and left it
swimmable, because a deeper one would cut the team from the zone it must bridge from. Taken conservatively;
the author should say whether crossing it should cost anything.

**Is a Millstone 50 blocks from its spawn and 155 from the enemy's the right place for the one objective?** The
gates demand it. It leaves the watermill, the board's best-looking place, a stop on the way and not a prize.

**Should the cellar open under or beside the goal?** It lies on the lower shelf, 18 blocks from the Millstone,
and is a refuge and a flank. I did not tunnel toward the goal.

**Is 27.5% dead ground a fault on a one-objective board?** The dead part is the east half of the spawn's own
piece and its mirror. I left it, since trees may not stand there.

**Is the Millstone's gold the right monument for a board this size?** `cube-3` needs ender stone, gold or
emerald, and I chose gold so the hay roofs and the goal carry one accent.
