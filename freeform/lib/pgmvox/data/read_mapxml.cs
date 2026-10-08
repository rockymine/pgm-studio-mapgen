// Read a map.xml with the studio's own parser and say what it found: every objective by kind, the regions, and
// the validity check the studio runs before an export. pgmvox.objectives writes map.xml; this is how a board
// knows the studio reads the same map from it.
//
//   dotnet run read_mapxml.cs -- <map.xml> [<map.xml> ...]
#:project /home/user/pgm-studio/src/PgmStudio.Pgm/PgmStudio.Pgm.csproj
#:property PublishAot=false

using System.Collections;
using System.Text.Json;
using PgmStudio.Pgm;

var failed = false;
foreach (var path in args)
{
    try
    {
        var map = MapParser.Parse(path);
        var doc = Serializer.ToDict(map);
        var counts = new SortedDictionary<string, int>();
        foreach (var (key, value) in doc)
            if (value is IList list && list.Count > 0) counts[key] = list.Count;
        var validity = MapValidity.Check(doc);
        Console.WriteLine(JsonSerializer.Serialize(new
        {
            path, valid = validity.Valid, counts,
            issues = validity.Issues.Select(i => $"{i.Severity}: {i.Message}"),
        }));
        failed |= !validity.Valid;
    }
    catch (Exception e)
    {
        Console.WriteLine(JsonSerializer.Serialize(new { path, valid = false, error = $"{e.GetType().Name}: {e.Message}" }));
        failed = true;
    }
}
return failed ? 1 : 0;
