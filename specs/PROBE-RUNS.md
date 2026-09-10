# The colouring probe: ten boards, five places, two palettes

Ten boards built from `rockymine-probe`, the hand-authored unpainted map beside this file. Each was painted
by a fresh agent given `rockymine-probe/PROMPT.md` verbatim, working only through the studio's HTTP API,
with no access to this repository and no knowledge that it was one of a pair.

The pairs differ in one thing: the studio each was painted against. Five boards ran against `pgm-studio` at
`43de43a`, where `GET /api/terrain/blocks` answers each block's sprite, contrast, colours and construction
per face; five ran against its parent `98262bf`, where the same route answers one mean colour and nothing
else. Same board, same brief, same place on both sides of every pair.

| place | with texture data | without |
|---|---|---|
| plains | `probe-plains-2` | `probe-plains-1` |
| a desert | `probe-desert-1` | `probe-desert-2` |
| a snowfield | `probe-snowfield-1` | `probe-snowfield-2` |
| badlands | `probe-badlands-1` | `probe-badlands-2` |
| a volcanic ashfield | `probe-ashfield-2` | `probe-ashfield-1` |

Which arm took which index was shuffled so a slug carries no hint of its arm.

Each `specs/<slug>/` holds the three documents the board is described by, the `provenance.json` the export
wrote, `score.json` — every finding the texture scorer reads out of that board's registry — and the two
isometric renders. Each `maps/<slug>/` is the world it exported to.

## What the ten boards showed

Scored on `mush`, `clash`, `repeat` and `collapse` per pair, the texture data **did not change the paint**:
mush moved three ways better and two worse, mean −0.8p, which under a sign test is a coin. `collapse` — the
fault the face data exists to catch — fired exactly twice, once per arm, both `Smooth Sandstone` pairs on
the two desert boards.

The reason is in the transcripts rather than the numbers. `contrast` and `construction` appear in all five
texture-arm runs and in none of the others, so the data was read; `texture` and every sprite name appear
**zero** times in all ten. Agents consumed the two numeric fields and never compared the one categorical
field that answers whether two blocks are the same block on a face — which is the only field `collapse`
depends on.

Three things every board did regardless of arm: all ten told terrain from the things standing on it, with
no `kind: made` to help; all ten left the geometry untouched; and none of the ten repeated a block inside a
pattern once weighted stop lists are deduplicated.
