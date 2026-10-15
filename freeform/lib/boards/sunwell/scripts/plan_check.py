"""Check Sunwell's plan before anything is built: what every drop asks of a player, what every hill costs to take and
to keep, and whether the two sides are the same.

1. THE FALL. Minecraft's per-tick fall for a body that steps, runs or sprint-jumps off an edge: how far out each
   carries a player over a drop of twenty-two, and how long it takes. A player can land shorter than their way's
   reach by letting go, never further, so a target's near side decides the gentlest way that hits it.
2. THE DROPS. For every drop, each target on the left and the middle (the right is the left's mirror): how far it
   lies from the edge and which way reaches it. The falls, and the shafts.
3. THE HILLS. For every hill: what lands a player on it (a pool, the bucket, the islet), how far its nearest side
   is from a drop a punch could knock its holder down, and the soonest a player can touch it, in seconds from the
   spawn, by the quickest line of the bucket and the shafts.
4. THE LAP. Seconds from the top shelf to the lake by four habits: the falls every time, the pools every time, the
   bucket every time, and the bucket with every shaft taken.
5. THE GEOMETRY. Every pool, hole, basin and hill on its shelf, beyond the edge above it; no two pools, holes or
   basins on top of each other; and the right side the left's mirror.

    python3 plan_check.py
"""
import plan as P

DY = P.DROP
HALF = 0.3


def reach():
    return {how: P.fall(DY, how) for how in P.LEAVES}


def gentlest(s0, R):
    for how in ("step off", "run off", "sprint jump"):
        if R[how][1] + HALF >= s0:
            return how
    return None


def leave(habit, kind, s0, R, k):
    """What a gap costs a habit: (seconds in the air and landing, landing s, drops advanced), or None."""
    if kind == "the lake":
        return P.fall(DY, "step off")[0] / 20, 1.0, 1
    if habit == "the falls":
        return (1.0 + DY / P.FALLS_SPEED, 2.5, 1) if kind == "falls" else None
    if habit == "the pools":
        if kind != "pool":
            return None
        how = gentlest(s0, R)
        return (R[how][0] / 20 + 0.8, s0 + 1, 1) if how else None
    if kind == "falls":
        return None
    if kind == "shaft":
        if habit != "the bucket and the shafts":
            return None
        return P.fall(3 * DY, "sprint jump")[0] / 20 + 0.8, s0 + 1, 3
    how = gentlest(s0, R) or "sprint jump"
    return R[how][0] / 20 + 0.3, max(s0, R["step off"][1]), 1        # the bucket, at the target's near side


def lines(habit, R):
    """The quickest arrival at every drop's edge-leaving, by habit: {(drop, (x, s)): seconds}."""
    n = len(P.DROPS)
    best = {(0, (0.0, None)): 0.0}
    for k in range(n):
        for (kk, (xl, sl)), t0 in [it for it in best.items() if it[0][0] == k]:
            for kind, gx0, gx1, s0, sd in P.gaps(k):
                c = leave(habit, kind, s0, R, k)
                if c is None:
                    continue
                t, s_land, step = c
                xg = min(max(xl, gx0), gx1)
                forward = 4.0 if sl is None else sl + 2 * P.EDGE
                v = t0 + (abs(xl - xg) + forward) / P.SPEED + t
                key = (min(k + step, n), (xg, s_land))
                if v < best.get(key, 1e9):
                    best[key] = v
    return best


def hill_times(R):
    """The soonest each hill is touched, by the bucket and the shafts: leave the edge over it and land in it."""
    best = lines("the bucket and the shafts", R)
    out = {}
    for k in range(len(P.DROPS)):
        starts = [(land, t) for (kk, land), t in best.items() if kk == k]
        for name, x0, x1, s0, s1, sd in P.hills(k):
            soonest = 1e9
            for (xl, sl), t0 in starts:
                xg = min(max(xl, x0), x1)
                forward = 4.0 if sl is None else sl + 2 * P.EDGE
                how = gentlest(s0, R) or "sprint jump"
                soonest = min(soonest, t0 + (abs(xl - xg) + forward) / P.SPEED + R[how][0] / 20 + 0.3)
            out[(k, name, sd)] = soonest
    return out


def lands_by(k, x0, x1, s0, s1, R):
    if P.DROPS[k].get("lake"):
        return "the bucket (the islet is two over the water)"
    for name, p0, p1, q0, q1, sd in P.pools(k):
        if p0 <= x1 and x0 <= p1 and q0 <= s1 and s0 <= q1:
            return f"{name} by a {gentlest(q0, R) or 'NOTHING'}"
    return f"the bucket, a {gentlest(s0, R)}"


