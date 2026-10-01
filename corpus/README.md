# corpus/

Hand-built worlds that nothing can re-derive. A script that took a reading is not committed and a board that
was driven lives in `maps/`; what is here was built by hand and is read by tools that expect it to stay.

| World | What it is | Read by |
|---|---|---|
| `tree-showcase` | 95 author-built trees, one per 19 × 19 platform, in 20 bands along z | `pgm-studio/tools/seed-trees.cs`, which seeds the studio's tree corpus and writes `tree-showcase/trees.json`; `tools/trees.py catalogue\|match\|verify` |

**A tree here is the only thing a `copied` style may be cut from.** `copied` means cut out of a world, so a
body assembled by hand and filed as one is a recipe claiming a provenance it does not have.

**Every tree here was built by rockymine, and a board planting one credits them.** The seeder records the
builder on each cut when it is run with `--builder=rockymine`, which `tools/seed-studio.py` passes, and the
studio credits them in `map.xml` as the original builder of the copied trees wherever one of theirs stands. A recipe pulled
with `GET /api/tree-styles/{id}/json` carries the name as `builder`; a style copied into a spec by hand keeps it
only if the copy does.

## What each row is

**A seeded recipe is named for what it is: `<kind>-<n>`.** The row is assigned by the z a tree's foot
stands at — a new row opens where the gap between one foot and the next is over 20 blocks — and the kind is
the one `tree-showcase/kinds.json` states for that row, or for the tree itself where its row does not describe
it. `n` counts a kind through the world in row order and along x, so `oak-1`…`oak-4` are `r9`, `oak-5`…`oak-9`
`r12` and `oak-10` `r14`.

**`kinds.json` is what the seeder reads, and the table below is the same statement in the author's words.**
The seeder refuses a row the file names no kind for, and matches a library row by where it was cut, so a
relabel renames the trees already filed: change the file and the table together.

**A row opens for every band, including one the seeder does not file.** `r15` is the wool tree, which
`seed-trees.cs` files only when it is passed `--wool`, and the row is held for it either way. So the rows are
the world's, and `wool-tree-1` is simply absent from a run without the flag.

**The row is the band, and the band is a kind. [author]** Twenty bands, and what each one is is the
author's — nothing in the world or the library states it, and no measurement recovers it.

| row | trees | what it is **[author]** | named | built of | height |
|---|---|---|---|---|---|
| `r1` | 3 | the olive form again, smaller | `small-olive` | oak log, oak and birch leaves | 7–8 |
| `r2` | 3 | large pine | `large-pine` 1–3 | dark-oak log, birch and spruce leaves | 20–22 |
| `r3` | 2 | large pine | `large-pine` 4–5 | dark-oak log, four leaf kinds | 25–26 |
| `r4` | 5 | tiny spruce, about vanilla's size | `tiny-spruce` | acacia log, birch leaves | 12–15 |
| `r5` | 3 | real dark oak — fat stem, flat crown | `dark-oak` | dark-oak log, acacia and birch leaves | 12–13 |
| `r6` | 9 | tiny oak, vanilla's size with a larger crown | `tiny-oak` | oak log | 7–10 |
| `r7` | 8 | tall spruce — **and `r7-4` is its own kind**, a small Sequoioideae | `tall-spruce` 1–7, `sequoia-1` | acacia log, birch leaves | 19–35 |
| `r8` | 7 | acacia | `acacia` | acacia log | 8–9 |
| `r9` | 4 | the oak kind, with `r12` and `r14` | `oak` 1–4 | oak log, wooden slab | 15–16 |
| `r10` | 5 | small olive, two main branches each | `olive` | dark-oak log, dark-oak leaves | 9–10 |
| `r11` | 9 | its own oak set — very dense leaves, small stems | `dense-oak` | oak log | 12–15 |
| `r12` | 5 | the oak kind, with `r9` and `r14` | `oak` 5–9 | oak log, wooden slab | 12–16 |
| `r13` | 10 | birch | `birch` | birch log | 11–16 |
| `r14` | 1 | the oak kind, with `r9` and `r12` | `oak-10` | oak log | 18 |
| `r15` | 1 | a tree of wool, and the one the library does not hold | `wool-tree` | wool | 23 |
| `r16` | 6 | jungle | `jungle` | jungle log, jungle and oak leaves | 16–20 |
| `r17` | 5 | a kind of willow | `willow` | dark-oak log, oak leaves | 16 |
| `r18` | 2 | a giant acacia, the baobab — very custom, for a desert, mesa or dry board only | `baobab` | acacia log, oak, spruce and birch leaves | 20–30 |
| `r19` | 5 | olive, five more of `r10`'s | `olive` 6–10 | dark-oak log, dark-oak leaves, planks and wooden slabs | 8–10 |
| `r20` | 2 | large oak, of the oak sets and closest to the dense oak | `large-oak` | oak log, oak or dark-oak leaves | 18–26 |

