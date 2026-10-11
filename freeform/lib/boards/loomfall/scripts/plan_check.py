"""Check Loomfall's plan before anything is built: what a player falling from every cell lands on, how long each carpet
lasts, and where a carpet narrows to a trap.

1. THE FALLS. For every carpet, its cells by what lies under them: the next carpet, a carpet further down (a
   shortcut to fresh wool), or nothing (death). The holes the same way.
2. THE CARPETS. Each carpet's wool, how far it lies over the next, and how long it would last with ten, twenty and
   thirty players on it, each running and trampling seven cells a second: a floor's life, not a match's.
3. THE NARROWS. Cells of wool with at most one neighbour of wool: a sliver a running player is trapped on.

    python3 plan_check.py
"""
import plan as P


def main():
    out = []
    total = 0
    for k, c in enumerate(P.CARPETS):
        name, x0, x1, z0, z1, y, holes = c
        cs = P.cells(c)
        total += len(cs)
        lands = {}
        for x, z in cs:
            j = P.below(k, x, z)
            lands[j] = lands.get(j, 0) + 1
        nxt = P.CARPETS[k + 1][5] if k + 1 < len(P.CARPETS) else P.KILL_Y
        parts = []
        for j in sorted(lands, key=lambda j: (j is None, j)):
            label = "nothing: out" if j is None else ("the next" if j == k + 1 else f"{P.CARPETS[j][0]}, {j - k} down")
            parts.append(f"{label} {lands[j] / len(cs):.0%}")
        hole_under = []
        for a, b, c0, d in holes:
            j = P.below(k, a, c0)
            hole_under.append("over nothing" if j is None else f"over {P.CARPETS[j][0]}")
        life = ", ".join(f"{n}: {len(cs) / (n * P.RUN):.0f} s" for n in (10, 20, 30))
        narrows = sum(1 for x, zz in cs if sum((x + dx, zz + dz) in cs for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))) <= 1)
        out.append(f"{k + 1}. {name}, {x1 - x0 + 1} x {z1 - z0 + 1} at {y}, {len(cs)} wool, {y - nxt} over the "
                   f"{'next' if k + 1 < len(P.CARPETS) else 'kill height'}")
        out.append("   a fall lands on: " + "; ".join(parts))
        if holes:
            out.append(f"   {len(holes)} moth holes: " + ", ".join(hole_under))
        out.append(f"   it lasts, with players: {life}; slivers: {narrows}")
    out.append(f"wool in all: {total}; with twenty players, a floor's worth of trampling every {total / (20 * P.RUN):.0f} s")
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main()
