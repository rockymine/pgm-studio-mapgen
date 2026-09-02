"""The fast loop: a spec through the previews, in seconds, without a drive.

    python3 tools/loop.py specs/<slug> [--slug <slug>] [--no-relief] [--no-dressing]
                          [--candidates <propId> x,z [x,z ...]]
                          [--profile x=<x>[,z=<z0>..<z1>[,<step>]]] [--profile z=<z>[,x=<x0>..<x1>[,<step>]]]
                          [--column x,z [x,z ...]]

A drive is ten minutes; a placement question is answered by two previews that take twenty seconds. This
reads the spec the way `drive.py` does — a plan compiled and patched with its finish, or a drawn layout —
and posts the result to `sketch/relief/read` (the terrain in numbers: range, steps, barriers, crossings)
and `sketch/dressing` (what every prop did, and every decline with its rule and coordinates). Nothing is
stored. The map has to have been driven once before, because the dressing preview reads the stored intent
for the spawn doors and the goal rings `DR-KEEP` keeps clear.

`--candidates` is the placement oracle the API does not have: the named prop is duplicated at every
position given, as `cand-1`, `cand-2`, …, and one dressing pass says which of them stand and which are
declined and why. Eight candidates cost one pass. `--profile` and `--column` post `sketch/columns`, which
builds the board and is the one heavy read here, and print the ground's surface along a line or the whole
column at a position, which is how a scarp's side or a bench's edge is checked without a world.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import drive  # noqa: E402


def option(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def values_after(flag):
    """Every `x,z` pair following a flag, up to the next flag."""
    if flag not in sys.argv:
        return []
    out = []
    for token in sys.argv[sys.argv.index(flag) + 1:]:
        if token.startswith("--"):
            break
        out.append(token)
    return out


def load(specdir):
    base = os.path.basename(specdir.rstrip("/"))
    with open(f"{specdir}/{base}.plan.json") as handle:
        plan = json.load(handle)
    finish_path = f"{specdir}/{base}.finish.json"
    if os.path.exists(finish_path):
        with open(finish_path) as handle:
            finish = json.load(handle)
        _, compiled = drive.call("POST", "/plan/compile", plan)
        return drive.patch_layout(compiled["layout"], finish), base
    with open(f"{specdir}/{base}.layout.json") as handle:
        return json.load(handle), base


def decode_columns(payload):
    """`{(x, z): (ground top y, top y, runs)}` off the flat stride `sketch/columns` answers."""
    cols = payload["cols"]
    layers = payload.get("layers") or []
    decoded = {}
    i = 0
    while i < len(cols):
        x, z, count = cols[i], cols[i + 1], cols[i + 2]
        i += 3
        ground = top = None
        runs = []
        for _ in range(count):
            y_top, y_bottom, palette, layer = cols[i:i + 4]
            i += 4
            runs.append((y_top, y_bottom, palette, layer))
            top = y_top if top is None else max(top, y_top)
            if layer == 0 or (not layers and layer == -1):
                ground = y_top if ground is None else max(ground, y_top)
        decoded[(x, z)] = (ground, top, runs)
    return decoded


def profile(decoded, spec):
    fields = dict(part.split("=") for part in spec.split(","))
    step = int(fields.get("step", 3))
    if "x" in fields and ".." not in fields["x"]:
        x = int(fields["x"])
        lo, _, hi = fields.get("z", "-60..60").partition("..")
        line = [(x, z) for z in range(int(lo), int(hi) + 1, step)]
        print(f"  x={x}: " + " ".join(f"{z}:{decoded.get((x, z), (None,))[0]}" for x, z in line))
    else:
        z = int(fields["z"])
        lo, _, hi = fields.get("x", "-60..60").partition("..")
        line = [(x, z) for x in range(int(lo), int(hi) + 1, step)]
        print(f"  z={z}: " + " ".join(f"{x}:{decoded.get((x, z), (None,))[0]}" for x, z in line))


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    specdir = sys.argv[1]
    layout, base = load(specdir)
    slug = option("--slug", base)

    if "--no-relief" not in sys.argv:
        print("== relief")
        _, read = drive.call("POST", f"/map/{slug}/sketch/relief/read", layout, fatal=False)
        for group in read.get("groups") or []:
            print("   " + json.dumps({k: group.get(k) for k in ("group", "cells", "low", "high", "relief", "steps", "cliffs", "acrossX", "acrossZ")}))

    candidates = values_after("--candidates")
    if candidates:
        prop_id, positions = candidates[0], candidates[1:]
        props = layout.setdefault("dressing", {}).setdefault("props", [])
        original = next((p for p in props if p["id"] == prop_id), None)
        if original is None:
            raise SystemExit(f"--candidates: no prop '{prop_id}' in the dressing")
        props[:] = [p for p in props if p["id"] != prop_id]
        for n, position in enumerate(positions, 1):
            x, z = (int(v) for v in position.split(","))
            candidate = dict(original)
            candidate.update({"id": f"cand-{n}", "x": x, "z": z})
            props.append(candidate)
        print(f"== candidates for '{prop_id}': {len(positions)} positions in one pass")

    if "--no-dressing" not in sys.argv or candidates:
        print("== dressing")
        _, dressed = drive.call("POST", f"/map/{slug}/sketch/dressing", layout, fatal=False)
        declined = dressed.get("declines") or []
        for decline in declined:
            print(f"   decline {decline.get('rule')}  {decline.get('message', '')[:200]}")
        placed = {p.get("id") for p in dressed.get("props") or []}
        print(f"   placed {len(placed)}, declined {len(declined)}")
        if candidates:
            standing = [pos for n, pos in enumerate(candidates[1:], 1) if f"cand-{n}" in placed]
            print(f"   '{candidates[0]}' stands at: {', '.join(standing) or 'none of them'}")

    profiles = [sys.argv[i + 1] for i, token in enumerate(sys.argv) if token == "--profile"]
    columns = values_after("--column")
    if profiles or columns:
        print("== columns (builds the board)")
        _, payload = drive.call("POST", f"/map/{slug}/sketch/columns", layout, fatal=False)
        decoded = decode_columns(payload)
        for spec in profiles:
            profile(decoded, spec)
        for position in columns:
            x, z = (int(v) for v in position.split(","))
            ground, top, runs = decoded.get((x, z), (None, None, []))
            print(f"  column ({x},{z}): ground {ground}, top {top}; runs top..bottom (y_top, y_bottom, layer): "
                  + " ".join(f"({a},{b},{layer})" for a, b, _p, layer in sorted(runs, reverse=True)))


if __name__ == "__main__":
    main()
