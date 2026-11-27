"""Rebuild the Eismulde's built-half side from a few long lines running along the gap, and measure the fit."""
import sys, json, math, collections
S = sys.argv[1]
sys.path.insert(0, S + "/variants"); import kit, loft
v = json.load(open(S + "/variants/mid-7/variant.json")); kit.set_shift(*v["shift"])
blocks = {(v["blocks"][i], v["blocks"][i + 1], v["blocks"][i + 2]) for i in range(0, len(v["blocks"]), 4)}
top = kit.tops(blocks)
half = {c: y for c, y in top.items() if kit.across(*c) < 0}          # loft A's columns
old_top = kit.tops(kit.existing())
def height(x, z):
    """The Eismulde's surface at (x, z), from its own columns; at the edge, the author's ground."""
    key = (round(x), round(z))
    if key in top: return top[key]
    near = [top[(key[0] + a, key[1] + b)] for a in (-1, 0, 1) for b in (-1, 0, 1) if (key[0] + a, key[1] + b) in top]
    if near: return sum(near) / len(near)
    near = [old_top[(key[0] + a, key[1] + b)] for a in range(-2, 3) for b in range(-2, 3) if (key[0] + a, key[1] + b) in old_top]
    return sum(near) / len(near) if near else None
# the gap's built-half edge as a function of along: the furthest-out loft-A column at each station
edge = {}
for (x, z) in half:
    s = round(kit.along(x, z)); a = kit.across(x, z)
    if s not in edge or a < edge[s]: edge[s] = a
S0, S1 = min(edge), max(edge)
def point(s, frac):
    a = edge.get(round(s)) if round(s) in edge else min(edge.values(), key=lambda e: 0)
    a = a * (1 - frac)                                      # frac 0 = the edge, 1 = the cut line
    x = kit.PIVOT[0] + s * kit.CUT[0] + a * kit.NORMAL[0]; z = kit.PIVOT[1] + s * kit.CUT[1] + a * kit.NORMAL[1]
    return (x, z)
def simplify(samples, tol):
    """Fewest points whose spline stays within `tol` of the samples' heights."""
    keep = [0, len(samples) - 1]
    while True:
        pts = [samples[k] for k in sorted(keep)]
        curve = loft.curve(pts, step=0.5) if len(pts) > 1 else pts
        worst, idx = 0, None
        for k, p in enumerate(samples):
            q = min(curve, key=lambda c: (c[0] - p[0]) ** 2 + (c[2] - p[2]) ** 2)
            d = abs(q[1] - p[1])
            if d > worst and k not in keep: worst, idx = d, k
        if worst <= tol or idx is None: return [samples[k] for k in sorted(keep)]
        keep.append(idx)
def build(fracs, tol, spacing=2):
    lines = []
    for f in fracs:
        samples = []
        for s in range(S0, S1 + 1, spacing):
            x, z = point(s, f); y = height(x, z)
            if y is not None: samples.append((x, y, z))
        lines.append(simplify(samples, tol))
    return lines
def score(lines):
    b = kit.loft_blocks(lines, thickness=1)
    t = kit.tops(b)
    diffs = [abs(t[c] - y) for c, y in half.items() if c in t]
    missing = sum(1 for c in half if c not in t)
    return sum(d <= 1 for d in diffs) / len(half), max(diffs), missing
for fracs in ((0, .35, .7, 1), (0, .25, .5, .75, 1), (0, .2, .4, .6, .8, 1)):
    for tol in (0.75, 1.0):
        lines = build(fracs, tol)
        within, worst, missing = score(lines)
        print(f"{len(fracs)} lines, tolerance {tol}: points {sum(map(len, lines))} per line {[len(l) for l in lines]} | within 1 block {within:.0%}, worst {worst}, columns missed {missing} of {len(half)}")

if len(sys.argv) > 2 and sys.argv[2] == "final":
    fr = (0, 0.3, 0.6, 1)
    lines = build(fr, 1.0)
    within, worst, missing = score(lines)
    print("final", [len(l) for l in lines], "points", sum(map(len, lines)), f"within 1: {within:.0%}, worst {worst}, missed {missing}")
    slope, floor = lines[:3], lines[2:]
    rnd = lambda p: (math.floor(p[0] + .5), math.floor(p[1] + .5), math.floor(p[2] + .5))
    out = ["Die Eismulde, schlank: wenige lange Linien laengs der Luecke", "",
           "Nur Loft A (deine Seite bis zur Mittellinie). Jede Linie: erster Punkt Linksklick, die weiteren Rechtsklicks,",
           "in der angegebenen Reihenfolge; die Linien eines Lofts in der angegebenen Reihenfolge. y ist der oberste Block.",
           "Die Linie 'Muldenrand' ist die letzte des Hangs und die erste des Bodens: beide Lofts teilen sie.",
           f"Zweite Haelfte um 4 in x und 10 in z verschoben, Drehung um ({kit.PIVOT[0]} | {kit.PIVOT[1]}): (x, z) -> (123 - x, 183 - z).", ""]
    names = ["Rand (an deinem Boden)", "Hangmitte", "Muldenrand", "Mittellinie"]
    out.append("== Muldenhang (gelb): 3 Linien")
    for k, l in enumerate(slope): out.append(f"  {names[k]:24s}: " + "  ".join("%d %d %d" % rnd(p) for p in l))
    out += ["", "== Muldenboden (hellgrau): 2 Linien"]
    for k, l in enumerate(floor): out.append(f"  {names[k + 2]:24s}: " + "  ".join("%d %d %d" % rnd(p) for p in l))
    open(S + "/simplify/eismulde-schlank.txt", "w").write("\n".join(out) + "\n")
    json.dump({"slope": [[rnd(p) for p in l] for l in slope], "floor": [[rnd(p) for p in l] for l in floor]}, open(S + "/simplify/lean.json", "w"))
    print("\n".join(out[7:]))
