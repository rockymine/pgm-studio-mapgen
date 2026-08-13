// Compile a plan, then replace its terrain shapes with authored polygons and attach every finish the
// plan cannot state — relief, a theme registry, room shells and dressing — before building the world.
//   dotnet run tools/world-build.cs -- <plan.json> <world.json> <themes.json> <rooms.json> <dressing.json> <name> <outZip>
// rooms.json is {"cage": …, "spawn": …}; any of world/themes/rooms/dressing may be the literal "-" to skip.
using System.Net.Http;
using System.Text;
using System.Text.Json.Nodes;

var api = Environment.GetEnvironmentVariable("PGM_STUDIO_API") ?? "http://localhost:5189/api";
var (planPath, worldPath, themesPath, roomsPath, dressingPath, wanted, outZip) =
    (args[0], args[1], args[2], args[3], args[4], args[5], args[6]);

using var http = new HttpClient { Timeout = TimeSpan.FromMinutes(15) };

static JsonNode? Load(string path) =>
    path == "-" ? null : JsonNode.Parse(File.ReadAllText(path));

var plan = Load(planPath)!;
var world = Load(worldPath);
var themes = Load(themesPath);
var rooms = Load(roomsPath);
var dressing = Load(dressingPath);

async Task<JsonNode> Call(HttpMethod method, string path, JsonNode? body, string what)
{
    using var request = new HttpRequestMessage(method, api + path);
    if (body is not null) request.Content = new StringContent(body.ToJsonString(), Encoding.UTF8, "application/json");
    var response = await http.SendAsync(request);
    var text = await response.Content.ReadAsStringAsync();
    if (!response.IsSuccessStatusCode) throw new Exception($"{what}: HTTP {(int)response.StatusCode} {text}");
    Console.WriteLine($"  {what}: {(int)response.StatusCode}");
    return text.Length == 0 ? new JsonObject() : JsonNode.Parse(text)!;
}

var slug = (await Call(HttpMethod.Post, "/plan", new JsonObject { ["name"] = wanted }, "POST /plan"))
    ["slug"]!.GetValue<string>();
Console.WriteLine($"  slug = {slug}");

await Call(HttpMethod.Put, $"/map/{slug}/plan", plan.DeepClone(), "PUT plan");
var compiled = await Call(HttpMethod.Post, "/plan/compile", plan.DeepClone(), "POST compile");

var layout = compiled["layout"]!.DeepClone()!;
var intent = compiled["intent"]!.DeepClone()!;

// ── Terrain: the authored polygons replace every compiled shape that is not a structural rectangle.
// A role-tagged shape is the plan's own spawn/wool projection and is locked, so it is carried through.
// The plan's compiled shapes carry its elevation tiers, so they are kept rather than replaced. A tier is
// named by the height it stands at, which is how a theme reaches shapes whose ids the compiler minted.
if (world?["themeByHeight"] is JsonObject byHeight)
    foreach (var shape in layout["layout"]!["shapes"]!.AsArray())
        if (shape!["base_height"]?.GetValue<double>() is { } h &&
            byHeight[((int)h).ToString()] is { } themeName)
            shape["theme"] = themeName.DeepClone();

// A compiled tier is the rectangle union its plan pieces fused to. Promoting one to an authored polygon
// moves its anchor points instead of carving them away, which is what makes an edge organic rather than
// nibbled — the inner boundaries it shares with the tiers above and below are kept exactly.
// A tier can fuse to more than one shape. The polygon replaces the first and the tier's other shapes are
// dropped, so the authored outline is the only thing describing that height — leaving them in would keep
// their rectangles showing through wherever the polygon pulled inside them.
if (world?["reshapeByHeight"] is JsonObject reshape)
{
    var done = new HashSet<int>();
    var shapes = layout["layout"]!["shapes"]!.AsArray();
    var island = layout["layout"]!["islands"]!.AsArray().First()!;
    foreach (var shape in shapes.ToList())
    {
        if (shape!["role"] is not null || shape["base_height"]?.GetValue<double>() is not { } h) continue;
        if (reshape[((int)h).ToString()] is not { } vertices) continue;

        if (done.Add((int)h))
        {
            shape["type"] = "polygon";
            shape["vertices"] = vertices.DeepClone();
            Console.WriteLine($"  reshaped tier {(int)h} → {vertices.AsArray().Count} vertices");
            continue;
        }

        var dropped = shape["id"]!.GetValue<string>();
        shapes.Remove(shape);
        var ids = island["shapeIds"]!.AsArray();
        foreach (var id in ids.ToList())
            if (id!.GetValue<string>() == dropped) ids.Remove(id);
        Console.WriteLine($"  dropped {dropped} — tier {(int)h} is the authored polygon now");
    }
}

// Arbitrary shape properties by tier — relief_scope above all, which is how a built thing standing on the
// ground keeps its floor flat while the field rolls around it.
if (world?["shapePropsByHeight"] is JsonObject props)
    foreach (var shape in layout["layout"]!["shapes"]!.AsArray())
        if (shape!["role"] is null && shape["base_height"]?.GetValue<double>() is { } h &&
            props[((int)h).ToString()] is JsonObject fields)
            foreach (var (key, value) in fields)
                shape[key] = value!.DeepClone();

// Authored polygons on top: the voids dropped through, the erected mesa.
if (world?["addShapes"] is JsonArray extra)
{
    var shapes = layout["layout"]!["shapes"]!.AsArray();
    var island = layout["layout"]!["islands"]!.AsArray().First()!;
    foreach (var shape in extra)
    {
        shapes.Add(shape!.DeepClone());
        island["shapeIds"]!.AsArray().Add((JsonNode)JsonValue.Create(shape["id"]!.GetValue<string>()));
    }
    Console.WriteLine($"  shapes: {shapes.Count} ({extra.Count} authored on top of the plan's tiers)");
}

if (world?["relief"] is { } relief) layout["relief"] = relief.DeepClone();

if (themes is JsonObject registry)
{
    layout["themes"] = registry.DeepClone();
    layout["mapTheme"] = registry.First().Key;
    Console.WriteLine($"  themes: {string.Join(", ", registry.Select(t => t.Key))} (default {registry.First().Key})");
}

if (rooms is not null) layout["roomStyles"] = rooms.DeepClone();
if (dressing is not null) layout["dressing"] = dressing.DeepClone();

await Call(HttpMethod.Put, $"/map/{slug}/sketch/from-plan?force=true", layout, "PUT sketch/from-plan");
await Call(HttpMethod.Post, $"/map/{slug}/sketch/finish", null, "POST sketch/finish");
await Call(HttpMethod.Put, $"/map/{slug}/intent/from-plan", intent, "PUT intent/from-plan");

var zip = await http.GetAsync($"{api}/map/{slug}/export");
if (!zip.IsSuccessStatusCode)
    throw new Exception($"export: HTTP {(int)zip.StatusCode} {await zip.Content.ReadAsStringAsync()}");
File.WriteAllBytes(outZip, await zip.Content.ReadAsByteArrayAsync());
Console.WriteLine($"  export → {outZip} ({new FileInfo(outZip).Length / 1024} KB)");
Console.WriteLine($"DONE slug={slug}");
