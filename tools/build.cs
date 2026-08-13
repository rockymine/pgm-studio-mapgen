// Drives a plan all the way to an exported world through the studio's own API, injecting the two things a
// mapgen spec cannot state: a terrain theme whose materials are named as blocks, and a room style of its own.
//   dotnet run tools/clayclay-build.cs -- <plan.json> <theme.json> <wool-room.json> <spawn-room.json> <name> <outZip>
using System.Net.Http;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

var api = Environment.GetEnvironmentVariable("PGM_STUDIO_API") ?? "http://localhost:5189/api";
var planPath = args[0];
var themePath = args[1];
var roomPath = args[2];
var spawnRoomPath = args[3];
var dressingPath = args[4];
var wanted = args[5];
var outZip = args[6];

using var http = new HttpClient { Timeout = TimeSpan.FromMinutes(10) };

var plan = JsonNode.Parse(File.ReadAllText(planPath))!;
var theme = JsonNode.Parse(File.ReadAllText(themePath))!;
var room = JsonNode.Parse(File.ReadAllText(roomPath))!;
var spawnRoom = JsonNode.Parse(File.ReadAllText(spawnRoomPath))!;
var dressing = JsonNode.Parse(File.ReadAllText(dressingPath))!;

static StringContent Body(JsonNode node) =>
    new(node.ToJsonString(), Encoding.UTF8, "application/json");

async Task<JsonNode> Call(HttpMethod method, string path, JsonNode? body, string what)
{
    using var request = new HttpRequestMessage(method, api + path);
    if (body is not null) request.Content = Body(body);
    var response = await http.SendAsync(request);
    var text = await response.Content.ReadAsStringAsync();
    if (!response.IsSuccessStatusCode)
        throw new Exception($"{what}: HTTP {(int)response.StatusCode} {text}");
    Console.WriteLine($"  {what}: {(int)response.StatusCode}");
    return text.Length == 0 ? new JsonObject() : JsonNode.Parse(text)!;
}

// 1. originate the map row
var created = await Call(HttpMethod.Post, "/plan",
    new JsonObject { ["name"] = wanted }, "POST /plan");
var slug = created["slug"]!.GetValue<string>();
Console.WriteLine($"  slug = {slug}");

// 2. store the document, then compile it
await Call(HttpMethod.Put, $"/map/{slug}/plan", plan.DeepClone(), $"PUT /map/{slug}/plan");
var compiled = await Call(HttpMethod.Post, "/plan/compile", plan.DeepClone(), "POST /plan/compile");

var warnings = compiled["warnings"] is JsonArray warn ? warn : null;
if (warnings is { Count: > 0 })
    foreach (var w in warnings) Console.WriteLine($"  warning: {w}");

var layout = compiled["layout"]!.DeepClone()!;
var intent = compiled["intent"]!.DeepClone()!;

// 3. the finish a plan cannot carry: a named theme registry + the map default, and the two room shells
layout["themes"] = new JsonObject { ["clay"] = theme.DeepClone() };
layout["mapTheme"] = "clay";
layout["roomStyles"] = new JsonObject
{
    ["cage"] = room.DeepClone(),
    ["spawn"] = spawnRoom.DeepClone(),
};
layout["dressing"] = dressing.DeepClone();

// 4. terrain, then the world, then the gameplay
await Call(HttpMethod.Put, $"/map/{slug}/sketch/from-plan?force=true", layout, "PUT sketch/from-plan");
await Call(HttpMethod.Post, $"/map/{slug}/sketch/finish", null, "POST sketch/finish");
await Call(HttpMethod.Put, $"/map/{slug}/intent/from-plan", intent, "PUT intent/from-plan");

// 5. the world itself
var zip = await http.GetAsync($"{api}/map/{slug}/export");
if (!zip.IsSuccessStatusCode)
    throw new Exception($"export: HTTP {(int)zip.StatusCode} {await zip.Content.ReadAsStringAsync()}");
File.WriteAllBytes(outZip, await zip.Content.ReadAsByteArrayAsync());
Console.WriteLine($"  export → {outZip} ({new FileInfo(outZip).Length / 1024} KB)");
Console.WriteLine($"DONE slug={slug}");
