#:project /home/user/pgm-studio/src/PgmStudio.Minecraft/PgmStudio.Minecraft.csproj
#:property JsonSerializerIsReflectionEnabledByDefault=true
#:property PublishAot=false
#:property TreatWarningsAsErrors=false
// Scratch: draw a world folder through the studio's eye renderer.
//   dotnet run eye.cs <worldDir> info
//   dotnet run eye.cs <worldDir> <jobs.json> <outDir>
// jobs.json: [{ "name": "a", "w":1280, "h":720, "frames": 1,
//               "from": {"x":0,"y":40,"z":-60,"yaw":0,"pitch":20,"fov":70}, "to": {...}? }]
using System.Diagnostics;
using System.Text.Json;
using PgmStudio.Minecraft.Anvil;
using PgmStudio.Minecraft.Render;

var worldDir = args[0];
var regionDir = Directory.Exists(Path.Combine(worldDir, "region")) ? Path.Combine(worldDir, "region") : worldDir;
var world = new VoxelWorld();
int minX = int.MaxValue, maxX = int.MinValue, minY = int.MaxValue, maxY = int.MinValue, minZ = int.MaxValue, maxZ = int.MinValue;
long count = 0;
var tops = new Dictionary<(int, int), int>();
if (worldDir != "empty") foreach (var block in Directory.GetFiles(regionDir, "*.mca").SelectMany(AnvilRegion.ReadChunks).SelectMany(AnvilRegion.Blocks))
{
    if (block.Id == 0) continue;
    world.SetBlock(block.X, block.Y, block.Z, block.Id, block.Data);
    count++;
    if (block.X < minX) minX = block.X; if (block.X > maxX) maxX = block.X;
    if (block.Y < minY) minY = block.Y; if (block.Y > maxY) maxY = block.Y;
    if (block.Z < minZ) minZ = block.Z; if (block.Z > maxZ) maxZ = block.Z;
    if (!tops.TryGetValue((block.X, block.Z), out var top) || block.Y > top) tops[(block.X, block.Z)] = block.Y;
}
if (Environment.GetEnvironmentVariable("EDITS") is { Length: > 0 } editFile)
    foreach (var edit in JsonSerializer.Deserialize<int[][]>(File.ReadAllText(editFile))!)
    {
        // [x,y,z,id,data?] sets one block; [x0,y0,z0,x1,y1,z1,id,data] fills a box
        if (edit.Length >= 8)
        {
            for (var x = Math.Min(edit[0], edit[3]); x <= Math.Max(edit[0], edit[3]); x++)
                for (var y = Math.Min(edit[1], edit[4]); y <= Math.Max(edit[1], edit[4]); y++)
                    for (var z = Math.Min(edit[2], edit[5]); z <= Math.Max(edit[2], edit[5]); z++)
                        world.SetBlock(x, y, z, edit[6], edit[7]);
            minX = Math.Min(minX, Math.Min(edit[0], edit[3])); maxX = Math.Max(maxX, Math.Max(edit[0], edit[3]));
            minY = Math.Min(minY, Math.Min(edit[1], edit[4])); maxY = Math.Max(maxY, Math.Max(edit[1], edit[4]));
            minZ = Math.Min(minZ, Math.Min(edit[2], edit[5])); maxZ = Math.Max(maxZ, Math.Max(edit[2], edit[5]));
        }
        else world.SetBlock(edit[0], edit[1], edit[2], edit[3], edit.Length > 4 ? edit[4] : 0);
    }
