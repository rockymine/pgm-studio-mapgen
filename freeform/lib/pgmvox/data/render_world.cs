// Draw a generated voxel volume with the studio's own textured renderer (EyeScene, the game's sprites).
//
//   dotnet run render_world.cs -- <build-dir> <client-1.8.9.jar> <shots.json>
//
// <build-dir> is what gen.py wrote (volume.bin, as write_world.cs reads it). <shots.json> is a list of pictures:
//   [{ "out": "a.png", "box": [x0, y0, z0, x1, y1, z1], "yaw": 30, "pitch": 28, "fov": 36, "w": 1600, "h": 1000 }]
// The box clips the world, so a crop is drawn without what stands round it. yaw is degrees the eye is turned from
// looking south (0 looks south from the north, 90 west from the east, 180 north, 270 east); the eye is placed by
// the size of what stands in the box, far enough that its bounding sphere fits the frame. One process draws every shot, so the sprites
// are read once.
#:project /home/user/pgm-studio/src/PgmStudio.Minecraft/PgmStudio.Minecraft.csproj
#:property PublishAot=false

using System.Text.Json.Nodes;
using PgmStudio.Minecraft.Anvil;
using PgmStudio.Minecraft.Render;

var buildDir = args[0];
using var jar = File.OpenRead(args[1]);
var textures = BlockTextureSet.FromJar(jar);
var shots = JsonNode.Parse(File.ReadAllText(args[2]))!.AsArray();

using var fs = File.OpenRead(Path.Combine(buildDir, "volume.bin"));
using var br = new BinaryReader(fs);
if (new string(br.ReadChars(4)) != "RWV1") throw new Exception("bad volume.bin");
int x0 = br.ReadInt32(), y0 = br.ReadInt32(), z0 = br.ReadInt32();
int sx = br.ReadInt32(), sy = br.ReadInt32(), sz = br.ReadInt32();
var ids = br.ReadBytes(sx * sy * sz * 2);
var data = br.ReadBytes(sx * sy * sz);
var biomes = br.ReadBytes(sx * sz);

foreach (var shot in shots)
{
    var box = shot!["box"]!.AsArray().Select(v => (int)v!).ToArray();
    var world = new VoxelWorld();
    int lx = int.MaxValue, ly = int.MaxValue, lz = int.MaxValue, hx = int.MinValue, hy = int.MinValue, hz = int.MinValue;
    for (var x = Math.Max(box[0], x0); x <= Math.Min(box[3], x0 + sx - 1); x++)
    for (var z = Math.Max(box[2], z0); z <= Math.Min(box[5], z0 + sz - 1); z++)
    {
        for (var y = Math.Max(box[1], y0); y <= Math.Min(box[4], y0 + sy - 1); y++)
        {
            var i = ((x - x0) * sy + (y - y0)) * sz + (z - z0);
            var id = ids[2 * i] | (ids[2 * i + 1] << 8);
            if (id == 0 || id == 36) continue;
            world.SetBlock(x, y, z, id, data[i]);
            lx = Math.Min(lx, x); ly = Math.Min(ly, y); lz = Math.Min(lz, z);
            hx = Math.Max(hx, x); hy = Math.Max(hy, y); hz = Math.Max(hz, z);
        }
    }
    for (var x = Math.Max(box[0], x0); x <= Math.Min(box[3], x0 + sx - 1); x++)
    for (var z = Math.Max(box[2], z0); z <= Math.Min(box[5], z0 + sz - 1); z++)
        world.SetBiome(x, z, biomes[(x - x0) * sz + (z - z0)]);

    if (lx == int.MaxValue) continue;
    box = [lx, ly, lz, hx, hy, hz];                     // framed on what stands in the box, not on its air
    double yawDeg = (double?)shot["yaw"] ?? 30, pitchDeg = (double?)shot["pitch"] ?? 28, fov = (double?)shot["fov"] ?? 36;
    int w = (int?)shot["w"] ?? 1600, h = (int?)shot["h"] ?? 1000;
    double mx = (box[0] + box[3] + 1) / 2.0, my = (box[1] + box[4] + 1) / 2.0, mz = (box[2] + box[5] + 1) / 2.0;
    double bw = box[3] - box[0] + 1, bh = box[4] - box[1] + 1, bd = box[5] - box[2] + 1;
    var radius = 0.5 * Math.Sqrt(bw * bw + bh * bh + bd * bd) * ((double?)shot["breathing"] ?? 1.0);
    var halfAcross = fov * Math.PI / 360;
    var halfDown = Math.Atan(Math.Tan(halfAcross) * h / w);
    var distance = radius / Math.Sin(Math.Min(halfAcross, halfDown));
    double yaw = yawDeg * Math.PI / 180, pitch = pitchDeg * Math.PI / 180;
    var camera = new EyeCamera(mx + Math.Sin(yaw) * Math.Cos(pitch) * distance, my + Math.Sin(pitch) * distance,
                               mz - Math.Cos(yaw) * Math.Cos(pitch) * distance, yawDeg, pitchDeg, fov);
    var picture = EyeScene.Of(world, textures).Draw(camera, w, h);
    var outPath = shot["out"]!.GetValue<string>();
    File.WriteAllBytes(outPath, picture.Png());
    Console.WriteLine($"drew {outPath}");
}
