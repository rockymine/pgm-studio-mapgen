"""The map's half as layers for the 3D viewer: every block with its layer, and every wool sheet that lofts within a
block as its low-poly mesh, its lines and their points."""
import os, sys, pickle, json, math, collections
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, sys.argv[1])
import loft
from lines import fit_lofts, components, near
from reconstruct import from_frame

half = pickle.load(open(sys.argv[1] + "/half.pkl", "rb"))
OUT = sys.argv[2]
STEP = 2.0

WOOL = {0: ("Weiß", "#e4e8e8", "Lane zur Wolle", "Untergrund"), 1: ("Orange", "#e8761c", "Wände des Untergrunds an der Lane", "Untergrund"),
        2: ("Magenta", "#b84db0", "offenes Gestein: Übergang von der Oberfläche in den Untergrund, auch das Loch am Eingang der Wool-Lane", "Untergrund"), 3: ("Hellblau", "#4aaed6", "Berge", "Gelände"),
        4: ("Gelb", "#efc12f", "flacheres Gelände", "Gelände"), 6: ("Rosa", "#e892ad", "Kante zwischen Decke und Wand im Untergrund, für Tiefe", "Untergrund"),
        7: ("Dunkelgrau", "#4a5053", "Teil des Bauwerks", "Bauwerke"), 8: ("Hellgrau", "#9a9a92", "Boden", "Gelände"),
        9: ("Türkis", "#1f8d96", "", "Sonstige Wolle"), 10: ("Violett", "#7b35ab", "Rampe unter dem Core", "Untergrund"),
        11: ("Blau", "#3a3f9e", "", "Sonstige Wolle"), 12: ("Braun", "#77502f", "", "Sonstige Wolle"),
        14: ("Rot", "#a8302b", "Decke, komplett unterirdisch", "Untergrund"), 15: ("Schwarz", "#25272b", "Dach eines Gebäudeteils", "Bauwerke")}
STRUCTURE_WOOL = {7, 14, 15}          # parts of a building: drawn as its faces, never lofted
SKIP = {0, 6, 8, 9, 10, 11, 27, 28, 30, 31, 32, 37, 38, 39, 40, 50, 51, 55, 59, 63, 64, 65, 66, 68, 69, 70, 71, 72, 75, 76, 77, 78,
        83, 93, 94, 96, 104, 105, 106, 111, 115, 131, 132, 141, 142, 143, 147, 148, 149, 150, 157, 167, 171, 175, 176, 177, 193,
        194, 195, 196, 197}
MARK = {41: "#f2d03a", 57: "#5fe0d5", 133: "#2fd36a", 42: "#d8d8d8"}
STONE = {(1, 0): "#7f7f7f", (1, 1): "#9a6c58", (1, 2): "#a77562", (1, 3): "#bdbdbd", (1, 4): "#c3c3c3", (1, 5): "#858585",
         (1, 6): "#8c8c8c", 4: "#6e6e6e", 98: "#7a7a7a", 139: "#707070", 109: "#7a7a7a", 44: "#8a8a8a", 43: "#9e9e9e",
         45: "#96604c", 108: "#96604c", 112: "#3a1d22", 113: "#3a1d22", 114: "#3a1d22", 101: "#8d8d8d", 85: "#8f7448", 5: "#9c7f4e",
         17: "#6b5433", 67: "#6e6e6e", 48: "#5f6e5f", 24: "#d8cf9b", 128: "#d8cf9b", 155: "#ece9e2", 156: "#ece9e2", 168: "#5fa596",
         89: "#e8c47a", 123: "#9a6e44", 124: "#e8c47a", 2: "#6c9a3c", 3: "#86603f", 12: "#dbd3a0", 13: "#857f7e", 80: "#f0fbfb"}

layers, palette, pal_index, blocks = [], [], {}, []

def layer(key, name, note, colour, group):
    for k, l in enumerate(layers):
        if l["key"] == key: return k
    layers.append({"key": key, "name": name, "note": note, "colour": colour, "group": group, "blocks": 0, "meshes": []})
    return len(layers) - 1

def classify(b, c=None):
    i, d = b
    if i == 35:
        if d in (5, 13):
            return layer("wool-stütz", "Hellgrün und Grün", "Stützwände", "#76b52a", "Gelände"), "#76b52a" if d == 5 else "#58702a"
        if d == 8 and c not in lofted:
            return layer("ceiling", "Hellgrau und Ton", "Decke im großen Raum, Schachbrett-Dach des Bunkers", "#a3a8b4", "Bauwerke"), "#9a9a92"
        name, colour, note, group = WOOL[d]
        return layer(f"wool-{d}", name, note, colour, group), colour
    if i in MARK: return layer("marks", "Markierungen", "Gold, Diamant, Smaragd, Eisen", "#f2d03a", "Hilfen"), MARK[i]
    if i == 7: return layer("bedrock", "Grundgestein", "", "#3b3b3e", "Bauwerke"), "#3b3b3e"
    if i in (49, 10, 11): return layer("core", "Obsidian und Lava", "Kern", "#2a2238", "Bauwerke"), "#d9661a" if i in (10, 11) else "#221c30"
    if i in (20, 95, 102, 160): return layer("glass", "Glas", "", "#b9d6e2", "Bauwerke"), "#b9d6e2"
    if i == 82: return layer("ceiling", "Hellgrau und Ton", "Decke im großen Raum, Schachbrett-Dach des Bunkers", "#a3a8b4", "Bauwerke"), "#a3a8b4"
    if i in (159, 172): return layer("clay", "Türkiser Ton", "dunkelgraue Akzentfarbe, u. a. an den Treppenwänden", "#5d6d72", "Bauwerke"), {172: "#98604a"}.get(i, "#5d6d72")
    colour = STONE.get((i, d), STONE.get(i, "#8a8a8a"))
    return layer("stone", "Stein", "Bunker, Gänge, Fassade", "#7f7f7f", "Bauwerke"), colour

