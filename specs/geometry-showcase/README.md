# Geometry Showcase

Eleven ways of stating a mass or getting a player up one, out of sketch shapes alone — no buildings,
no props, no relief. `reports/geometry-showcase.md` is the account: the constructs, what each
measured, and the four findings the build produced.

```
python3 specs/geometry-showcase/build-spec.py          # writes the three documents
python3 tools/drive.py specs/geometry-showcase "Geometry Showcase" --out maps/geometry-showcase
```

`geometry.py` beside it is the vocabulary. `grade()` is the one piece of arithmetic the board turns
on — the rasterizer rounds a shape's surface at the cell centre, so a flight's anchors are stated
half a step below its first cell or every other tread comes out two blocks high. `treads()` runs the
same reading forward, which is how a landing's height is stated rather than guessed.

`renders/close/` holds a `?format=text` transect through each construct, taken by hand because the
driver transects features rather than terrain. Read those before the pictures.

**A flight is not finished at its last tread.** Nothing the studio reads back asks whether a climb
arrives anywhere: `slopes` classifies cells, `walk` travels an aim line, `transect` cuts where it is
pointed, and a flight that tops out level with the ground for one cell and then falls twenty-four
passes all three. The question is per flight — take the last tread, step four cells on **in the
direction of travel**, and require ground within one course. This board has fourteen of them, listed
with their top treads in `reports/geometry-showcase.md`; three of them failed it on the first build.
