"""Check Islets' plan: each team's walk to the hill (the same for both, or the board is unfair), and every jump."""
from plan import WALK, build
from pgmvox import plangraph as G

R = build()
E = G.graph(R, WALK)
J = G.jumps(R, WALK)
hill = [(x, z) for x in range(-2, 2) for z in range(-4, 4)]
a = G.arrivals(E, {"red": [(-24, 0)], "blue": [(23, -1)]}, {"the hill": hill})
print(f"to the hill: red {a['the hill']['red']:.1f}, blue {a['the hill']['blue']:.1f}")
print(f"jumps the plan allows: {len(J)}, the widest {max((g for *_, g in J), default=0)}")
