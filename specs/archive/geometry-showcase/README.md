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

**A flight is not finished at its last tread.** Three climbs here topped out level with the ground for
one cell and then fell twenty-four, and every whole-board read called them walkable — none of them is
asked about a flight. That question is `SK26` now, in the studio, so this board is checked by the tool
rather than by hand.

**A wall stands on the ground rather than being it.** Drawn as ground it builds the right shape and the
wrong column: a shape's theme paints everything it owns, so the field's grass and soil under the wall
are replaced down to bedrock. The rampart, its crenellation, its piers and the drum ring are a layer at
the field's own surface; the podium another at the plateau's.
