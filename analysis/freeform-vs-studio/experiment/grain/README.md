# The grain setting, tried on a built board

**On a board built from relief marks, the grain setting changes almost nothing.** `exp-abbeymoor-studio` was
stored three more times on a local studio with only its relief grain changed, from amplitude 1.2 at scale 8 (the
board as built) to 1.2 at 24, 3 at 24 and 5 at 48. Of the 26,904 land columns, the strongest setting moved 5,008
(19%) and none by more than 4 blocks; the share of neighbouring columns 2 or more blocks apart went from 5.3% to
5.9% (read from each built world's region files: the highest terrain block per column).

**The reason is in the solver: grain never overrides a statement** (`ReliefSolver`, the grain pass skips every
pinned cell), so the area marks that state this board's floors keep their heights whatever the grain says. The
stepped look of the slopes comes from the flat mark areas and the bevels between them, painted stone where they
are steep. Rolling ground needs noise as a layer of its own, over a region, that no mark overrides.

| Picture | What it shows |
|---|---|
| `grid-overview.png` | the whole board from the overview camera, four settings |
| `grid-flank.png` | the abbey hill's south flank, `from=-10,-30&y=48&look=-44,-40` |
| `grid-bog.png` | the abbey hill from the bog, `from=6,-14&look=-24,-69` |
