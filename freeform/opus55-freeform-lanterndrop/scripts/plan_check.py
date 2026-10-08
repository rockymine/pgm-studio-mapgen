"""Check Lantern Drop's plan before anything is built: whether every jump can be made, what every landing costs, and
what a lap and every hill take.

1. THE LINKS. For every link from a piece to the next: the drop, the void to clear along the course and across it,
   the gentlest way of leaving the edge that clears it by the fall model, and what the landing does: nothing, hurts,
   or kills unless it ends in water. A link no way of leaving can clear is a fault.
2. THE PIECES. How long a player runs across each, and how wide it is: a narrow piece is where a punch puts a player
   in the void.
3. THE HILLS. For every hill: what lands a player on it, and the soonest a player can touch it, in seconds from the
   spawn, down the quickest line.
4. THE LAP. Seconds from the bell court to the barge down either way.
5. THE GEOMETRY. No two pieces overlap, and the right way is the left's mirror.

    python3 plan_check.py
"""
import math

import plan as P

HALF = 0.3
WAYS = ("step off", "run off", "sprint jump")


def gentlest(dy, dist):
    for how in WAYS:
        if P.fall(dy, how)[1] + HALF >= dist + 0.5:
            return how
    return None


def landing(a, b, dy):
    if P.damage(dy) < P.HEALTH:
        return f"{P.damage(dy)} damage" if P.damage(dy) else "no damage"
    ex = b[8]
    if ex.get("harbour"):
        return "kills on the deck: the bucket, or the harbour's water"
    if "water" in ex:
        return "kills: the cistern, or the bucket"
    return "kills: the bucket"


def check():
    out = []
    ps = P.pieces()
    out.append("link                                           drop  along across  way          landing")
    faults = 0
    best = {}                                                   # piece -> soonest arrival at its near edge
    start = [p for p in ps if p[8].get("spawn")][0]
    best[(start[0], start[9])] = 0.0
    for a, b in P.links():
        dy = a[7] - b[7]
        along, across = P.gap(a, b)
        dist = math.hypot(max(along, 0), across)
        how = gentlest(dy, dist) if dy >= 0 else None
        if how is None:
            faults += 1
        if a[9] != "right" and b[9] != "right":
            label = f"{a[1]} ({a[9]}) to {b[1]}"
            out.append(f"{label:<46} {dy:>4} {along:>5} {across:>6}  {how or 'NO WAY':<12} {landing(a, b, dy)}")
        if (a[0], a[9]) in best and how:
            run = (a[6] - a[5] + 1) / P.SPEED
            t = best[(a[0], a[9])] + run + P.fall(dy, how)[0] / 20 + (0.3 if P.damage(dy) >= P.HEALTH else 0)
            key = (b[0], b[9])
            best[key] = min(best.get(key, 1e9), t)
    out.append(f"links no way of leaving the edge can clear: {faults}")
    out.append(health_line(ps))
    out.append("piece                      run  wide  hill")
    for p in ps:
        if p[9] == "right":
            continue
        hill = ""
        if p[8].get("hill"):
            hill = f"{P.POINTS['last' if p[8].get('last') else 'hill']}/s, soonest {best.get((p[0], p[9]), float('nan')):.0f} s"
        out.append(f"{p[1]:<26} {p[6] - p[5] + 1:>3}  {p[4] - p[3] + 1:>4}  {hill}")
    last = [p for p in ps if p[8].get("last")][0]
    lap = best[(last[0], last[9])] + (last[6] - last[5] + 1) / P.SPEED
    out.append(f"a lap, the bell court to the barge's far end: {lap:.0f} s; hills: "
               f"{sum(1 for p in ps if p[8].get('hill'))}")
    return out


REGEN = 0.25                                                    # health a second, full and never hungry


def health_line(ps):
    """Down the left way without a bucket: health on landing, regenerating a point every four seconds, taking every
    cistern and the harbour's water where they are. Where it runs out, the bucket is not a choice."""
    line = [p for p in ps if p[9] in ("left", "middle")]
    hp, notes = float(P.HEALTH), []
    for a, b in zip(line, line[1:]):
        dy = a[7] - b[7]
        along, across = P.gap(a, b)
        how = gentlest(dy, math.hypot(max(along, 0), across))
        t = (a[6] - a[5] + 1) / P.SPEED + P.fall(dy, how)[0] / 20
        hp = min(P.HEALTH, hp + REGEN * t)
        water = "water" in b[8] or b[8].get("harbour")
        dmg = 0 if water else P.damage(dy)
        hp -= dmg
        notes.append(f"{b[1].replace('the ', '')} {max(hp, 0):.0f}" + (" DEAD" if hp <= 0 else ""))
        if hp <= 0:
            hp = float(P.HEALTH)                                   # a bucket there: the line goes on full
    return "without a bucket, health on landing: " + ", ".join(notes)


def geometry():
    ps = P.pieces()
    bad = []
    for i, a in enumerate(ps):
        for b in ps[i + 1:]:
            if a[3] <= b[4] and b[3] <= a[4] and a[5] <= b[6] and b[5] <= a[6]:
                bad.append(f"{a[1]} ({a[9]}) on {b[1]} ({b[9]})")
    return bad


def main():
    out = check()
    bad = geometry()
    out.append(f"pieces on top of each other: {len(bad)}" + (f" {bad[:4]}" if bad else "") + "; the right way is the "
               "left's mirror by construction")
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main()
