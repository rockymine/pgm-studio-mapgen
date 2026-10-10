# Riftwater in layers: how the page is made, and the map style

`../index.html` is the Riftwater port shown as a stack of layers: the outline, sixteen ground steps and twelve world
steps, each with the columns it changed; every shape the port's code names, drawn by the kind of geometry it is
written as; a hill and a crater over four kinds of area; the sinkhole and the spoil heap as records.

`./build.sh` rebuilds it from the port in about ten seconds. `heights.py` runs the port's `land()` with a snapshot
after each step and asserts the ground is the port's own. `worldsteps.py` runs `gen.py`'s steps one at a time and
prints whether the world hashes to the one `check/boards.json` holds. The rest draws and assembles; what they
write goes to `out/`, which is not committed.

## The style

The style lives in `style.py`, and every picture on the page is drawn with it. It is the look meant for showing a
board in the studio and on the site.

**The ground is coloured by height on a hypsometric ramp.** Dark green is low, yellow sits around y 54, brown is
the hillside and pale cream the crest. The stops are set where boards actually live, between y 44 and 64, so a
two-block rise is a visible change of colour.

**The light comes from the north-west, the top-left of the picture.** Faces turned toward it are lit. Light from
any other side makes the eye read hills as hollows.

**A contour line marks every second block and a heavy one every tenth.** Close-ups draw one per block. A line is
the pixel edge between two cells whose heights fall in different bands, so it follows the block grid exactly.

**Pink outlines what a step changed.** The tint is light and the edge is solid, so the ground under it still reads.

**Shapes are coloured by the geometry they are written as.**

| Colour | Kind |
|---|---|
| pink | circle or ellipse: a centre and radii |
| blue | a line of points, splined, with a width |
| orange | a polygon or rectangle: its corners |
| purple | a noise line: one offset per row, no points |
| grey | a band along an axis |
