# pgm-studio-mapgen

Composed worlds and the configuration that produced them. Each map here was authored through
[pgm-studio](https://github.com/rockymine/pgm-studio) and is committed whole — `region/`, `level.dat`
and `map.xml` — so it can be pulled straight onto a machine with Minecraft and loaded without
rebuilding anything.

```
maps/<slug>/region/*.mca   the world
maps/<slug>/level.dat
maps/<slug>/map.xml        what a PGM server loads
maps/<slug>/renders/       top-down and surface renders, for looking at it without Minecraft
specs/<slug>.*.json        the plan, theme and room style that produced it
tools/                     the driver that turns those three into the world above
```

A map's `specs/` trio is the whole of what was authored; the world is derived from it and is
committed as the artifact rather than as a source. Rebuilding one needs a running pgm-studio API and
a migrated database.

## Maps

| Folder | `map.xml` name | Mode | Size | What it is |
|---|---|---|---|---|
| `clayclay_redux` | ClayClay Redux | CTW | 142×158 | A recreation of `OvercastCommunity/CommunityMaps/ctw/clayclay` — two rot_180 plus-shaped clay islands joined by four void hops. See [FINDINGS.md](FINDINGS.md). |
| `ashen_quarry` | Ashen Quarry | DTM | 360×240 | Authored from scratch rather than traced: a walled town on a raised polygon, a 17-deep quarry the destroyable stands in, a tilted mesa and an area-mark hill, on one interlocking landmass. **Work in progress** — no dressing yet. See [review/ashen_quarry.md](review/ashen_quarry.md). |

**A recreation never reuses the original's name.** Both the folder and the `<name>` in `map.xml` carry
a suffix, because a PGM server loading this repo alongside the community corpus would otherwise see
two maps calling themselves the same thing. The name lives in the plan document's `meta.name`, which
is what the compile reads — changing the folder alone is not enough.

## Rebuilding

```bash
dotnet run tools/build.cs -- specs/clayclay_redux/clayclay_redux.plan.json \
                             specs/clayclay_redux/clayclay_redux.theme.json \
                             specs/clayclay_redux/clayclay_redux.room.json \
                             specs/clayclay_redux/clayclay_redux.spawn-room.json \
                             specs/clayclay_redux/clayclay_redux.dressing.json \
                             "ClayClay Redux" out.zip
```

`tools/column-probe.cs` prints one vertical column of a built world, which is the only way to check a
layered wall or a stamped room — every renderer in the studio is plan-view.

## Reports

| File | Is |
|---|---|
| [FINDINGS.md](FINDINGS.md) | the measured record — what the original is, what the recreation reproduces, and every gap found, per review round |
| [AGENT-REPORT.md](AGENT-REPORT.md) | an opinion piece from the agent that authored the map: why the `mapgen` spec was the wrong layer to work at, what the documentation got right, and an account of the two claims it got wrong |
| `review/` | the author's reviews of each build |
