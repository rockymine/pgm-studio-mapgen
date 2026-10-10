// Export the studio's SurfaceGradient answers over test grounds, so pgmvox.terrain.slope_deg is tested against the
// studio's own reading of slope, cell for cell.
//
//   python3 slope_cases.py cases.json
//   dotnet run export_slopes.cs -- cases.json slopes.json && gzip -9 -f slopes.json
//
// Each case is a grid of tops with null where the ground is not (off the footprint); each answer is the degrees
// at every cell that has ground, at windows 1, 2 and 3.
#:project /home/user/pgm-studio/src/PgmStudio.Geom/PgmStudio.Geom.csproj
#:property PublishAot=false

using System.Text.Json;
using PgmStudio.Geom.Algorithms;

var cases = JsonSerializer.Deserialize<List<int?[][]>>(File.ReadAllText(args[0]))!;
var answers = new List<object>();
foreach (var grid in cases)
{
    var tops = new Dictionary<(int, int), int>();
    for (var x = 0; x < grid.Length; x++)
        for (var z = 0; z < grid[x].Length; z++)
            if (grid[x][z] is { } t) tops[(x, z)] = t;
    var byWindow = new Dictionary<string, int[][]>();
    foreach (var window in new[] { 1, 2, 3 })
        byWindow[window.ToString()] = Enumerable.Range(0, grid.Length).Select(x =>
            Enumerable.Range(0, grid[x].Length).Select(z =>
                tops.ContainsKey((x, z)) ? SurfaceGradient.Degrees(tops, x, z, window) : -1).ToArray()).ToArray();
    answers.Add(new { grid, degrees = byWindow });
}
File.WriteAllText(args[1], JsonSerializer.Serialize(answers));
Console.WriteLine($"{answers.Count} grounds");
