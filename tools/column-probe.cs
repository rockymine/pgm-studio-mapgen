#:project ../src/PgmStudio.Minecraft/PgmStudio.Minecraft.csproj
// Print one vertical column of a built world, top block to bottom — the section view no renderer offers.
//   dotnet run tools/column-probe.cs -- <regionDir> <x> <z> [x z ...]
using PgmStudio.Minecraft;

var regionDir = args[0];
var wanted = new HashSet<(int X, int Z)>();
for (var i = 1; i + 1 < args.Length; i += 2)
    wanted.Add((int.Parse(args[i]), int.Parse(args[i + 1])));

var column = wanted.ToDictionary(cell => cell, _ => new List<WorldBlock>());
foreach (var chunk in Directory.GetFiles(regionDir, "*.mca").SelectMany(AnvilRegion.ReadChunks))
    foreach (var cell in AnvilRegion.Blocks(chunk))
        if (column.TryGetValue((cell.X, cell.Z), out var stack))
            stack.Add(cell);

foreach (var ((x, z), stack) in column)
{
    Console.WriteLine($"=== column ({x}, {z}) — {stack.Count} solid blocks ===");
    foreach (var cell in stack.OrderByDescending(b => b.Y))
        Console.WriteLine($"  y{cell.Y,3}  {cell.Id,4}:{cell.Data,-2}  {BlockPalette.Name(cell.Id, cell.Data)}");
}
