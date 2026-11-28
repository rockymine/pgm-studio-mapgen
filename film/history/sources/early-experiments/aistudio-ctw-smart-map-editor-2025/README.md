# The AI Studio app "CTW Smart Map Editor"

`aistudio-export-2026-11-28.zip` is the author's download of his second Google AI Studio project, sent on 28 November
2026 as "der Export des anderen Projekts auf aistudio" (twenty-third instalment of his account). The export's README
gives its address as `https://ai.studio/apps/64b87bef-555a-4d66-83f5-a76f377a3cc1`. The files carry the time of the
export, not of their writing, and no repository of this code is in the record, so the export itself dates nothing.

**It is a manual editor for a layout as a graph.** `metadata.json` describes it as "a web-based tool for game
designers to create, document, and analyze 'Capture the Wool' (CTW) map layouts using a structured graph-based approach
with enforced symmetry and AI-powered analysis". A new project asks for a map name, a team side width (120 blocks by
default), a middle gap (40) and a map height (100). The tools are Select, Node, Edge, Rect, Path, Delete and Clear, with
undo and redo; the result is saved with "Export JSON". 25 files, about 2,250 lines of TypeScript.

**Every node and edge is mirrored for the other team as it is placed.** `services/mapLogic.ts` keeps a `mirroredId` on
each node and edge and mirrors the x coordinate across the middle (`mirrorCoordinates`).

**The author places three kinds of node and the app names the rest from the graph.** By hand: Spawn, Wool Room and
Intersection. "Auto-Classify Nodes" (`classifyNodes`) then renames each intersection in this order: Island for a node
with no edge, Wool Entry beside a wool room, Spawn Entry beside a spawn, Hub for three or more edges, Frontline for
exactly one, Scaffold otherwise. Edges are Walkway or Bridge. "Path" finds the shortest path between two nodes.

**"Validate Map" checks two things.** A spawn and a wool room for each team are errors when missing; unconnected
nodes are a warning. The report goes to the browser console.

**The analysis by a model is written but not connected.** `services/geminiService.ts` would send the layout as JSON to
`gemini-2.5-flash` with a prompt that begins "You are an expert game designer specializing in 'Capture the Wool' (CTW)
maps for Minecraft" and asks for an overall impression, strategic strengths, potential weaknesses and actionable
suggestions. No other file imports or calls it, and the interface has no button for it.

**It is the link of 7 October 2025, by the author's word.** That day he sent Ruediger an AI Studio link with "nur
manueller editor" (eighteenth instalment); on 28 November 2026 he confirmed that this project was that link
(twenty-fourth instalment). The link's id of then cannot be compared, because the apps were migrated and their ids
changed.

**The author did not know the analysis was in it.** Told of `geminiService.ts`, he said it was completely new to him,
that he will therefore never have tested it, and that it would probably not have delivered anything good then.

## The pictures

Taken on 28 November 2026 from a local build of the export, with the stylesheet and libraries installed from npm where
the app loads them from a CDN, and with no API key.

| File | What it shows |
|---|---|
| `01-new-project.png` | the "Create New Project" dialogue with its defaults |
| `02-empty-canvas.png` | the empty canvas after "Create Map" |
| `03-a-graph-drawn-for-the-picture.png` | seven nodes and seven walkways placed for the picture on 28 November 2026, not a layout of the author's: a spawn (square), two wool rooms (hexagons) and four intersections, after "Auto-Classify Nodes", with both teams listed (14 nodes, 14 edges) |
