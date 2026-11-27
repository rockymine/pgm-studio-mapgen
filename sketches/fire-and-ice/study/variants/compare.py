"""The author's terrain and every variant measured the same way: how dense the points are, how hilly the surface is,
how many layers it combines and how far it reaches. Prints a table and writes compare.json beside the viewer."""
import glob
import json
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.dirname(HERE)
STRUCTURE = (-15, 52, -22, 31)        # x0, x1, z0, z1 of the main building's stone tops


def measure(layers, name):
    """One row of readings over a list of viewer layers (each with meshes of tris, lines, points)."""
    columns, area, tilt, heights = set(), 0.0, [], []
    lines = points = lofts = 0
    colours = set()
    for layer in layers:
        if not layer["meshes"]: continue
        colours.add(layer["colour"])
        for m in layer["meshes"]:
            lofts += 1; lines += len(m["lines"]); points += len(m["points"]) // 3
            t = m["tris"]
            for i in range(0, len(t), 9):
                a, b, c = [(t[i + 3 * k] / 10, t[i + 3 * k + 1] / 10, t[i + 3 * k + 2] / 10) for k in range(3)]
                u = [b[j] - a[j] for j in range(3)]; v = [c[j] - a[j] for j in range(3)]
                n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
                size = math.sqrt(sum(x * x for x in n)) / 2
                if size < 1e-6: continue
                angle = math.degrees(math.acos(min(1, abs(n[1]) / (2 * size))))
                area += size; tilt.append((angle, size))
                for p in (a, b, c):
                    columns.add((round(p[0]), round(p[2]))); heights.append(p[1])
    if not tilt: return None
    tilt.sort()
    total = sum(s for _, s in tilt)
    def share(limit): return sum(s for a, s in tilt if a > limit) / total
    acc, median = 0, 0
    for a, s in tilt:
        acc += s
        if acc >= total / 2: median = a; break
    x0, x1, z0, z1 = STRUCTURE
    beyond = sum(1 for x, z in columns if not (x0 <= x <= x1 and z0 <= z <= z1)) / max(1, len(columns))
    return {"name": name, "lofts": lofts, "lines": lines, "points": points, "area": round(area),
            "points_per_100": round(100 * points / area, 1), "lines_per_100": round(100 * lines / area, 2),
            "tilt_median": round(median), "over_30": round(100 * share(30)), "over_45": round(100 * share(45)),
            "height": [round(min(heights)), round(max(heights))], "colours": len(colours), "beyond_building": round(100 * beyond)}


def main():
    rows = []
    m = json.load(open(os.path.join(SCRATCH, "viewer", "map.json")))
    rows.append(dict(measure([l for l in m["layers"] if l["group"] == "Gelände"], "Autor: Gelände"), id="author"))
    for l in m["layers"]:
        if l["group"] == "Gelände": rows.append(dict(measure([l], f"Autor: {l['name']}"), id="author/" + l["key"]))
    checker = {(x, z) for (x, y, z), (n, g) in __import__("kit").existing().items() if n == "Hellgrau und Ton" and y == 59}
    for path in sorted(glob.glob(os.path.join(HERE, "*", "variant.json"))):
        v = json.load(open(path))
        row = measure(v["layers"], f"{v['id']}: {v['title']}")
        if not row: continue
        row["slot"] = v["slot"]; row["id"] = v["id"]
        if v["slot"] == "cover":
            covered = {(v["blocks"][i], v["blocks"][i + 2]) for i in range(0, len(v["blocks"]), 4) if v["blocks"][i + 1] > 59}
            row["checker_covered"] = round(100 * len(checker & covered) / len(checker))
        rows.append(row)
    cols = ["name", "lofts", "lines", "points", "area", "points_per_100", "lines_per_100", "tilt_median", "over_30", "over_45", "height", "colours", "beyond_building", "checker_covered"]
    print(" | ".join(cols))
    for r in rows: print(" | ".join(str(r.get(c, "")) for c in cols))
    json.dump(rows, open(os.path.join(SCRATCH, "viewer", "compare.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
