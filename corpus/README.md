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
and the next is over 20 blocks — and `n` counts along x inside it. So the name carries no kind, no height
and no form.

**The row is the band, and the band is a kind. [author]** Fourteen bands, and what each one is is the
author's — nothing in the world or the library states it, and no measurement recovers it.

| row | trees | what it is **[author]** | built of | height |
|---|---|---|---|---|
| `r1` | 3 | the olive form again, smaller | oak log, oak and birch leaves | 7–8 |
| `r2` | 3 | large pine | dark-oak log, birch and spruce leaves | 20–22 |
| `r3` | 2 | large pine | dark-oak log, four leaf kinds | 25–26 |
| `r4` | 5 | tiny spruce, about vanilla's size | acacia log, birch leaves | 12–15 |
| `r5` | 3 | real dark oak — fat stem, flat crown | dark-oak log, acacia and birch leaves | 12–13 |
| `r6` | 9 | tiny oak, vanilla's size with a larger crown | oak log | 7–10 |
| `r7` | 8 | tall spruce — **and `r7-4` is its own kind**, a small Sequoioideae | acacia log, birch leaves | 19–35 |
| `r8` | 7 | acacia | acacia log | 8–9 |
| `r9` | 4 | the oak kind, with `r12` and `r14` | oak log, wooden slab | 14–16 |
| `r10` | 5 | small olive, two main branches each | dark-oak log, dark-oak leaves | 9–10 |
| `r11` | 9 | its own oak set — very dense leaves, small stems | oak log | 12–15 |
| `r12` | 5 | the oak kind, with `r9` and `r14` | oak log, wooden slab | 12–16 |
| `r13` | 10 | birch | birch log | 11–16 |
| `r14` | 1 | the oak kind, with `r9` and `r12` | oak log | 18 |

**The block a tree is built of is not what it is, and reading the one for the other is the trap this table
exists to close.** `r7` is acacia log and birch leaves and is a tall spruce; `r4` is the same two blocks
and is a tiny spruce; `r2` and `r3` are dark-oak log under birch and spruce leaves and are pines. The wood
is picked for its colour.

**So a name built from the stem would be wrong as well as ambiguous.** Of the fourteen bands, six are
built on oak log, four on dark oak, three on acacia and one on birch — and in two of the three acacia
bands the tree is not an acacia at all.

**`r7-4` is the one tree the row it stands in does not describe.** It is **35 courses and 161 logs**
against 19–27 and 21–39 for the other seven, which is the measurement under the author's reading of it as
its own kind.

**Fourteen bands are fewer than fourteen kinds.** `r9`, `r12` and `r14` are one oak at one size — 12 to 18
courses across the three — and `r1` is `r10`'s olive form built smaller.

**Seventy-four of the seventy-five are filed.** The missing one is `r15`, a tree built entirely of wool
with no log and no leaf in it, which `seed-trees.cs` counts only when it is passed `--wool`.

**Where a name can carry meaning is a spec.** `tools/trees.py bodies --row <z>=<prefix>` cuts a row into
bodies under a prefix the author chooses, which is how `specs/fable-millrace-revamp/trees.json` names its
22 — the library's `r<row>` naming is the seeder's, not a rule about copied trees.
