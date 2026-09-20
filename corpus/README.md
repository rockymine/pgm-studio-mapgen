# corpus/

Hand-built worlds that nothing can re-derive. A script that took a reading is not committed and a board that
was driven lives in `maps/`; what is here was built by hand and is read by tools that expect it to stay.

| World | What it is | Read by |
|---|---|---|
| `tree-showcase` | 75 author-built trees, one per 19 × 19 platform, sorted into 14 families by crown | `pgm-studio/tools/seed-trees.cs`, which seeds the studio's tree corpus; `tools/trees.py catalogue\|match\|bodies` |

**A tree here is the only thing a `copied` style may be cut from.** `copied` means cut out of a world, so a
body assembled by hand and filed as one is a recipe claiming a provenance it does not have.

## What each row is

**A seeded recipe is named `showcase-r<row>-<n>`, and the name says where the tree stood and nothing
else.** The row is assigned by the z its foot stands at — a new row opens where the gap between one foot
and the next is over 20 blocks — and `n` counts along x inside it. So the name carries no species, no
height and no form.

**The row is the family, though, because the world is laid in bands and each band holds one.** Fourteen
rows, fourteen families. What the name cannot say, this table does — read out of the seeded library rather
than off the platforms:

| row | trees | stem | other wood | height |
|---|---|---|---|---|
| `r1` | 3 | oak | wooden slab | 7–8 |
| `r2` | 3 | dark oak | wooden slab | 20–22 |
| `r3` | 2 | dark oak | — | 25–26 |
| `r4` | 5 | acacia | — | 12–15 |
| `r5` | 3 | dark oak | — | 12–13 |
| `r6` | 9 | oak | — | 7–10 |
| `r7` | 8 | acacia | — | 19–35 |
| `r8` | 7 | acacia | — | 8–9 |
| `r9` | 4 | oak | wooden slab | 14–16 |
| `r10` | 5 | dark oak | — | 9–10 |
| `r11` | 9 | oak | — | 12–15 |
| `r12` | 5 | oak | wooden slab | 12–16 |
| `r13` | 10 | birch | — | 11–16 |
| `r14` | 1 | oak | — | 18 |

**A family is a crown, not a species, and the table is why a name built from the stem would not work.**
Oak is the stem of six of the fourteen and acacia of three, so the wood identifies nothing; what separates
`r1`'s oaks at 7–8 from `r9`'s at 14–16 from `r11`'s at 12–15 is the shape over them.

**Seventy-four of the seventy-five are filed.** The missing one is `r15`, a tree built entirely of wool
with no log and no leaf in it, which `seed-trees.cs` counts only when it is passed `--wool`.

**Where a name can carry meaning is a spec.** `tools/trees.py bodies --row <z>=<prefix>` cuts a row into
bodies under a prefix the author chooses, which is how `specs/fable-millrace-revamp/trees.json` names
its 22 — the library's `r<row>` naming is the seeder's, not a rule about copied trees.
