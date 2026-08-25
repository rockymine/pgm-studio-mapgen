# Kiln Row — a terrace of flats on a mesa shelf, and a dry river between

> A small capture-the-wool board, built to a brief that asked for **desert and mesa**, with houses
> from the studio's own template stock — a brick roof and clay — reading as an apartment building.

**In one sentence:** a dry wadi with a banded bluff over each end of it, a row of three flats along
each bluff's shelf with the wool room at one end and the spawn at the other, and two ramps down into
the sand, which is the only ground the two teams share.

**72 × 128 blocks**, `rot_180` about the origin, one landmass of **4,608 cells**, ground from **y8 to
y27**, symmetry error **0**. Wadi at y10, shelf at y20, caprock at y27.

## The strata are in the `wall` bucket, because a mesa is a cliff

There is no material that bands by world height, and this board did not need one.

A theme's **wall** bucket paints the exposed riser of a column, and a `layered` stack read on it is
read **by depth from the top of the face**. On a board whose drops all begin at one shelf, banding by
depth *is* banding by altitude — so one stack of white, orange, terracotta, red, brown, orange, red
sandstone and sandstone, in that order and those thicknesses, is the rock of the whole board:

| Course below the shelf lip | Block |
|---|---|
| 0–1 | white stained clay |
| 2–4 | orange stained clay |
| 5–6 | hardened clay |
| 7–8 | red stained clay |
| 9–11 | brown stained clay |
| 12–15 | orange stained clay |
| 16–18 | red sandstone |
| 19–24 | sandstone |

It is the wall material of **all three** themes here, so the bluff, the ramps' cheeks and the
channel's own bank are one rock in one order — and those eight colours appear nowhere else. Look
down at the board and it is sand; stand under the bluff and it is a mesa.

## The cliff is a `scarp`, which is a mark that draws a drop

`scarp` pins `high` on one side of a polyline and `low` on the other, holds each for `band` blocks,
and leaves `face` blocks unpinned between them — so the grade is `(high − low) / face` and the
relaxation builds exactly that, wherever the line is drawn.

| Mark | Runs | High → low | Face | Band |
|---|---|---|---|---|
| `bluff` | `(-44,31) → (-14,29) → (16,30) → (44,28)` | 20 → 11 | 4 | 9 |
| `caprock` | `(-44,61) → (0,60) → (44,61)` | 27 → 20 | 2 | 4 |

Both are drawn past both edges of the board, so the frame cuts a cliff rather than closing one. It is
the instrument the last landscape wanted and did not have: `tarnfell`'s beach came out as two
terraces and a five-course step because two flat marks were butted together, and a scarp is the thing
that says *drop* instead of hoping two heights make one.

## What is where

| Band | Ground | Carries |
|---|---|---|
| \|z\| 60..64 | **caprock**, y27 | the back bluff behind the spawn, two cairns |
| \|z\| 44..60 | **the shelf**, y20 | the wool room at one end, the spawn at the other, the street between |
| \|z\| 32..41 | the shelf's front | **three flats**, two storeys under a brick roof, the end ones open to the sky |
| \|z\| 26..34 | **the bluff**, y20 → y11 | the strata, and two ramps cut through it at x = ±26 |
| \|z\| 0..26 | **the wadi**, y8..12 | a braided dry channel, four acacia, scree off the bluff |

**The rooms stand at the ends of the shelf and the flats in the middle**, which is not a composition
choice: the ground in front of a door is kept clear, and four flats drawn across the shelf front were
all declined `DR-KEEP`. With the rooms at the ends, the clear columns are the ends too, and the forty
blocks between them is where a terrace goes.

## The flats

One style, two roofs. `@kr-block` is two storeys of sandstone with an end-stone string course and a
band of orange clay, arched birch-stair windows, under a **brick gable** with an end-stone gable
face — the studio's own `desert brick` preset extended upward. `@kr-deck` is the same building with
the roof laid in **air** and a cobblestone-wall parapet over the upper deck, so the two ends of each
row are open to the sky. Nine by nine, three to a row, three-block gaps: a terrace rather than three
houses.

Three storeys was the first draft and it was wrong — on a board whose highest natural ground is y27,
a 9 × 9 building fifteen courses tall is a tower.

## What it costs

`GET …/preflight`: **export gate OPEN**. Round-trip, mirror, buildability and traversability all
clean. The dressing pass takes 23 prop documents and **declines none**.

`GET …/coverage`: **1.2 % dead** — 109 of 9,216 ground cells sit off every route. On a board this
size with a wool carried out and back, nearly every block is on somebody's way somewhere.

`GET …/plan/flow`: the attacker walks **104** blocks to the wool and the defender **56**, a ratio of
0.54 — a two-ramp board, where the defence can be at either end of its own shelf but has to choose.

## Where it departs, and why

**`G8` reads a fill-ratio of 1.** The critic measures a solid landmass against a composed wool board;
this one is a single polygon with nothing cut out of it. It gates nothing.

**Both ramps are on the defender's shelf.** An attacker who wants the wool must climb the wool's own
bluff, at x = ±26, in front of one room or the other. That is the whole defensive shape of the board
and it is deliberate: on 128 blocks of length there is no room for a flanking route that is not
simply a third ramp.
