// Write a generated voxel volume to Minecraft 1.8 region files through the studio's own writer.
//
//   dotnet run write_world.cs -- <build-dir> <world-dir>
//
// <build-dir> holds what gen.py wrote:
//   volume.bin  "RWV1", int32 x0 y0 z0 sx sy sz, then uint16 ids[sx*sy*sz] and uint8 data[sx*sy*sz]
//               indexed ((x*sy)+y)*sz+z, then uint8 biomes[sx*sz] indexed x*sz+z
//   tiles.json  [{ "kind": "Chest", x, y, z, items: [{slot, id, count, damage, ench?: [[id, level], ..]}] },
//                { "kind": "Sign", x, y, z, lines: ["..", ..] },
//                { "kind": "Banner", x, y, z, base: <dye 0..15>, patterns: [{pattern, color}] }]
//   level.json  { name, spawn: [x, y, z] }
// Air is skipped, so a chunk exists only where something stands and the void stays void.
#:project /home/user/pgm-studio/src/PgmStudio.Minecraft/PgmStudio.Minecraft.csproj
#:property PublishAot=false

using System.Text.Json;
using System.Text.Json.Nodes;
using fNbt;
using PgmStudio.Minecraft.Anvil;

var buildDir = args[0];
var worldDir = args[1];

using var fs = File.OpenRead(Path.Combine(buildDir, "volume.bin"));
using var br = new BinaryReader(fs);
var magic = new string(br.ReadChars(4));
if (magic != "RWV1") throw new Exception("bad magic " + magic);
int x0 = br.ReadInt32(), y0 = br.ReadInt32(), z0 = br.ReadInt32();
int sx = br.ReadInt32(), sy = br.ReadInt32(), sz = br.ReadInt32();
var n = sx * sy * sz;
var idBytes = br.ReadBytes(n * 2);
var data = br.ReadBytes(n);
var biomes = br.ReadBytes(sx * sz);

var world = new VoxelWorld();
long placed = 0;
for (var x = 0; x < sx; x++)
for (var y = 0; y < sy; y++)
for (var z = 0; z < sz; z++)
{
    var i = (x * sy + y) * sz + z;
    var id = idBytes[2 * i] | (idBytes[2 * i + 1] << 8);
    if (id == 0) continue;
    world.SetBlock(x0 + x, y0 + y, z0 + z, id, data[i]);
    placed++;
}
for (var x = 0; x < sx; x++)
for (var z = 0; z < sz; z++)
    world.SetBiome(x0 + x, z0 + z, biomes[x * sz + z]);

var tiles = JsonNode.Parse(File.ReadAllText(Path.Combine(buildDir, "tiles.json")))!.AsArray();
foreach (var t in tiles)
{
    int tx = (int)t!["x"]!, ty = (int)t["y"]!, tz = (int)t["z"]!;
    var kind = (string)t["kind"]!;
    var tag = new NbtCompound { new NbtString("id", kind), new NbtInt("x", tx), new NbtInt("y", ty), new NbtInt("z", tz) };
    if (kind == "Chest")
    {
        var list = new NbtList("Items", NbtTagType.Compound);
        foreach (var it in t["items"]!.AsArray())
        {
            var item = new NbtCompound
            {
                new NbtByte("Slot", (byte)(int)it!["slot"]!),
                new NbtString("id", (string)it["id"]!),
                new NbtByte("Count", (byte)(int)it["count"]!),
                new NbtShort("Damage", (short)(int)(it["damage"] ?? 0)),
            };
            if (it["ench"] is JsonArray ench)
            {
                var list2 = new NbtList("ench", NbtTagType.Compound);
                foreach (var e in ench)
                    list2.Add(new NbtCompound { new NbtShort("id", (short)(int)e![0]!), new NbtShort("lvl", (short)(int)e[1]!) });
                item.Add(new NbtCompound("tag") { list2 });
            }
            list.Add(item);
        }
        tag.Add(list);
    }
    else if (kind == "Sign")
    {
        var lines = t["lines"]!.AsArray();
        for (var k = 0; k < 4; k++)
        {
            var text = k < lines.Count ? (string)lines[k]! : "";
            tag.Add(new NbtString($"Text{k + 1}", JsonSerializer.Serialize(new Dictionary<string, string> { ["text"] = text })));
        }
    }
    else if (kind == "Banner")
    {
        tag.Add(new NbtInt("Base", (int)t["base"]!));
        var pats = new NbtList("Patterns", NbtTagType.Compound);
        foreach (var p in (t["patterns"]?.AsArray() ?? new JsonArray()))
            pats.Add(new NbtCompound { new NbtString("Pattern", (string)p!["pattern"]!), new NbtInt("Color", (int)p["color"]!) });
        tag.Add(pats);
    }
    world.AddTileEntity(tx, tz, tag);
}

var level = JsonNode.Parse(File.ReadAllText(Path.Combine(buildDir, "level.json")))!;
var spawn = level["spawn"]!.AsArray();
AnvilRegionWriter.Write(world, Path.Combine(worldDir, "region"));
LevelDatWriter.Write(worldDir, (string)level["name"]!, (int)spawn[0]!, (int)spawn[1]!, (int)spawn[2]!,
    DateTimeOffset.UtcNow.ToUnixTimeMilliseconds());
Console.WriteLine($"wrote {placed} blocks, {tiles.Count} tile entities, {world.ChunkCoords.Count()} chunks -> {worldDir}");
