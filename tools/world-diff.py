"""Two worlds of one board read against each other, keyed by the first world's provenance.

    python3 tools/world-diff.py <original-region> <edited-region>
                                [--provenance specs/<slug>/provenance.json] [--things 60] [--min-thing 6]
                                [--json <out.json>]

The first world is the studio's build of the board and the second is the same board after a person edited
it in game. The read answers, in order: how many columns kept their surface height, which is the number
that decides whether everything else can be read as substitution rather than drift; what each block became
on the unmoved columns, by the provenance pass that laid it and by its depth under the surface; every
thing one world has and the other does not, clustered into 26-connected bodies of `--min-thing` blocks or
more and listed with a bounding box; and four targeted reads that turn out to be asked of every revamp —
the bed under the water, the plants and what they stand on, the biomes, and how much of each material
shows on a face to air.

`--provenance` is the sidecar the driver writes beside a spec; without it every column is one class and the
substitution table loses its pass axis. With `--json` the things and the tables are written out for a
lift or a review to read. The same read with the edited world replaced by a fresh rebuild of the original
is the determinism control: the drift it reports is what a rebuild moves, and the diff against the hand
work is only trustworthy where that drift is not.
"""
import json
import os
import sys
from collections import Counter, defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anvil import World, TREE, WATER, PLANT, name, census  # noqa: E402

PASS = {None: "ground", 0: "ground", 1: "structure", 2: "made", 3: "prop"}
ZONES = ["top", "d1", "d2", "d3", "d4-6", "d7+"]
N26 = [(dx, dy, dz) for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1) if (dx, dy, dz) != (0, 0, 0)]
FACES = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1))


def zone(depth):
    return "top" if depth == 0 else f"d{depth}" if depth <= 3 else "d4-6" if depth <= 6 else "d7+"


def surface(column):
    """The y of the topmost block that is not a tree or a plant, so a crown does not count as ground."""
    for y, block_id, _data in reversed(column):
        if block_id not in TREE:
            return y
    return None


def claims(provenance_path):
    """`{(x, z): (pass, owner)}` from the driver's sidecar."""
    with open(provenance_path) as handle:
        provenance = json.load(handle)
    owners = provenance["owners"]
    claimed = {}
    for run in provenance["runs"]:
        which = PASS[run.get("pass")]
        owner = owners[run["owner"] - 1] if "owner" in run else None
        for x in range(run["MinX"], run["MaxX"] + 1):
            claimed[(x, run["Z"])] = (which, owner)
    return claimed


def components(voxels, min_size):
    seen = set()
    found = []
    for start in voxels:
        if start in seen:
            continue
        queue = deque([start])
        seen.add(start)
        cells = []
        while queue:
            point = queue.popleft()
            cells.append(point)
            x, y, z = point
            for dx, dy, dz in N26:
                neighbour = (x + dx, y + dy, z + dz)
                if neighbour in voxels and neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        if len(cells) >= min_size:
            found.append(cells)
    found.sort(key=len, reverse=True)
    return found


def bbox(cells):
    xs = [p[0] for p in cells]
    ys = [p[1] for p in cells]
    zs = [p[2] for p in cells]
    return [min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)]


