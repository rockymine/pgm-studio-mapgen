"""Check Spark's plan before anything is built: where a hit kills at each knockback level, and that nothing on the
spark is a place to hide.

1. THE REACH. For every knockback level, how far a plain hit carries a player, by the model.
2. THE KILLING GROUND. How far the floor lies from the water, by the shortest straight push a crate does not stop;
   and for every level, the share of the floor from which a plain hit and a sprinting hit can put a player in the
   water, and of the directions a hit could come from, the share that would. The model is an upper bound, so the
   first share fills early; the second says how much an attacker must be on the right side, and should climb from
   a few in ten to nearly all as the level climbs a step a minute.
3. THE CRATES. None taller than two; no floor cell walled on three sides by crates (a pocket to hide in); and how
   far the floor lies from something to brace against.

    python3 plan_check.py
"""
import math

import plan as P

R = 50


def floor_cells():
    return [(x, z) for x in range(-R, R + 1) for z in range(-R, R + 1) if P.is_floor(x, z)]


def void_cells():
    return [(x, z) for x in range(-R, R + 1) for z in range(-R, R + 1) if not P.is_floor(x, z)]


def to_water(x, z):
    """The shortest straight push from a cell that ends over the void before a crate stops it."""
    best = 99.0
    for i in range(48):
        a = i * math.pi / 24
        dx, dz = math.cos(a), math.sin(a)
        t = 0.5
        while t < best:
            px, pz = int(round(x + dx * t)), int(round(z + dz * t))
            if P.crate_at(px, pz):
                break
            if not P.is_floor(px, pz):
                best = t
                break
            t += 0.5
    return best


def killing(cells, level, sprint=True):
    """For every cell, the share of the 32 directions a hit could push a player in that ends over the void before
    the push runs out or a crate stops it; and the share of cells with at least one such direction."""
    reach = {s: P.knock(level, s, sprint) for s in P.SLIP}
    dirs = [(math.cos(a), math.sin(a)) for a in [i * math.pi / 16 for i in range(32)]]
    shares, some = [], 0
    for x, z in cells:
        r = reach[P.surface(x, z)]
        n = 0
        for dx, dz in dirs:
            t = 0.5
            while t <= r:
                px, pz = int(round(x + dx * t)), int(round(z + dz * t))
                if P.crate_at(px, pz):
                    break
                if not P.is_floor(px, pz):
                    n += 1
                    break
                t += 0.5
        shares.append(n / len(dirs))
        some += n > 0
    return sum(shares) / len(shares), some / len(cells)


def main():
    out = []
    cells = [c for c in floor_cells() if not P.crate_at(*c)]
    holes = sum(1 for x in range(-R, R + 1) for z in range(-R, R + 1) if P.on_spark(x, z) and not P.is_floor(x, z))
    hub = sum(1 for x, z in cells if math.hypot(x, z) <= P.HUB_R)
    span = max(math.hypot(x, z) for x, z in cells)
    out.append(f"the floor: {len(cells)} blocks to stand on, {hub} of them in the hub, the rest on {len(P.RAYS)} rays; "
               f"{holes} blocks of the hub cut out for its eye; {len(P.CRATES)} blocks to brace against; "
               f"tip to tip {2 * span:.0f} across at most")
    widths = []
    for a, length, w0, w1 in P.RAYS:
        widths.append(f"{length}")
    out.append("the rays' lengths from the centre: " + ", ".join(widths))
    d = sorted(to_water(x, z) for x, z in cells)
    q = lambda f: d[min(len(d) - 1, int(f * len(d)))]
    out.append(f"how far a push must carry a player off the spark: a quarter of the floor within {q(0.25):.1f}, half "
               f"within {q(0.5):.1f}, nine tenths within {q(0.9):.1f}, the furthest {d[-1]:.1f}")
    out.append("knockback  reach   a plain hit: the floor it can kill from, the directions that kill"
               "   a sprinting hit: the same")
    for t, level in P.LEVELS:
        a0, s0 = killing(cells, level, sprint=False)
        a1, s1 = killing(cells, level)
        out.append(f"{level} (from {t // 60}m)  {P.knock(level, 'clay', False):5.1f}"
                   f"        {s0:6.0%} {a0:6.0%}{'':42}{s1:6.0%} {a1:6.0%}")
    tall = [c for c in P.CRATES if c[4] > 2]
    pockets = []
    for x, z in cells:
        walls = sum(1 for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)) if P.crate_at(x + dx, z + dz))
        if walls >= 3:
            pockets.append((x, z))
    near = []
    for x, z in cells:
        d = min(math.hypot(x - (c[0] + c[1]) / 2, z - (c[2] + c[3]) / 2) for c in P.CRATES)
        near.append(d)
    near.sort()
    out.append(f"crates taller than two: {len(tall)}; floor cells walled on three sides by crates: {len(pockets)}; "
               f"from a crate, half the floor lies within {near[len(near) // 2]:.0f}, all of it within {near[-1]:.0f}")
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main()
