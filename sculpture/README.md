# sculpture/ — two ways to build a thing that is not terrain

Two boards, and the difference between them is the whole point. `SCULPTING-WITH-LAYERS.md` at the repository
root is the account; this is the pair of pictures it was written from.

## `forms/` — written in the sketch's own shapes

Nine parametric structures on one deck, every one of them circles, polygons and rectangles with a floor and a
height. Eight of the nine are a **single layer**, because a layer holds one arbitrary height field and the
taller add wins each column outright — so a dome is concentric discs whose tops rise inward, and a hollow one
is the same discs with their floors rising too.

![the form gallery](forms/renders/forms-iso.png)

| form | layers | shapes |
|---|---|---|
| roundhouse wall (two doors, inner floor) | 1 | 4 |
| conical roof | 1 | 9 |
| hollow dome, radius 13, three thick | 1 | 13 |
| hollow ellipse, 15 × 9, rotated | 1 | 2 |
| tapered tower, thirty courses | 1 | 6 |
| ziggurat, five tiers | 1 | 5 |
| arch, twenty-two span | 1 | 11 |
| colonnade of twelve, with a saucer dome | 2 | 24 |
| amphitheatre, six tiers | 1 | 7 |

These stay editable in the Draw phase after they land, which is the reason to prefer them: the document holds
a circle with a radius, not four hundred rectangles that happen to look like one.

**The one form that needed a different answer is the amphitheatre.** Its height field falls inward, and
nesting can only build one that rises, so its tiers are annuli — and an annulus is one polygon, not an add
minus a subtract (`SCULPTING-WITH-LAYERS.md` §2).

## `models/` — compiled from solids

Four models built as spheres, capsules, extruded profiles and booleans, then decomposed mechanically: per
column, maximal runs of one material, and the *n*-th run of every column goes on layer *n*.

![the sculpture gallery](models/renders/sculpture-iso.png)

| model | size (x, y, z) | blocks | layers | shapes |
|---|---|---|---|---|
| robot | 26 × 45 × 14 | 4,486 | 16 | 746 |
| space station | 118 × 58 × 66 | 29,418 | 7 | 2,557 |
| car | 22 × 14 × 38 | 4,630 | 3 | 212 |
| hooded statue | 25 × 45 × 23 | 6,699 | 8 | 363 |

The layer count is not the height — it is how many separately-coloured runs the busiest column passes
through. `models/renders/<name>-layers.png` draws each model one panel per layer, which is the picture of
that: the robot's first layer holds 1,686 of its blocks and its fifteenth holds one.

![the robot, layer by layer](models/renders/robot-layers.png)

Beside each is `<name>-iso.png` and `<name>-front.png` — an orthographic face, because an isometric view
flatters a silhouette and a straight-on elevation does not.

## What is in each folder

```
forms/forms.layout.json          the sketch document that was posted
forms/renders/                   what the studio built from it
models/sculpture.layout.json
models/renders/
```

Both were posted whole through `POST /api/map/from-documents` — a layout and a bare intent, no plan, since a
gallery board is played for nothing. `maps/opus5-automaton` is the same props on a board that *is* played for
something.

Rebuild either with `python3 tools/sculpt/gallery_forms.py <dir>` or `gallery_sculpture.py <dir>` against a
running studio.
