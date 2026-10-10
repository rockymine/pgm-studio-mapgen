# Two freeform boards written as layers

**Each folder takes one freeform board apart, measures which code writes which blocks, and writes the whole board
again as one JSON document of ordered layers.** The question is the author's: whether an agent that writes a board
as a script would lose freedom if it had to state the board as layers the studio can hold and show.

| Folder | Board | Subject |
|---|---|---|
| `riftwater/` | Riftwater (DTM) | the pgmvox port at `freeform/lib/ports/riftwater` first, the standalone original beside it |
| `hollow-mesa/` | Hollow Mesa (DTC) | the standalone board; it has no pgmvox port |

Each holds `ANATOMY.md` (the pipeline in run order, with the blocks each step leaves), `FINDINGS.md` (the answer),
and the board as layers (`*.layers.json`). The block attribution behind the numbers is in `riftwater/method/*.json`;
the instrumenting scripts were investigation and are not kept.
