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

| Slug | Mode | Size | What it is |
|---|---|---|---|
| `clayclay` | CTW | 142×158 | A recreation of `OvercastCommunity/CommunityMaps/ctw/clayclay` — two rot_180 plus-shaped clay islands joined by four void hops. See [FINDINGS.md](FINDINGS.md). |

## Rebuilding

```bash
dotnet run tools/build.cs -- specs/clayclay.plan.json \
                             specs/clayclay.theme.json \
                             specs/clayclay.room.json \
                             "ClayClay" out.zip
```

`tools/column-probe.cs` prints one vertical column of a built world, which is the only way to check a
layered wall or a stamped room — every renderer in the studio is plan-view.
