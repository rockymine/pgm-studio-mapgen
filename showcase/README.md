# showcase/ — one technique per map

Every map in `maps/` is a board: a whole design, with a dozen decisions in it at once. That makes them poor
things to learn from. A reader who wants to know *how a cliff is stated* has to find the cliff inside a
thousand-line finish and work out which of its fields are the cliff and which are the map around it.

A showcase is the other thing. It is **one technique, on a board that does nothing else**, so the document
that states it is short enough to read in full and small enough to paste into an example. Each folder here is
a complete map — it compiles, it builds, it exports, a server would load it — and the only reason it exists is
the one line in its README saying what it demonstrates.

## The rule that makes them readable

**Every showcase forks `01-base-board`'s plan and changes only what its technique needs.** The base board is
the smallest legal capture board there is: two teams, one wool each, `rot_180`, a gap in the middle that is
crossed by building. It scores 0 against the evaluator with no violation and no lint, so anything a showcase's
evaluation says is about the technique rather than about the board.

That makes the **diff the lesson**. A reader comparing `06-cliff`'s plan against `01-base-board`'s sees the
technique and nothing else, and a reader comparing two showcases against each other sees exactly what
separates two ways of moving ground.

## What a folder holds

```
<nn>-<concept>/
  README.md                    what the technique is, the document that says it, what to look at
  <nn>-<concept>.plan.json     the board            — authored
  <nn>-<concept>.finish.json   the technique        — authored
  <nn>-<concept>.layout.json   what was posted      — written by the driver
  <nn>-<concept>.intent.json   what was posted      — written by the driver
  renders/                     the pictures it was reviewed from, including the board grid and the flow
  world/                       region/, level.dat, map.xml — what a server loads
```

The two authored files are the whole of the input. Everything else is derived from them and committed so a
reader can see the result without a running studio.

## Running one

```bash
python3 tools/drive.py showcase/<nn>-<concept> "<Map Name>" --out showcase/<nn>-<concept>/world
```

The driver posts the two documents through the whole pipeline and prints every finding at every place one can
appear. `tools/README.md` documents it; `AUTHORING-BRIEF.md` is the authoring account these were written
against.

## The showcases

| | Folder | The technique | Said in |
|---|---|---|---|
| 01 | `01-base-board` | the smallest legal capture board, and what "legal" is measured by | the plan alone |