def edge_dist(k, x0, x1, s0, s1):
    """From a hill on shelf k + 1 to the nearest place its holder could be knocked down: the shelf's own edge (the
    next drop), or a shaft through it."""
    d = s0 + 2 * P.EDGE
    for name, a0, a1, b0, b1, sd in P.shafts(k):
        dx = max(a0 - x1, x0 - a1, 0)
        ds = max(b0 - s1, s0 - b1, 0)
        d = min(d, dx + ds)
    return d


def check():
    out = []
    R = reach()
    out.append("the fall of 22: " + "; ".join(f"{how}: {R[how][1]:.1f} out, {R[how][0] / 20:.2f} s" for how in P.LEAVES)
               + f"; unbroken it does {P.damage(DY)} of {P.HEALTH} health")
    for k, d in enumerate(P.DROPS):
        if d.get("lake"):
            out.append(f"drop {k + 1}, {P.shelf_y(k)} to the lake at {P.LAKE_Y}: the lake anywhere; the islet, "
                       f"{P.shelf_y(k) - P.ISLET['y']} down, only by the bucket")
            continue
        parts = []
        for name, x0, x1, s0, s1, sd in P.pools(k):
            if sd == "right":
                continue
            parts.append(f"{sd} {name} {x1 - x0 + 1}x{s1 - s0 + 1} at {s0}-{s1}: {gentlest(s0, R) or 'OUT OF REACH'}")
        for name, x0, x1, s0, s1, sd in P.shafts(k):
            if sd == "right":
                continue
            under = "the lake" if k + 3 >= len(P.DROPS) else "a pool two shelves down"
            parts.append(f"{sd} shaft at {s0}-{s1}: {gentlest(s0, R)}, over {under}")
        parts.append(f"the falls both sides, {DY / P.FALLS_SPEED:.1f} s")
        out.append(f"drop {k + 1}, {P.shelf_y(k)} to {P.shelf_y(k + 1)}: " + "; ".join(parts))
    out.append("hill                                   lands by                                  to a drop  soonest")
    times = hill_times(R)
    for k in range(len(P.DROPS)):
        for name, x0, x1, s0, s1, sd in P.hills(k):
            if sd == "right":
                continue
            pts = P.POINTS["last" if P.DROPS[k].get("lake") else "hill"]
            label = f"{k + 1}. {sd} {name} ({pts}/s)"
            out.append(f"{label:<38} {lands_by(k, x0, x1, s0, s1, R):<42} {edge_dist(k, x0, x1, s0, s1):>5}  {times[(k, name, sd)]:6.0f} s")
    laps = {h: min(v for (k, l), v in lines(h, R).items() if k == len(P.DROPS))
            for h in ("the falls", "the pools", "the bucket", "the bucket and the shafts")}
    out.append("a lap, top to lake, by habit: " + "; ".join(f"{h} {v:.0f} s" for h, v in laps.items()))
    return out


def geometry():
    bad = []
    taken = {}
    for k, d in enumerate(P.DROPS):
        if d.get("lake"):
            continue
        solid = [(n, a, b, c, e, sd, k + 1) for n, a, b, c, e, sd in P.pools(k) + P.shafts(k) + P.falls(k)]
        for name, x0, x1, s0, s1, sd, shelf in solid + [(n, a, b, c, e, sd, k + 1) for n, a, b, c, e, sd in P.hills(k)]:
            for x in range(x0, x1 + 1):
                for s in range(s0, s1 + 1):
                    z = P.z_of(k, s)
                    if not P.on_shelf(shelf, x, z):
                        bad.append(f"drop {k + 1}: {sd} {name} leaves its shelf at ({x}, {z})")
                    if s < 1:
                        bad.append(f"drop {k + 1}: {sd} {name} under the edge above")
        for name, x0, x1, s0, s1, sd, shelf in solid:
            for x in range(x0, x1 + 1):
                for s in range(s0, s1 + 1):
                    key = (shelf, x, P.z_of(k, s))
                    if key in taken and taken[key] != (name, sd):
                        bad.append(f"drop {k + 1}: {sd} {name} on top of {taken[key][1]} {taken[key][0]}")
                    taken[key] = (name, sd)
    mirror_bad = 0
    for k in range(len(P.DROPS)):
        for getter in (P.pools, P.shafts, P.falls, P.hills):
            items = getter(k)
            left = sorted((n, -b, -a, c, e) for n, a, b, c, e, sd in items if sd == "left")
            right = sorted((n, a, b, c, e) for n, a, b, c, e, sd in items if sd == "right")
            mirror_bad += left != right
    return bad, mirror_bad


def main():
    out = check()
    bad, mirror_bad = geometry()
    out.append(f"pools, holes, basins and hills off their shelf, under an edge, or on top of another: {len(bad)}"
               + (" " + "; ".join(sorted(set(bad))[:5]) if bad else "")
               + f"; drops whose right side is not the left's mirror: {mirror_bad}")
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main()
