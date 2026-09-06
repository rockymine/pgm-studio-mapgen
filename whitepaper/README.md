# whitepaper/

Presentation material about pgm-studio and how maps are authored in it — written for mapmakers who have
never seen the studio, and for anyone weighing up whether an agent can be trusted to author a board.

Everything here was produced against a **running studio** rather than from documents. The board it is built
around, **Marlbeck**, was authored from nothing while the paper was being written; every refusal, complaint
and number quoted is the studio's own answer, reproduced verbatim.

```
white-paper.md            the paper — 12 sections, 15 figures, ~11,700 words
presentation/index.html   the same argument as 33 slides; open it in a browser
docs-audit.md             34 factual errors found in pgm-studio's own docs, and which were fixed
figures/                  the studio's own surfaces, screenshotted live
marlbeck/                 the worked example: its two authored documents, its world, and 40 read-backs
```

## The paper

`white-paper.md` argues three things and shows the evidence for each.

1. **Describing a map as four documents makes it checkable.** A plan is forty lines and answers `GO1` in two
   seconds; a world is a million blocks and answers nothing.
2. **A system that refuses by name and answers in numbers can be driven by an agent without a human watching
   each step.** 111 built worlds in this repository say so, and so does §5, which is one more.
3. **The seam between what a person decides and what a model derives is real, and it moves** — every
   capability that turns a matter of taste into a question with a read behind it moves it, and the corpus
   dates each one.

It is honest about what the studio does not do. §10 is a limits section with real numbers in it, including
this board's own 34.4% dead ground and the one complaint it ships with.

## The deck

`presentation/index.html` is self-contained — no build step, no dependencies, no network beyond two Google
Fonts that degrade to a system stack. Arrow keys, click, or swipe; `#12` in the URL deep-links to a slide;
**Print** lays every slide out one per page for a PDF.

## Marlbeck

A destroy-the-monument board, 84 × 256 blocks under `rot_180`, one monument a team, the two halves joined
only by a build zone over a 32-block strait. It exists to be looked at rather than to be played, and
`marlbeck/README.md` says what it is and what it took.

```bash
export PGM_STUDIO_API=http://localhost:7894/api
python3 tools/drive.py whitepaper/marlbeck "Marlbeck" \
        --out whitepaper/marlbeck/world --renders whitepaper/marlbeck/renders
```

It ships **0 barrier cells and 0 faces** over eighteen blocks of relief, a symmetry error of zero, and one
open `DR-DRY` complaint that §5.5 of the paper explains rather than hides.

## The audit

`docs-audit.md` is a by-product worth its own file. Reading the studio's code closely enough to describe it
turned up 34 measurable errors in its own documentation — a type name that does not exist, a rule family
missing from a table that claims to list them all, and twenty-two stale counts. The distribution is the
finding: **every documented endpoint, path and failure code is correct**, because three tests parse the
endpoint tables and fail when a row and a route disagree. Every stale figure is in ungated prose.

The clear ones are fixed in `rockymine/pgm-studio` on
`claude/pgm-studio-mapmaking-whitepaper-raxcr2`; the rest are listed with the reason they were left.

## Reproducing the figures

The UI screenshots in `figures/` are Chromium at 1600 × 1000, `deviceScaleFactor: 2`, against a studio with
Marlbeck stored. The world renders in `marlbeck/renders/` are what `tools/drive.py` writes on every run — the
studio's own `/render/*` answers, plus the isometric and x-ray it draws from the per-column runs, plus
twelve `?format=text` reads.

Nothing here is drawn by hand, and nothing is a mock-up.