**The block a tree is built of is not what it is, and reading the one for the other is the trap this table
exists to close.** `r7` is acacia log and birch leaves and is a tall spruce; `r4` is the same two blocks
and is a tiny spruce; `r2` and `r3` are dark-oak log under birch and spruce leaves and are pines. The wood
is picked for its colour.

**So a name built from the stem would be wrong as well as ambiguous.** Of the nineteen leafed bands, seven
are built on oak log, six on dark oak, four on acacia, one on birch and one on jungle — and in two of
the four acacia bands the tree is not an acacia at all, while the willows are dark oak under oak leaves.

**`r7-4` is the one tree the row it stands in does not describe.** It is **35 courses and 161 logs**
against 19–27 and 21–39 for the other seven, which is the measurement under the author's reading of it as
its own kind.

**Twenty bands are fewer than twenty kinds.** `r9`, `r12` and `r14` are one oak at one size — 12 to
18 courses across the three — `r19` is more of `r10`'s olive, and `r1` is that olive built smaller.

**Ninety-four of the ninety-five are filed.** The one that is not is `r15`'s, built entirely of wool with
no log and no leaf in it, so only `--wool` sees it. A body counts as a tree only when a solid block sits
within two courses under its foot, and every leafed tree here stands on its platform.

**Thirty trees stand on planks laid under the trunk, and the plank is the tree's foot.** The seeder
counts a plank as tree above the world's lowest course, which is the course the platforms lie on, and a
foot is the lowest wood nearest the trunk. `(8, 1, -493)` in `r1`, `(134, 1, -74)` in `r11` and
`(70, 1, -31)` in `r12` are three of them: without the plank each trunk would hang a course above its
platform.

**Two trees lay wooden slabs in the plank course beside their foot.** `r9-3` at `(48, 1, -152)` carries
two and `r12-1` at `(7, 1, -32)` carries one, so planting either sets the slab on the ground beside the
planks rather than into it.

**Planks are part of a crown too, and a crown read without them falls apart.** 38 trees carry planks,
367 between them, and `r12-3`'s 39 spruce planks are what join the top 107 blocks of its crown to its
trunk.

**Nine tips still hang one block clear of the tree they belong to, and the seeder files each with that
tree.** No 26-connected step reaches them from their own wood, so each joins the standing tree whose
blocks come nearest it, within four blocks. Each is one or two blocks at a crown's tip, in `r3`, `r7`
and `r9`.

## The snapshot a board copies from

**`tree-showcase/trees.json` is every filed tree as a board states it.** Each entry is a tree's name, the foot
it stands on in this world, and the recipe the studio's library answers for it, body block for block. It is
the one file here that is generated: the cut that seeds the library writes it, run from the studio's checkout
after any change to the world or to `kinds.json`, and nothing edits it by hand.

```
dotnet run tools/seed-trees.cs ../pgm-studio-mapgen/corpus/tree-showcase --builder=rockymine \
    --json=../pgm-studio-mapgen/corpus/tree-showcase/trees.json
```

**A board copies its trees from the snapshot and keeps no cut of its own.** Its script names, for each style
key of its own, the showcase tree that key is, and states that tree's recipe whole. So a board's trees are the
world's as the cutter reads it, and a re-cut reaches a board the next time its script runs. The key is the
board's word for a role; the name is the showcase's, and it is the name that says what a tree is.