def option(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    original = World(sys.argv[1])
    edited = World(sys.argv[2])
    provenance = option("--provenance")
    things_shown = int(option("--things", 60))
    min_thing = int(option("--min-thing", 6))
    json_out = option("--json")
    result = {}

    columns_a, columns_b = original.columns(), edited.columns()
    print(f"original {sys.argv[1]}: {len(columns_a)} columns, bounds {original.bounds()}")
    print(f"edited   {sys.argv[2]}: {len(columns_b)} columns, bounds {edited.bounds()}")

    # ── 1. block census, both worlds ───────────────────────────────────────────────────────────────────
    count_a, count_b = Counter(), Counter()
    for column in columns_a.values():
        for _y, block_id, data in column:
            count_a[(block_id, data)] += 1
    for column in columns_b.values():
        for _y, block_id, data in column:
            count_b[(block_id, data)] += 1
    print(f"\n== blocks: original {sum(count_a.values())}, edited {sum(count_b.values())}; the forty that moved most")
    print("  id:data           original      edited       delta")
    rows = sorted(set(count_a) | set(count_b), key=lambda k: -abs(count_b[k] - count_a[k]))
    for key in rows[:40]:
        print(f"  {name(key):14} {count_a[key]:10} {count_b[key]:10}  {count_b[key] - count_a[key]:+10}")
    result["census"] = {name(k): [count_a[k], count_b[k]] for k in rows[:200]}

    # ── 2. the surface: which columns kept their height ────────────────────────────────────────────────
    height_delta = Counter()
    kept = []
    for xz in set(columns_a) | set(columns_b):
        top_a = surface(columns_a.get(xz, []))
        top_b = surface(columns_b.get(xz, []))
        if top_a is None or top_b is None:
            height_delta["only in " + ("original" if top_b is None else "edited")] += 1
            continue
        height_delta[top_b - top_a] += 1
        if top_a == top_b:
            kept.append(xz)
    total_both = sum(v for k, v in height_delta.items() if isinstance(k, int))
    print(f"\n== surface: {len(kept)} of {total_both} columns keep their exact height"
          f" ({len(kept) * 100 / max(1, total_both):.1f}%); trees and plants ignored")
    print("  delta histogram: " + ", ".join(f"{k}: {v}" for k, v in sorted(height_delta.items(), key=lambda kv: str(kv[0]))))
    result["surface"] = {"kept": len(kept), "columns": total_both,
                         "histogram": {str(k): v for k, v in height_delta.items()}}

    # ── 3. substitution on the unmoved columns, by pass and depth ──────────────────────────────────────
    claimed = claims(provenance) if provenance else {}
    if provenance:
        print(f"\n== provenance: {len(claimed)} claimed columns, {Counter(v[0] for v in claimed.values())}")
    substitution = defaultdict(Counter)
    for xz in kept:
        top = surface(columns_a[xz])
        which = claimed.get(xz, ("unclaimed" if provenance else "all", None))[0]
        blocks_a = {y: (i, d) for y, i, d in columns_a[xz]}
        blocks_b = {y: (i, d) for y, i, d in columns_b[xz]}
        for y in range(top, -1, -1):
            substitution[(which, zone(top - y))][(blocks_a.get(y, (0, 0)), blocks_b.get(y, (0, 0)))] += 1
    print("\n== what each block became on the unmoved columns, by pass and depth under the surface")
    table = {}
    for which in ["ground", "prop", "structure", "made", "unclaimed", "all"]:
        for depth in ZONES:
            counter = substitution.get((which, depth))
            if not counter:
                continue
            total = sum(counter.values())
            changed = sum(v for k, v in counter.items() if k[0] != k[1])
            print(f"\n  {which} / {depth}: {total} blocks, {changed} changed ({changed * 100 // max(total, 1)}%)")
            by_source = defaultdict(Counter)
            for (was, became), count in counter.items():
                by_source[was][became] += count
            rows = []
            for was, became in sorted(by_source.items(), key=lambda kv: -sum(kv[1].values()))[:8]:
                subtotal = sum(became.values())
                print(f"    {name(was):>12} ({subtotal:7}) -> {census(became, 8)}")
                rows.append({"was": name(was), "count": subtotal,
                             "became": {name(b): n for b, n in became.most_common(8)}})
            table[f"{which}/{depth}"] = rows
    result["substitution"] = table

    # ── 4. things: blocks only one world has, clustered ────────────────────────────────────────────────
    voxels_a, voxels_b = original.voxels(), edited.voxels()
    only_b = {p: v for p, v in voxels_b.items() if p not in voxels_a}
    only_a = {p: v for p, v in voxels_a.items() if p not in voxels_b}
    print(f"\n== blocks only the edited world has: {len(only_b)}; only the original has: {len(only_a)}")
    result["things"] = {}
    for label, key, voxels in (("ADDED", "added", only_b), ("REMOVED", "removed", only_a)):
        bodies = components(voxels, min_thing)
        print(f"\n  {label}: {len(bodies)} things of {min_thing}+ blocks; the {min(things_shown, len(bodies))} largest")
        listed = []
        for shown, cells in enumerate(bodies[:200]):
            box = bbox(cells)
            counted = Counter(voxels[p] for p in cells)
            if shown < things_shown:
                print(f"  {len(cells):6}  x{box[0]}..{box[3]} y{box[1]}..{box[4]} z{box[2]}..{box[5]}"
                      f"  [{box[3] - box[0] + 1}x{box[4] - box[1] + 1}x{box[5] - box[2] + 1}]  {census(counted, 6)}")
            listed.append({"blocks": len(cells), "box": box, "census": {name(b): n for b, n in counted.most_common(6)}})
        result["things"][key] = listed

    # ── 5. the bed under the water ─────────────────────────────────────────────────────────────────────
    bed_a, bed_b = Counter(), [Counter(), Counter(), Counter()]
    for (x, z), column in columns_b.items():
        water_ys = [y for y, i, _d in column if i in WATER]
        if not water_ys:
            continue
        floor = min(water_ys)
        for k in range(3):
            bed_b[k][voxels_b.get((x, floor - 1 - k, z), (0, 0))] += 1
        bed_a[voxels_a.get((x, floor - 1, z), (0, 0))] += 1
    if bed_a:
        print(f"\n== the bed under the water ({sum(bed_a.values())} water columns in the edited world)")
        print(f"  original, first block under the water: {census(bed_a)}")
        for k in range(3):
            print(f"  edited, {k + 1} under the water:           {census(bed_b[k])}")

    # ── 6. plants ──────────────────────────────────────────────────────────────────────────────────────
    plants, stands_on = Counter(), Counter()
    for (x, y, z), value in voxels_b.items():
        if value[0] in PLANT:
            plants[value] += 1
            stands_on[voxels_b.get((x, y - 1, z), (0, 0))] += 1
    grass_topped = sum(1 for column in columns_b.values()
                       if column and (column[-1][1] == 2 or (len(column) > 1 and column[-1][1] in PLANT and column[-2][1] == 2)))
    print(f"\n== plants in the edited world: {sum(plants.values())} on {grass_topped} grass-topped columns")
    if plants:
        print(f"  which: {census(plants)}")
        print(f"  standing on: {census(stands_on)}")

    # ── 7. biomes ──────────────────────────────────────────────────────────────────────────────────────
    biome_a, biome_b = Counter(), Counter()
    for (x, z) in columns_b:
        if x % 4 or z % 4:
            continue
        biome_a[original.biome(x, z)] += 1
        biome_b[edited.biome(x, z)] += 1
    print(f"\n== biomes, sampled every four blocks: original {biome_a.most_common(8)}")
    print(f"                                     edited   {biome_b.most_common(12)}")

    # ── 8. exposure: how much of each material shows ───────────────────────────────────────────────────
    totals = Counter(v for v in voxels_b.values() if v[0] not in WATER)
    watched = [block for block, _n in totals.most_common(14)]
    exposed = Counter()
    for (x, y, z), value in voxels_b.items():
        if value not in watched:
            continue
        for dx, dy, dz in FACES:
            if voxels_b.get((x + dx, y + dy, z + dz), (0, 0))[0] in (0, 8, 9):
                exposed[value] += 1
                break
    print("\n== exposure in the edited world: blocks with a face to air or water, of the fourteen commonest materials")
    for block in watched:
        print(f"  {name(block):14} {exposed[block]:8} of {totals[block]:8}  ({exposed[block] * 100 / max(1, totals[block]):.0f}%)")
    result["exposure"] = {name(b): [exposed[b], totals[b]] for b in watched}

    if json_out:
        with open(json_out, "w") as handle:
            json.dump(result, handle, indent=1)
        print(f"\nwrote {json_out}")


if __name__ == "__main__":
    main()
