// Compose a board with the studio's own generator and say what its deriver reads off it, as JSON a board script can
// lay: the plan itself, and the fanned board in cells — every standing cell and the piece and image it is, where
// building is allowed and what each build region links, the islands and their roles, the enclosed voids and their
// classes, and every wool room. pgmvox.plan.composed reads it.
//
//   dotnet run compose_board.cs -- <players> <symmetry> <seed> <out.json>
//   dotnet run compose_board.cs -- <players> <symmetry> <first>-<last>      a line a seed: wools, size, voids
#:project /home/user/pgm-studio/src/PgmStudio.Pgm/PgmStudio.Pgm.csproj
#:property PublishAot=false
#:property JsonSerializerIsReflectionEnabledByDefault=true

using System.Text.Json;
using PgmStudio.Pgm.Compose;
using PgmStudio.Pgm.Derive;
using PgmStudio.Pgm.Plan;

int players = int.Parse(args[0]);
string sym = args[1];
if (args[2].Contains('-'))
{
    var span = args[2].Split('-').Select(ulong.Parse).ToArray();
    for (var sd = span[0]; sd <= span[1]; sd++)
    {
        var st = Composer.ComposeStages(new ComposeRequest(players, 2, sym, sd, 5));
        var p = PlanVoids.Declare(st.Plan);
        PlanBoxAnnotation.Apply(p, st.Unit);
        var g = BoardDeriver.Ground(p);
        var d = BoardDeriver.Derive(g);
        var xs = d.Filled.Keys.Select(c => c.Item1).ToList();
        var zs = d.Filled.Keys.Select(c => c.Item2).ToList();
        Console.WriteLine($"seed {sd}: {g.WoolRooms.Count} wool rooms, {xs.Max() - xs.Min() + 1}x{zs.Max() - zs.Min() + 1} cells, " +
                          $"{d.Islands.Count} islands, {d.Voids.Count} voids [{string.Join(",", d.Voids.Select(v => v.Class))}], " +
                          $"mid {d.MidForm}, boxes {string.Join(" ", p.Boxes.Select(b => b.Kind))}");
    }
    return;
}
ulong seed = ulong.Parse(args[2]);
var stages = Composer.ComposeStages(new ComposeRequest(players, 2, sym, seed, 5));
var plan = PlanVoids.Declare(stages.Plan);
PlanBoxAnnotation.Apply(plan, stages.Unit);
var ground = BoardDeriver.Ground(plan);
var s = BoardDeriver.Derive(ground);

var cells = new List<int[]>();
var cellOwner = new List<string>();
foreach (var ((x, z), (owner, k)) in s.Filled)
{
    cells.Add([x, z, k]);
    cellOwner.Add(owner);
}
var doc = new
{
    players, symmetry = sym, seed, cell = s.Cell, midForm = s.MidForm,
    plan = JsonDocument.Parse(plan.ToJson()).RootElement,
    filled = cells, owners = cellOwner,
    build = s.Build.Select(c => new[] { c.Item1, c.Item2 }),
    buildKind = s.BuildKindOf.Select(kv => new { x = kv.Key.Item1, z = kv.Key.Item2, kind = kv.Value }),
    islands = s.Islands.Select((cs, i) => new
    {
        role = s.Roles[i], stepping = s.SteppingKind[i], cells = cs.Select(c => new[] { c.Item1, c.Item2 }),
    }),
    voids = s.Voids.Select(v => new
    {
        cls = v.Class, declared = v.Declared, crossRoutes = v.CrossRoutes, cells = v.Cells.Select(c => new[] { c.Item1, c.Item2 }),
    }),
    woolRooms = ground.WoolRooms.Select(r => new
    {
        wool = r.Wool, k = r.K, mx = r.MarkerX, mz = r.MarkerZ, cells = r.Cells.Select(c => new[] { c.Item1, c.Item2 }),
    }),
    spawnOwners = ground.SpawnOwners, woolOwners = ground.WoolOwners,
    zones = s.Zones.Select(z => new { kind = z.Kind, neutrals = z.Neutrals, width = z.Width }),
};
File.WriteAllText(args[3], JsonSerializer.Serialize(doc, new JsonSerializerOptions { WriteIndented = false }));
Console.WriteLine($"composed {players} players, {sym}, seed {seed}: cell {s.Cell}, {s.Filled.Count} standing cells, " +
                  $"{s.Islands.Count} islands, {s.Voids.Count} enclosed voids, mid {s.MidForm}");
