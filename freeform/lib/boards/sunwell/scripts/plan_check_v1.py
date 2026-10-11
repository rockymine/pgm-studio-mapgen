"""Check Sunwell's plan before anything is built: what every drop asks of a player, and what a lap costs.

1. THE FALL. Minecraft's per-tick fall for a body that steps, runs or sprint-jumps off an edge: how far out each
   carries a player over a drop of twenty-two, and how long the fall takes. A player can always land shorter than
   their way's reach by letting go of the keys, so a target's near side decides the gentlest way that hits it.
2. THE DROPS. For every drop, each target: how far it lies from the edge, which way of leaving reaches it, and
   what happens on a miss. The falls' and the bucket's cost. A shaft: whether a sprint jump carries a player into
   its hole, and whether the pool two shelves down catches them.
3. THE LAP. Seconds from the top shelf to the lake by four habits: the falls every time, the nearest pool every
   time, the bucket every time, and the bucket with every shaft taken.
4. THE GEOMETRY. Every pool, hole and basin on its shelf, inside the shaft, beyond the edge above, and not on top
   of another.

    python3 plan_check.py
"""
import plan_v1 as P

DY = P.DROP
HALF = 0.3                                                       # a player's half-width


def reach():
    return {how: P.fall(DY, how) for how in P.LEAVES}


def gentlest(s0, R):
    for how in ("step off", "run off", "sprint jump"):
        if R[how][1] + HALF >= s0:
            return how
    return None


def walk_back(s):
    """From a landing s beyond shelf k's edge, back under it to shelf k + 1's edge."""
    return (s + 2 * P.EDGE) / P.SPEED


def laps(habit, R):
    """The quickest lap for a habit, choosing at each drop among the gaps the habit allows: walking from where the
    last drop landed, across the shelf and out to the gap's edge, then the fall and what it costs to land."""
    best = {(0, (0.0, None)): 0.0}                                # (drop, (landing x, landing s)) -> seconds
    n = len(P.DROPS)
    for k in range(n):
        for (kk, (xl, sl)), t0 in [item for item in best.items() if item[0][0] == k]:
            for kind, gx0, gx1, s0 in P.gaps(k):
                if habit == "the falls" and kind not in ("falls", "the lake"):
                    continue
                if habit == "the pools" and kind not in ("pool", "the lake"):
                    continue
                if habit == "the bucket" and kind == "shaft":
                    continue
                xg = min(max(xl, gx0), gx1)
                forward = 4.0 if sl is None else sl + 2 * P.EDGE
                walk = (abs(xl - xg) + forward) / P.SPEED
                if kind == "falls":
                    t, land, step = 1.0 + DY / P.FALLS_SPEED, (xg, 2.5), 1
                elif kind == "shaft":
                    t, land, step = P.fall(3 * DY, "sprint jump")[0] / 20 + 0.8, (xg, s0 + 1), 3
                elif kind == "the lake":
                    t, land, step = P.fall(DY, "step off")[0] / 20, (xg, 1.0), 1
                elif habit == "the pools":
                    how = gentlest(s0, R)
                    if how is None:
                        continue
                    t, land, step = R[how][0] / 20 + 0.8, (xg, s0 + 1), 1
                else:                                             # the bucket, at the gap's foot
                    t, land, step = R["step off"][0] / 20 + 0.3, (xg, R["step off"][1]), 1
                key = (min(k + step, n), land)
                v = t0 + walk + t
                if v < best.get(key, 1e9):
                    best[key] = v
    return min(v for (k, land), v in best.items() if k == n)


def check():
    out = []
    R = reach()
    out.append("the fall of 22: " + "; ".join(f"{how}: {R[how][1]:.1f} out, {R[how][0] / 20:.2f} s" for how in P.LEAVES)
               + f"; unbroken it does {P.damage(DY)} of {P.HEALTH} health")
    for k, d in enumerate(P.DROPS):
        parts = []
        if d.get("lake"):
            out.append(f"drop {k + 1}, {P.shelf_y(k)} to {P.LAKE_Y}: the lake, anywhere")
            continue
        for name, x0, x1, s0, s1 in P.pools(k):
            how = gentlest(s0, R)
            parts.append(f"{name} {x1 - x0 + 1}x{s1 - s0 + 1} at {s0}-{s1}: {how or 'OUT OF REACH'}")
        if d.get("falls") is not None:
            parts.append(f"the falls at x {d['falls']}: {DY / P.FALLS_SPEED:.1f} s down")
        if "shaft" in d:
            x0, x1, s0, s1 = d["shaft"]
            how = gentlest(s0, R)
            t66, r66 = P.fall(3 * DY, "sprint jump")
            p0, p1 = s0 - P.SHAFT_POOL_MARGIN, s1 + P.SHAFT_POOL_MARGIN
            under = "the lake" if k + 2 >= len(P.DROPS) - 1 else f"a pool at {p0}-{p1}"
            parts.append(f"the shaft {x1 - x0 + 1}x{s1 - s0 + 1} at {s0}-{s1}: {how or 'OUT OF REACH'}, over {under} "
                         f"{min(3 * DY, P.shelf_y(k) - P.LAKE_Y)} down; an unchecked sprint jump runs on to {r66:.1f}: brake in the air")
        out.append(f"drop {k + 1}, {P.shelf_y(k)} to {P.shelf_y(k + 1)}: " + "; ".join(parts))
    lap = {h: laps(h, R) for h in ("the falls", "the pools", "the bucket", "the bucket and the shafts")}
    out.append("a lap, top to lake, by habit: " + "; ".join(f"{k} {v:.0f} s" for k, v in lap.items()))
    return out


def geometry():
    bad = []
    taken = {}
    for k, d in enumerate(P.DROPS):
        if d.get("lake"):
            continue
        boxes = [(name, x0, x1, s0, s1, k + 1) for name, x0, x1, s0, s1 in P.pools(k)]
        if d.get("falls") is not None:
            fx = d["falls"]
            boxes.append(("the falls' basin", min(fx, fx + (1 if fx < 0 else -1) * 3), max(fx, fx + (1 if fx < 0 else -1) * 3), 1, 4, k + 1))
        if "shaft" in d:
            x0, x1, s0, s1 = d["shaft"]
            boxes.append(("the shaft", x0, x1, s0, s1, k + 1))
        for name, x0, x1, s0, s1, shelf in boxes:
            for x in range(x0, x1 + 1):
                for s in range(s0, s1 + 1):
                    z = P.z_of(k, s)
                    if not P.on_shelf(shelf, x, z):
                        bad.append(f"drop {k + 1}: {name} leaves shelf {shelf + 1} at ({x}, {z})")
                    if s < 1:
                        bad.append(f"drop {k + 1}: {name} under the edge above at ({x}, {z})")
                    key = (shelf, x, z)
                    if key in taken and taken[key] != (k, name):
                        bad.append(f"drop {k + 1}: {name} on top of {taken[key][1]} on shelf {shelf + 1} at ({x}, {z})")
                    taken[key] = (k, name)
    return bad


def main():
    out = check()
    bad = geometry()
    out.append(f"pools, holes and basins off their shelf, under an edge, or on top of another: {len(bad)}"
               + (" " + "; ".join(sorted(set(bad))[:6]) if bad else ""))
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main()