lofted = set()

def mesh_of(f):
    fr, lofts, (lo, hi) = f["frame"], f["lofts"], f["window"]
    mid = hi + 0.5                    # the sheet's upper face, so lofts meet blocks at their top
    world = lambda a, b, w: from_frame(*lofts.to_uvw(a, b, w + mid), fr)
    pairs, rows = lofts.strips()
    tris = []
    for l0, r0, l1, r1 in pairs:
        rungs = lofts.rungs(l0, r0, l1, r1)
        span = max(abs(r0[1] - r0[0]), abs(r1[1] - r1[0]))
        n = max(2, math.ceil(span / STEP) + 1)
        pick = [rungs[round(k * (len(rungs) - 1) / (n - 1))] for k in range(n)]
        for (p0, q0), (p1, q1) in zip(pick, pick[1:]):
            P0, Q0, P1, Q1 = world(*p0), world(*q0), world(*p1), world(*q1)
            tris += [P0, Q0, P1, Q0, Q1, P1]
    lines, points = [], []
    for b, ls in rows:
        for line in ls:
            curve = loft.curve(line, step=1.0) if len(line) > 1 else line
            lines.append([world(*p) for p in curve])
            points += [world(*p) for p in line]
    return tris, lines, points

q = lambda p: [round(v * 10) for v in p]
stats = collections.defaultdict(lambda: {"lines": 0, "points": 0, "free": 0, "pieces": 0, "boxed": 0})
GROUPS = ["Gelände", "Untergrund", "Bauwerke", "Sonstige Wolle", "Hilfen"]
for d in range(16):
    cells = [c for c, b in half.items() if b == (35, d)]
    if not cells or d in STRUCTURE_WOOL: continue
    k = classify((35, d), "lofted-probe")[0] if d != 8 else layer("wool-8", WOOL[8][0], WOOL[8][2], WOOL[8][1], "Gelände")
    marks = [c for c, b in half.items() if b[0] in MARK]
    markset = set(marks)
    for comp in components(cells, 1):
        if len(comp) < 60: continue
        cs = set(comp)
        own = [m for m in marks if near(m, cs)]
        main = fit_lofts(cs, own, pairing="arc")
        parts = [main] + [fit_lofts(set(e), [m for m in own if near(m, set(e))], pairing="arc") for e in components(main["extra"])]
        built = set()
        for f in parts: built |= f["lofts"].build(f["frame"], f["window"])
        recall = sum(near(c, built) for c in cs) / len(cs); precision = sum(near(c, cs) for c in built) / max(1, len(built))
        if recall < 0.95 or precision < 0.97:
            stats[k]["boxed"] += len(comp); print(f"wool {d}: {len(comp)} blocks stay blocks ({recall:.0%} / {precision:.0%})"); continue
        lofted |= cs
        for f in parts:
            tris, lines, points = mesh_of(f)
            layers[k]["meshes"].append({"tris": [v for p in tris for v in q(p)], "lines": [[v for p in l for v in q(p)] for l in lines],
                                        "points": [v for p in points for v in q(p)]})
        s = stats[k]; s["pieces"] += 1; s["free"] += len(parts) - 1
        s["lines"] += sum(f["lines"] for f in parts); s["points"] += sum(f["points"] for f in parts)
        print(f"wool {d}: {len(comp)} blocks -> {sum(f['lines'] for f in parts)} lines, {len(tris)//3} triangles ({recall:.1%} / {precision:.1%})")

for c, b in half.items():
    if b[0] in SKIP: continue
    k, colour = classify(b, c)
    layers[k]["blocks"] += 1
    if (k, colour) not in pal_index: pal_index[(k, colour)] = len(palette); palette.append([k, colour])
    blocks += [c[0], c[1], c[2], pal_index[(k, colour)] * 2 + (c in lofted)]
for k, l in enumerate(layers):
    l.update(stats.get(k, {}))
order = GROUPS
data = {"pivot": [119, 173], "layers": layers, "palette": palette, "blocks": blocks, "order": order}
json.dump(data, open(OUT, "w"), separators=(",", ":"))
tri = sum(len(m["tris"]) // 9 for l in layers for m in l["meshes"])
print("layers", [(l["name"], l["blocks"], len(l["meshes"])) for l in layers], "triangles", tri, "blocks", len(blocks) // 4)
