// Export the studio's own block knowledge for pgmvox: every 1.8 id's name, role, shape and colour per data
// value, and the data each block takes under the five symmetry operations, as the studio turns it.
//
//   dotnet run export_blocks.cs -- <out.json>
//
// pgmvox reads the JSON this writes; nothing in the library keeps a colour or a turn table of its own, so a
// change in the studio reaches every freeform board by re-running this export.
#:project /home/user/pgm-studio/src/PgmStudio.Minecraft/PgmStudio.Minecraft.csproj
#:property PublishAot=false

using System.Text.Json;
using PgmStudio.Minecraft.Palette;

var ops = new Dictionary<string, Func<int, int, (int X, int Z)>>
{
    ["cw"] = (x, z) => (-z, x),          // a quarter turn clockwise seen from above: east to south
    ["ccw"] = (x, z) => (z, -x),
    ["half"] = (x, z) => (-x, -z),
    ["mirror_x"] = (x, z) => (-x, z),    // flip east and west
    ["mirror_z"] = (x, z) => (x, -z),    // flip north and south
};
var blocks = new List<object>();
for (var id = 0; id < BlockVariants.BlockIdCount; id++)
{
    var names = new string[16];
    var colours = new string[16];
    for (var d = 0; d < 16; d++)
    {
        names[d] = BlockPalette.Name(id, d);
        colours[d] = BlockPalette.Hex(id, d);
    }
    var turned = ops.ToDictionary(o => o.Key, o => Enumerable.Range(0, 16).Select(d => BlockGeometry.Turned(id, d, o.Value)).ToArray());
    blocks.Add(new
    {
        id,
        name = BlockPalette.Name(id, 0),
        role = BlockRoles.Of(id).ToString().ToLowerInvariant(),
        stood_through = BlockRoles.StoodThrough(id),
        full_cube = BlockRoles.IsFullCube(id),
        seen_through = BlockRoles.SeenThrough(id),
        stands_on_ground = BlockRoles.StandsOnGround(id),
        liquid = BlockRoles.IsLiquid(id),
        stair = BlockFamilies.IsStair(id),
        slab = BlockFamilies.IsSlab(id),
        fronted = BlockFamilies.IsFronted(id),
        torch = BlockFamilies.IsTorch(id),
        fence_gate = BlockFamilies.IsFenceGate(id),
        names,
        colours,
        turned,
    });
}
var outPath = args[0];
File.WriteAllText(outPath, JsonSerializer.Serialize(new { source = "PgmStudio.Minecraft.Palette", blocks }));
Console.WriteLine($"wrote {blocks.Count} block ids to {outPath}");
