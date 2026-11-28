# The AI Studio app "Minecraft CTW Map Generator"

`aistudio-export-2026-11-28.zip` is the author's download of his Google AI Studio app, sent on 28 November 2026
(twenty-second instalment of his account). The app's address today is
`https://aistudio.google.com/apps/646f11e8-105c-43af-96b8-41eb1e89ff92`; it opens only for a signed-in Google account.
The author had to migrate the app and no longer has the chat it was made in.

**The export is the repository `CTW-Layout-Generator`, file for file.** All eleven source files (`App.tsx`,
`types.ts`, `lib/mapGenerator.ts` and the eight components), `package.json`, `index.tsx`, `tsconfig.json` and
`.gitignore` are identical to the repository's last commit, `ec9ca62` of 3 October 2025, 22:12 +0200. Four files
differ, none of them in the app's logic: `README.md` (the banner picture and the app link, which in the repository is
`ai.studio/apps/drive/1hrvcpxAKMVquEG6UF8FFPvDKL90Juip2`), `metadata.json` (3 lines), `index.html` (1 line) and
`vite.config.ts` (9 lines). The app therefore stands where it stood on 3 October 2025.

**The repository's five commits.** `2aed35c`, 28 September 2025 02:42 +0200, "Initial commit" (committer GitHub);
`6691417` and `84ca4c2`, 1 October 00:05 and 00:25, "initialize project" and "refactor ui"; `3eab815` and `ec9ca62`,
3 October 22:04 and 22:12, "fix: styling, feat: step-wise manual editor" and "feat: add snapping to intra-team
horizontal symmetry line".

**The app calls no model.** Its code holds no Gemini client and no network call; `package.json` depends on React
alone. Gemini wrote the app; the layouts come from a seeded generator in `lib/mapGenerator.ts`.

## The pictures

Taken on 28 November 2026 from a local build of the export. The page's Tailwind stylesheet and React were installed
from npm for the build, where the app loads them from a CDN; nothing else was changed.

| File | What it shows |
|---|---|
| `01-generator-two-teams.png` | "Minecraft CTW Tools", tab "Generator": two teams, team width 90, height 160, gap 24, lane width 4, a random seed; nodes, lanes and dashed void crossings; "Regenerate Layout", "New Map", "Download JSON" |
| `02-generator-four-teams.png` | the same with four teams |
| `03-generator-settings-open.png` | the panels open: grid mode Standard or Row-Independent, symmetry Mirror or Rotation, islands, spawn locations, what to show |
| `04-documentation.png` | the app's own documentation: the 3×3 grid of zones, the node types (spawn, spawn entry, wool, wool entry and more) and their placement rules |
| `05-manual-editor.png` | tab "Manual Editor", three steps (Setup, Placement, Routes): canvas size, a background image to trace, map scope and two symmetries |

The layouts in the pictures are today's random output; the seed is on screen.