Console.WriteLine($"blocks {count}  x {minX}..{maxX}  y {minY}..{maxY}  z {minZ}..{maxZ}");
if (args[1] == "find")
{
    // find <id[,id...]> [x0 y0 z0 x1 y1 z1]  -> clusters of matching blocks (bounding boxes), biggest first
    var ids = args[2].Split(',').Select(int.Parse).ToHashSet();
    int[]? within = args.Length >= 9 ? args[3..9].Select(int.Parse).ToArray() : null;
    var hits = new List<(int X, int Y, int Z, int Id, int Data)>();
    for (var x = within?[0] ?? minX; x <= (within?[3] ?? maxX); x++)
        for (var z = within?[2] ?? minZ; z <= (within?[5] ?? maxZ); z++)
            for (var y = within?[1] ?? minY; y <= (within?[4] ?? maxY); y++)
            {
                var (id, data) = world.GetBlock(x, y, z);
                if (ids.Contains(id)) hits.Add((x, y, z, id, data));
            }
    // cluster by 3-block proximity (grid buckets of 4)
    var clusters = hits.GroupBy(h => (h.X >> 3, h.Z >> 3)).OrderByDescending(g => g.Count()).Take(60);
    Console.WriteLine($"{hits.Count} blocks");
    foreach (var cluster in clusters)
        Console.WriteLine($"  n={cluster.Count(),5}  x {cluster.Min(h => h.X)}..{cluster.Max(h => h.X)}  y {cluster.Min(h => h.Y)}..{cluster.Max(h => h.Y)}  z {cluster.Min(h => h.Z)}..{cluster.Max(h => h.Z)}  ids {string.Join(",", cluster.Select(h => $"{h.Id}:{h.Data}").Distinct().Take(6))}");
    return;
}
if (args[1] == "slice")
{
    // slice <y> [x0 z0 x1 z1] -> block ids at one level, as a grid of 3-char cells
    var level = int.Parse(args[2]);
    int[]? within = args.Length >= 7 ? args[3..7].Select(int.Parse).ToArray() : null;
    for (var z = within?[1] ?? minZ; z <= (within?[3] ?? maxZ); z++)
    {
        var line = new System.Text.StringBuilder($"{z,5} ");
        for (var x = within?[0] ?? minX; x <= (within?[2] ?? maxX); x++) { var id = world.GetBlock(x, level, z).Id; line.Append(id == 0 ? "  ." : $"{id,3}"); }
        Console.WriteLine(line);
    }
    return;
}
if (args[1] == "info")
{
    var step = args.Length > 2 ? int.Parse(args[2]) : 4;
    for (var z = minZ; z <= maxZ; z += step)
    {
        var line = new System.Text.StringBuilder();
        for (var x = minX; x <= maxX; x += step)
            line.Append(tops.TryGetValue((x, z), out var top) ? (char)(top < 10 ? '0' + top : top < 36 ? 'a' + top - 10 : top < 62 ? 'A' + top - 36 : '#') : ' ');
        Console.WriteLine($"{z,5} {line}");
    }
    return;
}
await using var jar = File.OpenRead(Environment.GetEnvironmentVariable("JAR") ?? "/tmp/claude-0/-home-user/5b5a763a-8f02-5e92-a825-a8c273c7b88d/scratchpad/tex/client.jar");
var scene = EyeScene.Of(world, BlockTextureSet.FromJar(jar));
List<Job> jobs;
var outDir = args[2];
if (args[1] == "overview")
{
    // four corners and one from straight above, each looking at the middle of the board
    var name = args.Length > 3 ? args[3] : "ov";
    double midX = (minX + maxX) / 2.0, midZ = (minZ + maxZ) / 2.0, spanX = maxX - minX, spanZ = maxZ - minZ;
    var groundY = tops.Values.OrderBy(v => v).ElementAt(tops.Count / 2);
    var reach = Math.Max(spanX, spanZ);
    jobs = [];
    var corner = 0;
    foreach (var (sx, sz) in new[] { (1, 1), (-1, 1), (-1, -1), (1, -1) })
    {
        double x = midX + sx * spanX * 0.62, z = midZ + sz * spanZ * 0.62, y = groundY + reach * 0.55;
        var yaw = Math.Atan2(-(midX - x), midZ - z) * 180 / Math.PI;
        var pitch = Math.Atan2(y - groundY, Math.Sqrt((midX - x) * (midX - x) + (midZ - z) * (midZ - z))) * 180 / Math.PI;
        jobs.Add(new Job($"{name}-c{corner++}", new Cam(x, y, z, yaw, pitch, 70), W: 960, H: 540));
    }
    jobs.Add(new Job($"{name}-top", new Cam(midX, groundY + reach * 0.95, midZ + 0.01, 180, 89.9, 70), W: 960, H: 540));
    Console.WriteLine($"ground~{groundY}");
}
else jobs = JsonSerializer.Deserialize<List<Job>>(File.ReadAllText(args[1]), new JsonSerializerOptions { PropertyNameCaseInsensitive = true })!;
Directory.CreateDirectory(outDir);
foreach (var job in jobs)
{
    var watch = Stopwatch.StartNew();
    var to = job.To ?? job.From;
    for (var frame = 0; frame < job.Frames; frame++)
    {
        var t = job.Frames == 1 ? 0 : (double)frame / (job.Frames - 1);
        if (job.Ease) t = t * t * (3 - 2 * t);
        double Mix(double a, double b) => a + (b - a) * t;
        var camera = new EyeCamera(Mix(job.From.X, to.X), Mix(job.From.Y, to.Y), Mix(job.From.Z, to.Z),
                                   Mix(job.From.Yaw, to.Yaw), Mix(job.From.Pitch, to.Pitch), Mix(job.From.Fov, to.Fov));
        var picture = scene.Draw(camera, job.W, job.H, job.Ss);
        var name = job.Frames == 1 ? $"{job.Name}.png" : $"{job.Name}-{frame:0000}.png";
        File.WriteAllBytes(Path.Combine(outDir, name), picture.Png());
        if (job.Depth)
        {
            // depth along the view axis to the block each pixel's ray hits, at half size: R,G = depth * 64 (16 bit), B = 255 where sky
            int dw = job.W / 2, dh = job.H / 2;
            var depth = new byte[dw * dh * 3];
            var yawR = camera.Yaw * Math.PI / 180; var pitchR = camera.Pitch * Math.PI / 180;
            var fwd = (X: -Math.Sin(yawR) * Math.Cos(pitchR), Y: -Math.Sin(pitchR), Z: Math.Cos(yawR) * Math.Cos(pitchR));
            Parallel.For(0, dh, row =>
            {
                for (var col = 0; col < dw; col++)
                {
                    var o = (row * dw + col) * 3;
                    if (scene.Pick(camera, dw, dh, col, row) is { } hit)
                    {
                        var d = (hit.Block.X + 0.5 - camera.X) * fwd.X + (hit.Block.Y + 0.5 - camera.Y) * fwd.Y + (hit.Block.Z + 0.5 - camera.Z) * fwd.Z;
                        var v = (int)Math.Clamp(d * 64, 0, 65535);
                        depth[o] = (byte)(v >> 8); depth[o + 1] = (byte)(v & 255);
                    }
                    else depth[o + 2] = 255;
                }
            });
            File.WriteAllBytes(Path.Combine(outDir, name.Replace(".png", ".depth.png")), PgmStudio.Geom.Render.PngWriter.Encode(dw, dh, depth));
        }
    }
    Console.WriteLine($"{job.Name}: {job.Frames} frame(s) in {watch.Elapsed.TotalSeconds:0.0}s");
}

record Cam(double X, double Y, double Z, double Yaw, double Pitch, double Fov = 70);
record Job(string Name, Cam From, Cam? To = null, int Frames = 1, int W = 1280, int H = 720, int Ss = 2, bool Ease = true, bool Depth = false);
