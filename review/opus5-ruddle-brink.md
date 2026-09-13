# Ruddle Brink — one red scarp, climbed in exactly three places

> A core board. Each team holds a low red bench under its own cliff; the face above that
> bench is barrier everywhere except three places, and no two of them cost the same thing.

**In one sentence:** a headland of red sandstone where a plateau ends in an eleven-block
brink over the ground both cores stand on, and the only ways up are a scree the relief was
left to solve, a cut road, and a long ramp — so a defender who holds the brink is holding
three doors and not a wall.

104 × 200 blocks, `rot_180`, base surface 12, brow 23. One landmass a side, joined by a
**build zone over 24 blocks of void** and by nothing else.

## The board, measured

| | |
|---|---|
| plateau (brow) | z −100..−76, y23, the defenders' ground, spawn at the back |
| the brink | z −78..−72, `scarp` high 23 low 12, `face` **2** |
| bench | z −72..−12, y12, the fighting ground; the core stands on it |
| strait | z −12..12, void, full board width |
| core | world (−22, −62), obsidian `pillar-3`, float 6 |

`GO1` own 49 · enemy 159 · **ratio 3.24** (band 3–4) · `CT12` strait **24** (band 15–40).

## The three ways up, each transected

| way | x | what it is | measured |
|---|---|---|---|
| the scree | −34..−20 | no scarp mark; the two pads pull apart and the relaxation falls through the gap | rises 14, worst step 2, **2 scramble, 0 barrier** |
| the cut road | −7..6 | `height_mode: level` embankment, 24 run for 11 rise | rises 11, **worst step 1** |
| the long ramp | 22..33 | the same, 30 run, gentler and further out | rises 11, **worst step 1** |
| the face between | ±10 | the scarp itself | **BARRIER +4, +4, +3** — not climbable on foot |

That last row is the board. The first version had `face: 6`, which built an eleven-block
drop over six blocks — a 45° slope a player walks up anywhere — and the identity sentence
was simply false. `face: 2` is what made it a brink.

## Why the ways up climb in z and not along the face

A way up needs at least twice its rise in run, so an eleven-block face wants 22 blocks. Run
along the cliff and each way spends 22 blocks *of cliff*; three of them eat a 104-block
board. Both built ways are **embankments standing on the bench and climbing north into the
face**, so each spends about ten blocks of cliff for its twenty-two of run, and 63% of the
brink stays unbroken.

## What it is made of

Three themes, and the census agrees: `brink` 87.3%, `scree` 6.8%, `works` 6.0%, with 376
and 320 cells of drawn border between them.

The ground is finished **by angle**: `layered` on the `slope` axis, cut at 18° and 40°
against a measured distribution of 56.9% under 10° and 15% at 40°+ — wind-blown red sand on
the flat, orange clay on the shoulder, bare red sandstone on the face. The strata are in
`wall` **and** `fill`, because a cliff is what the wall bucket paints and a stack stated
only in `surface` bands the top four courses and leaves the face plain.

Three tone families, named before anything was painted: **ground** red (sandstone, red sand,
orange clay), **built** pale (sandstone, smooth sandstone, spruce), **accent** grey (gravel,
andesite) and used only on the talus. The gate cot is timber on pale stone standing on red
rock — never the family under its feet.

## Standing complaints, and why they stand

- **`EL1` ×2** — "'brow'–'bench' steps 11 blocks … wants a ramp or a flight". The plan tier
  walks pieces flat and cannot see an authored flight at all. The three transects above are
  the answer.
- **`RL2`** — "243 of its steps are taller than a player can scramble. The elevation is
  there and was never graded." That is the cliff, and grading it would delete the board.

## What went wrong

- Coverage began at **49.7% dead** — a 104 × 240 board with one core has two journeys and the
  bench corners are on neither. Shortening it, moving the spawn off the centre line so the
  home walk runs diagonally, and cutting the bench narrower than the brow took it to **19.2%**.
- The `backridge` push originally ran across the whole plateau with `falloff 8`, and its skirt
  reached the lip. A push is added to the surface the marks solved, so it **graded the scarp**:
  the cliff read as a walk-up everywhere. It became two shoulders either side of the spawn
  that stop 6 blocks clear of the face.
- Every paint patch on the first three builds painted nothing at all, in silence. See the run
  report: a scoping shape must declare a `height_mode`.
