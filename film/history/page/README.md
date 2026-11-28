# The reading page

`build.py` turns `HISTORY.md`, `timeline.md`, `OUTLINE.md`, `interview-questions.md` and `storyboard.json` into one
HTML page with five views (outline, storyboard, the history, timeline, open questions) and copies every picture the
storyboard and the chapters use into `out/img/` as a resized JPEG. `page.tmpl.html` is its layout; `look.cjs` renders
the result at desktop and phone width in both themes for a check before publishing.

It needs Python with `markdown` and `Pillow`. The paths at the top of `build.py` name the machine it was written on;
run it from a copy of this folder and publish `out/index.html` with the files under `out/img/`.
