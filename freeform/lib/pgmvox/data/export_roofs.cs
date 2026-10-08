// Export the studio's RoofField answers over a set of cases, so pgmvox.build's roof is tested against the
// studio's own formulas block for block rather than against a copy of them.
//
//   dotnet run export_roofs.cs -- roofs.json && gzip -9 -f roofs.json
//
// Each case is one roof; each cell it covers gives crown, riser, half, upslope, on_ridge and past_verge.
#:project /home/user/pgm-studio/src/PgmStudio.Minecraft/PgmStudio.Minecraft.csproj
#:property PublishAot=false

using System.Text.Json;
using PgmStudio.Domain;
using PgmStudio.Minecraft.Houses;

var cases = new List<object>();
var edges = new[] { RoomEdge.NegZ, RoomEdge.PosZ, RoomEdge.NegX, RoomEdge.PosX };
var names = new[] { "n", "s", "w", "e" };
var boxes = new[] { (0, 0, 8, 4), (0, 0, 5, 11), (-3, 2, 3, 8), (0, 0, 14, 6), (0, 0, 9, 9) };
foreach (var form in Enum.GetValues<RoofForm>())
    foreach (var (x0, z0, x1, z1) in boxes)
        foreach (var (overhang, pitch, halves) in new[] { (0, 1, false), (1, 1, false), (2, 1, true), (1, 2, false), (1, 1, true) })
            foreach (var f in new[] { 1, 3 })
            {
                var field = new RoofField(form, x0, z0, x1, z1, overhang, 70, pitch, edges[f], halves);
                var cells = new List<object>();
                for (var x = field.MinX; x <= field.MaxX; x++)
                    for (var z = field.MinZ; z <= field.MaxZ; z++)
                    {
                        var up = field.Upslope(x, z);
                        cells.Add(new object[] { x, z, field.Crown(x, z), field.Riser(x, z), field.Half(x, z),
                            up is { } u ? names[(int)u] : "", field.OnRidge(x, z), field.PastVerge(x, z) });
                    }
                cases.Add(new
                {
                    form = form.ToString().ToLowerInvariant(), box = new[] { x0, z0, x1, z1 }, overhang, pitch,
                    halves, front = names[f], peak = field.Peak, trough = field.Trough, cells,
                });
            }
File.WriteAllText(args[0], JsonSerializer.Serialize(cases));
Console.WriteLine($"{cases.Count} roofs");
