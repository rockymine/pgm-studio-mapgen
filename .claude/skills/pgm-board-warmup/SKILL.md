---
name: pgm-board-warmup
description: The first ten minutes of an authoring run — what this repository costs to read,
  what must never be opened, and one drill that checks whether a board can be read before one
  is built. Load once, at the start of a run, before pgm-board.
---

# Before the first board

Two things, in order: what reading costs here, and one drill. Together they run about 15k
tokens and ten minutes, and both are done before a plan is written.

## 1. The budget, because this repository is larger than any context window

The documents a run is pointed at come to **~82k tokens** — 41% of a 200k window before a
single map is opened. Everything below assumes that is already spent.

| Read | ~tokens | When |
|---|---|---|
| `00-board.txt` | 0.4–3k | freely |
| one named `renders/*.txt` | ~1.1k median | freely, **named individually** |
| `02-heightmap.txt` · `03-slopes.txt` | 1.3–10k | one board at a time |
| every text render of one board | **30–57k** | never — name the file wanted |
| median `*.layout.json` | ~12k | only through `jq`, never whole |
| `fable-millrace-revamp`, `opus5-slipway` layouts | **397k · 367k** | **never open. Either one ends the run.** |

**Never `cat` a `*.layout.json`.** Two of them exceed a whole window and 27 exceed 20k. A
layout is queried: `jq '.shapes | length'`, `jq '.shapes[] | select(.id=="…")'`. Same for a
large `*.finish.json`.

**A one-line answer is a `grep`, not a file read.** `03-slopes.txt` runs to 10k tokens and its
verdict is one line: `grep 'cells:' …/03-slopes.txt`.

**`specs/` is split, and the split is the reading rule.** Fifteen boards sit flat and are worth
reading; the other 111 are under `specs/archive/` — probes, experiments run to find the limit
of one mechanism, early runs, superseded boards. **Nothing under `specs/archive/` is a model
for anything.** It is kept as a record, and a board opened from it teaches whatever went wrong
there. For one technique at a time, `showcase/` is smaller and directed, and is the right place
over either.

When a *number* is wanted rather than an example, `GET /api/rules` and `GET /api/rules/terms`
answer in one fetch and are greppable. That is cheaper than any board.

## 2. The drill: predict three boards, then check

Three boards whose ground differs as much as anything in the flat set does. For each, read
**only** `specs/<slug>/renders/02-heightmap.txt` — about 6k tokens for all three — and write
down three numbers per board **before checking any of them**:

- `scramble%` and `barrier%` — the share of cells that are a scramble, and that are barrier
- how many **faces** the board has

| Board | |
|---|---|
| `opus5-alderfen` | a fen board |
| `fable-mossgill` | a gill board |
| `opus5-millrace` | a flooded basin |

Then check, at a cost of nothing:

```bash
for s in opus5-alderfen fable-mossgill opus5-millrace; do
  echo "== $s"; grep -h 'cells:\|faces:' specs/$s/renders/03-slopes.txt
done
```

One of the three is quiet underfoot and still carries the most impassable ground in the set.
A prediction that reads steepness and calls it passability will miss it, and missing it is the
point: `scramble` is ground a player climbs and `barrier` is ground a player cannot, and a
board is finished against the difference.

**Score it and write the errors into the run's report before authoring anything.** Within 3
percentage points on `scramble%` and `barrier%` is calibrated; outside 8 means the heightmap is
not being read, and the answer is one more board and a second attempt rather than starting to
build. A run that cannot predict a board it can see has no way to tell whether the board it
builds is the board it intended.

*(The 3-and-8 bands are a first setting and are the author's to move once a few runs have
scored.)*

## 3. Stop

Do not open a second render of any drill board, do not read their plans, and do not carry them
forward as models — they are calibration, not reference. Load `pgm-board` and begin.
